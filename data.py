pedaleurs = [(None, None, None, None, None, None)
             ] * 220  #(NOM,PRENOM,JEUNE,NATION,EQUIPE,int(nombre))
ecarts = [None] * 23
points = [None] * 23
grimpeurs = [None] * 23
jeunes = [None] * 23
eq = [None] * 23
ecarts[0] = [(0, 0)] * 220
grimpeurs[0] = [(0, 200)] * 220
points[0] = [(0, 200)] * 220
jeunes[0] = [0] * 220
etape = 0
rankg = 1
rankj = 1
rankgr = 1
rankp = 1
ranke = 1
#type of track
plat = [6, 10, 18, 21]
acci = [2, 3, 7, 8, 12]
#harder than acci
intermediate = [5, 11, 17]
montagne = [4, 9, 13, 14, 15, 19, 20]
clm = [1, 16]

STAGES = 23  #number of stages

abbrevations = dict()
abbrevations['Astana Pro Team'] = 'AST'
abbrevations['Team LottoNL-Jumbo'] = 'TLJ'
abbrevations['Movistar Team'] = 'MOV'
abbrevations['Team EF Education First-Drapac p/b Cannondale'] = 'EFD'
abbrevations['BORA - hansgrohe'] = 'BOH'
abbrevations['Bahrain Merida Pro Cycling Team'] = 'TBM'
abbrevations['Team Dimension Data'] = 'DDD'
abbrevations['Team Sky'] = 'SKY'
abbrevations['UAE-Team Emirates'] = 'UAD'
abbrevations['AG2R La Mondiale'] = 'ALM'
abbrevations['Cofidis, Solutions Crédits'] = 'COF'
abbrevations['Euskadi - Murias'] = 'EUS'
abbrevations['Mitchelton-Scott'] = 'MTS'
abbrevations['Groupama - FDJ'] = 'FDJ'
abbrevations['Quick-Step Floors'] = 'QST'
abbrevations['BMC Racing Team'] = 'BMC'
abbrevations['Trek - Segafredo'] = 'TFS'
abbrevations['Lotto Soudal'] = 'LTS'
abbrevations['Team Katusha - Alpecin'] = 'TKA'
abbrevations['Caja Rural - Seguros RGA'] = 'CJR'
abbrevations['Team Sunweb'] = 'SUN'
abbrevations['Burgos-BH'] = 'BBH'


def newstage(etape1):
    global rankg
    global rankj
    global rankgr
    global rankp
    global etape
    global ranke
    etape = etape1
    rankg = 1
    rankj = 1
    rankgr = 1
    rankp = 1
    ranke = 1
    ecarts[etape] = [(None, None)] * 220
    grimpeurs[etape] = [(0, 200)] * 220
    points[etape] = [(0, 200)] * 220
    jeunes[etape] = [None] * 220
    eq[etape] = dict()
