# Fix for Compound Query Handling

## 🔍 Problem Description

**User Query**: "tell me what is in production and what is pending"

**Current Behavior**: 
- Generic search across all agents
- Returns unfiltered stories, irrelevant incidents, no deployments
- Poor formatting

**Expected Behavior**:
- Detect compound query (two questions in one)
- Query deployments for "in production"
- Query backlog stories for "pending"
- Format results clearly for both parts

---

## 🎯 Root Causes

1. **No compound query detection** - System treats "X and Y" as single query
2. **"Production" doesn't map to deployments** - Maps to ServiceNow but gets incidents
3. **"Pending" doesn't filter stories** - Returns all stories, not just backlog
4. **Poor response formatting** - Lists of "unknown, unknown, unknown"

---

## ✅ The Fix

### Part 1: Detect Compound Queries

Add this method to `OrchestratorAgent`:

```python
def _is_compound_query(self, query: str) -> bool:
    """Detect if query contains multiple distinct questions."""
    query_lower = query.lower()
    
    # Compound indicators
    indicators = [
        " and ",
        " and also ",
        ", and ",
        " as well as ",
        " plus ",
        " also ",
    ]
    
    # Question patterns that suggest multiple intents
    multiple_questions = [
        "what is" in query_lower and "what is" in query_lower[query_lower.index("what is")+7:],
        "tell me" in query_lower and "and" in query_lower,
        "show me" in query_lower and "and" in query_lower,
    ]
    
    has_indicator = any(ind in query_lower for ind in indicators)
    has_multiple_questions = any(multiple_questions)
    
    return has_indicator and has_multiple_questions

def _split_compound_query(self, query: str) -> list[str]:
    """Split compound query into individual sub-queries."""
    query_lower = query.lower()
    
    # Split on common conjunctions
    split_patterns = [" and ", ", and ", " and also ", " as well as "]
    
    for pattern in split_patterns:
        if pattern in query_lower:
            parts = query.split(pattern, 1)
            return [part.strip() for part in parts if part.strip()]
    
    return [query]

def _combine_compound_results(self, persona: str, results: list[tuple[str, str]]) -> str:
    """Combine results from multiple sub-queries into cohesive response."""
    if len(results) == 1:
        return results[0][1]
    
    response = f"{persona}, here's the information you requested:\n\n"
    
    for i, (sub_query, sub_response) in enumerate(results, 1):
        # Extract the main content (skip persona prefix)
        content = sub_response
        if content.startswith(persona):
            # Remove "Executive, " prefix
            content = content[len(persona)+2:]
        
        response += f"## Part {i}: {sub_query.capitalize()}\n\n"
        response += content + "\n\n"
    
    return response.strip()
```

### Part 2: Improve "Production" Intent Detection

Modify `_agents_for_query()` to explicitly check for deployment queries:

```python
def _agents_for_query(self, user_query: str, intent: dict[str, Any] | None = None):
    # ... existing code ...
    
    query = user_query.lower()
    agents = []
    
    # IMPROVED: Detect deployment-specific queries
    deployment_keywords = ["in production", "deployed", "deployment", "live features"]
    is_deployment_query = any(keyword in query for keyword in deployment_keywords)
    
    if is_deployment_query:
        # Explicitly request deployments, not incidents
        agents.append(("ServiceNow Agent", self.servicenow_agent))
    elif "deploy" in query or "production" in query:
        # Generic production query - may need both
        agents.append(("ServiceNow Agent", self.servicenow_agent))
    
    # ... rest of existing code ...
```

### Part 3: Add "Pending" Story Filtering

Add this method to handle pending/backlog queries:

```python
async def _get_pending_stories(self) -> dict[str, Any]:
    """Get stories that are pending (backlog, to do, ready)."""
    # Query JIRA for backlog stories
    result = await self.jira_agent.retrieve_context("backlog stories")
    
    if not result.get("success"):
        return {"success": False, "data": {"items": []}}
    
    stories = result.get("data", {}).get("items", [])
    
    # Filter for pending statuses
    pending_statuses = ["backlog", "to do", "ready", "open"]
    pending_stories = [
        story for story in stories
        if story.get("status", "").lower() in pending_statuses
    ]
    
    # Sort by priority and points
    priority_order = {"high": 1, "medium": 2, "low": 3}
    pending_stories.sort(
        key=lambda s: (
            priority_order.get(s.get("priority", "medium").lower(), 4),
            -s.get("story_points", 0)
        )
    )
    
    return {
        "success": True,
        "data": {"items": pending_stories},
        "summary": {
            "total_pending": len(pending_stories),
            "high_priority": sum(1 for s in pending_stories if s.get("priority", "").lower() == "high"),
            "total_points": sum(s.get("story_points", 0) for s in pending_stories),
        }
    }
```

### Part 4: Improve Response Formatting

Add specific formatters for production + pending queries:

```python
def _format_production_and_pending(self, persona: str, 
                                   deployments: list[dict], 
                                   pending_stories: list[dict]) -> str:
    """Format response for 'what's in production and what's pending' query."""
    
    response = f"{persona}, here's your production and pending status:\n\n"
    
    # Part 1: Production Deployments
    response += f"## In Production ({len(deployments)} features)\n\n"
    
    if deployments:
        response += "| # | Feature | Version |\n"
        response += "|---|---------|----------|\n"
        for i, dep in enumerate(deployments[:10], 1):
            feature = dep.get("feature_name", "Unknown")
            version = dep.get("version", "Unknown")
            response += f"| {i} | {feature} | {version} |\n"
        
        if len(deployments) > 10:
            response += f"\n_[{len(deployments) - 10} more deployments...]_\n"
    else:
        response += "_No deployments found._\n"
    
    response += "\n"
    
    # Part 2: Pending Stories
    response += f"## Pending in Backlog ({len(pending_stories)} stories)\n\n"
    
    if pending_stories:
        # Group by priority
        high_priority = [s for s in pending_stories if s.get("priority", "").lower() == "high"]
        medium_priority = [s for s in pending_stories if s.get("priority", "").lower() == "medium"]
        
        if high_priority:
            response += "**High Priority:**\n"
            for story in high_priority[:5]:
                key = story.get("story_key", "???")
                title = story.get("title", "Unknown")
                points = story.get("story_points", 0)
                response += f"- {key}: {title} ({points} pts)\n"
            response += "\n"
        
        if medium_priority:
            response += "**Medium Priority:**\n"
            for story in medium_priority[:3]:
                key = story.get("story_key", "???")
                title = story.get("title", "Unknown")
                points = story.get("story_points", 0)
                response += f"- {key}: {title} ({points} pts)\n"
            response += "\n"
        
        total_points = sum(s.get("story_points", 0) for s in pending_stories)
        response += f"_Total pending work: {total_points} story points_\n"
    else:
        response += "_No pending stories in backlog._\n"
    
    return response
```

### Part 5: Integrate into process_query

Update `process_query()` to handle compound queries:

```python
async def process_query(self, user_persona: str, user_query: str, 
                       conversation_history: list[dict[str, str]] | None = None):
    user_query_lower = user_query.lower()
    
    # === EXISTING META-COMMANDS ===
    if self._is_formatting_request(user_query, conversation_history):
        return self._reformat_last_response(user_persona, conversation_history)
    
    if self._is_elaboration_request(user_query, conversation_history):
        return self._elaborate_last_response(user_persona, conversation_history)
    
    if self._is_story_drafting_request(user_query):
        # ... existing code ...
    
    # === NEW: COMPOUND QUERY DETECTION ===
    if self._is_compound_query(user_query):
        sub_queries = self._split_compound_query(user_query)
        results = []
        
        for sub_query in sub_queries:
            # Process each sub-query independently
            sub_response = await self.process_query(user_persona, sub_query, conversation_history)
            results.append((sub_query, sub_response))
        
        return self._combine_compound_results(user_persona, results)
    
    # === SPECIAL: PRODUCTION + PENDING QUERY ===
    if ("production" in user_query_lower or "deployed" in user_query_lower) and \
       ("pending" in user_query_lower or "backlog" in user_query_lower):
        
        # Get deployments
        sn_result = await self.servicenow_agent.retrieve_context("production deployments")
        deployments = sn_result.get("data", {}).get("deployments", [])
        
        # Get pending stories
        pending_result = await self._get_pending_stories()
        pending_stories = pending_result.get("data", {}).get("items", [])
        
        return self._format_production_and_pending(user_persona, deployments, pending_stories)
    
    # === CONTINUE WITH NORMAL FLOW ===
    self.last_intent = self.intent_classifier.classify(user_query)
    ...
```

---

## 🧪 Test Cases

### Test 1: Production + Pending
```
User: "tell me what is in production and what is pending"
Expected:
  - Deployments table
  - Pending stories by priority
  - Story point totals
```

### Test 2: Other Compound Queries
```
User: "show me bugs and show me deployments"
Expected:
  - Part 1: Bug list
  - Part 2: Deployment list
```

### Test 3: Not a Compound Query
```
User: "show me production errors"
Expected: Normal query (not split)
```

---

## 📊 Expected Output

```
Executive, here's your production and pending status:

## In Production (17 features)

| # | Feature                            | Version |
|---|------------------------------------|---------|
| 1 | Stripe payment gateway integration | v2.4.0  |
| 2 | Fraud detection rules engine       | v1.8.2  |
| 3 | Account reconciliation automation  | v3.1.0  |
| 4 | Fraud scoring optimization         | v1.7.1  |
| 5 | Reconciliation observability       | v3.1.6  |
...

## Pending in Backlog (23 stories)

**High Priority:**
- STORY-105: Improve payment gateway timeout recovery (8 pts)
- STORY-112: Protect payment capacity during spikes (8 pts)
- STORY-118: Reduce fraud scoring latency (8 pts)

**Medium Priority:**
- STORY-108: Strengthen reconciliation detection (5 pts)
- STORY-115: Add payment latency monitoring (5 pts)
- STORY-120: Improve error reporting (3 pts)

_Total pending work: 89 story points_
```

---

## 🎯 Benefits

- ✅ Handles compound queries correctly
- ✅ "Production" correctly maps to deployments
- ✅ "Pending" correctly filters for backlog
- ✅ Clean, structured formatting
- ✅ Executive-friendly summary

---

## ⚠️ Edge Cases

### Case 1: Three-part compound query
```
User: "show me production, pending, and bugs"
Solution: Split into 3 sub-queries
```

### Case 2: Ambiguous "and"
```
User: "show me stories about payments and fraud"
Solution: Don't split (single topic with "and")
Detection: No question words in second part
```

### Case 3: Recursive compound queries
```
User asks compound query → Each part is also compound
Solution: Recursive handling with depth limit
```

---

## 📝 Implementation Priority

**HIGH** - This is a common executive query pattern:
- "What's deployed and what's pending"
- "Show me production and backlog"
- "Tell me live features and upcoming work"

**Estimated Time**: 60-75 minutes

---

## 🔗 Related Improvements

Also consider:
- Status comparison queries ("how much is done vs pending")
- Timeline queries ("what deployed this week and what's next")
- Velocity queries ("what shipped and what's planned this sprint")

---

## 🎉 Success Criteria

The fix is successful when:
1. ✅ Compound queries detected correctly
2. ✅ "Production" returns deployments (not incidents)
3. ✅ "Pending" returns backlog stories (filtered by status)
4. ✅ Response is well-formatted and structured
5. ✅ Normal single queries continue to work
