import streamlit as st
from collections import Counter


def render_mood_chart(entries: list):
    """Line chart of mood score over time."""
    if not entries:
        return

    dates = [e["date"] for e in entries]
    moods = [e["mood"] for e in entries]

    st.subheader("😊 Mood Over Time")

    # Build a simple data dict for st.line_chart
    data = {"Mood (1–5)": moods}

    import pandas as pd
    df = pd.DataFrame(data, index=dates)
    st.line_chart(df, use_container_width=True, color=["#4CAF50"])

    # Mood distribution bar
    st.subheader("📊 Mood Distribution")
    mood_counts = Counter(moods)
    mood_labels = {1: "😞 Very Low", 2: "😕 Low", 3: "😐 Neutral", 4: "🙂 Good", 5: "😊 Great"}
    dist_data = {mood_labels[k]: mood_counts.get(k, 0) for k in [1, 2, 3, 4, 5]}
    df_dist = pd.DataFrame({"Count": list(dist_data.values())}, index=list(dist_data.keys()))
    st.bar_chart(df_dist, use_container_width=True, color=["#66BB6A"])


def render_emotion_breakdown(entries: list):
    """Bar chart of most common emotions across entries."""
    all_emotions = []
    for e in entries:
        all_emotions.extend(e.get("emotions", []))

    if not all_emotions:
        return

    import pandas as pd

    st.subheader("💭 Most Common Emotions")
    counts = Counter(all_emotions)
    top = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:12])

    df = pd.DataFrame({"Times recorded": list(top.values())}, index=list(top.keys()))
    st.bar_chart(df, use_container_width=True, color=["#42A5F5"])
