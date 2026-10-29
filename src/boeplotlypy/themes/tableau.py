"""Classic Tableau theme: the familiar Tableau 10 palette on a clean light canvas,
with the restrained, dashboard-friendly styling Tableau is known for."""

import plotly.graph_objects as go

NAME = "tableau"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#FFFFFF"
_TEXT = "#3A3A3A"
_GRID = "#E6E6E6"
_FONT = "Tableau, 'Benton Sans', Arial, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 24, "color": "#2C2C2C"}},
        # Tableau 10.
        "colorway": [
            "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
            "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC",
        ],
        "colorscale": {
            "sequential": [[0, "#D8E3EF"], [0.5, "#4E79A7"], [1, "#2C4A6E"]],
            "diverging": [[0, "#E15759"], [0.5, "#F5F5F5"], [1, "#4E79A7"]],
        },
        "hovermode": "closest",
        "hoverlabel": {"font": {"family": _FONT}},
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": "#BFBFBF",
            "zerolinecolor": _GRID,
            "tickcolor": "#BFBFBF",
            "tickfont": {"color": _TEXT},
            "showgrid": False,
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": "#BFBFBF",
            "zerolinecolor": _GRID,
            "tickcolor": "#BFBFBF",
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _GRID, "borderwidth": 0},
    },
    data={
        # Clean, professional defaults: medium lines, tidy dots, gently rounded bars.
        "scatter": [
            go.Scatter(mode="lines+markers", line={"width": 2}, marker={"size": 7})
        ],
        "bar": [go.Bar(marker={"cornerradius": 2, "line": {"width": 0}})],
    },
)
