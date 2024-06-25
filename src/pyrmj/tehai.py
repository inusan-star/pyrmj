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

    @staticmethod
    def valid_mentsu(mentsu):
        """
        面子として有効か判定する
        """
        if re.match(r"^z.*[089]", mentsu):
            return None

        black_mentsu = mentsu.replace("0", "5")

        if re.match(r"^[mpsz](\d)\1\1[\+\=\-]\1?$", black_mentsu):
            return re.sub(r"([mps])05", r"\g<1>" + "50", mentsu)

        elif re.match(r"^[mpsz](\d)\1\1\1[\+\=\-]?$", black_mentsu):
            sorted_mentsu = "".join(sorted(re.findall(r"\d(?![\+\=\-])", mentsu), reverse=True))
            return mentsu[0] + sorted_mentsu + (re.search(r"\d[\+\=\-]$", mentsu) or [""])[0]

        elif re.match(r"^[mps]\d+\-\d*$", black_mentsu):
            akahai = re.search(r"0", mentsu)
            numbers = sorted(map(int, re.findall(r"\d", black_mentsu)))

            if len(numbers) != 3:
                return None

            if numbers[0] + 1 != numbers[1] or numbers[1] + 1 != numbers[2]:
                return None

            black_mentsu = black_mentsu[0] + "".join(sorted(re.findall(r"\d[\+\=\-]?", black_mentsu)))
            return black_mentsu.replace("5", "0") if akahai else black_mentsu

        return None
