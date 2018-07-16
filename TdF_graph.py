
# coding: utf-8

# In[39]:


#libs used
import PyPDF2 as pypdf
import urllib3
import matplotlib.pyplot as plt
import io
import re
#globals
http = urllib3.PoolManager()
pedaleurs=[(None,None,None,None,None,None)]*220 #(NOM,PRENOM,JEUNE,NATION,EQUIPE,int(nombre))
ecarts=[None]*23
points=[None]*23
grimpeurs=[None]*23
jeunes=[None]*23
eq=[dict()]*23


def general_proc(string):                       #general classement
    global rankg                                #ecarts[etape][nombre]=(ecart,rank)    
    global ecart
    global pedaleurs
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
        jeunes[etape]=[None]*220
        for pedaleur in entries:                    #process each rider
            jeunes_proc(pedaleur)
    elif ('CLASSEMENT PAR POINTS'==page[:len('CLASSEMENT PAR POINTS')]):
        page=re.sub('.*PrénomEquipePointsNatNat','',page)#cut the start
        page=re.split('Page',page)[0]                    #cut the end
        page=re.split(' km',page,1)[0]
        entries=re.split(' \d* ',page)               #split the riders
        entries=entries[1:]                          #first is garbage
        points[etape]=[(None,None)]*220
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
        grimpeurs[etape]=[(None,None)]*220
        for pedaleur in entries:                        #process each rider
            grimpeurs_proc(pedaleur)
    elif ('CLASSEMENT GENERAL ETAPE ' in page):
        page=re.sub('.*PrénomEq.NatTempsEcart','',page) #cut the start
        page=re.split('Page',page,1)[0]                 #cut the end
        entries=re.split(' \d* ',page)                  #split the riders
        entries=entries[1:]                             #first is garbage
        ecarts[etape]=[(None,None)]*220
        for pedaleur in entries:                        #process each rider
            general_proc(pedaleur)
       
 #gather the data
for etape in range(1,22):
    rankg=1
    rankj=1
    rankgr=1
    rankp=1
    etapestring=str(etape).zfill(2)
    print('working on stage:'+etapestring)
    URL = 'http://azure.tissottiming.com/File/00031001070101'+etapestring+'FFFFFFFFFFFFFF00'
    #download the data
    r = http.request('GET',URL)
    #check if press-release is ready/a PDF
    if r.info()['Content-type']!='application/pdf':
        print (etapestring+' not ready')
        break
    #open the file
    read_pdf = pypdf.PdfFileReader(io.BytesIO(r.data))
    #process each page
    for pagenum in range(read_pdf.getNumPages()):
        process(read_pdf.getPage(pagenum).extractText())
    print(etapestring+' is processed')
print('all done')


# In[18]:


plt.plot([1, 2, 3, 4],[[1,2,3],[12,2,4],[2,None,1],[8,5,4]])
plt.show()


# In[17]:





# In[36]:





# In[38]:




