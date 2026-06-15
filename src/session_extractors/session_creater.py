from datetime import datetime
import json
import os

def build_sessions(activities):
    sessions=[]

    session_start = activities[0]["timestamp"].replace("T", " ").split(".")[0]
    session_end = "current session"
    
    session={
        "session_start": session_start,
        "session_end": session_end,
        "activities": [activities[0]],
    }
    
    
    for i in range(1,len(activities)):
        prev = int(datetime.fromisoformat(activities[i-1]["timestamp"]).timestamp())
        curr = int(datetime.fromisoformat(activities[i]["timestamp"]).timestamp())
        
        if ((curr-prev)<1800):
            session["activities"].append(activities[i]) # Storing the activity
        else:
            session_end = activities[i]["timestamp"].replace("T", " ").split(".")[0]
            session["session_end"] = session_end
            sessions.append(session) # Storing the session
            session_start = activities[i]["timestamp"].replace("T", " ").split(".")[0]
            session_end = "current session"

            session={
                "session_start": session_start,
                "session_end": session_end,
                "activities": [activities[i]]
            } # Creating new session
        
    sessions.append(session) # Storing Current Session

    return sessions

def update_sessions():
    flag = False # Finding the creation of new session

    # Resolve path to sessions.json and history.json
    sessions_file = os.path.join(os.path.dirname(__file__), 'sessions.json')
    history_file = os.path.join(os.path.dirname(__file__), '../agent/history.json')
    
    # Loading the last session
    try:
        with open(sessions_file, "r") as f:
            sessions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        sessions = []

    # Loading the last activity
    try:
        with open(history_file, "r") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    # Handle case where history has less than 2 items
    if len(history) < 2:
        if len(history) == 1:
            curr = history[0]
            if not sessions:
                # Creating first session
                record = {
                    "session_start": curr["timestamp"].replace("T", " ").split(".")[0],
                    "session_end": "Current Session",
                    "session_activities": [curr]
                }
                flag = True
                sessions.append(record)
                
                # Save sessions to file
                with open(sessions_file, "w") as f:
                    json.dump(sessions, f, indent=4)
            
            return (sessions, flag)
        else:
            # No history yet
            return ([], False)
    
    prev = history[-2]
    curr = history[-1]

    if not sessions:
        # Creating a new session
        record = {
            "session_id": 1,
            "session_type": "Unknown Type",
            "session_start": curr["timestamp"].replace("T", " ").split(".")[0],
            "session_end": "Current Session",
            "session_activities": [curr]
        }

        flag = True

        # Storing current new session
        sessions.append(record)

        return (sessions, flag)

    else:
        flag = False
        curr_session = sessions[-1]

    prev_time = int(datetime.fromisoformat(prev["timestamp"]).timestamp())
    curr_time = int(datetime.fromisoformat(curr["timestamp"]).timestamp())

    if (curr_time - prev_time) < 180:
        # Appending into current session
        curr_session["session_activities"].append(curr)
        sessions[-1] = curr_session
    
    else:
        # Closing the previous session
        curr_session["session_end"] = curr["timestamp"].replace("T", " ").split(".")[0]
        sessions[-1] = curr_session
        
        # Creating a new session
        record = {
            "session_id": len(sessions)+1,
            "session_type": "Unknown Category",
            "session_start": curr["timestamp"].replace("T", " ").split(".")[0],
            "session_end": "Current Session",
            "session_activities": [curr]
        }
        flag = True

        # Append the session
        sessions.append(record)

    # # Save sessions to file
    # with open(sessions_file, "w") as f:
    #     json.dump(sessions, f, indent=4)
    
    return (sessions, flag)