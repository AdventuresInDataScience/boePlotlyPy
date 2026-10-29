"""Star Wars theme: the opening-crawl look — black space, that famous crawl
yellow, and a lightsaber colourway. Lines glow with translucent fills and
bright marker haloes."""

import plotly.graph_objects as go

NAME = "star_wars"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#000000"
_PANEL = "#050608"
_CRAWL = "#FFE81F"  # the Star Wars logo yellow
_TEXT = "#E8E8E8"
_GRID = "#16181C"
_FONT = "'Pathway Gothic One', 'Franklin Gothic Medium', 'Trebuchet MS', sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _FONT, "size": 15, "color": _TEXT},
        "title": {"font": {"family": _FONT, "size": 30, "color": _CRAWL}},
        # Lightsaber colours: electric blue, red, vivid green, purple, crawl-yellow, white.
        "colorway": ["#1FA2FF", "#FF2B2B", "#4DFF5A", "#B05CFF", "#FFE81F", "#F4F4F4",
                     "#FF8C1A", "#00E5D0", "#FF4FA3", "#8AB4FF"],
        "colorscale": {
            "sequential": [[0, "#050608"], [0.5, "#B05CFF"], [1, "#FFE81F"]],
            "diverging": [[0, "#1FA2FF"], [0.5, "#050608"], [1, "#FF2B2B"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": _CRAWL,
            "font": {"family": _FONT, "color": _CRAWL},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": "#3A3D44",
            "zerolinecolor": "#3A3D44",
            "tickcolor": "#3A3D44",
            "tickfont": {"color": _TEXT},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "griddash": "dot",
            "linecolor": "#3A3D44",
            "zerolinecolor": "#3A3D44",
            "tickcolor": "#3A3D44",
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _BG, "bordercolor": _CRAWL, "borderwidth": 1},
    },
    data={
        # Sabers: bright spline beams with a soft glow underneath and a halo
        # around each marker (a light outer ring over a solid core).
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 3.5, "shape": "spline", "smoothing": 0.6},
                marker={"size": 9, "line": {"color": "rgba(255,255,255,0.85)", "width": 2}},
                fill="tozeroy",
                fillcolor="rgba(31, 162, 255, 0.10)",
            )
        ],
        "bar": [
            go.Bar(
                marker={
                    "cornerradius": 2,
                    "opacity": 0.9,
                    "line": {"color": _CRAWL, "width": 1},
                }
            )
        ],
    },
)
