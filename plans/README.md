# ThermoLab implementation plans

One detailed implementation plan per module — the enhancement layer between
[`thermolab_university_thermodynamics_brainstorm.md`](../thermolab_university_thermodynamics_brainstorm.md)
(the master curriculum document) and the content in `content/`. This folder is where
content is enhanced and refined beyond the brainstorm — derivation routes, library
signatures, misconception falsifiers, quiz banks, runtime budgets — before any content
file is written.

Plans are **design artifacts, not content**: nothing here is linted by the validators or
deployed to the site. But every seeded formula must already obey the course conventions
(sign convention, macros, epistemic labels — see invariants below) so it can be pasted
into `content/` untouched.

Every plan follows [`_template.md`](_template.md). Built modules carry an as-built
summary plus a gap list instead of a full specification.

## Files

| Plan | Brainstorm §3 row | Status |
|---|---|---|
| [00-orientation.md](00-orientation.md) | 0. Orientation | built |
| [01-equilibrium.md](01-equilibrium.md) | 1. Thermal equilibrium | built |
| [02-equations-of-state.md](02-equations-of-state.md) | 2. Equations of state | built |
| [03-random-walks.md](03-random-walks.md) | 3. Probability and emergence | planned |
| [04-pressure.md](04-pressure.md) | 4. Kinetic theory | built |
| [05-work-paths.md](05-work-paths.md) | 5. First law | built |
| [06-processes.md](06-processes.md) | 6. Thermodynamic processes | planned |
| [07-second-law.md](07-second-law.md) | 7. Second law | planned |
| [08-multiplicity.md](08-multiplicity.md) | 8. Entropy | built |
| [09-fundamental-relation.md](09-fundamental-relation.md) | 9. Fundamental relation | planned |
| [10-potentials.md](10-potentials.md) | 10. Thermodynamic potentials | planned |
| [11-ensembles.md](11-ensembles.md) | 11. Statistical ensembles | planned |
| [12-partition-functions.md](12-partition-functions.md) | 12. Partition functions | planned |
| [13-chemical-potential.md](13-chemical-potential.md) | 13. Chemical potential | planned |
| [14-coexistence.md](14-coexistence.md) | 14. Phase equilibrium | planned |
| [15-ising.md](15-ising.md) | 15. Phase transitions | planned |
| [16-radiation-solids.md](16-radiation-solids.md) | 16. Thermal radiation and solids | planned |
| [17-quantum-gases.md](17-quantum-gases.md) | 17. Quantum statistics | planned |
| [18-fluctuations-transport.md](18-fluctuations-transport.md) | 18. Fluctuations and transport | planned |

## Canonical module map

Module ids are a flat two-digit `NN-slug` counter matching brainstorm §3 module numbers
1:1. Ids are opaque; teaching order is set by the TOC in `content/en/myst.yml` (02 and
03 slot before the built 04 at build time). Two placement decisions: **module 3 lives in
`statistical-mechanics/`** — it opens the micro-to-macro program (03 → 08 → 11 → 12);
`foundations/` is pre-course material. **`advanced/` becomes a new top-level content
directory** for modules 13–18 (the brainstorm §9 layout; the prerequisite boundary is
real — quantum mechanics is assumed only from module 17).

| # | Module id | content/en/ path | Title | Centrepiece | Status |
|---|---|---|---|---|---|
| 0 | `00-orientation` | `foundations/` | Orientation | diagnostic + readiness quiz | **built** |
| 1 | `01-equilibrium` | `thermodynamics/` | Thermal equilibrium | two bodies exchanging energy | **built** |
| 2 | `02-equations-of-state` | `thermodynamics/` | Equations of state | interactive P-V-T surface | **built** |
| 3 | `03-random-walks` | `statistical-mechanics/` | Probability and emergence | walker cloud → Gaussian | planned |
| 4 | `04-pressure` | `thermodynamics/` | Kinetic theory | particles + piston | **built** |
| 5 | `05-work-paths` | `thermodynamics/` | Work and paths (first law) | draw a P-V path, compute W | **built** |
| 6 | `06-processes` | `thermodynamics/` | Thermodynamic processes | polytropic slider + full W/Q/ΔU/ΔT ledger | planned |
| 7 | `07-second-law` | `thermodynamics/` | The second law | engine constructor vs Carnot bound | planned |
| 8 | `08-multiplicity` | `statistical-mechanics/` | Entropy and multiplicity | two-box multiplicity simulation | **built** |
| 9 | `09-fundamental-relation` | `thermodynamics/` | The fundamental relation | entropy-surface maximizer | planned |
| 10 | `10-potentials` | `thermodynamics/` | Thermodynamic potentials | natural-variables map + Maxwell verifier | planned |
| 11 | `11-ensembles` | `statistical-mechanics/` | Statistical ensembles | finite heat bath → Boltzmann | planned |
| 12 | `12-partition-functions` | `statistical-mechanics/` | Partition functions | U, S, F, C_V from Z numerically | planned |
| 13 | `13-chemical-potential` | `advanced/` | Chemical potential | two systems exchanging particles | planned |
| 14 | `14-coexistence` | `advanced/` | Phase equilibrium | vdW Maxwell construction, Clausius–Clapeyron | planned |
| 15 | `15-ising` | `advanced/` | Phase transitions | Metropolis Ising through T_c | planned |
| 16 | `16-radiation-solids` | `advanced/` | Thermal radiation and solids | blackbody + Einstein/Debye explorers | planned |
| 17 | `17-quantum-gases` | `advanced/` | Quantum statistics | MB/BE/FD occupation explorer | planned |
| 18 | `18-fluctuations-transport` | `advanced/` | Fluctuations and transport | random walk → diffusion equation | planned |

Slug notes: `03-random-walks`, `14-coexistence`, and `15-ising` name the module's
centrepiece rather than the brainstorm chapter title, keeping the two "phase" modules
unmistakable. Modules 0–12 are the one-semester core; 13–18 are the second-term /
honours extension.

### Teaching order

Teaching order equals id order. The spiral (brainstorm §2) is deliberate: pressure is
observed macroscopically (02) and reproduced microscopically (04); entropy is introduced
macroscopically (07), reinterpreted statistically (08), and unified structurally (09);
free energy appears thermodynamically (10) and is derived from the canonical ensemble
(11–12).

## Cross-plan invariants

1. **Sign convention** — `dU = \dbar Q + \dbar \Won` (work done *on* the system),
   everywhere, silently switching never. Module 07 may present the engine convention
   (`W_by`) only as an explicitly labeled exception, per `content/en/conventions.md`.
2. **Module contract** — mandatory sections in this exact order, as MyST labels
   `(<slug>-<suffix>)=`: `puzzle → predict → explore → derive → verify → transfer →
   quiz → explain`, plus optional `advanced` **last**; no core content may depend on an
   advanced section. Frontmatter carries `module:` and non-empty `objectives:` with
   `OBJ-NN-K` ids in ASCII math (enforced by `scripts/check_modelspec.py`).
3. **Model specifications** — every simulation gets the 7-bullet spec in fixed order:
   System / Dynamics / Boundary / Ensemble / Ignored / Valid when / Failure modes; the
   same block heads the docstring of every `src/thermolab` physics file.
4. **Epistemic labels** — claims are boxed as `definition | empirical-law | theorem |
   model-assumption | approximation | numerical-observation | open-question`; at least
   one per module page. Simulation never proves: derivations establish, simulations
   illustrate, experiments decide.
5. **Single-owner library rule** — each `src/thermolab` file is *introduced* by exactly
   one plan (ownership table below); other plans may extend it with their own functions
   only. Notebooks orchestrate lessons; they never re-implement physics.
6. **Bilingual artifact family** — every module ships: EN page + `-problems.md` + lab
   notebook + quiz bank (`assessment/quizzes/<slug>.en.yml` and `.he.yml`) + HE mirrors
   with `en_source_hash` stamps; `glossary/terms.yml` is the *only* source of Hebrew
   terminology (new terms land there with `he_reject` candidates); in-progress pages are
   listed in `translation-pending.txt`.
7. **Misconception registry** — `assessment/misconceptions.yml` entries are design
   requirements: the assigned module must stage a falsifying experiment and a quiz
   distractor built on the wrong model. Plans propose NEW entries; registry edits happen
   when the module is built.
8. **Six physics-test categories** — every library addition is covered under
   dimensional / conservation / analytic-limit / large-N / convergence /
   seed-independence (`tests/physics/`, pytest markers in `pyproject.toml`).

## `src/thermolab/` ownership

Existing files `constants`, `units`, `forms`, `multiplicity`, `validation` are consumed
but never extended. `sampling` (00/03), `equilibrium` (01/09), `kinetics` (04/18), and
`paths` (05/06) each have one introducing module and one extender.

| New file | Introduced by | Extended by | Serves modules |
|---|---|---|---|
| `gases.py` | 02 | — | 02, 04, 06, 14, 17 |
| `cycles.py` | 07 | — | 07, 09, 10 |
| `fundamental.py` | 09 | — | 09, 10, 13 |
| `potentials.py` | 10 | — | 10, 13, 14 |
| `ensembles.py` | 11 | — | 11, 12, 13 |
| `partition.py` | 12 | — | 12, 16, 18 |
| `chemical.py` | 13 | — | 13, 14, 17 |
| `phases.py` | 14 | — | 14, 15 |
| `ising.py` | 15 | — | 15 |
| `radiation.py` | 16 | — | 16, 17 |
| `quantum.py` | 17 | — | 17 |
| `transport.py` | 18 | — | 18 |

| Existing file | Extended by | With |
|---|---|---|
| `sampling.py` | 03 | random-walk ensembles, CLT machinery |
| `paths.py` | 06 | polytropic family, heat capacities, process ledger |
| `equilibrium.py` | 09 | entropy ledger on energy exchanges |
| `kinetics.py` | 18 | mean free path, collision rate |

The brainstorm §9 file list is adapted: `phase_transitions.py` is split into `phases.py`
(14, deterministic EOS analysis) + `ising.py` (15, stochastic Monte Carlo) to honour the
single-owner rule; `visualization.py` is rejected — rendering lives in `media/render/`
scripts, the library is physics only.

## Conflict log

- **C1 — 05/06 boundary.** Built `05-work-paths` already owns the path constructors,
  `W_on` along arbitrary paths, exact-vs-inexact differentials, and path comparison for
  work. Module 06 is re-scoped to: heat capacities `C_V`/`C_P`/Mayer/γ *derived* (05
  takes γ as an input), the adiabat `P V^gamma = const` derivation (05 asserts it), the
  full per-process Q/ΔU/ΔT ledger, the polytropic family, and quantitative irreversible
  processes (Joule free expansion, sudden compression). Both plans state the division.
- **C2 — entropy split across 07/08/09.** 07 defines Clausius entropy
  (`S = ∫ \dbar Q_rev / T` + the Clausius inequality, via `cycles.py`); 08 keeps the
  statistical half (as built); 09 owns quantitative entropy *production* (entropy-surface
  experiments + the `equilibrium.py` extension). 08's gap list records a future
  verify-bridge (`\kB ln Omega` ↔ `∫ \dbar Q_rev / T`) and a mixing/Gibbs-paradox
  transfer teaser. This preserves the brainstorm §2 spiral: macroscopic → statistical →
  structural.
- **C3 — pending misconception re-pointings** (registry edits at build time):
  `canonical-equal-probability` → `11-ensembles` (falsifier: exact enumeration shows
  joint system+bath microstates equiprobable while the system's marginal is
  exponentially weighted); `negative-t-colder` → `12-partition-functions` (paramagnet
  S(U) peak; an inverted population gives off heat to any positive-T body — hotter than
  T = ∞, not colder than zero).
- **C4a — duplicated physics.** `ideal_gas_pressure` is defined in both `kinetics.py`
  and `paths.py` (and `ideal_gas_temperature` in `paths.py` only). Plan 02 makes
  `gases.py` the canonical home; `kinetics`/`paths` import from it — one-line refactors
  applied when 02 is built.
- **C4b — 16/17 ordering.** 16 needs the Planck occupation before 17 exists: 16 derives
  it inline (self-contained); 17's verify section recomputes the Planck curve from
  `quantum.bose_einstein(mu=0)` to close the loop. No file introduced by a later module
  is imported by an earlier one.
- **C4c — Einstein-solid spiral.** `equilibrium.py`'s Einstein solid recurs deliberately:
  01 (energy exchange) → 09 (its S(U,N) fundamental relation) → 12 (oscillator Z
  reproduces 01's temperature map) → 16 (Einstein heat capacity). Plans seed these as
  payoffs, not accidents.
- **C4d — repo layout.** The brainstorm §9 sketch (`book/`, `visualization.py`) is
  superseded by the real bilingual `content/{en,he}` structure and the media-scripts
  rule; the brainstorm's section headings and module rows remain canonical for content.

## Status

| Module | Plan | Content built |
|---|---|---|
| 00, 01, 04, 05, 08 | as-built + gap list | yes |
| 02, 03, 06, 07, 09–12 | full specification | no |
| 13–18 | full specification | no |

## Validation gates (per module, when built)

```sh
uv run python scripts/check_modelspec.py --module <NN-slug>
uv run python scripts/check_assessment.py
uv run python scripts/check_glossary.py
uv run python scripts/check_parity.py
uv run python -m pytest tests/physics -q
uv run python scripts/validate_all.py --module <NN-slug>
```
