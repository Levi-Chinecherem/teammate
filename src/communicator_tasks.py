from celery import Celery
from dotenv import load_dotenv
from communicator import send_message
import os

load_dotenv()
redis_url = os.getenv("REDIS_URL")
app = Celery("communicator", broker=redis_url)

@app.task
def send_message_task(state):
    return send_message(state)