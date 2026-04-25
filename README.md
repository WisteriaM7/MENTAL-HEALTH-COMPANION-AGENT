# 🌿 Mental Health Companion Agents

A simple AI-powered journaling + reflection app built with Streamlit + Ollama.

## ✨ Features
- Daily mood tracking (1–5)
- Emotion tagging
- Open journaling
- AI Agents:
  - Reflection Agent
  - Cognitive Reframe Agent
  - Wellness Tracker Agent
- Mood trend visualization
- Local data storage (privacy-first)

## ⚠️ Disclaimer
This app is NOT a substitute for professional mental health support.

## 🚀 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt

2. Install Ollama

Download from: https://ollama.com

Run:

ollama pull llama3
ollama serve
3. (Optional) Seed sample data
python seed_sample_data.py
4. Run app
streamlit run app.py
🧠 Tech Stack
Python
Streamlit
Ollama (local LLM)
JSON (local storage)
📂 Data Storage

All journal entries are stored locally in:

journal_data/YYYY-MM-DD.json
🔒 Privacy
No cloud storage
No tracking
Everything stays on your machine
📌 Future Improvements
Voice journaling
Emotion detection from text
Weekly reports export (PDF)
Multi-user login

---

# ⚡ Important Fix (DO THIS)

Your uploaded file is named:


app(1).py


👉 Rename it to:


app.py


Otherwise Streamlit won’t run correctly.

---

# 🧠 What Each File Does (quick clarity)

### 🧾 app.py
Main UI + agent orchestration  
→ tabs, inputs, buttons, outputs  
(see: :contentReference[oaicite:0]{index=0})

---

### 🤖 agents.py
All agent logic + prompts  
→ Reflection / Reframe / Wellness  
(see: :contentReference[oaicite:1]{index=1})

---

### 💾 storage.py
Handles saving + loading entries  
→ JSON per day  
(see: :contentReference[oaicite:2]{index=2})

---

### 📊 charts.py
Trend visualization  
→ mood graph + emotion frequency  
(see: :contentReference[oaicite:3]{index=3})

---

### 🔌 ollama_client.py
Connects to local LLM  
→ handles errors cleanly  
(see: :contentReference[oaicite:4]{index=4})

---

### 🌱 seed_sample_data.py
Generates 14 days of fake data  
→ helps test charts instantly  
(see: :contentReference[oaicite:5]{index=5})

---

# 🚀 How to Run (quick version)

```bash
ollama serve
streamlit run app.py
💡 Pro Tips (from experience)
If Ollama fails → your app will still run (graceful fallback already built)

Use lighter model if slow:

llama3:8b
mistral
phi3
First run feels empty → use seed script
