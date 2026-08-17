@echo off
REM ============================================================
REM Quick Proxy Fix for MAHALO
REM This script updates NO_PROXY to include localhost
REM ============================================================
echo.
echo ============================================================
echo MAHALO - Proxy Fix Utility
echo ============================================================
echo.

REM Check current NO_PROXY setting
echo Current proxy configuration:
echo   HTTP_PROXY: %HTTP_PROXY%
echo   NO_PROXY: %NO_PROXY%
echo.

REM Check if localhost is already in NO_PROXY
if defined NO_PROXY (
    echo %NO_PROXY% | findstr /C:"localhost" >nul
    if errorlevel 1 (
        echo [ACTION] localhost NOT found in NO_PROXY - Adding it...
        SET "NO_PROXY=localhost,127.0.0.1,%NO_PROXY%"
        echo [SUCCESS] Updated NO_PROXY to: %NO_PROXY%
    ) else (
        echo [OK] localhost already in NO_PROXY - no changes needed
        goto :end
    )
) else (
    echo [ACTION] NO_PROXY not set - Setting it now...
    SET "NO_PROXY=localhost,127.0.0.1"
    echo [SUCCESS] Set NO_PROXY to: %NO_PROXY%
)

echo.
echo ============================================================
echo Fix Applied!
echo ============================================================
echo.
echo IMPORTANT: This fix is only active in this command prompt session.
echo.
echo To make it permanent:
echo   1. Run this in PowerShell as Administrator:
echo      [Environment]::SetEnvironmentVariable("NO_PROXY", "localhost,127.0.0.1,%NO_PROXY%", "User")
echo.
echo   2. Or add to .env file:
echo      NO_PROXY=localhost,127.0.0.1,.frgb.gov,.frb.org,.frb.pvt,.base.awscfs.frb.pvt,.frb.gov,.frbres.org
echo.
echo   3. Or use Windows Environment Variables dialog:
echo      - Search "Environment Variables" in Windows
echo      - Edit NO_PROXY under User Variables
echo      - Add "localhost,127.0.0.1" at the beginning
echo.
echo ============================================================
echo Next Steps:
echo ============================================================
echo 1. Keep this window open
echo 2. Run: python check_services.py
echo 3. If services are running, test queries in MAHALO
echo.

:end
pause
