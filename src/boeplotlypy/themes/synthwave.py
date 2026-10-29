"""Synthwave theme: 80s retro-future sunset — deep purple night, hot pink and
cyan neon, glowing area fills over a dotted retro grid."""

import plotly.graph_objects as go

NAME = "synthwave"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#241734"
_PANEL = "#2B213A"
_TEXT = "#F5E1FF"
_PINK = "#FF2A6D"
_CYAN = "#05D9E8"
_GRID = "#3D2B5A"
_FONT = "Verdana, 'Trebuchet MS', sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 26, "color": _PINK}},
        "colorway": [_PINK, _CYAN, "#D1F7FF", "#FF6C11", "#7700FF", "#F9C80E",
                     "#FE53BB", "#08F7FE", "#B967FF", "#FF8B00"],
        "colorscale": {
            "sequential": [[0, "#2B213A"], [0.5, "#7700FF"], [1, _PINK]],
            "diverging": [[0, _CYAN], [0.5, "#2B213A"], [1, _PINK]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": _PINK,
            "font": {"family": _FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _PINK,
            "zerolinecolor": _GRID,
            "tickcolor": _PINK,
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
        "legend": {"bgcolor": _PANEL, "bordercolor": _PINK, "borderwidth": 1},
    },
    data={
        # Glowing neon beams with haloed markers and a sunset-pink wash.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 3},
                marker={"size": 8, "line": {"color": "rgba(255,255,255,0.6)", "width": 2}},
                fill="tozeroy",
                fillcolor="rgba(255, 42, 109, 0.12)",
            )
        ],
        "bar": [
            go.Bar(marker={"cornerradius": 3, "opacity": 0.9, "line": {"color": _PINK, "width": 1}})
        ],
    },
)
