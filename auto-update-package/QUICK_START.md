# 🚀 QUICK START - 5 Minute Setup

## Your Calendar - Auto-Updates Daily, $0 Cost

### What You Have Now:
✅ **63 verified events** for 2026  
✅ **Strategic scoring** (0-100 scale)  
✅ **Competitor tracking** (4 platforms)  
✅ **Complete auto-update system** ready to deploy  

---

## 📦 Option 1: GitHub (RECOMMENDED - FREE)

### Step 1: Create GitHub Account (2 min)
1. Go to https://github.com
2. Click "Sign up"
3. Choose a username
4. Verify email

### Step 2: Create Repository (1 min)
1. Click "+" in top-right
2. Click "New repository"
3. Name: `adtech-calendar`
4. Make it **Public** (required for free hosting)
5. Click "Create repository"

### Step 3: Upload Files (1 min)
1. Click "uploading an existing file"
2. Drag and drop these 8 files:
   ```
   ✓ index.html
   ✓ event_updater.py
   ✓ core_events.json
   ✓ requirements.txt
   ✓ README.md
   ✓ DEPLOYMENT_GUIDE.md
   ✓ setup.sh
   ✓ .github/workflows/update-calendar.yml
   ```
3. Click "Commit changes"

### Step 4: Enable GitHub Pages (1 min)
1. Click "Settings" tab
2. Scroll to "Pages" in left sidebar
3. Under "Source": Select "Deploy from a branch"
4. Under "Branch": Select "main" and "/ (root)"
5. Click "Save"

### Step 5: Done! 🎉
Your calendar is now live at:
```
https://YOUR_USERNAME.github.io/adtech-calendar/
```

**What happens next:**
- ✅ Calendar updates automatically every day at 3 AM UTC
- ✅ New events added automatically
- ✅ You get email notifications (optional)
- ✅ View update history in "Actions" tab

**Total cost:** $0/month forever  
**Maintenance required:** 0 hours/month

---

## 📦 Option 2: Your Web Server (10 min)

### Requirements:
- Web server with SSH access
- Python 3.11+ installed
- Cron job access

### Steps:

1. **Upload files to server:**
   ```bash
   scp -r auto-update-package/* user@your-server:/var/www/calendar/
   ```

2. **SSH into server:**
   ```bash
   ssh user@your-server
   cd /var/www/calendar
   ```

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Set up cron job:**
   ```bash
   crontab -e
   # Add this line:
   0 3 * * * cd /var/www/calendar && python3 event_updater.py
   ```

5. **Test it:**
   ```bash
   RUN_ONCE=true python3 event_updater.py
   # Check if events.json was created
   ```

6. **Access calendar:**
   ```
   https://yourdomain.com/calendar/
   ```

**Monthly cost:** $5-10 (server hosting)

---

## 📦 Option 3: Docker (10 min)

### Requirements:
- Docker installed
- docker-compose installed

### Steps:

1. **Navigate to package directory:**
   ```bash
   cd auto-update-package
   ```

2. **Run setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   # Choose option 3 (Docker)
   ```

3. **Start container:**
   ```bash
   docker-compose up -d
   ```

4. **Check status:**
   ```bash
   docker-compose logs -f
   ```

5. **Access events.json:**
   ```bash
   # Located in ./data/events.json
   ```

6. **Serve with nginx or copy to web server**

**Monthly cost:** Depends on hosting

---

## 🎯 Which Option Should I Choose?

### Choose GitHub if:
- ✅ You want FREE hosting
- ✅ You want ZERO maintenance
- ✅ You want automatic backups
- ✅ You want version control
- ✅ You're okay with public repo

→ **Best for 95% of users**

### Choose Web Server if:
- You already pay for hosting
- You want custom domain immediately
- You need private hosting

### Choose Docker if:
- You're a DevOps team
- You use containers already
- You want maximum portability

---

## ✏️ How to Manage Events

### Adding an Event:

1. Open `core_events.json`
2. Add your event:
```json
{
  "name": "New Event Name",
  "dates": "Mar 15-17",
  "month": "March",
  "location": "New York, USA",
  "region": "North America",
  "tier": 2,
  "score": 75,
  "audiences": ["Ad Tech", "Affiliates"],
  "focus": ["Performance marketing"],
  "cost": "$495-995 USD",
  "competitors": ["Taboola"],
  "confirmed": true,
  "autoUpdate": false,
  "website": "https://event.com"
}
```
3. Save and commit (GitHub) or upload (server)

### Removing an Event:
1. Delete event from `core_events.json`
2. Save and commit/upload

**Important:** Set `"autoUpdate": false` to protect your manual edits!

---

## 📊 What Gets Updated Automatically

### System Adds:
- ✅ New events announced after setup
- ✅ Date changes to existing events
- ✅ Location updates
- ✅ Competitor presence updates

### System Keeps:
- ✅ All your manually-verified events
- ✅ Events marked `"autoUpdate": false`
- ✅ Your custom scoring overrides

### System Removes:
- ✅ Duplicate events
- ✅ Cancelled events (when detected)
- ✅ Past events (after they happen)

---

## 🔍 Monitoring Your Calendar

### GitHub Actions (Option 1):
1. Go to your repo
2. Click "Actions" tab
3. See all update runs
4. Click any run for details
5. Green ✓ = success, Red ✗ = error

### Command Line:
```bash
# Check last update time
cat events.json | grep lastUpdated

# Count total events  
cat events.json | grep -c '"name"'

# View logs
tail -f event_updater.log
```

### Calendar Display:
Your calendar shows "Last Updated: [timestamp]" at top

---

## 🆘 Common Issues

### "Calendar not updating"
**Fix:** Check GitHub Actions tab for errors

### "Duplicate events showing"
**Fix:** Edit `core_events.json` to remove duplicates

### "My manual changes disappeared"
**Fix:** Set `"autoUpdate": false` on those events

### "GitHub Pages not working"
**Fix:** Ensure repo is Public and Pages is enabled in Settings

---

## 📞 Getting Help

1. **README.md** - Quick reference
2. **DEPLOYMENT_GUIDE.md** - Detailed instructions
3. **EXECUTIVE_SUMMARY.md** - Overview and options
4. **GitHub Actions Logs** - Debug update issues
5. **event_updater.log** - Local troubleshooting

---

## ✅ Checklist

Before you start:
- [ ] Read this guide (you're doing it!)
- [ ] Choose deployment option
- [ ] Have required accounts/access ready

After setup:
- [ ] Calendar is accessible at your URL
- [ ] First update ran successfully  
- [ ] You can see all 63 events
- [ ] "Last Updated" timestamp shows
- [ ] Bookmark your calendar URL

---

## 🎉 You're Done!

Your calendar will now:
- ✅ Update every day at 3 AM UTC
- ✅ Add new events as announced
- ✅ Keep your verified events safe
- ✅ Calculate strategic scores
- ✅ Track competitors
- ✅ Require zero maintenance

**Next Steps:**
1. Share calendar URL with team
2. Add to browser bookmarks
3. Check Actions tab tomorrow to see first auto-update

---

**Need help?** All documentation is included in this package.

**Ready to start?** Pick an option above and follow the steps!

**Questions about specific events?** Edit `core_events.json` anytime.
