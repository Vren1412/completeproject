import streamlit as st
from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime
import base64

st.set_page_config(layout="wide")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if os.path.exists("bg1.jpg"):
    bg_img = get_base64("bg1.jpg")
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_img}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stButton > button {{
            background-color: #0e1117;
            color: white;
            border-radius: 8px;
        }}
        </style>
    """, unsafe_allow_html=True)

IMAGE_DIR = "uploaded_images"
ANNOTATED_DIR = "annotated_images"
DB_FILE = "image_predictions.csv"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(ANNOTATED_DIR, exist_ok=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def admin_login():
    with st.sidebar:
        st.title("🔐 Admin Login")
        if not st.session_state.logged_in:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if username == "Sudha" and password == "Sudha":
                    st.session_state.logged_in = True
                    st.success("Login successful")
                else:
                    st.error("Invalid credentials")
        else:
            st.success("Logged in as admin ✅")
            if st.button("Logout"):
                st.session_state.logged_in = False

admin_login()

@st.cache_resource
def load_model():
    rf = Roboflow(api_key="cto2SFwA0t7Z5g5qqOQi")
    project = rf.workspace().project("smart-waste-management-h5yif-mwcpw")
    return project.version(1).model

model = load_model()

def process_image(image_path, save_name):
    result = model.predict(image_path, confidence=40, overlap=30).json()
    predictions = result["predictions"]

    xyxy, confidences, class_ids, labels = [], [], [], []

    for pred in predictions:
        x1 = int(pred["x"] - pred["width"] / 2)
        y1 = int(pred["y"] - pred["height"] / 2)
        x2 = int(pred["x"] + pred["width"] / 2)
        y2 = int(pred["y"] + pred["height"] / 2)

        xyxy.append([x1, y1, x2, y2])
        confidences.append(pred["confidence"])
        class_ids.append(pred.get("class_id", 0))
        labels.append(pred["class"])

    detections = sv.Detections(
        xyxy=np.array(xyxy),
        confidence=np.array(confidences),
        class_id=np.array(class_ids)
    )

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    annotated_image = box_annotator.annotate(scene=image_rgb.copy(), detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)
    save_path = os.path.join(ANNOTATED_DIR, save_name)
    cv2.imwrite(save_path, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

    return annotated_image, labels, save_path


def save_log(filename, labels, annotated_img_path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = {
        "filename": filename,
        "timestamp": timestamp,
        "labels": ', '.join(labels),
        "annotated_path": annotated_img_path
    }

    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        df = pd.DataFrame([new_data])

    df.to_csv(DB_FILE, index=False)

if st.session_state.logged_in:
    st.title("🌍 Smart Waste Management Admin Panel")

    tab1, tab2 = st.tabs(["📷 Predict Waste", "🖼 View All Predictions"])

    with tab1:
        uploaded_file = st.file_uploader("Upload an image for prediction", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            save_path = os.path.join(IMAGE_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            if st.button("🔍 Predict Waste"):
                annotated_image, labels, annotated_path = process_image(save_path, uploaded_file.name)
                st.image(annotated_image, caption="Detected Waste", use_column_width=True)
                save_log(uploaded_file.name, labels, annotated_path)
                st.success(f"Prediction complete: {', '.join(set(labels))}")

    with tab2:
        if os.path.exists(DB_FILE):
            df = pd.read_csv(DB_FILE)
            st.subheader("📑 Prediction History")
            for _, row in df.iterrows():
                with st.container():
                    cols = st.columns([1, 3])
                    if os.path.exists(row['annotated_path']):
                        cols[0].image(row['annotated_path'], use_column_width=True)
                    cols[1].markdown(f"""
                        **Filename**: `{row['filename']}`  
                        **Timestamp**: {row['timestamp']}  
                        **Detected**: `{row['labels']}`  
                    """)
        else:
            st.warning("No predictions yet. Upload images to get started.")
else:
    st.info("👈 Please login from sidebar to use the app.")

