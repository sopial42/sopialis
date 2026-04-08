#!/usr/bin/env python3
"""
Google Calendar Sync for Sopialis
Fetches events from both pro and personal calendars
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def main():
    creds_file = Path('/data/.openclaw/workspace/google-calendar-credentials.json')
    
    if not creds_file.exists():
        print("Error: Credentials file not found")
        sys.exit(1)
    
    # Try importing Google libraries
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 
                       'google-auth-oauthlib', 'google-auth-httplib2', 
                       'google-api-python-client'], check=True)
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    
    # Load credentials
    with open(creds_file) as f:
        creds_dict = json.load(f)
    
    # Create service
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    service = build('calendar', 'v3', credentials=credentials)
    
    # Get tomorrow's date
    tomorrow = (datetime.utcnow() + timedelta(days=1)).date()
    tomorrow_start = f"{tomorrow}T00:00:00Z"
    tomorrow_end = f"{tomorrow}T23:59:59Z"
    
    calendars = {
        'axel.dhondt@sopial.fr': 'Pro',
        'dhondt.ax@gmail.com': 'Personal'
    }
    
    result = f"📅 Tomorrow's Agenda - {tomorrow}\n"
    result += "=" * 50 + "\n"
    
    for cal_id, label in calendars.items():
        try:
            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=tomorrow_start,
                timeMax=tomorrow_end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            result += f"\n{label} Calendar:\n"
            
            if not events:
                result += "  No events scheduled\n"
            else:
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    title = event.get('summary', 'Untitled')
                    location = event.get('location', '')
                    
                    if 'T' in start:
                        time_obj = datetime.fromisoformat(start.replace('Z', '+00:00'))
                        time_str = time_obj.strftime('%H:%M')
                    else:
                        time_str = "All day"
                    
                    loc_str = f" 📍 {location}" if location else ""
                    result += f"  • {time_str} - {title}{loc_str}\n"
        
        except Exception as e:
            result += f"\n{label} Calendar: Error - {str(e)}\n"
    
    result += "=" * 50 + "\n"
    print(result)

if __name__ == '__main__':
    main()
