# AI Concierge Platform

AI-powered concierge service that makes personalized white-glove service scalable for family offices and high-net-worth clients.

## 🎯 Overview

- **Multi-channel communication**: Slack, Email, Web
- **Proactive reminders**: Birthdays, renewals, maintenance schedules
- **Smart recommendations**: Restaurants, venues, vendors, gifts
- **Project management**: Track complex concierge requests
- **AI agents**: Intelligent routing and contextual responses

## 🏗️ Architecture

```
Frontend (Next.js on Vercel)
    ↓
Backend (FastAPI on Railway)
    ↓
Database (PostgreSQL on Supabase)
    ↓
AI Layer (Claude via Anthropic API)
    ↓
Integrations (Slack, AWS SES)
```

## 📁 Project Structure

```
ai-concierge/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI application
│   │   ├── config.py    # Environment configuration
│   │   ├── database.py  # Database connection
│   │   ├── api/         # API endpoints
│   │   ├── agents/      # AI agents
│   │   ├── integrations/# Slack, Email integrations
│   │   ├── models/      # Database models
│   │   └── utils/       # Utility functions
│   ├── tests/           # Test files
│   ├── requirements.txt # Python dependencies
│   └── .env.example     # Environment variables template
├── frontend/            # Next.js frontend (coming soon)
└── docs/               # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL (via Supabase)
- Slack workspace
- Anthropic API key
- AWS account (for SES)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ai-concierge.git
cd ai-concierge

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your credentials

# Run locally
uvicorn app.main:app --reload --port 8000
```

### Environment Variables

See `.env.example` for all required variables:

- **Supabase**: Database connection
- **Anthropic**: AI/Claude API
- **Slack**: Bot tokens for messaging
- **AWS SES**: Email sending/receiving
- **Application**: Secret keys and config

Full setup guide: [ENV_SETUP_GUIDE.md](docs/ENV_SETUP_GUIDE.md)

## 🗄️ Database Schema

27 tables organized into 8 domains:

1. **Identity**: organizations, accounts, persons
2. **Communication**: comm_identities, conversations, messages
3. **Households**: households, addresses
4. **Dates & Reminders**: date_items, reminder_rules
5. **Projects**: projects, tasks
6. **Recommendations**: vendors, venues, restaurants, products
7. **AI Infrastructure**: agent_roster, embeddings
8. **Audit**: event_log

Full schema: [schema_mvp.sql](docs/schema_mvp.sql)

## 🤖 AI Agents

### Orchestrator Agent
Routes incoming messages to appropriate specialized agents.

### Retrieval Agent
Queries database for client information and preferences.

### Recommendation Agent
Provides personalized suggestions based on client profile.

### Reminder Agent
Sends proactive reminders for important dates and events.

### Project Management Agent
Tracks and updates ongoing concierge projects.

### Data Capture Agent
Extracts structured information from conversations.

## 📡 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check with database test
- `GET /docs` - Interactive API documentation

### Coming Soon
- `POST /api/messages` - Send message to AI
- `GET /api/persons` - List clients
- `GET /api/projects` - List projects
- `POST /api/reminders` - Create reminder

Full API documentation: http://localhost:8000/docs

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Test specific file
pytest tests/test_agents.py -v
```

## 🚂 Deployment

### Railway (Backend)
```bash
# Push to deploy
git push origin main
```

Railway automatically:
- Detects Python app
- Installs dependencies
- Runs Procfile
- Exposes HTTPS endpoint

### Vercel (Frontend)
```bash
# Deploy from GitHub
# Vercel auto-deploys on push to main
```

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL (Supabase) |
| Frontend | Next.js (React) |
| AI | Claude (Anthropic) |
| Agent Framework | LangGraph |
| Email | Amazon SES |
| Chat | Slack SDK |
| Backend Hosting | Railway |
| Frontend Hosting | Vercel |
| Vector Search | pgvector |

## 🔐 Security

- ✅ Environment variables never committed
- ✅ Row-level security on database
- ✅ JWT authentication
- ✅ HTTPS everywhere
- ✅ Service keys backend-only
- ✅ CORS configured
- ✅ Rate limiting (coming soon)

## 📚 Documentation

- [Technical Specification](docs/AI_Concierge_Technical_Specification_v2.docx)
- [Database Schema](docs/schema_mvp.sql)
- [Environment Setup Guide](docs/ENV_SETUP_GUIDE.md)
- [Day 0 Implementation Guide](docs/DAY_0_IMPLEMENTATION_GUIDE.md)
- [Command Cheat Sheet](docs/COMMAND_CHEAT_SHEET.md)

## 🗓️ Development Roadmap

### Week 1 (MVP)
- [x] Database schema deployed
- [x] Backend skeleton with health check
- [x] Slack integration
- [ ] Orchestrator agent
- [ ] Retrieval agent
- [ ] Reminder agent
- [ ] Basic staff dashboard

### Week 2
- [ ] Email integration (SES)
- [ ] Project management
- [ ] Recommendation engine
- [ ] End-to-end testing
- [ ] Production deployment

### Future (V2)
- [ ] Client-facing web portal
- [ ] Data capture agent
- [ ] Web search integration
- [ ] Analytics dashboard
- [ ] Mobile app

## 🤝 Contributing

This is a private project. For questions or suggestions, contact the team.

## 📄 License

Proprietary - All Rights Reserved

## 🆘 Support

- Check [Command Cheat Sheet](docs/COMMAND_CHEAT_SHEET.md) for common commands
- See [Troubleshooting Guide](docs/DAY_0_IMPLEMENTATION_GUIDE.md#troubleshooting)
- Review logs in Railway dashboard
- Check Supabase dashboard for database issues

## 📈 Metrics

**Target for MVP:**
- Support 5 clients
- 100+ interactions per day
- <5 second response time
- 95%+ accuracy
- 99.5% uptime

---

Built with ❤️ using Claude, FastAPI, and Supabase
