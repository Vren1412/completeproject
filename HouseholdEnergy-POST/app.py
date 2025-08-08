import streamlit as st
import pandas as pd
import numpy as np
import platform
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle

# Page config
st.set_page_config(page_title="Energy Platform Login", layout="centered")

# Session state to manage login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login screen
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>Residential Energy Consumption Prediction Platform</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Login Portal</h3>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("login_form"):
        st.subheader("🔐 User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        if username == "vaishnavi" and password == "admin123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password. Please try again.")

# Main app after login
if st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>Residential Energy Consumption Prediction Platform</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("3. Loading Libraries and Data")

    st.subheader("3.1 Libraries Loaded ✅")
    st.markdown("""
    - pandas for data handling  
    - numpy for numeric processing  
    - scikit-learn for model development  
    - platform for system info  
    """)

    st.subheader("3.2 Library Versions 📦")
    st.text(f"Python version: {platform.python_version()}")
    st.text(f"Pandas version: {pd.__version__}")
    st.text(f"Numpy version: {np.__version__}")
    st.text(f"Scikit-learn version: {sklearn.__version__}")

    st.subheader("3.3 Upload and Preview Data")
    uploaded_file = st.file_uploader("Upload Energy CSV File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file, parse_dates=[['Date', 'Time']])
        df.set_index('Date_Time', inplace=True)
        df['hour'] = df.index.hour
        st.dataframe(df.head())

        st.header("4. Exploratory Data Analysis")
        st.subheader("4.1 Data Dimensionality")
        st.write(f"Shape: {df.shape}")

        st.subheader("4.2 Data Types")
        st.write(df.dtypes)

        st.subheader("4.3 Summary Statistics")
        st.write(df.describe())

        st.subheader("4.4 Missing Values")
        st.write(df.isnull().sum())

        st.subheader("4.5 Target Distribution")
        st.line_chart(df['Global_active_power'])

        st.subheader("4.6 Outlier Detection")
        st.write(df['Global_active_power'].describe(percentiles=[.01, .25, .5, .75, .99]))

        st.subheader("4.7 Correlation Heatmap")
        st.write(df.corr().style.background_gradient(cmap='coolwarm'))

        st.header("5. Data Transformation & Preprocessing")
        q_low = df['Global_active_power'].quantile(0.01)
        q_hi = df['Global_active_power'].quantile(0.99)
        df_filtered = df[(df['Global_active_power'] > q_low) & (df['Global_active_power'] < q_hi)]
        st.write(f"After removing outliers: {df_filtered.shape}")

        st.header("6. Feature Engineering")
        corr = df_filtered.corr()
        st.subheader("6.1 Feature Correlation with Target")
        st.bar_chart(corr['Global_active_power'].drop('Global_active_power'))

        st.header("7. Model Development & Evaluation")
        st.subheader("7.1 Train-Test Split & Model Training")
        target = 'Global_active_power'
        X = df_filtered.drop(target, axis=1)
        y = df_filtered[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        st.subheader("7.2 Model Evaluation")
        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        accuracy_percent = r2 * 100

        st.metric("Mean Squared Error", f"{mse:.4f}")
        st.metric("R² Score", f"{r2:.4f}")
        st.metric("Model Accuracy", f"{accuracy_percent:.2f}%")

        st.subheader("7.3 Actual vs Predicted")
        result_df = pd.DataFrame({"Actual": y_test.values, "Predicted": preds})
        st.line_chart(result_df)

        with open("energy_model.pkl", "wb") as f:
            pickle.dump(model, f)

        st.subheader("7.4 Test Model with Your Input")
        with st.form("prediction_form"):
            st.write("Enter feature values to predict Global Active Power")

            col1, col2, col3 = st.columns(3)
            with col1:
                global_reactive_power = st.number_input("Global Reactive Power", min_value=0.0, max_value=1.0, value=0.1)
                voltage = st.number_input("Voltage", min_value=100.0, max_value=300.0, value=240.0)
            with col2:
                global_intensity = st.number_input("Global Intensity", min_value=0.0, max_value=30.0, value=10.0)
                sub_metering_1 = st.number_input("Sub Metering 1", min_value=0, max_value=100, value=0)
            with col3:
                sub_metering_2 = st.number_input("Sub Metering 2", min_value=0, max_value=100, value=0)
                sub_metering_3 = st.number_input("Sub Metering 3", min_value=0, max_value=100, value=0)
                hour = st.slider("Hour of the Day", min_value=0, max_value=23, value=12)

            submitted = st.form_submit_button("Predict")

            if submitted:
                input_data = pd.DataFrame([[global_reactive_power, voltage, global_intensity,
                                            sub_metering_1, sub_metering_2, sub_metering_3, hour]],
                                          columns=["Global_reactive_power", "Voltage", "Global_intensity",
                                                   "Sub_metering_1", "Sub_metering_2", "Sub_metering_3", "hour"])
                prediction = model.predict(input_data)[0]
                st.success(f"🔌 Predicted Global Active Power: *{prediction:.3f} kW*")
