# Cantonese Ornamentation

LaTeX catalog showcasing the **cantonese** ornament family from
[`cantonese-pgfornament/`](cantonese-pgfornament/) — a pgfornament-compatible
package of original Cantonese decorative motifs.

## Build

Requires XeLaTeX, TikZ, and initialized git submodules (for the shared
preamble fonts/styles):

```shell
git submodule update --init --recursive
make
```

Or manually:

```shell
export TEXINPUTS="cantonese-pgfornament/latex//:cantonese-pgfornament/generic/cantonese//:$TEXINPUTS"
xelatex -output-directory=out cantonese-ornamentation.tex
xelatex -output-directory=out cantonese-ornamentation.tex
```

Output: `out/cantonese-ornamentation.pdf`

## Package usage

```latex
\usepackage{cantoneseornament}
\cantoneseornament[width=2cm, color=Maroon]{1}
\cantoneseframe[corner=1, edge=16, width=8cm]{Content}
\cantonesedivider{77}
```

Regenerate all 100 ornaments from SVG sources:

```shell
make ornaments
```

## Layout

| Path | Purpose |
|------|---------|
| `cantonese-ornamentation.tex` | Catalog root document |
| `preamble/pgfornament.tex` | cantoneseornament + `\ornamentview` grid macro |
| `sections/` | Cantonese ornament groupings by taxonomy |
| `cantonese-pgfornament/` | Cantonese ornament package (engine + artwork) |

## Upstream reference

The placement engine is based on vendored pgfornament v1.3. Full upstream manual:

```shell
cd cantonese-pgfornament/doc && lualatex ornaments.tex
```
