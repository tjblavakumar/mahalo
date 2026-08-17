# MAHALO - Phase 2: Build MCP Servers ## Model Context Protocol Integration Layer
Phase Goal: Wrap each mock API with MCP (Model Context Protocol) servers to expose tools and resources in a standardized way.

Estimated Time: 3-4 hours

Prerequisites:

Phase 1 completed successfully
All 3 mock APIs running and tested
Database populated with seed data
📋 Phase 2 Overview
This phase creates the MCP (Model Context Protocol) layer:

Install MCP SDK - Python MCP library
Understand MCP Concepts - Tools, Resources, Prompts
JIRA MCP Server (Port 6001) - Expose JIRA operations
ServiceNow MCP Server (Port 6002) - Expose ServiceNow operations
Splunk MCP Server (Port 6003) - Expose Splunk operations
Test MCP Servers - Verify protocol compliance
What is MCP?
Model Context Protocol (MCP) is a standardized way for AI applications to interact with external tools and data sources. It defines:

Tools - Functions that can be called (e.g., create_story, search_logs)
Resources - Data that can be read (e.g., list of stories, log entries)
Prompts - Pre-defined prompt templates
Sampling - LLM completion requests
For MAHALO, we'll focus on Tools and Resources.

🔧 Understanding MCP Architecture
MCP Flow
AI Agent → MCP Client → MCP Server → Tool API → Database
    ↑                                              ↓
    └──────────────── Response ───────────────────┘
Our Implementation
JIRA Agent → MCP Client → JIRA MCP Server → JIRA API (5001) → Database
Each MCP Server:

Exposes tools as MCP-compliant functions
Translates MCP calls to HTTP API calls
Returns responses in MCP format
Handles errors gracefully
Task 2.1: Install MCP SDK ⬜
Instruction to Coding Assistant: Install the Python MCP SDK and dependencies.

Update requirements.txt
Add MCP SDK to requirements.txt:

cat >> requirements.txt << 'EOF'

# ==================== MCP SDK ====================
# Note: For this POC, we're using a simplified MCP-compatible implementation
# The official MCP SDK is under active development
# We'll create our own mcp_base.py that follows MCP protocol concepts

# No additional package needed - we'll implement it ourselves
EOF

**Note:** We are **NOT** installing the official MCP SDK. Instead, we'll create a simplified MCP-compatible implementation in `mcp_servers/mcp_base.py` that demonstrates the MCP protocol concepts for this proof of concept.

**Why this approach:**
- The official MCP Python SDK may not be stable yet
- For a POC, we don't need full MCP protocol compliance
- We can implement the core concepts (Tools, Resources) ourselves
- This gives us more control and is easier to understand
- Production systems would use the official SDK when it's mature

**Our Approach: Create Simplified MCP Base Classes**

Since we're building a POC, we'll create our own MCP-compatible base classes that follow the core concepts:

**Create mcp_servers/mcp_base.py:**

"""
MCP Base Classes (Simplified Implementation)
For demonstration purposes - compatible with MCP protocol concepts
"""
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import asyncio
import httpx

class MCPToolType(str, Enum):
    """MCP Tool Types"""
    FUNCTION = "function"

@dataclass
class MCPTool:
    """MCP Tool Definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    handler: Optional[Callable] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        return {
            "type": MCPToolType.FUNCTION,
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema
            }
        }

@dataclass
class MCPResource:
    """MCP Resource Definition"""
    uri: str
    name: str
    description: str
    mime_type: str = "application/json"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "mimeType": self.mime_type
        }

class MCPServer:
    """Base MCP Server Implementation"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, MCPResource] = {}
        self.http_client = httpx.AsyncClient()
    
    def register_tool(self, tool: MCPTool):
        """Register a tool with the server"""
        self.tools[tool.name] = tool
        print(f"  📝 Registered tool: {tool.name}")
    
    def register_resource(self, resource: MCPResource):
        """Register a resource with the server"""
        self.resources[resource.uri] = resource
        print(f"  📝 Registered resource: {resource.name}")
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources"""
        return [resource.to_dict() for resource in self.resources.values()]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        if not tool.handler:
            raise ValueError(f"Tool '{tool_name}' has no handler")
        
        # Execute tool handler
        result = await tool.handler(arguments)
        return result
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a resource by URI"""
        if uri not in self.resources:
            raise ValueError(f"Resource '{uri}' not found")
        
        # Implementation would fetch actual resource data
        return {"uri": uri, "data": "Resource data would be here"}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.name,
            "version": self.version,
            "tools_count": len(self.tools),
            "resources_count": len(self.resources)
        }
    
    async def close(self):
        """Cleanup resources"""
        await self.http_client.aclose()

# Export classes
__all__ = ["MCPServer", "MCPTool", "MCPResource", "MCPToolType"]
Test MCP Base Classes
python -c "from mcp_servers.mcp_base import MCPServer, MCPTool; print('✅ MCP base classes imported successfully')"
Acceptance Criteria:

✅ MCP SDK installed (or base classes created)
✅ Can import MCP modules without errors
✅ Base classes provide Tool and Resource support
Mark Complete: ⬜ → ✅

Task 2.2: Create JIRA MCP Server - Tools ⬜
Instruction to Coding Assistant: Define MCP tools for JIRA operations.

Create mcp_servers/jira_mcp/tools.py
"""
JIRA MCP Tools
Define tools that expose JIRA functionality via MCP
"""
from typing import Dict, Any, List
from mcp_servers.mcp_base import MCPTool
import httpx

class JiraMCPTools:
    """JIRA MCP Tool Definitions"""
    
    def __init__(self, jira_api_url: str = "http://localhost:5001"):
        self.jira_api_url = jira_api_url
        self.client = httpx.AsyncClient()
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    # ==================== TOOL HANDLERS ====================
    
    async def create_user_story_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for create_user_story tool"""
        try:
            response = await self.client.post(
                f"{self.jira_api_url}/api/jira/stories",
                json=arguments
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def search_stories_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for search_stories tool"""
        try:
            response = await self.client.post(
                f"{self.jira_api_url}/api/jira/stories/search",
                json=arguments
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_story_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_story tool"""
        try:
            story_key = arguments.get("story_key")
            response = await self.client.get(
                f"{self.jira_api_url}/api/jira/stories/{story_key}"
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_story_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for update_story tool"""
        try:
            story_key = arguments.pop("story_key")
            response = await self.client.patch(
                f"{self.jira_api_url}/api/jira/stories/{story_key}",
                json=arguments
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_stories_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for list_stories tool"""
        try:
            params = {}
            if "status" in arguments:
                params["status"] = arguments["status"]
            if "assignee" in arguments:
                params["assignee"] = arguments["assignee"]
            if "sprint" in arguments:
                params["sprint"] = arguments["sprint"]
            
            response = await self.client.get(
                f"{self.jira_api_url}/api/jira/stories",
                params=params
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def create_bug_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for create_bug tool"""
        try:
            response = await self.client.post(
                f"{self.jira_api_url}/api/jira/bugs",
                json=arguments
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_bugs_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for list_bugs tool"""
        try:
            params = {}
            if "status" in arguments:
                params["status"] = arguments["status"]
            if "severity" in arguments:
                params["severity"] = arguments["severity"]
            if "assignee" in arguments:
                params["assignee"] = arguments["assignee"]
            
            response = await self.client.get(
                f"{self.jira_api_url}/api/jira/bugs",
                params=params
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_sprint_summary_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_sprint_summary tool"""
        try:
            sprint_name = arguments.get("sprint_name")
            response = await self.client.get(
                f"{self.jira_api_url}/api/jira/sprints/{sprint_name}/summary"
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_user_tasks_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_user_tasks tool"""
        try:
            username = arguments.get("username")
            
            # Get stories
            stories_response = await self.client.get(
                f"{self.jira_api_url}/api/jira/stories",
                params={"assignee": username}
            )
            stories_response.raise_for_status()
            
            # Get bugs
            bugs_response = await self.client.get(
                f"{self.jira_api_url}/api/jira/bugs",
                params={"assignee": username}
            )
            bugs_response.raise_for_status()
            
            return {
                "success": True,
                "data": {
                    "stories": stories_response.json(),
                    "bugs": bugs_response.json()
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def calculate_velocity_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for calculate_velocity tool"""
        try:
            params = {}
            if "last_n_sprints" in arguments:
                params["last_n_sprints"] = arguments["last_n_sprints"]
            
            response = await self.client.get(
                f"{self.jira_api_url}/api/jira/velocity",
                params=params
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== TOOL DEFINITIONS ====================
    
    def get_tools(self) -> List[MCPTool]:
        """Get all JIRA MCP tool definitions"""
        return [
            MCPTool(
                name="create_user_story",
                description="Create a new user story in JIRA. Use this to add new features or requirements to the backlog.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Story title (required, 5-200 characters)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed story description"
                        },
                        "assignee_username": {
                            "type": "string",
                            "description": "Username of assignee (e.g., 'alice_dev')"
                        },
                        "reporter_username": {
                            "type": "string",
                            "description": "Username of reporter (e.g., 'bob_pm')"
                        },
                        "story_points": {
                            "type": "integer",
                            "description": "Story points (0-100)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Critical"],
                            "description": "Story priority"
                        },
                        "sprint": {
                            "type": "string",
                            "description": "Sprint name (e.g., 'Sprint 23')"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["Backlog", "Dev", "UAT", "Done"],
                            "description": "Story status"
                        }
                    },
                    "required": ["title"]
                },
                handler=self.create_user_story_handler
            ),
            MCPTool(
                name="search_stories",
                description="Search for user stories by title. Use this to find existing stories or check for duplicates before creating new ones.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Search query for story title"
                        }
                    },
                    "required": ["title"]
                },
                handler=self.search_stories_handler
            ),
            MCPTool(
                name="get_story",
                description="Get detailed information about a specific user story by its key (e.g., STORY-123).",
                input_schema={
                    "type": "object",
                    "properties": {
                        "story_key": {
                            "type": "string",
                            "description": "Story key (e.g., 'STORY-123')"
                        }
                    },
                    "required": ["story_key"]
                },
                handler=self.get_story_handler
            ),
            MCPTool(
                name="update_story",
                description="Update an existing user story. Can update title, description, status, assignee, story points, or priority.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "story_key": {
                            "type": "string",
                            "description": "Story key to update (e.g., 'STORY-123')"
                        },
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": ["Backlog", "Dev", "UAT", "Done"]
                        },
                        "assignee_username": {"type": "string"},
                        "story_points": {"type": "integer"},
                        "priority": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Critical"]
                        }
                    },
                    "required": ["story_key"]
                },
                handler=self.update_story_handler
            ),
            MCPTool(
                name="list_stories",
                description="List user stories with optional filters. Can filter by status, assignee, or sprint.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["Backlog", "Dev", "UAT", "Done"],
                            "description": "Filter by status"
                        },
                        "assignee": {
                            "type": "string",
                            "description": "Filter by assignee username"
                        },
                        "sprint": {
                            "type": "string",
                            "description": "Filter by sprint name"
                        }
                    }
                },
                handler=self.list_stories_handler
            ),
            MCPTool(
                name="create_bug",
                description="Create a new bug/defect in JIRA. Use this to report issues found during testing or production.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Bug title (required)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Bug description and reproduction steps"
                        },
                        "assignee_username": {"type": "string"},
                        "reporter_username": {"type": "string"},
                        "severity": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Critical"],
                            "description": "Bug severity"
                        },
                        "related_story_key": {
                            "type": "string",
                            "description": "Related story key if bug is linked to a story"
                        },
                        "servicenow_incident_id": {
                            "type": "string",
                            "description": "ServiceNow incident number if linked"
                        }
                    },
                    "required": ["title"]
                },
                handler=self.create_bug_handler
            ),
            MCPTool(
                name="list_bugs",
                description="List bugs with optional filters. Can filter by status, severity, or assignee.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["Open", "In Progress", "Testing", "Closed"]
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Critical"]
                        },
                        "assignee": {"type": "string"}
                    }
                },
                handler=self.list_bugs_handler
            ),
            MCPTool(
                name="get_sprint_summary",
                description="Get comprehensive sprint summary including stories by status, bug count, velocity, and team metrics.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "sprint_name": {
                            "type": "string",
                            "description": "Sprint name (e.g., 'Sprint 23')"
                        }
                    },
                    "required": ["sprint_name"]
                },
                handler=self.get_sprint_summary_handler
            ),
            MCPTool(
                name="get_user_tasks",
                description="Get all tasks (stories and bugs) assigned to a specific user. Useful for developers to see their workload.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "Username (e.g., 'alice_dev')"
                        }
                    },
                    "required": ["username"]
                },
                handler=self.get_user_tasks_handler
            ),
            MCPTool(
                name="calculate_velocity",
                description="Calculate team velocity over last N sprints. Helps track team performance trends.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "last_n_sprints": {
                            "type": "integer",
                            "description": "Number of sprints to analyze (default: 3)"
                        }
                    }
                },
                handler=self.calculate_velocity_handler
            )
        ]

# For testing
if __name__ == "__main__":
    tools = JiraMCPTools()
    tool_list = tools.get_tools()
    print(f"✅ Defined {len(tool_list)} JIRA MCP tools:")
    for tool in tool_list:
        print(f"   - {tool.name}: {tool.description[:60]}...")
Test JIRA Tools
python mcp_servers/jira_mcp/tools.py
Expected Output:

✅ Defined 10 JIRA MCP tools:
   - create_user_story: Create a new user story in JIRA...
   - search_stories: Search for user stories by title...
   - get_story: Get detailed information about a specific user story...
   - update_story: Update an existing user story...
   - list_stories: List user stories with optional filters...
   - create_bug: Create a new bug/defect in JIRA...
   - list_bugs: List bugs with optional filters...
   - get_sprint_summary: Get comprehensive sprint summary...
   - get_user_tasks: Get all tasks assigned to a specific user...
   - calculate_velocity: Calculate team velocity over last N sprints...
Acceptance Criteria:

✅ All 10 JIRA tools defined
✅ Each tool has clear description
✅ Input schemas properly defined
✅ Handlers implemented for all tools
✅ Tools follow MCP protocol format
Mark Complete: ⬜ → ✅

Task 2.3: Create JIRA MCP Server ⬜
Instruction to Coding Assistant: Create the main JIRA MCP server that registers and serves tools.

Create mcp_servers/jira_mcp/server.py
"""
JIRA MCP Server
Main MCP server for JIRA tool integration
"""
from mcp_servers.mcp_base import MCPServer
from mcp_servers.jira_mcp.tools import JiraMCPTools
from backend.config import settings
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class JiraMCPServer:
    """JIRA MCP Server Implementation"""
    
    def __init__(self):
        self.mcp_server = MCPServer(name="jira-mcp", version="1.0.0")
        self.jira_tools = JiraMCPTools(
            jira_api_url=f"http://localhost:{settings.JIRA_API_PORT}"
        )
        self.app = FastAPI(
            title="MAHALO JIRA MCP Server",
            description="MCP Server for JIRA - exposes JIRA tools via Model Context Protocol",
            version="1.0.0"
        )
        self._setup_routes()
        self._register_tools()
    
    def _register_tools(self):
        """Register all JIRA tools with MCP server"""
        print("📝 Registering JIRA MCP tools...")
        for tool in self.jira_tools.get_tools():
            self.mcp_server.register_tool(tool)
        print(f"✅ Registered {len(self.mcp_server.tools)} tools")
    
    def _setup_routes(self):
        """Setup FastAPI routes for MCP protocol"""
        
        # Add CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        # Root endpoint
        @self.app.get("/")
        async def root():
            return {
                "service": "JIRA MCP Server",
                "version": "1.0.0",
                "protocol": "MCP",
                "port": settings.MCP_JIRA_PORT
            }
        
        # Health check
        @self.app.get("/health")
        async def health():
            return {"status": "healthy", "service": "jira-mcp"}
        
        # MCP: List available tools
        @self.app.get("/mcp/tools")
        async def list_tools():
            """List all available MCP tools"""
            return {
                "tools": self.mcp_server.list_tools(),
                "count": len(self.mcp_server.tools)
            }
        
        # MCP: Call a tool
        @self.app.post("/mcp/call_tool")
        async def call_tool(request: dict):
            """
            Call an MCP tool
            
            Request format:
            {
                "tool_name": "create_user_story",
                "arguments": {
                    "title": "My Story",
                    "description": "Story description"
                }
            }
            """
            tool_name = request.get("tool_name")
            arguments = request.get("arguments", {})
            
            try:
                result = await self.mcp_server.call_tool(tool_name, arguments)
                return result
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        # MCP: Server information
        @self.app.get("/mcp/info")
        async def server_info():
            """Get MCP server information"""
            return self.mcp_server.get_server_info()
    
    def run(self):
        """Run the MCP server"""
        print("=" * 60)
        print("🚀 Starting JIRA MCP Server")
        print(f"📍 Port: {settings.MCP_JIRA_PORT}")
        print(f"🔧 JIRA API: http://localhost:{settings.JIRA_API_PORT}")
        print(f"📚 Tools: {len(self.mcp_server.tools)}")
        print("=" * 60)
        
        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=settings.MCP_JIRA_PORT,
            log_level="info"
        )
    
    async def close(self):
        """Cleanup resources"""
        await self.jira_tools.close()
        await self.mcp_server.close()

# Main entry point
if __name__ == "__main__":
    server = JiraMCPServer()
    server.run()
Create mcp_servers/jira_mcp/init.py
"""JIRA MCP Server Package"""
from mcp_servers.jira_mcp.server import JiraMCPServer

__all__ = ["JiraMCPServer"]
Test JIRA MCP Server
Terminal 1 - Start JIRA API:

python backend/jira/app.py
Terminal 2 - Start JIRA MCP Server:

python mcp_servers/jira_mcp/server.py
Terminal 3 - Test MCP Endpoints:

# Test health
curl http://localhost:6001/health

# List available tools
curl http://localhost:6001/mcp/tools

# Get server info
curl http://localhost:6001/mcp/info

# Call a tool (get sprint summary)
curl -X POST http://localhost:6001/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_sprint_summary",
    "arguments": {"sprint_name": "Sprint 23"}
  }'
Expected Output (list tools):

{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "create_user_story",
        "description": "Create a new user story in JIRA...",
        "parameters": {...}
      }
    },
    ...
  ],
  "count": 10
}
Acceptance Criteria:

✅ JIRA MCP Server starts on port 6001
✅ Can list all tools via /mcp/tools
✅ Can call tools via /mcp/call_tool
✅ Tools successfully communicate with JIRA API
✅ Responses in MCP-compatible format
Mark Complete: ⬜ → ✅

Task 2.4: Create ServiceNow MCP Server ⬜
Instruction to Coding Assistant: Create ServiceNow MCP server following the same pattern as JIRA.

Create mcp_servers/servicenow_mcp/tools.py
"""
ServiceNow MCP Tools
Define tools for ServiceNow incident management
"""
from typing import Dict, Any, List
from mcp_servers.mcp_base import MCPTool
import httpx

class ServiceNowMCPTools:
    """ServiceNow MCP Tool Definitions"""
    
    def __init__(self, servicenow_api_url: str = "http://localhost:5002"):
        self.servicenow_api_url = servicenow_api_url
        self.client = httpx.AsyncClient()
    
    async def close(self):
        await self.client.aclose()
    
    # ==================== TOOL HANDLERS ====================
    
    async def create_incident_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for create_incident tool"""
        try:
            response = await self.client.post(
                f"{self.servicenow_api_url}/api/servicenow/incidents",
                json=arguments
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_incident_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_incident tool"""
        try:
            incident_number = arguments.get("incident_number")
            response = await self.client.get(
                f"{self.servicenow_api_url}/api/servicenow/incidents/{incident_number}"
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_incidents_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for list_incidents tool"""
        try:
            params = {}
            if "status" in arguments:
                params["status"] = arguments["status"]
            if "priority" in arguments:
                params["priority"] = arguments["priority"]
            
            response = await self.client.get(
                f"{self.servicenow_api_url}/api/servicenow/incidents",
                params=params
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_incident_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for update_incident tool"""
        try:
            incident_number = arguments.pop("incident_number")
            response = await self.client.patch(
                f"{self.servicenow_api_url}/api/servicenow/incidents/{incident_number}",
                json=arguments
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== TOOL DEFINITIONS ====================
    
    def get_tools(self) -> List[MCPTool]:
        """Get all ServiceNow MCP tool definitions"""
        return [
            MCPTool(
                name="create_incident",
                description="Create a new incident in ServiceNow for production issues, outages, or service requests.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Incident title (required)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed incident description"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Critical"],
                            "description": "Incident priority"
                        },
                        "category": {
                            "type": "string",
                            "description": "Incident category (Infrastructure, Application, Network)"
                        },
                        "assigned_to": {
                            "type": "string",
                            "description": "Assigned team member"
                        },
                        "reported_by": {
                            "type": "string",
                            "description": "Reporter name"
                        },
                        "jira_bug_key": {
                            "type": "string",
                            "description": "Related JIRA bug key for cross-tool linking"
                        }
                    },
                    "required": ["title"]
                },
                handler=self.create_incident_handler
            ),
            MCPTool(
                name="get_incident",
                description="Get detailed information about a specific incident by its number (e.g., INC0001234).",
                input_schema={
                    "type": "object",
                    "properties": {
                        "incident_number": {
                            "type": "string",
                            "description": "Incident number (e.g., 'INC0001234')"
                        }
                    },
                    "required": ["incident_number"]
                },
                handler=self.get_incident_handler
            ),
            MCPTool(
                name="list_incidents",
                description="List incidents with optional filters. Can filter by status or priority.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["New", "In Progress", "Resolved", "Closed"],
                            "description": "Filter by incident status"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Critical"],
                            "description": "Filter by priority"
                        }
                    }
                },
                handler=self.list_incidents_handler
            ),
            MCPTool(
                name="update_incident",
                description="Update an existing incident. Can update status, priority, assignee, or link to JIRA bug.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "incident_number": {
                            "type": "string",
                            "description": "Incident number to update"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["New", "In Progress", "Resolved", "Closed"]
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Critical"]
                        },
                        "assigned_to": {"type": "string"},
                        "jira_bug_key": {"type": "string"}
                    },
                    "required": ["incident_number"]
                },
                handler=self.update_incident_handler
            )
        ]

if __name__ == "__main__":
    tools = ServiceNowMCPTools()
    tool_list = tools.get_tools()
    print(f"✅ Defined {len(tool_list)} ServiceNow MCP tools:")
    for tool in tool_list:
        print(f"   - {tool.name}")
Create mcp_servers/servicenow_mcp/server.py
"""ServiceNow MCP Server"""
from mcp_servers.mcp_base import MCPServer
from mcp_servers.servicenow_mcp.tools import ServiceNowMCPTools
from backend.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class ServiceNowMCPServer:
    """ServiceNow MCP Server Implementation"""
    
    def __init__(self):
        self.mcp_server = MCPServer(name="servicenow-mcp", version="1.0.0")
        self.sn_tools = ServiceNowMCPTools(
            servicenow_api_url=f"http://localhost:{settings.SERVICENOW_API_PORT}"
        )
        self.app = FastAPI(title="MAHALO ServiceNow MCP Server", version="1.0.0")
        self._setup_routes()
        self._register_tools()
    
    def _register_tools(self):
        print("📝 Registering ServiceNow MCP tools...")
        for tool in self.sn_tools.get_tools():
            self.mcp_server.register_tool(tool)
        print(f"✅ Registered {len(self.mcp_server.tools)} tools")
    
    def _setup_routes(self):
        self.app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
        
        @self.app.get("/")
        async def root():
            return {"service": "ServiceNow MCP Server", "port": settings.MCP_SERVICENOW_PORT}
        
        @self.app.get("/health")
        async def health():
            return {"status": "healthy"}
        
        @self.app.get("/mcp/tools")
        async def list_tools():
            return {"tools": self.mcp_server.list_tools(), "count": len(self.mcp_server.tools)}
        
        @self.app.post("/mcp/call_tool")
        async def call_tool(request: dict):
            try:
                return await self.mcp_server.call_tool(request["tool_name"], request.get("arguments", {}))
            except Exception as e:
                return {"success": False, "error": str(e)}
    
    def run(self):
        print(f"🚀 Starting ServiceNow MCP Server on port {settings.MCP_SERVICENOW_PORT}")
        uvicorn.run(self.app, host="0.0.0.0", port=settings.MCP_SERVICENOW_PORT, log_level="info")

if __name__ == "__main__":
    server = ServiceNowMCPServer()
    server.run()
Start ServiceNow MCP Server:

# Make sure ServiceNow API is running first
python backend/servicenow/app.py  # Terminal 1

# Start MCP Server
python mcp_servers/servicenow_mcp/server.py  # Terminal 2

# Test
curl http://localhost:6002/mcp/tools  # Terminal 3
Acceptance Criteria:

✅ ServiceNow MCP Server starts on port 6002
✅ 4 tools registered (create, get, list, update incidents)
✅ Tools work correctly
✅ Can call tools via MCP protocol
Mark Complete: ⬜ → ✅

Task 2.5: Create Splunk MCP Server ⬜
Instruction to Coding Assistant: Create Splunk MCP server for log search operations.

Create mcp_servers/splunk_mcp/tools.py
"""Splunk MCP Tools"""
from typing import Dict, Any, List
from mcp_servers.mcp_base import MCPTool
import httpx

class SplunkMCPTools:
    """Splunk MCP Tool Definitions"""
    
    def __init__(self, splunk_api_url: str = "http://localhost:5003"):
        self.splunk_api_url = splunk_api_url
        self.client = httpx.AsyncClient()
    
    async def close(self):
        await self.client.aclose()
    
    async def search_logs_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for search_logs tool"""
        try:
            response = await self.client.post(
                f"{self.splunk_api_url}/api/splunk/logs/search",
                json=arguments
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_error_logs_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_error_logs tool"""
        try:
            params = {"limit": arguments.get("limit", 50)}
            response = await self.client.get(
                f"{self.splunk_api_url}/api/splunk/logs/errors",
                params=params
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_logs_by_service_handler(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for get_logs_by_service tool"""
        try:
            params = {
                "service": arguments.get("service"),
                "log_level": arguments.get("log_level"),
                "limit": arguments.get("limit", 100)
            }
            response = await self.client.get(
                f"{self.splunk_api_url}/api/splunk/logs",
                params=params
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_tools(self) -> List[MCPTool]:
        """Get all Splunk MCP tool definitions"""
        return [
            MCPTool(
                name="search_logs",
                description="Search logs with flexible filters. Can search by service, log level, environment, and time range.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service name (e.g., 'login-service', 'payment-service')"
                        },
                        "log_level": {
                            "type": "string",
                            "enum": ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"],
                            "description": "Log level filter"
                        },
                        "environment": {
                            "type": "string",
                            "enum": ["dev", "uat", "prod"],
                            "description": "Environment filter"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Max number of results (default: 100)"
                        }
                    }
                },
                handler=self.search_logs_handler
            ),
            MCPTool(
                name="get_error_logs",
                description="Get recent ERROR and FATAL level logs. Useful for identifying production issues.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Max number of results (default: 50)"
                        }
                    }
                },
                handler=self.get_error_logs_handler
            ),
            MCPTool(
                name="get_logs_by_service",
                description="Get logs for a specific service with optional log level filter.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service name (required)"
                        },
                        "log_level": {
                            "type": "string",
                            "enum": ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Max results (default: 100)"
                        }
                    },
                    "required": ["service"]
                },
                handler=self.get_logs_by_service_handler
            )
        ]

if __name__ == "__main__":
    tools = SplunkMCPTools()
    tool_list = tools.get_tools()
    print(f"✅ Defined {len(tool_list)} Splunk MCP tools:")
    for tool in tool_list:
        print(f"   - {tool.name}")
Create mcp_servers/splunk_mcp/server.py
"""Splunk MCP Server"""
from mcp_servers.mcp_base import MCPServer
from mcp_servers.splunk_mcp.tools import SplunkMCPTools
from backend.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class SplunkMCPServer:
    def __init__(self):
        self.mcp_server = MCPServer(name="splunk-mcp", version="1.0.0")
        self.splunk_tools = SplunkMCPTools(
            splunk_api_url=f"http://localhost:{settings.SPLUNK_API_PORT}"
        )
        self.app = FastAPI(title="MAHALO Splunk MCP Server", version="1.0.0")
        self._setup_routes()
        self._register_tools()
    
    def _register_tools(self):
        print("📝 Registering Splunk MCP tools...")
        for tool in self.splunk_tools.get_tools():
            self.mcp_server.register_tool(tool)
        print(f"✅ Registered {len(self.mcp_server.tools)} tools")
    
    def _setup_routes(self):
        self.app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
        
        @self.app.get("/")
        async def root():
            return {"service": "Splunk MCP Server", "port": settings.MCP_SPLUNK_PORT}
        
        @self.app.get("/health")
        async def health():
            return {"status": "healthy"}
        
        @self.app.get("/mcp/tools")
        async def list_tools():
            return {"tools": self.mcp_server.list_tools(), "count": len(self.mcp_server.tools)}
        
        @self.app.post("/mcp/call_tool")
        async def call_tool(request: dict):
            try:
                return await self.mcp_server.call_tool(request["tool_name"], request.get("arguments", {}))
            except Exception as e:
                return {"success": False, "error": str(e)}
    
    def run(self):
        print(f"🚀 Starting Splunk MCP Server on port {settings.MCP_SPLUNK_PORT}")
        uvicorn.run(self.app, host="0.0.0.0", port=settings.MCP_SPLUNK_PORT, log_level="info")

if __name__ == "__main__":
    server = SplunkMCPServer()
    server.run()
Start and test:

python mcp_servers/splunk_mcp/server.py
Acceptance Criteria:

✅ Splunk MCP Server starts on port 6003
✅ 3 tools registered (search, get_error_logs, get_logs_by_service)
✅ Can query logs via MCP protocol
Mark Complete: ⬜ → ✅

Task 2.6: Create MCP Server Tests ⬜
Instruction to Coding Assistant: Create automated tests for MCP servers.

Create tests/test_mcp_servers.py
"""
MCP Server Tests
Test MCP protocol compliance and tool execution
"""
import pytest
import httpx
import asyncio
from backend.database import init_db
from backend.jira.seed_data import seed_jira_data
from backend.servicenow.seed_data import seed_servicenow_data

# Setup: Ensure data is seeded
@pytest.fixture(scope="module", autouse=True)
def setup_test_data():
    """Setup test data"""
    init_db()
    seed_jira_data()
    seed_servicenow_data()
    yield

# ==================== JIRA MCP TESTS ====================

@pytest.mark.asyncio
async def test_jira_mcp_health():
    """Test JIRA MCP server health"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:6001/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_jira_mcp_list_tools():
    """Test listing JIRA MCP tools"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:6001/mcp/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert data["count"] == 10  # JIRA has 10 tools

@pytest.mark.asyncio
async def test_jira_mcp_call_tool_sprint_summary():
    """Test calling get_sprint_summary tool"""
    async with httpx.AsyncClient() as client:
        payload = {
            "tool_name": "get_sprint_summary",
            "arguments": {"sprint_name": "Sprint 23"}
        }
        response = await client.post("http://localhost:6001/mcp/call_tool", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["sprint_name"] == "Sprint 23"

@pytest.mark.asyncio
async def test_jira_mcp_call_tool_search_stories():
    """Test calling search_stories tool"""
    async with httpx.AsyncClient() as client:
        payload = {
            "tool_name": "search_stories",
            "arguments": {"title": "authentication"}
        }
        response = await client.post("http://localhost:6001/mcp/call_tool", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

# ==================== SERVICENOW MCP TESTS ====================

@pytest.mark.asyncio
async def test_servicenow_mcp_health():
    """Test ServiceNow MCP server health"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:6002/health")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_servicenow_mcp_list_tools():
    """Test listing ServiceNow MCP tools"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:6002/mcp/tools")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 4  # ServiceNow has 4 tools

@pytest.mark.asyncio
async def test_servicenow_mcp_call_tool_list_incidents():
    """Test calling list_incidents tool"""
    async with httpx.AsyncClient() as client:
        payload = {
            "tool_name": "list_incidents",
            "arguments": {"priority": "Critical"}
        }
        response = await client.post("http://localhost:6002/mcp/call_tool", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

# ==================== SPLUNK MCP TESTS ====================

@pytest.mark.asyncio
async def test_splunk_mcp_health():
    """Test Splunk MCP server health"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:6003/health")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_splunk_mcp_list_tools():
    """Test listing Splunk MCP tools"""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:6003/mcp/tools")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3  # Splunk has 3 tools

@pytest.mark.asyncio
async def test_splunk_mcp_call_tool_get_error_logs():
    """Test calling get_error_logs tool"""
    async with httpx.AsyncClient() as client:
        payload = {
            "tool_name": "get_error_logs",
            "arguments": {"limit": 10}
        }
        response = await client.post("http://localhost:6003/mcp/call_tool", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
Run MCP tests (ensure all servers are running):

# Start all APIs and MCP servers first
python backend/jira/app.py &
python backend/servicenow/app.py &
python backend/splunk/app.py &
python mcp_servers/jira_mcp/server.py &
python mcp_servers/servicenow_mcp/server.py &
python mcp_servers/splunk_mcp/server.py &

# Run tests
pytest tests/test_mcp_servers.py -v
Acceptance Criteria:

✅ All MCP health checks pass
✅ Can list tools from all MCP servers
✅ Can call tools via MCP protocol
✅ All tests pass
Mark Complete: ⬜ → ✅

Task 2.7: Create Start Script for All Services ⬜
Instruction to Coding Assistant: Create convenient script to start all services (APIs + MCP servers).

Update scripts/start_all.sh
#!/bin/bash
echo "=" | tr '\n' '=' | head -c 60; echo
echo "🚀 Starting MAHALO Services"
echo "=" | tr '\n' '=' | head -c 60; echo
echo

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Start JIRA API
echo "📝 Starting JIRA API (port 5001)..."
python backend/jira/app.py &
JIRA_PID=$!
sleep 2

# Start ServiceNow API
echo "🎫 Starting ServiceNow API (port 5002)..."
python backend/servicenow/app.py &
SN_PID=$!
sleep 2

# Start Splunk API
echo "📊 Starting Splunk API (port 5003)..."
python backend/splunk/app.py &
SPLUNK_PID=$!
sleep 2

# Start JIRA MCP Server
echo "🔌 Starting JIRA MCP Server (port 6001)..."
python mcp_servers/jira_mcp/server.py &
JIRA_MCP_PID=$!
sleep 2

# Start ServiceNow MCP Server
echo "🔌 Starting ServiceNow MCP Server (port 6002)..."
python mcp_servers/servicenow_mcp/server.py &
SN_MCP_PID=$!
sleep 2

# Start Splunk MCP Server
echo "🔌 Starting Splunk MCP Server (port 6003)..."
python mcp_servers/splunk_mcp/server.py &
SPLUNK_MCP_PID=$!
sleep 2

# Save PIDs
echo "$JIRA_PID $SN_PID $SPLUNK_PID $JIRA_MCP_PID $SN_MCP_PID $SPLUNK_MCP_PID" > .mahalo_pids

echo
echo "=" | tr '\n' '=' | head -c 60; echo
echo "✅ All services started!"
echo "=" | tr '\n' '=' | head -c 60; echo
echo
echo "📋 Service URLs:"
echo "  🔸 JIRA API:         http://localhost:5001"
echo "  🔸 ServiceNow API:   http://localhost:5002"
echo "  🔸 Splunk API:       http://localhost:5003"
echo "  🔸 JIRA MCP:         http://localhost:6001"
echo "  🔸 ServiceNow MCP:   http://localhost:6002"
echo "  🔸 Splunk MCP:       http://localhost:6003"
echo
echo "🛑 To stop all services: bash scripts/stop_all.sh"
echo
Make executable and test
chmod +x scripts/start_all.sh
bash scripts/start_all.sh
Verify all services:

curl http://localhost:5001/health  # JIRA API
curl http://localhost:5002/health  # ServiceNow API
curl http://localhost:5003/health  # Splunk API
curl http://localhost:6001/health  # JIRA MCP
curl http://localhost:6002/health  # ServiceNow MCP
curl http://localhost:6003/health  # Splunk MCP
Acceptance Criteria:

✅ Script starts all 6 services
✅ All services respond to health checks
✅ PIDs saved for cleanup
✅ Clear output showing service URLs
Mark Complete: ⬜ → ✅

✅ Phase 2 Completion Checklist
Before proceeding to Phase 3, verify:

MCP Infrastructure
 MCP base classes created or SDK installed
 MCP protocol concepts understood (Tools, Resources)
JIRA MCP Server
 10 tools defined with proper schemas
 Server runs on port 6001
 Can list tools via /mcp/tools
 Can call tools via /mcp/call_tool
 All tools successfully call JIRA API
ServiceNow MCP Server
 4 tools defined
 Server runs on port 6002
 Can list and call tools
 Cross-tool linking works (jira_bug_key)
Splunk MCP Server
 3 tools defined
 Server runs on port 6003
 Can search logs via MCP
 Error log queries work
Testing & Scripts
 MCP server tests pass
 start_all.sh script works
 All 6 services can run simultaneously
Final Validation
Start all services:

bash scripts/start_all.sh
Run MCP tests:

pytest tests/test_mcp_servers.py -v
Test tool calling:

# JIRA: Get sprint summary
curl -X POST http://localhost:6001/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_sprint_summary", "arguments": {"sprint_name": "Sprint 23"}}'

# ServiceNow: List incidents
curl -X POST http://localhost:6002/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "list_incidents", "arguments": {"priority": "Critical"}}'

# Splunk: Get error logs
curl -X POST http://localhost:6003/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "get_error_logs", "arguments": {"limit": 5}}'
All commands should return successful responses.

🎉 Phase 2 Complete!
What We've Accomplished
✅ MCP base classes/SDK integrated
✅ JIRA MCP Server with 10 tools (port 6001)
✅ ServiceNow MCP Server with 4 tools (port 6002)
✅ Splunk MCP Server with 3 tools (port 6003)
✅ MCP protocol compliance (tools listing, calling)
✅ Automated MCP server tests
✅ Start script for all services
✅ Cross-tool correlation support

What's Next: Phase 3 - Build AI Agents
In Phase 3, you will:

Install and configure LiteLLM
Create Orchestrator Agent (routes to specialized agents)
Create JIRA Agent (uses JIRA MCP tools)
Create ServiceNow Agent (uses ServiceNow MCP tools)
Create Splunk Agent (uses Splunk MCP tools)
Create Context Manager (cross-tool correlation)
Test agent interactions
Architecture So Far
Mock APIs (5001-5003) ✅
    ↓
MCP Servers (6001-6003) ✅
    ↓
AI Agents (Next Phase) ⬜
    ↓
Main API Gateway ⬜
    ↓
React UI ⬜
Ready to Proceed?
# Verify Phase 2 complete
bash scripts/start_all.sh
pytest tests/test_mcp_servers.py -v
curl http://localhost:6001/mcp/tools | jq