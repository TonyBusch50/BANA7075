import streamlit as st
import pandas as pd
import requests

# FastAPI backend URL. Used to send requests from Streamlit
# to FastAPI for model predictions.
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("DOM Predictor - ML Model UI")

#################################
# === Single Input Prediction ===
#################################
# Users can manually enter feature values for each feature
st.subheader("Single Input Prediction")
# Streamlit Input for saleamount as an integer
saleamount = st.number_input("Desired Sale Amount?", step=1, format="%d", min_value=0)
AgeofHome = st.number_input("Age of Home?")
Bedrooms = st.number_input("Bedrooms?")
Bathrooms = st.number_input("Bathrooms (include half baths)?")
Acreage = st.number_input("Acreage of land:")
Basement = st.selectbox("What kind of basement do you have?", ["Full", "Partial", "Full Crawl", "Partial Crawl"])
if Basement == "Full":
    Basement_Type_Full_Basement = 1.
    Basement_Type_Full_Crawl = 0.
    Basement_Type_Part_Basement = 0.
    Basement_Type_Part_Crawl = 0.
elif Basement == "Partial":
    Basement_Type_Full_Basement = 0.
    Basement_Type_Full_Crawl = 0.
    Basement_Type_Part_Basement = 1.
    Basement_Type_Part_Crawl = 0.
elif Basement == "Full Crawl":
    Basement_Type_Full_Basement = 0.
    Basement_Type_Full_Crawl = 1.
    Basement_Type_Part_Basement = 0.
    Basement_Type_Part_Crawl = 0.
else:
    Basement_Type_Full_Basement = 0.
    Basement_Type_Full_Crawl = 0.
    Basement_Type_Part_Basement = 0.
    Basement_Type_Part_Crawl = 1.

#weekend = st.selectbox("Is it a weekend?", [0, 1])
#holiday = st.selectbox("Is it a holiday?", [0, 1])
#price_per_kg = st.number_input("Price per Kg ($)", value=1.54)
#promo = st.selectbox("Promotion Available?", [0, 1])
#previous_days_demand = st.number_input("Previous Days Demand", value=1313)

# This button triggers a request to FastAPI's /predict endpoint.
if st.button("Predict Days on Market"):
    input_data = [{
        "saleamount": int(saleamount),
        "AgeofHome": float(AgeofHome),
        "Bedrooms": float(Bedrooms),
        "Bathrooms": float(Bathrooms),
        "Acreage": float(Acreage),
        "Basement_Type_Full_Basement": float(Basement_Type_Full_Basement),
        "Basement_Type_Part_Basement": float(Basement_Type_Part_Basement),
        "Basement_Type_Full_Crawl": float(Basement_Type_Full_Crawl),
        "Basement_Type_Part_Crawl": float(Basement_Type_Full_Crawl),
    }]

    response = requests.post(f"{FASTAPI_URL}/predict", json=input_data)

    # The response is displayed on the Streamlit UI.
    if response.status_code == 200:
        prediction = response.json()["predictions"][0]
        st.success(f"Predicted Demand: {prediction:.2f}")
    else:
        st.error("Error fetching prediction. Check FastAPI logs.")

###########################################
# === Batch Prediction with File Upload ===
###########################################
# Users can upload a CSV file containing multiple rows of input data.
st.subheader("Batch Prediction via CSV Upload")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:", df.head())

    # The file is sent to the FastAPI /predict_batch endpoint.
    if st.button("Get Batch Predictions"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{FASTAPI_URL}/predict_batch", files=files)

        #Predictions are added to the dataset and displayed on the UI.
        if response.status_code == 200:
            predictions = response.json()["predictions"]
            df["Predicted Demand"] = predictions
            st.subheader("Predictions:")
            st.write(df)
        else:
            st.error("Error processing batch prediction.")