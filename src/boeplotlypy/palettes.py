"""Bank of England colour palettes, ported from the R package boeCharts.

Source: https://github.com/bank-of-england/boeCharts (``R/colours.R`` and
``R/combinations.R``, commit 45c64d6). Colour names follow boeCharts so the two
can be compared line by line.

Use them as plain data::

    import boeplotlypy as boe

    boe.PALETTES["vibrant_a"]          # ('#00294E', '#E9496A', '#FAD0C5')
    px.bar(..., color_discrete_sequence=boe.PALETTES["boe"])
    px.imshow(..., color_continuous_scale=boe.palettes.colorscale("red_blue"))

To add a palette, add an entry to ``_DEFINITIONS`` under the group it belongs to.
``PALETTES``, ``PALETTE_GROUPS`` and the tests all pick it up.
"""

from __future__ import annotations

import difflib
from types import MappingProxyType

# ---------------------------------------------------------------------------
# Base colour sets. Combination palettes below reference these, as in boeCharts.
# ---------------------------------------------------------------------------

_BOE = {
    "red": "#A51140",
    "light_green": "#7AB800",
    "mid_blue": "#165788",
    "orange": "#E05206",
    "teal": "#00839D",
    "purple": "#4E3780",
    "fuchsia": "#A31A7E",
    "dark_green": "#50882E",
    "dark_blue": "#002A42",
    "yellow": "#EEAF30",
    "dark_teal": "#005E6E",
    "lavender": "#AC98DB",
    "maroon": "#6C0721",
    "light_blue": "#63B1E5",
    "plum": "#752864",
    "stone": "#CAC0B6",
    "black": "#1E1E1E",
}

_RICH = {
    "rich_blue": "#00294E",
    "rich_teal": "#005E6E",
    "rich_green": "#3A7130",
    "rich_orange": "#C94D1B",
    "rich_purple": "#2B1E56",
    "rich_plum": "#5D2049",
    "rich_red": "#AA0B3C",
}

_HIGHLIGHTS = {
    "red": "#E9496A",
    "fuchsia": "#B0358B",
    "purple": "#706CB0",
    "orange": "#EF7B00",
    "green": "#A2C617",
    "teal": "#47AA9C",
    "blue": "#1488CA",
}

_SOFT = {
    "peach": "#FAD0C5",
    "light_pink": "#DA9CC6",
    "mauve": "#D2CDE8",
    "yellow": "#FDC41F",
    "light_green": "#DCE169",
    "light_teal": "#B3DBCD",
    "light_blue": "#85C9F0",
}

_NEUTRAL = {
    "light_grey": "#EBEBEB",
    "grey": "#C8CCCF",
    "dark_grey": "#6B7E87",
    "black": "#1E1E1E",
    "stone": "#D9CEC1",
}

_IDENTITY = {
    "boe_aqua": "#3CD7D9",
    "boe_orange": "#FF7300",
    "boe_purple": "#9E71FE",
    "boe_gold": "#D4AF37",
    "boe_green": "#A5D700",
    "boe_pink": "#FF50C8",
    "boe_azure": "#5297FF",
    "boe_yellow": "#FFD200",
    "boe_peach": "#FF9173",
    "boe_red": "#FD015B",
}

# ---------------------------------------------------------------------------
# All palettes, grouped as in boeCharts' R/palettes.R. Order within each
# palette is the order colours are assigned to series.
# ---------------------------------------------------------------------------

_DEFINITIONS = {
    "identity": {
        "boe_identity": _IDENTITY,
        "boe_brand_main": {
            "boe_dark_blue": "#12273F",
            "boe_aqua": _IDENTITY["boe_aqua"],
            "boe_stone": "#C4C9CF",
        },
        "boe_brand_secondary": {
            "boe_orange": _IDENTITY["boe_orange"],
            "boe_purple": _IDENTITY["boe_purple"],
            "boe_gold": _IDENTITY["boe_gold"],
        },
    },
    "shades": {
        "boe_shades_aqua": {
            "boe_dark_aqua": "#34BCC1",
            "boe_aqua": "#3CD7D9",
            "boe_mid_aqua": "#77E3E4",
            "boe_light_aqua": "#A7EDEE",
            "boe_extra_light_aqua": "#CEF5F5",
        },
    },
    "standard": {
        "boe": _BOE,
        "boe_rich": _RICH,
        "boe_highlights": _HIGHLIGHTS,
        "boe_soft": _SOFT,
        "boe_neutral": _NEUTRAL,
    },
    "harmonious": {
        "harmonious_blue": {
            "rich_blue": _RICH["rich_blue"],
            "blue": _HIGHLIGHTS["blue"],
            "light_blue": _SOFT["light_blue"],
        },
        "harmonious_teal": {
            "rich_teal": _RICH["rich_teal"],
            "teal": _HIGHLIGHTS["teal"],
            "light_teal": _SOFT["light_teal"],
        },
        "harmonious_green": {
            "rich_green": _RICH["rich_green"],
            "green": _HIGHLIGHTS["green"],
            "light_green": _SOFT["light_green"],
        },
        "harmonious_orange": {
            "rich_orange": _RICH["rich_orange"],
            "orange": _HIGHLIGHTS["orange"],
            "yellow": _SOFT["yellow"],
        },
        "harmonious_purple": {
            "rich_purple": _RICH["rich_purple"],
            "purple": _HIGHLIGHTS["purple"],
            "mauve": _SOFT["mauve"],
        },
        "harmonious_pink": {
            "rich_plum": _RICH["rich_plum"],
            "fuchsia": _HIGHLIGHTS["fuchsia"],
            "light_pink": _SOFT["light_pink"],
        },
        "harmonious_red": {
            "rich_red": _RICH["rich_red"],
            "red": _HIGHLIGHTS["red"],
            "peach": _SOFT["peach"],
        },
        "harmonious_grey": {
            "black": _NEUTRAL["black"],
            "dark_grey": _NEUTRAL["dark_grey"],
            "grey": _NEUTRAL["grey"],
        },
    },
    "vibrant": {
        "vibrant_a": {
            "rich_blue": _RICH["rich_blue"],
            "red": _HIGHLIGHTS["red"],
            "peach": _SOFT["peach"],
        },
        "vibrant_b": {
            "rich_blue": _RICH["rich_blue"],
            "teal": _HIGHLIGHTS["teal"],
            "light_green": _SOFT["light_green"],
        },
        "vibrant_c": {
            "rich_purple": _RICH["rich_purple"],
            "purple": _HIGHLIGHTS["purple"],
            "yellow": _SOFT["yellow"],
        },
        "vibrant_d": {
            "rich_plum": _RICH["rich_plum"],
            "blue": _HIGHLIGHTS["blue"],
            "light_blue": _SOFT["light_blue"],
        },
        "vibrant_e": {
            "rich_teal": _RICH["rich_teal"],
            "red": _HIGHLIGHTS["red"],
            "grey": _NEUTRAL["grey"],
        },
        "vibrant_f": {
            "rich_red": _RICH["rich_red"],
            "orange": _HIGHLIGHTS["orange"],
            "peach": _SOFT["peach"],
        },
        "vibrant_g": {
            "rich_green": _RICH["rich_green"],
            "teal": _HIGHLIGHTS["teal"],
            "mauve": _SOFT["mauve"],
        },
        "vibrant_h": {
            # boeCharts references `boe_rich$orange`, which doesn't exist, so in R
            # this palette silently loses its first colour. rich_orange is the
            # evident intent.
            "rich_orange": _RICH["rich_orange"],
            "fuchsia": _HIGHLIGHTS["fuchsia"],
            "yellow": _SOFT["yellow"],
        },
    },
    "diverging": {
        "red_blue": {
            "red": _RICH["rich_red"],
            "grey": _NEUTRAL["light_grey"],
            "blue": _RICH["rich_blue"],
        },
        "red_green": {
            "red": _RICH["rich_red"],
            "grey": _NEUTRAL["light_grey"],
            "green": _RICH["rich_green"],
        },
        "red_gray": {
            "red": _RICH["rich_red"],
            "grey": _NEUTRAL["light_grey"],
            "dark_grey": _NEUTRAL["dark_grey"],
        },
        "red_yellow_green": {
            "red": _RICH["rich_red"],
            "yellow": _SOFT["yellow"],
            "green": _RICH["rich_green"],
        },
        "red_yellow_blue": {
            "red": _RICH["rich_red"],
            "yellow": _SOFT["yellow"],
            "blue": _RICH["rich_blue"],
        },
        "purple_green": {
            "purple": _HIGHLIGHTS["purple"],
            "grey": _NEUTRAL["light_grey"],
            "green": _RICH["rich_green"],
        },
        "pink_green": {
            "pink": _HIGHLIGHTS["fuchsia"],
            "grey": _NEUTRAL["light_grey"],
            "green": _RICH["rich_green"],
        },
    },
    "publication": {
        "boe_website": {
            "boe_rich_blue": _RICH["rich_blue"],
            "boe_red": _HIGHLIGHTS["red"],
            "boe_rich_teal": _RICH["rich_teal"],
        },
        "boe_overground": {
            "boe_purple": _HIGHLIGHTS["purple"],
            "boe_red": _HIGHLIGHTS["red"],
            "boe_rich_purple": _RICH["rich_purple"],
        },
        "pre_mpc": {
            "red": _BOE["red"],
            "dark_blue": _BOE["dark_blue"],
            "stone": "#B39F87",
            "dark_green": _BOE["dark_green"],
            "yellow": _BOE["yellow"],
            "fuchsia": _BOE["fuchsia"],
            "orange": _BOE["orange"],
        },
        "pre_mpc_light": {
            "light_red": "#D182AB",
            "light_blue": "#6199CB",
            "light_stone": "#D9CEC1",
        },
        "fsr": {
            "mid_blue": "#165788",
            "dark_pink": "#A31A7E",
            "golden_yellow": "#EEAF30",
            "lime_green": "#7AB800",
            "light_blue": "#63B1E5",
            "summer_red": "#D53647",
            "violet": "#6773B6",
            "deep_turquoise": "#005E6E",
            "leaf_green": "#69923A",
            "khaki": "#A79E70",
            "warm_grey": "#CAC0B6",
            "purple": "#57068C",
            "plum": "#752864",
            "lavender": "#AC98DB",
            "red": "#A51140",
            "dark_orange": "#E05206",
            "light_orange": "#DF7A00",
        },
        "fsr_main": {
            "boe_purple": _HIGHLIGHTS["purple"],
            "boe_rich_purple": _RICH["rich_purple"],
        },
        "fsr_currency": {
            "sterling": "#165788",
            "usd": "#A31A7E",
            "euro": "#EEAF30",
            "yen": "#7AB800",
        },
        "fsr_average": {
            "light_orange": "#DF7A00",
            "mid_blue": "#165788",
            "light_blue": "#63B1E5",
        },
        "mpr_main": {
            "boe_teal": _HIGHLIGHTS["teal"],
            "boe_green": _HIGHLIGHTS["green"],
        },
        "mcg": {
            "fuchsia": "#FF00FF",
            "dark_blue": "#000066",
            "green": "#008000",
            "aqua_blue": "#39F9F9",
            "maroon": "#993366",
            "orange": "#FD9900",
        },
    },
}


#: Every palette by name, e.g. ``PALETTES["boe"]``: a tuple of hex colours. Read-only.
PALETTES = MappingProxyType({
    name: tuple(colours.values())
    for group in _DEFINITIONS.values()
    for name, colours in group.items()
})

#: Palette names by group (identity, shades, standard, harmonious, vibrant,
#: diverging, publication), as boeCharts groups them.
PALETTE_GROUPS = MappingProxyType({group: tuple(palettes) for group, palettes in _DEFINITIONS.items()})


def palette_colours(palette: str | list[str] | tuple[str, ...]) -> list[str]:
    """Return a palette's colours, given its name or a list of colours.

    An unknown name raises a ``KeyError`` that suggests the closest names.
    """
    if not isinstance(palette, str):
        return list(palette)
    if palette not in PALETTES:
        close = difflib.get_close_matches(palette, PALETTES, n=3)
        hint = f" Did you mean: {', '.join(close)}?" if close else ""
        raise KeyError(f"Unknown palette {palette!r}.{hint} Available palettes: {', '.join(PALETTES)}.")
    return list(PALETTES[palette])


# Continuous scales. boeCharts interpolates between palette colours in CIELAB
# (scales::gradient_n_pal(..., "Lab")), which keeps blends bright, whereas
# Plotly interpolates in RGB between colourscale stops. So colorscale() samples
# the Lab gradient at enough stops that Plotly's RGB steps between them are
# invisible.

_WHITE_D65 = (0.95047, 1.0, 1.08883)
_STOPS = 21


def _hex_to_lab(colour: str) -> tuple[float, float, float]:
    rgb = [int(colour.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    r, g, b = (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb)
    xyz = (
        0.4124564 * r + 0.3575761 * g + 0.1804375 * b,
        0.2126729 * r + 0.7151522 * g + 0.0721750 * b,
        0.0193339 * r + 0.1191920 * g + 0.9503041 * b,
    )
    fx, fy, fz = (
        t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29
        for t in (v / w for v, w in zip(xyz, _WHITE_D65))
    )
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _lab_to_hex(lab: tuple[float, float, float]) -> str:
    L, a, b = lab
    fy = (L + 16) / 116
    x, y, z = (
        (t ** 3 if t > 6 / 29 else 3 * (6 / 29) ** 2 * (t - 4 / 29)) * w
        for t, w in zip((fy + a / 500, fy, fy - b / 200), _WHITE_D65)
    )
    linear = (
        3.2404542 * x - 1.5371385 * y - 0.4985314 * z,
        -0.9692660 * x + 1.8760108 * y + 0.0415560 * z,
        0.0556434 * x - 0.2040259 * y + 1.0572252 * z,
    )
    rgb = (12.92 * c if c <= 0.0031308 else 1.055 * max(c, 0.0) ** (1 / 2.4) - 0.055 for c in linear)
    return "#" + "".join(f"{round(min(max(c, 0.0), 1.0) * 255):02X}" for c in rgb)


def colorscale(palette: str | list[str], reverse: bool = False) -> list[list]:
    """Return a Plotly colourscale running evenly through a palette's colours.

    The equivalent of boeCharts' ``scale_colour_continuous_boe(palette)``. Pass
    the result to ``color_continuous_scale=`` (Plotly Express) or
    ``colorscale=`` (graph objects).

    Args:
        palette: A palette name from ``PALETTES``, or a list of hex colours.
        reverse: Run the colours in the opposite order (e.g. blue to red
            rather than red to blue).
    """
    colours = palette_colours(palette)
    if reverse:
        colours.reverse()
    if len(colours) == 1:
        colours *= 2
    labs = [_hex_to_lab(c) for c in colours]
    segments = len(labs) - 1
    scale = []
    for i in range(_STOPS):
        pos = i / (_STOPS - 1)
        seg = min(int(pos * segments), segments - 1)
        t = pos * segments - seg
        lab = tuple(a + (b - a) * t for a, b in zip(labs[seg], labs[seg + 1]))
        scale.append([round(pos, 6), _lab_to_hex(lab)])
    # Use the exact palette colours at the ends, free of conversion rounding.
    scale[0][1], scale[-1][1] = colours[0].upper(), colours[-1].upper()
    return scale
