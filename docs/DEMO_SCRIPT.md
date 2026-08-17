# MAHALO Demo Walkthrough

Use this script for a 10-minute MahaloPay demonstration.

## 1. Start the Demo

1. Activate the Python environment.
2. Run the platform startup script for your operating system.
3. Open `http://localhost:3000`.
4. Confirm the system pulse reports the main API.

## 2. Executive View

Select **Executive** and ask:

> Show me the current sprint status and critical payment issues.

Explain that the orchestrator classifies the request and can route it toward JIRA, ServiceNow, or Splunk.

## 3. Product Manager View

Select **Product Manager** and ask:

> Show me the payment backlog.

Use the JIRA mock API or Swagger page at `http://localhost:5001/docs` to show the seeded stories and MahaloPay domain data.

## 4. Developer View

Select **Developer** and ask:

> Show payment service errors and latency signals.

Use the Splunk mock API at `http://localhost:5003/docs` to show searchable logs.

## 5. QA View

Select **QA** and ask:

> What incidents are active for payment processing?

Use the ServiceNow mock API at `http://localhost:5002/docs` to show the seeded incidents.

## 6. Show MCP Discovery

Open these endpoints in a browser or terminal:

```bash
curl http://localhost:6001/tools
curl http://localhost:6002/tools
curl http://localhost:6003/tools
```

Point out that the MCP layer presents standardized tool definitions over each mock service.

## 7. Reset the Demo

Click **Reset demo data** in the UI, or run:

```bash
curl -X POST http://localhost:8000/api/admin/reset-data
```

The SQLite data returns to the initial MahaloPay scenario and chat context is cleared.

## 8. Close

Use the platform as a single conversational entry point while the underlying tools retain their own API boundaries. Emphasize that this is a local proof of concept, not a production deployment.
