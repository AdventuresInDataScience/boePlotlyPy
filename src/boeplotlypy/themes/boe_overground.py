"""Bank Overground: boeCharts' ``theme_overground()``.

Minimal and airy: slate text, a bold teal title over a bold subtitle,
horizontal gridlines only and a thin x-axis line with long ticks.
"""

from ._boe import boe_template

NAME = "boe_overground"

TEMPLATE = boe_template(NAME, {
    # boeCharts' 3-colour boe_overground palette is a subset of boe_highlights.
    "palette": "boe_highlights",
    "text_colour": "#657581",
    "title_bold": True,
    "title_position": "plot",
    "subtitle_bold": True,
    "caption_colour": "#1E1E1E",
    "grid": "X",
    "axis": "X",
})
