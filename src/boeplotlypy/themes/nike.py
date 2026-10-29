"""Nike-inspired theme: bold condensed type, orange/grey colourway, athletic
value labels on bars and confident heavy lines."""

import plotly.graph_objects as go

NAME = "nike"
HIDDEN = True  # easter egg: registered, but not listed or documented

_ORANGE = "#ec7424"
_INK = "#333333"
_TITLE_FONT = "HelveticaNeue-CondensedBold, Helvetica, Sans-serif"
_BODY_FONT = "Helvetica Neue, Helvetica, Sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        # Note - 'family' must be a single string, NOT a list or dict!
        "title": {"font": {"family": _TITLE_FONT, "size": 30, "color": _INK}},
        "font": {"family": _BODY_FONT, "size": 16, "color": _INK},
        "colorway": ["#ec7424", "#a4abab", "#111111", "#f5a623", "#6d6e71",
                     "#d65a00", "#c8cccc", "#3a3a3a", "#ff9a4d", "#8a8f8f"],
        "hovermode": "x unified",
        "hoverlabel": {"bgcolor": _INK, "bordercolor": _ORANGE, "font": {"color": "#FFFFFF"}},
        "xaxis": {"linecolor": _INK, "tickcolor": _INK, "tickfont": {"color": _INK}, "showgrid": False},
        "yaxis": {"gridcolor": "#E6E6E6", "linecolor": _INK, "tickcolor": _INK, "tickfont": {"color": _INK}},
    },
    data={
        "bar": [
            go.Bar(
                texttemplate="%{value:$.2s}",
                textposition="outside",
                textfont={"family": _BODY_FONT, "size": 20, "color": _INK},
                marker={"line": {"width": 0}},
            )
        ],
        # Bold, fast, athletic lines with large dots.
        "scatter": [
            go.Scatter(mode="lines+markers", line={"width": 4}, marker={"size": 9})
        ],
    },
)
