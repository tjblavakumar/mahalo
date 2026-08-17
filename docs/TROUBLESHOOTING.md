# MAHALO Troubleshooting

## Port Already in Use

Find the process using a port and stop it, or change the corresponding value in `.env`.

Linux:

```bash
lsof -i :8000
./scripts/stop_all.sh
```

Windows:

```bat
netstat -aon | findstr :8000
scripts\stop_all.bat
```

## Virtual Environment Not Found

Create and activate it from the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows use `python -m venv venv` and `venv\Scripts\activate`.

## Frontend Cannot Reach the API

Confirm the API responds:

```bash
curl http://localhost:8000/health
```

Then confirm the frontend is using `VITE_API_URL=http://localhost:8000` or its default. Restart Vite after changing environment variables.

## Chat Returns a Model Error

Check `.env` for one of `ONE_MIN_AI_API_KEY`, `LLM_API_KEY`, `OPEN_API_KEY`, or `OPENAI_API_KEY`, plus the matching base URL and `LITELLM_MODEL`. Only one provider key is required. The local orchestrator falls back to deterministic routing when the configured provider is unavailable.

## Duplicate Data During Tests

Run tests through the repository virtual environment. The test session resets the demo database automatically:

```bash
pytest tests/ -q
```

For a manual reset, run `./scripts/reset_demo.sh` or `scripts\reset_demo.bat`.

## MCP Server Is Unreachable

Check the server health and tool discovery endpoints:

```bash
curl http://localhost:6001/health
curl http://localhost:6001/tools
```

Confirm startup scripts use `mcp_servers`, with an underscore. The old `mcp-servers` directory is not used.

## Warnings During Tests

FastAPI lifecycle and SQLAlchemy datetime deprecation warnings may appear. They do not currently fail the test suite; they are follow-up maintenance items for a future cleanup pass.
