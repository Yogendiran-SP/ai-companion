from google import genai
from dotenv import load_dotenv
import os, json

def get_suggestion(record:dict, session:dict):
    load_dotenv()
    API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=API_KEY)

    # Resolve path to history.json
    history_file = os.path.join(os.path.dirname(__file__), 'history.json')
    
    with open(history_file, "r") as f:
        history = json.load(f)

    recent_history = history[:-1][-10:] # Get the last 10 records excluding the current one from history
    # print(record) # Debugging statement
    content = {
        "app": record["app"],
        "context": record["context"],
        "recent_history": recent_history,
        "current_session_details": session
    }

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"Here is the current context of the user's activity: {content}. Based on this context, provide useful suggestions to enhance the user's productivity or experience in ONLY 3 lines."
    )

    return response.text.strip()
