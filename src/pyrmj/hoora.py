import re
from .yama import Yama


def get_pre_yaku(yaku):
    """
    状況役一覧を取得する
    """
    pre_yaku = []

    if yaku["riichi"] == 1:
        pre_yaku.append({"name": "立直", "hansuu": 1})

    if yaku["riichi"] == 2:
        pre_yaku.append({"name": "ダブル立直", "hansuu": 2})

    if yaku["ippatsu"]:
        pre_yaku.append({"name": "一発", "hansuu": 1})

    if yaku["haitei"] == 1:
        pre_yaku.append({"name": "海底摸月", "hansuu": 1})

    if yaku["haitei"] == 2:
        pre_yaku.append({"name": "河底撈魚", "hansuu": 1})

    if yaku["rinshan"]:
        pre_yaku.append({"name": "嶺上開花", "hansuu": 1})

    if yaku["chankan"]:
        pre_yaku.append({"name": "槍槓", "hansuu": 1})

    if yaku["tenhoo"] == 1:
        pre_yaku = [{"name": "天和", "hansuu": "*"}]

    if yaku["tenhoo"] == 2:
        pre_yaku = [{"name": "地和", "hansuu": "*"}]

    return pre_yaku


def get_post_yaku(tehai, ron_hai, dora, uradora):
    """
    懸賞役一覧を取得する
    """
    new_tehai = tehai.clone()

    if ron_hai:
        new_tehai.tsumo(ron_hai)

    tehai_string = new_tehai.to_string()
    post_yaku = []
    suit_string_list = re.findall(r"[mpsz][^mpsz,]*", tehai_string)
    n_dora = 0

    for hai in dora:
        hai = Yama.dora(hai)
        regexp = re.compile(hai[1])

        for suit_string in suit_string_list:
            if suit_string[0] != hai[0]:
                continue

            suit_string = suit_string.replace("0", "5")
            numbers = regexp.findall(suit_string)

            if numbers:
                n_dora += len(numbers)

    if n_dora:
        post_yaku.append({"name": "ドラ", "hansuu": n_dora})

    n_akahai = tehai_string.count("0")

    if n_akahai > 0:
        post_yaku.append({"name": "赤ドラ", "hansuu": n_akahai})

    n_uradora = 0

    for hai in uradora or []:
        hai = Yama.dora(hai)
        regexp = re.compile(hai[1])

        for suit_string in suit_string_list:
            if suit_string[0] != suit_string[0]:
                continue

            suit_string = suit_string.replace("0", "5")
            numbers = regexp.findall(suit_string)

            if numbers:
                n_uradora += len(numbers)

    if n_uradora:
        post_yaku.append({"name": "裏ドラ", "hansuu": n_uradora})

    return post_yaku


def hoora_mentsu_kokushi(tehai, hoora_hai):
    """
    国士無双形の和了形を取得する
    """
    if len(tehai.fuuro_) > 0:
        return []

    mentsu_list = []
    n_toitsu = 0

    for suit in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai_[suit]
        numbers = [1, 2, 3, 4, 5, 6, 7] if suit == "z" else [1, 9]

        for number in numbers:
            if juntehai[number] == 2:
                mentsu = (
                    f"{suit}{str(number) * 2}{hoora_hai[2]}!"
                    if (f"{suit}{number}" == hoora_hai[:2])
                    else f"{suit}{str(number) * 2}"
                )
                mentsu_list.insert(0, mentsu)
                n_toitsu += 1

            elif juntehai[number] == 1:
                mentsu = f"{suit}{number}{hoora_hai[2]}!" if (f"{suit}{number}" == hoora_hai[:2]) else f"{suit}{number}"
                mentsu_list.append(mentsu)

            else:
                return []

    return [mentsu_list] if n_toitsu == 1 else []


def hoora_mentsu_chiitoi(tehai, hoora_hai):
    """
    七対子形の和了形を取得する
    """
    if len(tehai.fuuro_) > 0:
        return []

    mentsu_list = []

    for suit in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai_[suit]

        for number in range(1, len(juntehai)):
            if juntehai[number] == 0:
                continue

            if juntehai[number] == 2:
                mentsu = (
                    f"{suit}{str(number) * 2}{hoora_hai[2]}!"
                    if (f"{suit}{number}" == hoora_hai[:2])
                    else f"{suit}{str(number) * 2}"
                )
                mentsu_list.append(mentsu)

            else:
                return []

    return [mentsu_list] if len(mentsu_list) == 7 else []


def hoora_mentsu_chuuren(tehai, hoora_hai):
    """
    九蓮宝燈形の和了形を取得する
    """
    if len(tehai.fuuro_) > 0:
        return []

    suit = hoora_hai[0]
    if suit == "z":
        return []

    mentsu = suit
    juntehai = tehai.juntehai_[suit]

    for number in range(1, 10):
        if juntehai[number] == 0:
            return []

        if (number == 1 or number == 9) and juntehai[number] < 3:
            return []

        n_pai = juntehai[number] - 1 if number == int(hoora_hai[1]) else juntehai[number]

        for _ in range(n_pai):
            mentsu += str(number)

    if len(mentsu) != 14:
        return []

    mentsu += f"{hoora_hai[1:]}!"
    return [[mentsu]]


def mentsu_suit(suit, juntehai, number=1):
    """
    同色内の面子を取得する
    """
    if number > 9:
        return [[]]

    if juntehai[number] == 0:
        return mentsu_suit(suit, juntehai, number + 1)

    shuntsu = []

    if number <= 7 and juntehai[number] > 0 and juntehai[number + 1] > 0 and juntehai[number + 2] > 0:
        juntehai[number] -= 1
        juntehai[number + 1] -= 1
        juntehai[number + 2] -= 1
        shuntsu = mentsu_suit(suit, juntehai, number)
        juntehai[number] += 1
        juntehai[number + 1] += 1
        juntehai[number + 2] += 1

        for shuntsu_mentsu in shuntsu:
            shuntsu_mentsu.insert(0, f"{suit}{number}{number + 1}{number + 2}")

    kootsu = []

    if juntehai[number] == 3:
        juntehai[number] -= 3
        kootsu = mentsu_suit(suit, juntehai, number + 1)
        juntehai[number] += 3

        for kootsu_mentsu in kootsu:
            kootsu_mentsu.insert(0, f"{suit}{str(number) * 3}")

    return shuntsu + kootsu


def mentsu_all(tehai):
    """
    4面子となる組み合わせを全て取得する
    """
    tehai_all = [[]]

    for suit in ["m", "p", "s"]:
        new_mentsu = []

        for mentsu_list in tehai_all:
            for mentsu_suit_list in mentsu_suit(suit, tehai.juntehai_[suit]):
                new_mentsu.append(mentsu_list + mentsu_suit_list)

        tehai_all = new_mentsu

    zihai = []

    for number in range(1, 8):
        if tehai.juntehai_["z"][number] == 0:
            continue

        if tehai.juntehai_["z"][number] != 3:
            return []

        zihai.append(f"z{str(number) * 3}")

    fuuro = [mentsu.replace("0", "5") for mentsu in tehai.fuuro_]

    return [te_hai + zihai + fuuro for te_hai in tehai_all]


def add_hoora_hai(mentsu, hai):
    """
    和了牌にマークを付ける
    """
    suit, number, direction = hai[0], hai[1], hai[2]
    new_mentsu = []

    for i, mentsu_item in enumerate(mentsu):
        if re.search(r"[\+\=\-]|\d{4}", mentsu_item):
            continue

        if i > 0 and mentsu_item == mentsu[i - 1]:
            continue

        replaced_mentsu = re.sub(re.compile(f"^({suit}.*{number})"), r"\g<1>" + f"{direction}!", mentsu_item)

        if replaced_mentsu == mentsu_item:
            continue

        tmp_mentsu = mentsu[:]
        tmp_mentsu[i] = replaced_mentsu
        new_mentsu.append(tmp_mentsu)

    return new_mentsu


def hoora_mentsu_ippan(tehai, hoora_hai):
    """
    一般形の和了形を取得する
    """
    mentsu_lists = []

    for suit in ["m", "p", "s", "z"]:
        juntehai = tehai.juntehai_[suit]

        for number in range(1, len(juntehai)):
            if juntehai[number] < 2:
                continue

            juntehai[number] -= 2
            jantou = f"{suit}{str(number) * 2}"

            for mentsu_list in mentsu_all(tehai):
                mentsu_list.insert(0, jantou)

                if len(mentsu_list) != 5:
                    continue

                mentsu_lists.extend(add_hoora_hai(mentsu_list, hoora_hai))

            juntehai[number] += 2

    return mentsu_lists
