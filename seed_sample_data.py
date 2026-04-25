"""
Run this script once to generate 14 days of sample journal entries.
This lets you immediately test the Wellness Trends charts.

Usage:
    python seed_sample_data.py
"""

import json
from datetime import date, timedelta
from pathlib import Path
import random

DATA_DIR = Path("journal_data")
DATA_DIR.mkdir(exist_ok=True)

SAMPLE_ENTRIES = [
    (4, ["Grateful", "Calm"],        "Had a good morning walk. Felt clear-headed.",          "Morning light"),
    (3, ["Tired", "Neutral"],        "Long day at work. Nothing particularly bad though.",   "Hot tea"),
    (2, ["Overwhelmed", "Anxious"],  "Deadline pressure. Hard to focus. Mind racing.",       "My desk plant"),
    (4, ["Happy", "Connected"],      "Caught up with an old friend over lunch.",             "That conversation"),
    (3, ["Focused", "Calm"],         "Productive day. Got a lot done.",                      "The quiet afternoon"),
    (5, ["Happy", "Energised"],      "Weekend hiking trip. Felt alive.",                     "Fresh air"),
    (4, ["Content", "Grateful"],     "Lazy morning. Read a book.",                           "No alarm today"),
    (2, ["Sad", "Lonely"],           "Missing people. Not sure why I feel so flat today.",   "My warm bed"),
    (3, ["Tired", "Hopeful"],        "Starting to feel better. Slow but okay.",              "Progress, however small"),
    (4, ["Calm", "Content"],         "Cooked a proper meal. Small win.",                     "Good food"),
    (3, ["Anxious", "Focused"],      "Presentation today. Nervous but it went okay.",        "It went okay"),
    (4, ["Happy", "Grateful"],       "Weekend. Rested well.",                                "Sleep"),
    (5, ["Energised", "Connected"],  "Great day. Everything clicked.",                       "Momentum"),
    (3, ["Calm", "Tired"],           "Quiet day. Nothing major. Just here.",                 "Being here"),
]

today = date.today()

for i, (mood, emotions, journal, gratitude) in enumerate(reversed(SAMPLE_ENTRIES)):
    entry_date = today - timedelta(days=len(SAMPLE_ENTRIES) - i)
    path = DATA_DIR / f"{entry_date.isoformat()}.json"
    if path.exists():
        print(f"  Skipping {entry_date} (already exists)")
        continue
    record = {
        "date":      entry_date.isoformat(),
        "timestamp": f"{entry_date.isoformat()} 20:00:00",
        "mood":      mood,
        "emotions":  emotions,
        "journal":   journal,
        "gratitude": gratitude,
        "results":   {},
    }
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    print(f"  Created {entry_date}: mood={mood}, emotions={emotions}")

print(f"\nDone. {len(SAMPLE_ENTRIES)} sample entries created in journal_data/")
print("Now run: streamlit run app.py  and check the Wellness Trends tab.")
