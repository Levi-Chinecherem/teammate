# Teammate: An Intelligent Multi-Agent AI Teammate

![Project Status](https://img.shields.io/badge/status-in%20development-orange)
![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)
![Teams](https://img.shields.io/badge/integration-Microsoft%20Teams-blue?logo=microsoftteams)
![Stars](https://img.shields.io/github/stars/Levi-Chinecherem/teammate?style=social)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)
![Author](https://img.shields.io/badge/author-Levi%20Chinecherem%20Chidi-blue)
![Repo Size](https://img.shields.io/github/repo-size/Levi-Chinecherem/teammate)
![Last Commit](https://img.shields.io/github/last-commit/Levi-Chinecherem/teammate)
![Coverage](https://img.shields.io/badge/coverage-0%25-red)
![Pull Requests](https://img.shields.io/github/issues-pr/Levi-Chinecherem/teammate)
![Issues](https://img.shields.io/github/issues/Levi-Chinecherem/teammate)
![Celery](https://img.shields.io/badge/tasks-Celery-green?logo=celery)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-blue?logo=postgresql)
![Azure Speech](https://img.shields.io/badge/speech-Azure%20Speech-lightblue?logo=microsoftazure)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-green)
![Transformers](https://img.shields.io/badge/NLP-Transformers-yellow?logo=huggingface)
![LangGraph](https://img.shields.io/badge/framework-LangGraph-lightgrey)
![Build Status](https://img.shields.io/github/workflow/status/Levi-Chinecherem/teammate/CI?label=build)

**Developed by Levi Chinecherem Chidi**  
**Date**: February 27, 2025

## Overview
Teammate is a cutting-edge, multi-agent AI system designed to function as a fully integrated, human-like team member within Microsoft Teams. Activated only by its name, "Teammate," it leverages a central intelligence to orchestrate specialized sub-agents, delivering a seamless experience in scheduling, communication, documentation, and meeting participation. Teammate goes beyond traditional automation by reading diverse documents, answering questions about them, making intelligent suggestions, and presenting content with real-time screen-sharing verification—all while adhering to team etiquette and responding naturally via text or voice.

## Purpose
Teammate redefines team collaboration by acting as an intelligent, proactive partner that alleviates administrative burdens, enhances decision-making, and ensures effective communication. It addresses inefficiencies in meeting management, documentation, and content accessibility, making it an indispensable asset for modern teams.

---

## Features
### Core Capabilities
1. **Name-Based Activation**:
   - Responds only when "Teammate" is called (e.g., "Teammate, schedule a meeting").
   - Ignores accidental mentions if instructed (e.g., "Teammate, I didn’t mean that").
2. **Multi-Agent System**:
   - Central intelligence (Teammate) oversees sub-agents: Scheduler, Note-Taker, Presenter, Communicator, Document-Reader, and Suggestor.
   - Built using LangGraph for dynamic task coordination.
3. **Teams Integration**:
   - Fully embedded in Microsoft Teams for chat, meetings, calendar, and screen-sharing.
4. **Voice Interaction**:
   - Listens to meeting audio and speaks using natural text-to-speech.
5. **Contextual Awareness**:
   - Tracks meeting state, assigned roles, and discussion context.

### Sub-Agent Functions
1. **Scheduler**:
   - Schedules meetings, sends individual reminders via Teams calls or text messages 2 minutes prior, and manages calendars.
   - Example: "Teammate, schedule a meeting with John at 3 PM" → calls/texts John individually before the meeting.
2. **Note-Taker**:
   - Records meeting minutes with speaker attribution (e.g., "John: Let’s finalize the report").
   - Stores notes in a database and retrieves them (e.g., file path) on demand.
   - Example: "Teammate, take notes" → starts capturing who said what.
3. **Presenter**:
   - Delivers presentations (text or slides) by sharing slides/charts in Teams.
   - Verifies visibility with team members (e.g., "Teammate: Can you see the slides?") and resharing if needed.
   - Example: "Teammate, present the Q1 slides" → shares and confirms before proceeding.
4. **Communicator**:
   - Sends emails, Teams messages (group or individual), or speaks in meetings.
   - Example: "Teammate, call John to remind him of the meeting" → initiates a Teams call.
5. **Document-Reader**:
   - Reads and interprets shared documents (Excel, CSV, Docs, TXT, PDF, PowerPoint, images, audio, video).
   - Answers team member questions about content (e.g., "Teammate, what’s in row 5 of the Excel file?").
   - Example: "Teammate, summarize the PDF" → provides a concise summary.
6. **Suggestor**:
   - Offers intelligent suggestions based on meeting discussions using LLM reasoning (e.g., GPT-like model).
   - Contributes only when asked (e.g., "Teammate, what do you suggest?").
   - Example: Suggests action items or optimizations derived from context.

### Behavioral Rules
- **Etiquette**: Silent in meetings unless addressed, respecting team dynamics.
- **Flexibility**: Executes specific instructions (e.g., "Teammate, say ‘Let’s begin’") or adapts to roles.
- **Error Handling**: Resets actions if mistakenly triggered (e.g., "Teammate, ignore that").

---

## Use Cases
1. **Corporate Teams**:
   - Streamlines meetings, documentation, and content queries for efficiency.
2. **Project Management**:
   - Tracks discussions, suggests next steps, and presents updates.
3. **Education**:
   - Records lectures, answers questions about materials, and presents slides.
4. **Remote Work**:
   - Ensures timely reminders and accessible documentation for distributed teams.
5. **Research Teams**:
   - Analyzes shared documents and provides insights during discussions.

---

## Problems Solved
1. **Inefficient Meeting Management**:
   - Automates scheduling and reminders (calls/texts), reducing no-shows.
2. **Poor Documentation**:
   - Captures detailed, speaker-attributed minutes for clarity.
3. **Communication Gaps**:
   - Delivers individual notifications and messages promptly.
4. **Inaccessible Content**:
   - Makes all document types queryable, enhancing team knowledge.
5. **Lack of Insight**:
   - Provides intelligent suggestions to improve decision-making.
6. **Presentation Issues**:
   - Ensures slides are visible to all via verified screen-sharing.

---

## Technology Stack
### Core Framework
- **Python**: Core language for development and integration.
- **LangGraph**: Orchestrates the multi-agent workflow.

### Microsoft Teams Integration
- **Microsoft Graph API**: Manages scheduling, messaging, calls, and screen-sharing.
- **Microsoft Bot Framework**: Enables real-time Teams interaction.

### Natural Language Processing (NLP)
- **Hugging Face Transformers**: Powers intent detection, context understanding, and document querying.
- **Custom Trigger**: Filters "Teammate" mentions with context.

### Speech Processing
- **Azure Speech Service**:
  - Speech-to-text: Interprets audio with speaker diarization.
  - Text-to-speech: Generates natural voice output.
- **Fallback**: ElevenLabs for alternative voice synthesis.

### Document Processing
- **Pandas**: Reads Excel and CSV files.
- **python-docx**: Parses DOCX files.
- **PyPDF2**: Extracts PDF content.
- **python-pptx**: Handles PowerPoint slides.
- **Tesseract OCR**: Reads text from images.
- **SpeechRecognition**: Transcribes audio.
- **MoviePy**: Extracts video audio for transcription.
- **Pydantic**: Validates document data structures.

### LLM Reasoning
- **GPT-like Model**: Integrates a pretrained model (e.g., via Hugging Face) for suggestion generation.

### Data Management
- **PostgreSQL**: Stores meeting data, notes, and document metadata.

### Task Automation
- **Celery**: Schedules reminders and background tasks.

### Development Notes
- Docker is excluded during development per Levi Chinecherem Chidi’s preference, with potential use for deployment later.

---

## System Architecture
1. **Central Intelligence (Teammate)**:
   - Listens for "Teammate" in Teams (text/audio) and delegates tasks via LangGraph.
   - Maintains context and enforces rules.
2. **Sub-Agents**:
   - Independent nodes in the LangGraph graph, each with specialized roles.
   - Interact with Teams, database, and external APIs.
3. **Input/Output**:
   - **Text**: Teams messages via Bot Framework.
   - **Voice**: Audio via Azure Speech Service.
   - **Visual**: Screen-sharing via Graph API.
   - **Files**: Paths or answers from document content.
4. **Persistence**:
   - PostgreSQL for scalable storage.

---

## Implementation Details
### Central Intelligence (LangGraph)
```python
from langgraph.graph import StateGraph, END

class TeammateState:
    input: str
    context: dict
    action_taken: bool = False

workflow = StateGraph(TeammateState)
workflow.add_node("listener", listen_for_name)
workflow.add_node("scheduler", schedule_meeting)
workflow.add_node("notetaker", take_notes)
workflow.add_node("presenter", deliver_presentation)
workflow.add_node("communicator", send_message)
workflow.add_node("document_reader", read_document)
workflow.add_node("suggestor", make_suggestion)
workflow.add_conditional_edges("listener", route_to_agent)
workflow.set_entry_point("listener")
teammate = workflow.compile()

def listen_for_name(state):
    if "teammate" in state.input.lower():
        if "ignore" in state.input.lower():
            state.action_taken = False
        else:
            state.action_taken = True
    return state

def route_to_agent(state):
    if not state.action_taken:
        return END
    intent = detect_intent(state.input)  # e.g., "schedule", "read"
    return intent
```

### Scheduler (Reminders)
```python
from msgraph.core import GraphClient

def schedule_meeting(state):
    client = GraphClient(credential="credential")
    event = client.users["user_id"].calendar.events.post({
        "subject": "Team Meeting",
        "start": {"dateTime": "2025-02-28T15:00:00", "timeZone": "UTC"},
        "end": {"dateTime": "2025-02-28T16:00:00", "timeZone": "UTC"},
        "attendees": [{"emailAddress": {"address": "john@example.com"}}]
    })
    # Schedule individual reminders
    for attendee in state.context["attendees"]:
        celery_app.send_task("send_reminder", args=[attendee, "call"], eta=event.start - timedelta(minutes=2))
        celery_app.send_task("send_reminder", args=[attendee, "text"], eta=event.start - timedelta(minutes=2))
```

### Document-Reader
```python
import pandas as pd
from PyPDF2 import PdfReader
from pptx import Presentation

def read_document(state):
    doc_path = state.context["document_path"]
    if doc_path.endswith(".xlsx"):
        df = pd.read_excel(doc_path)
        return df.to_string()
    elif doc_path.endswith(".pdf"):
        reader = PdfReader(doc_path)
        return " ".join([page.extract_text() for page in reader.pages])
    elif doc_path.endswith(".pptx"):
        prs = Presentation(doc_path)
        return " ".join([shape.text for slide in prs.slides for shape in slide.shapes if shape.has_text_frame])
    # Add handlers for other formats (CSV, TXT, images, audio, video)
    question = state.input.split("Teammate,")[1].strip()
    return answer_question(question, content)
```

### Suggestor
```python
from transformers import pipeline

suggestor = pipeline("text-generation", model="gpt-2")
def make_suggestion(state):
    context = state.context["meeting_discussion"]
    suggestion = suggestor(f"Based on {context}, I suggest: ", max_length=50)
    return suggestion[0]["generated_text"]
```

### Presenter (Screen-Sharing)
```python
def deliver_presentation(state):
    client = GraphClient(credential="credential")
    prs = Presentation(state.context["slides_path"])
    client.me.onlineMeetings.post({"subject": "Presentation"})  # Join meeting
    for slide in prs.slides:
        slide_content = " ".join([shape.text for shape in slide.shapes if shape.has_text_frame])
        client.me.share_content(content=slide_content, content_type="slide")  # Simulate screen-share
        speak("Can you see the slides?")
        response = wait_for_response()
        while "no" in response.lower():
            client.me.stop_sharing()
            client.me.share_content(content=slide_content, content_type="slide")
            speak("Can you see the slides now?")
            response = wait_for_response()
        speak(slide_content)
```

---

## Development Plan
1. **Phase 1: Core Setup**:
   - Build LangGraph with listener and Scheduler.
   - Integrate Teams Bot Framework.
2. **Phase 2: Voice and Documents**:
   - Add Azure Speech and document-reading capabilities.
3. **Phase 3: Full Suite**:
   - Implement Note-Taker, Presenter, Communicator, Document-Reader, Suggestor.
   - Test in Teams meetings.
4. **Phase 4: Refinement**:
   - Enhance suggestion reasoning and presentation sharing.
   - Deploy as a service (Docker optional post-development).

---

## Challenges and Solutions
1. **Complex Documents**:
   - **Solution**: Robust parsing with error handling for each format.
2. **Accurate Suggestions**:
   - **Solution**: Fine-tune LLM on team-specific data.
3. **Screen-Sharing Reliability**:
   - **Solution**: Fallback to text output if sharing fails repeatedly.

---

## Future Enhancements
- **Multi-Language**: Supports diverse languages for global teams.
- **Personalization**: Learns team habits for tailored suggestions.
- **Advanced Analytics**: Summarizes trends from documents and meetings.

---

## Credits
- **Developer**: Levi Chinecherem Chidi
- **Vision**: A transformative AI teammate for the future of work.

Teammate is a groundbreaking system that blends intelligence, adaptability, and seamless integration into one powerful entity. For inquiries, contact Levi Chinecherem Chidi.
