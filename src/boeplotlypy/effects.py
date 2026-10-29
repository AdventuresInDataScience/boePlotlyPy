"""``add_glow``: a neon glow under line traces, used by some of the hidden themes.

A template can only set defaults for the traces a figure already has; it can't
add new ones. A glow needs wider, translucent copies of each line drawn
underneath it, so it is applied to a finished figure instead.
"""

from __future__ import annotations

import plotly.colors as pc
import plotly.graph_objects as go


def add_glow(fig: go.Figure, *, layers: int = 4, width_growth: float = 4.0,
             max_opacity: float = 0.18) -> go.Figure:
    """Add a soft glow beneath every line trace, in place.

    Args:
        fig: The figure to change (also returned, for chaining).
        layers: Number of glow copies per line; more gives a smoother falloff.
        width_growth: How much wider each successive copy is, in px.
        max_opacity: Opacity of the innermost copy; outer copies fade out.
    """
    template = fig.layout.template
    colorway = (template.layout.colorway if template else None) or pc.qualitative.Plotly

    glow = []
    # Plotly assigns colourway colours across all traces in order, bars included.
    for index, trace in enumerate(fig.data):
        if trace.type not in ("scatter", "scattergl") or "lines" not in (trace.mode or "lines"):
            continue
        # Pin the line's colour so the glow matches it after the traces are reordered.
        trace.line.color = trace.line.color or colorway[index % len(colorway)]
        try:
            r, g, b = pc.unlabel_rgb(pc.convert_colors_to_same_type(trace.line.color, "rgb")[0][0])
        except (IndexError, ValueError):  # named CSS colours: glow without transparency
            r = None
        base_width = trace.line.width if trace.line.width is not None else 2
        for layer in range(layers, 0, -1):  # widest and faintest first
            opacity = max_opacity * layer / layers
            glow.append(go.Scatter(
                x=trace.x, y=trace.y, mode="lines",
                line={"color": f"rgba({r:g}, {g:g}, {b:g}, {opacity})" if r is not None else trace.line.color,
                      "width": base_width + width_growth * layer,
                      "shape": trace.line.shape, "smoothing": trace.line.smoothing},
                hoverinfo="skip", showlegend=False, legendgroup=trace.legendgroup,
                xaxis=trace.xaxis, yaxis=trace.yaxis,
            ))

    if glow:
        # New traces can only be appended, so add them and then move them first
        # so they draw underneath the originals.
        n = len(fig.data)
        fig.add_traces(glow)
        fig.data = fig.data[n:] + fig.data[:n]
    return fig
