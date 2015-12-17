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

# List of all your agent functions that can be called from within the management script.
# A real developer should do this differently, but this is more easy.
def get_value(number):
    # return the result of one of the pre-define numbers
    print "get_value, of of item with number=",number

    # An example of a value that is acquired using Python only.
    # returns a string
    if number == 1:
        return sys.platform

    # Another example of a value that is acquired using Python only.
    # returns a string
    if number == 2:
        return sys.getdefaultencoding()             

    # Useless of course but returning an int
    # Hier kunnen we zelf een funcite aan hangen dus
    if number == 3:
        return 8888

    # Example in which a PowerShell script is used. The STDOUT is used to pass results back to python.
    # Exporting with export-csv and reading the CSV using Python is also possible of course.
    if number == 4:
        p=subprocess.Popen(['powershell.exe',    # Atlijd gelijk of volledig pad naar powershell.exe
            '-ExecutionPolicy', 'Unrestricted',  # Override current Execution Policy | Check eerst of Set-ExecutionPolicy uitgevoerd moet worden
            '.\\scripts\\agent_counters.ps1'],   # Pad naar de powershell scripts
        stdout=subprocess.PIPE)                  # Zorg ervoor dat je de STDOUT kan opvragen.
        output = p.stdout.read()                 # De stdout als varaiabele output
        return output

    # Example of sing a PowerShell oneliner. Useful for simple PowerShell commands.
    if number == 5:
        p=subprocess.Popen(['powershell',
                            "get-service | measure-object | select -expandproperty count"],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        return output

    # Powershell: Beschikbaar RAM in MB
    if number == 6:
        p=subprocess.Popen(['powershell',
                            '(Get-Counter -Counter "\Memory\Available MBytes").CounterSamples[0].CookedValue'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()+" MB"
        return output
        
    # Powershell: Eerst beschikbare IP adres
    if number == 7:
        p=subprocess.Popen(['powershell',
                            'Get-NetIPAddress -AddressFamily IPv4 | Select -first 1 IPAddress | Format-Wide'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        return output
        
    # Powershell: Beschikbaar geheugen op C:
    if number == 8:
        p=subprocess.Popen(['powershell',
                            """Get-WmiObject Win32_logicaldisk ` | Select -first 1 FreeSpace | 
                               ForEach-Object {$_.freespace / 1GB}"""],
                            stdout = subprocess.PIPE)
        output = float(p.stdout.read())
        output = str("%.2f" % output)+" GB"
        return output
        
    # Powershell: System uptime
    if number == 9:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\get-uptime.ps1 localhost | Select uptime | Format-Wide'],
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
