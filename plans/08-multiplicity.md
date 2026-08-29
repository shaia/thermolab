# Module 08 — Entropy and multiplicity — Implementation Plan

> **Brainstorm:** §3 module 8 (+ §5 "Entropy and multiplicity laboratory", §10 Prototype C).
> **Module id:** `08-multiplicity`.
> **Content path:** `content/en/statistical-mechanics/08-multiplicity.md`. **Status:** built.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

This is the course's Prototype C and, by the brainstorm's own reckoning, its hardest idea: the
macroscopic arrow of time is not mechanics but counting. The page opens with the time-reversal
puzzle (gas fills, never regathers; every collision is reversible) and dissolves it with the
two-state model — `Omega(N, n) = C(N, n)` microstates per macrostate, equal a priori
probability boxed as a *postulate*, the `1/sqrt(N)` collapse of the peak's relative width, and
Boltzmann's `S = \kB \ln \Omega` with the logarithm forced by additivity. No energy, no
temperature: equilibrium macrostates are simply overwhelmingly probable, and irreversibility
emerges from combinatorics alone.

Per conflict-log item C2, 08 is the statistical middle of the entropy spiral 07 → 08 → 09: 07
introduces entropy macroscopically as the Clausius integral `S = \int \dbar Q_rev / T`, 08
reinterprets it as a count of microstates, and 09 unifies the two in `S(U,V,N)` and owns
quantitative entropy *production*. The built page honours the split by never invoking heat or
temperature; its second law is "the total multiplicity of an isolated system overwhelmingly
increases", falsified at subsystem level, with the mechanism for *which way* an exchange runs
deferred to 11 (energy) and 13 (particles). Beyond the brainstorm row it adds two numerically
staged misconception falsifiers (isotope crystal, subsystem bookkeeping), Stirling's formula
as an error-bounded tool, and extensivity as a measured thermodynamic-limit observation —
seeds for 09's maximization principle and 11–12's ensemble equivalence.

## 2. Position in the course

- **Requires:** `00-orientation` — basic probability, histograms, the predict-first habit;
  `04-pressure` — the `N^{-1/2}` relative-fluctuation law, called back when the peak width is
  derived. It does *not* assume `03-random-walks` (not yet built): the Gaussian limit is
  derived directly by second-order expansion of `ln Omega`, with the CLT named only as context.
- **Feeds:** `09-fundamental-relation` — `S = \kB \ln \Omega` and peak sharpness become the
  entropy surface and constrained maximization; `11-ensembles` — the model-spec failure mode
  ("different energies, where the Boltzmann factor takes over") is 11's opening; `12`
  (paramagnet counting), `13` (particle-exchange mechanism promised in advanced), `15`
  (interacting failure mode), `18` (fluctuation scaling).
- **Explicitly not assumed:** Clausius entropy `S = \int \dbar Q_rev / T` and the Clausius
  inequality — 07's per C2; temperature, heat, the Boltzmann factor (11's); the first law
  `dU = \dbar Q + \dbar \Won` plays no role in this energy-free model.

## 3. Module specification

**As-built summary.** The page ships the full section contract (`puzzle → predict → explore →
derive → verify → transfer → quiz → explain → advanced`) with six objectives `OBJ-08-1..6`
(irreversibility as counting; the equal-probability postulate; `Omega(N,n)` and peak width;
`S = kB ln Omega` from additivity; Stirling and extensivity; entropy vs "disorder"). Predict
stages four commit-first questions, two of them misconception traps. Explore carries the
7-bullet model spec and two language-neutral MP4s (`multiplicity-two-box.mp4`,
`multiplicity-peak.mp4`) rendered from the library by `media/render/render_multiplicity.py`.
Every epistemic class except `empirical-law` is boxed: `definition` ×3, `model-assumption` ×2,
`theorem` (log from additivity), `approximation` ×2 (Gaussian limit; Stirling with measured
2-term vs 3-term errors), `numerical-observation` ×4, `open-question` (what the urn can prove).
`entropy-is-disorder` is falsified by the isotope crystal (`Omega = 1` vs
`Omega(1000,500) ~ 2.7e299`, identical appearance); `subsystem-entropy-increase` by exact
bookkeeping (`Delta S_L/kB ~ -0.17` against `+133.77` total), the missing dynamics honestly
flagged as stipulated. The lab (9 parts) counts `N = 10` by hand, fits the `N^(-1/2)` width
exponent, measures Stirling/extensivity errors, overlays Gaussian vs exact at `N = 4000`, runs
the Ehrenfest urn plus a 24-realisation spread, re-runs both falsifiers as assertions, embeds
the test-suite checks, and ends with an `ipywidgets` explorer (`N` slider 4–400, vectorized
NumPy, Pyodide-safe). Quiz bank: `Q-08-1..9` (6 multiple-choice, 1 numeric, 1 prediction, 1
short-answer), every objective covered, distractors keyed to both registry misconceptions.
Problem set: 6 problems (5 pen-first, 1 computational), objective-tagged.

**Gap list**

1. **C2(a) — verify-bridge to Clausius entropy.** Once 07 exists (`cycles.py`), add a verify
   check that `\kB \ln \Omega` reproduces `\int \dbar Q_rev / T` for a concrete case — free
   expansion doubling the volume: `Delta S = N \kB \ln 2` from counting vs from 07's
   reversible isothermal replacement path. Also pays off predict question 4 (melting ice),
   whose quantitative `Q/T` ledger the built page cannot yet supply.
2. **C2(b) — gas-mixing / Gibbs-paradox transfer teaser.** The brainstorm centrepiece is "gas
   mixing and multiplicity simulation"; the built module does the two-box Ehrenfest version.
   Mixing entropy is qualitative in transfer, Gibbs paradox advanced-only. Owed: a transfer
   teaser to the quantitative two-species mixing simulation and the indistinguishability fix
   (natural home 13, with 09's extensivity machinery); glossary terms already landed.
3. **Weak cross-linking.** Back-link the Gaussian-limit box to 03's CLT once 03 is built, and
   add the forward/backward module links the template asks of the four transfer bullets.
4. **No closing `measurement:` cell.** The lab measures (fitted exponent, urn spread) but
   never lands a formal value ± error cell; the width exponent vs `-0.5` is the candidate.
5. **No convergence-category test.** `tests/physics/test_convergence.py` never touches
   `multiplicity`; the Stirling order-0 → order-1 → exact ladder would close invariant 8.
6. **No real-experiment counterpart.** Brainstorm §5 says "use coins"; a 20-coin shuffle
   count imported into lab Part 1 would be nearly free.

**Validation gates:** the six standard per-module commands (README bottom) with
`--module 08-multiplicity`; all pass as built.

## 4. Library and tests

- **`src/thermolab` — introduced: `multiplicity.py`** (single owner, never extended), 7-bullet
  model-spec docstring in place. `multiplicity(n_objects, n_in_first_state) -> float` —
  `Omega(N,n)` via the log form; `log_multiplicity(...) -> float` — `ln Omega` by log-gamma;
  `log_multiplicity_array(n_objects, counts) -> ndarray` — vectorised `ln Omega`;
  `entropy(...) -> float` — `S = kB ln Omega` [J/K]; `probability(...) -> float` —
  `Omega / 2^N` under the postulate; `stirling_log_factorial(n, order=1) -> float` — 2/3-term
  Stirling, testable against `gammaln`; `gaussian_multiplicity_fraction(n, counts)` — peak
  Gaussian, `sigma = sqrt(N)/2`; `peak_relative_width(n) -> float` — `N^(-1/2)`;
  `sample_two_box(n_objects, n_steps, rng, n_in_first_state=None) -> ndarray` — Ehrenfest urn
  with explicit generator.
- **Existing used:** `constants.K_B`; `validation.relative_error`/`scaling_exponent` (lab).
- **`tests/physics/` coverage:** dimensional — entropy is a J/K float, `Omega` dimensionless
  (`test_dimensions.py`); conservation — urn occupancy bounded, count conserved
  (`test_conservation.py`); analytic-limit — exact binomial at small `N`, peak at even split,
  Stirling error `< 1.01/(12N)`, Gaussian within 1% at `N = 4000`, `S = 0` at ordered extremes
  (`test_limits.py`); large-N — width-exponent fit, `1e-80` corner suppression at `N = 10^4`,
  shrinking extensivity discrepancy, urn holds the split (`test_scaling.py`,
  `test_limits.py`); seed-independence — urn statistics across generators (`test_seeds.py`);
  convergence — **not covered** (gap 5).

## 5. Assessment hooks

Checkpoint synthesis: 04 + 08 — one `N^{-1/2}` law from two roots (time-averaged pressure vs
pure combinatorics); problem 5's subsystem ledger is the refrigerator seed for 07/10 synthesis
("something else pays more than the difference"). Exam themes: postulate-vs-theorem status of
equal probability (Q-08-2), multiplicity arithmetic under scaling (Q-08-7's three-quantity
prediction), extensivity as a limit statement (Q-08-9). Feeds 09's entropy-surface capstone,
11–12's paramagnet `S(U)` (this counting verbatim), and the future 07↔08 bridge of gap 1.

## 6. Build order and validation gates

Built — third of the three brainstorm §10 prototypes (C), after 04 (A) and 05 (B); it anchors
`statistical-mechanics/`, which 03 later opens. Landed with it: `entropy-is-disorder` and
`subsystem-entropy-increase` are `status: addressed` in `assessment/misconceptions.yml`;
`microstate`, `macrostate`, `multiplicity`, `entropy` (with `he_reject`), `entropy-of-mixing`,
`gibbs-paradox`, `shannon-entropy`, `ergodicity` are in `glossary/terms.yml`. HE mirror family
complete — verified present: `content/he/statistical-mechanics/08-multiplicity{,-problems}.md`,
`notebooks/he/labs/08-multiplicity.ipynb`, `assessment/quizzes/08-multiplicity.he.yml`; 08 is
absent from `translation-pending.txt` (only 01's family is listed). Gates: the six README
commands with `--module 08-multiplicity`.

## 7. Deviations from the brainstorm

- **C2 re-scope (major).** Brainstorm §3 row 8 lists "Clausius entropy, entropy production,
  mixing and irreversibility"; built 08 is purely statistical. Clausius entropy and the
  inequality → 07; quantitative entropy production → 09. Rationale: preserves the §2 spiral
  (macroscopic → statistical → structural) and keeps 08 free of temperature entirely.
- **Centrepiece narrowed.** "Gas mixing and multiplicity simulation" → two-box Ehrenfest urn:
  isomorphic counting, browser-cheap; the mixing/Gibbs-paradox half is owed as a transfer
  teaser (gap 2) rather than silently dropped.
- **Additions beyond the row:** measured Stirling `1/(12N)` bound, extensivity-as-limit
  observation, the subsystem-entropy falsifier, and Loschmidt/Poincaré in advanced — all in
  service of the §7 accuracy framework's epistemic labels.
