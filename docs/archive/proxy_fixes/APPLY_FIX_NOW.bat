@echo off
REM Immediate fix for NO_PROXY issue
REM Run this script, then test again

echo ============================================================
echo MAHALO - Immediate NO_PROXY Fix
echo ============================================================
echo.

echo Current NO_PROXY: %NO_PROXY%
echo.

SET "NO_PROXY=localhost,127.0.0.1,.frgb.gov,.frb.org,.frb.pvt,.base.awscfs.frb.pvt,.frb.gov,.frbres.org"

echo Updated NO_PROXY: %NO_PROXY%
echo.
echo [SUCCESS] NO_PROXY has been updated for this session!
echo.
echo ============================================================
echo IMPORTANT: Keep this window open!
echo ============================================================
echo.
echo This fix only applies to THIS command prompt session.
echo Run your tests from THIS WINDOW.
echo.
echo Next steps:
echo   1. From THIS window, run: python test_proxy_config.py
echo   2. You should now see Status: 200 for all tests
echo   3. Start services from THIS window: scripts\start_all.bat
echo.
echo To make this permanent, see instructions at the end.
echo.
pause

REM Keep the window open in the new environment
cmd /k
