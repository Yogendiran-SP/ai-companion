from datetime import datetime

# Modify this to session classification
def session_classification(session):

    WEIGHTS = {
        "IDE": 3,
        "TERMINAL": 2,
        "SETTINGS": 3,
        "FILE EXPLORER": 1,
        "BROWSER": 0
    }

    weight = {
        "CODING": 0,
        "LEARNING": 0,
        "SYSTEM_CONFIGURATION": 0,
        "ENTERTAINMENT": 0
    }

    for activity in session["session_activities"]:
        if activity["category"] == "IDE":
            weight["CODING"] += WEIGHTS["IDE"]
        elif activity["category"] == "TERMINAL":
            weight["CODING"] += WEIGHTS["TERMINAL"]
        elif activity["category"] == "SETTINGS":
            weight["SYSTEM_CONFIGURATION"] += WEIGHTS["SETTINGS"]
        elif activity["category"] == "FILE EXPLORER":
            weight["CODING"] += WEIGHTS["FILE EXPLORER"]
            weight["SYSTEM_CONFIGURATION"] += WEIGHTS["FILE EXPLORER"]
    
    return max(weight, key=weight.get)

def classify_session(session):

    WEIGHTS = {
        "IDE": 3,
        "TERMINAL": 2,
        "SETTINGS": 3,
        "FILE EXPLORER": 1,
        "BROWSER": 0
    }

    weight = {
        "CODING": 0,
        "LEARNING": 0,
        "SYSTEM_CONFIGURATION": 0,
        "ENTERTAINMENT": 0
    }

    # Support multiple session formats:
    # - {'session_details': {'activities': [...]}}
    # - {'activities': [...]} (flat)
    # - a list of activity dicts
    if isinstance(session, dict) and "session_details" in session and isinstance(session["session_details"], dict) and "activities" in session["session_details"]:
        activities = session["session_details"]["activities"]
    elif isinstance(session, dict) and "activities" in session:
        activities = session["activities"]
    elif isinstance(session, list):
        activities = session
    else:
        activities = []

    for activity in activities:
        cat = activity.get("category")
        if cat == "IDE":
            weight["CODING"] += WEIGHTS["IDE"]
        elif cat == "TERMINAL":
            weight["CODING"] += WEIGHTS["TERMINAL"]
        elif cat == "BROWSER":
            weight["CODING"] += WEIGHTS["BROWSER"]
            weight["LEARNING"] += WEIGHTS["BROWSER"]
            weight["ENTERTAINMENT"] += WEIGHTS["BROWSER"]
        elif cat == "FILE EXPLORER":
            weight["SYSTEM_CONFIGURATION"] += WEIGHTS["FILE EXPLORER"]
        elif cat == "SETTINGS":
            weight["SYSTEM_CONFIGURATION"] += WEIGHTS["SETTINGS"]
        
    category = max(weight, key=weight.get)
    weight = {key: 0 for key in weight}

    return category