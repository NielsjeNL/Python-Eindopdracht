# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 02:08:36 2016

@author: jaspe
"""
from lxml import etree
import agentconnector
import cgi, cgitb
import logging
import os
cgitb.enable()
# HTML-metadata
#print 'Status: 200 OK\n'
print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
#-----------------------
#configuratie inladen
configtree = etree.parse('mgmtconfig.xml')
#print etree.tostring(configtree, pretty_print=True).decode('UTF-8') # print inhoud van XML pagina

# Loop door alle servers...
systems = configtree.xpath('/config/server')
serveragent={}
for i in systems:
    name = i.get('name')
    host = i.xpath('./host')[0].text
    port = i.xpath('./port')[0].text
    serveragent[i.get('name')] = agentconnector.agent(name, host, port)
    
#opvragen CGI data
cgidata = cgi.FieldStorage()
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

## Debugging data
#page = 'Server1'
#results = '1'
#req_all = True
#print vars()

#-------------------------------
# Opvragen opgegeven waardes bij agent

if results == '1':
    if req_all == True:
        reactie = serveragent[page].retrievedata(platform=True, ip=True, loggedinusers=True, services=True, freespace=True, ram=True, uptime=True)
    else:
        reactie = serveragent[page].retrievedata(platform=req_platform, ip=req_ip, loggedinusers=req_loggedinusers, services=req_services, freespace=req_freespace, ram=req_ram, uptime=req_uptime)
#loop door waardes heen
#for i in cgidata.keys():
#    print i, '-', cgidata[i].value,"<br/>"


# Opbouwen HTML pagina
print '''<!DOCTYPE html>

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>%s - Beheertool</title>
  <link href="style.css" rel="stylesheet" type="text/css">
  <link rel="shortcut icon" href="./images/favicon.ico" type="image/x-icon">
  <link rel="icon" href="./images/favicon.ico" type="image/x-icon">
  <script language="javascript" type="text/javascript">
  function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
  }
</script>
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

print '''</ul>
<ul class="header-nav right">
<!--- if page is agent dan onderlinen ofzo-->
<!-- endif -->
<li class="header-nav-item"><a href="#" class="header-nav-link" alt="Button autorefresh"><img class="header-icon" src="./images/refresh-icon.png"/></a></li>
</ul>
</div>
</div>
<div class="main-content">'''
if page == 'Home':
    print '''
    <h1>Homepage</h1>
    <p>Welkom op de beheerspagina van het management systeem van Jasper en Niels. Dit systeem kan van agents systeem informatie opvragen, welke informatie precies kan worden aangegeven in het selectie veld op de desbetreffende agent pagina.</p>
    <p>Voordat het systeem werkt moet eerst het configuratiebestand worden aangepast, hoe dat dit precies moet staat beschreven in het INSTALL.txt bestand.</p>    
    '''
if page != 'Home':
    print '''
    <h1>%s</h1>
    <p>
      Selecteer de counters die opgehaald moeten worden.
    </p><br />
    <form id="form-agents" action="?page=%s&results=1" method="post">
        <table>
            <tr><td style="border-bottom: solid; border-bottom-width: 2px;">Alles ophalen:</td>
                <td style="border-bottom: solid; border-bottom-width: 2px;"><input type="checkbox" name="req_all" value="True"/>Yes</td></tr>
            <tr><td>Platform-type:</td><td><input type="checkbox" name="req_platform" value="True"/>Yes</td></tr>
            <tr><td>Running en totaal # services:</td><td><input type="checkbox" name="req_services" value="True"/>Yes</td></tr>
            <tr><td>Totaal RAM en beschikbaar RAM:</td><td><input type="checkbox" name="req_ram" value="True"/>Yes</td></tr>
            <tr><td>Eerst beschikbaar IP:</td><td><input type="checkbox" name="req_ip" value="True"/>Yes</td></tr>
            <tr><td>Vrij geheugen op C:</td><td><input type="checkbox" name="req_freespace" value="True"/>Yes</td></tr>
            <tr><td>Systeem uptime:</td><td><input type="checkbox" name="req_uptime" value="True"/>Yes</td></tr>
            <tr><td>Aantal ingelogde users:</td><td><input type="checkbox" name="req_loggedinusers" value="True"/>Yes</td></tr>
        </table>
        <input type="submit" name="submitform" value="Vraag op"/> 
    </form>
    ''' % (page,page)
    if results == '1':
        if reactie == False:
            print '''<p>De agent is niet te bereiken! Controleer de instellingen / netwerk verbinding en probeer het opnieuw.</p>'''
        else:
            resultaten = agentconnector.process_response(reactie)
            tablerows = ''
            for i in resultaten:
                if i == 'services':
                    tablerows = tablerows + ("<tr><td>Running services</td><td>%s</td></tr>" % (resultaten[i][0]))
                else:
                    tablerows = tablerows + ("<tr><td>%s</td><td>%s</td></tr>" % (i,resultaten[i]))
            
            print '''
            <div class="item-wd-1-3">
                <div class="item-content">
                    <h1>Systeem informatie</h1>
                        <table> '''
            print tablerows
            print '''</table>
            	</div>
            </div> '''

print '''</div>
<div class="container footer">
	<p>© 2015 door Jasper van Duijn en Niels den Otter</p>

</div>
</body>
</html>'''