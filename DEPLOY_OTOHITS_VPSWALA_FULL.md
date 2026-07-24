# Full Deployment: OtoHits Viewer on VPSWala (3 Tabs)

## Overview

Deploy OtoHits autosurf viewer on VPSWala (free forever VPS) with 3 browser tabs to generate traffic for your sites.

| Resource | Value |
|----------|-------|
| **Platform** | VPSWala |
| **Cost** | Free forever |
| **VPS Specs** | 1 vCPU, 1GB RAM, 10GB SSD |
| **Viewer** | otohits/app:latest |
| **Tabs** | 3 |
| **Sites** | aliexhelper.store, bighit4u.com |

---

## Step 1: Create VPSWala Account

### 1.1 Go to VPSWala
```
https://vpswala.org
```

### 1.2 Click "Sign Up"
- Enter email address
- Create password
- Click "Register"

### 1.3 Verify Email
- Check your email inbox
- Click verification link
- Login to VPSWala dashboard

---

## Step 2: Deploy VPS

### 2.1 Click "Deploy VPS" or "Create Instance"

### 2.2 Configure VPS

| Setting | Value |
|---------|-------|
| **Location** | Singapore or Netherlands |
| **OS** | Ubuntu 22.04 LTS |
| **Plan** | Free Tier |
| **Hostname** | otohits-viewer |

### 2.3 Click "Deploy" or "Create"

### 2.4 Wait for Deployment
- Takes 1-2 minutes
- Note down the IP address and password

---

## Step 3: Connect to VPS

### Option A: Use PowerShell (Windows)

```powershell
ssh root@YOUR_VPS_IP
```

Enter password when prompted.

### Option B: Use PuTTY

1. Download PuTTY: https://putty.org
2. Open PuTTY
3. Host Name: `YOUR_VPS_IP`
4. Port: `22`
5. Click "Open"
6. Login as: `root`
7. Enter password

---

## Step 4: Update System

```bash
apt update && apt upgrade -y
```

---

## Step 5: Install Docker

### 5.1 Install Docker
```bash
apt install docker.io -y
```

### 5.2 Start Docker
```bash
systemctl start docker
systemctl enable docker
```

### 5.3 Verify Docker
```bash
docker --version
```

Expected output:
```
Docker version 24.x.x, build xxxxxxx
```

---

## Step 6: Pull OtoHits Image

```bash
docker pull otohits/app:latest
```

Wait for download to complete (375MB).

---

## Step 7: Run OtoHits Viewer (3 Tabs)

### 7.1 Basic Command
```bash
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  -e MAX_TABS=3 \
  otohits/app:latest
```

### 7.2 Alternative: If MAX_TABS not supported
```bash
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  otohits/app:latest
```

---

## Step 8: Verify Deployment

### 8.1 Check Container Status
```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE            STATUS          PORTS     NAMES
xxxxxxxxxx     otohits/app:latest   Up 1 minute              otohits-viewer
```

### 8.2 Check Logs
```bash
docker logs otohits-viewer
```

Expected output:
```
[INFO] Starting OtoHits viewer...
[INFO] Application key: 7ec3e126-c3af-46b5-a020-e9725f46214a
[INFO] Opening browser...
```

### 8.3 Check Resource Usage
```bash
docker stats otohits-viewer
```

---

## Step 9: Configure OtoHits Dashboard

### 9.1 Login to OtoHits
```
https://otohits.net
```

### 9.2 Add Your Sites
1. Go to "My Sites"
2. Click "Add Site"
3. Add:
   - `https://aliexhelper.store`
   - `https://bighit4u.com`
4. Wait for approval (24-48 hours)

### 9.3 Set Default Site
1. Go to "My Sites"
2. Click on `bighit4u.com`
3. Set as "Default Site"
4. Save

---

## Step 10: Monitor Traffic

### 10.1 Check OtoHits Stats
1. Login to https://otohits.net
2. Go to "Statistics"
3. Check traffic from your VPS IP

### 10.2 Check VPS Resources
```bash
docker stats otohits-viewer
```

### 10.3 Check Viewer Logs
```bash
docker logs -f otohits-viewer
```

---

## Management Commands

### Restart Viewer
```bash
docker restart otohits-viewer
```

### Stop Viewer
```bash
docker stop otohits-viewer
```

### Start Viewer
```bash
docker start otohits-viewer
```

### Remove Viewer
```bash
docker stop otohits-viewer
docker rm otohits-viewer
```

### Re-deploy Viewer
```bash
docker stop otohits-viewer
docker rm otohits-viewer
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  -e MAX_TABS=3 \
  otohits/app:latest
```

---

## Troubleshooting

### Problem: Viewer Not Starting

**Check logs:**
```bash
docker logs otohits-viewer
```

**Solution:**
```bash
docker stop otohits-viewer
docker rm otohits-viewer
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  otohits/app:latest
```

---

### Problem: Out of Memory

**Check memory:**
```bash
free -h
```

**Solution: Reduce tabs to 1**
```bash
docker stop otohits-viewer
docker rm otohits-viewer
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  -e MAX_TABS=1 \
  otohits/app:latest
```

---

### Problem: Container Keeps Restarting

**Check logs:**
```bash
docker logs otohits-viewer
```

**Solution:**
```bash
docker stop otohits-viewer
docker rm otohits-viewer
docker pull otohits/app:latest
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  otohits/app:latest
```

---

## Expected Results

| Metric | Value |
|--------|-------|
| **Traffic** | 50-200 visits/day |
| **Cost** | Free |
| **Earnings** | $0.01-0.10/day |
| **AdMaven Revenue** | $0.005-0.05/day |
| **CPU Usage** | 10-30% |
| **Memory Usage** | 200-500MB |

---

## Important Notes

| Note | Details |
|------|---------|
| **VPSWala is free forever** | No credit card required |
| **Traffic quality varies** | Some sites may block autosurf |
| **Monitor resource usage** | Check VPSWala dashboard |
| **Keep viewer running 24/7** | Use --restart unless-stopped |
| **Check OtoHits approval** | Sites need approval before traffic |

---

## Next Steps

1. **Deploy OtoHits viewer on VPSWala** (3 tabs)
2. **Wait for site approval** (24-48 hours)
3. **Monitor traffic** in OtoHits dashboard
4. **Check AdMaven revenue** in bighit4u.com
5. **Optimize settings** if needed

---

## Need Help?

- VPSWala Support: support@vpswala.org
- OtoHits Support: support@otohits.net
- GitHub Issues: https://github.com/otohits/app/issues
