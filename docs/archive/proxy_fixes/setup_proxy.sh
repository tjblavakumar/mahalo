#!/bin/bash
# Quick setup script for Linux/Mac to configure proxy for MAHALO
# Usage: source setup_proxy.sh [proxy_server:port]

echo "========================================"
echo "MAHALO Proxy Configuration Setup"
echo "========================================"
echo ""

if [ -z "$1" ]; then
    echo "Usage: source setup_proxy.sh [proxy_server:port]"
    echo "Example: source setup_proxy.sh proxy.company.com:8080"
    echo ""
    echo "Or run without arguments to set only NO_PROXY for localhost"
    echo ""
    
    # Set NO_PROXY even without proxy server
    export NO_PROXY="localhost,127.0.0.1,::1"
    echo "[OK] NO_PROXY set to: $NO_PROXY"
    echo ""
    echo "To persist these settings, add them to ~/.bashrc or ~/.zshrc"
    echo "or add them to the .env file in the project root."
    echo ""
    return 0 2>/dev/null || exit 0
fi

# Set proxy settings
export HTTP_PROXY="http://$1"
export HTTPS_PROXY="http://$1"
export NO_PROXY="localhost,127.0.0.1,::1"

echo "[OK] HTTP_PROXY set to: $HTTP_PROXY"
echo "[OK] HTTPS_PROXY set to: $HTTPS_PROXY"
echo "[OK] NO_PROXY set to: $NO_PROXY"
echo ""

echo "========================================"
echo "Configuration Complete!"
echo "========================================"
echo ""
echo "IMPORTANT: These settings are only for this terminal session."
echo ""
echo "To persist these settings:"
echo "1. Add to ~/.bashrc or ~/.zshrc:"
echo "   export HTTP_PROXY=$HTTP_PROXY"
echo "   export HTTPS_PROXY=$HTTPS_PROXY"
echo "   export NO_PROXY=$NO_PROXY"
echo ""
echo "2. Or add to .env file:"
echo "   HTTP_PROXY=$HTTP_PROXY"
echo "   HTTPS_PROXY=$HTTPS_PROXY"
echo "   NO_PROXY=$NO_PROXY"
echo ""
echo "Next steps:"
echo "1. Start MAHALO services"
echo "2. Run: python test_proxy_config.py"
echo ""
