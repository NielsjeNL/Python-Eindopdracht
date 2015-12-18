gwmi Win32_OperatingSystem | % { 
$waarde = $_.TotalVisibleMemorySize/1000000 
"{0:N1}" -f $waarde
} 