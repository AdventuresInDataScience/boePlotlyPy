"""Visual regression: render reference charts and compare them with saved PNGs.

Baselines live in tests/baseline/. After an intentional visual change, review
the new images and refresh the baselines with:

    uv run pytest -m visual --update-baselines

On a mismatch, the new render and a difference image are written to
tests/visual_output/ for review. Fonts differ between machines, so baselines
should be generated and checked on one platform (e.g. CI).
"""

from pathlib import Path

import pytest

import boeplotlypy as boe

from conftest import BOE_THEMES, CHARTS

PIL = pytest.importorskip("PIL")
from PIL import Image, ImageChops  # noqa: E402

BASELINE_DIR = Path(__file__).parent / "baseline"
OUTPUT_DIR = Path(__file__).parent / "visual_output"

# Share of pixels allowed to differ noticeably (anti-aliasing, minor engine changes).
TOLERANCE = 0.01
CHANNEL_THRESHOLD = 40

CASES = [(theme, chart) for theme in BOE_THEMES for chart in ("line", "bar_stacked")]


def render(theme, chart, path):
    fig = boe.apply_formatting(
        CHARTS[chart][0](), theme=theme,
        title="Chart 1.1: Reference chart", subtitle="Per cent",
        source="Sources: ONS and Bank calculations.", hline0=True,
    )
    fig.update_layout(width=700, height=450)
    fig.write_image(path)


def changed_fraction(a, b):
    if a.size != b.size:
        return 1.0
    diff = ImageChops.difference(a.convert("RGB"), b.convert("RGB")).convert("L")
    changed = sum(diff.histogram()[CHANNEL_THRESHOLD + 1:])
    return changed / (a.size[0] * a.size[1])


@pytest.mark.render
@pytest.mark.visual
@pytest.mark.parametrize("theme, chart", CASES)
def test_matches_baseline(theme, chart, request):
    name = f"{theme}_{chart}.png"
    baseline = BASELINE_DIR / name

    if request.config.getoption("--update-baselines"):
        BASELINE_DIR.mkdir(exist_ok=True)
        render(theme, chart, baseline)
        pytest.skip(f"baseline written: {baseline.name}")
    if not baseline.exists():
        pytest.skip(f"no baseline for {name}; run with --update-baselines")

    OUTPUT_DIR.mkdir(exist_ok=True)
    actual = OUTPUT_DIR / name
    render(theme, chart, actual)
    with Image.open(baseline) as expected, Image.open(actual) as got:
        fraction = changed_fraction(expected, got)
        if fraction > TOLERANCE:
            ImageChops.difference(expected.convert("RGB"), got.convert("RGB")).save(
                OUTPUT_DIR / f"diff_{name}"
            )
    assert fraction <= TOLERANCE, (
        f"{name}: {fraction:.1%} of pixels changed; see {OUTPUT_DIR}"
    )
    actual.unlink()
