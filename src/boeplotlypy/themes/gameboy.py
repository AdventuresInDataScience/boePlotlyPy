"""Game Boy theme: the original DMG 4-shade olive-green LCD palette, with crisp
8-bit pixel-stepped lines, square markers and sharp dot-matrix bars."""

import plotly.graph_objects as go

NAME = "gameboy"
HIDDEN = True  # easter egg: registered, but not listed or documented

_DARKEST = "#0F380F"
_DARK = "#306230"
_LIGHT = "#8BAC0F"
_LIGHTEST = "#9BBC0F"
_FONT = "VT323, 'Courier New', Consolas, monospace"
# Press Start 2P is too wide for tick labels, so use it for the title only.
_TITLE_FONT = "'Press Start 2P', VT323, 'Courier New', monospace"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _LIGHTEST,
        "plot_bgcolor": _LIGHTEST,
        "font": {"family": _FONT, "size": 14, "color": _DARKEST},
        "title": {"font": {"family": _TITLE_FONT, "size": 20, "color": _DARKEST}},
        "colorway": [_DARKEST, _DARK, _LIGHT, "#5A7A20", "#2A4D1E", "#789B0E",
                     "#43671E", "#A6C32A", "#1B3010", "#6E8F1F"],
        "colorscale": {
            "sequential": [[0, _LIGHTEST], [0.33, _LIGHT], [0.66, _DARK], [1, _DARKEST]],
        },
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": _LIGHTEST,
            "bordercolor": _DARKEST,
            "font": {"family": _FONT, "color": _DARKEST},
        },
        "xaxis": {
            "gridcolor": _LIGHT,
            "griddash": "dot",
            "linecolor": _DARKEST,
            "linewidth": 2,
            "zerolinecolor": _DARK,
            "tickcolor": _DARKEST,
            "tickfont": {"color": _DARKEST},
        },
        "yaxis": {
            "gridcolor": _LIGHT,
            "griddash": "dot",
            "linecolor": _DARKEST,
            "linewidth": 2,
            "zerolinecolor": _DARK,
            "tickcolor": _DARKEST,
            "tickfont": {"color": _DARKEST},
        },
        "legend": {"bgcolor": _LIGHTEST, "bordercolor": _DARKEST, "borderwidth": 2},
    },
    data={
        # 8-bit feel: stepped lines and square "pixel" markers.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 3, "shape": "hv"},
                marker={"symbol": "square", "size": 7},
            )
        ],
        # Sharp dot-matrix columns (no rounding).
        "bar": [go.Bar(marker={"line": {"color": _DARKEST, "width": 2}})],
    },
)
