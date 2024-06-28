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

    assert Kawa().dahai("m1_").hai_.pop() == "m1_"
    assert Kawa().dahai("m1*").hai_.pop() == "m1*"
    assert Kawa().dahai("m1_*").hai_.pop() == "m1_*"


if __name__ == "__main__":
    pytest.main()
