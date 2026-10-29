"""Builds the Bank of England Plotly templates.

Each BoE theme module (boe_mpr.py and so on) lists the settings where it differs
from ``DEFAULTS`` below, mirroring the arguments of the matching ``theme_*()``
function in the R package boeCharts, and passes them to :func:`boe_template`.
The leading underscore stops the theme loader registering this module as a theme.

Units: boeCharts sizes text in points and lines in ggplot size units, while
Plotly uses pixels. :func:`pt` and :func:`ggplot_size` convert at 96 dpi. Lines
are drawn at least 1px wide: boeCharts' hairlines (0.4-0.6px) suit R's 300 dpi
exports but nearly vanish on screen.

:func:`grid_layout`, :func:`axis_layout` and :func:`legend_layout` translate
boeCharts' option values into Plotly settings, for both the templates and
``apply_formatting``.
"""

from __future__ import annotations

import plotly.graph_objects as go

from ..palettes import palette_colours, colorscale

#: Key under ``layout.meta`` where a BoE template stores its full style, so
#: ``apply_formatting`` can read it back from a figure.
META_KEY = "boeplotlypy"

CALIBRI = "Calibri, Carlito, 'Segoe UI', Arial, sans-serif"
ARIAL = "Arial, 'Liberation Sans', Helvetica, sans-serif"

LEGEND_POSITIONS = (
    "top-left", "top-right", "bottom-left", "bottom-right",
    "top", "bottom", "left", "right", "none",
)


def pt(points: float) -> float:
    """Convert a font size or length in points to pixels."""
    return round(points * 96 / 72, 2)


def ggplot_size(size: float) -> float:
    """Convert a ggplot line ``size`` to a Plotly line width in pixels."""
    return round(size * 72.27 / 25.4, 2)


# Every setting a BoE theme can change. Values follow boeCharts' theme_mpr().
# Colours set to None fall back to text_colour.
DEFAULTS = {
    "palette": "boe",
    "sequential": ["#EBEBEB", "#1488CA", "#00294E"],  # continuous scale: light grey to rich blue
    "font": CALIBRI,
    "base_size": 11.5,                   # pt
    "text_colour": "#1E1E1E",
    "background": "#FFFFFF",
    "title_size": 18,                    # pt
    "title_colour": "#005E6E",
    "title_bold": False,
    "title_position": "panel",           # "panel": aligned with the plot area; "plot": with the figure edge
    "subtitle_size": 14,                 # pt
    "subtitle_colour": None,
    "subtitle_bold": False,
    "grid": False,                       # boeCharts grid value, see grid_layout()
    "grid_colour": "#C8CCCF",
    "grid_width": ggplot_size(0.2),
    "axis": False,                       # boeCharts axis value, see axis_layout()
    "axis_colour": "#C8CCCF",
    "axis_width": ggplot_size(0.15),
    "ticks": "outside",                  # or "inside"
    "tick_length": 10,                   # pt
    "box": False,                        # border round the plot area, as ggplot's theme_bw()
    "legend": "top-left",                # see legend_layout()
    "legend_orientation": "h",
    "legend_bold": False,
    "legend_text_colour": None,
    "caption_colour": None,              # the source line added by apply_formatting
    "caption_align": "left",
    "hline0_colour": "#C4C9CE",          # boeCharts' add_hline0() default
    "margin": [5.75, 5.75, 5.75, 23],    # pt: top, right, bottom, left, as boeCharts' plot.margin
}


def _letters(spec: str | bool) -> str:
    """Normalise a boeCharts grid/axis value to the letters it switches on."""
    if spec is True:
        return "XYxy"
    if spec is False:
        return ""
    if not isinstance(spec, str) or set(spec) - set("XYxy"):
        raise ValueError(f"Expected True, False or a string of the letters X, Y, x, y; got {spec!r}.")
    return spec


def grid_layout(grid: str | bool, colour: str, width: float) -> tuple[dict, dict]:
    """Return ``(xaxis, yaxis)`` settings for a boeCharts ``grid`` value.

    As in boeCharts, ``"X"`` shows horizontal gridlines (they run along the x
    direction), ``"Y"`` vertical ones, and lowercase ``"x"``/``"y"`` the matching
    minor gridlines. ``True`` shows all of them and ``False`` none.
    """
    g = _letters(grid)
    line = {"gridcolor": colour, "gridwidth": max(width, 1)}
    xaxis = {**line, "showgrid": "Y" in g, "minor": {**line, "showgrid": "y" in g}}
    yaxis = {**line, "showgrid": "X" in g, "minor": {**line, "showgrid": "x" in g}}
    return xaxis, yaxis


def axis_layout(axis: str | bool, colour: str, width: float, ticks: str = "outside",
                tick_length: float = 10, box: bool = False) -> tuple[dict, dict]:
    """Return ``(xaxis, yaxis)`` settings for a boeCharts ``axis`` value.

    ``"X"`` draws the x-axis line and its ticks, ``"Y"`` the y-axis line and
    ticks, ``True`` both and ``False`` neither (case doesn't matter).
    ``box=True`` instead draws a border round the whole plot area with ticks on
    both axes, as the MPR and FSR themes do.
    """
    on = "xy" if box else _letters(axis).lower()
    width = max(width, 1)
    return tuple(
        {
            "showline": letter in on,
            "mirror": box,
            "linecolor": colour,
            "linewidth": width,
            "ticks": ticks if letter in on else "",
            "ticklen": pt(tick_length),
            "tickwidth": width,
            "tickcolor": colour,
        }
        for letter in "xy"
    )


def legend_layout(position: str, orientation: str = "h") -> dict:
    """Return ``layout.legend`` settings for a legend position.

    One of ``LEGEND_POSITIONS``. Top legends sit just above the plot area and
    bottom legends at the bottom of the figure, aligned with the plot area's
    left edge, centre or right edge; Plotly widens the margins to fit them.
    """
    if position not in LEGEND_POSITIONS:
        raise ValueError(f"Unknown legend position {position!r}. Choose from: {', '.join(LEGEND_POSITIONS)}.")
    if position == "none":
        return {"visible": False}
    if position in ("left", "right"):
        right = position == "right"
        return {"visible": True, "orientation": "v",
                "x": 1.02 if right else -0.02, "xanchor": "left" if right else "right", "xref": "paper",
                "y": 0.5, "yanchor": "middle", "yref": "paper"}
    vertical, _, horizontal = position.partition("-")
    x, xanchor = {"left": (0, "left"), "right": (1, "right"), "": (0.5, "center")}[horizontal]
    return {"visible": True, "orientation": orientation,
            "x": x, "xanchor": xanchor, "xref": "paper",
            "y": 1.0 if vertical == "top" else 0.0, "yanchor": "bottom",
            "yref": "paper" if vertical == "top" else "container"}


def boe_template(name: str, overrides: dict) -> go.layout.Template:
    """Build the Plotly template for a BoE theme from its differences to ``DEFAULTS``."""
    s = {**DEFAULTS, **overrides, "name": name}
    for key in ("subtitle_colour", "legend_text_colour", "caption_colour"):
        s[key] = s[key] or s["text_colour"]

    top, right, bottom, left = (pt(m) for m in s["margin"])
    grid_x, grid_y = grid_layout(s["grid"], s["grid_colour"], s["grid_width"])
    line_x, line_y = axis_layout(s["axis"], s["axis_colour"], s["axis_width"],
                                 s["ticks"], s["tick_length"], s["box"])
    axis_common = {"zeroline": False, "automargin": True, "tickfont": {"color": s["text_colour"]},
                   "title": {"standoff": pt(s["base_size"] / 2)}}

    if s["title_position"] == "plot":
        # The figure's left edge, inset by the top margin so the title lines up
        # with the axis labels (Plotly puts those close to the edge).
        title_x = {"xref": "container", "pad": {"l": top, "t": top}}
    else:
        title_x = {"xref": "paper", "pad": {"t": top}}

    legend_font = {"color": s["legend_text_colour"], "weight": "bold" if s["legend_bold"] else "normal"}

    return go.layout.Template(layout={
        "font": {"family": s["font"], "size": pt(s["base_size"]), "color": s["text_colour"]},
        "paper_bgcolor": s["background"],
        "plot_bgcolor": s["background"],
        "colorway": palette_colours(s["palette"]),
        "colorscale": {"sequential": colorscale(s["sequential"]), "diverging": colorscale("red_blue")},
        "title": {
            **title_x, "x": 0, "xanchor": "left",
            "y": 1, "yref": "container", "yanchor": "top", "automargin": True,
            "font": {"size": pt(s["title_size"]), "color": s["title_colour"],
                     "weight": "bold" if s["title_bold"] else "normal"},
            "subtitle": {"font": {"size": pt(s["subtitle_size"]), "color": s["subtitle_colour"],
                                  "weight": "bold" if s["subtitle_bold"] else "normal"}},
        },
        "legend": {**legend_layout(s["legend"], s["legend_orientation"]),
                   "bgcolor": "rgba(0,0,0,0)", "font": legend_font, "title": {"font": legend_font}},
        "margin": {"t": top, "r": right, "b": bottom, "l": left},
        "xaxis": {**axis_common, **grid_x, **line_x},
        "yaxis": {**axis_common, **grid_y, **line_y},
        "hoverlabel": {"font": {"family": s["font"]}},
        "bargap": 0.1,  # ggplot's geom_col fills 90% of each slot
        "meta": {META_KEY: s},
    })
