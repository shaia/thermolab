# Module 13 — Chemical potential — Implementation Plan

> **Brainstorm:** §3 module 13 (+ §2 spiral, §4 rhythm, §6 misconceptions, §7 accuracy framework).
> **Module id:** `13-chemical-potential`.
> **Content path:** `content/en/advanced/13-chemical-potential.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Water flows downhill; heat flows down temperature gradients; what do *particles* flow down? The
obvious answer — concentration — is wrong, and this module opens by breaking it: two connected
boxes can sit in perfect equilibrium at wildly different densities the moment their site energies
differ (gravity, an adsorbing wall, an electric offset). The thing that actually equalizes is the
chemical potential, the most notoriously slippery quantity in thermal physics, and the module's
job is to make it operational twice over: microcanonically as `\mu = -T (\partial S/\partial N)`
— the third slope of 09's trio, finally getting its own module — and practically as
`(\partial G/\partial N)_{T,P}` via 10's potentials, with the equivalence shown, not asserted.

The spiral payoff is deliberate and boxed: the barometric density profile, derived in 11 from the
Boltzmann factor, is re-derived here as a *constant-mu* condition — same physics, two languages —
and the bath argument of 11 is extended from energy exchange to particle exchange, yielding the
grand-canonical weight `e^{-(E_s - \mu N_s)/(\kB T)}` as a theorem with hypotheses. The module
then cashes mu in three currencies: adsorption (independent-site occupation, a Langmuir-type
curve that is secretly 17's Fermi-Dirac function), a toy chemical equilibrium (mass action from
mu balance for A ⇌ B), and osmosis (solvent-mu equality across a membrane → van 't Hoff).

As the first module of the ADVANCED tier (new `content/en/advanced/` directory, brainstorm §9),
it also carries structural weight: it plants mu-equality as the master equilibrium condition that
14 will apply between phases, and it names — without deriving — the quantum concentration `n_Q`
whose origin belongs to 17. The full grand partition function `\Xi` is explicitly deferred;
everything here runs on entropy maximization plus one-site bookkeeping.

## 2. Position in the course

- **Requires:** `09-fundamental-relation` — the slope definitions on `S(U,V,N)` (`1/T`, `P/T`,
  and the so-far-unused `-\mu/T`), constrained maximization of `S_total`, Euler relation and
  extensivity; `10-potentials` — `G(T,P,N)`, Legendre structure, and `dG = -S dT + V dP + \mu dN`
  as the derivative bookkeeping; `11-ensembles` — the finite-bath argument and the Boltzmann
  factor `e^{-E/(\kB T)}` (barometric version reused verbatim); `12-partition-functions` —
  fluency manipulating `Z` and `F = -\kB T \ln Z` for the single-site calculation.
- **Feeds:** `14-coexistence` — THE consumer: phase coexistence is mu equality between phases,
  applied on day one; `17-quantum-gases` — `\mu(T)` as the knob that fixes `N` in BE/FD, plus
  `site_occupation` reappearing as the Fermi-Dirac function and `n_Q` finally derived; 08's owed
  mixing/Gibbs-paradox teaser (gap 2 there) lands its quantitative home in this module's transfer.
- **Explicitly not assumed:** the grand partition function `\Xi` and its derivative machinery
  (deferred to 17); reaction thermochemistry beyond the toy A ⇌ B (no Hess's law, no standard
  states); electrochemistry; quantum statistics (`n_Q` is named, not derived); Fick's law or any
  transport rate — this module decides *where* particles end up, 18 decides *how fast*.

## 3. Module specification

- **Identity and scope** — brainstorm §3 row 13 in full: particle exchange, grand-canonical
  ensemble (single-site form only), reactions and osmotic equilibrium as toys. Deliberately
  deferred: full `\Xi` formalism and `n_Q`'s derivation → 17; multi-phase mu equality → 14;
  transport rates toward equilibrium → 18.
- **Prerequisites** — 09 (slope trio on `S(U,V,N)`, `S_total` maximization, Euler relation);
  10 (`G`, `dG = -S dT + V dP + \mu dN`); 11 (bath argument, Boltzmann factor, barometric law);
  12 (`Z` and `F = -\kB T \ln Z` for one site).
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-13-1`: define mu = -T (dS/dN)|_{U,V} and evaluate it numerically for a model S(U,V,N).
  - `OBJ-13-2`: show mu = (dG/dN)|_{T,P} agrees with the entropic definition and explain why
    G = mu N for a one-component system (Euler relation).
  - `OBJ-13-3`: predict particle-flow direction from mu values alone, including cases where flow
    runs *against* the concentration gradient.
  - `OBJ-13-4`: derive equal mu (at common T) as the equilibrium condition by maximizing S_total
    under N_1 + N_2 = const, mirroring 09's energy argument.
  - `OBJ-13-5`: use mu = kB T ln(n/n_Q) + u_ext for the ideal gas to re-derive the barometric
    formula as constant mu, and reconcile it with 11's Boltzmann-factor derivation.
  - `OBJ-13-6`: state P(s) proportional to e^{-(E_s - mu N_s)/(kB T)} with its hypotheses and
    apply it to one adsorption site, obtaining the Langmuir-type occupation curve.
  - `OBJ-13-7`: apply mu balance to a toy A <=> B reaction (mass action) and to osmotic
    equilibrium (van 't Hoff Pi = n_s kB T), stating the dilute limits of both.
- **Mathematical background** — already has: partial derivatives with held variables, Lagrange-
  style constrained maximization (09), logarithm algebra, Taylor expansion. Introduced here:
  nothing new — the point is that no new mathematics is needed, only a new *slope*.
- **Physical intuition goals** — student can predict without algebra: (1) which way particles
  flow given two mu values, even when density says otherwise; (2) that raising a box's floor
  energy `u_ext` empties it at equilibrium, exponentially; (3) that adding solute *lowers* the
  solvent's mu, so pure solvent flows *in*; (4) that classical-gas mu is negative and becomes
  less negative as `n` rises toward `n_Q`.
- **Section skeleton seeds** — contract order:
  - *puzzle:* two connected boxes, one floor raised by `u_ext`: at equilibrium the densities are
    visibly unequal and *stay* unequal. Boxed question: "heat flows down T; what do particles
    flow down — and why is it not concentration?"
  - *predict:* (1) equal densities or not at equilibrium? (targets `particles-flow-concentration`);
    (2) raise `u_ext` — which way do particles drift, and by how much (guess a functional form)?
    (3) two systems, same energy per particle — can particles still flow? (targets
    `mu-energy-per-particle`); (4) sugar solution vs pure water across a membrane — which way
    does the *water* move? (targets `osmosis-solute-flow`).
  - *explore:* the centrepiece exchange sim: sliders for `u_b - u_a` (0 to 10 kB T), `T`,
    `N_total` (10^2 to 2x10^4), `M_a/M_b` site ratio; live panels: particle counts N_a(t), the
    two densities, and a mu-meter showing mu_a and mu_b converging while densities split.
    Second tab: gas above an adsorbing surface — site-energy slider, occupation vs `\mu` curve.
  - *derive:* route (1)–(5) below, in order; barometric re-derivation boxed as the spiral payoff.
  - *verify:* numeric mu from `mu_from_entropy` vs closed-form ideal-gas mu; exchange-sim
    endpoint vs the analytic split `n_a/n_b = e^{-(u_a - u_b)/(\kB T)}` — the latter becomes the
    `numerical-observation` admonition; barometric profile from constant mu vs 11's stored curve.
  - *transfer:* (1) → 14: two *phases* of one substance are just two "boxes" — coexistence is mu
    equality; (2) → 17: the site-occupation curve *is* Fermi-Dirac; (3) ← 11: barometric formula,
    two languages; (4) ← 08/09: mixing entropy done quantitatively — the Gibbs-paradox teaser
    owed by 08 gap 2; (5) doping/defect concentrations in solids as mass-action practice.
  - *quiz:* mu vs concentration as the flow variable; numeric slope evaluation; G = mu N;
    barometric ratio; grand-canonical hypotheses; site occupation; van 't Hoff sign and size.
  - *explain:* "Explain to a chemist friend why particles can flow from low to high
    concentration without any pump"; "Why is the chemical potential of a classical ideal gas
    negative, and what would mu near zero signal?" (seeds 17).
  - *advanced (optional, last):* fugacity and activity as industry names for `e^{\mu/(\kB T)}`
    bookkeeping; Gibbs–Duhem re-read as "mu is not independent — fix T and P and mu is fixed"
    (back-link 09). Safe to skip: nothing downstream cites either; 14 restates what it needs.
- **Core derivations** — ordered:
  1. *Exchange equilibrium:* maximize `S_{tot} = S_1(N_1) + S_2(N - N_1)` at fixed `U, V` →
     `\partial S_1/\partial N_1 = \partial S_2/\partial N_2` → with
     `\mu \equiv -T \left(\frac{\partial S}{\partial N}\right)_{U,V}`, equal `\mu/T`; at common
     `T`, `\mu_1 = \mu_2`. Sign traced: particles flow from high mu to low mu because that is
     the direction `S_{tot}` increases. Mirrors 09's energy argument bullet for bullet.
  2. *Practical face:* from `dU = T\,dS - P\,dV + \mu\,dN` (09's relation, quasistatic form of
     `dU = \dbar Q + \dbar \Won` extended to open systems) Legendre-walk to
     `\mu = \left(\frac{\partial G}{\partial N}\right)_{T,P}`; Euler relation gives `G = \mu N`.
  3. *Ideal-gas mu with an offset:* from Sackur–Tetrode-shaped `S` (09) or 12's `Z`,
     `\mu = \kB T \ln(n/n_Q) + u_{\mathrm{ext}}`, with `n_Q(T)` *named* as the quantum
     concentration and boxed as a forward pointer (origin → 17).
  4. *Barometric re-derivation:* constant `\mu` in a column → `\kB T \ln n(z) + m g z = const`
     → `n(z) = n(0)\, e^{-m g z/(\kB T)}`; boxed spiral payoff against 11's Boltzmann route.
  5. *Grand-canonical weight:* 11's finite-bath expansion redone with the reservoir entropy
     expanded in both `U` and `N`: `P(s) \propto e^{-(E_s - \mu N_s)/(\kB T)}` — theorem, with
     hypotheses (large reservoir, fixed T and mu, weak coupling). Applied ONLY to one adsorption
     site: `\langle n \rangle = 1/\big(e^{(\epsilon - \mu)/(\kB T)} + 1\big)` (independent-site
     shortcut; full `\Xi` deferred). Then mass action for A ⇌ B from `\mu_A = \mu_B`:
     `n_B/n_A = (n_{Q,B}/n_{Q,A})\, e^{-\Delta\epsilon/(\kB T)}`; and osmosis from solvent-mu
     equality: dilute expansion → `\Pi = n_s \kB T` (van 't Hoff).
- **Model specification draft** (centrepiece sim; also heads `chemical.py`):
  - *System:* `N` non-interacting particles distributed over two dilute lattice-gas boxes, box A
    with `M_a` sites at energy `u_a` and box B with `M_b` sites at `u_b`.
  - *Dynamics:* one randomly chosen particle per step proposes hopping to a uniformly random
    site in the other box; accepted with Metropolis probability `min(1, e^{-\Delta u/(\kB T)})`.
  - *Boundary:* closed to particles as a pair (`N_a + N_b` exactly conserved); held at fixed `T`
    by an implicit thermal bath that supplies/absorbs the hop energy.
  - *Ensemble:* canonical for the pair at fixed `T, N`; each box separately is approximately
    grand canonical, with the other box acting as its particle reservoir.
  - *Ignored:* particle-particle interactions, multiple occupancy corrections (dilute), hop
    *rates* (time is steps, not seconds), spatial structure within a box.
  - *Valid when:* dilute occupation `N_i \ll M_i` and classical regime `n \ll n_Q`.
  - *Failure modes:* near-full boxes (hard-core corrections), interacting particles (15's
    territory), degenerate regime `n \gtrsim n_Q` where quantum statistics take over (17).
- **Epistemic classification** — boxed claims: `definition` — mu (both faces), quantum
  concentration `n_Q` (named); `theorem` — equal-mu equilibrium condition (hypotheses: exchange
  allowed, S maximized), `G = \mu N` from extensivity, grand-canonical weight (bath hypotheses
  explicit); `model-assumption` — independent sites, dilute lattice gas, ideal-solution osmosis,
  `n_Q` origin deferred (forward-pointer box to 17); `approximation` — dilute van 't Hoff
  expansion; `numerical-observation` — exchange sim equalizing mu at unequal densities,
  mu-difference fluctuations shrinking with `N`.
- **Misconceptions** — NEW entries proposed (registry edits at build time):
  - `particles-flow-concentration` · "Particles always flow from high to low concentration." ·
    falsifier: the offset-box sim equilibrates at unequal densities, and started from *equal*
    densities the flow runs toward the denser-to-be box · distractor: Fick's-law intuition
    ("diffusion always erases density differences").
  - `mu-energy-per-particle` · "The chemical potential is just the energy per particle." ·
    falsifier: two boxes prepared with identical energy per particle but different `n/M`;
    particles still flow — the entropic `\kB T \ln(n/n_Q)` term does the work · distractor:
    "flow stops when energies per particle match".
  - `osmosis-solute-flow` · "Osmosis is solute being pushed through the membrane." · falsifier:
    dialysis-tubing cell gains mass — *solvent* flows toward the solution; van 't Hoff's `\Pi`
    is positive on the solution side · distractor: "sugar leaks out until concentrations match".
- **Glossary terms** — new keys (suggested he; `he_reject` candidates): `chemical-potential` /
  chemical potential / פוטנציאל כימי; `grand-canonical-ensemble` / grand canonical ensemble /
  צבר גרנד-קנוני (aligns with existing צבר קנוני) / reject [אנסמבל גרנד קנוני];
  `particle-reservoir` / particle reservoir / מאגר חלקיקים; `adsorption` / adsorption / ספיחה /
  reject [אדסורפציה]; `semipermeable-membrane` / semipermeable membrane / קרום חדיר-למחצה;
  `mass-action` / law of mass action / חוק פעולת המסה; `quantum-concentration` / quantum
  concentration / ריכוז קוונטי; advanced only: `fugacity` / fugacity / פוגסיות; `activity` /
  activity / פעילות / reject [אקטיביות]. Collisions checked: `osmotic-pressure` already exists
  (לחץ אוסמוטי) — reuse, do not re-add; `diffusion` exists and stays 18's vocabulary.
- **Interactive controls and simulations** — (1) *exchange centrepiece:* sliders `u_b - u_a`
  (0–10 kB T), `T`, `N_total` (10^2–2x10^4), `M_a : M_b`; renders N_a(t) trace, twin density
  bars, and a live mu-meter (mu_a, mu_b) with the analytic split overlaid; the offset slider
  relocates the equilibrium split live. (2) *adsorption tab:* `\epsilon` and gas-pressure
  sliders; renders occupation vs `\mu` (the Langmuir/FD curve) with the sim's measured site
  occupancy scattered on top. (3) *barometric strip:* `T` and `m g` sliders; column density
  histogram vs the constant-mu exponential.
- **Virtual lab outline** — `notebooks/en/labs/13-chemical-potential.ipynb`: (1) model setup —
  build the two-box system, state the 7-bullet spec; (2) predictions — commit to the four
  predict answers in code cells; (3) run `particle_exchange_sim`, plot N_a(t) and mu_a - mu_b;
  (4) numeric mu — `mu_from_entropy` on 09's Sackur–Tetrode-shaped relation vs `ideal_gas_mu`;
  (5) equilibrium split vs `u_ext` sweep, fit the exponential; (6) `site_occupation` vs measured
  single-site occupancy; (7) barometric profile from constant mu vs 11's Boltzmann curve;
  (8) osmosis data import (`data/13-chemical-potential/osmosis.csv`), Pi vs concentration fit;
  (9) *measurement:* fitted van 't Hoff slope → estimate of R T (per-mole kB T) ± fit error.
- **Real-experiment counterpart** — dialysis-tubing sucrose cells (primary; gummy-bear variant
  for home use): 4–5 sucrose concentrations, mass gain vs time and vs concentration; the linear
  Pi-vs-c fit yields a van 't Hoff estimate of R T. Import path: students record mass series in
  `data/13-chemical-potential/osmosis.csv` (columns: conc_mol_L, t_min, mass_g), loaded in lab
  part 8 with pandas; cheap (< $20) and genuinely quantitative.
- **Media assets** — `media/render/render_chemical.py`, language-neutral (no burned-in text):
  MP4 1 `chemical-exchange` — two boxes with raised floor, dots drifting until densities split
  while two side gauges (mu bars) meet; MP4 2 `chemical-mu-trace` — N_a(t) and mu_a - mu_b
  decaying to zero, twin axes; MP4 3 `chemical-barometric` — column of dots settling into the
  exponential profile with the constant-mu level line.
- **Quiz bank outline** — `assessment/quizzes/13-chemical-potential.en.yml`:
  - `Q-13-1` MC — which quantity equalizes at particle equilibrium (OBJ-13-3;
    distractor: concentration, from `particles-flow-concentration`).
  - `Q-13-2` numeric — finite-difference mu from tabulated S(N) at fixed U, V (OBJ-13-1).
  - `Q-13-3` MC — why G = mu N holds for one component but F != mu N (OBJ-13-2).
  - `Q-13-4` MC — flow direction given (mu, n) pairs where mu and n rank oppositely
    (OBJ-13-3, OBJ-13-4; distractor from `mu-energy-per-particle`).
  - `Q-13-5` numeric — density ratio between two heights from constant mu (OBJ-13-5).
  - `Q-13-6` MC — which hypotheses the grand-canonical weight needs (OBJ-13-6; distractor
    echoes `canonical-equal-probability`: "all (E_s, N_s) states equally probable").
  - `Q-13-7` numeric — site occupation at given (epsilon - mu)/kB T (OBJ-13-6).
  - `Q-13-8` numeric — mass-action ratio n_B/n_A for a toy Delta-epsilon (OBJ-13-7).
  - `Q-13-9` MC — osmosis direction and van 't Hoff magnitude (OBJ-13-7; distractor from
    `osmosis-solute-flow`).
  - `Q-13-10` free — explain in words why classical ideal-gas mu is negative and what changes
    as n approaches n_Q (OBJ-13-1, OBJ-13-5; seeds 17). Every OBJ covered at least once.
- **Problem set outline** — `13-chemical-potential-problems.md`: analytical — (P1) two-exchange
  maximization: derive equal T *and* equal mu simultaneously [OBJ-13-4]; (P2) G = mu N from the
  Euler relation, and why mu depends only on (T, P) [OBJ-13-2]; (P3) isothermal column with an
  adsorbing floor: split N between column and surface [OBJ-13-5, OBJ-13-6]; computational —
  (P4) fluctuation of mu_a - mu_b vs N_total, fit the power law [OBJ-13-3]; (P5) fit a Langmuir
  isotherm to simulated occupancy vs pressure [OBJ-13-6]; challenge — (P6) two-solute membrane
  ladder: chain van 't Hoff across two compartments and predict the final levels [OBJ-13-7].
- **Runtime budget** — Pyodide-safe: the exchange sim tracks a single integer N_a per step
  (equilibrium.py's pattern); 10^5 steps at N_total = 2x10^4 runs in ~1 s (scalar loop, no
  per-particle arrays; pre-draw the two uniform arrays). Occupation curves and barometric
  profiles are closed-form NumPy vectors (10^3 points). No Numba; nothing exceeds a few
  seconds in-browser. Widgets: 4 sliders + 2 tabs, pure ipywidgets + matplotlib.
- **Validation gates** — the six per-module commands (README bottom) with
  `--module 13-chemical-potential`; extra: `check_modelspec.py` must see the new `advanced/`
  path, and the myst.yml TOC gains the `advanced/` chapter in the same commit.
- **Open questions for the author** — each with a recommendation:
  1. Ideal-gas mu form: `\kB T \ln(n/n_Q)` with `n_Q` named-but-deferred, vs the classical form
     with an unnamed additive constant. *Recommend* `n/n_Q` + a forward-pointer box to 17: the
     formula stays absolute, mu < 0 has a visible reference point, and 17 pays it off.
  2. Centrepiece flavour: two offset gas boxes vs gas-above-adsorbing-surface. *Recommend*
     offset boxes as centrepiece (cleanest concentration falsifier), adsorption as explore tab 2.
  3. Advanced section depth for fugacity/activity + Gibbs–Duhem re-read. *Recommend* brief —
     one screen, names and one back-link each; nothing downstream depends on it.
  4. Real experiment: dialysis tubing vs gummy bear. *Recommend* tubing as the graded version
     (quantitative Pi vs c), gummy bear as the take-home variant in the same CSV format.
  5. Gibbs–Duhem glossary key ownership (09 derives it, 13 re-reads it). *Recommend* 09 lands
     the key; 13 only cross-references. Coordinate when 09's plan is written.

## 4. Library and tests

- **`src/thermolab` — existing used:** `fundamental.py` (09) — model `S(U,V,N)` relations that
  `mu_from_entropy` differentiates; `potentials.py` (10) — `G` construction for `mu_from_gibbs`;
  `ensembles.py` (11) — bath machinery and the stored barometric/Boltzmann profile for the
  verify overlay; `partition.py` (12) — single-site `Z` cross-check of `site_occupation`;
  `constants.K_B`; `validation.relative_error` / `scaling_exponent` (lab fits).
- **`src/thermolab` — new: `chemical.py`** (introduced by 13 per README ownership; serves 13,
  14, 17; no extender). Docstring header carries the 7-bullet model spec from §3 verbatim.
  Functions (signature — one-line contract):
  `mu_from_entropy(relation, n_particles, energy, volume, dn=1.0) -> float` — numeric
  `-T (\partial S/\partial N)|_{U,V}` by central difference on any callable `S(U, V, N)`;
  `mu_from_gibbs(gibbs, n_particles, temperature, pressure, dn=1.0) -> float` — numeric
  `(\partial G/\partial N)|_{T,P}`, the practical face, testable against the entropic one;
  `ideal_gas_mu(number_density, temperature, mass, u_ext=0.0) -> float` —
  `\kB T \ln(n/n_Q) + u_{ext}` in J, with `n_Q(T, m)` computed internally;
  `quantum_concentration(temperature, mass) -> float` — `n_Q` [1/m^3], named constant for 17;
  `particle_exchange_sim(system_a, system_b, n_steps, rng) -> ExchangeTrace` — Metropolis hop
  dynamics; trace of `N_a(t)` plus derived `mu_a(t) - mu_b(t) -> 0`, `N_total` exactly conserved;
  `equilibrium_split(system_a, system_b) -> tuple[float, float]` — closed-form
  `n_a/n_b = e^{-(u_a-u_b)/(\kB T)}` endpoint the sim must reproduce;
  `site_occupation(mu, temperature, site_energy) -> float` — independent-site grand-canonical
  `1/(e^{(\epsilon-\mu)/(\kB T)} + 1)`;
  `mass_action_equilibrium(delta_epsilon, temperature, nq_ratio=1.0) -> float` — toy A ⇌ B
  ratio `n_B/n_A` from mu balance;
  `osmotic_pressure(concentration, temperature) -> float` — van 't Hoff `\Pi = n_s \kB T` [Pa].
- **`tests/physics/` additions:** dimensional — mu functions return J, `osmotic_pressure`
  returns Pa, `quantum_concentration` returns 1/m^3 (`test_dimensions.py`); conservation —
  `particle_exchange_sim` conserves `N_a + N_b` exactly every step (`test_conservation.py`);
  analytic-limit — `mu_from_entropy` on the Sackur–Tetrode relation matches `ideal_gas_mu` to
  0.1%, `mu_from_gibbs` matches `mu_from_entropy`, sim endpoint matches `equilibrium_split`,
  barometric profile from constant mu matches 11's Boltzmann result, `site_occupation` → 0/1
  in the `\epsilon \mp \mu \gg \kB T` limits (`test_limits.py`); large-N — std of
  `mu_a - mu_b` at equilibrium shrinks with a fitted negative power of `N_total`
  (`test_scaling.py`); convergence — `mu_from_entropy` central-difference error falls as
  `dn^2` under stencil refinement (`test_convergence.py`); seed-independence — exchange
  equilibrium split agrees across generators within statistical error (`test_seeds.py`).

## 5. Assessment hooks

Checkpoint synthesis: 09 + 13 — one maximization principle, three slopes (energy exchange gives
equal T, volume gives equal P, particles give equal mu): a single problem walks all three on one
`S(U,V,N)` surface. 11 + 13 — the barometric formula derived twice, students must state which
hypotheses each route needs. Exam themes: flow-direction ranking tasks with mu/density traps
(Q-13-4's discriminator); "why is mu negative" as a free-response staple; grand-canonical
hypotheses vs the canonical-equal-probability trap. Feeds forward: 14's opening problem
(coexistence as two-box mu equality with the boxes as phases) consumes `chemical.py` verbatim;
17's occupation-function capstone re-labels `site_occupation` as Fermi-Dirac and asks what
changed (nothing but the name); the 08-owed mixing/Gibbs-paradox teaser becomes a synthesis
problem here (two-species exchange, indistinguishability fixing extensivity).

## 6. Build order and validation gates

Build after 12 — 13 opens the advanced tier and is the first page in the new
`content/en/advanced/` directory, so its commit also creates the directory and adds the
`advanced/` chapter to `content/en/myst.yml`'s TOC (placement decision recorded in README's
canonical map). It must not land before 09–12: every derivation leans on their results, and
`chemical.py` imports from `fundamental`, `potentials`, and `ensembles` (single-owner rule —
no file introduced by a later module is imported by an earlier one). Alongside it land: the
three NEW misconception entries in `assessment/misconceptions.yml` (`status: addressed` with
falsifier + distractor as staged in §3), and the §3 glossary keys in `glossary/terms.yml` with
`he_reject` candidates. HE-mirror artifact family: `content/he/advanced/13-chemical-potential.md`
+ `-problems.md`, `notebooks/he/labs/13-chemical-potential.ipynb`,
`assessment/quizzes/13-chemical-potential.he.yml`, each stamped with `en_source_hash`; the page
is listed in `translation-pending.txt` until the mirror lands. Gates: the six README commands
with `--module 13-chemical-potential`.

## 7. Deviations from the brainstorm

- **Independent-site shortcut instead of full grand-Z.** Brainstorm row 13 says "grand canonical
  ensemble"; this plan derives the grand-canonical *weight* and applies it only to independent
  single sites, deferring `\Xi` and its derivative machinery to 17. Rationale: one site delivers
  every payoff this module needs (Langmuir curve, FD preview) at a tenth of the formalism.
- **Reactions and osmosis scoped as toys.** "Reactions and osmotic equilibrium" is honoured as
  A ⇌ B mass action and dilute van 't Hoff only — no standard states, no thermochemistry.
  Rationale: the point is mu balance as a master principle, not chemistry coverage.
- **First module in the new `advanced/` directory.** Content layout addition (TOC chapter at
  build time) not spelled out in the brainstorm row; follows README's canonical-map decision.
- **Additions beyond the row:** the concentration-vs-mu puzzle framing, the boxed barometric
  double-derivation (11 back-link), the `n_Q` forward-pointer box, and the dialysis-tubing
  osmosis experiment — all in service of §2's spiral and §7's epistemic-labeling framework.
