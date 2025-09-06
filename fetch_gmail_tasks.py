import os
import datetime
import json
import base64
import re
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# 📌 Define the necessary API scopes  
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send", 
    "https://www.googleapis.com/auth/calendar"
]

# ✅ Authenticate and get Google services
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

# 🤖 AI-powered email classification and response generation
def classify_email_with_ai(subject, body):
    """Classify email content using AI and generate appropriate response"""
    try:
        # Set up OpenAI (using a mock response for demo if no API key)
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        if not openai.api_key:
            print("⚠️ No OpenAI API key found, using mock AI responses for demo")
            return classify_email_mock(subject, body)
        
        prompt = f"""
        Analyze this email and classify it into one of these categories: 
        - urgent (needs immediate response)
        - meeting (meeting request or scheduling)
        - information (informational, no response needed)
        - task (assigns a task or request)
        
        Subject: {subject}
        Body: {body[:500]}...
        
        Provide classification and suggest a brief response if needed.
        Format: Classification: [category] | Response: [suggested response or "No response needed"]
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"⚠️ AI classification failed: {e}")
        return classify_email_mock(subject, body)

def classify_email_mock(subject, body):
    """Mock AI classification for demo purposes"""
    subject_lower = subject.lower()
    body_lower = body.lower()
    
    if any(word in subject_lower for word in ['urgent', 'asap', 'important', 'critical']):
        return "Classification: urgent | Response: Thank you for your email. I'll prioritize this and respond shortly."
    elif any(word in subject_lower + body_lower for word in ['meeting', 'schedule', 'calendar', 'appointment']):
        return "Classification: meeting | Response: I'll check my calendar and get back to you with available times."
    elif any(word in subject_lower + body_lower for word in ['task', 'please', 'could you', 'request']):
        return "Classification: task | Response: I've received your request and will work on this. I'll update you on progress."
    else:
        return "Classification: information | Response: No response needed"

# 📧 Fetch recent emails from Gmail
def fetch_recent_emails(service, max_results=5):
    """Fetch recent emails from Gmail inbox"""
    try:
        print(f"\n🔍 Fetching {max_results} recent emails...")
        
        # Get message list
        results = service.users().messages().list(
            userId='me', 
            labelIds=['INBOX'],
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        email_data = []
        for i, message in enumerate(messages, 1):
            # Get full message
            msg = service.users().messages().get(
                userId='me', 
                id=message['id']
            ).execute()
            
            # Extract headers
            headers = msg['payload'].get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
            
            # Extract body
            body = extract_email_body(msg['payload'])
            
            print(f"\n📨 Email {i}:")
            print(f"   From: {sender}")
            print(f"   Subject: {subject}")
            print(f"   Date: {date}")
            print(f"   Preview: {body[:100]}..." if len(body) > 100 else f"   Body: {body}")
            
            # AI Classification
            print(f"\n🤖 AI Analysis:")
            ai_response = classify_email_with_ai(subject, body)
            print(f"   {ai_response}")
            
            email_data.append({
                'id': message['id'],
                'subject': subject,
                'sender': sender,
                'body': body,
                'ai_analysis': ai_response
            })
            
            print("-" * 80)
        
        return email_data
        
    except Exception as e:
        print(f"❌ Error fetching emails: {e}")
        return []

def extract_email_body(payload):
    """Extract email body from Gmail API payload"""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    else:
        if payload['mimeType'] == 'text/plain':
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    
    # Clean up body text
    body = re.sub(r'\r\n', '\n', body)
    body = re.sub(r'\n+', '\n', body)
    return body.strip()

# 📤 Send AI-generated response email
def send_response_email(service, to_email, subject, body):
    """Send an email response"""
    try:
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = f"Re: {subject}"
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"✅ Response sent successfully! Message ID: {send_message['id']}")
        return send_message
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return None

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

# 🔄 Main AI-powered email processing function
def main():
    print("🚀 Starting AI-Powered Email Assistant Demo")
    print("=" * 60)
    
    # Authenticate with Google services
    print("🔐 Authenticating with Google APIs...")
    creds = authenticate_google()
    
    # Build services
    gmail_service = build("gmail", "v1", credentials=creds)
    calendar_service = build("calendar", "v3", credentials=creds)
    
    print("✅ Authentication successful!")
    
    # 📧 Process emails with AI
    print("\n📧 GMAIL AI PROCESSING")
    print("=" * 40)
    
    emails = fetch_recent_emails(gmail_service, max_results=3)
    
    if emails:
        print(f"\n📊 SUMMARY: Processed {len(emails)} emails")
        
        # Count classifications
        urgent_count = sum(1 for email in emails if 'urgent' in email['ai_analysis'].lower())
        meeting_count = sum(1 for email in emails if 'meeting' in email['ai_analysis'].lower()) 
        task_count = sum(1 for email in emails if 'task' in email['ai_analysis'].lower())
        
        print(f"   🔴 Urgent emails: {urgent_count}")
        print(f"   🗓️  Meeting requests: {meeting_count}")  
        print(f"   📋 Task assignments: {task_count}")
        
        # Create calendar event for urgent emails if any
        if urgent_count > 0:
            print(f"\n📅 Creating calendar reminder for {urgent_count} urgent email(s)")
            event_title = f"Follow up on {urgent_count} urgent email(s)"
            start_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            end_time = start_time + datetime.timedelta(minutes=30)
            
            create_calendar_event(
                calendar_service, 
                event_title, 
                start_time.isoformat(), 
                end_time.isoformat(), 
                "Review and respond to urgent emails requiring immediate attention."
            )
    else:
        print("📭 No emails found in inbox")
    
    print(f"\n🎯 AI-Powered Email Demo Complete!")
    print("=" * 60)
    print("📹 This demo showed:")
    print("   ✅ Gmail API integration")
    print("   ✅ AI-powered email classification")
    print("   ✅ Automatic response suggestions")
    print("   ✅ Calendar integration for task management")
    print("   ✅ Smart priority detection")

if __name__ == "__main__":
    main()
