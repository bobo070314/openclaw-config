$scripts = "D:\bobo\openclaw-foreign\scripts"
$tasks = @(
    @{name="Gateway AutoStart"; xml="task-gateway-autostart.xml"},
    @{name="IGP API AutoStart"; xml="task-igp-api-autostart.xml"},
    @{name="Heartbeat Morning"; xml="task-heartbeat-morning.xml"},
    @{name="Heartbeat Afternoon"; xml="task-heartbeat-afternoon.xml"},
    @{name="Heartbeat Evening"; xml="task-heartbeat-evening.xml"},
    @{name="Heartbeat Night"; xml="task-heartbeat-night.xml"}
)
$ok = $true
$i = 1
foreach($t in $tasks) {
    Write-Host ("[{0}/6] {1}..." -f $i, $t.name)
    $r = schtasks /create /tn ("OpenClaw\" + $t.name) /xml ($scripts + "\" + $t.xml) /f 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK]" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $r" -ForegroundColor Red
        $ok = $false
    }
    $i++
}
if ($ok) {
    Write-Host "`nAll 6 tasks registered." -ForegroundColor Green
} else {
    Write-Host "`nSome tasks failed." -ForegroundColor Red
}
