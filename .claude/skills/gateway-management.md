# Gateway Management

## Purpose
Manage the OpenClaw gateway on port 18900 — start, stop, test, and monitor.

## Commands
```powershell
# Start gateway
$env:OPENCLAW_CONFIG_PATH = 'openclaw-minimal.json'
node.exe .\openclaw\openclaw.mjs gateway --port 18900

# Stop gateway
$oldPid = (Get-NetTCPConnection -LocalPort 18900 -ErrorAction SilentlyContinue).OwningProcess
if ($oldPid) { Stop-Process -Id $oldPid -Force; Write-Host "Closed $oldPid" }

# Test gateway
$headers = @{Authorization = "***"}
$body = @{model="openclaw"; messages=@(@{role="user"; content="你好"})} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:18900/v1/chat/completions" -Method Post -Headers $headers -ContentType "application/json" -Body $body
```
