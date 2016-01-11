# -*- coding: utf-8 -*-
""""Dit script vraagt waardes op van de agents en zet deze elke 5 minuten in een database."""
from pysimplesoap.client import SoapClient, SoapFault
from lxml import etree
import sqlite3
import sys
import re
import datetime as datetime
import time

# Variabelen aanmaken
datadict = {'hostname':'','datetime':'','r1':'', 'r2running':'', 'r2stopped':'',
            'r3total':'','r3free':'','r4':'', 'r5':'', 'r6':'','r7':0};
hosts   = {}

# Config inlezen
configtree = etree.parse('dbrequests.xml')
#for tag in configtree.getiterator():
    #print tag.tag, tag.text
    #if tag.tag is str( 'hostname'):    # De bedoeling was om automatisch het aantal hosts in het XML bestand te scannen
        #print tag.text                 # Maar i.v.m. te weinig tijd is dit niet gelukt.
aantalHosts = 99                        # Hiermee instellen hoeveel agents in het XML bestand zitten
try:
    for i in range(aantalHosts):
        hostname = str(configtree.xpath('/config/hostname/text()')[i])
        hosts[i] = hostname
except:
    pass
print 'Ingestelde hosts:', hosts
    
# Poort instellen
port = str(configtree.xpath('/config/port/text()')[0])

# SQLite DB opzetten, als data.db niet bestaat maakt hij deze vanzelf aan
conn = sqlite3.connect('data.db')
# Aanmaken tabel DB als deze niet bestaat
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS management (
	datetime	TEXT,
	hostname	TEXT,
	platform	TEXT,
	servicesRunning	INTEGER,
	servicesStopped	INTEGER,
	ramTotal	TEXT,
	ramVrij	INTEGER,
	IP	TEXT,
	schijfruimte	TEXT,
	uptime	TEXT,
	ingelogdeUsers	TEXT);''')
# DB weer sluiten, anders wordt deze permanent gelocked totdat script stopt
conn.close()
###############################################################################
# Verbinding testen en fout weergeven als deze niet werkt
for key in hosts:
    hostname = hosts[key]
    client = SoapClient(
        location = "http://"+hostname+":"+port+"/",
        action = "http://"+hostname+":"+port+"/", # SOAPAction
        namespace = "http://example.com/sample.wsdl",
        soap_ns='soap',
        ns = False)
    try:
        print client.get_value(number=999).resultaat
        print 'Verbinding met',hostname,'ok'
    except:
        print "Er is iets fout gegaan met het opzetten van de verbinding met",hostname,", controleer adres en poort"
    #exit()
    
def requestData():
    """Data ophalen van de agents en deze in de database zetten"""
    # SQLite DB opzetten
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
        
    print "\nData aan het ophalen..."
    sys.stdout.flush() # Console forceren om te printen
    for key in hosts:
        hostname = hosts[key]
        client = SoapClient(
            location = "http://"+hostname+":"+port+"/",
            action = "http://"+hostname+":"+port+"/", # SOAPAction
            namespace = "http://example.com/sample.wsdl",
            soap_ns='soap',
            ns = False)
        print 'Data voor host',hostname
        # Gegevens ophalen en in dict zetten
        datadict['hostname'] = hostname
        datadict['datetime'] = str(datetime.datetime.now())
        datadict['r1'] = str(client.get_value(number=1).resultaat).strip()
        datadict['r3']=str(client.get_value(number=3).resultaat).strip()
        datadict['r4']=str(client.get_value(number=4).resultaat).strip()
        datadict['r5']=str(client.get_value(number=5).resultaat).strip()
        datadict['r6']=str(client.get_value(number=6).resultaat).strip()
        datadict['r7']=str(client.get_value(number=7).resultaat).strip()
        # RegExp toepassen en dan in dict zetten
        RegExpS = '[0-9]{1,3}'  # RegExp voor Services
        r2 = str(client.get_value(number=2).resultaat).strip()
        r2 = re.findall(RegExpS, r2)
        datadict['r2running'] = int(r2[0])
        datadict['r2stopped'] = int(r2[1])
        
        RegExpR = '[0-9]{1,6}'  # RegExp voor RAM
        r3 = str(client.get_value(number=3).resultaat).strip()
        r3 = re.findall(RegExpR, r3)    
        datadict['r3total'] = int(r3[0])
        datadict['r3free']  = int(r3[1])
        
        print "Hostname:", datadict['hostname']
        print "Datum en tijd:", datadict['datetime']
        print "Platform type:", datadict['r1']
        print "Running en totaal aantal services:", datadict['r2running'],'running,', datadict['r2stopped'],'gestopt'
        print "Totaal werkgeheugen en beschikbaar geheugen:", datadict['r3total'],'MB totaal,',datadict['r3free'],'MB vrij'
        print "Eerst beschikbare IP-adres:", datadict['r4']
        print "Vrije schijfruimte op C: :", datadict['r5']
        print "Systeem Uptime:", datadict['r6']
        print "Aantal ingelogde gebruikers:", datadict['r7'],"\n"
        print "Committing naar de database..."
        
        # Elke key inserten
        try:
            c.execute('''INSERT INTO management (datetime, hostname, platform, servicesRunning, servicesStopped, 
                                                 ramTotal, ramVrij, IP, schijfruimte, uptime, ingelogdeUsers)  
                         VALUES (:datetime, :hostname, :r1, :r2running,:r2stopped, 
                                 :r3total, :r3free, :r4, :r5, :r6, :r7)''', datadict)
            conn.commit()
            print 'Alles gecommit!\n'
        except:
            print 'Er is iets fout gegaan, is de database gelocked?\n'
            print 'Commit wordt nu overgeslagen...'
    conn.close()
   
###############################################################################
work = True
while work:
    requestData()     # Alles opvragen en in de database zetten
    time.sleep(300)   # 5min wachten