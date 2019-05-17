import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from ast import literal_eval
from collections import defaultdict
import os


def plot(etape, race, year):
    raceString = 'race/' + race + '/' + year + '/'
    folderName = os.path.basename(raceString.replace("/", "@"))

    categories = 5
    categoryHelper = categories - 1
    pMFinish = mpatches.Patch(edgecolor=(0, 0, 0),
                              facecolor=(0 / categoryHelper,
                                         0 / categoryHelper, 1),
                              alpha=0.3,
                              label='mountain finish')
    pMountain = mpatches.Patch(edgecolor=(0, 0, 0),
                               facecolor=(1 / categoryHelper,
                                          1 / categoryHelper, 1),
                               alpha=0.3,
                               label='mountain')
    pHFinish = mpatches.Patch(edgecolor=(0, 0, 0),
                              facecolor=(2 / categoryHelper,
                                         2 / categoryHelper, 1),
                              alpha=0.3,
                              label='hill finish')
    pHilly = mpatches.Patch(edgecolor=(0, 0, 0),
                            facecolor=(3 / categoryHelper, 3 / categoryHelper,
                                       1),
                            alpha=0.3,
                            label='hilly')
    pFlat = mpatches.Patch(edgecolor=(0, 0, 0),
                           facecolor=(4 / categoryHelper, 4 / categoryHelper,
                                      1),
                           alpha=0.3,
                           label='flat')
    pTT = mpatches.Patch(edgecolor=(0, 0, 0),
                         facecolor=(1, 1, 1),
                         alpha=1,
                         hatch='///',
                         label='TT')
    patches = [pTT, pFlat, pHilly, pHFinish, pMountain, pMFinish]
    patchnames = [
        'TT', 'flat', 'hilly', 'hill finish', 'mountain', 'mountain finish'
    ]

    plt.rcParams.update({
        'figure.figsize': (25, 50),
        'font.size': 18,
        'lines.linewidth': 2.5,
        'legend.fontsize': 15,
        'legend.handlelength': 2
    })
    etapeStringspace = len(str(etape - 1))
    lastResultName = [
        x for x in os.listdir(folderName)
        if x[-(1 + etapeStringspace):] == '%' + str(etape - 1)
    ]
    fileName = lastResultName[0]
    lastResult = readFile(folderName, fileName)
    plotAmount = len(lastResult.keys())
    subplotNumber = 1
    for category in lastResult.keys():
        print(category)
        plt.subplot(plotAmount, 1, subplotNumber)
        plt.xlim(0, etape - 1)
        plt.xlabel('stage')
        plt.xticks(range(etape))
        drivers = [
            driver for driver in lastResult[category].keys()
            if lastResult[category][driver][1] <= 10
        ]
        #color the background acording to track type
        stageProfile = readFile(folderName, 'stageProfile')
        for etapeIterator in range(etape - 1):
            for profileType in range(categories + 1):
                if etapeIterator in stageProfile[profileType]:
                    plt.axvspan(etapeIterator,
                                etapeIterator + 1,
                                facecolor=patches[profileType].get_fc(),
                                alpha=0.3,
                                hatch=patches[profileType].get_hatch())

        data = [None] * (etape + 1)
        data[0] = defaultdict(lambda: (0, 1000))
        for etapeIterator in range(1, etape):
            etapeStringspace = len(str(etapeIterator))
            raceNumber = [
                x for x in os.listdir(folderName)
                if x[-(1 + etapeStringspace):] == '%' + str(etapeIterator)
            ]
            stageData = readFile(folderName, raceNumber[0])
            if category in stageData:
                stageData = stageData[category]
            else:
                stageData = dict()
            stageData = defaultdict(lambda: (0, 1000), stageData)
            data[etapeIterator] = stageData
        riders = plt.plot(range(etape), [[data[et][dr][0] for dr in drivers]
                                         for et in range(etape)])
        if category == 'Points' or category == 'KOM':
            plt.ylabel('points')
        else:
            plt.ylabel('gap in sec')
            plt.gca().invert_yaxis()
        plt.title(category.upper() + ' ' + year)
        #make handles for legend
        handl = riders + patches
        #only take certain fields from riders+ tracktype names,
        if category == 'Teams':
            handl = riders + patches
            labl = [dr for dr in drivers] + patchnames
        else:
            pedaleurInfo = readFile(folderName, 'pedaleurs')
            teamAbbrevations = readFile(folderName, 'teamAbbrevations')
            labl = [
                str(peds)[1:-1].replace('\'', '') for peds in [[
                    pedaleurInfo[dr][0] + ' ' +
                    pedaleurInfo[dr][1], pedaleurInfo[dr][2].upper(),
                    teamAbbrevations[pedaleurInfo[dr][3]]
                ] for dr in drivers]
            ] + patchnames
        plt.legend(handles=handl, labels=labl)
        subplotNumber = subplotNumber + 1

    #output
    plt.savefig(race + year + '.png', dpi='figure', bbox_inches='tight')


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
