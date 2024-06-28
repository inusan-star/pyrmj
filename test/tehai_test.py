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
            None,
        ),
        (["_"], None),
        (["z0"], ValueError),
        (["m1", "m1", "m1", "m1", "m1"], ValueError),
    ]

    for haipai, expected in test_cases:
        if expected is None:
            assert Tehai(haipai) is not None

        else:
            with pytest.raises(expected):
                Tehai(haipai)


if __name__ == "__main__":
    pytest.main()
