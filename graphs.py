import matplotlib.pyplot as plt
import cStringIO
import sqlite3
import numpy as np

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
    
def services_bar(hostname):    
    '''Maakt een horizontale balk van alle services. Data haalt hij uit de SQL database. '''
    listSQL = []
    
    # SQLite DB openen
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""SELECT datetime, hostname, servicesRunning, servicesStopped FROM management 
                WHERE hostname=\'"""+hostname+"""\' ORDER BY datetime DESC""")
    for i in range(5):
        a = c.fetchone()
        listSQL.append(a)
    # DB weer sluiten, anders wordt deze permanent gelocked totdat script stopt
    conn.close()    
    
    # Totalen optellen
    servT1 = listSQL[0][2] + listSQL [0][3]
    servT2 = listSQL[1][2] + listSQL [1][3]
    servT3 = listSQL[2][2] + listSQL [2][3]
    servT4 = listSQL[3][2] + listSQL [3][3]
    servT5 = listSQL[4][2] + listSQL [4][3]
    # Grafiek maken van de services
    N = 5
    servRunning = (listSQL[0][2], listSQL[1][2], listSQL[2][2], listSQL[3][2], listSQL[4][2]) # Running services
    servStopped = (listSQL[0][3], listSQL[1][3], listSQL[2][3], listSQL[3][3], listSQL[4][3]) # Gestopte serivces
    servTotal = (servT1, servT2, servT3, servT4, servT5) # Totale services
    servRStd = (3, 3, 3, 3, 3) # Voor de lijntjes die de getallen met de balk verbinden
    servSStd = (4, 4, 4, 4, 4)
    servTStd = (6, 6, 6, 6, 6)
    
    ind = np.arange(0, N*1.2, 1.2)  # the x locations for the groups
    width  = 0.35       # the width of the bars
    width2 = 0.7       # for the blue bar
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, servRunning, width, color='r', yerr=servRStd) # Rektangle van de running services
    rects2 = ax.bar(ind + width, servStopped, width, color='y', yerr=servSStd) # En van de gestopte
    rects3 = ax.bar(ind + width2, servTotal, width, color='b', yerr=servTStd) # En van de totalen
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Aantal services') # Verticale label
    ax.set_title('Running en gestopte services') # Label aan de top
    ax.set_xticks(ind + 0.55) # Posities van de textlabels
    ax.set_xticklabels(('M1', 'M2', 'M3', 'M4', 'M5')) # Labels aan de onderkant
    
    ax.legend((rects1[0], rects2[0], rects3[0]), ('Running', 'Gestopt', 'Totaal'), loc=4)
    
    def autolabel(rects): 
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    #plt.show()
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)
    return sio.getvalue().encode("base64").strip()