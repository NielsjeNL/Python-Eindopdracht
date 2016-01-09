function Get-Services {
#$total = (Get-Service).length
$stopped = (Get-Service | Where-Object { $_.Status -eq "Stopped" }).length
$running = (Get-Service | Where-Object { $_.Status -eq "Running" }).length

$Display = "" + $running + " running services en " + $stopped + " gestopte"
write-host $Display
}
Get-Services