
# coding: utf-8
#libs used
import PyPDF2 as pypdf
import urllib3
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io
import re
#globals
http = urllib3.PoolManager()
pedaleurs=[(None,None,None,None,None,None)]*220 #(NOM,PRENOM,JEUNE,NATION,EQUIPE,int(nombre))
ecarts=[None]*23
points=[None]*23
grimpeurs=[None]*23
jeunes=[None]*23
eq=[None]*23
ecarts[0]=[(0,0)]*220
grimpeurs[0]=[(0,200)]*220
points[0]=[(0,200)]*220
jeunes[0]=[0]*220


def general_proc(string):                       #general classement
    global rankg                                #ecarts[etape][nombre]=(ecart,rank)
    global pedaleurs
    global ecart
    helpr=''
    for k in range(len(string)):                #take away all till the start of the number
        if not string[k].isupper():
            helpr+=(string[k])
        else:
            break
    #seperate number from the distance
    if helpr[-1]=='"':                            #there is an actual distance in seconds
        ecart=0
        ecart+=int(helpr[-2])
        ecart+=int(helpr[-3])*10
        if helpr[-4]=='\'':                       #there are minutes
            ecart+=int(helpr[-5])*60
            ecart+=int(helpr[-6])*600
            if helpr[-7]=='h':                    #there are hours
                ecart+=int(helpr[-8])*60*60
                nombre=helpr[:-8]                 #get the numbers
            else:
                nombre=helpr[:-6]
        else:
            nombre=helpr[:-3]
    else:
        nombre=''                                #same as above pedaleur
        for char in helpr:                       #get just the name
            if char.isdigit():
                nombre+=char
            else:
                break
    ecarts[etape][int(nombre)]=(ecart,rankg)
    rankg+=1
    #fill up the pedaleurs
    if pedaleurs[int(nombre)]==(None,None,None,None,None,None): #pedaleur not added         ######change done
        EQUIPE=string[k:k+3] #both EQUIPE and NATION are both 3 catpital letters
        NATION=string[k+3:k+6]
        for q in range(k+6,len(string)):         #find start of second name
            if string[q].isupper():
                break
        JEUNE=string[q-1]=='*'                    #check if the driver is a young rider
        for p in range(q,len(string)):
            if string[p].islower():               #the second letter of the first name is low
                p-=1
                break
        NOM=string[q:p-1]                          #string[p] is always a whitespace
        PRENOM=string[p:]
        pedaleurs[int(nombre)]=(NOM,PRENOM,JEUNE,NATION,EQUIPE,int(nombre))
def point_proc(string):                            #point classement
    global rankp                                   #points[etape][nombre]=(poi,rank)
    nombre=''
    poi=''
    checkpoint=False
    for i in range(len(string)):                   ###########why checkpoint
        if string[i].isdigit():                 #get number
            nombre+=string[i]
            checkpoint=True
        elif checkpoint==True:
            break
    for q in range(i,len(string)):             #get points start
        if string[q].isdigit():
            break
    string+='buffer'                                #need buffer if number is at the end
    for p in range(q,len(string)):             #get points end
        if not string[p].isdigit():
            break
    nombre=int(nombre)
    poi=int(string[q:p])
    points[etape][nombre]=(poi,rankp)
    rankp+=1
def grimpeurs_proc(string):                   #mountain classement
    global rankgr                             #grimpeurs[etape][nombre]=(grim,rank)
    nombre=''
    grim=''
    checkpoint=False                                    ###why checkpoint
    for i in range(len(string)):
        if string[i].isdigit():               #get number
            nombre+=string[i]
            checkpoint=True
        elif checkpoint==True:
            break
    for q in range(i,len(string)):           #get mountain points start
        if string[q].isdigit():
            break
    for p in range(q,len(string)):           #get mountain points end
        if string[p].isupper():
            break
    nombre=int(nombre)
    grim=int(string[q:p])
    grimpeurs[etape][nombre]=(grim,rankgr)
    rankgr+=1
def jeunes_proc(string):                       #young classement
    global rankj                               #jeunes[etape][int(nombre)]=(rank) (you have to crossreverence it with the general classement)
    nombre=''
    checkpoint=False
    for i in range(len(string)):               #find the number
        if string[i].isdigit():
            nombre+=string[i]
            checkpoint=True
        elif checkpoint and not string[i].isdigit():
            break
    jeunes[etape][int(nombre)]=(rankj)
    rankj+=1

def process(page):
    if ('CLASSEMENT DES JEUNES'==page[:len('CLASSEMENT DES JEUNES')]):
        page=re.split('Page',page,1)[0]              #cut the end
        if len(re.findall('DosNom',page))==2:        #check if there is a daily classement
            page=re.sub('.*NatTempsEcart','',page)   #cut the start
            page=re.sub('.* 1 ',' ',page,1)
        elif len(re.findall('DosNom',page))>2:
            print(page)
            print('problem jeunes')
        page=re.sub('.* 1 ','1',page)               #cut the start again
        entries=re.split(' \d* ',page)              #split the riders
        for pedaleur in entries:                    #process each rider
            jeunes_proc(pedaleur)
    elif ('CLASSEMENT PAR POINTS'==page[:len('CLASSEMENT PAR POINTS')]):
        page=re.sub('.*PrénomEquipePointsNatNat','',page)#cut the start
        #print('pageb',page)
        page=re.split('Page',page)[0]                    #cut the end
        #print('pagea',page)
        page=re.split('Arrivée',page)[0]
        page=re.split(' km',page,1)[0]
        entries=re.split(' \d* ',page)               #split the riders
        entries=entries[1:]                          #first is garbage
        for pedaleur in entries:                     #process each rider
            point_proc(pedaleur)
    elif('CLASSEMENT PAR EQUIPES'==page[:len('CLASSEMENT PAR EQUIPES')]): #eq[etape][equipenom]=(ranke,ecart)
        page=re.sub('.*\s1(?P<first>[A-Z])','\g<first>',page,0,re.DOTALL)#cut the start
        page=re.split('Page',page,1)[0]              #cut the end
        page=re.split('\s[0-9]+',page)               #split the equipes
        ranke=1
        for equipe in page:
            for i in range(len(equipe)):
                if (equipe[i].isdigit() and (equipe[i+1]=='h' or equipe[i+1].isdigit())) or equipe[i]=='\'':
                    break
            equipenom=equipe[:i]
            if equipe[i]=='\'':                      #equipe has the same distance as above
                eq[etape][equipenom]=(ranke,ecart)
                ranke+=1
                continue
            else:
                ecart=0
            if equipe[i+1]=='h':                    #get distance
                ecart+=int(equipe[i])*60*60
                i+=2
            if equipe[i+2]=='\'':
                ecart+=int(equipe[i])*60*10
                ecart+=int(equipe[i+1])*60
                i+=3
            if equipe[i+2]=='"':
                ecart+=int(equipe[i])*10
                ecart+=int(equipe[i+1])
            eq[etape][equipenom]=(ranke,ecart)
            ranke+=1
    elif ('CLASSEMENT DU MEILLEUR GRIMPEUR'==page[:len('CLASSEMENT DU MEILLEUR GRIMPEUR')]):
        page=re.sub('.*PrénomEquipePointsNatNat','',page) #cut the start
        page=re.split('Page',page)[0]                  #cut the end
        page=re.split(' km',page,1)[0]
        entries=re.split(' \d* ',page)                  #split the riders
        entries=entries[1:]                             #first is garbage
        for pedaleur in entries:                        #process each rider
            grimpeurs_proc(pedaleur)
    elif ('CLASSEMENT GENERAL ETAPE ' in page):
        page=re.sub('.*PrénomEq.NatTempsEcart','',page) #cut the start
        page=re.split('Page',page,1)[0]                 #cut the end
        entries=re.split(' \d* ',page)                  #split the riders
        entries=entries[1:]                             #first is garbage
        for pedaleur in entries:                        #process each rider
            general_proc(pedaleur)

 #gather the data
for etape in range(1,23): #change range back to 22
    rankg=1
    rankj=1
    rankgr=1
    rankp=1
    etapestring=(str(hex(etape))[2:]).zfill(2)
    print('working on stage:'+str(etape))
    URL = 'http://azure.tissottiming.com/File/00031001070101'+etapestring+'FFFFFFFFFFFFFF00'
    #download the data
    r = http.request('GET',URL)
#   #check if press-release is ready/a PDF
    if r.info()['Content-type']!='application/pdf':
        print (str(etape)+' not ready')
        break
    #open the file
    ecarts[etape]=[(None,None)]*220
    grimpeurs[etape]=[(0,200)]*220
    points[etape]=[(0,200)]*220
    jeunes[etape]=[None]*220
    eq[etape]=dict()

    read_pdf = pypdf.PdfFileReader(io.BytesIO(r.data))
    #read_pdf=pypdf.PdfFileReader('cat.pdf')
    #process each page
    for pagenum in range(read_pdf.getNumPages()):
        process(read_pdf.getPage(pagenum).extractText())
    print(str(etape)+' is processed')
print('all done')

plat=[1,2,4,7,8,13,18,21]
acci=[5,6,9,14,15]
montagne=[10,11,12,16,17,19]
clm=[3,20]
eq[0]=dict()
for i in eq[1].keys():
    eq[0][i]=(0,0)

pmont = mpatches.Patch(color=(0/3,0/3,1),alpha=0.3, label='mountain')
pacci = mpatches.Patch(color=(1/3,1/3,1),alpha=0.3, label='hilly')
pplat = mpatches.Patch(color=(2/3,2/3,1),alpha=0.3, label='flat')
pclm = mpatches.Patch(color=(1,1,1),alpha=0.3, label='TT')
patches=[pmont,pacci,pplat,pclm]
patchnames=['mountain','hilly','flat','TT']

#usual jaune plot
plt.rcParams.update({'figure.figsize':(30,50),'font.size': 18,'lines.linewidth': 2.5,'legend.fontsize':15,'legend.handlelength':2})
drivers=[i for i in range(220) if ecarts[etape-1][i][1] is not None and ecarts[etape-1][i][1]<=10]
plt.subplot(6,1,1)
plt.xlim(0,etape-1)
plt.xlabel('stage')
plt.xticks(range(etape))
for i in range(1,etape-1):
    if i in plat:
        plt.axvspan(i-1, i, facecolor=pplat.get_fc(), alpha=0.3)
    elif i in montagne:
        plt.axvspan(i-1, i, facecolor=pmont.get_fc(), alpha=0.3)
    elif i in clm:
        plt.axvspan(i-1, i, facecolor=pclm.get_fc(), alpha=0.3)
    elif i in acci:
        plt.axvspan(i-1, i, facecolor=pacci.get_fc(), alpha=0.3)
riders=plt.plot(range(etape),[[ecarts[et][dr][0] for dr in drivers] for et in range(etape)])
plt.ylabel('gap in sec')
plt.title('maillot jaune 2018')
plt.gca().invert_yaxis()
handl=riders+patches
labl=[str(peds)[1:-1] for peds in[[pedaleurs[dr][0]+' '+pedaleurs[dr][1],pedaleurs[dr][3:5]] for dr in drivers]]+patchnames
plt.legend(handles=handl,labels=labl)
#respected jaune plot
plt.subplot(6,1,2)
plt.xlim(0,etape-1)
plt.xlabel('stage')
plt.xticks(range(etape))
for i in range(1,etape):
    if i in plat:
        plt.axvspan(i-1, i, facecolor=pplat.get_fc(), alpha=0.3)
    elif i in montagne:
        plt.axvspan(i-1, i, facecolor=pmont.get_fc(), alpha=0.3)
    elif i in clm:
        plt.axvspan(i-1, i, facecolor=pclm.get_fc(), alpha=0.3)
    elif i in acci:
        plt.axvspan(i-1, i, facecolor=pacci.get_fc(), alpha=0.3)
plt.ylabel('gap in sec')
plt.title('maillot jaune 2018 best 10 compared')
plt.gca().invert_yaxis()
riders=plt.plot(range(etape),[[ecarts[et][dr][0] -min([ecarts[et][dri][0] for dri in drivers]) for dr in drivers] for et in range(etape)])
handl=riders+patches
labl=[str(peds)[1:-1] for peds in[[pedaleurs[dr][0]+' '+pedaleurs[dr][1],pedaleurs[dr][3:5]] for dr in drivers]]+patchnames
plt.legend(handles=handl,labels=labl)
#maillot vert
drivers=[i for i in range(220) if points[etape-1][i][1] is not None and points[etape-1][i][1]<=10]
plt.subplot(6,1,3)
plt.xlim(0,etape-1)
plt.xlabel('stage')
plt.xticks(range(etape))
for i in range(1,etape):
    if i in plat:
        plt.axvspan(i-1, i, facecolor=pplat.get_fc(), alpha=0.3)
    elif i in montagne:
        plt.axvspan(i-1, i, facecolor=pmont.get_fc(), alpha=0.3)
    elif i in clm:
        plt.axvspan(i-1, i, facecolor=pclm.get_fc(), alpha=0.3)
    elif i in acci:
        plt.axvspan(i-1, i, facecolor=pacci.get_fc(), alpha=0.3)
plt.ylabel('points')
plt.title('maillot vert 2018')
riders=plt.plot(range(etape),[[points[et][dr][0] for dr in drivers] for et in range(etape)])
handl=riders+patches
labl=[str(peds)[1:-1] for peds in[[pedaleurs[dr][0]+' '+pedaleurs[dr][1],pedaleurs[dr][3:5]] for dr in drivers]]+patchnames
plt.legend(handles=handl,labels=labl)
#maillot a points
drivers=[i for i in range(220) if grimpeurs[etape-1][i][1] is not None and grimpeurs[etape-1][i][1]<=10]
plt.subplot(6,1,4)
plt.xlim(0,etape-1)
plt.xlabel('stage')
plt.xticks(range(etape))
for i in range(1,etape):
    if i in plat:
        plt.axvspan(i-1, i, facecolor=pplat.get_fc(), alpha=0.3)
    elif i in montagne:
        plt.axvspan(i-1, i, facecolor=pmont.get_fc(), alpha=0.3)
    elif i in clm:
        plt.axvspan(i-1, i, facecolor=pclm.get_fc(), alpha=0.3)
    elif i in acci:
        plt.axvspan(i-1, i, facecolor=pacci.get_fc(), alpha=0.3)
plt.ylabel('points')
plt.title('maillot à pois 2018')
riders=plt.plot(range(etape),[[grimpeurs[et][dr][0] for dr in drivers] for et in range(etape)])
handl=riders+patches
labl=[str(peds)[1:-1] for peds in[[pedaleurs[dr][0]+' '+pedaleurs[dr][1],pedaleurs[dr][3:5]] for dr in drivers]]+patchnames
plt.legend(handles=handl,labels=labl)

#maillot blanc
drivers=[i for i in range(220) if jeunes[etape-1][i] is not None and jeunes[etape-1][i]<=10]
plt.subplot(6,1,5)
plt.xlim(0,etape-1)
plt.xlabel('stage')
plt.xticks(range(etape))
for i in range(1,etape):
    if i in plat:
        plt.axvspan(i-1, i, facecolor=pplat.get_fc(), alpha=0.3)
    elif i in montagne:
        plt.axvspan(i-1, i, facecolor=pmont.get_fc(), alpha=0.3)
    elif i in clm:
        plt.axvspan(i-1, i, facecolor=pclm.get_fc(), alpha=0.3)
    elif i in acci:
        plt.axvspan(i-1, i, facecolor=pacci.get_fc(), alpha=0.3)
plt.ylabel('gap in sec')
plt.title('maillot blanc 2018')
riders=plt.plot(range(etape),[[ecarts[et][dr][0] -min([ecarts[et][dri][0] for dri in drivers]) for dr in drivers] for et in range(etape)])
plt.gca().invert_yaxis()
handl=riders+patches
labl=[str(peds)[1:-1] for peds in[[pedaleurs[dr][0]+' '+pedaleurs[dr][1],pedaleurs[dr][3:5]] for dr in drivers]]+patchnames
plt.legend(handles=handl,labels=labl)
#team
drivers=[i for i in eq[1].keys() if eq[etape-1][i][0]<=10]
plt.subplot(6,1,6)
plt.xlim(0,etape-1)
plt.xlabel('stage')
plt.xticks(range(etape))
for i in range(1,etape):
    if i in plat:
        plt.axvspan(i-1, i, facecolor=pplat.get_fc(), alpha=0.3)
    elif i in montagne:
        plt.axvspan(i-1, i, facecolor=pmont.get_fc(), alpha=0.3)
    elif i in clm:
        plt.axvspan(i-1, i, facecolor=pclm.get_fc(), alpha=0.3)
    elif i in acci:
        plt.axvspan(i-1, i, facecolor=pacci.get_fc(), alpha=0.3)
plt.ylabel('gap in sec')
plt.title('team classification 2018')
riders=plt.plot(range(etape),[[eq[et][dr][1] -min([eq[et][dri][1] for dri in drivers]) for dr in drivers] for et in range(etape)])
plt.gca().invert_yaxis()
handl=riders+patches
labl=[dr for dr in drivers]+patchnames
plt.legend(handles=handl,labels=labl)
plt.savefig('tdf2018.png',dpi='figure', bbox_inches='tight')
plt.show()
