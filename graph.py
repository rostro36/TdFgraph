import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#import data
from data import pedaleurs, ecarts, points, grimpeurs, jeunes, eq, plat, acci, intermediate, montagne, clm, abbrevations

#globals are not needed since we only read them and dont write to them.


def plot(etape):
    eq[0] = dict()

    #make start=0
    for i in eq[1].keys():
        eq[0][i] = (0, 0)

    #give font/patch for every type of track
    pmont = mpatches.Patch(color=(0 / 4, 0 / 4, 1), alpha=0.3, label='mountain')
    pint = mpatches.Patch(
        color=(1 / 4, 1 / 4, 1), alpha=0.3, label='intermediate')
    pacci = mpatches.Patch(color=(2 / 4, 2 / 4, 1), alpha=0.3, label='hilly')
    pplat = mpatches.Patch(color=(3 / 4, 3 / 4, 1), alpha=0.3, label='flat')
    pclm = mpatches.Patch(color=(1, 1, 1), alpha=0.3, label='TT')
    patches = [pmont, pacci, pplat, pclm]
    patchnames = ['mountain', 'intermediate', 'hilly', 'flat', 'TT']

    #usual jaune plot
    plt.rcParams.update({
        'figure.figsize': (25, 50),
        'font.size': 18,
        'lines.linewidth': 2.5,
        'legend.fontsize': 15,
        'legend.handlelength': 2
    })
    #find top 10 in ecarts
    drivers = [
        i for i in range(220)
        if ecarts[etape - 1][i][1] is not None and ecarts[etape - 1][i][1] <= 10
    ]
    #pick subplot
    plt.subplot(5, 1, 1)
    plt.xlim(0, etape - 1)
    plt.xlabel('stage')
    plt.xticks(range(etape))
    #color the background acording to track type
    for i in range(1, etape - 1):
        if i in plat:
            plt.axvspan(i - 1, i, facecolor=pplat.get_fc(), alpha=0.3)
        elif i in montagne:
            plt.axvspan(i - 1, i, facecolor=pmont.get_fc(), alpha=0.3)
        elif i in clm:
            plt.axvspan(i - 1, i, facecolor=pclm.get_fc(), alpha=0.3)
        elif i in acci:
            plt.axvspan(i - 1, i, facecolor=pacci.get_fc(), alpha=0.3)
        elif i in intermediate:
            plt.axvspan(i - 1, i, facecolor=pint.get_fc(), alpha=0.3)
    riders = plt.plot(
        range(etape),
        [[ecarts[et][dr][0] for dr in drivers] for et in range(etape)])
    plt.ylabel('gap in sec')
    plt.title('GC 2018')
    plt.gca().invert_yaxis()
    #make handles for legend
    handl = riders + patches
    #only take certain fields from riders+ tracktype names,
    labl = [
        str(peds)[1:-1] for peds in [[
            pedaleurs[dr][0] + ' ' + pedaleurs[dr][1], pedaleurs[dr][3].upper(),
            abbrevations[pedaleurs[dr][4]]
        ] for dr in drivers]
    ] + patchnames
    plt.legend(handles=handl, labels=labl)

    #respected jaune plot
    plt.subplot(5, 1, 2)
    plt.xlim(0, etape - 1)
    plt.xlabel('stage')
    plt.xticks(range(etape))
    for i in range(1, etape):
        if i in plat:
            plt.axvspan(i - 1, i, facecolor=pplat.get_fc(), alpha=0.3)
        elif i in montagne:
            plt.axvspan(i - 1, i, facecolor=pmont.get_fc(), alpha=0.3)
        elif i in clm:
            plt.axvspan(i - 1, i, facecolor=pclm.get_fc(), alpha=0.3)
        elif i in acci:
            plt.axvspan(i - 1, i, facecolor=pacci.get_fc(), alpha=0.3)
        elif i in intermediate:
            plt.axvspan(i - 1, i, facecolor=pint.get_fc(), alpha=0.3)
    plt.ylabel('gap in sec')
    plt.title('GC 2018 best 10 compared')
    plt.gca().invert_yaxis()
    riders = plt.plot(
        range(etape), [[
            ecarts[et][dr][0] - min([ecarts[et][dri][0]
                                     for dri in drivers])
            for dr in drivers
        ]
                       for et in range(etape)])
    handl = riders + patches
    labl = [
        str(peds)[1:-1] for peds in [[
            pedaleurs[dr][0] + ' ' + pedaleurs[dr][1], pedaleurs[dr][3].upper(),
            abbrevations[pedaleurs[dr][4]]
        ] for dr in drivers]
    ] + patchnames
    plt.legend(handles=handl, labels=labl)

    #maillot vert
    drivers = [
        i for i in range(220)
        if points[etape - 1][i][1] is not None and points[etape - 1][i][1] <= 10
    ]
    plt.subplot(5, 1, 3)
    plt.xlim(0, etape - 1)
    plt.xlabel('stage')
    plt.xticks(range(etape))
    for i in range(1, etape):
        if i in plat:
            plt.axvspan(i - 1, i, facecolor=pplat.get_fc(), alpha=0.3)
        elif i in montagne:
            plt.axvspan(i - 1, i, facecolor=pmont.get_fc(), alpha=0.3)
        elif i in clm:
            plt.axvspan(i - 1, i, facecolor=pclm.get_fc(), alpha=0.3)
        elif i in acci:
            plt.axvspan(i - 1, i, facecolor=pacci.get_fc(), alpha=0.3)
        elif i in intermediate:
            plt.axvspan(i - 1, i, facecolor=pint.get_fc(), alpha=0.3)
    plt.ylabel('points')
    plt.title('point classification 2018')
    riders = plt.plot(
        range(etape),
        [[points[et][dr][0] for dr in drivers] for et in range(etape)])
    handl = riders + patches
    labl = [
        str(peds)[1:-1] for peds in [[
            pedaleurs[dr][0] + ' ' + pedaleurs[dr][1], pedaleurs[dr][3].upper(),
            abbrevations[pedaleurs[dr][4]]
        ] for dr in drivers]
    ] + patchnames
    plt.legend(handles=handl, labels=labl)

    #maillot a points
    drivers = [
        i for i in range(220) if grimpeurs[etape - 1][i][1] is not None and
        grimpeurs[etape - 1][i][1] <= 10
    ]
    plt.subplot(5, 1, 4)
    plt.xlim(0, etape - 1)
    plt.xlabel('stage')
    plt.xticks(range(etape))
    for i in range(1, etape):
        if i in plat:
            plt.axvspan(i - 1, i, facecolor=pplat.get_fc(), alpha=0.3)
        elif i in montagne:
            plt.axvspan(i - 1, i, facecolor=pmont.get_fc(), alpha=0.3)
        elif i in clm:
            plt.axvspan(i - 1, i, facecolor=pclm.get_fc(), alpha=0.3)
        elif i in acci:
            plt.axvspan(i - 1, i, facecolor=pacci.get_fc(), alpha=0.3)
        elif i in intermediate:
            plt.axvspan(i - 1, i, facecolor=pint.get_fc(), alpha=0.3)
    plt.ylabel('points')
    plt.title('king of the mountain 2018')
    riders = plt.plot(
        range(etape),
        [[grimpeurs[et][dr][0] for dr in drivers] for et in range(etape)])
    handl = riders + patches
    labl = [
        str(peds)[1:-1] for peds in [[
            pedaleurs[dr][0] + ' ' + pedaleurs[dr][1], pedaleurs[dr][3].upper(),
            abbrevations[pedaleurs[dr][4]]
        ] for dr in drivers]
    ] + patchnames
    plt.legend(handles=handl, labels=labl)

    # #maillot blanc
    # drivers = [
    #     i for i in range(220)
    #     if jeunes[etape - 1][i] is not None and jeunes[etape - 1][i] <= 10
    # ]
    # plt.subplot(6, 1, 5)
    # plt.xlim(0, etape - 1)
    # plt.xlabel('stage')
    # plt.xticks(range(etape))
    # for i in range(1, etape):
    #     if i in plat:
    #         plt.axvspan(i - 1, i, facecolor=pplat.get_fc(), alpha=0.3)
    #     elif i in montagne:
    #         plt.axvspan(i - 1, i, facecolor=pmont.get_fc(), alpha=0.3)
    #     elif i in clm:
    #         plt.axvspan(i - 1, i, facecolor=pclm.get_fc(), alpha=0.3)
    #     elif i in acci:
    #         plt.axvspan(i - 1, i, facecolor=pacci.get_fc(), alpha=0.3)
    #     elif i in intermediate:
    #         plt.axvspan(i - 1, i, facecolor=pint.get_fc(), alpha=0.3)
    # plt.ylabel('gap in sec')
    # plt.title('maillot blanc 2018')
    # riders = plt.plot(
    #     range(etape), [[
    #         ecarts[et][dr][0] - min([ecarts[et][dri][0]
    #                                  for dri in drivers])
    #         for dr in drivers
    #     ]
    #                    for et in range(etape)])
    # plt.gca().invert_yaxis()
    # handl = riders + patches
    # labl = [
    #     str(peds)[1:-1] for peds in
    #     [[pedaleurs[dr][0] + ' ' + pedaleurs[dr][1], pedaleurs[dr][3:5]]
    #      for dr in drivers]
    # ] + patchnames
    # plt.legend(handles=handl, labels=labl)
    #team
    drivers = [i for i in eq[1].keys() if eq[etape - 1][i][0] <= 10]
    plt.subplot(5, 1, 5)
    plt.xlim(0, etape - 1)
    plt.xlabel('stage')
    plt.xticks(range(etape))
    for i in range(1, etape):
        if i in plat:
            plt.axvspan(i - 1, i, facecolor=pplat.get_fc(), alpha=0.3)
        elif i in montagne:
            plt.axvspan(i - 1, i, facecolor=pmont.get_fc(), alpha=0.3)
        elif i in clm:
            plt.axvspan(i - 1, i, facecolor=pclm.get_fc(), alpha=0.3)
        elif i in acci:
            plt.axvspan(i - 1, i, facecolor=pacci.get_fc(), alpha=0.3)
        elif i in intermediate:
            plt.axvspan(i - 1, i, facecolor=pint.get_fc(), alpha=0.3)
    plt.ylabel('gap in sec')
    plt.title('team classification 2018')
    riders = plt.plot(
        range(etape), [[
            eq[et][dr][1] - min([eq[et][dri][1]
                                 for dri in drivers])
            for dr in drivers
        ]
                       for et in range(etape)])
    plt.gca().invert_yaxis()
    handl = riders + patches
    labl = [dr for dr in drivers] + patchnames
    plt.legend(handles=handl, labels=labl)

    #output
    plt.savefig('vuelta2018.png', dpi='figure', bbox_inches='tight')
    plt.show()
