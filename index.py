# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 02:08:36 2016

@author: jasper & niels
"""
from lxml import etree
import agentconnector
import cgi, cgitb
import logging
import graphs
cgitb.enable()
# HTML-metadata
#print 'Status: 200 OK\n'
print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
#-----------------------
#configuratie inladen
configtree = etree.parse('mgmtconfig.xml')
#print etree.tostring(configtree, pretty_print=True).decode('UTF-8') # print inhoud van XML pagina

# Logging opzetten
logfile = str(configtree.xpath('/config/logging/logfile/text()')[0])
loglevel = str(configtree.xpath('/config/logging/loglevel/text()')[0])
logger = logging.getLogger()
logger.setLevel(loglevel)

# file handler maken, deze schrijft uiteindelijk het log weg
handler = logging.FileHandler(logfile)
handler.setLevel(loglevel)

# format voor het log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# begin van het log schrijven
logger.warning('--------------BEGIN LOG--------------')
logger.warning('Script is begonnen')

# Loop door alle servers...
systems = configtree.xpath('/config/server')
serveragent={}
for i in systems:
    name = i.get('name')
    host = i.xpath('./host')[0].text
    port = i.xpath('./port')[0].text
    serveragent[i.get('name')] = agentconnector.agent(name, host, port)
    logger.warning(serveragent[i.get('name')])
    
#opvragen CGI data
cgidata = cgi.FieldStorage()
logger.warning('CGI data: '+str(cgidata))
page = cgidata.getvalue('page')
results = cgidata.getvalue('results')
req_all  = bool(cgidata.getvalue('req_all'))
req_platform  = bool(cgidata.getvalue('req_platform'))
req_services  = bool(cgidata.getvalue('req_services'))
req_ram  = bool(cgidata.getvalue('req_ram'))
req_ip  = bool(cgidata.getvalue('req_ip'))
req_freespace  = bool(cgidata.getvalue('req_freespace'))
req_uptime  = bool(cgidata.getvalue('req_uptime'))
req_loggedinusers  = bool(cgidata.getvalue('req_loggedinusers'))

if page == None:
    page = 'Home'

#-------------------------------
# Opvragen opgegeven waardes bij agent

if results == '1':
    if req_all == True:
        logger.warning('Alle gegevens van '+page+' worden opgevraagd.')
        reactie = serveragent[page].retrievedata(platform=True, ip=True, loggedinusers=True, services=True, freespace=True, ram=True, uptime=True)
    else:
        logger.warning('Gegevens van '+page+': platform '+ str(req_platform) +"ip"+ str(req_ip) +"loggedin users"+ str(req_loggedinusers) +"services"+ str(req_services) +"freespace"+ str(req_freespace)+"ram"+ str(req_ram) +"uptime"+ str(req_uptime))
        reactie = serveragent[page].retrievedata(platform=req_platform, ip=req_ip, loggedinusers=req_loggedinusers, services=req_services, freespace=req_freespace, ram=req_ram, uptime=req_uptime)

# Opbouwen HTML pagina
print '''<!DOCTYPE html>

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>%s - Beheertool</title>
  <link href="style.css" rel="stylesheet" type="text/css">
  <link rel="shortcut icon" href="./images/favicon.ico" type="image/x-icon">
  <link rel="icon" href="./images/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-1.10.2.js"></script>
  <script src="https://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
</head>

<body>
<div class="header">
<div class="container">
<ul class="header-nav left">''' %page
if page == 'home':
    print '''<li class="header-nav-item"><a class="header-nav-linkc" href="index.py">Homepagina</a></li>'''
else:
    print '''<li class="header-nav-item"><a class="header-nav-link" href="index.py">Homepagina</a></li>'''
    
for name in serveragent:
    if page == name:
        print "<li class=\"header-nav-item\"><a class=\"header-nav-linkc\" href=\"index.py?page=%s\">%s</a></li>" % (name,name)
    else:
        print "<li class=\"header-nav-item\"><a class=\"header-nav-link\" href=\"index.py?page=%s\">%s</a></li>" % (name,name)
if page == 'history':
    print '''<li class="header-nav-item"><a class="header-nav-linkc" href="index.py?page=history">History</a></li>'''
else:
    print '''<li class="header-nav-item"><a class="header-nav-link" href="index.py?page=history">History</a></li>'''
print '''</ul>
<!--
<ul class="header-nav right">

<li class="header-nav-item"><a href="#" class="header-nav-link" alt="Button autorefresh"><img class="header-icon" src="./images/refresh-icon.png"/></a></li>
</ul> -->
</div>
</div>
<div class="main-content">'''
if page == 'Home':
    logger.warning('Homepagina wordt weergegeven')
    print '''
    <h1>Homepage</h1>
    <p>Welkom op de beheerspagina van het management systeem van Jasper en Niels. Dit systeem kan van agents systeem informatie opvragen, welke informatie precies kan worden aangegeven in het selectie veld op de desbetreffende agent pagina.</p>
    <p>Voordat het systeem werkt moet eerst het configuratiebestand worden aangepast, hoe dat dit precies moet staat beschreven in het INSTALL.txt bestand.</p>    
    '''
elif page == 'history':
	print '''<h1>Historische data</h1>
	<p>Op deze pagina worden oude gegevens uit de database weergegeven van de agents die in het XML bestand zijn aangemaakt. Dit kan handig zijn om patronen te herkennen.</p> <p>Op dit moment wordt er elke 5 minuten data opgehaald en worden alleen de laatste 5 resultaten weergegeven, als er nog geen 5 resultaten zijn wordt er niets weergegeven.</p>
	'''
	for name in serveragent:
		grafiek = graphs.services_bar(name)
		if grafiek != False:
			print ''' <div class="item-wd-2-4">
                    	<div class="item-content">
                    		<h1>%s</h1>
                    		<p>Status van de laatste 5 keer dat de services zijn opgevraagd op %s</p>
                    		<img src="data:image/png;base64,%s"/>
                    	</div>
                    </div>
                    ''' % (name,name,grafiek)
	
elif page != 'Home':
    logger.warning(page +' pagina wordt weergegeven')
    print '''
    <h1>%s</h1>
    <p>
      Selecteer de counters die opgehaald moeten worden.
    </p><br />
    <form id="form-agents" action="?page=%s&results=1" method="post">
        <table>
            <tr><td style="border-bottom: solid; border-bottom-width: 2px;">Alles ophalen:</td><td style="border-bottom: solid; border-bottom-width: 2px;"/><td style="border-bottom: solid; border-bottom-width: 2px;"/>
            <td style="border-bottom: solid; border-bottom-width: 2px;"><input type="checkbox" name="req_all" value="True"/>Yes</td></tr>
			
            <tr><td>Platform-type:</td><td><input type="checkbox" name="req_platform" value="True"/>Yes</td><td>Running en totaal # services:</td><td><input type="checkbox" name="req_services" value="True"/>Yes</td></tr>
            <tr><td>Totaal RAM en beschikbaar RAM:</td><td><input type="checkbox" name="req_ram" value="True"/>Yes</td><td>Eerst beschikbaar IP:</td><td><input type="checkbox" name="req_ip" value="True"/>Yes</td></tr>
            <tr><td>Vrij geheugen op C:</td><td><input type="checkbox" name="req_freespace" value="True"/>Yes</td><td>Systeem uptime:</td><td><input type="checkbox" name="req_uptime" value="True"/>Yes</td></tr>
            <tr><td>Aantal ingelogde users:</td><td><input type="checkbox" name="req_loggedinusers" value="True"/>Yes</td></tr>
        </table>
        <input type="submit" name="submitform" value="Vraag op"/> 
    </form>
    ''' % (page,page)
    if results == '1':
        if reactie == False:
            logger.warning(page +' is onbreikbaar, controleer netwerkverbinding / instellingen')
            print '''<p>De agent is niet te bereiken! Controleer de instellingen / netwerk verbinding en probeer het opnieuw.</p>'''
        else:
            resultaten = agentconnector.process_response(reactie)
            logger.warning("Resultaten ontvangen: "+str(resultaten))
            tablerows = ''
            grafieken = ''
            for i in resultaten:
                if i == 'services':
                    grafiek = graphs.gen_pie_xofx(resultaten[i][0],resultaten[i][1],'Running','Stopped')
                    logger.warning("Services grafiek gegenereerd")
                    grafieken = grafieken + ''' <div class="item-wd-2-4">
                    	<div class="item-content">
                    		<h1>Services</h1>
                    		<p>Status: %i running services en %i gestopte services</p>
                    		<img src="data:image/png;base64,%s"/>
                    	</div>
                    </div>
                    ''' % (int(resultaten[i][0]),int(resultaten[i][1]),grafiek)
                    tablerows = tablerows + ("<tr><td>Running services</td><td>%s</td></tr>" % (resultaten[i][0]))
                elif i == 'freespace':
                    percentage = int(100-float(resultaten[i][1])/float(resultaten[i][0])*100)
                    grafieken = grafieken + ''' 
                    <script>
                          $(function() {
                            $( "#progressbar1" ).progressbar({
                              value: %i
                            });
                          });
                          </script>                    
                    <div class="item-wd-2-4">
                    	<div class="item-content">
                    		<h1>Hard disk</h1>
                    		<p>Info over C:\ schijf: <br/> Omvang: %s GB<br/>Beschikbaar: %s GB</p>
                    		<div id="progressbar1"><div class="progress-label">%i %%</div></div>
                    	</div>
                    </div>
                    ''' % (percentage, str(resultaten[i][0]),str(resultaten[i][1]),percentage)
                    tablerows = tablerows + ("<tr><td>Vrije schijf ruimte</td><td>%s GB</td></tr>" % (resultaten[i][1]))
                elif i=='ram':
                    percentage = int(100-(float(resultaten[i][1])/float(resultaten[i][0])*100))
                    grafieken = grafieken + '''
                    <script>
                          $(function() {
                            $( "#progressbar" ).progressbar({
                              value: %i
                            });
                          });
                          </script>
                    <div class="item-wd-2-4">
                    	<div class="item-content">
                    		<h1>Werkgeheugen</h1>
                    		<p>Onderstaande balk geeft aan hoeveel geheugen er van de %s MB verbruikt is.</p>
                    		<div id="progressbar"><div class="progress-label">%i %%</div></div>
                    	</div>
                    </div>
                    ''' % (percentage,resultaten[i][0],percentage)
                    tablerows = tablerows + ("<tr><td>Werkgeheugen</td><td>%s MB</td></tr>" % (resultaten[i][0]))
                else:
                    tablerows = tablerows + ("<tr><td>%s</td><td>%s</td></tr>" % (i,resultaten[i]))
                
            
            print '''
            <div class="item-wd-2-4">
                <div class="item-content">
                    <h1>Systeem informatie</h1>
                        <table> '''
            print tablerows
            print '''</table>
            	</div>
            </div> '''
            print grafieken
print '''</div>
<div class="container footer">
	<p>© 2015 door Jasper van Duijn en Niels den Otter</p>

</div>
</body>
</html>'''
logger.warning('Pagina volledig verstuurd.')
logger.warning('---------------END LOG---------------')
handler.close()
logger.removeHandler(handler)