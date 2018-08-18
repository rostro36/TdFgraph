import re
import data


#since we write and it changes all the time, at least for some of them.
def general_proc(string):  #general classement
    #data.ecarts[etape][nombre]=(ecart,rank)
    global ecart
    helpr = ''
    for k in range(len(string)):  #take away all till the start of the number
        if not string[k].isupper():
            helpr += (string[k])
        else:
            break
    #seperate number from the distance
    if helpr[-1] == '"':  #there is an actual distance in seconds
        ecart = 0
        ecart += int(helpr[-2])
        ecart += int(helpr[-3]) * 10
        if helpr[-4] == '\'':  #there are minutes
            ecart += int(helpr[-5]) * 60
            ecart += int(helpr[-6]) * 600
            if helpr[-7] == 'h':  #there are hours
                ecart += int(helpr[-8]) * 60 * 60
                nombre = helpr[:-8]  #get the numbers
            else:
                nombre = helpr[:-6]
        else:
            nombre = helpr[:-3]
    else:
        nombre = ''  #same as above pedaleur
        for char in helpr:  #get just the name
            if char.isdigit():
                nombre += char
            else:
                break
    data.ecarts[data.etape][int(nombre)] = (ecart, data.rankg)
    data.rankg += 1
    #fill up the data.pedaleurs
    if data.pedaleurs[int(nombre)] == (
            None, None, None, None, None,
            None):  #pedaleur not added         ######change done
        EQUIPE = string[k:k +
                        3]  #both EQUIPE and NATION are both 3 catpital letters
        NATION = string[k + 3:k + 6]
        for q in range(k + 6, len(string)):  #find start of second name
            if string[q].isupper():
                break
        JEUNE = string[q - 1] == '*'  #check if the driver is a young rider
        for p in range(q, len(string)):
            if string[p].islower():  #the second letter of the first name is low
                p -= 1
                break
        NOM = string[q:p - 1]  #string[p] is always a whitespace
        PRENOM = string[p:]
        data.pedaleurs[int(nombre)] = (NOM, PRENOM, JEUNE, NATION, EQUIPE,
                                       int(nombre))


def point_proc(string):  #point classement
    #points[etape][nombre]=(poi,rank)
    nombre = ''
    poi = ''
    for i in range(len(string)):
        if string[i].isdigit():  #get number
            nombre += string[i]
        elif len(nombre) > 0:  #check if already written to number
            break
    for q in range(i, len(string)):  #get points start
        if string[q].isdigit():
            break
    string += 'buffer'  #need buffer if number is at the end
    for p in range(q, len(string)):  #get points end
        if not string[p].isdigit():
            break
    nombre = int(nombre)
    poi = int(string[q:p])
    data.points[data.etape][nombre] = (poi, data.rankp)
    data.rankp += 1


def grimpeurs_proc(string):  #mountain classement
    #grimpeurs[etape][nombre]=(grim,rank)
    nombre = ''
    grim = ''
    for i in range(len(string)):
        if string[i].isdigit():  #get number
            nombre += string[i]
        elif len(nombre) > 0:  #check if already written to number
            break
    for q in range(i, len(string)):  #get mountain points start
        if string[q].isdigit():
            break
    for p in range(q, len(string)):  #get mountain points end
        if string[p].isupper():
            break
    nombre = int(nombre)
    grim = int(string[q:p])
    data.grimpeurs[data.etape][nombre] = (grim, data.rankgr)
    data.rankgr += 1


def jeunes_proc(string):  #young classement
    #jeunes[etape][int(nombre)]=(rank) (you have to crossreverence it with the general classement)
    nombre = ''
    for i in range(len(string)):  #find the number
        if string[i].isdigit():
            nombre += string[i]
        elif len(nombre) > 0:  #check if already written to number
            break
    data.jeunes[data.etape][int(nombre)] = (data.rankj)
    data.rankj += 1


def process(page):
    if ('CLASSEMENT DES JEUNES' == page[:len('CLASSEMENT DES JEUNES')]):
        page = re.split('Page', page, 1)[0]  #cut the end
        if len(re.findall('DosNom',
                          page)) == 2:  #check if there is a daily classement
            page = re.sub('.*NatTempsEcart', '', page)  #cut the start
            page = re.sub('.* 1 ', ' ', page, 1)
        elif len(re.findall('DosNom', page)) > 2:
            print(page)
            print('problem jeunes')
        page = re.sub('.* 1 ', '1', page)  #cut the start again
        entries = re.split(' \d* ', page)  #split the riders
        for pedaleur in entries:  #process each rider
            jeunes_proc(pedaleur)
    elif ('CLASSEMENT PAR POINTS' == page[:len('CLASSEMENT PAR POINTS')]):
        page = re.sub('.*PrénomEquipePointsNatNat', '', page)  #cut the start
        #print('pageb',page)
        page = re.split('Page', page)[0]  #cut the end
        #print('pagea',page)
        page = re.split('Arrivée', page)[0]
        page = re.split(' km', page, 1)[0]
        entries = re.split(' \d* ', page)  #split the riders
        entries = entries[1:]  #first is garbage
        for pedaleur in entries:  #process each rider
            point_proc(pedaleur)
    elif ('CLASSEMENT PAR EQUIPES' == page[:len('CLASSEMENT PAR EQUIPES')]
         ):  #data.eq[etape][equipenom]=(data.ranke,ecart)
        page = re.sub('.*\s1(?P<first>[A-Z])', '\g<first>', page, 0,
                      re.DOTALL)  #cut the start
        page = re.split('Page', page, 1)[0]  #cut the end
        page = re.split('\s[0-9]+', page)  #split the equipes
        data.ranke = 1
        for equipe in page:
            for i in range(len(equipe)):
                if (equipe[i].isdigit() and
                    (equipe[i + 1] == 'h' or
                     equipe[i + 1].isdigit())) or equipe[i] == '\'':
                    break
            equipenom = equipe[:i]
            if equipe[i] == '\'':  #equipe has the same distance as above
                data.eq[data.etape][equipenom] = (data.ranke, ecart)
                data.ranke += 1
                continue
            else:
                ecart = 0
            if equipe[i + 1] == 'h':  #get distance
                ecart += int(equipe[i]) * 60 * 60
                i += 2
            if equipe[i + 2] == '\'':
                ecart += int(equipe[i]) * 60 * 10
                ecart += int(equipe[i + 1]) * 60
                i += 3
            if equipe[i + 2] == '"':
                ecart += int(equipe[i]) * 10
                ecart += int(equipe[i + 1])
            data.eq[data.etape][equipenom] = (data.ranke, ecart)
            data.ranke += 1
    elif ('CLASSEMENT DU MEILLEUR GRIMPEUR' == page[:len(
            'CLASSEMENT DU MEILLEUR GRIMPEUR')]):
        page = re.sub('.*PrénomEquipePointsNatNat', '', page)  #cut the start
        page = re.split('Page', page)[0]  #cut the end
        page = re.split(' km', page, 1)[0]
        entries = re.split(' \d* ', page)  #split the riders
        entries = entries[1:]  #first is garbage
        for pedaleur in entries:  #process each rider
            grimpeurs_proc(pedaleur)
    elif ('CLASSEMENT GENERAL ETAPE ' in page):
        page = re.sub('.*PrénomEq.NatTempsEcart', '', page)  #cut the start
        page = re.split('Page', page, 1)[0]  #cut the end
        entries = re.split(' \d* ', page)  #split the riders
        entries = entries[1:]  #first is garbage
        for pedaleur in entries:  #process each rider
            general_proc(pedaleur)