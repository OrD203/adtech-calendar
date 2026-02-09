# AdTech Event Calendar - Auto-Update System

## 🚀 Quick Setup (5 Minutes)

### Option 1: GitHub Actions (Recommended - FREE)

**Perfect for: Teams wanting zero-cost, automated daily updates with version control**

#### Setup Steps:

1. **Create a GitHub repository**:
   ```bash
   git init adtech-calendar
   cd adtech-calendar
   ```

2. **Add the files**:
   ```bash
   # Copy these files to your repo:
   - event_updater.py
   - core_events.json
   - requirements.txt
   - .github/workflows/update-calendar.yml
   - index.html (your calendar HTML)
   ```

3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial calendar setup"
   git remote add origin https://github.com/YOUR_USERNAME/adtech-calendar.git
   git push -u origin main
   ```

4. **Enable GitHub Pages**:
   - Go to repo Settings > Pages
   - Source: Deploy from branch
   - Branch: main / root
   - Click Save

5. **Your calendar is now live at**:
   ```
   https://YOUR_USERNAME.github.io/adtech-calendar/
   ```

6. **Daily updates run automatically at 3 AM UTC**
   - View runs: Actions tab in your repo
   - Manual trigger: Actions > Update AdTech Event Calendar > Run workflow

**Total Cost**: $0/month ✅
**Maintenance**: Zero - fully automated ✅

---

### Option 2: Simple Web Server (If you already have hosting)

1. **Upload files to your web server**:
   ```bash
   scp event_updater.py your-server:/var/www/calendar/
   scp core_events.json your-server:/var/www/calendar/
   scp index.html your-server:/var/www/calendar/
   ```

2. **Set up daily cron job**:
   ```bash
   # SSH into server
   ssh your-server
   
   # Edit crontab
   crontab -e
   
   # Add this line (runs at 3 AM daily):
   0 3 * * * cd /var/www/calendar && python3 event_updater.py
   ```

3. **Access your calendar**:
   ```
   https://yourdomain.com/calendar/
   ```

---

## 📁 File Structure

```
adtech-calendar/
├── index.html                          # Your calendar interface
├── events.json                         # Auto-generated daily (DO NOT EDIT)
├── core_events.json                    # Manually verified events (EDIT THIS)
├── event_updater.py                    # Update script
├── requirements.txt                    # Python dependencies
├── .github/
│   └── workflows/
│       └── update-calendar.yml         # GitHub Actions config
├── DEPLOYMENT_GUIDE.md                 # Detailed deployment docs
└── README.md                           # This file
```

---

## ✏️ Managing Events

### Adding a New Event

Edit `core_events.json` and add your event:

```json
{
  "name": "Your Event Name",
  "dates": "Mar 15-17",
  "month": "March",
  "location": "New York, USA",
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
  "why": "Premier performance marketing event with 5K+ attendees",
  "website": "https://yourevent.com",
  "scoreBreakdown": {
    "audience": 23,
    "decisionMaker": 19,
    "competitive": 15,
    "commercial": 12,
    "influence": 6
  }
}
```

**Important**: Set `"autoUpdate": false` to prevent the system from changing your manual edits.

### Removing an Event

Simply delete the event object from `core_events.json`.

### Updating Event Details

Edit the event in `core_events.json` and commit the changes.

---

## 🔄 How Auto-Updates Work

```
Every day at 3 AM UTC:
┌─────────────────────────────────────────────┐
│ 1. Load your verified events                │
│    from core_events.json                    │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 2. Fetch new events from:                   │
│    • Event organizer APIs                   │
│    • Event aggregator sites                 │
│    • Web scraping                           │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 3. Merge & deduplicate                      │
│    Remove duplicate events                  │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 4. Calculate scores                         │
│    Apply strategic scoring algorithm        │
└─────────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ 5. Generate events.json                     │
│    Your calendar reads from this file       │
└─────────────────────────────────────────────┘
```

---

## 🔍 Monitoring Updates

### GitHub Actions (Option 1)
- Go to your repo's **Actions** tab
- See all update runs with success/failure status
- Click any run to see detailed logs
- Get email notifications on failures

### Command Line
```bash
# Check last update time
cat events.json | grep lastUpdated

# Count total events
cat events.json | grep -c '"name"'

# View update logs
tail -f event_updater.log
```

---

## 🎯 Current Status

Your calendar currently has:
- **63 verified events** for 2026
- **15 Tier 1** must-attend events
- **45 Tier 2** strategic events
- **3 Tier 3** opportunistic events
- Coverage across **5 regions**
- Competitor tracking for **4 platforms**

---

## 🆘 Troubleshooting

### "Events not updating"
**Check**:
1. GitHub Actions is enabled in repo settings
2. Workflow file is in `.github/workflows/`
3. Python dependencies installed correctly
4. Check Actions tab for error logs

### "Duplicate events appearing"
The system deduplicates by `name + dates`. If you see duplicates:
1. Check `core_events.json` for duplicates
2. Ensure event names match exactly
3. Review `event_updater.py` deduplication logic

### "Calendar showing old data"
1. Hard refresh browser (Ctrl+Shift+R)
2. Check `events.json` lastUpdated timestamp
3. Verify GitHub Pages is serving latest version

---

## 📊 Data Sources

The system can fetch from:
- ✅ **Manually verified** (core_events.json) - Always included
- 🔄 **Event organizer APIs** - When available
- 🌐 **10times.com** - Conference aggregator
- 🌐 **online.marketing** - Marketing event calendar
- 🔍 **Web scraping** - Direct from event websites

---

## 🔐 Security Notes

- **No API keys required** for basic functionality
- Events data is public information
- Web scraping respects robots.txt
- Rate limiting prevents server overload
- All dependencies are verified packages

---

## 📞 Support

**Questions?** Check:
1. `DEPLOYMENT_GUIDE.md` - Detailed setup instructions
2. GitHub Actions logs - View update runs
3. `event_updater.log` - Local update logs

---

## 🎉 You're All Set!

Your calendar will now:
- ✅ Update automatically every day at 3 AM
- ✅ Add new events as they're announced
- ✅ Keep your manually-verified events safe
- ✅ Calculate strategic scores
- ✅ Track competitor presence
- ✅ Show "Last Updated" timestamp

**Next Steps**:
1. Star ⭐ this repo to bookmark it
2. Enable GitHub notifications for update status
3. Share your calendar URL with your team!
