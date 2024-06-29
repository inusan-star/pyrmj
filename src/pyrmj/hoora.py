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
