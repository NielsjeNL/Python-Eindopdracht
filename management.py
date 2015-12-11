from pysimplesoap.client import SoapClient, SoapFault
import cgi, cgitb
cgitb.enable()

form = cgi.FieldStorage()

value1 = form.getvalue('value1')
value2  = form.getvalue('value2')

# create a simple consumer
client = SoapClient(
    location = "http://localhost:8008/",
    action = 'http://localhost:8008/', # SOAPAction
    namespace = "http://example.com/sample.wsdl",
    soap_ns='soap',
    ns = False)

#HTML-metadata I guess??
print "Content-Type: text/html;charset=utf-8"
print

#De default pagina
print '<HTML><HEAD><TITLE>Welkom bij dit management script ofzo enzo!</TITLE></HEAD>'
print '<BODY>'
print '<H1>Je kan allemaal dingen opvragen enzo!!! SUPER COOL!!!</H1>'

print '<p>'
print 'Hier komt uitleg over de knoppen...'
print '<br>'



# Code om zooi op te vragen
print "Resultaten:"
# call a few remote methods
r1=str(client.get_value(number=1).resultaat)
print "Resultaat number=1 :", r1
#
r2=str(client.get_value(number=2).resultaat)
print "Resultaat number=2 :", r2
#
r3=str(client.get_value(number=3).resultaat)
print "Resultaat number=3 :", int(r3) # r3 is a number!
#
r4=str(client.get_value(number=4).resultaat)
print "Resultaat number=4 :", r4.rstrip() # This is a multiline: strip the newline from the result!
#
r5=str(client.get_value(number=5).resultaat)
print "Resultaat number=5 :", r5.rstrip()
print '</BODY>'
print '</html>'

