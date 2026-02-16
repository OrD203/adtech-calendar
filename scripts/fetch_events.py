#!/usr/bin/env python3
"""
Fetch events from Google Sheets and save to JSON
"""
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def fetch_events_from_sheet():
    """Fetch events from Google Sheets"""
    
    # Setup Google Sheets API credentials
    credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
    sheet_id = os.getenv('SHEET_ID')
    
    if not credentials_json or not sheet_id:
        print("❌ Missing Google Sheets credentials or Sheet ID")
        return None
    
    # Parse credentials
    creds_dict = json.loads(credentials_json)
    
    # Authenticate
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # Open the sheet
    try:
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)  # First sheet
        
        # Get all records
        records = worksheet.get_all_records()
        
        print(f"✅ Fetched {len(records)} events from Google Sheets")
        
        # Save to JSON file
        with open('data/events.json', 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        return records
        
    except Exception as e:
        print(f"❌ Error fetching from Google Sheets: {e}")
        return None

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    events = fetch_events_from_sheet()
    
    if events:
        print(f"✅ Successfully saved {len(events)} events to data/events.json")
    else:
        print("❌ Failed to fetch events")
        exit(1)
