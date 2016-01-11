# Gekopiëerd van https://4sysops.com/archives/calculating-system-uptime-with-powershell/
function Get-Uptime {
   $os = Get-WmiObject win32_operatingsystem
   $uptime = (Get-Date) - ($os.ConvertToDateTime($os.lastbootuptime))
   $Display = "" + $Uptime.Days + " days, " + $Uptime.Hours + " hours, " + $Uptime.Minutes + " minutes" 
   write-host -NoNewline $Display
}
Get-Uptime