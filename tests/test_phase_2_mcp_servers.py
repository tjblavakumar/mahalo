import asyncio

from mcp_servers.mcp_base import MCPServer, MCPTool
from mcp_servers.jira_mcp.tools import JiraMCPTools
from mcp_servers.servicenow_mcp.tools import ServiceNowMCPTools
from mcp_servers.splunk_mcp.tools import SplunkMCPTools


def test_mcp_base_registration():
    server = MCPServer("test-server")
    tool = MCPTool(name="demo_tool", description="Demo tool", input_schema={"type": "object", "properties": {}})
    server.register_tool(tool)
    assert tool.name in server.tools
    assert server.list_tools()[0]["function"]["name"] == "demo_tool"


def test_jira_mcp_tools_object():
    tools = JiraMCPTools()
    assert hasattr(tools, "create_story_handler")
    assert hasattr(tools, "get_story_handler")


def test_servicenow_mcp_tools_object():
    tools = ServiceNowMCPTools()
    assert hasattr(tools, "list_incidents_handler")
    assert hasattr(tools, "get_incident_handler")


def test_splunk_mcp_tools_object():
    tools = SplunkMCPTools()
    assert hasattr(tools, "search_logs_handler")
    assert hasattr(tools, "list_logs_handler")
