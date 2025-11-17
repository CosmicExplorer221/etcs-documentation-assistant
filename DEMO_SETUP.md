# ETCS Documentation Assistant - Demo Setup

> **Ultra-simple setup with NO Docker required!**

This demo version uses in-memory storage (no database needed). Perfect for quick demos and testing the UI.

---

## Prerequisites

1. **Python 3.11+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download here](https://nodejs.org/)
3. **Git** - [Download here](https://git-scm.com/download/win)

That's it! No Docker needed! 🎉

---

## Quick Start (Windows)

### Step 1: Get the Code

```bash
# Open Command Prompt and navigate to your projects folder
cd C:\Users\YOUR_USERNAME\YOUR_PROJECTS_FOLDER

# Clone the repository
git clone https://github.com/CosmicExplorer221/etcs-documentation-assistant.git

# Enter the folder
cd etcs-documentation-assistant

# Switch to the correct branch
git checkout claude/etcs-doc-assistant-phase1-01G9xsahjw2YkHDBeLJZ3bHR
```

### Step 2: Start Backend (Terminal 1)

```bash
# Install Python packages (one-time only)
pip install fastapi uvicorn pydantic

# Start the demo server
python demo_server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

### Step 3: Start Frontend (Terminal 2)

Open a NEW Command Prompt:

```bash
# Navigate to frontend folder
cd C:\Users\YOUR_USERNAME\YOUR_PROJECTS_FOLDER\etcs-documentation-assistant\frontend

# Install packages (one-time, takes 2-3 minutes)
npm install

# Start frontend
npm run dev
```

You should see:
```
▲ Next.js 14.2.18
- Local:   http://localhost:3000
```

**Keep this terminal open!**

### Step 4: Open the App

Open your browser: **http://localhost:3000**

---

## That's It! 🚀

You now have:
- ✅ Beautiful chat interface
- ✅ 9 conversation styles
- ✅ Mock ETCS responses
- ✅ Citation display
- ✅ Professional UI

**No Docker, no database, no complexity!**

---

## What Works

| Feature | Status |
|---------|--------|
| Chat Interface | ✅ Working |
| 9 Conversation Styles | ✅ Working |
| Message History (in-session) | ✅ Working |
| Citations Display | ✅ Working (mock data) |
| Split-screen Layout | ✅ Working |
| Document Viewer | ⏳ Placeholder (Phase 3) |
| Real AI Responses | ⏳ Phase 2 (needs API keys) |
| Persistent Storage | ⏳ Phase 2 (needs database) |

---

## Conversation Styles

Try asking the same question in different styles:

1. **Professional** - Technical language for experienced engineers
2. **Entry-Level** - Clear explanations for junior engineers
3. **Newbie** - Simple terms for ETCS beginners
4. **10-Year-Old** - Very simple with analogies
5. **Detailed** - In-depth technical explanations
6. **Concise** - Brief, to-the-point answers
7. **Funny** - Technical info with humor
8. **Academic** - Formal, research-oriented
9. **Practical** - Focus on real-world application

---

## Sample Questions to Try

- "What is ETCS Level 2?"
- "Explain the Movement Authority concept"
- "How does the Radio Block Centre work?"
- "What are the main safety functions of ETCS?"

---

## Stopping the App

When you're done:

1. **Frontend terminal**: Press `Ctrl+C`
2. **Backend terminal**: Press `Ctrl+C`

---

## Next Time You Run It

```bash
# Terminal 1: Backend
python demo_server.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

Much faster - no installs needed!

---

## Troubleshooting

### "python is not recognized"
- Install Python and check "Add Python to PATH" during installation
- Restart Command Prompt

### "npm is not recognized"
- Install Node.js
- Restart Command Prompt

### "Port 8000 already in use"
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <number> /F
```

### Frontend shows connection error
- Make sure backend is running (http://localhost:8000)
- Check Terminal 1 for errors

---

## What's Different from Full Version?

**Demo Version (This):**
- ❌ No Docker needed
- ❌ No database setup
- ✅ In-memory storage (conversations reset on server restart)
- ✅ 2-minute setup
- ✅ Perfect for demos

**Full Version (README.md):**
- ✅ Docker with PostgreSQL, Redis, Qdrant
- ✅ Persistent storage
- ✅ Multi-user support
- ✅ Production-ready
- ⏱️ 30-minute setup

---

## Ready for Customer Demo?

This demo version is perfect for showing:
- UI/UX design
- Chat functionality
- Different conversation styles
- Professional interface
- Citation system concept

**For production:** Use the full version with database (see README.md)

---

## Need Help?

Questions? Issues? Let me know!

---

**Happy demoing!** 🚂✨
