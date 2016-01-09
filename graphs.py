import matplotlib.pyplot as plt
import cStringIO

# Grafieken genereren defines
def memory_used_bar(gebruikt, totaal):    
    '''Maakt een horizontale balk met percentage gebruikt en vrij '''
    pctused = float(gebruikt)/float(totaal)
    maximaal = 1-pctused
    fig = plt.figure(figsize=(8, 2))
    width = 1
    #plt.xlabel('Totaal: '+str(totaal))
    p1 = plt.barh(0, pctused,width,color='r')
    p2 = plt.barh(0, maximaal,width,color='y',left=pctused)
    plt.legend((p1[0], p2[0]), ('Gebruikt', 'Vrij'))
    frame = plt.gca()
    frame.axes.get_yaxis().set_visible(False)
    #plt.show()
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)
    return sio.getvalue().encode("base64").strip()