import os
from dotenv import load_dotenv
from msgraph.core import GraphClient
import requests
from teammate import run_teammate
from bottle import Bottle, request, response

# Load environment variables
load_dotenv()

# Graph API client (for bot authentication)
def get_graph_client():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    tenant_id = os.getenv("TENANT_ID")
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    auth_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    resp = requests.post(auth_url, data=auth_data)
    token = resp.json().get("access_token")
    return GraphClient(api_version="v1.0", access_token=token)

app = Bottle()

@app.post("/webhook")
def handle_webhook():
    payload = request.json
    if not payload or "text" not in payload.get("message", {}):
        response.status = 400
        return {"error": "Invalid payload"}
    
    command = payload["message"]["text"]
    context = payload.get("context", {})
    result = run_teammate(command, context)
    client = get_graph_client()
    chat_id = payload["conversation"]["id"]
    client.chats[chat_id].messages.post({
        "body": {"content": result.response or "Processed"}
    })
    return {"status": "success"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)