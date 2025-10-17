# Day 0: From Empty Repo to Working Skeleton
## Practical Implementation Guide for Cursor + Claude CLI

This guide takes you from an empty GitHub repo to a deployable MVP skeleton in ~4 hours.

---

## 🎯 Goal for Day 0

By end of today, you'll have:
- ✅ Complete project structure
- ✅ Database connected and schema deployed
- ✅ Basic FastAPI backend running locally
- ✅ One working endpoint (health check)
- ✅ Slack bot that receives messages (doesn't respond yet)
- ✅ Code committed to GitHub
- ✅ Railway deployment (even if minimal)

---

## 📁 Step 1: Set Up Project Structure (10 minutes)

### Clone your repo and create structure

```bash
# Clone your empty repo
git clone https://github.com/yourusername/ai-concierge.git
cd ai-concierge

# Create backend structure
mkdir -p backend/app/{api,agents,integrations,models,utils}
mkdir -p backend/tests

# Create frontend structure (we'll do this later)
mkdir -p frontend

# Create root files
touch backend/requirements.txt
touch backend/.env.example
touch backend/.env
touch backend/Procfile
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/config.py
touch backend/app/database.py
touch .gitignore
touch README.md
```

### Create .gitignore

```bash
cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/

# IDEs
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Logs
*.log
logs/

# Database
*.db
*.sqlite

# Node (for frontend later)
node_modules/
.next/
out/
dist/

# Misc
.pytest_cache/
.coverage
htmlcov/
EOF
```

### Commit the structure

```bash
git add .
git commit -m "Initial project structure"
git push origin main
```

---

## 📝 Step 2: Set Up Backend Skeleton (30 minutes)

### Create requirements.txt

```bash
cat > backend/requirements.txt << 'EOF'
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
supabase==2.3.0

# AI
anthropic==0.8.1
langgraph==0.0.20
langchain-core==0.1.3

# Integrations
slack-sdk==3.23.0
slack-bolt==1.18.0
boto3==1.34.10

# Utilities
python-dotenv==1.0.0
httpx==0.25.2
pydantic[email]==2.5.2
python-multipart==0.0.6

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.12.0
EOF
```

### Create Procfile (for Railway)

```bash
cat > backend/Procfile << 'EOF'
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF
```

### Create backend/app/config.py

Use Claude CLI to generate this file:

```bash
# From your project root
claude-cli ask "Generate a Python config.py file for a FastAPI app that loads these environment variables from .env: SUPABASE_URL, SUPABASE_SERVICE_KEY, DATABASE_URL, ANTHROPIC_API_KEY, SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_SIGNING_SECRET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, SES_EMAIL_ADDRESS, SECRET_KEY, ENVIRONMENT. Use pydantic-settings for type-safe config. Save to backend/app/config.py"
```

Or in Cursor, create `backend/app/config.py` and ask:
```
Generate a Pydantic Settings class that loads all environment variables 
from the .env.example file I showed you earlier. Use validation and defaults.
```

### Create backend/app/database.py

```bash
claude-cli ask "Generate a database.py file that creates a SQLAlchemy engine and session maker using the DATABASE_URL from config. Include a get_db() dependency for FastAPI. Save to backend/app/database.py"
```

Or manually create:

```python
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Create backend/app/main.py

```python
# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db

app = FastAPI(
    title="AI Concierge API",
    description="Backend API for AI-powered concierge platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "AI Concierge API",
        "environment": settings.ENVIRONMENT,
        "status": "running"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check with database connection test"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Create .env file

```bash
cp backend/.env.example backend/.env
# Now edit backend/.env with your actual credentials
```

---

## 🗄️ Step 3: Set Up Supabase (20 minutes)

### Create Supabase project
1. Go to https://supabase.com
2. Create new project: "ai-concierge"
3. Save the database password!
4. Wait ~2 minutes for provisioning

### Get credentials
1. Go to Project Settings → API
2. Copy:
   - URL → `SUPABASE_URL`
   - anon public → `SUPABASE_ANON_KEY`
   - service_role → `SUPABASE_SERVICE_KEY`

3. Go to Project Settings → Database
4. Copy Connection String (Transaction mode)
5. Replace `[YOUR-PASSWORD]` with your database password
6. This is your `DATABASE_URL`

### Deploy schema
1. Go to SQL Editor in Supabase
2. Click "New query"
3. Paste contents of `schema_mvp.sql`
4. Click "Run"
5. You should see: "Success. No rows returned"

### Update .env
```bash
# Edit backend/.env and add:
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGci...
DATABASE_URL=postgresql://postgres.xxxxx:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## 🚀 Step 4: Test Backend Locally (15 minutes)

### Install dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate     # On Windows

# Install packages
pip install -r requirements.txt
```

### Run the server

```bash
# Make sure you're in backend/ directory with venv activated
uvicorn app.main:app --reload --port 8000
```

### Test endpoints

Open another terminal:

```bash
# Test root endpoint
curl http://localhost:8000/

# Test health check (this tests database connection!)
curl http://localhost:8000/health
```

You should see:
```json
{"status": "healthy", "database": "connected"}
```

🎉 If this works, your database is connected!

---

## 💬 Step 5: Set Up Basic Slack Integration (30 minutes)

### Create Slack app
1. Go to https://api.slack.com/apps
2. "Create New App" → "From scratch"
3. Name: "AI Concierge"
4. Choose your workspace

### Enable Socket Mode
1. Settings → Socket Mode → Enable
2. Generate token with `connections:write` scope
3. Copy token → `SLACK_APP_TOKEN` (starts with `xapp-`)

### Add Bot Permissions
1. OAuth & Permissions → Bot Token Scopes
2. Add:
   - `chat:write`
   - `im:history`
   - `im:write`
   - `users:read`

3. Install to workspace
4. Copy "Bot User OAuth Token" → `SLACK_BOT_TOKEN` (starts with `xoxb-`)

### Get Signing Secret
1. Basic Information → App Credentials
2. Copy "Signing Secret" → `SLACK_SIGNING_SECRET`

### Update .env
```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_SIGNING_SECRET=abc123...
```

### Create Slack integration file

```bash
# Create the file
touch backend/app/integrations/__init__.py
touch backend/app/integrations/slack_bot.py
```

Use Claude CLI:

```bash
claude-cli ask "Generate a slack_bot.py file using slack_bolt and Socket Mode that:
1. Connects using SLACK_BOT_TOKEN and SLACK_APP_TOKEN from config
2. Listens for messages in DMs
3. Logs received messages
4. Responds with 'Message received: {text}'
5. Has a start() method to run the socket connection
Save to backend/app/integrations/slack_bot.py"
```

Or create manually:

```python
# backend/app/integrations/slack_bot.py
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Slack app
app = App(token=settings.SLACK_BOT_TOKEN)

@app.message("")
def handle_message(message, say, logger):
    """Handle all messages"""
    text = message.get("text", "")
    user = message.get("user")
    
    logger.info(f"Received message from {user}: {text}")
    
    # Simple echo for now
    say(f"Message received: {text}")

def start_slack_bot():
    """Start the Slack bot in Socket Mode"""
    handler = SocketModeHandler(app, settings.SLACK_APP_TOKEN)
    logger.info("Starting Slack bot...")
    handler.start()

if __name__ == "__main__":
    start_slack_bot()
```

### Test Slack bot

```bash
# In backend/ directory with venv activated
python -m app.integrations.slack_bot
```

Now go to Slack and message your bot. You should see:
- Log in terminal showing message received
- Bot responds with "Message received: [your text]"

🎉 If this works, Slack integration is done!

---

## 🚂 Step 6: Deploy to Railway (20 minutes)

### Commit your code

```bash
# Make sure you're in project root
git add .
git commit -m "Add backend skeleton with Slack integration"
git push origin main
```

### Create Railway project

1. Go to https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select your `ai-concierge` repo
5. Railway detects Python automatically

### Configure environment variables

1. Click your service → Variables
2. Add ALL variables from your .env:
   ```
   SUPABASE_URL=...
   SUPABASE_SERVICE_KEY=...
   DATABASE_URL=...
   ANTHROPIC_API_KEY=...
   SLACK_BOT_TOKEN=...
   SLACK_APP_TOKEN=...
   SLACK_SIGNING_SECRET=...
   SECRET_KEY=... (generate with: openssl rand -base64 32)
   ENVIRONMENT=production
   ```

3. **Important**: Add this Railway-specific variable:
   ```
   PORT=8000
   ```

### Get your URL

1. Settings → Domains
2. Railway gives you: `https://something.up.railway.app`
3. Click "Generate Domain"

### Test deployment

```bash
# Wait ~2 minutes for deployment
curl https://your-app.up.railway.app/
curl https://your-app.up.railway.app/health
```

🎉 If this works, you're deployed!

---

## ✅ Day 0 Checklist

You should now have:

- [x] Project structure created
- [x] Backend skeleton with FastAPI
- [x] Database connected (Supabase)
- [x] Schema deployed
- [x] Health check endpoint working
- [x] Slack bot receiving messages
- [x] Code in GitHub
- [x] Deployed to Railway

---

## 🎯 What to Do Next (Day 1)

Tomorrow, you'll build the actual AI agents:

1. **Morning**: Create orchestrator agent
   - Use Claude CLI: "Generate orchestrator agent that routes Slack messages to appropriate handlers"
   - Connect it to your Slack bot

2. **Afternoon**: Create retrieval agent
   - Query database for client info
   - Use Claude CLI: "Generate retrieval agent that can query persons table"

3. **Evening**: Test end-to-end
   - Message bot in Slack
   - Bot queries database for your info
   - Bot responds with personalized message

---

## 🆘 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in backend/ with venv activated
pip install -r requirements.txt
```

### Database connection fails
```bash
# Test connection directly
psql "$DATABASE_URL" -c "SELECT 1"

# If this fails, check:
# 1. DATABASE_URL is correct
# 2. Password has no special chars (or is URL-encoded)
# 3. Supabase project is running
```

### Slack bot doesn't respond
```bash
# Check:
# 1. Socket Mode is enabled
# 2. Bot is installed to workspace
# 3. Bot has im:history and im:write scopes
# 4. SLACK_APP_TOKEN starts with xapp-
# 5. SLACK_BOT_TOKEN starts with xoxb-
```

### Railway deployment fails
```bash
# Check logs:
# 1. Railway dashboard → your service → Logs
# 2. Look for errors in deployment
# 3. Common issue: missing Procfile or wrong path
# 4. Make sure Procfile is in root, not backend/
```

---

## 💡 Using Claude CLI Effectively

### Pattern for generating code

```bash
# Be specific about:
# 1. What the file does
# 2. What it imports
# 3. Where to save it
# 4. Any specific requirements

claude-cli ask "Generate a [filename] that:
- Does X
- Uses Y library
- Imports Z from config
- Has error handling
- Includes type hints
Save to path/to/file.py"
```

### Pattern for fixing bugs

```bash
claude-cli ask "I'm getting error: [paste error]

Here's my code:
[paste code]

Fix the error and explain what was wrong."
```

### Using Cursor for faster iteration

In Cursor:
1. Select code
2. Cmd+K (Mac) or Ctrl+K (Windows)
3. Type what you want changed
4. Accept or reject changes

Example prompts:
- "Add error handling to this function"
- "Add type hints"
- "Make this async"
- "Add logging"

---

## 📚 Files You Should Have After Day 0

```
ai-concierge/
├── .gitignore
├── README.md
├── Procfile
└── backend/
    ├── requirements.txt
    ├── .env.example
    ├── .env (not in git)
    ├── app/
    │   ├── __init__.py
    │   ├── main.py          # FastAPI app with health check
    │   ├── config.py        # Environment variables
    │   ├── database.py      # Database connection
    │   ├── api/
    │   │   └── __init__.py
    │   ├── agents/
    │   │   └── __init__.py
    │   ├── integrations/
    │   │   ├── __init__.py
    │   │   └── slack_bot.py # Working Slack bot
    │   ├── models/
    │   │   └── __init__.py
    │   └── utils/
    │       └── __init__.py
    └── tests/
        └── __init__.py
```

---

## 🎉 Success Criteria for Day 0

You're ready for Day 1 if:

1. ✅ `curl https://your-railway-app.up.railway.app/health` returns `{"status": "healthy"}`
2. ✅ You can message your Slack bot and it responds
3. ✅ Your code is in GitHub
4. ✅ You understand the project structure
5. ✅ You can run the backend locally

If all 5 work, you've successfully completed Day 0! 🚀

Tomorrow you'll add the AI agents that make this actually intelligent.

---

## 📞 Next Steps

Reply with any errors you hit, and I'll help you debug them immediately.

Once Day 0 is complete, let me know and I'll give you the Day 1 guide for building your first AI agent.
