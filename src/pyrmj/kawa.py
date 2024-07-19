import re
from .tehai import Tehai


class Kawa:
    """
    河を表現するクラス
    """

    def __init__(self):
        self.hai_ = []
        self.find_ = {}

    def dahai(self, hai):
        """
        捨て牌に追加する
        """
        if not Tehai.valid_hai(hai):
            raise ValueError(f"Invalid hai: {hai}")

        self.hai_.append(re.sub(r"[\+\=\-]$", "", hai))
        self.find_[f"{hai[0]}{int(hai[1]) if hai[1] != '0' else 5}"] = True
        return self

    def fuuro(self, mentsu):
        """
        副露された状態にする
        """
        if not Tehai.valid_mentsu(mentsu):
            raise ValueError(f"Invalid mentsu: {mentsu}")

        number = re.search(r"\d(?=[\+\=\-])", mentsu)
        direction = re.search(r"[\+\=\-]", mentsu)

        if not direction:
            raise ValueError("No direction")

        hai = f"{mentsu[0]}{number.group()}" if number else mentsu[0]

        if self.hai_[-1][:2] != hai:
            raise ValueError(f"There is no {hai} in kawa")

        self.hai_[-1] += direction.group()
        return self

    def find(self, hai):
        """
        捨て牌か判定する
        """
        return self.find_.get(f"{hai[0]}{int(hai[1]) if hai[1] != '0' else 5}", False)
