# coding: utf-8
#libs used
from textprocess import process
from graph import plot
from setupAndDownload import download, upload, getProfile, getTeamnames, getPedaleurs
import os
import sys

#gather the data
race = sys.argv[1]
year = sys.argv[2]
raceString = 'race/' + race + '/' + year + '/'
URLBase = 'https://www.procyclingstats.com/'
URL = URLBase + raceString

folderName = os.path.basename(raceString.replace("/", "@"))
if not os.path.exists(folderName):
    os.makedirs(folderName)

(stageProfile, stageNames) = getProfile(URL)
fileName = os.path.join(folderName, 'stageProfile')
if not os.path.isfile(fileName):
    with open(fileName, 'w', encoding='utf-8') as file:
        file.write(str(stageProfile))

fileName = os.path.join(folderName, 'teamAbbrevations')
if not os.path.isfile(fileName):
    teamAbbrevations = getTeamnames(URL)
    with open(fileName, 'w', encoding='utf-8') as file:
        file.write(str(teamAbbrevations))

fileName = os.path.join(folderName, 'pedaleurs')
if not os.path.isfile(fileName):
    pedaleurs = getPedaleurs(URL)
    with open(fileName, 'w', encoding='utf-8') as file:
        file.write(str(pedaleurs))

stageNumber = 0
for stage in stageNames:
    fileName = os.path.join(folderName,
                            stage.replace("/", "@") + '%' + str(stageNumber))
    if not os.path.isfile(fileName):
        print('creating stage:' + str(stage))
        stageURL = URLBase + str(stage)
        page = download(stageURL)
        #DEBUG with open(fileName + 'test', 'w', encoding='utf-8') as file:
        #DEBUG    file.write(page)
        stageResults = process(page)
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(str(stageResults))
    stageNumber = stageNumber + 1
    print(str(stage) + ' is processed')
print('processing done')

imageName = plot(stageNumber, race, year)
print('Your image is uploaded at: ' + str(upload(imageName)))
