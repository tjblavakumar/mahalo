# Quick Test Guide

## 🧪 How to Test the Fixes

All four bugs have been fixed. Here's how to test them:

---

## Test 1: Format Response (Bug #1)

### Steps:
```
1. Start MAHALO
2. User: "what features are in production"
3. Wait for response (long comma-separated list)
4. User: "format your response"
```

### Expected Result:
```
Executive, here are the production deployments:

| # | Feature                            | Version |
|---|------------------------------------|---------|
| 1 | Stripe payment gateway integration | v2.4.0  |
| 2 | Fraud detection rules engine       | v1.8.2  |
...

**Total: 17 features deployed in production**
```

### ✅ Pass Criteria:
- Response is formatted as table
- NOT search results from agents
- Features are listed clearly

---

## Test 2: Elaboration Request (Bug #2)

### Steps:
```
1. User: "executive overview"
2. Wait for response (contains "Reliability score is 29.9%...")
3. User: "why do you recommend this. justify with more details"
```

### Expected Result:
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

With an error rate of 70.2%...

**Identified Gaps:**
- Gateway Timeout: 89 errors
- Connection Pool: 76 errors

**Cross-System Correlations:**
- Error theme 'gateway_timeout' has no corresponding JIRA stories
...
```

### ✅ Pass Criteria:
- Shows HOW score was calculated
- Shows WHY prioritization decision made
- Lists specific gaps and correlations
- NOT generic search results

---

## Test 3: Story Drafting (Bug #3)

### Steps:
```
1. User: "help me write a user story for payment gateway timeout recovery"
```

### Expected Result:
```
Executive, here is the complete JIRA story draft:

Title: Improve payment gateway timeout recovery and provider failover
Description: Handle provider timeouts with bounded retries, safe failure
states, and provider failover to ensure payment processing reliability.

Priority: High
Story points: 8
Sprint: Sprint 24

User story: As a MahaloPay customer, I want improve payment gateway timeout
recovery and provider failover, so that payment processing remains reliable.

Acceptance criteria:
- Payment gateway timeouts use bounded retries with exponential backoff
- Automatic failover to secondary provider when primary times out
- Retries do not duplicate a successful payment transaction
- Timeout events are logged with provider and transaction context
- Monitoring alerts when failover rate exceeds threshold
- Automated tests cover timeout, retry, and recovery scenarios

Evidence:
- Payment gateway timeout after 30 seconds for high-value transaction.
- Downstream payment provider returned intermittent 502 responses.

This is still a draft. Say 'create this story in JIRA' to save it.
```

### ✅ Pass Criteria:
- Complete story draft returned
- Topic-specific acceptance criteria (timeout/failover)
- Evidence from production logs
- NOT search results

---

## Test 4: Compound Query (Bug #4)

### Steps:
```
1. User: "tell me what is in production and what is pending"
```

### Expected Result:
```
Executive, here's your production and pending status:

## In Production (17 features)

| # | Feature                            | Version |
|---|------------------------------------|---------|
| 1 | Stripe payment gateway integration | v2.4.0  |
| 2 | Fraud detection rules engine       | v1.8.2  |
| 3 | Account reconciliation automation  | v3.1.0  |
...

## Pending in Backlog (23 stories)

**High Priority:**
- STORY-105: Improve payment gateway timeout recovery (8 pts)
- STORY-112: Protect payment capacity during spikes (8 pts)

**Medium Priority:**
- STORY-108: Strengthen reconciliation detection (5 pts)
- STORY-115: Add payment latency monitoring (5 pts)

_Total pending work: 89 story points_
```

### ✅ Pass Criteria:
- Both sections present (Production AND Pending)
- Deployments are shown (not incidents)
- Pending stories are filtered by backlog status
- Clean, structured format
- NOT "unknown, unknown, unknown" or unfiltered results

---

## Edge Case Tests

### Test 5: Format with No History
```
1. User: "format your response" (first message)
Expected: "I don't have a previous response to format."
```

### Test 6: Elaboration with No History
```
1. User: "explain that" (first message)
Expected: "I don't have a previous response to elaborate on."
```

### Test 7: Story Draft with No Topic
```
1. User: "help me write a user story"
Expected: "What feature or issue should the story address?"
```

---

## Regression Tests

### Test 8: Normal Queries Still Work
```
1. User: "show me bugs"
   Expected: Bug list (as before)

2. User: "executive overview"
   Expected: Executive summary (as before)

3. User: "what are the deployments"
   Expected: Deployment list (as before)
```

---

## Quick Verification Checklist

After running all tests, verify:

- [ ] Format requests work (Bug #1)
- [ ] Elaboration shows calculations (Bug #2)
- [ ] Story drafting creates complete drafts (Bug #3)
- [ ] Compound queries handle both parts (Bug #4)
- [ ] Edge cases handled gracefully
- [ ] Normal queries still work (no regressions)

---

## If Tests Fail

### Troubleshooting

**If format/elaboration requests still search agents:**
- Check that conversation_history is being passed to process_query
- Verify detection methods are being called

**If elaboration doesn't show calculations:**
- Check that self.last_insights is populated
- Verify correlation_engine.correlate_contexts() was called

**If story drafting still searches:**
- Check detection keywords match your query
- Verify topic extraction logic

**If compound query still returns bad results:**
- Check production+pending detection
- Verify _get_pending_stories() filters by status
- Check that deployments (not incidents) are returned

---

## Success Criteria

✅ **All four bugs are fixed when:**
1. "format your response" reformats (doesn't search)
2. "why do you recommend this" explains (doesn't search)
3. "help me write a story for X" drafts complete story (doesn't search)
4. "what is in production and what is pending" returns both sections properly formatted

---

## 🎉 Ready to Test!

Start MAHALO and run through these tests. All four bugs should now be fixed!

**Commands to start:**
```bash
# Windows
cd MAHALO\mahalo-main
scripts\start_all.bat

# Linux
cd MAHALO/mahalo-main
./scripts/start_all.sh
```

Then open browser to `http://localhost:3000` and test the queries above.

**Good luck! 🚀**
