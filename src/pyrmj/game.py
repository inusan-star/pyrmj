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

    def __init__(self, players, callback=None, rule_json=None, title=None):
        self.players_ = players
        self.callback_ = callback or (lambda: None)
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
            "tehai": [],
            "kawa": [],
            "player_id": [0, 1, 2, 3],
            "teban": None,
        }

        self.status_ = None
        self.reply_ = []
        self.max_kyokusuu_ = None
        self.haifu_ = {}

    def step(self, actions):
        """
        対局を進める
        """
        self.reply_ = [None] * 4

        for player_id, action in actions.items():
            self.reply_[player_id] = action or {}

        if self.status_ == self.KAIKYOKU:
            self.reply_kaikyoku()

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

        observation = []

        for player_id in range(4):
            observation.append(
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

        self.status_ = self.KAIKYOKU
        return observation

    def reply_kaikyoku(self):
        """
        開局の応答に対する処理
        """
        self.haipai()

    def haipai(self, yama=None):
        """
        配牌する
        """
        model = self.model_
        model["yama"] = yama or Yama(self.rule_)

        for cha_id in range(4):
            haipai = []

            for _ in range(13):
                haipai.append(model["shan"].tsumo())

            model["tehai"][cha_id] = Tehai(haipai)
            model["kawa"][cha_id] = Kawa()
            model["player_id"][cha_id] = (model["chiicha"] + model["kyokusuu"] + cha_id) % 4

        model["teban"] = -1
