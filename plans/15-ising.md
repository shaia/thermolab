# Module 15 — Phase transitions — Implementation Plan

> **Brainstorm:** §3 module 15 (+ §5 phase-transition laboratory's Ising half, §6 misconceptions,
> §7 accuracy framework, §8 assessment). **Module id:** `15-ising`.
> **Content path:** `content/en/advanced/15-ising.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Heat a piece of iron past 770 °C and it forgets which way it was magnetized; cool it back down and
it *must* choose a direction again — yet nothing in its energy function prefers up over down. Who
chooses? That is spontaneous symmetry breaking, and this module refuses to wave at it: the
canonical ensemble average says $m = 0$ by symmetry at every temperature, while the actual sample
on the bench magnetizes anyway. The resolution — ergodicity breaking in the thermodynamic limit —
is told honestly at finite N through *timescales*: below $T_c$ the time to cross between the $+m$
and $-m$ branches outgrows any simulation (and any lab), so a single sample lives in one branch
while the ensemble average keeps averaging over both.

The centrepiece is a live 2-D Metropolis Ising simulation swept through $T_c$, and the brainstorm
§5 demand is a contract, not a wish list: students must *see* hysteresis (field sweeps below
$T_c$), finite-size effects (the same transition rounded differently at L = 16, 32, 64), and
critical slowing down (autocorrelation time blowing up near $T_c$) — never only a smooth textbook
curve. Earlier ideas get their payoff here: 11's Boltzmann distribution is cashed in when
detailed balance *derives* the Metropolis rule; 12's fluctuation identities are reused verbatim
to read $\chi$ and $C$ out of variances; 14's first-order-vs-continuous language finally shows a
continuous transition in the flesh; 03's correlated-walk counterexample returns as the
autocorrelation time that decides how many Monte Carlo samples are actually independent.

The module is also the course's methodological capstone for stochastic computation: every
physics conclusion must carry an error bar, survive a seed change (`validation.seed_study`), and
be checked against an exact anchor (1-D closed forms, Onsager's $T_c$). Its closing intellectual
gift is universality — wildly different systems sharing the same critical exponents — planted as
a stated wonder, with the renormalization group explicitly left outside the course.

## 2. Position in the course

- **Requires:** `11-ensembles` — the Boltzmann distribution $p_s \propto e^{-E_s/(\kB T)}$ as the
  canonical stationary law (Metropolis is derived from it via detailed balance);
  `12-partition-functions` — the fluctuation identities $C = \mathrm{Var}(E)/(\kB T^2)$ and the
  paramagnet model (the h-only Ising limit is 12's paramagnet); `14-coexistence` — first-order
  vs continuous vocabulary, latent heat, and the critical point on the vdW dome;
  `03-random-walks` — sample averages with error bars, and the correlated-walk counterexample
  that autocorrelation time generalises.
- **Feeds:** nothing downstream consumes `ising.py` (terminal on this branch), but the module
  seeds *universality* as the course's closing intellectual gift, and `18-fluctuations-transport`
  reuses the correlation-time language (how long until samples are independent) for
  time-correlation functions.
- **Explicitly not assumed:** renormalization group (out of scope for the whole course — see
  §7); quantum spin (17's territory; $s_i = \pm 1$ is classical by fiat); Markov-chain theory
  beyond "this update rule has that stationary distribution"; finite-size *scaling theory* (the
  phenomenon is core, the data-collapse machinery is advanced-only).

## 3. Module specification

- **Identity and scope** — brainstorm row 15 in full: order parameters, symmetry breaking, the
  Ising model, critical behaviour, Monte Carlo simulation; plus the Ising half of the §5
  phase-transition laboratory (hysteresis, finite-size effects, critical slowing down — all
  three required deliverables). Deferred: renormalization group and exact finite-size scaling
  theory (advanced section names them, course never teaches them); vdW coexistence machinery
  stays in 14; quantum magnetism → 17 and beyond the course.
- **Prerequisites** — 11: Boltzmann distribution and the finite-bath argument behind it; 12:
  $C = \mathrm{Var}(E)/(\kB T^2)$ and the two-level paramagnet; 14: continuous-vs-first-order
  classification and "critical point"; 03: standard error of a mean and why correlated samples
  break the $N^{-1/2}$ count.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-15-1`: Write the Ising energy E = -J sum_<ij> s_i s_j - h sum_i s_i, define the order
    parameter m = (1/N) sum_i s_i, and state the up-down symmetry of the h = 0 model and what
    "spontaneously broken" means for it.
  - `OBJ-15-2`: Derive the Metropolis acceptance rule A = min(1, e^(-DeltaE/(k_B T))) from
    detailed balance with respect to the Boltzmann distribution, and explain why the chain
    samples equilibrium rather than simulating the magnet's real time evolution.
  - `OBJ-15-3`: Explain, via the domain-wall free energy DeltaF = 2J - k_B T ln N, why the 1-D
    Ising chain has no phase transition at any T > 0.
  - `OBJ-15-4`: Derive the mean-field self-consistency equation m = tanh((q J m + h)/(k_B T)),
    extract k_B T_c^MF = q J, and quantify how badly mean field misses Onsager's exact 2-D
    result k_B T_c = 2 J / ln(1 + sqrt(2)) ~ 2.269 J.
  - `OBJ-15-5`: Estimate <|m|>, chi = N Var(m)/(k_B T), and C from Monte Carlo traces using the
    fluctuation identities, and locate T_c from the susceptibility peak.
  - `OBJ-15-6`: Describe hysteresis, finite-size rounding, and critical slowing down
    operationally — m lags a swept field below T_c; the transition sharpens as L grows; the
    autocorrelation time peaks at T_c — and state what finite-L simulations can and cannot
    establish about the N -> infinity singularity.
  - `OBJ-15-7`: Attach a defensible uncertainty to a Monte Carlo observable using the
    autocorrelation time (N_eff = N_samples/(2 tau)) and independent-seed studies, and reject
    conclusions that do not survive a seed change.
- **Mathematical background** — already has: probability, variance, exponentials, tanh, log-log
  power-law reading (00/03/12). New here, at working level only: a Markov chain as
  "update rule + stationary distribution"; the autocorrelation function of a trace; reading a
  power law $|m| \sim (T_c - T)^{\beta_{\mathrm{exp}}}$ off data near a critical point.
- **Physical intuition goals** — student can predict, without algebra: (1) below $T_c$ at h = 0
  a large lattice stays magnetized one way for longer than any run, though $+m$ and $-m$ are
  exactly equally probable in the ensemble; (2) heating melts the order *continuously* — no
  latent heat, unlike 14's boiling; (3) equilibration is slowest *at* $T_c$, not deep in either
  phase; (4) the smooth m(T) shoulder at L = 16 is a finite-size artefact — L = 64 is visibly
  sharper, and no finite L is truly singular.
- **Section skeleton seeds** — contract order:
  - *puzzle:* iron heated past 770 °C forgets its magnetization; cooled, it must re-choose —
    boxed question: the energy function is exactly symmetric under flipping every spin, so who
    chooses the direction, and where did the symmetry go?
  - *predict:* (1) cool to T well below T_c at h = 0 — is the equilibrium sample's m zero,
    ±full, or history-dependent? (targets `ensemble-cancellation`); (2) at which T does the
    simulation take longest to settle: T << T_c, T = T_c, or T >> T_c? (targets
    `critical-fastest-settling`); (3) is m(T) for L = 16 sharper or smoother than for L = 64?;
    (4) below T_c, sweep h from +0.5 to -0.5 and back — does m(h) retrace or loop?
  - *explore:* live lattice, L selector {16, 32, 64}, T slider 1.0–4.0 (units of $J/\kB$)
    crossing $T_c \approx 2.269$, h slider −1..+1, quench button (equilibrate hot, drop T
    cold, watch domains coarsen), live m and E traces with a $\tau$ readout.
  - *derive:* the six-step route under core derivations — Hamiltonian, Metropolis from
    detailed balance, 1-D no-transition, mean field, Onsager anchor, critical phenomenology.
  - *verify:* 1-D simulation vs exact closed forms (seed study, 3-sigma); 2-D susceptibility
    peak location vs L bracketing Onsager's $T_c$ within finite-size drift (the module's
    flagship `numerical-observation` box); incremental energy bookkeeping vs full recompute;
    explicit statement of what the simulation *cannot* prove (the N → ∞ transition).
  - *transfer:* back to 11 (Metropolis is the Boltzmann distribution made executable), 12
    (fluctuation identities reused unchanged; h-only limit is the paramagnet), 14 (h-sweep
    below T_c is a first-order line ending at a critical point — same anatomy as the vdW
    dome), 03 (autocorrelation = the correlated-walk lesson); forward to 18 (correlation
    times); outward: universality — liquid-gas and binary-alloy critical points share Ising
    exponents (stated wonder, `numerical-observation`-grade citation, no derivation).
  - *quiz:* symmetry and order parameter; acceptance-rule computation; what MC time is;
    1-D argument; mean-field vs Onsager; fluctuation-identity reads; where τ peaks; what a
    magnetometer reads below T_c; what finite L proves.
  - *explain:* (1) why a simulation can never prove a phase transition exists; (2) who chooses
    the magnetization direction, in your own words; (3) why "Metropolis time" is not physical
    time; (4) why the 1-D chain refuses to order but the 2-D lattice does not.
  - *advanced (optional, always last):* finite-size scaling done properly — data collapse with
    the exact 2-D exponents beta = 1/8, gamma = 7/4, nu = 1; the 1-D transfer matrix in full;
    Wolff cluster updates named as the cure for critical slowing down (not implemented).
    Safe-to-skip boundary: core verify uses only peak *location* vs L; no core content or
    later module depends on exponent values or cluster algorithms.
- **Core derivations** — ordered:
  1. Model (`model-assumption` box): $E = -J \sum_{\langle ij \rangle} s_i s_j - h \sum_i s_i$,
     $s_i = \pm 1$, nearest neighbours, periodic boundaries; order parameter (definition)
     $m = \frac{1}{N} \sum_i s_i$. At h = 0, E is invariant under $s_i \to -s_i$ for all i.
  2. Metropolis from detailed balance (`theorem`, given 11): imposing
     $p_s P(s \to s') = p_{s'} P(s' \to s)$ with $p_s \propto e^{-E_s/(\kB T)}$ is satisfied by
     the acceptance $A = \min\!\big(1, e^{-\Delta E/(\kB T)}\big)$; stationarity of the
     Boltzmann distribution follows. Explicitly flagged: this fixes *where* the chain goes,
     not *how fast* — the dynamics is an algorithmic choice (feeds `mc-is-real-dynamics`).
  3. No 1-D transition (`theorem`): a single domain wall costs $\Delta E = 2J$ but can sit at
     N places, so $\Delta F = 2J - \kB T \ln N < 0$ for large N at any T > 0 — entropy always
     buys walls, order is destroyed. Exact anchors stated for verify: at h = 0,
     $E/N = -J \tanh\!\big(J/(\kB T)\big)$; in a field,
     $m = \sinh(h/(\kB T)) \big/ \sqrt{\sinh^2(h/(\kB T)) + e^{-4J/(\kB T)}}$
     (transfer-matrix proof relegated to advanced).
  4. Mean field (`approximation` box): replace neighbours by the average field →
     $m = \tanh\!\big((qJm + h)/(\kB T)\big)$, nontrivial solutions below
     $\kB T_c^{\mathrm{MF}} = qJ$ (q = 4 in 2-D, so $4J$). Where mean field lies: it predicts
     a transition even in 1-D (q = 2) where none exists, and overshoots 2-D by ~76%.
  5. Onsager anchor (`theorem`, stated without proof, referenced):
     $\kB T_c = \dfrac{2J}{\ln(1 + \sqrt{2})} \approx 2.269\,J$ — the exact 2-D h = 0 result,
     the module's reference value for every numerical bracket.
  6. Critical behaviour, phenomenologically: near $T_c$, $|m| \sim (T_c - T)^{\beta_{\mathrm{exp}}}$
     below, $\chi$ peaks and grows with L, $\tau$ blows up; universality named as the payoff
     (same exponents across systems); honest flag that extracting exponents at finite L needs
     finite-size scaling — advanced only.
- **Model specification draft** — for the Metropolis simulation (page + lab + `ising.py`):
  - **System:** an L × L square lattice of N = L² classical spins $s_i = \pm 1$ with
    nearest-neighbour coupling J > 0, uniform field h, periodic boundaries.
  - **Dynamics:** Metropolis Markov chain — checkerboard half-lattice proposals accepted with
    $\min(1, e^{-\Delta E/(\kB T)})$; a sampling scheme, not equations of motion.
  - **Boundary:** periodic (no edges); T and h imposed externally by an implicit bath.
  - **Ensemble:** canonical at temperature T — the chain's stationary distribution, by
    detailed balance.
  - **Ignored:** quantum spin, lattice vibrations, dipolar long-range forces, anisotropy,
    disorder, and real domain-wall pinning — everything that makes a real magnet a material.
  - **Valid when:** the chain has run long past burn-in and past $\tau(T)$ — the
    equilibrium-sampling regime; fast away from $T_c$ at moderate L.
  - **Failure modes:** near $T_c$, $\tau$ diverges with L (critical slowing down) — traces
    stay correlated and error bars are illusory without $N_{\mathrm{eff}}$; below $T_c$ at
    small |h| the chain traps in one magnetization branch (practical ergodicity breaking);
    skipping burn-in or thinning biases every observable.
- **Epistemic classification** — boxed claims: Hamiltonian → `model-assumption`; order
  parameter → `definition`; Metropolis samples Boltzmann → `theorem` (given 11); 1-D
  no-transition → `theorem`; mean-field self-consistency → `approximation`; Onsager $T_c$ →
  `theorem` (stated, not proven — reference anchor); $\chi$-peak drift bracketing Onsager,
  measured $\tau(T)$ peak, and the universality citation → `numerical-observation`; "does a
  finite simulation ever exhibit a phase transition?" → `open-question` box resolving to: the
  singularity is a statement about N → ∞ — finite runs give evidence, never proof.
- **Misconceptions** — no existing registry entry belongs here (11 and 12 take the pending
  canonical/negative-T ones); three NEW entries (ids collide with nothing in
  `assessment/misconceptions.yml`):
  - `critical-fastest-settling` · "At T_c the system settles fastest because it is 'between'
    phases." · falsifier: measure τ(T) across the sweep — the autocorrelation time *peaks* at
    T_c (critical slowing down), lab cell plots it · distractor: Q-15-7 option "fastest at
    T_c, since neither phase holds it back".
  - `ensemble-cancellation` · "Below T_c the equilibrium magnetization is m = 0 because up and
    down samples cancel." · falsifier: single runs hold |m| near 1 for the entire run while
    the branch-crossing time explodes with N; hysteresis loop shows history dependence —
    ensemble average ≠ single-sample reading · distractor: Q-15-8 option "a magnetometer reads
    zero below T_c at h = 0".
  - `mc-is-real-dynamics` · "Monte Carlo simulates the magnet's real time evolution." ·
    falsifier: run random-site and checkerboard updates side by side — different relaxation
    curves, identical equilibrium observables; the dynamics is an algorithm choice
    (model-assumption box) · distractor: Q-15-3 option "sweeps convert to seconds via a
    physical constant".
- **Glossary terms** — reused: `spin`, `ergodicity`, `critical-point` (02), `heat-capacity`.
  NEW (key / en / suggested he / `he_reject`):
  - `ising-model` / Ising model / מודל איזינג / [מודל אייזינג]
  - `order-parameter` / order parameter / פרמטר סדר / —
  - `symmetry-breaking` / spontaneous symmetry breaking / שבירת סימטריה ספונטנית / —
  - `magnetization` / magnetization / מגנוט / [מגנטיזציה]
  - `ferromagnet` / ferromagnet / פרומגנט / [פרו-מגנט]
  - `monte-carlo` / Monte Carlo method / שיטת מונטה קרלו / [מונטה-קרלו]
  - `metropolis` / Metropolis algorithm / אלגוריתם מטרופוליס / —
  - `detailed-balance` / detailed balance / איזון מפורט / —
  - `susceptibility` / magnetic susceptibility / סוספטיביליות מגנטית / [סוסצפטיביליות]
  - `hysteresis` / hysteresis / היסטרזיס / [היסטרסיס]
  - `critical-slowing-down` / critical slowing down / האטה קריטית / —
  - `autocorrelation-time` / autocorrelation time / זמן אוטוקורלציה / —
  - `universality` / universality / אוניברסליות / —
  - `domain-wall` / domain wall / קיר תחום / [דופן תחום]
  - `curie-temperature` / Curie temperature / טמפרטורת קירי / [טמפרטורת קורי]
- **Interactive controls and simulations** — (1) *lattice explorer* (centrepiece): live spin
  image, T and h sliders, L selector, quench button, rolling m and E traces, τ readout. (2)
  *T-sweep experiment:* scripted sweep over ~30 T points for L ∈ {16, 32, 64}; plots <|m|>(T),
  χ(T), C(T) with error bars, peak markers vs the Onsager line. (3) *hysteresis rig:* h swept
  ±0.5 at fixed T < T_c and T > T_c; loop area vs sweep rate and T. (4) *slowing-down meter:*
  τ(T) across the sweep, log scale, peak at T_c.
- **Virtual lab outline** — `notebooks/en/labs/15-ising.ipynb`: (1) setup — import `ising`,
  `validation`; reduced-units note (T in $J/\kB$); (2) prediction cells (commit before
  running); (3) build a state, watch `metropolis_sweep` order/disorder it at T = 1.5 vs 3.5;
  (4) 1-D warm-up: simulate a chain, compare <E>/N and m(h) to `ising_1d_exact` via
  `seed_study` (falsifies nothing, calibrates trust); (5) 2-D T-sweep for L ∈ {16, 32, 64} —
  <|m|>, χ, C with burn-in and thinning; (6) read T_c(L) off the χ peak, watch it drift toward
  `onsager_tc()` as L grows; (7) τ(T) measurement (falsifies `critical-fastest-settling`);
  (8) hysteresis loop below T_c + branch-trapping run (falsifies `ensemble-cancellation`);
  (9) update-rule swap (falsifies `mc-is-real-dynamics`); (10) *measurement:* T_c = value ±
  error from the L = 64 χ peak (seed-study spread + finite-size drift stated separately),
  quoted against 2.269 J/k_B.
- **Real-experiment counterpart** — none practical: microscopic spins and exchange couplings
  are invisible on a bench, and no cheap apparatus reaches a clean magnetic phase transition.
  Honest pairing (recommended, optional import): published magnetization-vs-temperature data
  for nickel (Curie point 631 K), shipped as a small CSV under `data/`, compared
  *qualitatively* to the mean-field and MC curves — the shape agreement and the near-$T_c$
  disagreement with mean field are both lessons.
- **Media assets** — `media/render/render_ising.py`, language-neutral (no burned-in text):
  `ising-quench.mp4` (hot lattice quenched below T_c, domains coarsening);
  `ising-hysteresis.mp4` (lattice beside its m–h loop while the field sweeps);
  `ising-tc-sweep.mp4` (lattice morphology and building m(T) as T crosses T_c, three L side
  by side — finite-size rounding visible).
- **Quiz bank outline** — every objective covered at least once; ASCII math:
  - `Q-15-1` (multiple-choice, OBJ-15-1): symmetry of the h = 0 energy and what m measures;
    distractor "E prefers all-up because J > 0 favours alignment *upward*".
  - `Q-15-2` (numeric, OBJ-15-2): acceptance probability for DeltaE = 4J at k_B T = 2J.
  - `Q-15-3` (multiple-choice, OBJ-15-2): what one Metropolis sweep corresponds to
    physically; distractor from `mc-is-real-dynamics`.
  - `Q-15-4` (multiple-choice, OBJ-15-3): why 1-D has no transition; distractor "the coupling
    is too weak in one dimension".
  - `Q-15-5` (numeric, OBJ-15-4): mean-field k_B T_c = 4J vs Onsager 2.269J — percent
    overestimate; plus the q = 2 sanity failure.
  - `Q-15-6` (numeric, OBJ-15-5): chi from N, T, and a given Var(m) via chi = N Var(m)/(k_B T).
  - `Q-15-7` (multiple-choice, OBJ-15-6): where equilibration is slowest; distractor from
    `critical-fastest-settling`.
  - `Q-15-8` (multiple-choice, OBJ-15-6): what a magnetometer reads on one sample below T_c at
    h = 0; distractor from `ensemble-cancellation`.
  - `Q-15-9` (numeric, OBJ-15-7): N_eff = N_samples/(2 tau) and the corrected error bar for a
    given trace length and tau.
  - `Q-15-10` (free, OBJ-15-6 + OBJ-15-7): what the L-dependence of the chi peak establishes
    about the thermodynamic limit, and what it cannot.
- **Problem set outline** — `15-ising-problems.md`: *analytical* — detailed-balance derivation
  of Metropolis, including why any A' = c·A with c < 1 also works (OBJ-15-2); domain-wall
  argument, then the 2-D counter-estimate (wall of length ℓ costs 2Jℓ but gains ~kB T ℓ ln 3
  entropy — why the argument only *permits* 2-D order) (OBJ-15-3); mean-field T_c and the
  slope of m(T) just below it (OBJ-15-4). *Computational* — reproduce the χ-peak drift table
  T_c(L) and extrapolate against 1/L (OBJ-15-5/6); measure β_exp from |m|(T) at L = 64 and
  report why the answer is biased (OBJ-15-6/7). *Challenge* — paramagnet limit J = 0: recover
  12's tanh(h/(k_B T)) exactly and reconcile with the 1-D formula (OBJ-15-1/5).
- **Runtime budget** — all Monte Carlo is vectorized NumPy (no Numba in Pyodide). One
  checkerboard sweep at L = 64 (4096 spins) = 2 half-updates, each ~10 whole-array ops
  (4 `np.roll` neighbour sums, exp, uniform draw, mask, apply) on 64 × 64 arrays ≈ 10⁵
  array-element ops per sweep. Interactive lattice: ~200 sweeps/frame ≈ 2 × 10⁷ el-ops —
  smooth. T-sweep experiment: 30 T points × 10³ sweeps for L ∈ {16, 32, 64} ≈ 1.5 × 10⁹
  el-ops dominated by L = 64 — runs in seconds-to-a-minute in Pyodide. L = 128 (4× cost) is
  the flagged patient-mode cap, off by default. Hysteresis and quench *animations* are
  pre-rendered MP4s via `media/render`; the lab recomputes only still curves.
- **Validation gates** — the six README commands with `--module 15-ising`; plus the physics
  suite's stochastic tests must use `validation.seed_study` (no bare single-seed asserts) and
  pass `-m "not slow"` with the reduced sweep counts.
- **Open questions for the author** —
  1. τ estimator: integrated autocorrelation with a self-consistent window vs exponential
     fit. **Recommend:** integrated with window (noisier but assumption-free; the noise is
     itself teachable).
  2. 1-D exact treatment: transfer matrix in core vs domain-wall-only. **Recommend:**
     domain-wall argument in core, closed forms *stated* as anchors, transfer matrix in
     advanced.
  3. Page-side interactivity: JS lattice widget vs MP4 + lab split. **Recommend:** follow 02's
     precedent — MP4 on the page, live widget only in the JupyterLite lab.
  4. Nickel data source: digitized classic Weiss–Forrer-era m(T) data vs schematic curve.
     **Recommend:** ship a small digitized CSV if licensing is clean, else draw schematic and
     say so in the caption.
  5. Wolff algorithm: implement or name-only. **Recommend:** name-only in advanced —
     implementing it would blunt the critical-slowing-down lesson the module exists to teach.

## 4. Library and tests

- **`src/thermolab` — existing used:** `validation.py` — `seed_study`/`SeedStudy` (every
  stochastic assertion), `convergence_study` (burn-in sufficiency), `scaling_exponent`
  (χ-peak growth with L); rng convention from `sampling.py` — every stochastic function takes
  an explicit `np.random.Generator`, never global state. `constants.py` is *not* used: the
  module runs in reduced units (§7).
- **`src/thermolab` — new:** `ising.py` (ownership table: introduced by 15, extended by none,
  serves 15 only). Docstring header, 7 bullets in fixed order — System: L × L classical spins
  ±1, nearest-neighbour J > 0, field h, periodic boundaries / Dynamics: checkerboard
  Metropolis Markov chain — sampling, not motion / Boundary: periodic; T, h external /
  Ensemble: canonical at T by detailed balance / Ignored: quantum spin, long-range forces,
  disorder, real materials / Valid when: run past burn-in and τ(T) / Failure modes: τ
  divergence near T_c, branch trapping below T_c, un-burned-in traces. Reduced units
  throughout: J = 1, temperature = $\kB T / J$, field = $h/J$. Functions:
  - `IsingState` — frozen-ish dataclass: `lattice: np.ndarray` (int8, ±1), `energy: float`,
    `magnetization: float` — totals kept incrementally by every update, never recomputed.
  - `random_state(size: int, rng: np.random.Generator) -> IsingState` /
    `aligned_state(size: int, up: bool = True) -> IsingState` — hot and cold starts.
  - `metropolis_sweep(state, temperature, field, rng) -> IsingState` — one full sweep as two
    vectorized checkerboard half-sweeps: sites of one colour have all four neighbours in the
    other colour, so simultaneous updates never touch a shared bond. Docstring documents why
    plain full-lattice simultaneous updating is wrong: two neighbours flipping together each
    evaluate ΔE against a stale configuration, breaking detailed balance with the Boltzmann
    distribution (canonical failure: it converges to the wrong ensemble).
  - `simulate(state, temperature, field, n_sweeps, rng, burn_in=200, thin=5) ->
    tuple[np.ndarray, np.ndarray, IsingState]` — retained per-spin m and E traces plus final
    state.
  - `observables(m_trace, e_trace, temperature, n_spins) -> IsingObservables` — mean |m|,
    χ = N Var(m)/T, c = N Var(e)/T² per spin (12's fluctuation identities reused verbatim).
  - `autocorrelation_time(trace: np.ndarray) -> float` — integrated τ with self-consistent
    window; returns ≥ 0.5 (uncorrelated floor).
  - `hysteresis_sweep(state, temperature, field_range, sweeps_per_step, rng) ->
    tuple[np.ndarray, np.ndarray]` — m along the up-then-down field ladder (the loop).
  - `ising_1d_exact(temperature, field=0.0) -> tuple[float, float]` — (e, m) per spin closed
    forms: e = -tanh(1/T) at h = 0; m = sinh(h/T)/sqrt(sinh²(h/T) + e^(-4/T)).
  - `onsager_tc() -> float` — 2/ln(1 + sqrt(2)) ≈ 2.269, the reference anchor.
- **`tests/physics/` additions** (six categories):
  - *dimensional:* reduced-units anchor — aligned L × L state has E = −2N exactly (2 bonds per
    site, J = 1) and m = 1; the test docstring records the deliberate reduced-units deviation
    (§7).
  - *conservation:* incremental bookkeeping — after 10³ sweeps, `state.energy` and
    `state.magnetization` equal a from-scratch recompute exactly (integer-valued in reduced
    units); global spin flip at h = 0 leaves E invariant (symmetry check).
  - *analytic-limit:* 1-D chain observables match `ising_1d_exact` within `seed_study` 3σ at
    two temperatures and one field; 2-D high-T limit — m → tanh(h/T) as neighbours decorrelate
    (T = 20, weak h); `onsager_tc()` equals 2/ln(1+√2) to machine precision.
  - *large-N:* χ peak height grows monotonically over L ∈ {8, 16, 32} and the peak location
    drifts *toward* `onsager_tc()`; positive growth exponent via `scaling_exponent` (marked
    `slow`).
  - *convergence:* burn-in sufficiency — <|m|> from doubling burn-in lengths converges
    (`convergence_study` against the longest-run value); thinning by τ leaves means unchanged
    within error.
  - *seed-independence:* <|m|> and χ at T = 1.5 and T = 3.0 (L = 16) via
    `validation.seed_study` — `agrees_with` the pooled mean; ordered-vs-disordered phase
    verdicts identical across all seeds.

## 5. Assessment hooks

Checkpoint synthesis (module-level, cross-section): (a) 14 + 15 — classify three transitions
with evidence: vdW boiling (first-order, latent heat, from 14), Ising h-sweep below T_c
(first-order-like jump with hysteresis), Ising T-crossing at h = 0 (continuous, no latent heat,
diverging χ) — then the punchline that 14's liquid-gas *critical point* and 15's Curie point
share exponents (universality, stated); (b) 12 + 15 — one dataset, both fluctuation identities:
extract C and χ from the same traces and defend the error bars via τ and seeds (OBJ-15-5/7).
Exam themes: derive Metropolis from detailed balance; the domain-wall argument; interpret a
χ(T; L) figure and say what it proves. As the terminal module of the phase branch, its capstone
seeds the course's closing essay prompt: "predictable macroscopic behaviour from uncertain
microscopic behaviour" — the phase transition as that idea's sharpest instance.

## 6. Build order and validation gates

Builds after 11, 12 and 14 (its derivation route consumes all three; teaching order = id
order). Terminal on its branch: nothing imports `ising.py`, so the module can land any time
after 14 without blocking others. Lands together in one change: page + problems + lab + quiz
bank; the three NEW misconception entries (status `addressed`) in
`assessment/misconceptions.yml`; the fifteen NEW glossary keys in `glossary/terms.yml` with
`he_reject` candidates; `media/render/render_ising.py` with the three MP4s. HE mirror family
(`.he.yml` quiz, HE page/problems/lab with `en_source_hash` stamps) follows; until it lands the
page is listed in `translation-pending.txt`. Gates: the six README commands with
`--module 15-ising`, with the stochastic-test rules from §3's validation-gates bullet.

## 7. Deviations from the brainstorm

- **Reduced units (J = 1) — licensed local exception to SI-with-\kB.** `ising.py` and all
  module figures measure energies in J and temperature as $\kB T / J$. Rationale: critical
  behaviour is the course's one genuinely unit-free subject — universality *is* the claim that
  the material constants scale out — and $\kB$ is retained in every formula via
  $\beta = 1/(\kB T)$, so the convention is a display choice, not a physics change. The
  dimensional-category test documents the choice; the page states it in the model-spec box.
- **`phase_transitions.py` split (README ownership decision, restated).** The brainstorm §9
  file is split into `phases.py` (14, deterministic EOS analysis) and `ising.py` (15,
  stochastic Monte Carlo) to honour the single-owner rule.
- **Renormalization group out of scope (re-scope).** The brainstorm's "critical behaviour" is
  delivered phenomenologically (power laws, exponents, universality as observed fact); RG is
  named once in the advanced section as the theory the course does not teach.
- **Exponent extraction demoted to advanced (re-scope).** Core verify uses only the χ-peak
  *location* vs L against Onsager; measuring β, γ honestly requires finite-size scaling, which
  would double the module. The problem set's β_exp task is framed as "measure it and explain
  why your answer is biased".
- **No bench experiment (addition of an honest substitute).** Brainstorm §5 verification
  against experimental data is met with published nickel m(T) data, qualitative comparison
  only — microscopic spin systems admit no cheap physical pairing.
