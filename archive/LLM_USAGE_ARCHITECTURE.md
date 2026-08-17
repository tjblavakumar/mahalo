# LLM Usage in MAHALO Architecture

## Summary: LLM is Only Used by Orchestrator

**Short Answer:** Only the **Orchestrator Agent** uses the LLM. The individual specialist agents (JIRA, ServiceNow, Splunk) use **rule-based logic** and do NOT call the LLM.

## Detailed Architecture

### 🎯 Orchestrator Agent (Uses LLM)

The orchestrator uses LLM in **two places**:

#### 1. Intent Classification
**File:** `agents/intent_classifier.py`

```python
from litellm import completion

class IntentClassifier:
    def classify(self, query: str) -> dict[str, Any]:
        # Tries LLM first if API key is configured
        if settings.ONE_MIN_AI_API_KEY:
            response = completion(
                model=settings.LITELLM_MODEL,
                api_key=settings.ONE_MIN_AI_API_KEY,
                messages=[...],
                temperature=0,
                max_tokens=180,
            )
            # Parse intent from LLM response
        
        # Falls back to rule-based classification if LLM unavailable
        return self._fallback(normalized)
```

**Purpose:** Classifies user intent into categories like:
- `executive_overview`
- `analyze_errors`
- `suggest_features`
- `create_story`
- `write_test_case`
- etc.

**Fallback:** If no LLM API key is configured, uses deterministic keyword matching.

#### 2. Response Generation
**File:** `agents/orchestrator.py`

```python
from litellm import completion

async def process_query(self, user_persona, user_query, conversation_history):
    # First, retrieve context from specialist agents (no LLM used here)
    agents_used, contexts = await self.retrieve_context(user_query, intent)
    
    # Then, try to generate response with LLM
    if settings.ONE_MIN_AI_API_KEY:
        try:
            response = completion(
                model=settings.LITELLM_MODEL,
                api_key=settings.ONE_MIN_AI_API_KEY,
                messages=[
                    {"role": "system", "content": "You are MAHALO orchestrator..."},
                    {"role": "user", "content": f"Request: {user_query}\nTool context: {contexts}"},
                ],
                temperature=0.3,
                max_tokens=250,
            )
            llm_text = response.choices[0].message.content
            if self._llm_response_is_grounded(user_query, llm_text, contexts):
                return llm_text
        except:
            pass
    
    # Falls back to deterministic response if LLM unavailable or response not grounded
    return self._fallback_response(user_persona, user_query, contexts)
```

**Purpose:** Generates natural language response based on the context retrieved from specialist agents.

**Fallback:** If LLM is unavailable or returns ungrounded responses, uses extensive template-based response generation.

### 🔧 Specialist Agents (No LLM - Rule-Based)

#### JIRA Agent
**File:** `agents/jira_agent.py`

```python
class JiraAgent:
    async def retrieve_context(self, query: str) -> dict[str, Any]:
        query_lower = query.lower()
        
        # Rule-based keyword matching
        if "bug" in query_lower:
            result = await self.tools.list_bugs_handler({"query": ""})
            # Calculate summary statistics
            # Return structured data
        
        if "velocity" in query_lower or "executive" in query_lower:
            result = await self.tools.search_stories_handler({"query": ""})
            # Calculate metrics
            # Return structured data
        
        # Direct API calls to JIRA backend via MCP tools
        # NO LLM USED
```

**What it does:**
- Keyword matching to determine which API to call
- Calls backend APIs via MCP tools
- Aggregates and calculates metrics (story points, completion %, etc.)
- Returns structured JSON data

**No LLM:** Pure Python logic and math.

#### ServiceNow Agent
**File:** `agents/servicenow_agent.py`

```python
class ServiceNowAgent:
    async def retrieve_context(self, query: str) -> dict[str, Any]:
        # Rule-based routing
        if "executive" in query.lower() or "overview" in query.lower():
            deployments = await self.tools.list_deployments_handler(...)
            incidents = await self.tools.list_incidents_handler(...)
            return combined_data
        
        if "deploy" in query.lower():
            return await self.tools.list_deployments_handler(...)
        
        return await self.tools.list_incidents_handler(...)
```

**What it does:**
- Simple keyword checks
- Calls backend APIs
- Returns structured data

**No LLM:** Just if/else logic.

#### Splunk Agent
**File:** `agents/splunk_agent.py`

```python
class SplunkAgent:
    async def retrieve_context(self, query: str) -> dict[str, Any]:
        # Extract search terms with regex
        words = re.findall(r"[a-z0-9_-]+", query_lower)
        terms = [term for term in words if len(term) > 2 and term not in ignored_terms]
        
        # Search logs for each term
        results = await gather(
            *(self.tools.search_logs_handler({"query": term}) for term in terms),
            return_exceptions=True,
        )
        
        # Filter and aggregate results
        # Calculate error counts
        # Return structured data
```

**What it does:**
- Regex-based keyword extraction
- Parallel log searches
- Filtering and counting
- Returns structured data

**No LLM:** Just regex, loops, and filters.

## Architecture Flow

```
┌─────────────────────────────────────────────────────────┐
│                      React UI                           │
│               (User: "executive summary")               │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓ HTTP POST /api/chat/message
┌─────────────────────────────────────────────────────────┐
│                   Main API Gateway                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│              🤖 ORCHESTRATOR AGENT (LLM)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 1. Intent Classification (LLM or fallback)       │  │
│  │    → Determines: executive_overview              │  │
│  │    → Selects agents: [JIRA, ServiceNow, Splunk] │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 2. Parallel Context Retrieval (NO LLM)           │  │
│  └──────────────────────────────────────────────────┘  │
└──────────┬────────────┬────────────┬───────────────────┘
           │            │            │
           ↓            ↓            ↓
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │   JIRA   │ │ServiceNow│ │  Splunk  │
    │  Agent   │ │  Agent   │ │  Agent   │
    │ (Rules)  │ │ (Rules)  │ │ (Rules)  │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         ↓            ↓            ↓
    [Keyword]    [Keyword]    [Regex]
    [Match]      [Match]      [Extract]
         │            │            │
         ↓            ↓            ↓
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │JIRA MCP  │ │ServiceNow│ │Splunk MCP│
    │  Tools   │ │MCP Tools │ │  Tools   │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         ↓            ↓            ↓
    HTTP GET    HTTP GET     HTTP GET
         │            │            │
         ↓            ↓            ↓
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │JIRA API  │ │ServiceNow│ │Splunk API│
    │(5001)    │ │API (5002)│ │(5003)    │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         ↓            ↓            ↓
    ┌─────────────────────────────────┐
    │      SQLite Database            │
    │        (mahalo.db)              │
    └─────────────────────────────────┘
           │            │            │
           ↓            ↓            ↓
    [Stories: 3]  [Incidents: 2] [Logs: 8]
           │            │            │
           └────────────┴────────────┘
                         │
                         ↓ Return context data
┌─────────────────────────────────────────────────────────┐
│              🤖 ORCHESTRATOR AGENT (LLM)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 3. Response Generation (LLM or fallback)         │  │
│  │    Takes context from agents                     │  │
│  │    Generates natural language response           │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
                "Executive, here is the MahaloPay 
                 executive update: - Delivery: 3 
                 tracked stories, 1 completed..."
```

## Why This Design?

### Advantages

1. **Cost Effective**
   - Only 2 LLM calls per user query (intent + response)
   - Specialist agents use free rule-based logic
   - Data retrieval is deterministic and fast

2. **Reliable**
   - Specialist agents always return consistent, structured data
   - No LLM hallucinations in data retrieval
   - Fallback to rule-based responses if LLM fails

3. **Testable**
   - Specialist agents have predictable behavior
   - Easy to write unit tests
   - LLM is only used for natural language formatting

4. **Fast**
   - Parallel execution of specialist agents
   - No LLM latency for data retrieval
   - Only orchestrator waits for LLM

5. **Transparent**
   - Clear separation between data (agents) and presentation (orchestrator)
   - Easy to debug what data was retrieved
   - Grounding check ensures LLM uses actual data

### Trade-offs

**What you get:**
- Natural language responses when LLM is available
- Structured, accurate data from specialist agents
- Graceful degradation when LLM unavailable

**What you don't get:**
- LLM-powered semantic search within agents (uses keyword matching instead)
- LLM-based query understanding at agent level (orchestrator handles this)
- Conversational multi-turn within individual agents

## Configuration

### With LLM (Current Setup)
```bash
# In .env
LITELLM_MODEL=gpt-4o-mini
ONE_MIN_AI_API_KEY=your_api_key_here
ONE_MIN_AI_BASE_URL=https://api.1min.ai/v1
```

**Behavior:**
- Intent classification uses LLM
- Response generation uses LLM (with fallback)
- Natural, conversational responses

### Without LLM
```bash
# In .env
# ONE_MIN_AI_API_KEY=  # Leave blank or unset
```

**Behavior:**
- Intent classification uses keyword matching
- Response generation uses templates
- Structured, predictable responses
- Still fully functional!

## Example Flow: "executive summary"

### Step 1: Intent Classification (LLM)
```python
# Orchestrator calls IntentClassifier
result = {
    "intent": "executive_overview",
    "agents": ["JIRA Agent", "ServiceNow Agent", "Splunk Agent"],
    "entities": {},
    "requires_confirmation": False
}
```

### Step 2: Parallel Data Retrieval (No LLM)

**JIRA Agent:**
```python
# Detects "executive" keyword
# Calls list_stories_handler with query=""
# Returns: {
#   "source": "JIRA",
#   "success": True,
#   "data": {"items": [3 stories]},
#   "summary": {
#     "total_stories": 3,
#     "completed_stories": 1,
#     "total_story_points": 26,
#     "completed_story_points": 8,
#     "completion_percent": 30.8
#   }
# }
```

**ServiceNow Agent:**
```python
# Detects "executive" keyword
# Calls list_deployments + list_incidents
# Returns: {
#   "source": "ServiceNow",
#   "success": True,
#   "data": {
#     "deployments": [3 items],
#     "incidents": [2 items]
#   }
# }
```

**Splunk Agent:**
```python
# Detects "executive" keyword
# Calls search_logs_handler with query=""
# Returns: {
#   "source": "Splunk",
#   "success": True,
#   "data": {"items": [8 logs]},
#   "summary": {
#     "total_logs": 8,
#     "error_count": 5
#   }
# }
```

### Step 3: Response Generation (LLM or Fallback)

**If LLM available:**
```python
response = completion(
    model="gpt-4o-mini",
    messages=[{
        "role": "system",
        "content": "You are MAHALO orchestrator for persona 'Executive'..."
    }, {
        "role": "user",
        "content": "Request: executive summary\nTool context: {all_the_context_data}"
    }],
    temperature=0.3,
)
# Returns natural language response
```

**If LLM unavailable:**
```python
# Uses _fallback_response with template:
return (
    f"{persona}, here is the MahaloPay executive update:\n"
    f"- Delivery: {total_stories} tracked stories, {completed} completed.\n"
    f"- Production: {len(deployments)} deployed features.\n"
    f"- Operations: {active_incidents} active or monitoring incidents.\n"
    f"- Reliability: {error_count} error logs out of {total_logs} total logs.\n"
    "Priority: review the recurring payment gateway, capacity, and "
    "reconciliation signals before expanding the roadmap."
)
```

## Summary Table

| Component | Uses LLM? | Purpose | Fallback Behavior |
|-----------|-----------|---------|-------------------|
| **Intent Classifier** | ✅ Yes (optional) | Classify user intent | Keyword matching |
| **Orchestrator Response** | ✅ Yes (optional) | Generate natural response | Template-based responses |
| **JIRA Agent** | ❌ No | Retrieve JIRA data | N/A (always rule-based) |
| **ServiceNow Agent** | ❌ No | Retrieve ServiceNow data | N/A (always rule-based) |
| **Splunk Agent** | ❌ No | Retrieve Splunk logs | N/A (always rule-based) |
| **MCP Tools** | ❌ No | HTTP clients | N/A (pure HTTP) |
| **Backend APIs** | ❌ No | Database queries | N/A (SQL queries) |

## Conclusion

**Only the Orchestrator uses LLM**, and even that is optional with robust fallbacks. The specialist agents are entirely rule-based, ensuring:
- Predictable data retrieval
- No LLM hallucinations in facts
- Fast, parallelized execution
- Testable, deterministic behavior
- Cost-effective architecture

This is a **"LLM at the edges"** design pattern where LLM handles natural language understanding and generation, but the core business logic and data retrieval is deterministic code.
