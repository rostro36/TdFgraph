import pytest
import socket
import setupAndDownload as sAP
from ast import literal_eval


@pytest.mark.lowLevel
def test_download():
    given = sAP.download('https://postman-echo.com/get?foo1=bar1&foo2=bar2')
    expected = '{"args":{"foo1":"bar1","foo2":"bar2"},"headers":{"x-forwarded-proto":"https","host":"postman-echo.com","accept-encoding":"identity","x-forwarded-port":"443"},"url":"https://postman-echo.com/get?foo1=bar1&foo2=bar2"}'
    assert given == expected


@pytest.mark.lowLevel
def test_download_no_net(monkeypatch):
    with pytest.raises(SystemExit) as exit:
        with pytest.raises(Exception) as ex:

            def guard(*args, **kwargs):
                raise Exception("I told you not to use the Internet!")

            monkeypatch.setattr(socket, 'socket', guard)
            sAP.download('https://httpbin.org/get')
    assert exit.type == SystemExit


@pytest.mark.midLevel
def test_teamnames():
    given = sAP.getTeamnames(
        'https://www.procyclingstats.com/race/vuelta-a-espana/2018/')
    expected = literal_eval(
        "{'BORA - hansgrohe': 'BOH', 'Mitchelton-Scott': 'MTS', 'Quick-Step Floors': 'QST', 'Movistar Team': 'MOV', 'BMC Racing Team': 'BMC', 'Bahrain Merida Pro Cycling Team': 'TBM', 'Team Sky': 'SKY', 'UAE-Team Emirates': 'UAD', 'Astana Pro Team': 'AST', 'Team EF Education First-Drapac p/b Cannondale': 'EFD', 'Team LottoNL-Jumbo': 'TLJ', 'Lotto Soudal': 'LTS', 'Team Sunweb': 'SUN', 'AG2R La Mondiale': 'ALM', 'Groupama - FDJ': 'FDJ', 'Cofidis, Solutions Crédits': 'COF', 'Trek - Segafredo': 'TFS', 'Team Katusha - Alpecin': 'TKA', 'Team Dimension Data': 'DDD', 'Euskadi - Murias': 'EUS', 'Caja Rural - Seguros RGA': 'CJR', 'Burgos-BH': 'BBH'}"
    )
    assert given == expected


@pytest.mark.midLevel
def test_Readiness():
    given = sAP.getStageReadiness(
        'https://www.procyclingstats.com/race/vuelta-a-espana/2018/')
    expected = ([21, 21, 21, 0, 21], 21)
    assert given == expected


@pytest.mark.midLevel
def test_Profile():
    given = sAP.getProfile(
        'https://www.procyclingstats.com/race/vuelta-a-espana/2018/')
    expected = [[0, 15], [0, 9, 15, 17, 20], [1, 5, 6, 10, 11], [7],
                [2, 4, 13], [3, 8, 12, 14, 16, 18, 19]]
    assert given == expected


@pytest.mark.midLevel
def test_Pedaleurs():
    given = sAP.getPedaleurs(
        'https://www.procyclingstats.com/race/vuelta-a-espana/2018/')
    expected = literal_eval("""{
        1: ('NIBALI', 'Vincenzo', 'it', 'Bahrain Merida Pro Cycling Team', 1),
        2:
        ('GARCÍA CORTINA', 'Iván', 'es', 'Bahrain Merida Pro Cycling Team', 2),
        3: ('IZAGIRRE', 'Gorka', 'es', 'Bahrain Merida Pro Cycling Team', 3),
        4: ('IZAGIRRE', 'Ion', 'es', 'Bahrain Merida Pro Cycling Team', 4),
        5: ('PADUN', 'Mark', 'ua', 'Bahrain Merida Pro Cycling Team', 5),
        6:
        ('PELLIZOTTI', 'Franco', 'it', 'Bahrain Merida Pro Cycling Team', 6),
        7:
        ('PERNSTEINER', 'Hermann', 'at', 'Bahrain Merida Pro Cycling Team', 7),
        8: ('PIBERNIK', 'Luka', 'si', 'Bahrain Merida Pro Cycling Team', 8),
        11: ('DUPONT', 'Hubert', 'fr', 'AG2R La Mondiale', 11),
        12: ('CHEREL', 'Mickaël', 'fr', 'AG2R La Mondiale', 12),
        13: ('DUVAL', 'Julien', 'fr', 'AG2R La Mondiale', 13),
        14: ('GALLOPIN', 'Tony', 'fr', 'AG2R La Mondiale', 14),
        15: ('GASTAUER', 'Ben', 'lu', 'AG2R La Mondiale', 15),
        16: ('GENIEZ', 'Alexandre', 'fr', 'AG2R La Mondiale', 16),
        17: ('GOUGEARD', 'Alexis', 'fr', 'AG2R La Mondiale', 17),
        18: ('PETERS', 'Nans', 'fr', 'AG2R La Mondiale', 18),
        21: ('LÓPEZ', 'Miguel Ángel', 'co', 'Astana Pro Team', 21),
        22: ('BILBAO', 'Pello', 'es', 'Astana Pro Team', 22),
        23: ('CATALDO', 'Dario', 'it', 'Astana Pro Team', 23),
        24: ('FRAILE', 'Omar', 'es', 'Astana Pro Team', 24),
        25: ('HIRT', 'Jan', 'cz', 'Astana Pro Team', 25),
        26: ('STALNOV', 'Nikita', 'kz', 'Astana Pro Team', 26),
        27: ('VILLELLA', 'Davide', 'it', 'Astana Pro Team', 27),
        28: ('ZEITS', 'Andrey', 'kz', 'Astana Pro Team', 28),
        31: ('PORTE', 'Richie', 'au', 'BMC Racing Team', 31),
        32: ('BOOKWALTER', 'Brent', 'us', 'BMC Racing Team', 32),
        33: ('DE MARCHI', 'Alessandro', 'it', 'BMC Racing Team', 33),
        34: ('DENNIS', 'Rohan', 'au', 'BMC Racing Team', 34),
        35: ('ROCHE', 'Nicolas', 'ie', 'BMC Racing Team', 35),
        36: ('ROSSKOPF', 'Joey', 'us', 'BMC Racing Team', 36),
        37: ('TEUNS', 'Dylan', 'be', 'BMC Racing Team', 37),
        38: ('VENTOSO', 'Francisco José', 'es', 'BMC Racing Team', 38),
        41: ('SAGAN', 'Peter', 'sk', 'BORA - hansgrohe', 41),
        42: ('BUCHMANN', 'Emanuel', 'de', 'BORA - hansgrohe', 42),
        43: ('BURGHARDT', 'Marcus', 'de', 'BORA - hansgrohe', 43),
        44: ('FORMOLO', 'Davide', 'it', 'BORA - hansgrohe', 44),
        45: ('MAJKA', 'Rafał', 'pl', 'BORA - hansgrohe', 45),
        46: ('MCCARTHY', 'Jay', 'au', 'BORA - hansgrohe', 46),
        47: ('PÖSTLBERGER', 'Lukas', 'at', 'BORA - hansgrohe', 47),
        48: ('SCHWARZMANN', 'Michael', 'de', 'BORA - hansgrohe', 48),
        51: ('PINOT', 'Thibaut', 'fr', 'Groupama - FDJ', 51),
        52: ('DELAGE', 'Mickaël', 'fr', 'Groupama - FDJ', 52),
        53: ('DUCHESNE', 'Antoine', 'ca', 'Groupama - FDJ', 53),
        54: ('MOLARD', 'Rudy', 'fr', 'Groupama - FDJ', 54),
        55: ('PREIDLER', 'Georg', 'at', 'Groupama - FDJ', 55),
        56: ('SARREAU', 'Marc', 'fr', 'Groupama - FDJ', 56),
        57: ('THOMAS', 'Benjamin', 'fr', 'Groupama - FDJ', 57),
        58: ('VINCENT', 'Léo', 'fr', 'Groupama - FDJ', 58),
        61: ('BENOOT', 'Tiesj', 'be', 'Lotto Soudal', 61),
        62: ('ARMÉE', 'Sander', 'be', 'Lotto Soudal', 62),
        63: ('CAMPENAERTS', 'Victor', 'be', 'Lotto Soudal', 63),
        64: ('DE GENDT', 'Thomas', 'be', 'Lotto Soudal', 64),
        65: ('LAMBRECHT', 'Bjorg', 'be', 'Lotto Soudal', 65),
        66: ('MONFORT', 'Maxime', 'be', 'Lotto Soudal', 66),
        67: ('VAN DER SANDE', 'Tosh', 'be', 'Lotto Soudal', 67),
        68: ('WALLAYS', 'Jelle', 'be', 'Lotto Soudal', 68),
        71: ('YATES', 'Simon', 'gb', 'Mitchelton-Scott', 71),
        72: ('ALBASINI', 'Michael', 'ch', 'Mitchelton-Scott', 72),
        73: ('EDMONDSON', 'Alex', 'au', 'Mitchelton-Scott', 73),
        74: ('HAIG', 'Jack', 'au', 'Mitchelton-Scott', 74),
        75: ('HOWSON', 'Damien', 'au', 'Mitchelton-Scott', 75),
        76: ('MEZGEC', 'Luka', 'si', 'Mitchelton-Scott', 76),
        77: ('TRENTIN', 'Matteo', 'it', 'Mitchelton-Scott', 77),
        78: ('YATES', 'Adam', 'gb', 'Mitchelton-Scott', 78),
        81: ('QUINTANA', 'Nairo', 'co', 'Movistar Team', 81),
        82: ('AMADOR', 'Andrey', 'cr', 'Movistar Team', 82),
        83: ('ANACONA', 'Winner', 'co', 'Movistar Team', 83),
        84: ('BENNATI', 'Daniele', 'it', 'Movistar Team', 84),
        85: ('CARAPAZ', 'Richard', 'ec', 'Movistar Team', 85),
        86: ('ERVITI', 'Imanol', 'es', 'Movistar Team', 86),
        87: ('OLIVEIRA', 'Nelson', 'pt', 'Movistar Team', 87),
        88: ('VALVERDE', 'Alejandro', 'es', 'Movistar Team', 88),
        91: ('VIVIANI', 'Elia', 'it', 'Quick-Step Floors', 91),
        92: ('ASGREEN', 'Kasper', 'dk', 'Quick-Step Floors', 92),
        93: ('DE PLUS', 'Laurens', 'be', 'Quick-Step Floors', 93),
        94: ('DEVENYNS', 'Dries', 'be', 'Quick-Step Floors', 94),
        95: ('MAS', 'Enric', 'es', 'Quick-Step Floors', 95),
        96: ('MØRKØV', 'Michael', 'dk', 'Quick-Step Floors', 96),
        97: ('SABATINI', 'Fabio', 'it', 'Quick-Step Floors', 97),
        98: ('SERRY', 'Pieter', 'be', 'Quick-Step Floors', 98),
        101: ('MEINTJES', 'Louis', 'za', 'Team Dimension Data', 101),
        102: ('ANTÓN', 'Igor', 'es', 'Team Dimension Data', 102),
        103: ('CUMMINGS', 'Steve', 'gb', 'Team Dimension Data', 103),
        104: ('GHEBREIGZABHIER', 'Amanuel', 'er', 'Team Dimension Data', 104),
        105: ('GIBBONS', 'Ryan', 'za', 'Team Dimension Data', 105),
        106: ('KING', 'Ben', 'us', 'Team Dimension Data', 106),
        107: ('KUDUS', 'Merhawi', 'er', 'Team Dimension Data', 107),
        108: ('VAN ZYL', 'Johann', 'za', 'Team Dimension Data', 108),
        111: ('URÁN', 'Rigoberto', 'co',
              'Team EF Education First-Drapac p/b Cannondale', 111),
        112: ('CLARKE', 'Simon', 'au',
              'Team EF Education First-Drapac p/b Cannondale', 112),
        113: ('DOCKER', 'Mitchell', 'au',
              'Team EF Education First-Drapac p/b Cannondale', 113),
        114: ('LANGEVELD', 'Sebastian', 'nl',
              'Team EF Education First-Drapac p/b Cannondale', 114),
        115: ('MORENO', 'Daniel', 'es',
              'Team EF Education First-Drapac p/b Cannondale', 115),
        116: ('ROLLAND', 'Pierre', 'fr',
              'Team EF Education First-Drapac p/b Cannondale', 116),
        117: ('VAN ASBROECK', 'Tom', 'be',
              'Team EF Education First-Drapac p/b Cannondale', 117),
        118: ('WOODS', 'Michael', 'ca',
              'Team EF Education First-Drapac p/b Cannondale', 118),
        121: ('ZAKARIN', 'Ilnur', 'ru', 'Team Katusha - Alpecin', 121),
        122: ('BOSWELL', 'Ian', 'us', 'Team Katusha - Alpecin', 122),
        123: ('GONÇALVES', 'José', 'pt', 'Team Katusha - Alpecin', 123),
        124: ('HOLLENSTEIN', 'Reto', 'ch', 'Team Katusha - Alpecin', 124),
        125: ('KOCHETKOV', 'Pavel', 'ru', 'Team Katusha - Alpecin', 125),
        126: ('LAMMERTINK', 'Maurits', 'nl', 'Team Katusha - Alpecin', 126),
        127: ('MACHADO', 'Tiago', 'pt', 'Team Katusha - Alpecin', 127),
        128: ('RESTREPO', 'Jhonatan', 'co', 'Team Katusha - Alpecin', 128),
        131: ('KRUIJSWIJK', 'Steven', 'nl', 'Team LottoNL-Jumbo', 131),
        132: ('BENNETT', 'George', 'nz', 'Team LottoNL-Jumbo', 132),
        133: ('BOOM', 'Lars', 'nl', 'Team LottoNL-Jumbo', 133),
        134: ('DE TIER', 'Floris', 'be', 'Team LottoNL-Jumbo', 134),
        135: ('KUSS', 'Sepp', 'us', 'Team LottoNL-Jumbo', 135),
        136: ('LEEZER', 'Tom', 'nl', 'Team LottoNL-Jumbo', 136),
        137: ('LINDEMAN', 'Bert-Jan', 'nl', 'Team LottoNL-Jumbo', 137),
        138: ('VAN POPPEL', 'Danny', 'nl', 'Team LottoNL-Jumbo', 138),
        141: ('DE LA CRUZ', 'David', 'es', 'Team Sky', 141),
        142: ('CASTROVIEJO', 'Jonathan', 'es', 'Team Sky', 142),
        143: ('GEOGHEGAN HART', 'Tao', 'gb', 'Team Sky', 143),
        144: ('HENAO', 'Sergio', 'co', 'Team Sky', 144),
        145: ('KWIATKOWSKI', 'Michał', 'pl', 'Team Sky', 145),
        146: ('PUCCIO', 'Salvatore', 'it', 'Team Sky', 146),
        147: ('SIVAKOV', 'Pavel', 'ru', 'Team Sky', 147),
        148: ('VAN BAARLE', 'Dylan', 'nl', 'Team Sky', 148),
        151: ('KELDERMAN', 'Wilco', 'nl', 'Team Sunweb', 151),
        152: ('FRÖHLINGER', 'Johannes', 'de', 'Team Sunweb', 152),
        153: ('GESCHKE', 'Simon', 'de', 'Team Sunweb', 153),
        154: ('HINDLEY', 'Jai', 'au', 'Team Sunweb', 154),
        155: ('STORER', 'Michael', 'au', 'Team Sunweb', 155),
        156: ('TEUNISSEN', 'Mike', 'nl', 'Team Sunweb', 156),
        157: ('TUSVELD', 'Martijn', 'nl', 'Team Sunweb', 157),
        158: ('WALSCHEID', 'Max', 'de', 'Team Sunweb', 158),
        161: ('MOLLEMA', 'Bauke', 'nl', 'Trek - Segafredo', 161),
        162: ('BRAMBILLA', 'Gianluca', 'it', 'Trek - Segafredo', 162),
        163: ('BRÄNDLE', 'Matthias', 'at', 'Trek - Segafredo', 163),
        164: ('CONCI', 'Nicola', 'it', 'Trek - Segafredo', 164),
        165: ('FELLINE', 'Fabio', 'it', 'Trek - Segafredo', 165),
        166: ('IRIZAR', 'Markel', 'es', 'Trek - Segafredo', 166),
        167: ('NIZZOLO', 'Giacomo', 'it', 'Trek - Segafredo', 167),
        168: ('REIJNEN', 'Kiel', 'us', 'Trek - Segafredo', 168),
        171: ('ARU', 'Fabio', 'it', 'UAE-Team Emirates', 171),
        172: ('BYSTRØM', 'Sven Erik', 'no', 'UAE-Team Emirates', 172),
        173: ('CONSONNI', 'Simone', 'it', 'UAE-Team Emirates', 173),
        174: ('CONTI', 'Valerio', 'it', 'UAE-Team Emirates', 174),
        175: ('LAENGEN', 'Vegard Stake', 'no', 'UAE-Team Emirates', 175),
        176: ('MARTIN', 'Dan', 'ie', 'UAE-Team Emirates', 176),
        177: ('PETILLI', 'Simone', 'it', 'UAE-Team Emirates', 177),
        178: ('RAVASI', 'Edward', 'it', 'UAE-Team Emirates', 178),
        181: ('MENDES', 'José', 'pt', 'Burgos-BH', 181),
        182: ('BOL', 'Jetse', 'nl', 'Burgos-BH', 182),
        183: ('CABEDO', 'Óscar', 'es', 'Burgos-BH', 183),
        184: ('CUBERO', 'Jorge', 'es', 'Burgos-BH', 184),
        185: ('EZQUERRA', 'Jesús', 'es', 'Burgos-BH', 185),
        186: ('SIMÓN', 'Jordi', 'es', 'Burgos-BH', 186),
        187: ('RUBIO', 'Diego', 'es', 'Burgos-BH', 187),
        188: ('TORRES', 'Pablo', 'es', 'Burgos-BH', 188),
        191: ('PARDILLA', 'Sergio', 'es', 'Caja Rural - Seguros RGA', 191),
        192: ('ARANBURU', 'Alex', 'es', 'Caja Rural - Seguros RGA', 192),
        193: ('LASTRA', 'Jonathan', 'es', 'Caja Rural - Seguros RGA', 193),
        194: ('MAS', 'Lluís', 'es', 'Caja Rural - Seguros RGA', 194),
        195: ('MOLINA', 'Antonio', 'es', 'Caja Rural - Seguros RGA', 195),
        196: ('RODRÍGUEZ', 'Cristián', 'es', 'Caja Rural - Seguros RGA', 196),
        197: ('SCHULTZ', 'Nick', 'au', 'Caja Rural - Seguros RGA', 197),
        198: ('SOTO', 'Nelson Andrés', 'co', 'Caja Rural - Seguros RGA', 198),
        201: ('BOUHANNI', 'Nacer', 'fr', 'Cofidis, Solutions Crédits', 201),
        202: ('CHETOUT', 'Loïc', 'fr', 'Cofidis, Solutions Crédits', 202),
        203: ('HERRADA', 'Jesús', 'es', 'Cofidis, Solutions Crédits', 203),
        204: ('HERRADA', 'José', 'es', 'Cofidis, Solutions Crédits', 204),
        205:
        ('LE TURNIER', 'Mathias', 'fr', 'Cofidis, Solutions Crédits', 205),
        206: ('MATÉ', 'Luis Ángel', 'es', 'Cofidis, Solutions Crédits', 206),
        207: ('ROSSETTO', 'Stéphane', 'fr', 'Cofidis, Solutions Crédits', 207),
        208: ('VANBILSEN', 'Kenneth', 'be', 'Cofidis, Solutions Crédits', 208),
        211: ('PRADES', 'Eduard', 'es', 'Euskadi - Murias', 211),
        212: ('ABERASTURI', 'Jon', 'es', 'Euskadi - Murias', 212),
        213: ('BAGÜES', 'Aritz', 'es', 'Euskadi - Murias', 213),
        214: ('BIZKARRA', 'Mikel', 'es', 'Euskadi - Murias', 214),
        215: ('BRAVO', 'Garikoitz', 'es', 'Euskadi - Murias', 215),
        216: ('ITURRIA', 'Mikel', 'es', 'Euskadi - Murias', 216),
        217: ('RODRÍGUEZ', 'Óscar', 'es', 'Euskadi - Murias', 217),
        218: ('SÁEZ', 'Héctor', 'es', 'Euskadi - Murias', 218)
    }""")
    assert given == expected
