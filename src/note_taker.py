import os
import azure.cognitiveservices.speech as speechsdk
from utils.db import get_db_connection
from dotenv import load_dotenv
import logging
from msgraph.core import GraphClient
import requests
import threading

# Load environment variables
load_dotenv()
speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NoteTaker")

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

# Global state for note-taking
note_taking_active = False
recognizer = None

def start_note_taking(meeting_id):
    global note_taking_active, recognizer
    logger.info(f"Starting note-taking for meeting ID: {meeting_id}")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.enable_diarization = True
    speech_config.diarization_minimum_number_of_speakers = 1
    speech_config.diarization_maximum_number_of_speakers = 10

    # Use default microphone or stream (Teams audio integration TBD)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    def handle_recognized(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            speaker = evt.result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_RecognitionSpeakerId, "Unknown")
            text = evt.result.text
            logger.info(f"Speaker {speaker}: {text}")
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO minutes (meeting_id, speaker, text) VALUES (%s, %s, %s);",
                (meeting_id, speaker, text)
            )
            conn.commit()
            cur.close()
            conn.close()

    recognizer.recognized.connect(handle_recognized)
    recognizer.start_continuous_recognition()
    note_taking_active = True

def stop_note_taking():
    global note_taking_active, recognizer
    if note_taking_active and recognizer:
        recognizer.stop_continuous_recognition()
        note_taking_active = False
        recognizer = None
        logger.info("Stopped note-taking")

def take_notes(state):
    """Handle note-taking command."""
    logger.info(f"Processing note-taking command: {state.input}")
    command = state.input.lower().replace("teammate", "").strip()

    if "take notes" in command or "start taking notes" in command:
        # Assume a meeting exists (enhance with meeting context later)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM meetings ORDER BY start_time DESC LIMIT 1;")
        meeting_id = cur.fetchone()
        if not meeting_id:
            state.context["response"] = "No recent meeting found to take notes for."
            cur.close()
            conn.close()
            return state
        meeting_id = meeting_id[0]
        cur.close()
        conn.close()

        if not note_taking_active:
            threading.Thread(target=start_note_taking, args=(meeting_id,), daemon=True).start()
            state.context["response"] = f"Started taking notes for meeting ID {meeting_id}."
        else:
            state.context["response"] = "Already taking notes."
    
    elif "stop taking notes" in command:
        if note_taking_active:
            stop_note_taking()
            state.context["response"] = "Stopped taking notes."
        else:
            state.context["response"] = "Not currently taking notes."
    
    else:
        state.context["response"] = "Unrecognized note-taking command."
    
    return state

if __name__ == "__main__":
    state = {"input": "Teammate, take notes", "context": {}, "action_taken": True}
    result = take_notes(state)
    print(result)