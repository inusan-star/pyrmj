import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from .utils import Utils
from .shanten import shanten


class PolicyCNN(nn.Module):
    """
    ポリシーCNN
    """

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=(4, 5), padding=0)
        self.bn1 = nn.BatchNorm2d(64)
        self.dropout1 = nn.Dropout(0.5)

        self.conv2 = nn.Conv2d(64, 64, kernel_size=(4, 5), padding=0)
        self.bn2 = nn.BatchNorm2d(64)
        self.dropout2 = nn.Dropout(0.5)

        self.conv3 = nn.Conv2d(64, 64, kernel_size=(4, 5), padding=0)
        self.bn3 = nn.BatchNorm2d(64)
        self.dropout3 = nn.Dropout(0.5)

        self.conv4 = nn.Conv2d(64, 32, kernel_size=(4, 5), padding=0)
        self.bn4 = nn.BatchNorm2d(32)
        self.dropout4 = nn.Dropout(0.5)

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(self._get_conv_output_size(), 256)
        self.bn5 = nn.LayerNorm(256)
        self.dropout5 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(256, 34)

    def _get_conv_output_size(self):
        x = torch.randn(1, 1, 34, 142)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.flatten(x)
        return x.size(1)

    def forward(self, x):
        """
        順伝播
        """
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.dropout1(x)

        x = F.relu(self.bn2(self.conv2(x)))
        x = self.dropout2(x)

        x = F.relu(self.bn3(self.conv3(x)))
        x = self.dropout3(x)

        x = F.relu(self.bn4(self.conv4(x)))
        x = self.dropout4(x)

        x = self.flatten(x)

        x = F.relu(self.bn5(self.fc1(x)))
        x = self.dropout5(x)

        x = F.softmax(self.fc2(x), dim=1)

        return x


class AIAgent:
    """
    麻雀エージェントの基底クラス
    """

    def __init__(self):
        self.gamma = 0.98
        self.lr = 0.0002

        self.memory = []
        self.model = PolicyCNN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)

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
        dahai_list = []
        n_shanten = shanten(game_info["tehai"])

        for hai in game_info["dahai"]:
            tehai = game_info["tehai"].clone().dahai(hai)

            if shanten(tehai) > n_shanten:
                continue

            dahai_list.append(hai)

        input_tensor = self.create_input(game_info)
        probs = self.model(input_tensor)[0]
        probs_np = probs.detach().numpy()
        possible_hais = dahai_list
        possible_indices = [self.hai_to_index(hai[0], int(hai[1])) for hai in possible_hais]
        mask = np.zeros_like(probs_np)

        for idx in possible_indices:
            mask[idx] = 1

        masked_probs = probs_np * mask
        masked_probs /= np.sum(masked_probs)
        action_index = np.argmax(masked_probs)
        action_hai = None

        for hai in possible_hais:
            if self.hai_to_index(hai[0], int(hai[1])) == action_index:
                action_hai = hai
                break

        action_prob = probs[action_index]

        self.add(action_prob)

        return action_hai

    def create_input(self, game_info):
        """
        ニューラルネットワークの入力を生成する
        """

        tsumo = self.encode_tsumo(game_info["tehai"].tsumo_)
        juntehai = self.encode_juntehai(game_info["tehai"].juntehai_)
        player0_kawa = self.encode_kawa(game_info["kawa"][0])
        player1_kawa = self.encode_kawa(game_info["kawa"][1])
        player2_kawa = self.encode_kawa(game_info["kawa"][2])
        player3_kawa = self.encode_kawa(game_info["kawa"][3])
        dora_indicator = self.encode_dora_indicator(game_info["dora_indicator"])
        riichi = self.encode_riichi(game_info["is_riichi"])
        bakaze = self.encode_kaze(game_info["bakaze"])
        zikaze = self.encode_kaze(game_info["zikaze"])

        input_tensor = np.concatenate(
            [
                tsumo,
                juntehai,
                player0_kawa,
                player1_kawa,
                player2_kawa,
                player3_kawa,
                dora_indicator,
                riichi,
                bakaze,
                zikaze,
            ],
            axis=1,
        )

        input_tensor = torch.tensor(input_tensor, dtype=torch.float32)
        input_tensor = input_tensor.unsqueeze(0).unsqueeze(0)
        return input_tensor

    def encode_tsumo(self, tsumo):
        """
        ツモをエンコードする
        """
        encoded = np.zeros((34, 1))

        if not tsumo:
            return encoded

        suit, number = tsumo[0], int(tsumo[1])
        encoded[self.hai_to_index(suit, number), 0] = 1
        return encoded

    def encode_juntehai(self, juntehai):
        """
        純手牌をエンコードする
        """
        encoded = np.zeros((34, 4))

        for suit in ["m", "p", "s", "z"]:
            for number in range(1, len(juntehai[suit])):
                for _ in range(juntehai[suit][number]):
                    index = self.hai_to_index(suit, number)

                    for i in range(4):
                        if encoded[index, i] == 0:
                            encoded[index, i] = 1
                            break

        return encoded

    def encode_kawa(self, kawa):
        """
        河をエンコードする
        """
        encoded = np.zeros((34, 30))

        for i, hai in enumerate(kawa):
            suit, number = hai[0], int(hai[1])
            encoded[self.hai_to_index(suit, number), i] = 1

        return encoded

    def encode_dora_indicator(self, dora_indicator):
        """
        ドラ表示牌をエンコードする
        """
        encoded = np.zeros((34, 5))

        for i, hai in enumerate(dora_indicator):
            suit, number = hai[0], int(hai[1])
            encoded[self.hai_to_index(suit, number), i] = 1

        return encoded

    def encode_riichi(self, is_riichi):
        """
        リーチ状態をエンコードする
        """
        encoded = np.zeros((34, 4))

        for i, status in enumerate(is_riichi):
            if status:
                encoded[:, i] = 1

        return encoded

    def encode_kaze(self, kaze):
        """
        風をエンコードする
        """
        encoded = np.zeros((34, 4))
        encoded[:, kaze] = 1
        return encoded

    def hai_to_index(self, suit, number):
        """
        牌をインデックスに変換する
        """
        if number == 0:
            number = 5

        if suit == "m":
            return number - 1

        elif suit == "p":
            return 9 + number - 1

        elif suit == "s":
            return 18 + number - 1

        elif suit == "z":
            return 27 + number - 1

    def add(self, prob):
        """
        メモリにデータを追加する
        """
        self.memory.append(prob)

    def update(self, final_reward):
        """
        ポリシーの更新
        """
        grad, loss = 0, 0

        memory_length = len(self.memory)
        rewards = [0] * memory_length
        rewards[-1] = final_reward

        for t in reversed(range(memory_length)):
            reward = rewards[t]
            prob = self.memory[t]
            grad = reward + self.gamma * grad
            loss += -torch.log(prob) * grad

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.memory = []
