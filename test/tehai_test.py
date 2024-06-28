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


if __name__ == "__main__":
    pytest.main()
