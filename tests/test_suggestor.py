import os
from dotenv import load_dotenv
from msgraph.core import GraphClient
import requests
from utils.db import test_db
from teammate import run_teammate
import time

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
    print(f"Connected as: {user.display_name}")

    test_db()

    # Test all sub-agents
    commands = [
        "Teammate, schedule a meeting at 3 PM",
        "Teammate, take notes",  # Run, speak "Test discussion", then stop after 5s
        "Teammate, present the Q1 slides",
        "Teammate, tell the team we’re starting",
        "Teammate, what’s in row 5 of the Excel file?",
        "Teammate, what do you suggest?"
    ]
    for cmd in commands:
        print(f"\nTesting: {cmd}")
        result = run_teammate(cmd)
        print(f"Result: {result.context.get('response', 'No response')}")
        if "take notes" in cmd:
            time.sleep(5)  # Speak "Test discussion" into mic
            result = run_teammate("Teammate, stop taking notes")
            print(f"Stop notes: {result.context.get('response', 'No response')}")
        time.sleep(1)