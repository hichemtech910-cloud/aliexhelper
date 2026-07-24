# Full Deployment: OtoHits Viewer on Sealos (Multiple Tasks)

## Overview

Deploy OtoHits autosurf viewer on Sealos Cloud with multiple tasks (containers) to generate traffic for your sites.

| Resource | Value |
|----------|-------|
| **Platform** | Sealos Cloud |
| **Cost** | $5 free credit (7-day trial) |
| **Task 1** | OtoHits Viewer (bighit4u.com) |
| **Task 2** | OtoHits Viewer (aliexhelper.store) |
| **Task 3** | OtoHits Viewer (backup) |

---

## Step 1: Create Sealos Account

### 1.1 Go to Sealos
```
https://cloud.sealos.run
```

### 1.2 Click "Sign Up"
- Enter email address
- Create password
- Click "Register"

### 1.3 Verify Email
- Check your email inbox
- Click verification link
- Login to Sealos dashboard

---

## Step 2: Access Container Management

### 2.1 Click "Containers" or "App Management"
- Look for "Containers" in the sidebar
- Or click "Deploy" → "Container"

### 2.2 You'll see the Container Management page

---

## Step 3: Deploy Task 1 (bighit4u.com)

### 3.1 Click "Create Container"

### 3.2 Configure Container

| Setting | Value |
|---------|-------|
| **Name** | otohits-bighit |
| **Image** | otohits/app:latest |
| **CPU** | 0.5 vCPU |
| **Memory** | 512MB |
| **Replicas** | 1 |

### 3.3 Add Environment Variables

Click "Environment Variables" and add:

| Key | Value |
|-----|-------|
| `APPLICATION_KEY` | `7ec3e126-c3af-46b5-a020-e9725f46214a` |

### 3.4 Click "Deploy" or "Create"

### 3.5 Wait for Deployment
- Takes 1-2 minutes
- Status should show "Running"

---

## Step 4: Deploy Task 2 (aliexhelper.store)

### 4.1 Click "Create Container" again

### 4.2 Configure Container

| Setting | Value |
|---------|-------|
| **Name** | otohits-aliex |
| **Image** | otohits/app:latest |
| **CPU** | 0.5 vCPU |
| **Memory** | 512MB |
| **Replicas** | 1 |

### 4.3 Add Environment Variables

| Key | Value |
|-----|-------|
| `APPLICATION_KEY` | `7ec3e126-c3af-46b5-a020-e9725f46214a` |

### 4.4 Click "Deploy"

---

## Step 5: Deploy Task 3 (Backup)

### 5.1 Click "Create Container" again

### 5.2 Configure Container

| Setting | Value |
|---------|-------|
| **Name** | otohits-backup |
| **Image** | otohits/app:latest |
| **CPU** | 0.5 vCPU |
| **Memory** | 512MB |
| **Replicas** | 1 |

### 5.3 Add Environment Variables

| Key | Value |
|-----|-------|
| `APPLICATION_KEY` | `7ec3e126-c3af-46b5-a020-e9725f46214a` |

### 5.4 Click "Deploy"

---

## Step 6: Verify All Tasks

### 6.1 Check Container Status
You should see 3 containers:

| Name | Status | Image |
|------|--------|-------|
| otohits-bighit | Running | otohits/app:latest |
| otohits-aliex | Running | otohits/app:latest |
| otohits-backup | Running | otohits/app:latest |

### 6.2 Check Logs for Each Container

Click on each container → "Logs"

Expected output:
```
[INFO] Starting OtoHits viewer...
[INFO] Application key: 7ec3e126-c3af-46b5-a020-e9725f46214a
[INFO] Opening browser...
```

---

## Step 7: Configure OtoHits Dashboard

### 7.1 Login to OtoHits
```
https://otohits.net
```

### 7.2 Add Your Sites
1. Go to "My Sites"
2. Click "Add Site"
3. Add:
   - `https://bighit4u.com`
   - `https://aliexhelper.store`
4. Wait for approval (24-48 hours)

### 7.3 Set Default Site
1. Go to "My Sites"
2. Click on `bighit4u.com`
3. Set as "Default Site"
4. Save

---

## Step 8: Monitor Traffic

### 8.1 Check OtoHits Stats
1. Login to https://otohits.net
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
2. Pull latest image: `otohits/app:latest`
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
| **Check OtoHits approval** | Sites need approval before traffic |

---

## Next Steps

1. **Deploy 3 tasks on Sealos** (Steps 3-5)
2. **Wait for site approval** (24-48 hours)
3. **Monitor traffic** in OtoHits dashboard
4. **Check AdMaven revenue** in bighit4u.com
5. **Optimize settings** if needed

---

## Need Help?

- Sealos Support: support@sealos.io
- OtoHits Support: support@otohits.net
- GitHub Issues: https://github.com/otohits/app/issues
