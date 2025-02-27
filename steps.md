### Development Steps for Teammate

#### Step 1: Set Up Development Environment
- **Goal**: Establish a consistent, reproducible environment for development.
- **Tools**: Python 3.11, pip, virtualenv, Git, PostgreSQL, Visual Studio Code (or preferred IDE).
- **Actions**:
  - Install Python 3.11 from python.org or package manager (e.g., `apt`, `brew`).
  - Create a virtual environment: `python -m venv venv`.
  - Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).
  - Install base dependencies: `pip install wheel setuptools`.
  - Install PostgreSQL locally or use a cloud instance (e.g., Azure Database for PostgreSQL).
  - Initialize a Git repository: `git init`.
  - Set up VS Code with Python extension, configuring the interpreter to the virtual environment.
- **Outcome**: A working Python environment with version control and a database ready for development.
- **Duration**: 1-2 hours.

#### Step 2: Install Core Dependencies
- **Goal**: Install all required Python libraries and tools for Teammate’s functionality.
- **Tools**: pip, requirements.txt.
- **Actions**:
  - Create a `requirements.txt` file listing: `langgraph`, `msgraph-core`, `azure-cognitiveservices-speech`, `transformers`, `torch`, `pandas`, `python-docx`, `PyPDF2`, `python-pptx`, `pytesseract`, `speechrecognition`, `moviepy`, `pydantic`, `psycopg2-binary`, `celery`, `requests`.
  - Run `pip install -r requirements.txt`.
  - Verify installations: `pip list` and test imports in a Python shell (e.g., `import langgraph`).
- **Outcome**: All libraries installed, ready for coding the multi-agent system, Teams integration, document processing, and more.
- **Duration**: 1 hour.

#### Step 3: Configure Microsoft Teams Integration
- **Goal**: Set up Teammate as a Teams bot with access to Graph API.
- **Tools**: Azure Portal, Microsoft Bot Framework, Graph API credentials.
- **Actions**:
  - Register an app in Azure AD (portal.azure.com) to get client ID, secret, and tenant ID.
  - Enable Bot Framework channel in Azure Bot Service, linking it to Teams.
  - Configure permissions in Graph API (e.g., `Calendars.ReadWrite`, `ChatMessage.Send`, `OnlineMeetings.ReadWrite`).
  - Store credentials securely in a `.env` file using `python-dotenv`.
  - Test connectivity with a simple bot that echoes messages in Teams.
- **Outcome**: Teammate bot registered and able to receive/send messages in Teams.
- **Duration**: 2-3 hours.

#### Step 4: Set Up PostgreSQL Database
- **Goal**: Create a database schema to store meeting data, minutes, and documents.
- **Tools**: PostgreSQL, psycopg2, SQL scripts.
- **Actions**:
  - Create a database: `CREATE DATABASE teammate;`.
  - Define tables: `meetings` (id, title, start_time, attendees), `minutes` (id, meeting_id, speaker, text), `documents` (id, path, type, content).
  - Write SQL scripts in a `setup_db.sql` file and run them: `psql -d teammate -f setup_db.sql`.
  - Test connectivity with psycopg2: Connect and insert a sample row.
- **Outcome**: A functional database for persistent storage.
- **Duration**: 2 hours.

#### Step 5: Implement Central Intelligence with LangGraph
- **Goal**: Build Teammate’s core logic to listen for commands and route tasks to sub-agents.
- **Tools**: LangGraph, Python, Hugging Face Transformers (for NLP).
- **Actions**:
  - Create a `teammate.py` file defining the `TeammateState` class with fields: `input`, `context`, `action_taken`.
  - Set up a LangGraph workflow with nodes for the listener and placeholders for sub-agents.
  - Implement the `listen_for_name` function to detect "Teammate" and handle ignore commands.
  - Use a transformer model to parse intents (e.g., "schedule", "read") in `route_to_agent`.
  - Test with dummy inputs to ensure routing works.
- **Outcome**: Teammate can process commands and delegate tasks.
- **Duration**: 4-5 hours.

#### Step 6: Develop Scheduler Sub-Agent
- **Goal**: Enable scheduling meetings and sending reminders via calls/texts.
- **Tools**: msgraph-core, Celery, PostgreSQL.
- **Actions**:
  - Create `scheduler.py` with a `schedule_meeting` function using Graph API to create events.
  - Implement reminder logic with Celery tasks for individual calls and texts 2 minutes prior.
  - Store meeting details in the database.
  - Test by scheduling a meeting and verifying reminders in Teams.
- **Outcome**: Scheduler can create events and notify team members individually.
- **Duration**: 3-4 hours.

#### Step 7: Develop Note-Taker Sub-Agent
- **Goal**: Record meeting minutes with speaker attribution.
- **Tools**: Azure Speech Service, PostgreSQL.
- **Actions**:
  - Create `note_taker.py` with functions to start/stop continuous speech recognition.
  - Use Azure Speech SDK with diarization to identify speakers.
  - Save notes to the `minutes` table with speaker and text.
  - Test in a mock Teams meeting with multiple speakers.
- **Outcome**: Note-Taker captures who said what during meetings.
- **Duration**: 4-5 hours.

#### Step 8: Develop Presenter Sub-Agent
- **Goal**: Present slides with screen-sharing and visibility verification.
- **Tools**: python-pptx, msgraph-core, Azure Speech Service.
- **Actions**:
  - Create `presenter.py` with a `deliver_presentation` function to read PPTX files.
  - Use Graph API to share slides in Teams and speak content via TTS.
  - Implement a verification loop: Ask "Can you see the slides?" and reshare if "no" is detected.
  - Test in a Teams meeting with sample slides.
- **Outcome**: Presenter shares and confirms visibility before presenting.
- **Duration**: 4-5 hours.

#### Step 9: Develop Communicator Sub-Agent
- **Goal**: Send messages, make calls, and speak in meetings.
- **Tools**: msgraph-core, Azure Speech Service.
- **Actions**:
  - Create `communicator.py` with functions for sending Teams messages, initiating calls, and speaking.
  - Integrate with Scheduler for reminders.
  - Test by sending a message and call to a test user in Teams.
- **Outcome**: Communicator handles all communication tasks.
- **Duration**: 3-4 hours.

#### Step 10: Develop Document-Reader Sub-Agent
- **Goal**: Read and answer questions about diverse document types.
- **Tools**: Pandas, PyPDF2, python-docx, python-pptx, Tesseract OCR, SpeechRecognition, MoviePy, Hugging Face Transformers.
- **Actions**:
  - Create `document_reader.py` with parsing functions for each format (Excel, CSV, PDF, etc.).
  - Use OCR for images, audio transcription for audio/video, and text extraction for others.
  - Implement a QA function using a transformer model to answer questions.
  - Store processed content in the database.
  - Test by uploading a PDF and asking, "What’s on page 2?"
- **Outcome**: Document-Reader interprets documents and responds to queries.
- **Duration**: 6-8 hours.

#### Step 11: Develop Suggestor Sub-Agent
- **Goal**: Provide intelligent suggestions based on meeting context.
- **Tools**: Hugging Face Transformers (GPT-like model), PostgreSQL.
- **Actions**:
  - Create `suggestor.py` with a `make_suggestion` function using a pretrained LLM.
  - Fetch meeting context from the database to inform suggestions.
  - Test with sample discussion text: "Teammate, what do you suggest?"
- **Outcome**: Suggestor contributes meaningful ideas when asked.
- **Duration**: 3-4 hours.

#### Step 12: Integrate Sub-Agents with Central Intelligence
- **Goal**: Connect all sub-agents to Teammate’s LangGraph workflow.
- **Tools**: LangGraph, Python.
- **Actions**:
  - Update `teammate.py` to include all sub-agent nodes and routing logic.
  - Ensure seamless handoff of state between Teammate and sub-agents.
  - Test end-to-end with commands like "Teammate, schedule a meeting" and "Teammate, suggest an action."
- **Outcome**: Fully functional multi-agent system.
- **Duration**: 3-4 hours.

#### Step 13: Test the Full System
- **Goal**: Validate Teammate’s functionality in a real-world scenario.
- **Tools**: Teams test environment, test scripts.
- **Actions**:
  - Set up a test Teams channel with multiple users.
  - Run scenarios: Schedule a meeting, take notes, present slides, read a document, suggest an idea.
  - Log issues and refine based on feedback.
- **Outcome**: Teammate operates seamlessly across all features.
- **Duration**: 4-6 hours.

#### Step 14: Deploy the System
- **Goal**: Launch Teammate as a persistent service.
- **Tools**: Cloud provider (e.g., Azure), Celery worker, optional Docker (post-development).
- **Actions**:
  - Configure a cloud VM or app service (e.g., Azure App Service).
  - Set up Celery with a broker (e.g., Redis) for task scheduling.
  - Run the bot as a background process with a startup script.
  - Monitor logs and performance.
- **Outcome**: Teammate is live and accessible in Teams.
- **Duration**: 3-5 hours.

---

### Full System Folder Structure
Here’s the folder structure to organize the Teammate system:

```
teammate/
│
├── .env                # Environment variables (e.g., API keys)
├── .gitignore          # Git ignore file (e.g., venv/, *.pyc)
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── setup_db.sql        # Database schema setup script
│
├── src/                # Source code directory
│   ├── __init__.py     # Makes src a package
│   ├── teammate.py     # Central intelligence (LangGraph workflow)
│   ├── scheduler.py    # Scheduler sub-agent
│   ├── note_taker.py   # Note-Taker sub-agent
│   ├── presenter.py    # Presenter sub-agent
│   ├── communicator.py # Communicator sub-agent
│   ├── document_reader.py # Document-Reader sub-agent
│   ├── suggestor.py    # Suggestor sub-agent
│   ├── utils/          # Utility functions
│   │   ├── __init__.py
│   │   ├── db.py      # Database connection and queries
│   │   ├── teams.py   # Teams API helpers
│   │   ├── speech.py  # Speech processing helpers
│   │   └── nlp.py     # NLP and intent detection
│   └── main.py         # Entry point to run the system
│
├── tests/              # Test suite
│   ├── __init__.py
│   ├── test_scheduler.py
│   ├── test_note_taker.py
│   ├── test_presenter.py
│   ├── test_communicator.py
│   ├── test_document_reader.py
│   ├── test_suggestor.py
│   └── test_teammate.py
│
└── data/               # Sample data for testing
    ├── sample_meeting.docx
    ├── sample_slides.pptx
    ├── sample_report.pdf
    └── sample_audio.mp3
```

- **Root**: Configuration files and documentation.
- **src/**: Core logic split by sub-agents and utilities.
- **tests/**: Unit tests for each component.
- **data/**: Test files for document reading and presentations.

---

### Notes
- **Modularity**: Each step builds on the previous one, with clear deliverables.
- **Flexibility**: Steps can be assigned to different developers or AIs.
- **Next Steps**: Request any step (e.g., "Step 5") for detailed code and instructions.
