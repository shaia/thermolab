# Module 12 — Partition functions — Implementation Plan

> **Brainstorm:** §3 module 12 (+ §4 step 6 transfer list, §5 "Fluctuation laboratory" seed,
> §6 misconception list). **Module id:** `12-partition-functions`.
> **Content path:** `content/en/statistical-mechanics/12-partition-functions.md`.
> **Status:** planned. Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Module 11 handed students `Z` dismissively: the number you divide by so probabilities sum to
one. This module opens on the scandal that follows: differentiate `\ln Z` once in `\beta`
and out falls `U`; twice, and `C_V` — with the energy fluctuations thrown in; combine, and
`S` and `F` appear. Boxed puzzle: *why does the normalization constant know everything?* The
resolution — `\ln Z`'s derivatives are the moments of the Boltzmann distribution, so the
bookkeeping object is the generating function of the whole equilibrium — is earned by
numerically reconstructing `U(T)`, `S(T)`, `F(T)`, `C_V(T)` from `Z` for a two-level system,
an N-spin paramagnet, and a harmonic oscillator, watching the dots land on the closed forms.

Two spiral debts are paid. First, the free energy: 10 introduced `F = U - TS` by Legendre
construction; here the ensemble *derives* it — `F = -\kB T \ln Z`, proved via consistency
with 10's `S = -(\partial F/\partial T)_{V,N}`, the payoff stated explicitly. Second, C4c:
the oscillator `Z`, at 01's quantum size, is overlaid on *simulated* Einstein-solid data
from `equilibrium.simulate_energy_exchange` — theory meets the course's first simulation,
matching its equipartition temperature map at high `T` and explaining, at low `T`, exactly
the failure mode 01's model spec declared. The paramagnet is this module's named model
system, so the pending `negative-t-colder` misconception lands here per C3: the `S(U)` dome
peaks, `\beta = \partial S/\partial U` crosses zero, and the negative branch beyond is
*hotter* than `T = \infty`, not colder than zero — falsified by heat flow, not by slogan.

Seeds forward: 16's Einstein/Debye solids *are* oscillator partition functions; 13's `\Xi`
generalizes `Z`; 17 swaps levels for occupations; 18 receives `Var(E) = \kB T^2 C_V`, proved
here, exploited there. The ideal-gas `z` is built but advanced-only, where Sackur–Tetrode is
finally derived — closing 09's stated-not-derived loop.

## 2. Position in the course

- **Requires:** `11-ensembles` — `P_s = e^{-\beta E_s}/Z` with hypotheses, `Z` as
  normalization, `\beta = 1/(\kB T)` as the bath's slope, the worked two-level system
  (`ensembles.TwoLevelSystem`, `boltzmann_distribution`); `10-potentials` — `F = U - TS`,
  `S = -(\partial F/\partial T)_{V,N}`; `09-fundamental-relation` — `1/T = (\partial S/
  \partial U)_{V,N}` as a slope (negative `T` is that slope going negative);
  `08-multiplicity` — binomial counting, `S = \kB \ln \Omega` for the exact `S(U)`;
  `01-equilibrium` — the Einstein-solid simulation and its equipartition map
  `T = q \cdot quantum/(n \kB)` (the C4c overlay's data source).
- **Feeds:** `16-radiation-solids` — Einstein/Debye `C_V(T)` from `z_harmonic`, the Planck
  sum as its geometric series re-read; `13-chemical-potential` — `\Xi` generalizes `Z`;
  `17-quantum-gases` — levels → occupations; `18` — `Var(E) = \kB T^2 C_V` quantitatively.
- **Explicitly not assumed:** quantum mechanics beyond "discrete energy levels, taken as
  given inputs" (boxed model assumption — real quantization is 16/17's); grand-canonical
  machinery; maximum-entropy derivations; Monte Carlo (only the C4c overlay inherits
  randomness, from 01's simulation).

## 3. Module specification

- **Identity and scope** — brainstorm §3 row 12: thermodynamic quantities from `Z`; ideal
  gas, paramagnet, harmonic oscillators; centrepiece "numerically reconstruct `U`, `S`, `F`
  and `C_V` from `Z`". Deferred: `N!`/Sackur–Tetrode to this module's *advanced* section;
  Einstein/Debye to 16; `\Xi` to 13; quantitative fluctuations to 18; interacting spins to 15.
- **Prerequisites** — 11 (`Z`, Boltzmann distribution), 10 (`F`, Legendre), 09 (`S(U)`
  slopes), 08 (binomial counting), 01 (Einstein-solid data); specifics in §2.
- **Learning objectives** —
  - `OBJ-12-1` Compute Z = sum_s exp(-E_s/(kB T)) for a discrete-level system and explain why
    the normalization determines everything: derivatives of ln Z are energy moments.
  - `OBJ-12-2` Derive U = -d(ln Z)/d(beta) and apply it, analytically and numerically, to all
    three model systems.
  - `OBJ-12-3` Prove Var(E) = d^2(ln Z)/d(beta)^2 = kB T^2 C_V and show the paramagnet's
    relative energy fluctuation scales as N^(-1/2).
  - `OBJ-12-4` Derive F = -kB T ln Z by consistency with S = -(dF/dT)_V and F = U - TS, and
    classify it as a theorem connecting ensemble to thermodynamics, not a definition.
  - `OBJ-12-5` Reconstruct U(T), S(T), F(T), C_V(T) from Z by controlled numeric
    differentiation; state the stencil's expected order and verify the measured order.
  - `OBJ-12-6` Use Z_N = z^N for independent distinguishable subsystems to work the
    paramagnet: m = N mu tanh(mu B/(kB T)), Curie limit m ~ N mu^2 B/(kB T), saturation.
  - `OBJ-12-7` Read the paramagnet's S(U) dome: beta = dS/dU crosses zero at the peak, is
    negative beyond; predict that an inverted population gives heat to ANY positive-T body —
    negative T is hotter than T = infinity, not colder than absolute zero.
  - `OBJ-12-8` Recover equipartition U -> kB T as the oscillator's high-T limit; predict
    freeze-out (C_V exponentially small) when kB T << hbar*omega.
- **Mathematical background** — has: log-space combinatorics (08), finite differences
  (09/11), Legendre transforms (10). Introduced: the geometric series for `z_harmonic`,
  `tanh`/`cosh`, differentiating a *numerically evaluated* function (truncation-vs-roundoff
  step choice), `\ln Z` as a generating function.
- **Physical intuition goals** — (1) say which levels matter: those within a few `\kB T` of
  the ground state; (2) paramagnet at sight: halve `T` at small `B` — `m` doubles (Curie);
  large `B/T` — saturation; (3) oscillator `C_V` before algebra: `\kB` plateau at high `T`,
  exponentially dead below `\hbar\omega/\kB`; (4) call the heat-flow direction between an
  inverted spin population and a room-temperature body, and say why "colder than 0 K" fails.
- **Section skeleton seeds** —
  - *puzzle:* 11's throwaway line ("Z is just what you divide by") against a live plot where
    `-\partial \ln Z/\partial \beta` traces the mean energy exactly. Boxed: "Why does the
    normalization know everything?"
  - *predict:* (1) which quantity does d(ln Z)/d(beta) give, with what sign? (2) raise `T` at
    fixed `B` — does `m` rise or fall, by what law? (3) keep pumping energy in past `U = 0`:
    does `T` rise, diverge, or go negative — and if the spins then touch a room-temperature
    body, which way does heat flow? [targets `negative-t-colder`] (4) an oscillator at
    `\kB T \gg \hbar\omega` — how much energy does it hold? [04/06 payoff]
  - *explore:* the Z-machine (see Interactive controls): pick a system, drag its level-scale
    slider, watch four reconstructed curves ride their closed forms; a second tab overlays
    the oscillator prediction on 01's simulated data.
  - *derive:* the seven-step route under Core derivations.
  - *verify:* numeric-vs-closed-form residuals for all three systems and the measured stencil
    order ~2 (`numerical-observation` box states the tolerance); the C4c overlay — `T(U)`
    through 01's simulated points within seed error, departing where 01's spec said.
  - *transfer:* brainstorm §4 step 6 with links — two-level → paramagnet (in core); molecular
    excitation ratios (`z_harmonic` populations); atmospheric density (11's barometric coda
    re-read); defect concentrations (Arrhenius as a two-state `Z`); chemical equilibrium
    (`[B]/[A] = e^{-\Delta/(\kB T)}`, matures in 13). Forward doors: 16, 13 (`\Xi`), 18.
  - *quiz:* generating-function insight; `U` from `\ln Z`; theorem-vs-definition status of
    `F`; negative-`T` heat flow; Curie scaling; freeze-out; stencil order; fluctuations.
  - *explain:* (1) convince a skeptic `Z` is not "just" a normalization; (2) rewrite
    "negative temperature means colder than absolute zero" correctly, via the `S(U)` slope;
    (3) is `F = -\kB T \ln Z` a definition or a theorem — what had to be checked?
  - *advanced (optional, last):* the `N!`/Gibbs correction motivated by the extensivity
    failure of `S` without it (08's Gibbs-paradox teaser honored); Sackur–Tetrode derived
    from `z_ideal_gas` (closing 09's loop); negative-`T` lab realization (population
    inversion, NMR, lasers) and thermodynamic-limit caveats. Safe to skip: the core
    negative-`T` argument and 13–18's cores depend on nothing here.
- **Core derivations** — (1) *recap:* `Z = \sum_s e^{-\beta E_s}`, `P_s = e^{-\beta E_s}/Z`
  from 11; `Z` boxed as `definition`. (2) *energy theorem:* `U = \sum_s E_s P_s =
  -\partial \ln Z/\partial \beta`. (3) *heat capacity and fluctuations:* at fixed `V, N`,
  `dU = \dbar Q + \dbar \Won` reduces to `\dbar Q`, so `C_V = (\partial U/\partial T)_{V,N}`;
  `\partial^2 \ln Z/\partial \beta^2 = Var(E)` plus the chain rule give
  `Var(E) = \kB T^2 C_V` — theorem, proof sketched; quantitative use is 18's.
  (4) *free-energy payoff:* `F = -\kB T \ln Z` satisfies `-(\partial F/\partial T)_{V,N} =
  \kB \ln Z + U/T = (U - F)/T = S`, hence `F = U - TS` — the ensemble *derives* 10's
  potential; the Gibbs-entropy bridge `S = -\kB \sum_s P_s \ln P_s` proved in P3.
  (5) *factorization:* `Z_N = z^N` for independent distinguishable subsystems; the
  identical-particle `N!` correction flagged, deferred to advanced. (6) *paramagnet worked
  fully:* levels `\mp \mu B`, `z = 2 \cosh(\mu B/(\kB T))`, `m = N \mu \tanh(\mu B/(\kB T))`;
  Curie limit `m \approx N \mu^2 B/(\kB T)`; saturation `m \to N \mu`; exact `S(U) = \kB \ln
  \binom{N}{n_\uparrow}` by 08's counting — the dome peaks at `U = 0`, `\beta` crosses zero,
  negative beyond; heat flow: total multiplicity rises when the inverted population sheds
  energy to *any* positive-`T` body — negative `T` sits above `T = \infty` (C3 falsifier).
  (7) *oscillator:* `z = e^{-\beta\hbar\omega/2}/(1 - e^{-\beta\hbar\omega})` (geometric
  series), `U = \hbar\omega (1/2 + 1/(e^{\beta\hbar\omega} - 1))`; high `T`: `U \to \kB T`,
  `C_V \to \kB` — equipartition recovered, the 04/06 f-counting payoff; low `T`:
  `C_V \approx \kB (\hbar\omega/(\kB T))^2 e^{-\hbar\omega/(\kB T)}` — the door to 16.
- **Model specification draft** — **System:** discrete-level model systems — two-level with
  gap `\Delta`, `N` independent spins at `\mp \mu B`, a harmonic ladder `E_n = \hbar\omega
  (n + 1/2)` — plus the semiclassical ideal-gas `z` (advanced only). **Dynamics:** none —
  equilibrium averages from the canonical distribution; no time evolution, no sampling.
  **Boundary:** contact with an infinite bath at `T` — 11's idealization, error bar measured
  there. **Ensemble:** canonical, exactly. **Ignored:** interactions between subsystems,
  level shifts beyond the linear Zeeman term, identical-particle exchange (advanced).
  **Valid when:** level spectra are fixed, known inputs; subsystems independent. **Failure
  modes:** interacting spins (15's Ising), quantum indistinguishability at high density or
  low `T` (17), levels that depend on the state variables.
- **Epistemic classification** — `Z`: `definition` (11's). Discrete levels as given inputs:
  `model-assumption` box (mandatory). `U = -\partial \ln Z/\partial \beta`,
  `Var(E) = \kB T^2 C_V`, `F = -\kB T \ln Z`, `Z_N = z^N`, negative-`T` heat flow: `theorem`
  boxes with hypotheses. Equipartition: `approximation` (`\kB T \gg \hbar\omega`).
  Reconstruction tolerance, measured stencil order, C4c overlay: `numerical-observation`
  boxes — the overlay illustrates; the derivation establishes.
- **Misconceptions** — `negative-t-colder` (registry: unassigned, pending) re-pointed here
  per C3 — the paramagnet is this module's named model system. Falsifier: `S(U)` explorer
  plus lab part 6 — `\beta` computed on both sides of the peak, then the inverted population
  is paired with a positive-`T` body and multiplicity bookkeeping shows energy leaving the
  spins: hotter than `T = \infty`, not colder than zero. Distractor: Q-12-4. Registry edit
  at build time (§6). NEW: `dulong-petit-always` · "C_V of any solid is 3N kB at all
  temperatures" · falsifier: the freeze-out curve — `C_V` collapses exponentially below
  `\hbar\omega/\kB` (an observation here; the full Einstein/Debye story is 16's — open
  question 2) · distractor from Dulong–Petit in Q-12-6. NEW: `free-energy-formula-definition`
  · "F = -kB T ln Z is the definition of free energy" · falsifier: epistemic, staged in
  derive step 4 and lab part 4 — `F` was defined in 10 without ensembles; the lab computes
  `-\kB T \ln Z` and `U - TS` independently and finds them equal · distractor in Q-12-3.
- **Glossary terms** — existing keys reused untouched (no collisions): `partition-function`,
  `free-energy`, `boltzmann-distribution`, `heat-capacity`, `equipartition`, `spin`,
  `fluctuation`, `boltzmann-constant`. NEW: `paramagnet` · he פרמגנט · `he_reject`
  [פאראמגנט]; `magnetization` · he מגנוט · `he_reject` [מגנטיזציה]; `curie-law` · he חוק
  קירי · `he_reject` [חוק קורי]; `negative-temperature` · he טמפרטורה שלילית;
  `harmonic-oscillator` · he מתנד הרמוני · `he_reject` [אוסצילטור הרמוני];
  `population-inversion` (advanced) · he היפוך אוכלוסיות.
- **Interactive controls and simulations** — Sim 1 (centrepiece), the Z-machine: system
  selector (two-level | paramagnet | oscillator); sliders `\Delta` (0.1–10 `\kB T_0`),
  `\mu B` (0–5 `\kB T_0`) with `N` (10–10^4, log), `\hbar\omega` (0.1–10 `\kB T_0`); ~10^3
  temperatures; stacked `U/S/F/C_V` panels — reconstruction dots over closed-form lines,
  live max-residual readout. Sim 2, C4c overlay: oscillator-`Z` `T(U)` (zero-point
  subtracted, `\hbar\omega =` 01's `quantum`) over simulated final states; a band marks
  where 01's equipartition map is trusted. Sim 3, `S(U)` explorer: `U` slider; the dome, a
  live tangent whose `\beta` readout flips sign at the peak, a heat-flow arrow against a
  positive-`T` companion. Sim 4: `m(T, B)` map with Curie guide and saturation plateau.
- **Virtual lab outline** — `notebooks/en/labs/12-partition-functions.ipynb`: (1) model spec
  restated, imports; (2) predictions committed; (3) two-level `z` by hand vs `z_two_level`;
  (4) `thermo_from_z` vs closed forms, plus the `F` falsifier as an assertion:
  `-\kB T \ln Z = U - TS` at float tolerance; (5) stencil study — grid refinement via
  `validation.convergence_study`, measured order vs the stated 2; (6) paramagnet —
  `\ln Z_N = N \ln z`; Curie `1/T` fit; fluctuation-vs-`N` slope via
  `validation.scaling_exponent` (target −1/2); `entropy_of_energy` across the band, `\beta`
  on both sides of the peak, falsifier as assertion: pairing the inverted state with a
  positive-`T` body raises total `S` only when the spins *lose* energy; (7) oscillator —
  truncated sum vs closed form (cutoff study), both asymptotes; (8) C4c overlay —
  `simulate_energy_exchange` endpoints under `validation.seed_study`, prediction through the
  point cloud; (9) optional Curie-data coda; (10) *measurement:* fitted stencil order
  `p = value ± error` (target 2), plus a Curie constant ± error if the coda runs.
- **Real-experiment counterpart** — recommended: paramagnetic susceptibility vs temperature
  from published Curie-law measurements (classic public-domain tabulations exist — e.g.
  Onnes-era gadolinium sulfate data), bundled as CSV (offline-safe, source cited), imported
  into lab cell 9 for a `\chi = C/T` fit. Honesty note: a data-import pairing, not a desk
  experiment; if no citable table surfaces at build time, fall back to "none practical" and
  keep the fit as a synthetic-data exercise (open question 3).
- **Media assets** — `media/render/render_partition.py`: shot 1 — four-panel reconstruction,
  dots converging onto closed-form lines as the grid refines; shot 2 — the `S(U)` dome with
  the tangent slope flipping sign past the peak; shot 3 — oscillator `C_V(T)` freeze-out
  rising to the equipartition plateau. Language-neutral, numeric axes, no burned-in text.
- **Quiz bank outline** — `Q-12-1` (multiple-choice; OBJ-12-1, -2): what is -d(ln Z)/d(beta)?
  correct: U; distractors: F; "nothing — Z only normalizes". `Q-12-2` (numeric; OBJ-12-2):
  two-level, Delta = 2 kB T: U = Delta e^-2/(1 + e^-2) ~ 0.12 Delta. `Q-12-3`
  (multiple-choice; OBJ-12-4; distractor: `free-energy-formula-definition`): epistemic
  status of F = -kB T ln Z — a theorem linking ensemble to 10's F; distractor: "a
  definition". `Q-12-4` (multiple-choice; OBJ-12-7; **distractor: `negative-t-colder`**): an
  inverted spin population touches a room-temperature body — heat flows OUT of the spins;
  distractor: "into the spins, because negative T is colder than absolute zero". `Q-12-5`
  (numeric; OBJ-12-6): Curie regime, halve T at fixed small B: m doubles. `Q-12-6`
  (multiple-choice; OBJ-12-8; distractor: `dulong-petit-always`): oscillator C_V at
  kB T << hbar*omega — exponentially small; distractor: "kB per oscillator at every
  temperature". `Q-12-7` (prediction/numeric; OBJ-12-3): N = 10^4 vs 10^6 — relative
  fluctuation shrinks by 10 (N^(-1/2)). `Q-12-8` (multiple-choice; OBJ-12-5): halving a
  second-order stencil's step quarters the truncation error. `Q-12-9` (free; OBJ-12-1, -4):
  why the normalization knows everything, and what had to be *checked* before writing
  F = -kB T ln Z. Coverage: OBJ-1→Q1,Q9; 2→Q1,Q2; 3→Q7; 4→Q3,Q9; 5→Q8; 6→Q5; 7→Q4; 8→Q6.
- **Problem set outline** — P1 analytical (OBJ-12-2) — derive `U = -\partial \ln Z/\partial
  \beta`; recover 11's two-level `\langle E \rangle`. P2 analytical (OBJ-12-3) — prove
  `Var(E) = \kB T^2 C_V`; extract the `N^{-1/2}` law. P3 analytical (OBJ-12-4) — show
  `S = -(\partial F/\partial T)_{V,N}` equals `-\kB \sum_s P_s \ln P_s`; confirm
  `F = U - TS`. P4 analytical (OBJ-12-6, -7) — the full paramagnet: `z`, `m(T,B)`, Curie
  limit, exact `S(U)`, locate `\beta = 0`. P5 computational (OBJ-12-5) — race a one-sided
  difference against the central stencil; measure both orders. P6 computational (OBJ-12-5,
  -8) — extend the C4c overlay across quantum sizes; map where 01's equipartition reading
  fails. P7 challenge (OBJ-12-1) — isomer equilibrium `[B]/[A] = e^{-\Delta/(\kB T)}`;
  defect concentrations (seeds 13). P8 challenge (advanced) — Sackur–Tetrode from
  `z_ideal_gas` with `N!`; show `S` fails extensivity without it (Gibbs-paradox back-link).
- **Runtime budget** — trivial: ~10^3-point temperature grids; the paramagnet is `O(1)` per
  point via factorization (never a `2^N` sum); `S(U)` is one `log_multiplicity_array` call
  over `N + 1` macrostates (`N \le 10^4`); the oscillator's exact sum truncates at
  `n_{max} = \lceil 30 \kB T/(\hbar\omega) \rceil` (tail `< e^{-30}`, cap 10^4 terms). The
  one nontrivial cost is the C4c overlay: `\le 8` seeds × `\le 10^5` steps of 01's
  simulation — seconds in Pyodide, cached. Vectorized NumPy; MP4s prerendered.
- **Validation gates** — the six per-module commands (README bottom) with
  `--module 12-partition-functions`; `check_assessment.py` must see `negative-t-colder`
  flipped to `addressed` once the build-time registry edit lands (§6).
- **Open questions for the author** — (1) Zero-point energy in `z_harmonic`: recommend
  keeping it (shifts `U`, `F` by a constant; `S`, `C_V` untouched — teachable), the C4c
  overlay subtracting it to match 01's quanta. (2) Who registers `dulong-petit-always` — 12
  or 16? Recommend 12 (falsifier and distractor staged here), 16 deepening it; coordinate
  before the registry edit. (3) Curie data: bundled tabulation vs "none practical" —
  recommend bundling if a citable table is found in a day's search, else the synthetic
  fallback; do not block the build on it. (4) Ideal-gas placement: recommend `z_ideal_gas`
  in the library but the page keeping the ideal gas entirely in advanced — `N!` would blur
  the factorization story. (5) `\hbar` is needed but `constants.py` is
  consumed-never-extended — recommend a module-level `H_BAR` in `partition.py` citing the
  ownership rule; revisit if 16/17 agree to promote it.

## 4. Library and tests

- **`src/thermolab` — existing used:** `ensembles.boltzmann_distribution` / `TwoLevelSystem`
  (11's handover); `multiplicity.log_multiplicity_array` (the exact `S(U)`);
  `equilibrium.TwoBodyState` / `from_temperatures` / `simulate_energy_exchange` (C4c
  overlay); `constants.K_B`; `validation.convergence_study`, `scaling_exponent`,
  `seed_study`, `relative_error`.
- **`src/thermolab` — new: `partition.py`** (introduced by 12 per the README ownership
  table; serves 12, 16, 18; single owner, no extenders). Docstring opens with §3's 7-bullet
  model spec verbatim. Functions — `z_two_level(delta, temperature) -> float`:
  `z = 1 + e^{-\Delta/(\kB T)}`, ground state at zero. `z_paramagnet(n_spins, moment, field,
  temperature) -> float`: returns `\ln Z_N = N \ln(2 \cosh(\mu B/(\kB T)))` — log form,
  since `Z_N` overflows at any interesting `N`. `z_harmonic(hbar_omega, temperature,
  n_max=None) -> float`: closed geometric form when `n_max` is `None`, exact truncated sum
  otherwise (cutoff policy in §3) — the pair is the convergence test. `z_ideal_gas(v,
  temperature, mass) -> float`: per-particle semiclassical `z = V/\lambda^3`,
  `\lambda = h/\sqrt{2\pi m \kB T}` (advanced only). `thermo_from_z(z_func,
  temperature_grid) -> ThermoFromZ`: reconstructs `(U, S, F, C_V)` from `\ln Z` alone —
  second-order central differences in `\beta`, per-point step `h = \beta \cdot
  \epsilon_{machine}^{1/3}` (truncation–roundoff optimum, documented), one-sided at
  endpoints; `F = -\kB T \ln Z`, `S = (U - F)/T`. `paramagnet_magnetization(n_spins, moment,
  field, temperature) -> float`: `m = N \mu \tanh(\mu B/(\kB T))` [J/T], Curie and
  saturation limits in the docstring. `entropy_of_energy(n_spins, moment, field, u_grid) ->
  ndarray`: exact paramagnet `S(U)` over the full band by binomial counting — including the
  negative-`\beta` branch past the peak (the C3 falsifier's engine).
- **`tests/physics/` additions:** dimensional — `U`, `F` in J; `S`, `C_V` in J/K; `m` in
  J/T; every `z` (or `\ln Z`) dimensionless. conservation — n/a and stated so in the test
  file: nothing flows in a deterministic equilibrium module; the nearest identity,
  `F = U - TS` across the grid, is filed under analytic-limit. analytic-limit —
  `thermo_from_z` vs closed forms for all three systems (relative error `< 10^{-6}`
  interior); oscillator high-`T` → `U = \kB T`, `C_V = \kB`, and the freeze-out asymptote;
  two-level matches `ensembles.TwoLevelSystem.mean_energy`; Curie and saturation limits;
  `entropy_of_energy` peak at `U = 0`, symmetric negative branch. large-N — relative
  fluctuation `\sqrt{Var(E)}/|U|` fits slope −1/2 via `scaling_exponent`; `\ln Z` additivity
  in `N`. convergence — measured stencil order ≈ 2 under grid refinement
  (`convergence_study`); truncated `z_harmonic` → closed form geometrically in `n_max`.
  seed-independence — n/a for `partition.py` itself (deterministic, no RNG) and stated so;
  the C4c overlay inherits seeds through `equilibrium.simulate_energy_exchange`, handled via
  `validation.seed_study`: the `Z`-predicted equilibrium temperature agrees with the
  simulated final temperature within 3 standard errors across seeds.

## 5. Assessment hooks

This module closes the one-semester core, so its checkpoint is the micro-to-macro capstone:
"from a postulate to a potential" — one problem chaining 08's equal weights → 11's Boltzmann
factor → `Z` → `F = -\kB T \ln Z`, each step tagged with its epistemic status. Cross-module
synthesis: the C4c Einstein-solid triptych — 01's simulated relaxation endpoint, 09's
`S(U,N)` slope, and 12's oscillator `Z` must yield one temperature map by three different
means. Exam themes: theorem-vs-definition discrimination (Q-12-3); negative-`T` heat-flow
reasoning from an `S(U)` sketch; "which levels matter at this `T`" estimation. Feeds: 16's
Einstein/Debye capstone reuses `thermo_from_z` against real heat-capacity data; 13 matures
P7; 18's fluctuation capstone quantifies P2.

## 6. Build order and validation gates

Build immediately after 11 (hard dependency: the Boltzmann distribution and `ensembles.py`);
10 must also precede (the `F` payoff needs the Legendre structure to pay *off*) — id order
09 → 10 → 11 → 12 works as build order and completes the core. Alongside the build: in
`assessment/misconceptions.yml`, re-point `negative-t-colder` from `assigned_module:
unassigned` to `12-partition-functions` and flip `status: pending → addressed` (the C3 edit
— made at build time, not before, per invariant 7), and add the two NEW entries subject to
open question 2; in `glossary/terms.yml`, land the six NEW terms with `he_reject`
candidates. HE-mirror family: `content/he/statistical-mechanics/12-partition-functions
{,-problems}.md`, `notebooks/he/labs/12-partition-functions.ipynb`,
`assessment/quizzes/12-partition-functions.he.yml`, each stamped with `en_source_hash`; the
EN page sits in `translation-pending.txt` until the HE family lands. Gates: the six README
commands with `--module 12-partition-functions`, plus a `check_assessment.py` re-run
confirming the misconception flip.

## 7. Deviations from the brainstorm

- **C3 re-pointing.** `negative-t-colder` (registry: unassigned, pending) is assigned here,
  not to 11 — the paramagnet is this module's named model system and the falsifier needs its
  `S(U)` dome. Falsifier and distractor per §3; registry edit at build time; 11's plan
  records the matching deferral.
- **Ideal gas demoted to advanced; Sackur–Tetrode derived there.** Brainstorm row 12 lists
  the ideal gas as a headline system; the core keeps the three discrete systems and moves it
  — with the `N!`/Gibbs correction — to advanced, closing 09's stated-not-derived loop.
  Rationale: indistinguishability would blur the clean `Z_N = z^N` story.
- **`Var(E) = \kB T^2 C_V` stated and proved here, exploited in 18.** A deliberate seed
  beyond the row: the identity costs three lines once `\ln Z` is in hand; 18 inherits it as
  a known theorem rather than deriving it mid-story.
- **Negative-`T` core kept; its lab-realization story moved advanced.** The `S(U)` argument
  stays in core because it carries the C3 falsifier; population inversion, NMR, and lasers
  go to advanced as culture.
- **Equipartition recovered as a limit.** Addition beyond the row: the oscillator's high-`T`
  limit is staged as the payoff of 04/06's f-counting and the doorway to 16's freeze-out
  story, tying the classical and statistical halves of the course together.
