#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "============================================================"
echo " MAHALO - Stopping All Services (Linux)"
echo "============================================================"

echo "Stopping MAHALO backend and frontend processes..."

pkill -f "uvicorn backend.jira.app:app" || true
pkill -f "uvicorn backend.servicenow.app:app" || true
pkill -f "uvicorn backend.splunk.app:app" || true
pkill -f "mcp_servers.jira_mcp.server" || true
pkill -f "mcp_servers.servicenow_mcp.server" || true
pkill -f "mcp_servers.splunk_mcp.server" || true
pkill -f "uvicorn api.main:app" || true
pkill -f "frontend.*npm start" || true

for port in 5001 5002 5003 6001 6002 6003 8000 3000; do
  if command -v lsof >/dev/null 2>&1; then
    lsof -ti tcp:$port | xargs -r kill -9 || true
  fi
done

echo "All MAHALO services stopped."
