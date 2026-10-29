"""Dracula theme: the well-loved dark palette — deep slate with vivid pastels,
styled like a modern code editor with rounded bars and crisp markers."""

import plotly.graph_objects as go

NAME = "dracula"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#282A36"
_PANEL = "#21222C"
_TEXT = "#F8F8F2"
_GRID = "#44475A"
_PURPLE = "#BD93F9"
_FONT = "'Fira Code', Consolas, monospace"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 24, "color": _PURPLE}},
        "colorway": [
            "#FF79C6", "#BD93F9", "#8BE9FD", "#50FA7B", "#FFB86C",
            "#FF5555", "#F1FA8C", "#6272A4", "#FF92E0", "#69FF94",
        ],
        "colorscale": {
            "sequential": [[0, "#282A36"], [0.5, "#BD93F9"], [1, "#FF79C6"]],
            "diverging": [[0, "#8BE9FD"], [0.5, "#282A36"], [1, "#FF79C6"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _PANEL,
            "bordercolor": _PURPLE,
            "font": {"family": _FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": "#6272A4",
            "zerolinecolor": _GRID,
            "tickcolor": "#6272A4",
            "tickfont": {"color": _TEXT},
            "showgrid": False,
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": "#6272A4",
            "zerolinecolor": _GRID,
            "tickcolor": "#6272A4",
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _PANEL, "bordercolor": _GRID, "borderwidth": 0},
    },
    data={
        "scatter": [
            go.Scatter(mode="lines+markers", line={"width": 3}, marker={"size": 7})
        ],
        "bar": [go.Bar(marker={"cornerradius": 5, "line": {"width": 0}})],
    },
)
