import json
import os

def initial_save(sessions, session_categories):
    # Resolve path to sessions_history.json
    history_file = os.path.join(os.path.dirname(__file__), 'sessions_history.json')
    # Load existing history
    try:
        with open(history_file, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    # Append new record and save
    content = {
        "session_id": len(history)+1,
        "session_type": session_categories,
        "session_details": sessions
    }

    history.append(content)
    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

def create_session_save(sessions, session_category):
    # Resolve path to sessions_history.json
    session_file = os.path.join(os.path.dirname(__file__), 'sessions.json')
    
    # # Load existing history
    # try:
    #     with open(session_file, "r") as f:
    #         sessions = json.load(f)
    # except (FileNotFoundError, json.JSONDecodeError):
    #     sessions = []

    # # Update last session with activity timestamps
    # if sessions:
    #     sessions[-1]["session_end"] = session["session_start"]

    # # Extract timestamps from activities list
    # activities = session["activities"]

    # Append new record and save
    sessions[-1]["session_type"] = session_category
    # content = {
    #     "session_id": len(sessions)+1,
    #     "session_type": session_category,
    #     "session_start": session["session_start"],
    #     "session_end": session["session_end"],
    #     "session_activities": session["session_activities"]
    # }

    # sessions.append(content)
    with open(session_file, "w") as f:
        json.dump(sessions, f, indent=4)

def update_session_save(session, session_category):
    # Resolve path to sessions_history.json
    session_file = os.path.join(os.path.dirname(__file__), 'sessions.json')
    
    # Load existing history
    try:
        with open(session_file, "r") as f:
            sessions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        sessions = []

    # Update current session details
    if sessions:
        sessions[-1]["session_activities"] = session["session_activities"]
        sessions[-1]["session_type"] = session_category

    with open(session_file, "w") as f:
        json.dump(sessions, f, indent=4)