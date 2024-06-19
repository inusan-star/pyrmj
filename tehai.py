import re


HAI_UNICODE = {
    "m0": "\033[91m🀋\033[00m",
    "m1": "🀇",
    "m2": "🀈",
    "m3": "🀉",
    "m4": "🀊",
    "m5": "🀋",
    "m6": "🀌",
    "m7": "🀍",
    "m8": "🀎",
    "m9": "🀏",
    "p0": "\033[91m🀝\033[00m",
    "p1": "🀙",
    "p2": "🀚",
    "p3": "🀛",
    "p4": "🀜",
    "p5": "🀝",
    "p6": "🀞",
    "p7": "🀟",
    "p8": "🀠",
    "p9": "🀡",
    "s0": "\033[91m🀔\033[00m",
    "s1": "🀐",
    "s2": "🀑",
    "s3": "🀒",
    "s4": "🀓",
    "s5": "🀔",
    "s6": "🀕",
    "s7": "🀖",
    "s8": "🀗",
    "s9": "🀘",
    "z1": "🀀",
    "z2": "🀁",
    "z3": "🀂",
    "z4": "🀃",
    "z5": "🀆",
    "z6": "🀅",
    "z7": "🀄",
    "_": "🀫",
}


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

        black_mentsu = mentsu.replace("0", "5")

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

        if mentsu != self.valid_mentsu(mentsu):
            raise ValueError("Invalid")

        if re.search(r"\d{4}$", mentsu):
            raise ValueError("Invalid")

        if re.search(r"\d{3}[\+\=\-]\d$", mentsu):
            raise ValueError("Invalid")

        s = mentsu[0]

        for n in re.findall(r"\d(?![\+\=\-])", mentsu):
            self.decrease(s, int(n))

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

        if mentsu != self.valid_mentsu(mentsu):
            raise ValueError("Invalid")

        s = mentsu[0]

        if re.search(r"\d{4}$", mentsu):
            for n in re.findall(r"\d", mentsu):
                self.decrease(s, int(n))

            self.fuuro.append(mentsu)

        elif re.search(r"\d{3}[\+\=\-]\d$", mentsu):
            m1 = mentsu[:5]
            index = (i for i, m2 in enumerate(self.fuuro) if m1 == m2)
            target_index = next(index, -1)

            if target_index < 0:
                raise ValueError("Invalid")

            self.fuuro[target_index] = mentsu
            self.decrease(s, int(mentsu[-1]))

        else:
            raise ValueError("Invalid")

        self.tsumo = None
        return self

    def menzen(self):
        """
        門前かどうかを判定する
        """
        return len([m for m in self.fuuro if re.search(r"[\+\=\-]", m)]) == 0

    def get_riichi(self):
        """
        リーチしているかどうかを判定する
        """
        return self.riichi

    def get_dahai(self, check=True):
        """
        打牌可能な牌の一覧を返す
        """
        if not self.tsumo:
            return None

        deny = {}

        if check and len(self.tsumo) > 2:
            mentsu = self.tsumo
            s = mentsu[0]
            match = re.search(r"\d(?=[\+\=\-])", mentsu)
            n = int(match.group()) if match and int(match.group()) != 0 else 5
            deny[s + str(n)] = True

            if not re.match(r"^[mpsz](\d)\1\1", mentsu.replace("0", "5")):
                if n < 7 and re.match(r"^[mps]\d\-\d\d$", mentsu):
                    deny[s + str(n + 3)] = True

                if 3 < n and re.match(r"^[mps]\d\d\d\-$", mentsu):
                    deny[s + str(n - 3)] = True

        dahai = []

        if not self.riichi:
            for s in ["m", "p", "s", "z"]:
                juntehai = self.juntehai[s]

                for n in range(1, len(juntehai)):
                    if juntehai[n] == 0:
                        continue

                    if s + str(n) in deny:
                        continue

                    if s + str(n) == self.tsumo and juntehai[n] == 1:
                        continue

                    if s == "z" or n != 5:
                        dahai.append(s + str(n))

                    else:
                        if juntehai[0] > 0 and (
                            s + "0" != self.tsumo or juntehai[0] > 1
                        ):
                            dahai.append(s + "0")

                        if juntehai[0] < juntehai[5]:
                            dahai.append(s + str(n))

        if len(self.tsumo) == 2:
            dahai.append(self.tsumo + "_")

        return dahai

    def get_chii_mentsu(self, hai, check=True):
        """
        チー可能な面子の一覧を返す
        """

        if self.tsumo:
            return None

        if not self.valid_hai(hai):
            raise ValueError("Invalid")

        mentsu = []
        s, n = hai[0], int(hai[1]) if int(hai[1]) != 0 else 5
        d = re.search(r"[\+\=\-]$", hai)

        if not d:
            raise ValueError("Invalid")

        if s == "z" or d.group() != "-":
            return mentsu

        if self.riichi:
            return mentsu

        juntehai = self.juntehai[s]

        if 3 <= n and 0 < juntehai[n - 2] and 0 < juntehai[n - 1]:
            if not check or (
                (juntehai[n] + (juntehai[n - 3] if n > 3 else 0))
                < 14 - (len(self.fuuro) + 1) * 3
            ):
                if n - 2 == 5 and juntehai[0] > 0:
                    mentsu.append(f"{s}067-")

                if n - 1 == 5 and juntehai[0] > 0:
                    mentsu.append(f"{s}406-")

                if (n - 2 != 5 and n - 1 != 5) or juntehai[0] < juntehai[5]:
                    mentsu.append(f"{s}{n-2}{n-1}{hai[1]}{d.group()}")

        if 2 <= n <= 8 and 0 < juntehai[n - 1] and 0 < juntehai[n + 1]:
            if not check or juntehai[n] < 14 - (len(self.fuuro) + 1) * 3:
                if n - 1 == 5 and juntehai[0] > 0:
                    mentsu.append(f"{s}06-7")

                if n + 1 == 5 and juntehai[0] > 0:
                    mentsu.append(f"{s}34-0")

                if (n - 1 != 5 and n + 1 != 5) or juntehai[0] < juntehai[5]:
                    mentsu.append(f"{s}{n-1}{hai[1]}{d.group()}{n+1}")

        if n <= 7 and 0 < juntehai[n + 1] and 0 < juntehai[n + 2]:
            if not check or (
                (juntehai[n] + (juntehai[n + 3] if n < 7 else 0))
                < 14 - (len(self.fuuro) + 1) * 3
            ):
                if n + 1 == 5 and juntehai[0] > 0:
                    mentsu.append(f"{s}4-06")

                if n + 2 == 5 and juntehai[0] > 0:
                    mentsu.append(f"{s}3-40")

                if (n + 1 != 5 and n + 2 != 5) or juntehai[0] < juntehai[5]:
                    mentsu.append(f"{s}{hai[1]}{d.group()}{n+1}{n+2}")

        return mentsu

    def get_pon_mentsu(self, hai):
        """
        ポン可能な面子の一覧を返す
        """
        if self.tsumo:
            return None

        if not self.valid_hai(hai):
            raise ValueError("Invalid")

        mentsu = []
        s, n = hai[0], int(hai[1]) if int(hai[1]) != 0 else 5
        d = re.search(r"[\+\=\-]$", hai)

        if not d:
            raise ValueError("Invalid")

        if self.riichi:
            return mentsu

        juntehai = self.juntehai[s]

        if juntehai[n] >= 2:
            if n == 5 and juntehai[0] >= 2:
                mentsu.append(f"{s}00{hai[1]}{d.group()}")

            if n == 5 and juntehai[0] >= 1 and juntehai[5] - juntehai[0] >= 1:
                mentsu.append(f"{s}50{hai[1]}{d.group()}")

            if n != 5 or juntehai[5] - juntehai[0] >= 2:
                mentsu.append(f"{s}{str(n)}{str(n)}{hai[1]}{d.group()}")

        return mentsu

    def get_kan_mentsu(self, hai=None):
        """
        カン可能な面子の一覧を返す
        """
        mentsu = []

        if hai:
            if self.tsumo:
                return None

            if not self.valid_hai(hai):
                raise ValueError("Invalid")

            s, n = hai[0], int(hai[1]) if int(hai[1]) != 0 else 5
            d = re.search(r"[\+\=\-]$", hai)

            if not d:
                raise ValueError("Invalid")

            if self.riichi:
                return mentsu

            juntehai = self.juntehai[s]

            if juntehai[n] == 3:
                if n == 5:
                    mentsu = [f"{s}{"5" * (3 - juntehai[0])}{"0" * juntehai[0]}{hai[1]}{d.group()}"]

                else:
                    mentsu = [f"{s}{str(n) * 4}{d.group()}"]

        else:
            if not self.tsumo:
                return None

            if len(self.tsumo) > 2:
                return None

            hai = self.tsumo.replace("0", "5")

            for s in ["m", "p", "s", "z"]:
                juntehai = self.juntehai[s]

                for n in range(1, len(juntehai)):
                    if juntehai[n] == 0:
                        continue

                    if juntehai[n] == 4:
                        if self.riichi and s + str(n) != hai:
                            continue

                        if n == 5:
                            mentsu.append(f"{s}{"5" * (4 - juntehai[0])}{"0" * juntehai[0]}")

                        else:
                            mentsu.append(f"{s}{str(n) * 4}")

                    else:
                        if self.riichi:
                            continue

                        for m in self.fuuro:
                            if m.replace("0", "5")[:4] == f"{s}{str(n) * 3}":
                                if n == 5 and juntehai[0] > 0:
                                    mentsu.append(m + "0")

                                else:
                                    mentsu.append(m + str(n))

        return mentsu

    def to_json(self):
        """
        牌姿をjsonで返す
        """
        json_output = {"tehai": {"juntehai": [], "fuuro": []}}
        tsumo = self.tsumo

        for s in ["m", "p", "s", "z"]:
            juntehai = self.juntehai[s]
            n_akahai = juntehai[0]

            for n in range(1, len(juntehai)):
                n_hai = juntehai[n]

                if f"{s}{n}" == tsumo:
                    n_hai -= 1

                elif n == 5 and f"{s}{0}" == tsumo:
                    n_akahai -= 1
                    n_hai -= 1

                for _ in range(n_hai):
                    hai = s

                    if n == 5 and n_akahai > 0:
                        hai += "0"
                        n_akahai -= 1

                    else:
                        hai += str(n)

                    json_output["tehai"]["juntehai"].append(
                        {
                            "type": "normal",
                            "hai": hai,
                        }
                    )

        if tsumo and len(tsumo) == 2:
            json_output["tehai"]["juntehai"].append(
                {
                    "type": "tsumo",
                    "hai": tsumo,
                }
            )

        for mentsu in self.fuuro:
            s = mentsu[0]

            if re.match(r"^[mpsz](\d)\1\1\1$", mentsu.replace("0", "5")):
                nn = re.findall(r"\d", mentsu)
                json_output["tehai"]["fuuro"].append(
                    [
                        {"type": "normal", "hai": "_"},
                        {"type": "normal", "hai": f"{s}{nn[2]}"},
                        {"type": "normal", "hai": f"{s}{nn[3]}"},
                        {"type": "normal", "hai": "_"},
                    ]
                )

            elif re.match(r"^[mpsz](\d)\1\1\1?[\+\=\-]\1?$", mentsu.replace("0", "5")):
                not_fuuro = re.search(r"[\+\=\-]\d$", mentsu)
                d = re.search(r"[\+\=\-]", mentsu).group()
                hai = [f"{s}{n}" for n in re.findall(r"\d", mentsu)]
                hai_r = [hai[2], hai[3]] if not_fuuro else [hai[-1]]
                hai_l = (
                    [hai[1], hai[2]] if not not_fuuro and len(hai) == 4 else [hai[1]]
                )

                if d == "+":
                    json_output["tehai"]["fuuro"].append(
                        [
                            {"type": "normal", "hai": hai[0]},
                            *[{"type": "normal", "hai": h} for h in hai_l],
                            *[{"type": "rotate", "hai": h} for h in hai_r],
                        ]
                    )

                elif d == "=":
                    json_output["tehai"]["fuuro"].append(
                        [
                            {"type": "normal", "hai": hai[0]},
                            *[{"type": "rotate", "hai": h} for h in hai_r],
                            *[{"type": "normal", "hai": h} for h in hai_l],
                        ]
                    )

                elif d == "-":
                    json_output["tehai"]["fuuro"].append(
                        [
                            *[{"type": "rotate", "hai": h} for h in hai_r],
                            {"type": "normal", "hai": hai[0]},
                            *[{"type": "normal", "hai": h} for h in hai_l],
                        ]
                    )

            else:
                nn = [re.search(r"\d(?=\-)", mentsu).group()] + re.findall(
                    r"\d(?!\-)", mentsu
                )
                json_output["tehai"]["fuuro"].append(
                    [
                        {"type": "rotate", "hai": f"{s}{nn[0]}"},
                        {"type": "normal", "hai": f"{s}{nn[1]}"},
                        {"type": "normal", "hai": f"{s}{nn[2]}"},
                    ]
                )

        return json_output

    def to_display(self, open_hand=True):
        """
        牌を引く
        """
        json_data = self.to_json()

        for hai_data in json_data["tehai"]["juntehai"]:
            if hai_data["type"] == "tsumo":
                print(" ", end="")

            if open_hand:
                print(HAI_UNICODE[hai_data["hai"]], end="")

            else:
                print(HAI_UNICODE["_"], end="")

        print("  ", end="")

        for mentsu in json_data["tehai"]["fuuro"][::-1]:
            for hai_data in mentsu:
                if hai_data["type"] == "rotate":
                    print("/", end="")

                print(HAI_UNICODE[hai_data["hai"]], end="")

            print(" ", end="")

        print("\n")
