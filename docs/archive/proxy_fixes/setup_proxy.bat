@echo off
REM Quick setup script for Windows to configure proxy for MAHALO
REM Run this before starting MAHALO services

echo ========================================
echo MAHALO Proxy Configuration Setup
echo ========================================
echo.

REM Check if proxy server is provided as argument
if "%1"=="" (
    echo Usage: setup_proxy.bat [proxy_server:port]
    echo Example: setup_proxy.bat proxy.company.com:8080
    echo.
    echo Or run without arguments to set only NO_PROXY for localhost
    echo.
    
    REM Set NO_PROXY even without proxy server
    SET NO_PROXY=localhost,127.0.0.1,::1
    echo [OK] NO_PROXY set to: %NO_PROXY%
    echo.
    echo To persist these settings, add them to your System Environment Variables
    echo or add them to the .env file in the project root.
    echo.
    pause
    exit /b 0
)

REM Set proxy settings
SET HTTP_PROXY=http://%1
SET HTTPS_PROXY=http://%1
SET NO_PROXY=localhost,127.0.0.1,::1

echo [OK] HTTP_PROXY set to: %HTTP_PROXY%
echo [OK] HTTPS_PROXY set to: %HTTPS_PROXY%
echo [OK] NO_PROXY set to: %NO_PROXY%
echo.

echo ========================================
echo Configuration Complete!
echo ========================================
echo.
echo IMPORTANT: These settings are only for this command prompt session.
echo.
echo To persist these settings:
echo 1. Add to System Environment Variables (Windows Settings)
echo 2. Or add to .env file:
echo    HTTP_PROXY=%HTTP_PROXY%
echo    HTTPS_PROXY=%HTTPS_PROXY%
echo    NO_PROXY=%NO_PROXY%
echo.
echo Next steps:
echo 1. Keep this command prompt open
echo 2. Start MAHALO services from this window
echo 3. Run: python test_proxy_config.py
echo.
pause
