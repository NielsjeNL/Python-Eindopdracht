﻿# Schaamteloos gekopieerd van http://ss64.com/ps/syntax-get-uptime.html

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
                     "$ComputerName did not respond"