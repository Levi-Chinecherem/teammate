from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from transformers import pipeline
import logging
from scheduler import schedule_meeting
from note_taker import take_notes
from presenter import deliver_presentation
from communicator import send_message
from document_reader import read_document_agent as read_document
from suggestor import make_suggestion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Teammate")

# Define state model with richer context
class TeammateState(BaseModel):
    input: str  # User command
    context: Dict[str, Any]  # Meeting ID, chat ID, etc.
    action_taken: bool = False  # Whether to proceed
    response: str = ""  # Response to user

# NLP pipeline for intent detection (more robust)
nlp = pipeline("text-classification", model="distilbert-base-uncased", return_all_scores=True)

def detect_intent(command: str) -> str:
    """Detect intent with NLP and keyword fallback."""
    command = command.lower().replace("teammate", "").strip()
    intents = {
        "schedule": ["schedule", "meeting", "set up", "plan"],
        "notes": ["take notes", "record", "minutes", "start taking", "stop taking"],
        "present": ["present", "slides", "show", "display"],
        "message": ["send", "tell", "call", "say", "remind"],
        "read": ["read", "what’s in", "summarize", "open"],
        "suggest": ["suggest", "what do you think", "recommend", "idea"]
    }

    # NLP-based scoring
    scores = nlp(command)
    intent_scores = {intent: 0.0 for intent in intents}
    for label, score in scores[0]:
        for intent, keywords in intents.items():
            if any(keyword in label for keyword in keywords):
                intent_scores[intent] += score["score"]

    # Keyword fallback
    for intent, keywords in intents.items():
        if any(keyword in command for keyword in keywords):
            intent_scores[intent] += 1.0  # Boost for exact matches

    detected_intent = max(intent_scores, key=intent_scores.get)
    if intent_scores[detected_intent] < 0.5:  # Threshold for confidence
        return "unknown"
    return detected_intent

def listen_for_name(state: TeammateState) -> TeammateState:
    """Check if Teammate is called and handle ignore commands."""
    logger.info(f"Received input: {state.input}")
    if "teammate" in state.input.lower():
        if "ignore" in state.input.lower() or "don’t" in state.input.lower():
            state.action_taken = False
            state.response = "Command ignored as requested."
            logger.info("Ignoring command")
        else:
            state.action_taken = True
            logger.info("Teammate activated")
    else:
        state.action_taken = False
    return state

def route_to_agent(state: TeammateState) -> str:
    """Route command to appropriate sub-agent."""
    if not state.action_taken:
        logger.info("No action taken, ending flow")
        return END
    
    intent = detect_intent(state.input)
    logger.info(f"Detected intent: {intent}")
    
    intent_map = {
        "schedule": "scheduler",
        "notes": "notetaker",
        "present": "presenter",
        "message": "communicator",
        "read": "document_reader",
        "suggest": "suggestor"
    }
    
    if intent in intent_map:
        return intent_map[intent]
    state.response = "Unrecognized command. Please try again."
    return END

# Build the workflow
workflow = StateGraph(TeammateState)
workflow.add_node("listener", listen_for_name)
workflow.add_node("scheduler", schedule_meeting)
workflow.add_node("notetaker", take_notes)
workflow.add_node("presenter", deliver_presentation)
workflow.add_node("communicator", send_message)
workflow.add_node("document_reader", read_document)
workflow.add_node("suggestor", make_suggestion)

workflow.add_conditional_edges("listener", route_to_agent, {
    "scheduler": "scheduler",
    "notetaker": "notetaker",
    "presenter": "presenter",
    "communicator": "communicator",
    "document_reader": "document_reader",
    "suggestor": "suggestor",
    END: END
})

workflow.set_entry_point("listener")
teammate = workflow.compile()

def run_teammate(command: str, initial_context: Dict[str, Any] = None) -> TeammateState:
    """Run Teammate with a command and optional context."""
    initial_state = TeammateState(input=command, context=initial_context or {})
    result = teammate.invoke(initial_state)
    return result

if __name__ == "__main__":
    test_commands = [
        "Teammate, schedule a meeting at 3 PM",
        "Teammate, take notes",
        "Teammate, present the Q1 slides",
        "Teammate, tell the team we’re starting",
        "Teammate, what’s in row 5 of the Excel file?",
        "Teammate, what do you suggest?",
        "Teammate, ignore this",
        "Random text"
    ]
    for cmd in test_commands:
        print(f"\nTesting: {cmd}")
        result = run_teammate(cmd)
        print(f"Result: {result.response or 'Processed'}")