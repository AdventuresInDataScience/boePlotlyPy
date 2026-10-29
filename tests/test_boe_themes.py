"""Tests for the Bank of England themes and the template builder in themes/_boe.py."""

import plotly.graph_objects as go
import plotly.io as pio
import pytest

import boeplotlypy as boe
from boeplotlypy.fonts import FONT_FILES
from boeplotlypy.themes._boe import (
    CALIBRI,
    LEGEND_POSITIONS,
    META_KEY,
    axis_layout,
    boe_template,
    ggplot_size,
    grid_layout,
    legend_layout,
    pt,
)

BOE_THEMES = ["boe_fsr", "boe_identity", "boe_mcg", "boe_mpr", "boe_overground"]


def layout_of(name):
    return pio.templates[name].layout


def style_of(name):
    return layout_of(name).meta[META_KEY]


def test_boe_themes_are_the_listed_themes():
    assert boe.registered_themes() == BOE_THEMES


# --- Every BoE theme --------------------------------------------------------

@pytest.mark.parametrize("name", BOE_THEMES)
def test_template_matches_its_style(name):
    s, lay = style_of(name), layout_of(name)
    assert s["name"] == name
    assert tuple(lay.colorway) == boe.PALETTES[s["palette"]]
    assert lay.font.family == s["font"]
    assert lay.font.size == pt(s["base_size"])
    assert lay.font.color == s["text_colour"]
    assert lay.title.font.size == pt(s["title_size"])
    assert lay.title.font.color == s["title_colour"]
    assert lay.title.subtitle.font.size == pt(s["subtitle_size"])
    assert lay.title.xanchor == "left" and lay.title.x == 0
    assert lay.paper_bgcolor == lay.plot_bgcolor == s["background"]
    assert lay.colorscale.sequential and lay.colorscale.diverging


@pytest.mark.parametrize("name", BOE_THEMES)
def test_unset_colours_fall_back_to_text_colour(name):
    s = style_of(name)
    for key in ("subtitle_colour", "legend_text_colour", "caption_colour"):
        assert s[key]


@pytest.mark.parametrize("name", BOE_THEMES)
def test_other_subplot_types_match(name):
    # 3D, polar and ternary subplots get the theme's background on import.
    lay = layout_of(name)
    assert lay.polar.bgcolor == lay.scene.xaxis.backgroundcolor == lay.plot_bgcolor


@pytest.mark.parametrize("name", BOE_THEMES)
def test_lines_are_at_least_one_pixel(name):
    lay = layout_of(name)
    for axis in (lay.xaxis, lay.yaxis):
        assert axis.gridwidth >= 1 and axis.linewidth >= 1


# --- Per-theme looks, matching the boeCharts theme functions ---------------

@pytest.mark.parametrize(
    "name, horizontal_grid, x_line, y_line, title_xref, bold_title, legend",
    [
        ("boe_mpr", False, True, True, "paper", False, "top-left"),
        ("boe_fsr", False, True, True, "paper", False, "top-left"),
        ("boe_overground", True, True, False, "container", True, "top-left"),
        ("boe_identity", True, True, False, "container", True, "top-left"),
        ("boe_mcg", False, True, True, "container", True, "bottom"),
    ],
)
def test_theme_looks(name, horizontal_grid, x_line, y_line, title_xref, bold_title, legend):
    lay = layout_of(name)
    assert lay.yaxis.showgrid is horizontal_grid
    assert lay.xaxis.showgrid is False
    assert lay.xaxis.showline is x_line and lay.yaxis.showline is y_line
    assert (lay.xaxis.ticks != "") is x_line and (lay.yaxis.ticks != "") is y_line
    # "paper": aligned with the plot area; "container": with the figure edge.
    assert lay.title.xref == title_xref
    assert lay.title.font.weight == ("bold" if bold_title else "normal")
    for key, value in legend_layout(legend).items():
        assert lay.legend[key] == value, key


@pytest.mark.parametrize("name", ["boe_mpr", "boe_fsr"])
def test_mpr_boxed_plot_area_with_inward_ticks(name):
    lay = layout_of(name)
    for axis in (lay.xaxis, lay.yaxis):
        assert axis.mirror is True
        assert axis.ticks == "inside"
        assert axis.linecolor == "#333333"


def test_fsr_is_mpr_with_the_fsr_palette():
    mpr, fsr = style_of("boe_mpr"), style_of("boe_fsr")
    assert {**mpr, "name": "boe_fsr", "palette": "fsr"} == fsr


def test_identity_is_dark_with_white_bold_legend():
    lay = layout_of("boe_identity")
    assert lay.paper_bgcolor == "#12273F"
    assert lay.legend.font.weight == "bold"
    assert lay.legend.font.color == "#FFFFFF"
    assert "Arial" in lay.font.family


@pytest.mark.parametrize("name", ["boe_mpr", "boe_fsr", "boe_overground"])
def test_calibri_themes_fall_back_to_bundled_carlito(name):
    family = layout_of(name).font.family
    assert family == CALIBRI
    assert family.index("Calibri") < family.index("Carlito")
    assert "Carlito" in FONT_FILES


# --- Unit conversion --------------------------------------------------------

def test_pt_to_px():
    assert pt(18) == 24
    assert pt(11.5) == pytest.approx(15.33, abs=0.01)


def test_ggplot_size_to_px():
    assert ggplot_size(1) == pytest.approx(2.85, abs=0.01)
    assert ggplot_size(0.5) == pytest.approx(1.42, abs=0.01)


# --- grid / axis / legend translation --------------------------------------

@pytest.mark.parametrize(
    "grid, x_major, y_major, x_minor, y_minor",
    [
        ("X", False, True, False, False),
        ("Y", True, False, False, False),
        ("XY", True, True, False, False),
        ("Xx", False, True, False, True),
        ("Yy", True, False, True, False),
        (True, True, True, True, True),
        (False, False, False, False, False),
    ],
)
def test_grid_layout_follows_boecharts(grid, x_major, y_major, x_minor, y_minor):
    xaxis, yaxis = grid_layout(grid, "#000000", 1)
    assert xaxis["showgrid"] is x_major          # vertical lines
    assert yaxis["showgrid"] is y_major          # horizontal lines
    assert xaxis["minor"]["showgrid"] is x_minor
    assert yaxis["minor"]["showgrid"] is y_minor


@pytest.mark.parametrize("bad", ["Z", "horizontal", 3])
def test_grid_layout_rejects_unknown_values(bad):
    with pytest.raises(ValueError):
        grid_layout(bad, "#000000", 1)


@pytest.mark.parametrize(
    "axis, x_on, y_on",
    [("X", True, False), ("x", True, False), ("Y", False, True), ("XY", True, True),
     (True, True, True), (False, False, False)],
)
def test_axis_layout_follows_boecharts(axis, x_on, y_on):
    xaxis, yaxis = axis_layout(axis, "#000000", 1)
    assert xaxis["showline"] is x_on and (xaxis["ticks"] == "outside") is x_on
    assert yaxis["showline"] is y_on and (yaxis["ticks"] == "outside") is y_on


def test_axis_layout_box_overrides_axis():
    for axis in axis_layout(False, "#000000", 1, ticks="inside", box=True):
        assert axis["showline"] and axis["mirror"] and axis["ticks"] == "inside"


def test_hairlines_are_widened_to_one_pixel():
    xaxis, _ = grid_layout("X", "#000000", 0.4)
    line, _ = axis_layout("X", "#000000", 0.4)
    assert xaxis["gridwidth"] == line["linewidth"] == 1


@pytest.mark.parametrize("position", LEGEND_POSITIONS)
def test_legend_layout_is_valid_plotly(position):
    go.layout.Legend(legend_layout(position))  # raises if Plotly rejects it


@pytest.mark.parametrize(
    "position, x, xanchor",
    [("top-left", 0, "left"), ("top-right", 1, "right"), ("top", 0.5, "center"),
     ("bottom-left", 0, "left"), ("bottom-right", 1, "right"), ("bottom", 0.5, "center")],
)
def test_legend_layout_alignment(position, x, xanchor):
    legend = legend_layout(position)
    assert (legend["x"], legend["xanchor"]) == (x, xanchor)
    expected_y = (1.0, "paper") if position.startswith("top") else (0.0, "container")
    assert (legend["y"], legend["yref"]) == expected_y


def test_legend_layout_none_hides_legend():
    assert legend_layout("none") == {"visible": False}


def test_legend_layout_rejects_unknown_position():
    with pytest.raises(ValueError, match="top-left"):
        legend_layout("middle")


# --- Adding a theme: one dict of differences --------------------------------

def test_custom_theme_builds_a_valid_template():
    template = boe_template("custom", {"palette": "vibrant_a", "grid": "XY", "axis": True})
    assert list(template.layout.colorway) == list(boe.PALETTES["vibrant_a"])
    assert template.layout.xaxis.showgrid and template.layout.yaxis.showgrid
    go.Figure(layout={"template": template}).to_plotly_json()


def test_unknown_palette_in_theme_fails_loudly():
    with pytest.raises(KeyError, match="Unknown palette"):
        boe_template("custom", {"palette": "nope"})
