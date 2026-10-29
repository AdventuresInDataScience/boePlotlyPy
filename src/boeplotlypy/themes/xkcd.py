"""xkcd theme: hand-drawn comic look using a sketchy font and chunky black axes.

Plotly can't render genuinely wobbly "sketch" lines the way matplotlib's
``plt.xkcd()`` does, but the look is mostly carried by the font and the bold,
playful styling: fat rounded spline lines, big circle markers and thick black
bar outlines. This theme prefers the "xkcd Script" / "Humor Sans" fonts if the
viewer has them installed, and falls back to Comic Sans.
"""

import plotly.graph_objects as go

NAME = "xkcd"
HIDDEN = True  # easter egg: registered, but not listed or documented

_INK = "#000000"
_BG = "#FFFFFF"
_FONT = "Comic Neue, xkcd Script, Humor Sans, Comic Sans MS, Comic Sans, cursive"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 16, "color": _INK},
        "title": {"font": {"family": _FONT, "size": 28, "color": _INK}},
        "colorway": ["#1F77B4", "#E41A1C", "#4DAF4A", "#FF7F00", "#984EA3", "#000000",
                     "#A65628", "#F781BF", "#FFD92F", "#17BECF"],
        "hovermode": "closest",
        "hoverlabel": {"font": {"family": _FONT}},
        "xaxis": {
            "showgrid": False,
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "zerolinewidth": 2,
            "tickcolor": _INK,
            "ticks": "outside",
            "tickfont": {"family": _FONT, "color": _INK},
        },
        "yaxis": {
            "showgrid": False,
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "zerolinewidth": 2,
            "tickcolor": _INK,
            "ticks": "outside",
            "tickfont": {"family": _FONT, "color": _INK},
        },
        "legend": {"borderwidth": 2, "bordercolor": _INK},
    },
    data={
        # Fat, soft, hand-drawn-ish lines with chunky markers ringed in ink.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 4, "shape": "spline", "smoothing": 1.3},
                marker={"size": 10, "line": {"color": _INK, "width": 2}},
            )
        ],
        "bar": [go.Bar(marker={"line": {"color": _INK, "width": 2.5}})],
    },
)
