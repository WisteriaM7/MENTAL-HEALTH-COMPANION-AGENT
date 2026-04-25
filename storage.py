import json
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_DIR = Path("journal_data")
DATA_DIR.mkdir(exist_ok=True)


def _path_for_date(d: date) -> Path:
    return DATA_DIR / f"{d.isoformat()}.json"


def save_entry(mood: int, emotions: list, journal: str, gratitude: str, results: dict):
    today = date.today()
    record = {
        "date":      today.isoformat(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood":      mood,
        "emotions":  emotions,
        "journal":   journal,
        "gratitude": gratitude,
        "results":   results,
    }
    with open(_path_for_date(today), "w") as f:
        json.dump(record, f, indent=2)


def load_today_entry() -> dict | None:
    path = _path_for_date(date.today())
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def delete_today_entry():
    path = _path_for_date(date.today())
    if path.exists():
        path.unlink()


def load_all_entries() -> list:
    entries = []
    for path in sorted(DATA_DIR.glob("????-??-??.json")):
        try:
            with open(path) as f:
                entries.append(json.load(f))
        except Exception:
            pass
    return entries


def load_entries_last_n_days(n: int) -> list:
    today  = date.today()
    cutoff = today - timedelta(days=n)
    return [
        e for e in load_all_entries()
        if date.fromisoformat(e["date"]) >= cutoff
    ]
