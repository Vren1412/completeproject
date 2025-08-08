from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = "3.jpg"


rf = Roboflow(api_key="cto2SFwA0t7Z5g5qqOQi")
project = rf.workspace().project("smart-waste-management-h5yif-mwcpw")
model = project.version(1).model

result = model.predict(image_path, confidence=40, overlap=30).json()

predictions = result["predictions"]

unique_classes = set(pred["class"] for pred in predictions)
print("Unique Detected Classes:")
for cls in unique_classes:
    print(f"- {cls}")


xyxy = []
confidences = []
class_ids = []
labels = []

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

plt.figure(figsize=(10, 10))
plt.imshow(annotated_image)
plt.axis('off')
plt.title("Annotated Image")
plt.show()

cv2.imwrite("output2.jpg", cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
print("Annotated image saved as output.jpg")
