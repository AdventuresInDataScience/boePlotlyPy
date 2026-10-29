"""Monetary and Financial Conditions publications: boeCharts' ``theme_mcg_pub()``.

Built on ggplot's ``theme_classic()``: solid x and y axis lines with short
outward ticks, no gridlines, a bold title and the legend centred below.
"""

from ._boe import ARIAL, boe_template, ggplot_size

NAME = "boe_mcg"

_TEXT = "#2B2B2B"

TEMPLATE = boe_template(NAME, {
    "palette": "mcg",
    "font": ARIAL,  # boeCharts uses the device's default sans-serif
    "text_colour": _TEXT,
    "title_colour": _TEXT,
    "title_bold": True,
    "title_position": "plot",
    "axis": True,
    "axis_colour": _TEXT,
    "axis_width": ggplot_size(0.5),
    "tick_length": 4,
    "legend": "bottom",
    "caption_align": "right",
})
