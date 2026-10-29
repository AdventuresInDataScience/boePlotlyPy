"""Power BI theme: the default Power BI palette and Segoe UI type on a light
canvas, with the softly rounded bars and clean lines of a Power BI report."""

import plotly.graph_objects as go

NAME = "powerbi"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#FFFFFF"
_TEXT = "#252423"
_GRID = "#E1DFDD"
_FONT = "Segoe UI, 'Segoe UI', Arial, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 24, "color": "#252423"}},
        # Power BI default theme palette.
        "colorway": [
            "#01B8AA", "#374649", "#FD625E", "#F2C80F", "#5F6B6D",
            "#8AD4EB", "#FE9666", "#A66999", "#3599B8", "#DFBFBF",
        ],
        "colorscale": {
            "sequential": [[0, "#E6F7F5"], [0.5, "#01B8AA"], [1, "#0A6B63"]],
            "diverging": [[0, "#FD625E"], [0.5, "#F5F5F5"], [1, "#01B8AA"]],
        },
        "hovermode": "closest",
        "hoverlabel": {"font": {"family": _FONT}},
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": "#C8C6C4",
            "zerolinecolor": _GRID,
            "tickcolor": "#C8C6C4",
            "tickfont": {"color": _TEXT},
            "showgrid": False,
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": "#C8C6C4",
            "zerolinecolor": _GRID,
            "tickcolor": "#C8C6C4",
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _GRID, "borderwidth": 0},
    },
    data={
        "scatter": [
            go.Scatter(mode="lines+markers", line={"width": 2.5}, marker={"size": 7})
        ],
        # Power BI's signature softly rounded column tops.
        "bar": [go.Bar(marker={"cornerradius": 4, "line": {"width": 0}})],
    },
)
