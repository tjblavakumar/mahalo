# 🎯 MAHALO Project - Quick Start Guide

## What is MAHALO?

MAHALO is an intelligent AI assistant that helps you query and analyze data from multiple sources (JIRA, ServiceNow, Splunk) using natural language.

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```powershell
cd C:\Users\L1LTB01\LavaCode\MAHALO\mahalo-main
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate Test Data
```powershell
# Quick demo dataset (fast, no API cost)
python backend\utils\generate_test_data.py --jira-data 50 --servicenow-data 30 --splunk-data 100 --servicenow-deployments 20
```

### 3. Start Backend Services
```powershell
# Terminal 1 - JIRA Service (Port 5001)
python -m uvicorn backend.jira.app:app --host 0.0.0.0 --port 5001 --reload

# Terminal 2 - ServiceNow Service (Port 5002)
python -m uvicorn backend.servicenow.app:app --host 0.0.0.0 --port 5002 --reload

# Terminal 3 - Splunk Service (Port 5003)
python -m uvicorn backend.splunk.app:app --host 0.0.0.0 --port 5003 --reload
```

Or use the scripts:
```powershell
cd scripts
.\start_all.bat
```

### 4. Verify Services
```powershell
python check_services.py
```

You should see ✓ for all three services.

### 5. Start Main API
```powershell
# Terminal 4 - Main API (Port 8000)
python api/main.py
```

### 6. Start Frontend
```powershell
cd frontend
npm install
npm run dev
```

Visit: http://localhost:3000

## 📁 Project Structure

```
mahalo-main/
├── api/                    # Main API gateway
│   ├── main.py            # FastAPI application
│   └── routes/            # API route handlers
│       ├── admin.py       # Admin endpoints
│       └── chat.py        # Chat/query endpoints
│
├── backend/               # Mock backend services
│   ├── config.py         # Configuration settings
│   ├── database.py       # SQLite database setup
│   ├── models/           # SQLAlchemy models
│   ├── jira/            # JIRA mock API
│   ├── servicenow/      # ServiceNow mock API
│   ├── splunk/          # Splunk mock API
│   └── utils/           # Utilities
│       ├── generate_test_data.py      # Fast data generator
│       └── generate_test_data_llm.py  # LLM-enhanced generator
│
├── agents/              # AI agents for different tasks
│   ├── orchestrator.py  # Main orchestration agent
│   ├── jira_agent.py   # JIRA query agent
│   ├── servicenow_agent.py  # ServiceNow query agent
│   └── splunk_agent.py # Splunk query agent
│
├── mcp_servers/        # MCP server implementations
│   ├── jira_mcp/
│   ├── servicenow_mcp/
│   └── splunk_mcp/
│
├── frontend/           # React frontend application
│   ├── src/
│   └── package.json
│
├── scripts/            # Utility scripts
│   ├── start_all.bat  # Start all services
│   ├── stop_all.bat   # Stop all services
│   └── generate_test_data.bat  # Generate test data
│
├── docs/              # Documentation
│   └── archive/       # Archived documentation
│
└── tests/            # Test files
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# API Configuration
MAIN_API_PORT=8000
JIRA_API_PORT=5001
SERVICENOW_API_PORT=5002
SPLUNK_API_PORT=5003

# LLM Configuration
ONE_MIN_AI_API_KEY=your_api_key_here
ONE_MIN_AI_BASE_URL=https://api.1min.ai/v1
LITELLM_MODEL=gpt-4o-mini

# Database
DATABASE_URL=sqlite:///./mahalo.db

# Proxy (if needed)
NO_PROXY=localhost,127.0.0.1
```

## 📝 Common Tasks

### Generate Test Data

**Fast (No API cost):**
```powershell
python backend\utils\generate_test_data.py --jira-data 100 --servicenow-data 50 --splunk-data 200
```

**LLM-Enhanced (Better quality, requires API):**
```powershell
python backend\utils\generate_test_data_llm.py --quick
```

### Check Service Health
```powershell
python check_services.py
```

### Reset Database
```powershell
python backend\utils\reset_data.py
```

### Run Tests
```powershell
pytest tests/
```

## 🎯 Example Queries

Once everything is running, try these queries in the frontend:

1. **Simple Query:**
   - "Show me high priority JIRA stories"
   - "What incidents happened this week?"
   - "Show me error logs from payment-service"

2. **Complex Query:**
   - "Show me critical bugs and their related incidents"
   - "What deployments happened in production last month?"
   - "Give me an executive summary of all issues"

3. **Multi-Source Query:**
   - "Show me JIRA stories, related bugs, and any incidents"
   - "What's the status of payment-related issues across all systems?"

## 🐛 Troubleshooting

### Services Won't Start
```powershell
# Check if ports are already in use
netstat -ano | findstr "5001 5002 5003 8000"

# Kill processes if needed
taskkill /F /PID <process_id>
```

### No Data Returned
```powershell
# Verify database has data
python -c "from backend.database import SessionLocal; from backend.models.jira_models import JiraStory; db = SessionLocal(); print(f'Stories: {db.query(JiraStory).count()}'); db.close()"

# Generate data if empty
python backend\utils\generate_test_data.py --jira-data 20 --servicenow-data 10 --splunk-data 50
```

### Import Errors
```powershell
# Make sure virtual environment is activated
.\.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Proxy Issues
If behind a corporate proxy, add to .env:
```bash
NO_PROXY=localhost,127.0.0.1
```

## 📚 Documentation

- **START_HERE.md** - This file (quick start guide)
- **docs/archive/** - Archived documentation (proxy fixes, test data improvements)
- **backend/utils/README_TEST_DATA.md** - Test data generation guide

## 🛠️ Development

### Code Structure
- **API Layer** (`api/`) - FastAPI REST endpoints
- **Backend Services** (`backend/`) - Mock data sources
- **Agents** (`agents/`) - LLM-powered query agents
- **Frontend** (`frontend/`) - React UI

### Adding New Features
1. Add backend models in `backend/models/`
2. Create service routes in `backend/<service>/routes.py`
3. Add agent logic in `agents/`
4. Update frontend components in `frontend/src/`

## 🚀 Deployment

### Production Checklist
- [ ] Set proper environment variables
- [ ] Use production database (PostgreSQL recommended)
- [ ] Configure CORS properly
- [ ] Set up HTTPS
- [ ] Enable logging and monitoring
- [ ] Set resource limits
- [ ] Configure rate limiting

## 📧 Support

For issues or questions:
1. Check troubleshooting section above
2. Review archived docs in `docs/archive/`
3. Check console logs for errors

## 🎉 Quick Win

Want to see it working immediately?

```powershell
# 1. Generate data (30 seconds)
python backend\utils\generate_test_data.py --jira-data 20 --servicenow-data 10 --splunk-data 30

# 2. Start services (in scripts folder)
cd scripts
.\start_all.bat

# 3. Check health
cd ..
python check_services.py

# 4. Start main API
python api/main.py

# 5. In new terminal - start frontend
cd frontend
npm run dev
```

Open http://localhost:3000 and start querying! 🎊

---

**Last Updated:** December 2024
**Version:** 1.0.0
