import os
from dotenv import load_dotenv
from msgraph.core import GraphClient
import requests
from utils.db import test_db
from teammate import run_teammate
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename="teammate.log", filemode="a",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("Test")

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")

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

if __name__ == "__main__":
    client = get_graph_client()
    user = client.me.get()
    logger.info(f"Connected as: {user.display_name}")
    print(f"Connected as: {user.display_name}")

    test_db()

    # Simulate a meeting workflow
    context = {"chat_id": None}  # Shared context
    commands = [
        "Teammate, schedule a meeting at 3 PM",
        "Teammate, tell the team Meeting scheduled for 3 PM",
        "Teammate, take notes",  # Speak "Discuss project timelines" during pause
        "Teammate, stop taking notes",
        "Teammate, present the Q1 slides",
        "Teammate, what’s in row 5 of the Excel file?",
        "Teammate, what do you suggest?",
        "Teammate, tell the team Great discussion today"
    ]

    for cmd in commands:
        logger.info(f"Executing: {cmd}")
        print(f"\nExecuting: {cmd}")
        result = run_teammate(cmd, context)
        context = result.context  # Update context
        logger.info(f"Result: {result.response or 'Processed'}")
        print(f"Result: {result.response or 'Processed'}")
        if "schedule" in cmd:
            time.sleep(2)  # Allow scheduling
        elif "take notes" in cmd and "stop" not in cmd:
            print("Speak 'Discuss project timelines' now...")
            time.sleep(10)  # Time to speak
        elif "present" in cmd or "tell" in cmd:
            time.sleep(3)  # Allow Teams/speech actions
        elif "suggest" in cmd:
            time.sleep(2)  # Allow suggestion generation

    # Check reminder (wait until 2 minutes before 3 PM today/tomorrow)
    logger.info("Waiting for reminders (manual check at 2:58 PM)")
    print("Check Teams for reminders at 2:58 PM today or tomorrow.")