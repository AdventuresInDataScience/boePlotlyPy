"""Nord theme: the popular cool, muted arctic palette (Polar Night + Aurora),
styled soft and modern — gently rounded bars and smooth, calm lines."""

import plotly.graph_objects as go

NAME = "nord"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#2E3440"
_PANEL = "#3B4252"
_TEXT = "#ECEFF4"
_GRID = "#434C5E"
_FROST = "#88C0D0"
_FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 24, "color": _TEXT}},
        # Aurora + Frost.
        "colorway": [
            "#88C0D0", "#BF616A", "#A3BE8C", "#EBCB8B", "#B48EAD",
            "#5E81AC", "#D08770", "#8FBCBB", "#81A1C1", "#D8DEE9",
        ],
        "colorscale": {
            "sequential": [[0, "#2E3440"], [0.5, "#5E81AC"], [1, "#88C0D0"]],
            "diverging": [[0, "#BF616A"], [0.5, "#ECEFF4"], [1, "#5E81AC"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _PANEL,
            "bordercolor": _FROST,
            "font": {"family": _FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": "#4C566A",
            "zerolinecolor": _GRID,
            "tickcolor": "#4C566A",
            "tickfont": {"color": _TEXT},
            "showgrid": False,
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": "#4C566A",
            "zerolinecolor": _GRID,
            "tickcolor": "#4C566A",
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _PANEL, "bordercolor": _GRID, "borderwidth": 0},
    },
    data={
        # Calm, smooth lines and softly rounded bars.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 2.5, "shape": "spline", "smoothing": 0.5},
                marker={"size": 7},
            )
        ],
        "bar": [go.Bar(marker={"cornerradius": 4, "line": {"width": 0}})],
    },
)
