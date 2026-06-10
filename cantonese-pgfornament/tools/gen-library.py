#!/usr/bin/env python3
"""Regenerate pgflibrarycantonese.code.tex from copied .pgf and .dim.json files."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PGF_DIR = ROOT / "generic" / "cantonese"
LIBRARY = ROOT / "latex" / "pgflibrarycantonese.code.tex"


def ornament_ids() -> list[int]:
    ids: list[int] = []
    for path in PGF_DIR.glob("cantonese*.pgf"):
        match = re.fullmatch(r"cantonese(\d+)\.pgf", path.name)
        if match:
            ids.append(int(match.group(1)))
    return sorted(ids)


def load_dimensions(oid: int) -> tuple[int, int]:
    dim_path = PGF_DIR / f"cantonese{oid}.dim.json"
    if dim_path.exists():
        data = json.loads(dim_path.read_text(encoding="utf-8"))
        return int(data["width"]), int(data["height"])
    return 200, 200


def build_library() -> str:
    lines = [
        "% pgflibrarycantonese.code.tex — dimension table for cantonese ornament family",
        "% AUTO-GENERATED — do not edit by hand; run tools/gen-library.py",
        r"\typeout{2026/06/10 0.1  pgflibrarycantonese.code.tex}",
        r"\makeatletter",
        r"\def\@pgfornamentDim#1{% dim in bp",
        r"\ifcase#1\relax%",
    ]

    prev = 0
    for oid in ornament_ids():
        for _ in range(prev + 1, oid):
            lines.append(r"\or")
        w, h = load_dimensions(oid)
        lines.append(f"\\or\\def\\@pgfornamentX{{{w}}}\\def\\@pgfornamentY{{{h}}}% {oid}")
        prev = oid

    lines += [
        r"\fi%",
        r"}%",
        r"% Load .pgf files by explicit project path (works with LaTeX Workshop / output-directory)",
        r"\def\pgf@@ornament#1{%",
        r"\begingroup",
        r"\def\ubb{\pgfusepath{use as bounding box}}",
        r"\def\i{\pgfusepath{clip}}%",
        r"\def\k{\pgfusepath{stroke}}%",
        r"\let\o\pgfpathclose",
        r"\let\s\pgfusepathqfillstroke",
        r"\def\p ##1##2{\pgfqpoint{##1bp}{##2bp}}%",
        r"\def\m ##1 ##2 {\pgfpathmoveto{\p{##1}{##2}}}%",
        r"\def\l ##1 ##2 {\pgfpathlineto{\p{##1}{##2}}}%",
        r"\def\r ##1 ##2 ##3 ##4 {\pgfpathrectangle{\p{##1}{##2}}{\p{##3}{##4}}}%",
        r"\def\c ##1 ##2 ##3 ##4 ##5 ##6 {%",
        r"\pgfpathcurveto{\p{##1}{##2}}{\p{##3}{##4}}{\p{##5}{##6}}}%",
        r"\@@input cantonese-pgfornament/generic/cantonese/cantonese#1.pgf%",
        r"\endgroup}%",
        r"\makeatother",
        r"\endinput",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    LIBRARY.write_text(build_library(), encoding="utf-8")
    print(f"Wrote {LIBRARY} ({len(ornament_ids())} ornaments)")


if __name__ == "__main__":
    main()
