# Deploy 9Hits Docker on Sealos Cloud

## Overview
Sealos Cloud is a free Kubernetes-based platform that allows deploying any Docker image. You can deploy the 9Hits viewer without a credit card.

## Step 1: Create a Sealos Account

1. Go to [https://sealos.io](https://sealos.io)
2. Click **"Get Started"** or **"Start Free"**
3. Sign up with your email (no credit card required)
4. Verify your email and login

## Step 2: Open App Launchpad

1. After logging in, you'll see the Sealos Dashboard
2. Click on **"App Launchpad"** from the main menu
3. Click **"Create App"** or **"Deploy New App"**

## Step 3: Configure the 9Hits Container

### Basic Settings

1. **App Name**: `9hits-viewer`
2. **Image**: `9hitste/app:latest`

### Environment Variables

Click **"Environment Variables"** and add:

| Name | Value |
|------|-------|
| `ACCESS_KEY` | `42948cff9e97420a74d54801a3c73077` |
| `SYSTEM_SESSION` | `true` |
| `ALLOW_CRYPTO` | `no` |
| `ALLOW_ADULT` | `no` |
| `ALLOW_POPUPS` | `yes` |

### Resource Configuration

- **CPU**: 1 Core (minimum)
- **Memory**: 1 GB (minimum)
- **Replicas**: 1

### Network Settings

- **Port**: Not needed (9Hits viewer doesn't expose a web server)
- **Network Mode**: Default

## Step 4: Deploy

1. Review your configuration
2. Click **"Deploy"** or **"Create"**
3. Wait for the deployment to complete (1-2 minutes)

## Step 5: Verify Deployment

1. Go to **"App Management"** in Sealos Dashboard
2. Find `9hits-viewer` in the list
3. Check that the status shows **"Running"**
4. Click on the app to view logs

## Step 6: Check 9Hits Dashboard

1. Go to [https://panel.9hits.com](https://panel.9hits.com)
2. Login with your account
3. Go to **"Sessions"** or **"Viewer"**
4. You should see a new session running from Sealos

## Troubleshooting

### If the container fails to start:

1. Check the logs in Sealos App Management
2. Verify the ACCESS_KEY is correct
3. Make sure the image `9hitste/app:latest` is accessible

### If no sessions appear:

1. Wait 5-10 minutes for the viewer to connect
2. Check your 9Hits account for any errors
3. Verify the SYSTEM_SESSION is set to `true`

### To restart the container:

1. Go to App Management
2. Find `9hits-viewer`
3. Click **"Restart"**

## Notes

- Sealos Cloud free tier includes:
  - 1 vCPU
  - 1 GB RAM
  - 1 GB storage
  - Sufficient for 1 9Hits session

- The 9Hits viewer runs 24/7 as long as the container is running

- You can add more sessions by increasing replicas or creating multiple deployments

## Alternative: Using Sealos CLI (Advanced)

If you prefer using the command line:

```bash
# Install Sealos CLI
curl -fsSL https://raw.githubusercontent.com/labring/sealos/main/scripts/install.sh | sh

# Login to Sealos
sealos login

# Deploy 9Hits viewer
sealos run docker.io/9hitste/app:latest \
  --name=9hits-viewer \
  --env=ACCESS_KEY=42948cff9e97420a74d54801a3c73077 \
  --env=SYSTEM_SESSION=true \
  --env=ALLOW_CRYPTO=no
```

## Cost

**$0** — Sealos Cloud free tier is sufficient for 1 9Hits session.

## Links

- Sealos Cloud: https://sealos.io
- 9Hits Panel: https://panel.9hits.com
- 9Hits Docker Hub: https://hub.docker.com/r/9hitste/app
