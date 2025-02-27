Got it—thanks for clarifying! I’ll tailor the instructions for Fedora 41, a Linux-based OS, and avoid Windows-specific assumptions moving forward. Let’s proceed with **Step 3: Configure Microsoft Teams Integration**. This step sets up Teammate as a bot in Microsoft Teams with access to the Graph API, enabling it to interact with Teams for messaging, scheduling, and more. Below is a detailed, self-contained guide optimized for Fedora 41, with all necessary tools, commands, and verification steps.

---

### Step 3: Configure Microsoft Teams Integration

#### Goal
Set up Teammate as a Microsoft Teams bot with Microsoft Graph API access, allowing it to receive commands, send messages, schedule meetings, and participate in Teams. This step establishes the foundational integration with Teams, critical for Teammate’s functionality.

#### Tools
- **Azure Portal**: For registering the bot and obtaining credentials.
- **Microsoft Bot Framework**: For creating a Teams bot.
- **Microsoft Graph API**: For programmatic access to Teams features (e.g., calendar, chat).
- **Python**: With `msgraph-core` and `requests` (installed in Step 2).
- **Fedora 41 Terminal**: For running commands and scripts.
- **`python-dotenv`**: For managing environment variables securely.

#### Prerequisites
- Fedora 41 system with Python 3.11 and virtual environment active (`source teammate/venv/bin/activate` from Step 1).
- Dependencies installed from Step 2 (`msgraph-core`, `requests`, `python-dotenv`).
- Internet access for Azure authentication and API calls.

#### Actions and Instructions

1. **Register an App in Azure Active Directory**
   - **Why**: Provides credentials for Teammate to authenticate with Teams and Graph API.
   - **How**:
     - Open a browser and go to [portal.azure.com](https://portal.azure.com/).
     - Sign in with a Microsoft account (create one if needed).
     - Navigate to **Azure Active Directory** > **App registrations** > **New registration**.
     - Fill in:
       - **Name**: `TeammateBot`.
       - **Supported account types**: "Accounts in any organizational directory (Any Azure AD directory - Multitenant)".
       - **Redirect URI**: Leave blank for now (we’ll add it later).
     - Click **Register**.
     - Note the **Application (client) ID** (e.g., `123e4567-e89b-12d3-a456-426614174000`) and **Directory (tenant) ID** (e.g., `987fcdeb-12ab-34cd-56ef-789101112131`) from the app overview page.
   - **Outcome**: An Azure AD app is created for Teammate.

2. **Generate a Client Secret**
   - **Why**: Allows secure authentication with the Graph API.
   - **How**:
     - In the Azure Portal, go to your `TeammateBot` app > **Certificates & secrets**.
     - Under **Client secrets**, click **New client secret**.
     - Set **Description**: `Teammate Secret` and **Expires**: 24 months (or your preference).
     - Click **Add**.
     - Copy the **Value** of the secret immediately (e.g., `abc123~xyz789...`)—it won’t be visible again.
   - **Outcome**: A secret key is generated for API authentication.

3. **Configure Graph API Permissions**
   - **Why**: Grants Teammate access to Teams features like calendars, messages, and meetings.
   - **How**:
     - Go to `TeammateBot` app > **API permissions** > **Add a permission** > **Microsoft Graph** > **Application permissions**.
     - Add the following permissions:
       - `Calendars.ReadWrite` (schedule meetings).
       - `ChatMessage.Send` (send messages).
       - `OnlineMeetings.ReadWrite` (join/present in meetings).
       - `User.Read.All` (access user info for reminders).
     - Click **Add permissions**.
     - Click **Grant admin consent for [your tenant]** (requires admin privileges; if personal account, consent is automatic).
   - **Verify**: Permissions list shows green checkmarks under **Status**.
   - **Outcome**: Teammate has necessary API access.

4. **Set Up Microsoft Bot Framework**
   - **Why**: Registers Teammate as a bot that can interact in Teams channels.
   - **How**:
     - Go to **Azure Portal** > **Create a resource** > Search for “Azure Bot” > **Create**.
     - Fill in:
       - **Bot handle**: `TeammateBot`.
       - **Subscription**: Your Azure subscription (free tier works for testing).
       - **Resource group**: Create new (e.g., `teammate-rg`) or use existing.
       - **Location**: Choose a nearby region (e.g., `East US`).
       - **App type**: Multi Tenant.
       - **Microsoft App ID**: Paste the **Application (client) ID** from Step 3.1.
     - Click **Review + Create** > **Create**.
     - Once deployed, go to the bot resource > **Channels** > **Microsoft Teams** > **Apply** > Accept terms.
     - Test the bot connection: Go to **Test in Web Chat** (it won’t work fully yet, but ensure no errors).
   - **Outcome**: Teammate is registered as a Teams bot.

5. **Store Credentials in `.env` File**
   - **Why**: Keeps sensitive credentials secure and accessible to the Python code.
   - **How**:
     - In the `teammate` directory, create a `.env` file:
       ```bash
       nano .env
       ```
     - Add the following, replacing with your values:
       ```
       CLIENT_ID=123e4567-e89b-12d3-a456-426614174000
       CLIENT_SECRET=abc123~xyz789...
       TENANT_ID=987fcdeb-12ab-34cd-56ef-789101112131
       ```
     - Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X` in nano).
     - Ensure `.env` is in `.gitignore` (from Step 1) to avoid committing secrets.
   - **Outcome**: Credentials are securely stored.

6. **Test Connectivity with a Simple Bot**
   - **Why**: Verifies Teams integration works before full implementation.
   - **How**:
     - Create a `src/` directory and a basic bot script:
       ```bash
       mkdir src
       touch src/main.py
       ```
     - Edit `src/main.py` with the following Python code:
       ```python
       import os
       from dotenv import load_dotenv
       from msgraph.core import GraphClient
       import requests

       # Load environment variables
       load_dotenv()
       client_id = os.getenv("CLIENT_ID")
       client_secret = os.getenv("CLIENT_SECRET")
       tenant_id = os.getenv("TENANT_ID")

       # Authenticate with Graph API
       auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
       auth_data = {
           "grant_type": "client_credentials",
           "client_id": client_id,
           "client_secret": client_secret,
           "scope": "https://graph.microsoft.com/.default"
       }
       response = requests.post(auth_url, data=auth_data)
       token = response.json().get("access_token")

       # Test Graph API call (get current user info)
       client = GraphClient(api_version="v1.0", access_token=token)
       user = client.me.get()
       print(f"Connected as: {user.display_name}")
       ```
     - Install `nano` if not present: `sudo dnf install nano`.
     - Run the script: `python src/main.py`.
     - Expected output: "Connected as: [Your Name]" (or an error if misconfigured).
   - **Troubleshooting**:
     - **401 Unauthorized**: Check `CLIENT_ID`, `CLIENT_SECRET`, and `TENANT_ID` in `.env`.
     - **Permission Denied**: Ensure permissions are granted in Step 3.3.
     - **Module Not Found**: Verify Step 2 completed (`pip install msgraph-core requests python-dotenv`).
   - **Outcome**: Basic Graph API connectivity is confirmed.

7. **Add Files to Git**
   - **Why**: Tracks initial Teams integration setup in version control.
   - **How**:
     - Stage files: `git add .env src/main.py`.
     - Commit: `git commit -m "Configure Microsoft Teams integration with basic bot"`.
   - **Note**: `.env` won’t commit due to `.gitignore`, which is intentional.
   - **Outcome**: Changes are versioned.

#### Outcome
- Teammate is registered as a Teams bot with Graph API access.
- Credentials are securely stored in `.env`.
- A basic script confirms connectivity, ready to expand into full bot functionality in later steps.

#### Duration
- Approximately 2-3 hours, depending on familiarity with Azure and Teams setup.

#### Fedora 41-Specific Notes
- **Package Manager**: Use `dnf` instead of `apt` (e.g., `sudo dnf install python3-devel` if build tools are needed).
- **Firewall**: If Azure connectivity fails, check `firewalld`: `sudo firewall-cmd --add-service=https --permanent` and reload (`sudo firewall-cmd --reload`).
- **Terminal**: Commands assume a Bash shell (default in Fedora).

#### Troubleshooting
- **Azure Portal Access**: Ensure your account has sufficient permissions (e.g., not blocked by organizational policies).
- **Graph API Errors**: Double-check permissions and token scope in the auth request.
- **Bot Not Responding**: Verify the Teams channel is enabled in Azure Bot Service.

---

### Next Steps
With Teams integration configured, you’re ready for **Step 4: Set Up PostgreSQL Database**. Let me know when you want to proceed, and I’ll provide the detailed guide tailored for Fedora 41, including SQL scripts and database code! How did this step feel? Any Azure or Teams setup questions?