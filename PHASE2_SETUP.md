# Phase 2 Setup Guide - RAG System

Phase 2 adds the complete RAG (Retrieval-Augmented Generation) system with real ETCS documentation integration.

## What's New in Phase 2

✅ **Real AI Integration** - Gemini 1.5 Flash for chat responses
✅ **Document Processing** - PDF text extraction and intelligent chunking
✅ **Vector Search** - Semantic search using Qdrant vector database
✅ **Smart Citations** - Automatic citation extraction and formatting
✅ **9 Conversation Styles** - Professional, Entry-Level, Newbie, 10-Year-Old, Detailed, Concise, Funny, Academic, Practical

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for Qdrant)
- Gemini API Key (FREE tier available)
- ETCS PDF documents in `backend/documents/`

## Step-by-Step Setup

### 1. Get Gemini API Key (FREE)

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your-actual-api-key-here
```

### 3. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies in Phase 2:
- `google-generativeai` - Gemini API client
- `pymupdf` - PDF text extraction
- `qdrant-client` - Vector database client
- `langchain` - RAG framework

### 4. Start Qdrant Vector Database

```bash
# From project root
docker-compose up -d qdrant

# Verify Qdrant is running
curl http://localhost:6333/collections
```

Qdrant will be available at: http://localhost:6333

### 5. Add ETCS Documents

Place your ETCS PDF files in `backend/documents/`:

```
backend/documents/
  ├── Subset-026.pdf
  ├── Subset-023.pdf
  ├── Subset-037.pdf
  └── ... (other subsets)
```

### 6. Initialize Documents

This script processes all PDFs and loads them into Qdrant:

```bash
cd backend
python scripts/init_documents.py
```

What it does:
1. ✅ Extracts text from PDFs using PyMuPDF
2. ✅ Creates intelligent chunks (1000 chars, 200 overlap)
3. ✅ Generates embeddings using Gemini
4. ✅ Stores in Qdrant vector database

**Note:** This may take 5-30 minutes depending on document size and number. This is a ONE-TIME operation - embeddings are stored permanently.

### 7. Start Backend Server

```bash
# From backend directory
python -m app.main

# Or with hot reload
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000

### 8. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

## How It Works

### RAG Pipeline

```
User Question
    ↓
1. Generate Query Embedding (Gemini)
    ↓
2. Search Vector Database (Qdrant)
    ↓
3. Retrieve Top 5 Relevant Chunks
    ↓
4. Build Context with Citations
    ↓
5. Generate AI Response (Gemini)
    ↓
6. Extract & Format Citations
    ↓
User receives answer with sources
```

### Example Query Flow

**User asks:** "What is a Movement Authority?"

1. **Embedding:** Query converted to 768-dim vector
2. **Search:** Qdrant finds top 5 similar chunks from Subset-026
3. **Context:** Chunks assembled with metadata [Subset-026, §3.4.2, p.42]
4. **Generation:** Gemini generates response using context
5. **Citations:** Response includes `[Subset-026, §3.4.2, p.42, ¶5]`

## API Endpoints (Phase 2)

### Chat with RAG
```bash
POST /api/v1/chat/message
{
  "message": "What is ETCS Level 2?",
  "style": "professional",
  "conversation_id": null
}

Response:
{
  "conversation_id": "uuid",
  "message": {
    "content": "ETCS Level 2 is...",
    "citations": [
      {
        "subset": "Subset-026",
        "section": "3.4.2",
        "page": 42,
        "paragraph": "5",
        "text": "excerpt..."
      }
    ]
  }
}
```

### Search Documents
```bash
POST /api/v1/documents/search
{
  "query": "radio block centre",
  "top_k": 5,
  "subset_filter": "Subset-026"
}
```

### List Documents
```bash
GET /api/v1/documents/list
```

### Collection Info
```bash
GET /api/v1/documents/info
```

## Conversation Styles

Test different styles for the same question:

**Professional**: Technical terminology, formal tone
**Entry-Level**: Clear explanations, defined acronyms
**Newbie**: Simple language, everyday analogies
**10-Year-Old**: Very simple, fun comparisons
**Detailed**: In-depth, comprehensive explanations
**Concise**: Brief, bullet-point answers
**Funny**: Humor + accuracy
**Academic**: Scholarly, research-oriented
**Practical**: Real-world application focus

## Troubleshooting

### "No results found"
- Ensure documents are initialized: `python scripts/init_documents.py`
- Check Qdrant is running: `docker-compose ps`
- Verify collection exists: `curl http://localhost:6333/collections`

### "Gemini API error"
- Check API key in `.env`
- Verify key is valid at https://makersuite.google.com/app/apikey
- Check rate limits (free tier: 15 RPM)

### "PDF extraction failed"
- Ensure PDFs are text-based (not scanned images)
- Check file permissions on `backend/documents/`
- Try with a single small PDF first

### Slow responses
- First query may be slow (cold start)
- Subsequent queries should be fast (<2s)
- Consider using paid Gemini tier for higher rate limits

## Performance

**Document Processing:**
- Small PDF (50 pages): ~2-5 minutes
- Large PDF (500 pages): ~20-30 minutes
- **ONE-TIME operation** - never needs repeating

**Query Response:**
- Vector search: <100ms
- Gemini generation: 1-2 seconds
- Total: ~2 seconds

**Scalability:**
- Supports 1000s of pages
- Concurrent users: Limited by Gemini rate limits
- Vector search scales linearly

## Cost Analysis

**Gemini Free Tier:**
- 15 requests per minute
- Perfect for development and demos
- No credit card required

**Gemini Paid Tier:**
- $0.00025 per 1K characters (input)
- $0.00050 per 1K characters (output)
- Example: 100 queries/day = ~$0.50/month

**vs OpenAI:**
- 8-10x cheaper than GPT-4
- Similar quality for technical docs

## Next Steps

**Phase 3:** Split-screen document viewer with highlighting
**Phase 4:** Advanced search, bookmarks, multi-user support

## Support

- Check logs: `backend/app/logs/`
- API docs: http://localhost:8000/api/docs
- Issues: Create issue in GitHub repo

---

**Phase 2 Complete!** 🎉

You now have a fully functional RAG system with real ETCS documentation.
