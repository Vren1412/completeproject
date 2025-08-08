import streamlit as st
from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime
from PIL import Image


st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .main {
        background-image: url("https://images.unsplash.com/photo-1699891730676-037bed3c1bed");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }
    div.stButton > button {
        background-color: #0e1117;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    </style>
""", unsafe_allow_html=True)


IMAGE_DIR = "uploaded_images"
DB_FILE = "image_predictions.csv"
os.makedirs(IMAGE_DIR, exist_ok=True)


def admin_login():
    st.sidebar.title("🔐 Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    return username == "admin" and password == "admin123"

@st.cache_resource
def load_model():
    rf = Roboflow(api_key="cto2SFwA0t7Z5g5qqOQi")
    project = rf.workspace().project("smart-waste-management-h5yif-mwcpw")
    return project.version(1).model

model = load_model()

def process_image(image_path):
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

    return annotated_image, labels

def save_image_and_log(uploaded_file, labels):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(IMAGE_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    new_data = {
        "filename": uploaded_file.name,
        "timestamp": timestamp,
        "labels": ', '.join(labels)
    }

    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        df = pd.DataFrame([new_data])

    df.to_csv(DB_FILE, index=False)

if admin_login():
    st.title("🌍 Smart Waste Management Admin Panel")

    tab1, tab2 = st.tabs(["📷 Predict Waste", "📊 View Uploaded Images"])

    with tab1:
        uploaded_file = st.file_uploader("Upload an image for prediction", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            img_path = os.path.join(IMAGE_DIR, uploaded_file.name)
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            if st.button("🔍 Predict Waste"):
                annotated_image, labels = process_image(img_path)
                st.image(annotated_image, caption="Detected Waste", use_column_width=True)
                save_image_and_log(uploaded_file, labels)
                st.success(f"Prediction complete: {', '.join(set(labels))}")

    with tab2:
        if os.path.exists(DB_FILE):
            df = pd.read_csv(DB_FILE)
            st.dataframe(df)
        else:
            st.warning("No images uploaded yet.")

else:
    st.warning("Please login as admin to access this application.")

