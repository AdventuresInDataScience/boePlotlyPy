"""Shared test data: a catalogue of chart types and a set of awkward datasets.

Tests are parametrised over these, so adding a chart type or dataset here
extends every matrix test automatically.
"""

import numpy as np
import pytest
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import boeplotlypy as boe

BOE_THEMES = boe.registered_themes()

_rng = np.random.default_rng(42)
_QUARTERS = pd.date_range("2019-01-01", periods=12, freq="QS")

LONG = pd.DataFrame({
    "date": list(_QUARTERS) * 3,
    "value": np.r_[np.linspace(-1, 3, 12), np.linspace(2, -2, 12), _rng.normal(0, 1, 12)],
    "series": ["Households"] * 12 + ["Corporates"] * 12 + ["Government"] * 12,
    "panel": (["UK"] * 6 + ["Euro area"] * 6) * 3,
    "size": _rng.uniform(5, 30, 36),
    "err": _rng.uniform(0.1, 0.5, 36),
})
WIDE = LONG.pivot(index="date", columns="series", values="value").reset_index()
TREE = pd.DataFrame({
    "sector": ["Banks", "Banks", "Insurers", "Insurers", "Funds"],
    "firm": ["A", "B", "C", "D", "E"],
    "assets": [40, 25, 15, 10, 10],
})
COUNTRIES = pd.DataFrame({"iso": ["GBR", "FRA", "DEU", "USA"], "rate": [5.0, 4.0, 4.0, 5.5]})


def _secondary_y():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_scatter(x=WIDE["date"], y=WIDE["Households"], name="Households")
    fig.add_scatter(x=WIDE["date"], y=WIDE["Corporates"] * 100, name="Corporates", secondary_y=True)
    return fig


#: name -> function returning a fresh figure (built with Plotly's default theme).
#: "categorical" marks charts whose series colours come from the palette.
CHARTS = {
    "line": (lambda: px.line(LONG, x="date", y="value", color="series"), True),
    "line_markers": (lambda: px.line(LONG, x="date", y="value", color="series", markers=True), True),
    "line_wide_form": (lambda: px.line(WIDE, x="date", y=["Households", "Corporates"]), True),
    "area": (lambda: px.area(LONG, x="date", y="value", color="series"), True),
    "bar_grouped": (lambda: px.bar(LONG, x="date", y="value", color="series", barmode="group"), True),
    "bar_stacked": (lambda: px.bar(LONG, x="date", y="value", color="series"), True),
    "bar_horizontal": (lambda: px.bar(LONG.head(12), y="date", x="value", color="series", orientation="h"), True),
    "scatter": (lambda: px.scatter(LONG, x="date", y="value", color="series"), True),
    "bubble": (lambda: px.scatter(LONG, x="date", y="value", color="series", size="size"), True),
    "error_bars": (lambda: px.scatter(LONG, x="date", y="value", color="series", error_y="err"), True),
    "histogram": (lambda: px.histogram(LONG, x="value", color="series"), True),
    "box": (lambda: px.box(LONG, x="series", y="value", color="series"), True),
    "violin": (lambda: px.violin(LONG, x="series", y="value", color="series"), True),
    "strip": (lambda: px.strip(LONG, x="series", y="value", color="series"), True),
    "ecdf": (lambda: px.ecdf(LONG, x="value", color="series"), True),
    "funnel": (lambda: px.funnel(TREE, x="assets", y="firm", color="sector"), True),
    "facet_col": (lambda: px.line(LONG, x="date", y="value", color="series", facet_col="panel"), True),
    "facet_grid": (lambda: px.bar(LONG, x="date", y="value", color="series", facet_row="panel", facet_col="series"), True),
    "secondary_y": (_secondary_y, True),
    "scatter_continuous": (lambda: px.scatter(LONG, x="date", y="value", color="value"), False),
    "heatmap": (lambda: px.imshow(_rng.normal(0, 1, (6, 8))), False),
    "density_heatmap": (lambda: px.density_heatmap(LONG, x="date", y="value"), False),
    "contour": (lambda: go.Figure(go.Contour(z=_rng.normal(0, 1, (6, 6)))), False),
    "pie": (lambda: px.pie(TREE, values="assets", names="firm"), False),
    "donut": (lambda: px.pie(TREE, values="assets", names="firm", hole=0.5), False),
    "sunburst": (lambda: px.sunburst(TREE, path=["sector", "firm"], values="assets"), False),
    "treemap": (lambda: px.treemap(TREE, path=["sector", "firm"], values="assets"), False),
    "waterfall": (lambda: go.Figure(go.Waterfall(x=list("abcd"), y=[3, -1, 2, -0.5])), False),
    "ohlc": (lambda: go.Figure(go.Ohlc(x=_QUARTERS[:4], open=[1, 2, 3, 2], high=[3, 4, 4, 3], low=[0, 1, 2, 1], close=[2, 3, 2, 2])), False),
    "candlestick": (lambda: go.Figure(go.Candlestick(x=_QUARTERS[:4], open=[1, 2, 3, 2], high=[3, 4, 4, 3], low=[0, 1, 2, 1], close=[2, 3, 2, 2])), False),
    "scatter_3d": (lambda: px.scatter_3d(LONG, x="value", y="size", z="err", color="series"), True),
    "line_polar": (lambda: px.line_polar(LONG.head(12), r="size", theta="value", color="series"), True),
    "bar_polar": (lambda: px.bar_polar(LONG, r="size", theta="series", color="series"), True),
    "scatter_ternary": (lambda: px.scatter_ternary(LONG, a="size", b="err", c="value", color="series"), True),
    "choropleth": (lambda: px.choropleth(COUNTRIES, locations="iso", color="rate"), False),
    "scatter_geo": (lambda: px.scatter_geo(COUNTRIES, locations="iso", color="iso"), True),
}


_N = 8
#: Awkward data shapes for a line chart: name -> kwargs for px.line.
DATASETS = {
    "quarterly_dates": dict(x=list(_QUARTERS[:_N]), y=list(range(_N))),
    "monthly_dates": dict(x=list(pd.date_range("2020-01-01", periods=_N, freq="MS")), y=list(range(_N))),
    "daily_dates": dict(x=list(pd.date_range("2024-01-01", periods=_N, freq="D")), y=list(range(_N))),
    "timezone_dates": dict(x=list(pd.date_range("2024-01-01", periods=_N, freq="h", tz="Europe/London")), y=list(range(_N))),
    "categorical_x": dict(x=[f"2023 Q{i % 4 + 1} ({i})" for i in range(_N)], y=list(range(_N))),
    "numeric_x": dict(x=list(np.linspace(0, 1, _N)), y=list(range(_N))),
    "all_negative": dict(x=list(range(_N)), y=[-v - 1 for v in range(_N)]),
    "straddles_zero": dict(x=list(range(_N)), y=[v - 4 for v in range(_N)]),
    "with_gaps": dict(x=list(range(_N)), y=[1, 2, None, 4, np.nan, 6, 7, 8]),
    "large_values": dict(x=list(range(_N)), y=[v * 1e9 for v in range(_N)]),
    "tiny_values": dict(x=list(range(_N)), y=[v * 1e-6 for v in range(_N)]),
    "single_point": dict(x=[1], y=[1]),
    "numpy_arrays": dict(x=np.arange(_N), y=np.arange(_N) ** 2),
    "pandas_series": dict(x=pd.Series(range(_N)), y=pd.Series(range(_N)) * 2),
    "unicode_names": dict(x=list(range(_N)), y=list(range(_N)),
                          color=["£ Sterling", "€ Euro"] * (_N // 2)),
    "many_series": dict(x=list(range(_N)) * 20, y=list(range(_N * 20)),
                        color=[f"s{i}" for i in range(20) for _ in range(_N)]),
}


def pytest_addoption(parser):
    parser.addoption("--update-baselines", action="store_true",
                     help="Re-render the visual regression baselines in tests/baseline/.")


@pytest.fixture(scope="session")
def _kaleido_server():
    """One persistent headless browser for all rendering, instead of one per figure."""
    import kaleido

    start = getattr(kaleido, "start_sync_server", None)
    if start is None:  # older kaleido: render one figure at a time
        yield
        return
    start(silence_warnings=True)
    yield
    kaleido.stop_sync_server(silence_warnings=True)


@pytest.fixture(autouse=True)
def _render_with_shared_browser(request):
    if request.node.get_closest_marker("render"):
        request.getfixturevalue("_kaleido_server")
