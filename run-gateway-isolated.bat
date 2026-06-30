@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

title OpenClaw-Foreign-Isolated -- PORT 18900

echo ========================================
echo   彻底隔离版: OpenClaw Foreign (18900)
echo ========================================
echo.

REM ========== 关键: 覆盖系统环境变量，彻底切断 QClaw 干扰 ==========

REM --- 强制指向 Foreign 自己的配置（对抗 QClaw 系统级 env var） ---
set "OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw.json"

REM --- 清除 QClaw LLM 拦截 ---
set "QCLAW_LLM_BASE_URL="
set "QCLAW_LLM_API_KEY="
set "QCLAW_PLUGIN_CONFIG_PATH="

REM --- 用独立的 state 目录 ---
set "OPENCLAW_STATE_DIR=D:\bobo\openclaw-foreign\state"

REM --- 禁止加载 bundle plugins（重要！防自动扫描 QClaw 扩展） ---
set "OPENCLAW_DISABLE_BUNDLED_PLUGINS=1"

REM --- 只保留核心 PATH，排除 QClaw ---
set "PATH=D:\Program Files\nodejs;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem"

REM --- 加载 .env（仅 Key，不含 CONF_PATH，因为已强制覆盖） ---
for /f "tokens=1,2 delims==" %%a in (D:\bobo\openclaw-foreign\.env) do (
    if not "%%a"=="" if not "%%a"=="#" set "%%a=%%b"
)

REM --- 确保 OPENCLAW_CONFIG_PATH 不被 .env 覆盖 ---
set "OPENCLAW_CONFIG_PATH=D:\bobo\openclaw-foreign\openclaw.json"

REM ========== 清理 ==========

REM --- 杀掉占用 18900 的旧进程 ---
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\kill-port.ps1" 18900

REM --- 清理锁文件 ---
if exist "D:\bobo\openclaw-foreign\state\gateway.lock" del /f "D:\bobo\openclaw-foreign\state\gateway.lock" >nul 2>&1

REM ========== 验证配置 ==========
echo.
echo === 环境变量检查 ===
echo OPENCLAW_CONFIG_PATH = %OPENCLAW_CONFIG_PATH%
echo QCLAW_LLM_BASE_URL   = [%QCLAW_LLM_BASE_URL%] (应为空)
echo QCLAW_LLM_API_KEY    = [%QCLAW_LLM_API_KEY%] (应为空)
echo OPENCLAW_DISABLE_BUNDLED_PLUGINS = %OPENCLAW_DISABLE_BUNDLED_PLUGINS%
echo PATH = %PATH%
echo.
echo Node:
"D:\Program Files\nodejs\node.exe" --version

echo.
echo === 启动 Gateway (18900) ===

"D:\Program Files\nodejs\node.exe" "D:\bobo\openclaw-foreign\openclaw\openclaw.mjs" gateway --port 18900

echo [%DATE% %TIME%] Gateway exited with code %ERRORLEVEL%
pause
