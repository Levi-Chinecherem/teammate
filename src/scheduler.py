import os
from datetime import datetime, timedelta
from msgraph.core import GraphClient
import requests
from pydantic import BaseModel
from utils.db import get_db_connection
from celery import Celery
from dotenv import load_dotenv
import logging
from communicator import send_message

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
redis_url = os.getenv("REDIS_URL")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Scheduler")

# Celery setup with Render Redis
app = Celery("scheduler", broker=redis_url)

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

# Pydantic model for meeting data
class Meeting(BaseModel):
    title: str
    start_time: datetime
    attendees: list[str]

# Celery task for sending reminders
# @app.task
# def send_reminder(attendee: str, method: str, meeting_title: str):
#     client = get_graph_client()
#     if method == "text":
#         chat = client.users[attendee].chats.post({"chatType": "oneOnOne"})
#         client.chats[chat.id].messages.post({
#             "body": {"content": f"Reminder: '{meeting_title}' starts in 2 minutes!"}
#         })
#     elif method == "call":
#         # Placeholder for Teams call (limited in client credentials flow)
#         logger.info(f"Simulating call to {attendee} for {meeting_title}")
#     logger.info(f"Sent {method} reminder to {attendee}")

# Update schedule_meeting to use send_message
def schedule_meeting(state):
    logger.info(f"Scheduling meeting with input: {state.input}")
    command = state.input.lower().replace("teammate", "").strip()
    
    if "at" not in command:
        state.context["response"] = "Please specify a time (e.g., 'at 3 PM')."
        return state
     
    parts = command.split("at")
    title = parts[0].replace("schedule a meeting", "").strip() or "Team Meeting"
    time_str = parts[1].strip()
    
    try:
        start_time = datetime.strptime(f"{datetime.now().date()} {time_str}", "%Y-%m-%d %I %p")
        if start_time < datetime.now():
            start_time += timedelta(days=1)
    except ValueError:
        state.context["response"] = "Invalid time format. Use '3 PM' or similar."
        return state

    attendees = ["user@example.com"]

    client = get_graph_client()
    event = {
        "subject": title,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": (start_time + timedelta(hours=1)).isoformat(), "timeZone": "UTC"},
        "attendees": [{"emailAddress": {"address": email}} for email in attendees]
    }
    response = client.me.events.post(event)
    event_id = response.id
    logger.info(f"Scheduled meeting: {title} at {start_time}, ID: {event_id}")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO meetings (title, start_time, attendees) VALUES (%s, %s, %s) RETURNING id;",
        (title, start_time, attendees)
    )
    db_meeting_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    reminder_time = start_time - timedelta(minutes=2)
    for attendee in attendees:
        reminder_state = {
            "input": f"Teammate, tell {attendee} Reminder: '{title}' starts in 2 minutes",
            "context": {},
            "action_taken": True
        }
        app.send_task("communicator_tasks.send_message", args=[reminder_state], eta=reminder_time)
        reminder_state["input"] = f"Teammate, call {attendee}"
        app.send_task("communicator_tasks.send_message", args=[reminder_state], eta=reminder_time)

    state.context["response"] = f"Scheduled '{title}' at {time_str} with ID {db_meeting_id}."
    return state

def schedule_meeting(state):
    """Schedule a meeting and set reminders."""
    logger.info(f"Scheduling meeting with input: {state.input}")
    command = state.input.lower().replace("teammate", "").strip()
    
    if "at" not in command:
        state.context["response"] = "Please specify a time (e.g., 'at 3 PM')."
        return state
     
    parts = command.split("at")
    title = parts[0].replace("schedule a meeting", "").strip() or "Team Meeting"
    time_str = parts[1].strip()
    
    try:
        start_time = datetime.strptime(f"{datetime.now().date()} {time_str}", "%Y-%m-%d %I %p")
        if start_time < datetime.now():
            start_time += timedelta(days=1)  # Assume next day if past
    except ValueError:
        state.context["response"] = "Invalid time format. Use '3 PM' or similar."
        return state

    attendees = ["user@example.com"]  # Hardcoded for now; enhance later

    # Schedule via Graph API
    client = get_graph_client()
    event = {
        "subject": title,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": (start_time + timedelta(hours=1)).isoformat(), "timeZone": "UTC"},
        "attendees": [{"emailAddress": {"address": email}} for email in attendees]
    }
    response = client.me.events.post(event)
    event_id = response.id
    logger.info(f"Scheduled meeting: {title} at {start_time}, ID: {event_id}")

    # Store in database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO meetings (title, start_time, attendees) VALUES (%s, %s, %s) RETURNING id;",
        (title, start_time, attendees)
    )
    db_meeting_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Schedule reminders with Render Redis
    reminder_time = start_time - timedelta(minutes=2)
    for attendee in attendees:
        send_reminder.apply_async(args=[attendee, "text", title], eta=reminder_time)
        send_reminder.apply_async(args=[attendee, "call", title], eta=reminder_time)

    state.context["response"] = f"Scheduled '{title}' at {time_str} with ID {db_meeting_id}."
    return state

if __name__ == "__main__":
    state = {"input": "Teammate, schedule a meeting at 3 PM", "context": {}, "action_taken": True}
    result = schedule_meeting(state)
    print(result)