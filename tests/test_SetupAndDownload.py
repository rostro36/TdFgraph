import pytest

import socket
from ast import literal_eval
import urllib3

import TdFgraph.setupAndDownload as sAP

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)  #we do not check the certs of the resultssite, because it is not important enouogh for such a project.


@pytest.mark.lowLevel
def test_download():
    given = sAP.download('https://postman-echo.com/get?foo1=bar1&foo2=bar2')
    expected = '{"args":{"foo1":"bar1","foo2":"bar2"},"headers":{"x-forwarded-proto":"https","x-forwarded-port":"443","host":"postman-echo.com","x-amzn-trace-id":"Root=1-5f61dc10-8f3e088838c107c0724bf890","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","accept-language":"de,en-US;q=0.7,en;q=0.3","accept-encoding":"gzip, deflate, br","upgrade-insecure-requests":"1"},"url":"https://postman-echo.com/get?foo1=bar1&foo2=bar2"}'
    assert given.strip()[:153] == expected[:153]


@pytest.mark.lowLevel
def test_download_no_net(monkeypatch):
    with pytest.raises(SystemExit) as exit:
        with pytest.raises(Exception) as ex:

            def guard(*args, **kwargs):
                raise Exception("I told you not to use the Internet!")

            monkeypatch.setattr(socket, 'socket', guard)
            sAP.download('https://httpbin.org/get')
    assert exit.type == SystemExit


@pytest.mark.lowLevel
def test_upload():
    given = sAP.upload('tour-de-france2018.png')
    assert given[:20] == 'https://i.imgur.com/'


@pytest.mark.lowLevel
def test_upload_no_net(monkeypatch):
    with pytest.raises(SystemExit) as exit:
        with pytest.raises(Exception) as ex:

            def guard(*args, **kwargs):
                raise Exception("I told you not to use the Internet!")

            monkeypatch.setattr(socket, 'socket', guard)
            sAP.upload('tour-de-france2018.png')
    assert exit.type == SystemExit


@pytest.mark.lowLevel
def test_upload_wrong_file():
    with pytest.raises(SystemExit) as exit:
        with pytest.raises(Exception) as ex:
            sAP.upload('tour-de-france3120.png')
    assert exit.type == SystemExit


@pytest.mark.midLevel
def test_teamnames():
    given = sAP.getTeamnames(
        'https://www.procyclingstats.com/race/vuelta-a-espana/2018/')
    expected = literal_eval(
        "{'BORA - hansgrohe': 'BOH', 'Mitchelton-Scott': 'MTS', 'Quick-Step Floors': 'QST', 'Movistar Team': 'MOV', 'BMC Racing Team': 'BMC', 'Bahrain Merida Pro Cycling Team': 'TBM', 'Team Sky': 'SKY', 'UAE-Team Emirates': 'UAD', 'Astana Pro Team': 'AST', 'Team EF Education First-Drapac p/b Cannondale': 'EFD', 'Team LottoNL-Jumbo': 'TLJ', 'Lotto Soudal': 'LTS', 'Team Sunweb': 'SUN', 'AG2R La Mondiale': 'ALM', 'Groupama - FDJ': 'FDJ', 'Cofidis, Solutions Crédits': 'COF', 'Trek - Segafredo': 'TFS', 'Team Katusha Alpecin': 'TKA', 'Team Dimension Data': 'DDD', 'Euskadi - Murias': 'EUS', 'Caja Rural - Seguros RGA': 'CJR', 'Burgos-BH': 'BBH'}"
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
        'https://www.procyclingstats.com/race/tour-de-romandie/2018/')
    expected = ([[3], [], [1, 2, 5], [0], [4], [3]], [
        'race/tour-de-romandie/2018/prologue',
        'race/tour-de-romandie/2018/stage-1',
        'race/tour-de-romandie/2018/stage-2',
        'race/tour-de-romandie/2018/stage-3',
        'race/tour-de-romandie/2018/stage-4',
        'race/tour-de-romandie/2018/stage-5'
    ])
    assert given == expected


@pytest.mark.midLevel
def test_Pedaleurs():
    given = sAP.getPedaleurs(
        'https://www.procyclingstats.com/race/vuelta-a-espana/2018/')
    with open('tests/pedaleurs_testresult', 'r', encoding='utf-8') as file:
        expected = literal_eval(file.read())
    assert given == expected
