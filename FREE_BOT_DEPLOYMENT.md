# Free Ways to Deploy OtoHits Bot

## Best Free Options (No Credit Card)

| Platform | Free Forever? | Credit Card? | Docker? | Works? |
|----------|---------------|--------------|---------|--------|
| **VPSWala** | Yes | No | Yes | Maybe |
| **GratisVPS** | Yes | No | Yes | Maybe |
| **Koyeb** | Yes | No | Yes | Maybe |
| **Back4app** | Yes | No | Yes | Maybe |

---

## Option 1: VPSWala (Recommended)

### Steps
1. Go to https://vpswala.org
2. Sign up (email only)
3. Deploy Ubuntu 22.04 VPS
4. Install Docker:
```bash
apt update && apt upgrade -y
apt install docker.io -y
systemctl start docker
systemctl enable docker
```
5. Run OtoHits viewer:
```bash
docker run -d \
  --name otohits-viewer \
  --restart unless-stopped \
  -e APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  otohits/app:latest
```

---

## Option 2: GratisVPS

### Steps
1. Go to https://gratisvps.net
2. Sign up (email only)
3. Deploy Docker container
4. Run OtoHits viewer

---

## Option 3: Koyeb

### Steps
1. Go to https://www.koyeb.com
2. Sign up (email only)
3. Deploy Docker image: `otohits/app:latest`
4. Add environment variable:
   - Key: `APPLICATION_KEY`
   - Value: `7ec3e126-c3af-46b5-a020-e9725f46214a`

---

## Option 4: Back4app

### Steps
1. Go to https://www.back4app.com
2. Sign up (email only)
3. Deploy Docker image: `otohits/app:latest`
4. Add environment variable

---

## Important Warning

| Issue | Details |
|-------|---------|
| **Anti-cheat** | OtoHits may block cloud IPs |
| **Headless browser** | Detected in containers |
| **Datacenter IP** | Not residential |

---

## Best Solution

Run OtoHits on your **home PC**:
1. Download OtoHits viewer
2. Install on Windows
3. Keep running 24/7
4. Residential IP = no anti-cheat issues

---

## Recommendation

1. **Try VPSWala first** - Free forever
2. **If blocked, use your PC** - Most reliable
3. **Try 9Hits instead** - Different anti-cheat

---

Which option do you want to try?
