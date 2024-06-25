import re


class Tehai:
    """
    手牌を表すクラス
    """

    def __init__(self, haipai=None):
        if haipai is None:
            haipai = []

        self.juntehai_ = {
            "_": 0,
            "m": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "p": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "s": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "z": [0, 0, 0, 0, 0, 0, 0, 0],
        }
        self.fuuro_ = []
        self.tsumo_ = None
        self.riichi_ = False

        for hai in haipai:
            if hai == "_":
                self.juntehai_["_"] += 1
                continue

            if not self.valid_hai(hai):
                raise ValueError(f"Invalid hai: {hai}")

            suit, number = hai[0], int(hai[1])

            if self.juntehai_[suit][number] == 4:
                raise ValueError(f"Too many hais: {hai}")

            self.juntehai_[suit][number] += 1

            if suit != "z" and number == 0:
                self.juntehai_[suit][5] += 1

    @staticmethod
    def valid_hai(hai):
        """
        牌として有効か判定する
        """
        if re.match(r"^(?:[mps]\d|z[1-7])_?\*?[\+\=\-]?$", hai):
            return hai
        return None
