import streamlit as st
import numpy as np
import joblib

model = joblib.load("linear_model.pkl")   

st.set_page_config(page_title="House Price Predictor", layout="centered")

st.title("🏠 House Price Prediction")
st.write("Enter house features to predict the sale price")

# Inputs
overall_qual = st.slider("Overall Quality (1–10)", 1, 10, 5)
gr_liv_area = st.number_input("Living Area (sq ft)", min_value=300, value=1500)
garage_cars = st.slider("Garage Cars", 0, 4, 2)
total_bsmt = st.number_input("Total Basement SF", min_value=0, value=800)
year_built = st.slider("Year Built", 1870, 2025, 2005)
full_bath = st.slider("Full Bathrooms", 0, 4, 2)
bedroom = st.slider("Bedrooms Above Ground", 0, 6, 3)
lot_area = st.number_input("Lot Area", min_value=1000, value=8000)

# Predict
if st.button("Predict Price 💰"):
    X_new = np.array([[
        overall_qual,
        gr_liv_area,
        garage_cars,
        total_bsmt,
        year_built,
        full_bath,
        bedroom,
        lot_area
    ]])

    price = model.predict(X_new)[0]

    st.success(f"🏷️ Predicted Sale Price: ${price:,.0f}")
