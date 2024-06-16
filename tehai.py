import re


class Tehai:
    """
    手牌を表すクラス
    """

    def __init__(self, haipai=None):
        if haipai is None:
            haipai = []

        self.juntehai = {
            "_": 0,
            "m": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "p": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "s": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "z": [0, 0, 0, 0, 0, 0, 0, 0],
        }
        self.furo = []
        self.tsumo = None
        self.richi = False

        for hai in haipai:
            if hai == "_":
                self.juntehai["_"] += 1
                continue

            if not (hai := self.valid_hai(hai)):
                raise ValueError("Invalid")

            s, n = hai[0], int(hai[1])

            if self.juntehai[s][n] == 4:
                raise ValueError("Too many")

            self.juntehai[s][n] += 1

            if s != "z" and n == 0:
                self.juntehai[s][5] += 1

    @staticmethod
    def valid_hai(hai):
        """
        牌として有効かどうかを判定する
        """
        if re.match(r"^(?:[mps]\d|z[1-7])_?\*?[\+\=\-]?$", hai):
            return hai

        return None

    @staticmethod
    def valid_mentsu(mentsu):
        """
        面子として有効かどうかを判定する
        """
        if re.match(r"^z.*[089]", mentsu):
            return None

        black_mentsu = re.sub(r"0", "5", mentsu)

        if re.match(r"^[mpsz](\d)\1\1[\+\=\-]\1?$", black_mentsu):
            return re.sub(r"([mps])05", r"\g<1>" + "50", mentsu)

        elif re.match(r"^[mpsz](\d)\1\1\1[\+\=\-]?$", black_mentsu):
            sorted_mentsu = "".join(
                sorted(re.findall(r"\d(?![\+\=\-])", mentsu), reverse=True)
            )
            return (
                mentsu[0]
                + sorted_mentsu
                + (re.search(r"\d[\+\=\-]$", mentsu) or [""])[0]
            )

        elif re.match(r"^[mps]\d+\-\d*$", black_mentsu):
            akahai = re.search(r"0", mentsu)
            numbers = sorted(map(int, re.findall(r"\d", black_mentsu)))

            if len(numbers) != 3:
                return None

            if numbers[0] + 1 != numbers[1] or numbers[1] + 1 != numbers[2]:
                return None

            black_mentsu = black_mentsu[0] + "".join(
                sorted(re.findall(r"\d[\+\=\-]?", black_mentsu))
            )
            return re.sub(r"5", "0", black_mentsu) if akahai else black_mentsu

        return None

    @classmethod
    def from_string(cls, tehai_string=""):
        """
        文字列からTehaiクラスのインスタンスを生成する
        """
        furo = tehai_string.split(",")
        juntehai = furo.pop(0)
        haipai = re.findall(r"_", juntehai) or []

        for suit_string in re.findall(r"[mpsz]\d+", juntehai) or []:
            s = suit_string[0]

            for n in re.findall(r"\d", suit_string):
                if s == "z" and (int(n) < 1 or 7 < int(n)):
                    continue
                haipai.append(s + n)

        haipai = haipai[: 14 - len([x for x in furo if x]) * 3]
        tsumo = (len(haipai) - 2) % 3 == 0 and haipai[-1] or None
        tehai = cls(haipai)
        last = None

        for mentsu in furo:
            if not mentsu:
                tehai.tsumo = last
                break

            mentsu = cls.valid_mentsu(mentsu)

            if mentsu:
                tehai.furo.append(mentsu)
                last = mentsu

        tehai.tsumo = tehai.tsumo or tsumo or None
        tehai.richi = juntehai[-1] == "*"
        return tehai
