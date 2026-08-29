# Module 11 — Statistical ensembles — Implementation Plan

> **Brainstorm:** §3 module 11 (+ §5 "Finite heat-bath experiment", §4 step 6 transfer list,
> §6 misconception list). **Module id:** `11-ensembles`.
> **Content path:** `content/en/statistical-mechanics/11-ensembles.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

The module opens on a collision between the subject's two most-quoted pillars. Module 08 boxed
"all accessible microstates of an isolated system are equally probable" as *the* fundamental
assumption; every physicist also quotes "high-energy states are exponentially rare" — the
Boltzmann factor. Stated side by side they sound contradictory: equal probability or
exponential weighting, which is it? The resolution is the whole module: equal probability
applies to the isolated *whole* (system + bath), while the exponential is the *subsystem's
marginal*, and the thing that turns one into the other is nothing but counting the bath's
multiplicity. The centrepiece makes that resolution visible by exact enumeration — no Monte
Carlo, no dynamics: a two-level system (then a small Einstein solid) coupled to a *finite*
Einstein-solid bath, a slider growing `N_bath` while the occupation histogram converges to
`e^{-E/(\kB T)}` and a side panel shows the joint distribution staying flat as the marginal
sharpens into the exponential — the C3 falsifier as the module's main visual.

In the spiral this is where the micro-to-macro program (03 → 08 → 11 → 12) pays its first
macroscopic dividend: 08's postulate plus 09's slope definition `1/T = (\partial S/\partial
U)_{V,N}` produce the canonical distribution in three lines of counting, and 01's Einstein
solids return as the bath (conflict-log C4c payoff — the same `TwoBodyState` mechanics, now
asked a probability question instead of a relaxation question). What the plan deepens over the
brainstorm row: the brainstorm promises the finite-bath experiment "shows how the canonical
ensemble emerges and why an infinite bath is an approximation"; this plan upgrades
"approximation" to a *measured* statement — the next-order term in the bath expansion computed
explicitly and plotted against the exact finite-bath enumeration, a `1/N_bath` error bar on
the infinite-bath idealization.

Seeds planted forward: `Z` is introduced strictly as a normalization constant — its power is
deliberately 12's story; the bath-counting argument reruns with particle exchange in 13 (grand
canonical); Metropolis acceptance ratios in 15 are Boltzmann ratios awaiting this derivation;
17's quantum occupations replace the levels; the advanced ensemble-equivalence sketch seeds
18's energy-fluctuation result. The negative-beta teaser is deferred to 12 per C3.

## 2. Position in the course

- **Requires:** `08-multiplicity` — the fundamental assumption boxed as a postulate,
  `\Omega` counting with `multiplicity.log_multiplicity`, `S = \kB \ln \Omega`, and the
  sharp-peak arithmetic; `09-fundamental-relation` — the slope definition
  `1/T = (\partial S/\partial U)_{V,N}` (beta *is* that slope) and the Einstein-solid
  `S(U,N)` surface; `01-equilibrium` — Einstein-solid mechanics: quanta of size `quantum`,
  oscillator counts, `C = n \kB`, and `equilibrium.TwoBodyState` as the composite's language.
- **Feeds:** `12-partition-functions` — consumes `P_s = e^{-\beta E_s}/Z` and unleashes `Z`
  (`U`, `S`, `F`, `C_V` from it; two-level and oscillator as first workhorses);
  `13-chemical-potential` — the identical bath argument with particle exchange gives
  `e^{-\beta(E_s - \mu N_s)}`; `15-ising` — Metropolis weights justified by Boltzmann ratios;
  `17-quantum-gases` — occupations of single-particle levels; `18` — the advanced
  fluctuation seed.
- **Explicitly not assumed:** partition-function manipulations (`U = -\partial \ln Z /
  \partial \beta`, `F = -\kB T \ln Z` — all 12's); quantum mechanics (quanta are 01's model
  discretization, not QM — real quantization waits for 16/17); maximum-entropy or
  Lagrange-multiplier derivations of the canonical distribution.

## 3. Module specification

- **Identity and scope** — brainstorm §3 row 11: microcanonical and canonical ensembles, the
  Boltzmann distribution, and the finite-bath emergence experiment of §5. Deliberately
  deferred: everything `Z` can do (12), grand canonical (13), negative temperature (12, per
  C3), deriving 04's speed distribution from the Boltzmann factor (back-link only, payoff in
  12/17).
- **Prerequisites** — 08 (postulate, `\Omega`, `S = \kB \ln \Omega`), 09 (`1/T = \partial S /
  \partial U`; Einstein-solid `S(U,N)`), 01 (Einstein-solid quanta and heat capacity); full
  statements in §2.
- **Learning objectives** —
  - `OBJ-11-1` State what the microcanonical and canonical ensembles each describe (isolated
    system at fixed total energy vs subsystem exchanging energy with a bath) and which
    probability rule applies to each: equal weights vs P_s = exp(-E_s/(kB T))/Z.
  - `OBJ-11-2` Derive P(s) proportional to Omega_bath(U_tot - E_s) from the fundamental
    assumption by counting alone, and explain why this form is exact for any bath size.
  - `OBJ-11-3` Derive the Boltzmann distribution P_s = exp(-beta E_s)/Z by expanding
    ln Omega_bath to first order, stating both hypotheses (E_s << U_bath; bath curvature
    negligible) and identifying what breaks when they fail.
  - `OBJ-11-4` Explain how "all accessible microstates are equally probable" and "high-energy
    states are exponentially rare" are both true at once: equal weights govern the isolated
    whole, the exponential governs the subsystem's marginal.
  - `OBJ-11-5` Identify beta = 1/(kB T) as the bath's d(ln Omega)/dU slope from module 09 and
    compute it by finite difference for an Einstein-solid bath, in units of 1/J.
  - `OBJ-11-6` Quantify the finite-bath error: show the leading correction to ln P_s scales
    as 1/N_bath and verify it against exact enumeration, so that "infinite bath" is an
    approximation with a measurable error bar.
  - `OBJ-11-7` Work the two-level system fully: occupations, mean energy
    <E> = eps/(exp(eps/(kB T)) + 1), and the T -> 0 and T -> infinity limits.
  - `OBJ-11-8` Transfer the Boltzmann factor to new contexts: barometric formula
    exp(-m g h/(kB T)), Arrhenius/defect concentrations, molecular excitation ratios.
- **Mathematical background** — already has: binomial and Einstein-solid combinatorics via
  log-gamma (08/09), Taylor expansion with error terms (00/09), partial-derivative slope
  definitions (09). Introduced here: joint vs marginal distributions (marginalizing = summing
  over bath microstates), sup-norm (max-abs) distance between distributions, the log-sum-exp
  shift for safe normalization of `e^{-\beta E_s}`.
- **Physical intuition goals** — (1) rank level populations at sight: two levels split by
  `\Delta E` are occupied in ratio `e^{-\Delta E/(\kB T)}`; (2) predict that growing the bath
  at fixed `T` does not change the histogram's slope, only its fidelity to a pure
  exponential — and that doubling `N_bath` roughly halves the residual; (3) say why "the
  system's temperature" is really the bath's `\partial S/\partial U` slope that the system
  inherits — hence why two different systems on one bath share one beta; (4) predict the
  T → ∞ two-level limit is 50/50 occupancy, never population inversion.
- **Section skeleton seeds** —
  - *puzzle:* the two pillars side by side — 08's boxed equal-probability postulate vs the
    universally quoted exponential rarity of high-energy states. Boxed question: "How can
    both be true of the same matter at the same time?"
  - *predict:* (1) a two-level system sits in equilibrium with a bath — are its two states
    equally likely? [targets `canonical-equal-probability`]; (2) grow the bath at fixed
    temperature — does the occupation histogram change slope, or only get cleaner?; (3) with
    every *joint* microstate equally weighted, which is more probable: system excited or
    system ground — and why?; (4) heat the bath to T → ∞ — does the excited-state population
    approach 1, 1/2, or 0?
  - *explore:* the finite-bath enumerator (controls and renders under Interactive controls
    below); students watch the marginal converge and the joint panel stay flat, and read the
    live sup-norm distance to the Boltzmann curve.
  - *derive:* the six-step route under Core derivations — recap, exact counting result,
    expansion with hypotheses, Boltzmann + `Z` as normalization, the `1/N_bath` honesty
    clause, the two-level system worked fully.
  - *verify:* exact-enumeration marginal vs `boltzmann_distribution` overlay; the log-log
    sup-norm-vs-`N_bath` plot with slope −1 (the `numerical-observation` box); central
    difference beta vs 09's analytic slope.
  - *transfer:* barometric formula; Arrhenius factors and defect concentrations; molecular
    excitation ratios (brainstorm §4's list); back-link to 04's speed distribution as a
    Boltzmann factor in velocity; forward pointer to 12.
  - *quiz:* joint-vs-marginal discrimination, ensemble identification, two-level numerics,
    derivation hypotheses, finite-bath scaling, beta ownership, Boltzmann-factor transfer.
  - *explain:* (1) rewrite "the canonical ensemble means every microstate is equally
    probable" so it is correct, and say precisely what was wrong; (2) explain why
    temperature is a bath property the system inherits; (3) explain why the Boltzmann factor
    needs no collisions or dynamics — what does the counting alone deliver?
  - *advanced (optional, last):* equivalence of ensembles in the thermodynamic limit — the
    system's relative energy fluctuation shrinks as it grows at fixed `T`, so canonical and
    microcanonical predictions merge; plotted, not proved; seeds 18's `Var(E)` result. Safe
    to skip: no core content, and nothing in 12–18's core, depends on it.
- **Core derivations** — (1) *microcanonical recap:* composite (system + bath) isolated at
  `U_{tot}`, rigid non-working wall so `dU = \dbar Q + \dbar \Won` reduces to quanta exchange
  with `\dbar \Won = 0`; every joint microstate equally probable (08's postulate, re-boxed).
  (2) *exact counting:* `P(s) = \Omega_{bath}(U_{tot} - E_s) / \sum_{s'} \Omega_{bath}(U_{tot}
  - E_{s'})` — each system state `s` pairs with `\Omega_{bath}` bath microstates; exact for
  *any* bath size; for the Einstein bath `\Omega_{bath}(N, q) = \binom{q + N - 1}{q}`.
  (3) *expansion:* `\ln \Omega_{bath}(U_{tot} - E_s) = \ln \Omega_{bath}(U_{tot}) - \beta E_s
  + \tfrac{1}{2} E_s^2 \, \partial^2 \ln \Omega_{bath}/\partial U^2 + \dots` with `\beta =
  \partial \ln \Omega_{bath}/\partial U = 1/(\kB T)` by 09's slope definition — boxed as a
  theorem *with its hypotheses*: `E_s \ll U_{bath}` and curvature term `\ll 1`.
  (4) *Boltzmann distribution:* `P_s = e^{-\beta E_s} / Z`, `Z = \sum_s e^{-\beta E_s}` — `Z`
  introduced as the normalization constant only; its power is 12's. (5) *honesty clause:* for
  the Einstein bath in its equipartition regime the neglected term is `E_s^2 / (2 N_{bath}
  (\kB T)^2)` — computed, and plotted against the exact enumeration's deviation; "an infinite
  bath is an approximation with a measurable error bar". (6) *two-level system worked:*
  `p_{exc} = e^{-\beta \epsilon} / (1 + e^{-\beta \epsilon})`, `\langle E \rangle = \epsilon /
  (e^{\beta \epsilon} + 1)`; limits `T \to 0` (all ground) and `T \to \infty` (occupations
  → 1/2, `\langle E \rangle \to \epsilon/2` — no inversion at any positive `T`).
- **Model specification draft** — **System:** a `K`-level small system (two-level with gap
  `\epsilon`, or an Einstein solid of `n_{sys}` oscillators with degeneracies `g(k) =
  \binom{k + n_{sys} - 1}{k}`) sharing `q_{tot}` quanta with an Einstein-solid bath of
  `N_{bath}` oscillators. **Dynamics:** none — every accessible joint microstate is
  enumerated and weighted equally; no time evolution, no sampling. **Boundary:** the
  composite is isolated (`q_{tot}` exactly fixed); the internal wall is rigid and passes
  quanta only. **Ensemble:** exactly microcanonical for the composite; the system's marginal
  is the object that converges to canonical as `N_{bath}` grows. **Ignored:** wall
  interaction energy, unequal quantum sizes, spatial structure, physical exchange rates.
  **Valid when:** shared quantum size and a genuinely isolated composite — the *enumeration*
  is exact at every size; the *canonical form* additionally needs `E_s \ll U_{bath}`.
  **Failure modes:** reading a "temperature" off a tiny bath whose `\ln \Omega` has no smooth
  slope yet; `E_s` comparable to `U_{tot}`, where the marginal visibly departs from the
  exponential — the module plots exactly this departure rather than hiding it.
- **Epistemic classification** — fundamental assumption (equal joint weights):
  `model-assumption` box, recapping 08; `P(s) \propto \Omega_{bath}(U_{tot} - E_s)`:
  `theorem` (exact counting consequence, any bath size); Boltzmann distribution: `theorem`
  boxed *with hypotheses stated* (`E_s \ll U_{bath}`, curvature negligible); `\beta` as bath
  slope: `definition` (inherited from 09); `Z`: `definition` (normalization only); the
  `1/N_{bath}` convergence and error-bar plots: `numerical-observation` boxes (two mandatory:
  sup-norm scaling; predicted vs measured correction term).
- **Misconceptions** — `canonical-equal-probability` ("The canonical ensemble means every
  microstate is equally probable"; registry currently `assigned_module: unassigned`,
  `status: pending`) is re-pointed to this module per C3: falsifying experiment = the
  centrepiece side panel — exact enumeration shows joint system+bath microstates equiprobable
  while the system's own marginal is exponentially weighted; quiz distractor = Q-11-1 (and
  reused in Q-11-2); the registry edit itself happens when the module is built (§6).
  Reinforce, without re-claiming, 08's `subsystem-entropy-increase`: the energy-exchange
  mechanism 08's advanced section promised arrives here. NEW proposed:
  `temperature-of-system-alone` · "Temperature is a property of the system alone even when it
  is in contact with a bath" · falsifier: the same two-level system against equal-energy baths
  of different sizes shows different occupations — beta is the bath's slope, read by
  `beta_of_bath` · distractor in Q-11-6. NEW proposed: `boltzmann-factor-dynamical` · "The
  Boltzmann factor is a dynamical effect of collisions" · falsifier: the centrepiece has no
  dynamics at all — pure counting produces the exponential · distractor in Q-11-4.
- **Glossary terms** — existing keys reused untouched (no collisions; do not re-add):
  `ensemble`, `canonical-ensemble`, `microcanonical-ensemble`, `microcanonical`,
  `boltzmann-distribution`, `partition-function`, `boltzmann-constant`, `thermal-contact`,
  `postulate`. NEW: `heat-bath` · en "heat bath (reservoir)" · he אמבט חום · `he_reject`
  [מאגר חום, רזרבואר]; `boltzmann-factor` · en "Boltzmann factor" · he גורם בולצמן ·
  `he_reject` [פקטור בולצמן]; `two-level-system` · en "two-level system" · he מערכת דו-רמתית
  · `he_reject` [מערכת שתי רמות]; `marginal-distribution` · en "marginal distribution" · he
  התפלגות שולית · `he_reject` [התפלגות מרג'ינלית].
- **Interactive controls and simulations** — Sim 1 (centrepiece), the finite-bath enumerator:
  sliders `N_bath` (2–500 oscillators, log-spaced), quanta per bath oscillator (0.1–10, sets
  `T`), system gap `\epsilon` (1–5 quanta), system selector (two-level | 3-oscillator solid);
  renders the occupation histogram with the Boltzmann overlay, the joint-vs-marginal side
  panel (joint flat, marginal exponential), and a live sup-norm readout. Sim 2, convergence
  tracker: log-log sup-norm distance vs `N_bath` accumulating as the slider sweeps, with a
  slope −1 guide. Sim 3, two-level explorer: `T` slider; occupations and `\langle E \rangle`
  vs `T` with both limit asymptotes drawn.
- **Virtual lab outline** — `notebooks/en/labs/11-ensembles.ipynb`: (1) model setup — model
  spec restated, imports, two-level system + Einstein bath objects; (2) predictions — the
  four predict questions committed and stored; (3) hand enumeration — `N_bath = 3`,
  `q_tot = 3`: list every joint microstate by hand, verify against `enumerate_joint`;
  (4) falsifier as assertion — joint probabilities all equal within float tolerance *and*
  marginal strictly decreasing in `E_s`; (5) bath sweep — `bath_size_sweep` at fixed quanta
  per oscillator, marginals overlaid on the Boltzmann curve; (6) scaling — log-log sup-norm
  distance vs `N_bath`, slope fit via `validation.scaling_exponent`; (7) beta — central
  difference `beta_of_bath` vs the digamma-exact slope, `validation.convergence_study`;
  (8) two-level closed form — occupations and `\langle E \rangle` vs `T`, both limits
  checked; (9) optional coda — barometric formula: import cached pressure–altitude CSV, fit
  the scale height `\kB T/(m g)`; (10) *measurement:* fitted sup-norm scaling exponent
  `alpha = value ± error` (target −1), plus scale height ± error if the coda is run.
- **Real-experiment counterpart** — none practical for the core: no desk-scale apparatus
  enumerates microstates of a system-plus-bath composite. Nearest honest pairing, and
  recommended as an *optional* lab coda: the isothermal atmosphere — the barometric formula
  is a Boltzmann factor in disguise (`P(h) \propto e^{-m g h/(\kB T)}`), with public
  pressure–altitude data (bundled standard-atmosphere CSV) imported into lab cell 9.
- **Media assets** — `media/render/render_ensembles.py`: shot 1, the occupation histogram
  morphing onto the exponential as the bath grows (marginal convergence); shot 2, split
  screen — joint distribution staying flat while the marginal sharpens (the C3 falsifier).
  Language-neutral: numeric axes only, no text burned into frames.
- **Quiz bank outline** — `Q-11-1` (multiple-choice; OBJ-11-4; **distractor:
  `canonical-equal-probability`**): a system equilibrated with a bath — which microstates are
  equally probable? correct: all *joint* system+bath microstates; distractor: all microstates
  of the system. `Q-11-2` (multiple-choice; OBJ-11-1; reuses the same distractor): match
  ensemble ↔ situation ↔ probability rule; trap pairs "canonical" with "equal weights".
  `Q-11-3` (numeric; OBJ-11-7): occupancy ratio for eps = 2 kB T is exp(-2) ~ 0.135.
  `Q-11-4` (multiple-choice; OBJ-11-3; distractor: `boltzmann-factor-dynamical`): which
  hypotheses the derivation needs; distractor "frequent collisions must shuffle the energy".
  `Q-11-5` (prediction/numeric; OBJ-11-6): doubling N_bath at fixed T does what to the
  sup-norm error? halves it. `Q-11-6` (multiple-choice; OBJ-11-5; distractor:
  `temperature-of-system-alone`): what beta = 1/(kB T) is — the bath's d(ln Omega)/dU slope.
  `Q-11-7` (free; OBJ-11-2, OBJ-11-4): explain joint-flat vs marginal-exponential in your own
  words. `Q-11-8` (multiple-choice; OBJ-11-8): which energy enters the barometric exponent
  (m g h). `Q-11-9` (multiple-choice; OBJ-11-7): T -> infinity two-level occupancy -> 1/2;
  distractor "all particles excited". `Q-11-10` (numeric; OBJ-11-2): hand enumeration —
  two-level system (gap 1 quantum), 3-oscillator bath, q_tot = 3: P(excited) = 6/16 = 0.375.
  Every objective covered: 1→Q2; 2→Q7,Q10; 3→Q4; 4→Q1,Q7; 5→Q6; 6→Q5; 7→Q3,Q9; 8→Q8.
- **Problem set outline** — `11-ensembles-problems.md`: P1 analytical (OBJ-11-2) — hand
  enumeration of the two-level + 3-oscillator-bath composite for `q_tot = 1..6`; watch the
  marginal drift toward the exponential. P2 analytical (OBJ-11-3, -6) — carry the bath
  expansion to second order and derive the `E_s^2/(2 N_{bath} (\kB T)^2)` correction; predict
  the sup-norm slope. P3 analytical (OBJ-11-7, -8) — a magnetic dipole in field `B` as a
  two-level system with `\epsilon = 2 \mu B`: magnetization vs `T`, Curie-law limit (seeds
  12's paramagnet). P4 computational (OBJ-11-6) — reproduce `bath_size_sweep`, fit the
  exponent with `validation.scaling_exponent`, compare to P2. P5 analytical/transfer
  (OBJ-11-8) — barometric formula from the Boltzmann factor; estimate the N2 scale height at
  288 K (~8.7 km) and compare with the coda data. P6 challenge (OBJ-11-4, -5) — two
  *different* systems sharing one bath acquire the same beta: prove it from the joint
  enumeration, and explain why temperature is universal across systems on one bath.
- **Runtime budget** — exact enumeration is cheap by construction: one
  `multiplicity.log_multiplicity_array` call per marginal (`K` log-gamma evaluations,
  vectorized, everything in log space with a max-shift before `exp` — no overflow at any
  slider setting). Caps: total quanta `q_tot <= ~10^3`, `N_bath <= ~10^3` oscillators,
  system states `K <= ~50`, sweep over `<= 50` bath sizes — the full lab recomputes in well
  under a second in Pyodide; MP4s are prerendered. Numba is unavailable and unneeded; there
  is no RNG anywhere in this module.
- **Validation gates** — the six per-module commands (README bottom) with
  `--module 11-ensembles`; additionally `check_assessment.py` must see
  `canonical-equal-probability` flipped to `addressed` once the build-time registry edit
  lands (§6).
- **Open questions for the author** — (1) Does explore ship both systems or two-level only?
  Recommend both: two-level carries the derivation; the 3-oscillator solid shows degeneracy
  entering the marginal as `g(E) e^{-\beta E}`. (2) Register one or both NEW misconceptions?
  Recommend both — the centrepiece stages both falsifiers at zero extra cost. (3) Barometric
  coda data source: bundled ISA table vs live fetch — recommend bundled CSV (Pyodide
  offline-safe), source cited in the notebook. (4) Advanced depth — recommend plotting the
  system's relative energy fluctuation shrinking with system size at fixed `T` and stopping
  there, deferring `Var(E) = \kB T^2 C_V` to 18. (5) Joint panel granularity — recommend
  microstate-level flat bars at tiny sizes (readable), per-macrostate counts beyond.

## 4. Library and tests

- **`src/thermolab` — existing used:** `multiplicity.log_multiplicity` /
  `log_multiplicity_array` — the Einstein-solid count is `\Omega(N, q) = \binom{q + N - 1}
  {q}`, i.e. `log_multiplicity(q + N - 1, q)`; no new combinatorics is written.
  `constants.K_B`; `equilibrium.TwoBodyState` / `from_temperatures` (composite setup and the
  01-synthesis problem); `validation.scaling_exponent`, `convergence_study`,
  `relative_error` (lab and tests). Verify may cross-check `beta_of_bath` against 09's
  `fundamental.py` numeric slope helpers (09 builds first; ownership untouched).
- **`src/thermolab` — new: `ensembles.py`** (introduced by 11 per the README ownership table;
  serves 11, 12, 13; single owner, no extenders). Docstring opens with the 7-bullet model
  spec from §3 verbatim. Functions — `enumerate_joint(system_levels, n_bath, total_quanta,
  quantum) -> JointEnumeration`: exact joint-microstate table — per system state `(E_s, g_s)`
  the bath quanta, `ln Omega_bath`, and joint count; `system_levels` as `(energy_quanta,
  degeneracy)` pairs so two-level and small-solid systems share one code path.
  `marginal_occupation(joint) -> ndarray`: the system's normalized marginal, log-sum-exp
  safe. `bath_size_sweep(system_levels, n_bath_range, quanta_per_oscillator, quantum) ->
  BathSweepResult`: marginals vs `N_bath` at fixed energy density (fixed `T`) plus the
  sup-norm distance to the Boltzmann limit for each size. `boltzmann_distribution(levels,
  temperature) -> ndarray`: `P_s = e^{-E_s/(\kB T)}/Z`, shift-normalized.
  `beta_of_bath(n_bath, quanta, quantum) -> float`: central-difference `\partial \ln \Omega /
  \partial U` in 1/J — 09's slope, evaluated on the bath. `TwoLevelSystem(gap)` dataclass:
  `excited_occupation(temperature)`, `mean_energy(temperature)`, limit notes in docstrings.
- **`tests/physics/` additions:** dimensional — `beta_of_bath` returns 1/J (scales inversely
  with `quantum`); `boltzmann_distribution` dimensionless and sums to 1. conservation —
  every `enumerate_joint` row conserves `q_sys + q_bath = q_tot`; joint counts sum to the
  composite's total `\Omega`. analytic-limit — `TwoLevelSystem` occupations match the closed
  form at several `T`, plus both limits; `marginal_occupation` of `enumerate_joint` matches
  `boltzmann_distribution` to tolerance at large `N_bath`; Q-11-10's 6/16 by hand.
  large-N — sup-norm distance vs `N_bath` fits slope −1 via `validation.scaling_exponent`;
  measured deviation tracks the predicted `E_s^2/(2 N_{bath} (\kB T)^2)` term.
  convergence — central-difference `beta_of_bath` approaches the digamma-exact slope with
  second-order error as the bath is scaled up at fixed `T` (`validation.convergence_study`).
  seed-independence — n/a and stated so in the test file: the module is exact enumeration
  with no RNG anywhere; there is nothing for a seed to vary.

## 5. Assessment hooks

Checkpoint synthesis: "one postulate, one derivative, one exponential" — a problem chaining
08's equal-probability postulate through 09's `1/T = \partial S/\partial U` to the Boltzmann
factor in a single argument, each step tagged with its epistemic status. Cross-module
synthesis: revisit 01's two bodies and show body A's energy distribution at joint equilibrium
is canonical with body B as its bath once `n_b \gg n_a` — the C4c Einstein-solid spiral
closing its probability loop. Exam themes: joint-vs-marginal discrimination (the C3
discriminator, Q-11-1's core), hypothesis-tracking on the Boltzmann theorem (when and how it
fails — finite baths, large `E_s`), reading beta off an `S(U)` plot. Feeds: 12's capstone
(reconstructing `U`, `S`, `F`, `C_V` from `Z` — this module hands over `Z` as normalization
plus the two-level sum as its first worked example), 13's grand-canonical rerun of the bath
argument, 15's Metropolis justification, and 18's fluctuation capstone via the advanced seed.

## 6. Build order and validation gates

Build after 09 (the only unbuilt hard dependency — beta needs the slope definition; 01 and 08
are built) and immediately before 12, which consumes `P_s = e^{-\beta E_s}/Z`; 10 sits on the
independent thermodynamic track, so 09 → 10 → 11 → 12 id order also works as build order.
Alongside the build: in `assessment/misconceptions.yml`, re-point `canonical-equal-probability`
from `assigned_module: unassigned` to `11-ensembles` and flip `status: pending → addressed`
(the C3 edit — made at build time, not before, per invariant 7), and add the two proposed NEW
entries per §3 open question 2; in `glossary/terms.yml`, land the four NEW terms with
`he_reject` candidates (existing ensemble-family keys reused untouched). HE-mirror artifact
family: `content/he/statistical-mechanics/11-ensembles{,-problems}.md`,
`notebooks/he/labs/11-ensembles.ipynb`, `assessment/quizzes/11-ensembles.he.yml`, each stamped
with `en_source_hash`; the EN page is listed in `translation-pending.txt` until the HE family
lands. Gates: the six README commands with `--module 11-ensembles`, plus the
`check_assessment.py` re-run confirming the misconception flip.

## 7. Deviations from the brainstorm

- **C3 re-pointing.** `canonical-equal-probability` (registry: unassigned, pending) is
  assigned to this module; falsifier and distractor as specified in §3; the registry edit
  happens at build time. Rationale: the exact joint/marginal enumeration is the only place in
  the course where the wrong model makes a visibly wrong prediction by pure arithmetic.
- **`Z` deliberately left undeveloped.** Introduced strictly as the normalization constant;
  every manipulation of `Z` is 12's story. Rationale: keeps 11 a pure counting module and
  gives 12 a clean, earned payoff.
- **Centrepiece sharpened: enumeration, not simulation.** Brainstorm §5 has the small system
  "exchange energy" with baths of different sizes; the plan replaces sampling with exact
  enumeration. Rationale: the falsifier becomes arithmetic rather than statistics — and it
  powers the proposed `boltzmann-factor-dynamical` falsifier for free.
- **Addition beyond the row: the `1/N_bath` honesty clause.** The next-order expansion term
  computed and plotted against the exact finite-bath deviation, upgrading the brainstorm's
  "an infinite bath is an approximation" to a statement with a measured error bar.
- **Negative-beta teaser deferred to 12** with `negative-t-colder`, per C3; 11 notes only
  that no positive `T` inverts the two-level populations.
