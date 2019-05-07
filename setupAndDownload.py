import urllib3
import re
from textprocess import getName, getNumber

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)  #we do not check the certs of the resultssite, because it is not important enouogh for such a project.

http = urllib3.PoolManager()


def download(URL):
    try:
        r = http.request('GET', URL)  #get the actual site
    except Exception as ex:
        print(ex)
        print('Internet not working.')
        quit()
    page = r.data.decode('UTF-8')
    return page


def getProfile(URL):
    profileURL = URL + 'gc/stages/winners'
    page = download(profileURL)
    stageProfile = [[] for i in range(6)]
    sections = re.split(r'icon profile p', page)[1:]
    for i in range(len(sections)):
        steepness = int(sections[i][0])
        stageProfile[steepness].append(i)

        #test if Timetrial
        testTT = re.split(r' - ', sections[i])[0]
        if testTT[-1] == ')':
            stageProfile[0].append(i)
    return (stageProfile)


def getStageReadiness(URL):
    stagesURL = URL + 'gc/stages/leaders-overview'
    page = download(stagesURL)
    stages = re.split(r'<tr class=""><td class=" " >', page)[1:]
    numberOfStages = len(stages)
    # GC Points KOM Youth Teams
    FLAGS = [0, 0, 0, 0, 0]
    for stageNumber in range(len(stages)):
        testStage = stages[stageNumber]
        for i in range(len(FLAGS)):
            if i < 4:
                testStage = re.split(r'href="rider/', testStage, 1)[1]
            else:
                testStage = re.split(r'href="team/', testStage, 1)[1]
            if not testStage[0] == '"' and (FLAGS[i] == stageNumber
                                            or FLAGS[i] == 0):
                #do not start at 0
                FLAGS[i] = stageNumber + 1
            #pedaleur = re.split(r'data-name="gc" >\+', pedaleur, 1)[1]
    return (FLAGS, numberOfStages)


def getTeamnames(URL):
    teamDict = dict()
    rankingURL = URL + 'gc/startlist/teams-ranked'
    page = download(rankingURL)
    teamEntries = re.split(r'a  href="', page)[1:]
    for teamEntry in teamEntries:
        teamURL = 'https://www.procyclingstats.com/' + re.split(
            r'"', teamEntry, 1)[0]
        teamPage = download(teamURL)
        (namePart, abbrevationPart) = re.split(r'Abbreviation: </b>', teamPage,
                                               1)
        teamAbbrevation = abbrevationPart[:3]
        namePart = re.split(r'></span><h1>', namePart, 1)[1]
        teamName = re.split(r'  ', namePart, 1)[0]
        teamDict[teamName] = teamAbbrevation
    return teamDict


def getPedaleurs(URL):
    pedaleurURL = URL + 'stage-1/startlist'
    page = download(pedaleurURL)
    #<a href="team/bahrain-merida-pro-cycling-team-2018">Bahrain Merida Pro Cycling Team</a></h4><a href="team/bahrain-merida-pro-cycling-team-2018"><img src="../images/shirts/bx/eb/bahrain-merida-pro-cycling-team-2018-n2.png" /></a><div class="riders" style=" "><span style="display: inline-block; width: 27px; ">1</span><span class="flag it"></span> <a class="rider blue " href="rider/vincenzo-nibali"><span class=""><span>NIBALI</span> Vincenzo</span></a><br /><span style="display: inline-block; width: 27px; ">2</span><span class="flag es"></span> <a class="rider blue " href="rider/ivan-garcia-cortina"><span class=""><span>GARCÍA CORTINA</span> Iván</span></a><br /><span style="display: inline-block; width: 27px; ">3</span><span class="flag es"></span> <a class="rider blue " href="rider/gorka-izagirre"><span class=""><span>IZAGIRRE</span> Gorka</span></a><br /><span style="display: inline-block; width: 27px; ">4</span><span class="flag es"></span> <a class="rider blue " href="rider/ion-izagirre"><span class=""><span>IZAGIRRE</span> Ion</span></a><br /><span style="display: inline-block; width: 27px; ">5</span><span class="flag ua"></span> <a class="rider blue " href="rider/mark-padun"><span class=""><span>PADUN</span> Mark</span></a><br /><span style="display: inline-block; width: 27px; ">6</span><span class="flag it"></span> <a class="rider blue " href="rider/franco-pellizotti"><span class=""><span>PELLIZOTTI</span> Franco</span></a><br /><span style="display: inline-block; width: 27px; ">7</span><span class="flag at"></span> <a class="rider blue " href="rider/hermann-pernsteiner"><span class=""><span>PERNSTEINER</span> Hermann</span></a><br /><span style="display: inline-block; width: 27px; ">8</span><span class="flag si"></span> <a class="rider blue " href="rider/luka-pibernik"><span class=""><span>PIBERNIK</span> Luka</span></a><br /></div></li><li class="team" ><h4>2. <span class="icon tick2 "></span>
    allTeams = re.split(r' <a href="team/', page)[1:]
    pedaleurInfo = dict()
    for team in allTeams:
        team = re.split(r'>', team, 1)[1]
        EQUIPE = getName(team)
        pedaleurs = re.split(r'width: 27px; ">', team)[1:]
        #(NOM,PRENOM,JEUNE,NATION,EQUIPE,int(nombre))
        #jump to nation
        for pedaleur in pedaleurs:
            NUMBER = getNumber(pedaleur)
            pedaleur = re.split(r'<span class="flag ', pedaleur, 1)[1]
            NATION = pedaleur[:2]
            #go further to name
            pedaleur = re.split(r'><span class=""><span>', pedaleur, 1)[1]
            NOM = getName(pedaleur)
            #go to PRENOM
            pedaleur = re.split(r'</span> ', pedaleur, 1)[1]
            PRENOM = getName(pedaleur)

            pedaleurInfo[NUMBER] = (NOM, PRENOM, NATION, EQUIPE, NUMBER)
    return pedaleurInfo
