import re
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

with open("./GL-MahjongTile.base64", "r", encoding="utf-8") as font_file:
    base_font = font_file.read()


def view_tehai(tehai, font_size=50, open_hand=True):
    """
    手牌を表示する
    """
    font_width = font_size * 0.55
    font_height = font_size * 0.81
    margin = font_size * 0.1
    thickness = font_size * 0.02

    svg = svgwrite.Drawing(
        size=(font_width * 20.5 + margin * 2, font_width * 2 + margin * 2),
        profile="full",
    )
    svg.add(
        svg.style(
            f"""@font-face {{
            font-family: 'GL-MahjongTile';
            src: url(data:font/otf;base64,{base_font}) format('opentype');
            }}
        """
        )
    )

    start_x = margin
    tehai_json = tehai.to_json()

    for hai_data in tehai_json["tehai"]["juntehai"]:
        if hai_data["type"] == "tsumo":
            start_x += font_width * 0.5

        if not open_hand:
            hai_data["hai"] = "_"

        svg.add(
            svg.text(
                HAI_UNICODE[hai_data["hai"]],
                insert=(start_x, font_width * 2 + margin),
                font_size=font_size,
                font_family="GL-MahjongTile",
                fill="red" if re.match(r"^[mps]0", hai_data["hai"]) else "black",
            )
        )
        start_x += font_width

    start_x += font_width * 0.5

    for mentsu in tehai_json["tehai"]["fuuro"][::-1]:
        for hai_data in mentsu:
            if hai_data["type"] == "rotate0":
                svg.add(
                    svg.text(
                        HAI_UNICODE[hai_data["hai"]],
                        insert=(start_x + font_height, font_width * 2 + margin),
                        font_size=font_size,
                        font_family="GL-MahjongTile",
                        fill=(
                            "red" if re.match(r"^[mps]0", hai_data["hai"]) else "black"
                        ),
                        transform=f"""rotate(
                            -90,
                            {start_x + font_height + 2 * thickness},
                            {font_width * 2 + margin + thickness}
                        )""",
                    )
                )
                start_x += font_height

            elif hai_data["type"] == "rotate1":
                start_x -= font_height
                svg.add(
                    svg.text(
                        HAI_UNICODE[hai_data["hai"]],
                        insert=(start_x + font_height, font_width + margin),
                        font_size=font_size,
                        font_family="GL-MahjongTile",
                        fill=(
                            "red" if re.match(r"^[mps]0", hai_data["hai"]) else "black"
                        ),
                        transform=f"""rotate(
                            -90,
                            {start_x + font_height + 2 * thickness},
                            {font_width + margin + thickness}
                        )""",
                    )
                )
                start_x += font_height

            else:
                svg.add(
                    svg.text(
                        HAI_UNICODE[hai_data["hai"]],
                        insert=(start_x, font_width * 2 + margin),
                        font_size=font_size,
                        font_family="GL-MahjongTile",
                        fill=(
                            "red" if re.match(r"^[mps]0", hai_data["hai"]) else "black"
                        ),
                    )
                )
                start_x += font_width

        start_x += font_width * 0.5

    display(SVG(svg.tostring()))
