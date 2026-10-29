"""Amber terminal theme: vintage amber-phosphor CRT monitor, monospace, with
stepped readout lines, square markers and a faint amber scan wash."""

import plotly.graph_objects as go

NAME = "amber_terminal"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#1A0F00"
_AMBER = "#FFB000"
_DIM = "#AA7400"
_GRID = "#3D2A00"
_FONT = "VT323, 'Courier New', Consolas, monospace"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 14, "color": _AMBER},
        "title": {"font": {"family": _FONT, "size": 24, "color": _AMBER}},
        "colorway": ["#FFB000", "#FFCB47", "#CC8E00", "#FFD980", "#AA7400", "#7A5400",
                     "#FFA200", "#E69500", "#FFE0A3", "#B37400"],
        "colorscale": {
            "sequential": [[0, "#1A0F00"], [0.5, _DIM], [1, _AMBER]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": _AMBER,
            "font": {"family": _FONT, "color": _AMBER},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _DIM,
            "zerolinecolor": _DIM,
            "tickcolor": _DIM,
            "tickfont": {"color": _AMBER},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _DIM,
            "zerolinecolor": _DIM,
            "tickcolor": _DIM,
            "tickfont": {"color": _AMBER},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _DIM, "borderwidth": 1},
    },
    data={
        # CRT readout: stepped lines, square markers, faint amber wash.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 2, "shape": "hv"},
                marker={"symbol": "square", "size": 6},
                fill="tozeroy",
                fillcolor="rgba(255, 176, 0, 0.07)",
            )
        ],
        "bar": [go.Bar(marker={"opacity": 0.85, "line": {"color": _AMBER, "width": 1}})],
    },
)
