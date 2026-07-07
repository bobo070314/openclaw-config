#requires -RunAsAdministrator
<#
.SYNOPSIS
    Fix OpenClaw Task Scheduler tasks — set LogonType=InteractiveToken
    Uses Task Scheduler COM API (no XML needed)
#>

$taskNames = @(
    "Gateway AutoStart",
    "IGP API AutoStart",
    "Heartbeat Morning",
    "Heartbeat Afternoon",
    "Heartbeat Evening",
    "Heartbeat Night"
)

$taskDescriptions = @{
    "Gateway AutoStart" = "OpenClaw Gateway autostart"
    "IGP API AutoStart" = "IGP API autostart"
    "Heartbeat Morning" = "HEARTBEAT 晨检 (09:00)"
    "Heartbeat Evening" = "HEARTBEAT 晚间 (19:00)"
    "Heartbeat Afternoon" = "HEARTBEAT 午后 (13:00)"
    "Heartbeat Night" = "HEARTBEAT 夜间 (23:00)"
}

$taskActions = @{
    "Gateway AutoStart" = @{
        "cmd" = "D:\bobo\openclaw-foreign\start-foreign.bat"
        "args" = ""
        "workdir" = "D:\bobo\openclaw-foreign"
    }
    "IGP API AutoStart" = @{
        "cmd" = "C:\Windows\System32\cmd.exe"
        "args" = '/c "D:\bobo\openclaw-foreign\start-igp-api.bat"'
        "workdir" = "D:\bobo\openclaw-foreign"
    }
    "Heartbeat Morning" = @{
        "cmd" = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        "args" = '-ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\heartbeat_check.ps1" -TimeLabel "晨检"'
        "workdir" = "D:\bobo\openclaw-foreign"
    }
    "Heartbeat Afternoon" = @{
        "cmd" = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        "args" = '-ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\heartbeat_check.ps1" -TimeLabel "午后"'
        "workdir" = "D:\bobo\openclaw-foreign"
    }
    "Heartbeat Evening" = @{
        "cmd" = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        "args" = '-ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\heartbeat_check.ps1" -TimeLabel "晚间"'
        "workdir" = "D:\bobo\openclaw-foreign"
    }
    "Heartbeat Night" = @{
        "cmd" = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        "args" = '-ExecutionPolicy Bypass -File "D:\bobo\openclaw-foreign\scripts\heartbeat_check.ps1" -TimeLabel "夜间"'
        "workdir" = "D:\bobo\openclaw-foreign"
    }
}

$taskTriggers = @{
    "Gateway AutoStart" = @{"type" = "boot"; "delay" = "PT30S"}
    "IGP API AutoStart" = @{"type" = "boot"; "delay" = "PT60S"}
    "Heartbeat Morning" = @{"type" = "daily"; "start" = "2026-07-06T09:00:00"}
    "Heartbeat Afternoon" = @{"type" = "daily"; "start" = "2026-07-06T13:00:00"}
    "Heartbeat Evening" = @{"type" = "daily"; "start" = "2026-07-06T19:00:00"}
    "Heartbeat Night" = @{"type" = "daily"; "start" = "2026-07-06T23:00:00"}
}

$svc = New-Object -ComObject "Schedule.Service"
$svc.Connect()

$root = $svc.GetFolder("\OpenClaw")

# Delete existing tasks
foreach ($tn in $taskNames) {
    try {
        $root.DeleteTask($tn, 0)
        Write-Host "  Deleted: $tn"
    } catch {
        Write-Host "  Not found or already deleted: $tn"
    }
}

# Create each task
foreach ($tn in $taskNames) {
    $td = $svc.NewTask(0)  # TASK_CREATE
    
    # General settings
    $td.RegistrationInfo.Description = $taskDescriptions[$tn]
    $td.RegistrationInfo.Author = "asus"
    $td.Settings.DisallowStartIfOnBatteries = $false
    $td.Settings.StopIfGoingOnBatteries = $false
    $td.Settings.StartWhenAvailable = $true
    $td.Settings.RunOnlyIfIdle = $false
    $td.Settings.RunOnlyIfNetworkAvailable = $false
    $td.Settings.Enabled = $true
    $td.Settings.AllowStartOnDemand = $true
    $td.Settings.ExecutionTimeLimit = "PT0S"
    $td.Settings.Priority = 7
    $td.Settings.RestartCount = 3
    $td.Settings.RestartInterval = "PT1M"
    
    # Principal: LogonType=InteractiveToken (KEY FIX!)
    $td.Principal.UserId = "asus"
    $td.Principal.LogonType = 3  # TASK_LOGON_INTERACTIVE_TOKEN
    $td.Principal.RunLevel = 1   # TASK_RUNLEVEL_HIGHEST
    
    # Trigger
    $triggerInfo = $taskTriggers[$tn]
    if ($triggerInfo["type"] -eq "boot") {
        $trigger = $td.Triggers.Create(8)  # TASK_TRIGGER_BOOT
        $trigger.Delay = $triggerInfo["delay"]
    } else {
        $trigger = $td.Triggers.Create(2)  # TASK_TRIGGER_DAILY
        $trigger.StartBoundary = $triggerInfo["start"]
    }
    $trigger.Enabled = $true
    
    # Action
    $actionInfo = $taskActions[$tn]
    $action = $td.Actions.Create(0)  # TASK_ACTION_EXEC
    $action.Path = $actionInfo["cmd"]
    if ($actionInfo["args"]) {
        $action.Arguments = $actionInfo["args"]
    }
    $action.WorkingDirectory = $actionInfo["workdir"]
    
    # Register (create or update)
    $root.RegisterTaskDefinition($tn, $td, 4, $null, $null, 3)  # TASK_CREATE_OR_UPDATE | TASK_LOGON_INTERACTIVE_TOKEN
    Write-Host "  CREATED: $tn"
}

Write-Host "`nAll 6 tasks registered with LogonType=InteractiveToken"
Write-Host "`n=== Verification ==="
schtasks /query /fo LIST | Select-String "OpenClaw" -Context 0,0
