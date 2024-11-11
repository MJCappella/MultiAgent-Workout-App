from langflow.load import run_flow_from_json
from dotenv import load_env

load_env()


TWEAKS = {
  "TextInput-rZLTH": {
    "input_value": "question"
  },
 
  "TextInput-EO1Ku": {
    "input_value": "profile"
  },
}

result = run_flow_from_json(flow="AskAI.json",
                            input_value="message",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)