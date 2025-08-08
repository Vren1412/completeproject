import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
df = pd.read_csv("healthcare_dataset.csv")

# Separate features and label
X = df.drop("target", axis=1)
y = df["target"]

# Encode the labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reshape input for CNN (samples, time steps, features)
X_cnn = np.expand_dims(X_scaled, axis=2)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_cnn, y_categorical, test_size=0.2, random_state=42)

# Build CNN model
model = Sequential([
    Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X_cnn.shape[1], 1)),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(y_categorical.shape[1], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Create model directory if it doesn't exist
os.makedirs("model", exist_ok=True)

# Save model
model.save("model/cnn_model.h5")
print("✅ Model trained and saved to model/cnn_model.h5")
