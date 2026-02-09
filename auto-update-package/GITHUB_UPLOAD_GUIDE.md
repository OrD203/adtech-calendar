# GitHub File Upload - Step-by-Step Guide

## Method 1: Direct Upload in Browser (EASIEST)

### Step 1: You Just Created Your Repo
After clicking "Create repository", you'll see a page that says:
```
"Quick setup — if you've done this kind of thing before"
```

### Step 2: Look for This Link
On that same page, scroll down a bit and you'll see:

```
"...or create a new file on the command line"
```

Right above that, there's a link that says:
**"uploading an existing file"** ← Click this!

### Step 3: Upload Files
You'll now see a page titled: **"Add files to [your-repo-name]"**

**Two options here:**

#### Option A: Drag and Drop
1. Open your file explorer/finder
2. Navigate to: `/mnt/user-data/outputs/auto-update-package/`
3. Select ALL these files:
   - index.html
   - event_updater.py
   - core_events.json
   - requirements.txt
   - README.md
   - DEPLOYMENT_GUIDE.md
   - EXECUTIVE_SUMMARY.md
   - QUICK_START.md
   - setup.sh
4. Drag them into the GitHub page (there's a dotted box)
5. Drop them

#### Option B: Click to Choose
1. Click "choose your files" link
2. Navigate to `/mnt/user-data/outputs/auto-update-package/`
3. Select all files (Ctrl+A or Cmd+A)
4. Click "Open"

### Step 4: Upload the Workflow File
**IMPORTANT:** GitHub won't let you create folders via drag-and-drop in the initial upload.

After uploading the main files:
1. Click "Add file" dropdown (top right)
2. Click "Create new file"
3. In the filename box, type: `.github/workflows/update-calendar.yml`
   - GitHub will automatically create the folders when you type the `/`
4. Copy-paste the contents from `update-calendar.yml` into the editor
5. Scroll down and click "Commit new file"

### Step 5: Commit Changes
At the bottom of the upload page:
1. You'll see "Commit changes"
2. Leave the default message ("Add files via upload")
3. Click the green **"Commit changes"** button

**Done!** Your files are now in GitHub.

---

## Method 2: GitHub Desktop App (IF YOU PREFER DESKTOP APP)

### Step 1: Download GitHub Desktop
- Go to: https://desktop.github.com/
- Download and install

### Step 2: Clone Your Repository
1. Open GitHub Desktop
2. File > Clone Repository
3. Find your `adtech-calendar` repo
4. Choose where to save it on your computer
5. Click "Clone"

### Step 3: Copy Files
1. Open the folder where you cloned the repo
2. Copy ALL files from `/mnt/user-data/outputs/auto-update-package/`
3. Paste them into your cloned repo folder
4. Make sure to include the `.github` folder with the `workflows` subfolder

### Step 4: Commit and Push
1. GitHub Desktop will show all the new files
2. Add a commit message: "Initial calendar setup"
3. Click "Commit to main"
4. Click "Push origin" (top right)

**Done!** Files are uploaded.

---

## Method 3: Command Line (IF YOU'RE COMFORTABLE WITH TERMINAL)

### Step 1: Navigate to Package Directory
```bash
cd /mnt/user-data/outputs/auto-update-package/
```

### Step 2: Initialize Git
```bash
git init
git add .
git commit -m "Initial calendar setup"
```

### Step 3: Connect to GitHub
```bash
# Replace YOUR_USERNAME and YOUR_REPO with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 4: Enter Credentials
- Username: Your GitHub username
- Password: Use a Personal Access Token (not your GitHub password)
  - Create token at: https://github.com/settings/tokens

**Done!** Files are uploaded.

---

## 🎯 Quick Visual Guide - Browser Upload

```
1. Create Repository
   ↓
2. You see: "Quick setup" page
   ↓
3. Look for: "uploading an existing file" link
   ↓
4. Click it
   ↓
5. Drag and drop files OR click "choose your files"
   ↓
6. Select all 9 files from auto-update-package folder
   ↓
7. Click "Commit changes" (green button at bottom)
   ↓
8. Separately add .github/workflows/update-calendar.yml
   (Use "Create new file" button, type the path with /)
   ↓
9. Done! ✅
```

---

## 📂 Files You're Uploading (Checklist)

Main files (upload first):
- [ ] index.html
- [ ] event_updater.py  
- [ ] core_events.json
- [ ] requirements.txt
- [ ] README.md
- [ ] DEPLOYMENT_GUIDE.md
- [ ] EXECUTIVE_SUMMARY.md
- [ ] QUICK_START.md
- [ ] setup.sh

Workflow file (create separately):
- [ ] .github/workflows/update-calendar.yml

**Total: 10 files**

---

## ❓ Troubleshooting

### "I don't see 'uploading an existing file'"
**Solution:** 
1. Go to your repo homepage (github.com/USERNAME/REPO)
2. Click "Add file" dropdown (near the green "Code" button)
3. Click "Upload files"

### "It won't let me create .github folder"
**Solution:**
1. First upload all the regular files
2. Then use "Add file" > "Create new file"
3. Type the FULL path: `.github/workflows/update-calendar.yml`
4. GitHub creates the folders automatically

### "I uploaded files but can't find them"
**Check:**
1. Go to your repo homepage
2. You should see the file list
3. If not, click the "Code" tab at the top

---

## 🎬 After Upload - Next Step

Once all files are uploaded:

1. Click **"Settings"** tab (top of your repo)
2. Scroll to **"Pages"** in left sidebar  
3. Under "Source": Select **"Deploy from a branch"**
4. Under "Branch": Select **"main"** and **"/ (root)"**
5. Click **"Save"**

Wait 1-2 minutes, then your calendar will be live at:
```
https://YOUR_USERNAME.github.io/adtech-calendar/
```

---

## 💡 Pro Tip

Can't find the auto-update-package folder on your computer?

The files are currently in Claude's environment. You need to:

**Option A: Download the package first**
1. I can create a ZIP file for you
2. You download it
3. Extract it
4. Then upload to GitHub

**Option B: Copy-paste each file**
1. I'll show you the contents of each file
2. You create the files manually in GitHub
3. Copy-paste the contents

**Which would you prefer?** Let me know and I'll help!
