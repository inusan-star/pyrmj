import pytest
from pyrmj import Yama


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

    for rule, expected in test_cases:
        yama = Yama(rule)
        assert ",".join(sorted(yama.hai_)) == expected


if __name__ == "__main__":
    pytest.main()
