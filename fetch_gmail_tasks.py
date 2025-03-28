import os
import datetime
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 📌 Define the necessary API scopes
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# ✅ Authenticate and get Google Calendar service
def authenticate_google():
    creds = None
    token_path = "token.json"

    # 🔄 Load existing credentials if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # 🌐 Refresh or request new authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # 💾 Save the credentials for the next run
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return creds

# 📅 Function to create an event in Google Calendar
def create_calendar_event(service, summary, start_time, end_time, description=""):
    event_data = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }

    # 🚀 Insert event into Google Calendar
    event = service.events().insert(calendarId="primary", body=event_data).execute()

    # 🔗 Print event link for verification
    print(f"✅ Event Created: {event.get('htmlLink')}")
    return event.get("htmlLink")

# 🔄 Main function to authenticate and add an event
def main():
    creds = authenticate_google()
    service = build("calendar", "v3", credentials=creds)

    # 📌 Example Task Event
    event_title = "AI Agentic Task Review"
    start_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # 2 hours from now
    end_time = start_time + datetime.timedelta(hours=1)

    # 📝 Create event
    create_calendar_event(service, event_title, start_time.isoformat(), end_time.isoformat(), "Discuss AI Agentic progress.")

if __name__ == "__main__":
    main()
