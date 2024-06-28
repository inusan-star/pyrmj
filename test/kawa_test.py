import pytest
from pyrmj import Kawa


def test_class_exists():
    """
    クラスが存在することのテスト
    """
    print("▶︎ クラスが存在することのテスト")

    assert Kawa is not None


def test___init__():
    """
    __init__(self)のテスト
    """
    print("▶︎ __init__(self)のテスト")

    assert Kawa() is not None
    assert len(Kawa().hai_) == 0


def test_dahai():
    """
    dahai(self, hai)のテスト
    """
    print("▶︎ dahai(self, hai)のテスト")

    with pytest.raises(ValueError):
        Kawa().dahai("z8")

    kawa = Kawa()
    assert len(kawa.hai_) + 1 == len(kawa.dahai("m1").hai_)

    test_cases = ["m1_", "m1*", "m1_*"]

    for hai in test_cases:
        assert Kawa().dahai(hai).hai_.pop() == hai


def test_fuuro():
    """
    fuuro(self, mentsu)のテスト
    """
    print("▶︎ fuuro(self, mentsu)のテスト")

    test_cases = [("m1", "m1-"), ("m1", "m1111"), ("m1", "m12-3")]

    for hai, mentsu in test_cases:
        with pytest.raises(ValueError):
            Kawa().dahai(hai).fuuro(mentsu)

    kawa = Kawa().dahai("m1_")
    assert len(kawa.hai_) == len(kawa.fuuro("m111+").hai_)

    kawa = Kawa().dahai("m2*")
    assert kawa.fuuro("m12-3").hai_.pop() == "m2*-"


if __name__ == "__main__":
    pytest.main()
