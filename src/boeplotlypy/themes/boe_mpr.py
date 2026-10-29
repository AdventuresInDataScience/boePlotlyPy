"""Monetary Policy Report: boeCharts' ``theme_mpr()``.

Built on ggplot's ``theme_bw()``: a thin border round the plot area, ticks that
point inwards, no gridlines, and a plain teal title aligned with the plot area.
"""

from ._boe import boe_template, ggplot_size

NAME = "boe_mpr"

STYLE = {
    "palette": "boe",
    # theme_bw's panel border and ticks: grey20, ggplot size 0.5.
    "box": True,
    "axis_colour": "#333333",
    "axis_width": ggplot_size(0.5),
    "ticks": "inside",
    "tick_length": 0.35 * 72 / 2.54,  # 0.35 cm
}

TEMPLATE = boe_template(NAME, STYLE)
