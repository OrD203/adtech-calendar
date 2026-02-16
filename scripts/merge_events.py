#!/usr/bin/env python3
"""
Merge discovered events with existing events and Google Sheets data
"""
import json
import os
from datetime import datetime

def load_json(filepath):
    """Load JSON file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading {filepath}: {e}")
    return []

def save_json(data, filepath):
    """Save JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def normalize_event_name(name):
    """Normalize event name for comparison"""
    return name.lower().strip().replace('  ', ' ')

def events_are_duplicate(event1, event2):
    """Check if two events are duplicates"""
    name1 = normalize_event_name(event1.get('name', ''))
    name2 = normalize_event_name(event2.get('name', ''))
    
    # Same name = duplicate
    if name1 == name2:
        return True
    
    # Very similar names (edit distance < 3)
    if similarity_score(name1, name2) > 0.85:
        return True
    
    return False

def similarity_score(s1, s2):
    """Calculate similarity between two strings (0-1)"""
    if not s1 or not s2:
        return 0
    
    # Simple similarity check
    words1 = set(s1.split())
    words2 = set(s2.split())
    
    if not words1 or not words2:
        return 0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)

def merge_events():
    """Merge discovered events with existing calendar events"""
    print("🔄 Merging events from all sources...")
    
    # Ensure data directory exists
    import os
    os.makedirs('data', exist_ok=True)
    
    # Load discovered events
    discovered = load_json('data/discovered_events.json')
    print(f"  📊 Discovered events: {len(discovered)}")
    
    # Load Google Sheets events (if available)
    sheets_events = load_json('data/events.json')
    
    # If no existing events.json, initialize with empty list
    if not sheets_events:
        print(f"  📊 Google Sheets events: 0 (initializing)")
        sheets_events = []
    else:
        print(f"  📊 Google Sheets events: {len(sheets_events)}")
    
    # Load current calendar events (extract from index.html)
    current_events = extract_current_events()
    print(f"  📊 Current calendar events: {len(current_events)}")
    
    # Merge all sources
    all_events = []
    seen_events = set()
    
    # Priority 1: Google Sheets events (manually curated)
    for event in sheets_events:
        name = normalize_event_name(event.get('name', ''))
        if name and name not in seen_events:
            all_events.append(event)
            seen_events.add(name)
    
    # Priority 2: Current calendar events
    for event in current_events:
        name = normalize_event_name(event.get('name', ''))
        if name and name not in seen_events:
            all_events.append(event)
            seen_events.add(name)
    
    # Priority 3: Newly discovered events (not duplicates)
    new_count = 0
    for event in discovered:
        name = normalize_event_name(event.get('name', ''))
        
        # Check if it's a duplicate
        is_duplicate = False
        for existing_name in seen_events:
            if similarity_score(name, existing_name) > 0.85:
                is_duplicate = True
                break
        
        if not is_duplicate and name:
            # Enrich discovered event with defaults
            event.setdefault('region', 'North America')
            event.setdefault('tier', 3)
            event.setdefault('score', 65)
            event.setdefault('audiences', ['Ad Tech', 'Agencies', 'Advertisers'])
            event.setdefault('focus', ['Digital marketing'])
            event.setdefault('cost', 'TBD')
            event.setdefault('competitors', ['Taboola', 'MGID'])
            event.setdefault('podcast', False)
            event.setdefault('confirmed', False)
            event.setdefault('why', f'Auto-discovered event - {event.get("source", "web scraping")}')
            event.setdefault('month', extract_month_from_dates(event.get('dates', '')))
            
            # Add score breakdown
            event['score_audience'] = 20
            event['score_decision_maker'] = 16
            event['score_competitive'] = 12
            event['score_commercial'] = 10
            event['score_influence'] = 7
            
            all_events.append(event)
            seen_events.add(name)
            new_count += 1
            print(f"  ✨ New event added: {event['name']}")
    
    print()
    print(f"📊 Merge complete:")
    print(f"  Total events: {len(all_events)}")
    print(f"  New events discovered: {new_count}")
    
    # Save merged events
    save_json(all_events, 'data/events.json')
    
    return all_events

def extract_current_events():
    """Extract events from current index.html"""
    # This would parse the current HTML to get existing events
    # For now, return empty list (events will come from Google Sheets or discovered)
    return []

def extract_month_from_dates(dates):
    """Extract month name from date string"""
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    
    dates_lower = dates.lower()
    
    for month in months:
        if month.lower()[:3] in dates_lower:
            return month
    
    return 'TBD'

if __name__ == '__main__':
    events = merge_events()
    print(f"\n✅ Merged {len(events)} total events")
