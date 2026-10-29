"""Financial Stability Report: boeCharts' ``theme_fsr()``.

boeCharts gives this the same look as ``theme_mpr()``; here it differs only in
using the FSR colour palette.
"""

from . import boe_mpr
from ._boe import boe_template

NAME = "boe_fsr"

TEMPLATE = boe_template(NAME, {**boe_mpr.STYLE, "palette": "fsr"})
