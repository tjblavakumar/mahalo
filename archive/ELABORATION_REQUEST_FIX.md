# Fix for "Why Do You Recommend This" Bug

## 🔍 Problem Description

**User Query Sequence:**
1. System: "Reliability score is 29.9%. Prioritize error reduction and monitoring improvements."
2. User: "why do you recommend this. justify with more details"
3. System: Searches JIRA and Splunk for "why", "recommend", "justify", "details"
4. Returns: "JIRA found 50 matching stories, Splunk found 356 logs..."

**Expected**: Explain WHY 29.9% score, WHAT went into the calculation, WHY error reduction is prioritized

**Actual**: Irrelevant search results

---

## 🎯 Root Cause

Same issue as "format your response" - the system doesn't detect **elaboration/justification requests** that refer to previous responses.

### Query Pattern Recognition Needed

```
"why do you recommend this" = User wants EXPLANATION of previous recommendation
"justify with more details" = User wants JUSTIFICATION with calculations/details
"explain that" = User wants elaboration on previous statement
```

All these are **META-COMMANDS** referring to conversation history, not new queries.

---

## ✅ The Fix

Add detection for elaboration/justification requests (similar to format response fix):

### Step 1: Add Detection Method

```python
def _is_elaboration_request(self, query: str, conversation_history: list[dict[str, str]] | None = None) -> bool:
    """Detect if the query is requesting elaboration/explanation of previous response."""
    query_lower = query.lower()
    
    # Check for elaboration/explanation keywords
    elaboration_keywords = [
        "why", "how", "explain", "elaborate", "clarify", "justify",
        "what do you mean", "can you explain", "tell me more",
        "give me more details", "provide more details", "break down",
        "walk me through"
    ]
    
    # References to previous response
    response_references = [
        "this", "that", "your recommendation", "your answer",
        "your response", "the recommendation", "the score",
        "that recommendation", "that score", "this score"
    ]
    
    has_elaboration = any(keyword in query_lower for keyword in elaboration_keywords)
    has_reference = any(ref in query_lower for ref in response_references)
    
    # Short queries with elaboration keywords are likely meta-commands
    is_short_elaboration = (
        has_elaboration and
        len(query.split()) <= 10 and
        conversation_history and len(conversation_history) > 0
    )
    
    return (has_elaboration and has_reference) or is_short_elaboration
```

### Step 2: Add Elaboration Handler

```python
def _elaborate_last_response(self, persona: str, conversation_history: list[dict[str, str]] | None = None) -> str:
    """Provide detailed elaboration of the last assistant response."""
    if not conversation_history or len(conversation_history) == 0:
        return f"{persona}, I don't have a previous response to elaborate on."
    
    # Find last assistant response
    last_response = None
    for message in reversed(conversation_history):
        if message.get("role") == "assistant":
            last_response = message.get("content", "")
            break
    
    if not last_response:
        return f"{persona}, I couldn't find a previous response to elaborate on."
    
    # Check if it's a health score/reliability recommendation
    if "reliability score" in last_response.lower() or "health score" in last_response.lower():
        return self._elaborate_health_score(persona)
    
    # Check if it's a deployment recommendation
    if "deploy" in last_response.lower() and "recommend" in last_response.lower():
        return self._elaborate_deployment_recommendation(persona)
    
    # Check if it's a priority recommendation
    if "prioritize" in last_response.lower() or "priority" in last_response.lower():
        return self._elaborate_priority_recommendation(persona)
    
    # Default: provide general elaboration
    return self._elaborate_generic_response(persona, last_response)
```

### Step 3: Add Specific Elaboration Methods

```python
def _elaborate_health_score(self, persona: str) -> str:
    """Elaborate on health/reliability score calculation."""
    if not self.last_insights:
        return f"{persona}, I don't have detailed health metrics available."
    
    summary = self.last_insights.get("summary", {})
    health = self.last_insights.get("health_score", {})
    gaps = self.last_insights.get("gaps", [])
    correlations = self.last_insights.get("correlations", [])
    
    # Build detailed explanation
    response = f"{persona}, here's the detailed breakdown of the reliability score:\n\n"
    
    # Explain the calculation
    response += "## Score Calculation\n\n"
    response += f"**Overall Score: {health.get('overall_score', 0)}%** ({health.get('status', 'Unknown')})\n\n"
    response += "This is calculated from three components:\n\n"
    response += f"1. **Delivery Health: {health.get('delivery_score', 0)}%**\n"
    response += f"   - {summary.get('completed_stories', 0)} of {summary.get('total_stories', 0)} stories completed\n"
    response += f"   - Completion rate drives this metric\n\n"
    
    response += f"2. **Operations Health: {health.get('operations_score', 0)}%**\n"
    response += f"   - {summary.get('active_incidents', 0)} of {summary.get('total_incidents', 0)} incidents active\n"
    response += f"   - Lower active incidents = higher score\n\n"
    
    response += f"3. **Reliability Health: {health.get('reliability_score', 0)}%**\n"
    response += f"   - {summary.get('total_errors', 0)} errors in {summary.get('total_logs', 0)} logs\n"
    response += f"   - Error rate: {summary.get('error_rate', 0):.1f}%\n"
    response += f"   - **This is why the overall score is low**\n\n"
    
    # Explain why error reduction is prioritized
    response += "## Why Prioritize Error Reduction\n\n"
    response += f"With an error rate of {summary.get('error_rate', 0):.1f}% and reliability at {health.get('reliability_score', 0)}%, "
    response += "the system has identified significant production issues:\n\n"
    
    # List specific problems found
    if gaps:
        response += "**Identified Gaps:**\n"
        for gap in gaps[:3]:
            response += f"- {gap.get('theme', 'Unknown issue')}: {gap.get('error_count', 0)} errors\n"
        response += "\n"
    
    if correlations:
        response += "**Cross-System Correlations:**\n"
        for corr in correlations[:3]:
            response += f"- {corr.get('recommendation', 'Unknown correlation')}\n"
        response += "\n"
    
    response += "These recurring patterns indicate systematic reliability problems that should be addressed before expanding features."
    
    return response

def _elaborate_priority_recommendation(self, persona: str) -> str:
    """Elaborate on why something is prioritized."""
    if not self.last_insights:
        return f"{persona}, I don't have detailed priority reasoning available."
    
    priorities = self.last_insights.get("priorities", [])
    
    if not priorities:
        return f"{persona}, I don't have specific priority recommendations available."
    
    response = f"{persona}, here's why these items are prioritized:\n\n"
    
    for priority in priorities[:3]:
        response += f"**{priority.get('rank')}. {priority.get('theme')}**\n"
        response += f"- Reason: {priority.get('reason')}\n"
        response += f"- Priority: {priority.get('suggested_priority')}\n"
        response += f"- Estimated effort: {priority.get('story_points_estimate')} story points\n\n"
    
    response += "\nPriorities are ranked based on:\n"
    response += "1. Error frequency and impact\n"
    response += "2. Customer-facing severity\n"
    response += "3. Current backlog coverage (gaps are prioritized)\n"
    response += "4. Cross-system correlations\n"
    
    return response

def _elaborate_deployment_recommendation(self, persona: str) -> str:
    """Elaborate on deployment recommendations."""
    # This would elaborate on why certain deployments are recommended
    return f"{persona}, deployment recommendations are based on correlation analysis of errors, incidents, and current backlog gaps. I can provide more specific details if you share which deployment you're curious about."

def _elaborate_generic_response(self, persona: str, response: str) -> str:
    """Generic elaboration when specific type isn't detected."""
    response = f"{persona}, let me elaborate on that:\n\n"
    response += "Based on the previous analysis, the recommendation considers:\n"
    response += "- Current system health metrics\n"
    response += "- Error patterns and frequency\n"
    response += "- Gaps in current backlog coverage\n"
    response += "- Cross-system correlations\n\n"
    response += "For more specific details, you can ask about:\n"
    response += "- Specific error themes\n"
    response += "- Individual health scores\n"
    response += "- Priority calculations\n"
    
    return response
```

### Step 4: Add to process_query

At the start of `process_query`, after greeting check, add:

```python
# Check for elaboration/justification requests
if self._is_elaboration_request(user_query, conversation_history):
    return self._elaborate_last_response(user_persona, conversation_history)
```

---

## 🧪 Test Cases

### Test 1: Health Score Elaboration
```
System: "Reliability score is 29.9%. Prioritize error reduction..."
User: "why do you recommend this. justify with more details"
Expected: Detailed breakdown showing:
  - How 29.9% was calculated
  - What the error rate is
  - Why it's prioritized
  - Specific gaps found
```

### Test 2: Generic Elaboration
```
System: "Create story for payment gateway timeouts"
User: "explain that recommendation"
Expected: Why timeouts are prioritized, evidence from logs, impact assessment
```

### Test 3: Priority Justification
```
System: "High priority recommendation: Fix database pool"
User: "justify the priority"
Expected: Explanation of priority ranking, frequency, impact, story points estimate
```

---

## 📊 Expected Output Example

```
Executive, here's the detailed breakdown of the reliability score:

## Score Calculation

**Overall Score: 29.9%** (Critical)

This is calculated from three components:

1. **Delivery Health: 45.2%**
   - 5 of 50 stories completed
   - Completion rate drives this metric

2. **Operations Health: 73.3%**
   - 4 of 15 incidents active
   - Lower active incidents = higher score

3. **Reliability Health: 29.9%**
   - 250 errors in 356 logs
   - Error rate: 70.2%
   - **This is why the overall score is low**

## Why Prioritize Error Reduction

With an error rate of 70.2% and reliability at 29.9%, the system has 
identified significant production issues:

**Identified Gaps:**
- Gateway Timeout: 89 errors
- Connection Pool: 76 errors
- Retry Capacity: 45 errors

**Cross-System Correlations:**
- Error theme 'gateway_timeout' has no corresponding JIRA stories
- 89 timeout errors without backlog coverage
- High-severity incident INC-001 correlated with 23 timeout errors

These recurring patterns indicate systematic reliability problems that 
should be addressed before expanding features.
```

---

## 🎯 Benefits

- ✅ Provides transparency into AI reasoning
- ✅ Shows calculations behind scores
- ✅ Builds user trust in recommendations
- ✅ Makes system more explainable
- ✅ Reduces "black box" feeling

---

## 📝 Implementation Priority

**HIGH** - This is critical for executive trust in AI recommendations. Without justification, recommendations feel arbitrary.

**Estimated Time**: 45-60 minutes

---

## 🔗 Related Fixes

This follows the same pattern as:
- `FORMAT_RESPONSE_FIX.md` - Format requests
- Can extend to: "give me more details", "break that down", "walk me through that"
