# Module 10 — Thermodynamic potentials — Implementation Plan

> **Brainstorm:** §3 module 10 (+ §5 "Maxwell-relation explorer", §7 accuracy framework).
> **Module id:** `10-potentials`.
> **Content path:** `content/en/thermodynamics/10-potentials.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Chemists tabulate `G`, engineers tabulate `H`, physicists reach for `F` — and none of them is
wrong. The module's through-line is that the potentials are not rival energies but answers to
differently constrained questions: one fundamental relation, `S(U,V,N)` from 09, viewed through
whichever window the laboratory actually holds fixed. The showpiece consequence is the module's
bonus hook: a Maxwell relation, `(\partial S/\partial V)_T = (\partial P/\partial T)_V`, whose
right side is a pressure gauge and a thermometer — entropy changes, the least tangible quantity
in the course, measured with the two most ordinary instruments in the building.

In the spiral (brainstorm §2, steps 7–8) this is where free energy appears *thermodynamically*;
its canonical-ensemble derivation `F = -\kB T \ln Z` deliberately waits for 11/12, and the page
says so out loud. Two debts from earlier modules are paid here: 05's exact-versus-inexact
machinery (and its advanced section, which promised this module would be "less mysterious")
pays off as the Maxwell relations — equality of mixed partials, checked numerically with the
very `forms.py` functions built there; and 07's second law is spent on the derive spine, the
honest composite-system argument that total entropy maximization at fixed `T,V` *is* system-`F`
minimization. Everything in the module is a derivative of 09's entropy surface; nothing new is
postulated.

The plan enhances the brainstorm row in four ways. The Legendre transform is taught
*geometrically* first — envelope of tangent lines, information preserved exactly because 09's
concavity makes slope and point interchangeable — with the algebraic recipe second. The
brainstorm §5 mandate is honored literally: students verify cross-derivatives numerically, which
"is much more useful than memorizing a thermodynamic square" — the square survives only as an
advanced-section curiosity, never as the method. A cheap, classic, quantitative real experiment
(rubber-band thermodynamics) makes the Maxwell showpiece tactile. And an advanced non-convex
teaser — Legendre *loses* information when convexity fails — plants 14's coexistence seed.

## 2. Position in the course

- **Requires:** `09-fundamental-relation` — `S(U,V,N)` and `dU = T dS - P dV + \mu dN`, the
  slope identifications `1/T = (\partial S/\partial U)_{V,N}`, the Euler relation
  `U = TS - PV + \mu N`, and concavity/stability (the exact property Legendre invertibility
  needs); `07-second-law` — `dS_tot >= 0` for an isolated composite and the reservoir
  bookkeeping `dS_r = -\dbar Q / T_r` (per conflict-log C2); `05-work-paths` — exact vs inexact
  differentials, the mixed-partials test, and `forms.py` itself; `06-processes` — the isobaric
  ledger and `C_P`, so `\Delta H = Q_P` lands as a callback, plus `C_P = (\partial H/\partial T)_P`.
- **Feeds:** `11-ensembles`/`12-partition-functions` — the `F = -\kB T \ln Z` seed planted in
  transfer is redeemed there, and 12's capstone checks canonical `F` against this module's
  thermodynamic `F` for the same models (Einstein-solid spiral, C4c); `13-chemical-potential` —
  `\mu = (\partial G/\partial N)_{T,P}` and `G = \mu N` are its opening lines; `14-coexistence`
  — `G` governs coexistence, and the advanced non-convex demo is the Maxwell-construction seed.
- **Explicitly not assumed:** partition functions, ensembles, the Boltzmann factor (11/12's);
  any statistical derivation of `F`; particle-exchange equilibria (`\mu` appears in
  differentials but is never varied — 13's); phase mixtures or non-concave relations in the
  core sections (14's).

## 3. Module specification

- **Identity and scope** — brainstorm row 10 in full: enthalpy, Helmholtz and Gibbs free
  energies, Legendre transforms, Maxwell relations; centrepiece = interactive natural-variables
  map *plus* the §5 Maxwell-relation explorer. Deferred: `F` from `Z` → 11/12; varying `N` and
  `\mu` physics → 13; coexistence / common tangent → 14; thermodynamic square → advanced
  curiosity only.
- **Prerequisites** — 09's `S(U,V,N)` + Euler + concavity; 07's second law with reservoir
  bookkeeping; 05's exactness test (`forms.mixed_partials_gap`); 06's `Q_P` ledger and `C_P`.
- **Learning objectives** — (frontmatter-verbatim, ASCII math)
  - `OBJ-10-1` Construct H = U + PV, F = U - TS, G = U - TS + PV as Legendre transforms of
    U(S,V,N) and write each differential (dH = T dS + V dP + mu dN; dF = -S dT - P dV + mu dN;
    dG = -S dT + V dP + mu dN).
  - `OBJ-10-2` Identify the natural variables of U, H, F, G and select the potential matched to
    a stated constraint: isolated -> S max; fixed T,V -> F min; fixed T,P -> G min;
    throttling -> H conserved.
  - `OBJ-10-3` Derive dF <= 0 at fixed T,V (and dG <= 0 at fixed T,P) from the second law
    applied to system + reservoir, and account for what pays when U rises while F falls.
  - `OBJ-10-4` State the four Maxwell relations as equalities of mixed partials of U, H, F, G
    and verify one numerically as a cross-derivative gap.
  - `OBJ-10-5` Use (dS/dV)_T = (dP/dT)_V to obtain an entropy change from pressure-gauge and
    thermometer data, e.g. Delta S = integral of (dP/dT)_V dV at fixed T.
  - `OBJ-10-6` Explain geometrically why the Legendre transform of a strictly convex (concave)
    function preserves all information, via the envelope of tangent lines.
  - `OBJ-10-7` Apply Delta H = Q_P to isobaric heating and throttling bookkeeping, and state
    precisely when Delta H = Q fails (non-PV work present, or P not constant).
- **Mathematical background** — already has: partial derivatives with held-variable subscripts,
  exact differentials and the mixed-partials test (05), convexity/concavity and stability (09).
  Introduced here: the Legendre transform (geometric, then algebraic), and the discipline of
  "a function *of which variables*" — why `U(T,V)` is a different (lesser) object than `U(S,V)`.
- **Physical intuition goals** — student can predict without algebra: (a) given a stated lab
  constraint, which potential is extremal and which way it moves; (b) that a gas in contact
  with a bath can *raise* its energy spontaneously — the bath pays `T \Delta S`, and `F` still
  falls; (c) from "a quickly stretched rubber band warms my lip", that a loaded band heated
  with a hair-dryer must *contract*; (d) that a throttled gas conserves `H`, not `U` or `T`.
- **Section skeleton seeds** —
  - *puzzle:* three communities, three tables — chemists publish `G`, engineers `H`, physicists
    `F`. Boxed question: are they disagreeing about the physics, or answering differently
    constrained questions? Hook: by the end, a pressure gauge and a thermometer will measure an
    entropy change.
  - *predict:* (1) gas + bath at fixed `T,V`, internal constraint released — must the gas's
    energy decrease? (targets `systems-minimize-energy`); (2) two samples in identical states,
    same `U` — can their usefulness for extracting work differ? (targets
    `free-energy-stored-energy`); (3) stretch a rubber band fast and touch it to your lip —
    warmer or cooler? then: heated under a fixed load, does it stretch or contract?; (4) is
    `\Delta H = Q` for every process, or under conditions? (targets `enthalpy-heat-content`).
  - *explore:* the natural-variables map (constraint selector: isolated / fixed `T,V` / fixed
    `T,P` / throttling; live ledger of `U`, `TS`, `PV`, `H`, `F`, `G`; which quantity is
    stationary) and the Maxwell explorer (manipulate a model fundamental relation, pick a
    potential and a variable pair, watch the numerical cross-derivative gap) — details below.
  - *derive:* geometric Legendre → algebraic recipe → the three definitions with differentials
    (boxed) → four Maxwell relations (theorem boxes) → composite-system minimization from the
    second law → `\Delta H = Q_P` and throttling. Route detail under core derivations.
  - *verify:* numeric Legendre vs closed-form `F` for the ideal gas and Einstein solid;
    `maxwell_check` gap → 0 under refinement (the `numerical-observation` admonition);
    minimization trace with `F` monotone down while `U` rises and `S_tot` climbs.
  - *transfer:* forward — `F = -\kB T \ln Z` named as 11/12's destination (seed, not result);
    `\mu = (\partial G/\partial N)_{T,P}` → 13; `G` and phase coexistence → 14. Backward —
    05's inexact differentials as the reason Maxwell relations are non-trivial; 08's
    entropic-force teaser redeemed by rubber-band elasticity. Sideways — `\Delta H` tables and
    Hess-law bookkeeping in chemistry as institutionalized `Q_P`.
  - *quiz:* constraint-to-potential matching; the F-vs-U minimization trap; Maxwell relation
    identification and use; entropy from `P(T)` data; `\Delta H = Q_P` validity; Legendre
    information preservation.
  - *explain:* (1) tell a chemist why physicists tabulate `F` while chemists tabulate `G`,
    without calling either wrong; (2) what exactly is "free" in free energy, and what is not;
    (3) why measuring how pressure rises with temperature at fixed volume tells you how entropy
    grows with volume, in words a lab technician would accept.
  - *advanced (last, safe to skip):* the thermodynamic square as a historical mnemonic
    curiosity (explicitly *not* the course's method — the verifier is); Massieu functions
    (Legendre of `S` rather than `U`); the non-convex information-loss demo — Legendre a
    dented `F(V)`, watch the transform go multivalued and forget the dent — flagged as 14's
    opening problem. No core content depends on any of it.
- **Core derivations** — ordered:
  1. *Legendre, geometrically.* For strictly convex `f(x)`: each tangent has slope
     `p = df/dx` and intercept `g(p) = f(x) - p x`; the tangent family envelopes the curve, so
     `g(p)` carries the same information as `f(x)`. 09's concavity is exactly what makes
     `x \leftrightarrow p` one-to-one. Algebraic recipe second: trade a variable for its
     conjugate slope by subtracting their product. Plain substitution `U(T,V)` loses the
     integration constant family — shown, not asserted.
  2. *The three potentials.* From 09's `dU = T dS - P dV + \mu dN` (the quasistatic reading of
     `dU = \dbar Q + \dbar \Won`, with `\dbar Q = T dS` and `\dbar \Won = -P dV + \mu dN`):
     `H = U + PV` gives `dH = T dS + V dP + \mu dN`; `F = U - TS` gives
     `dF = -S dT - P dV + \mu dN`; `G = U - TS + PV` gives `dG = -S dT + V dP + \mu dN` — each
     boxed as a definition. Euler (09) gives `G = \mu N` in one line.
  3. *Maxwell relations as theorems.* Each potential is a state function, so its differential
     is exact and 05's test applies. From `U`:
     `(\partial T/\partial V)_S = -(\partial P/\partial S)_V`; from `H`:
     `(\partial T/\partial P)_S = (\partial V/\partial S)_P`; from `F`:
     `(\partial S/\partial V)_T = (\partial P/\partial T)_V`; from `G`:
     `(\partial S/\partial P)_T = -(\partial V/\partial T)_P`. The `F` relation is the
     showpiece: its right side is directly measurable.
  4. *Minimization from the second law* (the derive spine, done honestly). Composite = system +
     ideal reservoir at `T_r`; 07 gives `dS_tot = dS + dS_r >= 0` with `dS_r = -\dbar Q / T_r`.
     At fixed `T = T_r`, `V`, `N`: `\dbar Q = dU`, so `dS_tot = -(dU - T dS)/T = -dF/T >= 0`,
     hence `dF <= 0` with equality at equilibrium — total entropy max ⇔ system `F` min. Same
     argument at fixed `T,P` with `\dbar Q = dU + P dV = dH` gives `dG <= 0`.
  5. *Enthalpy as bookkeeper.* Constant `P`, no non-PV work: `Q_P = \Delta H` (from
     `\Delta U = Q_P - P \Delta V`). Throttling: `U_2 + P_2 V_2 = U_1 + P_1 V_1`, so `H` is
     conserved across the plug. Honest boundary: one volt of electrical work breaks
     `\Delta H = Q` instantly.
- **Model specification draft** — (page simulation: natural-variables map / minimization demo)
  - **System:** a model substance described by a smooth, strictly concave fundamental relation
    `S(U,V,N)` from `fundamental.py` (Sackur–Tetrode ideal gas or Einstein solid), coupled to
    an ideal reservoir at `T_r` (and `P_r` in the `G` pane).
  - **Dynamics:** quasistatic release of an internal constraint; the composite sits on its
    equilibrium surface at every step.
  - **Boundary:** diathermal wall to the reservoir; frictionless piston at `P_r` where present;
    insulated walls in the isolated pane.
  - **Ensemble:** not applicable — the reservoir is a thermodynamic idealization; its
    statistical version (finite bath → Boltzmann) is 11's opening.
  - **Ignored:** fluctuations, finite reservoir size, relaxation dynamics, non-PV work.
  - **Valid when:** reservoir ≫ system; `S` smooth and strictly concave in `(U,V)`.
  - **Failure modes:** non-concave relations (Legendre goes multivalued — see advanced and 14);
    small baths (11); fast processes with no equilibrium path.
- **Epistemic classification** — `definition`: `H`, `F`, `G` with their differentials, natural
  variables, the Legendre transform (boxed, three boxes). `theorem`: the four Maxwell relations
  (boxed individually — 05's payoff); `dF <= 0` at fixed `T,V` and `dG <= 0` at fixed `T,P`
  *given* the second law; tangent-envelope invertibility for strictly convex `f`.
  `model-assumption`: ideal reservoir, quasistatic coupling (boxed once in explore).
  `approximation`: finite-`h` central differences in every numerical check.
  `numerical-observation`: gap → 0 at second order; `F` falls while `U` rises in the demo
  (boxed in verify). No `open-question` box; mandatory-admonition invariant met many times over.
- **Misconceptions** — NEW entries proposed (registry edits at build time):
  - `free-energy-stored-energy` · "Free energy is a kind of energy stored inside the system" ·
    falsifier: two identical states of the same gas (same `U`, same `S`) offered to baths at
    different `T_r`: the extractable work `-\Delta F` differs though nothing inside the system
    differs — `F` books a system-plus-constraint relationship, not a content · distractor:
    "F is conserved in an isolated system".
  - `systems-minimize-energy` · "Systems spontaneously evolve toward minimum energy" ·
    falsifier: isolated free expansion (U constant, S up — nothing minimized), then the
    minimization demo where `U` visibly *rises* while `F` falls, the bath paying `T \Delta S`
    · distractor: "equilibrium at fixed T,V is the state of lowest U".
  - `enthalpy-heat-content` · "Enthalpy is the heat contained in a body" (05's
    `heat-stored-in-body` echoed one level up) · falsifier: isobaric electrolysis — `Q` and
    `\Delta H` split as soon as electrical work crosses the boundary; plus two paths between
    the same states with different `Q` but one `\Delta H` · distractor: "Q = Delta H for any
    process between the same two states".
  - Addressed from the registry: `heat-stored-in-body` (05) is revisited via its enthalpy echo
    above; no re-pointings needed.
- **Glossary terms** — existing keys reused: `enthalpy`, `free-energy`, `state-function`,
  `potential-function`. NEW: `thermodynamic-potential` · thermodynamic potential ·
  פוטנציאל תרמודינמי; `helmholtz-free-energy` · Helmholtz free energy ·
  אנרגיה חופשית של הלמהולץ · he_reject: [אנרגית הלמהולץ]; `gibbs-free-energy` · Gibbs free
  energy · אנרגיה חופשית של גיבס · he_reject: [אנרגיית גיבס]; `legendre-transform` · Legendre
  transform · התמרת לז'נדר · he_reject: [התמרת לג'נדר, טרנספורם לז'נדר]; `maxwell-relation` ·
  Maxwell relation · יחס מקסוול · he_reject: [קשר מקסוול]; `natural-variables` · natural
  variables · משתנים טבעיים; `joule-thomson` · Joule–Thomson throttling · תהליך ג'ול-תומסון ·
  he_reject: [ג'אול-תומסון].
- **Interactive controls and simulations** — *Natural-variables map:* constraint selector
  (isolated / fixed `T,V` / fixed `T,P` / throttling), model selector (ideal gas / Einstein
  solid), constraint-release slider; renders the highlighted potential with its differential
  and a live stacked ledger of `U`, `TS`, `PV`, `H`, `F`, `G`; ranges `T` 50–1000 K, `V`
  1–100 L, `N = 10^22` fixed. *Maxwell explorer:* potential picker (U/H/F/G) and pair picker;
  model-parameter sliders deform the fundamental relation; renders the `maxwell_check` gap as
  a 200×200 heatmap over the natural-variable plane, with an `h`-refinement button that halves
  the step and drops the gap floor fourfold. *Minimization demo:* `free_energy_minimization`
  trace, two panels — `F` monotone down while `U` rises; bath + system entropy ledger stacked
  (08's subsystem-ledger reprise, now with a mechanism).
- **Virtual lab outline** — `notebooks/en/labs/10-potentials.ipynb`: (1) setup — load a
  `fundamental` relation, plot `U(S)` at fixed `V,N`; (2) predictions — commit the four
  predict answers; (3) numeric Legendre — `legendre_transform` on a 10^4-point `U(S)` grid,
  overlay closed-form `F(T)`, `relative_error < 1e-6`; (4) Maxwell heatmap — `maxwell_check`
  on `F`, halve `h` three times, fit convergence order ≈ 2; (5) entropy with a pressure gauge —
  synthetic noisy `P(T)` at several `V`, fit `(\partial P/\partial T)_V`, integrate over `V`;
  (6) minimization trace — assert `F` non-increasing and `S_tot` non-decreasing while `U`
  rises; (7) rubber band — import tension–temperature CSV, fit `(\partial f/\partial T)_L`,
  infer `(\partial S/\partial L)_T = -(\partial f/\partial T)_L < 0`; (8) *measurement:*
  `\Delta S` for `V \to 2V` from the noisy `P(T,V)` data, value ± error vs `N \kB \ln 2`.
- **Real-experiment counterpart** — rubber-band thermodynamics, the classic and nearly free:
  qualitative — stretch fast, touch to lip (adiabatic warming, `(\partial T/\partial L)_S > 0`);
  hang a weight and heat with a hair-dryer (contraction). Quantitative — force gauge +
  thermistor, tension at fixed length across 5–10 temperatures; CSV columns `(T_K, f_N)`
  imported in lab part 7; the Maxwell analogue
  `(\partial S/\partial L)_T = -(\partial f/\partial T)_L` turns the fitted slope into a
  measured entropy-per-stretch. Recommended: ship a reference dataset so the analysis runs
  without hardware, accept student CSVs in the same cell.
- **Media assets** — `media/render/render_potentials.py`, language-neutral, no burned-in text:
  (1) `potentials-tangent-envelope.mp4` — tangents sweep a convex `U(S)`, intercepts trace out
  `F`; reverse sweep rebuilds the curve from its tangents; (2) `potentials-minimization.mp4` —
  composite system + bath under constraint release, bars: `F` falls, `U` rises, `S_tot`
  climbs; (3) `potentials-maxwell-gap.mp4` — gap heatmap flattening to zero as `h` refines
  (log color scale).
- **Quiz bank outline** — `assessment/quizzes/10-potentials.en.yml`:
  - `Q-10-1` multiple-choice · match four stated constraints to the extremal quantity ·
    OBJ-10-2.
  - `Q-10-2` multiple-choice · gas + bath at fixed T,V: after release U has risen — possible?
    what fell? · OBJ-10-3 · distractor from `systems-minimize-energy`.
  - `Q-10-3` multiple-choice · throttling conserves which of U, H, S, T? · OBJ-10-7 ·
    distractor "U, because energy is conserved".
  - `Q-10-4` numeric · Delta S for V -> 2V at fixed T from (dP/dT)_V = N kB / V; expect
    N kB ln 2 · OBJ-10-5.
  - `Q-10-5` multiple-choice · which Maxwell relation follows from G? (three plausible sign /
    held-variable corruptions) · OBJ-10-4.
  - `Q-10-6` multiple-choice · two identical states, baths at different T_r: does extractable
    work differ? · OBJ-10-1 · distractor from `free-energy-stored-energy`.
  - `Q-10-7` free · in two sentences, why does the tangent-line envelope mean F(T,V) forgets
    nothing that U(S,V) knew? · OBJ-10-6.
  - `Q-10-8` numeric · isobaric heating: given Delta U, P, Delta V, compute Q_P and Delta H;
    then add electrical work and recompute Q · OBJ-10-7, OBJ-10-1 · distractor from
    `enthalpy-heat-content`.
  - `Q-10-9` prediction · from lip-warming on fast stretch, predict the sign of
    (dS/dL)_T and the loaded band's response to heating · OBJ-10-4, OBJ-10-5.
- **Problem set outline** — `10-potentials-problems.md`: analytical — derive the `G` Maxwell
  relation and use it to show `(\partial S/\partial P)_T = -N \kB / P` for the ideal gas
  (OBJ-10-4/5); prove `G = \mu N` from Euler + definitions (OBJ-10-1); isobaric electrolysis
  ledger, `Q` vs `\Delta H` (OBJ-10-7). Computational — numeric Legendre of the Einstein-solid
  `U(S)` vs closed-form `F`, error vs grid size (OBJ-10-1/6); `\Delta S` from a van der Waals
  `(\partial P/\partial T)_V` vs the ideal gas (OBJ-10-5). Challenge — 1-D ideal-chain model:
  from `S(L)` derive tension `f = -T (\partial S/\partial L)`, predict contraction on heating,
  confront the lab's rubber-band data (OBJ-10-3/4).
- **Runtime budget** — trivial for Pyodide: 1-D grid Legendre transforms at ~10^4 points are
  vectorized NumPy milliseconds; the 200×200 gap heatmap is 1.6×10^5 potential evaluations × a
  4-point stencil, well under a second; minimization traces are ~10^3 steps. No RNG, no Numba
  (unavailable anyway), MP4s pre-rendered. Nothing here strains the browser.
- **Validation gates** — the standard six per-module commands (README bottom) with
  `--module 10-potentials`, plus `uv run python -m pytest tests/physics -q -k potentials`.
- **Open questions for the author** — (1) exact `fundamental.py` surface names: this plan
  assumes the protocol sketched in §4; reconcile against 09's plan and land any rename there
  first — recommendation: keep a small `FundamentalRelation` protocol rather than free
  functions, since 13 consumes it too. (2) Rubber-band data: ship-only vs student-collected —
  recommendation: ship a measured reference CSV, accept student uploads in the same cell.
  (3) Carry `\mu dN` everywhere or suppress until 13 — recommendation: print `\mu dN` in every
  boxed differential, hold `N` fixed in all interactives, one-line pointer to 13. (4) How far
  the advanced non-convex demo goes — recommendation: stop at "the transform forgets the
  dent"; the repair (common tangent) belongs wholly to 14.

## 4. Library and tests

- **`src/thermolab` — existing used:** `forms.py` — `mixed_partials_gap` and `is_exact` are
  the Maxwell verifier's engine (the 05 payoff made literal); `fundamental.py` (09, assumed
  surface): a `FundamentalRelation` exposing `entropy(U,V,N)`, `energy(S,V,N)`, and slope
  evaluators `temperature` / `pressure` / `chemical_potential`, with shipped Sackur–Tetrode
  and Einstein-solid instances and a concavity check; `paths.py` — `isobaric_path` +
  `Path.heat_into_gas` for the `\Delta H = Q_P` cross-check; `constants.K_B`;
  `validation.relative_error` / `convergence_study` in tests and lab.
- **`src/thermolab` — new: `potentials.py`** (introduced by 10 per README ownership; serves
  10, 13, 14; never extended). Docstring header, 7-bullet model spec: System — a substance
  given by a smooth concave fundamental relation `S(U,V,N)`, optionally coupled to an ideal
  reservoir; Dynamics — quasistatic constraint release on the equilibrium surface; Boundary —
  diathermal wall, frictionless piston where `P_r` is fixed; Ensemble — not applicable,
  macroscopic thermodynamics; Ignored — fluctuations, finite-bath effects, non-PV work;
  Valid when — reservoir ≫ system and `S` strictly concave; Failure modes — non-convex
  relations (multivalued transform), tiny baths, non-quasistatic coupling. Functions:
  - `legendre_transform(f_grid, x_grid) -> tuple[ndarray, ndarray]` — numeric transform of a
    sampled strictly convex/concave relation: slopes by central differences, `g = f - p x`;
    raises on non-monotone slopes (the information-loss case — 14's teaser).
  - `helmholtz_from(relation, temperature, volume, n_particles) -> float` — `F = U - TS` at
    the state located by inverting `T = (\partial U/\partial S)_V` on the relation; joules.
  - `gibbs_from(relation, temperature, pressure, n_particles) -> float` — `G = U - TS + PV`
    at the state fixed by `(T, P, N)`; joules.
  - `enthalpy_from(relation, entropy, pressure, n_particles) -> float` — `H = U + PV` at the
    state fixed by `(S, P, N)`; joules.
  - `maxwell_check(potential, x_grid, y_grid, h=1e-5) -> ndarray` — builds the two
    first-derivative fields of a two-argument potential callable and returns the
    cross-derivative gap via `forms.mixed_partials_gap`; zero to `O(h^2)` iff the Maxwell
    relation holds on the sampled region.
  - `natural_variables(potential_name) -> NaturalVariables` — lookup/evaluator: natural
    variables, differential string, and the constraint under which the potential is
    stationary/minimized; powers the map.
  - `free_energy_minimization(relation, t_bath, volume, n_particles, constraint_grid) ->
    MinimizationTrace` — quasistatic release against an ideal `T`-bath; returns aligned arrays
    `U`, `S`, `F`, `S_tot` with the contract `F` non-increasing and `S_tot` non-decreasing.
- **`tests/physics/` additions:** dimensional — `helmholtz_from`/`gibbs_from`/`enthalpy_from`
  return joules; ledger identity `U = F + TS` closes in J (`test_dimensions.py`).
  conservation — **not applicable**: everything here is a deterministic evaluation of state
  functions, nothing flows or is transported; stated in the test module docstring.
  analytic-limit — numeric Legendre of the Sackur–Tetrode `U(S)` reproduces closed-form
  `F(T,V,N)` to `1e-6` relative; same for the Einstein solid; `maxwell_check` vanishes for the
  ideal-gas `F(T,V)`; `gibbs_from / N` equals `\mu` (Euler, 09 cross-check) (`test_limits.py`).
  large-N — extensivity: `F(2N, 2V) = 2 F(N, V)` across a decade of `N` (`test_scaling.py`).
  convergence — `maxwell_check` gap and `legendre_transform` error fall at fitted order ≈ 2
  under `h` / grid refinement, via `validation.convergence_study` (`test_convergence.py`).
  seed-independence — **not applicable**: no function takes a generator; the module is
  deterministic by construction; stated in the docstring.

## 5. Assessment hooks

Checkpoint synthesis: the 07 + 08 + 10 refrigerator/bath ledger — 08's problem-5 seed
("something else pays more than the difference") becomes quantitative here: the bath absorbs
`T \Delta S >= \Delta U`, and `-\Delta F` bounds the work you can harvest on the way. A second
synthesis pairs 05 + 10: from "which differentials were exact" to "which identities that
exactness buys". Exam-style themes: choose-the-potential scenario batteries; derive a Maxwell
relation from a named potential under time pressure; an entropy-from-`P(T)`-data problem in
the style of lab part 8. Feeds forward: 12's capstone reconstructs `F` from `Z` for the
Einstein solid and must match this module's thermodynamic `F` (spiral C4c closes); 13 opens on
`\mu = (\partial G/\partial N)_{T,P}`; 14's Maxwell construction is the repair of the advanced
section's broken (non-convex) Legendre transform.

## 6. Build order and validation gates

Builds after 07 and 09: the derive spine spends 07's second law, and every function in
`potentials.py` consumes 09's `fundamental.py` — building 10 is also the first external test
that 09's surface is adequate before 13 leans on both. Lands alongside: the seven new glossary
keys above (with `he_reject` candidates) in `glossary/terms.yml`; the three new misconception
entries in `assessment/misconceptions.yml` with `assigned_module: 10-potentials`. Artifact
family per invariant 6: EN page + `10-potentials-problems.md` + lab notebook + quiz bank
(`10-potentials.en.yml` / `.he.yml`) + HE mirrors stamped with `en_source_hash`; the page is
listed in `translation-pending.txt` from first commit until the mirror family lands. Gates:
the six README commands with `--module 10-potentials`; media rendered by
`render_potentials.py` before the page references its three MP4s.

## 7. Deviations from the brainstorm

- **Thermodynamic square demoted to advanced curiosity.** The brainstorm itself rules here —
  §5 calls numerical cross-derivative verification "much more useful than memorizing a
  thermodynamic square". The square appears only as a mnemonic footnote; the verifier is the
  method.
- **`F = -\kB T \ln Z` deferred to 11/12.** Preserves the §2 spiral (free energy
  thermodynamically here, canonically there); the transfer section plants the seed explicitly
  so the deferral reads as a promise, not an omission.
- **Non-convex Legendre teaser added (advanced).** Not in the row; a deliberate seed for 14's
  Maxwell construction — information loss on a dented relation is coexistence knocking.
- **Throttling promoted into the centrepiece map.** The row lists enthalpy; giving `H` a real
  constraint pane (`H` conserved across a plug) saves it from a definition-only cameo and sets
  up 14's Clausius–Clapeyron latent-heat bookkeeping.
- **Rubber-band real experiment added.** Brainstorm §5 offers no counterpart for this module;
  the band makes the showpiece Maxwell relation tactile, quantitative, and nearly free, and it
  redeems 08's entropic-force transfer teaser.
