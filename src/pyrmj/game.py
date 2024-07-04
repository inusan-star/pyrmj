import re
import copy
import random
import datetime
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
    RYUUKYOKU = "ryuukyoku"

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
        self.cannot_ron_ = [None] * 4
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
            self.reply_[player_id] = action or {}

        if None in self.reply_:
            return None

        if self.status_ == self.KAIKYOKU:
            return self.reply_kaikyoku()

        elif self.status_ == self.HAIPAI:
            return self.reply_haipai()

        elif self.status_ == self.TSUMO:
            return self.reply_tsumo()

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

        if reply.get("toupai", False):
            if self.allow_ryuukyoku():
                tehai = [""] * 4
                tehai[model["teban"]] = model["tehai"][model["teban"]].to_string()
                return self.ryuukyoku("九種九牌", tehai)

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
                    "kaikyoku": {
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
        self.ippatsu_ = [0, 0, 0, 0]
        self.n_kan_ = [0, 0, 0, 0]
        self.cannot_ron_ = [1, 1, 1, 1]
        self.hoora_ = []
        self.hoora_option_ = None
        self.no_game_ = False
        self.renchan_ = False
        self.tsumibou_ = model["tsumibou"]
        self.bunpai_ = None

        self.haifu_["tokuten"] = model["tokuten"][:]
        self.haifu_["log"].append([])
        haifu = {
            "haipai": {
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
                    message[cha_id]["haipai"]["tehai"][i] = ""

        return self.get_observation(self.HAIPAI, message)

    def tsumo(self):
        """
        ツモの局進行を行う
        """
        model = self.model_
        model["teban"] = (model["teban"] + 1) % 4
        tsumo_hai = model["yama"].tsumo()
        model["tehai"][model["teban"]].tsumo(tsumo_hai)
        haifu = {"tsumo": {"cha_id": model["teban"], "hai": tsumo_hai}}
        self.add_haifu(haifu)
        message = []

        for cha_id in range(4):
            message.append(copy.deepcopy(haifu))

            if cha_id != model["teban"]:
                message[cha_id]["tsumo"]["hai"] = ""

        return self.get_observation(self.TSUMO, message)

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
        haifu = {"ryuukyoku": {"name": name, "tehai": tehai, "bunpai": bunpai}}
        self.add_haifu(haifu)
        message = []

        for cha_id in range(4):
            message.append(copy.deepcopy(haifu))

        return self.get_observation(self.RYUUKYOKU, message)

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

    def allow_ryuukyoku(self):
        """
        流局が可能か判定する
        """
        model = self.model_
        return Utils.allow_ryuukyoku(self.rule_, model["tehai"][model["teban"]], self.first_tsumo_)
