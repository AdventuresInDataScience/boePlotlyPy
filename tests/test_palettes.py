"""Tests for the Bank of England palettes ported from boeCharts."""

import os
import re
import sys
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import pytest

import boeplotlypy as boe
from boeplotlypy.palettes import _hex_to_lab, _lab_to_hex, colorscale, palette_colours

ALL_PALETTES = list(boe.PALETTES)
HEX = re.compile(r"^#[0-9A-F]{6}$")


# --- Structure --------------------------------------------------------------

def test_palette_groups_match_boecharts():
    sizes = {group: len(names) for group, names in boe.PALETTE_GROUPS.items()}
    assert sizes == {
        "identity": 3,
        "shades": 1,
        "standard": 5,
        "harmonious": 8,
        "vibrant": 8,
        "diverging": 7,
        "publication": 10,
    }
    assert len(boe.PALETTES) == 42


def test_every_palette_is_in_exactly_one_group():
    grouped = [name for names in boe.PALETTE_GROUPS.values() for name in names]
    assert len(grouped) == len(set(grouped))
    assert sorted(grouped) == sorted(boe.PALETTES)


@pytest.mark.parametrize("name", ALL_PALETTES)
def test_palette_colours_are_uppercase_hex(name):
    colours = boe.PALETTES[name]
    assert isinstance(colours, tuple)
    assert len(colours) >= 2
    for colour in colours:
        assert HEX.match(colour), f"{name}: {colour!r} is not #RRGGBB"


@pytest.mark.parametrize("name", ALL_PALETTES)
def test_palette_has_no_repeated_colours(name):
    colours = boe.PALETTES[name]
    assert len(set(colours)) == len(colours)


@pytest.mark.parametrize(
    "name, length",
    [
        ("boe", 17), ("boe_rich", 7), ("boe_highlights", 7), ("boe_soft", 7),
        ("boe_neutral", 5), ("boe_identity", 10), ("boe_shades_aqua", 5),
        ("fsr", 17), ("pre_mpc", 7), ("mcg", 6), ("fsr_currency", 4),
        ("mpr_main", 2), ("fsr_main", 2), ("vibrant_a", 3), ("red_blue", 3),
    ],
)
def test_palette_lengths(name, length):
    assert len(boe.PALETTES[name]) == length


# --- Values (spot checks mirror boeCharts' own tests) -----------------------

def test_boe_palette_first_colour():
    assert boe.PALETTES["boe"][0] == "#A51140"


def test_boe_rich_fourth_colour():
    assert boe.PALETTES["boe_rich"][3] == "#C94D1B"


def test_boe_reversed_first_four():
    # boe_pal("boe", n = 4, reverse = TRUE)[1] == "#E05206" in boeCharts.
    assert boe.PALETTES["boe"][:4][::-1][0] == "#E05206"


def test_combination_palettes_reference_base_colours():
    rich, highlights, soft = (boe.PALETTES[n] for n in ("boe_rich", "boe_highlights", "boe_soft"))
    assert boe.PALETTES["vibrant_a"] == (rich[0], highlights[0], soft[0])
    assert boe.PALETTES["harmonious_blue"] == (rich[0], highlights[6], soft[6])


def test_diverging_palettes_have_neutral_or_light_midpoint():
    for name in boe.PALETTE_GROUPS["diverging"]:
        lightness = [_hex_to_lab(c)[0] for c in boe.PALETTES[name]]
        assert lightness[1] > max(lightness[0], lightness[2]), name


def test_vibrant_h_uses_rich_orange():
    # Deliberate fix of a boeCharts bug (it references a missing colour).
    assert boe.PALETTES["vibrant_h"] == ("#C94D1B", "#B0358B", "#FDC41F")


# --- Lookup -----------------------------------------------------------------

def test_palettes_are_read_only():
    with pytest.raises(TypeError):
        boe.PALETTES["boe"] = ("#000000",)  # type: ignore[index]


def test_palette_colours_by_name_or_list():
    assert palette_colours("vibrant_a") == list(boe.PALETTES["vibrant_a"])
    assert palette_colours(["#000000", "#FFFFFF"]) == ["#000000", "#FFFFFF"]


def test_unknown_palette_suggests_close_matches():
    with pytest.raises(KeyError, match="Did you mean: vibrant_"):
        palette_colours("vibrant_z")


def test_unknown_palette_lists_available():
    with pytest.raises(KeyError, match="Available palettes: boe_identity"):
        palette_colours("not_a_palette")


def test_palette_works_as_plotly_express_sequence():
    fig = px.bar(
        x=["a", "b", "c"], y=[1, 2, 3], color=["a", "b", "c"],
        color_discrete_sequence=boe.PALETTES["vibrant_a"],
    )
    assert [t.marker.color for t in fig.data] == list(boe.PALETTES["vibrant_a"])


# --- Colour-space conversion ------------------------------------------------

@pytest.mark.parametrize(
    "colour, lab",
    [
        ("#FFFFFF", (100.0, 0.0, 0.0)),
        ("#000000", (0.0, 0.0, 0.0)),
        ("#FF0000", (53.24, 80.09, 67.20)),
        ("#0000FF", (32.30, 79.19, -107.86)),
        ("#808080", (53.59, 0.0, 0.0)),
    ],
)
def test_hex_to_lab_reference_values(colour, lab):
    assert _hex_to_lab(colour) == pytest.approx(lab, abs=0.05)


@pytest.mark.parametrize("name", ALL_PALETTES)
def test_lab_round_trip_is_exact(name):
    for colour in boe.PALETTES[name]:
        assert _lab_to_hex(_hex_to_lab(colour)) == colour


# --- Continuous colourscales ------------------------------------------------

@pytest.mark.parametrize("name", ALL_PALETTES)
def test_colorscale_is_valid_for_plotly(name):
    scale = colorscale(name)
    positions = [stop[0] for stop in scale]
    assert positions[0] == 0 and positions[-1] == 1
    assert positions == sorted(positions)
    assert scale[0][1] == boe.PALETTES[name][0]
    assert scale[-1][1] == boe.PALETTES[name][-1]
    go.Heatmap(z=[[1, 2], [3, 4]], colorscale=scale)  # raises if Plotly rejects it


def test_colorscale_passes_through_middle_colour():
    # Three evenly spaced colours: the middle one sits at 0.5.
    scale = dict(colorscale("red_blue"))
    assert scale[0.5] == boe.PALETTES["red_blue"][1]


def test_colorscale_interpolates_in_lab_not_rgb():
    # Lab interpolation (as boeCharts does) keeps the midpoint brighter than a
    # naive RGB average of red and blue.
    mid = dict(colorscale(["#FF0000", "#0000FF"]))[0.5]
    assert _hex_to_lab(mid)[0] > _hex_to_lab("#800080")[0]


def test_colorscale_reverse():
    forward = colorscale("red_blue")
    backward = colorscale("red_blue", reverse=True)
    assert [c for _, c in backward] == [c for _, c in forward][::-1]


def test_colorscale_accepts_a_list_of_colours():
    scale = colorscale(["#ffffff", "#000000"])
    assert scale[0] == [0.0, "#FFFFFF"] and scale[-1] == [1.0, "#000000"]


def test_colorscale_single_colour():
    assert {colour for _, colour in colorscale(["#123456"])} == {"#123456"}


def test_colorscale_rejects_unknown_palette():
    with pytest.raises(KeyError):
        colorscale("not_a_palette")


def test_colorscale_works_with_plotly_express():
    fig = px.imshow([[1, 2], [3, 4]], color_continuous_scale=colorscale("red_blue"))
    assert fig.layout.coloraxis.colorscale[0][1] == "#AA0B3C"


# --- Sync with boeCharts (optional: needs a local checkout) ----------------

@pytest.mark.skipif(
    not os.environ.get("BOECHARTS_DIR"),
    reason="set BOECHARTS_DIR to a boeCharts checkout to compare against the R source",
)
def test_palettes_match_boecharts_source():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    from check_against_boecharts import compare

    assert compare(Path(os.environ["BOECHARTS_DIR"])) == 0
