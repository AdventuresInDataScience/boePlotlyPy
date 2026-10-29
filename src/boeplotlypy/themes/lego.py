"""Lego theme: primary brick colours, bold black outlines, and chunky rounded
"brick" bars topped with big round "stud" markers."""

import plotly.graph_objects as go

NAME = "lego"
HIDDEN = True  # easter egg: registered, but not listed or documented

# The sky-blue background of printed LEGO building instructions.
_SKY = "#4FA6DD"
_SKY_LIGHT = "#6FB9E8"
_INK = "#1B1B1B"
# "LEGO" is the brand font (if the viewer has it); "Lilita One" is the bundled
# bold-rounded open-source lookalike that ships with the package.
_FONT = "LEGO, 'Lilita One', Helvetica Neue, Helvetica, Arial, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _SKY,
        "plot_bgcolor": _SKY_LIGHT,
        "font": {"family": _FONT, "size": 15, "color": _INK},
        "title": {"font": {"family": _FONT, "size": 28, "color": _INK}},
        # Classic LEGO brick colours: red, yellow, blue, green, orange, black.
        "colorway": ["#D01012", "#F6D316", "#0057A6", "#00852B", "#FF6F00", "#1B1B1B",
                     "#9C27B0", "#00A1C9", "#A5CA18", "#8B5A2B"],
        "colorscale": {
            "sequential": [[0, "#F6D316"], [0.5, "#FF6F00"], [1, "#D01012"]],
        },
        "hovermode": "closest",
        "hoverlabel": {
            "bgcolor": "#FFFFFF",
            "bordercolor": _INK,
            "font": {"family": _FONT, "color": _INK},
        },
        "xaxis": {
            "gridcolor": "#FFFFFF",
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
        },
        "yaxis": {
            "gridcolor": "#FFFFFF",
            "linecolor": _INK,
            "linewidth": 2,
            "zerolinecolor": _INK,
            "tickcolor": _INK,
            "tickfont": {"color": _INK},
        },
        "legend": {"bgcolor": "#FFFFFF", "bordercolor": _INK, "borderwidth": 2},
    },
    data={
        # Moulded-plastic bricks: rounded corners, heavy black outline, and a dot
        # pattern that reads as the rows of studs on top of a LEGO brick.
        "bar": [
            go.Bar(
                marker={
                    "cornerradius": 6,
                    "line": {"color": _INK, "width": 3},
                    "pattern": {
                        "shape": ".",
                        "fillmode": "overlay",
                        "fgcolor": "#1B1B1B",
                        "fgopacity": 0.22,
                        "size": 11,
                        "solidity": 0.5,
                    },
                }
            )
        ],
        # Blocky square markers (LEGO is all right angles) on thick lines.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 4},
                marker={"symbol": "square", "size": 13, "line": {"color": _INK, "width": 2}},
            )
        ],
    },
)
