import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.app_extractors.app_detector import get_active_window_title
from src.agent.llm_client import get_suggestion
from src.agent.backend_client import send_heartbeat
import time
from src.app_extractors.activity_save import save_record
from src.session_extractors.session_manager import session_manager

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
        curr_session = session_manager()
        if curr_session:
            suggestion = get_suggestion(record, curr_session)
            print(suggestion)
    time.sleep(1)