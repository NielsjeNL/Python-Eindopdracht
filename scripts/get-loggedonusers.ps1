function Get-LoggedOnUser { 
#Requires -Version 2.0             
[CmdletBinding()]             
 Param              
   (                        
    [Parameter(Mandatory=$true, 
               Position=0,                           
               ValueFromPipeline=$true,             
               ValueFromPipelineByPropertyName=$true)]             
    [String[]]$ComputerName 
   )#End Param 
 
Begin             
{             
 #Write-Host "`n Checking Users . . . " 
 $i = 0             
}#Begin           
Process             
{ 
    $ComputerName | Foreach-object { 
    $Computer = $_ 
    try 
        { 
            $processinfo = @(Get-WmiObject -class win32_process -ComputerName $Computer -EA "Stop") 
                if ($processinfo) 
                {     
                    $processinfo | Foreach-Object {$_.GetOwner().User} |  
                    Where-Object {$_ -ne "NETWORK SERVICE" -and $_ -ne "LOCAL SERVICE" -and $_ -ne "SYSTEM"} | 
                    Sort-Object -Unique | 
                    ForEach-Object { New-Object psobject -Property @{Computer=$Computer;LoggedOn=$_} } |  
                    Select-Object Computer,LoggedOn 
                }#If 
        } 
    catch 
        { 
            "Cannot find any processes running on $computer" | Out-Host 
        } 
     }#Forech-object(Comptuters)        
             
}#Process 
End 
{ 
 
}#End 
#https://gallery.technet.microsoft.com/scriptcenter/d46b1f3b-36a4-4a56-951b-e37815a2df0c
}#Get-LoggedOnUser 

(Get-LoggedOnUser -ComputerName localhost | Select LoggedOn | Measure-Object | Select Count | Format-Wide)