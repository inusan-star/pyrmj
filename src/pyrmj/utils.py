import re
from .hoora import hoora_mentsu, hoora
from .shanten import shanten, yuukouhai


class Utils:
    """
    ユーティリティクラス
    """

    KAIKYOKU = "kaikyoku"
    HAIPAI = "haipai"
    TSUMO = "tsumo"
    DAHAI = "dahai"
    FUURO = "fuuro"
    KAN = "kan"
    KANTSUMO = "kantsumo"
    KAIKAN = "kaikan"
    HOORA = "hoora"
    TOUPAI = "toupai"
    RYUUKYOKU = "ryuukyoku"
    SYUUKYOKU = "syuukyoku"

    haifu_mapping = {
        KAIKYOKU: "kaiju",
        HAIPAI: "qipai",
        TSUMO: "zimo",
        DAHAI: "dapai",
        FUURO: "fulou",
        KAN: "gang",
        KANTSUMO: "gangzimo",
        KAIKAN: "kaigang",
        HOORA: "hule",
        RYUUKYOKU: "pingju",
        SYUUKYOKU: "jieju",
        "chiicha": "qijia",
        "tokuten": "defen",
        "bakaze": "zhuangfeng",
        "kyokusuu": "jushu",
        "tsumibou": "changbang",
        "riichibou": "lizhibang",
        "dora_indicator": "baopai",
        "tehai": "shoupai",
        "cha_id": "l",
        "hai": "p",
        "mentsu": "m",
        "houjuusha": "baojia",
        "uradora_indicator": "fubaopai",
        "hansuu": "fanshu",
        "yakuman": "damanguan",
        "yaku": "hupai",
        "bunpai": "fenpei",
    }

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
    def allow_riichi(rule_json, tehai, hai, haisuu, tokuten):
        """
        立直が可能か判定する
        """
        if not tehai.tsumo_:
            return False

        if tehai.riichi():
            return False

        if not tehai.menzen():
            return False

        if not rule_json["ツモ番なしリーチあり"] and haisuu < 4:
            return False

        if rule_json["トビ終了あり"] and tokuten < 1000:
            return False

        if shanten(tehai) > 0:
            return False

        if hai:
            new_tehai = tehai.clone().dahai(hai)
            return shanten(new_tehai) == 0 and len(yuukouhai(new_tehai)) > 0

        else:
            dahai = []

            for h in Utils.get_dahai(rule_json, tehai):
                new_tehai = tehai.clone().dahai(h)

                if shanten(new_tehai) == 0 and len(yuukouhai(new_tehai)) > 0:
                    dahai.append(h)

            return dahai if dahai else False

    @staticmethod
    def allow_hoora(rule_json, tehai, hai, bakaze, zikaze, yaku, not_friten=False):
        """
        和了が可能か判定する
        """
        if hai and not not_friten:
            return False

        new_tehai = tehai.clone()

        if hai:
            new_tehai.tsumo(hai)

        if shanten(new_tehai) != -1:
            return False

        if yaku:
            return True

        param = {
            "rule": rule_json,
            "bakaze": bakaze,
            "zikaze": zikaze,
            "yaku": {},
            "dora_indicator": [],
            "kyoutaku": {"tsumibou": 0, "riichibou": 0},
        }
        hoora_result = hoora(tehai, hai, param)
        return hoora_result is not None and hoora_result.get("yaku", None) is not None

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
