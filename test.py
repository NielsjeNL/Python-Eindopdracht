# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:22:25 2015

@author: Jasper
"""
import cgi
import matplotlib.pyplot as pyplot
import cStringIO
import cgi, cgitb

cgitb.enable()
def generate_graph():
    pyplot.plot([10,10,10,30,20,25,30,35,70,75,80,10],label='Belasting')
    pyplot.grid(True)
    pyplot.title('Processorbelasting gedurende het uur')
    pyplot.xlabel('Tijd in uren')
    pyplot.ylabel('Belasting in %')
    pyplot.legend(loc='upper left') # best / upper/lower/left/right
    pyplot.axis(ymin=0,ymax=100)
    #pyplot.show()
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
print """
<p>pyplot dingetje:</p>
<img src="data:image/png;base64,%s"/>
</body></html>""" % generate_graph()