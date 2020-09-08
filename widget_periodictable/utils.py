"""Utility functions"""

import re


HTML_COLOR_MAP = {
    "white": [
        255,
    ]
    * 3,
    "silver": [round(0.75 * i) for i in (255,) * 3],
    "gray": [round(0.5 * i) for i in (255,) * 3],
    "black": [
        0,
    ]
    * 3,
    "red": [255, 0, 0],
    "maroon": [round(0.5 * 255), 0, 0],
    "yellow": [255, 255, 0],
    "olive": [round(0.5 * i) for i in (255, 255, 0)],
    "lime": [0, 255, 0],
    "green": [0, round(0.5 * 255), 0],
    "aqua": [0, 255, 255],
    "teal": [round(0.5 * i) for i in (0, 255, 255)],
    "blue": [0, 0, 255],
    "navy": [0, 0, round(0.5 * 255)],
    "fuchsia": [255, 0, 255],
    "purple": [round(0.5 * i) for i in (255, 0, 255)],
    "pink": [255, 192, 203],
}


def faded_color(color: str, opacity: float = 0.38, as_rgb: bool = False) -> str:
    """Calculate rgb with X % opacity (default: 38 %) of color (white background)"""
    if re.match(r"#[a-fA-F0-9]{6}", color):
        # Hex color
        color = color.lstrip("#")
        color = [int(color[i : i + 2], 16) for i in (0, 2, 4)]
    elif re.match(r"rgb\([0-9]{1,3}(,\s*[0-9]{1,3}){2}\)", color):
        # RGB color
        tmp_color = color.lstrip("rgb(").rstrip(")")
        tmp_color = re.match(
            r"(?P<R>[0-9]{1,3}),\s*(?P<G>[0-9]{1,3}),\s*(?P<B>[0-9]{1,3})", tmp_color
        )
        if tmp_color is None:
            raise ValueError(f"Could not recognize rgb number in {color!r}")
        color = [int(tmp_color.group(i)) for i in ("R", "G", "B")]
        del tmp_color
    else:
        # Color name
        try:
            color = HTML_COLOR_MAP[color]
        except KeyError:
            # Return the color right back, un-faded
            return color

    color = tuple(round(255 - opacity * (255 - i)) for i in color)
    if as_rgb:
        return "".join(f"rgb{color!r}".split(" "))
    return "#{}".format("".join([hex(i)[2:] for i in color]))
