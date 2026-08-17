# Quick Fix: Proxy Setup for MAHALO

## 🚨 Problem
Agents returning 0 results? You're likely behind a corporate proxy!

## ✅ Quick Solution

### Step 1: Set Proxy Environment Variables

**Windows PowerShell:**
```powershell
$env:NO_PROXY="localhost,127.0.0.1"
$env:HTTP_PROXY="http://your-proxy:port"
$env:HTTPS_PROXY="http://your-proxy:port"
```

**Windows CMD:**
```cmd
SET NO_PROXY=localhost,127.0.0.1
SET HTTP_PROXY=http://your-proxy:port
SET HTTPS_PROXY=http://your-proxy:port
```

### Step 2: Restart MAHALO Services
Stop all running services and restart them for the changes to take effect.

### Step 3: Test
```bash
python test_proxy_config.py
```

## 🔍 Finding Your Proxy Settings

**Windows:**
1. Open "Internet Options" in Control Panel
2. Go to "Connections" → "LAN Settings"
3. Note the proxy server address and port

**Or check system proxy:**
```powershell
# PowerShell
netsh winhttp show proxy

# Check current environment
echo $env:HTTP_PROXY
```

## 🎯 Key Point

The critical fix is setting `NO_PROXY=localhost,127.0.0.1` to ensure local API calls bypass the proxy!

## 📖 More Details

See `PROXY_CONFIGURATION.md` for complete documentation.
