from fastapi import FastAPI

app = FastAPI()

@app.post("/heartbeat")
def heartbeat(payload: dict):
    # print(f"Agent Id: {payload["agent_id"]}")
    # print(f"App Name: {payload.get("active_app", "Unknown Application")}")
    
    return {
        "status": "success",
        "message": "Agent connected"
    }