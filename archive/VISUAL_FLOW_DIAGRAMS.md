# Visual Flow Diagrams

## Current (Broken) Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ User: "what features are in the production"                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────┐
         │   Intent Classifier       │
         │  "count_deployments"      │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │   ServiceNow Agent        │
         │   Query deployments       │
         └───────────┬───────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────┐
│ Response: "17 features deployed: Stripe (v2.4.0), Fraud..."    │
└────────────────────────────────────────────────────────────────┘
                     │
                     │ User stores in conversation history
                     ▼
┌────────────────────────────────────────────────────────────────┐
│ User: "format your response"                                   │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────┐
         │   Intent Classifier       │
         │  "general_sdlc"           │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────────────────────┐
         │   Route to ALL Agents                 │
         │   (JIRA + ServiceNow + Splunk)        │
         └───────────┬───────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────────┐
         │   Search for "format" "response"      │
         │   JIRA: 0 stories                     │
         │   ServiceNow: 0 incidents             │
         │   Splunk: 82 random logs              │
         └───────────┬───────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────┐
│ Response: "JIRA found 0 stories, ServiceNow found 0..."       │
│                                                                 │
│ ❌ WRONG! User wanted deployment list formatted, not search    │
└────────────────────────────────────────────────────────────────┘
```

---

## Fixed Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ User: "what features are in the production"                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────┐
         │   Intent Classifier       │
         │  "count_deployments"      │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────────┐
         │   ServiceNow Agent        │
         │   Query deployments       │
         └───────────┬───────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────┐
│ Response: "17 features deployed: Stripe (v2.4.0), Fraud..."    │
└────────────────────────────────────────────────────────────────┘
                     │
                     │ Saved to conversation history
                     ▼
┌────────────────────────────────────────────────────────────────┐
│ User: "format your response"                                   │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │   🆕 Meta-Command Detection            │
         │   _is_formatting_request()             │
         │   ✓ Contains "format" + "response"     │
         │   ✓ Short query (<= 5 words)           │
         │   ✓ Has conversation history           │
         └───────────┬───────────────────────────┘
                     │
                     │ EARLY EXIT - Skip intent classification
                     ▼
         ┌───────────────────────────────────────┐
         │   _reformat_last_response()            │
         │   1. Find last assistant message       │
         │   2. Detect type (deployment list)     │
         │   3. Call _format_deployment_list()    │
         └───────────┬───────────────────────────┘
                     │
                     ▼
         ┌───────────────────────────────────────┐
         │   _format_deployment_list()            │
         │   • Extract features & versions        │
         │   • Build markdown table               │
         │   • Return formatted result            │
         └───────────┬───────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────┐
│ Response:                                                       │
│                                                                 │
│ | # | Feature                    | Version |                   │
│ |---|----------------------------|---------|                   │
│ | 1 | Stripe payment gateway     | v2.4.0  |                   │
│ | 2 | Fraud detection engine     | v1.8.2  |                   │
│ | 3 | Account reconciliation     | v3.1.0  |                   │
│ ...                                                             │
│                                                                 │
│ **Total: 17 features deployed**                                │
│                                                                 │
│ ✅ CORRECT! User got formatted table without losing context    │
└────────────────────────────────────────────────────────────────┘
```

---

## Decision Tree: Meta-Command Detection

```
User Query: "format your response"
            │
            ▼
    ┌───────────────────┐
    │ Contains "format" │ ────No───▶ Continue to Intent Classifier
    │ keyword?          │
    └───────┬───────────┘
            │ Yes
            ▼
    ┌───────────────────────────┐
    │ Contains "response" or    │ ────No───▶ Continue to Intent Classifier
    │ "that" or "answer"?       │
    └───────┬───────────────────┘
            │ Yes
            ▼
    ┌───────────────────────────┐
    │ Query <= 5 words?         │ ────No───▶ Check conversation history
    └───────┬───────────────────┘
            │ Yes
            ▼
    ┌───────────────────────────┐
    │ Has conversation history? │ ────No───▶ Return "no previous response"
    └───────┬───────────────────┘
            │ Yes
            ▼
    ┌───────────────────────────┐
    │ 🎯 META-COMMAND DETECTED  │
    │ Route to reformat handler │
    └───────────────────────────┘
```

---

## Code Flow: New Methods

```
process_query()
    │
    ├──▶ _is_formatting_request(query, history)
    │       │
    │       ├──▶ Check for formatting keywords
    │       ├──▶ Check for response references  
    │       ├──▶ Check query length & history
    │       └──▶ Return True/False
    │
    └──▶ IF True:
            │
            └──▶ _reformat_last_response(persona, history)
                    │
                    ├──▶ Find last assistant message
                    │
                    ├──▶ Detect response type:
                    │      │
                    │      ├──▶ "features are deployed"?
                    │      │       └──▶ _format_deployment_list()
                    │      │
                    │      ├──▶ "executive update"?
                    │      │       └──▶ _format_executive_overview()
                    │      │
                    │      └──▶ Default
                    │              └──▶ _format_generic_response()
                    │
                    └──▶ Return formatted string
```

---

## Comparison: Before vs After

### Before Fix

```
┌──────────────────────────────────────────────────────────┐
│                    EVERY Query                           │
│                         │                                 │
│                         ▼                                 │
│              ┌──────────────────────┐                    │
│              │ Intent Classifier    │                    │
│              └──────────┬───────────┘                    │
│                         │                                 │
│                         ▼                                 │
│              ┌──────────────────────┐                    │
│              │ Agent Routing        │                    │
│              └──────────┬───────────┘                    │
│                         │                                 │
│                         ▼                                 │
│              ┌──────────────────────┐                    │
│              │ Query Agents         │                    │
│              └──────────┬───────────┘                    │
│                         │                                 │
│                         ▼                                 │
│                    Response                               │
└──────────────────────────────────────────────────────────┘

Problem: No way to refer to previous responses
```

### After Fix

```
┌──────────────────────────────────────────────────────────┐
│                    Query Received                         │
│                         │                                 │
│                         ▼                                 │
│              ┌──────────────────────┐                    │
│              │ Is Meta-Command?     │◀──── NEW!          │
│              └──────────┬───────────┘                    │
│                         │                                 │
│             ┌───────────┴───────────┐                    │
│             │                       │                     │
│             ▼                       ▼                     │
│     ┌──────────────┐      ┌──────────────┐              │
│     │ YES: Reformat│      │ NO: Continue │              │
│     │ Last Response│      │ Normal Flow  │              │
│     └──────┬───────┘      └──────┬───────┘              │
│            │                     │                        │
│            │                     ▼                        │
│            │          ┌──────────────────────┐           │
│            │          │ Intent Classifier    │           │
│            │          └──────────┬───────────┘           │
│            │                     │                        │
│            │                     ▼                        │
│            │          ┌──────────────────────┐           │
│            │          │ Agent Routing        │           │
│            │          └──────────┬───────────┘           │
│            │                     │                        │
│            │                     ▼                        │
│            │          ┌──────────────────────┐           │
│            │          │ Query Agents         │           │
│            │          └──────────┬───────────┘           │
│            │                     │                        │
│            └─────────────────────┘                        │
│                         │                                 │
│                         ▼                                 │
│                    Response                               │
└──────────────────────────────────────────────────────────┘

Solution: Meta-commands handled before agent routing
```

---

## Example: Deployment List Transformation

### Input (Previous Response)
```
Executive, 17 features are deployed in production: Stripe payment
gateway integration (v2.4.0), Fraud detection rules engine (v1.8.2),
Account reconciliation automation (v3.1.0), Fraud scoring optimization 1
(v1.7.1), Reconciliation observability 2 (v3.1.6)...
```

### Output (Formatted Table)
```
Executive, here are the production deployments:

| # | Feature                               | Version |
|---|---------------------------------------|---------|
| 1 | Stripe payment gateway integration    | v2.4.0  |
| 2 | Fraud detection rules engine          | v1.8.2  |
| 3 | Account reconciliation automation     | v3.1.0  |
| 4 | Fraud scoring optimization 1          | v1.7.1  |
| 5 | Reconciliation observability 2        | v3.1.6  |
...

**Total: 17 features deployed in production**
```

---

## State Machine: Conversation Context

```
         START
           │
           ▼
    ┌────────────┐
    │ No Context │
    └─────┬──────┘
          │
          │ User asks question
          ▼
    ┌─────────────────┐
    │ Agent Responds  │──────┐
    │ Saves to history│      │
    └─────┬───────────┘      │
          │                  │
          │ User asks        │ User asks
          │ meta-command     │ new question
          │                  │
          ▼                  ▼
    ┌─────────────────┐  ┌─────────────────┐
    │ Reformat Handler│  │ Agent Responds  │
    │ Uses history    │  │ Saves to history│
    └─────┬───────────┘  └─────┬───────────┘
          │                    │
          └────────┬───────────┘
                   │
                   ▼
            ┌─────────────┐
            │ Back to     │
            │ Has Context │
            └─────────────┘
```

---

## Success Flow

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ CONVERSATION FLOW - SUCCESSFUL                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

User:     "what features are in production"
          │
          ▼
System:   Queries ServiceNow
          Returns: "17 features deployed..."
          Saves to history
          │
          ▼
User:     "format your response"
          │
          ▼
System:   Detects meta-command ✓
          Retrieves last response ✓
          Formats as table ✓
          Returns formatted result ✓
          │
          ▼
User:     😊 "Thanks, much clearer!"
          │
          ▼
System:   Context preserved ✓
          User satisfied ✓
          Conversation continues ✓

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ RESULT: Smooth conversation, context maintained           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```
