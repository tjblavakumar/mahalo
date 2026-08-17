# MAHALO - Phase 0: Project Setup ## Foundation & Environment Configuration
Phase Goal: Set up the complete project structure, environment, and database foundation.

Estimated Time: 1-2 hours

Prerequisites:

Python 3.10 or higher installed
Node.js 16+ and npm installed
Git installed
Code editor (VS Code recommended)
Terminal/command line access
📋 Phase 0 Overview
This phase establishes the foundation for MAHALO:

Create complete folder structure
Initialize Python virtual environment
Install dependencies
Configure environment variables
Set up database models
Initialize SQLite database
Create basic documentation
Validate setup
Task 0.1: Verify Prerequisites ⬜
Instruction to Coding Assistant: Verify all required tools are installed before proceeding.

Check Python Version
python3 --version
# Should show Python 3.10.x or higher
Check Node.js and npm
node --version
# Should show v16.x or higher

npm --version
# Should show 9.x or higher
Check Git
git --version
# Should show git version 2.x or higher
Acceptance Criteria:

✅ Python 3.10+ installed
✅ Node.js 16+ installed
✅ npm 9+ installed
✅ Git 2+ installed
Mark Complete: ⬜ → ✅

Task 0.2: Create Root Project Directory ⬜
Instruction to Coding Assistant: Create the root project directory and navigate into it.

# Create project directory
mkdir mahalo
cd mahalo

# Verify you're in the right place
pwd
# Should show: /path/to/mahalo
Acceptance Criteria:

✅ Directory mahalo created
✅ Currently in mahalo directory
Mark Complete: ⬜ → ✅

Task 0.3: Create Complete Folder Structure ⬜
Instruction to Coding Assistant: Create all required directories and placeholder files for the project.

Create All Directories
# Documentation
mkdir -p docs

# Backend structure
mkdir -p backend/models
mkdir -p backend/jira
mkdir -p backend/servicenow
mkdir -p backend/splunk
mkdir -p backend/utils

# MCP servers
mkdir -p mcp_servers/jira_mcp
mkdir -p mcp_servers/servicenow_mcp
mkdir -p mcp_servers/splunk_mcp

# AI agents
mkdir -p agents/prompts

# Main API
mkdir -p api/routes

# Frontend
mkdir -p frontend/src/components
mkdir -p frontend/src/services
mkdir -p frontend/src/styles
mkdir -p frontend/src/utils
mkdir -p frontend/public

# Tests
mkdir -p tests

# Scripts
mkdir -p scripts

Important: MAHALO supports both Windows and Linux local development. Create OS-specific helper scripts in the same scripts/ directory:
- Windows: .bat files for local startup, shutdown, reset, and tests
- Linux/macOS: .sh files with equivalent functionality
Create Placeholder Files
Root level files:

touch README.md
touch requirements.txt
touch .env.example
touch .gitignore
Backend files:

touch backend/__init__.py
touch backend/config.py
touch backend/database.py

touch backend/models/__init__.py
touch backend/models/jira_models.py
touch backend/models/servicenow_models.py
touch backend/models/splunk_models.py

touch backend/jira/__init__.py
touch backend/jira/app.py
touch backend/jira/routes.py
touch backend/jira/service.py
touch backend/jira/seed_data.py

touch backend/servicenow/__init__.py
touch backend/servicenow/app.py
touch backend/servicenow/routes.py
touch backend/servicenow/service.py
touch backend/servicenow/seed_data.py

touch backend/splunk/__init__.py
touch backend/splunk/app.py
touch backend/splunk/routes.py
touch backend/splunk/service.py
touch backend/splunk/seed_data.py

touch backend/utils/__init__.py
touch backend/utils/reset_data.py
touch backend/utils/validators.py
MCP server files:

touch mcp_servers/jira_mcp/__init__.py
touch mcp_servers/jira_mcp/server.py
touch mcp_servers/jira_mcp/tools.py
touch mcp_servers/jira_mcp/resources.py

touch mcp_servers/servicenow_mcp/__init__.py
touch mcp_servers/servicenow_mcp/server.py
touch mcp_servers/servicenow_mcp/tools.py
touch mcp_servers/servicenow_mcp/resources.py

touch mcp_servers/splunk_mcp/__init__.py
touch mcp_servers/splunk_mcp/server.py
touch mcp_servers/splunk_mcp/tools.py
touch mcp_servers/splunk_mcp/resources.py
Agent files:

touch agents/__init__.py
touch agents/orchestrator.py
touch agents/jira_agent.py
touch agents/servicenow_agent.py
touch agents/splunk_agent.py
touch agents/context_manager.py

touch agents/prompts/orchestrator_prompt.txt
touch agents/prompts/jira_agent_prompt.txt
touch agents/prompts/servicenow_agent_prompt.txt
touch agents/prompts/splunk_agent_prompt.txt
API files:

touch api/__init__.py
touch api/main.py
touch api/middleware.py

touch api/routes/__init__.py
touch api/routes/chat.py
touch api/routes/admin.py
Test files:

touch tests/__init__.py
touch tests/test_jira_api.py
touch tests/test_servicenow_api.py
touch tests/test_splunk_api.py
touch tests/test_mcp_servers.py
touch tests/test_agents.py
touch tests/test_integration.py
Script files:

touch scripts/start_all.sh
touch scripts/stop_all.sh
touch scripts/reset_demo.sh
touch scripts/run_tests.sh

# Make scripts executable
chmod +x scripts/*.sh

# Windows scripts remain .bat and do not need chmod
Verify Structure
# Display directory tree (if tree command available)
tree -L 2

# Or use find command
find . -type d | sort
Expected Output:

mahalo/
├── agents/
│   └── prompts/
├── api/
│   └── routes/
├── backend/
│   ├── jira/
│   ├── models/
│   ├── servicenow/
│   ├── splunk/
│   └── utils/
├── docs/
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── services/
│       ├── styles/
│       └── utils/
├── mcp_servers/
│   ├── jira_mcp/
│   ├── servicenow_mcp/
│   └── splunk_mcp/
├── scripts/
└── tests/
Acceptance Criteria:

✅ All directories created
✅ All placeholder files created
✅ Scripts are executable
Mark Complete: ⬜ → ✅

Task 0.4: Initialize Python Virtual Environment ⬜
Instruction to Coding Assistant: Create and activate Python virtual environment.

Create Virtual Environment
python3 -m venv venv
Activate Virtual Environment
**On Windows:**

```batch
venv\Scripts\activate
```

**On Linux/macOS:**

```bash
source venv/bin/activate
```

Cross-platform note:
MAHALO should be runnable in both Windows and Linux local environments using the same Python dependencies and service configuration. The only platform-specific differences are the virtual environment activation command and the script extension used for automation.

Verify Activation
which python
# Should show path inside venv directory

python --version
# Should show Python 3.10+
Acceptance Criteria:

✅ Virtual environment created in venv/ directory
✅ Virtual environment activated (prompt shows (venv))
✅ Python points to venv python
Mark Complete: ⬜ → ✅

Task 0.5: Create requirements.txt ⬜
Instruction to Coding Assistant: Create the Python dependencies file with all required packages.

Create requirements.txt
cat > requirements.txt << 'EOF'
# Core Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1

# HTTP Client
httpx==0.26.0
requests==2.31.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0

# MCP SDK (will be configured in Phase 2)
# mcp==0.1.0

# AI/LLM (will be configured in Phase 3)
# litellm==1.17.0
# openai==1.0.0
# anthropic==0.8.0

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6
aiofiles==23.2.1

# Code Quality
black==23.12.1
flake8==7.0.0
EOF
Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt
Verify Installation
pip list
# Should show all installed packages

pip list | grep fastapi
# Should show: fastapi 0.109.0

pip list | grep sqlalchemy
# Should show: sqlalchemy 2.0.25
Acceptance Criteria:

✅ requirements.txt created
✅ All dependencies installed successfully
✅ No installation errors
✅ FastAPI and SQLAlchemy verified
Mark Complete: ⬜ → ✅

Task 0.6: Create .env.example Template ⬜
Instruction to Coding Assistant: Create environment variable template file.

Create .env.example
cat > .env.example << 'EOF'
# =============================================================================
# MAHALO Environment Configuration
# =============================================================================

# Database Configuration
DATABASE_URL=sqlite:///mahalo.db

# API Ports Configuration
JIRA_API_PORT=5001
SERVICENOW_API_PORT=5002
SPLUNK_API_PORT=5003
MAIN_API_PORT=8000

# MCP Server Ports Configuration
MCP_JIRA_PORT=6001
MCP_SERVICENOW_PORT=6002
MCP_SPLUNK_PORT=6003

# LiteLLM Configuration (Add in Phase 3)
# Choose one of the following:
LITELLM_MODEL=gpt-4
OPENAI_API_KEY=your_openai_api_key_here
# OR
# LITELLM_MODEL=claude-3-sonnet-20240229
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000

# Demo Settings
DEMO_RESET_ENABLED=true

# Logging Level (optional)
LOG_LEVEL=INFO
EOF
Acceptance Criteria:

✅ .env.example created with all variables
✅ Variables are well-documented
✅ Includes all required configurations
Mark Complete: ⬜ → ✅

Task 0.7: Create .env File ⬜
Instruction to Coding Assistant: Copy template to actual .env file (will be gitignored).

cp .env.example .env
Note: The .env file will contain actual API keys later. For now, default values are fine.

Acceptance Criteria:

✅ .env file created from template
✅ File is ready for customization
Mark Complete: ⬜ → ✅

Task 0.8: Create .gitignore ⬜
Instruction to Coding Assistant: Create comprehensive .gitignore file.

Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite
*.sqlite3
mahalo.db

# Environment Variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover
*.log
.tox/
.nox/

# Node (Frontend)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
frontend/build/
frontend/.env.local
frontend/.env.development.local
frontend/.env.test.local
frontend/.env.production.local

# OS
Thumbs.db
.DS_Store

# Process tracking
.mahalo_pids

# Temporary files
*.tmp
*.temp
.cache/
EOF
Acceptance Criteria:

✅ .gitignore created
✅ Covers Python, Node, IDE files
✅ Excludes sensitive files (.env, *.db)
Mark Complete: ⬜ → ✅

Task 0.9: Create README.md ⬜
Instruction to Coding Assistant: Create comprehensive project README.

Create README.md
cat > README.md << 'EOF'
# 🌺 MAHALO - AI Harness for SDLC

**MAHALO** (Multi-Agent Harness for Agile Lifecycle Orchestration) is an AI-powered proof of concept that demonstrates intelligent orchestration of SDLC tools (JIRA, ServiceNow, Splunk) using Model Context Protocol (MCP) and specialized AI agents.

## 🎯 What is MAHALO?

MAHALO provides a unified context layer where Product Managers, Developers, QA, and Executives can interact with multiple SDLC tools through natural language using a chat interface.

### Key Features
- 🤖 **AI-Powered Agents**: Specialized agents for JIRA, ServiceNow, and Splunk
- 🔗 **MCP Integration**: Standardized tool integration via Model Context Protocol
- 👥 **Role-Based Interface**: Personalized experience for each user persona
- 💬 **Chat-First**: Natural language interaction with all tools
- 🔍 **Cross-Tool Context**: Unified view across JIRA bugs, ServiceNow incidents, and Splunk logs

## 🏗️ Architecture
UI (React) → Main API → Orchestrator Agent → Specialized Agents → MCP Servers → Tool APIs → SQLite DB


### Components
- **Frontend**: React chat interface (port 3000)
- **Main API**: FastAPI gateway (port 8000)
- **Tool APIs**: Mock JIRA (5001), ServiceNow (5002), Splunk (5003)
- **MCP Servers**: JIRA MCP (6001), ServiceNow MCP (6002), Splunk MCP (6003)
- **AI Agents**: Orchestrator + 3 specialized agents (LiteLLM)
- **Database**: SQLite (mahalo.db)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- OpenAI or Anthropic API key

### Installation

1. **Clone and Setup Backend**
```bash
git clone <your-repo-url>
cd mahalo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your API keys (use notepad .env)
```

### Initialize Database
```batch
python backend/database.py
python backend/utils/reset_data.py
```

### Setup Frontend
```batch
cd frontend
npm install
cd ..
```

### Start All Services
**Windows:**
```batch
scripts\start_all.bat
```

**Unix/Mac:**
```bash
bash scripts/start_all.sh
```
Access Application
Frontend: http://localhost:3000
Main API: http://localhost:8000/docs
JIRA API: http://localhost:5001/docs
ServiceNow API: http://localhost:5002/docs
Splunk API: http://localhost:5003/docs
🧪 Testing
Run all automated tests:

**Windows:**
```batch
scripts\run_tests.bat
```

**Unix/Mac:**
```bash
bash scripts/run_tests.sh
```

Run specific test suite:

```bash
pytest tests/test_jira_api.py -v
pytest tests/test_agents.py -v
```
📚 Documentation
Architecture Plan - Complete architecture and design
Phase 0: Setup - Initial setup guide
API Documentation - API reference
Demo Script - How to demo MAHALO
🎬 Demo Workflows
1. Executive: Sprint Status
Select: Executive persona
Ask: "Show me the current sprint status"
Result: Real-time sprint metrics from JIRA
2. Product Manager: Create Story
Select: Product Manager persona
Ask: "Create a user story for implementing OAuth login"
Result: Duplicate check, refinement help, story creation
3. Developer: View Tasks
Select: Developer persona
Ask: "Show me my assigned tasks"
Result: Prioritized task list with context
4. Cross-Tool Correlation
Ask: "Tell me about BUG-789"
Result: Bug details + linked incident + related logs
🔄 Reset Demo Data
To reset all data to initial state:

**Windows:**
```batch
scripts\reset_demo.bat
```

**Unix/Mac:**
```bash
bash scripts/reset_demo.sh
```
🛠️ Development
Project Structure
mahalo/
├── backend/          # Python backend (FastAPI)
├── mcp_servers/      # MCP server implementations
├── agents/           # AI agents (LiteLLM)
├── api/              # Main API gateway
├── frontend/         # React UI
├── tests/            # Automated tests
├── scripts/          # Helper scripts
└── docs/             # Documentation
Start Individual Services
Backend APIs:

python backend/jira/app.py          # Port 5001
python backend/servicenow/app.py    # Port 5002
python backend/splunk/app.py        # Port 5003
MCP Servers:

python mcp_servers/jira_mcp/server.py          # Port 6001
python mcp_servers/servicenow_mcp/server.py    # Port 6002
python mcp_servers/splunk_mcp/server.py        # Port 6003
Main API:

python api/main.py                  # Port 8000
Frontend:

cd frontend && npm start            # Port 3000
📊 Technology Stack
Backend: Python 3.10+, FastAPI, SQLAlchemy
Frontend: React 18+, Axios
Database: SQLite
AI/LLM: LiteLLM (OpenAI/Anthropic)
MCP: Python MCP SDK
Testing: pytest
⚠️ Known Limitations (POC)
No real authentication (persona dropdown only)
Single-user mode (no concurrency)
Conversation history not persisted
Mock tools (not actual JIRA/ServiceNow/Splunk)
Local deployment only
No production hardening
🎯 Success Criteria
✅ All 3 tools run independently
✅ MCP servers operational
✅ AI agents respond intelligently
✅ UI displays responses in real-time
✅ Demo workflows work reliably
✅ Cross-tool correlation functional
🤝 Contributing
This is a proof of concept project. Feedback and suggestions welcome!

📝 License
MIT License - Built for demonstration purposes

🙏 Acknowledgments
Model Context Protocol (MCP) for standardized tool integration
LiteLLM for unified LLM interface
FastAPI for excellent Python web framework



**Acceptance Criteria:**
- ✅ README.md created
- ✅ Includes quick start guide
- ✅ Links to documentation
- ✅ Shows architecture overview

**Mark Complete:** ⬜ → ✅

---

## Task 0.10: Create Backend Configuration ⬜

**Instruction to Coding Assistant:**
Create the configuration management module.

### Create backend/config.py
```python
"""
MAHALO Configuration Management
Loads settings from environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///mahalo.db")
    
    # API Port Configuration
    JIRA_API_PORT: int = int(os.getenv("JIRA_API_PORT", 5001))
    SERVICENOW_API_PORT: int = int(os.getenv("SERVICENOW_API_PORT", 5002))
    SPLUNK_API_PORT: int = int(os.getenv("SPLUNK_API_PORT", 5003))
    MAIN_API_PORT: int = int(os.getenv("MAIN_API_PORT", 8000))
    
    # MCP Server Port Configuration
    MCP_JIRA_PORT: int = int(os.getenv("MCP_JIRA_PORT", 6001))
    MCP_SERVICENOW_PORT: int = int(os.getenv("MCP_SERVICENOW_PORT", 6002))
    MCP_SPLUNK_PORT: int = int(os.getenv("MCP_SPLUNK_PORT", 6003))
    
    # LiteLLM Configuration (will be used in Phase 3)
    LITELLM_MODEL: str = os.getenv("LITELLM_MODEL", "gpt-4")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Demo Settings
    DEMO_RESET_ENABLED: bool = os.getenv("DEMO_RESET_ENABLED", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Project Root Directory
    BASE_DIR: Path = Path(__file__).parent.parent
    
    def get_database_path(self) -> str:
        """Get absolute path to database file"""
        if self.DATABASE_URL.startswith("sqlite:///"):
            db_file = self.DATABASE_URL.replace("sqlite:///", "")
            return str(self.BASE_DIR / db_file)
        return self.DATABASE_URL
    
    def validate(self) -> bool:
        """Validate configuration (optional)"""
        # Add validation logic if needed
        return True
    
    def __repr__(self) -> str:
        """String representation (hide sensitive data)"""
        return f"Settings(JIRA_PORT={self.JIRA_API_PORT}, DB={self.DATABASE_URL})"

# Global settings instance
settings = Settings()

# Validate settings on import
if not settings.validate():
    raise ValueError("Invalid configuration settings")

if __name__ == "__main__":
    # Test configuration
    print("MAHALO Configuration:")
    print(f"  Database URL: {settings.DATABASE_URL}")
    print(f"  JIRA API Port: {settings.JIRA_API_PORT}")
    print(f"  ServiceNow API Port: {settings.SERVICENOW_API_PORT}")
    print(f"  Splunk API Port: {settings.SPLUNK_API_PORT}")
    print(f"  Main API Port: {settings.MAIN_API_PORT}")
    print(f"  MCP JIRA Port: {settings.MCP_JIRA_PORT}")
    print(f"  MCP ServiceNow Port: {settings.MCP_SERVICENOW_PORT}")
    print(f"  MCP Splunk Port: {settings.MCP_SPLUNK_PORT}")
    print(f"  Demo Reset Enabled: {settings.DEMO_RESET_ENABLED}")
    print(f"  Base Directory: {settings.BASE_DIR}")
    print("\n✅ Configuration loaded successfully!")
Test Configuration
python backend/config.py
Expected Output:

MAHALO Configuration:
  Database URL: sqlite:///mahalo.db
  JIRA API Port: 5001
  ServiceNow API Port: 5002
  Splunk API Port: 5003
  Main API Port: 8000
  MCP JIRA Port: 6001
  MCP ServiceNow Port: 6002
  MCP Splunk Port: 6003
  Demo Reset Enabled: True
  Base Directory: /path/to/mahalo

✅ Configuration loaded successfully!
Acceptance Criteria:

✅ backend/config.py created
✅ Loads environment variables correctly
✅ Settings class defined with all required fields
✅ Test runs without errors
Mark Complete: ⬜ → ✅

Task 0.11: Create Database Connection Module ⬜
Instruction to Coding Assistant: Create the database connection and initialization module.

Create backend/database.py
"""
MAHALO Database Connection and Initialization
SQLAlchemy setup with SQLite
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    # SQLite specific settings
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI routes.
    
    Usage:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database by creating all tables.
    
    This function should be called after all models are imported.
    It will create tables for all models that inherit from Base.
    """
    # Import all models to register them with Base
    # This ensures all tables are created
    try:
        from backend.models import jira_models
        from backend.models import servicenow_models
        from backend.models import splunk_models
        
        print("📦 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # List all created tables
        table_names = list(Base.metadata.tables.keys())
        print(f"✅ Database initialized successfully!")
        print(f"📊 Created {len(table_names)} tables:")
        for table_name in sorted(table_names):
            print(f"   - {table_name}")
        
    except ImportError as e:
        print(f"⚠️  Warning: Could not import all models: {e}")
        print("   Tables will be created when models are defined.")
        Base.metadata.create_all(bind=engine)
        print("✅ Database structure initialized (empty schema)")

def drop_all_tables():
    """
    Drop all tables from the database.
    WARNING: This will delete all data!
    
    Used for testing and demo reset.
    """
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped")

def get_table_info():
    """
    Get information about all tables in the database.
    
    Returns:
        dict: Table names and their column information
    """
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    table_info = {}
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        table_info[table_name] = {
            'columns': [col['name'] for col in columns],
            'column_count': len(columns)
        }
    
    return table_info

if __name__ == "__main__":
    """
    Test database initialization
    Run this script directly to initialize the database:
    python backend/database.py
    """
    print("=" * 60)
    print("MAHALO Database Initialization")
    print("=" * 60)
    print()
    
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Database Path: {settings.get_database_path()}")
    print()
    
    # Initialize database
    init_db()
    print()
    
    # Show table information
    print("📋 Table Information:")
    table_info = get_table_info()
    if table_info:
        for table_name, info in sorted(table_info.items()):
            print(f"   {table_name}: {info['column_count']} columns")
    else:
        print("   No tables found (models not yet defined)")
    
    print()
    print("✅ Database initialization complete!")
    print("=" * 60)
Test Database Module
python backend/database.py
Expected Output:

============================================================
MAHALO Database Initialization
============================================================

Database URL: sqlite:///mahalo.db
Database Path: /path/to/mahalo/mahalo.db

⚠️  Warning: Could not import all models: No module named 'backend.models.jira_models'
   Tables will be created when models are defined.
✅ Database structure initialized (empty schema)

📋 Table Information:
   No tables found (models not yet defined)

✅ Database initialization complete!
============================================================
Note: This is expected since we haven't created the models yet. They will be created in the next tasks.

Acceptance Criteria:

✅ backend/database.py created
✅ SQLAlchemy engine configured
✅ Session factory created
✅ init_db() function defined
✅ Script runs without errors
Mark Complete: ⬜ → ✅

Task 0.12: Create JIRA Data Models ⬜
Instruction to Coding Assistant: Create SQLAlchemy models for JIRA (users, stories, bugs, sprints).

Create backend/models/jira_models.py
"""
JIRA Data Models
SQLAlchemy models for JIRA users, stories, bugs, and sprints
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class JiraUser(Base):
    """JIRA User/Team Member"""
    __tablename__ = "jira_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    role = Column(String(50), default="developer")  # developer, pm, qa, executive
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    assigned_stories = relationship(
        "JiraStory",
        foreign_keys="JiraStory.assignee_id",
        back_populates="assignee"
    )
    reported_stories = relationship(
        "JiraStory",
        foreign_keys="JiraStory.reporter_id",
        back_populates="reporter"
    )
    assigned_bugs = relationship(
        "JiraBug",
        foreign_keys="JiraBug.assignee_id",
        back_populates="assignee"
    )
    reported_bugs = relationship(
        "JiraBug",
        foreign_keys="JiraBug.reporter_id",
        back_populates="reporter"
    )
    
    def __repr__(self):
        return f"<JiraUser(username='{self.username}', role='{self.role}')>"

class JiraStory(Base):
    """JIRA User Story"""
    __tablename__ = "jira_stories"
    
    id = Column(Integer, primary_key=True, index=True)
    story_key = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "STORY-123"
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False, default="Backlog")  # Backlog, Dev, UAT, Done
    assignee_id = Column(Integer, ForeignKey("jira_users.id"))
    reporter_id = Column(Integer, ForeignKey("jira_users.id"))
    story_points = Column(Integer, default=0)
    priority = Column(String(20), default="Medium")  # Low, Medium, High, Critical
    sprint = Column(String(50))  # Sprint name
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assignee = relationship(
        "JiraUser",
        foreign_keys=[assignee_id],
        back_populates="assigned_stories"
    )
    reporter = relationship(
        "JiraUser",
        foreign_keys=[reporter_id],
        back_populates="reported_stories"
    )
    bugs = relationship("JiraBug", back_populates="related_story")
    
    def __repr__(self):
        return f"<JiraStory(key='{self.story_key}', title='{self.title[:30]}...', status='{self.status}')>"

class JiraBug(Base):
    """JIRA Bug/Defect"""
    __tablename__ = "jira_bugs"
    
    id = Column(Integer, primary_key=True, index=True)
    bug_key = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "BUG-456"
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False, default="Open")  # Open, In Progress, Testing, Closed
    severity = Column(String(20), default="Medium")  # Low, Medium, High, Critical
    assignee_id = Column(Integer, ForeignKey("jira_users.id"))
    reporter_id = Column(Integer, ForeignKey("jira_users.id"))
    related_story_id = Column(Integer, ForeignKey("jira_stories.id"))
    servicenow_incident_id = Column(String(20))  # Cross-tool correlation
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assignee = relationship(
        "JiraUser",
        foreign_keys=[assignee_id],
        back_populates="assigned_bugs"
    )
    reporter = relationship(
        "JiraUser",
        foreign_keys=[reporter_id],
        back_populates="reported_bugs"
    )
    related_story = relationship("JiraStory", back_populates="bugs")
    
    def __repr__(self):
        return f"<JiraBug(key='{self.bug_key}', severity='{self.severity}', status='{self.status}')>"

class JiraSprint(Base):
    """JIRA Sprint"""
    __tablename__ = "jira_sprints"
    
    id = Column(Integer, primary_key=True, index=True)
    sprint_name = Column(String(50), unique=True, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_points = Column(Integer, default=0)
    completed_points = Column(Integer, default=0)
    status = Column(String(20), default="Active")  # Planning, Active, Completed
    
    def __repr__(self):
        return f"<JiraSprint(name='{self.sprint_name}', status='{self.status}')>"
Test JIRA Models
python -c "from backend.models.jira_models import JiraUser, JiraStory, JiraBug, JiraSprint; print('✅ JIRA models imported successfully')"
Acceptance Criteria:

✅ All 4 JIRA models defined (User, Story, Bug, Sprint)
✅ Relationships configured correctly
✅ Foreign keys defined
✅ Indexes on key fields
✅ Models import without errors
Mark Complete: ⬜ → ✅

Task 0.13: Create ServiceNow Data Models ⬜
Instruction to Coding Assistant: Create SQLAlchemy model for ServiceNow incidents.

Create backend/models/servicenow_models.py
"""
ServiceNow Data Models
SQLAlchemy models for ServiceNow incidents
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from backend.database import Base

class ServiceNowIncident(Base):
    """ServiceNow Incident"""
    __tablename__ = "servicenow_incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_number = Column(String(20), unique=True, nullable=False, index=True)  # e.g., "INC0001234"
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False, default="New")  # New, In Progress, Resolved, Closed
    priority = Column(String(20), default="Medium")  # Low, Medium, High, Critical
    category = Column(String(50))  # Infrastructure, Application, Network, etc.
    assigned_to = Column(String(100))
    reported_by = Column(String(100))
    jira_bug_key = Column(String(20))  # Cross-tool correlation to JIRA
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<ServiceNowIncident(number='{self.incident_number}', priority='{self.priority}', status='{self.status}')>"
Test ServiceNow Models
python -c "from backend.models.servicenow_models import ServiceNowIncident; print('✅ ServiceNow models imported successfully')"
Acceptance Criteria:

✅ ServiceNowIncident model defined
✅ Cross-tool correlation field (jira_bug_key) included
✅ Model imports without errors
Mark Complete: ⬜ → ✅

Task 0.14: Create Splunk Data Models ⬜
Instruction to Coding Assistant: Create SQLAlchemy model for Splunk logs with indexing.

Create backend/models/splunk_models.py
"""
Splunk Data Models
SQLAlchemy models for Splunk logs
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from datetime import datetime
from backend.database import Base
import json

class SplunkLog(Base):
    """Splunk Log Entry"""
    __tablename__ = "splunk_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    log_level = Column(String(20), nullable=False, index=True)  # DEBUG, INFO, WARN, ERROR, FATAL
    service = Column(String(100), nullable=False, index=True)  # Service name
    message = Column(Text, nullable=False)
    host = Column(String(100))
    environment = Column(String(20))  # dev, uat, prod
    correlation_id = Column(String(100))  # For request tracing
    jira_bug_key = Column(String(20))  # Cross-tool correlation to JIRA
    incident_number = Column(String(20))  # Cross-tool correlation to ServiceNow
    metadata = Column(Text)  # JSON stored as text (SQLite doesn't have native JSON)
    
    # Create composite indexes for common queries
    __table_args__ = (
        Index('idx_splunk_service_level', 'service', 'log_level'),
        Index('idx_splunk_timestamp_service', 'timestamp', 'service'),
    )
    
    def set_metadata(self, data: dict):
        """Store dictionary as JSON string"""
        if data:
            self.metadata = json.dumps(data)
        else:
            self.metadata = None
    
    def get_metadata(self) -> dict:
        """Parse JSON string to dictionary"""
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def __repr__(self):
        return f"<SplunkLog(level='{self.log_level}', service='{self.service}', time='{self.timestamp}')>"
Test Splunk Models
python -c "from backend.models.splunk_models import SplunkLog; print('✅ Splunk models imported successfully')"
Acceptance Criteria:

✅ SplunkLog model defined with metadata field
✅ Composite indexes for performance
✅ Cross-tool correlation fields included
✅ Helper methods for JSON metadata
✅ Model imports without errors
Mark Complete: ⬜ → ✅

Task 0.15: Update Models init.py ⬜
Instruction to Coding Assistant: Create models package initialization to export all models.

Create backend/models/init.py
"""
MAHALO Data Models Package
Exports all SQLAlchemy models for easy import
"""
from backend.models.jira_models import (
    JiraUser,
    JiraStory,
    JiraBug,
    JiraSprint
)
from backend.models.servicenow_models import (
    ServiceNowIncident
)
from backend.models.splunk_models import (
    SplunkLog
)

# Export all models
__all__ = [
    # JIRA Models
    "JiraUser",
    "JiraStory",
    "JiraBug",
    "JiraSprint",
    # ServiceNow Models
    "ServiceNowIncident",
    # Splunk Models
    "SplunkLog",
]
Test Models Package
python -c "from backend.models import JiraUser, JiraStory, JiraBug, JiraSprint, ServiceNowIncident, SplunkLog; print('✅ All models imported successfully from package')"
Acceptance Criteria:

✅ init.py exports all models
✅ All models can be imported from backend.models
✅ No import errors
Mark Complete: ⬜ → ✅

Task 0.16: Initialize Database with All Tables ⬜
Instruction to Coding Assistant: Run database initialization to create all tables.

Create Tables
python backend/database.py
Expected Output:

============================================================
MAHALO Database Initialization
============================================================

Database URL: sqlite:///mahalo.db
Database Path: /path/to/mahalo/mahalo.db

📦 Creating database tables...
✅ Database initialized successfully!
📊 Created 6 tables:
   - jira_bugs
   - jira_sprints
   - jira_stories
   - jira_users
   - servicenow_incidents
   - splunk_logs

📋 Table Information:
   jira_bugs: 11 columns
   jira_sprints: 7 columns
   jira_stories: 12 columns
   jira_users: 6 columns
   servicenow_incidents: 12 columns
   splunk_logs: 12 columns

✅ Database initialization complete!
============================================================
Verify Database File Created
ls -lh mahalo.db
Inspect Tables (Optional)
sqlite3 mahalo.db ".tables"
Expected Output:

jira_bugs            jira_users           splunk_logs
jira_sprints         servicenow_incidents
jira_stories
Check Table Schema (Optional)
sqlite3 mahalo.db ".schema jira_stories"
Acceptance Criteria:

✅ mahalo.db file created
✅ All 6 tables created successfully
✅ No errors during table creation
✅ Tables visible in SQLite
Mark Complete: ⬜ → ✅

Task 0.17: Create Documentation Folder Structure ⬜
Instruction to Coding Assistant: Copy planning documents to docs folder.

Copy MAHALO_PLAN.md
# If you have MAHALO_PLAN.md already downloaded, copy it:
cp /path/to/downloaded/MAHALO_PLAN.md docs/

# Or create a placeholder
cat > docs/MAHALO_PLAN.md << 'EOF'
# MAHALO - Architecture & Planning Document
(Copy the full MAHALO_PLAN.md content here)
EOF
Create Placeholder for Other Docs
touch docs/PHASE_1_MOCK_APIS.md
touch docs/PHASE_2_MCP_SERVERS.md
touch docs/PHASE_3_AI_AGENTS.md
touch docs/PHASE_4_UI_INTEGRATION.md
touch docs/PHASE_5_DOCUMENTATION.md
touch docs/API_DOCUMENTATION.md
touch docs/SETUP_GUIDE.md
touch docs/DEMO_SCRIPT.md
Acceptance Criteria:

✅ docs/ folder contains plan document
✅ Placeholder files for future phases created
Mark Complete: ⬜ → ✅

Task 0.18: Initialize Git Repository (Optional) ⬜
Instruction to Coding Assistant: Initialize git repository for version control.

Initialize Git
git init
Create Initial Commit
git add .
git commit -m "Initial project setup - Phase 0 complete"
Verify Git Status
git status
git log --oneline
Acceptance Criteria:

✅ Git repository initialized
✅ Initial commit created
✅ .gitignore working (no .env or *.db files tracked)
Mark Complete: ⬜ → ✅ (Optional)

✅ Phase 0 Validation Checklist
Before proceeding to Phase 1, verify all tasks are complete:

Project Structure
 All directories created
 All placeholder files created
 Scripts are executable
Python Environment
 Virtual environment created and activated
 All dependencies installed from requirements.txt
 No installation errors
Configuration
 .env.example created
 .env file created (copy of .env.example)
 backend/config.py loads settings correctly
 All ports configured (5001-5003, 6001-6003, 8000, 3000)
Database
 backend/database.py created
 All 6 data models created (jira_models, servicenow_models, splunk_models)
 mahalo.db file created
 All 6 tables exist in database
 Can query database without errors
Documentation
 README.md created
 .gitignore created
 docs/ folder structure ready
Validation Commands
# 1. Check Python environment
which python
python --version

# 2. Check dependencies
pip list | grep fastapi
pip list | grep sqlalchemy

# 3. Test configuration
python backend/config.py

# 4. Test database
python backend/database.py

# 5. Check database tables
sqlite3 mahalo.db ".tables"

# 6. Test model imports
python -c "from backend.models import JiraUser, ServiceNowIncident, SplunkLog; print('✅ All models OK')"
All commands should execute without errors.

🎉 Phase 0 Complete!
What We've Accomplished
✅ Complete project structure created
✅ Python environment configured
✅ Database models defined
✅ SQLite database initialized with all tables
✅ Configuration management setup
✅ Basic documentation created

What's Next: Phase 1 - Build Mock APIs
In Phase 1, you will:

Build JIRA API service layer
Build JIRA FastAPI application
Create JIRA seed data
Build ServiceNow API
Build Splunk API
Add automated tests
Create data reset utility
Ready to Proceed?
# Verify Phase 0 is complete
python backend/database.py
sqlite3 mahalo.db ".tables"
If you see all 6 tables listed, you're ready for Phase 1! 🚀

END OF PHASE 0

Perfect! I've created the PHASE_0_PROJECT_SETUP.md document as a single file. You can now:

Copy the entire content directly from the artifact above
Download it using the download button
Save it to your mahalo/docs/ folder
This covers:

✅ Complete project structure setup
✅ Python environment configuration
✅ Database models (JIRA, ServiceNow, Splunk)
✅ Database initialization
✅ Configuration management
✅ Documentation setup