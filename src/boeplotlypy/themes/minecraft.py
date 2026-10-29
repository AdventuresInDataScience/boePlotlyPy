"""Minecraft theme: blocky and game-like — the dark dirt/stone GUI look with a
bright grass-green/diamond/redstone block palette, hard-edged "pixel" columns,
square markers, stepped lines and a pixel-font title."""

import plotly.graph_objects as go

NAME = "minecraft"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#322C26"  # dark dirt/stone menu background
_PANEL = "#423B33"
_TEXT = "#ECE6DA"
_GRASS = "#6CC04A"
_INK = "#1B1813"
_GRID = "#554D43"
_TITLE_FONT = "'Press Start 2P', 'Courier New', monospace"
_BODY_FONT = "VT323, 'Courier New', Consolas, monospace"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _BODY_FONT, "size": 16, "color": _TEXT},
        "title": {"font": {"family": _TITLE_FONT, "size": 18, "color": _GRASS}},
        # Grass, dirt, stone, diamond, redstone, gold — Minecraft block colours.
        "colorway": ["#6CC04A", "#9C6B3F", "#A8A8A8", "#3FD3C6", "#D83A2B", "#F9C22E",
                     "#4F8F2E", "#5BA3D0", "#C8A24B", "#7E5C39"],
        "colorscale": {
            "sequential": [[0, "#322C26"], [0.5, "#9C6B3F"], [1, "#6CC04A"]],
        },
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": _INK,
            "bordercolor": _GRASS,
            "font": {"family": _BODY_FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _TEXT},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _PANEL, "bordercolor": _INK, "borderwidth": 2},
    },
    data={
        # Everything is a block: sharp columns with thick outlines, square markers,
        # stepped lines.
        "bar": [go.Bar(marker={"line": {"color": _INK, "width": 2.5}})],
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 3, "shape": "hv"},
                marker={"symbol": "square", "size": 9, "line": {"color": _INK, "width": 1.5}},
            )
        ],
    },
)
