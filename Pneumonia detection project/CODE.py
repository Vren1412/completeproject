from tkinter import messagebox, filedialog, Text, Frame, Label, Button, Tk, END, BOTH, WORD, GROOVE
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.layers import MaxPooling2D, Dense, Flatten, Convolution2D
from keras.models import Sequential, model_from_json
import pickle

main = Tk()
main.title("Identifying Pneumonia using X-Ray Images")
main.geometry("1300x700")
main.configure(bg='#f0f4f8')

filename = ""
accuracy = 0
X = []
Y = []
classifier = None
disease = ['No Pneumonia Detected', 'Pneumonia Detected']

# Load segmentation model
try:
    with open('Model/segmented_model.json', "r") as json_file:
        loaded_model_json = json_file.read()
        segmented_model = model_from_json(loaded_model_json)
    segmented_model.load_weights("Model/segmented_weights.h5")
    segmented_model._make_predict_function()
except Exception as e:
    messagebox.showerror("Model Load Error", str(e))

def PneumoniaSegmentation(filename):
    try:
        img = cv2.imread(filename, 0)
        img = cv2.resize(img, (64, 64))
        img = img.reshape(1, 64, 64, 1)
        img = (img - 127.0) / 127.0
        preds = segmented_model.predict(img)[0]
        segmented_image = cv2.resize(preds, (300, 300))
        return segmented_image * 255
    except Exception as e:
        messagebox.showerror("Segmentation Error", str(e))
        return np.zeros((300, 300))

def uploadDataset():
    global filename
    try:
        filename = filedialog.askdirectory(initialdir=".")
        text.delete('1.0', END)
        text.insert(END, filename + " loaded\n")
    except Exception as e:
        messagebox.showerror("Upload Error", str(e))

def datasetPreprocessing():
    global X, Y
    try:
        X.clear()
        Y.clear()
        if os.path.exists('Model/segmented_pneumonia_data.txt.npy'):
            X = np.load('Model/segmented_pneumonia_data.txt.npy')
            Y = np.load('Model/segmented_pneumonia_label.txt.npy')
        else:
            for label, subdir in enumerate(["no", "yes"]):
                path = os.path.join(filename, subdir)
                for img_name in os.listdir(path):
                    img = cv2.imread(os.path.join(path, img_name), 0)
                    if img is not None:
                        img = cv2.resize(img, (128, 128))
                        img = img.reshape(128, 128, 1)
                        X.append(img)
                        Y.append(label)
            X = np.asarray(X)
            Y = np.asarray(Y)
            np.save("Model/segmented_pneumonia_data.txt", X)
            np.save("Model/segmented_pneumonia_label.txt", Y)

        text.insert(END, f"Total number of images: {len(X)}\n")
        text.insert(END, f"Total number of classes: {len(set(Y))}\n")
        text.insert(END, f"Classes: {disease}\n")
    except Exception as e:
        messagebox.showerror("Preprocessing Error", str(e))

def PneumoniaDetectionModel():
    global accuracy, classifier
    try:
        YY = to_categorical(Y)
        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)
        x_train = X[indices]
        y_train = YY[indices]

        if os.path.exists('Model/model.json'):
            with open('Model/model.json', "r") as json_file:
                loaded_model_json = json_file.read()
                classifier = model_from_json(loaded_model_json)
            classifier.load_weights("Model/model_weights.h5")
            classifier._make_predict_function()
        else:
            X_train, X_test, y_train_split, y_test = train_test_split(x_train, y_train, test_size=0.2)
            classifier = Sequential()
            classifier.add(Convolution2D(32, 3, 3, input_shape=(128, 128, 1), activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Convolution2D(32, 3, 3, activation='relu'))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Flatten())
            classifier.add(Dense(128, activation='relu'))
            classifier.add(Dense(2, activation='softmax'))
            classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            hist = classifier.fit(x_train, y_train, batch_size=16, epochs=10, validation_split=0.2)
            classifier.save_weights('Model/model_weights.h5')
            with open("Model/model.json", "w") as json_file:
                json_file.write(classifier.to_json())
            with open('Model/history.pckl', 'wb') as f:
                pickle.dump(hist.history, f)

        with open('Model/history.pckl', 'rb') as f:
            data = pickle.load(f)
        accuracy = data['accuracy'][-1] * 100
        text.insert(END, f"CNN model trained with accuracy: {accuracy:.2f}%\n")
    except Exception as e:
        messagebox.showerror("Model Training Error", str(e))

def PneumoniaClassification():
    global classifier
    try:
        file = filedialog.askopenfilename()
        img = cv2.imread(file, 0)
        img = cv2.resize(img, (128, 128))
        img = img.reshape(1, 128, 128, 1)
        prediction = classifier.predict(img)
        cls = np.argmax(prediction)
        result = f"Classification Result: {disease[cls]}"
        text.insert(END, result + "\n")

        # Show result image in resizable and movable window
        img_display = cv2.imread(file)
        img_display = cv2.resize(img_display, (600, 400))
        cv2.putText(img_display, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow(result, img_display)

        if cls == 1:
            segmented_image = PneumoniaSegmentation(file)
            seg_display = cv2.resize(segmented_image.astype(np.uint8), (400, 300))
            cv2.imshow("Segmented Pneumonia Region", seg_display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        messagebox.showerror("Classification Error", str(e))

def graph():
    try:
        with open('Model/history.pckl', 'rb') as f:
            data = pickle.load(f)
        accuracy = data['accuracy']
        loss = data['loss']
        plt.plot(accuracy, label="Accuracy", color='green')
        plt.plot(loss, label="Loss", color='red')
        plt.title("Training Accuracy & Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Graph Error", str(e))

# GUI Layout
font_title = ('Segoe UI', 20, 'bold')
font_button = ('Segoe UI', 12, 'bold')
font_text = ('Consolas', 11)

Label(main, text='Identifying Pneumonia using X-Ray Images',
      bg='#2c3e50', fg='white', font=font_title, height=2, width=100, pady=10).pack(pady=(10, 20))

# Text Frame
text_frame = Frame(main, bg='white', bd=2, relief=GROOVE)
text_frame.place(x=50, y=100, width=1200, height=350)

text = Text(text_frame, font=font_text, wrap=WORD, bg='#fdfefe', fg='black')
text.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Buttons
button_frame = Frame(main, bg='#f0f4f8')
button_frame.place(x=50, y=470)

def styled_btn(master, txt, cmd, r, c):
    Button(master, text=txt, command=cmd, font=font_button,
           bg='#34495e', fg='white', activebackground='#2c3e50',
           padx=12, pady=6, bd=0).grid(row=r, column=c, padx=12, pady=10)

styled_btn(button_frame, "Upload Pneumonia X-Ray Images Dataset", uploadDataset, 0, 0)
styled_btn(button_frame, "Dataset Preprocessing & Features Extraction", datasetPreprocessing, 0, 1)
styled_btn(button_frame, "Trained CNN Pneumonia Detection Model", PneumoniaDetectionModel, 0, 2)
styled_btn(button_frame, "Pneumonia Segmentation & Classification", PneumoniaClassification, 1, 0)
styled_btn(button_frame, "Training Accuracy Graph", graph, 1, 1)

main.mainloop()
