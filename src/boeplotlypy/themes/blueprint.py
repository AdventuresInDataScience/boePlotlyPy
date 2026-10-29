"""Blueprint theme: a white technical drawing on engineering blueprint blue.

Leans hard into the draughtsman look — dashed grid lines, cross-hatched bar
fills, dashed plot lines and hollow ("circle-open") markers, all in monospace.
"""

import plotly.graph_objects as go

NAME = "blueprint"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#0A3D62"
_TEXT = "#EAF2FB"
_GRID = "#1B5A86"
_LINE = "#BBD7EE"
_FONT = "Share Tech Mono, Consolas, 'Courier New', monospace"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _BG,
        "font": {"family": _FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 24, "color": "#FFFFFF"}},
        "colorway": ["#FFFFFF", "#BBD7EE", "#7FB2DD", "#FFD166", "#A8E6CF", "#FF8B94",
                     "#5FA8E0", "#FFE39E", "#9FD8CB", "#E0E7EF"],
        "colorscale": {
            "sequential": [[0, "#0A3D62"], [0.5, "#7FB2DD"], [1, "#FFFFFF"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": "#FFFFFF",
            "font": {"family": _FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "griddash": "dash",
            "gridwidth": 1,
            "linecolor": _LINE,
            "zerolinecolor": _LINE,
            "tickcolor": _LINE,
            "tickfont": {"color": _TEXT},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "griddash": "dash",
            "gridwidth": 1,
            "linecolor": _LINE,
            "zerolinecolor": _LINE,
            "tickcolor": _LINE,
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _LINE, "borderwidth": 1},
    },
    data={
        # Draughtsman's plot: dashed construction lines with hollow markers.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 2, "dash": "dash"},
                marker={"symbol": "circle-open", "size": 9, "line": {"width": 1.5}},
            )
        ],
        # Cross-hatched bars, as if shaded by hand on drafting paper.
        "bar": [
            go.Bar(
                marker={
                    "line": {"color": "#FFFFFF", "width": 1.5},
                    "pattern": {"shape": "/", "fgcolor": "#FFFFFF", "bgcolor": _BG, "solidity": 0.2, "size": 8},
                }
            )
        ],
    },
)
