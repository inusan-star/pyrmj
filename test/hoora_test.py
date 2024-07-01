import pytest
from pyrmj import Tehai, hoora_mentsu, hoora_param, hoora, rule


def test_hoora_mentsu():
    """
    hoora_mentsu(tehai, ron_hai=None)のテスト
    """
    print("▶︎ hoora_mentsu(tehai, ron_hai=None)のテスト")

    test_cases = [
        ("m123p055s789z11122", None, [["z22_!", "m123", "p555", "s789", "z111"]]),
        ("m123p055s789z1112", "z2+", [["z22+!", "m123", "p555", "s789", "z111"]]),
        ("m123p055z1112,s7-89", "z2=", [["z22=!", "m123", "p555", "z111", "s7-89"]]),
        ("m225p4466s1199z33", "m0-", [["m22", "m55-!", "p44", "p66", "s11", "s99", "z33"]]),
        (
            "m9p19s19z12345677m1",
            None,
            [["z77", "m1_!", "m9", "p1", "p9", "s1", "s9", "z1", "z2", "z3", "z4", "z5", "z6"]],
        ),
        (
            "m19p19s19z1234567",
            "m9+",
            [["m99+!", "m1", "p1", "p9", "s1", "s9", "z1", "z2", "z3", "z4", "z5", "z6", "z7"]],
        ),
        ("m1112345678999", "m0=", [["m55=!", "m111", "m234", "m678", "m999"], ["m11123456789995=!"]]),
        ("___m123p055z2,s7-89", "z2=", []),
        ("m19p19s19z123456", "z7=", []),
        ("m111234567899", "m9=", []),
        ("m111123p789999z1z1", None, [["z11_!", "m123", "m111", "p789", "p999"]]),
    ]

    for tehai_string, ron_hai, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert hoora_mentsu(tehai, ron_hai) == expected

    test_cases = [
        ("m123p055s789z1122", []),
        ("m22", []),
        (
            "m223344p556677s88",
            [["s88_!", "m234", "m234", "p567", "p567"], ["m22", "m33", "m44", "p55", "p66", "p77", "s88_!"]],
        ),
        (
            "m111222333p89997",
            [["p99", "m123", "m123", "m123", "p7_!89"], ["p99", "m111", "m222", "m333", "p7_!89"]],
        ),
        (
            "m2234455p234s234m3",
            [["m22", "m3_!45", "m345", "p234", "s234"], ["m55", "m23_!4", "m234", "p234", "s234"]],
        ),
        (
            "m23p567s33345666m1",
            [["s33", "m1_!23", "p567", "s345", "s666"], ["s66", "m1_!23", "p567", "s333", "s456"]],
        ),
        ("s1113445678999s2", [["s99", "s111", "s2_!34", "s456", "s789"], ["s11134456789992_!"]]),
        ("s4067999z444s8,s8888", [["s99", "s456", "s78_!9", "z444", "s8888"]]),
    ]

    for tehai_string, expected in test_cases:
        tehai = Tehai.from_string(tehai_string)
        assert hoora_mentsu(tehai) == expected


def test_hoora():
    """
    hoora(tehai, ron_hai, param)のテスト
    """
    print("▶︎ hoora(tehai, ron_hai, param)のテスト")

    hoora_result = hoora(
        Tehai.from_string("m123p123z1z1,s1-23,z555="),
        None,
        hoora_param({"zikaze": 0, "rule": rule({"連風牌は2符": True})}),
    )
    assert hoora_result.get("fu") == 30

    hoora_result = hoora(
        Tehai.from_string("m22555p234s78,p777-"),
        "s6=",
        hoora_param({"rule": rule({"クイタンあり": False})}),
    )
    assert hoora_result.get("yaku") is None

    test_cases = [
        (
            "m22555p234777s78",
            "s6=",
            {"rule": rule({"クイタンあり": False})},
            {
                "yaku": [{"name": "断幺九", "hansuu": 1}],
                "fu": 40,
                "hansuu": 1,
                "yakuman": None,
                "tokuten": 1300,
                "bunpai": [0, 1300, 0, -1300],
            },
        ),
        (
            "m19p19s19z1234567",
            "m1+",
            {"rule": rule({"ダブル役満あり": False})},
            {
                "yaku": [{"name": "国士無双十三面", "hansuu": "*"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 1,
                "tokuten": 32000,
                "bunpai": [0, 32000, -32000, 0],
            },
        ),
        (
            "m111p333s777z111m3",
            "m3=",
            {"rule": rule({"ダブル役満あり": False})},
            {
                "yaku": [{"name": "四暗刻単騎", "hansuu": "*"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 1,
                "tokuten": 32000,
                "bunpai": [0, 32000, 0, -32000],
            },
        ),
        (
            "m22z22244,z333+,z111-",
            "z4=",
            {"rule": rule({"ダブル役満あり": False})},
            {
                "yaku": [{"name": "大四喜", "hansuu": "*"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 1,
                "tokuten": 32000,
                "bunpai": [0, 32000, 0, -32000],
            },
        ),
        (
            "m1112345678999",
            "m2=",
            {"rule": rule({"ダブル役満あり": False})},
            {
                "yaku": [{"name": "純正九蓮宝燈", "hansuu": "*"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 1,
                "tokuten": 32000,
                "bunpai": [0, 32000, 0, -32000],
            },
        ),
        (
            "z77,z111-,z2222,z333=3,z444+",
            None,
            {"riichibou": 1, "tsumibou": 1, "rule": rule({"役満の複合あり": False})},
            {
                "yaku": [{"name": "大四喜", "hansuu": "**", "houjuusha": "+"}, {"name": "字一色", "hansuu": "*"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 1,
                "tokuten": 32000,
                "bunpai": [0, 33300, -32300, 0],
            },
        ),
        (
            "z7,z111-,z2222,z333=3,z444+",
            "z7-",
            {"riichibou": 1, "tsumibou": 1, "rule": rule({"役満の複合あり": False})},
            {
                "yaku": [{"name": "大四喜", "hansuu": "**", "houjuusha": "+"}, {"name": "字一色", "hansuu": "*"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 1,
                "tokuten": 32000,
                "bunpai": [-16300, 33300, -16000, 0],
            },
        ),
        (
            "m2234,z555-5,z6666,z777+",
            "m5=",
            {"rule": rule({"役満パオあり": False})},
            {
                "yaku": [{"name": "大三元", "hansuu": "*"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 1,
                "tokuten": 32000,
                "bunpai": [0, 32000, 0, -32000],
            },
        ),
        (
            "m2,z222+,z4444,z333+,z111-",
            "m2=",
            {"rule": rule({"役満パオあり": False})},
            {
                "yaku": [{"name": "大四喜", "hansuu": "**"}],
                "fu": None,
                "hansuu": None,
                "yakuman": 2,
                "tokuten": 64000,
                "bunpai": [0, 64000, 0, -64000],
            },
        ),
        (
            "p22334455667788*",
            None,
            {"riichi": 1, "rule": rule({"数え役満あり": False})},
            {
                "yaku": [
                    {"name": "立直", "hansuu": 1},
                    {"name": "門前清自摸和", "hansuu": 1},
                    {"name": "平和", "hansuu": 1},
                    {"name": "断幺九", "hansuu": 1},
                    {"name": "二盃口", "hansuu": 3},
                    {"name": "清一色", "hansuu": 6},
                ],
                "fu": 20,
                "hansuu": 13,
                "yakuman": None,
                "tokuten": 24000,
                "bunpai": [-12000, 24000, -6000, -6000],
            },
        ),
        (
            "m22z111p445566s789",
            None,
            {"bakaze": 1, "zikaze": 0, "rule": rule({"切り上げ満貫あり": True})},
            {
                "yaku": [
                    {"name": "門前清自摸和", "hansuu": 1},
                    {"name": "自風 東", "hansuu": 1},
                    {"name": "一盃口", "hansuu": 1},
                ],
                "fu": 30,
                "hansuu": 3,
                "yakuman": None,
                "tokuten": 6000,
                "bunpai": [6000, -2000, -2000, -2000],
            },
        ),
        (
            "m11z111p123789s789",
            None,
            {"rule": rule({"切り上げ満貫あり": True})},
            {
                "yaku": [
                    {"name": "門前清自摸和", "hansuu": 1},
                    {"name": "場風 東", "hansuu": 1},
                    {"name": "混全帯幺九", "hansuu": 2},
                ],
                "fu": 30,
                "hansuu": 4,
                "yakuman": None,
                "tokuten": 8000,
                "bunpai": [-4000, 8000, -2000, -2000],
            },
        ),
        (
            "m11222789,z2222,m444=",
            None,
            {"bakaze": 1, "zikaze": 0, "rule": rule({"切り上げ満貫あり": True})},
            {
                "yaku": [{"name": "場風 南", "hansuu": 1}, {"name": "混一色", "hansuu": 2}],
                "fu": 60,
                "hansuu": 3,
                "yakuman": None,
                "tokuten": 12000,
                "bunpai": [12000, -4000, -4000, -4000],
            },
        ),
    ]

    for tehai_string, ron_hai, param, expected in test_cases:
        assert hoora(Tehai.from_string(tehai_string), ron_hai, hoora_param(param)) == expected


if __name__ == "__main__":
    pytest.main()
