from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
import cgi, cgitb
import datetime
import matplotlib.pyplot as plt
import cStringIO
cgitb.enable()

# ---------------------------------------------------------
# Variabelen aanmaken
form = cgi.FieldStorage()
hostnameHTTP = form.getvalue('hostname')
fx = form.getvalue('fx') # fx haalt alles op, fnummer alleen zijn eigen functie
f1  = form.getvalue('f1')
f2  = form.getvalue('f2')
f3  = form.getvalue('f3')
f31  = form.getvalue('f31')
f4  = form.getvalue('f4')
f5  = form.getvalue('f5')
f6  = form.getvalue('f6')
f7  = form.getvalue('f7')
# ---------------------------------------------------------
# Config inlezen
configtree = etree.parse('mgmtconfig.xml')
hostname = str(configtree.xpath('/config/hostname/text()')[0])
port = str(configtree.xpath('/config/port/text()')[0])

# ---------------------------------------------------------

# ---------------------------------------------------------
# Grafieken genereren defines
def gen_used_bar(gebruikt, totaal):
    '''Maakt een horizontale balk met percentage gebruikt en vrij '''
    pctused = float(gebruikt)/float(totaal)
    maximaal = 1-pctused
    fig = plt.figure(figsize=(8, 2))
    width = 1
    #plt.xlabel('Totaal: '+str(totaal))
    p1 = plt.barh(0, pctused,width,color='r')
    p2 = plt.barh(0, maximaal,width,color='y',left=pctused)
    plt.legend((p1[0], p2[0]), ('Gebruikt', 'Vrij'))
    frame = plt.gca()
    frame.axes.get_yaxis().set_visible(False)
    #plt.show()
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)
    return sio.getvalue().encode("base64").strip()
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
    
# HTML-data
print '<HTML>'
print '<HEAD>'
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
print '<link href="html/style.css" rel="stylesheet" type="text/css">'
print '<TITLE>Management script</TITLE>'
print '</HEAD>'
print '<p>Waardes opgehaald om: ',datetime.datetime.now().time().strftime('%H:%M:%S'),'</p>'
print "<table>"
# resultaten ophalen van de agent
# als fnummer of fx waar (True) is worden de counters opgehaald
if f1 or fx:
    r1=str(client.get_value(number=1).resultaat)
    print "<tr><td>"
    print "Platform type:</td><td>", r1,"</td></tr>"

if f2 or fx:
    r2=str(client.get_value(number=2).resultaat)
    print "<tr><td>"
    print "Running en totaal aantal services:</td><td>", r2.split(),"</td></tr>"

# uit de table gehaald voor nieuwe opmaakt type
#if f3 or fx:
#    r3=str(client.get_value(number=3).resultaat)
#    print "<tr><td>"
#    print "Totaal werkgeheugen en beschikbaar geheugen:</td><td>", r3.split(),"</td></tr>"

#if f31 or fx:
#    r31=str(client.get_value(number=31).resultaat)
#    print "<tr><td>"
#    print "Beschikbaar werkgeheugen:</td><td>", r31.rstrip(),"</td></tr>"

if f4 or fx:
    r4=str(client.get_value(number=4).resultaat)
    print "<tr><td>"
    print "Eerst beschikbare IP-adres:</td><td>", r4.rstrip(),"</td></tr>"

if f5 or fx:
    r5=str(client.get_value(number=5).resultaat)
    print "<tr><td>"
    print "Vrije schijfruimte op C: :</td><td>", r5.rstrip(),"</td></tr>"

if f6 or fx:
    r6=str(client.get_value(number=6).resultaat)
    print "<tr><td>"
    print "Systeem Uptime:</td><td>", r6.rstrip(),"</td></tr>"
    
if f7 or fx:
    r7=str(client.get_value(number=7).resultaat)
    print "<tr><td>"
    print "Aantal ingelogde gebruikers:</td><td>", r7.rstrip(),"</td></tr>"
print '</table>'

if f3 or fx:
    r3=str(client.get_value(number=3).resultaat).split()
    print """<div class="item-wd-2-4">
            	<div class="item-content">
            		<h1>Werkgeheugen</h1>
            		<p>Op dit moment is er %s MB beschikbaar van de %s MB</p>
            		<img src="data:image/png;base64,%s"/>
            	</div>
            </div>""" % (r3[1],r3[0],gen_used_bar(int(r3[0])-int(r3[1]),r3[0]))
print '</HTML>'