# Module 18 — Fluctuations and transport — Implementation Plan

> **Brainstorm:** §3 module 18 (+ §5 fluctuation laboratory, §6 misconceptions, §7 accuracy
> framework, §8 assessment). **Module id:** `18-fluctuations-transport`.
> **Content path:** `content/en/advanced/18-fluctuations-transport.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Every module so far has treated fluctuations as the noise around the signal: the N^(-1/2) blur
that dice (00, 03), pressure gauges (04) and energy traces (11, 12) all show, and that the
course has taught students to average away. The capstone inverts that stance. The same
molecular chaos that blurs the pressure gauge is what carries momentum, heat and particles
from place to place — and the fluctuation the canonical ensemble *cannot* suppress literally
equals a response function: $\mathrm{Var}(E) = \kB T^2 C_V$. A two-line derivation module 12
only stated here lands and gets used: measure a heat capacity from an energy trace, with no
calorimetry anywhere. Nothing dissipates that does not also fluctuate.

The centrepiece is 03's walker cloud with physics attached — a step becomes a free flight, the
step time an inverse collision rate — watched as it melts into the diffusion equation's
Gaussian Green's function. The diffusion coefficient is then measured three independent ways:
the MSD slope $\langle x^2 \rangle = 2 D t$, a fit of the spreading histogram to the Gaussian,
and the velocity-autocorrelation integral (Green–Kubo-lite). Three values agreeing within
error bars is the module's — and the course's — measurement-culture finale: value ± error, ×3.

The spiral closes on a paid IOU. Module 04's model spec documents its own failure mode —
"high density (particle-particle collisions matter)" — and admits that a collisionless gas can
only *preserve* a Maxwell-Boltzmann distribution, never establish one. This module extends
`kinetics.py` with `mean_free_path` and `collision_rate`, quantifying exactly the physics 04
declared out of scope, and the lab shows *why* the collisionless box cannot diffuse (its VACF
never decays between wall bounces). The course's guiding question gets its final answer: the
micro-noise does not merely permit macroscopic order — it *is* the transport mechanism.

## 2. Position in the course

- **Requires:** `03-random-walks` — walker-ensemble machinery in `sampling.py`, the CLT with
  its hypotheses (independent steps, finite variance) and the correlated-steps counterexample;
  `04-pressure` — `GasState`, `simulate`, `rms_speed`, the mean speed $\bar v$, and the
  documented "no particle–particle collisions" failure mode this module lifts;
  `11-ensembles` — the canonical ensemble and Boltzmann factor, plus its advanced-section seed
  "do the ensembles agree for large N?"; `12-partition-functions` — $C_V$ from $Z$, the
  two-level (Schottky) closed form, and the Var(E) identity *stated* there.
- **Feeds:** nothing — this is the capstone. Its §5 assessment hooks instead host the
  course-closing synthesis: one problem walking pressure → entropy → ensemble → fluctuation
  through a single system (touching 04, 08, 11, 12, 18).
- **Explicitly not assumed:** full linear-response/Kubo formalism (graduate course, named as
  the door not opened); hydrodynamics and Navier–Stokes; Langevin equations or stochastic
  calculus; the Boltzmann transport equation; Onsager reciprocity.

## 3. Module specification

- **Identity and scope** — brainstorm row 18: response functions, fluctuations, diffusion,
  viscosity, thermal conductivity, local equilibrium; centrepiece "random walk → diffusion
  equation experiment"; plus §5's fluctuation laboratory (relative fluctuations vs system
  size, N^(-1/2) scaling). Scope-triaged by design: fluctuation–response is done in full for
  Var(E)–C_V; diffusion is done properly (continuum limit, Green's function, three-way
  measurement); $\eta$ and $\kappa$ are mean-free-path *estimates* only; local equilibrium is
  one honest admonition. Deferred to no module: full Kubo theory — beyond the course.
- **Prerequisites** — 03: independent-increments walks, CLT hypotheses; 04: `GasState`,
  `initialise_gas(fix_temperature=False)` as the canonical-fluctuation source, $\bar v$; 11:
  Boltzmann weights; 12: $C_V$ from $Z$, two-level closed form.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-18-1`: Derive Var(E) = k_B T^2 C_V from the canonical ensemble in two lines, and use
    it to measure C_V from the energy fluctuations of a simulation, with no calorimetry.
  - `OBJ-18-2`: Show that sigma_E/<E> ~ N^(-1/2) follows from Var(E) = k_B T^2 C_V for
    extensive E and C_V, and explain why canonical and microcanonical descriptions therefore
    agree for macroscopic N (equivalence of ensembles).
  - `OBJ-18-3`: Derive the diffusion equation dP/dt = D d^2P/dx^2 as the continuum limit of an
    unbiased random walk with D = l^2/(2 tau) in 1-D, stating the hypotheses (independent
    steps, finite variance) and naming what breaks under correlated steps.
  - `OBJ-18-4`: Use the Green's function P(x,t) = (4 pi D t)^(-1/2) exp(-x^2/(4 D t)) to
    predict <x^2> = 2 D t and the sqrt(t) advance of a diffusion front, and distinguish
    diffusive (slope 1 in log-log MSD) from ballistic (slope 2) spreading.
  - `OBJ-18-5`: Measure D three independent ways — MSD slope, Green's-function histogram fit,
    velocity-autocorrelation integral — quote each as value ± error, and judge consistency.
  - `OBJ-18-6`: Estimate lambda = 1/(sqrt(2) n sigma), the collision rate, and the transport
    trio D ~ (1/3) vbar lambda, eta ~ (1/3) n m vbar lambda, kappa ~ (1/3) n vbar lambda c_v,
    stating each as order-of-magnitude only, and explain why eta is independent of density.
  - `OBJ-18-7`: State the local-equilibrium assumption behind every transport coefficient and
    identify when it fails (gradients steep on the scale of lambda).
- **Mathematical background** — already has: Taylor expansion, partial derivatives, Gaussian
  integrals (03, 08, 12), log-log slope fitting (00, 03), variance algebra (03). New here:
  continuum limit of a discrete master equation; autocorrelation functions and their discrete
  time-integration; a histogram read as an estimator of a PDF evolving in time.
- **Physical intuition goals** — student can predict, without algebra: (1) a dye front that
  took 1 h to travel 1 cm takes 4 h to travel 2 cm; (2) doubling N drops the *relative*
  energy fluctuation by sqrt(2) — and a longer run does not shrink it at all; (3) pumping out
  half the gas leaves its viscosity unchanged; (4) a gas with no particle–particle collisions
  cannot diffuse, however long it runs.
- **Section skeleton seeds** — contract order:
  - *puzzle:* 04's pressure trace jitters and the jitter was always discarded; yet a dye drop
    in still water spreads with no wind, no stirring, no pressure difference driving it. Boxed
    question: how can the chaos we spent seventeen modules averaging away be what carries dye,
    momentum and heat — and can the size of the "noise" itself be a material property?
  - *predict:* (1) double N — does sigma_E/<E> halve, drop by sqrt(2), or stay put? (2) dye
    front at 1 cm after 1 h: how far after 4 h? (targets `diffusion-steady-speed`); (3) pump
    out half the gas — does the viscosity halve? (targets `viscosity-vanishes-dilute`);
    (4) run the same simulation ten times longer — does the energy fluctuation shrink?
    (targets `fluctuations-are-error`).
  - *explore:* walker-cloud explorer — walker count 10^2–10^4, step length, snapshot-time
    slider; live histogram with Green's-function overlay toggle; MSD panel with log-log
    toggle; an "attach physics" switch mapping (l, tau) onto (lambda, 1/nu) for a chosen gas.
  - *verify:* `energy_fluctuation_cv` on ideal-gas draws vs (d/2) N k_B and on a two-level
    trace vs 12's closed form (the `numerical-observation` admonition); log-log MSD slope
    1.00 ± eps; the three D's overlap within error; eta's density flatline vs tabulated data.
  - *derive:* Var(E) identity → N^(-1/2) corollary → master equation → continuum limit →
    Green's function → Green–Kubo-lite (stated) → kinetic estimates → local-equilibrium
    admonition. Full route under core derivations below.
  - *transfer:* back to 03 (the CLT hypotheses *are* the diffusion-equation hypotheses), 04
    (the failure-mode IOU paid), 08 (diffusive mixing is multiplicity increase in motion), 11
    and 12 (the stated identity now derived and used); outward to Perrin — Brownian motion as
    the historical proof that atoms exist; forward, honestly, to nowhere in this course: the
    named door is nonequilibrium statistical mechanics (Kubo, Onsager).
  - *quiz:* fluctuation–response; N^(-1/2) and ensemble equivalence; sqrt(t) vs t fronts;
    three-way D consistency; mean free path numbers; eta vs density; local equilibrium.
  - *explain:* (1) convince a skeptic that a simulation's energy fluctuation is physics, not
    numerical error; (2) why a dye front decelerates although nothing slows the molecules;
    (3) why removing gas does not make it less viscous; (4) in what sense this module answers
    the course's guiding question.
  - *advanced (optional, always last):* proof sketch of Green–Kubo-lite (MSD as the double
    time-integral of the VACF); the persistent (correlated) walk worked out — D renormalises
    to (l^2/2 tau)(1+alpha)/(1-alpha), the promised 03 counterexample quantified; equivalence
    of ensembles stated with more care. Safe-to-skip boundary: core uses the Green–Kubo
    identity only as stated-and-verified; no core cell, quiz item or problem depends on this.
- **Core derivations** — ordered:
  1. Fluctuation–response (theorem, two lines): from $\langle E \rangle = -\partial_\beta \ln Z$,
     $\mathrm{Var}(E) = \partial_\beta^2 \ln Z = -\partial_\beta \langle E \rangle
     = \kB T^2 C_V$.
  2. Corollary (equivalence of ensembles): E and $C_V$ extensive $\Rightarrow$
     $\sigma_E/\langle E \rangle \sim N^{-1/2}$ — the canonical energy sharpens into the
     microcanonical one as N grows; closes 11's advanced seed.
  3. Random walk → diffusion: master equation
     $P(x, t{+}\tau) = \tfrac{1}{2} P(x{-}\ell, t) + \tfrac{1}{2} P(x{+}\ell, t)$; Taylor
     expand to $\partial_t P = D \, \partial_x^2 P$ with $D = \dfrac{\ell^2}{2\tau}$ (1-D).
     Theorem with hypotheses: independent steps, finite variance — 03's CLT conditions; the
     correlated-steps counterexample is what breaks it.
  4. Green's function $P(x,t) = (4\pi D t)^{-1/2} \, e^{-x^2/4 D t}$;
     $\langle x^2 \rangle = 2 D t$; the front advances as $\sqrt{t}$, never as $t$.
  5. Einstein-relation flavour (Green–Kubo-lite, stated + verified; proof sketch advanced):
     $D = \int_0^\infty \langle v(0)\, v(t) \rangle \, \mathrm{d}t$.
  6. Kinetic-theory estimates (each an approximation box, honest to O(1)):
     $\lambda = \dfrac{1}{\sqrt{2}\, n \sigma}$, $\nu = \bar v / \lambda$ with
     $\bar v = \sqrt{8 \kB T / (\pi m)}$; $D \approx \tfrac{1}{3} \bar v \lambda$,
     $\eta \approx \tfrac{1}{3} n m \bar v \lambda$,
     $\kappa \approx \tfrac{1}{3} n \bar v \lambda c_v$. Substituting $\lambda$:
     $\eta \approx \dfrac{m \bar v}{3 \sqrt{2}\, \sigma}$ — the density cancels; Maxwell's
     surprise, flagged and checked against real gas data across pressures.
- **Model specification draft** — for the walker-cloud centrepiece:
  - **System:** an ensemble of independent random walkers standing in for tagged particles in
    a dilute gas; positions (and, when attached, velocities $\pm \ell/\tau$) recorded per step.
  - **Dynamics:** unbiased steps of length $\ell$ every $\tau$; between analyses nothing else
    moves — the estimators in `transport.py` are dynamics-free functions of supplied traces.
  - **Boundary:** unbounded line — no walls, so spreading is never confined.
  - **Ensemble:** many independent walkers realise the ensemble average directly; time and
    ensemble averages agree by construction (independence), not by an ergodicity argument.
  - **Ignored:** walker–walker interactions, hydrodynamic backflow, convection, any memory
    between steps (velocity correlations enter only through supplied velocity traces).
  - **Valid when:** times long compared to $\tau$; many walkers; step statistics with finite
    variance.
  - **Failure modes:** correlated steps (D = l^2/(2 tau) fails — the advanced section's
    persistent walk); times of order $\tau$ (ballistic, MSD slope 2); drift or convection
    contaminating the MSD (the dye experiment's honest caveat).
- **Epistemic classification** — boxed claims: Var(E) identity → `theorem`; N^(-1/2)
  corollary / ensemble equivalence → `theorem`; random walk → diffusion equation with its
  hypotheses → `theorem`; Green–Kubo-lite → `theorem` stated with proof deferred to advanced,
  its check → `numerical-observation` (the module's mandatory numerical admonition); each
  kinetic-theory transport formula → `approximation` (order-of-magnitude, O(1)-honest);
  eta-vs-density flatline against data → `numerical-observation`; local equilibrium → exactly
  ONE `model-assumption` box, closing on the open door: transport assumes gradients gentle
  enough that each parcel is almost in equilibrium — the boundary of this course and the
  entrance to nonequilibrium statistical mechanics. Per the pinned scope decision, no more.
- **Misconceptions** — three NEW entries (no existing registry ids belong here):
  - `diffusion-steady-speed` · "Diffusion carries particles at a steady speed, so spread grows
    linearly in time." · falsifier: measure front position vs t on the walker cloud and the
    dye time-lapse — it advances as sqrt(t), log-log slope 1/2 · distractor: Q-18-4 option
    built on ballistic x = v t.
  - `fluctuations-are-error` · "Fluctuations in a simulation are measurement error, not
    physics." · falsifier: Var(E) of a canonical trace predicts C_V, verified against 12's
    closed form — an "error bar" that equals a material property, and one a longer run does
    not shrink · distractor: Q-18-1 option "run longer until the fluctuation goes away".
  - `viscosity-vanishes-dilute` · "A rarefied gas is less viscous — less stuff to rub." ·
    falsifier: eta ~ (1/3) n m vbar lambda with lambda = 1/(sqrt(2) n sigma) cancels n;
    tabulated gas viscosities are flat over a wide pressure range · distractor: Q-18-7 option
    "halves", imported from liquid intuition.
- **Glossary terms** — reused: `diffusion`, `mean-free-path`, `fluctuation`, `random-walk`,
  `collision`, `canonical-ensemble`. NEW (key / en / suggested he / `he_reject`):
  `diffusion-coefficient` / diffusion coefficient / מקדם דיפוזיה / —;
  `mean-squared-displacement` / mean squared displacement / ממוצע ריבוע ההעתק / [העתק ריבועי ממוצע];
  `greens-function` / Green's function / פונקציית גרין / —;
  `velocity-autocorrelation` / velocity autocorrelation / מתאם עצמי של המהירות / [אוטוקורלציה];
  `viscosity` / viscosity / צמיגות / —;
  `thermal-conductivity` / thermal conductivity / מוליכות חום / [הולכת חום];
  `response-function` / response function / פונקציית תגובה / —;
  `local-equilibrium` / local equilibrium / שיווי משקל מקומי / —;
  `collision-rate` / collision rate / קצב התנגשויות / —;
  `brownian-motion` / Brownian motion / תנועה בראונית / [תנועת בראון].
- **Interactive controls and simulations** — (1) *walker-cloud explorer* (the centrepiece; lab
  live, page MP4): walker count, step length, snapshot time; histogram + Green's-function
  overlay; MSD panel, linear/log-log toggle. (2) *fluctuation-scaling explorer*: N slider over
  2^4–2^12 two-level systems; live sigma_E/<E> vs N on log-log with a -1/2 guide line.
  (3) *transport-estimate calculator*: gas picker (He/N2/Ar), T and P sliders → lambda, nu, D,
  eta, kappa against tabulated values; a density slider showing eta's flatline. (4) *fronts
  race*: diffusive sqrt(t) vs ballistic t front, side by side.
- **Virtual lab outline** — `notebooks/en/labs/18-fluctuations-transport.ipynb`: (1) setup —
  `sampling` (03's walk machinery), `transport`, `kinetics`, `partition`, `validation`,
  `constants`; (2) prediction commits; (3) generate 10^4 walkers × 10^3 steps (one vectorized
  cumsum); histograms at three times with `diffusion_greens_function` overlaid; (4)
  `msd` + `d_from_msd` → D_1 ± err; (5) `d_from_histogram` → D_2 ± err; (6) walker velocity
  traces → `d_from_vacf` → D_3 ± err; contrast cell: VACF of a `kinetics.simulate` velocity
  trace stays flat between wall bounces — the collisionless box cannot diffuse, which is 04's
  failure mode seen from inside; (7) `mean_free_path` / `collision_rate` for N2 at STP; map
  (l, tau) → (lambda, 1/nu); `kinetic_estimates` trio vs tabulated D, eta, kappa; eta vs
  density flatline; (8) canonical energy traces — ideal-gas draws via
  `initialise_gas(fix_temperature=False)` and a two-level Boltzmann trace —
  `energy_fluctuation_cv` vs (d/2) N k_B and vs 12's closed form; sigma_E/<E> vs N slope via
  `scaling_exponent`; (9) import the dye time-lapse CSV (width vs sqrt(t) fit, convection
  caveat) and the Perrin displacement table (D of micron beads ± error); (10) *measurement:*
  D = value ± error, three ways, plus a consistency verdict (do the three intervals overlap?).
- **Real-experiment counterpart** — pinned recommendation, both halves: **food-dye-in-still-
  water time-lapse** (phone camera on a tripod, one frame per minute; fit spread width vs
  sqrt(t); honest caveats — convection from temperature gradients dominates unless the water
  has rested, so pre-register the residual check) as the cheap hands-on; **published
  Perrin-style Brownian-motion data** (displacement table of micron-scale beads, shipped as a
  small CSV under `data/` with citation) as the quantitative import: D ± error, the same
  estimator as cell 4 — and the measurement that made atoms respectable.
- **Media assets** — `media/render/render_transport.py`, language-neutral (no burned-in
  text): `transport-cloud.mp4` (the walker cloud melting into the Gaussian, overlay sharpening
  as N grows); `transport-fronts.mp4` (diffusive vs ballistic front racing, sqrt(t) falling
  behind); `transport-msd.mp4` (MSD growing with the log-log slope-1 guide appearing).
- **Quiz bank outline** — every objective covered at least once; ASCII math:
  - `Q-18-1` (multiple-choice, OBJ-18-1): what the scatter in a canonical energy trace *is*;
    distractor from `fluctuations-are-error` ("run longer until it goes away").
  - `Q-18-2` (numeric, OBJ-18-1): C_V from a quoted Var(E) and T via C_V = Var(E)/(k_B T^2);
    compare to the two-level closed form from 12.
  - `Q-18-3` (multiple-choice, OBJ-18-2): double N — sigma_E/<E> falls by sqrt(2); distractors
    "halves" and "unchanged"; follow-up phrase on which ensemble this vindicates for large N.
  - `Q-18-4` (numeric, OBJ-18-3 + OBJ-18-4): dye front 1 cm in 1 h — time to reach 2 cm
    (4 h, from x ~ sqrt(2 D t)); distractor 2 h from `diffusion-steady-speed` (x = v t).
  - `Q-18-5` (multiple-choice, OBJ-18-4): identify diffusive vs ballistic from log-log MSD
    slopes 1 vs 2; distractor conflating slope with speed.
  - `Q-18-6` (numeric, OBJ-18-6): lambda and collision rate for N2 at STP from
    lambda = 1/(sqrt(2) n sigma) — order 10^-7 m and 10^9 s^-1.
  - `Q-18-7` (multiple-choice, OBJ-18-6): halve the density — eta unchanged; distractor
    "halves" from `viscosity-vanishes-dilute`.
  - `Q-18-8` (free, OBJ-18-5): why three independent D estimates agreeing within error beat
    one high-precision fit; what disagreement would have implied.
  - `Q-18-9` (multiple-choice, OBJ-18-7): where the transport description fails first —
    gradients steep on the scale of lambda; distractor "at low temperature".
- **Problem set outline** — `18-fluctuations-transport-problems.md`: *analytical* — derive
  Var(E) = k_B T^2 C_V from Z (OBJ-18-1); continuum limit of the master equation with
  hypotheses stated (OBJ-18-3); show eta's density independence and estimate its O(1) honesty
  against tabulated N2 (OBJ-18-6). *Computational* — three-way D on shipped trajectories with
  a consistency verdict (OBJ-18-5); C_V from an energy trace vs 12's closed form (OBJ-18-1);
  lambda/nu table across gases (OBJ-18-6); Perrin CSV → D ± error (OBJ-18-4/5). *Challenge* —
  persistent walk: measure D vs (l^2/2 tau)(1+alpha)/(1-alpha) (OBJ-18-3); estimate N_A from
  Perrin's data given the Einstein–Stokes relation (OBJ-18-5); the course-closing synthesis
  problem (§5 below; OBJ-18-1/2/5).
- **Runtime budget** — 10^4 walkers × 10^3 steps is one cumsum on a (10^4, 10^3) array:
  ~80 MB float64 — use float32 (40 MB) and free intermediates; MSD over ~50 log-spaced lags,
  never all lags; histogram fits at 3 snapshot times. VACF from `kinetics.simulate` velocity
  traces: cap at N ≤ 200 particles × 2000 steps. Fluctuation scaling: ≤ 2^12 two-level
  systems × 10^3 samples, vectorized draws. Vectorized NumPy only (no Numba in Pyodide); the
  cloud → Gaussian evolution ships as a pre-rendered MP4 on the page, live only in the lab.
  Target: every lab cell interactive in-browser within seconds.
- **Validation gates** — the six README commands with `--module 18-fluctuations-transport`,
  plus: 04's existing physics tests re-run untouched (the `kinetics.py` extension must not
  alter `simulate`), and a pairwise-consistency test asserting the three D estimators agree
  with each other within combined errors on a common synthetic ensemble.
- **Open questions for the author** —
  1. VACF source for D_3: synthetic walker velocities (exact, closes the loop cleanly) vs
     `kinetics.simulate` traces (honest, but a collisionless box never decorrelates and its
     MSD saturates at the box scale). **Recommend:** walkers for the quantitative third D;
     the kinetics trace as the *demonstration* of why 04's model cannot diffuse.
  2. Which Perrin dataset to ship: the 1909 displacement-count table is public-domain and
     small. **Recommend:** digitized table under `data/` with full citation in the CSV header.
  3. Dye experiment delivery: require students' own footage or ship a sample? **Recommend:**
     ship a sample widths-vs-time CSV so the lab always runs, with instructions to replace it.
  4. Dimension bookkeeping: walker math is 1-D, kinetic formulas 3-D, 04's box is 2-D.
     **Recommend:** derive in 1-D, quote kinetic estimates in 3-D for real-gas contact, and
     state the dimension beside every formula; c_v in kappa is per-particle, (3/2) k_B.

## 4. Library and tests

- **`src/thermolab` — existing used:** `constants.py` (`K_B`, `AMU`); `sampling.py` — 03's
  walker-ensemble extension generates all trajectories; `kinetics.py` — `GasState`,
  `initialise_gas(fix_temperature=False)` (its docstring names fluctuation studies as the
  intended use), `simulate`, `rms_speed`; `partition.py` (12) — two-level closed-form C_V;
  `validation.py` — `seed_study`, `scaling_exponent`, `convergence_study`, `relative_error`;
  `units.py` test-side.
- **`src/thermolab` — new:** `transport.py` (ownership table: introduced by 18, extended by
  none, serves 18). Docstring header, 7 bullets in fixed order — System: independent random
  walkers standing in for tagged particles in a dilute gas / Dynamics: unbiased steps of
  length l every tau; estimator functions are dynamics-free over supplied traces / Boundary:
  unbounded — no walls / Ensemble: independent walkers realise the ensemble average directly /
  Ignored: walker interactions, hydrodynamic backflow, convection, step-to-step memory /
  Valid when: t >> tau, many walkers, finite step variance / Failure modes: correlated steps
  (D = l^2/(2 tau) fails), ballistic times t ~ tau, drift contaminating the MSD. Functions:
  - `msd(trajectories: np.ndarray) -> np.ndarray` — ensemble <x^2>(t) from a (walkers, steps)
    array, displacements measured from each walker's start.
  - `diffusion_greens_function(x: np.ndarray, t: float, d: float) -> np.ndarray` — the
    Gaussian solution (4 pi d t)^(-1/2) exp(-x^2/(4 d t)); normalised, variance 2 d t.
  - `d_from_msd(trajectories: np.ndarray, dt: float) -> tuple[float, float]` — D ± error from
    the linear fit <x^2> = 2 D t.
  - `d_from_histogram(trajectories: np.ndarray, dt: float) -> tuple[float, float]` — D ± error
    from fitting snapshot histograms to the Green's function at several times.
  - `d_from_vacf(velocities: np.ndarray, dt: float) -> tuple[float, float]` — Green–Kubo-lite:
    D ± error from discrete integration of the velocity autocorrelation.
  - `energy_fluctuation_cv(energy_trace: np.ndarray, temperature: float) -> float` —
    C_V = Var(E)/(k_B T^2): a heat capacity measured from fluctuations alone.
  - `kinetic_estimates(n_density: float, temperature: float, mass: float, sigma: float) ->
    tuple[float, float, float]` — the order-of-magnitude trio (D, eta, kappa).
- **`src/thermolab` — extended:** `kinetics.py` (README ownership: 04 introduces, 18 extends;
  spec only these two functions, dynamics untouched — this lifts 04's stated failure mode
  "high density (particle-particle collisions matter)" into computable form, §7 log):
  - `mean_free_path(n_density: float, sigma: float) -> float` — lambda = 1/(sqrt(2) n sigma).
  - `collision_rate(n_density: float, sigma: float, temperature: float, mass: float) ->
    float` — vbar/lambda with vbar = sqrt(8 k_B T/(pi m)).
- **`tests/physics/` additions** (six categories):
  - *dimensional:* pint re-evaluation via `units.py` — D in m^2/s, eta in Pa s, kappa in
    W/(m K); `mean_free_path` in m, `collision_rate` in 1/s; Green's function integrates to 1.
  - *conservation:* the `kinetics.py` extension leaves 04's energy-conservation tests passing
    byte-for-byte (`simulate` untouched; new functions are pure); `msd` uses every walker.
  - *analytic-limit:* `d_from_msd` recovers l^2/(2 tau) on synthetic walks with known D;
    `energy_fluctuation_cv` matches 12's closed-form two-level C_V and (d/2) N k_B for
    ideal-gas draws; `diffusion_greens_function` has variance 2 D t.
  - *large-N:* log-log MSD-vs-t exponent 1.0 via `validation.scaling_exponent`; relative
    Var(E) exponent -1/2 across N, same helper.
  - *convergence:* histogram-fit D error shrinks with walker count
    (`validation.convergence_study` over 10^2 → 10^4 walkers).
  - *seed-independence:* each of the three D estimators via `validation.seed_study` agrees
    with the input D within 3 standard errors; pairwise consistency across the trio.

## 5. Assessment hooks

The course-closing synthesis (checkpoint capstone, one system all the way down): a monatomic
ideal gas in a piston. (a) Compute its pressure kinetically and compare to $P V = N \kB T$
(04). (b) Compress it isothermally; book the work with $\mathrm{d}U = \dbar Q + \dbar \Won$
and the entropy change of gas and bath (05/08). (c) Couple it to a bath and derive its
canonical energy distribution (11), then $C_V$ from $Z$ (12). (d) Measure the same $C_V$ from
$\mathrm{Var}(E) = \kB T^2 C_V$ on simulated draws, and check
$\sigma_E/\langle E \rangle \sim N^{-1/2}$ (18) — one system walked pressure → entropy →
ensemble → fluctuation, touching 04, 08, 11, 12, 18. Exam themes: two-line fluctuation–
response derivation; sqrt(t) reasoning under time pressure; classify-the-claim across this
module's unusually wide epistemic range (theorem → approximation → model-assumption). Feeds
no later module — it is the capstone; the synthesis problem doubles as the course's exit
ticket alongside 00's diagnostic for a pre/post comparison.

## 6. Build order and validation gates

Last module in the build sequence, by design and by dependency: it consumes 03's `sampling`
extension, 11/12's `ensembles.py`/`partition.py`, and the built 04. `transport.py` unblocks
nothing. Lands together in one change: page + problems + lab + quiz bank; the three NEW
misconception entries (status `addressed`) in `assessment/misconceptions.yml`; the ten NEW
glossary keys with `he_reject` candidates in `glossary/terms.yml`; the `kinetics.py`
extension guarded by 04's untouched test suite; the Perrin CSV and sample dye CSV under
`data/`; `media/render/render_transport.py` and its three MP4s. HE mirror family (`.he.yml`
quiz, HE page/problems/lab with `en_source_hash` stamps) follows; until it lands the page is
listed in `translation-pending.txt`. Gates: the six README commands with
`--module 18-fluctuations-transport`, plus the two extras in §3's validation-gates bullet.

## 7. Deviations from the brainstorm

- **Scope triage of "response functions" (re-scope).** Brainstorm row 18 names response
  functions generally; full linear response is a graduate course. Reduced to the one identity
  done completely — $\mathrm{Var}(E) = \kB T^2 C_V$, derived, boxed, and used — plus
  Green–Kubo-lite for D (stated + verified, proof sketch advanced). Kubo/Onsager are named as
  the door not opened.
- **eta and kappa as order-of-magnitude estimates only (re-scope).** No Chapman–Enskog; each
  formula is an `approximation` box honest to O(1), with the eta-density flatline as the
  falsifiable payoff. Rationale: the estimates teach the mechanism; the exact coefficients do
  not fit the course.
- **Local equilibrium reduced to one admonition (re-scope, pinned).** One `model-assumption`
  box marking the course boundary — not a section, not a formalism.
- **`kinetics.py` failure-mode lift (addition, README ownership table).** 04's documented
  failure mode — "high density (particle-particle collisions matter)" — becomes computable:
  `mean_free_path` and `collision_rate` quantify the collisions the model ignores, without
  touching its dynamics; the lab shows the collisionless box cannot diffuse.
- **Course-closing synthesis added beyond the brainstorm row (addition).** §5's capstone
  problem walks one system through 04 → 08 → 11 → 12 → 18; the brainstorm has no closing
  synthesis, and a capstone module should end the course, not just itself.
- **Real-experiment pairing added beyond the brainstorm row (addition).** Dye time-lapse as
  the cheap hands-on plus Perrin data as the quantitative import — the brainstorm row names
  neither, and the capstone should end on experiment deciding.
