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


def test_kan():
    """
    kan(self, mentsu, check=True)のテスト
    """
    print("▶︎ kan(self, mentsu, check=True)のテスト")

    test_cases = [
        ("m1111p456s789z4567", "m1111", "p456s789z4567,m1111"),
        ("m1p456s789z4567,m111+", "m111+1", "p456s789z4567,m111+1"),
        ("m123p5555s789z4567", "p5555", "m123s789z4567,p5555"),
        ("m123p5s789z4567,p555=", "p555=5", "m123s789z4567,p555=5"),
        ("m123p456s9999z4567", "s9999", "m123p456z4567,s9999"),
        ("m123p456s9z4567,s999-", "s999-9", "m123p456z4567,s999-9"),
        ("m123p456s789z67777", "z7777", "m123p456s789z6,z7777"),
        ("m123p456s789z67,z777+", "z777+7", "m123p456s789z6,z777+7"),
        ("m0055p456s789z4567", "m5500", "p456s789z4567,m5500"),
        ("m123p5s789z4567,p505=", "p505=5", "m123s789z4567,p505=5"),
        ("m123p0s789z4567,p555=", "p555=0", "m123s789z4567,p555=0"),
        ("m1111p456s789z4567*", "m1111", "p456s789z4567*,m1111"),
        ("m1p456s789z4567*,m111+", "m111+1", "p456s789z4567*,m111+1"),
        ("______________", "m5550", "__________,m5550"),
        ("___________,m555=", "m555=0", "__________,m555=0"),
        ("m1112456s789z4567", "m456-", ValueError),
        ("m1112456s789z4567", "m111+", ValueError),
        ("m1112456s789z4567", "m1112", ValueError),
        ("m2456s789z4567,m111+", "m111+2", ValueError),
        ("m1111p456s789z456", "m1111", ValueError),
        ("m1111s789z4567,p456-,", "m1111", ValueError),
        ("m1112p456s789z4567", "m1111", ValueError),
        ("m13p456s789z567,m222=", "m2222", ValueError),
        ("m10p456s789z567,m555=", "m5555", ValueError),
        ("m15p456s789z567,m555=", "m5550", ValueError),
        ("m12p456s789z567,m222=", "m111=1", ValueError),
    ]

    for tehai_string, mentsu, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        if isinstance(expected, str):
            assert tehai.kan(mentsu).to_string() == expected

        else:
            with pytest.raises(expected):
                tehai.kan(mentsu)

    with pytest.raises(ValueError):
        Tehai.from_string("m1111p4444s789z567").kan("m1111").kan("p4444")

    assert Tehai.from_string("m1111p456s789z456").kan("m1111", False).to_string() == "p456s789z456,m1111"
    assert Tehai.from_string("m1111s789z4567,p456-,").kan("m1111", False).to_string() == "s789z4567,p456-,m1111"
    assert (
        Tehai.from_string("m1111p4444s789z567").kan("m1111", False).kan("p4444", False).to_string()
        == "s789z567,m1111,p4444"
    )


def test_menzen():
    """
    menzen(self)のテスト
    """
    print("▶︎ menzen(self)のテスト")

    test_cases = [
        ("m123p0s789z4567", True),
        ("p0s789z4567,m123-", False),
        ("m123p0s789,z1111", True),
    ]

    for tehai_string, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.menzen() == expected


def test_riichi():
    """
    get_riichi(self)のテスト
    """
    print("▶︎ get_riichi(self)のテスト")

    assert not Tehai.from_string("_____________").riichi()
    assert Tehai.from_string("_____________").tsumo("z7").dahai("z7_*").riichi()


def test_get_dahai():
    """
    get_dahai(self, check=True)のテスト
    """
    print("▶︎ get_dahai(self, check=True)のテスト")

    test_cases = [
        ("m123p406s789z4567", None),
        ("m123p406s789z2,z111+", None),
        ("_____________", None),
        ("__________,z111+", None),
        (
            "m123p406s789z11123",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p0",
                "p6",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2",
                "z3_",
            ],
        ),
        (
            "m123p406s789z12,z111+",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p0",
                "p6",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2_",
            ],
        ),
        ("m123p456s789z1234m1*", ["m1_"]),
        (
            "m123p405s789z11123",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p0",
                "p5",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2",
                "z3_",
            ],
        ),
        (
            "m123p45s789z11123p0",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p5",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2",
                "z3",
                "p0_",
            ],
        ),
        (
            "m123p45s789z11123p5",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p5",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2",
                "z3",
                "p5_",
            ],
        ),
        (
            "m123p405s789z1112p0",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p0",
                "p5",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2",
                "p0_",
            ],
        ),
        ("______________", []),
        ("___________,m123-,", []),
        (
            "m145p406s789z23,m1-23,",
            [
                "m5",
                "p4",
                "p0",
                "p6",
                "s7",
                "s8",
                "s9",
                "z2",
                "z3",
            ],
        ),
        (
            "m145p406s789z23,m234-,",
            [
                "m5",
                "p4",
                "p0",
                "p6",
                "s7",
                "s8",
                "s9",
                "z2",
                "z3",
            ],
        ),
        (
            "m123p258s789z23,p45-6,",
            [
                "m1",
                "m2",
                "m3",
                "p2",
                "p8",
                "s7",
                "s8",
                "s9",
                "z2",
                "z3",
            ],
        ),
        (
            "m123p456s467z23,s7-89,",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p5",
                "p6",
                "s4",
                "s6",
                "z2",
                "z3",
            ],
        ),
        (
            "m123p456s789z12,z111+,",
            [
                "m1",
                "m2",
                "m3",
                "p4",
                "p5",
                "p6",
                "s7",
                "s8",
                "s9",
                "z2",
            ],
        ),
        (
            "m256p456s789z12,m340-,",
            [
                "m6",
                "p4",
                "p5",
                "p6",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2",
            ],
        ),
        (
            "m206p456s789z12,m345-,",
            [
                "m6",
                "p4",
                "p5",
                "p6",
                "s7",
                "s8",
                "s9",
                "z1",
                "z2",
            ],
        ),
        ("m25p1s12678,z666+,m550-,", ["m2", "p1", "s1", "s2", "s6", "s7", "s8"]),
        ("m14,p456-,s789-,z111+,m234-,", []),
        ("m14,p456-,s789-,z111+,m1-23,", []),
        ("m22,p456-,s789-,z111+,m12-3,", []),
    ]

    for tehai_string, expected in test_cases:
        if expected is None:
            assert Tehai.from_string(tehai_string).get_dahai() is None

        else:
            assert Tehai.from_string(tehai_string).get_dahai() == expected

    assert Tehai.from_string("m145p406s789z23,m1-23,").get_dahai(False) == [
        "m1",
        "m4",
        "m5",
        "p4",
        "p0",
        "p6",
        "s7",
        "s8",
        "s9",
        "z2",
        "z3",
    ]


def test_get_chii_mentsu():
    """
    get_chii_mentsu(self, hai, check=True)のテスト
    """
    print("▶︎ get_chii_mentsu(self, hai, check=True)のテスト")

    test_cases = [
        ("m123p456s789z12345", "m1-"),
        ("m123p456s789z12,z333=,", "m1-"),
        ("______________", "m1-"),
    ]

    for tehai_string, hai in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.get_chii_mentsu(hai) is None

    test_cases = [
        ("m123p456s789z1234", "m5-", []),
        ("_____________", "m5-", []),
        ("m123p456s789z1234", "m3-", ["m123-"]),
        (
            "m1234p456s789z123",
            "m3-",
            ["m123-", "m23-4"],
        ),
        (
            "m12345p456s789z12",
            "m3-",
            ["m123-", "m23-4", "m3-45"],
        ),
        ("m123p456s789z1234", "p0-", ["p40-6"]),
        ("m123p34067s789z12", "p3-", ["p3-40"]),
        ("m123p34067s789z12", "p4-", ["p34-0", "p4-06"]),
        ("m123p34067s789z12", "p6-", ["p406-", "p06-7"]),
        ("m123p34067s789z12", "p7-", ["p067-"]),
        (
            "m123p340567s789z1",
            "p3-",
            ["p3-40", "p3-45"],
        ),
        ("m123p340567s789z1", "p4-", ["p34-0", "p34-5", "p4-06", "p4-56"]),
        ("m123p340567s789z1", "p6-", ["p406-", "p456-", "p06-7", "p56-7"]),
        ("m123p340567s789z1", "p7-", ["p067-", "p567-"]),
        ("m123p456s789z1234", "m3_-", ["m123-"]),
        ("m123p456s789z1234", "m3*-", ["m123-"]),
        (
            "m123p456s789z1234",
            "m3_*-",
            ["m123-"],
        ),
        ("m123p456s789z1234*", "m3-", []),
        (
            "s6789,m123-,p456-,z111+",
            "s6-",
            [],
        ),
        ("s6789,m123-,p456-,z111+", "s9-", []),
        ("s7889,m123-,p456-,z111+", "s8-", []),
        ("s7899,m123-,p456-,z111+", "s9-", []),
        ("s7789,m123-,p456-,z111+", "s7-", []),
        ("s6678999,m123-,p456-", "s6-", []),
        ("m123p456s789z1234", "z1-", []),
        ("m123p456s789z1234", "m1+", []),
        ("m123p456s789z1234", "m1=", []),
        ("m123p456s789z1234", "mm-", ValueError),
        ("m123p456s789z1234", "m1", ValueError),
    ]

    for tehai_string, hai, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        if isinstance(expected, list):
            assert tehai.get_chii_mentsu(hai) == expected

        else:
            with pytest.raises(expected):
                tehai.get_chii_mentsu(hai)

    test_cases = [
        (
            "s6789,m123-,p456-,z111+",
            "s6-",
            ["s6-78"],
        ),
        ("s6789,m123-,p456-,z111+", "s9-", ["s789-"]),
        ("s7889,m123-,p456-,z111+", "s8-", ["s78-9"]),
        ("s7899,m123-,p456-,z111+", "s9-", ["s789-"]),
        ("s7789,m123-,p456-,z111+", "s7-", ["s7-89"]),
        ("s6678999,m123-,p456-", "s6-", ["s6-78"]),
    ]

    for tehai_string, hai, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.get_chii_mentsu(hai, False) == expected


def test_get_pon_mentsu():
    """
    get_pon_mentsu(self, hai)のテスト
    """
    print("▶︎ get_pon_mentsu(self, hai)のテスト")

    test_cases = [
        ("m112p456s789z12345", "m1+"),
        ("m112p456s789z12,z333=,", "m1="),
        ("______________", "m1-"),
    ]

    for tehai_string, hai in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.get_pon_mentsu(hai) is None

    test_cases = [
        ("m123p456s789z1234", "m1+", []),
        ("_____________", "m1=", []),
        ("m112p456s789z1234", "m1+", ["m111+"]),
        ("m123p445s789z1234", "p4=", ["p444="]),
        ("m123p345s778z1234", "s7-", ["s777-"]),
        ("m123p455s789z1234", "p0+", ["p550+"]),
        ("m123p405s789z1234", "p0+", ["p500+"]),
        ("m123p400s789z1234", "p0+", ["p000+"]),
        ("m123p055s789z1234", "p5=", ["p505=", "p555="]),
        ("m123p005s789z1234", "p5=", ["p005=", "p505="]),
        ("m123p000s789z1234", "p5=", ["p005="]),
        ("m112p456s789z1234", "m1_+", ["m111+"]),
        ("m112p456s789z1234", "m1*+", ["m111+"]),
        ("m112p456s789z1234", "m1_*+", ["m111+"]),
        ("m112p456s789z1234*", "m1+", []),
        ("m123p456s789z1234", "mm+", ValueError),
        ("m112p456s789z1234", "m1", ValueError),
    ]

    for tehai_string, hai, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        if isinstance(expected, list):
            assert tehai.get_pon_mentsu(hai) == expected

        else:
            with pytest.raises(expected):
                tehai.get_pon_mentsu(hai)


def test_get_kan_mentsu():
    """
    get_kan_mentsu(self, hai=None)のテスト
    """
    print("▶︎ get_kan_mentsu(self, hai=None)のテスト")

    test_cases = [
        ("m111p456s789z12345", "m1+"),
        ("m111p456s789z12,z333=,", "m1+"),
        ("______________", "m1-"),
    ]

    for tehai_string, hai in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.get_kan_mentsu(hai) is None

    test_cases = [
        ("m123p456s789z1122", "z1+", []),
        ("_____________", "z1=", []),
        ("m111p456s789z1234", "m1+", ["m1111+"]),
        ("m123p444s789z1234", "p4=", ["p4444="]),
        ("m123p456s777z1234", "s7-", ["s7777-"]),
        ("m123p555s789z1234", "p0+", ["p5550+"]),
        ("m123p055s789z1234", "p5+", ["p5505+"]),
        ("m123p005s789z1234", "p5+", ["p5005+"]),
        ("m123p000s789z1234", "p5+", ["p0005+"]),
        ("m111p456s789z1234", "m1_+", ["m1111+"]),
        ("m111p456s789z1234", "m1*+", ["m1111+"]),
        ("m111p456s789z1234", "m1_*+", ["m1111+"]),
        ("m111p456s789z1234*", "m1+", []),
        ("m111p555s999z1234", "mm+", ValueError),
        ("m111p555s999z1234", "m1", ValueError),
    ]

    for tehai_string, hai, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        if isinstance(expected, list):
            assert tehai.get_kan_mentsu(hai) == expected

        else:
            with pytest.raises(expected):
                tehai.get_kan_mentsu(hai)

    test_cases = [
        ("m1111p555s999z123"),
        ("m1111p555s999,z333="),
        ("m11112p555s999,z333=,"),
        ("_____________"),
        ("m1p555s999z123,m111-"),
        ("m1p555s999,z333=,m111-"),
        ("m12p555s999,z333=,m111-,"),
        ("__________,m111-,"),
    ]

    for tehai_string in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.get_kan_mentsu() is None

    test_cases = [
        ("m123p456s789z12345", []),
        ("______________", []),
        ("m1111p456s789z1234", ["m1111"]),
        ("m123p4444s789z1234", ["p4444"]),
        ("m123p456s7777z1234", ["s7777"]),
        ("m123p456s789z11112", ["z1111"]),
        ("m123p0555s789z1234", ["p5550"]),
        ("m123p0055s789z1234", ["p5500"]),
        ("m123p0005s789z1234", ["p5000"]),
        ("m123p0000s789z1234", ["p0000"]),
        ("m111p456s789z1122m1*", ["m1111"]),
        ("m111123p456s78z11m4*", []),
        ("m1111p456s789z1111", ["m1111", "z1111"]),
        ("m123p456s789z12,z777+", []),
        ("___________,z777+", []),
        ("m1p456s789z1234,m111+", ["m111+1"]),
        ("m123p4s789z1234,p444=", ["p444=4"]),
        ("m123p456s7z1234,s777-", ["s777-7"]),
        ("m123p456s789z12,z111+", ["z111+1"]),
        ("m123p0s789z1234,p555=", ["p555=0"]),
        ("m123p5s789z1234,p550-", ["p550-5"]),
        ("p456s789z1234m1*,m111+", []),
        ("m1p4s789z123,m111+,p444=", ["m111+1", "p444=4"]),
        ("m1p456s789z1111,m111+", ["m111+1", "z1111"]),
    ]

    for tehai_string, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert tehai.get_kan_mentsu() == expected


if __name__ == "__main__":
    pytest.main()
