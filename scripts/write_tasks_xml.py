import codecs

def write_xml(path, description, cmd, args="", delay_seconds=30):
    delay = f"PT{delay_seconds}S"
    
    if args:
        action = f'''      <Command>{cmd}</Command>
      <Arguments>{args}</Arguments>'''
    else:
        action = f'''      <Command>{cmd}</Command>'''
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2026-07-06T09:00:00</Date>
    <Author>asus</Author>
    <Description>{description}</Description>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>{delay}</Delay>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <Enabled>true</Enabled>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
{action}
      <WorkingDirectory>D:\\bobo\\openclaw-foreign</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''
    
    with open(path, 'w', encoding='utf-16-le', newline='\r\n') as f:
        f.write(xml_content)

# 1. Gateway AutoStart (30s delay)
write_xml(
    r"D:\bobo\openclaw-foreign\scripts\task-gateway-autostart.xml",
    "OpenClaw Gateway (18789) boot autostart",
    r"D:\bobo\openclaw-foreign\start-foreign.bat",
    delay_seconds=30
)
print("Gateway XML: OK")

# 2. IGP API AutoStart (60s delay)
write_xml(
    r"D:\bobo\openclaw-foreign\scripts\task-igp-api-autostart.xml",
    "IGP API (8080) boot autostart",
    r"C:\Windows\System32\cmd.exe",
    args='/c "D:\\bobo\\openclaw-foreign\\start-igp-api.bat"',
    delay_seconds=60
)
print("IGP API XML: OK")

# 3-6. Heartbeat tasks (no exec needed, already good)
print("All XML files updated")
