# ============================================================
# MAHALO - Permanent Proxy Fix (PowerShell)
# This script permanently updates NO_PROXY in user environment
# Run with: powershell -ExecutionPolicy Bypass -File fix_proxy_permanent.ps1
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "MAHALO - Permanent Proxy Fix Utility" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get current NO_PROXY from user environment
$currentNoProxy = [Environment]::GetEnvironmentVariable("NO_PROXY", "User")

Write-Host "Current NO_PROXY (User): " -NoNewline
if ($currentNoProxy) {
    Write-Host $currentNoProxy -ForegroundColor Yellow
} else {
    Write-Host "(not set)" -ForegroundColor Gray
}
Write-Host ""

# Check if localhost is already included
if ($currentNoProxy -like "*localhost*") {
    Write-Host "[OK] localhost is already in NO_PROXY" -ForegroundColor Green
    Write-Host "No changes needed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

# Prepare new NO_PROXY value
if ($currentNoProxy) {
    $newNoProxy = "localhost,127.0.0.1,$currentNoProxy"
    Write-Host "[ACTION] Will add localhost to existing NO_PROXY" -ForegroundColor Yellow
} else {
    # If NO_PROXY is not set, get from system environment as fallback
    $systemNoProxy = [Environment]::GetEnvironmentVariable("NO_PROXY", "Machine")
    if ($systemNoProxy) {
        $newNoProxy = "localhost,127.0.0.1,$systemNoProxy"
        Write-Host "[ACTION] Will create user NO_PROXY based on system settings" -ForegroundColor Yellow
    } else {
        $newNoProxy = "localhost,127.0.0.1"
        Write-Host "[ACTION] Will create new NO_PROXY with localhost only" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "New NO_PROXY will be: " -NoNewline
Write-Host $newNoProxy -ForegroundColor Cyan
Write-Host ""

# Ask for confirmation
Write-Host "Do you want to apply this change? [Y/N]: " -NoNewline -ForegroundColor Yellow
$confirmation = Read-Host

if ($confirmation -eq 'Y' -or $confirmation -eq 'y') {
    try {
        # Set the new NO_PROXY in user environment
        [Environment]::SetEnvironmentVariable("NO_PROXY", $newNoProxy, "User")
        
        # Also set in current session
        $env:NO_PROXY = $newNoProxy
        
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "[SUCCESS] NO_PROXY updated successfully!" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "New value: $newNoProxy" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "IMPORTANT:" -ForegroundColor Yellow
        Write-Host "  1. The change is now permanent (saved in User Environment)" -ForegroundColor White
        Write-Host "  2. Current terminal session is updated" -ForegroundColor White
        Write-Host "  3. You may need to restart other applications to pick up the change" -ForegroundColor White
        Write-Host ""
        Write-Host "Next Steps:" -ForegroundColor Cyan
        Write-Host "  1. Test with: python check_services.py" -ForegroundColor White
        Write-Host "  2. Start MAHALO: scripts\start_all.bat" -ForegroundColor White
        Write-Host "  3. Run full test: python test_proxy_config.py" -ForegroundColor White
        Write-Host ""
        
    } catch {
        Write-Host ""
        Write-Host "[ERROR] Failed to update NO_PROXY: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "Try running PowerShell as Administrator" -ForegroundColor Yellow
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "[CANCELLED] No changes made" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
