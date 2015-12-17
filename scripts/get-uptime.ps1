# Schaamteloos gekopieerd van http://ss64.com/ps/syntax-get-uptime.html

# Accept input from the pipeline
Param([Parameter(mandatory=$true,ValueFromPipeline=$true)] [string[]]$ComputerName = @("."))

# Process the piped input (one computer at a time)
process { 
    # See if it responds to a ping, otherwise the WMI queries will fail
    $query = "select * from win32_pingstatus where address = '$ComputerName'"
        $ping = Get-WmiObject -query $query
        if ($ping.protocoladdress) {
            # Ping responded, so connect to the computer via WMI
                $os = Get-WmiObject Win32_OperatingSystem -ComputerName $ComputerName -ev myError -ea SilentlyContinue 

                if ($myError -ne $null)
                 {
                   # Error: WMI did not respond
                     "$ComputerName did not respond" }  else  {      $LastBootUpTime = $os.ConvertToDateTime($os.LastBootUpTime)     $LocalDateTime = $os.ConvertToDateTime($os.LocalDateTime)                # Calculate uptime - this is automatically a timespan     $up = $LocalDateTime - $LastBootUpTime     # Split into Days/Hours/Mins     $uptime = "$($up.Days) days, $($up.Hours)h, $($up.Minutes)mins"     # Save the results for this computer in an object     $results = new-object psobject     $results | add-member noteproperty LastBootUpTime $LastBootUpTime     $results | add-member noteproperty ComputerName $os.csname     $results | add-member noteproperty uptime $uptime     # Display the results     $results | Select-Object ComputerName,LastBootUpTime, uptime     }    # Next Ping result    }# End of the process block}