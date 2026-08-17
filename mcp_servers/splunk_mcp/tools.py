from __future__ import annotations

from typing import Any, Dict

import httpx


class SplunkMCPTools:
    def __init__(self, api_url: str = "http://localhost:5003"):
        self.api_url = api_url

    async def close(self):
        pass  # No client to close

    async def search_logs_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        query = arguments.get("query", "")
        try:
            async with httpx.AsyncClient(timeout=10.0, trust_env=True) as client:
                response = await client.get(f"{self.api_url}/api/splunk/search", params={"query": query})
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    async def list_logs_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=10.0, trust_env=True) as client:
                response = await client.get(f"{self.api_url}/api/splunk/logs")
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
