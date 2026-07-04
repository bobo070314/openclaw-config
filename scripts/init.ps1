# scripts/init.ps1
param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Resolve-Path (Join-Path $ScriptDir "..")

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenClaw Delivery - Initializer       " -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

# 1. 检查 .env
$EnvFile = Join-Path $RootDir ".env"
$EnvExample = Join-Path $RootDir ".env.example"
if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvExample) {
        Copy-Item $EnvExample $EnvFile
        Write-Host "[INFO] Created .env from .env.example." -ForegroundColor Yellow
        Write-Host "[INFO] Please fill in your API tokens in .env" -ForegroundColor Yellow
    } else {
        Write-Host "[WARN] .env.example not found. Creating minimal .env" -ForegroundColor Yellow
        "# OPENCLAW_API_KEY=your_key_here" | Out-File $EnvFile -Encoding utf8
    }
} else {
    Write-Host "[OK] .env exists." -ForegroundColor Green
}

# 2. 创建必要目录
$Directories = @(
    "data/runs",
    "data/evals",
    "logs",
    "configs"
)
foreach ($Dir in $Directories) {
    $Path = Join-Path $RootDir $Dir
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "[OK] Created: $Dir" -ForegroundColor Green
    }
}

# 3. 验证 Python 环境
Write-Host "`n[STEP] Checking Python..." -ForegroundColor Cyan
try {
    $PyVer = & python --version 2>&1
    Write-Host "[OK] $PyVer" -ForegroundColor Green
} catch {
    Write-Host "[FATAL] Python not found. Install Python 3.10+" -ForegroundColor Red
    exit 1
}

# 4. 检查依赖
Write-Host "[STEP] Checking requirements..." -ForegroundColor Cyan
$ReqFile = Join-Path $RootDir "requirements.txt"
if (Test-Path $ReqFile) {
    & pip install -r $ReqFile -q 2>&1 | Out-Null
    Write-Host "[OK] Dependencies installed." -ForegroundColor Green
} else {
    Write-Host "[WARN] requirements.txt not found. Skipping." -ForegroundColor Yellow
}

# 5. 健康检查
Write-Host "`n[STEP] Health Check..." -ForegroundColor Cyan
$Healthy = $false
$Endpoints = @(
    "http://localhost:18900/v1/models",
    "http://localhost:8080/health"
)
foreach ($Ep in $Endpoints) {
    try {
        $Response = Invoke-RestMethod -Uri $Ep -TimeoutSec 3 -ErrorAction Stop
        Write-Host "[OK] $Ep -> reachable" -ForegroundColor Green
        $Healthy = $true
    } catch {
        Write-Host "[WARN] $Ep -> unreachable (normal if not started)" -ForegroundColor Yellow
    }
}

# 6. 验证脚本可执行
Write-Host "`n[STEP] Validating delivery scripts..." -ForegroundColor Cyan
$ExpectedScripts = @(
    "scripts/orchestrator.py",
    "scripts/auto_rollback.ps1",
    "configs/agent_chain.yaml",
    "dashboards/metrics.md"
)
$AllFound = $true
foreach ($Script in $ExpectedScripts) {
    $SPath = Join-Path $RootDir $Script
    if (Test-Path $SPath) {
        Write-Host "[OK] $Script" -ForegroundColor Green
    } else {
        Write-Host "[WARN] $Script not found" -ForegroundColor Yellow
        $AllFound = $false
    }
}

# 7. 最终验收
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($AllFound) {
    Write-Host "  INIT: OK - Environment Ready          " -ForegroundColor Green
} else {
    Write-Host "  INIT: OK - Some Optional Files Missing" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
exit 0
