import copy
import random
import datetime
from .kawa import Kawa
from .rule import rule
from .tehai import Tehai
from .yama import Yama


class Game:
    """
    ゲーム進行を管理するクラス
    """

    KAIKYOKU = "kaikyoku"
    HAIPAI = "haipai"
    TSUMO = "tsumo"

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
        観測値を取得
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
        self.haifu_["log"][-1].append(haifu)

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
        self.haifu_["log"][-1].append(haifu)
        message = []

        for cha_id in range(4):
            message.append(copy.deepcopy(haifu))

            if cha_id != model["teban"]:
                message[cha_id]["tsumo"]["hai"] = ""

        return self.get_observation(self.TSUMO, message)
