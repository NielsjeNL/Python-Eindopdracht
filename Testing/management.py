# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 02:08:36 2016

@author: jaspe
"""
from lxml import etree
from agentconnector import *

# Config inlezen
configtree = etree.parse('mgmtconfig.xml')
#hostname = str(configtree.xpath('/config/hostname/text()')[0])
#port = str(configtree.xpath('/config/port/text()')[0])

# Loop door alle boeken...
systems = configtree.xpath('/config/server')
serveragent={}
for i in systems:
    name = i.get('name')
    host = i.xpath('./host')[0].text
    port = i.xpath('./port')[0].text
    serveragent[i.get('name')] = agent(name, host, port)
