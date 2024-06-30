import math
import re
from .rule import rule
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


def hoora_mentsu(tehai, ron_hai):
    """
    和了形を取得する
    """
    new_tehai = tehai.clone()

    if ron_hai:
        new_tehai.tsumo(ron_hai)

    if not new_tehai.tsumo_ or len(new_tehai.tsumo_) > 2:
        return []

    hoora_hai = (ron_hai if ron_hai else new_tehai.tsumo_ + "_").replace("0", "5")

    mentsu_lists = []
    mentsu_lists.extend(hoora_mentsu_ippan(new_tehai, hoora_hai))
    mentsu_lists.extend(hoora_mentsu_chiitoi(new_tehai, hoora_hai))
    mentsu_lists.extend(hoora_mentsu_kokushi(new_tehai, hoora_hai))
    mentsu_lists.extend(hoora_mentsu_chuuren(new_tehai, hoora_hai))

    return mentsu_lists


def get_fu_data(mentsu_list, bakaze, zikaze):
    """
    符と面子構成情報を取得する
    """
    bakaze_hai = re.compile(f"^z{bakaze + 1}.*$")
    zikaze_hai = re.compile(f"^z{zikaze + 1}.*$")
    sangenpai = r"^z[567].*$"
    yaochu = r"^.*[z19].*$"
    zihai = r"^z.*$"
    kootsu = r"^[mpsz](\d)\1\1.*$"
    anko = r"^[mpsz](\d)\1\1(?:\1|_\!)?$"
    kantsu = r"^[mpsz](\d)\1\1.*\1.*$"
    tanki = r"^[mpsz](\d)\1[\+\=\-\_]\!$"
    kanchan = r"^[mps]\d\d[\+\=\-\_]\!\d$"
    penchan = r"^[mps](123[\+\=\-\_]\!|7[\+\=\-\_]\!89)$"

    fu_data = {
        "fu": 20,
        "menzen": True,
        "tsumo": True,
        "shuntsu": {"m": [0, 0, 0, 0, 0, 0, 0, 0], "p": [0, 0, 0, 0, 0, 0, 0, 0], "s": [0, 0, 0, 0, 0, 0, 0, 0]},
        "kootsu": {
            "m": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "p": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "s": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "z": [0, 0, 0, 0, 0, 0, 0, 0],
        },
        "n_shuntsu": 0,
        "n_kootsu": 0,
        "n_anko": 0,
        "n_kantsu": 0,
        "n_yaochu": 0,
        "n_zihai": 0,
        "tanki": False,
        "pinfu": False,
        "bakaze": bakaze,
        "zikaze": zikaze,
    }

    for mentsu in mentsu_list:
        if re.search(r"[\+\=\-](?!\!)", mentsu):
            fu_data["menzen"] = False

        if re.search(r"[\+\=\-]\!", mentsu):
            fu_data["tsumo"] = False

        if len(mentsu_list) == 1:
            continue

        if re.match(tanki, mentsu):
            fu_data["tanki"] = True

        if len(mentsu_list) == 13:
            continue

        if re.match(yaochu, mentsu):
            fu_data["n_yaochu"] += 1

        if re.match(zihai, mentsu):
            fu_data["n_zihai"] += 1

        if len(mentsu_list) != 5:
            continue

        if mentsu == mentsu_list[0]:
            fu = 0

            if re.match(bakaze_hai, mentsu):
                fu += 2

            if re.match(zikaze_hai, mentsu):
                fu += 2

            if re.match(sangenpai, mentsu):
                fu += 2

            fu_data["fu"] += fu

            if fu_data["tanki"]:
                fu_data["fu"] += 2

        elif re.match(kootsu, mentsu):
            fu_data["n_kootsu"] += 1
            fu = 2

            if re.match(yaochu, mentsu):
                fu *= 2

            if re.match(anko, mentsu):
                fu *= 2
                fu_data["n_anko"] += 1

            if re.match(kantsu, mentsu):
                fu *= 4
                fu_data["n_kantsu"] += 1

            fu_data["fu"] += fu
            fu_data["kootsu"][mentsu[0]][int(mentsu[1])] += 1

        else:
            fu_data["n_shuntsu"] += 1

            if re.match(kanchan, mentsu):
                fu_data["fu"] += 2

            if re.match(penchan, mentsu):
                fu_data["fu"] += 2

            fu_data["shuntsu"][mentsu[0]][int(mentsu[1])] += 1

    if len(mentsu_list) == 7:
        fu_data["fu"] = 25

    elif len(mentsu_list) == 5:
        fu_data["pinfu"] = fu_data["menzen"] and fu_data["fu"] == 20

        if fu_data["tsumo"]:
            if not fu_data["pinfu"]:
                fu_data["fu"] += 2

        else:
            if fu_data["menzen"]:
                fu_data["fu"] += 10

            elif fu_data["fu"] == 20:
                fu_data["fu"] = 30

        fu_data["fu"] = math.ceil(fu_data["fu"] / 10) * 10

    return fu_data


def get_yaku(mentsu_list, fu_data, pre_yaku, post_yaku, rule_json):
    """
    和了役を取得する
    """

    def menzen_tsumo():
        """
        門前清自摸和か判定する
        """
        if fu_data["menzen"] and fu_data["tsumo"]:
            return [{"name": "門前清自摸和", "hansuu": 1}]

        return []

    def yaku_hai():
        """
        役牌か判定する
        """
        kaze_hai = ["東", "南", "西", "北"]
        yaku_hai_all = []

        if fu_data["kootsu"]["z"][fu_data["bakaze"] + 1]:
            yaku_hai_all.append({"name": f'場風 {kaze_hai[fu_data["bakaze"]]}', "hansuu": 1})

        if fu_data["kootsu"]["z"][fu_data["zikaze"] + 1]:
            yaku_hai_all.append({"name": f'自風 {kaze_hai[fu_data["zikaze"]]}', "hansuu": 1})

        if fu_data["kootsu"]["z"][5]:
            yaku_hai_all.append({"name": "役牌 白", "hansuu": 1})

        if fu_data["kootsu"]["z"][6]:
            yaku_hai_all.append({"name": "役牌 發", "hansuu": 1})

        if fu_data["kootsu"]["z"][7]:
            yaku_hai_all.append({"name": "役牌 中", "hansuu": 1})

        return yaku_hai_all

    def pinfu():
        """
        平和か判定する
        """
        if fu_data["pinfu"]:
            return [{"name": "平和", "hansuu": 1}]

        return []

    def tanyao():
        """
        断幺九か判定する
        """
        if fu_data["n_yaochu"] > 0:
            return []

        if rule_json["クイタンあり"] or fu_data["menzen"]:
            return [{"name": "断幺九", "hansuu": 1}]

        return []

    def iipeekoo():
        """
        一盃口か判定する
        """
        if not fu_data["menzen"]:
            return []

        shuntsu = fu_data["shuntsu"]
        peekoo = sum(n >> 1 for n in shuntsu["m"] + shuntsu["p"] + shuntsu["s"])

        if peekoo == 1:
            return [{"name": "一盃口", "hansuu": 1}]

        return []

    def sanshokudoujun():
        """
        三色同順か判定する
        """
        shuntsu = fu_data["shuntsu"]

        for number in range(1, 8):
            if shuntsu["m"][number] and shuntsu["p"][number] and shuntsu["s"][number]:
                return [{"name": "三色同順", "hansuu": 2 if fu_data["menzen"] else 1}]

        return []

    def ikkitsuukan():
        """
        一気通貫か判定する
        """
        shuntsu = fu_data["shuntsu"]

        for suit in ["m", "p", "s"]:
            if shuntsu[suit][1] and shuntsu[suit][4] and shuntsu[suit][7]:
                return [{"name": "一気通貫", "hansuu": 2 if fu_data["menzen"] else 1}]

        return []

    def chanta():
        """
        混全帯幺九か判定する
        """
        if fu_data["n_yaochu"] == 5 and fu_data["n_shuntsu"] > 0 and fu_data["n_zihai"] > 0:
            return [{"name": "混全帯幺九", "hansuu": 2 if fu_data["menzen"] else 1}]

        return []

    def chiitoi():
        """
        七対子か判定する
        """
        if len(mentsu_list) == 7:
            return [{"name": "七対子", "hansuu": 2}]

        return []

    def toitoi():
        """
        対々和か判定する
        """
        if fu_data["n_kootsu"] == 4:
            return [{"name": "対々和", "hansuu": 2}]

        return []

    def sananko():
        """
        三暗刻か判定する
        """
        if fu_data["n_anko"] == 3:
            return [{"name": "三暗刻", "hansuu": 2}]

        return []

    def sankantsu():
        """
        三槓子か判定する
        """
        if fu_data["n_kantsu"] == 3:
            return [{"name": "三槓子", "hansuu": 2}]

        return []

    def sanshokudoukoo():
        """
        三色同刻か判定する
        """
        kootsu = fu_data["kootsu"]

        for number in range(1, 10):
            if kootsu["m"][number] and kootsu["p"][number] and kootsu["s"][number]:
                return [{"name": "三色同刻", "hansuu": 2}]

        return []

    def honroutou():
        """
        混老頭か判定する
        """
        if fu_data["n_yaochu"] == len(mentsu_list) and fu_data["n_shuntsu"] == 0 and fu_data["n_zihai"] > 0:
            return [{"name": "混老頭", "hansuu": 2}]

        return []

    def shousangen():
        """
        小三元か判定する
        """
        kootsu = fu_data["kootsu"]

        if kootsu["z"][5] + kootsu["z"][6] + kootsu["z"][7] == 2 and re.match(r"^z[567]", mentsu_list[0]):
            return [{"name": "小三元", "hansuu": 2}]

        return []

    def honitsu():
        """
        混一色か判定する
        """
        for suit in ["m", "p", "s"]:
            zihai_suit_match = re.compile(f"^[z{suit}]")

            if (
                sum(1 for mentsu in mentsu_list if zihai_suit_match.match(mentsu)) == len(mentsu_list)
                and fu_data["n_zihai"] > 0
            ):
                return [{"name": "混一色", "hansuu": 3 if fu_data["menzen"] else 2}]

        return []

    def junchan():
        """
        純全帯幺九か判定する
        """
        if fu_data["n_yaochu"] == 5 and fu_data["n_shuntsu"] > 0 and fu_data["n_zihai"] == 0:
            return [{"name": "純全帯幺九", "hansuu": 3 if fu_data["menzen"] else 2}]

        return []

    def ryanpeekoo():
        """
        二盃口か判定する
        """
        if not fu_data["menzen"]:
            return []

        shuntsu = fu_data["shuntsu"]
        peekoo = sum(n >> 1 for n in shuntsu["m"] + shuntsu["p"] + shuntsu["s"])

        if peekoo == 2:
            return [{"name": "二盃口", "hansuu": 3}]

        return []

    def tinitsu():
        """
        清一色か判定する
        """
        for suit in ["m", "p", "s"]:
            suit_match = re.compile(f"^[{suit}]")

            if sum(1 for mentsu in mentsu_list if suit_match.match(mentsu)) == len(mentsu_list):
                return [{"name": "清一色", "hansuu": 6 if fu_data["menzen"] else 5}]

        return []

    def kokushi():
        """
        国士無双か判定する
        """
        if len(mentsu_list) != 13:
            return []

        if fu_data["tanki"]:
            return [{"name": "国士無双十三面", "hansuu": "**"}]

        else:
            return [{"name": "国士無双", "hansuu": "*"}]

    def suuanko():
        """
        四暗刻か判定する
        """
        if fu_data["n_anko"] != 4:
            return []

        if fu_data["tanki"]:
            return [{"name": "四暗刻単騎", "hansuu": "**"}]

        else:
            return [{"name": "四暗刻", "hansuu": "*"}]

    def daisangen():
        """
        大三元か判定する
        """
        kootsu = fu_data["kootsu"]

        if kootsu["z"][5] + kootsu["z"][6] + kootsu["z"][7] == 3:
            houjuu_mentsu = [
                mentsu for mentsu in mentsu_list if re.match(r"^z([567])\1\1(?:[\+\=\-]|\1)(?!\!)", mentsu)
            ]
            houjuusha = houjuu_mentsu[2].search(r"[\+\=\-]") if len(houjuu_mentsu) > 2 else None

            if houjuusha:
                return [{"name": "大三元", "hansuu": "*", "houjuusha": houjuusha[0]}]

            else:
                return [{"name": "大三元", "hansuu": "*"}]

        return []

    def suushii():
        """
        四喜和か判定する
        """
        kootsu = fu_data["kootsu"]

        if kootsu["z"][1] + kootsu["z"][2] + kootsu["z"][3] + kootsu["z"][4] == 4:
            houjuu_mentsu = [
                mentsu for mentsu in mentsu_list if re.match(r"^z([1234])\1\1(?:[\+\=\-]|\1)(?!\!)", mentsu)
            ]
            houjuusha = houjuu_mentsu[3].search(r"[\+\=\-]") if len(houjuu_mentsu) > 3 else None

            if houjuusha:
                return [{"name": "大四喜", "hansuu": "**", "houjuusha": houjuusha[0]}]

            else:
                return [{"name": "大四喜", "hansuu": "**"}]

        if kootsu["z"][1] + kootsu["z"][2] + kootsu["z"][3] + kootsu["z"][4] == 3 and re.match(
            r"^z[1234]", mentsu_list[0]
        ):
            return [{"name": "小四喜", "hansuu": "*"}]

        return []

    def tsuuiisoo():
        """
        字一色か判定する
        """
        if fu_data["n_zihai"] == len(mentsu_list):
            return [{"name": "字一色", "hansuu": "*"}]

        return []

    def ryuuiisoo():
        """
        緑一色か判定する
        """
        if any(re.match(r"^[mp]", mentsu) for mentsu in mentsu_list):
            return []

        if any(re.match(r"^z[^6]", mentsu) for mentsu in mentsu_list):
            return []

        if any(re.match(r"^s.*[1579]", mentsu) for mentsu in mentsu_list):
            return []

        return [{"name": "緑一色", "hansuu": "*"}]

    def chinroutou():
        """
        清老頭か判定する
        """
        if fu_data["n_yaochu"] == 5 and fu_data["n_kootsu"] == 4 and fu_data["n_zihai"] == 0:
            return [{"name": "清老頭", "hansuu": "*"}]

        return []

    def suukantsu():
        """
        四槓子か判定する
        """
        if fu_data["n_kantsu"] == 4:
            return [{"name": "四槓子", "hansuu": "*"}]

        return []

    def chuuren():
        """
        九蓮宝燈か判定する
        """
        if len(mentsu_list) != 1:
            return []

        if re.match(r"^[mpsz]1112345678999", mentsu_list[0]):
            return [{"name": "純正九蓮宝燈", "hansuu": "**"}]

        else:
            return [{"name": "九蓮宝燈", "hansuu": "*"}]

    yakuman = pre_yaku if (len(pre_yaku) > 0 and pre_yaku[0]["hansuu"][0] == "*") else []
    yakuman = (
        yakuman
        + kokushi()
        + suuanko()
        + daisangen()
        + suushii()
        + tsuuiisoo()
        + ryuuiisoo()
        + chinroutou()
        + suukantsu()
        + chuuren()
    )

    for yaku in yakuman:
        if not rule_json["ダブル役満あり"]:
            yaku["hansuu"] = "*"

        if not rule_json["役満パオあり"]:
            yaku.pop("houjuusha", None)

    if len(yakuman) > 0:
        return yakuman

    yaku = (
        pre_yaku
        + menzen_tsumo()
        + yaku_hai()
        + pinfu()
        + tanyao()
        + iipeekoo()
        + sanshokudoujun()
        + ikkitsuukan()
        + chanta()
        + chiitoi()
        + toitoi()
        + sananko()
        + sankantsu()
        + sanshokudoukoo()
        + honroutou()
        + shousangen()
        + honitsu()
        + junchan()
        + ryanpeekoo()
        + tinitsu()
    )

    if len(yaku) > 0:
        yaku += post_yaku

    return yaku


def get_tokuten(fu, yaku, ron_hai, param):
    """
    和了点を取得する
    """
    if len(yaku) == 0:
        return {"tokuten": 0}

    zikaze = param["zikaze"]
    hansuu, yakuman, tokuten, base, houjuusha, tokuten2, base2, houjuusha2 = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    if yaku[0]["hansuu"][0] == "*":
        fu = None
        yakuman = 1 if not param["rule"]["役満の複合あり"] else sum(len(y["hansuu"]) for y in yaku)
        base = 8000 * yakuman
        y = next((y for y in yaku if "houjuusha" in y), None)

        if y:
            houjuusha2 = (zikaze + {"+": 1, "=": 2, "-": 3}[y["houjuusha"]]) % 4
            base2 = 8000 * min(len(y["hansuu"]), yakuman)

    else:
        hansuu = sum(y["hansuu"] for y in yaku)

        if hansuu >= 13 and param["rule"]["数え役満あり"]:
            base = 8000

        elif hansuu >= 11:
            base = 6000

        elif hansuu >= 8:
            base = 4000

        elif hansuu >= 6:
            base = 3000

        elif param["rule"]["切り上げ満貫あり"] and fu << (2 + hansuu) == 1920:
            base = 2000

        else:
            base = min(fu << (2 + hansuu), 2000)

    bunpai = [0, 0, 0, 0]
    tsumi = param["kyoutaku"]["tsumibou"]
    riichi = param["kyoutaku"]["riichibou"]

    if houjuusha2 is not None:
        if ron_hai:
            base2 = base2 // 2

        base = base - base2
        tokuten2 = base2 * (6 if zikaze == 0 else 4)
        bunpai[zikaze] += tokuten2
        bunpai[houjuusha2] -= tokuten2

    else:
        tokuten2 = 0

    if ron_hai or base == 0:
        houjuusha = houjuusha2 if base == 0 else (zikaze + {"+": 1, "=": 2, "-": 3}[ron_hai[2]]) % 4
        tokuten = math.ceil(base * (6 if zikaze == 0 else 4) / 100) * 100
        bunpai[zikaze] += tokuten + tsumi * 300 + riichi * 1000
        bunpai[houjuusha] -= tokuten + tsumi * 300

    else:
        oya = math.ceil(base * 2 / 100) * 100
        ko = math.ceil(base / 100) * 100

        if zikaze == 0:
            tokuten = oya * 3

            for i in range(4):
                if i == zikaze:
                    bunpai[i] += tokuten + tsumi * 300 + riichi * 1000

                else:
                    bunpai[i] -= oya + tsumi * 100

        else:
            tokuten = oya + ko * 2

            for i in range(4):
                if i == zikaze:
                    bunpai[i] += tokuten + tsumi * 300 + riichi * 1000

                elif i == 0:
                    bunpai[i] -= oya + tsumi * 100

                else:
                    bunpai[i] -= ko + tsumi * 100

    return {
        "yaku": yaku,
        "fu": fu,
        "hansuu": hansuu,
        "yakuman": yakuman,
        "tokuten": tokuten + tokuten2,
        "bunpai": bunpai,
    }


def hoora(tehai, ron_hai, param):
    """
    和了点を計算する
    """
    if ron_hai:
        if not re.search(r"[\+\=\-]$", ron_hai):
            raise ValueError(f"Invalid ron hai: {ron_hai}")

        ron_hai = ron_hai[:2] + ron_hai[-1]

    max_hoora = {}

    pre_yaku = get_pre_yaku(param["yaku"])
    post_yaku = get_post_yaku(tehai, ron_hai, param["dora"], param["uradora"])

    for mentsu_list in hoora_mentsu(tehai, ron_hai):
        fu_data = get_fu_data(mentsu_list, param["bakaze"], param["zikaze"])
        yaku = get_yaku(mentsu_list, fu_data, pre_yaku, post_yaku, param["rule"])
        result_value = get_tokuten(fu_data["fu"], yaku, ron_hai, param)

        if (
            not max_hoora
            or result_value["tokuten"] > max_hoora["tokuten"]
            or (
                result_value["tokuten"] == max_hoora["tokuten"]
                and (
                    not result_value["hansuu"]
                    or result_value["hansuu"] > max_hoora["hansuu"]
                    or (result_value["hansuu"] == max_hoora["hansuu"] and result_value["fu"] > max_hoora["fu"])
                )
            )
        ):
            max_hoora = result_value

    return max_hoora


def hoora_param(param=None):
    """
    和了点の計算用のパラメータを取得する
    """
    if param is None:
        param = {}

    param_json = {
        "rule": param.get("rule", rule()),
        "bakaze": param.get("bakaze", 0),
        "zikaze": param.get("zikaze", 1),
        "yaku": {
            "riichi": param.get("riichi", 0),
            "ippatsu": param.get("ippatsu", False),
            "haitei": param.get("haitei", False),
            "rinshan": param.get("rinshan", False),
            "chankan": param.get("chankan", 0),
            "tenhoo": param.get("tenhoo", 0),
        },
        "dora": list(param.get("dora")) if param.get("dora") else [],
        "uradora": list(param.get("uradora")) if param.get("uradora") else None,
        "kyoutaku": {
            "tsumibou": param.get("tsumibou", 0),
            "riichibou": param.get("riichibou", 0),
        },
    }

    return param_json
