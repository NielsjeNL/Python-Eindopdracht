# -*- coding: utf-8 -*-
"""
Beschrijving van bestand

"""
from pysimplesoap.client import SoapClient
import datetime
import csv

class agent():
    ''' Class agent waarin de agentobjecten worden aangemaakt '''  
    def __init__(self, name, host, port):
        self.name = str(name)
        self.host = str(host) #of IP
        self.port = str(port)
        self.client = SoapClient(location = "http://"+self.host+":"+self.port+"/",
                                 action = "http://"+self.host+":"+self.port+"/",
                                 namespace = "http://example.com/sample.wsdl",
                                 soap_ns='soap',
                                 ns = False)
        self.online = self.checkconnection()
        self.csvfilename = 'management-'+self.name+'.csv'
        
        
    def __str__(self):
        '''functie die name, host, poort en laatst bekende verbindingsstatus teruggeeft.'''
        return ("Agent aangemaakt: %s %s:%s Verbindingscontrole: %s" % (self.name,self.host,self.port, str(self.online)))
    
    def checkconnection(self):
        '''Simpele test of dat de verbinding tot stand kan worden gebracht.'''
        try:
            self.client.Echo(value=True)
            return True
        except:
            return False
            
    def retrievedata(self, platform=False, ip=False, loggedinusers=False, services=False, freespace=False, ram=False, uptime=False):
        '''Functie om gegevens op te vragen aan de server. Er kan worden opgegeven welke waarde er moet worden opgevraagd door dat argument al True mee te geven'''
        try:
            response = self.client.get_value(platform=platform, ip=ip, loggedinusers=loggedinusers, services=services, freespace=freespace, ram=ram, uptime=uptime).resultaat
            self.online = True
            try:
                self.csvf  = open(self.csvfilename, 'a') 
                self.csvwriter = csv.writer(self.csvf,lineterminator='\n')
                self.csvwriter.writerow((datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.name, 'Requested zooi', repr(response)))
                self.csvf.close()
            except:
                print "Kan CSV bestand niet bijwerken"
            
            return response
        except:
            self.online = False
            return False

def process_response(response):
    '''input is pysoap simpleXML reactie verkregen van de agent, geeft dictionary terug met opgevraagde waarden'''
    output = {}
    todelete =[]
    output['platform'] = str(response.platform)
    output['ip'] = str(response.ip)
    output['loggedinusers'] = str(response.loggedinusers)
    output['services'] = str(response.services).split()
    output['freespace'] = str(response.freespace).split()
    output['ram'] = str(response.ram).split()
    output['uptime'] = str(response.uptime)
    for i in output:
        if output[i] == '':
            todelete.append(i)
        if output[i] == []:
            todelete.append(i)
    for i in todelete:
        del output[i]
    return output