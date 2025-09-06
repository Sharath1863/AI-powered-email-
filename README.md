# 🤖 AI-Powered Email Assistant

An intelligent email processing system that uses AI to classify emails, generate responses, and create calendar events automatically.

## 📋 Features

- **🔍 Email Analysis**: Automatically fetches and analyzes recent emails from Gmail
- **🤖 AI Classification**: Uses AI to classify emails into categories (urgent, meeting, task, information)
- **💬 Smart Responses**: Generates appropriate response suggestions for each email
- **📅 Calendar Integration**: Creates calendar events for urgent emails and meetings
- **📊 Analytics Dashboard**: Shows summary of email types and priorities

## 🚀 Demo Setup Instructions

### Prerequisites
1. Python 3.7 or higher
2. Google Account with Gmail access
3. OpenAI API key (optional - will use mock responses if not provided)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sharath1863/AI-powered-email-.git
   cd AI-powered-email-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google API credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Gmail API and Calendar API
   - Create credentials (OAuth 2.0 Client ID)
   - Download credentials as `credentials.json` and place in project root

4. **Set up OpenAI API (Optional)**
   - Create `.env` file in project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - If no API key is provided, the system will use mock AI responses for demonstration

### Running the Demo

```bash
python fetch_gmail_tasks.py
```

## 🎬 Video Demo Script

### What to Show in the Video:

1. **Introduction** (30 seconds)
   - "This is our AI-powered email assistant that automatically processes and responds to emails"
   - Show the code repository and file structure

2. **Code Walkthrough** (1 minute)
   - Highlight key functions: `fetch_recent_emails()`, `classify_email_with_ai()`
   - Show AI classification logic and response generation
   - Point out Gmail and Calendar API integrations

3. **Live Demo** (2 minutes)
   - Run the command: `python fetch_gmail_tasks.py`
   - Show authentication process
   - Display email fetching and AI analysis in real-time
   - Show the summary statistics
   - Check Google Calendar for created events

4. **Results Overview** (30 seconds)
   - Show the final output summary
   - Explain the business value: time savings, priority detection, automated responses

## 📊 Expected Output

```
🚀 Starting AI-Powered Email Assistant Demo
============================================================
🔐 Authenticating with Google APIs...
✅ Authentication successful!

📧 GMAIL AI PROCESSING
========================================

🔍 Fetching 3 recent emails...

📨 Email 1:
   From: manager@company.com
   Subject: Urgent: Project Deadline Update
   Date: Mon, 06 Sep 2024 10:30:00 +0000
   Preview: We need to discuss the project timeline changes...

🤖 AI Analysis:
   Classification: urgent | Response: Thank you for your email. I'll prioritize this and respond shortly.

📨 Email 2:
   From: team@company.com
   Subject: Weekly Team Meeting
   Date: Mon, 06 Sep 2024 09:15:00 +0000
   Preview: Our weekly standup is scheduled for...

🤖 AI Analysis:
   Classification: meeting | Response: I'll check my calendar and get back to you with available times.

📊 SUMMARY: Processed 3 emails
   🔴 Urgent emails: 1
   🗓️  Meeting requests: 1
   📋 Task assignments: 1

📅 Creating calendar reminder for 1 urgent email(s)
✅ Event Created: https://calendar.google.com/calendar/event?eid=...

🎯 AI-Powered Email Demo Complete!
============================================================
📹 This demo showed:
   ✅ Gmail API integration
   ✅ AI-powered email classification
   ✅ Automatic response suggestions
   ✅ Calendar integration for task management
   ✅ Smart priority detection
```

## 💼 Business Value

- **Time Savings**: Automatically categorizes and prioritizes emails
- **Never Miss Important**: Creates calendar reminders for urgent items
- **Consistent Responses**: AI-generated professional responses
- **Smart Organization**: Integrates with existing calendar workflow
- **Scalable**: Can process hundreds of emails quickly

## 🔧 Technical Architecture

- **Gmail API**: Fetches and processes email data
- **OpenAI GPT**: Classifies emails and generates responses
- **Google Calendar API**: Creates events for follow-ups
- **Python**: Core application logic
- **OAuth 2.0**: Secure authentication with Google services

## 🚨 Important Notes for Video

1. **Prepare Test Emails**: Have a few different types of emails in your inbox (urgent, meeting requests, tasks) for better demonstration
2. **Check Permissions**: Ensure the app has proper Gmail and Calendar permissions
3. **Mock Mode**: The demo works even without OpenAI API key using intelligent mock responses
4. **Real-time Processing**: The app processes emails in real-time, showing immediate results

## 📝 Next Steps

This demo shows the foundation for a production-ready AI email assistant that could include:
- Email auto-responses
- More sophisticated AI models
- Integration with CRM systems
- Team collaboration features
- Advanced analytics and reporting