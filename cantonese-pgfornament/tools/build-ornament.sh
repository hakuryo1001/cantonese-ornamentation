#!/usr/bin/env bash
# Build one ornament: SVG -> PGF, update library dimensions, append manifest entry.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$ROOT/tools"

usage() {
  echo "Usage: $0 <id> <svg-path> [name] [category] [family]" >&2
  echo "  id        numeric ornament id (e.g. 1)" >&2
  echo "  svg-path  path to source SVG" >&2
  echo "  name      optional display name" >&2
  echo "  category  corner|edge|centerpiece|divider|frame" >&2
  echo "  family    lingnan|maritime|merchant|flora|opera|sinoglyph" >&2
  exit 1
}

[[ $# -ge 2 ]] || usage

ID="$1"
SVG="$2"
NAME="${3:-ornament-${ID}}"
CATEGORY="${4:-other}"
FAMILY="${5:-lingnan}"

PGF="$ROOT/generic/cantonese/cantonese${ID}.pgf"
MANIFEST="$ROOT/manifest/ornaments.yaml"

python3 "$TOOLS/svg2pgf.py" "$SVG" "$PGF"
python3 "$TOOLS/gen-library.py"

python3 - "$MANIFEST" "$ID" "$NAME" "$CATEGORY" "$FAMILY" "$SVG" <<'PY'
import sys
from pathlib import Path

manifest, oid, name, category, family, source = sys.argv[1:7]
path = Path(manifest)
text = path.read_text(encoding="utf-8")
entry = (
    f"  - id: {oid}\n"
    f"    name: {name}\n"
    f"    category: {category}\n"
    f"    family: {family}\n"
    f"    status: built\n"
    f"    source: {source}\n"
)

if "ornaments: []" in text:
    text = text.replace("ornaments: []", "ornaments:\n" + entry)
elif f"id: {oid}\n" in text:
    print(f"Manifest already contains id {oid}", file=sys.stderr)
else:
    if not text.endswith("\n"):
        text += "\n"
    text += entry

path.write_text(text, encoding="utf-8")
print(f"Updated manifest: id {oid}")
PY

echo "Built cantonese${ID}.pgf"
