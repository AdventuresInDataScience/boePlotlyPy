"""``apply_formatting``: per-chart choices on top of a Bank of England theme."""

from __future__ import annotations

import warnings

import plotly.graph_objects as go
import plotly.io as pio

from .palettes import colorscale, palette_colours
from .themes._boe import META_KEY, axis_layout, ggplot_size, grid_layout, legend_layout, pt


def apply_formatting(
    fig: go.Figure,
    *,
    theme: str | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    source: str | None = None,
    palette: str | list[str] | None = None,
    legend: str | None = None,
    grid: str | bool | None = None,
    axis: str | bool | None = None,
    hline0: bool | dict | None = None,
) -> go.Figure:
    """Apply per-chart Bank of England formatting to a figure.

    Every argument is optional. Leave it out (``None``) to keep what the theme
    set. The figure is changed in place and also returned, so calls can be
    chained.

    Args:
        fig: A Plotly figure.
        theme: The BoE theme to apply: ``"boe_mpr"``, ``"boe_fsr"``,
            ``"boe_overground"``, ``"boe_identity"`` or ``"boe_mcg"``. The
            series are recoloured with the theme's palette (unless ``palette``
            is also given). If left out, the figure keeps its current theme;
            for non-BoE themes, the MPR look is used for things like the
            source line's colour.
        title: The chart title, e.g. ``"Chart 2.1: CPI inflation"``. Shown
            top left in the theme's title style.
        subtitle: The line under the title, typically the units, e.g.
            ``"Percentage changes on a year earlier"``.
        source: The source note printed under the chart, e.g.
            ``"Sources: ONS and Bank calculations."``. This is text for the
            reader; it has nothing to do with where colours come from.
        palette: Recolour the chart's series with a BoE palette name from
            ``boe.PALETTES`` (e.g. ``"vibrant_a"``) or your own list of hex
            colours. Series keep their order, a series repeated across facets
            keeps one colour, and continuous colour scales (heatmaps and so on)
            are rebuilt from the same palette. Rising/falling colours on OHLC,
            candlestick and waterfall charts are left alone. Warns if there are
            more series than colours.
        legend: Where the legend goes: ``"top-left"``, ``"top-right"``,
            ``"top"``, ``"bottom-left"``, ``"bottom-right"``, ``"bottom"``,
            ``"left"``, ``"right"``, or ``"none"`` to hide it.
        grid: Which gridlines to show, using boeCharts' convention: ``"X"`` for
            horizontal lines, ``"Y"`` for vertical lines, ``"XY"`` for both,
            lowercase ``"x"``/``"y"`` to add minor lines, ``True`` for all and
            ``False`` for none.
        axis: Which axis lines (and their ticks) to draw: ``"X"``, ``"Y"``,
            ``"XY"``/``True`` for both, or ``False`` for neither.
        hline0: Draw a strong line at y = 0 and make sure 0 is in view, like
            boeCharts' ``add_hline0()``. ``True`` uses boeCharts' defaults; pass
            ``{"colour": "#1E1E1E", "width": 3}`` to change them, or ``False``
            to remove the line.

    Returns:
        The same figure.

    Anything not covered here is ordinary Plotly. Make further changes
    *afterwards*, and they take priority::

        boe.apply_formatting(fig, title="...", legend="bottom", hline0=True)
        fig.update_layout(yaxis_side="right", height=500)
    """
    if theme is not None:
        if theme not in pio.templates:
            boe_themes = ", ".join(n for n in pio.templates if n.startswith("boe_"))
            raise ValueError(f"Unknown theme {theme!r}. BoE themes: {boe_themes}.")
        fig.update_layout(template=theme)

    # The BoE style stored on the figure's template, or MPR's for other templates.
    meta = fig.layout.template.layout.meta if fig.layout.template else None
    is_boe = isinstance(meta, dict) and META_KEY in meta
    style = meta[META_KEY] if is_boe else pio.templates["boe_mpr"].layout.meta[META_KEY]

    if title is not None:
        fig.update_layout(title_text=title)
    if subtitle is not None:
        fig.update_layout(title_subtitle_text=subtitle)
    # Plotly Express fixes trace colours when it builds a figure, so a new
    # theme only shows its palette if the traces are recoloured.
    if palette is None and theme is not None and is_boe:
        palette = style["palette"]
    if palette is not None:
        _recolour(fig, palette_colours(palette))
    if legend is not None:
        fig.update_layout(legend=legend_layout(legend, style["legend_orientation"]))
    if grid is not None:
        xaxis, yaxis = grid_layout(grid, style["grid_colour"], style["grid_width"])
        fig.update_xaxes(**xaxis)
        fig.update_yaxes(**yaxis)
    if axis is not None:
        xaxis, yaxis = axis_layout(axis, style["axis_colour"], style["axis_width"],
                                   style["ticks"], style["tick_length"])
        fig.update_xaxes(**xaxis)
        fig.update_yaxes(**yaxis)
    if hline0 is False:
        fig.update_yaxes(zeroline=False)
    elif hline0 is not None:
        options = hline0 if isinstance(hline0, dict) else {}
        if set(options) - {"colour", "width"}:
            raise ValueError(f"hline0 accepts 'colour' and 'width'; got {sorted(options)}.")
        fig.update_yaxes(
            zeroline=True,
            zerolinecolor=options.get("colour", style["hline0_colour"]),
            zerolinewidth=options.get("width", ggplot_size(1.5)),  # boeCharts' add_hline0() size
            rangemode="tozero",  # like ggplot, extend the axis to include the line
        )
    if source is not None:
        _add_source(fig, source, style)
    return fig


def _recolour(fig: go.Figure, colours: list[str]) -> None:
    """Give each series the next palette colour, and continuous scales the palette's gradient."""
    scale = colorscale(colours)
    series: dict = {}  # series key -> colour, in order of first appearance
    for trace in fig.data:
        if trace.type in ("ohlc", "candlestick", "waterfall"):
            continue  # rising/falling colours carry meaning
        if trace.type in ("pie", "sunburst", "treemap", "icicle", "funnelarea"):
            n = len(trace.labels if trace.labels is not None else trace.ids or [])
            trace.marker.colors = [colours[i % len(colours)] for i in range(n)]
        elif "colorscale" in trace:  # heatmap, contour, choropleth, surface, ...
            trace.colorscale = scale
        elif "marker" in trace and trace.marker.color is not None and not isinstance(trace.marker.color, str):
            # Markers coloured by data values. Shared colour axes are set below.
            if not trace.marker.coloraxis:
                trace.marker.colorscale = scale
        else:
            # Plotly Express repeats a series across facets with the same legendgroup.
            key = trace.legendgroup or trace.name or id(trace)
            colour = series.setdefault(key, colours[len(series) % len(colours)])
            if "line" in trace and "color" in trace.line:
                trace.line.color = colour
            if "marker" in trace and "color" in trace.marker:
                trace.marker.color = colour
            if trace.type in ("box", "violin"):
                trace.fillcolor = None  # Plotly derives it from the line colour

    if len(series) > len(colours):
        warnings.warn(f"This palette has {len(colours)} colours but the chart has "
                      f"{len(series)} series, so colours will repeat.", stacklevel=3)
    for name in fig.layout:
        if name.startswith("coloraxis") and fig.layout[name] is not None:
            fig.layout[name].colorscale = scale
    fig.update_layout(colorway=colours)


def _add_source(fig: go.Figure, text: str, style: dict) -> None:
    """Add the source line under everything else, aligned left or right as the theme says.

    Plotly can only position annotations relative to the plot area, so the
    source hangs below it by the estimated height of the x tick labels, the
    x-axis title and any bottom legend, and the bottom margin is set to fit.
    """
    font = pt(style["base_size"])
    line = font * 1.3
    pad = pt(style["margin"][2])
    left = style["caption_align"] == "left"

    xaxis = fig.layout.xaxis
    below = line + 4  # tick labels
    if (xaxis.ticks if xaxis.ticks is not None else style["ticks"]) == "outside":
        below += pt(style["tick_length"])
    if xaxis.title.text:
        below += line + pt(style["base_size"] / 2)  # axis title and its standoff

    # The legend's position may be set on the figure or inherited from the theme.
    legend = fig.layout.legend
    themed = fig.layout.template.layout.legend if fig.layout.template else go.layout.Legend()
    visible, yref, y = (legend[k] if legend[k] is not None else themed[k] for k in ("visible", "yref", "y"))
    bottom_legend = visible is not False and yref == "container" and (y or 0) < 0.5
    legend_height = line + 10 if bottom_legend else 0

    fig.layout.annotations = [a for a in fig.layout.annotations if a.name != "boe_source"]
    fig.add_annotation(
        name="boe_source", text=text, showarrow=False,
        xref="paper", x=0 if left else 1, xanchor="left" if left else "right",
        align="left" if left else "right",
        yref="paper", y=0, yanchor="top", yshift=-(below + legend_height),
        font={"size": font, "color": style["caption_colour"]},
    )
    fig.update_layout(margin_b=below + legend_height + line + pad)
    if bottom_legend:
        # Lift the legend above the source line. Container positions are a
        # fraction of the figure height, so this assumes the current height
        # (Plotly's default of 450px if none is set).
        legend.update(yref="container", yanchor="bottom", y=(line + pad) / (fig.layout.height or 450))
