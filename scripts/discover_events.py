#!/usr/bin/env python3
"""
Automatically discover new AdTech and Commerce events from the web
"""
import os
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

class EventDiscovery:
    """Discover new events from various sources"""
    
    def __init__(self):
        self.discovered_events = []
        self.sources = []
        
        # Keywords for event discovery
        self.keywords = [
            "adtech conference 2026",
            "digital marketing conference 2026",
            "affiliate marketing conference 2026",
            "e-commerce conference 2026",
            "retail conference 2026",
            "programmatic advertising conference 2026",
            "performance marketing conference 2026",
            "content marketing conference 2026",
            "social media marketing conference 2026",
            "commerce conference 2026"
        ]
        
        # Relevant categories
        self.categories = [
            "advertising",
            "marketing",
            "digital-marketing",
            "e-commerce",
            "retail",
            "technology",
            "affiliate-marketing"
        ]
    
    def discover_from_10times(self):
        """Scrape events from 10Times.com"""
        print("🔍 Searching 10Times.com...")
        
        base_url = "https://10times.com"
        categories = ["advertising", "marketing", "ecommerce", "digital-marketing"]
        
        for category in categories:
            try:
                url = f"{base_url}/{category}/usa"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    events = soup.find_all('div', class_='event-card')
                    
                    for event in events:
                        event_data = self._parse_10times_event(event)
                        if event_data and self._is_2026_event(event_data):
                            self.discovered_events.append(event_data)
                            print(f"  ✅ Found: {event_data['name']}")
                
            except Exception as e:
                print(f"  ⚠️ Error scraping 10Times {category}: {e}")
        
        return len(self.discovered_events)
    
    def discover_from_eventbrite(self):
        """Search Eventbrite API for events"""
        print("🔍 Searching Eventbrite...")
        
        # Eventbrite API (requires API key, but we can scrape search results)
        for keyword in self.keywords[:5]:  # Limit to avoid rate limits
            try:
                url = f"https://www.eventbrite.com/d/online/{ keyword.replace(' ', '-')}/"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    events = soup.find_all('div', class_='search-event-card')
                    
                    for event in events[:10]:  # Limit per keyword
                        event_data = self._parse_eventbrite_event(event)
                        if event_data and self._is_2026_event(event_data):
                            self.discovered_events.append(event_data)
                            print(f"  ✅ Found: {event_data['name']}")
                
            except Exception as e:
                print(f"  ⚠️ Error searching Eventbrite for '{keyword}': {e}")
        
        return len(self.discovered_events)
    
    def discover_from_google_search(self):
        """Use Google Custom Search API to find events"""
        print("🔍 Searching via Google...")
        
        # Note: Requires Google Custom Search API key
        api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        cx = os.getenv('GOOGLE_SEARCH_CX')
        
        if not api_key or not cx:
            print("  ⚠️ Google Search API not configured (skipping)")
            return 0
        
        base_url = "https://www.googleapis.com/customsearch/v1"
        
        for keyword in self.keywords:
            try:
                params = {
                    'key': api_key,
                    'cx': cx,
                    'q': keyword,
                    'num': 10
                }
                
                response = requests.get(base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    results = response.json()
                    
                    for item in results.get('items', []):
                        event_data = self._parse_google_result(item)
                        if event_data and self._is_2026_event(event_data):
                            self.discovered_events.append(event_data)
                            print(f"  ✅ Found: {event_data['name']}")
                
            except Exception as e:
                print(f"  ⚠️ Error with Google Search: {e}")
        
        return len(self.discovered_events)
    
    def discover_from_rss_feeds(self):
        """Monitor RSS feeds from event sites"""
        print("🔍 Checking RSS feeds...")
        
        feeds = [
            "https://www.eventbrite.com/rss/organizer_list_events/ORGANIZER_ID",
            "https://10times.com/rss/feed",
        ]
        
        # RSS parsing would go here
        # For now, placeholder
        return 0
    
    def discover_from_known_organizers(self):
        """Check websites of known event organizers"""
        print("🔍 Checking known organizers...")
        
        organizers = [
            {
                'name': 'Advertising Week',
                'url': 'https://advertisingweek.com/events/',
                'parser': self._parse_adweek_events
            },
            {
                'name': 'Informa Tech',
                'url': 'https://informaconnect.com/events/',
                'parser': self._parse_informa_events
            },
            {
                'name': 'DigiMarCon',
                'url': 'https://digimarcon.com/events/',
                'parser': self._parse_digimarcon_events
            }
        ]
        
        for organizer in organizers:
            try:
                response = requests.get(organizer['url'], timeout=10)
                
                if response.status_code == 200:
                    events = organizer['parser'](response.content)
                    for event in events:
                        if self._is_2026_event(event):
                            self.discovered_events.append(event)
                            print(f"  ✅ Found: {event['name']}")
                            
            except Exception as e:
                print(f"  ⚠️ Error with {organizer['name']}: {e}")
        
        return len(self.discovered_events)
    
    # Parsing helper methods
    
    def _parse_10times_event(self, event_element):
        """Parse event from 10Times HTML"""
        try:
            name = event_element.find('h2').text.strip()
            date_elem = event_element.find('span', class_='date')
            location_elem = event_element.find('span', class_='location')
            link_elem = event_element.find('a', href=True)
            
            return {
                'name': name,
                'dates': date_elem.text.strip() if date_elem else '',
                'location': location_elem.text.strip() if location_elem else '',
                'website': link_elem['href'] if link_elem else '',
                'source': '10Times',
                'tier': 3,  # Default to tier 3 for auto-discovered
                'score': 60
            }
        except:
            return None
    
    def _parse_eventbrite_event(self, event_element):
        """Parse event from Eventbrite HTML"""
        # Parsing logic here
        return None
    
    def _parse_google_result(self, result):
        """Parse Google search result"""
        try:
            # Extract structured data from Google result
            title = result.get('title', '')
            link = result.get('link', '')
            snippet = result.get('snippet', '')
            
            # Try to extract date from snippet
            dates = self._extract_dates_from_text(snippet)
            location = self._extract_location_from_text(snippet)
            
            if dates:
                return {
                    'name': title,
                    'dates': dates,
                    'location': location or 'TBD',
                    'website': link,
                    'source': 'Google Search',
                    'tier': 3,
                    'score': 60
                }
        except:
            return None
        
        return None
    
    def _parse_adweek_events(self, html_content):
        """Parse Advertising Week events"""
        events = []
        # Parsing logic here
        return events
    
    def _parse_informa_events(self, html_content):
        """Parse Informa events"""
        events = []
        # Parsing logic here
        return events
    
    def _parse_digimarcon_events(self, html_content):
        """Parse DigiMarCon events"""
        events = []
        # Parsing logic here
        return events
    
    def _is_2026_event(self, event):
        """Check if event is in 2026"""
        try:
            dates = event.get('dates', '')
            return '2026' in dates or '26' in dates
        except:
            return False
    
    def _extract_dates_from_text(self, text):
        """Extract dates from text using regex"""
        # Match patterns like "March 20-21, 2026" or "Apr 28-30"
        patterns = [
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}-?\d{0,2},? 2026',
            r'(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}-?\d{0,2},? 2026'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_location_from_text(self, text):
        """Extract location from text"""
        # Look for city, state/country patterns
        pattern = r'([A-Z][a-z]+(?:[ -][A-Z][a-z]+)*),?\s+([A-Z]{2,}|[A-Z][a-z]+)'
        match = re.search(pattern, text)
        
        if match:
            return f"{match.group(1)}, {match.group(2)}"
        
        return None
    
    def deduplicate_events(self):
        """Remove duplicate events based on name/date similarity"""
        print("🔄 Removing duplicates...")
        
        unique_events = []
        seen = set()
        
        for event in self.discovered_events:
            # Create a signature for the event
            signature = f"{event['name'].lower()}_{event.get('dates', '')}"
            
            if signature not in seen:
                seen.add(signature)
                unique_events.append(event)
        
        removed = len(self.discovered_events) - len(unique_events)
        print(f"  ℹ️ Removed {removed} duplicates")
        
        self.discovered_events = unique_events
        return len(unique_events)
    
    def filter_relevant_events(self):
        """Filter events to only include AdTech/Commerce related"""
        print("🎯 Filtering for relevance...")
        
        relevant_keywords = [
            'adtech', 'advertising', 'marketing', 'digital', 'commerce',
            'e-commerce', 'retail', 'affiliate', 'performance', 'media',
            'programmatic', 'content', 'social media', 'seo', 'sem'
        ]
        
        filtered = []
        
        for event in self.discovered_events:
            name_lower = event['name'].lower()
            
            # Check if any relevant keyword is in the name
            if any(keyword in name_lower for keyword in relevant_keywords):
                filtered.append(event)
        
        removed = len(self.discovered_events) - len(filtered)
        print(f"  ℹ️ Filtered out {removed} irrelevant events")
        
        self.discovered_events = filtered
        return len(filtered)
    
    def save_discovered_events(self, filepath='data/discovered_events.json'):
        """Save discovered events to JSON"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.discovered_events, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(self.discovered_events)} events to {filepath}")
        return len(self.discovered_events)


def main():
    """Main discovery process"""
    print("🚀 Starting automated event discovery...")
    print(f"📅 Looking for events in 2026")
    print()
    
    discovery = EventDiscovery()
    
    # Run discovery from all sources
    discovery.discover_from_10times()
    discovery.discover_from_eventbrite()
    discovery.discover_from_google_search()
    discovery.discover_from_known_organizers()
    
    print()
    print(f"📊 Total events found: {len(discovery.discovered_events)}")
    
    # Clean up results
    discovery.deduplicate_events()
    discovery.filter_relevant_events()
    
    print()
    print(f"✅ Final event count: {len(discovery.discovered_events)}")
    
    # Save results
    discovery.save_discovered_events()
    
    return discovery.discovered_events


if __name__ == '__main__':
    events = main()
    
    if events:
        print()
        print("🎉 Event discovery complete!")
        print(f"📝 Found {len(events)} new events")
    else:
        print()
        print("⚠️ No new events discovered")
