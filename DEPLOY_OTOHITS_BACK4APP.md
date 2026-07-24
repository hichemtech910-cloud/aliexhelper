# Deploy OtoHits Viewer on Back4app

## Overview

Back4app requires a GitHub repository with a Dockerfile. We'll create a simple repo that pulls and runs the OtoHits viewer.

---

## Step 1: Create GitHub Repository

### 1.1 Go to GitHub
```
https://github.com/new
```

### 1.2 Create Repository
- Name: `otohits-viewer`
- Public
- Click "Create repository"

---

## Step 2: Create Files

### 2.1 Create Dockerfile

Create a file named `Dockerfile` with this content:

```dockerfile
FROM otohits/app:latest

ENV APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a
```

### 2.2 Create .dockerignore

Create a file named `.dockerignore` with this content:

```
.git
.gitignore
README.md
```

### 2.3 Create README.md

Create a file named `README.md` with this content:

```markdown
# OtoHits Viewer

Auto-surf viewer for OtoHits.
```

---

## Step 3: Upload to GitHub

### 3.1 Upload Files
1. Go to your repository
2. Click "Add file" → "Upload files"
3. Drag and drop all 3 files
4. Click "Commit changes"

---

## Step 4: Deploy on Back4app

### 4.1 Go to Back4app
```
https://www.back4app.com
```

### 4.2 Sign Up
1. Click "Sign Up"
2. Enter email and password
3. Verify email
4. Login

### 4.3 Create App
1. Click "New App"
2. Select "Containers as a Service"
3. Click "Import from GitHub"

### 4.4 Connect GitHub
1. Click "Connect GitHub"
2. Authorize Back4app
3. Select `otohits-viewer` repository

### 4.5 Configure App
1. App Name: `otohits-viewer`
2. Branch: `main`
3. Port: `8080`
4. Click "Deploy"

### 4.6 Wait for Deployment
- Takes 2-5 minutes
- Status should show "Running"

---

## Step 5: Verify Deployment

### 5.1 Check Logs
1. Go to your app dashboard
2. Click "Logs"
3. Look for:
```
[INFO] Starting OtohitsApp...
[INFO] Login to Otohits...
[INFO] Connecting instance...
```

### 5.2 Check Status
1. Go to your app dashboard
2. Status should show "Running"

---

## Troubleshooting

### Problem: Build Failed

**Check logs for errors**

**Solution:**
1. Verify Dockerfile content
2. Push changes to GitHub
3. Redeploy

---

### Problem: Container Crashing

**Check logs for errors**

**Solution:**
1. Verify APPLICATION_KEY is correct
2. Check OtoHits dashboard for approval
3. Redeploy

---

### Problem: Anti-cheat Error

**This is expected on cloud platforms**

**Solution:**
1. Use your home PC instead
2. Or try 9Hits (different anti-cheat)

---

## Important Notes

| Note | Details |
|------|---------|
| **Back4app is free** | 1 container free |
| **Anti-cheat** | May block cloud IPs |
| **Sites need approval** | Wait 24-48 hours |
| **Monitor logs** | Check for errors |

---

## Need Help?

- Back4app Support: support@back4app.com
- OtoHits Support: support@otohits.net
