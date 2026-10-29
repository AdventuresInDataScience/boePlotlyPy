"""Bundled web fonts for the themes.

Plotly delegates text rendering to whatever is displaying the figure: a browser
(notebooks, ``fig.show()``, exported HTML) or a headless Chromium (kaleido image
export). Either way the font has to be *available* to that renderer.

This subpackage bundles a handful of open-source (SIL OFL) fonts and can inject
them as ``@font-face`` rules so browser-rendered figures pick them up without the
user installing anything:

    import boeplotlypy
    boeplotlypy.enable_fonts()        # in a notebook: registers the web fonts

For static image export (kaleido), install the ``.ttf`` files in this directory
to your OS instead — a headless renderer reads from the system font directories.
"""

from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

#: Directory holding the bundled ``.ttf`` files (to install them to the OS, for example).
FONTS_DIR = Path(__file__).resolve().parent

# family name -> list of (filename, weight, style)
FONT_FILES: dict[str, list[tuple[str, str, str]]] = {
    # Metric-compatible with Calibri, which the BoE themes use but can't be bundled.
    "Carlito": [
        ("Carlito-Regular.ttf", "400", "normal"),
        ("Carlito-Bold.ttf", "700", "normal"),
    ],
    "VT323": [("VT323-Regular.ttf", "400", "normal")],
    "Share Tech Mono": [("ShareTechMono-Regular.ttf", "400", "normal")],
    "Orbitron": [("Orbitron-Variable.ttf", "400 900", "normal")],
    "Press Start 2P": [("PressStart2P-Regular.ttf", "400", "normal")],
    "Comic Neue": [
        ("ComicNeue-Regular.ttf", "400", "normal"),
        ("ComicNeue-Bold.ttf", "700", "normal"),
    ],
    "Bangers": [("Bangers-Regular.ttf", "400", "normal")],
    "Pacifico": [("Pacifico-Regular.ttf", "400", "normal")],
    "Lilita One": [("LilitaOne-Regular.ttf", "400", "normal")],
    "Great Vibes": [("GreatVibes-Regular.ttf", "400", "normal")],
}


@lru_cache(maxsize=1)
def font_face_css() -> str:
    """Return ``@font-face`` rules with every bundled font embedded as base64.

    The result is self-contained (no external requests) and can be dropped into
    a ``<style>`` tag in a notebook or an exported HTML page.
    """
    rules = []
    for family, faces in FONT_FILES.items():
        for filename, weight, style in faces:
            path = FONTS_DIR / filename
            if not path.exists():
                continue
            b64 = base64.b64encode(path.read_bytes()).decode("ascii")
            rules.append(
                f"@font-face {{\n"
                f"  font-family: '{family}';\n"
                f"  font-weight: {weight};\n"
                f"  font-style: {style};\n"
                f"  font-display: swap;\n"
                f"  src: url(data:font/ttf;base64,{b64}) format('truetype');\n"
                f"}}"
            )
    return "\n".join(rules)


def enable_fonts() -> bool:
    """Inject the bundled fonts into the current notebook/IPython front-end.

    Returns ``True`` if the styles were displayed (i.e. an IPython display
    context is available), ``False`` otherwise. Call once per notebook session.
    """
    try:
        from IPython.display import HTML, display
    except ImportError:
        return False
    display(HTML(f"<style>\n{font_face_css()}\n</style>"))
    return True
