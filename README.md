# ETCS Documentation Assistant

> AI-Powered Platform for Railway Engineers to Interact with ETCS Technical Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)

## Overview

The ETCS Documentation Assistant is a production-ready web application designed to help railway engineers efficiently navigate and understand ETCS (European Train Control System) technical specifications through AI-powered conversations with precise citations and an integrated document viewer.

## Features

### Phase 1 (Current) ✅

- **AI Chat Interface** with 9 conversation styles:
  - Professional, Entry-Level, Newbie, 10-Year-Old
  - Detailed, Concise, Funny, Academic, Practical

- **User Authentication & Management**
  - JWT-based authentication with refresh tokens
  - Secure password hashing
  - User registration and login

- **Conversation Management**
  - Create, view, and delete conversations
  - Message history persistence
  - Citation display framework

- **Modern UI/UX**
  - Split-screen layout (chat + document viewer)
  - Responsive design (mobile-first)
  - Professional interface for engineers
  - Dark mode support

- **Backend Infrastructure**
  - RESTful API with FastAPI
  - PostgreSQL database with Alembic migrations
  - Redis caching
  - Qdrant vector database integration (ready for Phase 2)

### Phase 2 (Planned)

- RAG system with Claude API integration
- Document upload and processing pipeline
- PDF text extraction with metadata
- Semantic search with precise citations
- Auto-scroll and paragraph highlighting

### Phase 3 (Planned)

- Advanced document viewer with React-PDF
- Bookmarking and annotations
- Conversation export (PDF, Word, Markdown)
- ETCS glossary with tooltips

### Phase 4 (Future)

- Admin panel and analytics
- Version comparison tools
- Multi-language support (EN, DE, FR)
- Collaborative workspaces
- PWA with offline capabilities

## Tech Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand
- **Data Fetching**: React Query
- **Animations**: Framer Motion
- **Document Viewer**: React-PDF (Phase 3)

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 16
- **Vector DB**: Qdrant
- **Cache**: Redis
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Task Queue**: Celery (Phase 2)

### AI/ML (Phase 2)
- Claude API (Anthropic) - Chat
- OpenAI Embeddings - Vector search
- LangChain - RAG orchestration
- PyMuPDF - PDF processing

## Project Structure

```
etcs-documentation-assistant/
├── frontend/              # Next.js application
│   ├── src/
│   │   ├── app/          # App router pages
│   │   ├── components/   # React components
│   │   │   ├── chat/     # Chat interface
│   │   │   ├── document/ # Document viewer
│   │   │   ├── layout/   # Layout components
│   │   │   └── ui/       # shadcn/ui components
│   │   ├── lib/          # Utilities (API client, utils)
│   │   ├── types/        # TypeScript types
│   │   └── styles/       # Global styles
│   ├── public/           # Static assets
│   └── package.json
│
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/          # API routes (auth, chat)
│   │   ├── core/         # Config, database, security
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # Application entry point
│   ├── alembic/          # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml    # Infrastructure services
├── .env.example          # Environment variables template
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 16 (or use Docker)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd etcs-documentation-assistant
```

2. **Set up environment variables**

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: Change SECRET_KEY in production!

# Create frontend env file
cd frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
cd ..
```

3. **Start infrastructure services**

```bash
# Start PostgreSQL, Redis, and Qdrant
docker-compose up -d

# Wait for services to be healthy
docker-compose ps
```

4. **Set up backend**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/api/docs

5. **Set up frontend** (in a new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### Development Workflow

**Backend Development**

```bash
# Run tests
pytest

# Format code
black .

# Lint code
flake8

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

**Frontend Development**

```bash
# Type checking
npm run type-check

# Lint
npm run lint

# Build for production
npm run build
```

## API Documentation

### Authentication Endpoints

**POST** `/api/v1/auth/register` - Register new user
- Body: `{ email, password, full_name }`
- Returns: `{ access_token, refresh_token, user }`

**POST** `/api/v1/auth/login` - Login
- Body: `{ email, password }`
- Returns: `{ access_token, refresh_token, user }`

**POST** `/api/v1/auth/refresh` - Refresh access token
- Body: `{ refresh_token }`
- Returns: `{ access_token, refresh_token, user }`

**GET** `/api/v1/auth/me` - Get current user
- Headers: `Authorization: Bearer <token>`
- Returns: `{ id, email, full_name, ... }`

### Chat Endpoints

**POST** `/api/v1/chat/message` - Send message
- Headers: `Authorization: Bearer <token>`
- Body: `{ conversation_id?, message, style }`
- Returns: `{ conversation_id, message, citations }`

**GET** `/api/v1/chat/conversations` - List conversations
- Headers: `Authorization: Bearer <token>`
- Returns: `[{ id, title, style, created_at, ... }]`

**GET** `/api/v1/chat/conversations/{id}` - Get conversation with messages
- Headers: `Authorization: Bearer <token>`
- Returns: `{ id, title, messages: [...], ... }`

**DELETE** `/api/v1/chat/conversations/{id}` - Delete conversation
- Headers: `Authorization: Bearer <token>`

## Database Schema

### Users
- id (UUID), email, full_name, hashed_password
- is_active, is_superuser
- created_at, updated_at

### Conversations
- id (UUID), user_id, title, style
- created_at, updated_at

### Messages
- id (UUID), conversation_id, role (user/assistant)
- content, citations (JSON)
- created_at

### Documents (Phase 2)
- id (UUID), title, subset_number, version
- file_path, page_count, processed
- uploaded_at, processed_at

### Bookmarks (Phase 3)
- id (UUID), user_id, conversation_id, message_id
- note, created_at

## Environment Variables

See `.env.example` for all available configuration options.

**Critical variables:**
- `SECRET_KEY` - JWT secret (change in production!)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `ANTHROPIC_API_KEY` - Claude API key (Phase 2)
- `OPENAI_API_KEY` - OpenAI API key (Phase 2)

## Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=false`
- [ ] Configure production database
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS origins
- [ ] Set up monitoring (Sentry)
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline
- [ ] Performance testing
- [ ] Security audit

### Docker Production Build

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d
```

## Roadmap

### Phase 1: Foundation ✅ (Completed)
- Project structure and configuration
- Frontend UI/UX with chat interface
- Backend API with authentication
- Database models and migrations
- Docker infrastructure

### Phase 2: RAG System (Next)
- Document upload and processing
- PDF text extraction with chunking
- Vector embeddings and Qdrant integration
- Claude API integration for chat
- Citation extraction and linking

### Phase 3: Document Viewer
- React-PDF integration
- Auto-scroll to citations
- Paragraph highlighting
- Bookmarking system
- Annotation tools

### Phase 4: Advanced Features
- Semantic search
- Export functionality
- Admin panel
- Analytics dashboard
- Multi-language support

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- ETCS specifications by ERA (European Union Agency for Railways)
- shadcn/ui for beautiful UI components
- FastAPI and Next.js communities

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)
- Documentation: See `/docs` folder
- Email: support@example.com

---

Built with ❤️ for railway engineers worldwide
