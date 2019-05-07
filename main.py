# coding: utf-8
#libs used
from textprocess import process
from data import newstage
from graph import plot
from setupAndDownload import getStageReadiness, download, getProfile, getTeamnames, getPedaleurs

import traceback
import data

#gather the data
URL = 'https://www.procyclingstats.com/race/vuelta-a-espana/2018/'
stageProfile = getProfile(URL)
(readyFlags, numberOfStages) = getStageReadiness(URL)
teamAbbrevations = getTeamnames(URL)
pedaleurs = getPedaleurs(URL)
URL = URL + 'stage-'
for etape in range(1, numberOfStages):
    if etape > readyFlags[0]:
        break
    print('working on stage:' + str(etape))
    stageURL = URL + str(etape)
    page = download(stageURL)
    #open the file
    newstage(etape)
    process(page)
    print(str(etape) + ' is processed')
print('processing done')
plot(etape)  #get the actual site
