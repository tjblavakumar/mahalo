from typing import Any
import re

from mcp_servers.jira_mcp.tools import JiraMCPTools


class JiraAgent:
    def __init__(self, tools: JiraMCPTools | None = None):
        self.tools = tools or JiraMCPTools()

    async def retrieve_context(self, query: str) -> dict[str, Any]:
        query_lower = query.lower()
        story_match = re.search(r"\bstory[- ]?(\d+)\b", query_lower)
        if story_match and any(term in query_lower for term in ("test", "qa", "acceptance", "validate")):
            story_key = f"STORY-{story_match.group(1)}"
            result = await self.tools.get_story_handler({"story_key": story_key})
            return {"source": "JIRA", "query": query, "story_key": story_key, "record_type": "story_detail", **result}
        
        if "bug" in query_lower or "bugs" in query_lower:
            result = await self.tools.list_bugs_handler({"query": ""})
            if result.get("success"):
                bugs = result.get("data", {}).get("items", [])
                result["summary"] = {
                    "total_bugs": len(bugs),
                    "open_bugs": sum(bug.get("status", "").lower() in {"open", "in progress"} for bug in bugs),
                    "critical_bugs": sum(bug.get("severity", "").lower() == "critical" for bug in bugs),
                }
            return {"source": "JIRA", "query": query, "record_type": "bugs", **result}

        # Check if user wants all stories (summary/overview queries)
        get_all_stories = any(term in query_lower for term in (
            "velocity", "executive", "overview", "overall", "summary", "summarize",
            "all stories", "list stories", "show stories", "all", "everything"
        ))
        search_query = "" if get_all_stories else query
        result = await self.tools.search_stories_handler({"query": search_query})
        if result.get("success"):
            stories = result.get("data", {}).get("items", [])
            completed = [story for story in stories if story.get("status", "").lower() == "done"]
            total_points = sum(story.get("story_points", 0) or 0 for story in stories)
            completed_points = sum(story.get("story_points", 0) or 0 for story in completed)
            result["summary"] = {
                "total_stories": len(stories),
                "completed_stories": len(completed),
                "in_progress_stories": sum(story.get("status") == "In Progress" for story in stories),
                "backlog_stories": sum(story.get("status") == "Backlog" for story in stories),
                "total_story_points": total_points,
                "completed_story_points": completed_points,
                "completion_percent": round((completed_points / total_points) * 100, 1) if total_points else 0,
            }
        return {"source": "JIRA", "query": query, **result}

    async def create_story(self, story: dict[str, Any]) -> dict[str, Any]:
        return await self.tools.create_story_handler(story)

    def process_query(self, query: str) -> str:
        return "JIRA Agent: I would inspect payment stories, sprint status, and backlog."
