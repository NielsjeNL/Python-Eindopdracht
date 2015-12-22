# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:22:25 2015

@author: Jasper
"""
import cgi
import matplotlib.pyplot as pyplot
import cStringIO
import cgi, cgitb
from pysimplesoap.client import SoapClient

client = SoapClient(
    location = "http://127.0.0.1:8008/",
    action = "http://127.0.0.1:8008/", # SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    ns = False)

r2=str(client.get_value(number=2).resultaat)
waarde=r2.split()

cgitb.enable()
def generate_graphxofx(value1,value2):
    # Data to plot
    labels = 'Running', 'Stopped'
    sizes = [value1, value2]
    colors = ['gold', 'yellowgreen']
    explode = (0.1, 0)  # explode 1st slice
     
    # Plot
    pyplot.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    pyplot.title('Services')
    pyplot.axis('equal')
    format = "png"
    sio = cStringIO.StringIO()
    pyplot.savefig(sio, format=format)
    return sio.getvalue().encode("base64").strip()


#De default pagina
print 'Status: 200 OK\n'
print '<HTML>'
print '<HEAD>'
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
print '<TITLE>Test</TITLE>'
print '</HEAD>'
print '<BODY>'

print "<p>Running services,total :", r2.split(),"</p>"
print """
<p>pyplot dingetje:</p>
<img height="300px" src="data:image/png;base64,%s"/>
</body></html>""" % generate_graphxofx(waarde[0],waarde[1])