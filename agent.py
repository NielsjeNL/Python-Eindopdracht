from pysimplesoap.server import SoapDispatcher, SOAPHandler
from BaseHTTPServer import HTTPServer
from lxml import etree
import sys,subprocess
import warnings
# ---------------------------------------------------------
# Config inlezen
configtree = etree.parse('agentconfig.xml')
port = str(configtree.xpath('/config/port/text()')[0])

def echo(request):
    "Copy request->response (generic, any type)"
    return request.value
    
# functie met daarin een lijstje van alle dingen die we op kunnen vragen
def get_value(platform=False, ip=False, loggedinusers=False, services=False, freespace=False, ram=False, uptime=False):
    ''' Geeft waarden terug van de opgevraagde gegevens in een directory '''    
    #response ={}
    response = {'platform':'','services':'','ram':'','ip':'','freespace':'','uptime':'','loggedinusers':''}
    print "WAARDES OPGEVRAAGD platform", platform,"ip", ip,"loggedin users", loggedinusers,"services", services,"freespace", freespace,"ram", ram,"uptime", uptime

    # Opvragen platform type terug
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
   
    # Powershell: Eerst beschikbare IP adres
    if ip == True:
        p=subprocess.Popen(['powershell',
                            '-ExecutionPolicy', 'Unrestricted',
                            '.\\scripts\\get-firstIP.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        output = output.rstrip()
        response['ip'] = output

    # Powershell: Schijfruimte 
    if freespace == True:
        p=subprocess.Popen(['powershell.exe',
            '-ExecutionPolicy', 'Unrestricted',
            '.\\scripts\diskspace.ps1'],
        stdout=subprocess.PIPE)
        output = p.stdout.read()
        response['freespace'] = output
        
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
<<<<<<< HEAD
        return output
        
    if number == 999:
        output = 'Verbinding OK'
        return output

=======
        response['loggedinusers'] = output
>>>>>>> refs/remotes/origin/testing
    # Last value
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
warnings.filterwarnings("ignore")
dispatcher.register_function('get_value', get_value,
    returns={'resultaat': [{'platform':str, 'ip':str, 'loggedinusers':str, 'services':str, 'freespace':str, 'ram':str, 'uptime':str}] } ,   # return data type   
    args={'platform':bool, 'ip':bool, 'loggedinusers':bool, 'services':bool, 'freespace':bool,
          'ram':bool, 'uptime':bool}         # it seems that an argument is mandatory, although not needed as input for this function: therefore a dummy argument is supplied but not used.
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