# MAHALO

MAHALO is a local proof-of-concept for an AI-powered SDLC orchestrator built around a FinTech demo domain, MahaloPay.

## Local environments supported

- Windows 10/11
- Linux
- WSL2

The project keeps the same architecture and service layout across both OSes, but uses separate startup scripts for each environment.

## Quick start

### Windows

```bat
cd mahalo
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
scripts\start_all.bat
```

### Linux

```bash
cd mahalo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./scripts/start_all.sh
```

## Included scripts

- Windows: `scripts/start_all.bat`, `scripts/stop_all.bat`, `scripts/reset_demo.bat`, `scripts/run_tests.bat`
- Linux: `scripts/start_all.sh`, `scripts/stop_all.sh`, `scripts/reset_demo.sh`, `scripts/run_tests.sh`
- Data generation: `scripts/generate_test_data.sh` and `scripts/generate_test_data.bat`

## Frontend development

The React/Vite UI runs separately from the Python services:

```bash
cd frontend
npm install
npm run start
```

Open http://localhost:3000 while the main API is running on port 8000.

## Generate additional test data

The generator adds records without deleting existing data. For example:

```bash
./scripts/generate_test_data.sh --jira-data 100 --servicenow-data 100 --splunk-data 500 --servicenow-deployments 25
```

This adds 100 JIRA stories, 20 JIRA bugs, 10 generated sprints, 100 ServiceNow incidents, and 500 Splunk logs. Use `--seed` for repeatable generated values. Add `--reset` when you want to start from the standard MahaloPay demo data first.

For exact JIRA entity counts, use `--jira-stories`, `--jira-bugs`, and `--jira-sprints` instead of `--jira-data`.

Add ServiceNow deployment records separately:

```bash
./scripts/generate_test_data.sh --servicenow-deployments 25
```

## Default service ports

- JIRA mock API: 5001
- ServiceNow mock API: 5002
- Splunk mock API: 5003
- JIRA MCP: 6001
- ServiceNow MCP: 6002
- Splunk MCP: 6003
- Main API: 8000
- Frontend: 3000

## Notes

This project is intentionally designed as a local demo and learning project, with simplified MCP-like interfaces and mocked service data.

## Intent-aware orchestration

The orchestrator uses a structured LLM intent classifier when the configured model is available. It extracts the requested operation, relevant agents, and entities such as story keys or environments before retrieving MCP context. A deterministic classifier remains available when the LLM is unavailable. Any JIRA write still requires explicit user confirmation after a draft review.
