"""Matrix theme: phosphor green on black, monospace, digital-rain palette.

Lines render as digital step functions with square "pixel" markers and a faint
green wash, over a dotted terminal grid.
"""

import plotly.graph_objects as go

NAME = "matrix"
HIDDEN = True  # easter egg: registered, but not listed or documented

_GREEN = "#00FF41"
_DIM = "#008F11"
_BG = "#000000"
_GRID = "#003B00"
_FONT = "Share Tech Mono, 'Courier New', Consolas, monospace"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 14, "color": _GREEN},
        "title": {"font": {"family": _FONT, "size": 26, "color": _GREEN}},
        "colorway": ["#00FF41", "#008F11", "#39FF14", "#7CFC00", "#00B140", "#9EF01A",
                     "#00FF9C", "#5DBB63", "#B6FF00", "#2EE6A8"],
        "colorscale": {
            "sequential": [[0, "#001a00"], [0.5, "#008F11"], [1, "#00FF41"]],
            "diverging": [[0, "#000000"], [0.5, "#008F11"], [1, "#00FF41"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": _GREEN,
            "font": {"family": _FONT, "color": _GREEN},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _DIM,
            "zerolinecolor": _DIM,
            "tickcolor": _DIM,
            "tickfont": {"color": _GREEN},
            "title": {"font": {"color": _GREEN}},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": _DIM,
            "zerolinecolor": _DIM,
            "tickcolor": _DIM,
            "tickfont": {"color": _GREEN},
            "title": {"font": {"color": _GREEN}},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _DIM, "borderwidth": 1},
    },
    data={
        # Digital "stream": stepped lines, square pixel markers, faint phosphor wash.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 2, "shape": "hv"},
                marker={"symbol": "square", "size": 6},
                fill="tozeroy",
                fillcolor="rgba(0, 255, 65, 0.06)",
            )
        ],
        # Sharp, glowing-edged bars (no rounding — it's a terminal).
        "bar": [go.Bar(marker={"opacity": 0.85, "line": {"color": _GREEN, "width": 1}})],
    },
)
