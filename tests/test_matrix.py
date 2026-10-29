"""Matrix tests: every theme against every chart type, dataset and legend position.

The chart catalogue and datasets live in conftest.py. Fast tests check the
figure objects; tests marked ``render`` run plotly.js (via kaleido) and check
what it actually drew.
"""

import json
import warnings

import plotly.express as px
import pytest

import boeplotlypy as boe
from boeplotlypy.themes._boe import LEGEND_POSITIONS

from conftest import BOE_THEMES, CHARTS, DATASETS

CHART_NAMES = list(CHARTS)
CATEGORICAL = [name for name, (_, categorical) in CHARTS.items() if categorical]
ALL_ARGS = dict(
    title="Chart 1.1: A title", subtitle="Per cent", source="Sources: ONS and Bank calculations.",
    legend="bottom", grid="XY", axis=True, hline0=True,
)


def build(name):
    return CHARTS[name][0]()


def style(theme):
    return boe.apply_formatting(build("line"), theme=theme).layout.template.layout.meta["boeplotlypy"]


def series_colours(fig):
    """The single colour of each trace (line colour, else marker colour)."""
    out = []
    for t in fig.data:
        line = getattr(t, "line", None)
        colour = getattr(line, "color", None) if line is not None else None
        out.append(colour or t.marker.color)
    return out


def quiet(func, *args, **kwargs):
    """Call ignoring the 'more series than colours' warning (tested separately)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return func(*args, **kwargs)


# --- Every chart type x every theme ----------------------------------------

@pytest.mark.parametrize("theme", BOE_THEMES)
@pytest.mark.parametrize("chart", CHART_NAMES)
def test_theme_applies_to_chart(chart, theme):
    fig = quiet(boe.apply_formatting, build(chart), theme=theme)
    assert fig.layout.template.layout.meta["boeplotlypy"]["name"] == theme
    fig.to_plotly_json()


@pytest.mark.parametrize("theme", BOE_THEMES)
@pytest.mark.parametrize("chart", CATEGORICAL)
def test_series_take_theme_palette_in_order(chart, theme):
    fig = quiet(boe.apply_formatting, build(chart), theme=theme)
    palette = boe.PALETTES[style(theme)["palette"]]
    colours = series_colours(fig)
    assert all(c in palette for c in colours), colours
    # The first series always gets the palette's first colour.
    assert colours[0] == palette[0]


@pytest.mark.parametrize("theme", BOE_THEMES)
@pytest.mark.parametrize("chart", CHART_NAMES)
def test_all_arguments_on_every_chart(chart, theme):
    fig = quiet(boe.apply_formatting, build(chart), theme=theme, palette="vibrant_a", **ALL_ARGS)
    assert fig.layout.title.text == ALL_ARGS["title"]
    assert any(a.text == ALL_ARGS["source"] for a in fig.layout.annotations)
    fig.to_plotly_json()


@pytest.mark.parametrize("chart", CHART_NAMES)
def test_formatting_twice_is_stable(chart):
    fig = quiet(boe.apply_formatting, build(chart), theme="boe_mpr", **ALL_ARGS)
    once = json.loads(fig.to_json())
    quiet(boe.apply_formatting, fig, theme="boe_mpr", **ALL_ARGS)
    assert json.loads(fig.to_json()) == once


@pytest.mark.parametrize("chart", CATEGORICAL)
def test_switching_theme_recolours(chart):
    fig = quiet(boe.apply_formatting, build(chart), theme="boe_mpr")
    quiet(boe.apply_formatting, fig, theme="boe_identity")
    assert series_colours(fig)[0] == boe.PALETTES["boe_identity"][0]


# --- Awkward data x every theme ---------------------------------------------

@pytest.mark.parametrize("theme", BOE_THEMES)
@pytest.mark.parametrize("dataset", list(DATASETS))
def test_datasets(dataset, theme):
    fig = px.line(**DATASETS[dataset])
    quiet(boe.apply_formatting, fig, theme=theme, **ALL_ARGS)
    fig.to_plotly_json()


def test_many_series_warns_and_cycles():
    fig = px.line(**DATASETS["many_series"])
    with pytest.warns(UserWarning, match="20 series"):
        boe.apply_formatting(fig, theme="boe_mpr", palette="vibrant_a")
    colours = series_colours(fig)
    assert colours[:3] == colours[3:6] == list(boe.PALETTES["vibrant_a"])


# --- Legend positions x themes x charts with legends -------------------------

@pytest.mark.parametrize("theme", BOE_THEMES)
@pytest.mark.parametrize("position", LEGEND_POSITIONS)
@pytest.mark.parametrize("chart", ["line", "bar_stacked", "pie", "facet_col"])
def test_legend_positions(chart, position, theme):
    fig = quiet(boe.apply_formatting, build(chart), theme=theme, legend=position,
                source="Sources: ONS.")
    legend = fig.layout.legend
    assert legend.visible is (position != "none")
    if position.startswith("bottom"):
        # Lifted clear of the source line.
        assert legend.yref == "container" and legend.y > 0
    fig.to_plotly_json()


# --- What plotly.js actually draws -----------------------------------------

@pytest.mark.render
@pytest.mark.parametrize("theme", BOE_THEMES)
@pytest.mark.parametrize("chart", CHART_NAMES)
def test_rendered(chart, theme):
    fig = quiet(boe.apply_formatting, build(chart), theme=theme, **ALL_ARGS)
    s = style(theme)
    full = fig.full_figure_for_development(warn=False).layout
    assert full.font.family == s["font"]
    assert full.paper_bgcolor == s["background"]
    assert full.title.text == ALL_ARGS["title"]
    assert full.title.subtitle.text == ALL_ARGS["subtitle"]
    if full.showlegend:
        # Bottom legend, lifted clear of the source line.
        assert full.legend.yref == "container" and full.legend.y > 0
    if full.yaxis.range is not None and full.yaxis.type == "linear" and "yaxis" in fig.layout:
        # hline0 keeps zero in view on cartesian charts.
        lo, hi = sorted(full.yaxis.range)
        assert lo <= 0 <= hi or chart in ("heatmap", "bar_horizontal", "funnel")
