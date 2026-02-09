# AdTech Event Calendar - Auto-Update System Deployment Guide

## Overview
This system automatically updates your event calendar daily by:
1. Maintaining core manually-verified events (63 current events)
2. Fetching updates from event organizer APIs (when available)
3. Web scraping event aggregator sites (10times.com, online.marketing)
4. Re-calculating strategic scores based on latest data
5. Generating updated JSON file that the HTML calendar reads from

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Daily Update Process                      │
│                    (Runs at 3 AM daily)                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  1. Load Core Events (Verified)       │
        │     - Your 63 manually-verified events│
        │     - Always included, never removed  │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  2. Fetch from APIs                   │
        │     - Affiliate World API             │
        │     - DMEXCO API (if available)       │
        │     - Other event organizer APIs      │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  3. Web Scraping (Backup)             │
        │     - 10times.com event listings      │
        │     - online.marketing calendar       │
        │     - Event organizer websites        │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  4. Merge & Deduplicate               │
        │     - Combine all sources             │
        │     - Remove duplicates by name+date  │
        │     - Prioritize verified sources     │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  5. Re-calculate Scores               │
        │     - Apply scoring algorithm         │
        │     - Assign tier classification      │
        │     - Update competitor presence      │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  6. Generate events.json              │
        │     - Timestamp with lastUpdated      │
        │     - Full event data with scores     │
        │     - Metadata (sources, next update) │
        └───────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  7. HTML Calendar Auto-Loads          │
        │     - Fetches events.json on page load│
        │     - Displays "Last Updated" badge   │
        │     - Shows all events dynamically    │
        └───────────────────────────────────────┘
```

## Deployment Options

### Option 1: Cloud Hosted (Recommended for Production)

#### Using AWS Lambda + EventBridge
1. **Setup Lambda Function**:
   ```bash
   # Package dependencies
   pip install -r requirements.txt -t package/
   cd package && zip -r ../deployment.zip .
   cd .. && zip -g deployment.zip event_updater.py
   
   # Upload to AWS Lambda
   aws lambda create-function \
     --function-name adtech-calendar-updater \
     --runtime python3.11 \
     --handler event_updater.lambda_handler \
     --zip-file fileb://deployment.zip \
     --role arn:aws:iam::ACCOUNT:role/lambda-execution-role
   ```

2. **Setup EventBridge Rule**:
   ```bash
   # Daily trigger at 3 AM UTC
   aws events put-rule \
     --name adtech-calendar-daily \
     --schedule-expression "cron(0 3 * * ? *)"
   
   aws events put-targets \
     --rule adtech-calendar-daily \
     --targets "Id"="1","Arn"="arn:aws:lambda:REGION:ACCOUNT:function:adtech-calendar-updater"
   ```

3. **Setup S3 for events.json**:
   ```bash
   # Create bucket
   aws s3 mb s3://adtech-calendar-data
   
   # Enable public read for events.json
   aws s3api put-object-acl \
     --bucket adtech-calendar-data \
     --key events.json \
     --acl public-read
   ```

4. **Update HTML to fetch from S3**:
   ```javascript
   const EVENTS_URL = 'https://adtech-calendar-data.s3.amazonaws.com/events.json';
   ```

**Monthly Cost**: ~$2-5/month (Lambda + S3)

---

#### Using GitHub Actions (Free)
1. **Create `.github/workflows/update-calendar.yml`**:
   ```yaml
   name: Update Event Calendar
   
   on:
     schedule:
       - cron: '0 3 * * *'  # Daily at 3 AM UTC
     workflow_dispatch:  # Manual trigger
   
   jobs:
     update:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         
         - name: Install dependencies
           run: |
             pip install requests beautifulsoup4 schedule
         
         - name: Run updater
           env:
             RUN_ONCE: 'true'
           run: |
             python event_updater.py
         
         - name: Commit and push if changed
           run: |
             git config user.name "Calendar Bot"
             git config user.email "bot@example.com"
             git add events.json
             git diff --quiet && git diff --staged --quiet || \
               git commit -m "Auto-update: $(date)" && git push
   ```

2. **Host events.json on GitHub Pages** (free):
   - Enable GitHub Pages in repo settings
   - Access at: `https://username.github.io/repo-name/events.json`

**Monthly Cost**: $0 (free)

---

#### Using Vercel Serverless Functions (Free Tier)
1. **Create `api/update-events.py`**:
   ```python
   from event_updater import daily_update
   
   def handler(request):
       daily_update()
       return {'statusCode': 200, 'body': 'Updated'}
   ```

2. **Create `vercel.json`**:
   ```json
   {
     "crons": [{
       "path": "/api/update-events",
       "schedule": "0 3 * * *"
     }]
   }
   ```

3. **Deploy**:
   ```bash
   vercel deploy --prod
   ```

**Monthly Cost**: $0 (free tier)

---

### Option 2: Self-Hosted (VPS/Server)

#### Using systemd (Linux Server)
1. **Copy files to server**:
   ```bash
   scp event_updater.py user@server:/opt/adtech-calendar/
   scp core_events.json user@server:/opt/adtech-calendar/
   ```

2. **Create systemd service** (`/etc/systemd/system/adtech-calendar.service`):
   ```ini
   [Unit]
   Description=AdTech Event Calendar Updater
   After=network.target
   
   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/adtech-calendar
   ExecStart=/usr/bin/python3 /opt/adtech-calendar/event_updater.py
   Restart=on-failure
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start**:
   ```bash
   sudo systemctl enable adtech-calendar
   sudo systemctl start adtech-calendar
   sudo systemctl status adtech-calendar
   ```

4. **Serve events.json via nginx**:
   ```nginx
   server {
       listen 80;
       server_name calendar-api.yourdomain.com;
       
       location /events.json {
           root /opt/adtech-calendar;
           add_header Access-Control-Allow-Origin *;
           expires 1h;
       }
   }
   ```

**Monthly Cost**: $5-10/month (basic VPS)

---

### Option 3: Docker Container

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY event_updater.py .
COPY core_events.json .

CMD ["python", "event_updater.py"]
```

**Deploy with docker-compose**:
```yaml
version: '3'
services:
  calendar-updater:
    build: .
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - TZ=UTC
```

---

## Configuration

### Environment Variables
```bash
# Required
EVENTS_OUTPUT_PATH=/mnt/user-data/outputs/events.json
CORE_EVENTS_PATH=/home/claude/core_events.json

# Optional
UPDATE_TIME=03:00  # Time to run daily update (24hr format)
LOG_LEVEL=INFO
ENABLE_SCRAPING=true
API_TIMEOUT=10

# API Keys (when available)
AFFILIATE_WORLD_API_KEY=your_key_here
```

### requirements.txt
```
requests==2.31.0
beautifulsoup4==4.12.2
schedule==1.2.0
lxml==4.9.3
```

---

## Manual Event Management

### Adding a New Event Manually
Edit `core_events.json`:
```json
{
  "name": "New Event Name",
  "dates": "Mar 15-17",
  "month": "March",
  "location": "City, Country",
  "region": "North America",
  "tier": 2,
  "score": 75,
  "audiences": ["Ad Tech", "Affiliates"],
  "focus": ["Performance marketing"],
  "cost": "$495-995 USD",
  "competitors": ["Taboola", "MGID"],
  "podcast": true,
  "confirmed": true,
  "autoUpdate": false,
  "why": "Reason to attend",
  "website": "https://event.com",
  "scoreBreakdown": {
    "audience": 23,
    "decisionMaker": 19,
    "competitive": 15,
    "commercial": 12,
    "influence": 6
  }
}
```

**Note**: Set `"autoUpdate": false` to prevent the system from modifying your manual edits.

---

## Monitoring & Maintenance

### Check Logs
```bash
# View real-time logs
tail -f event_updater.log

# Check for errors
grep ERROR event_updater.log
```

### Manual Update Trigger
```bash
# Run update immediately
RUN_ONCE=true python event_updater.py
```

### Verify Events Count
```bash
# Check how many events were updated
cat events.json | jq '.metadata.totalEvents'

# Check last update time
cat events.json | jq '.lastUpdated'
```

---

## Troubleshooting

### Issue: No events fetched from APIs
**Solution**: Most event organizers don't provide public APIs. The system falls back to web scraping, which requires:
1. Proper user-agent headers
2. Rate limiting to avoid blocks
3. Parsing logic for each site's HTML structure

### Issue: Duplicate events appearing
**Solution**: Check deduplication logic in `event_updater.py`:
```python
# Events are deduplicated by name + dates
if not any(e['name'] == api_event['name'] and e['dates'] == api_event['dates'] 
           for e in all_events):
```

### Issue: Scores changing unexpectedly
**Solution**: Events with `"autoUpdate": true` will have scores recalculated. Set to `false` for manual control.

---

## Recommended Setup for Your Use Case

Based on your needs, I recommend:

**Best Option: GitHub Actions + GitHub Pages** (Free, reliable)
1. Zero cost
2. Version control for events
3. Automatic backups
4. Easy to review changes via commits
5. No server maintenance

**Alternative: AWS Lambda + S3** (Low cost, enterprise-grade)
1. More reliable than free tiers
2. Better performance
3. Professional infrastructure
4. ~$3/month cost

---

## Next Steps

1. **Choose deployment option** (GitHub Actions recommended)
2. **Set up hosting** for events.json
3. **Update HTML calendar** to fetch from events.json URL
4. **Test the update** process manually
5. **Monitor logs** for first few days
6. **Add more event sources** to fetcher as APIs become available

Would you like me to implement any specific deployment option in detail?
