# How to Deploy on Sealos (Step-by-Step)

## Step 1: Create Account

1. Go to **https://cloud.sealos.run**
2. Click **"Sign Up"**
3. Enter email and password
4. Verify email
5. Login

---

## Step 2: Go to Containers

1. Click **"Containers"** in sidebar
2. Or click **"Deploy"** → **"Container"**

---

## Step 3: Create First Container

1. Click **"Create Container"**
2. Fill in:

| Field | Value |
|-------|-------|
| Name | `otohits-1` |
| Image | `otohits/app:latest` |
| CPU | `0.5` |
| Memory | `512` |

3. Click **"Environment Variables"**
4. Add:

| Key | Value |
|-----|-------|
| `APPLICATION_KEY` | `7ec3e126-c3af-46b5-a020-e9725f46214a` |

5. Click **"Deploy"**

---

## Step 4: Create Second Container

1. Click **"Create Container"** again
2. Fill in:

| Field | Value |
|-------|-------|
| Name | `otohits-2` |
| Image | `otohits/app:latest` |
| CPU | `0.5` |
| Memory | `512` |

3. Add same environment variable
4. Click **"Deploy"**

---

## Step 5: Create Third Container

1. Click **"Create Container"** again
2. Fill in:

| Field | Value |
|-------|-------|
| Name | `otohits-3` |
| Image | `otohits/app:latest` |
| CPU | `0.5` |
| Memory | `512` |

3. Add same environment variable
4. Click **"Deploy"**

---

## Step 6: Verify

You should see 3 containers:

| Name | Status |
|------|--------|
| otohits-1 | Running |
| otohits-2 | Running |
| otohits-3 | Running |

---

## Done!

Your 3 OtoHits viewers are now running on Sealos.
