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
# Loop door alle servers...
#print etree.tostring(configtree, pretty_print=True).decode('UTF-8')
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
if page == None:
    page = 'Home'
#loop door waardes heen
#for i in cgidata.keys():
# print cgidata[i].value


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
    <form id="form-agents" action="?page=%s&results" method="post">
        <table>
            <tr><td style="border-bottom: solid; border-bottom-width: 2px;">Alles ophalen:</td>
                <td style="border-bottom: solid; border-bottom-width: 2px;"><input type="checkbox" name="req_all" value="True"/>Yes</td></tr>
            <tr><td>Platform-type:          </td><td><input type="checkbox" name="req_platform" value="True"/>Yes</td></tr>
            <tr><td>Running en totaal # services:</td><td><input type="checkbox" name="req_services" value="True"/>Yes</td></tr>
            <tr><td>Totaal RAM en beschikbaar RAM:             </td><td><input type="checkbox" name="req_ram" value="True"/>Yes</td></tr>
            <tr><td>Eerst beschikbaar IP:   </td><td><input type="checkbox" name="req_ip" value="True"/>Yes</td></tr>
            <tr><td>Vrij geheugen op C: :   </td><td><input type="checkbox" name="req_freespace" value="True"/>Yes</td></tr>
            <tr><td>Systeem uptime:         </td><td><input type="checkbox" name="req_uptime" value="True"/>Yes</td></tr>
            <tr><td>Aantal ingelogde users: </td><td><input type="checkbox" name="req_loggedinusers" value="True"/>Yes</td></tr>
        </table>
        <input type="submit" name="submitform" value="Vraag op"/> 
    </form>
    ''' % (page,page)
    if results == '1':
        print 'results is 1'

print '''</div>
<div class="container footer">
	<p>© 2015 door Jasper van Duijn en Niels den Otter</p>

</div>
</body>
</html>'''