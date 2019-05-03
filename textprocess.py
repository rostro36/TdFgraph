import re
import data


def check(page):
    return (len(re.findall(r'<tbody>', page)) >= 3)


def process(page):
    #split the report of the whole day to the different sections
    classements = re.split(r'<tbody>', page)[2:]
    if data.etape == 1:
        [gc, points, gcequipe] = classements
    else:
        [gc, points, kom, gcequipe] = classements
    procGC(gc)
    procPoints(points)
    if data.etape != 1:
        procKOM(kom)
    procGCEquipe(gcequipe)


def procGC(gc):
    #<tr data-id="1423" data-nation="pl"><td  >2</th><td  ><span style="font-size: 10px; color: #777; ">2</span></th><td  >-</th><td   class="xhide" data-name="bib" >145</th><td  ><span class="flags pl"></span> <a href="rider/michal-kwiatkowski"><span class="uppercase"> Kwiatkowski</span> Michał</a></th><td   class="xhide" data-name="age" >28</th><td  ><a href="team/team-sky-2018">Team Sky</a></th><td  ></th><td style=" text-align: right; "  class="xhide" data-name="gc" >2</th><td style=" text-align: right; "  class="xhide" data-name="gc" >+0:41</th><td style=" text-align: right; " ><span class="timelag">0:41</span> <span class="time ">0:41</span></th><td style=" text-align: right; "  class="xhide" data-name="time_wl" ><a class="gaps GapsFromRider " data-gap="14315" data-np="0" href="">+0:00</a></th></tr>

    gcPedaleurs = re.split(r'class="xhide" data-name="bib" >', gc)[1:-1]
    for pedaleur in gcPedaleurs:
        NUMBER = getNumber(pedaleur)
        if data.pedaleurs[NUMBER][0] is None:
            initPedaleur(NUMBER, pedaleur)
        #go to the time '\' to escape '+'
        pedaleur = re.split(r'data-name="gc" >\+', pedaleur, 1)[1]
        TIME = getTime(pedaleur)
        data.ecarts[data.etape][NUMBER] = (TIME, data.rankg)
        data.rankg += 1


def procPoints(points):
    #<tr data-id="1423" data-nation="pl"><td  >1</th><td  ><span style="font-size: 10px; color: #777; ">1</span></th><td  >-</th><td   class="xhide" data-name="bib" >145</th><td  ><span class="flags pl"></span> <a href="rider/michal-kwiatkowski"><span class="uppercase"> Kwiatkowski</span> Michał</a></th><td   class="xhide" data-name="age" >28</th><td  ><a href="team/team-sky-2018">Team Sky</a></th><td  >48</th></tr>
    pointsPedaleurs = re.split(r'class="xhide" data-name="bib" >',
                               points)[1:-1]
    for pedaleur in pointsPedaleurs:
        NUMBER = getNumber(pedaleur)
        #get to points
        pedaleur = re.split(r'</a></th><td  >', pedaleur, 1)[1]
        POINTS = getNumber(pedaleur)
        data.points[data.etape][NUMBER] = (POINTS, data.rankp)
        data.rankp += 1


def procKOM(kom):
    #<tr data-id="1136" data-nation="es"><td  >1</th><td  ><span style="font-size: 10px; color: #777; ">1</span></th><td  >-</th><td   class="xhide" data-name="bib" >206</th><td  ><span class="flags es"></span> <a href="rider/luis-angel-mate"><span class="uppercase"> Maté</span> Luis Ángel</a></th><td   class="xhide" data-name="age" >34</th><td  ><a href="team/cofidis-solutions-credits-2018">Cofidis, Solutions Crédits</a></th><td  >42</th></tr>

    komPedaleurs = re.split(r'class="xhide" data-name="bib" >', kom)[1:-1]
    for pedaleur in komPedaleurs:
        NUMBER = getNumber(pedaleur)
        #get to KOM points
        pedaleur = re.split(r'</a></th><td  >', pedaleur, 1)[1]
        KOM = getNumber(pedaleur)
        data.grimpeurs[data.etape][NUMBER] = (KOM, data.rankgr)
        data.rankgr += 1


def procGCEquipe(gcequipe):
    #<tr data-id="1375" data-nation="kz"><td  >1</th><td  ><span style="font-size: 10px; color: #777; ">1</span></th><td  >-</th><td   class="xhide" data-name="bib" ></th><td  ><span class="flags kz"></span> <a href="team/astana-pro-team-2018">Astana Pro Team</a></th><td style=" text-align: right; "  class="xhide" data-name="gc" ></th><td style=" text-align: right; "  class="xhide" data-name="gc" >+ - 22:26:15</th><td style=" text-align: right; " ><span class="timelag"> 67:17:18</span> <span class="time "> 67:17:18</span></th></tr>
    #<tr data-id="1330" data-nation="nl"><td  >2</th><td  ><span style="font-size: 10px; color: #777; ">2</span></th><td  >-</th><td   class="xhide" data-name="bib" ></th><td  ><span class="flags nl"></span> <a href="team/team-lottonl-jumbo-2018">Team LottoNL-Jumbo</a></th><td style=" text-align: right; "  class="xhide" data-name="gc" ></th><td style=" text-align: right; "  class="xhide" data-name="gc" >+ - 22:26:15</th><td style=" text-align: right; " ><span class="timelag">3:04</span> <span class="time ">3:04</span></th></tr>

    gcEQ = re.split(r'a href="team/', gcequipe)[1:]
    for equipe in gcEQ:
        #get to Team
        equipe = re.split(r'">', equipe, 1)[1]
        EQUIPE = getName(equipe)
        if data.ranke == 1:
            TIME = 0
        else:
            equipe = re.split(r'<span class="time ">', equipe, 1)[1]
            TIME = getTime(equipe)
        data.eq[data.etape][EQUIPE] = (data.ranke, TIME)
        data.ranke += 1


def initPedaleur(NUMBER, pedaleur):
    #(NOM,PRENOM,JEUNE,NATION,EQUIPE,int(nombre))
    #jump to nation
    pedaleur = re.split(r'<span class="flags ', pedaleur, 1)[1]
    NATION = pedaleur[:2]
    #go further to name
    pedaleur = re.split(r'class="uppercase">', pedaleur, 1)[1]
    NOM = getName(pedaleur)
    #go to PRENOM
    skip = len(NOM) + 8
    pedaleur = pedaleur[skip:]
    PRENOM = getName(pedaleur)
    #go to EQUIPE
    pedaleur = re.split('">', pedaleur, 1)[1]
    EQUIPE = getName(pedaleur)

    data.pedaleurs[NUMBER] = (NOM, PRENOM, None, NATION, EQUIPE, NUMBER)


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
