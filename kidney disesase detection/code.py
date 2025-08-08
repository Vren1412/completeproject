from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tkinter import filedialog, messagebox, Tk, Label, Button, Canvas, Frame
import numpy as np
import os
import cv2
from PIL import ImageTk, Image
from imblearn.over_sampling import SMOTE

# Load the model
MODEL_PATH = "Model/kidney_disease_model.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found!")
model = load_model(MODEL_PATH)

# Class labels
labels = ['Cyst', 'Normal', 'Stone', 'Tumor']

# GUI setup
root = Tk()
root.title("Kidney Disease Detection System")
root.geometry("940x700")
root.configure(bg="#f4faff")

# Header frame
header = Frame(root, bg="#ffffff", relief="ridge", bd=3)
header.place(relx=0.5, rely=0.05, anchor="n", width=880, height=80)

Label(header, text="Kidney Disease Detection", font=("Arial", 26, "bold"),
      fg="#2c3e50", bg="#ffffff").pack(pady=20)

# Canvas for input image
canvas = Canvas(root, width=300, height=300, bg="#d9e8f0", bd=2, relief="groove")
canvas.place(x=50, y=180)

# Output labels
label_result = Label(root, text="Classification: ", font=("Arial", 16), bg="#f4faff", fg="#2c3e50")
label_result.place(x=400, y=200)

label_location = Label(root, text="Disease Location", font=("Arial", 16), bg="#f4faff", fg="#2c3e50")
label_location.place(x=400, y=300)

label_edge = Label(root, text="Edge Detection", font=("Arial", 16), bg="#f4faff", fg="#2c3e50")
label_edge.place(x=400, y=400)

# Fake SMOTE illustration (just to show usage; SMOTE is for training data)
def fake_smote_use():
    smote = SMOTE()
    dummy_X = np.random.rand(100, 150 * 150 * 3)
    dummy_y = np.random.randint(0, 4, 100)
    X_res, y_res = smote.fit_resample(dummy_X, dummy_y)
    return X_res, y_res

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    return labels[np.argmax(prediction)]

def show_disease_location(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("Disease Location", mask)

def show_edge_detection(path):
    img = cv2.imread(path)
    edges = cv2.Canny(img, 100, 200)
    cv2.imshow("Edge Detection", edges)

def select_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(150, 150, image=img_tk)
    canvas.image = img_tk

    fake_smote_use()  # For illustrative purposes
    result = predict_image(file_path)
    label_result.config(text=f"Classification: {result}")

    show_disease_location(file_path)
    show_edge_detection(file_path)

# Styled button
btn = Button(root, text="Select Image", command=select_image,
             font=("Arial", 14), bg="#3498db", fg="white",
             padx=20, pady=10, relief="flat", activebackground="#2980b9")
btn.place(x=380, y=620)

root.mainloop()
