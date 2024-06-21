import json
import pytest
from tehai import Tehai
from shanten import shanten_kokushi, shanten_chiitoi

with open("./data/shanten_1.json", encoding="utf-8") as f:
    data1 = json.load(f)
with open("./data/shanten_2.json", encoding="utf-8") as f:
    data2 = json.load(f)
with open("./data/shanten_3.json", encoding="utf-8") as f:
    data3 = json.load(f)
with open("./data/shanten_4.json", encoding="utf-8") as f:
    data4 = json.load(f)


def test_shanten_kokushi():
    """
    shanten_kokushi(tehai)のテスト
    """
    print("▶︎ shanten_kokushi(tehai)のテスト")

    assert shanten_kokushi(Tehai.from_string()) == 13
    assert (
        shanten_kokushi(
            Tehai.from_string("m19p19s19z12345677").action_tsumo("m1", False)
        )
        == -1
    )

    test_cases = [
        ("m23455p345s45678", 13),
        ("m189p12s249z12345", 4),
        ("m119p12s299z12345", 3),
        ("m11p19s19z1234567", 0),
        ("m19p19s19z1234567", 0),
        ("m119p19s19z1234567", -1),
        ("m19p19s19z1234,z777=", float("inf")),
        ("m119p19s19z12345", 1),
    ]

    for tehai_string, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert shanten_kokushi(tehai) == expected

    for data in data1:
        tehai = Tehai(data["h"])
        assert shanten_kokushi(tehai) == data["s"][1]

    for data in data2:
        tehai = Tehai(data["h"])
        assert shanten_kokushi(tehai) == data["s"][1]

    for data in data3:
        tehai = Tehai(data["h"])
        assert shanten_kokushi(tehai) == data["s"][1]

    for data in data4:
        tehai = Tehai(data["h"])
        assert shanten_kokushi(tehai) == data["s"][1]


def test_shanten_chiitoi():
    """
    shanten_chiitoi(tehai)のテスト
    """
    print("▶︎ shanten_chiitoi(tehai))のテスト")

    assert shanten_chiitoi(Tehai.from_string()) == 13
    assert (
        shanten_chiitoi(
            Tehai.from_string("m1188p2288s05z1122")
            .action_tsumo("z7", False)
            .action_tsumo("z7", False)
        )
        == -1
    )

    test_cases = [
        ("m19p19s19z1234567", 6),
        ("m1188p288s05z1111", 2),
        ("m1188p2388s05z111", 1),
        ("m1188p288s055z111", 2),
        ("m1188p288s05z1177'", 0),
        ("m1188p288s05z1177p2", -1),
        ("m1188p288s05z2,z111=", float("inf")),
        ("m1188s05z1122", 3),
    ]

    for tehai_string, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert shanten_chiitoi(tehai) == expected

    for data in data1:
        tehai = Tehai(data["h"])
        assert shanten_chiitoi(tehai) == data["s"][2]

    for data in data2:
        tehai = Tehai(data["h"])
        assert shanten_chiitoi(tehai) == data["s"][2]

    for data in data3:
        tehai = Tehai(data["h"])
        assert shanten_chiitoi(tehai) == data["s"][2]

    for data in data4:
        tehai = Tehai(data["h"])
        assert shanten_chiitoi(tehai) == data["s"][2]


if __name__ == "__main__":
    pytest.main()
