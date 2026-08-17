# Proxy Configuration Guide

## Problem
If you're behind a corporate proxy, the MAHALO agents (JIRA, ServiceNow, Splunk) may fail to connect to APIs, returning 0 results even though the services are running.

## Solution
The code has been fixed to support proxy configuration through environment variables. Here's how to configure it:

## Configuration Steps

### Option 1: Environment Variables (Recommended)

#### Windows Command Prompt
```cmd
SET HTTP_PROXY=http://your-proxy-server:port
SET HTTPS_PROXY=http://your-proxy-server:port
SET NO_PROXY=localhost,127.0.0.1,::1
```

#### Windows PowerShell
```powershell
$env:HTTP_PROXY="http://your-proxy-server:port"
$env:HTTPS_PROXY="http://your-proxy-server:port"
$env:NO_PROXY="localhost,127.0.0.1,::1"
```

#### Linux/Mac
```bash
export HTTP_PROXY=http://your-proxy-server:port
export HTTPS_PROXY=http://your-proxy-server:port
export NO_PROXY=localhost,127.0.0.1,::1
```

### Option 2: .env File
Add these lines to your `.env` file in the project root:

```env
HTTP_PROXY=http://your-proxy-server:port
HTTPS_PROXY=http://your-proxy-server:port
NO_PROXY=localhost,127.0.0.1,::1
```

### Option 3: System-Wide Configuration

#### Windows
1. Open System Properties → Advanced → Environment Variables
2. Add system variables:
   - `HTTP_PROXY`: `http://your-proxy-server:port`
   - `HTTPS_PROXY`: `http://your-proxy-server:port`
   - `NO_PROXY`: `localhost,127.0.0.1,::1`

## Proxy with Authentication

If your proxy requires authentication:

```
HTTP_PROXY=http://username:password@your-proxy-server:port
HTTPS_PROXY=http://username:password@your-proxy-server:port
```

**Security Note**: For better security, consider using Windows Credential Manager or a secure vault instead of hardcoding credentials.

## Important: NO_PROXY Configuration

The `NO_PROXY` variable is crucial! It tells httpx to bypass the proxy for local services:

```
NO_PROXY=localhost,127.0.0.1,::1,*.local,host.docker.internal
```

Without this, your local API calls (localhost:5001, localhost:5002, localhost:5003) will try to go through the proxy and fail.

## Testing Proxy Configuration

Run the test script to verify your proxy configuration:

```bash
python test_proxy_config.py
```

This script will:
1. Display your current proxy environment variables
2. Test connections to JIRA, ServiceNow, and Splunk APIs
3. Provide recommendations if issues are detected

## What Was Fixed

The following files were updated to enable proxy support:

1. **mcp_servers/jira_mcp/tools.py** - Changed `trust_env=False` to `trust_env=True`
2. **mcp_servers/servicenow_mcp/tools.py** - Changed `trust_env=False` to `trust_env=True`
3. **mcp_servers/splunk_mcp/tools.py** - Changed `trust_env=False` to `trust_env=True`
4. **backend/config.py** - Added proxy configuration support and helper functions

### Why trust_env=True?

When `trust_env=True`, httpx automatically:
- Reads `HTTP_PROXY` and `HTTPS_PROXY` environment variables
- Respects `NO_PROXY` for local/internal services
- Handles proxy authentication if provided in the URL

The previous setting `trust_env=False` explicitly disabled all proxy support, causing all API calls to fail in corporate proxy environments.

## Troubleshooting

### Issue: Still getting 0 results after setting proxy

**Check:**
1. Verify environment variables are set correctly:
   ```bash
   # Windows CMD
   echo %HTTP_PROXY%
   
   # PowerShell
   echo $env:HTTP_PROXY
   
   # Linux/Mac
   echo $HTTP_PROXY
   ```

2. Ensure you've restarted the application after setting environment variables

3. Run the test script: `python test_proxy_config.py`

### Issue: Proxy works but local services timeout

**Solution:** Add localhost to NO_PROXY:
```
NO_PROXY=localhost,127.0.0.1,::1
```

### Issue: Certificate verification errors

If you get SSL certificate errors through the proxy, you may need to add your corporate CA certificate or temporarily disable verification (not recommended for production):

```python
# In tools.py files, you can add:
verify="/path/to/corporate-ca-cert.pem"  # Point to your CA bundle
# or
verify=False  # NOT recommended - only for testing
```

### Issue: Proxy authentication failures

1. Verify your credentials are correct
2. Check if your proxy requires domain authentication: `domain\\username:password`
3. Special characters in password may need URL encoding

## Common Proxy Servers

### Corporate Environments
- Microsoft TMG/Forefront: Usually port 8080 or 8888
- Squid Proxy: Usually port 3128
- Blue Coat: Usually port 8080
- Zscaler: Usually automatic PAC configuration

### Finding Your Proxy Settings (Windows)

1. Open Internet Options (Control Panel)
2. Go to Connections tab → LAN Settings
3. Note the proxy server address and port
4. Or check "Use automatic configuration script" for PAC URL

## Additional Resources

- [httpx proxy documentation](https://www.python-httpx.org/advanced/#http-proxying)
- [Environment variables for proxies](https://about.gitlab.com/blog/2021/01/27/we-need-to-talk-no-proxy/)

## Need Help?

If you're still experiencing issues:
1. Run `python test_proxy_config.py` and share the output
2. Check that backend services are running on ports 5001, 5002, 5003
3. Verify your proxy server is accessible
4. Check firewall/network settings
