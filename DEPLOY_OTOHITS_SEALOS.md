# Deploy OtoHits Docker on Sealos Cloud

## Overview
Sealos Cloud is a free Kubernetes-based platform that allows deploying any Docker image. You can deploy the OtoHits viewer without a credit card.

## Step 1: Create a Sealos Account

1. Go to [https://sealos.io](https://sealos.io)
2. Click **"Get Started"** or **"Start Free"**
3. Sign up with your email (no credit card required)
4. Verify your email and login

## Step 2: Open App Launchpad

1. After logging in, you'll see the Sealos Dashboard
2. Click on **"App Launchpad"** from the main menu
3. Click **"Create App"** or **"Deploy New App"**

## Step 3: Configure the OtoHits Container

### Basic Settings

1. **App Name**: `otohits-viewer`
2. **Image**: `otohits/app:latest`

### Environment Variables

Click **"Environment Variables"** and add:

| Name | Value |
|------|-------|
| `APPLICATION_KEY` | `7ec3e126-c3af-46b5-a020-e9725f46214a` |
| `SITES` | `aliexhelper.store,bighit4u.com` |
| `MAX_TABS` | `3` |

### Resource Configuration

- **CPU**: 1 Core (minimum)
- **Memory**: 1 GB (minimum)
- **Replicas**: 1

### Network Settings

- **Port**: Not needed (OtoHits viewer doesn't expose a web server)
- **Network Mode**: Default

## Step 4: Deploy

1. Review your configuration
2. Click **"Deploy"** or **"Create"**
3. Wait for the deployment to complete (1-2 minutes)

## Step 5: Verify Deployment

1. Go to **"App Management"** in Sealos Dashboard
2. Find `otohits-viewer` in the list
3. Check that the status shows **"Running"**
4. Click on the app to view logs

## Step 6: Check OtoHits Dashboard

1. Go to [https://otohits.com](https://otohits.com)
2. Login with your account
3. Go to **"My Sites"**
4. You should see visits appearing for `aliexhelper.store` and `bighit4u.com`

## Troubleshooting

### If the container fails to start:

1. Check the logs in Sealos App Management
2. Verify the APPLICATION_KEY is correct
3. Make sure the image `otohits/app:latest` is accessible

### If no visits appear:

1. Wait 5-10 minutes for the viewer to connect
2. Check your OtoHits account for any errors
3. Verify your sites are approved in OtoHits

### To restart the container:

1. Go to App Management
2. Find `otohits-viewer`
3. Click **"Restart"**

## Notes

- Sealos Cloud free tier includes:
  - 1 vCPU
  - 1 GB RAM
  - 1 GB storage
  - Sufficient for OtoHits viewer

- The OtoHits viewer runs 24/7 as long as the container is running

- You can add more sites by updating the SITES environment variable

## Alternative: Using Sealos CLI (Advanced)

If you prefer using the command line:

```bash
# Install Sealos CLI
curl -fsSL https://raw.githubusercontent.com/labring/sealos/main/scripts/install.sh | sh

# Login to Sealos
sealos login

# Deploy OtoHits viewer
sealos run docker.io/otohits/app:latest \
  --name=otohits-viewer \
  --env=APPLICATION_KEY=7ec3e126-c3af-46b5-a020-e9725f46214a \
  --env=SITES=aliexhelper.store,bighit4u.com \
  --env=MAX_TABS=3
```

## Cost

**$0** — Sealos Cloud free tier is sufficient for OtoHits viewer.

## Links

- Sealos Cloud: https://sealos.io
- OtoHits Dashboard: https://otohits.com
- OtoHits Docker Hub: https://hub.docker.com/r/otohits/app
