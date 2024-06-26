import random
from pyrmj import Tehai


class Yama:
    """
    牌山を表すクラス
    """

    def __init__(self, rule):
        random.seed(1704034800)  # シード値を設定（Time stamp of 1/1/2024）
        self.rule_ = rule
        akahai = rule["赤牌"]
        hai = []

        for suit in ["m", "p", "s", "z"]:
            for number in range(1, 8 if suit == "z" else 10):
                for i in range(4):
                    if number == 5 and i < akahai.get(suit, 0):
                        hai.append(f"{suit}0")

                    else:
                        hai.append(f"{suit}{number}")

        random.shuffle(hai)
        self.hai_ = hai
        self.dora_indicator_ = [self.hai_[4]]
        self.uradora_indicator_ = [self.hai_[9]] if rule["裏ドラあり"] else None
        self.not_yet_kaikan_ = False
        self.closed_ = False

    @staticmethod
    def dora(hai):
        """
        ドラを返す
        """
        if not Tehai.valid_hai(hai):
            raise ValueError(f"Invalid hai: {hai}")

        suit, number = hai[0], int(hai[1]) if hai[1] != "0" else 5

        if suit == "z":
            if number < 5:
                return f"{suit}{number % 4 + 1}"

            else:
                return f"{suit}{(number - 4) % 3 + 5}"

        else:
            return f"{suit}{number % 9 + 1}"

    def tsumo(self):
        """
        次のツモ牌を返す
        """
        if self.closed_:
            raise ValueError("Yama is closed")

        if self.haisuu() == 0:
            raise ValueError("No hais left")

        if self.not_yet_kaikan_:
            raise ValueError("Not yet kaikaned")

        return self.hai_.pop()

    def kantsumo(self):
        """
        次の槓ツモ牌を返す
        """
        if self.closed_:
            raise ValueError("Yama is closed")

        if self.haisuu() == 0:
            raise ValueError("No hais left")

        if self.not_yet_kaikan_:
            raise ValueError("Not yet kaikaned")

        if len(self.dora_indicator_) == 5:
            raise ValueError("Too many doras")

        self.not_yet_kaikan_ = self.rule_["カンドラあり"]

        if not self.not_yet_kaikan_:
            self.dora_indicator_.append("")

        return self.hai_.pop(0)

    def kaikan(self):
        """
        槓ドラを増やす
        """
        if self.closed_:
            raise ValueError("Yama is closed")

        if not self.not_yet_kaikan_:
            raise ValueError("Already kaikaned")

        self.dora_indicator_.append(self.hai_[4])

        if self.uradora_indicator_ and self.rule_["カン裏あり"]:
            self.uradora_indicator_.append(self.hai_[9])

        self.not_yet_kaikan_ = False
        return self

    def close(self):
        """
        牌山を固定する
        """
        self.closed_ = True
        return self

    def haisuu(self):
        """
        残り牌数を返す
        """
        return len(self.hai_) - 14

    def dora_indicator(self):
        """
        ドラ表示牌を返す
        """
        return [d for d in self.dora_indicator_ if d]

    def uradora_indicator(self):
        """
        裏ドラ表示牌を返す
        """
        if not self.closed_:
            return None

        return self.uradora_indicator_.copy() if self.uradora_indicator_ else None
