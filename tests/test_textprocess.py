import pytest

from ast import literal_eval
import os

import TdFgraph.textprocess as textprocess


@pytest.mark.lowLevel
def test_time():
    # 01:05:48 => 3948
    # 1:05:48 => 3948
    # 05:48 => 348
    # 15:48 => 948
    # 0:48 => 48
    # 0:00 => 0
    given = [
        " 01:05:48 ", " 1:05:48", "05:48 ", " 15:48", "0:48", "0:00", "  -  ",
        ",,"
    ]
    expected = [3948, 3948, 348, 948, 48, 0, 9223372036854775807, -1]
    for i in range(len(given)):
        assert textprocess.getTime(given[i]) == expected[i]


@pytest.mark.lowLevel
def test_name_team():
    given = [
        "   Astana Pro Team<", " Team LottoNL-Jumbo<",
        "Team EF Education First-Drapac p/b Cannondale<",
        "Cofidis, Solutions Crédits&nbsp;<"
    ]
    expected = [
        "Astana Pro Team", "Team LottoNL-Jumbo",
        "Team EF Education First-Drapac p/b Cannondale",
        "Cofidis, Solutions Crédits"
    ]
    for i in range(len(given)):
        assert textprocess.getName(given[i]) == expected[i]


@pytest.mark.lowLevel
def test_name_family():
    given = [" Maté<", " Luis Ángel<", "Kwiatkowski<", "Michał<"]
    expected = ["Maté", "Luis Ángel", "Kwiatkowski", "Michał"]
    for i in range(len(given)):
        assert textprocess.getName(given[i]) == expected[i]


@pytest.mark.lowLevel
def test_number():
    given = ["1<", "1", "1 ", "206</th", "48</th>"]
    expected = [1, 1, 1, 206, 48]
    for i in range(len(given)):
        assert textprocess.getNumber(given[i]) == expected[i]


@pytest.mark.midLevel
def test_gc():
    with open('tests/gc_testpage', 'r', encoding='utf-8') as file:
        testpage = file.read()
    print('ayoo')
    print(testpage)
    given = textprocess.procGC(testpage)
    expected = literal_eval(
        """{34: (0, 1), 145: (6, 2), 63: (7, 3), 87: (17, 4), 148: (20, 5), 33: (21, 6), 142: (21, 7), 153: (21, 8), 4: (22, 9), 151: (22, 10), 37: (22, 11), 165: (22, 12), 57: (23, 13), 82: (23, 14), 32: (23, 15), 88: (24, 16), 3: (24, 17), 143: (24, 18), 114: (25, 19), 161: (27, 20), 36: (28, 21), 75: (28, 22), 157: (28, 23), 106: (29, 24), 42: (29, 25), 68: (29, 26), 93: (29, 27), 131: (29, 28), 103: (29, 29), 71: (29, 30), 14: (30, 31), 73: (30, 32), 22: (30, 33), 81: (30, 34), 121: (30, 35), 163: (31, 36), 92: (31, 37), 147: (31, 38), 133: (33, 39), 95: (34, 40), 45: (34, 41), 47: (34, 42), 35: (35, 43), 21: (35, 44), 83: (35, 45), 94: (35, 46), 105: (35, 47), 174: (35, 48), 58: (36, 49), 5: (36, 50), 124: (36, 51), 162: (38, 52), 166: (38, 53), 55: (38, 54), 72: (38, 55), 16: (38, 56), 176: (38, 57), 41: (38, 58), 171: (39, 59), 112: (40, 60), 104: (40, 61), 54: (40, 62), 51: (40, 63), 78: (40, 64), 1: (40, 65), 194: (40, 66), 38: (41, 67), 98: (41, 68), 17: (42, 69), 61: (42, 70), 132: (42, 71), 175: (42, 72), 116: (42, 73), 66: (42, 74), 27: (42, 75), 158: (42, 76), 138: (42, 77), 91: (43, 78), 86: (44, 79), 111: (45, 80), 141: (45, 81), 113: (45, 82), 172: (46, 83), 203: (46, 84), 164: (47, 85), 74: (47, 86), 127: (47, 87), 85: (48, 88), 46: (48, 89), 64: (49, 90), 178: (49, 91), 156: (49, 92), 77: (49, 93), 218: (50, 94), 117: (50, 95), 115: (50, 96), 31: (51, 97), 144: (51, 98), 23: (51, 99), 102: (51, 100), 2: (51, 101), 154: (52, 102), 44: (53, 103), 26: (53, 104), 126: (53, 105), 65: (54, 106), 146: (54, 107), 84: (54, 108), 128: (54, 109), 107: (55, 110), 134: (55, 111), 173: (56, 112), 101: (57, 113), 185: (57, 114), 177: (57, 115), 187: (58, 116), 217: (58, 117), 211: (58, 118), 155: (59, 119), 7: (59, 120), 13: (59, 121), 118: (59, 122), 96: (59, 123), 76: (59, 124), 28: (60, 125), 53: (60, 126), 192: (61, 127), 207: (61, 128), 6: (62, 129), 122: (62, 130), 136: (62, 131), 15: (62, 132), 168: (62, 133), 195: (63, 134), 152: (63, 135), 182: (64, 136), 11: (64, 137), 181: (64, 138), 24: (64, 139), 62: (65, 140), 18: (65, 141), 108: (65, 142), 198: (66, 143), 12: (66, 144), 67: (67, 145), 8: (67, 146), 184: (67, 147), 56: (67, 148), 137: (67, 149), 197: (67, 150), 125: (68, 151), 206: (69, 152), 48: (70, 153), 213: (70, 154), 97: (70, 155), 193: (71, 156), 215: (71, 157), 188: (72, 158), 52: (72, 159), 167: (73, 160), 204: (73, 161), 208: (74, 162), 202: (75, 163), 196: (75, 164), 43: (75, 165), 205: (76, 166), 214: (76, 167), 216: (76, 168), 135: (77, 169), 123: (78, 170), 191: (80, 171), 186: (83, 172), 201: (94, 173), 25: (94, 174), 212: (98, 175), 183: (102, 176)}  """
    )
    assert given == expected


@pytest.mark.midLevel
def test_points():
    with open('tests/points_testpage', 'r', encoding='utf-8') as file:
        testpage = file.read()
    given = textprocess.procPoints(testpage)
    expected = literal_eval(
        """{34: (25, 1), 145: (20, 2), 63: (16, 3), 87: (14, 4), 148: (12, 5), 33: (10, 6), 142: (9, 7), 153: (8, 8), 4: (7, 9), 151: (6, 10), 37: (5, 11), 165: (4, 12), 57: (3, 13), 82: (2, 14), 32: (1, 15)} """
    )
    assert given == expected


@pytest.mark.midLevel
def test_kom():
    with open('tests/kom_testpage', 'r', encoding='utf-8') as file:
        testpage = file.read()
    given = textprocess.procKOM(testpage)
    expected = literal_eval(
        """{206: (11, 1), 64: (5, 2), 116: (4, 3), 88: (3, 4), 145: (2, 5), 93: (1, 6), 17: (1, 7)}"""
    )
    assert expected == given


@pytest.mark.midLevel
def test_youth():
    with open('tests/youth_testpage', 'r', encoding='utf-8') as file:
        testpage = file.read()
    given = textprocess.procYouth(testpage)
    expected = literal_eval(
        '{92: (0, 1), 116: (5, 2), 105: (5, 3), 111: (6, 4), 24: (7, 5), 156: (16, 6), 14: (16, 7), 165: (21, 8), 22: (41, 9), 174: (91, 10), 95: (107, 11), 164: (109, 12), 63: (122, 13), 153: (331, 14), 67: (453, 15), 152: (595, 16), 4: (744, 17), 13: (884, 18), 133: (1005, 19), 135: (1047, 20), 82: (1413, 21), 5: (1427, 22), 162: (1475, 23), 185: (1640, 24), 32: (1971, 25), 106: (1980, 26), 65: (1992, 27)}'
    )
    assert expected == given


@pytest.mark.midLevel
def test_team():
    with open('tests/teams_testpage', 'r', encoding='utf-8') as file:
        testpage = file.read()
    given = textprocess.procGCEquipe(testpage)
    expected = literal_eval(
        """{'BMC Racing Team': (0, 1), 'Team Sky': (4, 2), 'Movistar Team': (21, 3), 'Team Sunweb': (28, 4), 'Lotto Soudal': (35, 5), 'Trek - Segafredo': (37, 6), 'Bahrain Merida Pro Cycling Team': (39, 7), 'Mitchelton-Scott': (44, 8), 'Team Dimension Data': (50, 9), 'Quick-Step Floors': (51, 10), 'BORA - hansgrohe': (54, 11), 'Groupama - FDJ': (54, 12), 'Team LottoNL-Jumbo': (61, 13), 'Team EF Education First-Drapac p/b Cannondale': (64, 14), 'Astana Pro Team': (64, 15), 'AG2R La Mondiale': (67, 16), 'UAE-Team Emirates': (69, 17), 'Team Katusha - Alpecin': (70, 18), 'Caja Rural - Seguros RGA': (121, 19), 'Euskadi - Murias': (123, 20), 'Cofidis, Solutions Crédits': (133, 21), 'Burgos-BH': (136, 22)} """
    )
    assert expected == given


@pytest.mark.midLevel
def test_categories():
    testpath = 'tests/race@tour-de-france@2018@/race@tour-de-france@2018@stage-1%0test'
    with open(testpath, 'r', encoding='utf-8') as file:
        testpage = file.read()
    expected = textprocess.checkCategories(testpage)
    given = ["Stage1", "GC", "Points", "Youth", "KOM", "Teams"]
    assert expected == given


@pytest.mark.HighLevel
def test_process():
    testfiles = os.listdir('tests/race@tour-de-france@2018@')
    testfiles = [file for file in testfiles if file[-4:] == 'test']
    for testfile in testfiles:
        testfile = os.path.join('tests/race@tour-de-france@2018@', testfile)
        with open(testfile, 'r', encoding='utf-8') as file:
            testpage = file.read()
        expected = textprocess.process(testpage)
        with open(testfile[:-4], 'r', encoding='utf-8') as file:
            testpage = file.read()
        given = literal_eval(testpage)
        assert expected == given
