import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from ast import literal_eval
from collections import defaultdict
import os
etape = 0
folderName = ''


def plot(etapeNumber, race, year):
    plt.rcParams.update({
        'figure.figsize': (25, 50),
        'font.size': 18,
        'lines.linewidth': 2.5,
        'legend.fontsize': 15,
        'legend.handlelength': 2
    })
    global etape
    etape = etapeNumber
    raceString = 'race/' + race + '/' + year + '/'
    global folderName
    folderName = os.path.basename(raceString.replace("/", "@"))

    categories = len(readFile(folderName, 'stageProfile'))
    patches = createPatches(categories)
    patchnames = [
        'TT', 'flat', 'hilly', 'hill finish', 'mountain', 'mountain finish'
    ]

    lastResult = giveLastResult()

    plotAmountCategories = len(lastResult.keys())
    subplotNumber = 1
    for category in lastResult.keys():
        plt.subplot(plotAmountCategories, 1, subplotNumber)
        setupPLT(categories)
        #create Data
        topDrivers = [
            driver for driver in lastResult[category].keys()
            if lastResult[category][driver][1] <= 10
        ]
        data = [None] * (etape + 1)
        data[0] = defaultdict(lambda: (0, 1000))
        for etapeIterator in range(etape):
            etapeStringspace = len(str(etapeIterator))
            raceName = [
                x for x in os.listdir(folderName)
                if x[-(1 + etapeStringspace):] == '%' + str(etapeIterator)
            ]
            stageData = readFile(folderName, raceName[0])
            if category in stageData:
                stageData = stageData[category]
            else:
                stageData = dict()
            stageData = defaultdict(lambda: (0, 1000), stageData)
            data[etapeIterator + 1] = stageData

        riders = plt.plot(range(etape + 1),
                          [[data[et][dr][0] for dr in topDrivers]
                           for et in range(etape + 1)])

        #create Titles
        if category == 'Points' or category == 'KOM':
            plt.ylabel('points')
        else:
            plt.ylabel('gap in sec')
            plt.gca().invert_yaxis()
        plt.title(category + ' ' + beautify(race) + ' ' + year)

        #make handles for legend
        handl = riders + patches

        #only take certain fields from riders+ tracktype names,
        if category == 'Teams':
            handl = riders + patches
            labl = [dr for dr in topDrivers] + patchnames
        else:
            pedaleurInfo = readFile(folderName, 'pedaleurs')
            teamAbbrevations = readFile(folderName, 'teamAbbrevations')
            labl = [
                str(peds)[1:-1].replace('\'', '') for peds in [[
                    pedaleurInfo[dr][0] + ' ' +
                    pedaleurInfo[dr][1], pedaleurInfo[dr][2].upper(),
                    teamAbbrevations[pedaleurInfo[dr][3]]
                ] for dr in topDrivers]
            ] + patchnames
        plt.legend(handles=handl, labels=labl)
        subplotNumber = subplotNumber + 1

    #output
    plt.savefig(race + year + '.png', dpi='figure', bbox_inches='tight')
    return plt


def readFile(folderName, fileName):
    fullFileName = os.path.join(folderName, fileName)
    # special handling code here
    try:
        with open(fullFileName, 'r', encoding='utf-8') as file:
            fileContent = file.read()
    except IOError:
        print('Could not find: ' + fullFileName)
        quit()
    return literal_eval(fileContent)


def beautify(race):
    race = list(race)
    entryBuffer = list()
    resultBuffer = list()
    while len(race) > 0:
        if race[0] == '-':
            resultBuffer = addBuffer(resultBuffer, entryBuffer)
            entryBuffer = list()
            race.pop(0)
        else:
            entryBuffer.extend(race.pop(0))
    resultBuffer = addBuffer(resultBuffer, entryBuffer)
    return "".join(resultBuffer)[1:]


def addBuffer(resultBuffer, entryBuffer):
    if len(entryBuffer) > 2:
        entryBuffer[0] = entryBuffer[0].upper()
    resultBuffer.extend(' ')
    resultBuffer.extend(entryBuffer)
    return resultBuffer


def createPatches(categories):
    categoryNonTTT = categories - 1
    pMFinish = mpatches.Patch(edgecolor=(0, 0, 0),
                              facecolor=(0 / categoryNonTTT,
                                         0 / categoryNonTTT, 1),
                              alpha=0.3,
                              label='mountain finish')
    pMountain = mpatches.Patch(edgecolor=(0, 0, 0),
                               facecolor=(1 / categoryNonTTT,
                                          1 / categoryNonTTT, 1),
                               alpha=0.3,
                               label='mountain')
    pHFinish = mpatches.Patch(edgecolor=(0, 0, 0),
                              facecolor=(2 / categoryNonTTT,
                                         2 / categoryNonTTT, 1),
                              alpha=0.3,
                              label='hill finish')
    pHilly = mpatches.Patch(edgecolor=(0, 0, 0),
                            facecolor=(3 / categoryNonTTT, 3 / categoryNonTTT,
                                       1),
                            alpha=0.3,
                            label='hilly')
    pFlat = mpatches.Patch(edgecolor=(0, 0, 0),
                           facecolor=(4 / categoryNonTTT, 4 / categoryNonTTT,
                                      1),
                           alpha=0.3,
                           label='flat')
    pTT = mpatches.Patch(edgecolor=(0, 0, 0),
                         facecolor=(1, 1, 1),
                         alpha=1,
                         hatch='///',
                         label='TT')
    return [pTT, pFlat, pHilly, pHFinish, pMountain, pMFinish]


def setupPLT(categories):
    plt.xlim(0, etape)
    plt.xlabel('stage')
    plt.xticks(range(etape + 1))
    patches = createPatches(categories)
    #color the background acording to track type
    stageProfile = readFile(folderName, 'stageProfile')
    for profileType in range(categories):
        for etapeIterator in stageProfile[profileType]:
            plt.axvspan(etapeIterator,
                        etapeIterator + 1,
                        facecolor=patches[profileType].get_fc(),
                        alpha=0.3,
                        hatch=patches[profileType].get_hatch())


def giveLastResult():
    etapeStringspace = len(str(etape - 1))
    lastResultName = [
        x for x in os.listdir(folderName)
        if x[-(1 + etapeStringspace):] == '%' + str(etape - 1)
    ]
    fileName = lastResultName[0]
    return readFile(folderName, fileName)


if __name__ == '__main__':
    plot(21, 'tour-de-france', '2018')
