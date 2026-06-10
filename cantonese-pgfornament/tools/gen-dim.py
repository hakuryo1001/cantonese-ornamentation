#!/usr/bin/env python3
"""Compute ornament bounding box dimensions from an SVG file."""
from __future__ import annotations

import sys
from pathlib import Path

from svgpathtools import svg2paths2


def bbox(svg_path: str | Path) -> tuple[float, float, float, float]:
    paths, _attrs, svg_attrs = svg2paths2(str(svg_path))

    xmin = ymin = xmax = ymax = None

    for path in paths:
        if not path:
            continue
        bx = path.bbox()
        xmin = bx[0] if xmin is None else min(xmin, bx[0])
        xmax = bx[1] if xmax is None else max(xmax, bx[1])
        ymin = bx[2] if ymin is None else min(ymin, bx[2])
        ymax = bx[3] if ymax is None else max(ymax, bx[3])

    if xmin is None:
        viewbox = svg_attrs.get("viewBox") or svg_attrs.get("viewbox")
        if viewbox:
            parts = [float(v) for v in viewbox.replace(",", " ").split()]
            if len(parts) == 4:
                xmin, ymin, width, height = parts
                xmax = xmin + width
                ymax = ymin + height

    if xmin is None:
        raise ValueError(f"No paths or viewBox found in {svg_path}")

    return xmin, ymin, xmax, ymax


def dimensions(svg_path: str | Path) -> tuple[int, int]:
    xmin, ymin, xmax, ymax = bbox(svg_path)
    width = round(xmax - xmin)
    height = round(ymax - ymin)
    return max(width, 1), max(height, 1)


def dim_entry(ornament_id: int, width: int, height: int) -> str:
    return (
        f"\\or\\def\\@pgfornamentX{{{width}}}\\def\\@pgfornamentY{{{height}}}% {ornament_id}"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} input.svg [id]", file=sys.stderr)
        sys.exit(1)

    svg = sys.argv[1]
    w, h = dimensions(svg)
    print(f"bbox width={w}, height={h}")

    if len(sys.argv) >= 3:
        oid = int(sys.argv[2])
        print(dim_entry(oid, w, h))
