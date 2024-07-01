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

    hoora_result = hoora(
        Tehai.from_string("m22555p234777s78"),
        "s6=",
        hoora_param({"rule": rule({"クイタンあり": False})}),
    )
    assert hoora_result == {
        "yaku": [{"name": "断幺九", "hansuu": 1}],
        "fu": 40,
        "hansuu": 1,
        "yakuman": None,
        "tokuten": 1300,
        "bunpai": [0, 1300, 0, -1300],
    }


if __name__ == "__main__":
    pytest.main()
