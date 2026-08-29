# Module 09 — The fundamental relation — Implementation Plan

> **Brainstorm:** §3 module 9 (+ §4 notebook rhythm, §5 "Maxwell-relation explorer" seed,
> §6 misconceptions, §7 accuracy framework, §8 assessment). **Module id:** `09-fundamental-relation`.
> **Content path:** `content/en/thermodynamics/09-fundamental-relation.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

The structural summit of the entropy spiral (C2): 07 built entropy from heat engines as
$S = \int \dbar Q_{\text{rev}} / T$, 08 built it from counting as $S = \kB \ln \Omega$, and this
module reveals what either construction was *for* — hand me one function, $S(U,V,N)$, and I can
predict everything the system will ever do: every heat capacity, every pressure, every
equilibrium point. Its slopes are the intensive variables ($1/T$, $P/T$, $-\mu/T$), its
maximization under constraints is equilibrium, its curvature is stability, and its extensivity
alone forces the Euler relation $U = TS - PV + \mu N$ and Gibbs–Duhem. The page's opening act
resolves the oldest mystery in the course: why *temperatures* equalize, not energies — contact
maximizes total $S$ where the slopes $\partial S/\partial U$ match, so a big body and a small
body end with wildly unequal energies and exactly equal slopes.

Per C4c, the Einstein solid carries the module: 01's exchange simulation finally gets its
entropy ledger. The centrepiece is the entropy-surface explorer — two subsystems, slide the
partition of $U$ between them, watch $S_{\text{tot}}(U_1)$ peak exactly where the tangent slopes
agree; then release a constraint (wall turns diathermal, piston freed, wall perforated) and
watch the equilibrium point move. Equilibrium as constrained maximization is the single idea
that answers 01's "why does the flow stop exactly at equality": the ledger
$S_{\text{tot}}(t)$ computed along 01's own relaxation trajectory rises monotonically (within
statistical noise) and flattens precisely where `predicted_relaxation` flattens.

Beyond the brainstorm row, this plan lands quantitative entropy *production* (the C2 payoff):
finite-$\Delta T$ contact produces $\Delta S_{\text{tot}} > 0$ computed three ways (ledger,
closed form, calorimetry data), free expansion's $\Delta S = N \kB \ln(V_2/V_1)$ closes 06's
irreversible-process teaser, and the flow-versus-production distinction gets its own falsifier.
It plants seeds deliberately: 10 will Legendre-transform this surface (everything there
differentiates what is built here), 11 will read $\beta = \partial S/\partial U$ off a bath,
13 will develop the $\mu$ that is only *named* here.

## 2. Position in the course

- **Requires:** `07-second-law` — $S$ as a state function via the Clausius construction,
  `cycles.entropy_change` for reversible connecting paths, the Clausius inequality;
  `08-multiplicity` — $S = \kB \ln \Omega$, the additivity-forces-the-logarithm theorem, the
  equal-probability postulate, and the $N^{-1/2}$ sharpness of the multiplicity peak;
  `01-equilibrium` — the Einstein-solid exchange simulation, `ExchangeResult`, the weighted
  $T_{\text{eq}}$ and the `equal-weight-equilibrium` falsifier it staged; `02-equations-of-state`
  — extensive vs intensive vocabulary and $PV = N\kB T$ as the slope check's target;
  `05-work-paths`/`06-processes` — $dU = \dbar Q + \dbar \Won$ and inexactness of $\dbar Q$.
- **Feeds:** `10-potentials` — the surface to Legendre-transform; `euler_check` and
  `gibbs_duhem_check` are reused by its Maxwell verifier (README: `fundamental.py` serves
  09/10/13); `11-ensembles` — $\beta = \partial S/\partial U$ evaluated on a finite bath;
  `13-chemical-potential` — $\mu$ developed, particle-exchange equilibrium at equal $\mu/T$;
  `14-coexistence` — convex patches of the surface become the Maxwell construction.
- **Explicitly not assumed:** Legendre machinery and the potentials $H, F, G$ (10's);
  ensembles and the Boltzmann factor (11's); any quantum derivation of Sackur–Tetrode (12's
  advanced section / 17); phase coexistence (14's). Keep "free energy" out of the prose.

## 3. Module specification

- **Identity and scope** — brainstorm row 9 in full: $S(U,V,N)$, extensivity, Euler relation,
  Gibbs–Duhem, stability; plus the C2 grant of quantitative entropy production. Deferred: the
  potentials and Maxwell relations (10), $\mu$ beyond its slope definition (13), non-concave
  surfaces and coexistence (14), the quantum origin of Sackur–Tetrode (12 advanced / 17).
- **Prerequisites** — 07 (`entropy_change`, Clausius inequality), 08 ($\kB \ln \Omega$,
  additivity theorem, peak sharpness), 01 (`simulate_energy_exchange`, `ExchangeResult`,
  $T = q\varepsilon/(n\kB)$ map), 02 (extensive/intensive), 05 (first-law sign convention).
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-09-1`: State the entropy postulates (S extensive and additive, increasing in U,
    concave, maximized over unconstrained variables at equilibrium), classify them as model
    assumptions, and explain how 07's Clausius construction and 08's kB ln Omega each satisfy
    them.
  - `OBJ-09-2`: Define temperature, pressure, and chemical potential as slopes of the entropy
    surface — 1/T = dS/dU at fixed V,N; P/T = dS/dV at fixed U,N; -mu/T = dS/dN at fixed U,V —
    and extract them numerically from a tabulated S(U,V,N).
  - `OBJ-09-3`: Derive the equal-slope equilibrium conditions by maximizing S_total under
    U_1 + U_2 = const (and the V and N versions), predict flow directions from slope
    inequalities, and explain why temperatures equalize while energies generally do not.
  - `OBJ-09-4`: Derive the Euler relation U = T S - P V + mu N from extensivity alone, and
    the Gibbs-Duhem relation S dT - V dP + N dmu = 0 from it.
  - `OBJ-09-5`: Connect concavity of S to stability — C_V >= 0 and kappa_T >= 0 — and describe
    the runaway a convex patch would permit.
  - `OBJ-09-6`: Compute entropy production for finite-Delta-T contact,
    Delta S_total = C_A ln(T_eq/T_A0) + C_B ln(T_eq/T_B0) > 0, and for free expansion,
    Delta S = N kB ln(V2/V1); distinguish entropy that flows from entropy that is produced.
  - `OBJ-09-7`: Use the Einstein-solid S(U,n) to predict the equilibrium energy partition of
    unequal solids, verify it against module 01's exchange simulation via the entropy ledger,
    and state what the ledger's monotone rise does and does not prove.
- **Mathematical background** — already has: partial derivatives and constrained extrema
  (Lagrange not required — one-variable substitution suffices), Stirling (08), exact vs
  inexact differentials (05, `forms`). Introduced here: homogeneous functions of degree one
  and Euler's homogeneous-function theorem; stars-and-bars counting
  $\Omega(q,n) = \binom{q+n-1}{q}$ for the Einstein solid (08 counted two-state systems only).
- **Physical intuition goals** — student can predict without algebra: (1) a pebble dropped
  into a lake ends at the lake's temperature, holding a vanishing share of the energy;
  (2) energy flows toward the body with the *steeper* $S(U)$, i.e. the colder one, because
  that trade raises $S_{\text{tot}}$; (3) releasing any constraint can only move the
  equilibrium point to a state of higher total entropy; (4) a substance with negative $C_V$
  could not sit stably in contact with anything.
- **Section skeleton seeds** — contract order:
  - *puzzle:* one function to rule them all — and the boxed question: two bodies in contact,
    one huge and one tiny; nothing microscopic stops energy flowing further once the
    temperatures match, so what, exactly, is being maximized when the flow stops there and
    not at equal energies?
  - *predict:* (1) hot 2-kg block meets cold 0.2-kg block: equal final energies or equal
    final temperatures? [misconception trap]; (2) the entropy ledger of 01's simulation —
    can it ever tick down for a single step?; (3) a gas doubles its volume with no heat
    exchanged (free expansion): does $S$ rise, fall, or stay fixed?; (4) if $S(U)$ bulged
    convex somewhere, what would two identical bodies in contact do?
  - *explore:* entropy-surface explorer — sliders $n_A, n_B$ (16–4096 oscillators),
    total quanta $Q$ ($10^2$–$10^6$), partition slider $U_1$; renders $S_A$, $S_B$, and
    $S_{\text{tot}}(U_1)$ with live tangent-slope readouts $T_A, T_B$; buttons release
    constraints — wall→diathermal (Einstein pair), piston freed and wall perforated
    (Sackur–Tetrode pair) — and the maximizer's dot moves to the new peak.
  - *derive:* the seven-step route under core derivations below.
  - *verify:* numeric slopes vs closed forms; `composite_maximize` lands on equal-$T$;
    ledger vs closed-form $\Delta S_{\text{tot}}$; free expansion $N\kB\ln 2$ against 07's
    reversible-path `entropy_change` (paying 08's gap-1 bridge); ledger monotonicity as the
    mandatory `numerical-observation` box.
  - *transfer:* backward — 01 (the mystery answered), 06 (free-expansion ledger completed),
    07 (Clausius $S$ and this $S$ are one function), 08 (peak sharpness = why the maximum is
    all that matters); forward — 10 (Legendre), 11 ($\beta$ on the bath), 13 ($\mu$),
    14 (convexity failure); real world — why calorimetry works at all.
  - *quiz:* postulate status; slopes as intensive variables; equal-slope vs equal-energy;
    Euler/Gibbs–Duhem mechanics; stability catastrophe; flow-vs-production ledger;
    computability of irreversible $\Delta S$.
  - *explain:* (1) why does the logarithmically-slow growth of $S_A$ near its peak make a
    huge body an ideal "reservoir"? (2) a student says "entropy is produced whenever it
    flows" — repair the claim; (3) why can $\Delta S$ of free expansion be computed although
    no intermediate state is an equilibrium state?
  - *advanced (last, safe to skip):* Gibbs–Duhem as "one intensive variable is never free" —
    $T, P, \mu$ cannot be varied independently in a one-component system; and Callen's two
    postulational faces — entropy-maximum vs energy-minimum representations, shown equivalent
    on the explorer's surface. No core content depends on either.
- **Core derivations** — ordered:
  1. *Postulates* (boxed, model-assumption): $S$ extensive and additive over subsystems,
     $(\partial S/\partial U)_{V,N} > 0$, concave, and maximized over unconstrained variables
     at equilibrium. Reconciliation: 08's $\kB \ln \Omega$ delivers additivity (theorem) and
     maximization (peak counting); 07's Clausius $S$ delivers the state-function property;
     the postulates *assume* what those constructions established, now taken as the axioms.
  2. *Slopes:* $\dfrac{1}{T} = \left(\dfrac{\partial S}{\partial U}\right)_{V,N}$,
     $\dfrac{P}{T} = \left(\dfrac{\partial S}{\partial V}\right)_{U,N}$,
     $-\dfrac{\mu}{T} = \left(\dfrac{\partial S}{\partial N}\right)_{U,V}$ — $\mu$ introduced
     by name, developed in 13. Sanity anchor: on Sackur–Tetrode these give
     $U = \tfrac{3}{2} N \kB T$ and $PV = N \kB T$ — the slope definitions reproduce 04's
     kinetic temperature and 02's ideal-gas law. Quasistatic identification, stated
     carefully: $dU = \dbar Q + \dbar \Won$ always; for a quasistatic change
     $\dbar Q = T\,dS$ and $\dbar \Won = -P\,dV$, giving $dU = T\,dS - P\,dV + \mu\,dN$ — an
     identity among state functions valid between *any* neighbouring equilibrium states; only
     the term-by-term reading as heat and work fails off the quasistatic path.
  3. *Equal-slope equilibrium:* maximize $S_{\text{tot}} = S_1(U_1) + S_2(U - U_1)$ at fixed
     $U$: $\partial S_1/\partial U_1 = \partial S_2/\partial U_2 \Rightarrow T_1 = T_2$, with
     energy flowing toward the steeper slope until then. $V$ version $\Rightarrow P_1 = P_2$,
     $N$ version $\Rightarrow \mu_1 = \mu_2$. Big/small asymmetry: equal slopes, unequal
     energies — the puzzle resolved.
  4. *Einstein-solid fundamental relation* (the C4c payoff): with $q = U/\varepsilon$ and $n$
     oscillators, Stirling on $\ln\binom{q+n-1}{q}$ gives
     $S(U,n) = \kB\left[(q+n)\ln(q+n) - q\ln q - n\ln n\right]$, so
     $\dfrac{1}{T} = \dfrac{\kB}{\varepsilon}\ln\!\left(1 + \dfrac{n\varepsilon}{U}\right)$,
     whose high-$T$ limit is exactly 01's map $T = q\varepsilon/(n\kB)$.
  5. *Extensivity → Euler* (theorem given extensivity):
     $S(\lambda U, \lambda V, \lambda N) = \lambda S(U,V,N)$; differentiate at $\lambda = 1$:
     $S = U/T + PV/T - \mu N/T$, i.e. $U = TS - PV + \mu N$.
  6. *Gibbs–Duhem:* $d(TS - PV + \mu N) - (T\,dS - P\,dV + \mu\,dN)$ leaves
     $S\,dT - V\,dP + N\,d\mu = 0$.
  7. *Concavity ⇔ stability:* $\partial^2 S/\partial U^2 = -1/(T^2 C_V) \le 0 \Rightarrow
     C_V \ge 0$; the $V$-sector gives $\kappa_T \ge 0$. Catastrophe argument: a convex patch
     rewards segregation — a fluctuation moving energy from the cooler to the hotter side
     would *raise* $S_{\text{tot}}$ and run away; matter with $C_V < 0$ could never share a
     temperature with anything.
  8. *Entropy production* (C2 payoff): finite-$\Delta T$ contact,
     $\Delta S_{\text{tot}} = C_A \ln\dfrac{T_{\text{eq}}}{T_{A,0}} +
     C_B \ln\dfrac{T_{\text{eq}}}{T_{B,0}} > 0$ unless $T_{A,0} = T_{B,0}$ (concavity of ln);
     computed live on the Einstein exchange via the ledger. Free expansion from
     Sackur–Tetrode at fixed $U$: $\Delta S = N \kB \ln(V_2/V_1)$ — closing 06's teaser and
     08's gap-1 bridge in one stroke. Flow vs production: along a reversible isothermal leg,
     $\dbar Q_{\text{rev}}/T$ *flows* between system and bath with zero production.
- **Model specification draft** (heads `fundamental.py` and the explore box):
  - **System:** a fundamental relation $S(U,V,N)$ treated as the complete thermodynamic
    description; concretely the Einstein-solid $S(U,n)$ and monatomic-ideal-gas
    Sackur–Tetrode $S(U,V,N)$, alone or as two-subsystem composites.
  - **Dynamics:** none — the surface is static; "what happens" is constrained maximization of
    $S_{\text{tot}}$ over the partitions an internal wall permits.
  - **Boundary:** the composite is isolated; the internal wall's character (adiabatic or
    diathermal, fixed or movable, impermeable or permeable) is the constraint being released.
  - **Ensemble:** equilibrium thermodynamics — every point is an equilibrium state; the
    maximization postulate stands in for any relaxation dynamics (01 supplies one).
  - **Ignored:** fluctuations about the maximum (relative size $N^{-1/2}$, module 08),
    surface/interface terms, long-range forces that would break extensivity.
  - **Valid when:** subsystems macroscopic enough that $S$ is smooth and extensive; Einstein
    form in the classical high-$T$ regime; Sackur–Tetrode in the dilute classical regime.
  - **Failure modes:** small $n$ ($\ln N$ extensivity corrections, measured in 08); low $T$
    (Sackur–Tetrode $S \to -\infty$ unphysically — flagged, resolved in 17); convex patches
    (coexistence — 14's Maxwell construction repairs the surface).
- **Epistemic classification** — boxes on the page: entropy postulates → `model-assumption`;
  slope definitions of $T, P, \mu$ → `definition`; Euler and Gibbs–Duhem →
  `theorem` (given extensivity); quasistatic identification $T dS = \dbar Q_{\text{rev}}$ →
  `theorem` (given 07's construction); Sackur–Tetrode → stated result, `approximation` box
  with its quantum origin flagged as a forward pointer to 12's advanced section;
  ledger monotone within noise → `numerical-observation` (mandatory box); whether real
  matter's $S$ is exactly concave or convexity signals new physics → one-line
  `open-question` pointer at 14.
- **Misconceptions** — reinforced, not re-claimed: `subsystem-entropy-increase` (08's) —
  the ledger shows $S_A$ alone *falling* while $S_{\text{tot}}$ rises. NEW entries proposed:
  - `equal-energy-equilibrium` · "Equilibrium means both bodies end with equal energies." ·
    falsifier: unequal Einstein solids ($n_B = 10\,n_A$) equilibrate at equal slopes and a
    10:1 energy split, on the explorer and in 01's replayed simulation (ties to 01's
    `equal-weight-equilibrium`, which killed the equal-*temperature-average* variant) ·
    distractor in `Q-09-2`.
  - `entropy-flow-is-production` · "Entropy is produced whenever entropy flows." · falsifier:
    reversible isothermal leg — $\int \dbar Q_{\text{rev}}/T$ flows in, the bath's flows out,
    production exactly zero; contrast the finite-$\Delta T$ ledger where production is
    strictly positive · distractor in `Q-09-9`.
  - `entropy-undefined-off-equilibrium` · "S is only defined at equilibrium, so Delta S of an
    irreversible process cannot be computed." · falsifier: free expansion — endpoints are
    equilibrium states, so `cycles.entropy_change` along a reversible connecting path yields
    $N \kB \ln 2$, matching Sackur–Tetrode's difference exactly · distractor in `Q-09-10`.
- **Glossary terms** — verified against `glossary/terms.yml` (no collisions; `entropy`,
  `extensive`, `entropy-of-mixing`, `gibbs-paradox` exist): `fundamental-relation` / en
  "fundamental relation" / he היחס היסודי / `he_reject` [יחס פונדמנטלי]; `euler-relation` /
  "Euler relation" / יחס אוילר; `gibbs-duhem-relation` / "Gibbs–Duhem relation" /
  יחס גיבס–דוהם / `he_reject` [גיבס דוהם]; `chemical-potential` / "chemical potential" /
  פוטנציאל כימי; `entropy-production` / "entropy production" / ייצור אנטרופיה / `he_reject`
  [יצירת אנטרופיה]; `thermodynamic-stability` / "thermodynamic stability" /
  יציבות תרמודינמית; `diathermal` / "diathermal" / דיאתרמי.
- **Interactive controls and simulations** — (1) *entropy-surface explorer* (Einstein pair):
  sliders $n_A, n_B \in [16, 4096]$, total quanta $Q \in [10^2, 10^6]$, partition $U_1$;
  renders the three curves + tangent readouts; "release wall" animates the dot climbing to
  the peak. (2) *constraint-release panel* (Sackur–Tetrode pair): $(U_1, V_1)$ contour map of
  $S_{\text{tot}}$; buttons diathermal / free piston / perforate move the constrained maximum
  across the map. (3) *ledger strip*: 01's relaxation trace with cumulative
  $\Delta S_{\text{tot}}(t)$ beneath it, rising and flattening together.
- **Virtual lab outline** — `notebooks/en/labs/09-fundamental-relation.ipynb`: (1) setup —
  build both relations from `thermolab.fundamental`; (2) predictions cell (commit the four
  predict answers); (3) sweep the $U_1$ partition, plot $S_{\text{tot}}(U_1)$, locate the
  peak, read equal slopes off `temperature_of`; (4) release constraints, tabulate the moving
  maximum; (5) numeric slopes vs closed forms, halving $h$ to expose second-order
  convergence; (6) replay `simulate_energy_exchange` from 01, apply `entropy_produced`,
  overlay the closed-form $\Delta S_{\text{tot}}$; (7) `seed_study` of the ledger's final
  value and its worst single-step decrease; (8) Sackur–Tetrode: free expansion
  $N \kB \ln 2$ vs 07's `entropy_change`; `euler_check` and `gibbs_duhem_check` residuals;
  (9) mixing-calorimetry CSV import and *measurement:*
  $\Delta S_{\text{tot}} = \text{value} \pm \text{error}$ J/K from the fitted final $T$.
- **Real-experiment counterpart** — mixing calorimetry: hot and cold water masses in a foam
  cup, thermometer log as CSV (`data/09-mixing-calorimetry.csv` schema: `t_s, T_hot_K,
  T_cold_K, T_mix_K`); predict final $T$ from measured heat capacities, then
  $\Delta S_{\text{tot}} = m_1 c \ln(T_f/T_1) + m_2 c \ln(T_f/T_2) > 0$ — cheap, quantitative,
  imports directly into lab part 9.
- **Media assets** — `media/render/render_fundamental.py`, language-neutral MP4s:
  (1) `fundamental-partition-sweep.mp4` — $S_{\text{tot}}(U_1)$ with a travelling tangent
  pair that aligns at the peak; (2) `fundamental-constraint-release.mp4` — the contour-map
  maximum migrating as constraints drop; (3) `fundamental-ledger.mp4` — 01's relaxation with
  the cumulative entropy ledger rising beneath it. No text burned into frames.
- **Quiz bank outline** — `assessment/quizzes/09-fundamental-relation.en.yml`:
  `Q-09-1` MC (OBJ-09-1) — which listed statement is a postulate vs a theorem 08 proved;
  `Q-09-2` MC (OBJ-09-3) — big/small blocks in contact, final state; distractor
  `equal-energy-equilibrium`; `Q-09-3` numeric (OBJ-09-2) — finite-difference 1/T from a
  tabulated S(U); `Q-09-4` MC (OBJ-09-3) — flow direction from dS_1/dU_1 > dS_2/dU_2;
  `Q-09-5` numeric (OBJ-09-4) — check U - TS + PV - mu N = 0 from given values;
  `Q-09-6` MC (OBJ-09-4) — after fixing dT and dP, is dmu free? (Gibbs–Duhem);
  `Q-09-7` MC (OBJ-09-5) — what a convex S(U) patch permits; distractor "nothing observable";
  `Q-09-8` numeric (OBJ-09-6) — Delta S_total for 1 kg at 350 K mixed with 1 kg at 290 K;
  `Q-09-9` MC (OBJ-09-6) — reversible isothermal leg: entropy flows, none produced;
  distractor `entropy-flow-is-production`; `Q-09-10` MC (OBJ-09-6) — computing irreversible
  Delta S via a reversible connecting path; distractor `entropy-undefined-off-equilibrium`;
  `Q-09-11` prediction + short-answer (OBJ-09-7, OBJ-09-1) — will the ledger ever tick down,
  and what its monotone rise does and does not prove. Every `OBJ-09-K` covered.
- **Problem set outline** — `09-fundamental-relation-problems.md`: (1) analytical — derive
  the Einstein-solid $S(U,n)$ from stars-and-bars + Stirling, extract $1/T$, recover 01's
  high-$T$ map [OBJ-09-2,7]; (2) analytical — Euler and Gibbs–Duhem verified term-by-term on
  Sackur–Tetrode [OBJ-09-4]; (3) analytical — show
  $\partial^2 S/\partial U^2 = -1/(T^2 C_V)$ and write the runaway argument for $C_V < 0$
  [OBJ-09-5]; (4) computational — unequal solids: predict the equilibrium partition from
  equal slopes, verify with `composite_maximize` and the replayed 01 ledger [OBJ-09-3,6,7];
  (5) computational — Sackur–Tetrode pair with a freed piston then a perforated wall: equal
  $P$, then equal $\mu$ [OBJ-09-2,3]; (6) challenge — calorimetry with
  temperature-dependent $c(T)$ data: integrate $dS = C(T)\,dT/T$ numerically [OBJ-09-6].
- **Runtime budget** — trivial for Pyodide: entropy-surface grids are $200 \times 200$
  float64 ($\sim$0.3 MB); `composite_maximize` is a vectorized 1-D scan plus golden-section
  refinement; the ledger evaluates `gammaln` (scipy, Pyodide-available) on a $\sim 5\times10^4$-step
  trace in one vectorized call. Everything runs in well under a second; no Numba, pure NumPy.
- **Validation gates** — the README per-module block with `--module 09-fundamental-relation`;
  extra: `check_assessment.py` must see the three new misconception entries and every
  `OBJ-09-K` quiz-covered; `check_glossary.py` must see the seven new terms.
- **Open questions for the author** — (1) do the piston/perforation releases run only on the
  Sackur–Tetrode pair (Einstein solids have no $V$)? *Recommend yes*, with the asymmetry
  stated in explore. (2) Where does Planck's $h$ live for Sackur–Tetrode, given
  `constants.py` is closed to extension (README invariant 5)? *Recommend* a module-level
  `PLANCK_H` in `fundamental.py` with a comment. (3) Should `entropy_produced` use exact
  $\ln\binom{q+n-1}{q}$ via `multiplicity.log_multiplicity` or the Stirling closed form?
  *Recommend exact* — the ledger stays honest at small $n$ and Stirling becomes a measured
  approximation, echoing 08. (4) Constant $c$ or $c(T)$ for the water experiment?
  *Recommend constant $c$* in the lab, $c(T)$ in challenge problem 6.

## 4. Library and tests

- **`src/thermolab` — existing used:** `equilibrium` (`TwoBodyState`, `ExchangeResult`,
  `simulate_energy_exchange`, `from_temperatures`, `equilibrium_temperature`);
  `multiplicity.log_multiplicity` (stars-and-bars count feeds the ledger); `constants.K_B`,
  `constants.AMU`; `cycles.entropy_change` (07, reversible connecting paths);
  `validation.seed_study` / `convergence_study` / `relative_error`.
- **`src/thermolab` — new: `fundamental.py`** (owner 09 per README; serves 09/10/13), headed
  by the 7-bullet model-spec docstring above. Function-level sketch — a relation is a
  callable `s(u, v, n) -> float` in SI units (fixed-$V$ models close over a dummy $v$):
  - `einstein_solid_entropy(u, n, quantum) -> float | ndarray` — Stirling-form
    $S(U,n)$ of the Einstein solid, $q = u/\text{quantum}$, vectorized in `u`.
  - `sackur_tetrode_entropy(u, v, n, mass) -> float | ndarray` — the monatomic ideal-gas
    $S(U,V,N)$; stated result, quantum origin deferred (12 advanced / 17).
  - `entropy_surface(relation, u_grid, v_grid, n) -> ndarray` — tabulate $S$ on a grid for
    the explorer's contour panel.
  - `temperature_of(relation, u, v, n, h=...) -> float` — $T = 1/(\partial S/\partial U)$ by
    central differences; `pressure_of(...) -> float` — $P = T\,\partial S/\partial V$;
    `mu_of(...) -> float` — $\mu = -T\,\partial S/\partial N$.
  - `euler_check(relation, u, v, n) -> float` — relative residual of
    $U - TS + PV - \mu N = 0$; zero (to truncation error) iff the relation is extensive.
  - `gibbs_duhem_check(relation, u, v, n, du, dv) -> float` — relative residual of
    $S\,dT - V\,dP + N\,d\mu$ along a small displacement.
  - `composite_maximize(relation_1, relation_2, u_total, ...) -> CompositeEquilibrium` —
    partition $(u_1^*, S_{\max})$ maximizing $S_1 + S_2$ at fixed total; optional $V$/$N$
    channels for the released-constraint variants; conserves totals exactly.
  - `concavity_check(relation, u_grid, v, n) -> ndarray` — sign of the second difference of
    $S(U)$; `is_stable(relation, u, v, n) -> bool` — all curvatures non-positive at the point.
  - `entropy_production(c_a, t_a, c_b, t_b) -> float` — closed-form
    $\Delta S_{\text{tot}}$ of finite-$\Delta T$ contact; non-negative by construction.
- **`src/thermolab` — extended: `equilibrium.py`** (extender 09 per README; spec only this):
  - `entropy_produced(result: ExchangeResult) -> np.ndarray` — cumulative
    $\Delta S_{\text{tot}}(t) = \kB[\ln\Omega_A(q_A(t)) + \ln\Omega_B(q_B(t))] - S_{\text{tot}}(0)$
    along the module-01 trajectory, exact stars-and-bars counts, `(n_steps,)` array in J/K —
    the relaxation curve's entropy ledger, monotone within statistical noise
    (`numerical-observation`, never "proved monotone").
- **`tests/physics/` additions:** analytic-limit — `temperature_of(einstein)` matches the
  closed-form $1/T$ and, at high $T$, `from_temperatures`'s $T = q\varepsilon/(n\kB)$ map;
  Sackur–Tetrode slopes reproduce $U = \tfrac32 N\kB T$ and $PV = N\kB T$; `euler_check`
  $\approx 0$ for both relations; free-expansion $\Delta S = N\kB\ln 2$; `entropy_production`
  zero at equal $T$; conservation — `composite_maximize` partition sums exactly to
  `u_total`; `entropy_produced` never mutates its `ExchangeResult`; large-N — relative
  fluctuation of the ledger's final value shrinks $\sim N^{-1/2}$; the $S_{\text{tot}}(U_1)$
  peak sharpens with size; convergence — central-difference slope order $\approx 2$ via
  `convergence_study`; `composite_maximize` refines under grid halving; dimensional — $S$ in
  J/K, `temperature_of` in K, `pressure_of` in Pa, `mu_of` in J, checks via pint;
  seed-independence — ledger final value agrees across seeds within `seed_study` error, and
  monotone-within-tolerance holds for every seed.

## 5. Assessment hooks

Checkpoint synthesis: the three entropies unified — one problem computes $\Delta S$ of the
same contact process by 07's Clausius integral, 08's counting, and 09's ledger, and requires
an explanation of why they agree (the C2 spiral's exam form). "Reservoir" as a limit: show
the pebble-in-a-lake slope argument quantitatively — seeds 11's finite-bath centrepiece.
Flow-vs-production ledger problems become 10's efficiency bookkeeping and 13's mixing
entropy. Feeds later capstones: 10 differentiates this surface (Maxwell relations re-derive
`gibbs_duhem_check`); 12 recomputes the Einstein-solid $S(U,n)$ from $Z$ and closes C4c's
third arc; 14's Maxwell construction begins where `concavity_check` first fails.

## 6. Build order and validation gates

Build after 07 and 08 (both entropy constructions must exist to be unified; `cycles.py` must
exist for the verify bridge) and before 10 (which differentiates this surface) — teaching
slot 9, matching id order. Landing alongside the module: three new
`assessment/misconceptions.yml` entries (`equal-energy-equilibrium`,
`entropy-flow-is-production`, `entropy-undefined-off-equilibrium`, each `status: addressed`
with falsifier + distractor as specified) and seven `glossary/terms.yml` keys (§3 list) with
`he_reject` candidates. HE-mirror artifact family: page, `-problems.md`, lab notebook, quiz
bank `.he.yml`, each stamped `en_source_hash`; list all in `translation-pending.txt` until
translated. Media from `render_fundamental.py` (three MP4s, language-neutral). Gates: the
six README commands with `--module 09-fundamental-relation`, plus 08's gap-1 verify-bridge
check running green once this module's free-expansion result exists.

## 7. Deviations from the brainstorm

- **C2 re-scope (major):** quantitative entropy *production* lands here, not in row 8 —
  constrained-removal experiments plus the `equilibrium.py` ledger extension. Rationale:
  preserves the §2 spiral (07 macroscopic, 08 statistical, 09 structural) and gives
  production a surface to be measured against.
- **$\mu$ named here, developed in 13:** the slope definition and equal-$\mu$ condition
  appear; everything else (grand canonical, reactions, osmosis) stays in 13. Rationale: the
  fundamental relation is incomplete without its third slope, but 13 owns the physics.
- **Sackur–Tetrode stated, not derived:** presented as a stated result with its quantum
  origin flagged as a forward pointer to 12's advanced section. Rationale: deriving it needs
  phase-space counting this module has no room to build honestly.
- **Centrepiece sharpened:** "explore entropy surfaces" becomes a two-subsystem constrained
  maximizer with releasable constraints, run on the C4c Einstein solid so 01's simulation
  gets its ledger — additive, not a re-scope.
