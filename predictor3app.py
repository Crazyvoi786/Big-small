import streamlit as st
import random
from collections import deque

st.set_page_config(page_title="Shadow Point AI", layout="centered")
st.title("🔮 Shadow Point - AI Trend Predictor")

st.markdown("""
Welcome to **Shadow Point** – your private AI prediction engine.
Manually input outcomes, and the AI will detect trends, give predictions,
and automatically learn over time.
""")

# Memory buffer for outcomes
if "outcome_history" not in st.session_state:
    st.session_state.outcome_history = deque(maxlen=50)

# Manual Outcome Input
st.subheader("📥 Enter Latest Outcome")
latest = st.selectbox("Select Outcome:", ["Big", "Small"])

if st.button("Add Outcome"):
    st.session_state.outcome_history.append(latest)
    st.success(f"Added: {latest}")

# Show History
if st.session_state.outcome_history:
    st.subheader("📊 Outcome History")
    st.write(list(st.session_state.outcome_history))

    # AI Trend Detection
    def detect_trend(history):
        if len(history) < 5:
            return ("Not enough data", 0)

        trend = list(history)[-5:]  # Last 5 outcomes
        bigs = trend.count("Big")
        smalls = trend.count("Small")

        if bigs == smalls:
            return ("SKIP", 50)
        elif bigs > smalls:
            confidence = int((bigs / 5) * 100)
            return ("Big", confidence)
        else:
            confidence = int((smalls / 5) * 100)
            return ("Small", confidence)

    prediction, confidence = detect_trend(st.session_state.outcome_history)

    st.subheader("🧠 AI Prediction")
    st.info(f"Prediction: **{prediction}**  |  Confidence: {confidence}%")

else:
    st.warning("Please enter at least one outcome to begin prediction.")

st.markdown("---")
st.caption("Developed with ❤️ by Dodo for Crazy aka Shadow One")
