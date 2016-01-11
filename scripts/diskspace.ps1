Get-WmiObject Win32_logicaldisk ` | Select -first 1 FreeSpace | ForEach-Object {  $vrij = $_.freespace / 1GB}
Get-WmiObject Win32_logicaldisk ` | Select -first 1 Size | ForEach-Object { $totaal = $_.size / 1GB}
$totaal = "{0:N2}" -f $totaal
$vrij = "{0:N2}" -f $vrij

Write-Host -NoNewline "$totaal $vrij"