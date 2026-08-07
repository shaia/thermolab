# ThermoLab — Explore, Derive and Simulate Thermal Physics

An interactive, bilingual (English / עברית) computational textbook and virtual laboratory for
university-level thermal and statistical physics. Not a tutorial: a full learning environment
meant to take a student from zero to exam-ready at the level of leading university courses,
at the depth of a good book on the subject — plus everything interactive computing adds:
live simulations, laboratories, quizzes, exams and demonstration videos.

The guiding question, everywhere:

> **How does predictable macroscopic behaviour emerge from uncertain microscopic behaviour?**

## What's here

| Piece | Where | What it is |
| --- | --- | --- |
| Course text (EN) | `content/en/` | MyST Markdown site — the source of truth |
| Course text (HE) | `content/he/` | Full Hebrew mirror (RTL), kept in lockstep by tooling |
| Laboratories | `notebooks/{en,he}/labs/` | Interactive Jupyter notebooks (ipywidgets) |
| Physics engine | `src/thermolab/` | Plain, readable, vectorized NumPy — every model the course uses |
| Assessment | `assessment/` | Quiz banks (YAML, bilingual), exam-style problems, misconception registry |
| Animations | `media/render/` → `content/*/media/` | Simulation-rendered GIF demonstrations, language-neutral, embedded in both site copies |
| Validation | `tests/`, `scripts/` | The scientific-accuracy framework, mechanized (see below) |
| Instructor material | `instructor/` | Solutions, rubrics, diagnostics — never deployed (not yet authored) |

## Quickstart

Requirements: [uv](https://docs.astral.sh/uv/) and Node.js ≥ 18.

```powershell
uv sync                                   # Python 3.12 env with all deps
npm install                               # mystmd (site builder)

uv run pytest                             # physics test suite
uv run python scripts/validate_all.py     # every validation layer
uv run python scripts/build_site.py       # build both site copies + JupyterLite -> _site/
python -m http.server -d _site            # browse http://localhost:8000 (/en/ and /he/)

uv run jupyter lab                        # work with the lab notebooks
```

Other tools you will reach for while authoring:

```powershell
uv run python scripts/render_quizzes.py   # quiz banks -> site pages + notebook JSON
uv run python scripts/sync_notebooks.py   # copy EN code cells into the HE notebooks
uv run python scripts/stamp_hashes.py     # mark a finished translation as up to date
uv run python media/render/render_pressure.py   # regenerate a module's animations
```

On Windows, `uv` may not be on PATH; call it as `& "$env:USERPROFILE\.local\bin\uv.exe"`.

Live-preview a single language while writing: `cd content/en && npx myst start`.

## Quality: the scientific-accuracy framework

Every module passes six automated physics-test categories (dimensional consistency,
conservation, analytic limits, large-N scaling, numerical convergence, seed independence),
notebook execution in both languages, content lint (structure, model-spec blocks, fixed sign
convention `dU = δQ + δW_on`, epistemic labeling), assessment lint (answer keys, objective and
misconception coverage), and EN↔HE parity (tree, equation identity, notebook code-cell
identity, glossary consistency) — plus a human/assisted review pass. See `.claude/CLAUDE.md`
for the full conventions.

## Bilingual design

English is the authoring language; Hebrew is a first-class mirror, not an afterthought:
per-file `en_source_hash` staleness tracking, a canonical physics glossary
(`glossary/terms.yml`), byte-identical equations and code cells across languages, and an
RTL-aware build. `translation-pending.txt` must be empty for any release.

## Course map

Module 0 (orientation & prerequisites from zero) → 12 core modules (equilibrium, equations of
state, probability, kinetic theory, first law, processes, second law, entropy, fundamental
relation, potentials, ensembles, partition functions) → 6 advanced modules (chemical potential,
phase equilibrium, phase transitions, radiation & solids, quantum statistics, fluctuations &
transport). Currently built: the three vertical-slice prototypes — microscopic origin of
pressure, work & thermodynamic paths, entropy & multiplicity.
