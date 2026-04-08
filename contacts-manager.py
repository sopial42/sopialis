#!/usr/bin/env python3
"""
Google Contacts Manager for Sopialis
Create, read, and update contacts (no deletion)
"""

import json
import sys
from pathlib import Path

def setup_contacts_api():
    """Setup and test Google Contacts API"""
    
    workspace = Path('/data/.openclaw/workspace')
    creds_file = workspace / 'google-calendar-credentials.json'
    
    if not creds_file.exists():
        print("❌ Credentials file not found")
        return False
    
    print("📇 Google Contacts API Setup")
    print("=" * 60)
    
    # Load credentials
    with open(creds_file) as f:
        creds = json.load(f)
    
    print(f"✅ Credentials loaded")
    print(f"   Service Account: {creds['client_email']}")
    print(f"   Project: {creds['project_id']}")
    
    # Try to import Google libraries
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
        credentials = service_account.Credentials.from_service_account_info(
            creds,
            scopes=['https://www.googleapis.com/auth/contacts']
        )
        service = build('people', 'v1', credentials=credentials)
        print("✅ Contacts API configured")
    except Exception as e:
        print(f"❌ API setup failed: {e}")
        return False
    
    # Test: List existing contacts
    try:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=5,
            personFields='names,emailAddresses,phoneNumbers'
        ).execute()
        
        connections = results.get('connections', [])
        print(f"\n📋 Current contacts: {len(connections)}")
        
        if connections:
            print("\nFirst 5 contacts:")
            for person in connections:
                names = person.get('names', [])
                if names:
                    name = names[0].get('displayName', 'Unknown')
                    print(f"  • {name}")
    
    except Exception as e:
        print(f"⚠️  Could not list contacts: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Contacts API is ready!")
    print("\nYou can now:")
    print("  1. Create new contacts")
    print("  2. Update existing contacts")
    print("  3. List/search contacts")
    
    return True

def create_contact(name, email=None, phone=None):
    """Create a new contact"""
    
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    creds_file = Path('/data/.openclaw/workspace/google-calendar-credentials.json')
    with open(creds_file) as f:
        creds = json.load(f)
    
    credentials = service_account.Credentials.from_service_account_info(
        creds,
        scopes=['https://www.googleapis.com/auth/contacts']
    )
    service = build('people', 'v1', credentials=credentials)
    
    # Build contact data
    contact = {
        'names': [{'givenName': name}]
    }
    
    if email:
        contact['emailAddresses'] = [{'value': email, 'type': 'work'}]
    
    if phone:
        contact['phoneNumbers'] = [{'value': phone, 'type': 'mobile'}]
    
    try:
        result = service.people().createContact(body=contact).execute()
        contact_id = result['resourceName'].split('/')[-1]
        print(f"✅ Contact created: {name}")
        print(f"   ID: {contact_id}")
        if email:
            print(f"   Email: {email}")
        if phone:
            print(f"   Phone: {phone}")
        return result
    except Exception as e:
        print(f"❌ Failed to create contact: {e}")
        return None

def update_contact(contact_id, name=None, email=None, phone=None):
    """Update an existing contact"""
    
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    creds_file = Path('/data/.openclaw/workspace/google-calendar-credentials.json')
    with open(creds_file) as f:
        creds = json.load(f)
    
    credentials = service_account.Credentials.from_service_account_info(
        creds,
        scopes=['https://www.googleapis.com/auth/contacts']
    )
    service = build('people', 'v1', credentials=credentials)
    
    # Get current contact
    resource_name = f"people/{contact_id}"
    
    try:
        current = service.people().get(
            resourceName=resource_name,
            personFields='names,emailAddresses,phoneNumbers'
        ).execute()
        
        # Update fields
        if name:
            current['names'] = [{'givenName': name}]
        
        if email:
            current['emailAddresses'] = [{'value': email, 'type': 'work'}]
        
        if phone:
            current['phoneNumbers'] = [{'value': phone, 'type': 'mobile'}]
        
        result = service.people().updateContact(
            resourceName=resource_name,
            body=current
        ).execute()
        
        print(f"✅ Contact updated: {name or contact_id}")
        return result
    except Exception as e:
        print(f"❌ Failed to update contact: {e}")
        return None



def list_contacts(max_results=10):
    """List all contacts"""
    
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    creds_file = Path('/data/.openclaw/workspace/google-calendar-credentials.json')
    with open(creds_file) as f:
        creds = json.load(f)
    
    credentials = service_account.Credentials.from_service_account_info(
        creds,
        scopes=['https://www.googleapis.com/auth/contacts']
    )
    service = build('people', 'v1', credentials=credentials)
    
    try:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=max_results,
            personFields='names,emailAddresses,phoneNumbers,resourceName'
        ).execute()
        
        connections = results.get('connections', [])
        print(f"📇 Contacts ({len(connections)}):")
        
        for person in connections:
            names = person.get('names', [])
            emails = person.get('emailAddresses', [])
            phones = person.get('phoneNumbers', [])
            resource_name = person.get('resourceName', '')
            contact_id = resource_name.split('/')[-1] if resource_name else 'unknown'
            
            if names:
                name = names[0].get('displayName', 'Unknown')
                print(f"\n  • {name}")
                print(f"    ID: {contact_id}")
                
                if emails:
                    for email in emails:
                        print(f"    📧 {email.get('value', '')}")
                
                if phones:
                    for phone in phones:
                        print(f"    📱 {phone.get('value', '')}")
        
        return connections
    except Exception as e:
        print(f"❌ Failed to list contacts: {e}")
        return []

if __name__ == '__main__':
    if len(sys.argv) < 2:
        setup_contacts_api()
    else:
        command = sys.argv[1]
        
        if command == 'setup':
            setup_contacts_api()
        
        elif command == 'create':
            if len(sys.argv) < 3:
                print("Usage: python3 contacts-manager.py create <name> [email] [phone]")
                sys.exit(1)
            
            name = sys.argv[2]
            email = sys.argv[3] if len(sys.argv) > 3 else None
            phone = sys.argv[4] if len(sys.argv) > 4 else None
            create_contact(name, email, phone)
        
        elif command == 'update':
            if len(sys.argv) < 3:
                print("Usage: python3 contacts-manager.py update <contact_id> [name] [email] [phone]")
                sys.exit(1)
            
            contact_id = sys.argv[2]
            name = sys.argv[3] if len(sys.argv) > 3 else None
            email = sys.argv[4] if len(sys.argv) > 4 else None
            phone = sys.argv[5] if len(sys.argv) > 5 else None
            update_contact(contact_id, name, email, phone)
        

        
        elif command == 'list':
            max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            list_contacts(max_results)
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
