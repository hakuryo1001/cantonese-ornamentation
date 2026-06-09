# Cantonese Ornamentation — pgfhan catalog

LaTeX catalog showcasing all 78 **pgfhan** ornaments from the vendored
[`pgfornament/`](pgfornament/) package (Chinese traditional motifs).

## Build

Requires XeLaTeX, TikZ, and initialized git submodules (for the shared
preamble fonts/styles):

```shell
git submodule update --init --recursive
make
```

Or manually:

```shell
export TEXINPUTS="pgfornament/latex//:pgfornament/generic/pgfhan//:$TEXINPUTS"
xelatex main.tex
xelatex main.tex
```

Output: `main.pdf`

## Layout

| Path | Purpose |
|------|---------|
| `main.tex` | Catalog root document |
| `preamble/pgfornament.tex` | pgfornament + `\ornamentview` grid macro |
| `sections/` | pgfhan groupings (corners, lines, other symbols) |
| `pgfornament/` | Vendored upstream pgfornament package (read-only) |

## Upstream reference

Full pgfornament manual (vectorian + pgfhan + am):

```shell
cd pgfornament/doc && lualatex ornaments.tex
```
