import urllib3
import requests
import base64
import json
import re
from textprocess import getName, getNumber

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)  #we do not check the certs of the resultssite, because it is not important enouogh for such a project.

http = urllib3.PoolManager()


def upload(imageName):
    try:
        f = open(imageName,
                 "rb")  # open our image file as read only in binary mode
    except Exception as ex:
        print(ex)
        print('It seems as if your image to be uploaded is not ready.')
        quit()
    image_data = f.read()
    b64_image = base64.standard_b64encode(image_data)
    url = 'https://api.imgur.com/3/image'
    payload = {'image': b64_image}
    #payload = json.dumps(payload).encode('utf-8')
    headers = {'Authorization': 'Client-ID bb79416fdaad09a'}
    try:
        response = http.request('POST',
                                url,
                                headers=headers,
                                fields=payload,
                                retries=False)
    except Exception as ex:
        print(ex)
        print('Imgur could not be reached. Check your Internet.')
        quit()

    responseJSON = json.loads(response.data)
    return responseJSON["data"]["link"]


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
    if 'Could not find race' in page:
        raise Exception(URL +
                        ' does not exist, please check your input arguments.')
        quit()

    stageProfile = [[] for i in range(6)]
    stageNames = []
    sections = re.split(r'icon profile p', page)[1:]
    for i in range(len(sections)):
        steepness = int(sections[i][0])
        stageProfile[steepness].append(i)

        #test if Timetrial
        testPart = re.split(r' - ', sections[i])[0]
        if testPart[-1] == ')':
            stageProfile[0].append(i)

        testPart = re.split(r'<a  href="', testPart)[1]
        stageName = re.split(r'"', testPart)[0]
        stageNames.append(stageName)
    return (stageProfile, stageNames)


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

    allTeams = re.split(r' <a href="team/', page)[1:]
    pedaleurInfo = dict()

    for team in allTeams:
        team = re.split(r'>', team, 1)[1]
        EQUIPE = getName(team)

        pedaleurs = re.split(r'width: 27px; ">', team)[1:]
        for pedaleur in pedaleurs:
            NUMBER = getNumber(pedaleur)

            pedaleur = re.split(r'<span class="flag ', pedaleur, 1)[1]
            NATION = pedaleur[:2]

            pedaleur = re.split(r'><span class=""><span>', pedaleur, 1)[1]
            NOM = getName(pedaleur)

            pedaleur = re.split(r'</span> ', pedaleur, 1)[1]
            PRENOM = getName(pedaleur)

            pedaleurInfo[NUMBER] = (NOM, PRENOM, NATION, EQUIPE, NUMBER)
    return pedaleurInfo
