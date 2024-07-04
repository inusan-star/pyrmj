import re
from .hoora import hoora_mentsu
from .shanten import shanten, yuukouhai


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
    def get_pon_mentsu(tehai, hai, haisuu):
        """
        ポン可能な面子の一覧を返す
        """
        mentsu = tehai.get_pon_mentsu(hai)

        if not mentsu:
            return mentsu

        return [] if haisuu == 0 else mentsu

    @staticmethod
    def get_kan_mentsu(rule_json, tehai, hai, haisuu, n_kan):
        """
        カン可能な面子の一覧を返す
        """
        mentsu = tehai.get_kan_mentsu(hai)

        if not mentsu or len(mentsu) == 0:
            return mentsu

        if tehai.riichi():
            if rule_json["リーチ後暗槓許可レベル"] == 0:
                return []

            elif rule_json["リーチ後暗槓許可レベル"] == 1:
                new_tehai = tehai.clone().dahai(tehai.tsumo_)
                n_hoora1 = sum(len(hoora_mentsu(new_tehai, h)) for h in yuukouhai(new_tehai))
                new_tehai = tehai.clone().kan(mentsu[0])
                n_hoora2 = sum(len(hoora_mentsu(new_tehai, h)) for h in yuukouhai(new_tehai))

                if n_hoora1 > n_hoora2:
                    return []

            else:
                new_tehai = tehai.clone().dahai(tehai.tsumo_)
                n_yuukouhai1 = len(yuukouhai(new_tehai))
                new_tehai = tehai.clone().kan(mentsu[0])

                if shanten(new_tehai) > 0:
                    return []

                n_yuukouhai2 = len(yuukouhai(new_tehai))

                if n_yuukouhai1 > n_yuukouhai2:
                    return []

        return [] if haisuu == 0 or n_kan == 4 else mentsu

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
