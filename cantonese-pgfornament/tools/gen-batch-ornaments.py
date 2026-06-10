#!/usr/bin/env python3
"""Generate programmatic seed SVG ornaments for the Cantonese library."""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
SOURCE = ROOT / "source" / "ornaments"


def svg_header() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">\n'
    )


def svg_footer() -> str:
    return "</svg>\n"


def write_svg(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg_header() + body + svg_footer(), encoding="utf-8")


def lingnan_corner(i: int) -> str:
    depth = 30 + (i % 5) * 8
    notch = 10 + (i % 4) * 5
    return (
        f'<path d="M 0 200 L 0 {200 - depth} L {notch} {200 - depth} '
        f'L {notch} {200 - depth - notch} L {depth} {200 - depth - notch} '
        f'L {depth} 200 Z"/>'
    )


def lingnan_edge(i: int) -> str:
    amp = 12 + (i % 6) * 3
    period = 40 + (i % 5) * 8
    parts = ["M 0 100"]
    x = 0
    while x <= 200:
        parts.append(f"L {x + period / 2} {100 - amp}")
        parts.append(f"L {x + period} {100 + amp}")
        x += period
    parts.append("L 200 100")
    return f'<path d="{" ".join(parts)}"/>'


def lingnan_centerpiece(i: int) -> str:
    w = 80 + (i % 4) * 10
    h = 40 + (i % 3) * 8
    x = (200 - w) / 2
    y = (200 - h) / 2
    return (
        f'<path d="M {x} {y + h} L {x + w * 0.2} {y} L {x + w * 0.8} {y} '
        f'L {x + w} {y + h} L {x + w * 0.7} {y + h * 0.6} L {x + w * 0.3} {y + h * 0.6} Z"/>'
    )


def maritime_wave(i: int) -> str:
    amp = 15 + (i % 5) * 4
    return (
        f'<path d="M 0 {120 - amp} C 25 {120 + amp}, 75 {120 - amp}, 100 {120} '
        f'C 125 {120 + amp}, 175 {120 - amp}, 200 {120}"/>'
    )


def maritime_rope(i: int) -> str:
    coils = 3 + (i % 4)
    parts = []
    for c in range(coils):
        cx = 40 + c * 45
        parts.append(
            f"M {cx - 15} 100 C {cx - 15} 70, {cx + 15} 70, {cx + 15} 100 "
            f"C {cx + 15} 130, {cx - 15} 130, {cx - 15} 100"
        )
    return f'<path d="{" ".join(parts)}"/>'


def maritime_net(i: int) -> str:
    step = 25 + (i % 3) * 5
    lines = []
    for x in range(20, 181, step):
        lines.append(f"M {x} 40 L {x} 160")
    for y in range(50, 161, step):
        lines.append(f"M 30 {y} L 170 {y}")
    return f'<path d="{" ".join(lines)}"/>'


def merchant_seal(i: int) -> str:
    size = 90 + (i % 4) * 8
    x = (200 - size) / 2
    y = (200 - size) / 2
    inner = size * 0.15
    return (
        f'<path d="M {x} {y} L {x + size} {y} L {x + size} {y + size} L {x} {y + size} Z"/>'
        f'<path d="M {x + inner} {y + inner} L {x + size - inner} {y + inner} '
        f'L {x + size - inner} {y + size - inner} L {x + inner} {y + size - inner} Z"/>'
    )


def merchant_rod(i: int) -> str:
    count = 4 + (i % 5)
    spacing = 160 / count
    parts = []
    for r in range(count):
        x = 20 + r * spacing
        h = 60 + (r % 3) * 20
        parts.append(f"M {x} {200 - 30} L {x} {200 - 30 - h}")
        parts.append(f"M {x - 6} {200 - 30 - h} L {x + 6} {200 - 30 - h}")
    return f'<path d="{" ".join(parts)}"/>'


def merchant_sycee(i: int) -> str:
    w = 100 + (i % 3) * 15
    h = 50 + (i % 4) * 8
    x = (200 - w) / 2
    y = (200 - h) / 2
    bulge = h * 0.35
    return (
        f'<path d="M {x} {y + h / 2} Q {x + w / 2} {y - bulge}, {x + w} {y + h / 2} '
        f'Q {x + w / 2} {y + h + bulge}, {x} {y + h / 2}"/>'
    )


def specs() -> list[tuple[int, str, str, str, str]]:
    items: list[tuple[int, str, str, str, str]] = []

    for i in range(1, 51):
        cat = "corner" if i <= 15 else "edge" if i <= 35 else "centerpiece"
        if cat == "corner":
            body = lingnan_corner(i)
        elif cat == "edge":
            body = lingnan_edge(i)
        else:
            body = lingnan_centerpiece(i)
        items.append((i, "lingnan", cat, f"lingnan-{cat}-{i:03d}", body))

    for i in range(51, 76):
        local = i - 50
        kind = local % 3
        if kind == 0:
            cat, body = "edge", maritime_wave(local)
        elif kind == 1:
            cat, body = "edge", maritime_rope(local)
        else:
            cat, body = "edge", maritime_net(local)
        items.append((i, "maritime", cat, f"maritime-{cat}-{i:03d}", body))

    for i in range(76, 101):
        local = i - 75
        kind = local % 3
        if kind == 0:
            cat, body = "corner", merchant_seal(local)
        elif kind == 1:
            cat, body = "divider", merchant_rod(local)
        else:
            cat, body = "centerpiece", merchant_sycee(local)
        items.append((i, "merchant", cat, f"merchant-{cat}-{i:03d}", body))

    return items


def build_all() -> None:
    build_script = TOOLS / "build-ornament.sh"
    for oid, family, category, name, body in specs():
        svg_path = SOURCE / family / f"cantonese{oid}.svg"
        write_svg(svg_path, body)
        subprocess.run(
            ["bash", str(build_script), str(oid), str(svg_path), name, category, family],
            check=True,
        )


if __name__ == "__main__":
    build_all()
    print("Generated 100 ornaments")
