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
etape=0
rankg=1
rankj=1
rankgr=1
rankp=1

def newstage(etape1):
    global rankg
    global rankj
    global rankgr
    global rankp
    global etape
    etape=etape1
    rankg=1
    rankj=1
    rankgr=1
    rankp=1
    ecarts[etape]=[(None,None)]*220
    grimpeurs[etape]=[(0,200)]*220
    points[etape]=[(0,200)]*220
    jeunes[etape]=[None]*220
    eq[etape]=dict()
