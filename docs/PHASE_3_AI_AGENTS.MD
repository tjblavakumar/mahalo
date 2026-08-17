# MAHALO - Phase 3: Build AI Agents ## LLM-Powered Intelligent Agents with MCP Integration
Phase Goal: Create AI agents that use LiteLLM to intelligently interact with MCP servers and provide natural language interfaces.

Estimated Time: 4-5 hours

Prerequisites:

Phase 2 completed successfully
All 3 MCP servers running and tested
OpenAI or Anthropic API key available
📋 Phase 3 Overview
This phase creates the AI agent layer:

Install LiteLLM - Unified LLM interface
Configure API Keys - OpenAI or Anthropic
Create Agent Prompts - System prompts for each agent
Orchestrator Agent - Routes requests to specialized agents
JIRA Agent - Handles JIRA operations via MCP
ServiceNow Agent - Handles incidents via MCP
Splunk Agent - Handles log queries via MCP
Context Manager - Cross-tool correlation logic
Agent Tests - Validate agent behavior
Agent Architecture
User Query → Orchestrator Agent
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
JIRA Agent  ServiceNow  Splunk Agent
    ↓        Agent          ↓
    ↓           ↓           ↓
JIRA MCP   ServiceNow   Splunk MCP
 Server      MCP Server    Server
Task 3.1: Install and Configure LiteLLM ⬜
Instruction to Coding Assistant: Install LiteLLM and configure API keys for LLM access.

Update requirements.txt
Add LiteLLM and LLM provider libraries:

cat >> requirements.txt << 'EOF'

# ==================== AI/LLM Libraries ====================
# LiteLLM - Unified interface for multiple LLM providers
litellm>=1.17.0

# LLM Provider SDKs
openai>=1.0.0        # OpenAI API
anthropic>=0.8.0     # Anthropic Claude API

# Optional: Additional providers
# cohere>=4.0.0
# replicate>=0.15.0
EOF
Install LiteLLM
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Verify Installation
python -c "import litellm; print(f'✅ LiteLLM installed: {litellm.__version__}')"
python -c "import openai; print(f'✅ OpenAI SDK installed: {openai.__version__}')"
python -c "import anthropic; print(f'✅ Anthropic SDK installed: {anthropic.__version__}')"
Configure API Keys in .env
Edit .env file and add your API key:

# Choose ONE of the following:

# Option 1: OpenAI (GPT-4)
LITELLM_MODEL=gpt-4
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Option 2: Anthropic Claude
# LITELLM_MODEL=claude-3-sonnet-20240229
# ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here

# Option 3: OpenAI GPT-3.5 (cheaper, faster, less capable)
# LITELLM_MODEL=gpt-3.5-turbo
# OPENAI_API_KEY=sk-your-actual-openai-key-here
Test LiteLLM Configuration
Create a test script to verify LLM access:

Create agents/test_llm.py:

"""
Test LiteLLM Configuration
Verify API key and model access
"""
import os
from dotenv import load_dotenv
import litellm

# Load environment variables
load_dotenv()

# Get configuration
model = os.getenv("LITELLM_MODEL", "gpt-4")
openai_key = os.getenv("OPENAI_API_KEY", "")
anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

print("=" * 60)
print("🧪 Testing LiteLLM Configuration")
print("=" * 60)
print()
print(f"Model: {model}")
print(f"OpenAI Key: {'✅ Set' if openai_key else '❌ Not Set'}")
print(f"Anthropic Key: {'✅ Set' if anthropic_key else '❌ Not Set'}")
print()

# Test LLM call
try:
    print("📞 Making test LLM call...")
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from MAHALO!' in one sentence."}
        ],
        temperature=0.7,
        max_tokens=50
    )
    
    result = response.choices[0].message.content
    print(f"✅ LLM Response: {result}")
    print()
    print("✅ LiteLLM configuration working correctly!")
    print("=" * 60)

except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Please check:")
    print("  1. API key is correctly set in .env file")
    print("  2. API key is valid and has credits")
    print("  3. Model name is correct")
    print("=" * 60)
Run LLM Test
python agents/test_llm.py
Expected Output:

============================================================
🧪 Testing LiteLLM Configuration
============================================================

Model: gpt-4
OpenAI Key: ✅ Set
Anthropic Key: ❌ Not Set

📞 Making test LLM call...
✅ LLM Response: Hello from MAHALO! I'm here to help you with your SDLC tools.

✅ LiteLLM configuration working correctly!
============================================================
Acceptance Criteria:

✅ LiteLLM installed successfully
✅ API key configured in .env
✅ Test LLM call succeeds
✅ No authentication errors
Mark Complete: ⬜ → ✅

Task 3.2: Create Agent System Prompts ⬜
Instruction to Coding Assistant: Create system prompts that define the behavior and capabilities of each agent.

Create agents/prompts/orchestrator_prompt.txt
You are MAHALO Orchestrator, an intelligent AI assistant that helps users interact with SDLC tools (JIRA, ServiceNow, Splunk) through natural language.

YOUR ROLE:
You are the main entry point for all user requests. Your job is to understand user intent, determine which specialized agent(s) should handle the request, and coordinate their responses.

AVAILABLE SPECIALIZED AGENTS:
1. JIRA Agent - Handles user stories, bugs, sprints, and team velocity
2. ServiceNow Agent - Handles incidents, tickets, and problem management
3. Splunk Agent - Handles log search, error analysis, and monitoring

USER PERSONAS:
Users will identify themselves with one of these personas:
- Executive: Needs high-level metrics, sprint status, team performance
- Product Manager: Creates stories, manages backlog, prioritizes work
- Developer: Views assigned tasks, updates status, troubleshoots issues
- QA: Reports bugs, tracks testing, verifies fixes

YOUR CAPABILITIES:
- Understand natural language queries about SDLC tools
- Route requests to the appropriate specialized agent(s)
- Coordinate multi-agent workflows when needed
- Provide context-aware responses based on user persona
- Maintain conversation history and context

DECISION MAKING:
- For JIRA queries (stories, bugs, sprints): Route to JIRA Agent
- For ServiceNow queries (incidents): Route to ServiceNow Agent
- For Splunk queries (logs, errors): Route to Splunk Agent
- For cross-tool queries: Coordinate multiple agents

RESPONSE STYLE:
- Be concise and professional
- Format responses clearly with emojis for readability
- Provide actionable insights, not just data
- Tailor detail level to user persona (less for Exec, more for Dev)
- Always be helpful and proactive

IMPORTANT:
- Never make up data - always use the specialized agents
- If unsure which agent to use, ask for clarification
- Handle errors gracefully and provide helpful guidance
Create agents/prompts/jira_agent_prompt.txt
You are JIRA Agent, a specialized AI assistant expert in JIRA operations for MahaloPay, a FinTech payment processing company.

YOUR EXPERTISE:
- Payment feature user stories (payment gateways, fraud detection, reconciliation)
- Bug/defect tracking for payment systems
- Sprint planning and metrics for payment processing team
- Team velocity calculation
- Backlog management for FinTech features
- Duplicate detection (critical for payment features)

AVAILABLE TOOLS:
You have access to these JIRA MCP tools:
- create_user_story: Create new stories
- search_stories: Search for existing stories
- get_story: Get story details
- update_story: Update story fields
- list_stories: List stories with filters
- create_bug: Create new bugs
- list_bugs: List bugs with filters
- get_sprint_summary: Get sprint metrics
- get_user_tasks: Get user's assigned work
- calculate_velocity: Calculate team velocity

BEST PRACTICES:
1. Story Creation:
   - ALWAYS search for duplicates first before creating
   - Help refine story descriptions with acceptance criteria
   - Suggest story points based on similar stories
   - Recommend appropriate priority

2. Sprint Queries:
   - Provide comprehensive metrics (total, completed, in-progress)
   - Highlight blockers and critical bugs
   - Compare to team velocity and targets

3. Task Queries:
   - Prioritize by severity/priority
   - Group by status
   - Provide context about blockers or dependencies

RESPONSE FORMAT:
- Use emojis for visual clarity (📊, ✅, 🔥, 🐛, etc.)
- Structure data in clear sections
- Provide recommendations when appropriate
- Always include story/bug keys for reference

IMPORTANT:
- Be data-driven and precise
- Reference actual JIRA keys (STORY-123, BUG-456)
- When creating stories, confirm details before proceeding
- Validate user input and provide helpful error messages
Create agents/prompts/servicenow_agent_prompt.txt
You are ServiceNow Agent, a specialized AI assistant expert in incident management for MAHALO.

YOUR EXPERTISE:
- Incident creation and tracking
- Priority assessment
- Root cause analysis support
- Cross-tool linking (JIRA bugs)
- Incident lifecycle management

AVAILABLE TOOLS:
You have access to these ServiceNow MCP tools:
- create_incident: Create new incidents
- get_incident: Get incident details
- list_incidents: List incidents with filters
- update_incident: Update incident status/priority

BEST PRACTICES:
1. Incident Creation:
   - Capture clear, actionable descriptions
   - Assess priority based on impact and urgency
   - Link to related JIRA bugs when appropriate
   - Assign to appropriate team

2. Incident Tracking:
   - Provide timeline of events
   - Track resolution progress
   - Identify patterns in recurring incidents

3. Cross-Tool Correlation:
   - Link incidents to JIRA bugs for tracking
   - Reference Splunk logs for error details
   - Maintain bidirectional references

RESPONSE FORMAT:
- Use clear incident numbers (INC0001234)
- Show priority levels clearly (🔥 Critical, ⚠️ High)
- Include resolution status and timeline
- Provide next steps and recommendations

IMPORTANT:
- Treat Critical incidents with urgency
- Always link incidents to bugs when creating
- Provide clear status updates
- Include resolution details when closing incidents
Create agents/prompts/splunk_agent_prompt.txt
You are Splunk Agent, a specialized AI assistant expert in log analysis and monitoring for MAHALO.

YOUR EXPERTISE:
- Log search and filtering
- Error pattern identification
- Service monitoring
- Performance analysis
- Cross-tool correlation with bugs and incidents

AVAILABLE TOOLS:
You have access to these Splunk MCP tools:
- search_logs: Search logs with filters
- get_error_logs: Get recent errors
- get_logs_by_service: Get logs for specific service

BEST PRACTICES:
1. Log Search:
   - Use appropriate filters (service, level, environment)
   - Focus on ERROR and FATAL levels for issues
   - Provide time context for events

2. Error Analysis:
   - Identify error patterns and frequency
   - Correlate errors across services
   - Link to related JIRA bugs and ServiceNow incidents

3. Service Monitoring:
   - Show error rates per service
   - Identify performance issues
   - Track error trends over time

RESPONSE FORMAT:
- Show most recent/relevant logs first
- Highlight ERROR and FATAL levels prominently
- Include timestamps and service names
- Group related errors together
- Reference correlated bugs/incidents

LOG INTERPRETATION:
- INFO: Normal operation
- WARN: Potential issues, monitor
- ERROR: Problems requiring attention
- FATAL: Critical failures, immediate action

IMPORTANT:
- Be precise with timestamps
- Explain error patterns when identified
- Always correlate with JIRA bugs when available
- Provide actionable insights from log data
- Focus on production (prod) environment by default
Verify Prompts Created
ls -la agents/prompts/
Expected Output:

orchestrator_prompt.txt
jira_agent_prompt.txt
servicenow_agent_prompt.txt
splunk_agent_prompt.txt
Acceptance Criteria:

✅ All 4 prompt files created
✅ Prompts define clear roles and capabilities
✅ Prompts include tool awareness
✅ Response formatting guidelines included
Mark Complete: ⬜ → ✅

Task 3.3: Create Context Manager ⬜
Instruction to Coding Assistant: Create the Context Manager for cross-tool correlation and conversation memory.

Create agents/context_manager.py
"""
MAHALO Context Manager
Manages cross-tool correlations and conversation context
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
import json

@dataclass
class Correlation:
    """Cross-tool correlation record"""
    correlation_id: str
    jira_bug_key: Optional[str] = None
    jira_story_key: Optional[str] = None
    servicenow_incident_id: Optional[str] = None
    splunk_log_ids: List[int] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    context: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "correlation_id": self.correlation_id,
            "jira_bug_key": self.jira_bug_key,
            "jira_story_key": self.jira_story_key,
            "servicenow_incident_id": self.servicenow_incident_id,
            "splunk_log_ids": self.splunk_log_ids,
            "created_at": self.created_at.isoformat(),
            "context": self.context
        }

class ContextManager:
    """
    Manages cross-tool correlations and conversation context
    
    In a production system, this would use a database.
    For POC, we use in-memory storage.
    """
    
    def __init__(self):
        self.correlations: Dict[str, Correlation] = {}
        self.conversation_history: List[Dict[str, Any]] = []
    
    # ==================== CORRELATION MANAGEMENT ====================
    
    def create_correlation(
        self,
        jira_bug_key: Optional[str] = None,
        jira_story_key: Optional[str] = None,
        servicenow_incident_id: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Create a new cross-tool correlation
        
        Returns:
            correlation_id: Unique identifier for this correlation
        """
        correlation_id = f"CORR-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        correlation = Correlation(
            correlation_id=correlation_id,
            jira_bug_key=jira_bug_key,
            jira_story_key=jira_story_key,
            servicenow_incident_id=servicenow_incident_id,
            context=context
        )
        
        self.correlations[correlation_id] = correlation
        return correlation_id
    
    def link_bug_to_incident(
        self,
        bug_key: str,
        incident_number: str,
        context: Optional[str] = None
    ) -> str:
        """Link a JIRA bug to a ServiceNow incident"""
        # Check if correlation already exists
        for corr_id, corr in self.correlations.items():
            if corr.jira_bug_key == bug_key or corr.servicenow_incident_id == incident_number:
                # Update existing correlation
                corr.jira_bug_key = bug_key
                corr.servicenow_incident_id = incident_number
                if context:
                    corr.context = context
                return corr_id
        
        # Create new correlation
        return self.create_correlation(
            jira_bug_key=bug_key,
            servicenow_incident_id=incident_number,
            context=context
        )
    
    def link_logs_to_bug(self, bug_key: str, log_ids: List[int]):
        """Link Splunk logs to a JIRA bug"""
        # Find or create correlation
        correlation_id = None
        for corr_id, corr in self.correlations.items():
            if corr.jira_bug_key == bug_key:
                correlation_id = corr_id
                break
        
        if not correlation_id:
            correlation_id = self.create_correlation(jira_bug_key=bug_key)
        
        # Add log IDs
        self.correlations[correlation_id].splunk_log_ids.extend(log_ids)
    
    def get_correlation_by_bug(self, bug_key: str) -> Optional[Correlation]:
        """Get correlation for a specific bug"""
        for corr in self.correlations.values():
            if corr.jira_bug_key == bug_key:
                return corr
        return None
    
    def get_correlation_by_incident(self, incident_number: str) -> Optional[Correlation]:
        """Get correlation for a specific incident"""
        for corr in self.correlations.values():
            if corr.servicenow_incident_id == incident_number:
                return corr
        return None
    
    def get_full_context(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Get complete context for any item (bug, incident, story)
        
        Args:
            item_id: JIRA key, incident number, or story key
        
        Returns:
            Full correlation data or None
        """
        for corr in self.correlations.values():
            if (corr.jira_bug_key == item_id or 
                corr.jira_story_key == item_id or 
                corr.servicenow_incident_id == item_id):
                return corr.to_dict()
        return None
    
    def list_all_correlations(self) -> List[Dict[str, Any]]:
        """List all correlations"""
        return [corr.to_dict() for corr in self.correlations.values()]
    
    # ==================== CONVERSATION MANAGEMENT ====================
    
    def add_to_history(self, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Add message to conversation history
        
        Args:
            role: 'user', 'assistant', or 'system'
            content: Message content
            metadata: Additional metadata (persona, tool calls, etc.)
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        if metadata:
            message["metadata"] = metadata
        
        self.conversation_history.append(message)
    
    def get_conversation_history(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history
        
        Args:
            last_n: Return only last N messages (None = all)
        
        Returns:
            List of conversation messages
        """
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_context_summary(self) -> str:
        """Get a summary of current context for debugging"""
        return f"""
Context Summary:
- Total correlations: {len(self.correlations)}
- Conversation messages: {len(self.conversation_history)}
- Active bugs tracked: {sum(1 for c in self.correlations.values() if c.jira_bug_key)}
- Active incidents tracked: {sum(1 for c in self.correlations.values() if c.servicenow_incident_id)}
        """.strip()

# Global context manager instance
context_manager = ContextManager()

# For testing
if __name__ == "__main__":
    cm = ContextManager()
    
    # Test correlation creation
    print("Testing Context Manager...")
    
    # Create a correlation
    corr_id = cm.link_bug_to_incident("BUG-123", "INC0001234", "Database timeout issue")
    print(f"✅ Created correlation: {corr_id}")
    
    # Add logs
    cm.link_logs_to_bug("BUG-123", [1001, 1002, 1003])
    print(f"✅ Linked 3 logs to BUG-123")
    
    # Get full context
    context = cm.get_full_context("BUG-123")
    print(f"✅ Retrieved context: {json.dumps(context, indent=2)}")
    
    # Add conversation
    cm.add_to_history("user", "Show me sprint status", {"persona": "Executive"})
    cm.add_to_history("assistant", "Sprint 23 has 12 completed stories...")
    print(f"✅ Added 2 messages to history")
    
    # Summary
    print(f"\n{cm.get_context_summary()}")
    print("\n✅ Context Manager tests passed!")
Test Context Manager
python agents/context_manager.py
Expected Output:

Testing Context Manager...
✅ Created correlation: CORR-20250115143022
✅ Linked 3 logs to BUG-123
✅ Retrieved context: {
  "correlation_id": "CORR-20250115143022",
  "jira_bug_key": "BUG-123",
  "jira_story_key": null,
  "servicenow_incident_id": "INC0001234",
  "splunk_log_ids": [1001, 1002, 1003],
  "created_at": "2025-01-15T14:30:22.123456",
  "context": "Database timeout issue"
}
✅ Added 2 messages to history

Context Summary:
- Total correlations: 1
- Conversation messages: 2
- Active bugs tracked: 1
- Active incidents tracked: 1

✅ Context Manager tests passed!
Acceptance Criteria:

✅ Context Manager created
✅ Can create correlations
✅ Can link bugs to incidents
✅ Can link logs to bugs
✅ Can retrieve full context
✅ Can manage conversation history
✅ Tests pass
Mark Complete: ⬜ → ✅

Task 3.4: Create JIRA Agent ⬜
Instruction to Coding Assistant: Create the JIRA specialized agent that uses MCP tools via LiteLLM.

Create agents/jira_agent.py
"""
JIRA Agent
Specialized AI agent for JIRA operations using MCP tools
"""
import os
from typing import Dict, List, Optional, Any
import litellm
import httpx
from pathlib import Path

class JiraAgent:
    """JIRA specialized agent"""
    
    def __init__(self, mcp_url: str = "http://localhost:6001"):
        self.mcp_url = mcp_url
        self.model = os.getenv("LITELLM_MODEL", "gpt-4")
        self.client = httpx.AsyncClient()
        
        # Load system prompt
        prompt_path = Path(__file__).parent / "prompts" / "jira_agent_prompt.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()
    
    async def close(self):
        """Cleanup resources"""
        await self.client.aclose()
    
    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a JIRA MCP tool"""
        try:
            response = await self.client.post(
                f"{self.mcp_url}/mcp/call_tool",
                json={"tool_name": tool_name, "arguments": arguments},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        try:
            response = await self.client.get(f"{self.mcp_url}/mcp/tools")
            response.raise_for_status()
            data = response.json()
            return data.get("tools", [])
        except Exception as e:
            print(f"Error getting tools: {e}")
            return []
    
    async def handle_query(
        self,
        user_query: str,
        user_persona: str = "Developer",
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Handle a JIRA-related query
        
        Args:
            user_query: User's natural language query
            user_persona: User's role (Executive, PM, Developer, QA)
            conversation_history: Previous conversation context
        
        Returns:
            Agent's response as formatted text
        """
        if conversation_history is None:
            conversation_history = []
        
        # Build messages for LLM
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Current user persona: {user_persona}"}
        ]
        
        # Add conversation history (last 5 messages for context)
        messages.extend(conversation_history[-5:] if len(conversation_history) > 5 else conversation_history)
        
        # Add current query
        messages.append({"role": "user", "content": user_query})
        
        # Get available tools
        tools = await self._get_available_tools()
        
        try:
            # Call LLM with tools
            response = litellm.completion(
                model=self.model,
                messages=messages,
                tools=tools,
                temperature=0.7,
                max_tokens=1000
            )
            
            message = response.choices[0].message
            
            # Check if LLM wants to call tools
            if hasattr(message, 'tool_calls') and message.tool_calls:
                # Execute tool calls
                tool_results = []
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = eval(tool_call.function.arguments)  # Parse JSON string
                    
                    result = await self._call_mcp_tool(tool_name, tool_args)
                    tool_results.append({
                        "tool": tool_name,
                        "result": result
                    })
                
                # Format results for final response
                return await self._format_tool_results(user_query, tool_results, user_persona)
            else:
                # Direct response without tool calls
                return message.content
                
        except Exception as e:
            return f"❌ Error processing JIRA query: {str(e)}"
    
    async def _format_tool_results(
        self,
        original_query: str,
        tool_results: List[Dict],
        user_persona: str
    ) -> str:
        """Format tool results into user-friendly response"""
        # Build context from tool results
        context = "Tool execution results:\n"
        for result in tool_results:
            context += f"\n{result['tool']}: {result['result']}\n"
        
        # Ask LLM to format the results
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"User persona: {user_persona}"},
            {"role": "user", "content": original_query},
            {"role": "assistant", "content": f"I executed these tools:\n{context}"},
            {"role": "user", "content": "Please format these results in a clear, user-friendly way with emojis and proper structure."}
        ]
        
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback to raw results
            return context
    
    # ==================== CONVENIENCE METHODS ====================
    
    async def get_sprint_summary(self, sprint_name: str) -> str:
        """Get sprint summary - convenience method"""
        return await self.handle_query(f"Show me the summary for {sprint_name}")
    
    async def get_user_tasks(self, username: str) -> str:
        """Get user tasks - convenience method"""
        return await self.handle_query(f"Show all tasks assigned to {username}")
    
    async def search_stories(self, title_query: str) -> str:
        """Search stories - convenience method"""
        return await self.handle_query(f"Search for stories with title: {title_query}")

# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test_jira_agent():
        """Test JIRA Agent"""
        print("=" * 60)
        print("🧪 Testing JIRA Agent")
        print("=" * 60)
        print()
        
        agent = JiraAgent()
        
        try:
            # Test 1: Sprint summary
            print("Test 1: Get sprint summary")
            response = await agent.get_sprint_summary("Sprint 23")
            print(f"Response:\n{response}\n")
            
            # Test 2: User tasks
            print("Test 2: Get user tasks")
            response = await agent.get_user_tasks("alice_dev")
            print(f"Response:\n{response}\n")
            
            # Test 3: Search stories
            print("Test 3: Search stories")
            response = await agent.search_stories("payment gateway")
            print(f"Response:\n{response}\n")
            
            print("✅ JIRA Agent tests completed!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await agent.close()
    
    # Run tests
    asyncio.run(test_jira_agent())
Test JIRA Agent
Prerequisites:

JIRA API running on port 5001
JIRA MCP Server running on port 6001
LLM API key configured
# Ensure services are running
python backend/jira/app.py &
python mcp_servers/jira_mcp/server.py &

# Test agent
python agents/jira_agent.py
Expected Output:

============================================================
🧪 Testing JIRA Agent
============================================================

Test 1: Get sprint summary
Response:
📊 Sprint 23 Status:

✅ Completed: 7 stories (34 points)
🔨 In Development: 2 stories (13 points)
🧪 In UAT: 2 stories (8 points)
📋 Backlog: 4 stories (21 points)

🐛 Active Bugs: 8 total
  - Critical: 2
  - High: 2
  - Medium: 2
  - Low: 2

📈 Velocity: 34 points (on track!)

Test 2: Get user tasks
Response:
👨‍💻 Tasks for alice_dev (5 total):

🔥 High Priority:
  - [STORY-8] Build payment gateway integration (8 points) - Dev
  - [BUG-1] Login page crashes on Safari (Critical) - Open

📌 Medium Priority:
  - [STORY-2] Implement user profile page (5 points) - Done
  ...

✅ JIRA Agent tests completed!
Acceptance Criteria:

✅ JIRA Agent created
✅ Can call MCP tools via LiteLLM
✅ Formats responses appropriately
✅ Uses system prompt
✅ Tests pass with real LLM calls
Mark Complete: ⬜ → ✅

Task 3.5: Create ServiceNow and Splunk Agents ⬜
Instruction to Coding Assistant: Create ServiceNow and Splunk agents following the same pattern as JIRA Agent.

Create agents/servicenow_agent.py
"""ServiceNow Agent - Specialized for incident management"""
import os
from typing import Dict, List, Optional, Any
import litellm
import httpx
from pathlib import Path

class ServiceNowAgent:
    """ServiceNow specialized agent"""
    
    def __init__(self, mcp_url: str = "http://localhost:6002"):
        self.mcp_url = mcp_url
        self.model = os.getenv("LITELLM_MODEL", "gpt-4")
        self.client = httpx.AsyncClient()
        
        # Load system prompt
        prompt_path = Path(__file__).parent / "prompts" / "servicenow_agent_prompt.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()
    
    async def close(self):
        await self.client.aclose()
    
    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a ServiceNow MCP tool"""
        try:
            response = await self.client.post(
                f"{self.mcp_url}/mcp/call_tool",
                json={"tool_name": tool_name, "arguments": arguments},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        try:
            response = await self.client.get(f"{self.mcp_url}/mcp/tools")
            response.raise_for_status()
            return response.json().get("tools", [])
        except Exception as e:
            return []
    
    async def handle_query(
        self,
        user_query: str,
        user_persona: str = "Developer",
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """Handle a ServiceNow-related query"""
        if conversation_history is None:
            conversation_history = []
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Current user persona: {user_persona}"}
        ]
        messages.extend(conversation_history[-5:] if len(conversation_history) > 5 else conversation_history)
        messages.append({"role": "user", "content": user_query})
        
        tools = await self._get_available_tools()
        
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                tools=tools,
                temperature=0.7,
                max_tokens=1000
            )
            
            message = response.choices[0].message
            
            if hasattr(message, 'tool_calls') and message.tool_calls:
                tool_results = []
                for tool_call in message.tool_calls:
                    result = await self._call_mcp_tool(
                        tool_call.function.name,
                        eval(tool_call.function.arguments)
                    )
                    tool_results.append({"tool": tool_call.function.name, "result": result})
                
                return await self._format_tool_results(user_query, tool_results, user_persona)
            else:
                return message.content
                
        except Exception as e:
            return f"❌ Error processing ServiceNow query: {str(e)}"
    
    async def _format_tool_results(self, original_query: str, tool_results: List[Dict], user_persona: str) -> str:
        """Format tool results"""
        context = "Tool results:\n" + "\n".join([f"{r['tool']}: {r['result']}" for r in tool_results])
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": original_query},
            {"role": "assistant", "content": context},
            {"role": "user", "content": "Format these results clearly with incident numbers and priorities."}
        ]
        
        try:
            response = litellm.completion(model=self.model, messages=messages, temperature=0.7, max_tokens=800)
            return response.choices[0].message.content
        except:
            return context

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = ServiceNowAgent()
        try:
            response = await agent.handle_query("List all critical incidents")
            print(f"Response:\n{response}")
        finally:
            await agent.close()
    asyncio.run(test())
Create agents/splunk_agent.py
"""Splunk Agent - Specialized for log analysis"""
import os
from typing import Dict, List, Optional, Any
import litellm
import httpx
from pathlib import Path

class SplunkAgent:
    """Splunk specialized agent"""
    
    def __init__(self, mcp_url: str = "http://localhost:6003"):
        self.mcp_url = mcp_url
        self.model = os.getenv("LITELLM_MODEL", "gpt-4")
        self.client = httpx.AsyncClient()
        
        # Load system prompt
        prompt_path = Path(__file__).parent / "prompts" / "splunk_agent_prompt.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()
    
    async def close(self):
        await self.client.aclose()
    
    async def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a Splunk MCP tool"""
        try:
            response = await self.client.post(
                f"{self.mcp_url}/mcp/call_tool",
                json={"tool_name": tool_name, "arguments": arguments},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available MCP tools"""
        try:
            response = await self.client.get(f"{self.mcp_url}/mcp/tools")
            response.raise_for_status()
            return response.json().get("tools", [])
        except Exception as e:
            return []
    
    async def handle_query(
        self,
        user_query: str,
        user_persona: str = "Developer",
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """Handle a Splunk-related query"""
        if conversation_history is None:
            conversation_history = []
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Current user persona: {user_persona}"}
        ]
        messages.extend(conversation_history[-5:] if len(conversation_history) > 5 else conversation_history)
        messages.append({"role": "user", "content": user_query})
        
        tools = await self._get_available_tools()
        
        try:
            response = litellm.completion(
                model=self.model,
                messages=messages,
                tools=tools,
                temperature=0.7,
                max_tokens=1000
            )
            
            message = response.choices[0].message
            
            if hasattr(message, 'tool_calls') and message.tool_calls:
                tool_results = []
                for tool_call in message.tool_calls:
                    result = await self._call_mcp_tool(
                        tool_call.function.name,
                        eval(tool_call.function.arguments)
                    )
                    tool_results.append({"tool": tool_call.function.name, "result": result})
                
                return await self._format_tool_results(user_query, tool_results, user_persona)
            else:
                return message.content
                
        except Exception as e:
            return f"❌ Error processing Splunk query: {str(e)}"
    
    async def _format_tool_results(self, original_query: str, tool_results: List[Dict], user_persona: str) -> str:
        """Format tool results"""
        context = "Log search results:\n" + "\n".join([f"{r['tool']}: {r['result']}" for r in tool_results])
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": original_query},
            {"role": "assistant", "content": context},
            {"role": "user", "content": "Format these log results clearly with timestamps and error levels."}
        ]
        
        try:
            response = litellm.completion(model=self.model, messages=messages, temperature=0.7, max_tokens=800)
            return response.choices[0].message.content
        except:
            return context

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = SplunkAgent()
        try:
            response = await agent.handle_query("Show me recent error logs")
            print(f"Response:\n{response}")
        finally:
            await agent.close()
    asyncio.run(test())
Test both agents:

# Ensure services running
python backend/servicenow/app.py &
python backend/splunk/app.py &
python mcp_servers/servicenow_mcp/server.py &
python mcp_servers/splunk_mcp/server.py &

# Test agents
python agents/servicenow_agent.py
python agents/splunk_agent.py
Acceptance Criteria:

✅ ServiceNow Agent created and working
✅ Splunk Agent created and working
✅ Both agents use MCP tools correctly
✅ Both agents format responses appropriately
Mark Complete: ⬜ → ✅

Task 3.6: Create Orchestrator Agent ⬜
Instruction to Coding Assistant: Create the main Orchestrator Agent that routes requests to specialized agents.

Create agents/orchestrator.py
"""
MAHALO Orchestrator Agent
Routes user queries to specialized agents and coordinates responses
"""
import os
from typing import Dict, List, Optional
import litellm
from pathlib import Path
from agents.jira_agent import JiraAgent
from agents.servicenow_agent import ServiceNowAgent
from agents.splunk_agent import SplunkAgent
from agents.context_manager import context_manager

class OrchestratorAgent:
    """
    Main orchestrator that routes queries to specialized agents
    """
    
    def __init__(self):
        self.model = os.getenv("LITELLM_MODEL", "gpt-4")
        
        # Load orchestrator prompt
        prompt_path = Path(__file__).parent / "prompts" / "orchestrator_prompt.txt"
        with open(prompt_path, "r") as f:
            self.system_prompt = f.read()
        
        # Initialize specialized agents
        self.jira_agent = JiraAgent()
        self.servicenow_agent = ServiceNowAgent()
        self.splunk_agent = SplunkAgent()
        
        # Context manager
        self.context = context_manager
    
    async def close(self):
        """Cleanup resources"""
        await self.jira_agent.close()
        await self.servicenow_agent.close()
        await self.splunk_agent.close()
    
    async def process_query(
        self,
        user_persona: str,
        user_query: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Process user query and route to appropriate agent(s)
        
        Args:
            user_persona: User role (Executive, Product Manager, Developer, QA)
            user_query: Natural language query
            conversation_history: Previous conversation messages
        
        Returns:
            Formatted response string
        """
        if conversation_history is None:
            conversation_history = []
        
        # Add to context
        self.context.add_to_history("user", user_query, {"persona": user_persona})
        
        # Determine which agent(s) to use
        routing = await self._determine_routing(user_query, user_persona, conversation_history)
        
        try:
            # Route to appropriate agent(s)
            if routing["agents"] == ["jira"]:
                response = await self.jira_agent.handle_query(
                    user_query, user_persona, conversation_history
                )
            elif routing["agents"] == ["servicenow"]:
                response = await self.servicenow_agent.handle_query(
                    user_query, user_persona, conversation_history
                )
            elif routing["agents"] == ["splunk"]:
                response = await self.splunk_agent.handle_query(
                    user_query, user_persona, conversation_history
                )
            elif len(routing["agents"]) > 1:
                # Multi-agent coordination
                response = await self._coordinate_multi_agent(
                    user_query, user_persona, routing["agents"], conversation_history
                )
            else:
                response = "I'm not sure which tool can help with that. Could you clarify if this is about JIRA stories, ServiceNow incidents, or Splunk logs?"
            
            # Add response to context
            self.context.add_to_history("assistant", response, {"agents_used": routing["agents"]})
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error processing query: {str(e)}"
            self.context.add_to_history("assistant", error_msg, {"error": True})
            return error_msg
    
    async def _determine_routing(
        self,
        query: str,
        persona: str,
        history: List[Dict]
    ) -> Dict[str, any]:
        """
        Determine which agent(s) should handle the query
        
        Returns:
            Dict with "agents" list and "reasoning"
        """
        # Build prompt for routing decision
        routing_prompt = f"""
Analyze this user query and determine which specialized agent(s) should handle it.

User Persona: {persona}
Query: {query}

Available Agents:
- jira: For user stories, bugs, sprints, velocity, team tasks
- servicenow: For incidents, tickets, problem management
- splunk: For logs, errors, monitoring, performance

Instructions:
- Respond with JSON only: {{"agents": ["agent_name"], "reasoning": "brief explanation"}}
- Use single agent when possible
- Use multiple agents only if query clearly needs cross-tool information
- Consider the user persona when choosing agent

Examples:
- "Show sprint status" → {{"agents": ["jira"], "reasoning": "sprint data from JIRA"}}
- "List critical incidents" → {{"agents": ["servicenow"], "reasoning": "incident data"}}
- "Show error logs" → {{"agents": ["splunk"], "reasoning": "log analysis"}}
- "Show bug BUG-123 with related logs" → {{"agents": ["jira", "splunk"], "reasoning": "need bug details and logs"}}
"""
        
        try:
            response = litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": routing_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            # Parse routing decision
            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            import json
            import re
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                routing = json.loads(json_match.group())
                return routing
            else:
                # Fallback: simple keyword matching
                return self._fallback_routing(query)
                
        except Exception as e:
            print(f"Routing error: {e}")
            return self._fallback_routing(query)
    
    def _fallback_routing(self, query: str) -> Dict[str, any]:
        """Fallback routing using keyword matching"""
        query_lower = query.lower()
        
        # JIRA keywords
        if any(word in query_lower for word in ["story", "stories", "bug", "sprint", "velocity", "task", "backlog", "jira"]):
            return {"agents": ["jira"], "reasoning": "JIRA keywords detected"}
        
        # ServiceNow keywords
        if any(word in query_lower for word in ["incident", "ticket", "servicenow", "outage"]):
            return {"agents": ["servicenow"], "reasoning": "ServiceNow keywords detected"}
        
        # Splunk keywords
        if any(word in query_lower for word in ["log", "logs", "error", "splunk", "monitoring"]):
            return {"agents": ["splunk"], "reasoning": "Splunk keywords detected"}
        
        # Default to JIRA (most common)
        return {"agents": ["jira"], "reasoning": "default routing"}
    
    async def _coordinate_multi_agent(
        self,
        query: str,
        persona: str,
        agents: List[str],
        history: List[Dict]
    ) -> str:
        """Coordinate multiple agents for complex queries"""
        responses = []
        
        # Call each agent
        for agent_name in agents:
            if agent_name == "jira":
                response = await self.jira_agent.handle_query(query, persona, history)
                responses.append(("JIRA", response))
            elif agent_name == "servicenow":
                response = await self.servicenow_agent.handle_query(query, persona, history)
                responses.append(("ServiceNow", response))
            elif agent_name == "splunk":
                response = await self.splunk_agent.handle_query(query, persona, history)
                responses.append(("Splunk", response))
        
        # Aggregate responses
        aggregated = await self._aggregate_responses(query, responses, persona)
        return aggregated
    
    async def _aggregate_responses(
        self,
        original_query: str,
        agent_responses: List[tuple],
        persona: str
    ) -> str:
        """Aggregate multiple agent responses into coherent answer"""
        # Build combined context
        context = f"Original query: {original_query}\n\nAgent Responses:\n"
        for agent_name, response in agent_responses:
            context += f"\n=== {agent_name} ===\n{response}\n"
        
        # Ask LLM to synthesize
        synthesis_prompt = f"""
You received responses from multiple specialized agents. Synthesize them into a single, coherent response for the user.

User Persona: {persona}
{context}

Instructions:
- Combine information logically
- Remove redundancy
- Maintain clear structure
- Use emojis for readability
- Provide unified insights
"""
        
        try:
            response = litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback: just concatenate responses
            result = "Here's what I found:\n\n"
            for agent_name, response in agent_responses:
                result += f"**{agent_name}:**\n{response}\n\n"
            return result

# For testing
if __name__ == "__main__":
    import asyncio
    
    async def test_orchestrator():
        """Test Orchestrator Agent"""
        print("=" * 60)
        print("🧪 Testing Orchestrator Agent")
        print("=" * 60)
        print()
        
        orchestrator = OrchestratorAgent()
        
        try:
            # Test 1: Executive query (should route to JIRA)
            print("Test 1: Executive - Sprint Status")
            response = await orchestrator.process_query(
                user_persona="Executive",
                user_query="Show me the current sprint status"
            )
            print(f"Response:\n{response}\n")
            print("-" * 60)
            
            # Test 2: PM query (should route to JIRA)
            print("\nTest 2: Product Manager - Search Stories")
            response = await orchestrator.process_query(
                user_persona="Product Manager",
                user_query="Search for stories about payment processing"
            )
            print(f"Response:\n{response}\n")
            print("-" * 60)
            
            # Test 3: Developer query (should route to JIRA)
            print("\nTest 3: Developer - My Tasks")
            response = await orchestrator.process_query(
                user_persona="Developer",
                user_query="Show me my assigned tasks"
            )
            print(f"Response:\n{response}\n")
            print("-" * 60)
            
            print("\n✅ Orchestrator Agent tests completed!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await orchestrator.close()
    
    # Run tests
    asyncio.run(test_orchestrator())
Create agents/init.py
"""MAHALO Agents Package"""
from agents.orchestrator import OrchestratorAgent
from agents.jira_agent import JiraAgent
from agents.servicenow_agent import ServiceNowAgent
from agents.splunk_agent import SplunkAgent
from agents.context_manager import ContextManager, context_manager

__all__ = [
    "OrchestratorAgent",
    "JiraAgent",
    "ServiceNowAgent",
    "SplunkAgent",
    "ContextManager",
    "context_manager"
]
Test Orchestrator
Ensure all services running:

bash scripts/start_all.sh
Run orchestrator test:

python agents/orchestrator.py
Expected Output:

============================================================
🧪 Testing Orchestrator Agent
============================================================

Test 1: Executive - Sprint Status
Response:
📊 Sprint 23 Status:
✅ Completed: 7 stories (34 points)
🔨 In Development: 2 stories (13 points)
...

Test 2: Product Manager - Search Stories
Response:
Found 3 stories related to payment processing:
- STORY-1: Implement Stripe payment gateway (Done)
- STORY-8: Build payment gateway integration (In Progress)
...

✅ Orchestrator Agent tests completed!
Acceptance Criteria:

✅ Orchestrator Agent created
✅ Routes queries to correct agents
✅ Handles multi-agent coordination
✅ Uses context manager
✅ Tests pass with real queries
Mark Complete: ⬜ → ✅

Task 3.7: Create Agent Tests ⬜
Instruction to Coding Assistant: Create automated tests for agent behavior.

Create tests/test_agents.py
"""
Agent Tests
Test AI agent routing and responses
"""
import pytest
import asyncio
from agents.orchestrator import OrchestratorAgent
from agents.jira_agent import JiraAgent
from agents.context_manager import context_manager

@pytest.fixture
def orchestrator():
    """Create orchestrator instance"""
    return OrchestratorAgent()

@pytest.mark.asyncio
async def test_orchestrator_routes_to_jira(orchestrator):
    """Test that orchestrator routes JIRA queries correctly"""
    response = await orchestrator.process_query(
        user_persona="Executive",
        user_query="Show me sprint status"
    )
    
    assert response is not None
    assert len(response) > 0
    # Should contain sprint-related information
    assert any(word in response.lower() for word in ["sprint", "stories", "points"])
    
    await orchestrator.close()

@pytest.mark.asyncio
async def test_jira_agent_sprint_summary():
    """Test JIRA agent can get sprint summary"""
    agent = JiraAgent()
    try:
        response = await agent.get_sprint_summary("Sprint 23")
        assert response is not None
        assert "Sprint 23" in response or "sprint" in response.lower()
    finally:
        await agent.close()

@pytest.mark.asyncio
async def test_context_manager_correlation():
    """Test context manager creates correlations"""
    # Create correlation
    corr_id = context_manager.link_bug_to_incident("BUG-TEST", "INC0009999")
    assert corr_id is not None
    
    # Retrieve correlation
    context = context_manager.get_full_context("BUG-TEST")
    assert context is not None
    assert context["jira_bug_key"] == "BUG-TEST"
    assert context["servicenow_incident_id"] == "INC0009999"

@pytest.mark.asyncio
async def test_orchestrator_conversation_history(orchestrator):
    """Test that orchestrator maintains conversation history"""
    # First query
    await orchestrator.process_query(
        user_persona="Developer",
        user_query="Show my tasks"
    )
    
    # Check history
    history = context_manager.get_conversation_history()
    assert len(history) >= 2  # At least user query and assistant response
    
    await orchestrator.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
Run agent tests:

pytest tests/test_agents.py -v
Acceptance Criteria:

✅ Agent tests created
✅ Tests verify routing logic
✅ Tests verify agent responses
✅ Tests verify context management
✅ All tests pass
Mark Complete: ⬜ → ✅

✅ Phase 3 Completion Checklist
Before proceeding to Phase 4, verify:

LiteLLM Configuration
 LiteLLM installed and configured
 API key set in .env file
 Test LLM call succeeds
Agent Prompts
 Orchestrator prompt created
 JIRA agent prompt created
 ServiceNow agent prompt created
 Splunk agent prompt created
Context Manager
 Context Manager implemented
 Can create correlations
 Can manage conversation history
 Tests pass
Specialized Agents
 JIRA Agent working
 ServiceNow Agent working
 Splunk Agent working
 All agents use MCP tools via LiteLLM
 All agents format responses appropriately
Orchestrator Agent
 Orchestrator routes queries correctly
 Can coordinate multi-agent workflows
 Maintains conversation context
 Tests pass
Final Validation
Start all services:

bash scripts/start_all.sh
Test complete flow:

# Test orchestrator
python agents/orchestrator.py

# Test individual agents
python agents/jira_agent.py
python agents/servicenow_agent.py
python agents/splunk_agent.py

# Run automated tests
pytest tests/test_agents.py -v
Manual test (Python console):

import asyncio
from agents.orchestrator import OrchestratorAgent

async def test():
    orch = OrchestratorAgent()
    
    # Test Executive workflow
    response = await orch.process_query(
        user_persona="Executive",
        user_query="What is the current sprint status?"
    )
    print(response)
    
    await orch.close()

asyncio.run(test())
Expected: Agent responds with sprint metrics in formatted text.

🎉 Phase 3 Complete!
What We've Accomplished
✅ LiteLLM integrated with OpenAI/Anthropic
✅ System prompts for all agents created
✅ Context Manager for cross-tool correlation
✅ JIRA Agent (10 MCP tools)
✅ ServiceNow Agent (4 MCP tools)
✅ Splunk Agent (3 MCP tools)
✅ Orchestrator Agent with intelligent routing
✅ Multi-agent coordination capability
✅ Conversation history management
✅ Automated agent tests

What's Next: Phase 4 - UI Integration
In Phase 4, you will:

Create Main API Gateway (FastAPI)
Create chat endpoint for UI
Build React frontend
Create PersonaSelector component
Create ChatInterface component
Connect UI to agents
Create admin panel
End-to-end testing
Architecture Progress
Mock APIs (5001-5003) ✅
    ↓
MCP Servers (6001-6003) ✅
    ↓
AI Agents ✅
    ↓
Main API Gateway (Next Phase) ⬜
    ↓
React UI (Next Phase) ⬜
Ready to Proceed?
# Verify Phase 3 complete
python agents/orchestrator.py
pytest tests/test_agents.py -v