import re
import copy
import random
import datetime
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

    def __init__(self, rule_json=None, title=None):
        self.rule_ = rule_json or rule()

        self.model_ = {
            "title": title or "pyrmj - " + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
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
        self.reply_ = [None] * 4
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
        self.status_ = status
        self.reply_ = [None] * 4
        observation = {}

        for cha_id in range(4):
            player_id = self.model_["player_id"][cha_id]
            observation[player_id] = message[cha_id]

        return observation

    def step(self, actions):
        """
        対局を進める
        """
        for player_id, action in actions.items():
            self.reply_[player_id] = action or {}  # TODO: 要検討

        if None in self.reply_:  # TODO: 要検討
            return None, True  # TODO: 要検討

        if self.status_ == self.KAIKYOKU:
            return self.reply_kaikyoku(), False

        elif self.status_ == self.HAIPAI:
            return self.reply_haipai(), False

        elif self.status_ == self.TSUMO:
            return self.reply_tsumo(), False

        elif self.status_ == self.KAN:
            return self.reply_kan(), False

        elif self.status_ == self.KANTSUMO:
            return self.reply_tsumo(), False

        elif self.status_ == self.HOORA:
            return self.reply_hoora(), False

        elif self.status_ == self.RYUUKYOKU:
            return self.reply_ryuukyoku(), False

        elif self.status_ == self.SYUUKYOKU:
            # TODO: 牌譜をファイルに保存する
            return None, True

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

        if self.TOUPAI in reply:
            if self.allow_ryuukyoku():
                tehai = [""] * 4
                tehai[model["teban"]] = model["tehai"][model["teban"]].to_string()
                return self.ryuukyoku("九種九牌", tehai)

        elif self.HOORA in reply:
            if self.allow_hoora():
                return self.hoora()

        elif self.KAN in reply:
            if reply[self.KAN] in self.get_kan_mentsu():
                return self.kan(reply[self.KAN])

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

            if self.HOORA in reply and self.allow_hoora(cha_id):
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

    def kaikyoku(self, chiicha=None):
        """
        開局する
        """
        random.seed(1704034800)  # シード値を設定（Time stamp of 1/1/2024）
        self.model_["chiicha"] = chiicha if chiicha else random.randint(0, 3)
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
                    self.KAIKYOKU: {
                        "id": player_id,
                        "rule": self.rule_,
                        "title": self.haifu_["title"],
                        "player": self.haifu_["player"],
                        "chiicha": self.haifu_["chiicha"],
                    }
                }
            )

        return self.get_observation(self.KAIKYOKU, message)

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
            self.HAIPAI: {
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
                    message[cha_id][self.HAIPAI]["tehai"][i] = ""

        return self.get_observation(self.HAIPAI, message)

    def tsumo(self):
        """
        ツモの局進行を行う
        """
        model = self.model_
        model["teban"] = (model["teban"] + 1) % 4
        tsumo_hai = model["yama"].tsumo()
        model["tehai"][model["teban"]].tsumo(tsumo_hai)
        haifu = {self.TSUMO: {"cha_id": model["teban"], "hai": tsumo_hai}}
        self.add_haifu(haifu)
        message = []

        for cha_id in range(4):
            message.append(copy.deepcopy(haifu))

            if cha_id != model["teban"]:
                message[cha_id][self.TSUMO]["hai"] = ""

        return self.get_observation(self.TSUMO, message)

    def kan(self, mentsu):
        """
        カン（暗槓/加槓）の局進行を行う
        """
        model = self.model_
        model["tehai"][model["teban"]].kan(mentsu)
        haifu = {self.KAN: {"cha_id": model["teban"], "mentsu": mentsu}}
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

        observation_kan = self.get_observation(self.KAN, message)
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
        haifu = {self.KANTSUMO: {"cha_id": model["teban"], "hai": tsumo_hai}}
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
                message[cha_id][self.KANTSUMO]["hai"] = ""

        observation_kantsumo = self.get_observation(self.KANTSUMO, message)
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
        haifu = {self.KAIKAN: {"dora": dora_indicator}}
        self.add_haifu(haifu)
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(self.KAIKAN, message)

    def hoora(self):
        """
        和了の局進行を行う
        """
        model = self.model_

        if self.status_ != self.HOORA:
            model["yama"].close()
            self.hoora_option_ = (
                "chankan" if self.status_ == self.KAN else "rinshan" if self.status_ == self.KANTSUMO else None
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
            self.HOORA: {
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
            if not haifu[self.HOORA][key]:
                del haifu[self.HOORA][key]

        self.add_haifu(haifu)
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(self.HOORA, message)

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

        if self.rule_["場数"] == 0:
            self.renchan_ = True

        self.bunpai_ = bunpai
        haifu = {self.RYUUKYOKU: {"name": name, "tehai": tehai, "bunpai": bunpai}}
        self.add_haifu(haifu)
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(self.RYUUKYOKU, message)

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
        haifu = {self.SYUUKYOKU: self.haifu_}
        message = []

        for _ in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(self.SYUUKYOKU, message)

    def add_haifu(self, haifu):
        """
        牌譜を追加する
        """
        self.haifu_["log"][-1].append(haifu)

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
                model["tehai"][model["teban"]].riichi() or self.status_ == self.KANTSUMO or model["yama"].haisuu() == 0
            )
            return Utils.allow_hoora(
                self.rule_, model["tehai"][model["teban"]], None, model["bakaze"], model["teban"], yaku
            )
        else:
            hai = (self.kan_[0] + self.kan_[-1] if self.status_ == self.KAN else self.dahai_) + "_+=-"[
                (4 + model["teban"] - cha_id) % 4
            ]
            yaku = model["tehai"][cha_id].riichi() or self.status_ == self.KAN or model["yama"].haisuu() == 0
            return Utils.allow_hoora(
                self.rule_, model["tehai"][cha_id], hai, model["bakaze"], cha_id, yaku, self.not_friten_[cha_id]
            )

    def allow_ryuukyoku(self):
        """
        流局が可能か判定する
        """
        model = self.model_
        return Utils.allow_ryuukyoku(self.rule_, model["tehai"][model["teban"]], self.first_tsumo_)
