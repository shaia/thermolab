---
title: "Equations of state: from the ideal gas to a real one"
short_title: 02 · Equations of state
module: 02-equations-of-state
objectives:
  - id: OBJ-02-1
    text: State the state postulate for a simple compressible substance -- fixing two independent intensive variables fixes every other equilibrium property -- and explain why all equilibrium states therefore form a single surface in (P, v, T) space.
  - id: OBJ-02-2
    text: Classify a thermodynamic variable as intensive or extensive by the doubling test, form per-particle densities such as v = V/N, and predict which quantities change when two identical systems are joined.
  - id: OBJ-02-3
    text: Use the ideal gas law P V = N k_B T to compute any one of P, V, T, N from the others, and state its epistemic status -- an empirical law of the dilute classical regime, not a law of nature.
  - id: OBJ-02-4
    text: Explain the physical origin of the van der Waals constants a (mutual attraction lowers pressure by a/v^2) and b (excluded volume shifts v to v - b), and compute pressures from P = k_B T/(v - b) - a/v^2.
  - id: OBJ-02-5
    text: Derive the critical point (v_c, T_c, P_c) = (3b, 8a/(27 k_B b), a/(27 b^2)) from dP/dv = 0 and d^2P/dv^2 = 0 on the critical isotherm, and interpret why no pressure liquefies a gas above T_c.
  - id: OBJ-02-6
    text: Rewrite the vdW equation in reduced variables P_r = P/P_c, v_r = v/v_c, T_r = T/T_c to obtain the parameter-free law of corresponding states, and use the compressibility factor Z = P v/(k_B T) to quantify a real gas's distance from ideality.
---

# Equations of state: from the ideal gas to a real one

(02-equations-of-state-puzzle)=
## The puzzle: a lighter that sloshes, a cylinder that never does

Shake a butane lighter and you can hear it: liquid fuel, sloshing inside a transparent
plastic shell, at room temperature, held there by nothing more exotic than the pressure of
its own vapour. Beside it, a steel cylinder of compressed nitrogen sits on a workbench. Squeeze
its regulator as hard as engineering allows and nothing sloshes — nitrogen at room temperature
never liquefies, no matter how hard you compress it.

Both are just gases confined under pressure. Both, at low enough density, obey the same law:

$$
PV = Nk_BT .
$$

That law has no substance-specific constant in it anywhere — no molecular size, no
attraction, nothing that could possibly distinguish butane from nitrogen. A law blind to what
the molecules *are* cannot explain why one of them puddles at room temperature and the other
flatly refuses to.

:::{important} The question
Why does one substance's equilibrium surface fold at room temperature — allowing liquid and
vapour to coexist — while another's cannot, however hard you compress it? And what is the
ideal gas law missing that makes it blind to the difference?
:::

The answer is not exotic. Real molecules attract each other weakly at a distance, and they
are not points — they take up room. Putting both effects back into the equation of state,
carefully, is this module's entire content.

(02-equations-of-state-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* running anything. Write them down.

1. You have a gas bottle at $(N, V, T)$. You bring an identical second bottle and open the
   valve between them, so the two merge into one system at the same $T$ — twice the gas, in
   twice the volume. Which of $P$, $V$, $T$, $N$, $U$ change, and which stay the same?
2. $\mathrm{CO_2}$ at $280\ \mathrm{K}$ is compressed slowly at fixed temperature. As the
   volume shrinks, does the pressure keep climbing, level off at some point, or do something
   else? Sketch the curve you expect.
3. Is there a temperature above which *no* pressure, however large, can turn a gas into a
   liquid?
4. Two different gases — say $\mathrm{CO_2}$ and $\mathrm{N_2}$ — are each held at the same
   *reduced* temperature and reduced pressure (that is, the same multiple of their own
   critical temperature and critical pressure, even though those critical points are wildly
   different numbers). Do the two gases have the same compressibility factor $Z$, or does $Z$
   depend on which gas it is?

:::{note} Why we ask first
Question 1 is the doubling test this module makes precise: some quantities double, some do
not, and mixing them up is one of the most common errors in the subject. Question 4 previews
the module's real payoff: the ideal gas law is *not* a universal law every gas obeys, but once
pressure, volume and temperature are measured in units of a substance's own critical point, a
genuinely universal law re-emerges — just not the one you might have guessed.
:::

(02-equations-of-state-explore)=
## Explore the model

The laboratory notebook for this module lets you build a substance's van der Waals surface
from its constants $a$ and $b$, morph it continuously from the flat ideal-gas sheet, drag a
state point across it, and watch the three shadows that point casts onto the surrounding
walls.

Here is the surface itself, rotating, as $a$ and $b$ turn on from zero and a fold appears
where a flat sheet used to be:

:::{figure} ../media/gases-surface.mp4
:alt: A rotating three-dimensional pressure-volume-temperature surface that starts perfectly flat, like an ideal gas, and grows a fold as van der Waals constants are turned on, revealing a region where the surface is no longer single-valued in pressure for a given volume and temperature.
:width: 100%

The van der Waals $(P, v, T)$ surface, morphing on from the flat ideal-gas sheet as $a$ and
$b$ are turned up to a real substance's values. The fold that appears below the critical
temperature is the geometric signature of liquefaction — nothing in the flat ideal surface
could ever produce it.
:::

Now watch a single isotherm sweep down through the critical temperature:

:::{figure} ../media/gases-isotherms.mp4
:alt: A single pressure-volume isotherm curve that is smooth and monotonic at high temperature, flattens at a marked critical point, and develops a non-monotonic wiggle at temperatures below the critical temperature.
:width: 100%

One van der Waals isotherm, replotted as its temperature sweeps from above the critical
temperature to below it. Above $T_c$ the curve falls smoothly, just like an ideal gas. Below
$T_c$ it develops a non-monotonic wiggle — the van der Waals loop — flagged here and left
unexplained; see [Verify](#02-equations-of-state-verify).
:::

And here is a single state point sliding across the surface, its three shadows tracing an
isotherm, an isochore, and an isobar onto the three walls around it:

:::{figure} ../media/gases-shadows.mp4
:alt: A state point moving along a three-leg path on a pressure-volume-temperature surface, with its projection onto each of the three surrounding walls tracing out, in turn, an isotherm on the pressure-volume wall, an isochore on the pressure-temperature wall, and an isobar on the volume-temperature floor.
:width: 100%

A state point moves in three legs — constant $T$, then constant $v$, then constant $P$ — and
its shadow on each wall traces the corresponding named curve: an isotherm, an isochore, an
isobar. Every point on the surface is simultaneously all three kinds of curve, depending on
which pair of coordinates you hold fixed.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a fixed amount $N$ of a simple compressible substance, described entirely by
  the macroscopic coordinates $(P, v, T)$, with $v = V/N$ the volume per particle; the ideal
  gas is the special case $a = b = 0$.
- **Dynamics:** none — every rendered point is an equilibrium state; nothing evolves.
- **Boundary:** closed; $N$ is fixed, $v$ and $T$ are set externally, and $P$ is read off the
  equation of state.
- **Ensemble:** not applicable — this is macroscopic thermodynamics, not a sampled microstate.
- **Ignored:** everything microscopic ($a$ and $b$ enter as fitted constants, not
  derivations); how the system moves between states; the two-phase interior of the fold (the
  surface is drawn from the bare van der Waals equation).
- **Valid when:** the dilute classical regime (the ideal sheet); moderate densities near and
  above $T_c$ (the van der Waals sheet).
- **Failure modes:** the sub-critical region where the bare van der Waals isotherm gives
  $(\partial P/\partial v)_T > 0$ — no real substance equilibrates there, and a Maxwell
  construction is needed to repair it, which module 14 supplies; the cryogenic and
  quantum-degenerate regimes module 17 covers.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 02 — equations of state](/lite/lab/index.html?path=en/labs/02-equations-of-state.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/02-equations-of-state.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Set $a = b = 0$ and confirm the surface is perfectly flat — the ideal gas, with no fold
  anywhere, whatever temperature you look at.
- Turn on a substance's $a$ and $b$ and watch the fold appear below its critical temperature.
- Join two identical samples in the doubling-test cell and check which quantities the printed
  table says changed.

(02-equations-of-state-derive)=
## Derive the result

### The state postulate

:::{admonition} The state postulate
:class: empirical-law
For a simple compressible substance — a fixed amount of a single-component fluid, with no
electric, magnetic or surface effects — fixing any **two independent intensive variables**
fixes every other equilibrium property. Equivalently: every equilibrium state of such a
substance lies on a single two-dimensional surface in $(P, v, T)$ space, and an *equation of
state* is nothing but the equation of that surface.

This is a claim about the world, not a theorem derivable from the zeroth or first law alone —
it is an empirical generalisation, exactly like the zeroth law's claim that thermal
equilibrium is transitive ([module 1](01-equilibrium.md)). Nothing here is proven from more
basic principles; it is proposed, and every equation of state this module writes down is a
test of it.
:::

### Intensive versus extensive: the doubling test

:::{admonition} Intensive and extensive, by the doubling test
:class: definition
Join two identical copies of a system — same substance, same state — into one. A variable is
**extensive** if the joined value is *double* the original: $V$, $N$, and the internal energy
$U$ are extensive. A variable is **intensive** if the joined value is *unchanged*: $T$ and $P$
are intensive — they describe a local property of the substance, not how much of it there is.

Per-particle quantities such as $v \equiv V/N$ are intensive by construction: both numerator
and denominator double, so their ratio does not move. This is exactly why the state
postulate is phrased in terms of $v$ rather than $V$ — $v$, unlike $V$, is a property of the
*substance* at a given $(P, T)$, not of a particular sample of it.
:::

Pressure had better be intensive for "the pressure of the gas" to mean anything: two adjacent
litres of the same gas at the same temperature must report the same pressure, or a single
gauge reading would be meaningless. The laboratory verifies this by direct computation for
every equation of state below; the doubling test above is the reason it must come out that
way.

### The ideal gas law, reviewed

:::{admonition} The ideal gas law
:class: empirical-law
$$
PV = Nk_BT, \qquad\text{equivalently}\qquad Pv = k_BT \ \text{with}\ v = V/N.
$$

Derived in [module 4](04-pressure.md) from point particles that never interact, and
equivalently obtainable as the simplest equation of state consistent with the state postulate
plus the empirical observation that dilute gases share one equation of state
([module 1](01-equilibrium.md)). It has no substance-specific constant anywhere in it — which
is exactly its epistemic status: an empirical law of the *dilute classical regime*, exact only
as density falls to zero, and not a law every gas obeys at every density. Treating it as
universal is the `ideal-gas-universal` misconception this module's [Verify](#02-equations-of-state-verify)
section falsifies directly.
:::

### Two corrections, and the van der Waals equation

**Excluded volume.** A real molecule is not a point; it excludes other molecules from the
small region $b$ it occupies. Replacing the per-particle volume $v$ available to move around
in with the reduced volume $v - b$:

$$
P = \frac{k_BT}{v - b}.
$$

Because the denominator is *smaller* than $v$, this correction alone always *raises* the
pressure above the ideal value: molecules crowded into less usable room collide with the
walls more often.

:::{admonition} Attraction lowers the pressure
:class: model-assumption
A molecule deep inside the gas is pulled equally in every direction by its neighbours and
feels no net force. A molecule about to strike the wall has neighbours behind it and none
beyond the wall, so the net attraction pulls it *backwards*, slightly reducing the momentum
it delivers. [Module 4's advanced section](04-pressure.md#04-pressure-advanced) derives this
exactly as a virial correction; for a short-ranged attraction summed over every pair, the
mean-field estimate is that the pressure is lowered by $a/v^2$ — proportional to the square
of the density, because it takes *two* molecules, one to attract and one to be attracted, for
the effect to occur at all.
:::

Adding both corrections to the ideal gas law gives the **van der Waals equation of state**:

$$
\boxed{\; P = \frac{k_BT}{v - b} - \frac{a}{v^2} \;}
$$

Setting $a = b = 0$ recovers the ideal gas law exactly — not approximately, as
[Verify](#02-equations-of-state-verify) checks directly against `gases.ideal_gas_pressure`.
Neither correction is *derived* from first principles here; each is argued physically and
then simply added, which is exactly why the box above is a `model-assumption`, not a
`theorem`: the van der Waals equation is a plausible model, not a consequence of the state
postulate the way the ideal gas law can be read as one.

:::{admonition} A note on units: per particle, not per mole
:class: definition
Textbooks usually quote $a$ and $b$ per *mole*, with $n$ moles in place of $N$ particles and
$R$ in place of $k_B$: $(P + a_{\text{molar}}n^2/V^2)(V - n b_{\text{molar}}) = nRT$. This
course keeps $N$ a plain particle count everywhere and works in the per-particle volume
$v = V/N$, so `thermolab.gases` takes $a$, $b$ **per particle**:
$a = a_{\text{molar}}/N_A^2$ and $b = b_{\text{molar}}/N_A$. Both keep the same physical units
as their molar counterparts — only the numeric value shrinks enormously, since
$N_A \approx 6\times10^{23}$.
:::

### The critical point

Look again at the isotherm animation above. Above $T_c$, pressure falls monotonically as $v$
grows — one $v$ for every $P$, exactly as for an ideal gas. Below $T_c$, the curve is no
longer monotonic: it rises where it should fall. The boundary between the two behaviours is a
single special point, where the isotherm's slope and its curvature both vanish at once:

$$
\left(\frac{\partial P}{\partial v}\right)_T = 0, \qquad
\left(\frac{\partial^2 P}{\partial v^2}\right)_T = 0.
$$

Because $P$ depends on $v$ and $T$ alone — no explicit $N$, since $P$ is intensive — solving
these two equations together (a standard but slightly tedious piece of algebra, omitted here)
gives:

:::{admonition} The critical point
:class: theorem
$$
\boxed{\; v_c = 3b, \qquad k_BT_c = \frac{8a}{27b}, \qquad P_c = \frac{a}{27b^2} \;}
$$

All three are properties of the *substance* alone — intensive, with no particle count
anywhere in them, exactly as the state-postulate framing of this module promises. Below
$T_c$, a real substance can coexist as liquid and vapour simultaneously; as $T \to T_c$ the
two phases' densities converge, and at $T_c$ they become identical. Above $T_c$ there is no
distinction between "gas" and "liquid" at all — only a single **supercritical fluid** — which
is precisely why no pressure, however large, liquefies nitrogen at room temperature: room
temperature is far above nitrogen's $T_c = 126\ \mathrm{K}$, while it is comfortably below
butane's $T_c \approx 425\ \mathrm{K}$.
:::

### Reduced variables and the compressibility factor

Define **reduced** variables $P_r = P/P_c$, $v_r = v/v_c$, $T_r = T/T_c$ — pressure,
per-particle volume and temperature measured in units of the substance's own critical point.
Substituting the closed forms above into the van der Waals equation and simplifying eliminates
$a$, $b$ and every substance-specific number entirely:

:::{admonition} The law of corresponding states
:class: theorem
$$
\boxed{\; P_r = \frac{8T_r}{3v_r - 1} - \frac{3}{v_r^2} \;}
$$

Every van der Waals substance obeys this *same* equation, with no adjustable constants left
at all — this is the resolution [Predict](#02-equations-of-state-predict) question 4 was
pointing toward: the ideal gas law is not a universal law, but once $P$, $v$, $T$ are measured
relative to a substance's own critical point, a genuinely parameter-free law re-emerges.

A direct consequence is the **compressibility factor** $Z \equiv Pv/(k_BT)$, which is exactly
$1$ for an ideal gas and measures a real gas's distance from it. Evaluated at the critical
point itself,

$$
Z_c \equiv \frac{P_cv_c}{k_BT_c} = \frac{3}{8},
$$

a single dimensionless number every van der Waals substance shares — and a falsifiable
prediction, checked against real gases in [Verify](#02-equations-of-state-verify).
:::

(02-equations-of-state-verify)=
## Verify computationally

Deriving a formula and trusting it are different things. The laboratory checks the result
several ways, and each check is also a test in the project's test suite, so the claims on
this page cannot silently rot.

**1. The ideal-gas limit.** As $a, b \to 0$, `gases.van_der_waals_pressure` converges on
`gases.ideal_gas_pressure` — the same function [module 4](04-pressure.md) and
[module 5](05-work-paths.md) already rely on (`kinetics.py` and `paths.py` import it from
`gases.py` rather than each carrying their own copy).

**2. The critical point: closed form versus a numerical scan.** `vdw_critical_point` gives
$(v_c, T_c, P_c)$ from three lines of algebra. The laboratory also *measures* $T_c$ a second,
independent way — the kind of procedure an experimentalist without a closed form would actually
run. Note what that procedure cannot be: below $T_c$ the isotherm's loop makes
$\partial P/\partial v$ cross zero at two perfectly ordinary points, so simply hunting for the
smallest slope anywhere on a grid finds a sub-critical isotherm just as happily as the critical
one. The laboratory instead sweeps *down* through the supercritical branch, where the isotherm
stays monotonic and its flattest point shrinks continuously toward zero as $T \to T_c^+$, and
stops at the first temperature that flattens below a small threshold.

:::{admonition} A measurement needs an uncertainty attached
:class: numerical-observation
A flatness scan over a finite grid of temperatures and volumes cannot land exactly on $T_c$ —
only within half a grid spacing of it. The laboratory reports the scan's result as
$T_c = (\text{value}) \pm (\text{uncertainty})$, not as a bare number.

That error bar has two sources, and only one of them is the grid. Half a grid spacing covers
the *discretisation*; the flatness threshold contributes a separate **bias**, because a scan
stops as soon as the slope falls below the threshold rather than when it truly vanishes. Refine
the temperature grid alone and the quoted uncertainty shrinks while that bias does not — the
measurement drifts from agreeing with the closed form to disagreeing with it by many times its
own stated error, which is the signature of an error bar that has stopped being honest. The
threshold has to be tightened *in step with* the grid for the scan to converge. An uncertainty
that accounts for only the source you happened to think of is worth little more than no
uncertainty at all.
:::

**3. Z approaches 1 in the dilute limit.** As $v \to \infty$ at fixed $T$, both correction
terms in the van der Waals equation vanish and $Z \to 1$ — the formal statement of "ideal gas"
as a limit rather than a category.

**4. The NIST CO2 isotherm falsifies "the ideal gas law is universal".** `data/co2-isotherm-280k.csv`
holds representative published values for carbon dioxide's isothermal pressure-volume
behaviour at $280\ \mathrm{K}$ — comfortably below $\mathrm{CO_2}$'s critical temperature of
$304.13\ \mathrm{K}$. Computing $Z = Pv/(k_BT)$ along that isotherm and overlaying the ideal
prediction $Z = 1$ shows the two diverging sharply as the gas is compressed: the measured
pressure *plateaus* at the substance's saturation pressure while a naive $P = k_BT/v$
prediction keeps climbing without limit, and $Z$ falls to a small fraction of $1$ deep in the
two-phase region.

:::{admonition} The ideal gas law is not a law every gas obeys
:class: numerical-observation
This is the direct falsifier for `ideal-gas-universal`: real $\mathrm{CO_2}$ at $280\
\mathrm{K}$ does not track $P = k_BT/v$ once it is compressed past a few times its critical
volume — it flattens into a condensation plateau the ideal law has no way to predict, because
the ideal law contains no substance-specific information at all. The van der Waals prediction
tracks the *shape* of the departure — falling below ideal, then failing near the plateau in
its own way (see the open question below) — considerably better than the ideal law does, but
neither model reproduces the flat plateau itself.
:::

:::{admonition} What the wiggle means is left open
:class: open-question
Below $T_c$, the bare van der Waals equation does not plateau the way real $\mathrm{CO_2}$
does — it develops the non-monotonic loop the isotherm animation shows, with a region where
$(\partial P/\partial v)_T > 0$. That region cannot describe any stable equilibrium state, and
this module deliberately does not explain what replaces it or how the flat, physically correct
plateau is actually located. Module 14 resolves this with the Maxwell construction, reusing
the exact isotherms `gases.py` computes here. For now: the loop is a
real, checkable feature of the bare equation, and *why* it is unphysical, and what to do about
it, are questions this module raises without answering.
:::

(02-equations-of-state-transfer)=
## Transfer the idea

- **Back to module 4.** The empirical box above gets its microscopic derivation there — this
  module states $PV = Nk_BT$; that one *derives* it from particles bouncing off walls.
- **Forward to module 6.** Every process this course studies from here on is a curve drawn on
  the surface this module builds; module 6's work ledger integrates $P\,dv$ along such curves.
- **Forward to module 9.** $V$, $N$ and $U$ all doubling together under the doubling test is
  exactly the extensivity the fundamental relation's Euler relation depends on.
- **Forward to module 14, named and dated.** The wiggle above is real, checkable, and
  unexplained — module 14 names it, resolves it with the Maxwell construction, and reuses
  these exact isotherms to do it.
- **Forward to module 17.** Even the "ideal" sheet fails eventually — in the cryogenic,
  quantum-degenerate regime, where $Z \to 1$ stops being the right limit.

(02-equations-of-state-quiz)=
## Check your understanding

```{include} ../_generated/quiz-02-equations-of-state.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](02-equations-of-state-problems.md).

(02-equations-of-state-explain)=
## Explain it in your own words

Answer in a few sentences each. These are the questions that reveal whether the ideas landed;
no number will save you.

1. Explain why calling the ideal gas law a "law" can mislead a reader, and say precisely what
   kind of statement it actually is.
2. Explain, without writing an equation, why no pressure — however large — liquefies a gas
   above its critical temperature.
3. Explain why $v = V/N$ is intensive although $V$ and $N$ are each extensive.
4. Describe what would be physically wrong with a substance whose isotherm had
   $(\partial P/\partial v)_T > 0$ somewhere.

(02-equations-of-state-advanced)=
## Advanced: the virial expansion

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in modules 4, 6, 9, 14 or 17's core content depends on this section; module 14
re-derives what it needs directly from the van der Waals equation.
:::

The van der Waals equation is one particular, simple model of "real gases differ from ideal
ones." The systematic version of the same idea writes the compressibility factor as a power
series in the density $1/v$:

$$
Z = 1 + \frac{B(T)}{v} + \frac{C(T)}{v^2} + \cdots,
$$

the **virial expansion**, whose coefficients can in principle be computed exactly from the
intermolecular potential, order by order, rather than guessed at with two constants. Expanding
the boxed van der Waals equation in powers of $1/v$ gives its own second virial coefficient in
closed form:

$$
B(T) = b - \frac{a}{k_BT} .
$$

At low $T$, $B(T) < 0$ — attraction dominates and $Z < 1$; at high $T$, $B(T) > 0$ — excluded
volume dominates and $Z > 1$. The crossover defines the **Boyle temperature**,

$$
T_B = \frac{a}{k_Bb},
$$

the one temperature at which a van der Waals gas behaves ideally ($Z = 1$) over the widest
possible range of density, because the two corrections cancel to leading order in $1/v$ at
every density simultaneously. Real gases have Boyle temperatures too, and the virial
expansion — unlike the two-constant van der Waals model — can in principle be pushed to as
many terms as the data justify.
