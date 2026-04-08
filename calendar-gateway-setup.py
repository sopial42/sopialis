#!/usr/bin/env python3
"""
Calendar Gateway Setup
Configures OAuth and syncs Google Calendar via service account
Run on gateway with: python3 calendar-gateway-setup.py
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

def setup_calendar_sync():
    """Setup and test Google Calendar sync"""
    
    workspace = Path('/data/.openclaw/workspace')
    creds_file = workspace / 'google-calendar-credentials.json'
    
    if not creds_file.exists():
        print("❌ Credentials file not found")
        return False
    
    print("📅 Google Calendar Gateway Setup")
    print("=" * 60)
    
    # Load credentials
    with open(creds_file) as f:
        creds = json.load(f)
    
    print(f"✅ Credentials loaded")
    print(f"   Service Account: {creds['client_email']}")
    print(f"   Project: {creds['project_id']}")
    
    # Try to import and install Google libraries if needed
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        print(f"✅ Google libraries available")
    except ImportError:
        print("📦 Installing Google libraries...")
        import subprocess
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--break-system-packages', '-q',
                'google-auth-oauthlib', 'google-auth-httplib2', 'google-api-python-client'
            ], check=True)
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            print("✅ Google libraries installed")
        except Exception as e:
            print(f"❌ Failed to install: {e}")
            return False
    
    # Create service and test
    try:
        credentials = service_account.Credentials.from_service_account_info(creds)
        service = build('calendar', 'v3', credentials=credentials)
        print("✅ OAuth credentials configured")
    except Exception as e:
        print(f"❌ OAuth setup failed: {e}")
        return False
    
    # Fetch today's events as a test
    calendars = {
        'axel.dhondt@sopial.fr': 'Pro',
        'dhondt.ax@gmail.com': 'Personal'
    }
    
    today = datetime.utcnow().date()
    today_start = f"{today}T00:00:00Z"
    today_end = f"{today}T23:59:59Z"
    
    print(f"\n📋 Syncing today's events ({today})...")
    print("-" * 60)
    
    for cal_id, label in calendars.items():
        try:
            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=today_start,
                timeMax=today_end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            print(f"\n{label} Calendar ({cal_id}):")
            
            if not events:
                print("  No events scheduled")
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
                    print(f"  • {time_str} - {title}{loc_str}")
        
        except Exception as e:
            print(f"\n{label} Calendar: ❌ {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ Calendar sync is ready!")
    print("\nYou can now:")
    print("  1. Check calendars manually with: python3 calendar-gateway-setup.py")
    print("  2. Set up daily reminders via cron")
    print("  3. Integrate with Sopialis for automated updates")
    
    return True

if __name__ == '__main__':
    success = setup_calendar_sync()
    sys.exit(0 if success else 1)
