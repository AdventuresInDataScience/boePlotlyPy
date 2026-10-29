"""boeplotlypy: Bank of England chart styles for Plotly.

A Python counterpart to the R package boeCharts
(https://github.com/bank-of-england/boeCharts). Importing this package registers
every theme in ``boeplotlypy/themes/`` with Plotly, so it can be used by name::

    import boeplotlypy as boe
    import plotly.express as px

    fig = px.line(df, x="date", y="value", template="boe_mpr")
    boe.apply_formatting(fig, title="Chart 1.1", source="Sources: ONS.")

A theme module defines ``NAME`` (the template's name) and ``TEMPLATE`` (a
``plotly.graph_objects.layout.Template``). Modules that also set
``HIDDEN = True`` are registered but left out of :func:`registered_themes`.
"""

from __future__ import annotations

import importlib
import pkgutil

import plotly.graph_objects as go
import plotly.io as pio

from . import palettes, themes
from .effects import add_glow
from .fonts import enable_fonts, font_face_css
from .formatting import apply_formatting
from .palettes import PALETTE_GROUPS, PALETTES

__all__ = [
    "apply_formatting",
    "PALETTES",
    "PALETTE_GROUPS",
    "palettes",
    "registered_themes",
    "add_glow",
    "enable_fonts",
    "font_face_css",
]

# Theme name -> whether it is hidden, in registration order.
_THEMES: dict[str, bool] = {}


def registered_themes(include_hidden: bool = False) -> list[str]:
    """Return the names of the themes this package registered with Plotly.

    Hidden themes work by name like any other, but are only listed when
    ``include_hidden=True``.
    """
    return [name for name, hidden in _THEMES.items() if include_hidden or not hidden]


def _match_other_subplots(template: go.layout.Template) -> None:
    """Give 3D, polar, map and ternary subplots the template's 2D colours.

    Those subplot types have their own background and axis colours, which
    don't follow ``plot_bgcolor`` or the 2D axes. Settings the template already
    makes are kept. Templates that don't set a background are left alone.
    """
    lay = template.layout
    plot = lay.plot_bgcolor or lay.paper_bgcolor
    if plot is None:
        return
    grid, line = lay.xaxis.gridcolor, lay.xaxis.linecolor
    text = lay.xaxis.tickfont.color or lay.font.color
    axis3d = {"backgroundcolor": plot, "showbackground": True, "gridcolor": grid,
              "zerolinecolor": grid, "color": text}
    axis2d = {"gridcolor": grid, "linecolor": line, "color": text}
    lay.scene.update(xaxis=axis3d, yaxis=axis3d, zaxis=axis3d)
    lay.polar.update(bgcolor=plot, angularaxis=axis2d, radialaxis=axis2d)
    lay.ternary.update(bgcolor=plot, aaxis=axis2d, baxis=axis2d, caxis=axis2d)
    lay.geo.update(bgcolor=lay.paper_bgcolor or plot, landcolor=plot, lakecolor=plot,
                   coastlinecolor=line, framecolor=line, countrycolor=grid)


for _module_info in pkgutil.iter_modules(themes.__path__):
    if _module_info.name.startswith("_"):
        continue
    _module = importlib.import_module(f"{themes.__name__}.{_module_info.name}")
    _match_other_subplots(_module.TEMPLATE)
    pio.templates[_module.NAME] = _module.TEMPLATE
    _THEMES[_module.NAME] = getattr(_module, "HIDDEN", False)
