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
        self.fuuro = []
        self.tsumo = None
        self.riichi = False

        for hai in haipai:
            if hai == "_":
                self.juntehai["_"] += 1
                continue

            if not self.valid_hai(hai):
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
        牌姿からインスタンスを作成する
        """
        fuuro = tehai_string.split(",")
        juntehai = fuuro.pop(0)
        haipai = re.findall(r"_", juntehai) or []

        for suit_string in re.findall(r"[mpsz]\d+", juntehai) or []:
            s = suit_string[0]

            for n in re.findall(r"\d", suit_string):
                if s == "z" and (int(n) < 1 or 7 < int(n)):
                    continue
                haipai.append(s + n)

        haipai = haipai[: 14 - len([x for x in fuuro if x]) * 3]
        tsumo = (len(haipai) - 2) % 3 == 0 and haipai[-1] or None
        tehai = cls(haipai)
        last = None

        for mentsu in fuuro:
            if not mentsu:
                tehai.tsumo = last
                break

            mentsu = cls.valid_mentsu(mentsu)

            if mentsu:
                tehai.fuuro.append(mentsu)
                last = mentsu

        tehai.tsumo = tehai.tsumo or tsumo or None
        tehai.riichi = juntehai[-1:] == "*"
        return tehai

    def to_string(self):
        """
        牌姿を返す
        """
        tsumo_offset = -1 if self.tsumo == "_" else 0
        tehai_string = "_" * (self.juntehai["_"] + tsumo_offset)

        for s in ["m", "p", "s", "z"]:
            suit_string = s
            juntehai = self.juntehai[s]
            n_akahai = 0 if s == "z" else juntehai[0]

            for n in range(1, len(juntehai)):
                n_hai = juntehai[n]

                if self.tsumo:
                    if s + str(n) == self.tsumo:
                        n_hai -= 1

                    if n == 5 and s + "0" == self.tsumo:
                        n_hai -= 1
                        n_akahai -= 1

                for _ in range(n_hai):
                    if n == 5 and n_akahai > 0:
                        suit_string += "0"
                        n_akahai -= 1

                    else:
                        suit_string += str(n)

            if len(suit_string) > 1:
                tehai_string += suit_string

        if self.tsumo and len(self.tsumo) <= 2:
            tehai_string += self.tsumo

        if self.riichi:
            tehai_string += "*"

        for mentsu in self.fuuro:
            tehai_string += "," + mentsu

        if self.tsumo and len(self.tsumo) > 2:
            tehai_string += ","

        return tehai_string

    def clone(self):
        """
        インスタンスのクローンを作成する
        """
        tehai = Tehai()
        tehai.juntehai = {
            "_": self.juntehai["_"],
            "m": self.juntehai["m"][:],
            "p": self.juntehai["p"][:],
            "s": self.juntehai["s"][:],
            "z": self.juntehai["z"][:],
        }
        tehai.fuuro = self.fuuro[:]
        tehai.tsumo = self.tsumo
        tehai.riichi = self.riichi
        return tehai

    def update_from_string(self, tehai_string):
        """
        牌姿からインスタンスを更新する
        """
        tehai = self.from_string(tehai_string)
        self.juntehai = {
            "_": tehai.juntehai["_"],
            "m": tehai.juntehai["m"][:],
            "p": tehai.juntehai["p"][:],
            "s": tehai.juntehai["s"][:],
            "z": tehai.juntehai["z"][:],
        }
        self.fuuro = tehai.fuuro[:]
        self.tsumo = tehai.tsumo
        self.riichi = tehai.riichi
        return self

    def action_tsumo(self, hai, check=True):
        """
        ツモる
        """
        if check and self.tsumo:
            raise ValueError("Invalid")

        if hai == "_":
            self.juntehai["_"] += 1
            self.tsumo = hai

        else:
            if not self.valid_hai(hai):
                raise ValueError("Invalid")

            s, n = hai[0], int(hai[1])
            juntehai = self.juntehai[s]

            if juntehai[n] == 4:
                raise ValueError("Too many")

            juntehai[n] += 1

            if n == 0:
                if juntehai[5] == 4:
                    raise ValueError("Too many")

                juntehai[5] += 1

            self.tsumo = s + str(n)

        return self

    def decrease(self, s, n):
        """
        指定された牌を減らす
        """
        juntehai = self.juntehai[s]

        if juntehai[n] == 0 or (n == 5 and juntehai[0] == juntehai[5]):
            if self.juntehai["_"] == 0:
                raise ValueError("Invalid")

            self.juntehai["_"] -= 1

        else:
            juntehai[n] -= 1

            if n == 0:
                juntehai[5] -= 1

    def dahai(self, hai, check=True):
        """
        打牌する
        """
        if check and not self.tsumo:
            raise ValueError("Invalid")

        if not self.valid_hai(hai):
            raise ValueError("Invalid")

        s, n = hai[0], int(hai[1])
        self.decrease(s, n)
        self.tsumo = None

        if hai[-1] == "*":
            self.riichi = True

        return self

    def action_fuuro(self, mentsu, check=True):
        """
        副露する
        """
        if check and self.tsumo:
            raise ValueError("Invalid")

        if mentsu is not self.valid_mentsu(mentsu):
            raise ValueError("Invalid")

        if re.search(r"\d{4}$", mentsu):
            raise ValueError("Invalid")

        if re.search(r"\d{3}[\+\=\-]\d$", mentsu):
            raise ValueError("Invalid")

        s = mentsu[0]

        for n in re.findall(r"\d(?![\+\=\-])", mentsu):
            self.decrease(s, n)

        self.fuuro.append(mentsu)

        if not re.search(r"\d{4}", mentsu):
            self.tsumo = mentsu

        return self

    def kan(self, mentsu, check=True):
        """
        カン（暗槓/加槓）する
        """
        if check and not self.tsumo:
            raise ValueError("Invalid")

        if check and len(self.tsumo) > 2:
            raise ValueError("Invalid")

        if mentsu is not self.valid_mentsu(mentsu):
            raise ValueError("Invalid")

        s = mentsu[0]

        if re.search(r"\d{4}$", mentsu):
            for n in re.findall(r"\d", mentsu):
                self.decrease(s, n)

            self.fuuro.append(mentsu)

        elif re.search(r"\d{3}[\+\=\-]\d$", mentsu):
            m1 = mentsu[:5]
            index = (i for i, m2 in enumerate(self.fuuro) if m1 == m2)
            target_index = next(index, -1)

            if target_index < 0:
                raise ValueError("Invalid")

            self.fuuro[target_index] = mentsu
            self.decrease(s, mentsu[-1])
        else:
            raise ValueError("Invalid")

        self.tsumo = None
        return self
