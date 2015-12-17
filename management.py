from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
import cgi, cgitb
cgitb.enable()

# ---------------------------------------------------------
# Variabelen aanmaken
form = cgi.FieldStorage()
hostnameHTTP = form.getvalue('hostname')
value2  = form.getvalue('value2')

# ---------------------------------------------------------
# Config inlezen
configtree = etree.parse('mgmtconfig.xml')
hostname = str(configtree.xpath('/config/hostname/text()')[0])
port = str(configtree.xpath('/config/port/text()')[0])

# ---------------------------------------------------------
# create a simple consumer
client = SoapClient(
    location = "http://"+hostname+":"+port+"/",
    action = "http://"+hostname+":"+port+"/", # SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    ns = False)
try:
    client.get_value(number=1).resultaat
except:
    print "<p>Er is iets fout gegaan met het opzetten van de verbinding, controleer adres en poort</p>"
    exit() # tijdens testen eruit laten anders knalt je console eruit lel

# HTML-metadata
print 'Status: 200 OK\n'
#De default pagina
print '<HTML>'
print '<HEAD>'
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
print '<TITLE>Management script</TITLE>'
print '</HEAD>'
print '<BODY>'
print '<H1>Welkom bij dit management script!</H1>'
print '<p>Placeholder text aw yeah</p>'
# Code om zooi op te vragen
print "<p>"
print "Resultaten:<br>"
# call a few remote methods
r1=str(client.get_value(number=1).resultaat)
print "Resultaat number=1 :", r1,"<br>"

r2=str(client.get_value(number=2).resultaat)
print "Resultaat number=2 :", r2,"<br>"

r3=str(client.get_value(number=3).resultaat)
print "Resultaat number=3 :", int(r3),"<br>" # r3 is a number!

r4=str(client.get_value(number=4).resultaat)
print "Resultaat number=4 :", r4.rstrip(),"<br>" # This is a multiline: strip the newline from the result!

r5=str(client.get_value(number=5).resultaat)
print "Resultaat number=5 :", r5.rstrip(),"<br>"

r6=str(client.get_value(number=6).resultaat)
print "Beschikbaar werkgeheugen: (6):", r6.rstrip(),"<br>"

r7=str(client.get_value(number=7).resultaat)
print "Eerst beschikbare IP-adres: (7):", r7.rstrip(),"<br>"

r8=str(client.get_value(number=8).resultaat)
print "Vrije schijfruimte op C: (8):", r8.rstrip(),"<br>"

r9=str(client.get_value(number=9).resultaat)
print "Systeem Uptime (9):", r9.rstrip(),"<br>"
print "</p>"
print '</BODY>'
print '</HTML>'