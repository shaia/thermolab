# Module 05 — Work and thermodynamic paths — Implementation Plan

> **Brainstorm:** §3 module 5, §5 path editor, §10 prototype B. **Module id:** `05-work-paths`.
> **Content path:** `content/en/thermodynamics/05-work-paths.md`. **Status:** built.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Two engineers take the same gas from $A$ to $B$ and pay different bills — the module makes the
state-function/path-function distinction *visually unavoidable*, as brainstorm §5 demands:
routes through the $P$–$V$ plane are constructed, shaded, and priced; the work separates while
$\Delta U$ refuses to. The mathematics gets its honest name — exact versus inexact
differentials — first as pure math in `forms.py`, then wearing physical clothes in `paths.py`.
This is the course's **Prototype B** (brainstorm §10): the vertical slice testing mathematical
interactivity, graphical manipulation, and $\dbar$-versus-$d$.

The first law arrives with the fixed course convention, $dU = \dbar Q + \dbar \Won$, boxed as
a definition with an explicit warning about the rival $-\dbar W_{by}$ convention. The spiral
pays off 04: kinetic theory gave $U = \tfrac{f}{2} N \kB T = \tfrac{f}{2} P V$, so $\Delta U$
is endpoint-only and the first law *forces* $Q$ to be path-dependent by the compensating
amount. Seeds forward: the cycle's enclosed area is 07's engine in embryo, and the advanced
section shows $1/T$ as an integrating factor making $\dbar Q$ exact — the doorstep of 08.

## 2. Position in the course

- **Requires:** 00 — differentials and the units/conventions page; 01 — equilibrium states, so
  one $(P, V)$ pair labels the gas and quasistatic means "always on the state surface"; 04 —
  $P = N \kB T / V$ and equipartition $U = \tfrac{f}{2} N \kB T$, used verbatim for isotherm
  pressure and `internal_energy_change`.
- **Feeds:** 06 directly per conflict C1 — it extends `paths.py` (polytropes, heat capacities,
  process ledger) and derives what 05 asserts; 07 — cycles are `join`ed `Path`s, net work =
  enclosed area, `work_by_system` exists solely for 07's labeled engine convention; 08 — the
  integrating-factor teaser ($dS = \dbar Q_{rev}/T$); 10 — the differential-forms machinery.
- **Explicitly not assumed:** heat capacities $C_V$/$C_P$/Mayer, the derivation of $\gamma$ or
  of $P V^{\gamma} = \text{const}$, entropy, quantitative irreversible processes — all owned
  by 06 (or 07/08). Prose must not lean on them.

## 3. Module specification

**As-built summary.** The page carries all mandatory sections as `(05-work-paths-<suffix>)=`
labels in contract order plus `advanced` last; frontmatter objectives OBJ-05-1..5 in ASCII
math (state vs path functions; W_on = -int P dV; first-law signs; exact vs inexact; when area
= work). Puzzle: same start, same finish, different bill. Predict: four commit-first
questions, Q4 (sudden piston) targeting the area-under-curve over-generalisation. Explore:
7-bullet model spec, two language-neutral MP4 figures (two routes with accumulating work bars;
a cycle shading its enclosed area), JupyterLite lab link. Derive: boxed
$\Won = -\int_{V_1}^{V_2} P\,dV$; isotherm vs isobar-then-isochore (two-leg costs ~45% more);
`definition` boxes for sign convention / state function / path function; an `approximation`
box separating theorem from ideal-gas assumption. Verify: four checks mirrored 1:1 in lab
Part 5 and `tests/physics`, plus a `numerical-observation` box on the absolute-tolerance trap
at $10^{-18}\,\mathrm{J}$. Advanced: cross-derivative test on $\dbar Q$, the $1/T$ integrating
factor, irreversible work via $P_{ext}$. The lab (EN + HE) builds three routes, a cycle,
isotherm-vs-adiabat, then a slider-driven path editor (two movable control points,
piecewise-linear, live $\Won$ against the isothermal reference). Quiz bank: 10 questions
Q-05-1..10 (7 MC, 1 numeric, 1 prediction, 1 short-answer), every objective covered. Problem
set: 6 objective-tagged problems, P6 computational against `thermolab.paths`. All four
assigned misconceptions staged with falsifier + distractor: `heat-stored-in-body` (puzzle +
Q-05-1), `adiabatic-constant-t` (lab Part 3 + Q-05-10), `reversible-just-backward` (transfer
`model-assumption` box + Q-05-5/Q-05-9), `dq-dw-exact` (advanced + problem 5 + Q-05-4).

**Gap list**

1. **C1 boundary (deliberate, owed to 06).** 05 does *not* teach: $C_V$/$C_P$/Mayer/$\gamma$
   derivations ($\gamma = 5/3$ is a plain input in the lab, `adiabatic_pressure`, and
   problems); the derivation of $P V^{\gamma} = \text{const}$ (asserted in one sentence); the
   per-process Q/ΔU/ΔT ledger; the polytropic family; quantitative irreversible processes
   ($P_{ext}$ confined to advanced + problem 4). Once 06 exists, add forward pointers from the
   derive/advanced sections and lab Part 3.
2. **Heat capacities absent entirely** — brainstorm row 5 lists them under module 5; confirmed
   no $C_V$/$C_P$ mention in page/lab/quiz/problems. Correct per C1; no action in 05.
3. **Path editor is preset + sliders, not free-form drawing** (brainstorm §5: students "draw
   curves"). The explore prose ("you place points") slightly oversells. Click-to-place editor
   is a worthwhile later upgrade; not blocking.
4. **Rendered media not in repo** — `render_paths.py` produces `paths-two-routes.mp4` /
   `paths-cycle.mp4` but no MP4 exists anywhere; the figure includes and
   `content/en/_generated/quiz-05-work-paths.md` are build-time artifacts.
5. **Macro drift (cosmetic, course-wide)** — the page writes raw `\delta`, `W_{\mathrm{on}}`,
   `k_B` instead of the `myst.yml` macros `\dbar`/`\Won`/`\kB` that `conventions.md` uses.
6. **C4a duplicate** — `ideal_gas_pressure` in both `kinetics.py` and `paths.py`
   (`ideal_gas_temperature` in `paths.py` only); a cross-module consistency test pins them
   until plan 02 makes `gases.py` the canonical home.
7. **No real-experiment counterpart recorded** — a sealed-syringe / bike-pump pairing is
   cheap; the page should add it or state "none practical".

**Validation gates:** README gate block with `--module 05-work-paths`; lab Part 5 re-asserts
the suite's closed-form, path-dependence, first-law-closure, and convergence checks in-browser.

## 4. Library and tests

- **Existing used:** `constants.K_B`; `forms.py` (pure math, deliberately no model spec):
  `line_integral(m, n, x, y)` — trapezoid $\int M dx + N dy$ along a polyline;
  `mixed_partials_gap(m, n, x, y, h)` — exactness test by central differences; `is_exact(...)`
  — gap negligible everywhere sampled. Lab uses `validation.convergence_study`/`relative_error`.
- **Introduced: `paths.py`** (05 owns; 06 extends). Docstring header carries the 7-bullet
  model spec and the sign convention. `ideal_gas_pressure(n, T, V)` /
  `ideal_gas_temperature(n, P, V)` — ideal-gas law both ways (note C4a);
  `isothermal_pressure(V, n, T)`, `adiabatic_pressure(V, p_ref, v_ref, gamma)` — $P(V)$
  curves, **gamma is an input parameter**, derivation deferred to 06; `work_on_gas(V, P)` —
  $-\int P\,dV$ by trapezoid over sampled points; `work_by_system` — its negation, defined via
  `work_on_gas` so signs can never drift; `work_along(P_of_V, v0, v1, n_points)` — the
  convergence refinement knob; `isothermal_/adiabatic_/isobaric_work_on_gas` — closed forms;
  frozen `Path(volumes, pressures, label)` with `start`/`end`/`is_closed`, `work_on_gas()`,
  `internal_energy_change(f=3)` — endpoint-only $\tfrac{f}{2}(P_1 V_1 - P_0 V_0)$,
  `heat_into_gas(f=3)` — $Q = \Delta U - \Won$; constructors `isothermal_/adiabatic_/
  isobaric_/isochoric_path`; `join(*paths)` — concatenation with junction checks (07's cycles).
- **`tests/physics` (as built):** *dimensional* — `test_dimensions.py` types for pressure and
  work; *analytic-limit* — `test_limits.py` closed forms for all three processes, isochoric
  zero work, path dependence > 25%, endpoint-equal $\Delta U$, first-law closure on every
  path, 04/05 ideal-gas consistency, `forms` inexact-route + mixed-partials tests;
  *conservation* — `test_conservation.py` exact form is endpoint-only, zero around a loop;
  *convergence* — `test_convergence.py` second-order quadrature (isothermal, adiabatic,
  `line_integral`), isobaric exact at coarsest sampling; *large-N / seed-independence* — not
  applicable: `paths.py`/`forms.py` are deterministic, no RNG, no particle ensembles.

## 5. Assessment hooks

- **Checkpoint core:** P1 (three routes, one destination) + P2 (cycle); P6 bridges lab to
  graded work (fractional spread, fitted convergence order).
- **Cross-module:** the 45% two-route number recurs in 06's ledger; the rectangular cycle and
  `work_by_system` are 07's engine-constructor raw material; P3(d) and P5 (integrating factor)
  are 08's entry ramp; Q-05-8's prediction style recurs in the 06/07 banks.
- **Exam themes:** sign-convention discipline (Q-05-6 tolerates no mixing), the sudden piston
  / $P_{ext}$ distinction, the cross-derivative exactness test.

## 6. Build order and validation gates

Built (third thermodynamics module live; 02/03 slot before it in the `myst.yml` TOC at their
build time). `glossary/terms.yml` already carries the module vocabulary (work, state-function,
path-function, adiabatic, isothermal, quasistatic, reversible, irreversible,
exact-/inexact-differential, first-law); `assessment/misconceptions.yml` has all four ids
`assigned_module: 05-work-paths`, `status: addressed`. **HE mirror complete — verified:**
`content/he/thermodynamics/05-work-paths{,-problems}.md` with `en_source_hash` stamps,
`notebooks/he/labs/05-work-paths.ipynb`, `assessment/quizzes/05-work-paths.he.yml`, HE quiz
JSON; 05 is absent from `translation-pending.txt` (only 01 and index remain). Gates: the
README per-module command block with `--module 05-work-paths`.

## 7. Deviations from the brainstorm

- **C1 re-scope:** brainstorm §3 row 5 assigns "heat capacities" to module 5; deferred to 06,
  which derives $C_V$/$C_P$/Mayer/$\gamma$ and the adiabat — 05's story is path dependence,
  and capacities need 06's per-process ledger to mean anything. 05 takes $\gamma$ as an input.
- **Row 6 overlap absorbed:** "compare paths with identical endpoints" (row 6's centrepiece)
  is already done here — lab Parts 1–4 and verify check 3; 06 re-centres on the polytropic
  slider and the full W/Q/ΔU/ΔT ledger per the README map.
- **§5 editor simplified:** free-form curve drawing became preset constructors plus a
  two-control-point slider editor — an ipywidgets/Pyodide practicality (gap 3 tracks upgrade).
- **Sign convention:** brainstorm §5 writes $W = \int P\,dV$; the built module computes
  $\Won = -\int P\,dV$ per invariant 1 — `work_by_system` quarantines the other sign.
- **§10 prototype B extras:** no instructor notebook or formal pre/post concept questions;
  the predict/explain sections partially cover the latter.
