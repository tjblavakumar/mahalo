# Fix for "Format Your Response" Bug

## Problem Description

When a user asks "format your response" after receiving a response (like deployment list), the system:
1. Treats it as a NEW query instead of a meta-command
2. Routes it to JIRA, ServiceNow, and Splunk agents
3. Returns irrelevant search results (0 stories, 0 incidents, random logs)
4. Loses the context of the previous response

## Root Cause

The orchestrator's `process_query` method doesn't detect formatting/reformatting requests that refer to previous responses. It always attempts to classify the query and retrieve new context from agents.

## Solution

Add detection for meta-commands (formatting requests) BEFORE running intent classification and agent routing.

### Implementation

Add these methods to `orchestrator.py` in the `OrchestratorAgent` class:

```python
def _is_formatting_request(self, query: str, conversation_history: list[dict[str, str]] | None = None) -> bool:
    """Detect if the query is a request to reformat/explain the previous response."""
    query_lower = query.lower()
    
    # Check for formatting-related commands
    formatting_keywords = [
        "format", "reformat", "better format", "formatted", 
        "structure", "restructure", "organize", "reorganize",
        "cleaner", "more readable", "easier to read"
    ]
    
    response_references = [
        "your response", "that response", "the response", "your answer",
        "that answer", "the answer", "the output", "your output", "that"
    ]
    
    # Must have both a formatting keyword and a reference to previous response
    has_formatting = any(keyword in query_lower for keyword in formatting_keywords)
    has_reference = any(ref in query_lower for ref in response_references)
    
    # Short queries like "format your response" are very likely to be formatting requests
    is_short_formatting_query = (
        has_formatting and 
        len(query.split()) <= 5 and 
        conversation_history and len(conversation_history) > 0
    )
    
    return (has_formatting and has_reference) or is_short_formatting_query

def _reformat_last_response(self, persona: str, conversation_history: list[dict[str, str]] | None = None) -> str:
    """Reformat the last assistant response in a more structured way."""
    if not conversation_history or len(conversation_history) == 0:
        return f"{persona}, I don't have a previous response to format. Please ask a question first."
    
    # Find the last assistant response
    last_response = None
    for message in reversed(conversation_history):
        if message.get("role") == "assistant":
            last_response = message.get("content", "")
            break
    
    if not last_response:
        return f"{persona}, I couldn't find a previous response to format."
    
    # Check if the response contains deployment information
    if "features are deployed in production" in last_response.lower():
        return self._format_deployment_list(persona, last_response)
    
    # Check if it's an executive overview
    if "executive update" in last_response.lower() or "mahalo" in last_response.lower():
        return self._format_executive_overview(persona, last_response)
    
    # Default: add bullet points and structure
    return self._format_generic_response(persona, last_response)

def _format_deployment_list(self, persona: str, response: str) -> str:
    """Format deployment list in a clean table-like structure."""
    # Find all feature mentions with versions
    pattern = r'([^,]+?)\s*\(([v\d.]+)\)'
    matches = re.findall(pattern, response)
    
    if not matches:
        return response  # Can't parse, return original
    
    formatted = f"{persona}, here are the production deployments:\n\n"
    formatted += "| # | Feature | Version |\n"
    formatted += "|---|---------||---------|\n"
    
    for i, (feature, version) in enumerate(matches, 1):
        feature_clean = feature.strip().strip(',').strip()
        formatted += f"| {i} | {feature_clean} | {version} |\n"
    
    formatted += f"\n**Total: {len(matches)} features deployed in production**"
    
    return formatted

def _format_executive_overview(self, persona: str, response: str) -> str:
    """Format executive overview with better structure."""
    lines = response.split('\n')
    
    formatted = f"{persona}, here is the MahaloPay Executive Overview:\n\n"
    formatted += "## Key Metrics\n\n"
    
    for line in lines:
        line = line.strip()
        if line.startswith('-'):
            # Extract metric and format it
            formatted += f"{line}\n"
        elif line and not any(x in line.lower() for x in ['executive', 'mahalo', 'priority']):
            formatted += f"{line}\n"
    
    # Add priority section if it exists
    priority_lines = [l for l in lines if 'priority' in l.lower()]
    if priority_lines:
        formatted += "\n## Priority Recommendations\n\n"
        for line in priority_lines:
            formatted += f"{line.strip()}\n"
    
    return formatted

def _format_generic_response(self, persona: str, response: str) -> str:
    """Format generic response with better structure."""
    # If response already has good structure, just add a header
    if response.count('\n') >= 3 or '|' in response or response.startswith(persona):
        return response
    
    # Try to add some structure
    formatted = f"{persona}, here's a formatted version:\n\n"
    
    # Split on common delimiters
    if '.' in response and response.count('.') >= 2:
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        for sentence in sentences:
            if sentence:
                formatted += f"• {sentence}.\n"
    elif ',' in response and response.count(',') >= 3:
        items = [s.strip() for s in response.split(',') if s.strip()]
        for item in items:
            formatted += f"• {item}\n"
    else:
        formatted += response
    
    return formatted
```

### Modify `process_query` method

At the **very beginning** of `async def process_query`, add this check BEFORE intent classification:

```python
async def process_query(self, user_persona: str, user_query: str, conversation_history: list[dict[str, str]] | None = None):
    user_query_lower = user_query.lower()
    
    # ===== ADD THIS BLOCK AT THE START =====
    # Check if this is a formatting request for the previous response
    if self._is_formatting_request(user_query, conversation_history):
        return self._reformat_last_response(user_persona, conversation_history)
    # ===== END OF NEW CODE =====
    
    self.last_intent = self.intent_classifier.classify(user_query)
    if self.last_intent.get("intent") == "greeting":
        return f"Hello, {user_persona}. I'm MAHALO, your SDLC assistant. Ask me about delivery, incidents, deployments, logs, or production planning."
    # ... rest of the method continues unchanged
```

## Testing

After implementing this fix, test with:

```
User: "what features are in the production"
System: [Returns deployment list]

User: "format your response"
System: [Returns formatted table with deployments]
```

Expected output:
```
Executive, here are the production deployments:

| # | Feature | Version |
|---|---------|---------|
| 1 | Stripe payment gateway integration | v2.4.0 |
| 2 | Fraud detection rules engine | v1.8.2 |
...

**Total: 17 features deployed in production**
```

## Additional Improvements

Consider adding similar handling for other meta-commands:
- "explain that" / "explain your answer"
- "give me more details"
- "summarize that"
- "make it shorter"
- "expand on that"

These would all follow the same pattern - detect the meta-command BEFORE intent classification, then operate on conversation history instead of making new agent queries.
