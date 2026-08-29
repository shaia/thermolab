# Module 07 — The second law — Implementation Plan

> **Brainstorm:** §3 module 7 (+ §4 notebook rhythm, §5 laboratories, §6 misconceptions,
> §7 accuracy framework, §8 assessment). **Module id:** `07-second-law`.
> **Content path:** `content/en/thermodynamics/07-second-law.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Patent offices reject perpetual-motion machines of the second kind without reading past page
one. That refusal is the module's through-line: the second law begins life not as an equation
but as two blunt empirical prohibitions — Kelvin's (no cycle turns heat wholly into work) and
Clausius's (no cycle moves heat cold-to-hot unaided) — and everything else is squeezed out of
them by composition arguments. The student builds engines in the centrepiece constructor, tries
honestly to beat Carnot between two fixed reservoirs, fails every time, and then watches the
derivation explain why the failure is a theorem, not an engineering ceiling that better
lubricant will someday break.

The module is the macroscopic pass of the entropy spiral (brainstorm §2, conflict C2): the
Clausius inequality yields a path-independent integral, $\int \dbar Q_{\mathrm{rev}}/T$, and
with it a new state function $S$ — the payoff of module 05's exact-vs-inexact distinction,
since $1/T$ is precisely the integrating factor that turns the path function $\dbar Q$ into the
state function $\mathrm{d}S$. What $S$ *is* microscopically was already met in the built module
08 ($S = \kB \ln \Omega$); how $S(U,V,N)$ organises all of thermodynamics waits for 09. This
module defines $S$, computes it on ideal-gas legs, and deliberately stops there.

Relative to the brainstorm's one-row description, the plan deepens three things: refrigerators
and heat pumps become first-class (reversed cycles, COP, and the falsifier for "a fridge
violates the second law"), reversibility is defined properly (quasistatic + frictionless + no
finite-$\Delta T$ heat flow, reinforcing 05's `reversible-just-backward` falsifier), and the
thermodynamic temperature scale is presented as the prize of Carnot universality. Seeds are
planted for 09 (entropy production), 10 (free energies as constrained second-law statements),
and 13/14 (cycle arguments reused for $\mu$-equality and Clausius–Clapeyron).

## 2. Position in the course

- **Requires:** 05 — `Path`, `join`, $\Won = -\int P\,\mathrm{d}V$, `heat_into_gas`, and the
  exact-vs-inexact differential distinction; 06 — the polytropic path family, the per-process
  W/Q/ΔU/ΔT ledger, $\gamma$ and $C_V$/$C_P$ derived, and the endpoint-only irreversible models
  (`free_expansion`, `sudden_compression`); 04 — $U = \tfrac{f}{2} N \kB T$; 01 — equilibrium,
  reservoirs as idealised very-large bodies, empirical temperature.
- **Feeds:** 09 — `cycles.entropy_change` seeds the $S(U,V,N)$ fundamental relation and 09's
  quantitative entropy-production experiments; 10 — free energies restate the second law under
  constraints, and the maximum-work theorem re-derives Carnot; 13/14 — composite-cycle
  reasoning returns for $\mu$-equality and Clausius–Clapeyron; 08 (backward) — the recorded
  verify-bridge $\kB \ln \Omega \leftrightarrow \int \dbar Q_{\mathrm{rev}}/T$ in 08's gap list
  becomes actionable once this module lands.
- **Explicitly not assumed:** any statistical entropy formula in the derivation chain — 08's
  $S = \kB \ln \Omega$ appears only in the transfer bridge, never as a premise; no entropy
  *production* machinery or general $\mathrm{d}S \ge 0$ principle (09's, per C2); no real-gas
  equations of state; no Legendre transforms or potentials (10's).

## 3. Module specification

- **Identity and scope** — brainstorm §3 row 7 in full: Kelvin and Clausius statements, their
  equivalence, Carnot cycle and theorem, engines/refrigerators/heat pumps, efficiency bounds;
  plus (per C2) the Clausius inequality and the definition of Clausius entropy $S$. Deferred:
  entropy production and the maximization story → 09; free energies → 10; the statistical
  meaning of $S$ → already built in 08, only bridged here.
- **Prerequisites** — 05 (`Path`/`join`, work/heat as path functions), 06 (polytropes, process
  ledger, $\gamma$, irreversible endpoint models), 04 ($U = \tfrac{f}{2} N \kB T$), 01
  (reservoir idealisation).
- **Learning objectives** —
  - `OBJ-07-1` — State the Kelvin and Clausius statements and prove their equivalence by the
    composite-device (contrapositive) argument.
  - `OBJ-07-2` — Construct the ideal-gas Carnot cycle, compute the per-leg W/Q ledger with
    dU = dbar Q + dbar W_on, and derive eta_C = 1 - T_c/T_h.
  - `OBJ-07-3` — Prove Carnot's theorem by the composite-engine contradiction and explain how
    universality defines the thermodynamic temperature scale via Q_h/|Q_c| = T_h/T_c.
  - `OBJ-07-4` — Derive and apply the Clausius inequality: cyclic integral of dbar Q / T <= 0,
    with equality iff the cycle is reversible.
  - `OBJ-07-5` — Show that the integral of dbar Q_rev / T is path-independent, define the state
    function S, and compute Delta S for ideal-gas isothermal and adiabatic legs.
  - `OBJ-07-6` — Classify a process as reversible or irreversible using the three conditions
    (quasistatic + frictionless + no finite-Delta-T heat flow) and predict the sign of its
    cycle's Clausius sum.
  - `OBJ-07-7` — Analyse a cycle run backward as refrigerator or heat pump, compute COP, and
    explain why moving heat cold-to-hot with work input violates nothing.
- **Mathematical background** — already has: line integrals in the P-V plane, exact vs inexact
  differentials (05), $\ln$ algebra, the adiabat relation $T V^{\gamma-1} = \text{const}$ (06).
  Introduced here: cyclic integrals $\oint$, integrating factors as a physics payoff (the math
  is in the refresher), proof by composition/contradiction as a physical argument style.
- **Physical intuition goals** — (1) predict, before algebra, that a frictionless engine still
  must discard heat; (2) rank engine efficiencies from reservoir temperatures alone; (3) sense
  that a refrigerator is an engine run backward and that its ledger must show work in; (4) spot
  the irreversible leg in a cycle by asking "did heat cross a finite $\Delta T$? did the gas
  have a single $P$?".
- **Section skeleton seeds** —
  - *puzzle:* the patent office rejects second-kind perpetual-motion machines unread. Boxed
    question: why is "no engine beats Carnot" a law of nature rather than an engineering
    ceiling that better lubricant will someday break?
  - *predict:* (1) best efficiency of a perfectly frictionless, sealed engine between 600 K
    and 300 K — 100%, 50%, or neither? (targets `efficiency-loss-is-friction`); (2) does your
    kitchen refrigerator violate the second law, and what balances the books? (targets
    `refrigerator-violates-second-law`); (3) Carnot engine with helium vs argon between the
    same reservoirs — which wins? (targets `carnot-universal-number`); (4) run the cycle
    backward: useless, a heater, or a refrigerator?
  - *explore:* the engine constructor — join legs (isotherm/adiabat/isobar/isochore/polytrope
    slider from 06; irreversible endpoint jump) into a closed loop; $T_h, T_c$ sliders
    (200–1200 K); live P-V plot with signed-area shading, per-leg W/Q ledger, net work, and an
    $\eta$ (or COP) dial with the Carnot bound marked.
  - *derive:* the six-step route in core derivations below, ending in the boxed definition of
    $S$ and its ideal-gas evaluation — then stop (production is 09's).
  - *verify:* (1) simulated Carnot $\eta \to 1 - T_c/T_h$ to quadrature tolerance; (2)
    `clausius_sum` $\approx 0$ on reversible cycles and strictly negative once an irreversible
    leg is included — the mandatory `numerical-observation` box; (3) `entropy_change` agrees
    across two different reversible routes; (4) constructor sweep: no cycle between the same
    reservoirs beats $\eta_C$.
  - *transfer:* free-expansion $\Delta S$ computed the Clausius way equals 08's counting answer
    $N \kB \ln 2$ — the 07↔08 bridge teaser (the formal verify-bridge is 08's gap item); 09's
    fundamental relation; 10's free energies as second-law bookkeeping; power-station
    efficiencies vs the Carnot bound; Clausius–Clapeyron preview (14).
  - *quiz:* statements and equivalence; Carnot ledger and bound; Clausius-sum signs; $\Delta S$
    on legs; refrigerator/COP; reversibility classification.
  - *explain:* (1) why an isothermal expansion converting heat to work does not violate Kelvin
    (not a cycle); (2) tell an inventor, without equations, why page two goes unread; (3) why
    defining $S$ needs reversible paths although $S$ exists for every equilibrium state; (4)
    why "reversible" is not "can be run backward".
  - *advanced (optional, always last):* endoreversible engines and the Curzon–Ahlborn
    efficiency at maximum power, $\eta_{\mathrm{CA}} = 1 - \sqrt{T_c/T_h}$; why real plants sit
    near it; why a regenerator lets a Stirling engine approach Carnot. Safe to skip: no core
    content here or later depends on it.
- **Core derivations** — ordered: (1) reservoir, cycle, and engine defined; Kelvin and
  Clausius statements boxed as `empirical-law`; equivalence proved by composition — a Kelvin
  violator driving an ordinary refrigerator becomes a Clausius violator, and conversely. (2)
  Carnot cycle on the ideal gas: isothermal legs $Q_h = N \kB T_h \ln(V_2/V_1)$ (from
  $\Delta U = 0$, $\mathrm{d}U = \dbar Q + \dbar \Won$), adiabat junctions
  $T V^{\gamma-1} = \text{const} \Rightarrow V_3/V_4 = V_2/V_1$; for any cycle
  $\oint \mathrm{d}U = 0$ gives $-\Won^{\mathrm{net}} = Q_h + Q_c$ (signed, $Q_c < 0$), so
  $\eta = -\Won^{\mathrm{net}}/Q_h = 1 + Q_c/Q_h$, and for Carnot
  $\eta_C = 1 - T_c/T_h$. (3) Carnot's theorem: a putative better engine driving the reversed
  Carnot cycle pumps heat cold-to-hot with zero net work — contradiction with Clausius; boxed
  `theorem`. (4) Universality: all reversible engines share $\eta(T_h, T_c)$, so
  $Q_h/|Q_c| = T_h/T_c$ *defines* thermodynamic temperature; the ideal-gas scale coincides.
  (5) Clausius inequality by the standard partition-into-Carnot-strips argument: couple every
  heat exchange to one reference reservoir through reversible Carnot engines, apply Kelvin to
  the composite, obtain $\oint \dbar Q / T \le 0$, equality iff reversible (run it reversed).
  (6) Payoff, boxed `theorem`: for reversible cycles the equality makes
  $\int_a^b \dbar Q_{\mathrm{rev}}/T$ path-independent, defining a state function $S$ with
  $\mathrm{d}S = \dbar Q_{\mathrm{rev}}/T$ — $1/T$ is 05's promised integrating factor; stated
  explicitly: 08 already met what $S$ *is* microscopically, 09 owns the structural story
  $S(U,V,N)$. Evaluate: isothermal leg $\Delta S = N \kB \ln(V_b/V_a)$; reversible adiabat
  $\Delta S = 0$; general ideal gas
  $\Delta S = N \kB \ln(V_b/V_a) + \tfrac{f}{2} N \kB \ln(T_b/T_a)$. Stop.
- **Model specification draft** —
  - **System:** a fixed amount of ideal gas ($N$ particles, $f$ degrees of freedom) carried
    around a closed loop of legs in the P-V plane, exchanging heat with two ideal reservoirs.
  - **Dynamics:** quasistatic traversal — equilibrium at every point of each drawn leg;
    optional irreversible legs are endpoint-only jumps with prescribed Q and W_on (06's
    models), no intermediate states drawn.
  - **Boundary:** cylinder with frictionless piston; diathermal contact with one reservoir at
    a time, switched between legs; reservoirs have fixed T and infinite heat capacity.
  - **Ensemble:** not applicable — macroscopic thermodynamics.
  - **Ignored:** friction, finite-rate effects, gas non-ideality, reservoir internal dynamics,
    the mechanism that switches thermal contact.
  - **Valid when:** traversal is slow against the gas's relaxation time and each reservoir is
    large against the heat it exchanges.
  - **Failure modes:** fast strokes (no single P; the drawn area is not the work), finite
    reservoirs (T drifts mid-leg), and any leg ledgered as reversible while its heat crosses a
    finite temperature difference.
- **Epistemic classification** — Kelvin statement, Clausius statement: `empirical-law` (both
  boxed); Kelvin ⇔ Clausius, Carnot's theorem, Clausius inequality, S-is-a-state-function:
  `theorem` (Carnot's theorem and the S box are the module's showpiece boxes); ideal-gas
  working fluid: `model-assumption` (boxed at the constructor); $\eta_C = 1 - T_c/T_h$:
  theorem *given* that assumption, with universality restoring generality; irreversible cycles
  give strictly negative Clausius sums: `numerical-observation` (boxed in verify); reversibility
  conditions: `definition`; Curzon–Ahlborn: `model-assumption` (advanced).
- **Misconceptions** — addressed: `reversible-just-backward` (05's; reinforced, not
  re-claimed — the three-condition definition plus the endpoint-jump legs whose Clausius sum
  is negative). NEW entries proposed: `refrigerator-violates-second-law` · "A refrigerator
  violates the second law because it moves heat from cold to hot." · falsifier: the reversed
  constructor cycle's ledger shows $Q_h = |Q_c| + \Won^{\mathrm{net}}$ — the work input is
  visible, and the reservoir budget $|Q_h|/T_h - |Q_c|/T_c \ge 0$ balances · distractor: "heat
  left the cold box, so heat flowed cold-to-hot spontaneously". `efficiency-loss-is-friction`
  · "Efficiency below 100% is caused by friction alone." · falsifier: the simulated Carnot
  engine is frictionless by construction yet still discards $|Q_c| = (T_c/T_h) Q_h$ ·
  distractor: "a perfectly frictionless engine reaches eta = 1". `carnot-universal-number` ·
  "Carnot efficiency is one fixed number that applies to every engine regardless of its
  reservoirs." · falsifier: constructor sweep of $(T_h, T_c)$ pairs moves the bound; an engine
  can beat another pair's $\eta_C$, never its own · distractor: "no engine anywhere can exceed
  60%, whatever its reservoirs".
- **Glossary terms** — existing keys consumed: `heat-engine`, `carnot-efficiency`, `cycle`,
  `reversible`, `irreversible`, `quasistatic`, `entropy`. NEW: `reservoir` · heat reservoir ·
  מאגר חום · he_reject [רזרבואר]; `refrigerator` · refrigerator · מקרר; `heat-pump` · heat
  pump · משאבת חום; `coefficient-of-performance` · coefficient of performance (COP) · מקדם
  ביצועים · he_reject [מקדם ביצוע]; `thermodynamic-temperature` · thermodynamic temperature ·
  טמפרטורה תרמודינמית; `clausius-inequality` · Clausius inequality · אי-שוויון קלאוזיוס ·
  he_reject [אי שיוויון קלאוזיוס]; `perpetuum-second-kind` · perpetual-motion machine of the
  second kind · מכונת תנועה נצחית מהסוג השני.
- **Interactive controls and simulations** — (1) engine constructor: leg palette (isotherm,
  adiabat, isobar, isochore, polytrope with exponent slider $n \in [0, 3]$, irreversible
  jump), $T_h, T_c \in [200, 1200]$ K, per-leg endpoint drag; renders P-V loop with signed
  area, live per-leg ledger, $\eta$/COP dial against the $\eta_C$ marker; direction toggle
  flips engine ↔ refrigerator. (2) efficiency-vs-$T_c/T_h$ explorer: measured $\eta$ of the
  student's cycles scattered under the $1 - T_c/T_h$ line.
- **Virtual lab outline** — `notebooks/en/labs/07-second-law.ipynb`: (1) setup — build
  `carnot_cycle(600, 300, ...)`; (2) predictions committed (efficiency guess; does halving
  $T_c$ double $\eta$?; can a third leg beat Carnot?); (3) measure the per-leg ledger, net
  work, $Q_h$, $Q_c$, $\eta$; (4) sweep $\eta$ vs expansion ratio (flat) and vs $T_c/T_h$
  (the line); (5) beat-Carnot attempts with `otto_cycle`, `stirling_cycle`, free-form cycles;
  (6) reverse the cycle, measure COP against $T_c/(T_h - T_c)$; (7) swap one isotherm for a
  free-expansion jump + recompression, compute `clausius_sum` < 0; (8) *measurement:* simulated
  Carnot $\eta = 0.5000 \pm$ (quadrature error) vs the exact $0.5$, and
  `clausius_sum(carnot) = 0 \pm$ tolerance.
- **Real-experiment counterpart** — none practical: no desk-scale engine exposes a per-leg
  quasistatic W/Q ledger (combustion, friction, and finite-rate effects swamp it), so the
  simulated constructor *is* the apparatus. Optional qualitative pairing: a low-$\Delta T$
  Stirling desk toy on a mug of hot water — it reverses direction over ice, a direction-of-
  heat-flow demonstration only; no data import.
- **Media assets** — `media/render/render_second_law.py`: MP4 shot list, language-neutral:
  (1) Carnot loop traced leg-by-leg in the P-V plane, per-leg colour, net-work area filling;
  (2) composite-engine contradiction — a "better" engine driving a reversed Carnot engine,
  arrows merging into heat flowing cold-to-hot unaided; (3) the same loop run backward as a
  refrigerator, arrow widths showing $Q_h = |Q_c| + \Won^{\mathrm{net}}$.
- **Quiz bank outline** — `Q-07-1` (multiple-choice; OBJ-07-1) match hypothetical devices to
  the statement each violates. `Q-07-2` (free; OBJ-07-1) outline the composition proof of
  equivalence. `Q-07-3` (numeric; OBJ-07-2) per-leg ledger and $\eta$ for a given Carnot
  cycle. `Q-07-4` (multiple-choice; OBJ-07-2, OBJ-07-3) why $\eta < 1$ for the frictionless
  engine — distractor: `efficiency-loss-is-friction`. `Q-07-5` (multiple-choice; OBJ-07-7)
  the refrigerator ledger — distractor: `refrigerator-violates-second-law`. `Q-07-6` (numeric;
  OBJ-07-4) sign and value of the Clausius sum for a stated two-reservoir cycle. `Q-07-7`
  (numeric; OBJ-07-5) $\Delta S = N \kB \ln 2$ for isothermal doubling. `Q-07-8`
  (multiple-choice; OBJ-07-6) classify four processes as reversible/irreversible — distractor:
  `reversible-just-backward`. `Q-07-9` (multiple-choice; OBJ-07-3) which engines the Carnot
  bound constrains — distractor: `carnot-universal-number`. `Q-07-10` (numeric; OBJ-07-7)
  Carnot COP of a heat pump between given temperatures. Every OBJ-07-K covered at least once.
- **Problem set outline** — `07-second-law-problems.md`: analytical — (P1) prove Kelvin ⇔
  Clausius in both directions [OBJ-07-1]; (P2) Otto efficiency $\eta = 1 - r^{1-\gamma}$ from
  the ledger [OBJ-07-2]; (P3) show $1/T$ is an integrating factor for $\dbar Q_{\mathrm{rev}}$
  of the ideal gas [OBJ-07-5]. Computational — (P4) build a three-leg cycle, verify ledger
  closure and `clausius_sum` $\to 0$ [OBJ-07-4, OBJ-07-6]; (P5) sweep constructed engines
  against the bound [OBJ-07-3]. Challenge — (P6) endoreversible Curzon–Ahlborn engine:
  derive $\eta_{\mathrm{CA}} = 1 - \sqrt{T_c/T_h}$ at maximum power, compare with real plant
  data [advanced flavour; OBJ-07-2, OBJ-07-3].
- **Runtime budget** — deterministic 1-D quadrature only: legs of ≤ 2049 samples, cycles of
  ≤ 8 legs; no particles, no Monte Carlo. Every constructor update recomputes the full ledger
  in well under 50 ms in Pyodide (vectorized NumPy; Numba unavailable and unneeded). Cycle
  animations are pre-rendered MP4s (~200 frames), not computed in the browser.
- **Validation gates** — the standard per-module commands (README bottom) with
  `--module 07-second-law`; plus `pytest tests/physics -k cycles -q` green before content.
- **Open questions for the author** — (1) allow legs touching intermediate-temperature
  reservoirs in the constructor? Recommendation: yes — the Clausius inequality already covers
  multi-reservoir cycles; keep the quantitative multi-reservoir bound out of core. (2) should
  `stirling_cycle` model a regenerator (which would reach $\eta_C$)? Recommendation: no —
  non-regenerative in core, regenerator discussed in the advanced box. (3) thermodynamic
  temperature: full functional-equation derivation or compressed argument? Recommendation:
  compressed half-page in derive, functional-equation detail in advanced. (4) include the
  Stirling desk toy as a purchase-optional aside? Recommendation: yes, one paragraph,
  explicitly qualitative.

## 4. Library and tests

- **`src/thermolab` — existing used:** `paths.py` — `Path`, `join`, `isothermal_path`,
  `adiabatic_path`, `isobaric_path`, `isochoric_path`, `work_on_gas`, `ideal_gas_temperature`,
  `isothermal_work_on_gas`, `adiabatic_work_on_gas`, and `work_by_system` (whose docstring
  already reserves it for exactly this module's labeled aside); 06's planned extensions —
  polytropic paths, the process ledger, `free_expansion`, `sudden_compression`;
  `constants.K_B`.
- **`src/thermolab` — new: `cycles.py`** (introduced by 07 per the ownership table; extended
  by no one; serves 07, 09, 10). Docstring headed by the 7-bullet model spec in §3. Sketch:
  `Cycle(legs: tuple[Path, ...])` — frozen dataclass; validates that consecutive legs meet and
  the composite closes (via `paths.join` + `is_closed`); `ledger()` returns per-leg
  (label, W_on, Q, dU); `reversed()` returns the cycle run backward.
  `efficiency(cycle, degrees_of_freedom=3) -> float` — $\eta = -\Won^{\mathrm{net}} / Q_h$
  with $Q_h$ the sum of positive per-leg heats. `cop_refrigerator(cycle, ...) -> float` /
  `cop_heat_pump(cycle, ...) -> float` — $Q_c/\Won^{\mathrm{net}}$ and $Q_h$-delivered per
  work input for a backward-run cycle. `carnot_cycle(t_hot, t_cold, n_particles, v_start,
  expansion_ratio, gamma=5/3, n_points=513) -> Cycle` — two isotherms + two adiabats with
  junctions solved from $T V^{\gamma-1} = \text{const}$. `carnot_efficiency(t_hot, t_cold) ->
  float` — $1 - T_c/T_h$, the analytic reference. `otto_cycle(...) -> Cycle` — two adiabats +
  two isochores, parameterised by compression ratio. `stirling_cycle(...) -> Cycle` — two
  isotherms + two isochores, non-regenerative. `clausius_sum(cycle, degrees_of_freedom=3,
  reservoir_temperatures=None) -> float` — $\oint \dbar Q / T$ by leg-wise quadrature, with
  $T$ the gas temperature on quasistatic legs and an explicitly supplied reservoir temperature
  on endpoint-jump legs (keeping "T of what?" visible). `entropy_change(state_a, state_b,
  n_particles, degrees_of_freedom=3) -> float` — $\Delta S$ by constructing a reversible
  isotherm+adiabat connection and integrating $\dbar Q_{\mathrm{rev}}/T$.
- **`tests/physics/` additions:** dimensional — `entropy_change` and `clausius_sum`
  re-evaluated with pint carry $\mathrm{J\,K^{-1}}$; `efficiency`/COP dimensionless.
  conservation — every constructed cycle's ledger closes: per-leg dU sums to 0 and
  $Q^{\mathrm{net}} + \Won^{\mathrm{net}} = 0$ to float tolerance. analytic-limit —
  `efficiency(carnot_cycle(...))` → `carnot_efficiency` within quadrature tolerance;
  `efficiency(otto_cycle(r))` → $1 - r^{1-\gamma}$; `clausius_sum(carnot_cycle)` → 0;
  `cop_refrigerator(carnot.reversed())` → $T_c/(T_h - T_c)$; `entropy_change` matches
  $N \kB [\ln(V_b/V_a) + \tfrac{f}{2}\ln(T_b/T_a)]$. convergence — `clausius_sum` and
  `efficiency` errors fall ~4× per doubling of `n_points` (second-order trapezoid, measured
  as in `work_along`). large-N — n/a: macroscopic module, no particle ensembles.
  seed-independence — n/a: fully deterministic, no RNG anywhere in `cycles.py`.

## 5. Assessment hooks

Checkpoint synthesis: (a) 05+06+07 capstone — three routes between the same two states, each
with different W and Q (05/06) but identical $\Delta S$ (07): the state-vs-path-function story
closed in one table; (b) 07↔08 — compute the free-expansion $\Delta S$ twice, by reversible
replacement ($N \kB \ln 2$) and by counting (08's multiplicity doubling), and note the
agreement the formal verify-bridge (08's gap item) will later test in code. Exam themes:
cycle-ledger analysis, equivalence and composite-engine proofs, Clausius-sum sign reasoning.
Feeds forward: 09's entropy-surface capstone consumes `entropy_change`; 10 re-derives the
Carnot bound from maximum work; 14's Clausius–Clapeyron runs a Carnot cycle across the
coexistence dome.

## 6. Build order and validation gates

Builds after 06 and before 09: C1's artifacts (polytropic family, process ledger, irreversible
endpoint models) are hard imports here, and 09's `fundamental.py` consumes `cycles.py` — so the
sequence 06 → 07 → 09 is forced. Landing 07 also unblocks 08's recorded gap items (the
$\kB \ln \Omega \leftrightarrow \int \dbar Q_{\mathrm{rev}}/T$ verify-bridge and the mixing
teaser). Alongside the module: the seven NEW glossary keys land in `glossary/terms.yml` with
their `he_reject` candidates; the three NEW misconception entries land in
`assessment/misconceptions.yml` with `assigned_module: 07-second-law`. Artifact family: EN page
+ `07-second-law-problems.md` + lab notebook + quiz banks
(`assessment/quizzes/07-second-law.en.yml` / `.he.yml`) + HE mirrors stamped with
`en_source_hash`; the page is listed in `translation-pending.txt` until the mirror lands.
Gates: the six README commands with `--module 07-second-law`.

## 7. Deviations from the brainstorm

- **C2 entropy split applied:** the brainstorm's row 8 lists "Clausius entropy" under module
  8; the built 08 is purely statistical, so this module takes the Clausius definition and
  inequality (via `cycles.py`) and defers all entropy-production machinery to 09 — preserving
  the §2 spiral: macroscopic → statistical → structural.
- **Licensed sign-convention exception:** the module body keeps
  $\mathrm{d}U = \dbar Q + \dbar \Won$ throughout; exactly one labeled admonition presents
  $W_{\mathrm{by}} = -\Won$ and $\eta = W_{\mathrm{by}}^{\mathrm{net}}/Q_h$ as the
  engine-literature convention and converts back, per `content/en/conventions.md` — the single
  exception invariant 1 licenses.
- **Additions beyond the brainstorm row:** quantitative COP for refrigerators/heat pumps, the
  thermodynamic-temperature step, and the Curzon–Ahlborn advanced section — all natural
  closures of the row's "engines and refrigerators … efficiency bounds" scope.
- **Centrepiece unchanged:** the engine constructor vs the Carnot bound is the brainstorm's
  centrepiece verbatim, enriched with 06's polytropic and irreversible legs.
