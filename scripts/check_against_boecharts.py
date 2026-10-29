"""Compare boeplotlypy's palettes against a local checkout of boeCharts.

Parses the palette definitions in boeCharts' R source and reports any palette
or colour that differs from ``boeplotlypy.palettes``. Use it to verify the port
and to pick up changes when boeCharts is updated.

Run with:
    git clone --depth 1 https://github.com/bank-of-england/boeCharts.git <dir>
    uv run python scripts/check_against_boecharts.py <dir>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from boeplotlypy.palettes import _DEFINITIONS

# Deliberate deviations from boeCharts, documented in palettes.py.
KNOWN_DEVIATIONS = {"vibrant_h"}

_LIST_DEF = re.compile(r"^(\w+)\s*(?:<-|=)\s*(?:list|c)\((.*?)^\)", re.M | re.S)
_ENTRY = re.compile(r"(\w+)\s*=\s*(?:\"(#[0-9A-Fa-f]{6})\"|(\w+)\$(\w+))")


def _strip_roxygen(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))


def parse_r_palettes(repo: Path) -> dict[str, dict[str, dict[str, str]]]:
    """Return ``{group: {palette: {colour_name: hex}}}`` as defined in boeCharts."""
    colours: dict[str, dict[str, str]] = {}
    for filename in ("colours.R", "combinations.R"):
        text = _strip_roxygen((repo / "R" / filename).read_text(encoding="utf-8"))
        for name, body in _LIST_DEF.findall(text):
            entries: dict[str, str] = {}
            for key, hex_, ref_list, ref_key in _ENTRY.findall(body):
                if hex_:
                    entries[key] = hex_.upper()
                else:
                    # A reference like boe_rich$rich_blue. R yields NULL (and
                    # drops the colour) when the key doesn't exist.
                    value = colours.get(ref_list, {}).get(ref_key)
                    if value is not None:
                        entries[key] = value
            colours[name] = entries

    groups: dict[str, dict[str, dict[str, str]]] = {}
    text = _strip_roxygen((repo / "R" / "palettes.R").read_text(encoding="utf-8"))
    for group_name, body in _LIST_DEF.findall(text):
        if group_name == "boe_palettes":
            continue
        members = re.findall(r"(\w+)\s*=\s*\w+", body)
        # boe_identity_palettes -> identity, boe_vibrant_palettes -> vibrant, ...
        short = group_name.replace("boe_", "", 1).replace("_palettes", "")
        groups[short] = {m: colours[m] for m in members}
    return groups


def compare(repo: Path) -> int:
    r_groups = parse_r_palettes(repo)
    problems = []

    if list(r_groups) != list(_DEFINITIONS):
        problems.append(f"groups differ: R {list(r_groups)} vs Python {list(_DEFINITIONS)}")

    for group, r_palettes in r_groups.items():
        py_palettes = _DEFINITIONS.get(group, {})
        if list(r_palettes) != list(py_palettes):
            problems.append(
                f"[{group}] palettes differ: R {list(r_palettes)} vs Python {list(py_palettes)}"
            )
        for name, r_colours in r_palettes.items():
            if name in KNOWN_DEVIATIONS or name not in py_palettes:
                continue
            py_colours = {k: v.upper() for k, v in py_palettes[name].items()}
            if r_colours != py_colours:
                problems.append(f"[{group}] {name}: R {r_colours} vs Python {py_colours}")

    n = sum(len(p) for p in r_groups.values())
    if problems:
        print(f"{len(problems)} difference(s) across {n} boeCharts palettes:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"All {n} boeCharts palettes match "
          f"(known deviations: {', '.join(sorted(KNOWN_DEVIATIONS))}).")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(compare(Path(sys.argv[1])))
