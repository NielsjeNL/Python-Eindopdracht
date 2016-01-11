# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 02:08:36 2016

@author: jaspe
"""
from lxml import etree
from agentconnector import agent
import logging

#-----------------------
#configuratie inladen
configtree = etree.parse('mgmtconfig.xml')
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
# handler toevoegen aan het log, let op dat je dit maar 1 keer doet anders krijg je dubbele logs
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
    serveragent[i.get('name')] = agent(name, host, port)
    print (serveragent[i.get('name')])
    
    logger.warning('agent aangemaakt: '+serveragent[i.get('name')].name+' '+serveragent[i.get('name')].host+':'+serveragent[i.get('name')].port)
    logger.warning('verbinding check '+str(serveragent[i.get('name')].online))


logger.warning('---------------END LOG---------------')
handler.close()
logger.removeHandler(handler)