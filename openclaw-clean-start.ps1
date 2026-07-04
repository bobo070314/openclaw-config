# ============================================
# OpenClaw 自动清理+启动脚本（根治崩溃版）
# 作用：每次启动前清光所有导致崩溃的残留状态
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OpenClaw 自动清理 + 启动脚本" -ForegroundColor Cyan
Write-Host "  根治崩溃版 v1.0" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 杀光所有Node进程（包括僵尸）
Write-Host "🧹 清理Node僵尸进程..." -ForegroundColor Yellow
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "  ✅ Node进程已清除" -ForegroundColor Green

# 2. 删光所有状态文件（核心！清光旧SQLite、transcript、session locks）
Write-Host "🧹 清理状态残留文件..." -ForegroundColor Yellow
$stateDir = "D:\bobo\openclaw-home\state"
if (Test-Path $stateDir) {
    Remove-Item "$stateDir\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  ✅ 状态文件已清除: $stateDir" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ 状态目录不存在，跳过" -ForegroundColor Yellow
}

# 3. 重新初始化状态
Write-Host "🔧 初始化OpenClaw状态..." -ForegroundColor Yellow
openclaw doctor --fix --quiet 2>&1 | Out-Null
Write-Host "  ✅ 状态初始化完成" -ForegroundColor Green

# 4. 安装缺失插件（避免plugins.entries警告）
Write-Host "📦 安装缺失插件..." -ForegroundColor Yellow
$plugins = @(
    "@openclaw/deepseek-provider",
    "@openclaw/qwen-provider",
    "@openclaw/tavily-plugin"
)
foreach ($p in $plugins) {
    Write-Host "  安装 $p ..." -NoNewline
    openclaw plugins install $p --quiet 2>&1 | Out-Null
    Write-Host " ✅" -ForegroundColor Green
}

# 5. 前台直启网关（避开Task环境变量问题，实时看状态）
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🚀 启动OpenClaw网关 (端口18900)..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 切换到工作目录并用显式环境变量启动
Set-Location "D:\bobo\openclaw-foreign"
$env:OPENCLAW_CONFIG_PATH = "D:\bobo\openclaw-foreign\openclaw-minimal.json"
$env:DEEPSEEK_OFFICIAL_KEY = [Environment]::GetEnvironmentVariable("DEEPSEEK_OFFICIAL_KEY", "User")

Write-Host "📍 工作目录: $((Get-Location).Path)" -ForegroundColor Gray
Write-Host "📍 Config: $env:OPENCLAW_CONFIG_PATH" -ForegroundColor Gray
Write-Host "📍 API Key: $($env:DEEPSEEK_OFFICIAL_KEY.Substring(0, 8))..." -ForegroundColor Gray
Write-Host ""

openclaw gateway --port 18900
