import os
from transformers import pipeline
from utils.db import get_db_connection
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Suggestor")

# GPT-like model for text generation
suggestor = pipeline("text-generation", model="gpt2", max_length=50)

def get_meeting_context() -> str:
    """Retrieve recent meeting minutes from database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.title, mi.text
        FROM meetings m
        LEFT JOIN minutes mi ON m.id = mi.meeting_id
        ORDER BY m.start_time DESC
        LIMIT 5;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        return "No recent meeting context available."
    
    context = "Recent meeting discussion:\n"
    for title, text in rows:
        if text:
            context += f"- {title}: {text}\n"
    return context

def make_suggestion(state):
    """Generate a suggestion based on meeting context."""
    logger.info(f"Processing suggestion command: {state.input}")
    command = state.input.lower().replace("teammate", "").strip()

    if "suggest" not in command and "what do you think" not in command:
        state.context["response"] = "Please ask for a suggestion (e.g., 'what do you suggest?')."
        return state

    # Get context from recent minutes
    context = get_meeting_context()
    logger.info(f"Meeting context: {context}")

    # Generate suggestion
    prompt = f"{context}\nBased on this, I suggest: "
    try:
        suggestion = suggestor(prompt, num_return_sequences=1, max_length=100)[0]["generated_text"]
        suggestion = suggestion[len(prompt):].strip()  # Extract suggestion part
        if not suggestion:
            suggestion = "No specific suggestion generated."
    except Exception as e:
        suggestion = f"Error generating suggestion: {str(e)}"

    state.context["response"] = f"Suggestion: {suggestion}"
    logger.info(f"Generated suggestion: {suggestion}")
    return state

if __name__ == "__main__":
    state = {"input": "Teammate, what do you suggest?", "context": {}, "action_taken": True}
    result = make_suggestion(state)
    print(result)