<#
.SYNOPSIS Lossless DB + 配置文件自动备份（L5 + L9），保留 7 天
#>

$dbPath       = "D:\bobo\openclaw-foreign\memory\lossless\lcm.db"
$cfgPath      = "D:\bobo\openclaw-foreign\openclaw-minimal.json"
$backupRoot   = "D:\bobo\openclaw-foreign\backup"
$retention    = 7
$logDir       = "D:\bobo\openclaw-foreign\logs"
$logFile      = "$logDir\backup_$(Get-Date -Format 'yyyyMMdd').log"
$ts           = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

function Log($m) { "$ts $m" | Out-File -Append -FilePath $logFile -Encoding Default }

try {
    if (-not (Test-Path $dbPath)) { Log "FAIL source missing"; exit 1 }
    $fi = Get-Item $dbPath
    $sizeKB = [math]::Round($fi.Length / 1KB, 1)

    $monthDir = "$backupRoot\$(Get-Date -Format 'yyyy-MM')"
    New-Item -ItemType Directory -Path $monthDir -Force | Out-Null
    $backupFile = "$monthDir\lcm_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').db"

    Copy-Item -Path $dbPath -Destination $backupFile -Force
    if (Test-Path $backupFile) {
        $bs = [math]::Round((Get-Item $backupFile).Length / 1KB, 1)
        Log "OK backup $($fi.Name) -> $backupFile (${sizeKB}KB -> ${bs}KB)"
    } else {
        throw "copy verify failed"
    }

    $cut = (Get-Date).AddDays(-$retention)
    $total = 0
    Get-ChildItem $backupRoot -Recurse -Filter "lcm_*.db" | ForEach-Object {
        $total++
        if ($_.LastWriteTime -lt $cut) {
            Remove-Item -Path $_.FullName -Force
            Log "Clean $($_.Name)"
        }
    }
    Log "Total backups: $total"

    # === L9: 配置备份 ===
    if (Test-Path $cfgPath) {
        $cfgBackup = "$monthDir\config_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').json"
        Copy-Item -Path $cfgPath -Destination $cfgBackup -Force
        if (Test-Path $cfgBackup) {
            $cbs = [math]::Round((Get-Item $cfgBackup).Length / 1KB, 1)
            Log "Config backup: $cfgBackup (${cbs}KB)"
        }
    } else {
        Log "Config source missing"
    }

    exit 0
} catch {
    Log "Exception: $($_.Exception.Message)"
    exit 1
}
