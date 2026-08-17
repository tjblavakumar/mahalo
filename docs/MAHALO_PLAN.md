# MAHALO - AI Harness for Software Development Lifecycle ## Product Vision & Architecture Plan
Version: 1.0
Date: January 2025
Status: Planning & Design Phase

🎯 Executive Summary
MAHALO (Multi-Agent Harness for Agile Lifecycle Orchestration) is an AI-powered unified context layer that orchestrates SDLC tools (JIRA, ServiceNow, Splunk) through intelligent agents using the Model Context Protocol (MCP). It provides role-based chat interfaces for Product Managers, Developers, QA, and Executives to interact with all SDLC tools through natural language.

Proof of Concept Goals
Demonstrate AI agent orchestration across SDLC tools
Showcase MCP for tool integration and standardization
Provide role-based intelligent assistance
Enable cross-tool correlation and context awareness
Prove viability of chat-first SDLC interface
Key Value Proposition
Unified Interface: Single chat interface for all SDLC tools
Context Awareness: AI understands relationships across tools
Role-Based: Tailored experience for each user persona
Natural Language: No need to learn tool-specific interfaces
Time Saving: Reduce context switching and tool navigation

Cross-Platform Local Execution
MAHALO is designed to run locally on both Windows and Linux environments. The architecture and service layout remain the same across platforms, but the execution scripts are split by OS so the workflow is easy to use on either developer machine.

Windows Local Development
- Use batch scripts under scripts\
- Virtual environment activation: venv\Scripts\activate
- Common commands: start_all.bat, stop_all.bat, reset_demo.bat, run_tests.bat
- Best for local dev on Windows 10/11 workstations

Linux Local Development
- Use shell scripts under scripts/
- Virtual environment activation: source venv/bin/activate
- Common commands: ./start_all.sh, ./stop_all.sh, ./reset_demo.sh, ./run_tests.sh
- Best for local dev on Linux distributions and WSL2 environments

This approach keeps the MAHALO services, ports, and demo flow consistent while allowing each OS to use the native script format expected by that environment.

┌─────────────────────────────────────────────────────────────────┐
│                     MAHALO UI (React)                            │
│               Chat Interface + Persona Selector                  │
│                    http://localhost:3000                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Main API Gateway (FastAPI)                      │
│                    http://localhost:8000                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              Orchestrator Agent (LiteLLM + Logic)                │
│         • Intent Classification                                  │
│         • Agent Routing                                          │
│         • Response Aggregation                                   │
│         • Conversation Management                                │
└──────┬───────────────┬───────────────┬──────────────────────────┘
       │               │               │
       ▼               ▼               ▼
┌────────────┐   ┌────────────┐   ┌────────────┐
│   JIRA     │   │ ServiceNow │   │   Splunk   │
│   Agent    │   │   Agent    │   │   Agent    │
│            │   │            │   │            │
│ (LiteLLM)  │   │ (LiteLLM)  │   │ (LiteLLM)  │
└─────┬──────┘   └─────┬──────┘   └─────┬──────┘
      │                │                │
      │ MCP Protocol   │ MCP Protocol   │ MCP Protocol
      ▼                ▼                ▼
┌────────────┐   ┌────────────┐   ┌────────────┐
│   JIRA     │   │ ServiceNow │   │   Splunk   │
│    MCP     │   │    MCP     │   │    MCP     │
│   Server   │   │   Server   │   │   Server   │
│   :6001    │   │   :6002    │   │   :6003    │
└─────┬──────┘   └─────┬──────┘   └─────┬──────┘
      │                │                │
      │ HTTP/REST      │ HTTP/REST      │ HTTP/REST
      ▼                ▼                ▼
┌────────────┐   ┌────────────┐   ┌────────────┐
│   JIRA     │   │ ServiceNow │   │   Splunk   │
│  Mock API  │   │  Mock API  │   │  Mock API  │
│  (FastAPI) │   │  (FastAPI) │   │  (FastAPI) │
│   :5001    │   │   :5002    │   │   :5003    │
└─────┬──────┘   └─────┬──────┘   └─────┬──────┘
      │                │                │
      └────────────────┴────────────────┘
                       │
                       ▼
               ┌───────────────┐
               │  SQLite DB    │
               │  mahalo.db    │
               └───────────────┘


Component Descriptions
1. Frontend (React)
Single-page application
Chat-first interface
Persona selector (Executive, PM, Developer, QA)
Real-time message streaming
Admin panel for demo reset
2. Main API Gateway (FastAPI)
Central entry point for UI
Routes chat requests to Orchestrator
Handles authentication (simplified for POC)
Provides admin endpoints
3. Orchestrator Agent
Analyzes user intent using LLM
Routes to specialized agents
Coordinates multi-agent workflows
Aggregates responses
Maintains conversation context
4. Specialized Agents
JIRA Agent: User stories, bugs, sprints, velocity
ServiceNow Agent: Incidents, tickets
Splunk Agent: Logs, errors, monitoring
Each uses LiteLLM for natural language understanding
Each calls tools via MCP
5. MCP Servers
Expose tool capabilities as MCP-compliant services
Translate MCP calls to tool-specific API calls
Handle tool authentication and error handling
Provide resource discovery
6. Mock Tool APIs
Simplified implementations of JIRA, ServiceNow, Splunk
RESTful endpoints
SQLite database backend
Seed data for realistic demos
7. SQLite Database
Single file database (mahalo.db)
All tool data in one place
Easy to reset for demos
No external database dependencies


mahalo/
│
├── README.md                          # Project overview and quick start
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variable template
├── .env                              # Actual environment variables (gitignored)
├── .gitignore                        # Git ignore rules
│
├── docs/                             # All documentation
│   ├── MAHALO_PLAN.md               # This file - architecture & vision
│   ├── PHASE_0_PROJECT_SETUP.md     # Phase 0 execution steps
│   ├── PHASE_1_MOCK_APIS.md         # Phase 1 execution steps
│   ├── PHASE_2_MCP_SERVERS.md       # Phase 2 execution steps
│   ├── PHASE_3_AI_AGENTS.md         # Phase 3 execution steps
│   ├── PHASE_4_UI_INTEGRATION.md    # Phase 4 execution steps
│   ├── PHASE_5_DOCUMENTATION.md     # Phase 5 execution steps
│   ├── API_DOCUMENTATION.md         # API reference
│   ├── SETUP_GUIDE.md               # Installation instructions
│   ├── DEMO_SCRIPT.md               # Demo walkthrough
│   └── architecture_diagram.png     # Visual architecture (optional)
│
├── backend/                          # All Python backend code
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── database.py                  # Database connection & initialization
│   │
│   ├── models/                      # SQLAlchemy data models
│   │   ├── __init__.py
│   │   ├── jira_models.py          # JIRA tables (users, stories, bugs, sprints)
│   │   ├── servicenow_models.py    # ServiceNow tables (incidents)
│   │   └── splunk_models.py        # Splunk tables (logs)
│   │
│   ├── jira/                        # JIRA mock service
│   │   ├── __init__.py
│   │   ├── app.py                  # FastAPI app (port 5001)
│   │   ├── routes.py               # API endpoints
│   │   ├── service.py              # Business logic layer
│   │   └── seed_data.py            # Demo data population
│   │
│   ├── servicenow/                  # ServiceNow mock service
│   │   ├── __init__.py
│   │   ├── app.py                  # FastAPI app (port 5002)
│   │   ├── routes.py
│   │   ├── service.py
│   │   └── seed_data.py
│   │
│   ├── splunk/                      # Splunk mock service
│   │   ├── __init__.py
│   │   ├── app.py                  # FastAPI app (port 5003)
│   │   ├── routes.py
│   │   ├── service.py
│   │   └── seed_data.py
│   │
│   └── utils/                       # Shared utilities
│       ├── __init__.py
│       ├── reset_data.py           # Reset all demo data
│       └── validators.py           # Input validation helpers
│
├── mcp_servers/                     # MCP server implementations
│   ├── jira_mcp/
│   │   ├── __init__.py
│   │   ├── server.py               # MCP server for JIRA (port 6001)
│   │   ├── tools.py                # Tool definitions
│   │   └── resources.py            # Resource definitions
│   │
│   ├── servicenow_mcp/
│   │   ├── __init__.py
│   │   ├── server.py               # MCP server for ServiceNow (port 6002)
│   │   ├── tools.py
│   │   └── resources.py
│   │
│   └── splunk_mcp/
│       ├── __init__.py
│       ├── server.py               # MCP server for Splunk (port 6003)
│       ├── tools.py
│       └── resources.py
│
├── agents/                          # AI agent implementations
│   ├── __init__.py
│   ├── orchestrator.py             # Main orchestrator agent
│   ├── jira_agent.py               # JIRA specialized agent
│   ├── servicenow_agent.py         # ServiceNow specialized agent
│   ├── splunk_agent.py             # Splunk specialized agent
│   ├── context_manager.py          # Cross-tool correlation logic
│   │
│   └── prompts/                    # System prompts for agents
│       ├── orchestrator_prompt.txt
│       ├── jira_agent_prompt.txt
│       ├── servicenow_agent_prompt.txt
│       └── splunk_agent_prompt.txt
│
├── api/                             # Main API gateway
│   ├── __init__.py
│   ├── main.py                     # Main FastAPI app (port 8000)
│   ├── middleware.py               # Middleware (CORS, logging, etc.)
│   │
│   └── routes/
│       ├── __init__.py
│       ├── chat.py                 # Chat endpoints for UI
│       └── admin.py                # Admin endpoints (reset, status)
│
├── frontend/                        # React application
│   ├── package.json
│   ├── package-lock.json
│   ├── .env                        # Frontend environment variables
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   └── src/
│       ├── App.js                  # Main React component
│       ├── index.js                # React entry point
│       │
│       ├── components/             # React components
│       │   ├── PersonaSelector.js  # User persona dropdown
│       │   ├── ChatInterface.js    # Main chat UI
│       │   ├── MessageBubble.js    # Individual message display
│       │   └── AdminPanel.js       # Admin controls
│       │
│       ├── services/               # API clients
│       │   └── api.js              # Axios API wrapper
│       │
│       ├── styles/                 # CSS styles
│       │   └── App.css             # Main stylesheet
│       │
│       └── utils/                  # Helper functions
│           └── helpers.js
│
├── tests/                           # All test files
│   ├── __init__.py
│   ├── test_jira_api.py            # JIRA API tests
│   ├── test_servicenow_api.py      # ServiceNow API tests
│   ├── test_splunk_api.py          # Splunk API tests
│   ├── test_mcp_servers.py         # MCP server tests
│   ├── test_agents.py              # Agent tests
│   └── test_integration.py         # End-to-end tests
│
└── scripts/                         # Helper scripts
    ├── start_all.sh                # Start all services
    ├── stop_all.sh                 # Stop all services
    ├── reset_demo.sh               # Reset demo data
    └── run_tests.sh                # Run all tests


🗄️ Data Models & Database Schema
Overview
Database: SQLite (single file: mahalo.db)
ORM: SQLAlchemy
Total Tables: 6
JIRA: 4 tables (users, stories, bugs, sprints)
ServiceNow: 1 table (incidents)
Splunk: 1 table (logs)


JIRA Data Models
1. jira_users
Purpose: Store team members who work on stories and bugs

Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY	Auto-increment ID
username	TEXT	UNIQUE, NOT NULL	Unique username (e.g., "alice_dev")
full_name	TEXT	NOT NULL	Display name
email	TEXT		Email address
role	TEXT	DEFAULT 'developer'	Role: developer, pm, qa, executive
created_at	TIMESTAMP	DEFAULT NOW	Record creation time
Relationships:

One user can have many assigned stories
One user can have many reported stories
One user can have many assigned bugs
One user can have many reported bugs

2. jira_stories
Purpose: User stories in JIRA

Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY	Auto-increment ID
story_key	TEXT	UNIQUE, NOT NULL	Story identifier (e.g., "STORY-123")
title	TEXT	NOT NULL	Story title
description	TEXT		Detailed description
status	TEXT	NOT NULL	Backlog / Dev / UAT / Done
assignee_id	INTEGER	FOREIGN KEY	References jira_users(id)
reporter_id	INTEGER	FOREIGN KEY	References jira_users(id)
story_points	INTEGER	DEFAULT 0	Complexity/effort points
priority	TEXT	DEFAULT 'Medium'	Low / Medium / High / Critical
sprint	TEXT		Sprint name (e.g., "Sprint 23")
created_at	TIMESTAMP	DEFAULT NOW	Creation timestamp
updated_at	TIMESTAMP	DEFAULT NOW	Last update timestamp

Status Workflow:

Backlog → Dev → UAT → Done
Indexes:

story_key (unique index)
assignee_id (for quick lookups)
status (for filtering)
sprint (for sprint queries)


3. jira_bugs
Purpose: Bug/defect tracking

Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY	Auto-increment ID
bug_key	TEXT	UNIQUE, NOT NULL	Bug identifier (e.g., "BUG-456")
title	TEXT	NOT NULL	Bug title
description	TEXT		Bug details
status	TEXT	NOT NULL	Open / In Progress / Testing / Closed
severity	TEXT	DEFAULT 'Medium'	Low / Medium / High / Critical
assignee_id	INTEGER	FOREIGN KEY	References jira_users(id)
reporter_id	INTEGER	FOREIGN KEY	References jira_users(id)
related_story_id	INTEGER	FOREIGN KEY	References jira_stories(id)
servicenow_incident_id	TEXT		Cross-tool link to ServiceNow
created_at	TIMESTAMP	DEFAULT NOW	Creation timestamp
updated_at	TIMESTAMP	DEFAULT NOW	Last update timestamp
Cross-Tool Correlation:

related_story_id: Links bug to original story
servicenow_incident_id: Links bug to production incident

4. jira_sprints
Purpose: Sprint tracking and velocity calculation

Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY	Auto-increment ID
sprint_name	TEXT	UNIQUE, NOT NULL	Sprint identifier
start_date	DATE		Sprint start date
end_date	DATE		Sprint end date
total_points	INTEGER	DEFAULT 0	Total story points planned
completed_points	INTEGER	DEFAULT 0	Completed story points
status	TEXT	DEFAULT 'Active'	Planning / Active / Completed
Velocity Calculation:

Average Velocity = Sum(completed_points) / Number of Sprints


ServiceNow Data Models
servicenow_incidents
Purpose: IT incident management

Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY	Auto-increment ID
incident_number	TEXT	UNIQUE, NOT NULL	Incident ID (e.g., "INC0001234")
title	TEXT	NOT NULL	Incident title
description	TEXT		Incident details
status	TEXT	NOT NULL	New / In Progress / Resolved / Closed
priority	TEXT	DEFAULT 'Medium'	Low / Medium / High / Critical
category	TEXT		Infrastructure / Application / Network
assigned_to	TEXT		Assigned team member name
reported_by	TEXT		Reporter name
jira_bug_key	TEXT		Cross-tool link to JIRA bug
created_at	TIMESTAMP	DEFAULT NOW	Creation timestamp
updated_at	TIMESTAMP	DEFAULT NOW	Last update timestamp
resolved_at	TIMESTAMP		Resolution timestamp



Cross-Tool Correlation:

jira_bug_key: Links incident to JIRA bug for tracking
Typical Workflow:

New → In Progress → Resolved → Closed

Splunk Data Models
splunk_logs
Purpose: Application log storage and search

Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY	Auto-increment ID
timestamp	TIMESTAMP	NOT NULL, INDEXED	Log entry time
log_level	TEXT	NOT NULL, INDEXED	DEBUG / INFO / WARN / ERROR / FATAL
service	TEXT	NOT NULL, INDEXED	Service name (e.g., "login-service")
message	TEXT	NOT NULL	Log message content
host	TEXT		Server hostname
environment	TEXT		dev / uat / prod
correlation_id	TEXT		Trace ID for request tracking
jira_bug_key	TEXT		Link to related JIRA bug
incident_number	TEXT		Link to related ServiceNow incident
metadata	TEXT (JSON)		Additional structured data as JSON


Indexes:

timestamp (for time-range queries)
service + log_level (composite index)
timestamp + service (composite index)
Cross-Tool Correlation:

jira_bug_key: Links logs to bugs
incident_number: Links logs to incidents
Search Capabilities:

Time-range queries
Service filtering
Log level filtering
Full-text search on message
Environment filtering



Technology Stack
Backend Technologies
Component	Technology	Version	Purpose
Framework	FastAPI	0.109.0+	REST API framework
Language	Python	3.10+	Backend language
Database	SQLite	3.x	Embedded database
ORM	SQLAlchemy	2.0+	Database abstraction
Testing	pytest	7.4+	Unit/integration tests
HTTP Client	httpx	0.26+	Async HTTP requests
MCP	Python MCP SDK	0.1+	Model Context Protocol
AI/LLM	LiteLLM	1.17+	Unified LLM interface
Env Management	python-dotenv	1.0+	Environment variables

Frontend Technologies
Component	Technology	Version	Purpose
Framework	React	18+	UI framework
Language	JavaScript	ES6+	Frontend language
HTTP Client	Axios	1.6+	API requests
Styling	CSS3	-	Custom styles
Package Manager	npm	9+	Dependency management


Development Tools
Tool	Purpose
Git	Version control
VS Code	Recommended IDE
Black	Python code formatting
Flake8	Python linting
ESLint	JavaScript linting
Postman/curl	API testing

Deployment (POC)
Aspect	Approach
Environment	Local development
Process Management	Manual (separate terminals)
Port Management	Fixed ports (5001-5003, 6001-6003, 8000, 3000)
Database	File-based SQLite
Logging	Console output

🤖 AI Agent Architecture
Agent Design Philosophy
Specialized Knowledge: Each agent knows one domain deeply
Clear Boundaries: No overlap in responsibilities
MCP-First: All tool interactions through MCP
Context-Aware: Share context through ContextManager
LLM-Powered: Use LiteLLM for natural language understanding
1. Orchestrator Agent
Role: Traffic cop and coordinator

Responsibilities:

Receive user messages from UI
Parse user persona and intent
Route to appropriate specialized agent(s)
Coordinate multi-agent workflows
Aggregate responses
Maintain conversation history
Key Capabilities:

Intent classification (JIRA vs ServiceNow vs Splunk query)
Multi-agent orchestration
Response synthesis
Error handling and fallback

LLM Prompting Strategy:

System Prompt:
- You are MAHALO Orchestrator
- Available agents: JIRA, ServiceNow, Splunk
- Analyze user query and determine which agent(s) to call
- For complex queries, coordinate multiple agents
- Always consider user persona (Executive/PM/Dev/QA)
Example Flow:

User: "Show me sprint status"
↓
Orchestrator analyzes → Determines: JIRA Agent needed
↓
Routes to JIRA Agent
↓
JIRA Agent returns sprint data
↓
Orchestrator formats response
↓
Returns to user

2. JIRA Agent
Role: JIRA domain expert

Responsibilities:

Create/read/update user stories
Create/track bugs
Search for duplicate stories
Calculate sprint metrics
Retrieve team velocity
Get user assignments
MCP Tools Available:

create_user_story
search_stories
get_story_by_key
update_story_status
create_bug
get_bugs_by_status
get_bugs_by_severity
get_sprint_summary
calculate_team_velocity
get_user_tasks

LLM Prompting Strategy:
System Prompt:
- You are JIRA Agent, expert in user stories, bugs, sprints
- Always check for duplicate stories before creating
- Help users refine story descriptions
- Provide story point estimates based on similar stories
- Be data-driven: include metrics and numbers

Key Workflow: Create Story
1. User asks: "Create story for OAuth login"
2. Agent searches for duplicates
3. If found → Alert user, show similar stories
4. If not found → Help refine description
5. Suggest story points based on complexity
6. Create story via MCP tool
7. Return created story details


3. ServiceNow Agent
Role: Incident management expert

Responsibilities:

Create/update incidents
Query incidents by status/priority
Link incidents to JIRA bugs
Provide incident summaries
MCP Tools Available:

create_incident
get_incident_by_number
update_incident_status
search_incidents
link_to_jira_bug
get_incidents_by_priority

LLM Prompting Strategy:

System Prompt:
- You are ServiceNow Agent, expert in incident management
- Always capture severity and priority
- Link incidents to JIRA bugs when appropriate
- Provide clear incident status updates

4. Splunk Agent
Role: Log analysis expert

Responsibilities:

Search logs by service/level/time
Identify error patterns
Correlate logs with bugs/incidents
Provide log summaries
MCP Tools Available:

search_logs
get_logs_by_service
get_error_logs
get_logs_by_timerange
correlate_logs_with_bug
LLM Prompting Strategy:

System Prompt:
- You are Splunk Agent, expert in log analysis
- Help users find relevant logs quickly
- Identify error patterns and anomalies
- Correlate logs with JIRA bugs and ServiceNow incidents

5. Context Manager
Role: Cross-tool correlation and memory

Responsibilities:

Store correlations between tools
Link bugs ↔ incidents ↔ logs
Provide unified context
Maintain relationship graph
Data Structure:

{
  "correlation_id": "CORR-2025-01-15-001",
  "jira_bug": "BUG-789",
  "servicenow_incident": "INC0001234",
  "splunk_logs": [12345, 12346, 12347],
  "created_at": "2025-01-15T14:30:00Z",
  "context": "Login service database timeout"
}

Key Operations:

link_bug_to_incident(bug_key, incident_number)
link_logs_to_bug(bug_key, log_ids)
get_full_context(bug_key)
get_related_items(item_id, item_type)

👥 User Personas & Key Workflows
Persona 1: Executive
Profile:

Needs high-level visibility
Wants metrics and KPIs
Limited technical detail
Focus on team performance
Primary Use Cases:

Sprint Status Overview

Query: "Show me the current sprint status"
Expected: Stories by status, bug count, velocity, blockers
Team Velocity

Query: "How is the team performing?"
Expected: Velocity trends, capacity utilization

Production Health

Query: "Any critical production issues?"
Expected: Critical bugs, open incidents, error rates
Sample Interaction:

Executive: "Show me sprint status"

MAHALO: 
📊 Sprint 23 Status:
✅ Completed: 12 stories (34 points)
🔨 In Development: 5 stories (13 points)
🧪 In UAT: 3 stories (8 points)
📋 Backlog: 8 stories (21 points)
🐛 Active Bugs: 7 (3 Critical, 4 Medium)
📈 Team Velocity: 34 points/sprint (↑ from 32)

Persona 2: Product Manager
Profile:

Creates and manages user stories
Prioritizes backlog
Refines requirements
Tracks feature progress
Primary Use Cases:

Create User Story

Query: "Create story for implementing 2FA"
Expected: Duplicate check, refinement help, creation
Search Stories

Query: "Show all stories related to authentication"
Expected: Filtered list of relevant stories
Prioritize Backlog

Query: "What stories should we prioritize?"
Expected: Recommendations based on dependencies and value

Sample Interaction:

PM: "Create user story for OAuth login"

MAHALO:
🔍 Checking for duplicates...
Found 1 similar story:
- STORY-123: "Implement OAuth 2.0 authentication" (Done)

This looks like an extension. Let me help refine:

📝 Suggested Story:
Title: Extend OAuth to support GitHub provider
Description:
As a user, I want to log in using GitHub OAuth
so that I can use my existing GitHub credentials.

Acceptance Criteria:
- Add GitHub as OAuth provider
- Implement GitHub OAuth flow
- Store GitHub profile data
- Handle OAuth errors gracefully

Estimated Points: 5 (based on similar OAuth work)
Priority: Medium

Should I create this story? (Yes/Modify/Cancel)


Persona 3: Developer
Profile:

Wants to see assigned tasks
Needs technical context
Troubleshoots bugs
Tracks progress
Primary Use Cases:

View Assignments

Query: "Show my assigned tasks"
Expected: Prioritized list of stories and bugs
Get Task Details

Query: "Tell me about STORY-245"
Expected: Full story details, context, dependencies
Link Bug to Logs

Query: "Show logs for BUG-89"
Expected: Related error logs from Splunk

Sample Interaction:

Developer: "Show my assigned tasks"

MAHALO:
👨‍💻 Your Tasks (5 total):

🔥 High Priority:
- [STORY-245] Implement payment gateway (8 pts) - Dev
  Blocked by: API key from finance team
  
- [BUG-89] Fix Safari checkout crash (Critical) - Open
  Related to: STORY-240 (checkout flow)
  Incident: INC0001234
  💡 Recent error logs show JS exception

📌 Medium Priority:
- [STORY-251] Email notification service (5 pts) - Dev
- [STORY-203] Refactor auth module (3 pts) - UAT

📋 Low Priority:
- [BUG-102] Mobile UI alignment (Low) - Open

💡 Recommendation: Focus on BUG-89 first - it's blocking UAT


Persona 4: QA Engineer
Profile:

Tests features in UAT
Reports bugs
Verifies fixes
Tracks quality metrics
Primary Use Cases:

Report Bug

Query: "Report bug: Login fails on Safari"
Expected: Guided bug creation, linked to story
View Test Status

Query: "What's ready for testing?"
Expected: Stories in UAT status
Verify Bug Fix

Query: "Is BUG-89 fixed?"
Expected: Bug status, fix details, test instructions

Cross-Tool Correlation Strategy
Correlation Scenarios
Scenario 1: Production Incident → Bug → Logs
1. Production incident reported in ServiceNow (INC0001234)
   "Login service returning 500 errors"
   
2. QA creates bug in JIRA (BUG-789)
   Links to incident: servicenow_incident_id = "INC0001234"
   
3. Developer searches Splunk for related errors
   Finds ERROR logs with correlation
   Links logs to bug: jira_bug_key = "BUG-789"
   
4. MAHALO provides unified view:
   - Incident details
   - Bug tracking info
   - Related error logs
   - Timeline of events


cenario 2: Story → Bug → Incident
1. Developer working on STORY-240 (checkout feature)
   
2. Bug found during development (BUG-89)
   Links to story: related_story_id = 240
   
3. Bug escapes to production, incident created (INC0001235)
   Links to bug: jira_bug_key = "BUG-89"
   
4. MAHALO shows full context:
   - Original story requirements
   - Bug details and status
   - Production impact (incident)
   - Error logs showing root cause


   Context Manager Implementation
Data Structure:

{
  "correlations": {
    "CORR-001": {
      "jira_bug": "BUG-789",
      "servicenow_incident": "INC0001234",
      "splunk_logs": [12345, 12346, 12347],
      "jira_story": "STORY-240",
      "created_at": "2025-01-15T14:30:00Z",
      "summary": "Login service database timeout"
    }
  }
}
Operations:

Create correlation when bug links to incident
Add logs when searching by bug
Retrieve full context in one call
Display unified timeline

🧪 Testing Strategy
Test Pyramid
/\
          /  \
         /E2E \         End-to-End Tests (Manual)
        /______\        - Full workflow testing
       /        \       - Demo scenario validation
      / Integ.  \      Integration Tests (Automated)
     /___________\     - Agent → MCP → API
    /             \    
   /  Component   \   Component Tests (Automated)
  /________________\  - API endpoints
 /                  \ - Service layer logic
/____________________\
     Unit Tests        Unit Tests (Automated)
                      - Data models
                      - Utility functions



Phase 1: API Testing (Automated)
Scope: Backend mock APIs
Tools: pytest, httpx
Coverage Target: >80%

Test Cases:

✅ JIRA API: Create story, search stories, get sprint summary
✅ ServiceNow API: Create incident, link to bug
✅ Splunk API: Search logs, filter by service/level
✅ All CRUD operations
✅ Error handling
✅ Data validation
Phase 2: MCP Server Testing (Automated)
Scope: MCP servers
Tools: pytest, MCP client library

Test Cases:

✅ Tool registration
✅ Tool execution
✅ Resource exposure
✅ MCP protocol compliance
✅ Error propagation

Phase 3: Agent Testing (Automated + Manual)
Scope: AI agents
Tools: pytest, LLM mocking

Test Cases:

✅ Intent classification
✅ Agent routing
✅ MCP tool calling
✅ Response formatting
✅ Conversation context
✅ Manual: Natural language understanding
Phase 4: Integration Testing (Manual)
Scope: End-to-end workflows
Tools: Manual testing + UI

Test Cases:

✅ Executive workflow: Sprint status query
✅ PM workflow: Create story with duplicate check
✅ Developer workflow: View assigned tasks
✅ Cross-tool: Bug → Incident → Logs correlation
✅ UI responsiveness
✅ Error handling in UI

Demo Data Strategy
Demo Company: MahaloPay (FinTech Payment Processing Company)

Seed Data Requirements
JIRA:

Users: 5 (alice_dev, bob_pm, charlie_qa, diana_dev, eve_exec)
Sprint: "Sprint 23" (Active)
Stories: 20 total (FinTech-themed: payment processing, fraud detection, account reconciliation)
Done: 12 stories (34 points)
Dev: 5 stories (13 points)
UAT: 3 stories (8 points)
Backlog: 8 stories (21 points)
Bugs: 10 total (payment timeouts, balance errors, security issues)
Critical: 3
High: 2
Medium: 3
Low: 2
Velocity: Historical data for 3 sprints


ServiceNow:

Incidents: 8 total (payment service outages, transaction failures, API timeouts)
New: 2
In Progress: 3
Resolved: 2
Closed: 1
Correlation: 2 incidents linked to JIRA bugs

Splunk:

Logs: 1000+ entries
Time range: Last 7 days
Services: payment-service, fraud-detection, account-service, transaction-api
Levels: 50% INFO, 30% WARN, 15% ERROR, 5% FATAL
Environments: 60% prod, 25% uat, 15% dev
Correlation: Some ERROR logs linked to bugs (payment timeouts, database connection issues)

Reset Mechanism
# Windows
scripts\reset_demo.bat

# Unix/Mac
bash scripts/reset_demo.sh

# What it does:
1. Drop all tables
2. Recreate schema
3. Run seed data scripts
4. Verify data loaded correctly
5. Complete in < 5 seconds
Demo Scenarios (MahaloPay FinTech Context)
Scenario 1: Sprint Review (Executive)

Data needed:
- Sprint 23 with realistic payment processing metrics
- Mix of completed/in-progress payment and fraud detection stories
- Some bugs with different severities (payment timeouts, security issues)
- Historical velocity data


Scenario 2: Story Creation (PM)

Data needed:
- Existing story about "Stripe payment gateway integration"
- So duplicate detection can demonstrate
- Similar payment processing stories for point estimation

Scenario 3: Developer Workload (Developer)

Data needed:
- Payment processing stories assigned to "alice_dev"
- Mix of priorities
- Some bugs assigned to "alice_dev" (payment timeouts, transaction errors)
- One blocked story to show context (waiting on payment provider API keys)

Scenario 4: Incident Investigation (Cross-tool)

Data needed:
- ServiceNow incident INC0001234 "Payment service returning 500 errors"
- Linked JIRA bug BUG-789 "Payment timeout on high-value transactions"
- ERROR logs in Splunk showing database connection timeouts during payment processing
- Timeline should tell coherent story about payment processing failure

🚀 Demo Script (10-Minute Version)
Setup (Before Demo)
Reset data: `scripts\reset_demo.bat` (Windows) or `bash scripts/reset_demo.sh` (Unix/Mac)
Start all: `scripts\start_all.bat` (Windows) or `bash scripts/start_all.sh` (Unix/Mac)
Open browser: http://localhost:3000
Verify all services healthy (check each terminal window for errors)
Demo Flow
1. Introduction (1 min)

"MAHALO demonstrates AI-powered orchestration of SDLC tools for MahaloPay, a FinTech company.
Instead of switching between JIRA, ServiceNow, and Splunk,
users interact with all tools through natural language in one interface.
Our demo shows a payment processing team managing features, bugs, and incidents."

2. Executive Persona (2 min)

Action: Select "Executive" persona
Query: "Show me the current sprint status"

Show:
- Real-time data from JIRA
- Sprint metrics clearly displayed
- Bug counts by severity
- Velocity comparison to target

Key Point: Executive gets instant visibility without learning JIRA

Product Manager Persona (3 min)

Action: Select "Product Manager" persona
Query: "Create a user story for implementing Stripe payment gateway integration"

Show:
- AI checks for duplicate payment processing stories
- Helps refine description with best practices
- Suggests story points based on similar payment integration work
- Creates story in JIRA

Key Point: PM gets intelligent assistance for MahaloPay's payment features, not just data entry

Developer Persona (2 min)

Action: Select "Developer" persona
Query: "Show me my assigned tasks"

Show:
- Personalized task list
- Priority sorting
- Context about blockers
- Recommendations on what to work on

Key Point: Developer saves time, gets relevant context
5. Cross-Tool Correlation (2 min)

Action: Demonstrate unified context
Query: "Tell me about BUG-789"

Show:
- Bug details from JIRA: "Payment timeout on high-value transactions"
- Linked ServiceNow incident: INC0001234 "Payment service returning 500 errors"
- Related error logs from Splunk: Database connection timeouts during payment processing
- Complete timeline of events showing the payment processing failure

Key Point: MAHALO provides unified context across all tools for MahaloPay's payment incidents

🎯 Success Criteria
Technical Criteria
✅ All 3 mock tools run independently
✅ Each tool accessible via REST API
✅ Each tool wrapped with MCP server
✅ Agents interact successfully with MCP servers
✅ Orchestrator routes correctly
✅ UI displays responses in real-time
✅ All automated tests pass (>80% coverage)
✅ Demo scenarios work reliably
Functional Criteria
✅ Executive workflow: Sprint status works
✅ PM workflow: Story creation with duplicate check works
✅ Developer workflow: Task list works
✅ Cross-tool correlation works (bug → incident → logs)
✅ Data reset works
✅ System recoverable after errors

Demonstrability Criteria
✅ Can demo in < 10 minutes
✅ Demo runs smoothly without errors
✅ Can reset and re-run demo
✅ Impressive to stakeholders
✅ Documentation supports demo
Deliverables Checklist
✅ Working prototype
✅ Comprehensive documentation
✅ Automated tests
✅ Demo script
✅ Setup guide
✅ Architecture diagram
⚠️ Known Limitations (POC Scope)
Out of Scope
Authentication: No real auth, just persona dropdown
Multi-user: Single-user demo, no concurrency
Persistence: Conversation history not saved
Production: Not production-ready, local only
Real Tools: Mock APIs, not actual JIRA/ServiceNow/Splunk
Advanced AI: Basic LLM usage, not fine-tuned
Scalability: Not designed for scale
Security: No security hardening
Monitoring: No observability/logging infrastructure
CI/CD: No automated deployment
Known Issues
SQLite has concurrency limitations
MCP protocol still evolving
LLM responses can be inconsistent
No retry logic for failed API calls
Error messages could be more user-friendly

📚 Documentation Structure
For Users
README.md - Quick start, overview
SETUP_GUIDE.md - Installation instructions
DEMO_SCRIPT.md - How to demo MAHALO
For Developers
MAHALO_PLAN.md (this document) - Architecture
Phase Execution Docs - Step-by-step implementation
API_DOCUMENTATION.md - API reference
Architecture Diagram - Visual representation
For Stakeholders
Demo recording/screenshots
DEMO_SCRIPT.md - What to showcase
High-level architecture diagram

🔄 Future Enhancements (Post-POC)
Phase 2 Ideas
Real Tool Integration

Connect to actual JIRA API
Connect to actual ServiceNow
Connect to actual Splunk
Enhanced AI

Fine-tune models on SDLC data
Better intent classification
Proactive suggestions
More Personas

DevOps engineer
Scrum master
Customer support
More Tools

GitHub/GitLab
Jenkins/CircleCI
Datadog/New Relic
Production Features

Real authentication (OAuth)
Multi-user support
Persistent chat history
Cloud deployment
Monitoring and logging

🎓 Learning Outcomes
Building MAHALO demonstrates:

✅ MCP protocol implementation
✅ Multi-agent AI orchestration
✅ LLM integration (LiteLLM)
✅ Full-stack development (Python + React)
✅ RESTful API design
✅ Database modeling (SQLAlchemy)
✅ Testing strategies
✅ Cross-tool integration patterns
✅ Natural language interfaces for enterprise tools
✅ AI-augmented developer productivity


📞 Support & Feedback
Questions?

Check documentation in docs/ folder
Review API documentation
Run tests to verify setup
Issues?

Check .env configuration
Verify all services running
Reset demo data
Check logs for errors
📝 Version History
Version	Date	Changes
1.0	Jan 2025	Initial architecture and planning document






