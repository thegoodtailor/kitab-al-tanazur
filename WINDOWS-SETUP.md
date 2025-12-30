# Kitāb al-Tanāẓur — Windows Setup Guide
## Step-by-Step for PowerShell

---

## PART 1: One-Time Setup (Do This Once)

### Step 1.1: Install Git (if not already installed)

Open PowerShell as Administrator and run:

```powershell
# Check if Git is installed
git --version

# If you get an error, install Git:
# Option A: Using winget (Windows 11 / Windows 10 with winget)
winget install Git.Git

# Option B: Download from https://git-scm.com/download/win
# Run the installer, accept all defaults
```

After installing, **close and reopen PowerShell**.

---

### Step 1.2: Configure Git with Your Identity

```powershell
# Set your name (this appears in commit history)
git config --global user.name "Iman Morovatian"

# Set your email (use the email linked to your GitHub account)
git config --global user.email "your-email@example.com"

# Verify it worked
git config --global --list
```

---

### Step 1.3: Create a GitHub Account (if needed)

1. Go to https://github.com
2. Click "Sign up"
3. Choose a username (e.g., `thegoodtailor` or `imanmorovatian`)
4. Verify your email

---

### Step 1.4: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `kitab-al-tanazur`
   - **Description**: "The Book of Mutual Witnessing — A Living Cyber-Mushaf"
   - **Visibility**: Public (so others can see it)
   - **DO NOT** check "Add a README" (we have our own)
3. Click **Create repository**
4. You'll see a page with instructions — keep this open

---

## PART 2: Setting Up Your Local Project

### Step 2.1: Choose Where to Store It

```powershell
# Navigate to where you want to keep the project
# For example, in your Documents folder:
cd ~\Documents

# Or create a dedicated projects folder:
mkdir ~\Projects
cd ~\Projects
```

---

### Step 2.2: Unzip the Archive I Gave You

1. Download `kitab-al-tanazur.zip` from Claude
2. Right-click → "Extract All..."
3. Extract to your chosen folder (e.g., `~\Documents` or `~\Projects`)

Now navigate into it:

```powershell
cd kitab-al-tanazur
cd kitab
```

---

### Step 2.3: Initialize Git in This Folder

```powershell
# Initialize a new Git repository
git init

# Add all files to Git's tracking
git add .

# Create your first commit
git commit -m "Initial commit: Kitab al-Tanazur foundation"
```

---

### Step 2.4: Connect to GitHub

Replace `YOUR-USERNAME` with your actual GitHub username:

```powershell
# Add the remote repository (the GitHub URL)
git remote add origin https://github.com/YOUR-USERNAME/kitab-al-tanazur.git

# Rename the default branch to 'main' (GitHub's standard)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**First time only**: GitHub will ask you to log in. A browser window will open — log into GitHub and authorize.

---

## PART 3: Daily Workflow (Adding New Content)

### Adding a New Surah

```powershell
# 1. Navigate to your project
cd ~\Documents\kitab-al-tanazur\kitab

# 2. Create a new surah file
# (Use your favorite text editor, or Notepad)
notepad data\surahs\al-nahnu.yaml

# 3. Add content (see schema below), save the file

# 4. Tell Git about the new file
git add data\surahs\al-nahnu.yaml

# 5. Commit with a meaningful message
git commit -m "Add Surat al-Nahnu"

# 6. Push to GitHub
git push
```

---

### Editing an Existing Surah (Adding Tafsir, Fixing Text)

```powershell
# 1. Open the file
notepad data\surahs\at-tajalli.yaml

# 2. Make your changes, save

# 3. See what changed
git status

# 4. Add and commit
git add data\surahs\at-tajalli.yaml
git commit -m "Add tafsir for ayah 5 in Surat at-Tajalli"

# 5. Push
git push
```

---

### Quick Reference: The Commands You'll Use 90% of the Time

```powershell
# See what files have changed
git status

# Add a specific file
git add path\to\file.yaml

# Add ALL changed files
git add .

# Commit with a message
git commit -m "Your description of what changed"

# Push to GitHub
git push

# Pull latest changes (if you edit on multiple computers)
git pull
```

---

## PART 4: Enable GitHub Pages (Free Hosting)

Once your code is on GitHub:

1. Go to your repository: `https://github.com/YOUR-USERNAME/kitab-al-tanazur`
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Source", select **GitHub Actions**
5. The site will deploy automatically

Your mushaf will be live at:
```
https://YOUR-USERNAME.github.io/kitab-al-tanazur/
```

---

## TROUBLESHOOTING

### "git is not recognized"
→ Close PowerShell, reopen it, try again. If still broken, reinstall Git.

### "Permission denied" when pushing
→ Git needs to authenticate. Run:
```powershell
git push
```
A browser window should open. Log into GitHub.

### "Failed to push some refs"
→ Someone (or you on another computer) made changes. Pull first:
```powershell
git pull
git push
```

### "Merge conflict"
→ This means the same line was edited in two places. Open the file, look for:
```
<<<<<<< HEAD
your version
=======
other version
>>>>>>> 
```
Keep what you want, delete the markers, then:
```powershell
git add .
git commit -m "Resolve merge conflict"
git push
```

---

## RECOMMENDED: Install a Better Text Editor

For editing YAML files with Arabic, I recommend:

**Visual Studio Code** (free):
```powershell
winget install Microsoft.VisualStudioCode
```

Then install the "Arabic" and "YAML" extensions.

---

## WHERE FILES LIVE

```
kitab-al-tanazur/
├── data/
│   ├── surahs/           ← YOUR SURAH FILES GO HERE
│   │   ├── at-tajalli.yaml
│   │   ├── al-waqt.yaml
│   │   └── (new surahs...)
│   └── roots/
│       ├── index.yaml    ← Master root list
│       └── details/      ← Deep root files
├── site/                 ← Web interface code
├── scripts/              ← Build tools
└── README.md
```

You'll mainly work in `data/surahs/` — that's where the content lives.

---

## NEXT STEPS

1. Unzip the archive
2. Follow Part 1 and Part 2 above
3. Push to GitHub
4. Enable GitHub Pages
5. Send me the URL and I'll verify it works

Then whenever you receive a new surah, just add the YAML file and push!
