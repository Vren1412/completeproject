import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import os
import subprocess

# Optional: Run preprocessing and model if needed here
print("Launching the UI interface...")

# This will open the Streamlit app
subprocess.run(["streamlit", "run", "ui/app.py"])

# Load dataset
df = pd.read_csv("healthcare_dataset.csv")

# Ensure correct column names
print("Columns:", df.columns.tolist())

# Drop irrelevant column if exists (adjust according to actual column)
if 'ACTUAL_COLUMN_NAME' in df.columns:
    df = df.drop(['ACTUAL_COLUMN_NAME'], axis=1)

# Assume 'target' is the label column
X = df.drop(['target'], axis=1)
y = df['target']

# Preprocess
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42)

# Build CNN-like model
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(X.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Binary classification

model.compile(optimizer='adam',
              loss='binary_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(X_train, y_train, epochs=20,
                    batch_size=32, validation_split=0.2)

# Save model
model.save('model/cnn_model.h5')

# Evaluate
loss, acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {acc:.2f}")

# Plot accuracy
plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title("Model Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)
plt.savefig("results/accuracy_plot.png")


#"C:\Users\ASUS\AppData\Local\Programs\Python\Python37\python.exe" main.py
