function Get-Services {
#$total = (Get-Service).length
$stopped = (Get-Service | Where-Object { $_.Status -eq "Stopped" }).length
$running = (Get-Service | Where-Object { $_.Status -eq "Running" }).length

write-host -NoNewline $running $stopped
}
Get-Services