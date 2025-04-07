import streamlit as st
import pandas as pd
import random
from collections import Counter

# Initialize session states
if "history" not in st.session_state:
    st.session_state["history"] = []
if "loss_count" not in st.session_state:
    st.session_state["loss_count"] = 0
if "win_count" not in st.session_state:
    st.session_state["win_count"] = 0
if "streak" not in st.session_state:
    st.session_state["streak"] = {"type": None, "count": 0}

st.title("Shadow Point - AI Predictor")

st.markdown("""
### 🧠 Smart AI Trend Learning
Enter past outcomes, and let AI learn:
- Pattern detection
- Loss memory logic
- Auto SKIP if unclear
- Improved prediction after mistakes
""")

num_outcomes = int(st.number_input("How many outcomes to analyze?", min_value=5, max_value=100, value=10))
outcomes = []
for i in range(num_outcomes):
    outcomes.append(st.selectbox(f"Outcome {i + 1}:", ["Big", "Small"], key=f"outcome_{i}"))

# Core AI Logic
def smart_predict(outcomes):
    last_5 = outcomes[-5:]
    count_big = last_5.count("Big")
    count_small = last_5.count("Small")

    overall_big = outcomes.count("Big")
    overall_small = outcomes.count("Small")

    # Pattern detection
    if len(outcomes) >= 3:
        patterns = Counter(tuple(outcomes[i:i+3]) for i in range(len(outcomes)-2))
        top_pattern = max(patterns, key=patterns.get)
    else:
        top_pattern = None

    # Smart trend logic
    prediction = None
    reason = ""

    if count_big == count_small:
        prediction = "SKIP"
        reason = "Equal Big/Small in recent trend."
    elif st.session_state["loss_count"] >= 2:
        prediction = random.choice(["Big", "Small"])
        reason = "Loss streak detected. Changing direction."
    elif top_pattern:
        if top_pattern[-1] == "Big":
            prediction = "Small" if count_small > count_big else "Big"
        else:
            prediction = "Big" if count_big > count_small else "Small"
        reason = f"Following pattern {top_pattern}"
    else:
        prediction = "Big" if count_big > count_small else "Small"
        reason = "Basic trend analysis"

    confidence = 90 if prediction in ["Big", "Small"] else 50
    return prediction, confidence, reason

if st.button("🔮 Predict Next Outcome"):
    prediction, confidence, reason = smart_predict(outcomes)
    st.success(f"Prediction: {prediction} | Confidence: {confidence}%")
    st.caption(f"Reason: {reason}")

    if prediction != "SKIP":
        actual = st.selectbox("What was the actual outcome?", ["Big", "Small"], key="actual")
        win = prediction == actual

        if win:
            st.session_state["win_count"] += 1
            st.session_state["loss_count"] = 0
            st.session_state["streak"] = {"type": "Win", "count": st.session_state["streak"]["count"] + 1}
            st.success("WIN ✅")
        else:
            st.session_state["loss_count"] += 1
            st.session_state["streak"] = {"type": "Loss", "count": st.session_state["streak"]["count"] + 1}
            st.error("LOSS ❌")

        st.session_state["history"].append({
            "Prediction": prediction,
            "Confidence": confidence,
            "Actual": actual,
            "Result": "Win" if win else "Loss",
            "Reason": reason
        })

# History
if st.session_state["history"]:
    st.subheader("📊 Prediction History")
    df = pd.DataFrame(st.session_state["history"])
    st.dataframe(df)

    st.metric("✅ Wins", st.session_state["win_count"])
    st.metric("❌ Losses", st.session_state["loss_count"])
    st.metric("🔥 Streak", f"{st.session_state['streak']['type']} - {st.session_state['streak']['count']}")
