$info = systeminfo
$totaal = ($info | Select-String 'Total Physical Memory:').ToString().Split(':')[1].Trim()
$vrij = ($info | Select-String 'Available Physical Memory:').ToString().Split(':')[1].Trim()

$totaal = $totaal -replace ('\.', '') -replace (',', '') -replace (' MB', '')
$vrij = $vrij -replace ('\.', '') -replace (',', '') -replace (' MB', '')

write-host -NoNewline "$totaal $vrij"