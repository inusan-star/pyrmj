import pytest
from tehai import Tehai


class TestTehai:
    """
    Tehaiクラスのテスト
    """

    def test_class_exists(self):
        """
        クラスが存在することのテスト
        """
        print("▶︎ クラスが存在することのテスト")

        print("クラスが存在すること")
        assert Tehai is not None

    def test___init__(self):
        """
        __init__(self, haipai=None)のテスト
        """
        print("▶︎ __init__(self, haipai=None)のテスト")

        print("インスタンスが生成できること")
        assert Tehai() is not None

        print("配牌を指定してインスタンスが生成できること")
        haipai = [
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
        ]
        assert Tehai(haipai) is not None

        print("裏向きの牌を指定してインスタンスが生成できること")
        assert Tehai(["_"]) is not None

        print("不正な牌を含む配牌で例外が発生すること")
        with pytest.raises(ValueError):
            Tehai(["z0"])

        print("5枚目の牌を含む配牌で例外が発生すること")
        with pytest.raises(ValueError):
            Tehai(["m1", "m1", "m1", "m1", "m1"])

    def test_valid_hai(self):
        """
        valid_hai(hai)のテスト
        """
        print("▶︎ valid_hai(hai)のテスト")

        test_cases = [
            ("m1", "m1", "m1    : 正常"),
            ("p2_", "p2_", "p2_   : 正常(ツモ切り)"),
            ("s3*", "s3*", "s3*   : 正常(リーチ)"),
            ("z4_*", "z4_*", "z4_*  : 正常(ツモ切り・リーチ)"),
            ("m0-", "m0-", "m0-   : 正常(被副露)"),
            ("p5_+", "p5_+", "p5_+  : 正常(ツモ切り・被副露)"),
            ("s6*=", "s6*=", "s6*=  : 正常(リーチ・被副露)"),
            ("z7_*-", "z7_*-", "z7_*- : 正常(ツモ切り・リーチ・被副露)"),
            ("_", None, "_     : 不正(裏向き牌)"),
            ("x", None, "x     : 不正"),
            ("mm", None, "mm    : 不正"),
            ("z0", None, "z0    : 不正"),
            ("z8", None, "z8    : 不正"),
            ("m9x", None, "m9x   : 不正"),
            ("m9=*", None, "m9=*  : 不正"),
            ("m9*_", None, "m9*_  : 不正"),
            ("m9=_", None, "m9=_  : 不正"),
        ]

        for val, expected, description in test_cases:
            print(description)
            assert Tehai.valid_hai(val) == expected

    def test_valid_mentsu(self):
        """
        valid_mentsu(mentsu)のテスト
        """
        print("▶︎ valid_mentsu(mentsu)のテスト")

        test_cases = [
            ("m111+", "m111+", "m111+  : 正常"),
            ("p555=", "p555=", "p555=  : 正常"),
            ("s999-", "s999-", "s999-  : 正常"),
            ("z777+7", "z777+7", "z777+7 : 正常"),
            ("m2222", "m2222", "m2222  : 正常"),
            ("p550=", "p550=", "p550=  : 正常"),
            ("p5550=", "p5550=", "p5550= : 正常"),
            ("p055=", "p505=", "p055=  : 正常 => p505="),
            ("p055=0", "p505=0", "p055=0 : 正常 => p505=0"),
            ("p000=0", "p000=0", "p000=0 : 正常"),
            ("s0555-", "s5505-", "s0555- : 正常 => s5505-"),
            ("s0055-", "s5005-", "s0055- : 正常 => s5005-"),
            ("s0005", "s5000", "s0005  : 正常 => s5000"),
            ("s0000", "s0000", "s0000  : 正常"),
            ("m1-23", "m1-23", "m1-23  : 正常"),
            ("m12-3", "m12-3", "m12-3  : 正常"),
            ("m123-", "m123-", "m123-  : 正常"),
            ("m231-", "m1-23", "m231-  : 正常 => m1-23"),
            ("m312-", "m12-3", "m312-  : 正常 => m12-3"),
            ("m3-12", "m123-", "m3-12  : 正常 => m123-"),
            ("m460-", "m40-6", "m460-  : 正常 => m40-6"),
            ("m1234-", None, "m1234- : 不正"),
            ("m135-", None, "m135-  : 不正"),
            ("m1234", None, "m1234  : 不正"),
            ("m123", None, "m123   : 不正"),
            ("m111", None, "m111   : 不正"),
            ("z111=0", None, "z111=0 : 不正"),
        ]

        for val, expected, description in test_cases:
            print(description)
            assert Tehai.valid_mentsu(val) == expected


if __name__ == "__main__":
    pytest.main()
