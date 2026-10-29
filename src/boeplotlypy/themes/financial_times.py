"""Financial Times theme: the signature FT salmon paper, serif type, brand palette.

Deliberately restrained and editorial — crisp solid markers, thin lines, a single
horizontal grid and a discreet hatched fill under area traces, the way FT charts
shade a series.
"""

import plotly.graph_objects as go

NAME = "financial_times"
HIDDEN = True  # easter egg: registered, but not listed or documented

_PAPER = "#FFF1E5"  # FT "pink"
_TEXT = "#33302E"
_GRID = "#E8DDD0"
_FONT = "Georgia, 'Times New Roman', serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _PAPER,
        "plot_bgcolor": _PAPER,
        "font": {"family": _FONT, "size": 15, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 26, "color": "#000000"}},
        # FT brand colours: blue, claret, teal, slate, purple, oxford.
        "colorway": ["#0F5499", "#990F3D", "#0D7680", "#FF8833", "#593380", "#262A33",
                     "#1E88C7", "#C0392B", "#4DA17F", "#A6761D"],
        "colorscale": {
            "sequential": [[0, "#FFF1E5"], [0.5, "#FF8833"], [1, "#990F3D"]],
            "diverging": [[0, "#0F5499"], [0.5, "#FFF1E5"], [1, "#990F3D"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": "#FFFFFF",
            "bordercolor": "#33302E",
            "font": {"family": _FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": "#66605C",
            "zerolinecolor": "#66605C",
            "tickcolor": "#66605C",
            "tickfont": {"color": _TEXT},
            "showgrid": False,
            "ticks": "outside",
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": _GRID,
            "zerolinecolor": "#66605C",
            "tickcolor": "#66605C",
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _PAPER, "bordercolor": _GRID, "borderwidth": 0},
    },
    data={
        # Editorial line chart: thin confident lines, small solid dots, no rounding.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 2.5},
                marker={"size": 5},
            )
        ],
        # Solid, flat bars with a thin paper-coloured separator between segments.
        "bar": [go.Bar(marker={"line": {"color": _PAPER, "width": 1}})],
    },
)
