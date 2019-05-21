import pytest

from ast import literal_eval
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt

import TdFgraph.graph as graph


@pytest.mark.lowLevel
def test_beautify():
    given = ["giro-d-italia", "tour-de-france", "vuelta-a-espana"]
    expected = ['Giro d Italia', 'Tour de France', 'Vuelta a Espana']
    for i in range(len(given)):
        assert graph.beautify(given[i]) == expected[i]


@pytest.mark.lowLevel
def test_readFile():
    given = graph.readFile('race@tour-de-france@2018@',
                           'race@tour-de-france@2018@stage-1%0')
    expected = "{'GC': {103: (0, 1), 111: (4, 2), 144: (6, 3), 27: (9, 4), 95: (10, 5), 201: (10, 6), 163: (10, 7), 31: (10, 8), 194: (10, 9), 121: (10, 10), 114: (10, 11), 51: (10, 12), 213: (10, 13), 182: (10, 14), 8: (10, 15), 105: (10, 16), 128: (10, 17), 107: (10, 18), 104: (10, 19), 132: (10, 20), 52: (10, 21), 198: (10, 22), 216: (10, 23), 101: (10, 24), 87: (10, 25), 123: (10, 26), 171: (10, 27), 32: (10, 28), 41: (10, 29), 172: (10, 30), 56: (10, 31), 127: (10, 32), 75: (10, 33), 106: (10, 34), 21: (10, 35), 133: (10, 36), 131: (10, 37), 78: (10, 38), 148: (10, 39), 191: (10, 40), 156: (10, 41), 161: (10, 42), 141: (10, 43), 11: (10, 44), 116: (10, 45), 181: (10, 46), 207: (10, 47), 208: (10, 48), 217: (10, 49), 54: (10, 50), 147: (10, 51), 91: (10, 52), 47: (10, 53), 166: (10, 54), 88: (10, 55), 15: (10, 56), 183: (10, 57), 44: (10, 58), 157: (10, 59), 36: (10, 60), 177: (10, 61), 175: (10, 62), 38: (10, 63), 53: (32, 64), 23: (34, 65), 197: (34, 66), 98: (42, 67), 108: (43, 68), 167: (44, 69), 17: (44, 70), 145: (50, 71), 122: (52, 72), 138: (52, 73), 126: (52, 74), 48: (52, 75), 113: (52, 76), 112: (52, 77), 46: (52, 78), 118: (52, 79), 195: (52, 80), 12: (52, 81), 96: (52, 82), 81: (61, 83), 61: (61, 84), 16: (61, 85), 158: (61, 86), 214: (61, 87), 55: (61, 88), 168: (61, 89), 193: (61, 90), 1: (61, 91), 192: (61, 92), 37: (61, 93), 58: (61, 94), 188: (61, 95), 143: (61, 96), 125: (61, 97), 92: (61, 98), 93: (61, 99), 42: (61, 100), 203: (61, 101), 67: (61, 102), 211: (61, 103), 94: (72, 104), 134: (74, 105), 135: (74, 106), 24: (74, 107), 212: (82, 108), 187: (82, 109), 68: (84, 110), 72: (85, 111), 71: (85, 112), 2: (85, 113), 184: (85, 114), 73: (87, 115), 218: (88, 116), 33: (88, 117), 165: (88, 118), 164: (88, 119), 34: (92, 120), 202: (92, 121), 86: (97, 122), 43: (97, 123), 115: (100, 124), 153: (100, 125), 35: (100, 126), 5: (108, 127), 74: (122, 128), 146: (130, 129), 26: (141, 130), 174: (146, 131), 28: (146, 132), 14: (149, 133), 18: (149, 134), 136: (154, 135), 186: (154, 136), 102: (154, 137), 196: (154, 138), 152: (154, 139), 77: (154, 140), 204: (154, 141), 185: (154, 142), 85: (154, 143), 57: (154, 144), 117: (154, 145), 206: (154, 146), 97: (154, 147), 4: (154, 148), 205: (154, 149), 7: (154, 150), 82: (172, 151), 6: (174, 152), 142: (174, 153), 76: (174, 154), 22: (178, 155), 63: (190, 156), 215: (190, 157), 62: (192, 158), 83: (192, 159), 25: (192, 160), 178: (192, 161), 173: (192, 162), 45: (192, 163), 176: (202, 164), 84: (254, 165), 64: (254, 166), 65: (254, 167), 66: (254, 168), 137: (254, 169), 124: (254, 170), 162: (254, 171), 155: (393, 172), 151: (393, 173), 154: (393, 174), 3: (478, 175), 13: (480, 176)}, 'Points': {103: (63, 1), 111: (37, 2), 144: (24, 3), 95: (24, 4), 184: (20, 5), 45: (17, 6), 201: (16, 7), 215: (15, 8), 163: (14, 9), 31: (12, 10), 171: (11, 11), 194: (10, 12), 151: (10, 13), 112: (9, 14), 121: (8, 15), 131: (8, 16), 114: (7, 17), 51: (6, 18), 213: (5, 19), 216: (5, 20), 182: (4, 21), 8: (3, 22), 107: (3, 23), 105: (2, 24), 148: (2, 25), 113: (1, 26)}, 'Youth': {103: (0, 1), 163: (10, 2), 182: (10, 3), 172: (10, 4), 148: (10, 5), 208: (10, 6), 217: (10, 7), 147: (10, 8), 36: (10, 9), 98: (42, 10), 167: (44, 11), 126: (52, 12), 195: (52, 13), 168: (61, 14), 211: (61, 15), 2: (85, 16), 164: (88, 17), 43: (97, 18), 115: (100, 19), 5: (108, 20), 26: (141, 21), 14: (149, 22), 186: (154, 23), 152: (154, 24), 77: (154, 25), 85: (154, 26), 173: (192, 27), 45: (192, 28), 154: (393, 29)}, 'KOM': {45: (1, 1)}, 'Teams': {'Quick-Step Floors': (0, 1), 'Astana Pro Team': (0, 2), 'BORA - hansgrohe': (0, 3), 'Bahrain Merida Pro Cycling Team': (0, 4), 'Trek - Segafredo': (0, 5), 'Wanty - Groupe Gobert': (0, 6), 'Team Katusha Alpecin': (0, 7), 'Team Dimension Data': (0, 8), 'Team Sunweb': (0, 9), 'Cofidis, Solutions Crédits': (0, 10), 'Team LottoNL-Jumbo': (0, 11), 'Direct Energie': (0, 12), 'Lotto Soudal': (0, 13), 'Team Fortuneo - Samsic': (0, 14), 'AG2R La Mondiale': (24, 15), 'UAE-Team Emirates': (32, 16), 'Team EF Education First-Drapac p/b Cannondale': (34, 17), 'BMC Racing Team': (51, 18), 'Groupama - FDJ': (51, 19), 'Movistar Team': (75, 20), 'Team Sky': (126, 21), 'Mitchelton-Scott': (176, 22)}}"
    assert given == literal_eval(expected)


@pytest.mark.HighLevel
@pytest.mark.mpl_image_compare(savefig_kwargs={
    'dpi': 'figure',
    'bbox_inches': 'tight'
})
def test_plot():
    return graph.plot(21, 'tour-de-france', '2018')
