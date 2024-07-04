import re


class Utils:
    """
    ユーティリティクラス
    """

    @staticmethod
    def get_dahai(rule_json, tehai):
        """
        打牌可能な牌の一覧を返す
        """
        if rule_json["喰い替え許可レベル"] == 0:
            return tehai.get_dahai(True)

        if rule_json["喰い替え許可レベル"] == 1 and tehai.tsumo_ and len(tehai.tsumo_) > 2:

            match = re.search(r"\d(?=[\+\=\-])", tehai.tsumo_)
            deny = tehai.tsumo_[0] + (match.group() if match else "5")
            return [hai for hai in tehai.get_dahai(False) if hai.replace("0", "5") != deny]

        return tehai.get_dahai(False)

    @staticmethod
    def get_chii_mentsu(rule_json, tehai, hai, haisuu):
        """
        チー可能な面子の一覧を返す
        """
        mentsu = tehai.get_chii_mentsu(hai, rule_json["喰い替え許可レベル"] == 0)

        if not mentsu:
            return mentsu

        if (
            rule_json["喰い替え許可レベル"] == 1
            and len(tehai.fuuro_) == 3
            and tehai.juntehai_[hai[0]][int(hai[1])] == 2
        ):
            mentsu = []

        return [] if haisuu == 0 else mentsu

    @staticmethod
    def allow_ryuukyoku(rule_json, tehai, first_tsumo):
        """
        流局が可能か判定する
        """
        if not (first_tsumo and tehai.tsumo_):
            return False

        if not rule_json["途中流局あり"]:
            return False

        n_yaochu = 0

        for suit in ["m", "p", "s", "z"]:
            juntehai = tehai.juntehai_[suit]
            numbers = [1, 2, 3, 4, 5, 6, 7] if suit == "z" else [1, 9]

            for number in numbers:
                if juntehai[number] > 0:
                    n_yaochu += 1

        return n_yaochu >= 9
