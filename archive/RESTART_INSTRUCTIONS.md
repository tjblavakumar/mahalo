# RESTART INSTRUCTIONS

## Issue Resolved! ✅

The root cause was that `httpx` (the Python HTTP client) was using corporate proxy settings 
which blocked localhost connections. 

### What Was Fixed

Added `trust_env=False` to all httpx.AsyncClient calls in:
- `mcp_servers/jira_mcp/tools.py`
- `mcp_servers/servicenow_mcp/tools.py`  
- `mcp_servers/splunk_mcp/tools.py`

This bypasses the proxy for localhost connections.

### How to Apply the Fix

**Option 1: Restart just the Main API** (Fastest)

1. Find the terminal window titled **"MAHALO - Main API (8000)"**
2. Press `Ctrl+C` to stop it
3. Run this command in that terminal:
   ```cmd
   cd C:\Users\L1LTB01\LavaCode\MAHALO\mahalo-main
   venv\Scripts\activate
   python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

**Option 2: Full Restart** (Most reliable)

1. Run: `scripts\stop_all.bat`
2. Wait for all services to stop
3. Run: `scripts\start_all.bat`

### Verification

After restarting, refresh your browser at http://localhost:3000 and ask:
```
executive summary
```

You should now see:
```
Executive, here is the MahaloPay executive update:
- Delivery: 3 tracked stories, 1 completed.
- Production: 3 deployed features.
- Operations: 2 active or monitoring incidents.
- Reliability: 5 error logs out of 8 total logs.
```

Instead of all zeros! 🎉
