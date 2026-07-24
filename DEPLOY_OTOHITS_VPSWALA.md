# Deploy OtoHits Viewer on VPSWala (Free Forever)

## VPSWala Overview

| Feature | Details |
|---------|---------|
| **Price** | Free forever |
| **CPU** | 1 vCPU |
| **RAM** | 1 GB |
| **Storage** | 10 GB SSD |
| **Bandwidth** | 1 TB/month |
| **OS** | Ubuntu 22.04/24.04 |
| **Root Access** | Yes |

---

## Step 1: Sign Up for VPSWala

1. Go to https://vpswala.org
2. Click "Sign Up"
3. Enter email and password
4. Verify email
5. Login to dashboard

---

## Step 2: Create a VPS

1. Click "Create VPS" or "Deploy"
2. Select location: **Singapore** or **Netherlands**
3. Select OS: **Ubuntu 22.04**
4. Select plan: **Free Tier**
5. Click "Deploy"

---

## Step 3: Get VPS Details

After deployment, you'll receive:

| Detail | Value |
|--------|-------|
| **IP Address** | xxx.xxx.xxx.xxx |
| **Root Password** | xxxxxxxxxx |
| **SSH Port** | 22 |

---

## Step 4: Connect to VPS

### Using PowerShell (Windows)
```powershell
ssh root@YOUR_VPS_IP
```

### Using PuTTY
1. Download PuTTY from https://putty.org
2. Host Name: YOUR_VPS_IP
3. Port: 22
4. Click "Open"
5. Login as: root
6. Enter password

---

## Step 5: Install Docker

```bash
apt update && apt upgrade -y
apt install docker.io -y
systemctl start docker
systemctl enable docker
docker --version
```

---

## Step 6: Run OtoHits Viewer

### Basic Setup (1 tab)
```bash
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  otohits/app:latest
```

### 3 Tabs Setup
```bash
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  -e MAX_TABS=3 \
  otohits/app:latest
```

---

## Step 7: Verify Deployment

```bash
docker ps
docker logs otohits-viewer
```

---

## Step 8: Add Your Sites to OtoHits

1. Login to https://otohits.net
2. Go to "My Sites"
3. Add:
   - `aliexhelper.store`
   - `bighit4u.com`
4. Wait for approval (24-48 hours)

---

## Step 9: Configure Traffic

In OtoHits dashboard:
1. Go to "My Sites"
2. Select `bighit4u.com`
3. Set as default site
4. The viewer will now send traffic to bighit4u.com

---

## Step 10: Monitor Traffic

### Check OtoHits Stats
1. Login to https://otohits.net
2. Go to "Statistics"
3. Check traffic from your VPS IP

### Check VPS Resources
```bash
docker stats otohits-viewer
```

---

## Troubleshooting

### Viewer Not Starting
```bash
docker logs otohits-viewer
```

### Viewer Crashing
```bash
docker restart otohits-viewer
```

### Out of Memory
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

## Expected Results

| Metric | Value |
|--------|-------|
| **Traffic** | 50-200 visits/day |
| **Cost** | Free |
| **Earnings** | $0.01-0.10/day |
| **AdMaven Revenue** | $0.005-0.05/day |

---

## Notes

- VPSWala is free forever
- Traffic quality varies
- Monitor resource usage
- Keep viewer running 24/7

---

## Need Help?

- VPSWala Support: support@vpswala.org
- OtoHits Support: support@otohits.net
