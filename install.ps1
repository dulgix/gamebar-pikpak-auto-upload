param(
    [string]$TaskName = "PikPak Game Bar Clips"
)

$root = $PSScriptRoot
$script = Join-Path $root "gamebar_pikpak_uploader.py"
$config = Join-Path $root "config.json"

if (-not (Test-Path $script)) { throw "업로더 파일을 찾지 못했습니다: $script" }
if (-not (Test-Path $config)) { throw "config.example.json을 복사해 config.json을 먼저 만드세요." }

$python = (Get-Command python.exe -ErrorAction Stop).Source
$pythonw = Join-Path (Split-Path $python -Parent) "pythonw.exe"

# pythonw.exe runs Python without opening a console window.
if (Test-Path $pythonw) { $python = $pythonw }

$action = New-ScheduledTaskAction -Execute $python -Argument ('"{0}"' -f $script)
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "Game Bar clips to PikPak" -Force
Start-ScheduledTask -TaskName $TaskName
Write-Host "자동 업로드 작업을 등록하고 시작했습니다: $TaskName"
