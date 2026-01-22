import pickle
import pandas as pd
import streamlit as st
import joblib

#load the data
df = pd.read_csv("cleaned_df.csv")

#load pre-trained model
model = joblib.load("model.pkl")


#page setup
st.set_page_config(page_icon="🏠",page_title="House Price Prediction",
                   layout="wide")

#sidebar
with st.sidebar:
    st.title("House Price Prediction")
    st.image("house_logo.png")


def get_encoded_loc(location):
    for loc,encoded in  zip(df["location"],df["encoded_loc"]):
        if location==loc:
            return encoded

#user input:  location,bhk,bath,total sqft
pred = None
with st.container(border=True):
    c1,c2 = st.columns(2)
    with c1:
        location = st.selectbox("📌 Location: ",options=df["location"].unique())
        bhk = st.selectbox("🏠 BHK: ",options=sorted(df["bhk"].unique()))

    with c2:
        bath = st.selectbox("🛁 No. of Bathrooms: ",options=sorted(df["bath"].unique()))
        sqft = st.number_input("📐 Total Sqft: ",min_value=300)
    #convert str loc into encoded loc
    location= get_encoded_loc(location)
    a1,a2,a3 = st.columns([1.5,1,1])
    #Price prediction
    if a2.button("Predict Price"):
        data = [[sqft,bath,bhk,location]] # data as 2D
        pred = model.predict(data)[0] #predicts price
        pred = f"{pred*100000:.2f}"

if pred is not None:
    st.subheader(f"Predicted Price: Rs. {pred}")