import streamlit as st
import cv2
import numpy as np
import supervision as sv
from roboflow import Roboflow
import tempfile
from PIL import Image

st.set_page_config(page_title="Smart Waste Detection", layout="centered")
st.title("♻️ Smart Waste Detection using Roboflow")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display original image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to temporary path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        image_path = tmp_file.name
        image.save(image_path)

    # Load model
    rf = Roboflow(api_key="cto2SFwA0t7Z5g5qqOQi")
    project = rf.workspace("sudha-tyxpp").project("smart-waste-management-h5yif-mwcpw")
    model = project.version(1).model

    # Run prediction
    with st.spinner("Running detection..."):
        result = model.predict(image_path, confidence=40, overlap=30).json()
        predictions = result["predictions"]

        if not predictions:
            st.warning("No objects detected.")
        else:
            unique_classes = set(pred["class"] for pred in predictions)
            st.subheader("✅ Detected Classes")
            for cls in unique_classes:
                st.markdown(f"- {cls}")

            # Prepare detection arrays
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

            # Load and annotate image
            image_cv = cv2.imread(image_path)
            image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)

            box_annotator = sv.BoxAnnotator()
            label_annotator = sv.LabelAnnotator()

            annotated = box_annotator.annotate(scene=image_rgb.copy(), detections=detections)
            annotated = label_annotator.annotate(scene=annotated, detections=detections, labels=labels)

            # Show result
            st.subheader("📸 Annotated Image")
            st.image(annotated, use_column_width=True)

            # Save
            output_path = "output.jpg"
            cv2.imwrite(output_path, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
            st.success("Annotated image saved as output.jpg")

            with open(output_path, "rb") as f:
                st.download_button("📥 Download Annotated Image", f, file_name="output.jpg", mime="image/jpeg")
