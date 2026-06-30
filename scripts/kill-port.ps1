# kill-port.ps1 - 按端口号清理占用进程
# 用法: powershell -ExecutionPolicy Bypass -File kill-port.ps1 <port>
param(
    [Parameter(Mandatory=$true)]
    [int]$Port
)

$ErrorActionPreference = 'SilentlyContinue'

# 查找占用端口的进程
$lines = netstat -ano | Select-String ":$Port.*LISTENING"
if ($lines) {
    foreach ($line in $lines) {
        $parts = $line -split '\s+' | Where-Object { $_ -ne '' }
        $pid = $parts[-1]
        if ($pid -match '^\d+$') {
            Write-Host "[kill-port] Killing PID $pid on port $Port"
            Stop-Process -Id $pid -Force
            Start-Sleep -Seconds 1
        }
    }
    Write-Host "[kill-port] Port $Port is now free"
} else {
    Write-Host "[kill-port] Port $Port is already free"
}
