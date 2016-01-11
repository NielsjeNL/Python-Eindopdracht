$IP = Get-NetIPAddress -AddressFamily IPv4 | Select -first 1 IPAddress # AddressFamily kan eventueel weggehaald worden
$IP | ForEach-Object {Write-Host $_.IPAddress}                         # voor bedrijven met IPv6