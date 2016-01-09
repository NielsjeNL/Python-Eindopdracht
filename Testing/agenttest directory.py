from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from lxml import etree
import sys,subprocess
# ---------------------------------------------------------
# Variabelen aanmaken
#configtree = etree.parse('agentconfig.xml')

# ---------------------------------------------------------
# Config inlezen
#port = str(configtree.xpath('/config/port/text()')[0])
port = '8009'

def echo(request):
    "Copy request->response (generic, any type)"
    return request.value
    
# functie met daarin een lijstje van alle dingen die we op kunnen vragen
def get_value(platform=False, ip=False, loggedinusers=False, services=False, freespace=False,systeminfo=False, ram=False, uptime=False):
    # return the result of one of the pre-define numbers
    response ={}    
    print "WAARDES OPGEVRAAGD MET NUMMER ", platform, ip, loggedinusers, services, freespace,systeminfo, ram, uptime
    response = {'platform':'','services':'','ram':'','ip':'','freespace':'','uptime':'','loggedinusers':''}
    # An example of a value that is acquired using Python only.
    # returns a string
    if platform == True:
        response['platform'] = sys.platform
    # Running en totaal # services
    if services == True:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\services.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        response['services'] = output
        
    # Powershell: Totaal RAM in GB
    if ram == True:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\memory.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        response['ram'] = output
        
        
# dit is nu verwerkt in nummer 3
#    # Powershell: Beschikbaar RAM in MB
#    if number == 31:
#        p=subprocess.Popen(['powershell',
#                            '(Get-Counter -Counter "\Memory\Available MBytes").CounterSamples[0].CookedValue'],
#        stdout=subprocess.PIPE)
#        output = p.stdout.read()+" MB"
#        return output
   
    # Powershell: Eerst beschikbare IP adres
    if ip == True:
        p=subprocess.Popen(['powershell',
                            '.\\scripts\\get-firstIP.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        output = output.rstrip()
        response['ip'] = output
        
    # Powershell: Beschikbaar geheugen op C:
    if freespace == True:
        p=subprocess.Popen(['powershell',
                            """Get-WmiObject Win32_logicaldisk ` | Select -first 1 FreeSpace | 
                               ForEach-Object {$_.freespace / 1GB}"""],
                            stdout = subprocess.PIPE)
        output = float(p.stdout.read())
        output = str("%.2f" % output)+" GB"
        response['freespace'] =  output
        
    # Powershell: System uptime
    if uptime == True:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\get-uptime.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        response['uptime'] = output
        
    # Powershell: Aantal ingelogde gebruikers teruggeven
    if loggedinusers == True:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\\get-loggedonusers.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        response['loggedinusers'] = output
    # Last value
    print type(response)
    return response

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
    returns={'resultaat': [{str: str}] } ,   # return data type
    args={'platform':bool, 'ip':bool, 'loggedinusers':bool, 'services':bool, 'freespace':bool,
          'systeminfo':bool, 'ram':bool, 'uptime':bool}         # it seems that an argument is mandatory, although not needed as input for this function: therefore a dummy argument is supplied but not used.
    )

dispatcher.register_function('Echo', echo)

# Let this agent listen forever, do not change anything unless needed.
try:
    print "Starting server on port",port,"..."
    httpd = HTTPServer(("", int(port)), SOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()
except:
    print "Er is iets fout gegaan bij het opzetten van de server, controleer of de poort vrij is!"
    exit()
