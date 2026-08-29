# Module 14 — Phase equilibrium — Implementation Plan

> **Brainstorm:** §3 module 14 (+ §5 phase-transition laboratory, first half: "start with van
> der Waals isotherms and coexistence"; §6 misconceptions; §7 accuracy framework).
> **Module id:** `14-coexistence`. **Content path:** `content/en/advanced/14-coexistence.md`.
> **Status:** planned. Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Module 02 ended on a deliberate cliff-hanger: below T_c the van der Waals isotherm wiggles
through states where *compressing the gas lowers its pressure*. Module 09's stability criterion
now names the crime — $(\partial P/\partial v)_T > 0$ is mechanically impossible to sustain —
and this module watches nature refuse: real isotherms replace the wiggle with a dead-flat line
at exactly one pressure. The driving question is *who decides where the line goes*, and the
answer is the payoff of the whole 09 → 10 → 13 arc: two phases coexisting must agree on T, on
P, and on the chemical potential mu. From that single requirement the Maxwell equal-area
construction falls out as a *theorem* — integrate $d\mu = v\,dP$ along the model isotherm —
not as the aesthetic "make the areas look equal" gesture most textbooks offer.

The centrepiece is the brainstorm row's "phase diagram with movable coexistence point", built
live from the model: drag T along the coexistence curve and watch the flat line P_sat, the two
coexisting volumes, and the shaded equal areas update together; assemble the P_sat(T) points
into the full P-T diagram whose liquid-gas curve *ends* at 02's critical point. Along the way
the row's remaining cargo lands with proofs attached: the lever rule, Clausius-Clapeyron
$dP_{sat}/dT = L/(T\,\Delta v)$ derived from mu equality along the curve, latent heat computed
from the model, and the Gibbs phase rule demonstrated on the one-component diagram.

Beyond the row, the plan promotes metastability from footnote to physics: the binodal-spinodal
gap is where superheated water in a microwave and bubble-chamber detectors actually live, and
an explicit validity box says what mean-field vdW gets right (the states exist) and what it
ignores (nucleation kinetics decide their lifetime). The module is 15's mean-field warm-up:
first-order transitions, coexistence, and a curve that terminates at a critical point — where
15 picks up with what happens *at* that point.

## 2. Position in the course

- **Requires:** `02-equations-of-state` — `gases.py` as-is: `van_der_waals_pressure`,
  `vdw_critical_point` ($(v_c, T_c, P_c) = (3b,\ 8a/(27 \kB b),\ a/(27 b^2))$),
  `vdw_constants_from_critical`, reduced variables, and the wiggle left as an open-question
  box; `09-fundamental-relation` — stability from entropy concavity:
  $(\partial P/\partial v)_T \le 0$, i.e. $\kappa_T \ge 0$; `10-potentials` — G is minimized
  at fixed (T, P), and G = N mu for one component; `13-chemical-potential` — mu-equality as
  the particle-exchange equilibrium condition, and Gibbs-Duhem $d\mu = -s\,dT + v\,dP$.
- **Feeds:** `15-ising` — first-order/coexistence language, the mean-field disclaimer, and the
  shrinking $v_g - v_l \sim (1 - T/T_c)^{1/2}$ near T_c as the order-parameter seed; the
  liquid-gas curve *ending* at a critical point is 15's opening puzzle (what transition has no
  latent heat?); `17-quantum-gases` — BEC framed as a phase transition echo (mu pinned at the
  band edge plays the role P_sat plays here).
- **Explicitly not assumed:** order parameters, symmetry breaking, critical exponents,
  universality, Ising/Monte Carlo machinery — all 15's; any solid-phase model (vdW has none —
  see §3 open question 2); nucleation theory (named as the missing kinetics, never developed).

## 3. Module specification

- **Identity and scope** — brainstorm row 14: Gibbs phase rule, latent heat,
  Clausius-Clapeyron, van der Waals fluid; centrepiece "phase diagram with movable coexistence
  point". Covered: instability of the wiggle, spinodal, coexistence conditions, Maxwell
  construction via mu, lever rule, Clausius-Clapeyron, latent heat, phase rule, metastability.
  Deferred: the vdW EOS itself (02 owns it, per its deviation log); critical *behaviour*,
  order parameters, exponents → 15; solid phases and sublimation modeling → none (real-data
  demonstration only); nucleation kinetics → out of course scope, honestly flagged.
- **Prerequisites** — 02: vdW isotherms, critical point, reduced variables; 09: the stability
  criterion as a theorem; 10: min-G at fixed (T, P); 13: mu, mu-equality, Gibbs-Duhem.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-14-1`: Identify the segment of a sub-critical van der Waals isotherm where
    (dP/dv)_T > 0, explain why module 09's stability criterion forbids it, and locate the
    spinodal points where (dP/dv)_T changes sign.
  - `OBJ-14-2`: State the coexistence conditions — equal T, equal P, equal mu between the two
    phases — and derive the Maxwell equal-area construction as a theorem by integrating
    d mu = v dP along the isotherm between the coexisting states.
  - `OBJ-14-3`: Compute (P_sat, v_liq, v_gas) at a given T for a van der Waals fluid and use
    the lever rule x_gas = (v - v_liq)/(v_gas - v_liq) to find the phase fractions of a mixed
    state.
  - `OBJ-14-4`: Derive Clausius-Clapeyron dP_sat/dT = L/(T (v_gas - v_liq)) from mu equality
    along the coexistence curve, and use it to predict how the boiling point moves with
    ambient pressure.
  - `OBJ-14-5`: Compute the latent heat L = T (s_gas - s_liq) from the van der Waals model and
    extract the latent heat of water from published P_sat(T) data via a Clausius-Clapeyron
    fit, with an error estimate.
  - `OBJ-14-6`: State the Gibbs phase rule F = C - P + 2, derive it by counting mu-equality
    constraints, and read F off each feature of a one-component phase diagram (area, curve,
    triple point, critical point).
  - `OBJ-14-7`: Distinguish binodal from spinodal, explain why superheated and supercooled
    states between them are real but nucleation-limited, and state what the mean-field van
    der Waals model can and cannot say about them.
- **Mathematical background** — already has: partial derivatives, curves as constraints (00,
  02), Legendre/Gibbs-Duhem structure (10, 13). New here: root-finding as a physics tool —
  bracketing, bisection/Brent, and what "the roots coalesce" does to a solver near T_c.
- **Physical intuition goals** — student can predict, without algebra: (1) a pressure cooker
  raises the boiling point and altitude lowers it — pressure, not "100 C", decides; (2) while
  water boils at fixed P the thermometer freezes in place however hard the burner runs — only
  the boil *rate* changes; (3) halfway across the flat segment the cylinder holds liquid and
  vapor in lever-rule proportions — no molecule is "half evaporated"; (4) as T → T_c the two
  coexisting densities merge and the latent heat dies — above T_c there is nothing to boil.
- **Section skeleton seeds** — contract order:
  - *puzzle:* 02's saved isotherm reopened: between the spinodals, squeezing the gas *lowers*
    its pressure — a state that would collapse at the first fluctuation (09's criterion).
    Real CO2 instead flat-lines at one pressure. Boxed question: the model offers a continuum
    of horizontal chords — what physical law picks the unique height of the flat line?
  - *predict:* (1) where does the flat line sit — top of the wiggle, bottom, or somewhere
    forced by a conservation-like rule? sketch it; (2) water boils on a 3000 m mountain:
    above, below, or at 100 C? (targets `boiling-fixed-temperature`); (3) a kettle at a
    rolling boil gets its burner doubled — what does the thermometer do? (targets
    `boiling-heat-raises-t`); (4) heat a sealed half-full container past T_c — does the
    liquid boil away, or something stranger? (targets `critical-point-runs-out`).
  - *explore:* the movable-coexistence-point explorer — T slider below T_c drives the P-v
    panel (wiggle, flat line, shaded equal areas, spinodal ticks) and a synchronized P-T
    panel where the dragged point traces P_sat(T) up to the critical point; toggles: mu-vs-P
    loop inset (the crossing *is* P_sat), binodal/spinodal overlay, lever-rule readout.
  - *derive:* wiggle instability from 09 → coexistence conditions from 10 + 13 → equal-area
    as a theorem via $\int v\,dP = 0$ → lever rule → Clausius-Clapeyron from mu equality
    along the curve → vdW latent heat → phase rule. Full route under core derivations.
  - *verify:* equal-mu and equal-area solvers agree to tolerance; maxwell_construction
    collapses to $(v_c, P_c)$ as T → T_c; `clausius_clapeyron_check` — numeric dP_sat/dT vs
    L/(T Δv) — becomes the `numerical-observation` admonition; steam-table fit vs 2.26 MJ/kg.
  - *transfer:* back to 02 (the open-question box closes — link both ways); back to 09/13
    (stability and mu do real work); forward to 15 (the curve *ends*: what is a transition
    with no latent heat?); 17 (BEC as mu hitting its ceiling); everyday: pressure cookers,
    altitude cooking, freeze-drying below the triple point.
  - *quiz:* wiggle diagnosis; what fixes P_sat; lever rule; boiling vs pressure;
    Clausius-Clapeyron estimate; latent-heat plateau; phase-rule counting; critical point.
  - *explain:* (1) why "the areas are equal" is a theorem here and not a drawing rule —
    where mu enters; (2) why boiling water cannot exceed its boiling temperature while the
    pressure holds; (3) why a superheated liquid can exist at all if the flat line is "the"
    equilibrium; (4) what dies at the critical point, in one paragraph without formulas.
  - *advanced (optional, always last):* corresponding-states collapse of coexistence curves —
    P_sat/P_c vs T/T_c for several a, b pairs lands on one universal curve (02's reduced
    variables cashing in). Safe-to-skip boundary: 15 and 17 core depend on nothing here.
- **Core derivations** — ordered:
  1. Instability: 09's criterion $(\partial P/\partial v)_T \le 0$; the vdW wiggle violates
     it between the spinodal points, where $\kB T = \dfrac{2a\,(v-b)^2}{v^3}$.
  2. Coexistence: two phases exchanging energy, volume, particles ⇒ $T_l = T_g$, $P_l = P_g$,
     $\mu_l = \mu_g$; equivalently (10) $G = N_l \mu_l + N_g \mu_g$ is minimal at fixed (T,P)
     only when the mus agree.
  3. Equal-area theorem: at fixed T, Gibbs-Duhem gives $d\mu = v\,dP$; integrating along the
     model isotherm between the coexisting states, $\mu_g - \mu_l = \int_l^g v\,dP = 0$;
     by parts: $P_{sat}\,(v_g - v_l) = \int_{v_l}^{v_g} P(v)\,dv$ — the two lobes cut by the
     chord have equal areas, as a *consequence* of mu equality.
  4. Lever rule: $v = x_l v_l + x_g v_g$, $x_l + x_g = 1$ ⇒ $x_g = \dfrac{v - v_l}{v_g - v_l}$.
  5. Clausius-Clapeyron: $\mu_l(T, P_{sat}(T)) = \mu_g(T, P_{sat}(T))$ differentiated along
     the curve: $-s_l + v_l \dfrac{dP_{sat}}{dT} = -s_g + v_g \dfrac{dP_{sat}}{dT}$ ⇒
     $\dfrac{dP_{sat}}{dT} = \dfrac{s_g - s_l}{v_g - v_l} = \dfrac{L}{T\,\Delta v}$,
     with $L = T\,(s_g - s_l)$ per particle.
  6. vdW latent heat: at fixed T, $\Delta s = \kB \ln\dfrac{v_g - b}{v_l - b}$ ⇒
     $L = \kB T \ln\dfrac{v_g - b}{v_l - b}$; first-law cross-check with
     $\dbar Q = dU - \dbar\Won = dU + P\,dV$: $L = \Delta u + P_{sat}\,\Delta v$,
     $\Delta u = a\,(1/v_l - 1/v_g)$ — two routes, one number (a lab assertion).
  7. Phase rule: C components, P phases: P(C - 1) + 2 knobs minus C(P - 1) mu-equalities ⇒
     $F = C - P + 2$; one component: areas F = 2, curves F = 1, triple point F = 0; the
     critical point is where the liquid-gas curve stops being a boundary at all.
- **Model specification draft** — for the coexistence explorer (page MP4s + lab widget):
  - **System:** one van der Waals fluid (fixed N, fitted a and b) described by (P, v, T),
    split at coexistence into two homogeneous phases sharing T, P, mu.
  - **Dynamics:** none — every rendered state is equilibrium; dragging T re-solves statics.
  - **Boundary:** closed to matter; T and total v set externally, P read off the construction.
  - **Ensemble:** not applicable — macroscopic thermodynamics on a mean-field EOS.
  - **Ignored:** interfaces and surface tension (the two phases meet at zero cost);
    nucleation kinetics (metastable lifetimes); any solid phase; fluctuations near T_c.
  - **Valid when:** moderate densities, T not too far below T_c, one-component fluid;
    metastable *existence* (not lifetime) between binodal and spinodal.
  - **Failure modes:** near T_c mean-field exponents are quantitatively wrong (15's story);
    deep sub-critical liquids where vdW misses real-liquid structure; no triple point.
- **Epistemic classification** — boxed claims: vdW EOS → `model-assumption` (inherited from
  02, restated); stability criterion → `theorem` (09's concavity); coexistence conditions →
  `theorem`; equal-area construction → `theorem` — THE mandatory box, "given mu equality
  along the model isotherm"; Clausius-Clapeyron → `theorem`; phase rule → `theorem` (with F,
  C, P boxed as `definition`); metastable branches → `model-assumption` + `approximation`
  (real physics, mean-field validity limits, kinetics ignored); dP_sat/dT vs L/(T Δv) match
  and the steam-table fit → `numerical-observation`.
- **Misconceptions** — none of the existing registry entries is assigned here; three NEW
  entries (ids collide with nothing in `assessment/misconceptions.yml`):
  - `boiling-fixed-temperature` · "Water boils at exactly 100 C, period." · falsifier: the
    P_sat(T) steam-table curve — boiling happens where P_sat meets ambient pressure; the lab
    computes ~90 C at 0.7 atm · distractor: Q-14-4 option "100 C — altitude is irrelevant".
  - `boiling-heat-raises-t` · "While a liquid boils, added heat keeps raising its
    temperature." · falsifier: kettle + thermometer T(t) plateau while heat pours in —
    latent heat is absorbed at fixed T · distractor: Q-14-6 option "T climbs, just slower".
  - `critical-point-runs-out` · "The critical point is where the substance runs out of
    liquid." · falsifier: a continuous P-T path around the critical point turns gas into
    liquid with no transition crossed — the distinction dissolves; nothing is exhausted ·
    distractor: Q-14-8 option "the last of the liquid evaporates there".
- **Glossary terms** — reused: `van-der-waals`, `critical-point`, `isotherm`, `condensation`,
  `reduced-variables`, `corresponding-states` (02); `chemical-potential` (13); `free-energy`.
  NEW (key / en / suggested he / `he_reject`): `phase` / phase / פאזה / [פזה];
  `phase-diagram` / phase diagram / דיאגרמת פאזות / —; `coexistence` / coexistence /
  דו-קיום / —; `saturation-pressure` / saturation pressure / לחץ רוויה / —; `latent-heat` /
  latent heat / חום כמוס / —; `maxwell-construction` / Maxwell construction / בניית מקסוול /
  —; `clausius-clapeyron` / Clausius-Clapeyron equation / משוואת קלאוזיוס–קלפרון /
  [קלאוסיוס]; `lever-rule` / lever rule / כלל המנוף / —; `binodal` / binodal / בינודל / —;
  `spinodal` / spinodal / ספינודל / —; `metastable` / metastable / מטא-יציב / [מטה יציב];
  `triple-point` / triple point / נקודה משולשת / —; `gibbs-phase-rule` / Gibbs phase rule /
  כלל הפאזות של גיבס / —; `superheating` / superheating / חימום-יתר / —; `nucleation` /
  nucleation / גרעון / [נוקלאציה].
- **Interactive controls and simulations** — (1) *Maxwell explorer*: T slider (0.80–0.999
  T_c), P-v panel with wiggle + flat line + shaded lobes + spinodal ticks; mu-vs-P loop inset
  toggle — the self-intersection sits exactly at P_sat. (2) *phase-diagram builder*: the
  centrepiece — drag the coexistence point along P_sat(T) in the P-T plane, synchronized P-v
  view; binodal/spinodal domes overlaid in P-v; curve visibly terminates at (T_c, P_c).
  (3) *lever-rule explorer*: drag total v across the flat segment; stacked liquid/vapor
  fraction bar. (4) *around-the-critical-point*: animate a P-T path over the curve's end —
  density changes smoothly (falsifies `critical-point-runs-out`).
- **Virtual lab outline** — `notebooks/en/labs/14-coexistence.ipynb`: (1) setup — import
  `gases`, `phases`, constants; CO2's a, b via `vdw_constants_from_critical`; (2) prediction
  cells (commit first); (3) reopen 02's sub-critical isotherm, finite-difference (dP/dv)_T,
  shade the forbidden segment, mark spinodals; (4) `maxwell_construction` at one T: flat
  line, shaded lobes, mu(P) loop, assert equal-mu ≡ equal-area to tolerance; (5)
  `coexistence_curve` on a T-grid → P-T diagram ending at the critical point; overlay NIST
  CO2 saturation data; (6) `lever_rule` sweep across the dome; (7) `latent_heat` vs T — L →
  0 at T_c plotted; `clausius_clapeyron_check` asserted; (8) import the water steam-table
  CSV, fit ln P_sat vs 1/T (ideal-vapor form: slope = -L/kB), propagate fit error; (9)
  *measurement:* L(water) = value ± error from the fit, quoted against 2.26 MJ/kg (~40.7
  kJ/mol), with the ideal-vapor approximation's bias named.
- **Real-experiment counterpart** — decision: **published water P_sat(T) steam-table data**
  (NIST/IAPWS rows, ~280–420 K), shipped as a small CSV under `data/` — the quantitative lab
  measurement (Clausius-Clapeyron fit → latent heat, value ± error vs 2.26 MJ/kg). Optional
  bench pairing: kettle + kitchen thermometer — the T(t) boiling plateau falsifies
  `boiling-heat-raises-t` with zero equipment cost; plateau readings importable into the lab
  as a two-column CSV for the misconception cell.
- **Media assets** — `media/render/render_phases.py`, language-neutral (no burned-in text):
  `phases-maxwell.mp4` (T sweeps up: wiggle flattens, equal-area lobes shrink, construction
  collapses onto the critical point); `phases-coexistence.mp4` (P-T curve traced by the
  moving point, synchronized P-v panel, curve ending at T_c); `phases-lever.mp4` (state
  point crossing the dome, phase-fraction bar rebalancing).
- **Quiz bank outline** — every objective covered at least once; ASCII math:
  - `Q-14-1` (multiple-choice, OBJ-14-1): which isotherm segment is unphysical and why;
    distractor "the whole sub-critical isotherm is wrong".
  - `Q-14-2` (multiple-choice, OBJ-14-2): what fixes P_sat; distractor "the line is drawn
    where the two areas look equal — a graphical convention".
  - `Q-14-3` (numeric, OBJ-14-3): given (v_liq, v_gas) at some T, lever-rule fractions at a
    stated total v.
  - `Q-14-4` (multiple-choice, OBJ-14-4): boiling on a 3000 m mountain; distractor from
    `boiling-fixed-temperature`.
  - `Q-14-5` (numeric, OBJ-14-4 + OBJ-14-5): P_sat at two nearby temperatures given —
    estimate L via dP_sat/dT ≈ ΔP/ΔT = L/(T Δv), ideal-vapor Δv.
  - `Q-14-6` (multiple-choice, OBJ-14-5): burner doubled under boiling water — thermometer
    response; distractor from `boiling-heat-raises-t`.
  - `Q-14-7` (multiple-choice, OBJ-14-6): F at the triple point of a pure substance;
    distractor F = 1 from miscounting constraints.
  - `Q-14-8` (multiple-choice, OBJ-14-7): sealed half-full container heated past T_c;
    distractor from `critical-point-runs-out`.
  - `Q-14-9` (free, OBJ-14-2 + OBJ-14-7): explain why equal areas follows from mu equality,
    and why a superheated liquid can nonetheless exist for a while.
- **Problem set outline** — `14-coexistence-problems.md`: *analytical* — derive the spinodal
  condition and its T_c endpoint (OBJ-14-1); equal-area from d mu = v dP, by parts
  (OBJ-14-2); Clausius-Clapeyron, then show L → 0 and Δv → 0 at T_c while dP_sat/dT stays
  finite (OBJ-14-4/5). *Computational* — coexistence curves for two (a, b) pairs collapse in
  reduced variables (OBJ-14-3, advanced tie-in); steam-table fit with residual analysis
  (OBJ-14-5). *Challenge* — estimate water's superheat limit at 1 atm from the spinodal and
  confront microwave-superheating reports; why does reality stop short? (OBJ-14-7).
- **Runtime budget** — deterministic root-finding only, vectorized NumPy (no Numba in
  Pyodide): Brent solves on 10^3-point v-grids, ~3 root brackets per T; a 100-point
  coexistence curve costs ~10^5 EOS evaluations — well under a second. Widgets redraw on
  slider *release*; matplotlib, not physics, is the bottleneck. Target: every lab cell
  interactive in-browser in seconds.
- **Validation gates** — the six README commands with `--module 14-coexistence`, plus: the
  convergence pin — `maxwell_construction` documented and tested to converge for
  T ≤ 0.999 T_c at the stated tolerance (the near-T_c conditioning test below).
- **Open questions for the author** —
  1. Worked-example substance: CO2 (good vdW fluid, data already shipped by 02) vs water
     (familiar, vdW-poor). **Recommend:** CO2 for all model-side numbers, water only for the
     steam-table lab — and say the mismatch out loud; it is an epistemic lesson.
  2. Triple point without a solid phase in the model: schematic only, or real water P-T data?
     **Recommend:** ship a tiny real water phase-boundary CSV and plot the true diagram
     beside the model one; the phase rule is demonstrated on reality, the model shown honest.
  3. mu(P) loop inset: always visible or a toggle? **Recommend:** toggle, default off — it is
     the theorem made visible, but the first read should stay uncluttered.
  4. Advanced section: corresponding-states collapse vs multicomponent phase rule.
     **Recommend:** corresponding-states — pretty, computationally free, reinforces 02;
     multicomponent F-counting fits better as a one-line problem-set challenge.

## 4. Library and tests

- **`src/thermolab` — existing used:** `gases.py` (02): `van_der_waals_pressure`,
  `vdw_critical_point`, `vdw_constants_from_critical`, `reduced_variables`,
  `isotherm_family`; `potentials.py` (10): Gibbs/Helmholtz evaluators for the mu loop;
  `chemical.py` (13): mu conventions; `constants.py` (`K_B`); `validation.relative_error`.
  Consumes only — extends nothing (README single-owner rule; C4-family note: `phases.py` is
  the deterministic half of brainstorm §9's `phase_transitions.py`, split from 15's
  `ising.py`).
- **`src/thermolab` — new:** `phases.py` (ownership table: introduced by 14, extended by
  none; serves 14, 15). Docstring header, 7 bullets in fixed order — System: a one-component
  van der Waals fluid at coexistence, two homogeneous phases sharing T, P, mu / Dynamics:
  none — every function solves equilibrium conditions / Boundary: closed; T set, P_sat and
  volumes solved for / Ensemble: not applicable — macroscopic thermodynamics / Ignored:
  interfaces, nucleation kinetics, solid phases, near-critical fluctuations / Valid when:
  0 < T < T_c for construction routines; metastable branches as existence statements only /
  Failure modes: T → T_c (coalescing roots — see strategy note), T ≥ T_c (no coexistence;
  raises), mean-field exponents near T_c. Functions:
  - `vdw_chemical_potential(v, temperature, a, b) -> np.ndarray` — mu(T, v) up to an
    additive f(T) (irrelevant to equality at fixed T); powers the loop plot and residual.
  - `maxwell_construction(temperature, a, b) -> tuple[float, float, float]` —
    (p_sat, v_liq, v_gas) by root-finding: bracket P between the two spinodal pressures,
    Brent on the outer roots of P(v) = P per candidate, bisect the equal-area residual
    `∫P dv - P Δv` (≡ mu difference) to zero. Raises for T ≥ T_c.
  - `coexistence_curve(t_grid, a, b) -> tuple[np.ndarray, np.ndarray, np.ndarray]` —
    (p_sat, v_liq, v_gas) arrays over T; NaN above T_c; endpoint pinned at
    (T_c → v_c, P_c).
  - `spinodal_curve(a, b, n_points=200) -> tuple[np.ndarray, np.ndarray, np.ndarray]` —
    (T, v, P) locus of (dP/dv)_T = 0 from kB T = 2a (v-b)^2 / v^3, both branches.
  - `latent_heat(temperature, a, b) -> float` — L = kB T ln((v_gas - b)/(v_liq - b)) in J
    per particle; cross-checked in tests against Δu + P_sat Δv.
  - `clausius_clapeyron_check(temperature, a, b, dt=1e-3) -> tuple[float, float]` —
    (central-difference dP_sat/dT, L/(T Δv)); the verify admonition's two numbers.
  - `lever_rule(v, v_liq, v_gas) -> tuple[float, float]` — (x_liq, x_gas); raises outside
    [v_liq, v_gas].
  Strategy note in the docstring: near T_c the wiggle flattens, v_liq and v_gas coalesce as
  (1 - T/T_c)^(1/2), and the equal-area residual loses contrast; the solver works in reduced
  variables internally for conditioning, and its documented domain is T ≤ 0.999 T_c at
  rtol 1e-9 — beyond that it raises rather than returning noise.
- **`tests/physics/` additions** (six categories):
  - *dimensional:* `maxwell_construction` returns (Pa, m^3, m^3) under pint re-evaluation;
    `latent_heat` returns J; `lever_rule` fractions dimensionless summing to 1.
  - *conservation:* n/a — no dynamics, nothing transported; discharged by the lever-rule
    closure x_liq + x_gas = 1 and the roundtrip v = x_l v_l + x_g v_g (exact).
  - *analytic-limit:* equal-mu and equal-area residuals vanish together at the solution
    (theorem check, rtol 1e-8); construction collapses to `vdw_critical_point`'s (v_c, P_c)
    as T → T_c; spinodal endpoints meet the binodal at T_c; latent-heat closed form equals
    Δu + P_sat Δv; L → 0 as T → T_c; T ≥ T_c raises.
  - *large-N:* n/a — macroscopic EOS analysis; no particle number appears (stated, not
    skipped silently).
  - *convergence:* p_sat error falls at the solver's documented order as tolerance/grid
    refine; convergence holds up to the pinned T = 0.999 T_c domain edge; dP_sat/dT central
    difference converges at O(dt^2) toward L/(T Δv).
  - *seed-independence:* n/a — fully deterministic; no RNG anywhere in the file.

## 5. Assessment hooks

Checkpoint synthesis (module-level, not one section): (a) 09 + 13 + 14 — a full audit of the
wiggle: which of its three segments are stable, metastable, forbidden, and by which criterion;
(b) 02 + 14 — fit a, b from a substance's critical data, predict P_sat at a stated T, and
grade the prediction against tabulated data with the tolerance declared first; (c) the
steam-table capstone: L ± error from the fit, then the fit's own assumptions (ideal vapor,
L constant) audited via residuals. Exam themes: theorem-vs-drawing status of equal areas;
phase-rule counting under time pressure; metastable-vs-forbidden classification. Feeds 15's
opening (a transition with no latent heat) and its mean-field-limits discussion; feeds 17's
BEC-as-transition framing; the corresponding-states collapse is a ready capstone shared with 02.

## 6. Build order and validation gates

Builds after 02 (needs `gases.py` as shipped) and after 09, 10, 13 in teaching order — the mu
argument is the plan's spine, so 13 must exist first; 14 opens the `advanced/` directory
family started by 13 and unblocks 15's language. Lands together in one change: page + problems
+ lab + quiz bank; `phases.py` + its six-category tests; three NEW misconception entries
(status `addressed`) in `assessment/misconceptions.yml`; fifteen NEW glossary keys with
`he_reject` candidates in `glossary/terms.yml`; the water steam-table CSV (and the small real
phase-boundary CSV if open question 2 lands) under `data/`; `media/render/render_phases.py`
with the three MP4s. 02's open-question wiggle box gets its forward link flipped to a resolved
cross-reference. HE mirror family (`.he.yml` quiz, HE page/problems/lab with `en_source_hash`
stamps) follows; until it lands the page is listed in `translation-pending.txt`. Gates: the
six README commands with `--module 14-coexistence` plus the near-T_c convergence pin (§3).

## 7. Deviations from the brainstorm

- **Equal-area justified via mu, not the area hand-wave (method decision).** The construction
  is boxed as a `theorem` derived from ∫ v dP = 0 along the isotherm — 13's mu machinery makes
  the honest route free, and §7's epistemic framework forbids presenting a drawing rule as
  physics.
- **vdW EOS ownership stays with 02 (re-scope, mirror of 02's log).** Brainstorm row 14 lists
  "van der Waals fluid"; 02 built it. 14 consumes `gases.py` unchanged and adds only
  coexistence analysis in `phases.py` — the split half of §9's `phase_transitions.py`
  (README: `phases.py` 14-deterministic / `ising.py` 15-stochastic).
- **Metastability promoted to real physics (addition).** Superheated microwave water and
  bubble chambers enter the core narrative with a model-assumption box on what mean-field vdW
  omits (nucleation kinetics) — not a footnote, because the binodal/spinodal gap is where the
  stability theorem earns its keep.
- **Triple point demonstrated on real data (honesty deviation).** vdW has no solid phase, so
  the row's "Gibbs phase rule" is stated as a theorem and read off a real water P-T diagram,
  not the model's — the model's missing solid is named as a failure mode.
- **Slug names the centrepiece.** `14-coexistence` rather than "phase equilibrium", per the
  README slug note — keeps the two "phase" modules 14/15 unmistakable.
