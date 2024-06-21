def shanten_kokushi(tehai):
    """
    国士無双形の向聴数を計算する
    """
    if len(tehai.fuuro) > 0:
        return float("inf")

    n_yaochu = 0
    n_toitsu = 0

    for s in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai[s]
        nn = [1, 2, 3, 4, 5, 6, 7] if s == "z" else [1, 9]

        for n in nn:
            if juntehai[n] >= 1:
                n_yaochu += 1

            if juntehai[n] >= 2:
                n_toitsu += 1

    return 12 - n_yaochu if n_toitsu else 13 - n_yaochu


def shanten_chiitoi(tehai):
    """
    七対子形の向聴数を計算する
    """
    if len(tehai.fuuro) > 0:
        return float("inf")

    n_toitsu = 0
    n_koritsuhai = 0

    for s in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai[s]

        for n in range(1, len(juntehai)):
            if juntehai[n] >= 2:
                n_toitsu += 1

            elif juntehai[n] == 1:
                n_koritsuhai += 1

    if n_toitsu > 7:
        n_toitsu = 7

    if n_toitsu + n_koritsuhai > 7:
        n_koritsuhai = 7 - n_toitsu

    return 13 - n_toitsu * 2 - n_koritsuhai
