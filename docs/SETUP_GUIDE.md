# MAHALO Setup Guide

Last verified: 2026-08-13

## Prerequisites

- Python 3.10 or newer
- Node.js 16 or newer
- npm
- Git

## Linux or WSL2

From the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set exactly one provider key if live LLM responses are desired: `ONE_MIN_AI_API_KEY`, `LLM_API_KEY`, `OPEN_API_KEY`, or `OPENAI_API_KEY`. They are alternative names; the first non-empty value in that order is used. The orchestrator retains a deterministic local fallback when the key is unavailable or the request fails.

Install frontend dependencies once:

```bash
cd frontend
npm install
cd ..
```

Reset demo data and run tests:

```bash
./scripts/reset_demo.sh
./scripts/run_tests.sh
```

Start all services:

```bash
./scripts/start_all.sh
```

The script starts the mock APIs, MCP servers, main API, and frontend. Open `http://localhost:3000`.

## Windows

From the repository root in Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
cd frontend
npm install
cd ..
scripts\reset_demo.bat
scripts\run_tests.bat
scripts\start_all.bat
```

Open `http://localhost:3000` after startup. Use `scripts\stop_all.bat` to stop the services.

## Run Components Separately

## Generate Test Data

Add realistic records without deleting the existing demo data:

```bash
./scripts/generate_test_data.sh --jira-data 100 --servicenow-data 100 --splunk-data 500
```

The `--jira-data N` convenience option adds `N` stories, `N/5` bugs, and `N/10` sprints. Use `--jira-stories`, `--jira-bugs`, and `--jira-sprints` for exact JIRA counts. Add `--reset` before the counts to reseed the standard demo data first.

Generate ServiceNow deployment records independently:

```bash
./scripts/generate_test_data.sh --servicenow-deployments 25
```

Windows:

```bat
scripts\generate_test_data.bat --jira-data 100 --servicenow-data 100 --splunk-data 500
```

Main API:

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm run start
```

## Ports

The default ports are documented in [.env.example](../.env.example). Change them there and update any external client configuration before starting services.

## Security Note

This is a local demonstration. Authentication, authorization, production secrets management, HTTPS, and persistent conversation storage are intentionally out of scope.
