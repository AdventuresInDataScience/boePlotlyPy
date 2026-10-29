"""NASA theme: deep-space dark with the agency's blue/red, clean technical type
and a mission-readout feel."""

import plotly.graph_objects as go

NAME = "nasa"
HIDDEN = True  # easter egg: registered, but not listed or documented

_BG = "#0B1021"  # deep space navy
_PANEL = "#0E1530"
_TEXT = "#E6ECFF"
_NASA_BLUE = "#2E6FE8"
_NASA_RED = "#FC3D21"
_GRID = "#1C274D"
_TITLE_FONT = "Orbitron, 'Helvetica Neue', Arial, sans-serif"
_BODY_FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif"

TEMPLATE = go.layout.Template(
    layout={
        "paper_bgcolor": _BG,
        "plot_bgcolor": _PANEL,
        "font": {"family": _BODY_FONT, "size": 14, "color": _TEXT},
        "title": {"font": {"family": _TITLE_FONT, "size": 26, "color": "#FFFFFF"}},
        # NASA blue & red, plus instrument blues/greys for extra series.
        "colorway": ["#2E6FE8", "#FC3D21", "#58A6FF", "#FFFFFF", "#9AA7C7", "#FFB000",
                     "#1FC3F3", "#FF6F4D", "#7FA8FF", "#C0CCE6"],
        "colorscale": {
            "sequential": [[0, "#0B1021"], [0.5, "#2E6FE8"], [1, "#58A6FF"]],
            "diverging": [[0, "#FC3D21"], [0.5, "#0E1530"], [1, "#2E6FE8"]],
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": _BG,
            "bordercolor": _NASA_BLUE,
            "font": {"family": _BODY_FONT, "color": _TEXT},
        },
        "xaxis": {
            "gridcolor": _GRID,
            "linecolor": "#3A4A7D",
            "zerolinecolor": "#3A4A7D",
            "tickcolor": "#3A4A7D",
            "tickfont": {"color": _TEXT},
        },
        "yaxis": {
            "gridcolor": _GRID,
            "linecolor": "#3A4A7D",
            "zerolinecolor": "#3A4A7D",
            "tickcolor": "#3A4A7D",
            "tickfont": {"color": _TEXT},
        },
        "legend": {"bgcolor": _PANEL, "bordercolor": _GRID, "borderwidth": 1},
    },
    data={
        # Telemetry traces: crisp lines, diamond instrument markers.
        "scatter": [
            go.Scatter(
                mode="lines+markers",
                line={"width": 2.5},
                marker={"symbol": "diamond", "size": 7, "line": {"color": _BG, "width": 1}},
            )
        ],
        "bar": [go.Bar(marker={"cornerradius": 2, "line": {"color": _NASA_BLUE, "width": 1}})],
    },
)
