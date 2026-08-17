# Fix for "Help Me Write a User Story" Bug

## 🔍 Problem Description

**User Query**: "help me to write a user story for payment gateway timeout recovery"

**Current Behavior**: Searches JIRA and Splunk, returns "found 100 stories, found 149 logs"

**Expected Behavior**: Draft a complete user story with title, description, acceptance criteria, evidence from logs

**What Was Missed**: User is asking for ASSISTANCE DRAFTING a story, not searching for existing stories

---

## 🎯 Root Cause

The orchestrator only detects story drafting for these patterns:
- "analyze" + "story" → draft stories
- "suggest" / "recommend" + "story" → draft stories  
- "create" + "story" + "based on" → draft stories

**Missing patterns**:
- "help me write a story"
- "help me create a story"
- "draft a story for"
- "write a user story for"

---

## ✅ The Fix

### Step 1: Add Story Drafting Detection

Add this method to `OrchestratorAgent`:

```python
def _is_story_drafting_request(self, query: str) -> bool:
    """Detect if user is asking for help drafting a user story."""
    query_lower = query.lower()
    
    # Assistance/action keywords
    drafting_keywords = [
        "help me write",
        "help me create",
        "help me draft",
        "draft a",
        "write a",
        "create a",
        "generate a",
    ]
    
    # Story-related terms
    story_terms = [
        "user story",
        "story",
        "backlog item",
        "feature",
    ]
    
    # Check for drafting keyword + story term
    has_drafting = any(keyword in query_lower for keyword in drafting_keywords)
    has_story = any(term in query_lower for term in story_terms)
    
    return has_drafting and has_story

def _extract_story_topic(self, query: str) -> str:
    """Extract the specific topic/feature from the query."""
    query_lower = query.lower()
    
    # Remove common prefixes
    prefixes = [
        "help me write a user story for",
        "help me write a story for",
        "help me create a user story for",
        "help me create a story for",
        "draft a user story for",
        "draft a story for",
        "write a user story for",
        "write a story for",
        "create a user story for",
        "create a story for",
        "help me write the user story for",
        "help me to write a user story for",
        "help me to write the user story for",
        "this high priority item",
        "this",
    ]
    
    topic = query_lower
    for prefix in prefixes:
        topic = topic.replace(prefix, "").strip()
    
    # Clean up common artifacts
    topic = topic.strip(".:,;!?")
    topic = topic.strip()
    
    return topic if topic else None
```

### Step 2: Add Topic-Specific Story Drafting

```python
def _draft_story_for_topic(self, persona: str, topic: str, contexts: list[dict[str, Any]]) -> str:
    """Draft a user story for a specific topic using relevant context."""
    
    # Get logs related to the topic
    splunk_context = next((ctx for ctx in contexts if ctx.get("source") == "Splunk"), None)
    logs = []
    if splunk_context and splunk_context.get("success"):
        data = splunk_context.get("data", {})
        logs = data.get("items", []) if isinstance(data, dict) else data if isinstance(data, list) else []
    
    # Filter logs relevant to the topic
    topic_keywords = topic.lower().split()
    relevant_logs = [
        log for log in logs
        if any(keyword in log.get("message", "").lower() for keyword in topic_keywords)
    ]
    
    # If no relevant logs, use all logs
    if not relevant_logs and logs:
        relevant_logs = logs
    
    # Determine story details based on topic
    story = self._build_story_from_topic(topic, relevant_logs)
    
    # Store as pending story
    self.pending_stories = [story]
    
    # Return formatted draft
    return self._format_story_draft(persona, story)

def _build_story_from_topic(self, topic: str, logs: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a story structure based on the specified topic."""
    topic_lower = topic.lower()
    
    # Determine story details based on topic keywords
    if "timeout" in topic_lower or "failover" in topic_lower:
        title = "Improve payment gateway timeout recovery and provider failover"
        description = (
            "Handle provider timeouts with bounded retries, safe failure states, "
            "and provider failover to ensure payment processing reliability."
        )
        acceptance_criteria = [
            "Payment gateway timeouts use bounded retries with exponential backoff",
            "Automatic failover to secondary provider when primary times out",
            "Retries do not duplicate a successful payment transaction",
            "Timeout events are logged with provider and transaction context",
            "Monitoring alerts when failover rate exceeds threshold",
            "Automated tests cover timeout, retry, and recovery scenarios",
        ]
    elif "pool" in topic_lower or "capacity" in topic_lower:
        title = "Protect payment capacity during traffic spikes"
        description = (
            "Implement connection-pool protection, retry backoff, and capacity "
            "monitoring to prevent service degradation during high load."
        )
        acceptance_criteria = [
            "Connection-pool saturation is monitored with alerting",
            "Retry backoff prevents retry storms",
            "Capacity alerts reach the platform team",
            "Circuit breakers protect downstream services",
            "Load tests cover traffic spikes and recovery",
        ]
    elif "fraud" in topic_lower:
        title = "Reduce fraud scoring latency"
        description = (
            "Optimize fraud scoring to meet transaction processing SLA "
            "while maintaining detection accuracy."
        )
        acceptance_criteria = [
            "Fraud-scoring latency is measured against defined target",
            "High-risk transactions complete within SLA",
            "Scoring accuracy is maintained or improved",
            "Latency metrics are visible in dashboards",
            "Automated tests validate scoring performance",
        ]
    elif "reconciliation" in topic_lower or "balance" in topic_lower:
        title = "Strengthen reconciliation mismatch detection"
        description = (
            "Detect and surface reconciliation mismatches before settlement "
            "completes, with actionable operational alerts."
        )
        acceptance_criteria = [
            "Reconciliation mismatches create actionable alerts",
            "Mismatches are detected before settlement completion",
            "Alert context includes transaction and provider details",
            "Dashboards show reconciliation health trends",
            "Automated tests validate mismatch detection",
        ]
    else:
        # Generic reliability story
        title = f"Improve {topic}"
        description = f"Address production reliability issues related to {topic} to improve system stability and customer experience."
        acceptance_criteria = [
            f"Production issues related to {topic} are resolved",
            "Solution is tested in staging environment",
            "Monitoring is in place to detect regressions",
            "Documentation is updated",
            "Automated tests cover the fix",
        ]
    
    # Extract evidence from logs
    evidence = [log.get("message", "") for log in logs[:5]]
    
    return {
        "title": title,
        "description": description,
        "story_points": 8,
        "priority": "High",
        "status": "Backlog",
        "sprint": "Sprint 24",
        "acceptance_criteria": acceptance_criteria,
        "evidence": evidence,
    }
```

### Step 3: Add to process_query

In `process_query()`, add this check BEFORE querying agents:

```python
async def process_query(self, user_persona: str, user_query: str, 
                       conversation_history: list[dict[str, str]] | None = None):
    user_query_lower = user_query.lower()
    
    # === EXISTING META-COMMAND CHECKS ===
    if self._is_formatting_request(user_query, conversation_history):
        return self._reformat_last_response(user_persona, conversation_history)
    
    if self._is_elaboration_request(user_query, conversation_history):
        return self._elaborate_last_response(user_persona, conversation_history)
    
    # === NEW: Story Drafting Assistance ===
    if self._is_story_drafting_request(user_query):
        # Extract the topic
        topic = self._extract_story_topic(user_query)
        
        if topic:
            # Get relevant context (especially Splunk logs)
            agents_used, contexts = await self.retrieve_context(user_query, None)
            
            # Draft story for the specific topic
            return self._draft_story_for_topic(user_persona, topic, contexts)
        else:
            # No topic specified - ask for clarification
            return f"{user_persona}, I'd be happy to help you write a user story. What feature or issue should the story address?"
    
    # === CONTINUE WITH NORMAL FLOW ===
    self.last_intent = self.intent_classifier.classify(user_query)
    ...
```

---

## 🧪 Test Cases

### Test 1: Specific Topic
```
User: "help me write a user story for payment gateway timeout recovery"
Expected: Complete story draft with timeout-specific acceptance criteria
```

### Test 2: Different Topic
```
User: "help me create a story about fraud detection latency"
Expected: Complete story draft with fraud-specific acceptance criteria
```

### Test 3: Vague Request
```
User: "help me write a user story"
Expected: "What feature or issue should the story address?"
```

### Test 4: From Context (High Priority Item)
```
Previous: System recommended "payment gateway timeout recovery" as high priority
User: "help me write the user story for this high priority item"
Expected: Story draft for timeout recovery (using conversation context)
```

---

## 📊 Expected Output

```
Executive, here is a user story draft for payment gateway timeout recovery:

**Title**: Improve payment gateway timeout recovery and provider failover

**Description**: Handle provider timeouts with bounded retries, safe failure 
states, and provider failover to ensure payment processing reliability.

**User Story**: As a MahaloPay customer, I want payment gateway timeouts to 
be handled gracefully with automatic failover, so that my transactions succeed 
even when the primary provider is experiencing issues.

**Acceptance Criteria**:
- Payment gateway timeouts use bounded retries with exponential backoff
- Automatic failover to secondary provider when primary times out
- Retries do not duplicate a successful payment transaction
- Timeout events are logged with provider and transaction context
- Monitoring alerts when failover rate exceeds threshold
- Automated tests cover timeout, retry, and recovery scenarios

**Priority**: High
**Story Points**: 8
**Sprint**: Sprint 24

**Evidence from Production Logs**:
- Payment gateway timeout after 30 seconds for high-value transaction
- Downstream payment provider returned intermittent 502 responses

This is a draft. Say 'create this story in JIRA' to save it, or ask me to 
revise any section.
```

---

## 🎯 Benefits

- ✅ Users can ask for story drafting help naturally
- ✅ Stories are topic-specific (not generic)
- ✅ Evidence from production logs is included
- ✅ Acceptance criteria tailored to the topic
- ✅ Reduces manual story writing effort

---

## 🔗 Related Patterns

This detection can also handle:
- "draft a story for X"
- "write a user story about X"
- "create a story for X"
- "generate a user story for X"
- "help me with a story about X"

---

## ⚠️ Edge Cases

### Case 1: Vague Topic Reference
```
User: "help me write the user story for this high priority item"
                                         ^^^^
                                  Refers to previous context
```

**Solution**: Extract from conversation history what "this" refers to

### Case 2: No Topic Specified
```
User: "help me write a user story"
```

**Solution**: Ask for clarification: "What feature should the story address?"

### Case 3: Multiple Topics
```
User: "help me write stories for timeout and fraud issues"
```

**Solution**: Draft multiple stories or ask which to start with

---

## 📝 Implementation Priority

**CRITICAL** - This is a core user workflow:
1. System recommends high-priority features
2. User asks for help writing the story
3. System should assist, not search

**Estimated Time**: 60 minutes

---

## 🔄 Enhancement: Context-Aware Topic Extraction

For queries like "help me write the user story for this high priority item":

```python
def _extract_story_topic_with_context(self, query: str, 
                                     conversation_history: list[dict[str, str]] | None = None) -> str:
    """Extract story topic, using conversation context for pronouns like 'this'."""
    topic = self._extract_story_topic(query)
    
    # If topic is vague (like "this"), look at conversation history
    if not topic or topic in ["this", "that", "it", "the high priority item"]:
        if conversation_history:
            # Find the last recommendation or priority mention
            for message in reversed(conversation_history):
                if message.get("role") == "assistant":
                    content = message.get("content", "").lower()
                    
                    # Extract priority recommendations
                    if "priority" in content and "recommend" in content:
                        # Parse the recommendation text
                        # Example: "Top priority: Gateway Timeout Recovery"
                        import re
                        priority_match = re.search(r'priority[:\s]+([^.]+)', content, re.IGNORECASE)
                        if priority_match:
                            return priority_match.group(1).strip()
    
    return topic
```

---

## 🎉 Success Criteria

The fix is successful when:
1. ✅ "help me write a story for X" drafts a story about X
2. ✅ Story includes topic-specific acceptance criteria
3. ✅ Evidence from production logs is included
4. ✅ Story saved to pending_stories for JIRA creation
5. ✅ Normal queries continue to work
