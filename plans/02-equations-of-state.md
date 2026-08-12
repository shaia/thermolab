# Module 02 — Equations of state — Implementation Plan

> **Brainstorm:** §3 module 2 (+ §5 phase-transition laboratory's vdW-isotherm opening, §6
> misconceptions, §7 accuracy framework). **Module id:** `02-equations-of-state`.
> **Content path:** `content/en/thermodynamics/02-equations-of-state.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Module 01 ended with two bodies agreeing on a temperature; this module asks what else a body at
equilibrium has already agreed on. The through-line: for a simple compressible substance, fixing
any two independent intensive variables fixes *everything else* — every equilibrium state lies
on one two-dimensional surface in (P, v, T) space. That is a claim about the world (a state
postulate), not a theorem, and it is the reason "equation of state" is a meaningful phrase at
all: an EOS is nothing but the shape of that surface.

Two surfaces carry the story. The ideal-gas sheet $P v = \kB T$ is smooth everywhere — and the
smoothness is its failure: a surface with no fold can never liquefy. The van der Waals surface,
built from two microscopic apologies (molecules attract; molecules take up room), folds below a
critical temperature — liquefaction becomes visible geography, a cliff on the surface. The
sub-critical isotherm's up-and-down wiggle is shown, measured against real CO2 data, and
deliberately left *unexplained*: the module closes on it as a cliff-hanger that module 14
resolves with the Maxwell construction.

The plan deepens the brainstorm row three ways: intensive vs extensive is made rigorous (the
doubling test, densities like v = V/N) because module 09's Euler relation consumes extensivity
as a load-bearing property; the ideal gas law is framed strictly as an empirical-law box so that
the already-built 04 reads as its retro-payoff (kinetic theory *derives* what is merely
*summarised* here); and corresponding states plus the compressibility factor Z give the module a
quantitative bridge to published NIST isotherm data instead of a qualitative "real gases differ".

## 2. Position in the course

- **Requires:** `00-orientation` — SI units and the partial-derivative diagnostic (reading a
  slope-at-constant-T off a curve); `01-equilibrium` — state variables exist at equilibrium,
  and the zeroth law makes T a well-defined coordinate to build a surface over.
- **Feeds:** `04-pressure` (retro-link: 04's kinetic model derives the empirical law boxed
  here; this page points forward to it); `06-processes` (its process curves are paths drawn ON
  this surface; its $\Won = -\int P\,\mathrm{d}V$ ledger integrates along them);
  `09-fundamental-relation` (consumes the extensivity definition for the Euler relation);
  `14-coexistence` (resolves the wiggle via the Maxwell construction, reusing `gases.py`
  isotherms); `17-quantum-gases` (quantum corrections where even the "ideal" sheet fails).
- **Explicitly not assumed:** no heat/work/first-law machinery (module 05's — kept out of the
  prose); no microscopic model (04 comes later in teaching order); no probability; no
  coexistence vocabulary beyond the observed plateau — "Maxwell construction", "binodal" and
  "spinodal" are banned words on this page.

## 3. Module specification

- **Identity and scope** — brainstorm row 2 in full: ideal gas, real gases, intensive and
  extensive variables, interactive P-V-T surface. Covered: state postulate, intensive vs
  extensive, ideal EOS as empirical law, vdW EOS with the physical meaning of a and b, critical
  point, reduced variables / corresponding states, compressibility factor. Deferred:
  coexistence, Maxwell construction, Clausius-Clapeyron → 14; kinetic derivation → 04 (built);
  quantum corrections → 17.
- **Prerequisites** — 00: partial derivatives as constrained slopes; 01: equilibrium as the
  precondition for (P, v, T) to describe anything; conventions page: $P V = N \kB T$ form,
  plain-SI-floats library rule.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-02-1`: State the state postulate for a simple compressible substance — fixing two
    independent intensive variables fixes every other equilibrium property — and explain why
    all equilibrium states therefore form a single surface in (P, v, T) space.
  - `OBJ-02-2`: Classify a thermodynamic variable as intensive or extensive by the doubling
    test, form per-particle densities such as v = V/N, and predict which quantities change
    when two identical systems are joined.
  - `OBJ-02-3`: Use the ideal gas law P V = N k_B T to compute any one of P, V, T, N from the
    others, and state its epistemic status: an empirical law of the dilute classical regime,
    not a law of nature.
  - `OBJ-02-4`: Explain the physical origin of the van der Waals constants a (mutual
    attraction lowers pressure by a/v^2) and b (excluded volume shifts v to v - b), and
    compute pressures from P = k_B T/(v - b) - a/v^2.
  - `OBJ-02-5`: Derive the critical point (v_c, T_c, P_c) = (3b, 8a/(27 k_B b), a/(27 b^2))
    from dP/dv = 0 and d^2P/dv^2 = 0 on the critical isotherm, and interpret why no pressure
    liquefies a gas above T_c.
  - `OBJ-02-6`: Rewrite the vdW equation in reduced variables P_r = P/P_c, v_r = v/v_c,
    T_r = T/T_c to obtain the parameter-free law of corresponding states, and use the
    compressibility factor Z = P v/(k_B T) to quantify a real gas's distance from ideality.
- **Mathematical background** — already has: partial derivatives, curve sketching (00). New
  here: reading a function of two variables as a surface; simultaneous vanishing of first and
  second derivatives as "flatness"; nondimensionalisation by scaling out constants.
- **Physical intuition goals** — student can predict, without algebra: (1) joining two
  identical bottles doubles V, N, U but leaves P, T, v unchanged; (2) compressing CO2 at room
  temperature flat-lines the pressure while compressing N2 does not; (3) attraction makes
  measured P *lower* than ideal (Z < 1), excluded volume makes it *higher* (Z > 1), and which
  wins depends on density and temperature; (4) above T_c the gas/liquid distinction loses
  meaning — the fold is gone.
- **Section skeleton seeds** — contract order:
  - *puzzle:* a butane lighter sloshes — liquid at room temperature, made by mere pressure;
    the nitrogen cylinder beside it never liquefies however hard it is squeezed. Boxed
    question: why does one substance's equilibrium surface fold at room temperature while the
    other's cannot — and what is the ideal gas law missing that makes it blind to the
    difference?
  - *predict:* (1) join two identical gas bottles — which of P, V, T, N, U double? (targets
    `doubling-doubles-everything`); (2) slowly compress CO2 at 280 K — does P keep rising,
    plateau, or jump? sketch it; (3) is there a temperature above which no pressure can
    liquefy a gas?; (4) two different gases at the same (T_r, P_r): same Z or gas-dependent?
    (targets `ideal-gas-universal` via its corresponding-states repair).
  - *explore:* the P-V-T surface (page: pre-rendered rotating MP4; lab: live matplotlib 3-D)
    — T slider, a and b sliders morphing ideal → vdW, draggable state point pinned to the
    surface, toggles projecting isotherm/isobar/isochore shadows onto the P-v, P-T, v-T walls.
  - *derive:* state postulate → doubling test and densities → ideal EOS (empirical-law box) →
    vdW corrections (model-assumption box) → critical point by double-zero of $(\partial P/
    \partial v)_T$ → reduced EOS → Z. Full route under core derivations below.
  - *verify:* vdW → ideal as a, b → 0; closed-form critical point vs a numerical
    flatness scan (the `numerical-observation` admonition); Z → 1 in the dilute limit; NIST
    CO2 T_c against the vdW prediction — the honest miss (~4%) is itself the lesson.
  - *transfer:* back to 04 (the empirical box gets its microscopic derivation); forward to 06
    (processes are curves on this surface); 09 (extensivity seed: S, U, V, N all double
    together — the Euler relation will cash this in); 14 (the wiggle, named and dated: "module
    14 resolves this"); 17 (where even Z → 1 fails: quantum degeneracy).
  - *quiz:* state postulate; doubling test; ideal-law computation + validity regime; meaning
    of a and b; critical constants; corresponding states and Z.
  - *explain:* (1) why calling the ideal gas law a "law" can mislead, and what kind of
    statement it actually is; (2) why no pressure liquefies a gas above T_c; (3) why v = V/N
    is intensive although V and N are both extensive; (4) what would be physically wrong with
    a substance whose isotherm had (dP/dv)_T > 0.
  - *advanced (optional, always last):* the virial expansion as the systematic version of
    "real gases differ": Z = 1 + B(T)/v + ..., vdW's B(T) = b - a/(k_B T), Boyle temperature
    T_B = a/(k_B b). Safe-to-skip boundary: nothing in 04, 06, 09, 14 or 17 core depends on
    it; 14 re-derives what it needs.
- **Core derivations** — ordered:
  1. Empirical starting point $P V = N \kB T$, per-particle form $P v = \kB T$ with v = V/N.
  2. vdW model: $P = \dfrac{\kB T}{v - b} - \dfrac{a}{v^2}$ — excluded volume then mean-field
     attraction, each correction argued physically, neither derived (that honesty is the box).
  3. Critical point: $(\partial P/\partial v)_T = 0$ and $(\partial^2 P/\partial v^2)_T = 0$
     simultaneously give $v_c = 3b$, $\kB T_c = \dfrac{8a}{27 b}$, $P_c = \dfrac{a}{27 b^2}$.
  4. Reduced EOS: $P_r = \dfrac{8 T_r}{3 v_r - 1} - \dfrac{3}{v_r^2}$ — a and b scale out
     completely: the law of corresponding states.
  5. Universal critical compressibility $Z_c = \dfrac{P_c v_c}{\kB T_c} = \dfrac{3}{8}$ —
     one number every vdW fluid shares, and a falsifiable prediction (real gases: 0.23–0.31).
- **Model specification draft** — for the surface explorer (page MP4 + lab widget):
  - **System:** a fixed amount N of a simple compressible substance, described entirely by
    the macroscopic coordinates (P, v, T).
  - **Dynamics:** none — every rendered point is an equilibrium state; nothing evolves.
  - **Boundary:** closed; N fixed, v and T set externally, P read off the EOS.
  - **Ensemble:** not applicable — macroscopic thermodynamics.
  - **Ignored:** everything microscopic (a and b enter as fitted constants, not derivations);
    how the system moves between states; the two-phase interior of the fold (the surface is
    drawn from the bare vdW equation).
  - **Valid when:** dilute classical regime (ideal sheet); moderate densities near and above
    T_c (vdW sheet).
  - **Failure modes:** the sub-critical region where the bare vdW isotherm gives
    (dP/dv)_T > 0 — no real substance equilibrates there (module 14 repairs it); cryogenic /
    degenerate regimes (module 17).
- **Epistemic classification** — boxed claims: state postulate → `empirical-law` (prose notes
  its axiom-like role, as with the zeroth law in 01); intensive/extensive → `definition`;
  ideal gas law → `empirical-law` (the module's mandatory admonition, mirrored from the
  conventions page example); vdW EOS → `model-assumption`; critical constants and reduced EOS
  → `theorem` (given the model); Z-data collapse across gases → `numerical-observation`;
  the wiggle's meaning → `open-question` (explicitly deferred to 14).
- **Misconceptions** — none of the existing registry entries belongs here; two NEW entries
  (ids collide with nothing in `assessment/misconceptions.yml`):
  - `ideal-gas-universal` · "The ideal gas law is a law of nature that every gas obeys." ·
    falsifier: NIST CO2 280 K isotherm overlaid on P = k_B T/v — measured pressure plateaus at
    condensation while the ideal curve climbs; Z falls far below 1 · distractor: Q-02-4 option
    computing CO2's pressure from the ideal law inside the plateau.
  - `doubling-doubles-everything` · "Doubling a system doubles every property it has." ·
    falsifier: lab cell joins two identical samples and tabulates P, T unchanged against V, N,
    U doubled · distractor: Q-02-2 option "all of P, V, T and N double".
- **Glossary terms** — already present, reused: `equation-of-state`, `ideal-gas`,
  `ideal-gas-law`, `extensive`, `state-variable`, `virial`, `isothermal`. NEW (key / en /
  suggested he / `he_reject`):
  - `intensive` / intensive / אינטנסיבי / — (completes the existing `extensive`)
  - `state-postulate` / state postulate / הנחת המצב / —
  - `van-der-waals` / van der Waals equation / משוואת ואן דר ואלס / [ון דר ואלס, וואן דר וואלס]
  - `critical-point` / critical point / נקודה קריטית / —
  - `reduced-variables` / reduced variables / משתנים מצומצמים / —
  - `corresponding-states` / law of corresponding states / חוק המצבים המתאימים / —
  - `compressibility-factor` / compressibility factor / מקדם הדחיסות / [פקטור דחיסות]
  - `isotherm` / isotherm / איזותרמה / — (noun; the adjective `isothermal` exists)
  - `condensation` / condensation / עיבוי / —
- **Interactive controls and simulations** — (1) *surface explorer* (lab): v-grid × T-grid
  surface, sliders for T-highlight, a, b (a = b = 0 snaps to ideal); draggable state point;
  shadow toggles per projection plane. (2) *isotherm family explorer*: T slider sweeping
  through T_c with the vdW and ideal curves overlaid; below T_c the wiggle region is
  auto-highlighted. (3) *Z explorer*: Z vs P at selectable T_r for CO2/N2/Ar data plus the
  vdW prediction — the corresponding-states collapse seen live.
- **Virtual lab outline** — `notebooks/en/labs/02-equations-of-state.ipynb`: (1) setup —
  import `gases`, constants; (2) prediction cells (commit before running); (3) ideal surface
  via `pvt_surface`, live matplotlib 3-D with slider redraw; (4) doubling experiment — join
  two identical samples, print the intensive/extensive table (falsifies
  `doubling-doubles-everything`); (5) `isotherm_family` across T_c, spot the wiggle; (6)
  measure T_c for CO2's fitted a, b by scanning isotherms for flatness (min over v of
  |dP/dv| via finite differences), compare to `vdw_critical_point` and to NIST; (7) import
  the shipped NIST CO2 CSV, compute Z along the 280 K isotherm, overlay ideal vs vdW
  (falsifies `ideal-gas-universal`); (8) reduced-variable collapse of CO2/N2/Ar; (9)
  *measurement:* T_c(CO2) = value ± error from the flatness scan, quoted against 304.13 K.
- **Real-experiment counterpart** — decision: **published CO2 isotherm data from the NIST
  Chemistry WebBook** (isothermal property tables, 280–320 K, spanning T_c = 304.13 K),
  shipped as a small CSV under `data/` and loaded with NumPy in the lab; CO2 over N2 because
  its critical point sits near room temperature and its condensation plateau is dramatic at
  pedagogically friendly pressures (Andrews' historic experiment). Optional bench pairing: a
  sealed syringe of butane liquefying under thumb pressure — zero-cost, no data import.
- **Media assets** — `media/render/render_gases.py`, language-neutral (no burned-in text):
  `gases-surface.mp4` (rotating P-v-T surface morphing ideal → vdW, fold appearing);
  `gases-isotherms.mp4` (isotherm family swept through T_c, wiggle emerging below it);
  `gases-shadows.mp4` (state point sliding on the surface while its three wall projections
  trace isotherm/isobar/isochore).
- **Quiz bank outline** — every objective covered at least once; ASCII math:
  - `Q-02-1` (multiple-choice, OBJ-02-1): why two variables suffice; distractor "P, v and T
    are three independent knobs".
  - `Q-02-2` (multiple-choice, OBJ-02-2): join two identical bottles — which quantities
    double? distractor from `doubling-doubles-everything`.
  - `Q-02-3` (numeric, OBJ-02-3): N in a 30 m^3 room at 101325 Pa, 293 K from P V = N k_B T.
  - `Q-02-4` (multiple-choice, OBJ-02-3): CO2 compressed at 280 K — measured P vs ideal
    prediction; distractor from `ideal-gas-universal`.
  - `Q-02-5` (numeric, OBJ-02-4): vdW pressure for CO2 at given (v, T); sign and size of the
    deviation from ideal, and which constant dominates it.
  - `Q-02-6` (numeric, OBJ-02-5): T_c and P_c from given a, b via T_c = 8a/(27 k_B b),
    P_c = a/(27 b^2); compare to the NIST value.
  - `Q-02-7` (multiple-choice, OBJ-02-6): two different gases at equal (T_r, P_r) — same Z?
    distractor "Z depends on the gas's chemistry, so never".
  - `Q-02-8` (free, OBJ-02-1 + OBJ-02-4): explain why the real surface folds where the ideal
    one cannot, naming the physical role of a and b.
- **Problem set outline** — `02-equations-of-state-problems.md`: *analytical* — derive the
  critical constants (OBJ-02-5); show Z_c = 3/8 is gas-independent and compare to tabulated
  real values (OBJ-02-6); derive the reduced EOS (OBJ-02-6). *Computational* — fit a, b from
  NIST critical data via a = 27 (k_B T_c)^2/(64 P_c), b = k_B T_c/(8 P_c), predict the 280 K
  isotherm, quantify the miss (OBJ-02-3/4). *Challenge* — estimate b from a molecular
  diameter and compare to the fit; dimensional analysis of a and b (OBJ-02-2/4).
- **Runtime budget** — everything deterministic, vectorized NumPy only (no Numba in Pyodide):
  surface grid ≤ 100 × 100 (10^4 EOS evaluations, milliseconds); isotherm family 12 × 400;
  the lab's flatness scan 200 temperatures × 2000-point v-grid = 4 × 10^5 evaluations, well
  under a second. The bottleneck is matplotlib 3-D redraw, not physics: redraw on slider
  *release*, never on drag. Target: every cell interactive in-browser within seconds.
- **Validation gates** — the six README commands with `--module 02-equations-of-state`, plus:
  a physics test asserting `kinetics.ideal_gas_pressure is gases.ideal_gas_pressure` (and the
  `paths` pair) so the C4a dedup cannot silently regress.
- **Open questions for the author** —
  1. 3-D delivery in MyST + JupyterLite (the pinned question): options are a plotly/pythreejs
     embed (heavy payload, fragile offline), a bespoke JS widget (high cost), or split
     delivery. **Recommend:** pre-rendered rotating-surface MP4 on the page
     (`media/render`), live matplotlib 3-D with ipywidgets sliders in the lab notebook.
  2. Student-facing units for a and b: per-particle (J m^3 and m^3, matching the course's
     N k_B T convention) vs molar (Pa m^6 mol^-2). **Recommend:** per-particle throughout,
     with the molar conversion shown once where the NIST data is imported.
  3. Include the virial/Boyle-temperature material? **Recommend:** yes, but strictly inside
     the advanced section (`virial` is already in the glossary; 18 touches transport virials).
  4. Which gases in the corresponding-states overlay? **Recommend:** CO2 + N2 + Ar — data
     are free on NIST, and the trio spans polar-ish, diatomic and noble.

## 4. Library and tests

- **`src/thermolab` — existing used:** `constants.py` (`K_B`, `N_A`, `R_GAS`) only; the
  module is deliberately independent of the simulation files.
- **`src/thermolab` — new:** `gases.py` (ownership table: introduced by 02, extended by
  none; serves 02, 04, 06, 14, 17). Docstring header, 7 bullets in fixed order — System: a
  fixed amount of gas described by macroscopic coordinates (P, v, T) alone / Dynamics: none —
  every function evaluates equilibrium states / Boundary: closed, N fixed / Ensemble: not
  applicable — macroscopic thermodynamics / Ignored: all microscopic detail; a and b are
  phenomenological constants / Valid when: dilute classical (ideal) and moderate-density
  near-critical (vdW) regimes / Failure modes: the sub-critical (dP/dv)_T > 0 wiggle region
  (module 14) and quantum-degenerate regimes (module 17). Functions:
  - `ideal_gas_pressure(n_particles: int, temperature: float, volume: float) -> float` —
    P = N k_B T / V; canonical home (C4a: `kinetics`/`paths` re-import this).
  - `ideal_gas_temperature(n_particles: int, pressure: float, volume: float) -> float` —
    T = P V / (N k_B); moves here from `paths.py`.
  - `van_der_waals_pressure(v, temperature, a, b) -> np.ndarray` — P = k_B T/(v-b) - a/v^2,
    per-particle v; vectorized over v and T; raises for any v <= b.
  - `vdw_critical_point(a: float, b: float) -> tuple[float, float, float]` — closed form
    (v_c, T_c, P_c) = (3b, 8a/(27 k_B b), a/(27 b^2)).
  - `vdw_constants_from_critical(t_c: float, p_c: float) -> tuple[float, float]` — inverts
    the above; the NIST-data import path for fitting a and b.
  - `reduced_variables(pressure, v, temperature, a, b) -> tuple` — (P_r, v_r, T_r), each
    scaled by its critical value; `vdw_pressure_reduced(v_r, T_r) -> np.ndarray` — the
    parameter-free 8 T_r/(3 v_r - 1) - 3/v_r^2.
  - `compressibility_factor(pressure, v, temperature) -> np.ndarray` — Z = P v/(k_B T);
    `isotherm_family(v_grid, temperatures, a=0.0, b=0.0) -> np.ndarray` — (n_T, n_v)
    pressure array, a = b = 0 giving the ideal family; `pvt_surface(v_grid, t_grid, a=0.0,
    b=0.0) -> tuple[np.ndarray, ...]` — meshgrid (V, T, P) triple for surface rendering.
- **`tests/physics/` additions** (six categories):
  - *dimensional:* `van_der_waals_pressure` returns Pa under `pint` re-evaluation with a in
    J m^3, b in m^3; `vdw_critical_point` returns (m^3, K, Pa); `compressibility_factor` is
    dimensionless.
  - *conservation:* no dynamics — discharged by invariance: P ↔ T roundtrip
    (`ideal_gas_temperature(ideal_gas_pressure(...))` is exact) and reduced ↔ absolute
    roundtrip through `reduced_variables`.
  - *analytic-limit:* `van_der_waals_pressure(v, T, 0, 0)` equals the ideal law exactly;
    Z → 1 as v → ∞; `vdw_critical_point` matches the closed form; Z_c == 3/8;
    `vdw_pressure_reduced(1, 1) == 1`; alias test `kinetics.ideal_gas_pressure is
    gases.ideal_gas_pressure` (and the `paths` pair).
  - *large-N:* intensivity as code — `ideal_gas_pressure(2N, T, 2V) == ideal_gas_pressure(N,
    T, V)` exactly (the doubling test, mechanised).
  - *convergence:* central-difference dP/dv and d^2P/dv^2 at (v_c, T_c) tend to zero at the
    stencil's expected order as h shrinks.
  - *seed-independence:* n/a — every function is deterministic; no RNG anywhere in the file.

## 5. Assessment hooks

Checkpoint synthesis (belongs to the module, not one section): (a) 01 + 02 — two rigid gas
bottles at different temperatures are joined thermally: final T from 01's weighted average,
final pressures from the EOS; (b) data verdict — given one NIST CO2 state row, compute Z and
rule which model (ideal / vdW / neither) is adequate, with the tolerance stated first. Exam
themes: critical-constant derivation; classify-the-claim (epistemic label per statement);
doubling-test classification under time pressure. Feeds forward: 06's process-ledger problems
draw their curves on this module's surface; 14's Maxwell-construction capstone reopens the
saved wiggle isotherm from `gases.py` unchanged; 12's ideal-gas partition function closes the
loop on the empirical box a second time, microscopically.

## 6. Build order and validation gates

First planned module to build: teaching order slots it between the built 01 and built 04 (TOC
insertion by id in `content/en/myst.yml`), and `gases.py` unblocks 06, 14 and 17. Lands
together in one change: the page + problems + lab + quiz bank; the two NEW misconception
entries (status `addressed`) in `assessment/misconceptions.yml`; the nine NEW glossary keys in
`glossary/terms.yml` with `he_reject` candidates; the C4a refactor — delete the
`ideal_gas_pressure` body from `kinetics.py` and the `ideal_gas_pressure`/
`ideal_gas_temperature` bodies from `paths.py`, replacing each with a one-line import from
`gases`, guarded by the alias test. HE mirror family (`.he.yml` quiz, HE page/problems/lab
with `en_source_hash` stamps) follows; until it lands the page is listed in
`translation-pending.txt`. Gates: the six README commands with `--module
02-equations-of-state`.

## 7. Deviations from the brainstorm

- **vdW pulled forward from module 14 (re-scope).** Brainstorm row 14 owns the "van der Waals
  fluid"; row 2 says only "real gases". This plan gives 02 the vdW EOS, critical point,
  reduced variables and Z — 14 keeps coexistence, Maxwell construction and Clausius-Clapeyron.
  Rationale: the fold *is* the real-gas story, and 14 needs a fluid it can already compute.
- **C4a dedup (README conflict log).** `gases.py` becomes the canonical home of
  `ideal_gas_pressure` / `ideal_gas_temperature`; `kinetics.py` and `paths.py` switch to
  one-line imports when this module is built, with an alias test pinning the identity.
- **Maxwell construction strictly deferred.** The sub-critical wiggle is shown and measured
  but left unexplained by design — an `open-question` box and a transfer seed point to 14.
  Rationale: resolving it needs entropy and free-energy machinery from 07–10.
- **Page centrepiece downgraded from live 3-D to MP4 + lab notebook (addition/decision).**
  The brainstorm's "interactive P-V-T surface" is split: pre-rendered rotating surface on the
  page, live matplotlib 3-D in JupyterLite — pending the §3 open question, this keeps the
  page light and offline-safe.
- **Intensive/extensive rigor beyond the brainstorm row (addition).** The doubling test is
  made a boxed definition plus a lab experiment because module 09's Euler relation depends on
  extensivity being load-bearing, not decorative.
