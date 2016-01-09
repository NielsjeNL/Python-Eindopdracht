# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pysimplesoap.client import SoapClient
reactie = str()
class agent():
  
    def __init__(self, name, hostname, port):
        self.name = str(name)
        self.hostname = str(hostname) #of IP
        self.port = str(port)
        self.client = SoapClient(location = "http://"+self.hostname+":"+self.port+"/",
                                 action = "http://"+self.hostname+":"+self.port+"/",
                                 namespace = "http://example.com/sample.wsdl",
                                 soap_ns='soap',
                                 ns = False)
        print 'agent aangemaakt:',self.name, self.hostname,self.port
        print 'verbinding check', self._checkconnection()
    
    def _checkconnection(self):
        try:
            self.client.Echo(value=True)
            return True
        except:
            return False
            
    def retrievedata(self, platform=False, ip=False, loggedinusers=False, services=False, freespace=False,systeminfo=False, ram=False, uptime=False):
        response = self.client.get_value(platform=platform, ip=ip, loggedinusers=loggedinusers, services=services, freespace=freespace,systeminfo=systeminfo, ram=ram, uptime=uptime).resultaat
        reactie = response
        return response

test = agent('Jasper-PC', 'localhost', 8008)
test1 = agent('Jasper-PC1', 'localhost', 8009)

#data = test.retrievedata(platform=True,freespace=True)
#print data

reactie = test.client.get_value(platform=True)
reactie1  = test1.client.get_value(platform=True)
