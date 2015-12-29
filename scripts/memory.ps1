#gwmi Win32_OperatingSystem | % { 
#$waarde = $_.TotalVisibleMemorySize/1000000 
#"{0:N1}" -f $waarde
#} 

$totaal = (systeminfo | Select-String 'Total Physical Memory:').ToString().Split(':')[1].Trim()
$vrij = (systeminfo | Select-String 'Available Physical Memory:').ToString().Split(':')[1].Trim()

$totaal = $totaal -replace ('\.', '')
$totaal = $totaal -replace (',', '')
$totaal = $totaal -replace (' MB', '')
$vrij = $vrij -replace ('\.', '')
$vrij = $vrij -replace (',', '')
$vrij = $vrij -replace (' MB', '')

write-host "$totaal $vrij"