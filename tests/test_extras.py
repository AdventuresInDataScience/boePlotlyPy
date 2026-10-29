"""Tests for the add_glow effect and the bundled-font helpers."""

import plotly.graph_objects as go

import boeplotlypy
from boeplotlypy.fonts import FONT_FILES, FONTS_DIR, font_face_css


def _fig_with_lines(n_lines=2, n_bars=1):
    fig = go.Figure()
    for _ in range(n_bars):
        fig.add_bar(x=[1, 2, 3], y=[3, 1, 2])
    for _ in range(n_lines):
        fig.add_scatter(x=[1, 2, 3], y=[1, 2, 3], mode="lines+markers")
    fig.update_layout(template="star_wars")
    return fig


def test_add_glow_adds_layers_per_line():
    fig = _fig_with_lines(n_lines=2, n_bars=1)
    boeplotlypy.add_glow(fig, layers=4)
    # 4 glow traces per line, originals preserved (2 lines + 1 bar).
    assert len(fig.data) == 3 + 2 * 4


def test_add_glow_does_not_glow_bars():
    fig = _fig_with_lines(n_lines=0, n_bars=2)
    before = len(fig.data)
    boeplotlypy.add_glow(fig)
    assert len(fig.data) == before


def test_add_glow_glow_traces_are_hidden_and_serialise():
    fig = _fig_with_lines(n_lines=1, n_bars=0)
    boeplotlypy.add_glow(fig, layers=3)
    glow = [t for t in fig.data if t.showlegend is False]
    assert len(glow) == 3
    assert all(t.hoverinfo == "skip" for t in glow)
    # Glow colours should be translucent rgba derived from the line colour.
    assert any("rgba(" in (t.line.color or "") for t in glow)
    fig.to_plotly_json()  # raises if malformed


def test_font_face_css_embeds_every_family():
    css = font_face_css()
    for family in FONT_FILES:
        assert f"'{family}'" in css
    assert css.count("@font-face") == sum(len(v) for v in FONT_FILES.values())
    assert "base64," in css


def test_bundled_font_files_exist():
    for faces in FONT_FILES.values():
        for filename, _weight, _style in faces:
            assert (FONTS_DIR / filename).exists(), filename
