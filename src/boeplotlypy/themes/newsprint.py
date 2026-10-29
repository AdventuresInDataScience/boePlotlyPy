"""Newsprint theme: black-and-white newspaper — off-white paper, serif type, a
greyscale palette with a single ink-red accent, and halftone-dot bar fills."""

import plotly.graph_objects as go

NAME = "newsprint"
HIDDEN = True  # easter egg: registered, but not listed or documented

_PAPER = "#F4F1E8"
_INK = "#1A1A1A"
_RED = "#8B0000"
_GRID = "#D8D3C4"
_FONT = "Georgia, 'Times New Roman', 'Times', serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _PAPER,
        "plot_bgcolor": _PAPER,
        "font": {"family": _FONT, "size": 15, "color": _INK},
        "title": {"font": {"family": _FONT, "size": 30, "color": _INK}},
        # Greyscale "ink" tones plus one classic newspaper red.
        "colorway": ["#1A1A1A", "#707070", "#A9A9A9", "#8B0000", "#4D4D4D", "#C8C8C8",
                     "#2E2E2E", "#9E9E9E", "#5E0000", "#D8D8D8"],
        "colorscale": {
            "sequential": [[0, "#F4F1E8"], [0.5, "#707070"], [1, "#1A1A1A"]],
            "diverging": [[0, "#8B0000"], [0.5, "#F4F1E8"], [1, "#1A1A1A"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _PAPER,
            "bordercolor": _INK,
            "font": {"family": _FONT, "color": _INK},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": _INK,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
            "ticks": "outside",
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": _INK,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
        },
        "legend": {"bgcolor": _PAPER, "bordercolor": _INK, "borderwidth": 1},
    },
    data={
        # Halftone-printed bars: dotted pattern over the fill, hard ink outline.
        "bar": [
            go.Bar(
                marker={
                    "line": {"color": _INK, "width": 1.5},
                    "pattern": {"shape": ".", "fgcolor": _INK, "solidity": 0.35, "size": 6},
                }
            )
        ],
        # Spare editorial line work.
        "scatter": [
            go.Scatter(mode="lines+markers", line={"width": 2}, marker={"size": 5, "symbol": "circle"})
        ],
    },
)
