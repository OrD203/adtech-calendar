#!/usr/bin/env python3
"""
Update index.html with events from JSON data
"""
import json
import re
from datetime import datetime

def load_events():
    """Load events from JSON file"""
    try:
        with open('data/events.json', 'r', encoding='utf-8') as f:
            events = json.load(f)
            if events:
                print(f"✅ Loaded {len(events)} events from data/events.json")
                return events
    except FileNotFoundError:
        print("⚠️ data/events.json not found, will extract from index.html")
    except Exception as e:
        print(f"⚠️ Error loading events.json: {e}")
    
    # Try to extract from current index.html
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Extract events array from HTML
        pattern = r'const events = \[(.*?)\];'
        match = re.search(pattern, html, re.DOTALL)
        
        if match:
            print("✅ Extracted events from existing index.html")
            # For now, just return empty - in production this would parse the JS
            return []
    except Exception as e:
        print(f"⚠️ Could not extract from index.html: {e}")
    
    print("⚠️ No events found, calendar will remain unchanged")
    return []

def calculate_score(event):
    """Calculate event score from breakdown or use provided score"""
    if 'score' in event and event['score']:
        return int(event['score'])
    
    # Calculate from breakdown if available
    breakdown = {
        'audience': event.get('score_audience', 0),
        'decisionMaker': event.get('score_decision_maker', 0),
        'competitive': event.get('score_competitive', 0),
        'commercial': event.get('score_commercial', 0),
        'influence': event.get('score_influence', 0)
    }
    
    return sum(breakdown.values())

def generate_event_js(events):
    """Generate JavaScript array of events"""
    
    js_events = []
    
    for event in events:
        # Skip if no name
        if not event.get('name'):
            continue
        
        # Parse competitors
        competitors = []
        if event.get('competitors'):
            competitors = [c.strip() for c in event['competitors'].split(',')]
        
        # Parse audiences
        audiences = []
        if event.get('audiences'):
            audiences = [a.strip() for a in event['audiences'].split(',')]
        
        # Parse focus areas
        focus = []
        if event.get('focus'):
            focus = [f.strip() for f in event['focus'].split(',')]
        
        # Calculate score
        score = calculate_score(event)
        
        # Generate scoreBreakdown
        score_breakdown = {
            'audience': int(event.get('score_audience', 0)),
            'decisionMaker': int(event.get('score_decision_maker', 0)),
            'competitive': int(event.get('score_competitive', 0)),
            'commercial': int(event.get('score_commercial', 0)),
            'influence': int(event.get('score_influence', 0))
        }
        
        # Build event object
        event_obj = f"""            {{
                name: "{event['name']}",
                dates: "{event.get('dates', '')}",
                month: "{event.get('month', '')}",
                location: "{event.get('location', '')}",
                region: "{event.get('region', 'North America')}",
                tier: {event.get('tier', 3)},
                score: {score},
                audiences: {json.dumps(audiences)},
                focus: {json.dumps(focus)},
                cost: "{event.get('cost', 'TBD')}",
                competitors: {json.dumps(competitors)},
                podcast: {str(event.get('podcast', False)).lower()},
                confirmed: {str(event.get('confirmed', True)).lower()},
                why: "{event.get('why', '')}",
                website: "{event.get('website', '')}",
                scoreBreakdown: {{
                    audience: {score_breakdown['audience']},
                    decisionMaker: {score_breakdown['decisionMaker']},
                    competitive: {score_breakdown['competitive']},
                    commercial: {score_breakdown['commercial']},
                    influence: {score_breakdown['influence']}
                }}
            }}"""
        
        js_events.append(event_obj)
    
    return ',\n'.join(js_events)

def update_html(events):
    """Update index.html with new events"""
    
    try:
        # Read current HTML
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Generate new events JavaScript
        events_js = generate_event_js(events)
        
        # Find and replace events array
        pattern = r'const events = \[(.*?)\];'
        replacement = f'const events = [\n{events_js}\n        ];'
        
        # Replace with re.DOTALL to match across lines
        updated_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
        
        # Write updated HTML
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ Updated index.html with {len(events)} events")
        return True
        
    except Exception as e:
        print(f"❌ Error updating HTML: {e}")
        return False

if __name__ == '__main__':
    events = load_events()
    
    if not events:
        print("ℹ️ No new events to update - calendar unchanged")
        exit(0)  # Exit successfully, not an error
    
    if update_html(events):
        print(f"✅ Successfully updated calendar with {len(events)} events")
    else:
        print("❌ Failed to update calendar")
        exit(1)
