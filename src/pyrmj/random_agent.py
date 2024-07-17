import random
from .shanten import shanten
from .utils import Utils


class RandomAgent:
    """
    麻雀エージェントの基底クラス
    """

    def action(self, observation):
        """
        メッセージに対するアクションを返す
        """
        message = observation["message"]
        game_info = observation["game_info"]

        if Utils.TSUMO in message:
            return self.tsumo(message[Utils.TSUMO], game_info)

        elif Utils.DAHAI in message:
            return self.dahai(message[Utils.DAHAI], game_info)

        # elif Utils.FUURO in message:

        # elif Utils.KAN in message:

        # elif Utils.KANTSUMO in message:
        # return self.tsumo(message[Utils.KANTSUMO])

        return {}

    def tsumo(self, message, game_info):
        """
        ツモに対する処理
        """
        if message["cha_id"] != game_info["zikaze"]:
            return {}

        if game_info["tsumo_hoora"]:
            return {Utils.HOORA: "-"}

        else:
            dahai = self.select_dahai(game_info)

            if game_info["riichi"][dahai]:
                dahai += "*"

            return {Utils.DAHAI: dahai}

    def dahai(self, message, game_info):
        """
        打牌に対する処理
        """
        if message["cha_id"] == game_info["zikaze"]:
            if game_info["toupai"]:
                return {Utils.TOUPAI: "-"}

            else:
                return {}

        if game_info["ron_hoora"]:
            return {Utils.HOORA: "-"}

        elif game_info["toupai"]:
            return {Utils.TOUPAI: "-"}

        else:
            return {}

    def select_dahai(self, game_info):
        """
        打牌する牌を選択する
        """
        # random.seed(1704034800)  # TODO シード値を設定（Time stamp of 1/1/2024）
        dahai_list = []
        before_shanten = shanten(game_info["tehai"])

        for hai in game_info["dahai"]:
            tehai = game_info["tehai"].clone().dahai(hai)

            after_shanten = shanten(tehai)

            if after_shanten > before_shanten:
                continue

            elif after_shanten == before_shanten:
                dahai_list.append(hai)

            else:
                dahai_list = [hai]
                before_shanten = after_shanten

        return random.choice(dahai_list)
