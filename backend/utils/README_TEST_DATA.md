# Test Data Generation - Enhanced with LLM

## Overview

We now have **two test data generators**:

### 1. Original Generator (`generate_test_data.py`)
- **Pros**: Fast, deterministic, no API calls
- **Cons**: Repetitive, generic descriptions, limited variety
- **Use case**: Quick local testing, CI/CD pipelines

### 2. LLM-Enhanced Generator (`generate_test_data_llm.py`) ⭐ NEW
- **Pros**: Realistic, diverse, rich context, no duplicates
- **Cons**: Requires LLM API, slightly slower
- **Use case**: Demos, development, realistic testing scenarios

## Quick Start

### Install Dependencies (if needed)
```bash
cd MAHALO/mahalo-main
pip install openai
```

### Configure LLM
Set your API key in `.env`:
```bash
ONE_MIN_AI_API_KEY=your_api_key_here
ONE_MIN_AI_BASE_URL=https://api.1min.ai/v1
LITELLM_MODEL=gpt-4o-mini
```

### Generate Enhanced Test Data

#### Quick Demo Dataset (recommended for first try)
```bash
python backend/utils/generate_test_data_llm.py --quick
```

This generates:
- 10 JIRA stories with detailed descriptions
- 5 JIRA bugs with reproduction steps
- 2 sprints
- 8 ServiceNow incidents with timelines
- 6 deployments
- 15 Splunk logs with context

#### Custom Dataset
```bash
python backend/utils/generate_test_data_llm.py \
  --jira-stories 20 \
  --jira-bugs 10 \
  --jira-sprints 3 \
  --servicenow-incidents 15 \
  --servicenow-deployments 10 \
  --splunk-logs 50
```

#### Reset and Start Fresh
```bash
python backend/utils/generate_test_data_llm.py --quick --reset
```

## Key Improvements

### 🎯 Better Descriptions
**Before (Original):**
```
Title: Payment authorization improvement 1234
Description: Improve authorization reliability for checkout transactions.
```

**After (LLM-Enhanced):**
```
Title: Implement 3DS2 Strong Customer Authentication (SCA) for EU payments
Description: As a payment engineer, I need to implement 3DS2 authentication 
for all EU payment transactions to comply with PSD2 regulations.

Acceptance Criteria:
- Challenge flow triggers for transactions >€30
- Frictionless flow for low-risk transactions
- Proper handling of authentication timeouts
- Fallback to 3DS1 for unsupported issuers

Technical Context:
- Integrate with Stripe's 3DS2 API
- Store authentication results in payment_authorizations table
- Add retry logic for authentication timeouts
- Monitor authentication success rates in DataDog

Business Value:
Ensures EU regulatory compliance and reduces cart abandonment by 
implementing intelligent authentication flows.
```

### 🎨 More Variety
- **User names**: Diverse cultures and backgrounds
- **Story topics**: Payment-specific scenarios (3DS, SCA, PSD2, chargebacks, settlements)
- **Bug reports**: Real technical issues (race conditions, deadlocks, timeouts)
- **Incidents**: Detailed timelines with metrics and SLO impact
- **Logs**: Realistic error messages with IDs and context

### 🚫 No Duplicates
The LLM generates unique content each time, avoiding repetitive patterns.

### 📊 Rich Context
- JIRA stories include acceptance criteria and business value
- Bugs include reproduction steps and environment details
- Incidents include detection methods and resolution timelines
- Logs include transaction IDs, latency metrics, and error codes

## Performance Comparison

| Metric | Original | LLM-Enhanced |
|--------|----------|--------------|
| Speed for 10 stories | ~0.5s | ~3-5s |
| Description quality | Generic | Detailed & contextual |
| Variety | Low (same patterns) | High (unique each time) |
| Realism | Basic | Production-grade |
| API cost | Free | ~$0.01 per 100 items |

## Best Practices

### For Development
```bash
# Start with quick dataset
python backend/utils/generate_test_data_llm.py --quick

# Add more as needed without resetting
python backend/utils/generate_test_data_llm.py --jira-stories 5
```

### For Demos
```bash
# Generate comprehensive realistic dataset
python backend/utils/generate_test_data_llm.py --reset \
  --jira-stories 30 \
  --jira-bugs 15 \
  --jira-sprints 5 \
  --servicenow-incidents 20 \
  --servicenow-deployments 15 \
  --splunk-logs 100
```

### For CI/CD (Fast)
```bash
# Use original generator for speed
python backend/utils/generate_test_data.py \
  --jira-data 10 \
  --servicenow-data 5 \
  --splunk-data 20
```

## Troubleshooting

### "No API key" error
Set your LLM API key in `.env`:
```bash
ONE_MIN_AI_API_KEY=your_key_here
```

### "JSON parsing error"
The LLM occasionally returns malformed JSON. The script automatically extracts JSON from markdown blocks. If issues persist, try:
- Using a different seed: `--seed 123`
- Reducing batch size: generate fewer items per call

### "Too slow"
- Use `--quick` for smaller datasets
- Use original generator for speed: `generate_test_data.py`
- Reduce item counts

## Examples

### Generate Stories Only
```bash
python backend/utils/generate_test_data_llm.py --jira-stories 15 --jira-sprints 2
```

### Generate Incidents and Logs
```bash
python backend/utils/generate_test_data_llm.py \
  --servicenow-incidents 20 \
  --splunk-logs 50
```

### Fresh Start with Everything
```bash
python backend/utils/generate_test_data_llm.py --reset \
  --jira-stories 25 \
  --jira-bugs 12 \
  --jira-sprints 4 \
  --servicenow-incidents 18 \
  --servicenow-deployments 12 \
  --splunk-logs 75
```

## Architecture

The LLM generator uses structured prompts to ensure:
1. **Consistency**: All responses follow the same JSON schema
2. **Quality**: Detailed descriptions with proper technical context
3. **Variety**: High temperature (0.8-0.9) for diverse outputs
4. **Domain accuracy**: Prompts include payment platform context

## Migration Guide

To switch from old to new generator:

```bash
# Old way
python backend/utils/generate_test_data.py --jira-data 10

# New way (equivalent)
python backend/utils/generate_test_data_llm.py \
  --jira-stories 10 \
  --jira-bugs 2 \
  --jira-sprints 1
```

Both generators work side-by-side. You can use the old one for CI/CD speed and the new one for realistic demo data.

## Future Enhancements

Potential improvements:
- [ ] Batch processing for better performance
- [ ] Cache generated content for reuse
- [ ] Custom domain/industry prompts
- [ ] Generate related data (bugs linked to stories)
- [ ] Time-series data generation
- [ ] Multi-language support
- [ ] Custom templates per team

## Feedback

This is a new feature! Please report:
- Quality issues (unrealistic data)
- Performance problems
- Feature requests
- Bug reports

---

**Happy Testing! 🚀**
