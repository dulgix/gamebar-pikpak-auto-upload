param(
    [string]$TaskName = "PikPak Game Bar Clips"
)

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
Write-Host "자동 업로드 작업을 제거했습니다: $TaskName"
