# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 02:08:36 2016

@author: jaspe
"""
from lxml import etree
import agentconnector
import cgi, cgitb
import logging
cgitb.enable()

#-----------------------
#configuratie inladen
configtree = etree.parse('mgmtconfig.xml')

# Loop door alle servers...
print str(configtree.xpath('/config/logging/loglevel/text()')[0])
systems = configtree.xpath('/config/server')
serveragent={}
for i in systems:
    print ('banaan')
    name = i.get('name')
    host = i.xpath('./host')[0].text
    port = i.xpath('./port')[0].text
    serveragent[i.get('name')] = agentconnector.agent(name, host, port)

# HTML-metadata
#print 'Status: 200 OK\n'
print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

test = agentconnector.agent('Jasper-PC', 'localhost', 8008)
print test.name
# Tijdelijke test data
activeagent = 'Server1'

# Opbouwen HTML pagina
print '''<!DOCTYPE html>

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <title>Agent1 pagina</title>
  <link href="style.css" rel="stylesheet" type="text/css">
  <link rel="shortcut icon" href="./images/favicon.ico" type="image/x-icon">
  <link rel="icon" href="./images/favicon.ico" type="image/x-icon">
  <script language="javascript" type="text/javascri pt">
  function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
  }
</script>
</head>

<body>
<div class="header">
<div class="container">
<ul class="header-nav left">
<li class="header-nav-item"><a class="header-nav-link" href="index.py">Homepagina</a></li>'''

for name in serveragent:
    print '''banaan'''
    if activeagent == name:
        print "<li class=\"header-nav-item\"><a class=\"header-nav-linkc\" href=\"index.py?page=%s\">%s</a></li>" % (name,name)
    else:
        print "<li class=\"header-nav-item\"><a class=\"header-nav-link\" href=\"index.py?page=%s\">%s</a></li>" % (name,name)

print '''</ul>
<ul class="header-nav right">
<!--- if page is agent dan onderlinen ofzo-->
<li class="header-nav-item"><a href="?agent=%s" class="header-nav-link" alt="Button nieuwe data op te halen van de actieve agents"><img class="header-icon" src="./images/refresh-icon-agent.png"/></a></li>
<!-- endif -->
<li class="header-nav-item"><a href="?agent=%s" class="header-nav-link" alt="Button nieuwe data op te halen van alle agents"><img class="header-icon" src="./images/refresh-icon.png"/></a></li>
</ul>
</div>
</div>
<div class="main-content">
<h1>%s</h1>''' % (activeagent,activeagent,activeagent)
print '''
<p>
  Selecteer de counters die opgehaald moeten worden.
</p><br />
<form id="form-agents" action="?page=%s" method="post">
    <table>
        <tr><td style="border-bottom: solid; border-bottom-width: 2px;">Alles ophalen:</td>
            <td style="border-bottom: solid; border-bottom-width: 2px;"><input type="checkbox" name="fx" value="True"/>Yes</td></tr>
        <tr><td>Platform-type:          </td><td><input type="checkbox" name="f1" value="True"/>Yes</td></tr>
        <tr><td>Running en totaal # services:</td><td><input type="checkbox" name="f2" value="True"/>Yes</td></tr>
        <tr><td>Totaal RAM:             </td><td><input type="checkbox" name="f3" value="True"/>Yes</td></tr>
        <!-- overbodig<tr><td>Beschikbaar RAM:        </td><td><input type="checkbox" name="f31" value="True"/>Yes</td></tr>-->
        <tr><td>Eerst beschikbaar IP:   </td><td><input type="checkbox" name="f4" value="True"/>Yes</td></tr>
        <tr><td>Vrij geheugen op C: :   </td><td><input type="checkbox" name="f5" value="True"/>Yes</td></tr>
        <tr><td>Systeem uptime:         </td><td><input type="checkbox" name="f6" value="True"/>Yes</td></tr>
        <tr><td>Aantal ingelogde users: </td><td><input type="checkbox" name="f7" value="True"/>Yes</td></tr>
    </table>
    <input type="submit" name="submitform" value="Vraag op"/> 
</form> <br />
''' % (activeagent)
print '''</div>
<div class="container footer">
	<p>© 2015 door Jasper van Duijn en Niels den Otter</p>

</div>
</body>
</html>'''