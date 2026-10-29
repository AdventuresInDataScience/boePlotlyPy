"""Barbie theme: unapologetically pink, glossy and fun — script title, rounded
candy bars and big white-ringed bubble markers."""

import plotly.graph_objects as go

NAME = "barbie"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BARBIE = "#E0218A"  # the trademark "Barbie pink"
_BG = "#FFE3F1"
_PANEL = "#FFFFFF"
_INK = "#7A0C49"
_TITLE_FONT = "Pacifico, 'Brush Script MT', cursive"
_BODY_FONT = "'Trebuchet MS', 'Century Gothic', Verdana, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _BODY_FONT, "size": 15, "color": _INK},
        "title": {"font": {"family": _TITLE_FONT, "size": 34, "color": _BARBIE}},
        "colorway": ["#E0218A", "#FF6FB5", "#FF1493", "#C71585", "#00A0DC", "#FFD200",
                     "#FF85C0", "#A8005C", "#6EC6FF", "#B0E057"],
        "colorscale": {
            "sequential": [[0, "#FFE3F1"], [0.5, "#FF6FB5"], [1, "#E0218A"]],
            "diverging": [[0, "#00A0DC"], [0.5, "#FFFFFF"], [1, "#E0218A"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BARBIE,
            "bordercolor": "#FFFFFF",
            "font": {"family": _BODY_FONT, "color": "#FFFFFF"},
        },
        "xaxis": {
            "gridcolor": "#FBD0E6",
            "linecolor": _BARBIE,
            "zerolinecolor": "#FBD0E6",
            "tickcolor": _BARBIE,
            "tickfont": {"color": _INK},
        },
        "yaxis": {
            "gridcolor": "#FBD0E6",
            "linecolor": _BARBIE,
            "zerolinecolor": "#FBD0E6",
            "tickcolor": _BARBIE,
            "tickfont": {"color": _INK},
        },
        "legend": {"bgcolor": _PANEL, "bordercolor": _BARBIE, "borderwidth": 1},
    },
    data={
        # Glossy candy: very rounded bars, bubbly white-ringed markers, soft splines.
        "bar": [
            go.Bar(marker={"cornerradius": 12, "line": {"color": "#FFFFFF", "width": 2}})
        ],
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 4, "shape": "spline", "smoothing": 0.8},
                marker={"size": 12, "line": {"color": "#FFFFFF", "width": 2.5}},
            )
        ],
    },
)
