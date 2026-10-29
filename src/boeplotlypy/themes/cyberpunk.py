"""Cyberpunk theme: neon colours on near-black, alpha fills for a glowing look."""

import plotly.graph_objects as go

NAME = "cyberpunk"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#0A0E14"
_PANEL = "#10151F"
_TEXT = "#E6F1FF"
_CYAN = "#00F0FF"
_MAGENTA = "#FF00A0"
_GRID = "#1F2A3A"
_FONT = "Trebuchet MS, Verdana, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": "Orbitron, " + _FONT, "size": 26, "color": _CYAN}},
        # Saturated neons; translucent versions are applied in the data traces.
        "colorway": [_CYAN, _MAGENTA, "#FCEE09", "#A6FF00", "#9D00FF", "#FF6C11",
                     "#00FF9F", "#FF3CAC", "#2D5BFF", "#FF1F4F"],
        "colorscale": {
            "sequential": [[0, "#10151F"], [0.5, _MAGENTA], [1, _CYAN]],
            "diverging": [[0, _MAGENTA], [0.5, "#10151F"], [1, _CYAN]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": _CYAN,
            "font": {"family": _FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _CYAN,
            "zerolinecolor": _GRID,
            "tickcolor": _CYAN,
            "tickfont": {"color": _TEXT},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _CYAN,
            "zerolinecolor": _GRID,
            "tickcolor": _CYAN,
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _PANEL, "bordercolor": _CYAN, "borderwidth": 1},
    },
    data={
        # Glow effect: thick bright lines over a translucent fill of the same hue,
        # with a soft halo around each marker.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 3},
                marker={"size": 8, "opacity": 0.95, "line": {"color": "rgba(0,240,255,0.5)", "width": 3}},
                fill="tozeroy",
                fillcolor="rgba(0, 240, 255, 0.12)",
            )
        ],
        "bar": [
            go.Bar(
                marker={
                    "cornerradius": 2,
                    "opacity": 0.85,
                    "line": {"color": _CYAN, "width": 1},
                }
            )
        ],
    },
)
