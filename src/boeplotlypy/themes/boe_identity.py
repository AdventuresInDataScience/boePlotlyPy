"""Bank of England visual identity: boeCharts' ``theme_boe_identity()``.

The dark navy brand background with white bold titles and legend text, light
grey axes and horizontal gridlines, set in Arial.
"""

from ._boe import ARIAL, boe_template

NAME = "boe_identity"

_GREY = "#C4C9CE"

TEMPLATE = boe_template(NAME, {
    "palette": "boe_identity",
    "sequential": ["#34BCC1", "#3CD7D9", "#77E3E4", "#A7EDEE", "#CEF5F5"],  # boe_shades_aqua: high values glow
    "font": ARIAL,
    "base_size": 16,
    "text_colour": _GREY,
    "background": "#12273F",
    "title_colour": "#FFFFFF",
    "title_bold": True,
    "title_position": "plot",
    "subtitle_size": 18,
    "subtitle_colour": "#FFFFFF",
    "grid": "X",
    "grid_colour": _GREY,
    "grid_width": 0.5,
    "axis": "X",
    "axis_colour": _GREY,
    "axis_width": 0.5,
    "tick_length": 8,
    # boeCharts defaults to a vertical legend, which leaves little room for the
    # plot at typical screen sizes.
    "legend_orientation": "h",
    "legend_bold": True,
    "legend_text_colour": "#FFFFFF",
    "margin": [20, 20, 20, 20],
})
