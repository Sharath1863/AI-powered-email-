import os
import google.generativeai as genai
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Load Gmail API credentials
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("gmail", "v1", credentials=creds)

# Set up Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Fetch unread emails
results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
messages = results.get("messages", [])

if not messages:
    print("📭 No unread emails found.")
else:
    print(f"📨 Found {len(messages)} unread emails.")
    print("-" * 50)

    for msg in messages:
        msg_id = msg["id"]
        msg_data = service.users().messages().get(userId="me", id=msg_id, format="full").execute()

        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        snippet = msg_data.get("snippet", "No preview available")

        print(f"📧 **Subject:** {subject}")
        print(f"📜 **Snippet:** {snippet}")
        print("-" * 50)

        # Send each email separately to Gemini for explanation
        prompt = f"Explain the meaning and purpose of this email:\n\nSubject: {subject}\nBody: {snippet}"
        
        try:
            response = model.generate_content(prompt)
            explanation = response.text.strip() if response.text else "No explanation available."
            print(f"🔍 **Gemini Explanation:** {explanation}")
            print("=" * 50)
        except Exception as e:
            print(f"❌ Gemini API Error: {str(e)}")
