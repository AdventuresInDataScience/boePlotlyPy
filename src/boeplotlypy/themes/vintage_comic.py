"""Vintage comic theme: classic Golden/Silver-Age comic book — bright white
pages, yellow caption-box panels, garish primary inks, bold black outlines, a
punchy display title and Ben-Day dot fills."""

import plotly.graph_objects as go

NAME = "vintage_comic"
HIDDEN = True  # easter egg: registered, but not listed or documented

_PAGE = "#FFFFFF"  # comics were printed on white pages, not beige
_CAPTION = "#FFF1A8"  # the yellow caption/letter box
_INK = "#1A1A1A"
_GRID = "#E4E4E4"
_TITLE_FONT = "Bangers, Impact, 'Comic Sans MS', cursive"
_BODY_FONT = "'Comic Neue', 'Comic Sans MS', 'Trebuchet MS', sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _PAGE,
        "plot_bgcolor": _PAGE,
        "font": {"family": _BODY_FONT, "size": 15, "color": _INK},
        "title": {"font": {"family": _TITLE_FONT, "size": 36, "color": "#ED1C24"}},
        # Garish four-colour comic inks: blue, red, yellow, green, pink, purple,
        # orange, cyan, lime, magenta.
        "colorway": [
            "#1F6FE5", "#ED1C24", "#FFC200", "#2BB24C", "#EC4D9C",
            "#8E44AD", "#FF7A00", "#00B7C7", "#7BC043", "#C724B1",
        ],
        "colorscale": {
            "sequential": [[0, "#FFFFFF"], [0.5, "#FFC200"], [1, "#ED1C24"]],
            "diverging": [[0, "#1F6FE5"], [0.5, "#FFFFFF"], [1, "#ED1C24"]],
        },
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": _CAPTION,
            "bordercolor": _INK,
            "font": {"family": _BODY_FONT, "color": _INK},
        },
        # A thick black box around the plot, like a comic-strip panel border.
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": _INK,
            "linewidth": 4,
            "mirror": True,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": _INK,
            "linewidth": 4,
            "mirror": True,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
        },
        # The legend reads like a yellow caption box.
        "legend": {"bgcolor": _CAPTION, "bordercolor": _INK, "borderwidth": 2},
    },
    data={
        # Ben-Day dots printed over each bright fill, with heavy comic-art inking.
        "bar": [
            go.Bar(
                marker={
                    "line": {"color": _INK, "width": 3},
                    "pattern": {
                        "shape": ".",
                        "fillmode": "overlay",
                        "fgcolor": _INK,
                        "fgopacity": 0.35,
                        "size": 14,
                        "solidity": 0.5,
                    },
                }
            )
        ],
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 4},
                marker={"size": 11, "line": {"color": _INK, "width": 2}},
            )
        ],
    },
)
