import textprocess
import pytest


@pytest.mark.lowLevel
def test_time():
    # 01:05:48 => 3948
    # 1:05:48 => 3948
    # 05:48 => 348
    # 15:48 => 948
    # 0:48 => 48
    # 0:00 => 0
    given = [" 01:05:48 ", " 1:05:48", "05:48 ", " 15:48", "0:48", "0:00"]
    expected = [3948, 3948, 348, 948, 48, 0]
    for i in range(len(given)):
        assert textprocess.getTime(given[i]) == expected[i]


@pytest.mark.lowLevel
def test_name_team():
    given = [
        "   Astana Pro Team<", " Team LottoNL-Jumbo<",
        "Team EF Education First-Drapac p/b Cannondale<"
    ]
    expected = [
        "Astana Pro Team", "Team LottoNL-Jumbo",
        "Team EF Education First-Drapac p/b Cannondale"
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
