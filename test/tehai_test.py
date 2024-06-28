import pytest
from pyrmj import Tehai


def test_class_exists():
    """
    クラスが存在することのテスト
    """
    print("▶︎ クラスが存在することのテスト")

    assert Tehai is not None


def test___init__():
    """
    __init__(self, haipai=None)のテスト
    """
    print("▶︎ __init__(self, haipai=None)のテスト")

    assert Tehai() is not None

    test_cases = [
        (
            [
                "m0",
                "m1",
                "m9",
                "p0",
                "p1",
                "p9",
                "s0",
                "s1",
                "s9",
                "z1",
                "z2",
                "z6",
                "z7",
            ],
            "No error",
        ),
        (["_"], "No error"),
        (["z0"], ValueError),
        (["m1", "m1", "m1", "m1", "m1"], ValueError),
    ]

    for haipai, expected in test_cases:
        if expected == "No error":
            assert Tehai(haipai) is not None

        else:
            with pytest.raises(expected):
                Tehai(haipai)


def test_valid_hai():
    """
    valid_hai(hai)のテスト
    """
    print("▶︎ valid_hai(hai)のテスト")

    test_cases = [
        ("m1", "m1"),
        ("p2_", "p2_"),
        ("s3*", "s3*"),
        ("z4_*", "z4_*"),
        ("m0-", "m0-"),
        ("p5_+", "p5_+"),
        ("s6*=", "s6*="),
        ("z7_*-", "z7_*-"),
        ("_", None),
        ("x", None),
        ("mm", None),
        ("z0", None),
        ("z8", None),
        ("m9x", None),
        ("m9=*", None),
        ("m9*_", None),
        ("m9=_", None),
    ]

    for hai, expected in test_cases:
        if expected is None:
            assert Tehai.valid_hai(hai) is None

        else:
            assert Tehai.valid_hai(hai) == expected


def test_valid_mentsu():
    """
    valid_mentsu(mentsu)のテスト
    """
    print("▶︎ valid_mentsu(mentsu)のテスト")

    test_cases = [
        ("m111+", "m111+"),
        ("p555=", "p555="),
        ("s999-", "s999-"),
        ("z777+7", "z777+7"),
        ("m2222", "m2222"),
        ("p550=", "p550="),
        ("p5550=", "p5550="),
        ("p055=", "p505="),
        ("p055=0", "p505=0"),
        ("p000=0", "p000=0"),
        ("s0555-", "s5505-"),
        ("s0055-", "s5005-"),
        ("s0005", "s5000"),
        ("s0000", "s0000"),
        ("m1-23", "m1-23"),
        ("m12-3", "m12-3"),
        ("m123-", "m123-"),
        ("m231-", "m1-23"),
        ("m312-", "m12-3"),
        ("m3-12", "m123-"),
        ("m460-", "m40-6"),
        ("m1234-", None),
        ("m135-", None),
        ("m1234", None),
        ("m123", None),
        ("m111", None),
        ("z111=0", None),
    ]

    for mentsu, expected in test_cases:
        if expected is None:
            assert Tehai.valid_mentsu(mentsu) is None

        else:
            assert Tehai.valid_mentsu(mentsu) == expected


def test_from_string():
    """
    from_string(cls, tehai_string="")のテスト
    """
    print("▶︎ from_string(cls, tehai_string='')のテスト")

    assert Tehai.from_string().to_string() == ""

    test_cases = [
        ("", ""),
        ("z7654s987p654m321", "m123p456s789z4567"),
        ("m1,p123-,s555=,z777+7,m9999", "m1,p123-,s555=,z777+7,m9999"),
        ("m123p456s789____", "____m123p456s789"),
        ("m123p456____,s789-", "____m123p456,s789-"),
        ("m111p222s333", "m111p222s333"),
        ("m123456789p123456", "m123456789p1234p5"),
        ("m123456789p123,z111=", "m123456789p1p2,z111="),
        ("m123,z111=,p123-,s555=,z777+", "m1m2,z111=,p123-,s555=,z777+"),
        ("m11123456789991", "m1112345678999m1"),
        ("m11123456789990", "m1112345678999m0"),
        ("m12p345s678z23m3,z111=", "m12p345s678z23m3,z111="),
        ("m5550p5500s0000z00", "m0555p0055s0000"),
        ("m123p456s789z1112*", "m123p456s789z1112*"),
        ("m123p456s789z2*,z1111", "m123p456s789z2*,z1111"),
        ("m123p456s789z2*,z111+", "m123p456s789z2*,z111+"),
        ("m123p456s789z2,m403-", "m123p456s789z2,m3-40"),
        ("m123p456s789z2,m304-", "m123p456s789z2,m34-0"),
        ("m123p456s789z2,m345-", "m123p456s789z2,m345-"),
        ("m123p456s789z2,p050+", "m123p456s789z2,p500+"),
        ("m123p456s789z2,p055+", "m123p456s789z2,p505+"),
        ("m123p456s789z2,p550+", "m123p456s789z2,p550+"),
        ("m123p456s789z2,s0555=", "m123p456s789z2,s5505="),
        ("m123p456s789z2,s0050=", "m123p456s789z2,s5000="),
        ("m123p456s789z2,s0505", "m123p456s789z2,s5500"),
        ("m123p456s789z2,z000+", "m123p456s789z2"),
        ("m123p456s789z2,z888+", "m123p456s789z2"),
        ("m123p456s789z2,z1-23", "m123p456s789z2"),
        ("m123p456s789z2,s1+23", "m123p456s789z2"),
        ("m123p456s789z2,z11-", "m123p456s789z2"),
        ("m123p456s789z2,s13-5", "m123p456s789z2"),
        ("m123p456s789z2,m1p2s3-", "m123p456s789z2"),
        ("p456s789z1,m12-3,p999=,", "p456s789z1,m12-3,p999=,"),
    ]

    for tehai_string, expected in test_cases:
        assert Tehai.from_string(tehai_string).to_string() == expected


def test_clone():
    """
    clone(self)のテスト
    """
    print("▶︎ clone(self)のテスト")

    tehai = Tehai()
    assert tehai != tehai.clone()

    test_cases = [
        "m123p456s789z4567",
        "m1,p123-,s555=,z777+7,m9999",
        "m11123456789991",
        "m123p456s789z1112*",
        "___________,m123-",
    ]

    for tehai_string in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.to_string() == tehai.clone().to_string()

    tehai = Tehai.from_string("m123p456s789z4567")
    clone_tehai_string = tehai.clone().tsumo("m1").to_string()
    assert tehai.to_string() != clone_tehai_string

    tehai = Tehai.from_string("m123p456s789z34567")
    clone_tehai_string = tehai.clone().dahai("m1").to_string()
    assert tehai.to_string() != clone_tehai_string

    tehai = Tehai.from_string("m123p456s789z1167")
    clone_tehai_string = tehai.clone().fuuro("z111=").to_string()
    assert tehai.to_string() != clone_tehai_string

    tehai = Tehai.from_string("m123p456s789z11112")
    clone_tehai_string = tehai.clone().kan("z1111").to_string()
    assert tehai.to_string() != clone_tehai_string

    tehai = Tehai.from_string("m123p456s789z11223")
    clone_tehai_string = tehai.clone().dahai("z3*").to_string()
    assert tehai.to_string() != clone_tehai_string


def test_update_from_string():
    """
    update_from_string(self, tehai_string)のテスト
    """
    print("▶︎ update_from_string(self, tehai_string)のテスト")

    test_cases = ["m123p456s789z1122z2", "m123p456s789z2,z111=", "m123p456s789z1122*", "__________,z111="]

    for tehai_string in test_cases:
        assert Tehai().update_from_string(tehai_string).to_string() == tehai_string


def test_tsumo():
    """
    tsumo(self, hai, check=True)のテスト
    """
    print("▶︎ tsumo(self, hai, check=True)のテスト")

    test_cases = [
        ("m123p456s789z4567", "m1", "m123p456s789z4567m1"),
        ("m123p456s789z4567", "p1", "m123p456s789z4567p1"),
        ("m123p456s789z4567", "s1", "m123p456s789z4567s1"),
        ("m123p456s789z4567", "z1", "m123p456s789z4567z1"),
        ("m123p456s789z4567", "m0", "m123p456s789z4567m0"),
        ("m123p456s789z4567", "_", "m123p456s789z4567_"),
        ("m123p456s789z4567", "z0", ValueError),
        ("m123p456s789z4567", "z8", ValueError),
        ("m123p456s789z4567", "mm", ValueError),
        ("m123p456s789z4567", "xx", ValueError),
        ("m123p456s789z34567", "m1", ValueError),
        ("m123p456z34567,s789-,", "m1", ValueError),
        ("m123p456s789z1111", "z1", ValueError),
        ("m455556s789z1111", "m0", ValueError),
    ]

    for tehai_string, hai, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        if isinstance(expected, str):
            assert tehai.tsumo(hai).to_string() == expected

        else:
            with pytest.raises(expected):
                tehai.tsumo(hai)

    assert Tehai.from_string("m123p456s789z34567").tsumo("m1", check=False).to_string() == "m123p456s789z34567m1"


def test_dahai():
    """
    dahai(self, hai, check=True)のテスト
    """
    print("▶︎ dahai(self, hai, check=True)のテスト")

    test_cases = [
        ("m123p456s789z34567", "m1", "m23p456s789z34567"),
        ("m123p456s789z34567", "p4", "m123p56s789z34567"),
        ("m123p456s789z34567", "s7", "m123p456s89z34567"),
        ("m123p456s789z34567", "z3", "m123p456s789z4567"),
        ("m123p406s789z34567", "p0", "m123p46s789z34567"),
        ("m123p456s789z34567", "z7*", "m123p456s789z3456*"),
        ("m123p456s789z11223*", "z1", "m123p456s789z1223*"),
        ("______________", "m1", "_____________"),
        ("m123p456s789z34567", "z0", ValueError),
        ("m123p456s789z34567", "z8", ValueError),
        ("m123p456s789z34567", "mm", ValueError),
        ("m123p456s789z34567", "xx", ValueError),
        ("m123p456s789z4567", "_", ValueError),
        ("m123p456s789z4567", "m1", ValueError),
        ("m123p456s789z34567", "z1", ValueError),
        ("m123p456s789z34567", "p0", ValueError),
        ("m123p406s789z34567", "p5", ValueError),
    ]

    for tehai_string, hai, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        if isinstance(expected, str):
            assert tehai.dahai(hai).to_string() == expected

        else:
            with pytest.raises(expected):
                tehai.dahai(hai)

    assert Tehai.from_string("m123p456s789z4567").dahai("m1", check=False).to_string() == "m23p456s789z4567"


def test_fuuro():
    """
    fuuro(self, mentsu, check=True)のテスト
    """
    print("▶︎ fuuro(self, mentsu, check=True)のテスト")

    test_cases = [
        ("m23p456s789z34567", "m1-23", "p456s789z34567,m1-23,"),
        ("m123p46s789z34567", "p45-6", "m123s789z34567,p45-6,"),
        ("m123p456s99z34567", "s999+", "m123p456z34567,s999+,"),
        ("m123p456s789z1167", "z111=", "m123p456s789z67,z111=,"),
        ("m123p500s789z4567", "p5005-", "m123s789z4567,p5005-"),
        ("m123p456s789z4567*", "m1-23", "m1p456s789z4567*,m1-23,"),
        ("_____________", "m1-23", "___________,m1-23,"),
        ("m123p456s789z34567", "z3-45", ValueError),
        ("m123p456s789z34567", "m231-", ValueError),
        ("_____________", "m1111", ValueError),
        ("_____________", "m111+1", ValueError),
        ("m123p456s789z11567", "z111=", ValueError),
        ("m123p456s789z22,z111=,", "z222=", ValueError),
        ("m123p456s789z2,z111=", "z333=", ValueError),
        ("m123p40s789z22,z111=", "p456-", ValueError),
        ("m123p45s789z22,z111=", "p406-", ValueError),
    ]

    for tehai_string, mentsu, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        if isinstance(expected, str):
            assert tehai.fuuro(mentsu).to_string() == expected
        else:
            with pytest.raises(expected):
                tehai.fuuro(mentsu)

    test_cases = [
        ("m123p456s789z11567", "z111=", "m123p456s789z567,z111=,"),
        ("m123p456s789z22,z111=,", "z222=", "m123p456s789,z111=,z222=,"),
    ]

    for tehai_string, mentsu, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.fuuro(mentsu, False).to_string() == expected


if __name__ == "__main__":
    pytest.main()
