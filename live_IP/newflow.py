# pip install roboflow==1.1.63
# pip install supervision==0.25.1

from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np
import matplotlib.pyplot as plt

imgpath = "plastic_024.jpg"

# Initialize Roboflow
RF = Roboflow(api_key="Ty0EsIVI1DqCsrNgcCHb")  # Replace with your real API key
Project = RF.workspace().project("smart-waste-management-h5yif-mwcpw")
model = Project.version(1).model

# Get predictions
results = model.predict(imgpath, confidence=40, overlap=30).json()
predictions = results["predictions"]

# Get unique classes
unique_classes = set(pred["class"] for pred in predictions)
print("Unique_classes:", unique_classes)

for cls in unique_classes:
    print(f"- {cls}")

# Prepare detection data
xyxy = []
confidence = []
class_ids = []
labels = []

for pred in predictions:
    x1 = int(pred["x"] - pred["width"] / 2)
    y1 = int(pred["y"] - pred["height"] / 2)
    x2 = int(pred["x"] + pred["width"] / 2)
    y2 = int(pred["y"] + pred["height"] / 2)

    xyxy.append([x1, y1, x2, y2])
    confidence.append(pred["confidence"])
    class_ids.append(pred["class_id"])  # Use 'class_id', not 'class_ids'
    labels.append(pred["class"])

# Create detections object
detections = sv.Detections(
    xyxy=np.array(xyxy),
    confidence=np.array(confidence),
    class_id=np.array(class_ids),
)

# Read and convert image
image = cv2.imread(imgpath)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Annotate
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
annotated_image = box_annotator.annotate(scene=image_rgb, detections=detections)
annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)

# Show image using matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(annotated_image)
plt.axis("off")
plt.title("Annotated Image")
plt.show()

# Save image
cv2.imwrite("output.jpg", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
print("Annotated image saved as output.jpg")
