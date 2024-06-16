import re


class Tehai:
    """
    手牌を表すクラス
    """

    def __init__(self):
        self.tehai = []

    def valid_hai(self, hai):
        """
        牌として有効かどうかを判定する
        """
        if re.match(r"^(?:[mps]\d|z[1-7])_?\*?[\+\=\-]?$", hai):
            return hai

        return None

    def valid_mentsu(self, mentsu):
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
