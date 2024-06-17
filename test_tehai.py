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

    def test_action_tsumo(self):
        """
        action_tsumo(self, hai, check=True)のテスト
        """
        print("▶︎ action_tsumo(self, hai, check=True)のテスト")

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.action_tsumo("m1").to_string() == "m123p456s789z4567m1"

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.action_tsumo("p1").to_string() == "m123p456s789z4567p1"

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.action_tsumo("s1").to_string() == "m123p456s789z4567s1"

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.action_tsumo("z1").to_string() == "m123p456s789z4567z1"

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.action_tsumo("m0").to_string() == "m123p456s789z4567m0"

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.action_tsumo("_").to_string() == "m123p456s789z4567_"

        # with pytest.raises(ValueError):
        # Tehai.from_string("m123p456s789z4567").action_tsumo()

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").action_tsumo("z0")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").action_tsumo("z8")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").action_tsumo("mm")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").action_tsumo("xx")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z34567").action_tsumo("m1")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456z34567,s789-,").action_tsumo("m1")

        tehai = Tehai.from_string("m123p456s789z34567")
        assert (
            tehai.action_tsumo("m1", check=False).to_string() == "m123p456s789z34567m1"
        )

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z1111").action_tsumo("z1")

        with pytest.raises(ValueError):
            Tehai.from_string("m455556s789z1111").action_tsumo("m0")

    def test_dahai(self):
        """
        dahai(self, hai, check=True)のテスト
        """
        print("▶︎ dahai(self, hai, check=True)のテスト")

        tehai = Tehai.from_string("m123p456s789z34567")
        assert tehai.dahai("m1").to_string() == "m23p456s789z34567"

        tehai = Tehai.from_string("m123p456s789z34567")
        assert tehai.dahai("p4").to_string() == "m123p56s789z34567"

        tehai = Tehai.from_string("m123p456s789z34567")
        assert tehai.dahai("s7").to_string() == "m123p456s89z34567"

        tehai = Tehai.from_string("m123p456s789z34567")
        assert tehai.dahai("z3").to_string() == "m123p456s789z4567"

        tehai = Tehai.from_string("m123p406s789z34567")
        assert tehai.dahai("p0").to_string() == "m123p46s789z34567"

        tehai = Tehai.from_string("m123p456s789z34567")
        assert tehai.dahai("z7*").to_string() == "m123p456s789z3456*"

        tehai = Tehai.from_string("m123p456s789z11223*")
        assert tehai.dahai("z1").to_string() == "m123p456s789z1223*"

        tehai = Tehai.from_string("______________")
        assert tehai.dahai("m1").to_string() == "_____________"

        # with pytest.raises(ValueError):
        # Tehai.from_string("m123p456s789z34567").dahai()

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z34567").dahai("z0")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z34567").dahai("z8")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z34567").dahai("mm")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z34567").dahai("xx")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").dahai("_")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").dahai("m1")

        tehai = Tehai.from_string("m123p456s789z4567")
        assert tehai.dahai("m1", False).to_string() == "m23p456s789z4567"

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z34567").dahai("z1")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z34567").dahai("p0")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p406s789z34567").dahai("p5")

    def test_action_fuuro(self):
        """
        action_fuuro(self, mentsu, check=True)のテスト
        """
        print("▶︎ action_fuuro(self, mentsu, check=True)のテスト")

        tehai = Tehai.from_string("m23p456s789z34567")
        assert tehai.action_fuuro("m1-23").to_string() == "p456s789z34567,m1-23,"

        tehai = Tehai.from_string("m123p46s789z34567")
        assert tehai.action_fuuro("p45-6").to_string() == "m123s789z34567,p45-6,"

        tehai = Tehai.from_string("m123p456s99z34567")
        assert tehai.action_fuuro("s999+").to_string() == "m123p456z34567,s999+,"

        tehai = Tehai.from_string("m123p456s789z1167")
        assert tehai.action_fuuro("z111=").to_string() == "m123p456s789z67,z111=,"

        tehai = Tehai.from_string("m123p500s789z4567")
        assert tehai.action_fuuro("p5005-").to_string() == "m123s789z4567,p5005-"

        tehai = Tehai.from_string("m123p456s789z4567*")
        assert tehai.action_fuuro("m1-23").to_string() == "m1p456s789z4567*,m1-23,"

        tehai = Tehai.from_string("_____________")
        assert tehai.action_fuuro("m1-23").to_string() == "___________,m1-23,"

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").action_fuuro("z3-45")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z4567").action_fuuro("m231-")

        with pytest.raises(ValueError):
            Tehai.from_string("_____________").action_fuuro("m1111")

        with pytest.raises(ValueError):
            Tehai.from_string("_____________").action_fuuro("m111+1")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z11567").action_fuuro("z111=")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z22,z111=,").action_fuuro("z222=")

        tehai = Tehai.from_string("m123p456s789z11567")
        assert (
            tehai.action_fuuro("z111=", False).to_string() == "m123p456s789z567,z111=,"
        )

        tehai = Tehai.from_string("m123p456s789z22,z111=,")
        assert (
            tehai.action_fuuro("z222=", False).to_string()
            == "m123p456s789,z111=,z222=,"
        )

        with pytest.raises(ValueError):
            Tehai.from_string("m123p456s789z2,z111=").action_fuuro("z333=")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p40s789z22,z111=").action_fuuro("p456-")

        with pytest.raises(ValueError):
            Tehai.from_string("m123p45s789z22,z111=").action_fuuro("p406-")

    def test_kan(self):
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
        ]

        for tehai_string, mentsu, expected in test_cases:
            tehai = Tehai.from_string(tehai_string)
            assert tehai.kan(mentsu).to_string() == expected

        invalid_test_cases = [
            ("m1112456s789z4567", "m456-"),
            ("m1112456s789z4567", "m111+"),
            ("m1112456s789z4567", "m1112"),
            ("m2456s789z4567,m111+", "m111+2"),
            ("m1111p456s789z456", "m1111"),
            ("m1111s789z4567,p456-,", "m1111"),
            ("m1112p456s789z4567", "m1111"),
            ("m13p456s789z567,m222=", "m2222"),
            ("m10p456s789z567,m555=", "m5555"),
            ("m15p456s789z567,m555=", "m5550"),
            ("m12p456s789z567,m222=", "m111=1"),
        ]

        for tehai_string, mentsu in invalid_test_cases:
            tehai = Tehai.from_string(tehai_string)
            with pytest.raises(ValueError):
                tehai.kan(mentsu)

        tehai = Tehai.from_string("m1111p4444s789z567")
        with pytest.raises(ValueError):
            tehai.kan("m1111").kan("p4444")

        tehai = Tehai.from_string("m1111p456s789z456")
        assert tehai.kan("m1111", False).to_string() == "p456s789z456,m1111"

        tehai = Tehai.from_string("m1111s789z4567,p456-,")
        assert tehai.kan("m1111", False).to_string() == "s789z4567,p456-,m1111"

        tehai = Tehai.from_string("m1111p4444s789z567")
        assert (
            tehai.kan("m1111", False).kan("p4444", False).to_string()
            == "s789z567,m1111,p4444"
        )

    def test_menzen(self):
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

    def test_riichi(self):
        """
        get_riichi(self)のテスト
        """
        print("▶︎ get_riichi(self)のテスト")

        tehai = Tehai.from_string("_____________")
        assert not tehai.get_riichi()

        tehai = Tehai.from_string("_____________")
        assert tehai.action_tsumo("z7").dahai("z7_*").get_riichi()

    def test_get_dahai(self):
        """
        get_dahai(self, check=True)のテスト
        """
        print("▶︎ get_dahai(self, check=True)のテスト")

        invalid_test_cases = [
            "m123p406s789z4567",
            "m123p406s789z2,z111+",
            "_____________",
            "__________,z111+",
        ]

        for tehai_string in invalid_test_cases:
            tehai = Tehai.from_string(tehai_string)
            assert tehai.get_dahai() is None

        tehai = Tehai.from_string("m123p406s789z11123")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m123p406s789z12,z111+")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m123p456s789z1234m1*")
        assert tehai.get_dahai() == ["m1_"]

        tehai = Tehai.from_string("m123p405s789z11123")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m123p45s789z11123p0")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m123p45s789z11123p5")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m123p405s789z1112p0")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("______________")
        assert tehai.get_dahai() == []

        tehai = Tehai.from_string("___________,m123-,")
        assert tehai.get_dahai() == []

        tehai = Tehai.from_string("m145p406s789z23,m1-23,")
        assert tehai.get_dahai() == [
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

        tehai = Tehai.from_string("m145p406s789z23,m234-,")
        assert tehai.get_dahai() == [
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

        tehai = Tehai.from_string("m123p258s789z23,p45-6,")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m123p456s467z23,s7-89,")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m123p456s789z12,z111+,")
        assert tehai.get_dahai() == [
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
        ]

        tehai = Tehai.from_string("m256p456s789z12,m340-,")
        assert tehai.get_dahai() == [
            "m6",
            "p4",
            "p5",
            "p6",
            "s7",
            "s8",
            "s9",
            "z1",
            "z2",
        ]

        tehai = Tehai.from_string("m206p456s789z12,m345-,")
        assert tehai.get_dahai() == [
            "m6",
            "p4",
            "p5",
            "p6",
            "s7",
            "s8",
            "s9",
            "z1",
            "z2",
        ]

        tehai = Tehai.from_string("m25p1s12678,z666+,m550-,")
        assert tehai.get_dahai() == ["m2", "p1", "s1", "s2", "s6", "s7", "s8"]

        tehai = Tehai.from_string("m14,p456-,s789-,z111+,m234-,")
        assert tehai.get_dahai() == []

        tehai = Tehai.from_string("m14,p456-,s789-,z111+,m1-23,")
        assert tehai.get_dahai() == []

        tehai = Tehai.from_string("m22,p456-,s789-,z111+,m12-3,")
        assert tehai.get_dahai() == []

        tehai = Tehai.from_string("m145p406s789z23,m1-23,")
        assert tehai.get_dahai(check=False) == [
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

    def test_get_chii_mentsu(self):
        """
        get_chii_mentsu(self, hai, check=True)のテスト
        """
        print("▶︎ get_chii_mentsu(self, hai, check=True)のテスト")

        invalid_test_cases = [
            ("m123p456s789z12345", "m1-"),
            ("m123p456s789z12,z333=,", "m1-"),
            ("______________", "m1-"),
        ]

        for tehai_string, hai in invalid_test_cases:
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
            (
                "s6789,m123-,p456-,z111+",
                "s6-",
                ["s6-78"],
                False,
            ),
            ("s6789,m123-,p456-,z111+", "s9-", ["s789-"], False),
            ("s7889,m123-,p456-,z111+", "s8-", ["s78-9"], False),
            ("s7899,m123-,p456-,z111+", "s9-", ["s789-"], False),
            ("s7789,m123-,p456-,z111+", "s7-", ["s7-89"], False),
            ("s6678999,m123-,p456-", "s6-", ["s6-78"], False),
            ("m123p456s789z1234", "mm-", ValueError),
            ("m123p456s789z1234", "m1", ValueError),
            ("m123p456s789z1234", "z1-", []),
            ("m123p456s789z1234", "m1+", []),
            ("m123p456s789z1234", "m1=", []),
        ]

        for tehai_string, hai, expected, *args in test_cases:
            tehai = Tehai.from_string(tehai_string)
            if isinstance(expected, list):
                assert tehai.get_chii_mentsu(hai, *args) == expected
            else:
                with pytest.raises(expected):
                    tehai.get_chii_mentsu(hai, *args)


if __name__ == "__main__":
    pytest.main()
