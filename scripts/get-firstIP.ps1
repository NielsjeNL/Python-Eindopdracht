$IP = Get-NetIPAddress -AddressFamily IPv4 | Select -first 1 IPAddress
$IP | ForEach-Object {Write-Host $_.IPAddress}