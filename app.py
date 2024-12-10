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
st.title("AI-Enhanced Big-Small Predictor (Max Accuracy)")

# Input Section
st.header("Enter Recent Outcomes")
num_outcomes = int(st.number_input("How many past outcomes to analyze?", min_value=5, max_value=50, value=10))
outcomes = []
for i in range(num_outcomes):
    outcomes.append(st.selectbox(f"Outcome {i + 1}:", ["Big", "Small"], key=f"unique_key_{i}"))

# Prediction Logic
def predict_next(outcomes):
    # Analyze Short-Term Trends
    short_trend = outcomes[-5:] if len(outcomes) >= 5 else outcomes
    big_count = short_trend.count("Big")
    small_count = short_trend.count("Small")

    # Long-Term Trend Analysis
    long_trend = outcomes
    total_big = long_trend.count("Big")
    total_small = long_trend.count("Small")
    overall_trend = "Big" if total_big > total_small else "Small"

    # Pattern Recognition (3-step patterns)
    if len(outcomes) >= 3:
        pattern_counts = Counter(tuple(outcomes[i:i+3]) for i in range(len(outcomes)-2))
        common_pattern = max(pattern_counts, key=pattern_counts.get)
    else:
        common_pattern = None

    # AI-Based Weighted Prediction
    if short_trend[-1] == "Big" or (common_pattern and common_pattern[-1] == "Big"):
        prediction = "Small" if small_count > big_count else overall_trend
    else:
        prediction = "Big" if big_count > small_count else overall_trend

    # Confidence Score Calculation
    confidence = 90 if prediction == overall_trend else 75

    # Handle Edge Cases
    if small_count == big_count:
        prediction = random.choice(["Big", "Small"])
        confidence = 50  # Lower confidence for tie cases

    return prediction, confidence

# Prediction Button
if st.button("Predict Next Outcome"):
    prediction, confidence = predict_next(outcomes)
    st.success(f"Predicted Next Outcome: {prediction} (Confidence: {confidence}%)")
    
    # Simulate Result
    actual_outcome = st.selectbox("What was the actual outcome?", ["Big", "Small"], key="actual_result")
    is_win = prediction == actual_outcome

    # Update Win/Loss Counts
    if is_win:
        st.session_state["win_count"] += 1
        st.session_state["loss_count"] = 0
        st.session_state["streak"] = {"type": "Win", "count": st.session_state["streak"]["count"] + 1}
        st.success("Result: WIN!")
    else:
        st.session_state["loss_count"] += 1
        st.session_state["streak"] = {"type": "Loss", "count": st.session_state["streak"]["count"] + 1}
        st.warning("Result: LOSS!")

    # Save History
    st.session_state["history"].append({
        "Prediction": prediction,
        "Confidence": confidence,
        "Actual": actual_outcome,
        "Result": "Win" if is_win else "Loss"
    })

# Visualization
if st.session_state["history"]:
    st.subheader("Prediction History")
    df = pd.DataFrame(st.session_state["history"])
    st.dataframe(df)

    # Metrics
    st.metric("Total Wins", st.session_state["win_count"])
    st.metric("Total Losses", st.session_state["loss_count"])
    st.metric("Current Streak", f"{st.session_state['streak']['type']} - {st.session_state['streak']['count']}")

    # Visualization of Win/Loss
    st.subheader("Win/Loss Chart")
    win_loss_counts = df["Result"].value_counts()
    fig, ax = plt.subplots()
    win_loss_counts.plot(kind="bar", color=["green", "red"], ax=ax)
    ax.set_title("Win vs Loss Trends")
    ax.set_ylabel("Count")
    st.pyplot(fig)
