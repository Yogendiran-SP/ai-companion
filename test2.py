record = {
    "session_start": "hello",
    "session_end": "Current Session",
    "activities": [
        {
            "timestamp": "2026-06-10T21:50:33.740138",
            "context_type": "USER_CONTEXT",
            "app": "Visual Studio Code",
            "category": "IDE",
            "context": {
                "file": "session_save.py",
                "project": "ai-companion"
            }
        },
        {
            "timestamp": "2026-06-10T21:58:51.268227",
            "context_type": "USER_CONTEXT",
            "app": "Visual Studio Code",
            "category": "IDE",
            "context": {
                "file": "session_creater.py",
                "project": "ai-companion"
            }
        },
        {
            "timestamp": "2026-06-10T22:01:44.485337",
            "context_type": "USER_CONTEXT",
            "app": "Visual Studio Code",
            "category": "IDE",
            "context": {
                "file": "session_classifier.py",
                "project": "ai-companion"
            }
        }
    ]
}

for num in record["activities"]:
    if num["category"] == "IDE":
        print("Ide")