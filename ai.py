from langflow.load import run_flow_from_json
from dotenv import load_env
import requests
from typing import Optional
import os

load_env()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "c063f01a-4a05-45a1-94e9-bc96716d7a8b"
APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")

# runs the ask_ai flow
def ask_ai(profile, question):
    TWEAKS = {
    "TextInput-rZLTH": {
        "input_value": question
    },
    
    "TextInput-EO1Ku": {
        "input_value": profile
    },
    }

    result = run_flow_from_json(flow="AskAI.json",
                                input_value="message",
                                session_id="", # provide a session id if you want to use session state
                                fallback_to_env_vars=True, # False by default
                                tweaks=TWEAKS)

    return (result[0].outputs[0].results["text"]. data["text"])

# macro flow inputs
def get_macros(profile, goals):
    TWEAKS = {
        "TextInput-qB2eg": {
            "input_value": "goals"
        },
        "TextInput-MXtnA": {
            "input_value": "profile"
        },
    }
    return run_flow("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)

# runs the macro flow
def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]


result = get_macros("name:mike, age:22, weight:70kgs, 175cm", "I want to lose weight")
print(result)