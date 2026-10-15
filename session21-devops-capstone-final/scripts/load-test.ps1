param([int]$Requests = 200, [string]$Url = "http://localhost:8000/api/tasks")
1..$Requests | ForEach-Object { Invoke-WebRequest -UseBasicParsing $Url | Out-Null }
Write-Host "Sent $Requests requests to $Url"
