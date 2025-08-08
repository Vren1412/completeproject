import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load model
model = tf.keras.models.load_model('../model/cnn_model.h5')

# Load sample data structure
df = pd.read_csv('../healthcare_dataset.csv')
features = df.drop(columns=['target'])

# UI Title
st.set_page_config(page_title="Healthcare CNN Predictor", layout="centered")
st.title("🧠 Healthcare Risk Prediction with CNN")
st.markdown("Upload healthcare data to predict outcomes using a CNN model.")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    user_df = pd.read_csv(uploaded_file)

    # Preprocess
    try:
        X_user = user_df[features.columns]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_user)

        # Prediction
        preds = model.predict(X_scaled)
        preds_class = (preds > 0.5).astype(int)

        user_df["Prediction"] = preds_class
        st.success("✅ Prediction Completed")

        # Show results
        st.dataframe(user_df)

        # Download
        csv = user_df.to_csv(index=False).encode()
        st.download_button("Download Results", csv,
                           "predictions.csv", "text/csv")

        # Show accuracy graph
        st.subheader("📊 Model Accuracy Plot")
        st.image("../results/accuracy_plot.png", use_column_width=True)

    except Exception as e:
        st.error(f"Error processing input: {e}")
