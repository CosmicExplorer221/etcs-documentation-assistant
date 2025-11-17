# Qdrant Cloud Setup (No Docker Required!)

## Step 1: Create FREE Qdrant Cloud Account

1. Go to: https://cloud.qdrant.io/
2. Click "Sign Up" (use Google/GitHub for quick signup)
3. Create a new cluster:
   - Click "Create Cluster"
   - Region: Choose closest to you (Europe recommended)
   - Plan: **FREE** (1GB storage)
   - Click "Create"
4. Wait ~1 minute for cluster to start

## Step 2: Get Your Cluster URL and API Key

1. Click on your cluster name
2. Copy **Cluster URL** (looks like: `https://xxxxx.aws.cloud.qdrant.io:6333`)
3. Click "API Keys" tab
4. Click "Create API Key"
5. Copy the API key (save it somewhere safe!)

## Step 3: Update Your .env File

Open `backend/.env` and add:

```bash
# Qdrant Cloud Configuration
QDRANT_URL=https://your-cluster-url.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION_NAME=etcs_documents

# Your existing Gemini key
GEMINI_API_KEY=your-gemini-api-key-here
```

Replace with your actual cluster URL and API key!

## Step 4: Initialize Documents

```bash
cd backend
python scripts/init_documents.py
```

This will upload all PDFs to Qdrant Cloud (takes 5-30 min, ONE-TIME only).

## Step 5: Start the App

```bash
start-app.bat
```

Done! No Docker needed. Your vector database is in the cloud.

## Benefits

✅ No Docker installation
✅ Works from anywhere (internet connection needed)
✅ Perfect for demos
✅ Easy to share with team
✅ FREE tier (1GB storage)

## Troubleshooting

**"Connection refused"**
→ Check QDRANT_URL and QDRANT_API_KEY in .env

**"Collection not found"**
→ Run `python scripts/init_documents.py` first

**"Rate limit exceeded"**
→ Wait a minute, free tier has rate limits
