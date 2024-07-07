def shanten_kokushi(tehai):
    """
    国士無双形の向聴数を計算する
    """
    if len(tehai.fuuro_) > 0:
        return float("inf")

    n_yaochu = 0
    n_toitsu = 0

    for suit in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai_[suit]
        numbers = [1, 2, 3, 4, 5, 6, 7] if suit == "z" else [1, 9]

        for number in numbers:
            if juntehai[number] >= 1:
                n_yaochu += 1

            if juntehai[number] >= 2:
                n_toitsu += 1

    return 12 - n_yaochu if n_toitsu else 13 - n_yaochu


def shanten_chiitoi(tehai):
    """
    七対子形の向聴数を計算する
    """
    if len(tehai.fuuro_) > 0:
        return float("inf")

    n_toitsu = 0
    n_koritsuhai = 0

    for suit in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai_[suit]

        for number in range(1, len(juntehai)):
            if juntehai[number] >= 2:
                n_toitsu += 1

            elif juntehai[number] == 1:
                n_koritsuhai += 1

    if n_toitsu > 7:
        n_toitsu = 7

    if n_toitsu + n_koritsuhai > 7:
        n_koritsuhai = 7 - n_toitsu

    return 13 - n_toitsu * 2 - n_koritsuhai


def count_taatsu(juntehai):
    """
    塔子数、孤立牌数を数える
    """
    n_pai = 0
    n_taatsu = 0
    n_koritsuhai = 0

    for number in range(1, 10):
        n_pai += juntehai[number]

        if number <= 7 and juntehai[number + 1] == 0 and juntehai[number + 2] == 0:
            n_taatsu += n_pai // 2
            n_koritsuhai += n_pai % 2
            n_pai = 0

    n_taatsu += n_pai // 2
    n_koritsuhai += n_pai % 2

    return {"a": [0, n_taatsu, n_koritsuhai], "b": [0, n_taatsu, n_koritsuhai]}


def count_mentsu(juntehai, number=1):
    """
    面子数を数える
    """
    if number > 9:
        return count_taatsu(juntehai)

    max_result = count_mentsu(juntehai, number + 1)

    if number <= 7 and juntehai[number] > 0 and juntehai[number + 1] > 0 and juntehai[number + 2] > 0:
        juntehai[number] -= 1
        juntehai[number + 1] -= 1
        juntehai[number + 2] -= 1
        result = count_mentsu(juntehai, number)
        juntehai[number] += 1
        juntehai[number + 1] += 1
        juntehai[number + 2] += 1
        result["a"][0] += 1
        result["b"][0] += 1

        if result["a"][2] < max_result["a"][2] or (
            result["a"][2] == max_result["a"][2] and result["a"][1] < max_result["a"][1]
        ):
            max_result["a"] = result["a"]

        if result["b"][0] > max_result["b"][0] or (
            result["b"][0] == max_result["b"][0] and result["b"][1] > max_result["b"][1]
        ):
            max_result["b"] = result["b"]

    if juntehai[number] >= 3:
        juntehai[number] -= 3
        result = count_mentsu(juntehai, number)
        juntehai[number] += 3
        result["a"][0] += 1
        result["b"][0] += 1

        if result["a"][2] < max_result["a"][2] or (
            result["a"][2] == max_result["a"][2] and result["a"][1] < max_result["a"][1]
        ):
            max_result["a"] = result["a"]

        if result["b"][0] > max_result["b"][0] or (
            result["b"][0] == max_result["b"][0] and result["b"][1] > max_result["b"][1]
        ):
            max_result["b"] = result["b"]

    return max_result


def _shanten(n_mentsu, n_taatsu, n_koritsuhai, jantou):
    """
    面子数、塔子数、孤立牌数から向聴数を計算する
    """
    n_block = 4 if jantou else 5

    if n_mentsu > 4:
        n_taatsu += n_mentsu - 4
        n_mentsu = 4

    if n_mentsu + n_taatsu > 4:
        n_koritsuhai += n_mentsu + n_taatsu - 4
        n_taatsu = 4 - n_mentsu

    if n_mentsu + n_taatsu + n_koritsuhai > n_block:
        n_koritsuhai = n_block - n_mentsu - n_taatsu

    if jantou:
        n_taatsu += 1

    return 13 - n_mentsu * 3 - n_taatsu * 2 - n_koritsuhai


def shanten_tehai(tehai, jantou=False):
    """
    手牌から最小の向聴数を計算する
    """
    result = {
        "m": count_mentsu(tehai.juntehai_["m"]),
        "p": count_mentsu(tehai.juntehai_["p"]),
        "s": count_mentsu(tehai.juntehai_["s"]),
    }
    zihai = [0, 0, 0]

    for number in range(1, 8):
        if tehai.juntehai_["z"][number] >= 3:
            zihai[0] += 1

        elif tehai.juntehai_["z"][number] == 2:
            zihai[1] += 1

        elif tehai.juntehai_["z"][number] == 1:
            zihai[2] += 1

    n_fuuro = len(tehai.fuuro_)
    min_shanten = 13

    for manzu in [result["m"]["a"], result["m"]["b"]]:
        for pinzu in [result["p"]["a"], result["p"]["b"]]:
            for souzu in [result["s"]["a"], result["s"]["b"]]:
                shan = [n_fuuro, 0, 0]

                for i in range(3):
                    shan[i] += manzu[i] + pinzu[i] + souzu[i] + zihai[i]

                n_shanten = _shanten(shan[0], shan[1], shan[2], jantou)

                if n_shanten < min_shanten:
                    min_shanten = n_shanten

    return min_shanten


def shanten_ippan(tehai):
    """
    一般形の向聴数を計算する
    """
    min_shanten = shanten_tehai(tehai)

    for suit in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai_[suit]

        for number in range(1, len(juntehai)):
            if juntehai[number] >= 2:
                juntehai[number] -= 2
                n_shanten = shanten_tehai(tehai, True)
                juntehai[number] += 2

                if n_shanten < min_shanten:
                    min_shanten = n_shanten

    if min_shanten == -1 and tehai.tsumo_ and len(tehai.tsumo_) > 2:
        return 0

    return min_shanten


def shanten(tehai):
    """
    向聴数を計算する
    """

    return min(shanten_kokushi(tehai), shanten_chiitoi(tehai), shanten_ippan(tehai))


def yuukouhai(tehai, shanten_func=shanten):
    """
    有効牌を返す
    """
    if tehai.tsumo_:
        return None

    hai = []
    n_shanten = shanten_func(tehai)

    for suit in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai_[suit]

        for number in range(1, len(juntehai)):
            if juntehai[number] >= 4:
                continue

            juntehai[number] += 1

            if shanten_func(tehai) < n_shanten:
                hai.append(f"{suit}{number}")

            juntehai[number] -= 1

    return hai
