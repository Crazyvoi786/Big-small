import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from collections import Counter

# Initialize Session State
if "history" not in st.session_state:
    st.session_state["history"] = []
if "loss_count" not in st.session_state:
    st.session_state["loss_count"] = 0
if "win_count" not in st.session_state:
    st.session_state["win_count"] = 0
if "streak" not in st.session_state:
    st.session_state["streak"] = {"type": None, "count": 0}

# Title
st.title("🔮 Shadow Point - AI Trend Predictor")

# Input Section
st.header("Enter Recent Outcomes")
num_outcomes = int(st.number_input("How many past outcomes to analyze?", min_value=5, max_value=50, value=10))
outcomes = []
for i in range(num_outcomes):
    outcomes.append(st.selectbox(f"Outcome {i + 1}:", ["Big", "Small"], key=f"unique_key_{i}"))

# Deep Pattern Memory
def detect_loss_patterns(history):
    loss_patterns = []
    for entry in history:
        if entry["Result"] == "Loss":
            pattern = tuple(entry["Pattern"])
            loss_patterns.append(pattern)
    return loss_patterns

# Prediction Logic
def predict_next(outcomes):
    # Analyze Short-Term Trends
    short_trend = outcomes[-5:] if len(outcomes) >= 5 else outcomes
    big_count = short_trend.count("Big")
    small_count = short_trend.count("Small")

    # Long-Term Trend Analysis
    total_big = outcomes.count("Big")
    total_small = outcomes.count("Small")
    overall_trend = "Big" if total_big > total_small else "Small"

    # Pattern Recognition (3-step patterns)
    pattern = tuple(outcomes[-3:]) if len(outcomes) >= 3 else None

    # Memory: avoid repeating loss patterns
    loss_patterns = detect_loss_patterns(st.session_state["history"])
    if pattern in loss_patterns:
        st.warning("⚠️ This pattern has failed before. Adjusting...")
        prediction = "Small" if outcomes[-1] == "Big" else "Big"
        confidence = 65
    else:
        # AI-Based Weighted Prediction
        if outcomes[-1] == "Big":
            prediction = "Small" if small_count > big_count else overall_trend
        else:
            prediction = "Big" if big_count > small_count else overall_trend

        confidence = 90 if prediction == overall_trend else 75
        if small_count == big_count:
            prediction = random.choice(["Big", "Small"])
            confidence = 50

    return prediction, confidence, pattern

# Prediction Button
if st.button("Predict Next Outcome"):
    prediction, confidence, pattern = predict_next(outcomes)
    st.success(f"Predicted: {prediction} (Confidence: {confidence}%)")

    actual_outcome = st.selectbox("What was the actual outcome?", ["Big", "Small"], key="actual_result")
    is_win = prediction == actual_outcome

    # Update Win/Loss Counts
    if is_win:
        st.session_state["win_count"] += 1
        st.session_state["loss_count"] = 0
        st.session_state["streak"] = {"type": "Win", "count": st.session_state["streak"]["count"] + 1}
        st.success("✅ Result: WIN!")
    else:
        st.session_state["loss_count"] += 1
        st.session_state["streak"] = {"type": "Loss", "count": st.session_state["streak"]["count"] + 1}
        st.warning("❌ Result: LOSS!")

    # Save History
    st.session_state["history"].append({
        "Prediction": prediction,
        "Confidence": confidence,
        "Actual": actual_outcome,
        "Result": "Win" if is_win else "Loss",
        "Pattern": list(outcomes[-3:]) if len(outcomes) >= 3 else []
    })

# History Table
if st.session_state["history"]:
    st.subheader("Prediction History")
    df = pd.DataFrame(st.session_state["history"])
    st.dataframe(df)

    # Metrics
    st.metric("✅ Wins", st.session_state["win_count"])
    st.metric("❌ Losses", st.session_state["loss_count"])
    st.metric("🔥 Current Streak", f"{st.session_state['streak']['type']} - {st.session_state['streak']['count']}")

    # Chart
    st.subheader("📊 Win/Loss Trends")
    win_loss_counts = df["Result"].value_counts()
    fig, ax = plt.subplots()
    win_loss_counts.plot(kind="bar", color=["green", "red"], ax=ax)
    ax.set_title("Win vs Loss Chart")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Footer
st.caption("Created by Dodo | Shadow Point AI")
