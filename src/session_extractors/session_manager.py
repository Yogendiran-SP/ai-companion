import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.session_extractors.session_creater import update_sessions
from src.session_extractors.session_classifier import classify_session, session_classification
from src.session_extractors.session_save import update_session_save, create_session_save
import json


def session_manager():
    
    (sessions, flag) = update_sessions()
    
    # Handle case where sessions is empty
    if not sessions:
        print("Warning: No sessions available yet")
        return None
    
    # app_session_category = classify_session(sessions[-1])
    session_category = session_classification(sessions[-1])

    # Resolve path to sessions.json
    sessions_file = os.path.join(os.path.dirname(__file__), 'sessions.json')

    try:
        if flag:
            create_session_save(sessions, session_category)
        else:
            update_session_save(sessions[-1], session_category)
        
        # Sessions are already saved in update_sessions()
        with open(sessions_file, "r") as f:
            all_session = json.load(f)
        
        if all_session:
            return all_session[-1]
        else:
            return None

    except Exception as e:
        print(f"Error in session manager: {e}")
        import traceback
        traceback.print_exc()
        return None