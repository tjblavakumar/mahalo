# MAHALO API Documentation

Version: 1.0.0  
Last verified: 2026-08-13

MAHALO is a local proof of concept. The APIs below use mocked JIRA, ServiceNow, and Splunk data stored in SQLite.

## Service Map

| Service | URL | Purpose |
| --- | --- | --- |
| Main API | `http://localhost:8000` | UI gateway, chat, admin |
| JIRA mock API | `http://localhost:5001` | Users and stories |
| ServiceNow mock API | `http://localhost:5002` | Incidents |
| Splunk mock API | `http://localhost:5003` | Logs and search |
| JIRA MCP | `http://localhost:6001` | JIRA tool discovery/calls |
| ServiceNow MCP | `http://localhost:6002` | ServiceNow tool discovery/calls |
| Splunk MCP | `http://localhost:6003` | Splunk tool discovery/calls |

Interactive OpenAPI documentation is available at `/docs` on each FastAPI service.

## Main API

### `GET /health`

Returns the gateway health state.

### `GET /`

Returns service metadata, configured port, docs URL, and frontend URL.

### `GET /api/chat/personas`

Returns the four supported personas: Executive, Product Manager, Developer, and QA.

### `POST /api/chat/message`

Request:

```json
{
  "persona": "Developer",
  "message": "Show payment errors",
  "conversation_id": "optional-existing-id"
}
```

The gateway stores the user message, asks the selected specialist agents to retrieve matching records through MCP, sends that tool context to the configured LLM, stores the response, and returns a conversation ID:

For a follow-up such as "help me create the suggested use case with complete details", the orchestrator returns a detailed JIRA story draft with acceptance criteria and evidence. It does not write automatically. A subsequent explicit request such as "create this story in JIRA" writes the pending draft through the JIRA MCP tool and returns the created story key.

```json
{
  "response": "...",
  "timestamp": "2026-08-13T21:00:00.000000",
  "conversation_id": "conv-20260813210000",
  "agents_used": ["Splunk Agent"]
}
```

### `GET /api/chat/history/{conversation_id}`

Returns messages recorded for the specified conversation. Use the optional `limit` query parameter to control the number of messages.

### `GET /api/admin/status`

Returns the current main API status.

### `GET /api/admin/info`

Returns MAHALO metadata and reset capability.

### `GET /api/admin/stats`

Returns message counts for the current in-memory conversation context.

### `POST /api/admin/reset-data`

Reseeds SQLite with the MahaloPay demo data and clears conversation context.

## Mock APIs

The mock services expose these routes:

### JIRA, port 5001

- `GET /health`
- `GET /api/jira/users`
- `POST /api/jira/users`
- `GET /api/jira/stories`
- `POST /api/jira/stories`
- `GET /api/jira/stories/{story_key}`
- `GET /api/jira/bugs`

### ServiceNow, port 5002

- `GET /health`
- `GET /api/servicenow/incidents`
- `POST /api/servicenow/incidents`
- `GET /api/servicenow/incidents/{incident_id}`

### Splunk, port 5003

- `GET /health`
- `GET /api/splunk/logs`
- `POST /api/splunk/logs`
- `GET /api/splunk/search?query=...`

## MCP HTTP Surface

Each MCP server exposes:

- `GET /health`
- `GET /tools`
- `POST /tools/{tool_name}` with body `{ "arguments": {} }`

Available tools:

- JIRA: `create_story`, `search_stories`, `get_story`, `list_bugs`
- ServiceNow: `list_incidents`, `get_incident`
- Splunk: `search_logs`, `list_logs`

The orchestrator selects multiple agents when a query spans domains. For example, a request mentioning an incident and error logs retrieves both ServiceNow incidents and Splunk logs before response generation.

Example:

```bash
curl http://localhost:6001/tools
curl -X POST http://localhost:6003/tools/search_logs \
  -H "Content-Type: application/json" \
  -d '{"arguments":{"query":"payment"}}'
```

## Configuration

Configuration is loaded from the root `.env` file. Start from [.env.example](../.env.example). Never commit the real API key.

## Intent and Confirmation

Chat requests are first classified into a structured intent such as error analysis, deployment lookup, velocity analysis, story detail, QA test generation, or story creation. The classifier selects the relevant agents before MCP retrieval. If the LLM is unavailable, a deterministic fallback classifier is used. Story creation remains confirmation-gated: the system drafts the story first and writes to JIRA only after an explicit confirmation such as `create this story in JIRA`.

## Test Data Generation

Use `python -m backend.utils.generate_test_data --help` for all options. The generator is additive and uses a deterministic seed by default:

```bash
python -m backend.utils.generate_test_data \
  --jira-data 100 \
  --servicenow-data 100 \
  --splunk-data 500 \
  --seed 42
```

Use `--reset` to reload the standard demo data before adding generated records. Generated records use `STORY-GEN-*`, `BUG-GEN-*`, `Generated Sprint *`, `INC-GEN-*`, and `DEPLOY-GEN-*` identifiers so they are easy to recognize. Use `--servicenow-deployments N` to add N deployment records independently of incidents.
