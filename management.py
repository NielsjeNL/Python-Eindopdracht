from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
import cgi, cgitb
import datetime
import matplotlib.pyplot as plt
import cStringIO
import logging
import csv
cgitb.enable()

# Variabelen aanmaken
form = cgi.FieldStorage()
hostnameHTTP = form.getvalue('hostname')
hostnameHTTP = 'PAS1'
fx = form.getvalue('fx') # fx haalt alles op, fnummer alleen zijn eigen functie
#fx = True
f1  = form.getvalue('f1')
f2  = form.getvalue('f2')
f2 = True
f3  = form.getvalue('f3')
f31  = form.getvalue('f31')
f4  = form.getvalue('f4')
f5  = form.getvalue('f5')
f6  = form.getvalue('f6')
f7  = form.getvalue('f7')


# Config inlezen
configtree = etree.parse('mgmtconfig.xml')
hostname = str(configtree.xpath('/config/hostname/text()')[0])
port = str(configtree.xpath('/config/port/text()')[0])

# Logging opzetten
logfile = str(configtree.xpath('/config/logfile/text()')[0])
loglevel = str(configtree.xpath('/config/loglevel/text()')[0])
logger = logging.getLogger()
logger.setLevel(loglevel)
# file handler maken, deze schrijft uiteindelijk het log weg
handler = logging.FileHandler(logfile)
handler.setLevel(loglevel)
# format voor het log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# handler toevoegen aan het log, let op dat je dit maar 1 keer doet anders krijg je dubbele logs
logger.addHandler(handler)
# begin van het log schrijven
logger.warning('--------------BEGIN LOG--------------')
logger.warning('Script is begonnen')  

# CSV bestand opzetten
csvfilename = 'management-'+hostname+'.csv'
csvf  = open(csvfilename, 'a') 
csvwriter = csv.writer(csvf,lineterminator='\n')
#next(csvwriter)

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
print '<link href="style.css" rel="stylesheet" type="text/css">'
print '<TITLE>Management script</TITLE>'
print '</HEAD>'
print '<p>Waardes opgehaald om: ',datetime.datetime.now().time().strftime('%H:%M:%S'),'</p>'
print "<table>"
# resultaten ophalen van de agent
# als fnummer of fx waar (True) is worden de counters opgehaald
# Platform-type
if f1 or fx:
    logger.warning('Functie 1 opgevraagd')
    r1=str(client.get_value(number=1).resultaat)
    print "<tr><td>"
    print "Platform type:</td><td>", r1,"</td></tr>"
    logger.warning('Functie 1 ontvangen')
    csvwriter.writerow((datetime.date.today(), datetime.datetime.now().time().strftime('%H:%M:%S'),
                         hostname, 'Platform', r1.rstrip()))
# Running en totaal # services
if f2 or fx:
    logger.warning('Functie 2 opgevraagd')    
    r2=str(client.get_value(number=2).resultaat)
    print "<tr><td>"
    print "Running en totaal aantal services:</td><td>", r2.strip(),"</td></tr>"
    logger.warning('Functie 2 ontvangen')
    csvwriter.writerow((datetime.date.today(), datetime.datetime.now().time().strftime('%H:%M:%S'),
                         hostname, 'Running, totaal # services', r2.rstrip()))

# Totaal RAM
# ik zet deze ff terug om het resultaat ook in de lijst te laten weergeven
# dan wordt het voor mij wat overzichtelijker xd ~Niels
if f3 or fx:
    r3=str(client.get_value(number=3).resultaat)
    print "<tr><td>"
    print "Totaal werkgeheugen en beschikbaar geheugen:</td><td>", r3,"</td></tr>"
    
# PS: Eerst beschikbaar IP
if f4 or fx:
    logger.warning('Functie 4 opgevraagd')
    r4=str(client.get_value(number=4).resultaat)
    print "<tr><td>"
    print "Eerst beschikbare IP-adres:</td><td>", r4.rstrip(),"</td></tr>"
    logger.warning('Functie 4 ontvangen')
    csvwriter.writerow((datetime.date.today(), datetime.datetime.now().time().strftime('%H:%M:%S'),
                         hostname, 'Eerste IP', r4.rstrip()))
# PS: Beschikbaar gehugen op C:
if f5 or fx:
    logger.warning('Functie 5 opgevraagd')
    r5=str(client.get_value(number=5).resultaat)
    print "<tr><td>"
    print "Vrije schijfruimte op C: :</td><td>", r5.rstrip(),"</td></tr>"
    logger.warning('Functie 5 ontvangen')
    csvwriter.writerow((datetime.date.today(), datetime.datetime.now().time().strftime('%H:%M:%S'),
                        hostname, 'Geheugen op C:', r5.rstrip()))
# PS: System Uptime
if f6 or fx:
    logger.warning('Functie 6 opgevraagd')
    r6=str(client.get_value(number=6).resultaat)
    print "<tr><td>"
    print "Systeem Uptime:</td><td>", r6.rstrip(),"</td></tr>"
    logger.warning('Functie 6 ontvangen')
    csvwriter.writerow((datetime.date.today(), datetime.datetime.now().time().strftime('%H:%M:%S'),
                         hostname, 'System uptime', r6.rstrip()))
# PS: Aantal ingelogde users
if f7 or fx:
    logger.warning('Functie 7 opgevraagd')
    r7=str(client.get_value(number=7).resultaat)
    print "<tr><td>"
    print "Aantal ingelogde gebruikers:</td><td>", r7.rstrip(),"</td></tr>"
    logger.warning('Functie 7 ontvangen')
    csvwriter.writerow((datetime.date.today(), datetime.datetime.now().time().strftime('%H:%M:%S'),
                         hostname, 'Aantal ingelogde users', r7.rstrip()))
print '</table>'

if f3 or fx:
    logger.warning('Functie 3 opgevraagd')
    r3=str(client.get_value(number=3).resultaat).split()
    print """<div class="item-wd-2-4">
            	<div class="item-content">
            		<h1>Werkgeheugen</h1>
            		<p>Op dit moment is er %s MB beschikbaar van de %s MB</p>
            		<img src="data:image/png;base64,%s"/>
            	</div>
            </div>""" % (r3[1],r3[0],gen_used_bar(int(r3[0])-int(r3[1]),r3[0]))
    logger.warning('Functie 3 ontvangen')
    csvwriter.writerow((datetime.date.today(), datetime.datetime.now().time().strftime('%H:%M:%S'),
                         hostname, 'Totaal en vrij RAM', r3))
print '</HTML>'

logger.warning('---------------END LOG---------------')
handler.close()
logger.removeHandler(handler)
csvf.close()