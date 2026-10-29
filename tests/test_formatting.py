"""Tests for apply_formatting."""

import warnings

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytest

import boeplotlypy as boe
from boeplotlypy.themes._boe import ggplot_size

BOE_THEMES = boe.registered_themes()


@pytest.fixture
def df():
    return pd.DataFrame({
        "x": [1, 2, 3] * 3,
        "y": [1, -2, 3, 2, 1, 0, 3, 2, 1],
        "series": list("aaabbbccc"),
        "panel": list("pqpqpqpqp"),
    })


def line_colours(fig):
    return [t.line.color for t in fig.data]


def test_returns_the_same_figure(df):
    fig = px.line(df, x="x", y="y", color="series")
    assert boe.apply_formatting(fig) is fig


def test_no_arguments_changes_nothing(df):
    fig = px.line(df, x="x", y="y", color="series", template="boe_mpr")
    before = fig.to_plotly_json()
    boe.apply_formatting(fig)
    assert fig.to_plotly_json() == before


# --- theme ------------------------------------------------------------------

def test_explicit_palette_wins_over_theme_palette(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", color="series"),
                               theme="boe_fsr", palette="vibrant_a")
    assert line_colours(fig) == list(boe.PALETTES["vibrant_a"])


def test_unknown_theme_lists_boe_themes(df):
    with pytest.raises(ValueError, match="boe_mpr"):
        boe.apply_formatting(px.line(df, x="x", y="y"), theme="boe_nope")


def test_hidden_themes_work_too(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y"), theme="matrix")
    assert fig.layout.template.layout.paper_bgcolor is not None


# --- title / subtitle / source ---------------------------------------------

def test_title_and_subtitle(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", template="boe_mpr"),
                               title="Chart 1", subtitle="Per cent")
    assert fig.layout.title.text == "Chart 1"
    assert fig.layout.title.subtitle.text == "Per cent"


@pytest.mark.parametrize("theme, align", [("boe_mpr", "left"), ("boe_mcg", "right")])
def test_source_is_a_caption_under_the_chart(df, theme, align):
    fig = boe.apply_formatting(px.line(df, x="x", y="y"), theme=theme, source="Sources: ONS.")
    (note,) = fig.layout.annotations
    assert note.text == "Sources: ONS."
    assert note.xanchor == align
    assert note.y == 0 and note.yanchor == "top" and note.yshift < 0
    assert fig.layout.margin.b > -note.yshift  # room reserved below the labels


def test_source_is_replaced_not_duplicated(df):
    fig = px.line(df, x="x", y="y", template="boe_mpr")
    boe.apply_formatting(fig, source="First")
    boe.apply_formatting(fig, source="Second")
    assert [a.text for a in fig.layout.annotations] == ["Second"]


def test_source_keeps_user_annotations(df):
    fig = px.line(df, x="x", y="y", template="boe_mpr")
    fig.add_annotation(text="Peak", x=3, y=3)
    boe.apply_formatting(fig, source="Sources: ONS.")
    assert sorted(a.text for a in fig.layout.annotations) == ["Peak", "Sources: ONS."]


def test_source_lifts_a_bottom_legend(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", color="series"),
                               theme="boe_mcg", source="Sources: ONS.")
    assert fig.layout.legend.yref == "container" and fig.layout.legend.y > 0


@pytest.mark.parametrize("theme", BOE_THEMES)
def test_source_refits_when_called_again(df, theme):
    # Removing axis titles then re-applying must not leave the source floating
    # up into a bottom legend: it sits at the bottom edge of the figure.
    fig = boe.apply_formatting(px.line(df, x="x", y="y", color="series"), theme=theme,
                               legend="bottom", source="Sources: ONS.")
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    boe.apply_formatting(fig, source="Sources: ONS.")
    note = fig.layout.annotations[0]
    style = fig.layout.template.layout.meta["boeplotlypy"]
    line = round(style["base_size"] * 96 / 72, 2) * 1.3
    bottom_pad = round(style["margin"][2] * 96 / 72, 2)
    assert -note.yshift + line + bottom_pad == pytest.approx(fig.layout.margin.b)


def test_source_colour_follows_theme(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y"), theme="boe_identity", source="S")
    assert fig.layout.annotations[0].font.color == "#C4C9CE"


# --- palette ----------------------------------------------------------------

def test_palette_by_name(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", color="series"), palette="vibrant_b")
    assert line_colours(fig) == list(boe.PALETTES["vibrant_b"])
    assert list(fig.layout.colorway) == list(boe.PALETTES["vibrant_b"])


def test_palette_as_list(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", color="series"),
                               palette=["#111111", "#222222", "#333333"])
    assert line_colours(fig) == ["#111111", "#222222", "#333333"]


def test_palette_keeps_series_colour_across_facets(df):
    fig = px.line(df, x="x", y="y", color="series", facet_col="panel")
    boe.apply_formatting(fig, palette="boe")
    colour_of = {}
    for trace in fig.data:
        assert colour_of.setdefault(trace.name, trace.line.color) == trace.line.color
    assert list(colour_of.values()) == list(boe.PALETTES["boe"][:3])


def test_palette_recolours_pie_slices():
    fig = boe.apply_formatting(px.pie(values=[1, 2, 3, 4], names=list("abcd")), palette="boe")
    assert list(fig.data[0].marker.colors) == list(boe.PALETTES["boe"][:4])


def test_palette_recolours_sunburst():
    fig = px.sunburst(names=["root", "a", "b"], parents=["", "root", "root"], values=[0, 1, 2])
    boe.apply_formatting(fig, palette="vibrant_a")
    assert list(fig.data[0].marker.colors) == list(boe.PALETTES["vibrant_a"])


def test_palette_sets_continuous_colour_axis():
    fig = boe.apply_formatting(px.imshow([[1, 2], [3, 4]]), palette="red_blue")
    assert fig.layout.coloraxis.colorscale[0][1] == boe.PALETTES["red_blue"][0]


def test_palette_sets_trace_colourscale():
    fig = boe.apply_formatting(go.Figure(go.Heatmap(z=[[1, 2], [3, 4]])), palette="red_blue")
    assert fig.data[0].colorscale[-1][1] == boe.PALETTES["red_blue"][-1]


def test_palette_warns_when_too_short(df):
    with pytest.warns(UserWarning, match="2 colours but the chart has 3 series"):
        boe.apply_formatting(px.line(df, x="x", y="y", color="series"), palette="mpr_main")


def test_palette_does_not_warn_when_long_enough(df):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        boe.apply_formatting(px.line(df, x="x", y="y", color="series"), palette="boe")


def test_unknown_palette_suggests_names(df):
    with pytest.raises(KeyError, match="Did you mean"):
        boe.apply_formatting(px.line(df, x="x", y="y"), palette="vibrant_z")


# --- legend / grid / axis ---------------------------------------------------

def test_legend_none_hides_it(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", color="series"), legend="none")
    assert fig.layout.legend.visible is False


def test_legend_rejects_unknown(df):
    with pytest.raises(ValueError, match="top-left"):
        boe.apply_formatting(px.line(df, x="x", y="y"), legend="middle")


def test_grid_applies_to_every_facet(df):
    fig = px.line(df, x="x", y="y", color="series", facet_col="panel", template="boe_mpr")
    boe.apply_formatting(fig, grid="X")
    for axis in (fig.layout.yaxis, fig.layout.yaxis2):
        assert axis.showgrid is True
    for axis in (fig.layout.xaxis, fig.layout.xaxis2):
        assert axis.showgrid is False


def test_axis_lines(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", template="boe_overground"), axis="XY")
    assert fig.layout.xaxis.showline and fig.layout.yaxis.showline


def test_axis_false_removes_mpr_box(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", template="boe_mpr"), axis=False)
    assert fig.layout.xaxis.showline is False and fig.layout.xaxis.mirror is False


# --- hline0 -----------------------------------------------------------------

def test_hline0_defaults_match_boecharts(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y", template="boe_mpr"), hline0=True)
    y = fig.layout.yaxis
    assert y.zeroline is True
    assert y.zerolinecolor == "#C4C9CE"
    assert y.zerolinewidth == ggplot_size(1.5)
    assert y.rangemode == "tozero"


def test_hline0_custom(df):
    fig = boe.apply_formatting(px.line(df, x="x", y="y"), hline0={"colour": "#000000", "width": 2})
    assert (fig.layout.yaxis.zerolinecolor, fig.layout.yaxis.zerolinewidth) == ("#000000", 2)


def test_hline0_false_removes_it(df):
    fig = px.line(df, x="x", y="y", template="boe_mpr")
    boe.apply_formatting(fig, hline0=True)
    boe.apply_formatting(fig, hline0=False)
    assert fig.layout.yaxis.zeroline is False


def test_hline0_rejects_unknown_options(df):
    with pytest.raises(ValueError, match="colour"):
        boe.apply_formatting(px.line(df, x="x", y="y"), hline0={"size": 2})
