#!/usr/bin/env python3
"""
AdTech Event Calendar Daily Auto-Updater
Fetches latest event data from multiple sources and updates the calendar JSON
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import schedule
import time
import os
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('event_updater.log'),
        logging.StreamHandler()
    ]
)

class EventDataFetcher:
    """Fetches event data from various sources"""
    
    def __init__(self):
        self.events = []
        self.sources = {
            'affiliate_world': 'https://affiliateworldconferences.com/api/events',
            'dmexco': 'https://dmexco.com/api/event-data',
            'shoptalk': 'https://shoptalk.com/api/events',
            # Add more API endpoints as available
        }
    
    def fetch_from_apis(self) -> List[Dict[str, Any]]:
        """Fetch from official event APIs where available"""
        fetched_events = []
        
        for source_name, url in self.sources.items():
            try:
                logging.info(f"Fetching from {source_name}...")
                # Note: Most events don't have public APIs
                # This is a placeholder for when they do
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    fetched_events.extend(self.normalize_data(data, source_name))
            except Exception as e:
                logging.warning(f"Could not fetch from {source_name}: {e}")
        
        return fetched_events
    
    def fetch_from_10times(self) -> List[Dict[str, Any]]:
        """Fetch from 10times.com (event aggregator)"""
        events = []
        categories = ['advertising', 'ecommerce', 'affiliate-marketing', 'digital-marketing']
        
        for category in categories:
            try:
                url = f"https://10times.com/{category}/conferences-2026"
                logging.info(f"Scraping {category} from 10times.com...")
                # Note: Web scraping requires careful implementation
                # This is a simplified example
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Parse event cards (structure varies by site)
                    # events.extend(self.parse_10times(soup))
            except Exception as e:
                logging.warning(f"Could not scrape {category}: {e}")
        
        return events
    
    def normalize_data(self, raw_data: Any, source: str) -> List[Dict[str, Any]]:
        """Normalize data from different sources to standard format"""
        normalized = []
        # Implement normalization logic based on source
        return normalized
    
    def calculate_score(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate strategic scoring for an event"""
        score_breakdown = {
            'audience': 0,
            'decisionMaker': 0,
            'competitive': 0,
            'commercial': 0,
            'influence': 0
        }
        
        # Audience Relevance (0-30)
        if 'Ad Tech' in event.get('audiences', []) or 'Affiliates' in event.get('audiences', []):
            score_breakdown['audience'] = 25
        elif 'E-commerce' in event.get('audiences', []):
            score_breakdown['audience'] = 22
        else:
            score_breakdown['audience'] = 18
        
        # Decision-Maker Density (0-25)
        if event.get('attendees', 0) > 10000:
            score_breakdown['decisionMaker'] = 22
        elif event.get('attendees', 0) > 5000:
            score_breakdown['decisionMaker'] = 19
        else:
            score_breakdown['decisionMaker'] = 16
        
        # Competitive Presence (0-20)
        competitors = len(event.get('competitors', []))
        score_breakdown['competitive'] = min(20, competitors * 4)
        
        # Commercial Opportunity (0-15)
        if event.get('tier') == 1:
            score_breakdown['commercial'] = 14
        elif event.get('tier') == 2:
            score_breakdown['commercial'] = 11
        else:
            score_breakdown['commercial'] = 8
        
        # Industry Influence (0-10)
        if event.get('prestige', 0) > 8:
            score_breakdown['influence'] = 8
        else:
            score_breakdown['influence'] = 6
        
        total_score = sum(score_breakdown.values())
        
        # Determine tier based on score
        if total_score >= 80:
            tier = 1
        elif total_score >= 60:
            tier = 2
        else:
            tier = 3
        
        return {
            'score': total_score,
            'tier': tier,
            'scoreBreakdown': score_breakdown
        }
    
    def update_events_json(self, events: List[Dict[str, Any]]):
        """Update the events.json file"""
        output_file = '/mnt/user-data/outputs/events.json'
        
        try:
            with open(output_file, 'w') as f:
                json.dump({
                    'lastUpdated': datetime.now().isoformat(),
                    'events': events,
                    'metadata': {
                        'totalEvents': len(events),
                        'sources': list(self.sources.keys()),
                        'nextUpdate': (datetime.now() + timedelta(days=1)).isoformat()
                    }
                }, f, indent=2)
            
            logging.info(f"Successfully updated {output_file} with {len(events)} events")
            return True
        except Exception as e:
            logging.error(f"Failed to update events.json: {e}")
            return False


class ManualEventManager:
    """
    Manages manually curated events that should always be included
    These are high-priority events verified by the team
    """
    
    def get_core_events(self) -> List[Dict[str, Any]]:
        """Return the core manually-verified events"""
        # This would load from a separate JSON file of verified events
        core_events_file = '/home/claude/core_events.json'
        
        if os.path.exists(core_events_file):
            with open(core_events_file, 'r') as f:
                return json.load(f)
        
        return []


def daily_update():
    """Main function to run daily updates"""
    logging.info("=" * 50)
    logging.info("Starting daily event calendar update")
    logging.info("=" * 50)
    
    fetcher = EventDataFetcher()
    manager = ManualEventManager()
    
    # Get manually curated events (always keep these)
    core_events = manager.get_core_events()
    logging.info(f"Loaded {len(core_events)} core events")
    
    # Fetch new/updated events from APIs
    api_events = fetcher.fetch_from_apis()
    logging.info(f"Fetched {len(api_events)} events from APIs")
    
    # Merge and deduplicate
    all_events = core_events.copy()
    
    # Add API events that aren't duplicates
    for api_event in api_events:
        if not any(e['name'] == api_event['name'] and e['dates'] == api_event['dates'] 
                   for e in all_events):
            all_events.append(api_event)
    
    # Update scores for all events
    for event in all_events:
        if 'score' not in event or event.get('autoUpdate', True):
            scoring = fetcher.calculate_score(event)
            event.update(scoring)
    
    # Save updated events
    if fetcher.update_events_json(all_events):
        logging.info("Daily update completed successfully")
    else:
        logging.error("Daily update failed")


def run_scheduler():
    """Run the scheduler to update daily at 3 AM"""
    # Schedule daily update at 3 AM
    schedule.every().day.at("03:00").do(daily_update)
    
    # Also run immediately on startup
    logging.info("Running initial update...")
    daily_update()
    
    logging.info("Scheduler started. Waiting for next update at 03:00...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    # For manual testing, run once
    if os.getenv('RUN_ONCE', 'false').lower() == 'true':
        daily_update()
    else:
        # Run as a service
        run_scheduler()
