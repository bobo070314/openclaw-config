Set WshShell = CreateObject("WScript.Shell")

Dim fso
Dim projectDir
Dim nodePath
Dim gatewayScript
Dim configPath
Dim stateDir
Dim killPortScript
Dim launchCmd
Dim url
Dim attempts
Dim isReady

Set fso = CreateObject("Scripting.FileSystemObject")

projectDir = "D:\bobo\openclaw-foreign"
nodePath = "D:\Program Files\nodejs\node.exe"
gatewayScript = projectDir & "\openclaw\openclaw.mjs"
configPath = projectDir & "\openclaw-minimal.json"
stateDir = projectDir & "\state"
killPortScript = projectDir & "\scripts\kill-port.ps1"
url = "http://127.0.0.1:18900/chat?token=foreign18900&session=agent%3Amain%3Amain"

If Not fso.FileExists(nodePath) Then
    MsgBox "Launch failed: missing node.exe " & nodePath, vbCritical, "OpenClaw Foreign"
    Set fso = Nothing
    Set WshShell = Nothing
    WScript.Quit 1
End If

If Not fso.FileExists(gatewayScript) Then
    MsgBox "Launch failed: missing gateway script " & gatewayScript, vbCritical, "OpenClaw Foreign"
    Set fso = Nothing
    Set WshShell = Nothing
    WScript.Quit 1
End If

If Not fso.FileExists(configPath) Then
    MsgBox "Launch failed: missing config " & configPath, vbCritical, "OpenClaw Foreign"
    Set fso = Nothing
    Set WshShell = Nothing
    WScript.Quit 1
End If

' Lock config as read-only so openclaw cannot overwrite it at runtime
WshShell.Run "powershell -NoProfile -Command ""Set-ItemProperty '" & configPath & "' -Name IsReadOnly -Value $true""", 0, True

' Reset broken session state so gateway always starts fresh
Dim sessionsFile
sessionsFile = stateDir & "\agents\main\sessions\sessions.json"
If fso.FileExists(sessionsFile) Then
    Dim ts
    Set ts = fso.OpenTextFile(sessionsFile, 2, False)
    ts.Write "{}"
    ts.Close
    Set ts = Nothing
End If

' Kill any openclaw-home gateway started by scheduled task
WshShell.Run "powershell -NoProfile -Command ""Get-Process node -ErrorAction SilentlyContinue | Where-Object { $_.MainModule.FileName -like '*npm*' -or $_.MainModule.FileName -like '*openclaw-home*' } | Stop-Process -Force""", 0, True
WshShell.Run "powershell -NoProfile -Command ""$p = Get-NetTCPConnection -LocalPort 18900 -ErrorAction SilentlyContinue; if($p){ Stop-Process -Id $p.OwningProcess -Force -ErrorAction SilentlyContinue }""", 0, True
WScript.Sleep 1500

If fso.FileExists(killPortScript) Then
    WshShell.Run "powershell -NoProfile -ExecutionPolicy Bypass -File " & Chr(34) & killPortScript & Chr(34) & " 18900", 0, True
End If

' Clear QCLAW_ env vars, set OPENCLAW_ config only
launchCmd = "cmd /c cd /d " & Chr(34) & projectDir & Chr(34) & _
    " && set QCLAW_LLM_BASE_URL=" & _
    " && set QCLAW_LLM_API_KEY=" & _
    " && set QCLAW_PLUGIN_CONFIG_PATH=" & _
    " && set QCLAW_USER_DATA_DIR=" & _
    " && set " & Chr(34) & "OPENCLAW_CONFIG_PATH=" & configPath & Chr(34) & _
    " && set " & Chr(34) & "OPENCLAW_STATE_DIR=" & stateDir & Chr(34) & _
    " && " & Chr(34) & nodePath & Chr(34) & " " & Chr(34) & gatewayScript & Chr(34) & " gateway --port 18900"

' 1 = normal window, user can see errors if gateway crashes
WshShell.Run launchCmd, 1, False

isReady = False
For attempts = 1 To 24
    WScript.Sleep 1000
    If IsPortReady("http://127.0.0.1:18900/") Then
        isReady = True
        Exit For
    End If
Next

If isReady Then
    WshShell.Run url, 1, False
Else
    MsgBox "Gateway did not start in time. Check the OpenClaw-Foreign window.", vbExclamation, "OpenClaw Foreign"
End If

Set fso = Nothing
Set WshShell = Nothing

Function IsPortReady(targetUrl)
    On Error Resume Next

    Dim http
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", targetUrl, False
    http.Send

    If Err.Number = 0 Then
        IsPortReady = True
    Else
        IsPortReady = False
    End If

    Set http = Nothing
    Err.Clear
    On Error GoTo 0
End Function
