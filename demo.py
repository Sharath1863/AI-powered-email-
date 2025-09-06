#!/usr/bin/env python3
"""
AI-Powered Email Assistant - Demo Mode
=====================================
This script demonstrates the AI email processing functionality
without requiring actual Gmail credentials or API keys.
Perfect for video demonstrations to HR!
"""

import datetime
import json

def demo_classify_email(subject, body):
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

def demo_main():
    print("🚀 AI-Powered Email Assistant - DEMO MODE")
    print("=" * 60)
    print("📹 Perfect for HR Video Demonstration!")
    print("=" * 60)
    
    # Sample emails for demonstration
    sample_emails = [
        {
            'from': 'manager@company.com',
            'subject': 'URGENT: Project Deadline Update Required',
            'date': 'Mon, 06 Sep 2024 10:30:00 +0000',
            'body': 'Hi team, we need to discuss the project timeline changes immediately. The client has requested an accelerated delivery schedule and we need to assess if this is feasible. Please review the attached requirements and let me know your availability for an emergency meeting today.'
        },
        {
            'from': 'hr@company.com', 
            'subject': 'Weekly Team Meeting - Calendar Invite',
            'date': 'Mon, 06 Sep 2024 09:15:00 +0000',
            'body': 'Hello everyone, our weekly standup is scheduled for Wednesday at 2 PM. Please confirm your attendance and prepare updates on your current projects. The meeting will be held in Conference Room A.'
        },
        {
            'from': 'client@partner.com',
            'subject': 'Could you please review the contract terms?', 
            'date': 'Mon, 06 Sep 2024 08:45:00 +0000',
            'body': 'Dear team, I hope this email finds you well. Could you please review the attached contract terms and provide your feedback by end of week? We would like to finalize the agreement soon. Thank you for your attention to this matter.'
        },
        {
            'from': 'newsletter@techcompany.com',
            'subject': 'Weekly Tech Newsletter - Latest Updates',
            'date': 'Mon, 06 Sep 2024 07:00:00 +0000', 
            'body': 'This week in tech: New AI developments, cloud computing trends, and cybersecurity updates. Read more about the latest innovations in the industry.'
        }
    ]
    
    print("\n📧 GMAIL AI PROCESSING SIMULATION")
    print("=" * 40)
    print(f"🔍 Processing {len(sample_emails)} sample emails...")
    
    classifications = []
    
    for i, email in enumerate(sample_emails, 1):
        print(f"\n📨 Email {i}:")
        print(f"   From: {email['from']}")
        print(f"   Subject: {email['subject']}")
        print(f"   Date: {email['date']}")
        
        # Show preview of body
        preview = email['body'][:100] + "..." if len(email['body']) > 100 else email['body']
        print(f"   Preview: {preview}")
        
        # AI Classification
        print(f"\n🤖 AI Analysis:")
        ai_response = demo_classify_email(email['subject'], email['body'])
        print(f"   {ai_response}")
        
        # Extract classification for summary
        classification = ai_response.split('|')[0].replace('Classification:', '').strip()
        classifications.append(classification)
        
        print("-" * 80)
    
    # Summary statistics
    print(f"\n📊 SUMMARY: Processed {len(sample_emails)} emails")
    
    urgent_count = classifications.count('urgent')
    meeting_count = classifications.count('meeting')
    task_count = classifications.count('task')
    info_count = classifications.count('information')
    
    print(f"   🔴 Urgent emails: {urgent_count}")
    print(f"   🗓️  Meeting requests: {meeting_count}")
    print(f"   📋 Task assignments: {task_count}")
    print(f"   ℹ️  Informational: {info_count}")
    
    # Calendar integration simulation
    if urgent_count > 0:
        print(f"\n📅 CALENDAR INTEGRATION")
        print(f"   Creating calendar reminder for {urgent_count} urgent email(s)")
        
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
        print(f"   📍 Event: 'Follow up on {urgent_count} urgent email(s)'")
        print(f"   ⏰ Scheduled: {reminder_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   ✅ Calendar event created successfully!")
    
    print(f"\n🎯 AI-Powered Email Demo Complete!")
    print("=" * 60)
    print("📹 This demo showcased:")
    print("   ✅ Intelligent email classification")
    print("   ✅ AI-powered response generation") 
    print("   ✅ Priority detection and sorting")
    print("   ✅ Automatic calendar integration")
    print("   ✅ Business intelligence reporting")
    print("\n💼 BUSINESS VALUE:")
    print(f"   ⏱️  Time saved: ~{len(sample_emails) * 3} minutes of manual email review")
    print(f"   🎯 Priority emails identified: {urgent_count}")
    print(f"   📋 Action items tracked: {urgent_count + task_count + meeting_count}")
    print(f"   🤖 Responses suggested: {len([c for c in classifications if c != 'information'])}")

if __name__ == "__main__":
    demo_main()