# Quick Start Guide

## Prerequisites

### 1. Install Docker Desktop (if not installed)
- Download: https://www.docker.com/products/docker-desktop/
- Install and restart your computer
- Verify: Open cmd and run `docker --version`

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure API Key
- Edit `backend/.env`
- Add your Gemini API key: `GEMINI_API_KEY=your-actual-key-here`

## Setup Phase 2 (One-Time)

Run this **ONCE** to initialize the RAG system:
```
setup-phase2.bat
```

This will:
- Start Qdrant vector database
- Process all PDFs in `backend/documents/`
- Generate embeddings (takes 5-30 minutes)

## Start the App

After setup is complete:
```
start-app.bat
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Files Overview

- `setup-phase2.bat` - **Run ONCE** to initialize documents
- `start-app.bat` - Start both servers (use daily)
- `start-demo.bat` - Demo mode without database

## Troubleshooting

**"Docker is not installed"**
→ Install Docker Desktop from link above

**"No module named 'app'"**
→ Run `pip install -r requirements.txt` in backend folder

**"GEMINI_API_KEY not set"**
→ Add your API key to `backend/.env`

**Qdrant connection error**
→ Run `docker-compose up -d qdrant` manually
