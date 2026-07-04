# scripts/run_all.ps1
param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Resolve-Path (Join-Path $ScriptDir "..")

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenClaw Delivery - Run Pipeline       " -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

# 1. Source .env if present
$EnvFile = Join-Path $RootDir ".env"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match "^\s*([^#=]+)=(.*)$") {
            $Key = $matches[1].Trim()
            $Val = $matches[2].Trim().Trim('"', "'")
            Set-Item -Path "env:$Key" -Value $Val -ErrorAction SilentlyContinue
        }
    }
    Write-Host "[OK] Loaded .env" -ForegroundColor Green
}

# 2. Orchestrator
Write-Host "`n[MAIN] Running orchestrator..." -ForegroundColor Cyan
$Orch = Join-Path $ScriptDir "orchestrator.py"
if (Test-Path $Orch) {
    $env:PYTHONIOENCODING = 'utf-8'
    $env:PYTHONUTF8 = '1'
    & python $Orch
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Orchestrator finished." -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Orchestrator failed (exit code $LASTEXITCODE)" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} else {
    Write-Host "[WARN] orchestrator.py not found. Skipping." -ForegroundColor Yellow
}

# 3. Heartbeat verification
Write-Host "`n[CHECK] Running heartbeat..." -ForegroundColor Cyan
$Heartbeat = Join-Path $RootDir "family-corp-teams/v5/v6/api/igp_heartbeat.py"
if (Test-Path $Heartbeat) {
    & python $Heartbeat
} else {
    Write-Host "[WARN] heartbeat script not found. Skipping." -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RUN: DONE                               " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
