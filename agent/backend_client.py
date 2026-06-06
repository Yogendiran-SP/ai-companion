import requests

def send_heartbeat(payload: dict):
    response = requests.post("http://localhost:8000/heartbeat", json=payload)
    return response.json()
