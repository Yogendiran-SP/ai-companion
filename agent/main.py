from app_detector import get_active_window_title
from llm_client import get_suggestion
from backend_client import send_heartbeat
import time
from activity_save import save_record

timestamp = time.ctime()

payload = {
    "agent_id": "agent_001",
    "platform": "Windows",
    "timestamp": timestamp
}

# Send initial heartbeat to backend
response = send_heartbeat(payload)
print(response)

# Main loop to monitor active window and get suggestions
while True:
    (context, record) = get_active_window_title()
    
    # Checking if the app has changed before saving & getting suggestion to history
    if context["current_app"] != context["previous_app"] or context["current_file"] != context["previous_file"]:
        save_record(record)
        suggestion = get_suggestion(record)
        print(suggestion)
    time.sleep(1)