# How to Push to GitHub

## Step 1: Create a Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: "Project Store Push"
4. Select the **`repo`** checkbox (this gives full repository access)
5. Click **"Generate token"** at the bottom
6. **COPY THE TOKEN** (you won't see it again!)

## Step 2: Push Your Code

### Method 1: Interactive Push (Recommended)
Run this command:
```bash
git push -u origin main
```

When prompted:
- **Username:** `Prashantti-sudo`
- **Password:** Paste your token (not your GitHub password!)

### Method 2: Use Token in URL
If you have your token ready, run:
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/Prashantti-sudo/Project_store.git
git push -u origin main
```
(Replace `YOUR_TOKEN` with your actual token)

## Step 3: Verify
After pushing, check: https://github.com/Prashantti-sudo/Project_store

---

**Note:** Your code is already committed locally and ready to push!

