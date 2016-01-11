# -*- coding: utf-8 -*-
""""Dit script vraagt waardes op van de agents en zet deze elke 5 minuten in een database."""
from lxml import etree
import agentconnector
import sqlite3
import sys
import datetime as datetime
import time

# Variabelen aanmaken
datadict = {'hostname':'','datetime':'','r1':'', 'r2running':'', 'r2stopped':'',
            'r3total':'','r3free':'','r4':'', 'r5':'', 'r6':'','r7':0};
hosts   = {}

# Config inlezen
configtree = etree.parse('mgmtconfig.xml')
systems = configtree.xpath('/config/server')
for i in systems:
    name = i.get('name')
    host = i.xpath('./host')[0].text
    port = i.xpath('./port')[0].text
    hosts[i.get('name')] = agentconnector.agent(name, host, port)
    
print 'Ingestelde hosts:', hosts

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

    
def requestData():
    """Data ophalen van de agents en deze in de database zetten"""
    # SQLite DB opzetten
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
        
    print "\nData aan het ophalen..."
    sys.stdout.flush() # Console forceren om te printen
    for key in hosts:
        hostname = hosts[key]
        print 'Data voor host',hostname.name,'met hostname of ip',hostname.host
        # Gegevens ophalen en in dict zetten
        reactie = hostname.retrievedata(platform=True, ip=True, loggedinusers=True, services=True, freespace=True, ram=True, uptime=True)
        if reactie == False:
            print "ERROR: ", hostname.name, "is niet bereikbaar"
        else:
            datadict['hostname'] = hostname.name
            datadict['datetime'] = str(datetime.datetime.now())
            datadict['r1'] = str(reactie.platform)
            r2 = str(reactie.services)
            datadict['r3'] = str(reactie.ram)
            datadict['r4'] = str(reactie.ip)
            datadict['r5'] = str(reactie.freespace)
            datadict['r6'] = str(reactie.uptime)
            datadict['r7'] = str(reactie.loggedinusers)
            datadict['r2running'] = str(r2).split()[0]
            datadict['r2stopped'] = str(r2).split()[1]
            datadict['r3total'] = str(datadict['r3']).split()[0]
            datadict['r3free']  = str(datadict['r3']).split()[1]
            
            print "Hostname:", datadict['hostname']
            print "Datum en tijd:", datadict['datetime']
            print "Platform type:", datadict['r1']
            print "Running en totaal aantal services:", datadict['r2running'],'running,', datadict['r2stopped'],'gestopt'
            print "Totaal werkgeheugen en beschikbaar geheugen:", datadict['r3total'],'totaal,',datadict['r3free'],'vrij'
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