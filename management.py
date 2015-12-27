from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
import cgi, cgitb
import datetime
cgitb.enable()

# ---------------------------------------------------------
# Variabelen aanmaken
form = cgi.FieldStorage()
hostnameHTTP = form.getvalue('hostname')
fx = form.getvalue('fx') # fx haalt alles op, fnummer alleen zijn eigen functie
f1  = form.getvalue('f1')
f2  = form.getvalue('f2')
f3  = form.getvalue('f3')
f4  = form.getvalue('f4')
f5  = form.getvalue('f5')
f6  = form.getvalue('f6')
# ---------------------------------------------------------
# Config inlezen
configtree = etree.parse('mgmtconfig.xml')
hostname = str(configtree.xpath('/config/hostname/text()')[0])
port = str(configtree.xpath('/config/port/text()')[0])

# ---------------------------------------------------------
# HTML-metadata
print 'Status: 200 OK\n'

# Fout bij het laden van de pagina tegengaan voor als ik (N) zelf aan het testen ben
if hostnameHTTP == None:
    print "<p> </p>"
    exit()
    
# create a simple consumer
client = SoapClient(
    location = "http://"+hostnameHTTP+":"+port+"/",
    action = "http://"+hostnameHTTP+":"+port+"/", # SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    ns = False)

# Verbinding testen en fout weergeven als deze niet werkt
try:
    client.get_value(number=1).resultaat
except:
    print "<p>Er is iets fout gegaan met het opzetten van de verbinding, controleer adres en poort</p>"
    exit()
    
#De default pagina
print '<HTML>'
print '<HEAD>'
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
print '<TITLE>Management script</TITLE>'
print '</HEAD>'
print '<BODY>'
print '<h1 style="margin-bottom: -15px;">Resultaten</h1>'
print '<p>Waardes opgehaald om: ',datetime.datetime.now().time().strftime('%H:%H:%S'),'</p>'
# Code om zooi op te vragen
print "<p>"
print "Resultaten:<br>"
# resultaten ophalen van de agent
# als fnummer of fx waar (True) is worden de counters opgehaald
if f1 or fx:
    r1=str(client.get_value(number=1).resultaat)
    print "Platform type :", r1,"<br>"

if f2 or fx:
    r2=str(client.get_value(number=2).resultaat)
    print "Running services,total :", r2.split(),"<br>"

if f3 or fx:
    r3=str(client.get_value(number=3).resultaat)
    print "Totaal werkgeheugen:", r3.rstrip(),"<br>"

if f4 or fx:
    r4=str(client.get_value(number=4).resultaat)
    print "Eerst beschikbare IP-adres:", r4.rstrip(),"<br>"

if f5 or fx:
    r5=str(client.get_value(number=5).resultaat)
    print "Vrije schijfruimte op C:", r5.rstrip(),"<br>"

if f6 or fx:
    r6=str(client.get_value(number=6).resultaat)
    print "Systeem Uptime:", r6.rstrip(),"<br>"
print "</p>"
print '</BODY>'
print '</HTML>'