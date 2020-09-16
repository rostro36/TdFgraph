import re
import sys


def process(page):
    #split the report of the whole day to the different sections
    resultFlags = checkCategories(page)
    classements = re.split(r'<tbody><tr data-id="+[0-9]', page)[1:]
    resultObject = dict()
    procFunctions = {
        "GC": procGC,
        "Points": procPoints,
        "Youth": procYouth,
        "KOM": procKOM,
        "Teams": procGCEquipe
    }
    TTTFlag = re.search(r'\(TTT\) \| Results</title>', page) is None
    for name in resultFlags:
        if name[:5] == 'Stage':
            if TTTFlag:
                classements.pop(0)
        else:
            resultObject[name] = procFunctions[name](classements.pop(0))
    return resultObject


def checkCategories(page):
    possibleFlags = {
        "GC": '"st4"',
        "Points": '"st5"',
        "Youth": '"st6"',
        "KOM": '"st7"',
        "Teams": '"st10"',
        "Stage3": '"st3"',
        "Stage1": '"st1"',
        "Stage2": '"st2"'
    }
    if re.search(r'<tbody>', page) is None:
        print('This etape is not ready.')
        quit()
    resultFlags = []
    for name in possibleFlags.keys():
        match = re.search(possibleFlags[name], page)
        if match is not None:
            resultFlags.append((match, name))
    resultFlags.sort(key=lambda obj: obj[0].start())
    resultFlags = [names for (matches, names) in resultFlags]
    return resultFlags


def procGC(gc):
    rankg = 1
    ecarts = dict()
    gcPedaleurs = re.split(r'<td  class="hide"   data-name="bib"  >', gc)[1:]
    for pedaleur in gcPedaleurs:
        NUMBER = getNumber(pedaleur)
        if NUMBER is None:
            continue
        pedaleur = re.split(r'<span class="timeff">', pedaleur, 1)[1]
        if rankg == 1:
            TIME = 0
        else:
            TimeNew = getTime(pedaleur)
            if TimeNew != -1:
                TIME = TimeNew
        ecarts[NUMBER] = (TIME, rankg)
        rankg += 1
    return ecarts


def procPoints(points):
    #with open('points_testpage', 'w', encoding='utf-8') as file:
        #    file.write(points)    
    rankp = 1
    (points, pointsPedaleurs) = setupContainer(points)
    for pedaleur in pointsPedaleurs:
        NUMBER = getNumber(pedaleur)
        if NUMBER is None:
            continue
        #check if UCI points are also inside
        pedaleur = re.split(r'</th></tr>', pedaleur, 1)[0]
        pedaleur = re.split(r'</a></th><td   >', pedaleur,1)[-1]
        POINTSlist=[]
        POINTSlist.append(getNumber(pedaleur))
        while '</th><td   >' in pedaleur:
            pedaleur = re.split(r'</th><td   >', pedaleur,1)[-1]
            POINTSlist.append(getNumber(pedaleur))
        POINTS= POINTSlist[int(len(POINTSlist)/2)]
        points[NUMBER] = (POINTS, rankp)
        rankp += 1
    return points


def procKOM(kom):
    #with open('kom_testpage', 'w', encoding='utf-8') as file:
    #    file.write(kom)    
    rankgr = 1
    (grimpeurs, komPedaleurs) = setupContainer(kom)
    for pedaleur in komPedaleurs:
        NUMBER = getNumber(pedaleur)
        if NUMBER is None:
            continue
        #get to KOM points
        pedaleur = re.split(r'</th></tr>', pedaleur, 1)[0]
        pedaleur = re.split(r'</a></th><td   >', pedaleur,1)[-1]
        KOMlist=[]
        KOMlist.append(getNumber(pedaleur))
        while '</th><td   >' in pedaleur:
            pedaleur = re.split(r'</th><td   >', pedaleur,1)[-1]
            KOMlist.append(getNumber(pedaleur))
        KOM=KOMlist[int(len(KOMlist)/2)]
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
            TimeNew = getTime(equipe)
            if TimeNew != -1:
                TIME = TimeNew
        eq[EQUIPE] = (TIME, ranke)
        ranke += 1
    return eq


def procYouth(youth):
    ranky = 1
    (youths, youthEntries) = setupContainer(youth)
    for pedaleur in youthEntries:
        NUMBER = getNumber(pedaleur)
        if NUMBER is None:
            continue
        if ranky == 1:
            TIME = 0
        else:
            pedaleur = re.split(r'class="timeff">', pedaleur)[1]
            TIME = getTime(pedaleur)
        youths[NUMBER] = (TIME, ranky)
        ranky += 1
    return youths


def getNumber(pedaleur):
    nombre = ''
    while len(pedaleur) > 0 and pedaleur[0].isdigit():
        nombre += pedaleur[0]
        pedaleur = pedaleur[1:]
    if nombre == '':
        return None
    return int(nombre)


def getName(pedaleur):
    NAME = ''
    while pedaleur[0] != '<' and pedaleur[0] != '&':
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
        elif c == ',':
            return -1
        elif c == '-':
            return sys.maxsize
        else:
            SUBTIME = SUBTIME * 10 + int(c)
    return TIME + SUBTIME


def setupContainer(allPedaleurs):
    separatedPedaleurs = re.split(r'class="hide"   data-name="bib"  >',
                                  allPedaleurs)[1:]
    container = dict()
    return (container, separatedPedaleurs)
    