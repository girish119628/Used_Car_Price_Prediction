import streamlit as st
import joblib
import pandas as pd

# Load trained ML pipeline
pipeline = joblib.load("models/car_price_pipeline.pkl")

# Page title
st.title("Used Car Price Prediction")

# User inputs
brand = st.text_input("Enter Brand")

vehicle_age = st.number_input(
    "Vehicle Age",
    min_value=0,
    max_value=30,
    value=5
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=50000
)

seller_type = st.text_input("Seller Type")

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])

transmission_type = st.selectbox("Transmission Type", ["Manual", "Automatic"])

mileage = st.number_input(
    "Mileage",
    min_value=0.0,
    value=20.0
)

engine = st.number_input(
    "Engine (CC)",
    min_value=0.0,
    value=1200.0
)

max_power = st.number_input(
    "Max Power (bhp)",
    min_value=0.0,
    value=80.0
)

seats = st.number_input(
    "Number of Seats",
    min_value=1,
    max_value=10,
    value=5
)

if st.button("Predict Price"):

    input_data = pd.DataFrame({
        "brand": [brand],
        "vehicle_age": [vehicle_age],
        "km_driven": [km_driven],
        "seller_type": [seller_type],
        "fuel_type": [fuel_type],
        "transmission_type": [transmission_type],
        "mileage": [mileage],
        "engine": [engine],
        "max_power": [max_power],
        "seats": [seats]
    })

    prediction = pipeline.predict(input_data)

    st.success(
        f"Predicted Selling Price: ₹{prediction[0]:,.2f}"
    )
