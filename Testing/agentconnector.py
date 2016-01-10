# -*- coding: utf-8 -*-
"""
Beschrijving van bestand

"""
from pysimplesoap.client import SoapClient

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
        print 'agent aangemaakt:',self.name, self.host,self.port
        print 'verbinding check', self.online
    
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
            return response
        except:
            self.online = False
            return False

#test = agent('Jasper-PC1', 'localhost', 8008)
#reactie = test.retrievedata(platform=True, ip=True, loggedinusers=True, services=True, freespace=True, ram=True, uptime=True)
#print "Platform:",reactie.platform,"\nUptime:",reactie.uptime,"\nIP:",reactie.ip