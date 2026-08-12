# Module 01 — Thermal equilibrium — Implementation Plan

> **Brainstorm:** §3 module 1 (+ §4 notebook rhythm, §6 misconceptions, §8 assessment).
> **Module id:** `01-equilibrium`. **Content path:** `content/en/thermodynamics/01-equilibrium.md`.
> **Status:** built.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

The first physics module, and the course's first micro-to-macro bridge: two Einstein solids
exchange energy quanta one random hop at a time, and out of nothing but "a random exchange,
more likely from the fuller side" the macroscopic laws emerge — relaxation onto
$T_{\text{eq}} = (C_A T_{A,0} + C_B T_{B,0})/(C_A + C_B)$ from energy conservation alone, and
the exponential approach $T_A(t) - T_B(t) = (T_{A,0} - T_{B,0})\, e^{-t/\tau}$ with
$\tau = C_A C_B / (\kappa\,(C_A + C_B))$ from Newton's law of cooling. The zeroth law is
staged as the empirical axiom that makes temperature transitive, hence well-defined. The
boundary is rigid, so all transfer is heat ($dU = \dbar Q$ here; the full
$dU = \dbar Q + \dbar \Won$ ledger waits for 05).

The quiet centrepiece is exactness: the hop rule makes $\mathbb{E}[\Delta q_A]$ *exactly*
linear in $q_A$ (total quanta $Q$ never changes), so the expected gap decays as the geometric
$(1 - 1/Q)^n$ — the discrete law is the ODE's mathematics, not an approximation of it. The
page keeps the epistemic line sharp: the simulation illustrates the macroscopic law's
robustness to microscopic detail; it does not prove it for real contacts. This opens the C4c
Einstein-solid spiral — 01 (energy exchange) → 09 (its S(U,N) fundamental relation and
entropy ledger) → 12 (oscillator Z reproduces this module's temperature map) → 16 (Einstein
heat capacity) — and pre-answers, dynamically, what 08 answers combinatorially.

## 2. Position in the course

- **Requires:** 00 — the $N^{-1/2}$ law (`OBJ-00-3`), read straight off the lab's Part 3
  spread-scaling fit; mean/variance and seed-study honesty (`OBJ-00-2`) via
  `validation.seed_study`; SI conventions and dimensional checking (`OBJ-00-4`).
- **Feeds:** 09 — extends `equilibrium.py` with an entropy ledger on `ExchangeResult`
  (per-hop $\Delta S$ answers the puzzle's "why exactly at equality"); 12 — the oscillator
  partition function recomputes 01's temperature map $T = q\,\varepsilon/(n \kB)$ from $Z$;
  16 — Einstein heat capacity pays off the constant-$C$ approximation box; 08 — meets the
  same relaxation combinatorially, with no rate equation in sight.
- **Explicitly not assumed:** first-law formalism and $P$–$V$ work (05); entropy and
  multiplicity (08); kinetic theory (04); quantum statistics (17) — the model *names* its
  low-$T$ failure mode without explaining it.

## 3. Module specification

**As-built summary.** The page ships the full contract — `puzzle → predict → explore →
derive → verify → transfer → quiz → explain` plus a genuinely skippable `advanced` — under
`(01-equilibrium-<suffix>)=` labels, with objectives `OBJ-01-1..5` (zeroth law; equilibrium
as balanced not stopped exchange; weighted-average T_eq; exponential relaxation and tau; what
the simulation does and does not establish). Epistemic boxes: *empirical-law* twice (zeroth
law, Newton's cooling), *approximation* (constant $C$, pointing at 16), *model-assumption*
twice (mechanism ≠ real conduction; `from_temperatures` rounding), *numerical-observation*
(the exact discrete correspondence), *open-question* (what agreement does not prove),
*definition* (relaxation time). Both registry misconceptions are staged as designed:
`instant-equilibrium` (predict Q3, falsified by the finite-tau relaxation the lab measures,
distractor in `Q-01-2`) and `equal-weight-equilibrium` (predict Q1, falsified by the lab's
Part 2 unequal-size measurement, distractor in `Q-01-4`). The lab (5 parts) runs relaxation,
measures T_eq against the weighted average, fits the spread-vs-$Q$ exponent (~ -0.5), re-runs
the suite's own assertions in Part 4, and ends with sliders plus a reflection cell. The quiz
bank (`Q-01-1..8`: MC, numeric, prediction, short-answer) covers every objective; the problem
set (6, objective-tagged) spans zeroth-law reading, calorimetry, the tau derivation, forensic
cooling, model breakdown, and a computational finale on `thermolab.equilibrium`. Media:
`render_equilibrium.py` renders `equilibrium-relaxation.mp4` and
`equilibrium-fluctuations.mp4` from the library itself, language-neutral (generated
`content/*/media/` is gitignored by design).

**Gap list**

1. **Hebrew mirror pending (tracked).** `translation-pending.txt` lists this module's page,
   problems, and lab; only the quiz bank (`01-equilibrium.he.yml`) is mirrored. Close by
   translating all three using `glossary/terms.yml` terminology only (keys already present:
   `equilibrium`, `thermal-equilibrium`, `zeroth-law`, `relaxation-time`, `energy-quantum`,
   `thermal-contact`), stamping each with its `en_source_hash`, and deleting the three lines
   from `translation-pending.txt` so `check_parity.py` goes green.
2. **Brainstorm-row shortfall: systems, boundaries, state variables.** The page treats system
   and boundary only operationally (model spec, derive) — no open/closed/isolated wall
   taxonomy, and "state variable" never appears. Decide: a short definitions passage in 01,
   or explicit deferral to 02 (which owns intensive/extensive); record the outcome in §7.
3. **Forward-pointer seeds owed to the C4c spiral.** The transfer section's four targets are
   all real-world; none seeds 09 (entropy will answer the puzzle's own question), none seeds
   12 ($Z$ recomputes the $T = q\,\varepsilon/(n \kB)$ map), and 16 appears only in the
   derive-section approximation box. Add transfer bullets.
4. **Cross-reference tense.** The page cites modules 4 and 8 in past tense ("module 4
   asked", "module 4 met… module 8 met") though both come later — reword as forward pointers.
5. **Real-experiment counterpart absent.** The natural cheap pairing (cooling curve of hot
   water in a mug, fit tau) has no import cell in the lab; add one, or declare "none
   practical" explicitly on the page.

**Validation gates:** the README per-module block with `--module 01-equilibrium`; until gap 1
closes, `check_parity.py` correctly reports the three mirrors as PENDING.

## 4. Library and tests

- **Existing used:** `constants.K_B`; `validation.seed_study` / `scaling_exponent` (lab and
  suite); `multiplicity.sample_two_box` cited as the Ehrenfest-urn cousin.
- **Introduced — `src/thermolab/equilibrium.py`** (owner 01; extender 09 per README), headed
  by the 7-bullet model-spec docstring:
  - `TwoBodyState(n_a, n_b, q_a, q_b, quantum)` — frozen, validated; derives $C = n\,\kB$,
    $T = q\,\varepsilon/(n \kB)$, `total_quanta`, `total_oscillators`.
  - `from_temperatures(n_a, n_b, t_a, t_b, quantum) -> TwoBodyState` — rounds to integer
    quanta; realised $T$ off by $O(\varepsilon/(n \kB))$, caveat documented.
  - `equilibrium_temperature(c_a, t_a, c_b, t_b) -> float` — weighted average, mechanism-free.
  - `ExchangeResult(steps, q_a, initial)` — per-step record; derives `q_b`, temperatures,
    `final_state`. The type 09's entropy ledger extends.
  - `simulate_energy_exchange(state, n_steps, rng) -> ExchangeResult` — single-quantum hops;
    conserves $Q$ by construction; explicit `rng`, no global state.
  - `predicted_relaxation(state, steps) -> ndarray` — exact $\Delta T_0\,(1 - 1/Q)^n$ form.
  - `relaxation_time(state) -> float` — $\tau = -1/\ln(1 - 1/Q) \to Q$; implicit per-step
    conductance $\kappa = \kB / Q$.
- **`tests/physics/` coverage (all six categories, no additions owed):** dimensional —
  `test_dimensions.py` (plain SI floats; pint check that T_eq is a temperature);
  conservation — `test_conservation.py::test_energy_exchange_conserves_total_quanta`
  (hypothesis property); analytic-limit — `test_limits.py` (known T_eq cases; long-run T_eq;
  mean gap matches `predicted_relaxation` at one tau); large-N —
  `test_scaling.py::test_equilibration_gets_more_predictable_as_the_bodies_grow`;
  convergence — `test_convergence.py` (time-averaged $T_A$ tightens onto T_eq as the window
  grows); seed-independence — `test_seeds.py` (same-seed reproducibility, different-seed
  divergence, cross-seed agreement with the closed form).

## 5. Assessment hooks

- **Checkpoint themes:** calorimetry as the inverse problem (measure an unknown $C$);
  forensic cooling (problem 4) as the exam-style relaxation inversion; "a thermometer barely
  disturbs what it measures" (lab Part 5) — the small/large-body limit seeding 11's finite
  heat bath.
- **Feeds later synthesis:** 09 replays this module's exchange trajectories and reads the
  entropy ledger off them; 12 closes the loop by deriving the oscillator $U(T)$ from $Z$;
  16 answers problem 5(a) quantitatively with the Einstein $C_V(T)$.

## 6. Build order and validation gates

Built — teaching slot 1, directly after 00; the library file, both misconception registry
entries (`status: addressed`), and all glossary terms landed with it. **Remaining work
item:** HE completion (§3 gap 1) — translate page + problems + lab, stamp `en_source_hash`,
empty this module's lines from `translation-pending.txt`, then re-run the gates:
`check_modelspec.py --module 01-equilibrium`, `check_assessment.py`, `check_glossary.py`,
`check_parity.py`, `pytest tests/physics -q`, `validate_all.py --module 01-equilibrium`.

## 7. Deviations from the brainstorm

- **Centrepiece sharpened:** "two bodies exchanging energy" is built specifically as Einstein
  solids to arm the 01 → 09 → 12 → 16 spiral (C4c) — additive, not a re-scope.
- **Dynamics added:** Newton's cooling, $\tau$, and the exact discrete correspondence go
  beyond the row's static topic list — the module gains a "how fast", not just a "where".
- **State-variable vocabulary deferred (pending §3 gap 2):** intensive/extensive and the
  state-variable taxonomy sit naturally with equations of state in 02.
- **Media per C4d:** language-neutral MP4s rendered from the library by
  `render_equilibrium.py`; captions live in translated page prose, not burned into frames.
