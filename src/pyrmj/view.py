import re
import os
import svgwrite
from IPython.display import SVG, display

HAI_UNICODE = {
    "m0": "🀋",
    "m1": "🀇",
    "m2": "🀈",
    "m3": "🀉",
    "m4": "🀊",
    "m5": "🀋",
    "m6": "🀌",
    "m7": "🀍",
    "m8": "🀎",
    "m9": "🀏",
    "p0": "🀝",
    "p1": "🀙",
    "p2": "🀚",
    "p3": "🀛",
    "p4": "🀜",
    "p5": "🀝",
    "p6": "🀞",
    "p7": "🀟",
    "p8": "🀠",
    "p9": "🀡",
    "s0": "🀔",
    "s1": "🀐",
    "s2": "🀑",
    "s3": "🀒",
    "s4": "🀓",
    "s5": "🀔",
    "s6": "🀕",
    "s7": "🀖",
    "s8": "🀗",
    "s9": "🀘",
    "z1": "🀀",
    "z2": "🀁",
    "z3": "🀂",
    "z4": "🀃",
    "z5": "🀆",
    "z6": "🀅",
    "z7": "🀄",
    "_": "🀫",
}

with open(
    os.path.join(os.path.dirname(__file__), "../data/GL-MahjongTile.base64"),
    "r",
    encoding="utf-8",
) as font_file:
    base_font = font_file.read()


def add_text(svg, text, x, y, font_size, red, rotate=False):
    """
    SVGにテキストを追加する
    """

    for i, t in enumerate([text, "🀆"] if red else [text]):
        text_element = svg.text(
            t,
            insert=(x, y),
            font_size=font_size,
            font_family="GL-MahjongTile",
            fill="red" if red and i == 0 else "black",
        )

        if rotate:
            text_element["transform"] = (
                f"rotate(-90, {x + 0.04 * font_size}, {y + 0.02 * font_size})"
            )

        svg.add(text_element)


def view_tehai(tehai, font_size=50, open_hand=True):
    """
    手牌を表示する
    """
    font_width = font_size * 0.55
    font_height = font_size * 0.81
    margin = font_size * 0.1

    svg = svgwrite.Drawing(
        size=(font_width * 20.5 + margin * 2, font_width * 2 + margin * 2),
        profile="full",
    )
    svg.add(
        svg.style(
            f"""@font-face {{
                font-family: 'GL-MahjongTile';
                src: url(data:font/otf;base64,{base_font}) format('opentype');
            }}"""
        )
    )

    start_x = margin
    tehai_json = tehai.to_json()

    for hai_data in tehai_json["tehai"]["juntehai"]:
        if hai_data["type"] == "tsumo":
            start_x += font_width * 0.5

        text = HAI_UNICODE[hai_data["hai"]] if open_hand else HAI_UNICODE["_"]
        add_text(
            svg,
            text,
            start_x,
            font_width * 2 + margin,
            font_size,
            re.match(r"^[mps]0", hai_data["hai"]),
        )
        start_x += font_width

    start_x += font_width * 0.5

    for mentsu in tehai_json["tehai"]["fuuro"][::-1]:
        for hai_data in mentsu:
            text = HAI_UNICODE[hai_data["hai"]]
            rotate_type = re.match(r"^rotate([0-9])", hai_data["type"])

            if rotate_type:
                if rotate_type.group(1) == "1":
                    start_x -= font_height

                add_text(
                    svg,
                    text,
                    start_x + font_height,
                    font_width * (2 - int(rotate_type.group(1))) + margin,
                    font_size,
                    re.match(r"^[mps]0", hai_data["hai"]),
                    True,
                )
                start_x += font_height

            else:
                add_text(
                    svg,
                    text,
                    start_x,
                    font_width * 2 + margin,
                    font_size,
                    re.match(r"^[mps]0", hai_data["hai"]),
                )
                start_x += font_width

        start_x += font_width * 0.5

    display(SVG(svg.tostring()))
