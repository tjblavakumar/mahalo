# MAHALO Testing Checklist

Last verified: 2026-08-13

## Environment

- [x] Python 3.10+ available
- [x] Node.js 16+ and npm available
- [x] Virtual environment installs `requirements.txt`
- [x] Frontend dependencies install successfully
- [x] `.env.example` documents local configuration

## Backend

- [x] Main API health endpoint responds
- [x] JIRA mock API health and story flow pass
- [x] ServiceNow incident flow passes
- [x] Splunk log search flow passes
- [x] Demo reset reseeds SQLite data
- [x] Chat route records conversation context
- [x] Admin stats and reset endpoints pass

## MCP

- [x] MCP base tool registration passes
- [x] JIRA, ServiceNow, and Splunk tool wrappers import
- [x] MCP server health endpoints respond
- [x] MCP tool discovery responds
- [x] MCP tool calls return structured responses

## Frontend

- [x] Vite development server starts on port 3000
- [x] Production build succeeds
- [x] Persona selector is rendered
- [x] Chat composer calls the main API
- [x] System status and reset controls are wired
- [x] Responsive mobile layout is defined

## Commands

From the repository root:

```bash
source venv/bin/activate
pytest tests/ -q
cd frontend
npm run build
```

Expected result: all backend tests pass and the frontend build completes without errors.

## Known Scope Limits

- No authentication or authorization
- Conversation context is in memory
- MCP is a simplified local HTTP-compatible implementation
- External 1min.ai calls require a configured key and network access
