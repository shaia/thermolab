# Module 04 — The microscopic origin of pressure — Implementation Plan

> **Brainstorm:** §3 module 4, §5 particle pressure laboratory, §10 prototype A. **Module id:** `04-pressure`.
> **Content path:** `content/en/thermodynamics/04-pressure.md`. **Status:** built.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Every individual molecular impact is violent, random and discrete — yet a barometer built in
1643 still works. The module resolves the puzzle without making the collisions gentler: the
relative jitter of a sum over $N$ independent events falls as $N^{-1/2}$, and a mole puts it at
$4 \times 10^{-13}$, below the noise floor of reality. This is the course's **Prototype A**
(brainstorm §10) and its first quantitative law of large numbers — a measured exponent and a
measured coefficient of 1, explained via chi-square, not "the noise averages out".

The spiral does its first full turn: pressure, met macroscopically in 01 (and owed an empirical
treatment by 02), is *reproduced* from mechanics plus one statistical statement. The derivation
keeps the seam visible — $P = N m \langle v_x^2 \rangle / V$ is exact mechanics, equipartition
$m \langle v_x^2 \rangle = \kB T$ is statistics — giving $P V = N \kB T$ as a theorem within a
model; 11–12 later pry at exactly that seam. Seeds forward: the `fix_temperature` flag is the
canonical/microcanonical distinction in embryo (11), the virial correction previews van der
Waals (14), radiation pressure and freeze-out preview 16, and the honestly documented "no
particle–particle collisions" limitation is the hook 18 lifts.

## 2. Position in the course

- **Requires:** 00 — the dice result that the relative spread of a sample average falls as
  $N^{-1/2}$ (`sampling.py`), units and $\kB$; 01 — equilibrium as a macroscopic state, so "a
  gas at temperature $T$" is meaningful.
- **Feeds:** 05/06 — $P = N \kB T / V$ and equipartition-based $U(T)$, used verbatim by 05's
  isotherms and `internal_energy_change` and by 06's $C_V$/$C_P$ derivations; 11/12 —
  microstate language, ensemble foreshadowing, imposed-vs-derived Maxwell-Boltzmann; 14 — the
  advanced virial equation is the vdW $a$-term's origin; 16 — radiation pressure $P = u/3$,
  equipartition freeze-out; 18 — extends `kinetics.py` with `mean_free_path`/`collision_rate`,
  lifting this module's no-collision failure mode.
- **Explicitly not assumed:** the first law, heat, work (05's); entropy; the Boltzmann factor
  (Maxwell-Boltzmann is *imposed* at $t=0$, flagged as such); particle–particle collisions or
  transport; 02's empirical equation-of-state material.

## 3. Module specification

**As-built summary.** The page carries all mandatory sections as `(04-pressure-<suffix>)=`
labels in contract order plus `advanced` last, objectives OBJ-04-1..5 in ASCII math (steady P
from discrete impacts; derive P = N k_B T / V; temperature = mean energy per particle vs total
internal energy; N^(-1/2) fluctuations; model validity). *Predict* stages the mass-doubling and
"has motion stopped?" traps. *Explore:* two language-neutral MP4s (60 argon atoms beside their
converging running average; fractional traces at N = 20/200/2000), the 7-bullet model-spec box,
a `model-assumption` box stating the model can only *preserve* Maxwell-Boltzmann, never
establish it, and the JupyterLite lab link. *Derive:* one particle → all particles →
equipartition (boxed `theorem` with freeze-out caveat) → boxed $P V = N \kB T$, with an
`approximation` box separating model-theorem from empirical law. *Verify:* four checks mirrored
1:1 in lab Part 4 and `tests/physics` — EOS across eight seeds, machine-exact energy
conservation, equipartition, and the $N^{-1/2}$ law (`numerical-observation` box: chi-square,
exponent $-0.5$, coefficient 1) — closed by an `open-question` box on what simulation cannot
prove. *Transfer:* osmotic/radiation pressure, shot noise, polling; a `definition` box makes
"macroscopic" a statement about $N$. *Advanced:* interparticle collisions leave $P$ unchanged,
momentum flux, virial correction (14), ensemble agreement (11). The lab (EN+HE) runs impacts →
running average, EOS vs $N$/$T$/mass, the $N^{-1/2}$ fit across independently drawn microstates
(`fix_temperature=False`, subtlety explained), the four automated checks, and an ipywidgets
explorer. Quiz bank: Q-04-1..8 (5 MC, 1 numeric, 1 prediction, 1 short-answer), every objective
covered. Problems: 6 objective-tagged, P6 computational. Misconceptions staged:
`equilibrium-motion-stops` (predict Q4 + Q-04-1), `temperature-total-energy` (derive +
Q-04-2/Q-04-7 + problems 2–3), `heat-temperature-same` (tagged on Q-04-5 only — weak; gap 6).

**Gap list**

1. **Movable-piston centrepiece not built.** Brainstorm row 4 promises "particles colliding
   with a movable piston"; the built model has rigid *fixed* walls — a piston is only a static
   box-size parameter (lab Part 5 hands compression off to 05). A moving wall does work on the
   gas — deliberately 05/06 territory — but revisit when 06 builds compression processes.
2. **Equipartition beyond translational DOF deferred.** The `theorem` box states the general
   quadratic-DOF form and points forward to 16 (freeze-out), but no $f$-counting and no explicit
   $U = \tfrac{f}{2} N \kB T$ appears — which plan 05 §2 cites 04 for verbatim. Owed: a forward
   pointer to 06, where $C_V$/$C_P$ make $f$ operational, when 06 is built.
3. **C4a duplicate.** `ideal_gas_pressure` lives in both `kinetics.py` and `paths.py`;
   `test_ideal_gas_law_is_consistent_between_modules` pins them until plan 02 makes `gases.py`
   the canonical home — one-line import refactor at 02 build time.
4. **No pointer to 18's lift.** The no-collision failure mode is documented three times
   (docstring, model-spec box, open-question box) but nowhere says 18 extends `kinetics.py`
   with `mean_free_path`/`collision_rate`; add the forward pointer when 18 is built.
5. **"Molecular speeds" coverage thin** (brainstorm row content): Maxwell-Boltzmann is sampled
   but never plotted as a speed distribution, no $v_{mp}/\bar{v}/v_{rms}$ comparison;
   `rms_speed` and `windowed_pressures` are unused by page and lab.
6. **`heat-temperature-same` staging weak.** Registry says addressed by 04, yet heat barely
   appears; Q-04-5's distractors target fluctuation intuitions. Strengthen or re-point to 05.
7. **Build-time artifacts absent** — no MP4 in the repo (`render_pressure.py` must run) and no
   `content/en/_generated/quiz-04-pressure.md`; plus cosmetic macro drift (raw `k_B`, not
   `\kB`) and no real-experiment counterpart recorded (a syringe/pressure-sensor is cheap).

**Validation gates:** README gate block with `--module 04-pressure`; lab Part 4 re-asserts the
suite's conservation, equipartition, and seed-study EOS checks in-browser.

## 4. Library and tests

- **`src/thermolab` — existing used:** `constants.K_B`; `validation.scaling_exponent`,
  `seed_study` (mean, `standard_error`, `agrees_with`) in lab and tests.
- **`src/thermolab` — introduced: `kinetics.py`** (04 owns; 18 extends). Docstring carries the
  7-bullet model spec; failure modes: high density, low temperature, strong interactions.
  Frozen `GasState(positions, velocities, box, mass)` with `wall_measure`, `kinetic_energy`,
  `kinetic_temperature`; `sample_maxwell_boltzmann(n, T, m, rng, dimension=2)` — i.i.d.
  Gaussian components, variance $\kB T/m$; `initialise_gas(n, box, T, m, rng, remove_drift=True,
  fix_temperature=True)` — sharp-energy (microcanonical-like) vs raw canonical-fluctuating draw;
  frozen `SimulationResult` with `pressure(discard_fraction=0)` — impulse per time per wall
  measure — and `windowed_pressures(n)` (docstring: window scatter is a bounce-cutting artefact,
  not thermal); `simulate(state, dt, n_steps)` — *exact* free flight + specular reflection,
  dt-independent, raises on a double wall crossing; `max_stable_dt(state, safety=0.25)` —
  validity limit, not accuracy knob; `ideal_gas_pressure(n, T, V)` (C4a duplicate);
  `mean_kinetic_energy(T, d=2)`; `rms_speed(T, m, d=2)`.
- **`tests/physics` coverage:** *dimensional* — 2D pressure is force/length, `pressure()` ≡
  impulse/(t·wall); *conservation* — energy exact to ~1e-12, particle number and containment,
  oversized dt refuses, `remove_drift` preserves T; *analytic-limit* — simulated P reproduces
  $N \kB T/V$, $P \propto T$ and $\propto 1/V$, sampled equipartition, `kinetic_temperature`
  round-trip, kinetics/paths EOS pin; *large-N* — fluctuation exponent $-0.5 \pm 0.12$ over
  N = 25–400, coefficient $1/\sqrt{N}$; *convergence* — pressure independent of dt, estimate
  settles onto EOS as the window grows; *seed-independence* — same seed reproduces the gas,
  pressure and MB variance agree across seed families within statistical error.

## 5. Assessment hooks

- **Checkpoint synthesis:** P4 (where "pressure" stops meaning anything — bacterium-scale
  estimate) + P6 (fit the exponent, then state what it does *not* prove) are the exam core.
- **Cross-module:** the $N^{-1/2}$ touchstone recurs in 03 (CLT), 08 (multiplicity peak width)
  and 18; `fix_temperature` is 11's canonical entry ramp; the virial correction opens 14;
  freeze-out is 16's puzzle.
- **Exam themes:** mass-cancellation discipline (Q-04-3 separates right-answer-wrong-reason),
  temperature vs total energy, model-validity adjudication (P5c, Q-04-6), and
  simulation-never-proves epistemics (P6d, lab exit question 2).

## 6. Build order and validation gates

Built — second thermodynamics module live after 01; 02 and 03 slot before it in the
`content/en/myst.yml` TOC at their build time (02 also triggers the C4a dedup, gap 3).
`glossary/terms.yml` already carries pressure, ideal-gas, kinetic-theory, ideal-gas-law,
equipartition, fluctuation, osmotic-/radiation-pressure; `assessment/misconceptions.yml` has
all three ids `assigned_module: 04-pressure`, `status: addressed` (but see gap 6). **HE mirror
complete — verified:** `content/he/thermodynamics/04-pressure{,-problems}.md`,
`notebooks/he/labs/04-pressure.ipynb`, `assessment/quizzes/04-pressure.he.yml`; 04 is absent
from `translation-pending.txt` (only 01 and index remain). Gates: the README per-module command
block with `--module 04-pressure`.

## 7. Deviations from the brainstorm

- **Movable piston → fixed walls:** the exact specular integrator (dt-independent, machine-exact
  energy conservation) needs static walls; a moving piston does work on the gas — deferred to
  05/06 rather than half-taught here (gap 1 tracks the centrepiece).
- **2D, not 3D:** browser/Pyodide budget; library and derivation are dimension-neutral
  (`wall_measure`, volume-as-area), so nothing must be unlearned later.
- **Fluctuations measured across microstates, not within a run:** non-interacting particles
  bounce periodically, so within-run scatter is a windowing artefact; the built module says so
  explicitly — an honesty upgrade over the brainstorm's "shows pressure fluctuations".
- **"Molecular speeds" compressed** to MB sampling plus `rms_speed`; distribution shape and its
  derivation belong to 11/12 (gap 5 tracks a modest local upgrade).
- **Equipartition scoped to translational DOF:** general theorem stated, $f$-counting deferred
  to 06 and freeze-out to 16 (gap 2).
