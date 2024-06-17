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

        assert Tehai is not None

    def test___init__(self):
        """
        __init__(self, haipai=None)のテスト
        """
        print("▶︎ __init__(self, haipai=None)のテスト")

        assert Tehai() is not None

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

        assert Tehai(["_"]) is not None

        with pytest.raises(ValueError):
            Tehai(["z0"])

        with pytest.raises(ValueError):
            Tehai(["m1", "m1", "m1", "m1", "m1"])

    def test_valid_hai(self):
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
            assert Tehai.valid_hai(hai) == expected

    def test_valid_mentsu(self):
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
            assert Tehai.valid_mentsu(mentsu) == expected

    def test_from_string(self):
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

    def test_clone(self):
        """
        clone(self)のテスト
        """
        print("▶︎ clone(self)のテスト")

        tehai = Tehai()
        assert tehai != tehai.clone()

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.to_string() == tehai.clone().to_string()

        tehai = Tehai.from_string("m1,p123-,s555=,z777+7,m9999")
        assert tehai.to_string() == tehai.clone().to_string()

        tehai = Tehai.from_string("m11123456789991")
        assert tehai.to_string() == tehai.clone().to_string()

        tehai = Tehai.from_string("m123p456s789z1112*")
        assert tehai.to_string() == tehai.clone().to_string()

        tehai = Tehai.from_string("___________,m123-")
        assert tehai.to_string() == tehai.clone().to_string()

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.to_string() != tehai.clone().action_tsumo("m1").to_string()

        tehai = Tehai.from_string("m123p456s789z34567")
        assert tehai.to_string() != tehai.clone().dahai("m1").to_string()

        tehai = Tehai.from_string("m123p456s789z1167")
        assert tehai.to_string() != tehai.clone().action_fuuro("z111=").to_string()

        tehai = Tehai.from_string("m123p456s789z11112")
        assert tehai.to_string() != tehai.clone().kan("z1111").to_string()

        tehai = Tehai.from_string("m123p456s789z11223")
        assert tehai.to_string() != tehai.clone().dahai("z3*").to_string()

    def test_update_from_string(self):
        """
        update_from_string(self, tehai_string)のテスト
        """
        print("▶︎ update_from_string(self, tehai_string)のテスト")

        test_cases = [
            ("m123p456s789z1122z2", "m123p456s789z1122z2"),
            ("m123p456s789z2,z111=", "m123p456s789z2,z111="),
            ("m123p456s789z1122*", "m123p456s789z1122*"),
            ("__________,z111=", "__________,z111="),
        ]

        for tehai_string, expected in test_cases:
            assert Tehai().update_from_string(tehai_string).to_string() == expected


if __name__ == "__main__":
    pytest.main()
