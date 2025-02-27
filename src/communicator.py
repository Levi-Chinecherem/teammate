import os
import azure.cognitiveservices.speech as speechsdk
from msgraph.core import GraphClient
import requests
from utils.db import get_db_connection
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")
team_id = os.getenv("TEAM_ID")  # New: Teams team ID
channel_id = os.getenv("CHANNEL_ID")  # New: Teams channel ID

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Communicator")

# Graph API client
def get_graph_client():
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(auth_url, data=auth_data)
    token = response.json().get("access_token")
    return GraphClient(api_version="v1.0", access_token=token)

# Speech synthesis
def speak(text):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        logger.error(f"Speech synthesis failed: {result.reason}")

def send_message(state):
    """Handle communication commands."""
    logger.info(f"Processing communication command: {state.input}")
    command = state.input.lower().replace("teammate", "").strip()
    client = get_graph_client()

    # Validate essential environment variables
    if not all([team_id, channel_id]):
        state.context["response"] = "Error: TEAM_ID or CHANNEL_ID not configured in environment."
        return state

    # Parse command
    if "tell" in command or "send" in command:
        # Extract recipient and content
        if "to" in command:
            parts = command.split("to")
            content = parts[0].replace("tell", "").replace("send", "").strip()
            recipient_part = parts[1].strip()
        else:
            content = command.replace("tell", "").replace("send", "").strip()
            recipient_part = "team"  # Default to group chat

        if "team" in recipient_part:
            # Send to the configured Teams channel
            try:
                client.teams[team_id].channels[channel_id].messages.post({
                    "body": {"content": content}
                })
                recipient = "team"
            except Exception as e:
                state.context["response"] = f"Failed to send message to team: {str(e)}"
                return state
        else:
            # Individual chat (basic parsing for now)
            recipient = recipient_part.strip() or "user@example.com"  # Fallback if not parsed
            try:
                chat = client.users[recipient].chats.post({"chatType": "oneOnOne"})
                client.chats[chat.id].messages.post({"body": {"content": content}})
            except Exception as e:
                state.context["response"] = f"Failed to send message to {recipient}: {str(e)}"
                return state
        
        log_communication("text", recipient, content)
        state.context["response"] = f"Sent message to {recipient}: '{content}'"

    elif "call" in command:
        recipient = command.replace("call", "").strip() or "user@example.com"
        # Simulate call (client credentials can't initiate real calls)
        logger.info(f"Simulating call to {recipient}")
        log_communication("call", recipient, "Call initiated")
        state.context["response"] = f"Simulated call to {recipient} (real calls TBD)"

    elif "say" in command:
        content = command.replace("say", "").strip()
        speak(content)
        log_communication("speech", "meeting", content)
        state.context["response"] = f"Spoke in meeting: '{content}'"

    else:
        state.context["response"] = "Unrecognized communication command."

    return state

def log_communication(type_: str, recipient: str, content: str):
    """Log communication to database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO communications (type, recipient, content) VALUES (%s, %s, %s);",
        (type_, recipient, content)
    )
    conn.commit()
    cur.close()
    conn.close()
    logger.info(f"Logged {type_} communication to {recipient}: {content}")

if __name__ == "__main__":
    state = {"input": "Teammate, tell the team we’re starting", "context": {}, "action_taken": True}
    result = send_message(state)
    print(result)