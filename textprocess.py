import re

#def check(page):
#    return (len(re.findall(r'<tbody>', page)) >= 3)


def process(page, etape):
    #split the report of the whole day to the different sections
    classements = re.split(r'<tbody>', page)[1:]
    if etape == 1:
        [gc, points, gcequipe] = classements
    else:
        [gc, points, kom, gcequipe] = classements
    gcClassement = procGC(gc)
    pointsClassement = procPoints(points)
    equipeClassement = procGCEquipe(gcequipe)
    if etape != 1:
        komClassement = procKOM(kom)
    else:
        komClassement = []
    return (gcClassement, pointsClassement, equipeClassement, komClassement)


def procGC(gc):
    rankg = 1
    ecarts = dict()
    gcPedaleurs = re.split(r'<td  class="hide"   data-name="gc"  >\+', gc)[1:]
    #(ecarts, gcPedaleurs) = setupContainer(gc)
    for pedaleur in gcPedaleurs:
        TIME = getTime(pedaleur)
        pedaleur = re.split(r'class="hide"   data-name="bib"  >', pedaleur,
                            1)[1]
        NUMBER = getNumber(pedaleur)
        ecarts[NUMBER] = (TIME, rankg)
        rankg += 1
    return ecarts


def procPoints(points):
    rankp = 1
    (points, pointsPedaleurs) = setupContainer(points)
    for pedaleur in pointsPedaleurs:
        NUMBER = getNumber(pedaleur)
        #get to points
        pedaleur = re.split(r'/a></th><td   >', pedaleur, 1)[1]
        POINTS = getNumber(pedaleur)
        points[NUMBER] = (POINTS, rankp)
        rankp += 1
    return points


def procKOM(kom):
    rankgr = 1
    (grimpeurs, komPedaleurs) = setupContainer(kom)
    for pedaleur in komPedaleurs:
        NUMBER = getNumber(pedaleur)
        #get to KOM points
        pedaleur = re.split(r'</a></th><td   >', pedaleur, 1)[1]
        KOM = getNumber(pedaleur)
        grimpeurs[NUMBER] = (KOM, rankgr)
        rankgr += 1
    return grimpeurs


def procGCEquipe(gcequipe):
    ranke = 1
    gcEQ = re.split(r'a href="team/', gcequipe)[1:]
    eq = dict()
    for equipe in gcEQ:
        #get to Team
        equipe = re.split(r'">', equipe, 1)[1]
        EQUIPE = getName(equipe)
        if ranke == 1:
            TIME = 0
        else:
            equipe = re.split(r'class="timeff">', equipe, 1)[1]
            TIME = getTime(equipe)
        eq[EQUIPE] = (ranke, TIME)
        ranke += 1
    return eq


def getNumber(pedaleur):
    nombre = ''
    while len(pedaleur) > 0 and pedaleur[0].isdigit():
        nombre += pedaleur[0]
        pedaleur = pedaleur[1:]
    return int(nombre)


def getName(pedaleur):
    NAME = ''
    while pedaleur[0] != '<':
        #special case if namestring starts with a space
        if pedaleur[0] != ' ' or len(NAME) != 0:
            NAME += pedaleur[0]
        pedaleur = pedaleur[1:]
    #delete trailing spaces
    return NAME.rstrip()


def getTime(timeString):
    TIME = 0
    #SUBTIME is the time in the same messure e.g a '1' and a '2' part for 12 seconds
    SUBTIME = 0
    for c in timeString:
        if c == ':':
            TIME = (TIME + SUBTIME) * 60
            SUBTIME = 0
        elif c == '<':
            break
        elif c == ' ':
            pass
        else:
            SUBTIME = SUBTIME * 10 + int(c)
    return TIME + SUBTIME


def setupContainer(allPedaleurs):
    separatedPedaleurs = re.split(r'class="hide"   data-name="bib"  >',
                                  allPedaleurs)[1:]
    container = dict()
    return (container, separatedPedaleurs)
