# Module 06 — Thermodynamic processes — Implementation Plan

> **Brainstorm:** §3 module 6 (+ §4 notebook rhythm, §5 laboratories, §6 misconceptions,
> §8 assessment). **Module id:** `06-processes`.
> **Content path:** `content/en/thermodynamics/06-processes.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Module 05 ended with a machine for computing $\Won$ along any route and the discovery that
work and heat are path functions. This module turns that machine into a *taxonomy*: the named
processes — isobar, isotherm, adiabat, isochore — stop being four disconnected formulas and
become four points on one dial, the polytropic index $n$ in $P V^n = \text{const}$. The story
is the **ledger**: for every process, all four of $\Won$, $Q$, $\Delta U$, $\Delta T$, closed
by the first law, with nothing left vague. The heat capacities $C_V$ and $C_P$ are derived
here from 04's equipartition result — so $\gamma$, which 05 accepted as an input to
`adiabatic_pressure`, is finally computed from $f$, and 05's asserted adiabat
$P V^{\gamma} = \text{const}$ gets its promised derivation.

The second half of the arc is the course's first *quantitative* look at irreversibility. Two
zero-heat processes with the same volume doubling end at different temperatures — the
quasistatic adiabat cools, the Joule free expansion does not — and the ledger, not any new
law, explains why. Sudden compression then shows the reverse face: same endpoints as a
quasistatic compression, strictly more work on the gas, the excess appearing as extra
$\Delta U$. That excess is deliberately left as an unexplained surcharge: 07 names it
(second law), 09 prices it (entropy production). This module is the hinge between "energy
bookkeeping" (04–05) and "why some ledger entries can never be reversed" (07–09).

The spiral contact: macroscopic heat capacities are pinned to the microscopic $f$ of module
04 now, and are revisited when $f$ itself melts — freeze-out in 12 (partition functions) and
16 (Einstein/Debye solids). The vdW teaser (a *real* gas cools in free expansion) plants 14.

## 2. Position in the course

- **Requires:** 04-pressure — equipartition $U = \tfrac{f}{2} N \kB T$ (theorem box on that
  page) and $PV = N \kB T$; 05-work-paths — the `Path` machinery, $\Won = -\int P\,dV$ for
  quasistatic routes, $\Won = -\int P_{\text{ext}}\,dV$ otherwise (05's advanced section),
  exact vs inexact differentials, and the sign convention $dU = \dbar Q + \dbar \Won$.
- **C1 division of labour (stated here, logged in §7).** Built 05 owns: path constructors,
  work along arbitrary paths, exact-vs-inexact, and path *comparison for work*. This module
  owns: $C_V$ and $C_P$ **derived** (05 takes $\gamma$ as an input), the Mayer relation
  $C_P - C_V = N \kB$ and $\gamma$, the **derivation** of $P V^{\gamma} = \text{const}$ (05
  asserts it), the complete per-process ledger ($\Won$, $Q$, $\Delta U$, $\Delta T$), the
  polytropic family unifying the named processes, and quantitative irreversible processes
  (Joule free expansion, sudden compression) as endpoint-only models.
- **Feeds:** 07 — cycles are joined polytropic legs (`cycles.py` consumes `polytropic_path`
  and `process_ledger`); irreversible legs enter engine analysis; 09 — entropy production
  quantifies the sudden-compression excess work; 14 — vdW free-expansion cooling pays off
  the teaser; 12/16 — freeze-out replaces the frozen-$f$ assumption.
- **Explicitly not assumed:** entropy (not yet defined — no $\dbar Q/T$, no "reversible ⇔
  isentropic"); Carnot machinery and efficiency (07); any statistical-ensemble language;
  real-gas equations of state beyond a one-line vdW teaser (02/14).

## 3. Module specification

- **Identity and scope** — brainstorm §3 row 6: isothermal, adiabatic, isobaric, quasistatic
  and irreversible processes. Centrepiece re-scoped per C1 (05 already compares paths): a
  polytropic-index slider morphing isobar → isotherm → adiabat → isochore with a live
  $\Won/Q/\Delta U/\Delta T$ ledger. Deferred: engine cycles and efficiency (07), entropy
  accounting of irreversibility (09), heat-capacity freeze-out (12/16), real-gas Joule
  coefficient (14).
- **Prerequisites** — 04: $U = \tfrac{f}{2} N \kB T$, $PV = N \kB T$; 05: `Path`,
  $\Won = -\int P\,dV$, $Q = \Delta U - \Won$, inexactness of $\dbar Q$ and $\dbar \Won$,
  the external-pressure rule for non-quasistatic work.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-06-1` Derive C_V = (f/2) N k_B from U = (f/2) N k_B T and compute Q for
    constant-volume heating.
  - `OBJ-06-2` Derive the Mayer relation C_P - C_V = N k_B from the constant-pressure
    ledger and compute gamma = C_P/C_V = (f+2)/f.
  - `OBJ-06-3` Derive P V^gamma = const and T V^(gamma-1) = const for a quasistatic adiabat
    from dU = dW_on with dQ = 0.
  - `OBJ-06-4` Compute the full ledger (W_on, Q, dU, dT) for each named quasistatic process
    of an ideal gas between given endpoints.
  - `OBJ-06-5` Place the named processes in the polytropic family P V^n = const and predict
    the sign of each ledger entry as n varies.
  - `OBJ-06-6` Analyze Joule free expansion and sudden compression as endpoint-only models:
    justify each ledger entry and show W_on(sudden) > W_on(quasistatic) for compression.
  - `OBJ-06-7` Explain why zero heat does not imply constant temperature, using the work
    ledger to contrast adiabatic expansion with free expansion.
- **Mathematical background** — already has: definite integrals, $\ln$, separation of
  variables (05's advanced used partials; not needed here). Introduced here: solving a
  first-order ODE by separation ($\tfrac{f}{2}\,dT/T = -dV/V$) — one worked box; limits of
  the family $x^{1-n}/(1-n) \to \ln x$ as $n \to 1$ (used by the analytic-limit tests too).
- **Physical intuition goals** — student can predict without algebra: (1) an adiabat is
  steeper than the isotherm through the same point, because expansion also spends internal
  energy; (2) free expansion of an ideal gas leaves the thermometer unchanged — nothing
  pushed back, so nothing was paid; (3) heating at constant pressure needs more heat than at
  constant volume, because part of it leaks out as expansion work; (4) slamming a piston
  costs more work than easing it, and the gas ends hotter.
- **Section skeleton seeds** — contract order, MyST labels `(06-processes-<suffix>)=`:
  - *puzzle:* two identical gases each double their volume with **zero heat supplied**. One
    (quasistatic adiabatic expansion) comes out measurably cold; the other (free expansion
    into vacuum) does not cool at all. Boxed question: "no heat" evidently does not mean
    "no temperature change" — what, exactly, is different? (Answer: the work ledger.)
  - *predict:* (1) which of the two doubled gases is colder, or are they equal? (targets
    `expansion-always-cools`, reinforces 05's `adiabatic-constant-t`); (2) to raise T of a
    gas by 1 K, does constant-P need more, less, or the same heat as constant-V? (targets
    `cp-whenever-pressure`); (3) rank the work to compress V→V/2 isothermally, adiabatically,
    suddenly; (4) after a sudden compression to the same (P,V) endpoint, where did the extra
    work go? (targets `irreversible-work-lost`).
  - *explore:* the polytropic explorer — slider $n \in [0, 3]$ plus an $n \to \infty$
    snap-to-isochore button; markers at $n = 0, 1, \gamma$; live P–V plot of the polytrope
    between fixed endpoint volumes with the four-bar ledger updating per drag; a second
    control comparing quasistatic vs sudden compression between the same endpoints; an $f$
    selector (3/5/6) moving the $\gamma$ marker.
  - *derive:* the six-step route in core derivations below — $C_V$ from equipartition,
    $C_P$ and Mayer, the adiabat, the polytropic family and its ledger, free expansion,
    sudden compression.
  - *verify:* ledger closure $\Won + Q = \Delta U$ on every slider position; polytropic work
    at $n \to 1$ converging to the isothermal log formula (the `numerical-observation`
    admonition: the $\epsilon$-limit plot of $|W_n - W_1|$ shrinking linearly in $n - 1$);
    trapezoid vs closed form at second order; $Q = 0$ recovered numerically at $n = \gamma$.
  - *transfer:* diesel/fire-syringe ignition (adiabatic heating); sound waves are adiabatic,
    not isothermal — why $v_s$ needs $\gamma$; atmospheric lapse rate as an adiabat; cycles
    as joined polytropic legs (07); vdW free expansion cools — a *real* gas pays internal
    work against attraction (02/14).
  - *quiz:* heat-capacity selection, gamma computation, adiabat endpoint arithmetic, ledger
    signs across the polytropic dial, the free-expansion contrast, sudden-vs-quasistatic
    work; every distractor tied to a registry misconception.
  - *explain:* (1) why "no heat" and "no temperature change" are different claims; (2) why
    $C_P > C_V$ in words a first-year could follow; (3) a classmate says the extra work of a
    sudden compression is "wasted" — correct them using only the first law.
  - *advanced (safe to skip, nothing core depends on it):* the polytropic heat capacity
    $C_n = C_V (n - \gamma)/(n - 1)$, including the *negative* heat capacity band
    $1 < n < \gamma$ (gas gets colder while absorbing heat); staged compression — $k$ sudden
    steps approaching the quasistatic bill as $k \to \infty$, seeding 09's production limit.
- **Core derivations** — ordered; all convention-compliant with $dU = \dbar Q + \dbar \Won$:
  1. *$C_V$ from equipartition.* Constant volume ⇒ $\dbar \Won = 0$ ⇒ $\dbar Q = dU$ with
     $U = \tfrac{f}{2} N \kB T$, so
     $C_V \equiv \left(\dbar Q / dT\right)_V = \tfrac{f}{2} N \kB$.
     Model-assumption box: $f$ is frozen at a constant here; freeze-out is 12/16's story.
  2. *$C_P$ via the constant-pressure ledger, Mayer, $\gamma$.* At constant $P$,
     $\dbar \Won = -P\,dV = -N \kB\, dT$, so
     $\dbar Q = dU - \dbar \Won = \tfrac{f}{2} N \kB\, dT + N \kB\, dT$, giving
     $C_P = C_V + N \kB$ (Mayer) and $\gamma \equiv C_P / C_V = (f+2)/f$.
  3. *The adiabat — 05's assertion paid off.* $\dbar Q = 0$ ⇒ $dU = \dbar \Won$:
     $\tfrac{f}{2} N \kB\, dT = -P\,dV = -\tfrac{N \kB T}{V} dV$; separate and integrate ⇒
     $T V^{\gamma - 1} = \text{const}$ and, via $PV = N \kB T$, $P V^{\gamma} = \text{const}$.
  4. *The polytropic family.* Define $P V^n = \text{const}$; then for $n \ne 1$
     $\Won = (P_2 V_2 - P_1 V_1)/(n - 1)$, $\Delta U = \tfrac{f}{2}(P_2 V_2 - P_1 V_1)$,
     $Q = \Delta U - \Won = C_n \Delta T$ with $C_n = C_V (n - \gamma)/(n - 1)$. Checks:
     $n{=}0$ ⇒ $C_0 = C_P$ (isobar); $n{=}1$ ⇒ $C \to \infty$ (isotherm); $n{=}\gamma$ ⇒
     $C = 0$ (adiabat); $n \to \infty$ ⇒ $C \to C_V$ (isochore).
  5. *Joule free expansion (endpoint-only).* Rigid adiabatic vessel, partition removed:
     nothing moves at the boundary ⇒ $\Won = 0$; $Q = 0$ ⇒ $\Delta U = 0$; ideal gas
     $U = U(T)$ ⇒ $\Delta T = 0$. Teaser: for vdW, $\Delta U = 0$ forces $T$ down as
     molecules climb out of each other's attraction — hook to 02/14.
  6. *Sudden compression (endpoint-only).* Constant $P_{\text{ext}}$, adiabatic walls,
     piston latched at $V_2 < V_1$: $\Won = -P_{\text{ext}}(V_2 - V_1) > -\int P\,dV$ of the
     quasistatic route between the same endpoints, since $P_{\text{ext}} \ge P$ throughout;
     $Q = 0$ ⇒ $\Delta U = \Won$, $\Delta T = \Won / C_V$. The excess work is the seed of
     irreversibility — named in 07, priced as entropy production in 09.
- **Model specification draft** —
  - **System:** a fixed amount of ideal gas, $N$ particles, with $f$ frozen quadratic
    degrees of freedom.
  - **Dynamics:** quasistatic along polytropes $P V^n = \text{const}$; irreversible
    processes modelled by their equilibrium endpoints only — no intermediate state claimed.
  - **Boundary:** cylinder with frictionless piston, diathermal or adiabatic as the process
    requires; free expansion uses a rigid adiabatic vessel with a removable partition.
  - **Ensemble:** not applicable — macroscopic thermodynamics.
  - **Ignored:** gas non-ideality, temperature dependence of $f$, piston mass and friction,
    all finite-rate detail of the irreversible processes.
  - **Valid when:** dilute classical gas; quasistatic legs slow versus the relaxation time;
    the endpoints of irreversible processes are genuine equilibrium states.
  - **Failure modes:** real-gas free expansion ($\Delta T \ne 0$), vibrational freeze-out
    making $\gamma$ temperature-dependent, any question about mid-process values of $P$ or
    $T$ during a sudden step.
- **Epistemic classification** — $C_V$, $C_P$, $C_n$: *definition* (boxed); Mayer relation
  and $P V^{\gamma} = \text{const}$: *theorem* within the ideal-gas model; frozen $f$:
  *model-assumption* (boxed — the module's mandatory admonition, with the 12/16 pointer);
  endpoint-only treatment of irreversible processes: *approximation* (boxed); ideal-gas
  free-expansion $\Delta T = 0$: *theorem* in-model, *empirical-law* contrast for real
  gases (Joule's experiment); $n \to 1$ convergence plot: *numerical-observation* (boxed).
- **Misconceptions** — reinforced, no registry edit: `adiabatic-constant-t` (owned and
  addressed by 05); this module stages a second falsifier — the free-expansion *contrast* —
  and reuses the distractor in Q-06-7. NEW entries proposed (registry edit at build time):
  - `expansion-always-cools` · "Any expansion of a gas lowers its temperature." ·
    falsifier: Joule free expansion in the explorer — thermometer unchanged — beside the
    visibly cooling adiabat · distractor: free-expansion $T$ "computed" from
    $T V^{\gamma-1} = \text{const}$.
  - `cp-whenever-pressure` · "C_P is the right heat capacity whenever the gas is under
    pressure." · falsifier: constant-volume heating in the explorer — measured $Q/\Delta T$
    equals $C_V$ at any pressure · distractor: $Q = C_P \Delta T$ offered for an isochoric
    step.
  - `irreversible-work-lost` · "The extra work of an irreversible compression is lost
    energy." · falsifier: the sudden-compression ledger closes exactly — the excess appears
    as extra $\Delta U$ and $\Delta T$, nothing missing (where it can no longer *go* is
    availability, 07's story) · distractor: "the difference is dissipated and disappears
    from the energy account."
- **Glossary terms** — reuse existing keys: `heat-capacity`, `adiabatic`, `isothermal`,
  `isobaric`, `isochoric`, `quasistatic`, `irreversible`, `equipartition`,
  `degrees-of-freedom`. NEW: `polytropic` / polytropic process / he: תהליך פוליטרופי /
  `he_reject:` [פוליטרופיק]; `free-expansion` / free expansion / he: התפשטות חופשית;
  `heat-capacity-ratio` / heat-capacity ratio (gamma) / he: יחס קיבולי החום / `he_reject:`
  [יחס קיבולות חום]; `mayer-relation` / Mayer relation / he: יחס מאייר / `he_reject:`
  [יחס מאיר].
- **Interactive controls and simulations** — (1) *polytropic explorer:* slider
  $n \in [0, 3]$ (step 0.01) + isochore snap button; $f \in \{3, 5, 6\}$; fixed endpoints
  $V_1, V_2 = 2V_1$; renders the polytrope over 257 sampled points, reference isotherm and
  adiabat as ghosts, and the four-bar ledger (J) with $\Delta T$ readout (K). (2)
  *quasistatic-vs-sudden compressor:* shared endpoints $V_1 \to V_2 < V_1$, slider
  $P_{\text{ext}}$ from $P_{\text{quasistatic,max}}$ upward; renders both ledgers side by
  side and the excess-work bar. (3) *free-expansion panel:* partition-removal button, before
  and after states with thermometers, ledger of zeros — deliberately anticlimactic.
- **Virtual lab outline** — `notebooks/en/labs/06-processes.ipynb`: (1) setup — import
  `thermolab.paths`, choose $N$, $T_1$, $V_1$, $f$; (2) predictions cell — commit the four
  predict answers; (3) build the four named paths plus `polytropic_path` at slider-chosen
  $n$, tabulate `process_ledger` for each; (4) verify Mayer and $\gamma$ from
  `heat_capacity_cv/cp`; (5) sweep $n$ over $[0, 3]$, plot each ledger entry vs $n$, find
  the zero of $Q$ at $n = \gamma$; (6) sudden vs quasistatic compression, excess work vs
  $P_{\text{ext}}$; (7) *measurement:* fit the zero-crossing of $Q(n)$ from the sweep ⇒
  $\gamma = 1.667 \pm 0.002$ (monatomic run), compared against $(f+2)/f$.
- **Real-experiment counterpart** — **recommended: bicycle-pump adiabatic warming** (fire
  syringe as the dramatic classroom variant). Block the outlet, compress fast (≈ adiabatic),
  read barrel temperature with an IR thermometer; estimate compression ratio from plunger
  travel; compare with $T V^{\gamma-1} = \text{const}$. Data import: students record rows
  `(v_ratio, t_before_k, t_after_k)` in a CSV loaded by a lab cell that overlays the
  adiabat prediction and a least-squares $\gamma$ estimate. Rüchardt-style oscillation
  ($\gamma$ from a bouncing piston's period) is the instructor-hardware alternative — finer
  data, more apparatus; note it in the page's advanced section, do not build for it.
- **Media assets** — `media/render/render_processes.py`, language-neutral (no burned-in
  text): (1) `processes-polytrope-morph.mp4` — the polytrope sweeping $n: 0 \to 3$ through
  the marked isobar/isotherm/adiabat with the four ledger bars animating; (2)
  `processes-two-expansions.mp4` — split screen, adiabatic piston expansion vs partition
  removal, thermometer columns diverging; (3) `processes-sudden-piston.mp4` — quasistatic
  vs slammed compression, work bars accumulating to different heights.
- **Quiz bank outline** — `assessment/quizzes/06-processes.en.yml` (+ `.he.yml`):
  - `Q-06-1` multiple-choice · OBJ-06-1 · $C_V$ for monatomic vs diatomic; distractor:
    "heavier molecules ⇒ larger $C_V$".
  - `Q-06-2` numeric · OBJ-06-2 · compute $\gamma$ for $f = 5$ (1.4) and check Mayer.
  - `Q-06-3` multiple-choice · OBJ-06-2 · which capacity for heating a rigid tank at 2 atm;
    distractor from `cp-whenever-pressure`.
  - `Q-06-4` numeric · OBJ-06-3 · adiabatic halving of volume: $T_2 = T_1 2^{\gamma-1}$.
  - `Q-06-5` multiple-choice · OBJ-06-4, OBJ-06-5 · sign pattern of $(\Won, Q, \Delta T)$
    for expansion at $n = 0, 1, \gamma, \infty$; distractor: $Q > 0$ on the adiabat.
  - `Q-06-6` numeric · OBJ-06-4 · full four-entry ledger for an isobaric expansion.
  - `Q-06-7` multiple-choice · OBJ-06-6, OBJ-06-7 · the doubled-volume contrast; distractors
    from `expansion-always-cools` and 05's `adiabatic-constant-t`.
  - `Q-06-8` numeric · OBJ-06-6 · $\Won$ sudden vs quasistatic between the same endpoints;
    distractor from `irreversible-work-lost` ("the difference is destroyed").
  - `Q-06-9` free · OBJ-06-7 · explain in words why zero heat does not fix the temperature.
- **Problem set outline** — `06-processes-problems.md`: *analytical:* derive
  $C_n = C_V (n - \gamma)/(n - 1)$ and locate the negative band (OBJ-06-5); sudden
  compression to *pressure* equilibrium — show $T_2 = [f T_1 + 2 P_{\text{ext}} V_1 /
  (N \kB)]/(f + 2)$ (OBJ-06-6). *computational:* fit $n$ from a noisy $P$–$V$ trace
  (OBJ-06-5); fire-syringe ignition — minimum compression ratio to reach 500 K (OBJ-06-3).
  *challenge:* $k$-step staged sudden compression → show the total work decreases
  monotonically to the quasistatic bill as $k \to \infty$ (OBJ-06-6, seeds 09).
- **Runtime budget** — everything closed-form or 1-D quadrature: paths sampled at ≤ 513
  points, ledger recompute per slider drag is a handful of vectorized NumPy ops (< 5 ms in
  Pyodide); the $n$-sweep is 301 × 257 array evaluations (< 0.5 s); no Monte Carlo, no
  seeds, no Numba; animations are pre-rendered MP4s. The whole lab runs in seconds.
- **Validation gates** — the six README commands with `--module 06-processes`; extra:
  `pytest tests/physics -q -m "conservation or analytic_limit"` must pass with the new
  `paths` functions; `git diff --stat content/en/thermodynamics/05-work-paths.md` empty —
  this module must not touch 05's page.
- **Open questions for the author** — (1) sudden-compression explorer: latch the piston at
  $V_2$ (shared endpoints with the quasistatic route) or run to pressure equilibrium with
  $P_{\text{ext}}$? *Recommend latched* — endpoint sharing makes the comparison honest; the
  pressure-equilibrium variant goes to the problem set. (2) Molar $c_v, c_p$ alongside the
  extensive $N \kB$ forms? *Recommend extensive only*, one aside translating to molar for
  lab-book literacy. (3) Negative-$C_n$ band: advanced section or problems? *Recommend
  advanced* — it needs the $C_n$ plot. (4) Depth of the vdW free-expansion teaser?
  *Recommend one paragraph + transfer link*, no vdW algebra before 02 exists.

## 4. Library and tests

- **`src/thermolab` — existing used:** `paths.py` — `Path`, `isothermal_path`,
  `adiabatic_path`, `isobaric_path`, `isochoric_path`, `join`, `work_on_gas`, `work_along`,
  the three closed-form work functions, `ideal_gas_pressure`, `ideal_gas_temperature`
  (canonical home moves to `gases.py` when 02 builds — C4a); `constants.K_B`.
- **`src/thermolab` — new / extended:** extends `paths.py` (README ownership: introduced by
  05, extended by 06 with "polytropic family, heat capacities, process ledger"). Extender
  specs only its own functions; the file's 7-bullet docstring header is 05's:
  - `polytropic_pressure(volumes, p_ref, v_ref, n) -> np.ndarray` — $P(V)$ with
    $P V^n = P_{\text{ref}} V_{\text{ref}}^n$; `n = 1` allowed (isotherm through the ref).
  - `polytropic_path(p_start, v_start, v_end, n, n_points=257, label="polytropic") -> Path`
    — sampled polytrope, drop-in for the 05 constructors.
  - `polytropic_work_on_gas(p_start, v_start, p_end, v_end, n) -> float` — closed form
    $(P_2 V_2 - P_1 V_1)/(n - 1)$; raises on `n == 1` (use the isothermal formula).
  - `heat_capacity_cv(degrees_of_freedom, n_particles) -> float` — $C_V = \tfrac{f}{2} N \kB$
    in J/K.
  - `heat_capacity_cp(degrees_of_freedom, n_particles) -> float` — $C_V + N \kB$, defined
    *as* the Mayer sum so the relation can never drift.
  - `adiabatic_exponent(degrees_of_freedom) -> float` — $\gamma = (f + 2)/f$; the value 05
    took as an input is now computed.
  - `ProcessLedger` — frozen dataclass `(w_on, q, du, dt)`; the module's central object.
  - `process_ledger(path, n_particles, degrees_of_freedom=3) -> ProcessLedger` — ledger of
    a quasistatic `Path`, closed by construction: `q = du - w_on`, `dt = du /
    heat_capacity_cv(...)`.
  - `free_expansion(n_particles, temperature, v_start, v_end) -> ProcessLedger` —
    endpoint-only: all four entries zero for the ideal gas; exists to make the contrast
    executable, deliberately returns no `Path`.
  - `sudden_compression(n_particles, temperature, v_start, v_end, p_ext) -> ProcessLedger`
    — endpoint-only: `w_on = -p_ext * (v_end - v_start)`, `q = 0`; raises unless
    `p_ext >=` the gas pressure everywhere on the quasistatic route (else no compression).
- **`tests/physics/` additions:** *dimensional* — `heat_capacity_cv/cp` carry J/K under
  pint; ledger entries J and K. *conservation* — `w_on + q == du` (fractional tolerance,
  per 05's trap) for every named path, 20 random polytropes, and both endpoint models.
  *analytic-limit* — polytropic work at $n = 1 \pm 10^{-8}$ brackets the isothermal log
  formula; $n = \gamma$ reproduces `adiabatic_work_on_gas` and gives $Q = 0$; $n = 0$
  reproduces the isobaric formula; Mayer relation exact; free expansion gives
  $\Delta T = 0$; sudden $\Won$ strictly exceeds quasistatic $\Won$ for all tested
  $P_{\text{ext}}$. *large-N* — heat capacities extensive: doubling `n_particles` doubles
  both, ratio $\gamma$ invariant. *convergence* — `work_along` on a polytrope converges to
  the closed form at fitted order 2.0. *seed-independence* — n/a, module is deterministic
  (recorded in the test file header so the category is consciously waived, not forgotten).

## 5. Assessment hooks

Checkpoint synthesis (04+05+06): from a particle simulation's measured $f$, predict
$\gamma$, construct the adiabat, and reconcile the microscopic energy budget with the
macroscopic ledger. Exam themes: ledger-sign reasoning across the polytropic dial; "same
endpoints, different bills" now with all four entries; endpoint-only reasoning for
irreversible steps. Feeds forward: 07's engine constructor consumes `polytropic_path` +
`process_ledger` for every leg and inherits the staged-compression challenge as its
reversibility limit; 09's entropy-production lab reuses the sudden-compression excess as
the quantity it finally explains; the module-14 vdW lab answers the free-expansion teaser.

## 6. Build order and validation gates

Builds after 05 (extends its file, pays its assertion) and ideally after 02 lands `gases.py`
(C4a) — but nothing here blocks on 02: the ideal-gas relations already live in `paths.py`.
Alongside the build: `glossary/terms.yml` gains the four new keys of §3 (Hebrew per
suggestions, `he_reject` as listed); `assessment/misconceptions.yml` gains the three new
entries with `assigned_module: 06-processes`, and `adiabatic-constant-t` stays 05's.
Artifact family: EN page + `06-processes-problems.md` + lab notebook + quiz bank
`.en.yml`/`.he.yml` + HE mirrors stamped with `en_source_hash`; page listed in
`translation-pending.txt` until the mirror lands. Gates: the six README commands with
`--module 06-processes`, plus the two extras in §3's validation-gates bullet.

## 7. Deviations from the brainstorm

- **C1 re-scope (centrepiece).** Brainstorm row 6's centrepiece "compare paths with
  identical endpoints" is already built in 05; the centrepiece becomes the polytropic-index
  slider with the live $\Won/Q/\Delta U/\Delta T$ ledger, plus the quasistatic-vs-sudden
  comparator — the ledger, not path comparison, is what 05 left unowned.
- **Heat capacities moved here from brainstorm row 5.** Row 5 lists heat capacities under
  the first law, but 05 as built takes $\gamma$ as an input and derives nothing about
  $C_V/C_P$; deriving them here keeps 05 untouched and gives the adiabat derivation its
  prerequisites in the same page.
- **Equipartition assumed with frozen $f$; freeze-out deferred to 12/16.** The $C_V$
  derivation leans on 04's equipartition theorem box and flags constant $f$ as a
  model-assumption rather than qualifying every formula with $f(T)$.
- **Irreversible processes are endpoint-only models.** The brainstorm's "quasistatic and
  irreversible processes" is honoured without simulating non-equilibrium dynamics — no
  mid-process state is claimed, matching 05's external-pressure rule and deferring the
  *cost* of irreversibility to 07/09.
