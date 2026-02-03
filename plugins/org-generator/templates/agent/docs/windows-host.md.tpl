# Windows Host Installation Guide

## Prerequisites

- Windows Server 2012 R2 or later (Windows 10/11 for workstations)
- Administrator access
- Outbound internet access to `*.{{SITE}}`

## Installation

### GUI Installer

1. Download the latest Windows installer:
   - [64-bit](https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi)

2. Run the installer as Administrator

3. Enter your API key when prompted

4. Complete the installation wizard

### Command Line Installation

```powershell
# Download installer
Invoke-WebRequest -Uri "https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi" -OutFile "datadog-agent.msi"

# Install with API key
msiexec /qn /i datadog-agent.msi APIKEY="YOUR_API_KEY" SITE="{{SITE}}"
```

## Configuration

Configuration files are located at:
```
C:\ProgramData\Datadog\datadog.yaml
C:\ProgramData\Datadog\conf.d\
```

1. Copy the main configuration:
   ```powershell
   Copy-Item datadog.yaml -Destination "C:\ProgramData\Datadog\datadog.yaml"
   ```

2. Update the API key in the configuration file

3. Copy integration configs as needed

## Service Management

```powershell
Restart-Service -Name "DatadogAgent"
Stop-Service -Name "DatadogAgent"
Start-Service -Name "DatadogAgent"
Get-Service -Name "DatadogAgent"
```

## Verify Installation

```powershell
& "C:\Program Files\Datadog\Datadog Agent\bin\agent.exe" status
& "C:\Program Files\Datadog\Datadog Agent\bin\agent.exe" configcheck
```

## Log Locations

- Agent logs: `C:\ProgramData\Datadog\logs\agent.log`

## Troubleshooting

### Agent service won't start

1. Check Windows Event Viewer for errors
2. Verify API key is correct
3. Check `C:\ProgramData\Datadog\logs\agent.log`

### Permissions issues

```powershell
Add-LocalGroupMember -Group "Performance Monitor Users" -Member "ddagentuser"
```
