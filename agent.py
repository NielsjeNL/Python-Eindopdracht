from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from lxml import etree
import sys,subprocess
# ---------------------------------------------------------
# Variabelen aanmaken
configtree = etree.parse('agentconfig.xml')

# ---------------------------------------------------------
# Config inlezen
port = str(configtree.xpath('/config/port/text()')[0])

# functie met daarin een lijstje van alle dingen die we op kunnen vragen
def get_value(number):
    # return the result of one of the pre-define numbers
    print "get_value, of of item with number=",number

    # An example of a value that is acquired using Python only.
    # returns a string
    if number == 1:
        return sys.platform

    if number == 2:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\services.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        return output
    # Powershell: Totaal RAM in GB
    if number == 3:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\memory.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()+" GB"
        return output
        
        
    # Powershell: Beschikbaar RAM in MB
    if number == 31:
        p=subprocess.Popen(['powershell',
                            '(Get-Counter -Counter "\Memory\Available MBytes").CounterSamples[0].CookedValue'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()+" MB"
        return output
   
    # Powershell: Eerst beschikbare IP adres
    if number == 4:
        p=subprocess.Popen(['powershell',
                            'Get-NetIPAddress -AddressFamily IPv4 | Select -first 1 IPAddress | Format-Wide'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        return output
        
    # Powershell: Beschikbaar geheugen op C:
    if number == 5:
        p=subprocess.Popen(['powershell',
                            """Get-WmiObject Win32_logicaldisk ` | Select -first 1 FreeSpace | 
                               ForEach-Object {$_.freespace / 1GB}"""],
                            stdout = subprocess.PIPE)
        output = float(p.stdout.read())
        output = str("%.2f" % output)+" GB"
        return output
        
    # Powershell: System uptime
    if number == 6:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\get-uptime.ps1 localhost | Select uptime | Format-Wide'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        return output
        
    # Powershell: Aantal ingelogde gebruikers teruggeven
    if number == 7:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\get-loggedonusers.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        return output
    # Last value
    return None

# ---------------------------------------------------------
# do not change anything unless you know what you're doing.
dispatcher = SoapDispatcher(
    'my_dispatcher',
    location = "http://localhost:"+port+"/",
    action = "http://localhost:"+port+"/", #SOAPAction
    namespace = "http://example.com/sample.wsdl", prefix="ns0",
    trace = True,
    ns = True)

# do not change anything unless you know what you're doing.
dispatcher.register_function('get_value', get_value,
    returns={'resultaat': str},   # return data type
    args={'number': int}         # it seems that an argument is mandatory, although not needed as input for this function: therefore a dummy argument is supplied but not used.
    )

# Let this agent listen forever, do not change anything unless needed.
try:
    print "Starting server on port",port,"..."
    httpd = HTTPServer(("", int(port)), SOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()
except:
    print "Er is iets fout gegaan bij het opzetten van de server, controleer of de poort vrij is!"
    exit()
