import json
from datetime import datetime

def save_record(record):
    # Load existing history
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    # Append new record and save
    history.append(record)
    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)