# Module 00 — Orientation — Implementation Plan

> **Brainstorm:** §3 module 0 (+ §7, §8). **Module id:** `00-orientation`.
> **Content path:** `content/en/foundations/00-orientation.md`. **Status:** built.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Orientation is the course's contract-setting module. The built page does two jobs at once: it
states the question the whole course answers — how predictable macroscopic behaviour emerges
from unpredictable microscopic behaviour — in the smallest honest setting (dice: no energy, no
container, no dynamics), and it installs every convention the later modules assume silently:
the four-view table, the 7-bullet model spec, epistemic labels, the predict-first protocol,
and the three computational habits (explicit `rng` arguments, error bars on every stochastic
result, agreement judged as a dimensionless ratio).

The through-line is the N^(-1/2) emergence theme, derived from two facts only — means always
add; variances add for *independent* quantities — giving the boxed pair sigma_S = sigma_1
sqrt(N) (sum grows) and sigma_avg = sigma_1/sqrt(N) (average steadies), coefficient
sigma_1/mu_1 ~ 0.488 for a die. Deliberately withheld: the distribution's *shape* (module 3's
CLT) and the probability *guarantee* (Chebyshev → weak LLN, quarantined in the advanced
section). Two reference pages partner the module from outside the sequence — the diagnostic
routes each student into them: `math-refresher.md` (dimensions, partials, total differential,
line integrals, exactness; the readiness map deep-links its anchors) and `conventions.md`
(sign of work, \dbar, epistemic labels, model specs).

## 2. Position in the course

- **Requires:** nothing — first module; single-variable calculus is a course entry assumption.
- **Feeds:** **03** extends `sampling.py` with random-walk ensembles and CLT machinery (README
  ownership) and answers the deferred shape question, inheriting the `lln-compensation`
  falsifier pattern; **04** re-runs the argument with molecular velocities (gauge fluctuation
  at N^(-1/2)); **05** consumes lab Part 4 wholesale — exact vs inexact forms become dU vs
  \dbar \Won in the P–V plane; **08** cashes the model-spec *Ensemble* commentary ("equally
  probable by fiat" = the equal-a-priori postulate) and the multiplicity-peak narrowing;
  **18** is teased in the advanced section (variance additivity → energy fluctuation ↔ heat
  capacity). The diagnostic feeds every module via readiness routing into the partner pages.
- **Explicitly not assumed:** the CLT or any Gaussian shape; thermodynamic vocabulary; fluency
  with partials or differential forms (that is what is diagnosed); a prior probability course.

## 3. Module specification

**As-built summary.** The page carries objectives OBJ-00-1..7 — emergence via averages (1),
mean/variance of one die and of N copies (2), the N^(-1/2) law with sum-vs-average contrast
(3), dimensional analysis in SI (4), partials / total differential / line integrals (5),
exactness via mixed partials (6), the course's conventions (7) — and runs the full section
contract in order. *Puzzle:* one die is lawless, a thousand are a law; the boxed course
question. *Predict:* five commit-first items. *Explore:* two MP4s (`running-average`,
`spread-shrinks`), the model spec with commentary on *Dynamics: none* and *Ensemble as
postulate*, lab launch box, and a `numerical-observation` box separating observed settling
from derived law. *Derive:* `definition` and `theorem` boxes (variances add iff independent),
the boxed sigma pair, the ratio argument; shape and guarantee explicitly deferred. *Verify:*
four checks mirrored in the test suite (exponent −0.5, prefactor, sum +0.5 vs average −0.5,
and the "Dilution, not compensation" box — the `lln-compensation` falsifier), plus an
`open-question` box on what simulation cannot establish. *Transfer:* bullets to 03/04/08, the
road-ahead table for 0–18, the readiness map keyed to quiz ids and refresher anchors. *Quiz:*
includes generated `../_generated/quiz-00-orientation.md`. *Explain:* four free-response
items. *Advanced (last):* Markov → Chebyshev → weak law, marked safe to skip. The lab replays
the arc in six parts: running average, spread vs N, the conditioning experiment with a
pure-dilution overlay, exact/inexact line integrals via `forms`, an in-notebook assert block
mirroring the tests, and an `interact_manual` explorer (2–20 faces). The quiz bank has ten
items Q-00-1..10 (6 MC, 2 numeric, 1 prediction, 1 short-answer) covering every objective at
least once; Q-00-1's second distractor is the `lln-compensation` wrong model ("number right,
mechanism wrong"), and the registry entry is assigned here, status `addressed`. Six
objective-tagged problems include the correlated same-die variance (P1d), the absolute
10^-12 J tolerance trap (P3d), and a computational falsifier replication (P6c).
`media/render/render_orientation.py` renders both MP4s from `thermolab.sampling` itself,
language-neutral, deliberately drawing no histogram or bell — module 3's result stays unspoiled.

**Gap list**

1. **Brainstorm centrepiece shortfall — no concept map.** The "diagnostic concept map" exists
   only as the readiness-map *table* + quiz routing. Either render a real concept-map figure
   (skills → consuming modules) or permanently ratify the table as the map; decision owed.
2. **Stale status line.** Transfer says "Modules 4, 5 and 8 are written" — 01-equilibrium is
   built. One-line fix owed; the sentence will keep rotting, consider generating or dropping it.
3. **Forward pointers owed when 02/03 land:** module-3 transfer bullet and road-ahead rows gain
   links; the readiness-map partials row could point at 02's P–V–T surface (P4 already works on
   P(V,T) = N \kB T / V); 03 owes the back-link closing the deferred shape question.
4. **Diagnostic asymmetry in predict:** items cover probability (1–3), dimensions (4), partials
   (5); exactness and the sign convention are quiz-only (readiness map shows "Predicted in: —").
   A sixth commit-first item would make the diagnostic symmetric.
5. **OBJ-00-7 has no problem-set item** — conventions are tested only by Q-00-8/Q-00-10;
   defensible for a pen-and-paper set, but record the decision or add a short item.
6. **Held-variable trap is problems-only:** the (partial f/partial x)_y vs df/dx-along-a-path
   contrast lives in prediction 5 and P4(d) but has no distractor-bearing quiz item.

**Validation gates:** the six README per-module commands with `--module 00-orientation`; all
green as built (`media/` and `_generated/` are regenerated and staleness-checked by
`scripts/build_site.py`).

## 4. Library and tests

- **`src/thermolab` — existing used:** `forms.py` (`line_integral`, `mixed_partials_gap`,
  `is_exact`) in lab Part 4 and page verify; `validation.py` (`relative_error`,
  `scaling_exponent`, `seed_study`) in the lab and every stochastic test.
- **`src/thermolab` — introduced: `sampling.py`** (7-bullet model-spec docstring present;
  extended by 03 only): `die_mean` — (n+1)/2 exactly; `die_variance` — (n^2-1)/12 exactly;
  `die_relative_spread` — sigma/mean, the dimensionless N^(-1/2) coefficient; `roll_dice` —
  integer faces from an explicit generator; `running_average` — cumulative mean, the settling
  curve; `sample_averages` — one average per repeated experiment; `relative_spread_of_average`
  — measured std/mean across repetitions; `predicted_relative_spread` — the analytic
  (sigma_1/mu_1) N^(-1/2). Every stochastic function takes its `rng` explicitly.
- **`tests/physics/` coverage:** *dimensional* — `test_dimensions.py` (moments and spreads are
  pure floats; averages bounded by the faces); *conservation* — `test_conservation.py` (every
  roll a real face, counts conserved; running average ends exactly on the plain mean);
  *analytic-limit* — `test_limits.py` (7/2 and 35/12 exact; one-faced die has zero spread;
  coefficient identity at N = 100); *large-N* — `test_scaling.py` (fitted exponents −0.5
  average / +0.5 sum, prefactor within 10%); *convergence* — `test_convergence.py` (spread at
  N = 64 approaches prediction as n_samples grows); *seed-independence* — `test_seeds.py`
  (same seed reproduces exactly; `seed_study` agrees with theory at 3 sigma across base seeds).

## 5. Assessment hooks

Problem 6 is the module checkpoint: exponent *and* coefficient fit, falsifier replication with
an uncertainty, a loaded-die variant (coefficient moves, exponent does not), and "state one
thing your numbers do not prove". Exam themes: sum-vs-average direction, right-number
wrong-mechanism (Q-00-1's trap), absolute-vs-relative tolerance. Feeds forward: 03's CLT lab
reuses the spread machinery on walker ensembles; 04's synthesis compares gauge fluctuation to
(sigma_1/mu_1) N^(-1/2); 08 re-examines the ensemble postulate; 18's fluctuation–response
capstone picks up the advanced section's variance-additivity thread.

## 6. Build order and validation gates

Built first, deliberately: every later page assumes the contract this one installs. Landed
alongside it: `assessment/misconceptions.yml` entry `lln-compensation` (assigned here, status
`addressed`) and the glossary block `random-variable` … `dimensional-analysis` with
`he_reject` candidates. **HE mirror: complete** — `content/he/foundations/00-orientation.md`
(+ problems + math-refresher), `notebooks/he/labs/00-orientation.ipynb`, and
`assessment/quizzes/00-orientation.he.yml`, all `en_source_hash`-stamped;
`translation-pending.txt` lists only module 01 pages and `index.md`, nothing from 00. Gates:
the six README commands with `--module 00-orientation`, plus `scripts/check_notebooks.py` and
a `build_site.py` run to regenerate media and quiz includes.

## 7. Deviations from the brainstorm

- **Concept map → readiness map.** The graphical "diagnostic concept map" became a table
  mapping skill → prediction → quiz item → refresher anchor — actionable and testable, but the
  graphical artifact remains an open decision (gap 1).
- **Diagnostic grew a teaching arc.** The brainstorm row is pure diagnostic; the built page
  adds the N^(-1/2) derivation and the weak LLN, so orientation *states* the course question
  rather than only screening for it.
- **Math half split into partner pages** — `math-refresher.md` and `conventions.md` sit outside
  the module sequence for return visits; the module stays a module, references stay references.
- **`sampling.py` is an addition** — absent from the brainstorm §9 file list; created under the
  single-owner rule (00 introduces, 03 extends) so dice and random walks share one home.
- **No distribution shape anywhere** — page, lab, and render script all withhold histograms and
  fitted bells so module 3's CLT payoff arrives unspoiled (stated in the render script).
