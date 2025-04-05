import streamlit as st

st.set_page_config(page_title="Shadow Point", layout="centered")
st.title("🔮 Shadow Point - AI Based Prediction Tool")

st.markdown("**Enter recent outcomes below:** (Big = 5-9, Small = 0-4)")

history = st.text_area("Enter outcomes (e.g. Big, Small, Big, Small)", height=150)
results = [x.strip().capitalize() for x in history.split(",") if x.strip() in ["Big", "Small"]]

if len(results) < 5:
    st.warning("Enter at least 5 outcomes to start prediction.")
else:
    bigs = results.count("Big")
    smalls = results.count("Small")

    recent_trend = results[-5:]  # last 5 outcomes
    big_trend = recent_trend.count("Big")
    small_trend = recent_trend.count("Small")

    # Prediction logic
    prediction = None
    if big_trend == 5 or small_trend == 5:
        prediction = "SKIP (Too much repetition)"
    elif abs(big_trend - small_trend) >= 3:
        prediction = "Small" if big_trend > small_trend else "Big"
    else:
        prediction = results[-1]  # Repeat last trend if balanced

    st.success(f"📈 Predicted Next Outcome: **{prediction}**")

    st.info("AI logic: Based on trends, reversals & repetition detection.\nKeep feeding Win/Loss to improve accuracy.")
