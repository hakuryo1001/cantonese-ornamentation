#!/usr/bin/env python3
"""Convert SVG paths to pgfornament .pgf format."""
from __future__ import annotations

import sys
from pathlib import Path

from svgpathtools import CubicBezier, Line, QuadraticBezier, svg2paths2


def fmt(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def convert(svg_path: str | Path, out_path: str | Path) -> None:
    paths, _attrs, _svg_attrs = svg2paths2(str(svg_path))

    lines = [
        f"% generated from {Path(svg_path).name}",
        r"\pgfsetrectcap",
        "",
    ]

    for path in paths:
        if not path:
            continue

        start = path[0].start
        lines.append(rf"\m {fmt(start.real)} {fmt(start.imag)}")

        for seg in path:
            if isinstance(seg, Line):
                end = seg.end
                lines.append(rf"\l {fmt(end.real)} {fmt(end.imag)}")

            elif isinstance(seg, CubicBezier):
                c1, c2, end = seg.control1, seg.control2, seg.end
                lines.append(
                    rf"\c {fmt(c1.real)} {fmt(c1.imag)} "
                    rf"{fmt(c2.real)} {fmt(c2.imag)} "
                    rf"{fmt(end.real)} {fmt(end.imag)}"
                )

            elif isinstance(seg, QuadraticBezier):
                p0 = seg.start
                p1 = seg.control
                p2 = seg.end
                c1 = p0 + (2 / 3) * (p1 - p0)
                c2 = p2 + (2 / 3) * (p1 - p2)
                lines.append(
                    rf"\c {fmt(c1.real)} {fmt(c1.imag)} "
                    rf"{fmt(c2.real)} {fmt(c2.imag)} "
                    rf"{fmt(p2.real)} {fmt(p2.imag)}"
                )

            else:
                raise TypeError(f"Unsupported segment: {type(seg)}")

        lines.append("")

    lines += [r"\s", r"\endinput"]

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.svg output.pgf", file=sys.stderr)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
