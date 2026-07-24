# Deploy 9Hits Viewer on Sealos

## Overview

Deploy 9Hits autosurf viewer on Sealos Cloud with 3 tasks.

| Resource | Value |
|----------|-------|
| **Platform** | Sealos Cloud |
| **Cost** | $5 free credit (7-day trial) |
| **Task 1** | 9Hits Viewer (bighit4u.com) |
| **Task 2** | 9Hits Viewer (aliexhelper.store) |
| **Task 3** | 9Hits Viewer (backup) |

---

## Step 1: Login to Sealos

1. Go to **https://cloud.sealos.run**
2. Login with your account

---

## Step 2: Go to Containers

1. Click **"Containers"** in sidebar
2. Or click **"Deploy"** → **"Container"**

---

## Step 3: Deploy Task 1 (bighit4u.com)

### 3.1 Click "Create Container"

### 3.2 Configure Container

| Setting | Value |
|---------|-------|
| **Name** | `9hits-bighit` |
| **Image** | `9hitste/app:latest` |
| **CPU** | `0.5` |
| **Memory** | `512` |

### 3.3 Add Environment Variables

Click **"Environment Variables"** and add:

| Key | Value |
|-----|-------|
| `ACCESS_KEY` | `42948cff9e97420a74d54801a3c73077` |

### 3.4 Click "Deploy"

---

## Step 4: Deploy Task 2 (aliexhelper.store)

### 4.1 Click "Create Container" again

### 4.2 Configure Container

| Setting | Value |
|---------|-------|
| **Name** | `9hits-aliex` |
| **Image** | `9hitste/app:latest` |
| **CPU** | `0.5` |
| **Memory** | `512` |

### 4.3 Add Environment Variables

| Key | Value |
|-----|-------|
| `ACCESS_KEY` | `42948cff9e97420a74d54801a3c73077` |

### 4.4 Click "Deploy"

---

## Step 5: Deploy Task 3 (Backup)

### 5.1 Click "Create Container" again

### 5.2 Configure Container

| Setting | Value |
|---------|-------|
| **Name** | `9hits-backup` |
| **Image** | `9hitste/app:latest` |
| **CPU** | `0.5` |
| **Memory** | `512` |

### 5.3 Add Environment Variables

| Key | Value |
|-----|-------|
| `ACCESS_KEY` | `42948cff9e97420a74d54801a3c73077` |

### 5.4 Click "Deploy"

---

## Step 6: Verify All Tasks

### 6.1 Check Container Status

You should see 3 containers:

| Name | Status | Image |
|------|--------|-------|
| 9hits-bighit | Running | 9hitste/app:latest |
| 9hits-aliex | Running | 9hitste/app:latest |
| 9hits-backup | Running | 9hitste/app:latest |

### 6.2 Check Logs for Each Container

Click on each container → "Logs"

Expected output:
```
[INFO] Starting 9Hits viewer...
[INFO] Access key: 42948cff9e97420a74d54801a3c73077
[INFO] Opening browser...
```

---

## Step 7: Configure 9Hits Dashboard

### 7.1 Login to 9Hits
```
https://9hits.net
```

### 7.2 Add Your Sites
1. Go to "My Sites"
2. Click "Add Site"
3. Add:
   - `https://bighit4u.com`
   - `https://aliexhelper.store`
4. Wait for approval (24-48 hours)

---

## Step 8: Monitor Traffic

### 8.1 Check 9Hits Stats
1. Login to https://9hits.net
2. Go to "Statistics"
3. Check traffic from Sealos IPs

### 8.2 Check Sealos Resources
1. Go to Sealos dashboard
2. Check CPU/Memory usage
3. Check $5 credit usage

---

## Management Commands

### Restart Container
1. Go to Containers
2. Click on container name
3. Click "Restart"

### Stop Container
1. Go to Containers
2. Click on container name
3. Click "Stop"

### Delete Container
1. Go to Containers
2. Click on container name
3. Click "Delete"

---

## Cost Estimation

| Resource | Cost |
|----------|------|
| **3 Containers** | ~$0.50/day |
| **7-Day Trial** | $5 free |
| **Total Runtime** | ~10 days |

---

## Troubleshooting

### Problem: Container Not Starting

**Check logs:**
1. Click on container name
2. Click "Logs"
3. Look for errors

**Solution:**
1. Delete container
2. Re-deploy with correct settings

---

### Problem: Out of Memory

**Check resource usage:**
1. Click on container name
2. Check CPU/Memory graphs

**Solution: Reduce CPU/Memory**
1. Delete container
2. Re-deploy with lower settings:
   - CPU: 0.25 vCPU
   - Memory: 256MB

---

### Problem: Container Keeps Restarting

**Check logs:**
1. Click on container name
2. Click "Logs"
3. Look for crash reasons

**Solution:**
1. Delete container
2. Pull latest image: `9hitste/app:latest`
3. Re-deploy

---

## Expected Results

| Metric | Value |
|--------|-------|
| **Traffic** | 100-500 visits/day |
| **Cost** | ~$0.50/day |
| **Earnings** | $0.02-0.20/day |
| **AdMaven Revenue** | $0.01-0.10/day |

---

## Important Notes

| Note | Details |
|------|---------|
| **Sealos is 7-day trial** | Then paid (~$7/mo) |
| **Traffic quality varies** | Some sites may block autosurf |
| **Monitor credit usage** | Check Sealos dashboard |
| **Keep containers running** | 24/7 for best results |
| **Check 9Hits approval** | Sites need approval before traffic |

---

## Need Help?

- Sealos Support: support@sealos.io
- 9Hits Support: support@9hits.net
