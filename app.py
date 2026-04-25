import streamlit as st
from datetime import date, datetime
from agents import run_agent
from storage import (
    save_entry, load_today_entry, load_all_entries,
    load_entries_last_n_days, delete_today_entry,
)
from charts import render_mood_chart, render_emotion_breakdown

st.set_page_config(page_title="Wellness Journal", page_icon="🌿", layout="wide")

DISCLAIMER = (
    "🌿 **This app is a personal journaling and reflection tool. "
    "It is not a substitute for professional mental health support. "
    "If you are in distress or crisis, please reach out to a qualified mental health professional "
    "or a crisis helpline in your country.**"
)

MOOD_LABELS = {1: "😞 Very Low", 2: "😕 Low", 3: "😐 Neutral", 4: "🙂 Good", 5: "😊 Great"}
EMOTION_OPTIONS = [
    "Anxious", "Calm", "Sad", "Happy", "Angry", "Grateful",
    "Overwhelmed", "Hopeful", "Lonely", "Connected", "Tired", "Energised",
    "Confused", "Focused", "Frustrated", "Content",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🌿 Wellness Journal")
    st.caption("A private space for reflection.")
    st.divider()

    model = st.text_input("Ollama Model", value="llama3")

    st.divider()
    st.subheader("🤖 Agents")
    use_reflection = st.checkbox("🪞 Reflection Agent",       value=True)
    use_reframe    = st.checkbox("💡 Cognitive Reframe Agent", value=True)
    use_wellness   = st.checkbox("📈 Wellness Tracker Agent",  value=True)

    st.divider()
    st.info(DISCLAIMER, icon="ℹ️")


# ── Tabs ──────────────────────────────────────────────────────────────────────
st.title("🌿 Mental Health Companion")
st.caption("A safe, private journaling space. Your entries stay on your device.")

tab_journal, tab_trends, tab_history = st.tabs([
    "📝 Today's Journal", "📊 Wellness Trends", "📚 Past Entries"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: TODAY'S JOURNAL
# ══════════════════════════════════════════════════════════════════════════════
with tab_journal:
    today = date.today()
    st.subheader(f"📝 {today.strftime('%A, %B %d, %Y')}")

    # Check for existing entry
    existing = load_today_entry()
    if existing:
        st.info("You already have an entry for today. You can view it below or overwrite it.")
        with st.expander("📖 View today's saved entry", expanded=False):
            st.markdown(f"**Mood:** {MOOD_LABELS.get(existing.get('mood', 3), '—')}")
            st.markdown(f"**Emotions:** {', '.join(existing.get('emotions', []))}")
            st.markdown(f"**Journal:** {existing.get('journal', '')}")
        if st.button("🗑️ Delete today's entry", key="del_today"):
            delete_today_entry()
            st.success("Entry deleted.")
            st.rerun()

    st.divider()

    # ── Mood input ────────────────────────────────────────────────────────────
    st.subheader("How are you feeling today?")
    mood = st.slider("Mood (1 = Very Low, 5 = Great)", 1, 5, 3, key="mood_slider")
    st.caption(MOOD_LABELS[mood])

    # ── Emotions multi-select ─────────────────────────────────────────────────
    emotions = st.multiselect(
        "Which emotions are present for you right now?",
        EMOTION_OPTIONS,
        key="emotions_select",
    )

    # ── Journal entry ──────────────────────────────────────────────────────────
    st.subheader("Open Journal")
    journal_text = st.text_area(
        "Write freely. There are no right or wrong answers.",
        height=200,
        placeholder=(
            "How has your day been? What's on your mind? "
            "What are you grateful for, or what felt hard today?"
        ),
        key="journal_text",
    )

    # ── Gratitude ─────────────────────────────────────────────────────────────
    gratitude = st.text_input(
        "One thing you're grateful for today (optional)",
        placeholder="e.g. A kind message from a friend",
        key="gratitude_text",
    )

    # ── Run agents ────────────────────────────────────────────────────────────
    selected_agents = []
    if use_reflection: selected_agents.append("Reflection")
    if use_reframe:    selected_agents.append("Reframe")
    if use_wellness:   selected_agents.append("Wellness")

    if not selected_agents:
        st.warning("Enable at least one agent in the sidebar.")
    elif st.button("💾 Save & Get Insights", use_container_width=True, type="primary"):
        if not journal_text.strip() and not emotions:
            st.warning("Please write something in your journal or select some emotions.")
        else:
            # Build user context
            user_context = build_user_context(mood, emotions, journal_text, gratitude)

            # Load recent history for Wellness Agent
            recent = load_entries_last_n_days(7)
            history_summary = build_history_summary(recent)

            results = {}
            progress_bar = st.progress(0, text="Reflecting on your entry...")
            prior = ""

            for i, agent_name in enumerate(selected_agents):
                labels = {
                    "Reflection": "🪞 Reflection Agent",
                    "Reframe":    "💡 Cognitive Reframe Agent",
                    "Wellness":   "📈 Wellness Tracker Agent",
                }
                progress_bar.progress(
                    i / len(selected_agents),
                    text=f"Running {labels[agent_name]}...",
                )
                output = run_agent(
                    agent_name      = agent_name,
                    user_context    = user_context,
                    history_summary = history_summary,
                    prior_output    = prior,
                    model           = model,
                )
                results[agent_name] = output
                prior += f"\n\n{labels[agent_name]}:\n{output}"

            progress_bar.progress(1.0, text="Done.")

            # Save entry
            save_entry(
                mood      = mood,
                emotions  = emotions,
                journal   = journal_text,
                gratitude = gratitude,
                results   = results,
            )

            st.divider()
            st.subheader("💬 Your Companion's Response")
            display_agent_outputs(results)
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: WELLNESS TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab_trends:
    st.subheader("📊 Wellness Trends")

    days = st.selectbox("Show last", [7, 14, 30, 60, 90], index=0, key="trend_days")
    entries = load_entries_last_n_days(days)

    if len(entries) < 2:
        st.info(f"Keep journaling! Trends will appear after at least 2 entries. You have {len(entries)} so far.")
    else:
        st.caption(f"Based on {len(entries)} entries over the past {days} days.")
        render_mood_chart(entries)
        render_emotion_breakdown(entries)

        # Stats
        moods = [e["mood"] for e in entries]
        avg_mood = round(sum(moods) / len(moods), 1)
        best_day = max(entries, key=lambda e: e["mood"])
        low_day  = min(entries, key=lambda e: e["mood"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Mood", f"{avg_mood}/5")
        col2.metric("Best Day", f"{best_day['date']} ({MOOD_LABELS[best_day['mood']]})")
        col3.metric("Challenging Day", f"{low_day['date']} ({MOOD_LABELS[low_day['mood']]})")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: PAST ENTRIES
# ══════════════════════════════════════════════════════════════════════════════
with tab_history:
    st.subheader("📚 Past Journal Entries")
    all_entries = load_all_entries()

    if not all_entries:
        st.info("No entries yet. Start journaling in the Today's Journal tab.")
    else:
        for entry in reversed(all_entries):
            mood_label = MOOD_LABELS.get(entry.get("mood", 3), "—")
            emos = ", ".join(entry.get("emotions", [])) or "—"
            label = f"📅 {entry['date']}  |  {mood_label}  |  {emos}"
            with st.expander(label, expanded=False):
                st.markdown(f"**Journal:** {entry.get('journal', '—')}")
                if entry.get("gratitude"):
                    st.markdown(f"**Grateful for:** {entry['gratitude']}")
                results = entry.get("results", {})
                if results:
                    st.divider()
                    display_agent_outputs(results)


# ── Helpers ───────────────────────────────────────────────────────────────────

def build_user_context(mood: int, emotions: list, journal: str, gratitude: str) -> str:
    return (
        f"Date: {date.today()}\n"
        f"Mood score: {mood}/5 ({MOOD_LABELS[mood]})\n"
        f"Emotions present: {', '.join(emotions) if emotions else 'Not specified'}\n"
        f"Journal entry: {journal.strip() or 'No text written.'}\n"
        f"Gratitude: {gratitude.strip() or 'Not filled in.'}"
    )


def build_history_summary(entries: list) -> str:
    if not entries:
        return "No previous entries available."
    lines = []
    for e in entries:
        lines.append(
            f"{e['date']}: mood={e['mood']}/5, "
            f"emotions={', '.join(e.get('emotions', [])) or 'none'}"
        )
    return "Recent entries (oldest → newest):\n" + "\n".join(lines)


def display_agent_outputs(results: dict):
    meta = {
        "Reflection": ("🪞", "Reflection Agent"),
        "Reframe":    ("💡", "Cognitive Reframe Agent"),
        "Wellness":   ("📈", "Wellness Tracker Agent"),
    }
    for key, output in results.items():
        emoji, label = meta.get(key, ("🤖", key))
        st.markdown(f"### {emoji} {label}")
        st.markdown(output)
        st.divider()
