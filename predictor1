import streamlit as st

# Title & Description
st.title("🔮 Shadow Point - AI Prediction Tool")
st.markdown("Predict Big / Small with AI Logic based on trend and past outcomes.")

# Session state to store all past outcomes
if "history" not in st.session_state:
    st.session_state.history = []

# User input for outcome
st.subheader("📝 Enter New Outcome")
new_outcome = st.selectbox("Choose the latest outcome:", ["Big", "Small"])
if st.button("➕ Add Outcome"):
    st.session_state.history.append(new_outcome)
    st.success(f"Added: {new_outcome}")

# Show history
st.subheader("📊 Outcome History")
st.write(st.session_state.history[-20:])  # Show last 20 only

# AI Prediction Logic
def ai_predict(outcomes):
    if len(outcomes) < 5:
        return "Need more data", 0.0

    last_five = outcomes[-5:]
    big_count = last_five.count("Big")
    small_count = last_five.count("Small")
    
    confidence = abs(big_count - small_count) / 5.0  # 0.0 to 1.0

    if confidence < 0.2:
        return "SKIP", round(confidence, 2)

    prediction = "Big" if big_count > small_count else "Small"
    return prediction, round(confidence, 2)

# Predict Button
if st.button("🎯 Predict Next Outcome"):
    prediction, conf = ai_predict(st.session_state.history)
    if prediction == "SKIP":
        st.warning(f"🔁 Trend unclear, better to SKIP (Confidence: {conf})")
    else:
        st.success(f"🤖 AI Prediction: **{prediction}** (Confidence: {conf})")

# Reset option
if st.button("🧹 Clear All Data"):
    st.session_state.history = []
    st.success("Data Cleared")
