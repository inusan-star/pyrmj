import pytest
from pyrmj import Yama, rule


def test_class_exists():
    """
    クラスが存在することのテスト
    """
    print("▶︎ クラスが存在することのテスト")

    assert Yama is not None


def test___init__():
    """
    __init__(self, rule)のテスト
    """
    print("▶︎ __init__(self, rule)のテスト")

    test_cases = [
        (
            {"赤牌": {"m": 0, "p": 0, "s": 0}},
            "m1,m1,m1,m1,m2,m2,m2,m2,m3,m3,m3,m3,m4,m4,m4,m4,m5,m5,m5,m5,"
            "m6,m6,m6,m6,m7,m7,m7,m7,m8,m8,m8,m8,m9,m9,m9,m9,"
            "p1,p1,p1,p1,p2,p2,p2,p2,p3,p3,p3,p3,p4,p4,p4,p4,p5,p5,p5,p5,"
            "p6,p6,p6,p6,p7,p7,p7,p7,p8,p8,p8,p8,p9,p9,p9,p9,"
            "s1,s1,s1,s1,s2,s2,s2,s2,s3,s3,s3,s3,s4,s4,s4,s4,s5,s5,s5,s5,"
            "s6,s6,s6,s6,s7,s7,s7,s7,s8,s8,s8,s8,s9,s9,s9,s9,"
            "z1,z1,z1,z1,z2,z2,z2,z2,z3,z3,z3,z3,z4,z4,z4,z4,"
            "z5,z5,z5,z5,z6,z6,z6,z6,z7,z7,z7,z7",
        ),
        (
            {"赤牌": {"m": 1, "p": 2, "s": 3}},
            "m0,m1,m1,m1,m1,m2,m2,m2,m2,m3,m3,m3,m3,m4,m4,m4,m4,m5,m5,m5,"
            "m6,m6,m6,m6,m7,m7,m7,m7,m8,m8,m8,m8,m9,m9,m9,m9,"
            "p0,p0,p1,p1,p1,p1,p2,p2,p2,p2,p3,p3,p3,p3,p4,p4,p4,p4,p5,p5,"
            "p6,p6,p6,p6,p7,p7,p7,p7,p8,p8,p8,p8,p9,p9,p9,p9,"
            "s0,s0,s0,s1,s1,s1,s1,s2,s2,s2,s2,s3,s3,s3,s3,s4,s4,s4,s4,s5,"
            "s6,s6,s6,s6,s7,s7,s7,s7,s8,s8,s8,s8,s9,s9,s9,s9,"
            "z1,z1,z1,z1,z2,z2,z2,z2,z3,z3,z3,z3,z4,z4,z4,z4,"
            "z5,z5,z5,z5,z6,z6,z6,z6,z7,z7,z7,z7",
        ),
    ]

    for rule_json, expected in test_cases:
        yama = Yama(rule(rule_json))
        assert ",".join(sorted(yama.hai_)) == expected


def test_dora():
    """
    dora(hai)のテスト
    """
    print("▶︎ dora(hai)のテスト")

    test_cases = [
        ("m1", "m2"),
        ("m9", "m1"),
        ("m0", "m6"),
        ("p1", "p2"),
        ("p9", "p1"),
        ("p0", "p6"),
        ("s1", "s2"),
        ("s9", "s1"),
        ("s0", "s6"),
        ("z1", "z2"),
        ("z4", "z1"),
        ("z5", "z6"),
        ("z7", "z5"),
        ("z0", ValueError),
    ]

    for hai, expected in test_cases:
        if isinstance(expected, str):
            assert Yama.dora(hai) == expected

        else:
            with pytest.raises(expected):
                Yama.dora(hai)


def test_tsumo():
    """
    tsumo(self)のテスト
    """
    print("▶︎ tsumo(self)のテスト")

    assert Yama(rule()).tsumo() is not None

    yama = Yama(rule())
    initial_haisuu = yama.haisuu()
    yama.tsumo()
    assert initial_haisuu - 1 == yama.haisuu()

    yama = Yama(rule())
    while yama.haisuu() > 0:
        yama.tsumo()
    with pytest.raises(ValueError):
        yama.tsumo()

    with pytest.raises(ValueError):
        Yama(rule()).close().tsumo()


def test_kantsumo():
    """
    kantsumo(self)のテスト
    """
    print("▶︎ kantsumo(self)のテスト")

    assert Yama(rule()).kantsumo() is not None

    yama = Yama(rule())
    initial_haisuu = yama.haisuu()
    yama.kantsumo()
    assert initial_haisuu - 1 == yama.haisuu()

    yama = Yama(rule())
    yama.kantsumo()
    with pytest.raises(ValueError):
        yama.tsumo()

    yama = Yama(rule())
    yama.kantsumo()
    with pytest.raises(ValueError):
        yama.kantsumo()

    yama = Yama(rule())
    while yama.haisuu() > 0:
        yama.tsumo()
    with pytest.raises(ValueError):
        yama.kantsumo()

    with pytest.raises(ValueError):
        Yama(rule()).close().kantsumo()

    yama = Yama(rule())
    for _ in range(4):
        yama.kantsumo()
        yama.kaikan()
    with pytest.raises(ValueError):
        yama.kantsumo()

    yama = Yama(rule({"カンドラあり": False}))
    for _ in range(4):
        yama.kantsumo()
    assert len(yama.dora_indicator()) == 1
    with pytest.raises(ValueError):
        yama.kantsumo()


def test_kaikan():
    """
    kaikan(self)のテスト
    """
    print("▶︎ kaikan(self)のテスト")

    with pytest.raises(ValueError):
        Yama(rule()).kaikan()

    yama = Yama(rule())
    yama.kantsumo()
    assert yama.kaikan() is not None

    yama = Yama(rule())
    yama.kantsumo()
    assert len(yama.dora_indicator()) + 1 == len(yama.kaikan().dora_indicator())

    yama = Yama(rule())
    yama.kantsumo()
    assert len(yama.kaikan().close().uradora_indicator()) == 2

    yama = Yama(rule())
    yama.kantsumo()
    assert yama.kaikan().tsumo() is not None

    yama = Yama(rule())
    yama.kantsumo()
    assert yama.kaikan().kantsumo() is not None

    yama = Yama(rule())
    yama.kantsumo()
    with pytest.raises(ValueError):
        yama.close().kaikan()

    yama = Yama(rule({"カンドラあり": False}))
    yama.kantsumo()
    with pytest.raises(ValueError):
        yama.kaikan()

    yama = Yama(rule({"カン裏あり": False}))
    yama.kantsumo()
    assert len(yama.kaikan().close().uradora_indicator()) == 1

    yama = Yama(rule({"裏ドラあり": False}))
    yama.kantsumo()
    assert yama.kaikan().close().uradora_indicator() is None


def test_haisuu():
    """
    haisuu(self)のテスト
    """
    print("▶︎ haisuu(self)のテスト")

    assert Yama(rule()).haisuu() == 122


def test_dora_indicator():
    """
    dora_indicator(self)のテスト
    """
    print("▶︎ dora_indicator(self)のテスト")

    assert len(Yama(rule()).dora_indicator()) == 1


def test_uradora_indicator():
    """
    uradora_indicator(self)のテスト
    """
    print("▶︎ uradora_indicator(self)のテスト")

    assert Yama(rule()).uradora_indicator() is None
    assert Yama(rule({"裏ドラあり": False})).close().uradora_indicator() is None
    assert len(Yama(rule()).close().uradora_indicator()) == 1


if __name__ == "__main__":
    pytest.main()
