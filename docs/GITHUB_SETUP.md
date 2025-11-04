# GitHub Setup Guide for EduTrackX

## Method 1: Using Replit's GitHub Integration (Recommended)

You should see a GitHub connection button in your Replit interface. Here's how to use it:

### Step 1: Connect GitHub
1. Look for the GitHub connection button that appeared when I set up the integration
2. Click on it to authorize Replit to access your GitHub account
3. Grant the necessary permissions

### Step 2: Create or Connect Repository
Once connected, you can:
- **Create a new repository**: Let Replit create a new repo for you
- **Connect to existing repo**: Link to an existing GitHub repository

### Step 3: Push Your Code
After connecting:
- Your code will be automatically synced to GitHub
- Future changes can be pushed with a single click
- You can also pull changes from GitHub

---

## Method 2: Manual Git Setup (Alternative)

If you prefer to use Git commands directly, follow these steps:

### Step 1: Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: EduTrackX - Full-stack AI academic dashboard"
```

### Step 2: Create a GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the '+' icon → "New repository"
3. Name: `edutrackx` (or your preferred name)
4. Description: "AI-Powered Student Academic Dashboard"
5. Choose Public or Private
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

### Step 3: Connect Your Local Repository to GitHub

GitHub will show you commands. Use these:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/edutrackx.git

# Verify the remote was added
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 4: Verify

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed on the repo homepage

---

## What Gets Pushed to GitHub

Your .gitignore is configured to exclude:

**Excluded** (NOT pushed):
- `node_modules/` - Frontend dependencies
- `__pycache__/`, `*.pyc` - Python cache
- `.env` - Environment secrets
- `database.json` - User data
- `uploads/`, `reports/` - Generated files
- `*.pkl` - Trained ML models (large files)

**Included** (pushed):
- All source code (frontend & backend)
- Configuration files
- Documentation
- Training scripts (but not trained models)
- .gitignore, README.md
- Package files (package.json, requirements.txt)

---

## After Pushing to GitHub

### Step 1: Add Important Badges

Add these badges to your README.md for professionalism:

```markdown
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
```

### Step 2: Set Up GitHub Pages (Optional)

For project documentation:
1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, folder: /docs
4. Save

### Step 3: Add Topics/Tags

In your GitHub repo:
1. Click the gear icon next to "About"
2. Add topics: 
   - `student-dashboard`
   - `ai-powered`
   - `machine-learning`
   - `react`
   - `flask`
   - `education`
   - `academic-tracking`
   - `python`
   - `javascript`

### Step 4: Create Releases

Tag your first version:
```bash
git tag -a v1.0.0 -m "Initial release: EduTrackX MVP"
git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases → Draft a new release
2. Choose tag v1.0.0
3. Title: "EduTrackX v1.0.0 - Initial Release"
4. Description: List all features
5. Publish release

---

## Keeping GitHub Updated

### Regular Updates

Every time you make changes:

**Using Replit Integration:**
- Just click the sync button
- Your changes auto-push

**Using Git Commands:**
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### Creating Feature Branches

For new features:
```bash
git checkout -b feature/new-feature-name
# Make your changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature-name
```

Then create a Pull Request on GitHub.

---

## Collaboration on GitHub

### Allow Contributors

1. Go to Settings → Collaborators
2. Add team members by username/email
3. They can now clone and contribute

### Set Up Branch Protection

1. Settings → Branches
2. Add branch protection rule for `main`
3. Require pull request reviews
4. Require status checks to pass

---

## GitHub Actions (CI/CD) - Optional

Create `.github/workflows/test.yml`:

```yaml
name: Test EduTrackX

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          python -m pytest

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Build frontend
        run: |
          cd frontend
          npm run build
```

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/edutrackx.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --rebase
git push origin main
```

### Large files rejected
GitHub has a 100MB file limit. Our .gitignore should prevent this, but if it happens:
```bash
# Remove large file from Git
git rm --cached path/to/large/file
git commit -m "Remove large file"
git push origin main
```

### Authentication Issues

GitHub requires Personal Access Tokens (not passwords):
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: repo, workflow
4. Use token as password when pushing

Or use SSH:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Add public key to GitHub → Settings → SSH and GPG keys
git remote set-url origin git@github.com:YOUR_USERNAME/edutrackx.git
```

---

## Next Steps After GitHub Setup

1. **Share your repository**: Send the GitHub link to collaborators
2. **Star your own repo**: Shows activity
3. **Write a detailed README**: Already done! ✓
4. **Add screenshots**: Take screenshots of the app and add to README
5. **Create a demo video**: Record a 2-minute demo
6. **Set up project board**: GitHub Projects for task tracking
7. **Add a LICENSE file**: Choose MIT, Apache, GPL, etc.
8. **Create CONTRIBUTING.md**: Guidelines for contributors

---

## Quick Reference

**Clone your repo on another machine:**
```bash
git clone https://github.com/YOUR_USERNAME/edutrackx.git
cd edutrackx
```

**Setup on new machine:**
```bash
# Backend
cd backend
pip install -r requirements.txt
python ml/train_model.py
python run.py

# Frontend
cd frontend
npm install
npm run dev
```

---

Your code is now safely backed up on GitHub and ready to share with the world! 🚀
