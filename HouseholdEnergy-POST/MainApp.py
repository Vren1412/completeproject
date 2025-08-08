import streamlit as st
import pandas as pd
import platform
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle

def run_main_app():
    st.title("Residential Energy Consumption Prediction Platform")

    # ---------------------------- 3. Loading Libraries and Data -----------------------------------
    st.header("3. Loading Libraries and Data")

    st.subheader("3.1 Libraries Loaded")
    st.subheader("3.2 Library Versions")
    st.text(f"Python version: {platform.python_version()}")
    st.text(f"Pandas version: {pd.__version__}")
    st.text(f"Scikit-learn version: {sklearn.__version__}")

    st.subheader("3.3 Upload and Preview Data")
    uploaded_file = st.file_uploader("Upload Energy CSV File", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, parse_dates=[['Date', 'Time']])
            df.set_index('Date_Time', inplace=True)
            df['hour'] = df.index.hour

            # Drop unnamed index columns if present
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            st.dataframe(df.head())

            # --------------------------- 4. Exploratory Data Analysis ---------------------------
            st.header("4. Exploratory Data Analysis")
            st.write(f"Shape: {df.shape}")
            st.write(df.dtypes)
            st.write(df.describe())
            st.write("Missing Values:")
            st.write(df.isnull().sum())

            st.subheader("4.5 Target Distribution")
            st.line_chart(df['Global_active_power'])

            st.subheader("4.6 Outlier Detection")
            st.write(df['Global_active_power'].describe(percentiles=[.01, .25, .5, .75, .99]))

            st.subheader("4.7 Correlation Heatmap (Numeric View)")
            numeric_df = df.select_dtypes(include=['float64', 'int64'])
            st.write(numeric_df.corr().style.background_gradient(cmap='coolwarm'))

            # --------------------------- 5. Data Transformation & Preprocessing ---------------------------
            st.header("5. Data Transformation & Preprocessing")
            q_low = df['Global_active_power'].quantile(0.01)
            q_hi = df['Global_active_power'].quantile(0.99)
            df_filtered = df[(df['Global_active_power'] > q_low) & (df['Global_active_power'] < q_hi)]
            st.write(f"After removing outliers: {df_filtered.shape}")

            # --------------------------- 6. Feature Engineering ---------------------------
            st.header("6. Feature Engineering")
            corr = df_filtered.corr()
            st.bar_chart(corr['Global_active_power'].drop('Global_active_power'))

            # --------------------------- 7. Model Development ---------------------------
            st.header("7. Model Development & Comparison")

            target = 'Global_active_power'
            features = ['Global_reactive_power', 'Voltage', 'Global_intensity',
                        'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3', 'hour']

            if not all(f in df_filtered.columns for f in features + [target]):
                st.error("❌ One or more required columns are missing in your dataset.")
                return

            X = df_filtered[features]
            y = df_filtered[target]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = RandomForestRegressor(n_estimators=100)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            mse = mean_squared_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            st.metric("Mean Squared Error", f"{mse:.4f}")
            st.metric("R² Score", f"{r2:.4f}")
            st.metric("Model Accuracy", f"{r2 * 100:.2f}%")

            st.subheader("7.3 Actual vs Predicted")
            result_df = pd.DataFrame({"Actual": y_test.values, "Predicted": preds})
            st.line_chart(result_df)

            # Save the model
            with open("energy_model.pkl", "wb") as f:
                pickle.dump(model, f)

            # --------------------------- 8. Prediction Form ---------------------------
            st.subheader("7.4 Test Model with Your Input")
            with st.form("prediction_form"):
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
                                              columns=features)
                    prediction = model.predict(input_data)[0]
                    st.success(f"🔌 Predicted Global Active Power: **{prediction:.3f} kW**")

        except Exception as e:
            st.error(f"⚠️ Error processing file: {e}")
