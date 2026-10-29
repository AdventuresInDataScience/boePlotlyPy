"""Generate the README preview image (docs/images/boe_themes.png).

Renders a line chart and a bar chart in every Bank of England theme and tiles
them into one image. With ``--legacy``, also writes a preview per hidden theme
to docs/images/<theme>.png.

Run with:  uv run python scripts/generate_previews.py [--legacy]
"""

from __future__ import annotations

import math
import sys
import tempfile
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

import boeplotlypy as boe

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "images"
WIDTH, HEIGHT = 800, 500

# Legacy themes whose look depends on the add_glow() effect.
GLOW_THEMES = {"star_wars", "cyberpunk", "synthwave"}

_DATES = pd.date_range("2015-01-01", periods=40, freq="QS")
LINES = pd.DataFrame({
    "date": list(_DATES) * 3,
    "Per cent": [2 + 1.5 * math.sin(i / 4) + i * 0.02 for i in range(40)]
    + [1.8 + math.cos(i / 5) for i in range(40)]
    + [2.5 + 1.2 * math.sin(i / 3 + 1) - i * 0.03 for i in range(40)],
    "Series": ["CPI"] * 40 + ["Core CPI"] * 40 + ["Services"] * 40,
})
BARS = pd.DataFrame({
    "Quarter": ["2023 Q1", "2023 Q2", "2023 Q3", "2023 Q4"] * 3,
    "Contribution": [0.8, 0.9, 0.1, -1.4, -0.1, -0.8, -1.4, 0.3, -0.6, -1.0, -1.1, 0.3],
    "Sector": ["Households"] * 4 + ["Corporates"] * 4 + ["Government"] * 4,
})


def boe_figures(theme: str):
    """A line chart and a bar chart in the given theme."""
    line = px.line(LINES, x="date", y="Per cent", color="Series")
    bar = px.bar(BARS, x="Quarter", y="Contribution", color="Sector")
    for fig in (line, bar):
        fig.update_layout(width=WIDTH, height=HEIGHT, xaxis_title=None, yaxis_title=None)
    boe.apply_formatting(line, theme=theme, title="Chart 2.1: CPI inflation",
                         subtitle="Percentage changes on a year earlier",
                         source="Sources: ONS and Bank calculations.")
    boe.apply_formatting(bar, theme=theme, title="Chart 3.4: Contributions to growth",
                         subtitle="Percentage points",
                         source="Sources: ONS and Bank calculations.", hline0=True)
    return line, bar


def write_boe_sheet() -> Path:
    themes = boe.registered_themes()
    sheet = Image.new("RGB", (WIDTH * 2, HEIGHT * len(themes)), "white")
    with tempfile.TemporaryDirectory() as tmp:
        for row, theme in enumerate(themes):
            for col, fig in enumerate(boe_figures(theme)):
                path = Path(tmp) / f"{theme}_{col}.png"
                fig.write_image(path)
                with Image.open(path) as im:
                    sheet.paste(im, (col * WIDTH, row * HEIGHT))
            print(f"rendered {theme}")
    out = OUT_DIR / "boe_themes.png"
    sheet.save(out)
    return out


def write_legacy_previews() -> None:
    x = list(range(1, 13))
    for name in sorted(set(boe.registered_themes(include_hidden=True)) - set(boe.registered_themes())):
        fig = go.Figure()
        fig.add_bar(x=x, y=[4 + 3 * abs(math.sin(i / 1.3)) for i in x], name="Volume")
        fig.add_scatter(x=x, y=[10 + 6 * math.sin(i / 1.7) + i * 0.4 for i in x], mode="lines+markers", name="Series A")
        fig.add_scatter(x=x, y=[8 + 5 * math.cos(i / 2.1) + i * 0.25 for i in x], mode="lines+markers", name="Series B")
        fig.update_layout(template=name, title=f"boeplotlypy — {name}", width=900, height=500,
                          margin=dict(l=70, r=30, t=70, b=60))
        if name in GLOW_THEMES:
            boe.add_glow(fig)
        fig.write_image(OUT_DIR / f"{name}.png")
        print(f"wrote {name}.png")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"wrote {write_boe_sheet()}")
    if "--legacy" in sys.argv:
        write_legacy_previews()


if __name__ == "__main__":
    main()
