# Module 03 — Probability and Emergence — Implementation Plan

> **Brainstorm:** §3 module 3 (also §2 spiral, §5 fluctuation laboratory, §6, §7).
> **Module id:** `03-random-walks`.
> **Content path:** `content/en/statistical-mechanics/03-random-walks.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Module 00 ended on a deliberate cliff-hanger: it proved how *wide* the distribution of an
average is and explicitly deferred what *shape* it takes — "that it becomes a bell curve is the
central limit theorem, and it is module 3's result, not ours." This module is that payoff. One
drunkard's walk predicts nothing; ten thousand of them trace a Gaussian so precisely you can
set your watch by its width. That is the course's guiding question — predictable macroscopic
behaviour from uncertain microscopic behaviour — in its purest, deliberately physics-free form:
no energy, no particles, no container, and still the order appears.

In the spiral, 03 opens the micro-to-macro program (03 → 08 → 11 → 12). The upgrade over 00 is
twofold: from a single number (an average and its scatter) to a whole *profile* (the walker
density), and from a width law to a shape law (the CLT, stated as a theorem with hypotheses).
The module also plants the course's sharpest epistemic lesson so far: independence is a model
assumption, not a decoration — one honest counterexample (correlated steps) shows exactly which
hypothesis carries the Gaussian and what breaks without it.

Relative to the brainstorm's one-row description, this plan adds the correlated-steps
counterexample, promotes the binomial → Gaussian bridge (de Moivre–Laplace) to a named
deliverable because the already-built 08 leans on it in its "Gaussian limit" box (a retro-fill
08's gap list will pick up), and introduces the standard-error discipline that every later
lab's *measurement:* cell (value ± error) silently depends on. Multiplicity, which the
brainstorm row lists, stays with 08 where it was built (see §7).

## 2. Position in the course

- **Requires:** 00 — the random-variable/mean/variance/independence definitions box, the
  theorem "means always add; variances add for independent quantities", the N^(-1/2) law with
  its coefficient sigma_1/mu_1, and the dilution-not-compensation mechanism. Nothing else.
- **Feeds:** 08 — binomial pmf = two-box multiplicity fraction Omega(N,n)/2^N, and the
  de Moivre–Laplace bridge under its sharp-peak Gaussian box (retro-link); 04 — the shape
  behind the built pressure-trace fluctuations (retro-link from 03's transfer); 11/12 —
  fluctuations about ensemble averages as Gaussians with sqrt(N) absolute width; 18 — the
  walker ensemble is the discrete seed of the diffusion equation, and `sampling`'s walk
  machinery is reused there.
- **Explicitly not assumed:** any thermodynamics — no temperature, no energy, no `\kB`; no
  combinatorics beyond C(n,k) read as a path count (Omega, Stirling and entropy are 08's); no
  measure theory or characteristic functions in core (moment sketch is advanced-only).

## 3. Module specification

- **Identity and scope** — brainstorm row 3: random variables, random walks, central limit
  theorem, thousands of walkers converging toward a Gaussian. Deferred: multiplicity and
  Stirling to 08 (built); diffusion equation and transport to 18; anything with units to 04+.
- **Prerequisites** — 00 only, with the specific results listed in §2. The module must remain
  readable directly after 00: it is the second rung of the probability ladder, not a physics
  module.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-03-1`: Model a random walk as a sum of independent steps and compute <x_t> = mu_1 t
    and Var(x_t) = sigma_1^2 t, hence the RMS spread sigma_1 sqrt(t), for any step
    distribution with finite variance.
  - `OBJ-03-2`: Define the binomial distribution P(k) = C(n,k) p^k (1-p)^(n-k), compute its
    mean np and variance np(1-p), and map the +/-1 coin walk onto it exactly.
  - `OBJ-03-3`: State the central limit theorem with its hypotheses — independent,
    identically distributed steps of finite variance — and its conclusion, that
    (S_n - n mu)/(sigma sqrt(n)) approaches a standard Gaussian; identify which hypothesis
    fails in a given counterexample.
  - `OBJ-03-4`: Apply the de Moivre-Laplace bridge — approximate the binomial pmf by a
    Gaussian of mean np and variance np(1-p) — and state where the approximation is
    trustworthy.
  - `OBJ-03-5`: Distinguish the standard deviation of one quantity from the standard error of
    an estimated mean, and absolute spread growing as sqrt(N) from relative spread falling as
    N^(-1/2).
  - `OBJ-03-6`: Explain how a reproducible Gaussian profile emerges from an ensemble of
    individually unpredictable walkers, without invoking a restoring force or compensation.
- **Mathematical background** — *already has (00, cited not re-derived):* random variable,
  expectation, variance, standard deviation, independence, variance additivity, N^(-1/2).
  *Introduced here:* the binomial distribution; standardization (S_n - n mu)/(sigma sqrt(n));
  the CLT as a precisely stated theorem; de Moivre–Laplace as its coin-walk special case;
  standard deviation vs standard error. Nothing measure-theoretic anywhere.
- **Physical intuition goals** — student can predict without algebra: (1) a 100-step +/-1
  walker typically sits ~10 steps from the start, not 0 and not 100; (2) a walker found far
  right is *not* pulled back — its future is symmetric about where it stands; (3) the cloud's
  width grows as sqrt(t) while its mean stays put (unbiased) or drifts linearly (biased) —
  width and drift are independent facts; (4) changing the step distribution changes the
  Gaussian's width, never its shape.
- **Section skeleton seeds** — contract order:
  - *puzzle:* one drunkard's walk predicts nothing; ten thousand trace a Gaussian you can set
    your watch by. Boxed question: where does the order come from, when every step is pure
    noise?
  - *predict:* (1) typical |x| after 100 +/-1 steps? (2) a walker at +30 after 500 steps — is
    its next 500 steps biased back toward 0? (targets `walker-restoring-force`); (3) the cloud
    widens — is the average drifting? (targets `spread-means-drift`); (4) swap coin steps for
    uniform or heavy-tailed draws — does the long-time histogram shape change?
  - *explore:* sliders n_walkers 10..10^4 (log), n_steps 1..10^3, step-distribution selector
    (+/-1 coin, biased coin p = 0.6, uniform, heavy-ish tail), persistence slider q in [0,1)
    for the correlated mode; live: cloud, histogram with Gaussian overlay, sigma(t) vs
    sqrt(t) trace.
  - *derive:* displacement as sum of iid steps → 00's additivity theorem → mean/variance of
    x_t → binomial for the coin walk → de Moivre–Laplace by second-order log expansion → CLT
    theorem box (statement, hypotheses highlighted, proof deferred) → standard error.
  - *verify:* fitted spread exponent 0.500; binomial vs Gaussian sup-norm at n = 100; the
    three-distribution standardized collapse (the `numerical-observation` admonition); the
    correlated walk failing the same test.
  - *transfer:* (a) coin-walk binomial → 08's two-box Omega(N,n)/2^N, retro-link; (b) walk →
    diffusion teaser for 18, no PDE derived; (c) N^(-1/2) → 04's built pressure trace,
    retro-link; (d) Galton board as de Moivre–Laplace in wood; (e) every later lab's error
    bar is a standard error.
  - *quiz:* sqrt(t) scaling, binomial moments, CLT hypotheses, de Moivre–Laplace numbers,
    standard error vs deviation, both new misconceptions plus a `lln-compensation` reinforcer.
  - *explain:* repair "the walk is pulled back to zero"; which CLT hypothesis does the
    persistent walk break and what survives; why a pollster's error bar shrinks as N^(-1/2)
    while the raw vote count scatter grows.
  - *advanced (last, safe to skip):* moment/characteristic-function sketch of the CLT; 2D
    walks (prettier, adds nothing to the CLT story); the persistent walk's long-time recovery
    with variance factor (1+q)/(1-q). No core content depends on it.
- **Core derivations** — pure mathematics; no `\dbar`, `\Won` or `\kB` appears (the module is
  deliberately physics-free), formulas final-form:
  1. Sum of t iid steps: $\langle x_t \rangle = \mu_1 t$, $\operatorname{Var}(x_t) = \sigma_1^2 t$,
     so $\sigma_{x_t} = \sigma_1 \sqrt{t}$ — 00's additivity theorem re-read with t as "N".
  2. Coin walk to binomial: $P(k \text{ right-steps}) = \binom{n}{k} p^k (1-p)^{n-k}$, mean
     $np$, variance $np(1-p)$; displacement $x = 2k - n$.
  3. De Moivre–Laplace: expanding $\ln P(k)$ to second order about $k = np$ gives
     $\binom{n}{k} p^k (1-p)^{n-k} \approx \dfrac{1}{\sqrt{2\pi npq}}
     \exp\!\left[-\dfrac{(k-np)^2}{2npq}\right]$, $q = 1-p$.
  4. CLT (stated): for iid steps with finite variance,
     $\dfrac{S_n - n\mu_1}{\sigma_1 \sqrt{n}} \xrightarrow[n\to\infty]{} \mathcal{N}(0,1)$ —
     the shape is universal; the step distribution only sets $\mu_1$ and $\sigma_1$.
  5. Standard error: $\mathrm{SE} = \sigma_1/\sqrt{N}$ estimates the scatter of a *mean*;
     $\sigma_1$ describes one draw. Same algebra, opposite objects.
- **Model specification draft** —
  - **System:** N independent walkers on a line; each position is the running sum of its own
    steps; observables are the ensemble histogram, mean and spread.
  - **Dynamics:** each tick, every walker adds one fresh draw from the step distribution —
    independent across walkers and across time.
  - **Boundary:** none — the line is unbounded; N and the step distribution are fixed per run.
  - **Ensemble:** independent trials — each walker repeats the same experiment; nothing
    interacts.
  - **Ignored:** everything physical — no medium, no collisions, no energy, by design.
  - **Valid when:** steps are genuinely independent with finite variance; a seeded generator
    satisfies both by construction.
  - **Failure modes:** correlated steps (the module's own counterexample), infinite-variance
    steps (Cauchy), and any question about one walker's path beyond its distribution.
- **Epistemic classification** — boxed claims: CLT and de Moivre–Laplace = `theorem` (proof
  heuristic-only, said so in the box); independence + finite variance = `model-assumption`
  (boxed at the correlated counterexample); finite-(N, t) histogram → Gaussian agreement =
  `numerical-observation`; binomial pmf, standard error = `definition`; Gaussian-for-binomial
  at finite n = `approximation` (mirrors 08's box, now with its source).
- **Misconceptions** — reinforces `lln-compensation` (00's, not re-claimed) via the
  conditional-future experiment. NEW entries proposed:
  - `walker-restoring-force` · "A walker far to the right is pulled back toward zero." ·
    falsifier: condition on walkers at x >= +30 at t = 500; their subsequent mean displacement
    is 0, spread symmetric · distractor: "expected next-500-step displacement is -30 (back to
    the origin)".
  - `spread-means-drift` · "The cloud getting wider means the average position is drifting." ·
    falsifier: ensemble mean stays 0 within SE while sigma(t) grows as sqrt(t); biased walk
    shown beside it to display real drift · distractor: "sigma grows, so <x> must grow too".
  - `clt-always-applies` · "Any sum of many random quantities is Gaussian." · falsifier:
    persistent walk at q = 0.95 — standardized histogram visibly non-Gaussian at accessible n
    · distractor: "the histogram must collapse; only more steps are needed".
- **Glossary terms** — existing keys reused: `random-walk`, `central-limit-theorem`,
  `gaussian`, `random-variable`, `expectation`, `variance`, `standard-deviation`,
  `independence`, `binomial-coefficient`, `sample-mean`, `probability-distribution`. NEW:
  `binomial-distribution` / binomial distribution / התפלגות בינומית / he_reject:
  [התפלגות בינומיאלית]; `standard-error` / standard error / שגיאת תקן / he_reject:
  [שגיאה סטנדרטית]; `de-moivre-laplace` / de Moivre-Laplace theorem / משפט דה-מואבר–לפלס;
  `galton-board` / Galton board / לוח גלטון; `correlation` / correlation / מתאם / he_reject:
  [קורלציה]; `histogram` / histogram / היסטוגרמה.
- **Interactive controls and simulations** — (1) *walker cloud:* n_walkers (10..10^4, log),
  n_steps (1..10^3), step selector; renders trajectories fading to a cloud, live histogram at
  the current t with the CLT Gaussian overlaid, and sigma(t) against sigma_1 sqrt(t). (2) *CLT
  collapse:* the three step distributions' standardized-sum histograms drawn on one axis,
  n_terms slider 1..1024 (log) — wildly different at n = 1, one curve by n ~ 100. (3)
  *counterexample:* persistence slider q; same overlay machinery, visibly failing, boxed
  `model-assumption`. (4) *Galton board:* n_rows slider, exact binomial bars vs Gaussian curve.
- **Virtual lab outline** — `notebooks/en/labs/03-random-walks.ipynb`: setup (imports,
  seeded rng) → prediction cells (the four commit-first questions) → run
  `random_walk(10_000, 1_000, rng)`; cloud + histogram + `gaussian_limit` overlay → measure
  `walker_spread` at t in {4, 16, 64, 256, 1024}; fit `validation.scaling_exponent` → collapse
  study via `clt_sum_distribution` for the three step distributions → conditional-future
  experiment (falsifies `walker-restoring-force`) → `correlated_walk` at q in {0, 0.5, 0.95} →
  Galton-board / coin-flip data import and `binomial_to_gaussian` comparison → *measurement:*
  spread exponent alpha = value ± error (target 0.500 ± 0.02) and coefficient consistent with
  sigma_1.
- **Real-experiment counterpart** — **recommended: Galton board** (desk toy or video), the
  de Moivre–Laplace bridge in wood: count beads per bin, import as CSV
  (`data/galton-board.csv`, columns bin,count), compare with binomial(n_rows, 1/2) and its
  Gaussian. No-equipment fallback: class coin-flip protocol — each student flips 100 coins,
  reports the head count; the class histogram is the binomial directly. Both import through
  the same lab cell.
- **Media assets** — `media/render/render_random_walks.py`, language-neutral (no burned-in
  text): `walker-cloud.mp4` (one path alone, then 10^4 paths with the side histogram
  sharpening into a Gaussian); `sqrt-spread.mp4` (sigma(t) climbing the sqrt curve while the
  ensemble mean stays flat); `clt-collapse.mp4` (three step distributions' standardized
  histograms merging onto one curve as n grows; the correlated walk refusing to).
- **Quiz bank outline** — `assessment/quizzes/03-random-walks.{en,he}.yml`:
  - `Q-03-1` numeric · typical |x| after 400 +/-1 steps (→ 20) · OBJ-03-1 · distractor 400
    (`spread-means-drift`-adjacent: sum vs spread).
  - `Q-03-2` multiple-choice · walker at +30: expected position after 500 more steps · OBJ-03-1,
    OBJ-03-6 · distractor "near 0" built on `walker-restoring-force`.
  - `Q-03-3` numeric · binomial n = 100, p = 1/2: mean, sigma, the ~68% band (→ 50 ± 5) ·
    OBJ-03-2.
  - `Q-03-4` multiple-choice · which is NOT a CLT hypothesis (Gaussian steps) · OBJ-03-3.
  - `Q-03-5` multiple-choice · persistent walk: which hypothesis fails, what is observed ·
    OBJ-03-3 · distractor from `clt-always-applies`.
  - `Q-03-6` numeric · de Moivre-Laplace estimate of P(k = 50), n = 100, p = 1/2
    (→ 1/sqrt(50 pi) ≈ 0.0798) vs exact 0.0796 · OBJ-03-4.
  - `Q-03-7` multiple-choice · cloud widens as sqrt(t); what does the ensemble mean do ·
    OBJ-03-5 · distractor from `spread-means-drift`.
  - `Q-03-8` multiple-choice · quadruple the sample: standard error halves, standard deviation
    unchanged · OBJ-03-5.
  - `Q-03-9` multiple-choice · pick the correct account of where the Gaussian order comes from ·
    OBJ-03-6 · distractor built on compensation (reinforces `lln-compensation`).
  - `Q-03-10` numeric · biased coin p = 0.6: drift 0.2 t beside spread ~ sqrt(t) · OBJ-03-1,
    OBJ-03-5.
- **Problem set outline** — `03-random-walks-problems.md`: *analytical:* binomial variance
  from a Bernoulli sum (OBJ-03-2); de Moivre–Laplace peak by log expansion (OBJ-03-4);
  standard error of a mean of means (OBJ-03-5). *computational:* spread exponent for uniform
  steps (OBJ-03-1); return-to-origin frequency vs t (OBJ-03-6). *challenge:* 2D walk RMS
  distance (OBJ-03-1); persistent-walk variance factor (1+q)/(1-q) measured (OBJ-03-3); Cauchy
  steps — a *different* CLT failure, numerically explored (OBJ-03-3).
- **Runtime budget** — Pyodide, vectorized NumPy only (no Numba). Batch lab run: 10^4 walkers
  x 10^3 steps of +/-1 as int8 is 10 MB before cumsum; cumulate in float64 keeping only ~10
  logarithmic time slices (10^4 x 10 array, 0.8 MB) — seconds in the browser. Interactive
  default 2 x 10^3 walkers x 500 steps for slider responsiveness; full trajectories stored
  only there (8 MB float64). Histograms are O(n_walkers) per update.
- **Validation gates** — the README's six per-module commands with `--module 03-random-walks`;
  extra: `check_assessment.py` must see the two NEW misconception ids addressed and every
  OBJ-03-K covered by the quiz bank; the correlated-walk counterexample cell must run under
  the same seed discipline as everything else.
- **Open questions for the author** —
  1. Formal probability depth — *recommend:* exactly the delta over 00 (binomial, standard
     error, CLT statement, de Moivre–Laplace); recap 00's definitions in one citing box, never
     re-derive; nothing measure-theoretic.
  2. 2D walks core or advanced — *recommend:* advanced; prettier, adds nothing to the CLT
     story, and doubles the memory budget.
  3. Real experiment — *recommend:* Galton board primary, coin-flip class protocol as the
     no-equipment fallback (both feed the same import cell).
  4. Heavy-ish tail choice — *recommend:* Student-t with nu = 5 (visibly heavy, finite
     variance, so the CLT hypotheses hold); keep Cauchy out of core — it is the challenge
     problem.
  5. Show the persistent walk's long-time *recovery* (modified CLT, variance x (1+q)/(1-q)) —
     *recommend:* advanced only; core shows the failure of the naive prediction and names the
     broken hypothesis, nothing more.

## 4. Library and tests

- **`src/thermolab` — existing used:** `validation.scaling_exponent`, `validation.seed_study`,
  `validation.relative_error` (verify + tests); `multiplicity.log_multiplicity` /
  `multiplicity.probability` consumed by `binomial_to_gaussian` for exact log-gamma binomials
  (consumption only — `multiplicity` is never extended); `sampling.running_average` reused in
  the conditional-future experiment.
- **`src/thermolab` — extended:** `sampling.py` (owner 00, extender 03 per README table);
  extender specs only its own functions — signatures + one-line contracts:
  - `step_distribution(name: str) -> StepDist` — named sampler ("pm1", "biased", "uniform",
    "heavy") bundled with its exact step mean and variance, so overlays never re-estimate.
  - `random_walk(n_walkers: int, n_steps: int, rng: np.random.Generator, step: StepDist | str
    = "pm1", dim: int = 1) -> np.ndarray` — trajectory ensemble, shape (n_walkers,
    n_steps + 1[, dim]), x_0 = 0, cumulative sums of independent draws.
  - `walker_spread(trajectories: np.ndarray) -> np.ndarray` — cross-walker std at every time;
    the sqrt(t) curve, food for `scaling_exponent`.
  - `walker_histogram(positions: np.ndarray, n_bins: int) -> tuple[np.ndarray, np.ndarray]` —
    bin centres and unit-area empirical density at one time slice.
  - `gaussian_limit(x: np.ndarray, t: int, step: StepDist) -> np.ndarray` — the CLT overlay,
    the N(mu_1 t, sigma_1^2 t) density evaluated on x.
  - `clt_sum_distribution(n_terms: int, n_samples: int, rng: np.random.Generator, step:
    StepDist | str = "pm1") -> np.ndarray` — standardized sums (S_n - n mu_1)/(sigma_1
    sqrt(n)); raw material of the collapse.
  - `binomial_to_gaussian(n: int, p: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]` —
    k, exact pmf, matching Gaussian: the de Moivre–Laplace bridge 08's sharp-peak box reuses.
  - `correlated_walk(n_walkers: int, n_steps: int, persistence: float, rng:
    np.random.Generator) -> np.ndarray` — +/-1 walk repeating its previous step with
    probability q; q = 0 recovers `random_walk`, q → 1 breaks the naive CLT prediction.
- **`tests/physics/` additions:** *dimensional:* n/a — every quantity is dimensionless (steps
  and step-units), stated in the test module docstring. *conservation:* `walker_histogram`
  integrates to 1; `binomial_to_gaussian` pmf sums to 1 to 1e-12; trajectory shape preserves
  walker count. *analytic-limit:* measured Var(x_t) at t = 10^3 agrees with sigma_1^2 t within
  seed-study error for each named step distribution; binomial-vs-Gaussian sup-norm decreases
  over n in {25, 100, 400} and is < 1% near the peak at n = 100; `correlated_walk(q=0)`
  statistics match `random_walk`. *large-N:* spread exponent over t in {4,...,1024} fits
  0.500 ± 0.02 via `scaling_exponent`. *convergence:* standardized-sum histogram → standard
  Gaussian in sup-norm as n_terms doubles, for all three finite-variance step distributions;
  the q = 0.9 correlated walk *fails* the same criterion (the counterexample is itself a
  test). *seed-independence:* `seed_study` (8 seeds) on the fitted exponent `agrees_with(0.5)`
  and on the spread coefficient `agrees_with(sigma_1)`.

## 5. Assessment hooks

Checkpoint synthesis: (a) dice-to-walks — recompute 00's N^(-1/2) result as the walk's
t^(+1/2), and say in words why the same algebra reads oppositely for an average and a sum;
(b) binomial ↔ multiplicity — show quantitatively that 08's Omega(N,n)/2^N *is* this module's
coin-walk pmf, and that 08's peak width sqrt(N)/2 is de Moivre–Laplace's sigma at p = 1/2;
(c) error-bar audit — take any later lab's *measurement:* cell and identify what its ± number
is (a standard error, and of what). Exam themes: pick the failed CLT hypothesis from a
scenario; separate drift from spread for a biased walk. Feeds: 11/12 fluctuation problems
(energy fluctuations as Gaussians of absolute width sqrt(N)); 18's capstone consumes the
walker ensemble and sqrt(t) directly as the seed of the diffusion equation.

## 6. Build order and validation gates

Build after 02 (or in parallel — no shared files); teaching order slots 03 before the built 04
via the `content/en/myst.yml` TOC. Because 08 is already built, building 03 triggers the
retro-fill: 08's gap list gains a retro-link so its "Gaussian limit" `approximation` box cites
03's de Moivre–Laplace derivation instead of asserting it inline — a pointer edit in 08, no
content rewrite. At build time: the two NEW misconception ids land in
`assessment/misconceptions.yml` (status addressed, assigned_module 03-random-walks;
`lln-compensation` stays 00's), the six NEW glossary keys land in `glossary/terms.yml` with
`he_reject` candidates. Artifact family: EN page + `03-random-walks-problems.md` + lab
notebook + quiz banks `.en.yml`/`.he.yml` + HE mirrors stamped with `en_source_hash`; the page
is listed in `translation-pending.txt` until the mirror lands. Gates: the README's six
commands with `--module 03-random-walks`.

## 7. Deviations from the brainstorm

- **Placement** — lives in `statistical-mechanics/`, not `foundations/`: it opens the
  micro-to-macro program 03 → 08 → 11 → 12; `foundations/` is pre-course material (README map).
- **Slug** — `03-random-walks` names the centrepiece, not the chapter title "Probability and
  emergence" (README slug note); the title stays the brainstorm's.
- **Multiplicity dropped from scope** — the brainstorm row lists it, but built 08 owns
  Omega, Stirling and entropy; 03 keeps only C(n,k) as a path count, and bridges to 08 in
  transfer. Avoids re-teaching against a built module.
- **Correlated-steps counterexample added** — beyond the brainstorm row; the course rule
  "simulation never proves" needs one place where the load-bearing assumption (independence)
  visibly fails, and this is the cheapest honest place to stage it.
- **Retro-fill of built 08** — 08 was built before 03 and states the binomial → Gaussian
  bridge inline as an approximation box; 03 supplies its derivation and 08's gap list picks up
  the retro-link. 03 also links backward to 04's pressure trace for the same reason.
- **Probability basics recapped, not re-introduced** — the brainstorm places random variables
  here, but built 00 already introduced them (definitions box, variance additivity, N^(-1/2));
  03 cites 00 and introduces only the delta (binomial, standard error, CLT, de Moivre–Laplace).
