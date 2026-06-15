import json
import os

def save_record(record):
    # Resolve path to history.json in the agent directory
    history_file = os.path.join(os.path.dirname(__file__), '../agent/history.json')
    
    # Load existing history
    try:
        with open(history_file, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    # Append new record and save
    history.append(record)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)