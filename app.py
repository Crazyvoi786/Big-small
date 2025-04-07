import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from collections import Counter

# Google Sheets integration
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("ShadowPointData").sheet1  # Change this to your actual sheet name

# Initialize Session State
if "history" not in st.session_state:
    st.session_state["history"] = []
if "loss_count" not in st.session_state:
    st.session_state["loss_count"] = 0
if "win_count" not in st.session_state:
    st.session_state["win_count"] = 0
if "streak" not in st.session_state:
    st.session_state["streak"] = {"type": None, "count": 0}
if "last_prediction" not in st.session_state:
    st.session_state["last_prediction"] = "None"

# Title
st.title("AI-Enhanced Big-Small Predictor (Max Accuracy)")

# Input Section
st.header("Enter Recent Outcomes")
num_outcomes = int(st.number_input("How many past outcomes to analyze?", min_value=5, max_value=50, value=10))
outcomes = []

col1, col2 = st.columns(2)
with col1:
    for i in range(num_outcomes):
        outcome = st.selectbox(f"Outcome {i+1}", ["Big", "Small"], key=f"outcome_{i}")
        outcomes.append(outcome)

# Prediction Logic
def predict_next(outcomes):
    if len(outcomes) < 5:
        return "Not enough data"

    pattern = tuple(outcomes[-5:])
    freq = Counter([tuple(outcomes[i:i+5]) for i in range(len(outcomes)-5)])
    if freq[pattern] >= 2:
        last = outcomes[-1]
        return "Small" if last == "Big" else "Big"
    else:
        return "Skip"

# Predict Button
if st.button("Predict Next"):
    prediction = predict_next(outcomes)
    st.session_state["last_prediction"] = prediction
    if prediction == "Skip":
        st.warning("⚠️ Not enough clear pattern. Best to SKIP!")
    else:
        st.success(f"🔮 Prediction: {prediction}")

# Submit Result + Google Sheet Logging
st.header("Submit Actual Result")
actual_result = st.selectbox("What was the actual result?", ["Win", "Loss", "Pending"])
if st.button("Submit Result"):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

