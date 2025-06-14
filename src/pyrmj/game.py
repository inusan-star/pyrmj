import copy
import datetime
import json
import os
import random
import re
from .hoora import hoora
from .kawa import Kawa
from .rule import rule
from .shanten import shanten, yuukouhai
from .tehai import Tehai
from .utils import Utils
from .yama import Yama


class Game:
    """
    ゲーム進行を管理するクラス
    """

    def __init__(self, rule_json=None):
        self.rule_ = rule_json or rule()

        self.model_ = {}
        self.status_ = None
        self.finished_ = None
        self.reply_ = [None] * 4
        self.save_flag_ = None
        self.max_kyokusuu_ = None
        self.haifu_ = {}
        self.first_tsumo_ = None
        self.suufuurenda_ = None
        self.dahai_ = None
        self.kan_ = None
        self.riichi_ = [None] * 4
        self.ippatsu_ = [None] * 4
        self.n_kan_ = [None] * 4
        self.not_friten_ = [None] * 4
        self.hoora_ = []
        self.hoora_option_ = None
        self.no_game_ = None
        self.renchan_ = None
        self.tsumibou_ = None
        self.bunpai_ = None

    def get_observation(self, status, message):
        """
        観測値を返す
        """
        model = self.model_
        self.status_ = status
        self.reply_ = [None] * 4
        observation = {}

        for cha_id in range(4):
            player_id = self.model_["player_id"][cha_id]
            observation[player_id] = {}
            observation[player_id]["message"] = message[cha_id]
            observation[player_id]["game_info"] = {
                "bakaze": model["bakaze"],
                "zikaze": cha_id,
                "tehai": model["tehai"][cha_id].clone() if status != Utils.KAIKYOKU else None,
                "kawa": [kawa.hai_.copy() for kawa in model["kawa"]] if status != Utils.KAIKYOKU else None,
                "dora_indicator": model["yama"].dora_indicator() if status != Utils.KAIKYOKU else None,
                "is_riichi": self.riichi_ if status != Utils.KAIKYOKU else None,
                "tsumo_hoora": self.allow_hoora() if status == Utils.TSUMO and model["teban"] == cha_id else False,
                "dahai": (
                    self.get_dahai()
                    if (status == Utils.TSUMO or status == Utils.FUURO) and model["teban"] == cha_id
                    else None
                ),
                "riichi": (
                    {hai: self.allow_riichi(hai) for hai in self.get_dahai()}
                    if (status == Utils.TSUMO or status == Utils.FUURO) and model["teban"] == cha_id
                    else None
                ),
                "toupai": self.allow_toupai(cha_id) if status == Utils.DAHAI else False,
                "ron_hoora": self.allow_hoora(cha_id) if status == Utils.DAHAI and model["teban"] != cha_id else False,
            }

        return observation

    def reset(
        self,
        chiicha=None,
        save_flag=False,
    ):
        """
        対局を開始する
        """
        self.model_ = {
            "title": "pyrmj_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
            "player": ["自家", "下家", "対面", "上家"],
            "chiicha": 0,
            "bakaze": 0,
            "kyokusuu": 0,
            "tsumibou": 0,
            "riichibou": 0,
            "tokuten": [self.rule_["配給原点"]] * 4,
            "yama": None,
            "tehai": [None] * 4,
            "kawa": [None] * 4,
            "player_id": [0, 1, 2, 3],
            "teban": None,
        }
        self.status_ = None
        self.finished_ = None
        self.reply_ = [None] * 4
        self.save_flag_ = None
        self.max_kyokusuu_ = None
        self.haifu_ = {}
        self.first_tsumo_ = None
        self.suufuurenda_ = None
        self.dahai_ = None
        self.kan_ = None
        self.riichi_ = [None] * 4
        self.ippatsu_ = [None] * 4
        self.n_kan_ = [None] * 4
        self.not_friten_ = [None] * 4
        self.hoora_ = []
        self.hoora_option_ = None
        self.no_game_ = None
        self.renchan_ = None
        self.tsumibou_ = None
        self.bunpai_ = None

        self.save_flag_ = save_flag
        return self.kaikyoku(chiicha)

    def step(self, actions):
        """
        対局を進める
        """
        for player_id, action in actions.items():
            self.reply_[player_id] = action

        if None in self.reply_:
            raise ValueError("Action is None")

        if self.status_ == Utils.KAIKYOKU:
            return self.reply_kaikyoku()

        elif self.status_ == Utils.HAIPAI:
            return self.reply_haipai()

        elif self.status_ == Utils.TSUMO:
            return self.reply_tsumo()

        elif self.status_ == Utils.DAHAI:
            return self.reply_dahai()

        elif self.status_ == Utils.FUURO:
            return self.reply_fuuro()

        elif self.status_ == Utils.KAN:
            return self.reply_kan()

        elif self.status_ == Utils.KANTSUMO:
            return self.reply_tsumo()

        elif self.status_ == Utils.HOORA:
            return self.reply_hoora()

        elif self.status_ == Utils.RYUUKYOKU:
            return self.reply_ryuukyoku()

        elif self.status_ == Utils.SYUUKYOKU:
            return self.reply_syuukyoku()

    def reward(self):
        """
        報酬を返す
        """
        return {player_id: (tokuten - 25000) / 100 for player_id, tokuten in enumerate(self.haifu_["tokuten"])}

    def point(self):
        """
        ポイントを返す
        """
        return {player_id: (tokuten - 25000) / 100 for player_id, tokuten in enumerate(self.haifu_["tokuten"])}

    def done(self):
        """
        対局が終了したか返す
        """
        return self.finished_

    def reply_kaikyoku(self):
        """
        開局の応答に対する処理
        """
        return self.haipai()

    def reply_haipai(self):
        """
        配牌の応答に対する処理
        """
        return self.tsumo()

    def reply_tsumo(self):
        """
        ツモの応答に対する処理
        """
        model = self.model_
        reply = self.get_reply(model["teban"])

        if Utils.TOUPAI in reply:
            if self.allow_ryuukyoku():
                tehai = [""] * 4
                tehai[model["teban"]] = model["tehai"][model["teban"]].to_string()
                return self.ryuukyoku("九種九牌", tehai)

        elif Utils.HOORA in reply:
            if self.allow_hoora():
                return self.hoora()

        elif Utils.KAN in reply:
            if reply[Utils.KAN] in self.get_kan_mentsu():
                return self.kan(reply[Utils.KAN])

        elif Utils.DAHAI in reply:
            dahai = re.sub(r"\*$", "", reply[Utils.DAHAI])

            if dahai in self.get_dahai():
                if reply[Utils.DAHAI][-1] == "*" and self.allow_riichi(dahai):
                    return self.dahai(reply[Utils.DAHAI])

                return self.dahai(dahai)

        # TODO 応答が不正の場合
        hai = self.get_dahai().pop()
        return self.dahai(hai)

    def reply_dahai(self):
        """
        打牌の応答に対する処理
        """
        model = self.model_

        for i in range(1, 4):
            cha_id = (model["teban"] + i) % 4
            reply = self.get_reply(cha_id)

            if Utils.HOORA in reply and self.allow_hoora(cha_id):
                if self.rule_["最大同時和了数"] == 1 and self.hoora_:
                    continue

                self.hoora_.append(cha_id)

            else:
                tehai = model["tehai"][cha_id].clone().tsumo(self.dahai_)
                if shanten(tehai) == -1:
                    self.not_friten_[cha_id] = False

        if len(self.hoora_) == 3 and self.rule_["最大同時和了数"] == 2:
            tehai = [""] * 4

            for cha_id in self.hoora_:
                tehai[cha_id] = model["tehai"][cha_id].to_string()

            return self.ryuukyoku("三家和", tehai)

        elif self.hoora_:
            return self.hoora()

        if self.dahai_[-1] == "*":
            model["tokuten"][model["player_id"][model["teban"]]] -= 1000
            model["riichibou"] += 1

            if len([r for r in self.riichi_ if r]) == 4 and self.rule_["途中流局あり"]:
                tehai = [te.to_string() for te in model["tehai"]]
                return self.ryuukyoku("四家立直", tehai)

        if self.first_tsumo_ and model["teban"] == 3:
            self.first_tsumo_ = False

            if self.suufuurenda_:
                return self.ryuukyoku("四風連打")

        if sum(self.n_kan_) == 4:
            if max(self.n_kan_) < 4 and self.rule_["途中流局あり"]:
                return self.ryuukyoku("四開槓")

        if not model["yama"].haisuu():
            tehai = [""] * 4

            for cha_id in range(4):
                reply = self.get_reply(cha_id)

                if Utils.TOUPAI in reply:
                    tehai[cha_id] = reply[Utils.TOUPAI]

            return self.ryuukyoku("", tehai)

        for i in range(1, 4):
            cha_id = (model["teban"] + i) % 4
            reply = self.get_reply(cha_id)

            if Utils.FUURO in reply:
                mentsu = reply[Utils.FUURO].replace("0", "5")

                if re.match(r"^[mpsz](\d)\1\1\1", mentsu):
                    if reply[Utils.FUURO] in self.get_kan_mentsu(cha_id):
                        return self.fuuro(reply[Utils.FUURO])

                elif re.match(r"^[mpsz](\d)\1\1", mentsu):
                    if reply[Utils.FUURO] in self.get_pon_mentsu(cha_id):
                        return self.fuuro(reply[Utils.FUURO])

        cha_id = (model["teban"] + 1) % 4
        reply = self.get_reply(cha_id)

        if Utils.FUURO in reply:
            if reply[Utils.FUURO] in self.get_chii_mentsu(cha_id):
                return self.fuuro(reply[Utils.FUURO])

        return self.tsumo()

    def reply_fuuro(self):
        """
        副露の応答に対する処理
        """
        model = self.model_

        if self.kan_:
            return self.kantsumo()

        reply = self.get_reply(model["teban"])

        if Utils.DAHAI in reply:
            if reply[Utils.DAHAI] in self.get_dahai():
                return self.dahai(reply[Utils.DAHAI])

        # TODO 応答が不正の場合
        hai = self.get_dahai().pop()
        return self.dahai(hai)

    def reply_kan(self):
        """
        カン（暗槓/加槓）の応答に対する処理
        """
        model = self.model_

        if re.match(r"^[mpsz]\d{4}$", self.kan_):
            return self.kantsumo()

        for i in range(1, 4):
            cha_id = (model["teban"] + i) % 4
            reply = self.get_reply(cha_id)

            if Utils.HOORA in reply and self.allow_hoora(cha_id):
                if self.rule_["最大同時和了数"] == 1 and self.hoora_:
                    continue

                self.hoora_.append(cha_id)

            else:
                hai = f"{self.kan_[0]}{self.kan_[-1]}"
                tehai = model["tehai"][cha_id].clone().tsumo(hai)
                if shanten(tehai) == -1:
                    self.not_friten_[cha_id] = False

        if self.hoora_:
            return self.hoora()

        return self.kantsumo()

    def reply_hoora(self):
        """
        和了の応答に対する処理
        """
        model = self.model_

        for cha_id in range(4):
            model["tokuten"][model["player_id"][cha_id]] += self.bunpai_[cha_id]

        model["tsumibou"] = 0
        model["riichibou"] = 0

        if self.hoora_:
            return self.hoora()

        else:
            if self.renchan_:
                model["tsumibou"] = self.tsumibou_ + 1

            return self.last()

    def reply_ryuukyoku(self):
        """
        流局の応答に対する処理
        """
        model = self.model_

        for cha_id in range(4):
            model["tokuten"][model["player_id"][cha_id]] += self.bunpai_[cha_id]

        model["tsumibou"] += 1

        return self.last()

    def reply_syuukyoku(self):
        """
        終局の応答に対する処理
        """
        if self.save_flag_:
            self.save_haifu()

        self.finished_ = True
        return None

    def kaikyoku(self, chiicha):
        """
        開局する
        """
        # random.seed(1704034800)  # TODO シード値を設定（Time stamp of 1/1/2024）
        self.finished_ = False
        self.model_["chiicha"] = chiicha if chiicha is not None else random.randint(0, 3)
        self.max_kyokusuu_ = 0 if self.rule_["場数"] == 0 else self.rule_["場数"] * 4 - 1

        self.haifu_ = {
            "title": self.model_["title"],
            "player": self.model_["player"],
            "chiicha": self.model_["chiicha"],
            "log": [],
            "tokuten": self.model_["tokuten"][:],
            "point": [],
            "rank": [],
        }

        message = []

        for cha_id in range(4):
            player_id = cha_id
            message.append(
                {
                    Utils.KAIKYOKU: {
                        "id": player_id,
                        "rule": self.rule_,
                        "title": self.haifu_["title"],
                        "player": self.haifu_["player"],
                        "chiicha": self.haifu_["chiicha"],
                    }
                }
            )

        return self.get_observation(Utils.KAIKYOKU, message)

    def haipai(self, yama=None):
        """
        配牌の局進行を行う
        """
        model = self.model_
        model["yama"] = yama or Yama(self.rule_)

        for cha_id in range(4):
            haipai = []

            for _ in range(13):
                haipai.append(model["yama"].tsumo())

            model["tehai"][cha_id] = Tehai(haipai)
            model["kawa"][cha_id] = Kawa()
            model["player_id"][cha_id] = (model["chiicha"] + model["kyokusuu"] + cha_id) % 4

        model["teban"] = -1
        self.first_tsumo_ = True
        self.suufuurenda_ = self.rule_["途中流局あり"]
        self.dahai_ = None
        self.kan_ = None
        self.riichi_ = [0, 0, 0, 0]
        self.ippatsu_ = [False, False, False, False]
        self.n_kan_ = [0, 0, 0, 0]
        self.not_friten_ = [True, True, True, True]
        self.hoora_ = []
        self.hoora_option_ = None
        self.no_game_ = False
        self.renchan_ = False
        self.tsumibou_ = model["tsumibou"]
        self.bunpai_ = None

        self.haifu_["tokuten"] = model["tokuten"][:]
        self.haifu_["log"].append([])
        haifu = {
            Utils.HAIPAI: {
                "bakaze": model["bakaze"],
                "kyokusuu": model["kyokusuu"],
                "tsumibou": model["tsumibou"],
                "riichibou": model["riichibou"],
                "tokuten": [model["tokuten"][player_id] for player_id in model["player_id"]],
                "dora_indicator": model["yama"].dora_indicator_[0],
                "tehai": [tehai.to_string() for tehai in model["tehai"]],
            }
        }
        self.add_haifu(haifu)

        message = []

        for cha_id in range(4):
            message.append(copy.deepcopy(haifu))

            for i in range(4):
                if i != cha_id:
                    message[cha_id][Utils.HAIPAI]["tehai"][i] = ""

        return self.get_observation(Utils.HAIPAI, message)

    def tsumo(self):
        """
        ツモの局進行を行う
        """
        model = self.model_
        model["teban"] = (model["teban"] + 1) % 4
        tsumo_hai = model["yama"].tsumo()
        model["tehai"][model["teban"]].tsumo(tsumo_hai)
        haifu = {Utils.TSUMO: {"cha_id": model["teban"], "hai": tsumo_hai}}
        self.add_haifu(haifu)
        message = []

        for cha_id in range(4):
            message.append(copy.deepcopy(haifu))

            if cha_id != model["teban"]:
                message[cha_id][Utils.TSUMO]["hai"] = ""

        return self.get_observation(Utils.TSUMO, message)

    def dahai(self, hai):
        """
        打牌の局進行を行う
        """
        model = self.model_
        self.ippatsu_[model["teban"]] = False

        if not model["tehai"][model["teban"]].riichi():
            self.not_friten_[model["teban"]] = True

        model["tehai"][model["teban"]].dahai(hai)
        model["kawa"][model["teban"]].dahai(hai)

        if self.first_tsumo_:
            if not re.match(r"^z[1234]", hai):
                self.suufuurenda_ = False

            if self.dahai_ and self.dahai_[:2] != hai[:2]:
                self.suufuurenda_ = False

        else:
            self.suufuurenda_ = False

        if hai[-1] == "*":
            self.riichi_[model["teban"]] = 2 if self.first_tsumo_ else 1
            self.ippatsu_[model["teban"]] = self.rule_["一発あり"]

        if shanten(model["tehai"][model["teban"]]) == 0 and any(
            model["kawa"][model["teban"]].find(h) for h in yuukouhai(model["tehai"][model["teban"]])
        ):
            self.not_friten_[model["teban"]] = False

        self.dahai_ = hai
        haifu = {Utils.DAHAI: {"cha_id": model["teban"], "hai": hai}}
        self.add_haifu(haifu)

        if self.kan_:
            observation_kaikan = self.kaikan()

            if observation_kaikan is None:
                observation_kaikan = {}

        else:
            observation_kaikan = {}

        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        observation_dahai = self.get_observation(Utils.DAHAI, message)
        return {key: {**value, **observation_kaikan.get(key, {})} for key, value in observation_dahai.items()}

    def fuuro(self, mentsu):
        """
        副露の局進行を行う
        """
        model = self.model_
        self.first_tsumo_ = False
        self.ippatsu_ = [False, False, False, False]
        model["kawa"][model["teban"]].fuuro(mentsu)
        direction = re.search(r"[\+\=\-]", mentsu).group()
        model["teban"] = (model["teban"] + "_-=+".index(direction)) % 4
        model["tehai"][model["teban"]].fuuro(mentsu)

        if re.match(r"^[mpsz]\d{4}", mentsu):
            self.kan_ = mentsu
            self.n_kan_[model["teban"]] += 1

        haifu = {Utils.FUURO: {"cha_id": model["teban"], "mentsu": mentsu}}
        self.add_haifu(haifu)
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(Utils.FUURO, message)

    def kan(self, mentsu):
        """
        カン（暗槓/加槓）の局進行を行う
        """
        model = self.model_
        model["tehai"][model["teban"]].kan(mentsu)
        haifu = {Utils.KAN: {"cha_id": model["teban"], "mentsu": mentsu}}
        self.add_haifu(haifu)

        if self.kan_:
            observation_kaikan = self.kaikan()

            if observation_kaikan is None:
                observation_kaikan = {}

        else:
            observation_kaikan = {}

        self.kan_ = mentsu
        self.n_kan_[model["teban"]] += 1
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        observation_kan = self.get_observation(Utils.KAN, message)
        return {key: {**value, **observation_kaikan.get(key, {})} for key, value in observation_kan.items()}

    def kantsumo(self):
        """
        槓ツモの局進行を行う
        """
        model = self.model_
        self.first_tsumo_ = False
        self.ippatsu_ = [False, False, False, False]
        tsumo_hai = model["yama"].kantsumo()
        model["tehai"][model["teban"]].tsumo(tsumo_hai)
        haifu = {Utils.KANTSUMO: {"cha_id": model["teban"], "hai": tsumo_hai}}
        self.add_haifu(haifu)

        if not self.rule_["カンドラ後乗せ"] or re.match(r"^[mpsz]\d{4}$", self.kan_):
            observation_kaikan = self.kaikan()

            if observation_kaikan is None:
                observation_kaikan = {}

        else:
            observation_kaikan = {}

        message = []

        for cha_id in range(4):
            message.append(copy.deepcopy(haifu))

            if cha_id != model["teban"]:
                message[cha_id][Utils.KANTSUMO]["hai"] = ""

        observation_kantsumo = self.get_observation(Utils.KANTSUMO, message)
        return {key: {**value, **observation_kaikan.get(key, {})} for key, value in observation_kantsumo.items()}

    def kaikan(self):
        """
        開槓の局進行を行う
        """
        self.kan_ = None

        if not self.rule_["カンドラあり"]:
            return None

        model = self.model_

        model["yama"].kaikan()
        dora_indicator = model["yama"].dora_indicator().pop()
        haifu = {Utils.KAIKAN: {"dora_indicator": dora_indicator}}
        self.add_haifu(haifu)
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(Utils.KAIKAN, message)

    def hoora(self):
        """
        和了の局進行を行う
        """
        model = self.model_

        if self.status_ != Utils.HOORA:
            model["yama"].close()
            self.hoora_option_ = (
                "chankan" if self.status_ == Utils.KAN else "rinshan" if self.status_ == Utils.KANTSUMO else None
            )

        zikaze = self.hoora_.pop(0) if self.hoora_ else model["teban"]
        ron_hai = (
            None
            if zikaze == model["teban"]
            else (f"{self.kan_[0]}{self.kan_[-1]}" if self.hoora_option_ == "chankan" else self.dahai_[:2])
            + "_+=-"[(4 + model["teban"] - zikaze) % 4]
        )
        tehai = model["tehai"][zikaze].clone()
        uradora_indicator = model["yama"].uradora_indicator() if tehai.riichi() else None

        param = {
            "rule": self.rule_,
            "bakaze": model["bakaze"],
            "zikaze": zikaze,
            "yaku": {
                "riichi": self.riichi_[zikaze],
                "ippatsu": self.ippatsu_[zikaze],
                "chankan": self.hoora_option_ == "chankan",
                "rinshan": self.hoora_option_ == "rinshan",
                "haitei": (
                    0 if model["yama"].haisuu() > 0 or self.hoora_option_ == "rinshan" else 1 if not ron_hai else 2
                ),
                "tenhoo": 0 if not (self.first_tsumo_ and not ron_hai) else 1 if zikaze == 0 else 2,
            },
            "dora_indicator": model["yama"].dora_indicator(),
            "uradora_indicator": uradora_indicator,
            "kyoutaku": {"tsumibou": model["tsumibou"], "riichibou": model["riichibou"]},
        }
        hoora_result = hoora(tehai, ron_hai, param)

        if self.rule_["連荘方式"] > 0 and zikaze == 0:
            self.renchan_ = True

        if self.rule_["場数"] == 0:
            self.renchan_ = False

        self.bunpai_ = hoora_result["bunpai"]
        haifu = {
            Utils.HOORA: {
                "cha_id": zikaze,
                "tehai": tehai.tsumo(ron_hai).to_string() if ron_hai else tehai.to_string(),
                "houjuusha": model["teban"] if ron_hai else None,
                "uradora_indicator": uradora_indicator,
                "fu": hoora_result["fu"],
                "hansuu": hoora_result["hansuu"],
                "yakuman": hoora_result["yakuman"],
                "tokuten": hoora_result["tokuten"],
                "yaku": hoora_result["yaku"],
                "bunpai": hoora_result["bunpai"],
            }
        }

        for key in ["fu", "hansuu", "yakuman"]:
            if not haifu[Utils.HOORA][key]:
                del haifu[Utils.HOORA][key]

        self.add_haifu(haifu)
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(Utils.HOORA, message)

    def ryuukyoku(self, name, tehai=None):
        """
        流局の局進行を行う
        """
        if tehai is None:
            tehai = [""] * 4

        model = self.model_
        bunpai = [0, 0, 0, 0]

        if not name:
            n_yuukouhai = 0

            for cha_id in range(4):
                if self.rule_["ノーテン宣言あり"] and not tehai[cha_id] and not model["tehai"][cha_id].riichi():
                    continue

                if (
                    not self.rule_["ノーテン罰あり"]
                    and (self.rule_["連荘方式"] != 2 or cha_id != 0)
                    and not model["tehai"][cha_id].riichi()
                ):
                    tehai[cha_id] = ""

                elif shanten(model["tehai"][cha_id]) == 0 and len(yuukouhai(model["tehai"][cha_id])) > 0:
                    n_yuukouhai += 1
                    tehai[cha_id] = model["tehai"][cha_id].to_string()

                    if self.rule_["連荘方式"] == 2 and cha_id == 0:
                        self.renchan_ = True

                else:
                    tehai[cha_id] = ""

            if self.rule_["流し満貫あり"]:
                for cha_id in range(4):
                    all_yaochu = True

                    for hai in model["kawa"][cha_id].hai_:
                        if re.search(r"[\+\=\-]$", hai):
                            all_yaochu = False
                            break

                        if re.match(r"^z", hai):
                            continue

                        if re.match(r"^[mps][19]", hai):
                            continue

                        all_yaochu = False
                        break

                    if all_yaochu:
                        name = "流し満貫"

                        for i in range(4):
                            if cha_id == 0 and i == cha_id:
                                bunpai[i] += 12000

                            elif cha_id == 0:
                                bunpai[i] -= 4000

                            elif cha_id != 0 and i == cha_id:
                                bunpai[i] += 8000

                            elif cha_id != 0 and i == 0:
                                bunpai[i] -= 4000

                            else:
                                bunpai[i] -= 2000

            if not name:
                name = "荒牌平局"

                if self.rule_["ノーテン罰あり"] and 0 < n_yuukouhai < 4:
                    for cha_id in range(4):
                        if tehai[cha_id]:
                            bunpai[cha_id] = 3000 / n_yuukouhai

                        else:
                            bunpai[cha_id] = -3000 / (4 - n_yuukouhai)

            if self.rule_["連荘方式"] == 3:
                self.renchan_ = True

        else:
            self.no_game_ = True
            self.renchan_ = True

        if self.rule_["場数"] == 0 and not self.rule_["一局戦連荘なし"]:
            self.renchan_ = True

        self.bunpai_ = bunpai
        haifu = {Utils.RYUUKYOKU: {"name": name, "tehai": tehai, "bunpai": bunpai}}
        self.add_haifu(haifu)
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(Utils.RYUUKYOKU, message)

    def last(self):
        """
        対局終了か判定する
        """
        model = self.model_
        model["teban"] = -1

        if not self.renchan_:
            model["kyokusuu"] += 1
            model["bakaze"] += model["kyokusuu"] // 4
            model["kyokusuu"] = model["kyokusuu"] % 4

        syuukyoku = False
        top_player = -1
        tokuten = model["tokuten"]

        for i in range(4):
            player_id = (model["chiicha"] + i) % 4

            if tokuten[player_id] < 0 and self.rule_["トビ終了あり"]:
                syuukyoku = True

            if tokuten[player_id] >= 30000 and (top_player < 0 or tokuten[player_id] > tokuten[top_player]):
                top_player = player_id

        sum_kyokusuu = model["bakaze"] * 4 + model["kyokusuu"]

        if sum_kyokusuu > 15:
            syuukyoku = True

        elif (self.rule_["場数"] + 1) * 4 - 1 < sum_kyokusuu:
            syuukyoku = True

        elif self.max_kyokusuu_ < sum_kyokusuu:
            if self.rule_["延長戦方式"] == 0:
                syuukyoku = True

            elif self.rule_["場数"] == 0:
                syuukyoku = True

            elif top_player >= 0:
                syuukyoku = True

            else:
                self.max_kyokusuu_ += 4 if self.rule_["延長戦方式"] == 3 else 1 if self.rule_["延長戦方式"] == 2 else 0

        elif self.max_kyokusuu_ == sum_kyokusuu:
            if (
                self.rule_["オーラス止めあり"]
                and top_player == model["player_id"][0]
                and self.renchan_
                and not self.no_game_
            ):
                syuukyoku = True

        if syuukyoku:
            return self.syuukyoku()

        else:
            return self.haipai()

    def syuukyoku(self):
        """
        終局の局進行を行う
        """
        model = self.model_
        ranking = []
        tokuten = model["tokuten"]

        for i in range(4):
            player_id = (model["chiicha"] + i) % 4

            for j in range(4):
                if j == len(ranking) or tokuten[player_id] > tokuten[ranking[j]]:
                    ranking.insert(j, player_id)
                    break

        tokuten[ranking[0]] += model["riichibou"] * 1000
        self.haifu_["tokuten"] = tokuten
        rank = [0, 0, 0, 0]

        for i in range(4):
            rank[ranking[i]] = i + 1

        self.haifu_["rank"] = rank
        round_point = not any(re.search(r"\.\d$", p) for p in self.rule_["順位点"])
        point = [0, 0, 0, 0]

        for i in range(1, 4):
            rank_player_id = ranking[i]
            point[rank_player_id] = (tokuten[rank_player_id] - 30000) / 1000 + float(self.rule_["順位点"][i])

            if round_point:
                point[rank_player_id] = round(point[rank_player_id])

            point[ranking[0]] -= point[rank_player_id]

        self.haifu_["point"] = [f"{p:.0f}" if round_point else f"{p:.1f}" for p in point]
        haifu = {Utils.SYUUKYOKU: self.haifu_}
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(Utils.SYUUKYOKU, message)

    def add_haifu(self, haifu):
        """
        牌譜を追加する
        """
        self.haifu_["log"][-1].append(haifu)

    def save_haifu(self):
        """
        牌譜を保存する
        """
        transformed_haifu = Utils.transform_keys(copy.deepcopy(self.haifu_))
        save_dir = os.getcwd()
        file_path = os.path.join(save_dir, self.model_["title"] + ".json")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(transformed_haifu, file, ensure_ascii=False, indent=2)

    def get_reply(self, cha_id):
        """
        指定した家の応答を返す
        """
        model = self.model_
        return self.reply_[model["player_id"][cha_id]]

    def get_dahai(self):
        """
        打牌可能な牌の一覧を返す
        """
        model = self.model_
        return Utils.get_dahai(self.rule_, model["tehai"][model["teban"]])

    def get_chii_mentsu(self, cha_id):
        """
        チー可能な面子の一覧を返す
        """
        model = self.model_
        direction = "_+=-"[(4 + model["teban"] - cha_id) % 4]
        return Utils.get_chii_mentsu(
            self.rule_, model["tehai"][cha_id], f"{self.dahai_}{direction}", model["yama"].haisuu()
        )

    def get_pon_mentsu(self, cha_id):
        """
        ポン可能な面子の一覧を返す
        """
        model = self.model_
        direction = "_+=-"[(4 + model["teban"] - cha_id) % 4]
        return Utils.get_pon_mentsu(model["tehai"][cha_id], f"{self.dahai_}{direction}", model["yama"].haisuu())

    def get_kan_mentsu(self, cha_id=None):
        """
        カン可能な面子の一覧を返す
        """
        model = self.model_
        if cha_id is None:
            return Utils.get_kan_mentsu(
                self.rule_, model["tehai"][model["teban"]], None, model["yama"].haisuu(), sum(self.n_kan_)
            )

        else:
            direction = "_+=-"[(4 + model["teban"] - cha_id) % 4]
            return Utils.get_kan_mentsu(
                self.rule_,
                model["tehai"][cha_id],
                f"{self.dahai_}{direction}",
                model["yama"].haisuu(),
                sum(self.n_kan_),
            )

    def allow_riichi(self, hai):
        """
        立直が可能か判定する
        """
        model = self.model_
        return Utils.allow_riichi(
            self.rule_,
            model["tehai"][model["teban"]],
            hai,
            model["yama"].haisuu(),
            model["tokuten"][model["player_id"][model["teban"]]],
        )

    def allow_hoora(self, cha_id=None):
        """
        和了が可能か判定する
        """
        model = self.model_
        if cha_id is None:
            yaku = (
                model["tehai"][model["teban"]].riichi() or self.status_ == Utils.KANTSUMO or model["yama"].haisuu() == 0
            )
            return Utils.allow_hoora(
                self.rule_, model["tehai"][model["teban"]], None, model["bakaze"], model["teban"], yaku
            )
        else:
            hai = (self.kan_[0] + self.kan_[-1] if self.status_ == Utils.KAN else self.dahai_) + "_+=-"[
                (4 + model["teban"] - cha_id) % 4
            ]
            yaku = model["tehai"][cha_id].riichi() or self.status_ == Utils.KAN or model["yama"].haisuu() == 0
            return Utils.allow_hoora(
                self.rule_, model["tehai"][cha_id], hai, model["bakaze"], cha_id, yaku, self.not_friten_[cha_id]
            )

    def allow_toupai(self, cha_id):
        """
        倒牌（ノーテン宣言）が可能か判定する
        """
        model = self.model_
        return Utils.allow_toupai(self.rule_, model["tehai"][cha_id], model["yama"].haisuu())

    def allow_ryuukyoku(self):
        """
        流局が可能か判定する
        """
        model = self.model_
        return Utils.allow_ryuukyoku(self.rule_, model["tehai"][model["teban"]], self.first_tsumo_)
