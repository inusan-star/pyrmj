def get_pre_yaku(yaku):
    """
    状況役一覧を取得する
    """
    pre_yaku = []

    if yaku.get("riichi") == 1:
        pre_yaku.append({"name": "立直", "hansuu": 1})

    if yaku.get("riichi") == 2:
        pre_yaku.append({"name": "ダブル立直", "hansuu": 2})

    if yaku.get("ippatsu"):
        pre_yaku.append({"name": "一発", "hansuu": 1})

    if yaku.get("haitei") == 1:
        pre_yaku.append({"name": "海底摸月", "hansuu": 1})

    if yaku.get("haitei") == 2:
        pre_yaku.append({"name": "河底撈魚", "hansuu": 1})

    if yaku.get("rinshan"):
        pre_yaku.append({"name": "嶺上開花", "hansuu": 1})

    if yaku.get("chankan"):
        pre_yaku.append({"name": "槍槓", "hansuu": 1})

    if yaku.get("tenhoo") == 1:
        pre_yaku = [{"name": "天和", "hansuu": "*"}]

    if yaku.get("tenhoo") == 2:
        pre_yaku = [{"name": "地和", "hansuu": "*"}]

    return pre_yaku
