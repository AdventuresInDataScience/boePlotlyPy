"""Tests that every bundled theme (hidden ones included) registers and produces a valid Plotly template."""

import plotly.graph_objects as go
import plotly.io as pio
import pytest

import boeplotlypy

REGISTERED = boeplotlypy.registered_themes(include_hidden=True)


def test_import_registers_themes():
    assert len(REGISTERED) >= 1
    # A few we expect to always be present.
    for expected in ("matrix", "cyberpunk", "financial_times", "lego"):
        assert expected in REGISTERED


def test_hidden_themes_are_usable_but_not_listed():
    listed = boeplotlypy.registered_themes()
    hidden = set(REGISTERED) - set(listed)
    assert "matrix" in hidden
    for name in hidden:
        assert name in pio.templates
    assert set(listed) <= set(REGISTERED)


@pytest.mark.parametrize("name", REGISTERED)
def test_theme_is_registered_in_plotly(name):
    assert name in pio.templates


@pytest.mark.parametrize("name", REGISTERED)
def test_theme_template_is_valid(name):
    template = pio.templates[name]
    assert isinstance(template, go.layout.Template)
    # Every theme should at least define a colourway.
    assert template.layout.colorway, f"{name} has no colorway"


HIDDEN = sorted(set(REGISTERED) - set(boeplotlypy.registered_themes()))


@pytest.mark.parametrize("name", HIDDEN)
def test_theme_palette_has_depth(name):
    # The legacy themes should support medium-cardinality charts without the
    # colourway repeating too soon. (BoE themes use boeCharts' palettes as-is.)
    colorway = pio.templates[name].layout.colorway
    assert len(colorway) >= 10, f"{name} colourway only has {len(colorway)} colours"


@pytest.mark.parametrize("name", REGISTERED)
def test_theme_applies_to_a_figure(name):
    fig = go.Figure()
    fig.add_bar(x=[1, 2, 3], y=[3, 1, 2])
    fig.update_layout(template=name)
    # Validate by serialising — raises if the template is malformed.
    assert fig.to_plotly_json()["layout"]["template"] is not None


@pytest.mark.parametrize("name", REGISTERED)
def test_themes_style_noncartesian_subplots(name):
    # Themes that set a plot background should propagate it to 3D/polar/geo/
    # ternary subplots so those chart types match the theme too.
    lay = pio.templates[name].layout
    if lay.plot_bgcolor is None and lay.paper_bgcolor is None:
        pytest.skip(f"{name} sets no background")
    expected = lay.plot_bgcolor or lay.paper_bgcolor
    assert lay.polar.bgcolor == expected
    assert lay.scene.xaxis.backgroundcolor == expected
    assert lay.ternary.bgcolor == expected
