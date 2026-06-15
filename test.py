from datetime import datetime
import time

# p = datetime.now().isoformat()
# print(f"p: {p}")

# time.sleep(5)

# c = datetime.now().isoformat()
# print(f"c: {c}")

# prev = datetime.fromisoformat(p)
# curr = datetime.fromisoformat(c)

# diff = curr - prev
# d = curr.timestamp() - prev.timestamp()
# print(type(prev))
# print(f"{d:.6f}s")
# print(diff.total_seconds())

record = [
    {
        "timestamp": "2026-06-08T18:05:52.184927",
        "context_type": "SYSTEM_CONTEXT",
        "app": "Windows Terminal",
        "category": "TERMINAL",
        "context": {
            "directory": "C:\\Users\\Joel\\Joshua\\AI Companion\\ai-companion"
        }
    },
    {
        "timestamp": "2026-06-08T18:05:55.923767",
        "context_type": "USER_CONTEXT",
        "app": "Visual Studio Code",
        "category": "IDE",
        "context": {
            "file": "app_detector.py",
            "project": "ai-companion"
        }
    },
    {
        "timestamp": "2026-06-08T18:15:41.309726",
        "context_type": "SYSTEM_CONTEXT",
        "app": "Windows Terminal",
        "category": "TERMINAL",
        "context": {
            "directory": "C:\\Users\\Joel\\Joshua\\AI Companion\\ai-companion"
        }
    },
    {
        "timestamp": "2026-06-08T18:45:45.120349",
        "context_type": "USER_CONTEXT",
        "app": "Visual Studio Code",
        "category": "IDE",
        "context": {
            "file": "history.json",
            "project": "ai-companion"
        }
    },
    {
        "timestamp": "2026-06-08T19:17:32.467244",
        "context_type": "USER_CONTEXT",
        "app": "File Explorer",
        "category": "FILE EXPLORER",
        "context": {
            "tab_title": "agent",
            "directory": "Joel\\Joshua\\AI Companion\\ai-companion\\agent"
        }
    },
    {
        "timestamp": "2026-06-08T19:19:37.547211",
        "context_type": "USER_CONTEXT",
        "app": "Visual Studio Code",
        "category": "IDE",
        "context": {
            "file": "app_detector.py",
            "project": "ai-companion"
        }
    }
]

sessions=[]
session_start = record[0]["timestamp"].replace("T", " ").split(".")[0]
session_end = "Current Session"
session={
    "session_start": session_start,
    "session_end": session_end,
    "activities": [record[0]]
}
for i in range(1,len(record)):
    p = int(datetime.fromisoformat(record[i-1]["timestamp"]).timestamp())
    c = int(datetime.fromisoformat(record[i]["timestamp"]).timestamp())
    if ((c-p))<1800:
        session["activities"].append(record[i])
        # print(record[i])
    else:
        # print("Session overed\n")
        session_end = record[i]["timestamp"].replace("T", " ").split(".")[0]
        session["session_end"] = session_end
        sessions.append(session)
        session_start = record[i]["timestamp"].replace("T", " ").split(".")[0]
        session_end = "Current Session"
        session={
            "session_start": session_start,
            "session_end": session_end,
            "activities": []
        }
        session["activities"].append(record[i])
# Current session (Last session in sessions)
sessions.append(session)

# for session in sessions:
#     print(session,"\n")
# j=1
# for i in sessions:
#     print(f"Session {j}")
#     print(i,"\n")
#     j+=1

# print(f"Current Session:\n{sessions[len(sessions)-1]}")
    # print(f"c:{c}\np:{p}\nc-p:{c-p}")

import json
with open("src/agent/history.json", "r") as f:
    activities = json.load(f)
print(type(activities))

categories = []
curr_categories = []

for session in sessions:
    for activity in session["activities"]:
        if activity["category"] not in curr_categories:
            curr_categories.append(activity["category"])
    categories.append(curr_categories)
    curr_categories = []
    
WEIGHTS = {
    "IDE": 3,
    "TERMINAL": 2,
    "SETTINGS": 3,
    "FILE EXPLORER": 1,
    "BROWSERS": 0
}

weight = {
    "CODING": 0,
    "LEARNING": 0,
    "SYSTEM_CONFIGURATION": 0,
    "ENTERTAINMENT": 0
}
# print()
# for i in categories:
#     print(f"{i}")

i=1
for curr_categories in categories:
    print(f"Session{i}")
    if ("IDE" in curr_categories):
        weight["CODING"] += WEIGHTS["IDE"]
    if ("TERMINAL" in curr_categories):
        weight["CODING"] += WEIGHTS["TERMINAL"]
    if ("BROWSER" in curr_categories):
        weight["CODING"] += WEIGHTS["BROWSERS"]
        weight["LEARNING"] += WEIGHTS["BROWSERS"]
        weight["ENTERTAINMENT"] += WEIGHTS["BROWSERS"]
    if ("SETTINGS" in curr_categories):
        weight["SYSTEM_CONFIGURATION"] += WEIGHTS["SETTINGS"]
    if ("FILE EXPLORER" in curr_categories):
        weight["SYSTEM_CONFIGURATION"] += WEIGHTS["SETTINGS"]
    i += 1

    print(max(weight, key=weight.get))
    weight = {key: 0 for key in weight}