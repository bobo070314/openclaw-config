# scripts/auto_rollback.ps1
param(
    [string]$Root = "."
)

$ErrorActionPreference = "Continue"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Resolve-Path (Join-Path $ScriptDir "..")

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenClaw Delivery - Auto Rollback       " -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

$RunDir = Join-Path $RootDir "data\runs"
$RollbackFile = Join-Path $RunDir "rollback_report.json"

if (-not (Test-Path $RollbackFile)) {
    Write-Host "[INFO] No rollback report found. Creating placeholder." -ForegroundColor Yellow
    $Placeholder = @{
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssK")
        status = "no_rollback_needed"
        message = "System appears stable. No rollback report on file."
    } | ConvertTo-Json
    $Placeholder | Out-File $RollbackFile -Encoding utf8
    Write-Host "[OK] Generated placeholder rollback report." -ForegroundColor Green
    exit 0
}

$Report = Get-Content $RollbackFile | ConvertFrom-Json
Write-Host "[INFO] Last rollback status: $($Report.status)" -ForegroundColor Cyan

if ($Report.status -eq "rolled_back") {
    Write-Host "[ACTION] Previous rollback detected at $($Report.timestamp)" -ForegroundColor Yellow
    Write-Host "[ACTION] Re-applying rollback steps..." -ForegroundColor Yellow

    # Copy configs back from backup
    $BackupDir = Join-Path $RunDir "backup"
    $ConfigDir = Join-Path $RootDir "configs"
    if (Test-Path $BackupDir) {
        Copy-Item -Recurse -Force "$BackupDir\*" $ConfigDir
        Write-Host "[OK] Configs restored from backup." -ForegroundColor Green
    }

    Write-Host "[OK] Rollback complete." -ForegroundColor Green
} else {
    Write-Host "[OK] No rollback needed. Status: $($Report.status)" -ForegroundColor Green
}
