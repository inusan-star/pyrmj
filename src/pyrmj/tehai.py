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

    @classmethod
    def from_string(cls, tehai_string=""):
        """
        牌姿からインスタンスを作成する
        """
        fuuro = tehai_string.split(",")
        juntehai = fuuro.pop(0)
        haipai = re.findall(r"_", juntehai) or []

        for hai in re.findall(r"[mpsz]\d+", juntehai) or []:
            suit = hai[0]

            for number in re.findall(r"\d", hai):
                if suit == "z" and (int(number) < 1 or 7 < int(number)):
                    continue

                haipai.append(f"{suit}{number}")

        haipai = haipai[: 14 - len([mentsu for mentsu in fuuro if mentsu]) * 3]
        tsumo = (len(haipai) - 2) % 3 == 0 and haipai[-1] or None
        tehai = cls(haipai)
        last = None

        for mentsu in fuuro:
            if not mentsu:
                tehai.tsumo_ = last
                break

            mentsu = cls.valid_mentsu(mentsu)

            if mentsu:
                tehai.fuuro_.append(mentsu)
                last = mentsu

        tehai.tsumo_ = tehai.tsumo_ or tsumo or None
        tehai.riichi_ = juntehai[-1:] == "*"
        return tehai

    def to_string(self):
        """
        牌姿を返す
        """
        tehai_string = "_" * (self.juntehai_["_"] + (-1 if self.tsumo_ == "_" else 0))

        for suit in ["m", "p", "s", "z"]:
            suit_string = suit
            juntehai = self.juntehai_[suit]
            n_akahai = 0 if suit == "z" else juntehai[0]

            for number in range(1, len(juntehai)):
                n_hai = juntehai[number]

                if self.tsumo_:
                    if f"{suit}{number}" == self.tsumo_:
                        n_hai -= 1

                    if number == 5 and f"{suit}0" == self.tsumo_:
                        n_hai -= 1
                        n_akahai -= 1

                for _ in range(n_hai):
                    if number == 5 and n_akahai > 0:
                        suit_string += "0"
                        n_akahai -= 1

                    else:
                        suit_string += str(number)

            if len(suit_string) > 1:
                tehai_string += suit_string

        if self.tsumo_ and len(self.tsumo_) <= 2:
            tehai_string += self.tsumo_

        if self.riichi_:
            tehai_string += "*"

        for mentsu in self.fuuro_:
            tehai_string += f",{mentsu}"

        if self.tsumo_ and 2 < len(self.tsumo_):
            tehai_string += ","

        return tehai_string

    def clone(self):
        """
        インスタンスのクローンを作成する
        """
        tehai = Tehai()
        tehai.juntehai_ = {
            "_": self.juntehai_["_"],
            "m": self.juntehai_["m"][:],
            "p": self.juntehai_["p"][:],
            "s": self.juntehai_["s"][:],
            "z": self.juntehai_["z"][:],
        }
        tehai.fuuro_ = self.fuuro_[:]
        tehai.tsumo_ = self.tsumo_
        tehai.riichi_ = self.riichi_
        return tehai

    def update_from_string(self, tehai_string):
        """
        牌姿からインスタンスを置き換える
        """
        tehai = self.from_string(tehai_string)
        self.juntehai_ = {
            "_": tehai.juntehai_["_"],
            "m": tehai.juntehai_["m"][:],
            "p": tehai.juntehai_["p"][:],
            "s": tehai.juntehai_["s"][:],
            "z": tehai.juntehai_["z"][:],
        }
        self.fuuro_ = tehai.fuuro_[:]
        self.tsumo_ = tehai.tsumo_
        self.riichi_ = tehai.riichi_
        return self

    def tsumo(self, hai, check=True):
        """
        牌を引く
        """
        if check and self.tsumo_:
            raise ValueError("Already tsumoed")

        if hai == "_":
            self.juntehai_["_"] += 1
            self.tsumo_ = hai

        else:
            if not self.valid_hai(hai):
                raise ValueError(f"Invalid hai: {hai}")

            suit, number = hai[0], int(hai[1])
            juntehai = self.juntehai_[suit]

            if juntehai[number] == 4:
                raise ValueError(f"Too many hais: {hai}")

            juntehai[number] += 1

            if number == 0:
                if juntehai[5] == 4:
                    raise ValueError(f"Too many hais: {hai}")

                juntehai[5] += 1

            self.tsumo_ = f"{suit}{number}"

        return self

    def decrease(self, suit, number):
        """
        指定された牌を減らす
        """
        juntehai = self.juntehai_[suit]

        if juntehai[number] == 0 or (number == 5 and juntehai[0] == juntehai[5]):
            if self.juntehai_["_"] == 0:
                raise ValueError("There are no hidden hais")

            self.juntehai_["_"] -= 1

        else:
            juntehai[number] -= 1

            if number == 0:
                juntehai[5] -= 1

    def dahai(self, hai, check=True):
        """
        打牌する
        """
        if check and not self.tsumo_:
            raise ValueError("Not yet tsumoed")

        if not self.valid_hai(hai):
            raise ValueError(f"Invalid hai: {hai}")

        suit, number = hai[0], int(hai[1])
        self.decrease(suit, number)
        self.tsumo_ = None

        if hai[-1] == "*":
            self.riichi_ = True

        return self

    def fuuro(self, mentsu, check=True):
        """
        副露する
        """
        if check and self.tsumo_:
            raise ValueError("Already tsumoed")

        if mentsu != self.valid_mentsu(mentsu):
            raise ValueError(f"Invalid mentsu: {mentsu}")

        if re.search(r"\d{4}$", mentsu):
            raise ValueError("Invalid action: ankan")

        if re.search(r"\d{3}[\+\=\-]\d$", mentsu):
            raise ValueError("Invalid action: kakan")

        suit = mentsu[0]

        for number in re.findall(r"\d(?![\+\=\-])", mentsu):
            self.decrease(suit, int(number))

        self.fuuro_.append(mentsu)

        if not re.search(r"\d{4}", mentsu):
            self.tsumo_ = mentsu

        return self

    def kan(self, mentsu, check=True):
        """
        カン（暗槓/加槓）する
        """
        if check and not self.tsumo_:
            raise ValueError("Already tsumoed")

        if check and len(self.tsumo_) > 2:
            raise ValueError("Already tsumoed")

        if mentsu != self.valid_mentsu(mentsu):
            raise ValueError(f"Invalid mentsu: {mentsu}")

        suit = mentsu[0]

        if re.search(r"\d{4}$", mentsu):
            for number in re.findall(r"\d", mentsu):
                self.decrease(suit, int(number))

            self.fuuro_.append(mentsu)

        elif re.search(r"\d{3}[\+\=\-]\d$", mentsu):
            mentsu1 = mentsu[:5]
            index = (i for i, mentsu2 in enumerate(self.fuuro_) if mentsu1 == mentsu2)
            target_index = next(index, -1)

            if target_index < 0:
                raise ValueError("Invalid kakan")

            self.fuuro_[target_index] = mentsu
            self.decrease(suit, int(mentsu[-1]))

        else:
            raise ValueError("Invalid action")

        self.tsumo_ = None
        return self
