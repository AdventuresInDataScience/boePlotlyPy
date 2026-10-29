"""Coke theme: Coca-Cola red and white, classic serif type, and the brand's
flowing "ribbon" curves — sweeping splines over a soft red wash."""

import plotly.graph_objects as go

NAME = "coke"
HIDDEN = True  # easter egg: registered, but not listed or documented

_RED = "#F40009"
_BG = "#FFFFFF"
_INK = "#1A1A1A"
# Title uses the flowing Coca-Cola script: the brand "Coca Cola ii" font if the
# viewer has it, otherwise the bundled open-source "Great Vibes" Spencerian
# script. Body stays a readable serif (a script is unreadable for axis labels).
_TITLE_FONT = "'Coca Cola ii', 'Great Vibes', cursive"
_FONT = "Georgia, 'Times New Roman', serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 15, "color": _INK},
        "title": {"font": {"family": _TITLE_FONT, "size": 34, "color": _RED}},
        # Coke red, charcoal, silver and a darker brand red.
        "colorway": ["#F40009", "#1A1A1A", "#B0B0B0", "#A60005", "#E6E6E6", "#7A0003",
                     "#D9534F", "#8C8C8C", "#3D0000", "#5A5A5A"],
        "colorscale": {
            "sequential": [[0, "#FFE5E6"], [0.5, "#F40009"], [1, "#7A0003"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _RED,
            "bordercolor": "#FFFFFF",
            "font": {"family": _FONT, "color": "#FFFFFF"},
        },
        "xaxis": {
            "gridcolor": "#F0F0F0",
            "linecolor": _RED,
            "zerolinecolor": "#E0E0E0",
            "tickcolor": _RED,
            "tickfont": {"color": _INK},
        },
        "yaxis": {
            "gridcolor": "#F0F0F0",
            "linecolor": _RED,
            "zerolinecolor": "#E0E0E0",
            "tickcolor": _RED,
            "tickfont": {"color": _INK},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _RED, "borderwidth": 1},
    },
    data={
        # Flowing "Coca-Cola ribbon" splines with a soft red wash and white-ringed dots.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 4, "shape": "spline", "smoothing": 1.0},
                marker={"size": 8, "line": {"color": "#FFFFFF", "width": 1.5}},
                fill="tozeroy",
                fillcolor="rgba(244, 0, 9, 0.10)",
            )
        ],
        "bar": [
            go.Bar(marker={"cornerradius": 3, "line": {"color": "#FFFFFF", "width": 1.5}})
        ],
    },
)
