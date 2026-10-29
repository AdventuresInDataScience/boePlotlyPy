"""Star Trek LCARS theme: the 90s-era console look — black panels, amber and
mauve accents, condensed type, and the signature rounded "pill" blocks."""

import plotly.graph_objects as go

NAME = "star_trek"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#000000"
_ORANGE = "#FF9900"
_MAUVE = "#CC99CC"
_BLUE = "#9999FF"
_TEXT = "#FF9F66"
_GRID = "#332200"
_FONT = "Antonio, Arial Narrow, Helvetica, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 15, "color": _TEXT},
        "title": {"font": {"family": "Orbitron, " + _FONT, "size": 28, "color": _ORANGE}},
        # Canonical LCARS panel colours.
        "colorway": ["#FF9900", "#CC99CC", "#9999FF", "#FFCC66", "#CC6666", "#99CCFF",
                     "#FF9966", "#CC99FF", "#FFCC99", "#6699CC"],
        "colorscale": {
            "sequential": [[0, "#1a1000"], [0.5, "#CC6666"], [1, "#FF9900"]],
        },
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": _ORANGE,
            "font": {"family": _FONT, "color": _ORANGE},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _ORANGE,
            "zerolinecolor": _GRID,
            "tickcolor": _ORANGE,
            "tickfont": {"color": _MAUVE},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _ORANGE,
            "zerolinecolor": _GRID,
            "tickcolor": _ORANGE,
            "tickfont": {"color": _MAUVE},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _ORANGE, "borderwidth": 2},
    },
    data={
        # LCARS is all smooth rounded blocks: heavily rounded bars and fat,
        # marker-less rounded lines.
        "bar": [go.Bar(marker={"cornerradius": 14, "line": {"width": 0}})],
        "scatter": [
            go.Scatter(
                mode="lines",
                line={"width": 5, "shape": "spline", "smoothing": 0.8},
            )
        ],
    },
)
