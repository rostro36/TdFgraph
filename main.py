# coding: utf-8
#libs used
from textprocess import process
#from data import newstage
from graph import plot
from setupAndDownload import download, getProfile, getTeamnames, getPedaleurs
import os
#import traceback
#import data

#gather the data

raceString = 'race/vuelta-a-espana/2018/'
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

for stage in stageNames:
    fileName = os.path.join(folderName, stage.replace("/", "@"))
    if not os.path.isfile(fileName):
        print('creating stage:' + str(stage))
        stageURL = URLBase + str(stage)
        page = download(stageURL)
        with open(fileName + 'test', 'w', encoding='utf-8') as file:
            file.write(page)
        stageResults = process(page)
        with open(fileName, 'w', encoding='utf-8') as file:
            file.write(str(stageResults))
    print(str(stage) + ' is processed')
print('processing done')
#plot(len(stageNames))
