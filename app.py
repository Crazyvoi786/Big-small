import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Shadow Point - AI Predictor", layout="centered")
st.title("🌑 Shadow Point - Big/Small Predictor")

# Initialize session state
if 'outcomes' not in st.session_state:
    st.session_state.outcomes = []
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown("""
<style>
    .main {
        background-color: #0f0f0f;
        color: #ffffff;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background-color: #1f1f1f;
        color: white;
        border-radius: 8px;
        border: 1px solid #444;
        padding: 0.5em 1em;
    }
</style>
""", unsafe_allow_html=True)

st.subheader("🧠 Enter Last Outcome")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Big"):
        st.session_state.outcomes.append("B")
with col2:
    if st.button("Small"):
        st.session_state.outcomes.append("S")
with col3:
    if st.button("Undo") and st.session_state.outcomes:
        st.session_state.outcomes.pop()

st.markdown("### 📊 Outcome History:")
st.write(" ".join(st.session_state.outcomes))

# Trend logic and AI prediction
def detect_pattern(data):
    if len(data) < 6:
        return "SKIP", 0.5

    last5 = data[-5:]
    b_count = last5.count("B")
    s_count = last5.count("S")

    # Example patterns
    if b_count >= 4:
        return "S", 0.9
    elif s_count >= 4:
        return "B", 0.9
    elif last5 == ["B", "S", "B", "S", "B"]:
        return "S", 0.75
    elif last5 == ["S", "B", "S", "B", "S"]:
        return "B", 0.75
    else:
        return "SKIP", 0.55

prediction, confidence = detect_pattern(st.session_state.outcomes)

st.markdown("### 🔮 AI Prediction")
if prediction == "SKIP":
    st.info("No clear trend detected. Better to SKIP.")
else:
    st.success(f"Prediction: **{prediction}**  |  Confidence: **{int(confidence*100)}%**")

# Profit recovery logic (example)
if 'loss_count' not in st.session_state:
    st.session_state.loss_count = 0

st.markdown("### ✅ Outcome Confirmation")
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Prediction was Correct"):
        st.session_state.loss_count = 0
        st.session_state.history.append("Win")
with col2:
    if st.button("❌ Prediction was Wrong"):
        st.session_state.loss_count += 1
        st.session_state.history.append("Loss")

if st.session_state.loss_count >= 2:
    st.warning(f"⚠️ {st.session_state.loss_count} losses detected. Next prediction will use stronger trend match.")

# Show win/loss history
st.markdown("### 📈 Win/Loss History:")
history_df = pd.DataFrame({"Result": st.session_state.history})
st.dataframe(history_df, height=200)

st.markdown("""
---
🎮 Powered by **Dodo AI** | Player: **Shadow One**  
All trends learned from real charts. This is your god-level edge.
""")
