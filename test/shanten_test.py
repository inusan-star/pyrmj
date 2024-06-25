import json
import os
import pytest
from pyrmj import Tehai, shanten, shanten_chiitoi, shanten_ippan, shanten_kokushi

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "./data/shanten_1.json"), encoding="utf-8") as file:
    data1 = json.load(file)
with open(os.path.join(base_dir, "./data/shanten_1.json"), encoding="utf-8") as file:
    data2 = json.load(file)
with open(os.path.join(base_dir, "./data/shanten_1.json"), encoding="utf-8") as file:
    data3 = json.load(file)
with open(os.path.join(base_dir, "./data/shanten_1.json"), encoding="utf-8") as file:
    data4 = json.load(file)


def test_shanten_kokushi():
    """
    shanten_kokushi(tehai)のテスト
    """
    print("▶︎ shanten_kokushi(tehai)のテスト")

    assert shanten_kokushi(Tehai.from_string()) == 13
    assert (
        shanten_kokushi(Tehai.from_string("m19p19s19z12345677").tsumo("m1", False))
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
            .tsumo("z7", False)
            .tsumo("z7", False)
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


def test_shanten_ippan():
    """
    shanten_ippan(tehai)のテスト
    """
    print("▶︎ shanten_ippan(tehai))のテスト")

    assert shanten_ippan(Tehai.from_string()) == 13

    tehai = Tehai.from_string("m123,p123-,s456-,m789-")
    tehai.fuuro_list.append("z555=")
    assert shanten_ippan(tehai) == 0

    test_cases = [
        ("m123p406s789z1122", 0),
        ("m123p456s789z11222", -1),
        ("m123p456s789z2,z111=", 0),
        ("m12389p456s12789z1", 1),
        ("m12389p456s1289z11", 1),
        ("m133345568z23677", 2),
        ("p234s567,m222=,p0-67", 1),
        ("p222345z1234567", 4),
        ("p2344456z123456", 4),
        ("p11222345z12345", 3),
        ("p2234556788z123", 2),
        ("m11122,p123-,s12-3,z111=,", 0),
    ]

    for tehai_string, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert shanten_ippan(tehai) == expected

    for data in data1:
        tehai = Tehai(data["h"])
        assert shanten_ippan(tehai) == data["s"][0]

    for data in data2:
        tehai = Tehai(data["h"])
        assert shanten_ippan(tehai) == data["s"][0]

    for data in data3:
        tehai = Tehai(data["h"])
        assert shanten_ippan(tehai) == data["s"][0]

    for data in data4:
        tehai = Tehai(data["h"])
        assert shanten_ippan(tehai) == data["s"][0]


def test_shanten():
    """
    shanten(tehai)のテスト
    """
    print("▶︎ shanten(tehai)のテスト")

    test_cases = [
        ("m123p406s789z1122", 0),
        ("m19p19s19z1234567", 0),
        ("m1188p288s05z1177", 0),
    ]

    for tehai_string, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert shanten(tehai) == expected

    for data in data1:
        tehai = Tehai(data["h"])
        assert shanten(tehai) == min(data["s"])

    for data in data2:
        tehai = Tehai(data["h"])
        assert shanten(tehai) == min(data["s"])

    for data in data3:
        tehai = Tehai(data["h"])
        assert shanten(tehai) == min(data["s"])

    for data in data4:
        tehai = Tehai(data["h"])
        assert shanten(tehai) == min(data["s"])


if __name__ == "__main__":
    pytest.main()
