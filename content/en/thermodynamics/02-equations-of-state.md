---
title: "Equations of state: from the ideal gas to a real one"
short_title: 02 · Equations of state
module: 02-equations-of-state
objectives:
  - id: OBJ-02-1
    text: State the ideal gas law P V = N k_B T as reviewed from earlier modules, and name the two physical effects it necessarily leaves out.
  - id: OBJ-02-2
    text: Derive the N-particle van der Waals equation of state by adding a mean-field attraction correction and an excluded-volume correction to the ideal gas law, and explain what each correction represents physically.
  - id: OBJ-02-3
    text: Distinguish intensive from extensive state variables, and demonstrate that pressure is invariant under simultaneous scaling of N and V at fixed T.
  - id: OBJ-02-4
    text: Compute the critical point (T_c, P_c, V_c) of a van der Waals gas from its a and b constants, and explain what happens physically at that point.
  - id: OBJ-02-5
    text: Interpret a P-V-T surface, including the unphysical van der Waals loop below the critical temperature, and state where the mean-field model breaks down.
---

# Equations of state: from the ideal gas to a real one

(02-equations-of-state-puzzle)=
## The puzzle: a law that cannot see what the gas is made of

We derived $PV = Nk_BT$ in [module 4](04-pressure.md): particles bounce elastically off the
walls, the mass cancels out of the result, and what is left depends on nothing about the gas
except how many particles it has and how energetic they are. The same law, with the same
coefficient, for helium, for argon, for any dilute gas at all — the ideal gas law is famously
indifferent to what the molecules actually *are*.

Real gases are not indifferent to their own identity. Cool helium and it stays a gas down to
about $4\ \mathrm{K}$; cool argon and it condenses into a liquid at $87\ \mathrm{K}$; cool
water vapour and it condenses far higher, near $373\ \mathrm{K}$. A law with no way to tell
one substance from another cannot possibly predict when — or whether — that substance turns
into a liquid, and real gases also show measurably different pressures from the ideal-gas
prediction at the same $N$, $V$, $T$, long before condensation is anywhere in sight.

:::{important} The question
What is missing from $PV = Nk_BT$ that lets real gases differ from one another and eventually
condense — and can it be added back in without abandoning the reasoning that got us to the
ideal gas law in the first place?
:::

The two things missing are not exotic. Real molecules attract each other weakly at a
distance, and they are not points — they take up room. Putting both back in, carefully, is
this module's entire content.

(02-equations-of-state-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* running anything. Write them down.

1. Real molecules attract each other. Does that attraction make the pressure of a real gas
   higher or lower than $Nk_BT/V$, at the same $N$, $V$, $T$?
2. Real molecules have a nonzero size, so a container cannot be packed with an arbitrarily
   large number of them. Does that make the pressure higher or lower than ideal, at high
   density?
3. You double both $N$ and $V$ of a gas at fixed $T$ — the same substance, twice the sample.
   Does the pressure change?
4. A real gas is cooled at fixed volume, well below room temperature. Sketch what you expect
   its $P$–$V$ isotherms to look like as $T$ drops: do they stay simple monotonic curves, or
   can something qualitatively different happen at low enough $T$?

:::{note} Why we ask first
Questions 1 and 2 pull in opposite directions, and a real gas shows both effects at once —
which one dominates depends on the density. Question 4 is where this module is heading:
something genuinely new happens to the *shape* of an isotherm once a real gas is cooled far
enough, and it is the reason liquids exist at all.
:::

(02-equations-of-state-explore)=
## Explore the model

The laboratory notebook for this module lets you set $N$, the van der Waals constants $a$
and $b$ of a chosen substance, and a range of temperatures and volumes, then watch the
resulting P-V-T surface — and how it differs from the flat ideal-gas surface — bend as the
temperature drops toward the substance's critical point.

Here is the phenomenon in one picture: the same $(N, V, T)$ grid, evaluated once for the
ideal gas and once for a van der Waals gas with argon's constants, shown as two surfaces over
the same axes.

:::{figure} ../media/pvt-surface-ideal-vs-vdw.mp4
:alt: A rotating three-dimensional plot comparing the flat ideal-gas pressure surface (a pale wireframe) with the curved, coloured van der Waals surface for argon over the same range of volume and temperature.
:width: 100%

The van der Waals pressure surface for argon (coloured) against the ideal-gas surface over
the same $(V,T)$ grid (pale wireframe). The two agree closely at large volume — low
density — and pull apart as the volume shrinks toward the excluded volume $Nb$, exactly
where the ideal gas law is least trustworthy.
:::

Now watch a single isotherm — one fixed temperature, pressure plotted against volume — as
the temperature sweeps down through argon's critical temperature $T_c$:

:::{figure} ../media/pvt-isotherms-near-critical.mp4
:alt: A single P-V isotherm curve that is smooth and monotonic at high temperature, flattens at a marked critical point, and develops a non-monotonic wiggle at temperatures below the critical temperature.
:width: 100%

One van der Waals isotherm, replotted as its temperature sweeps from well above argon's
critical temperature to well below it. Above $T_c$ the curve falls smoothly, just like an
ideal gas. Below $T_c$ it develops a non-monotonic wiggle — the van der Waals loop — which is
the model's signature of a phase transition it cannot correctly resolve on its own.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** $N$ structureless molecules of a real gas, described in the van der Waals
  mean-field approximation; the ideal gas is the special case $a = b = 0$.
- **Dynamics:** none — this is a static equation of state relating equilibrium values of $P$,
  $V$, $T$ and $N$, not a trajectory to integrate.
- **Boundary:** a rigid container of volume $V$ at temperature $T$, or a piston varying $V$
  quasistatically along an isotherm.
- **Ensemble:** implicit thermodynamic equilibrium — $P(N,V,T)$ is an equilibrium equation of
  state; no microstate is sampled.
- **Ignored:** higher-order (beyond pairwise mean-field) interactions, quantum effects,
  internal molecular structure, mixtures of species, and any density dependence of $a$ and
  $b$ themselves.
- **Valid when:** the gas is dilute to moderately dense and classical, so that the mutual
  attraction and the molecules' own volume are both small, additive corrections to the
  ideal-gas pressure, away from the critical point.
- **Failure modes:** very high density, where a single mean-field pairwise correction can no
  longer capture the real interactions; at or below the critical temperature, where the
  equation's van der Waals loop is unphysical and a Maxwell construction (not derived here)
  is needed instead.
:::

:::{admonition} What this model cannot do
:class: model-assumption
The van der Waals equation replaces the true, fluctuating interactions between individual
molecule pairs with a single smoothed-out, average correction — a *mean-field*
approximation. It can show you *that* a loop appears in the isotherm below $T_c$, which is
the qualitative signature of a liquid-gas transition, but the loop itself is unphysical: real
matter never follows it. The actual constant-pressure path between liquid and gas is found
by the Maxwell equal-area construction, which replaces the loop rather than explaining it
away, and is left for the advanced section.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 02 — equations of state](/lite/lab/index.html?path=en/labs/02-equations-of-state.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/02-equations-of-state.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Set $a = b = 0$ and confirm the surface is perfectly flat in the sense that
  $P \propto T/V$ everywhere — the ideal gas, with nothing to distinguish one substance from
  another.
- Turn on argon's $a$ and $b$ and watch how much the surface bends near small volume, where
  the excluded-volume correction dominates.
- Sweep the temperature slider down through $T_c$ and watch the isotherm develop its loop.
  Note the volume at which the loop first appears — it is $V_c$.

(02-equations-of-state-derive)=
## Derive the result

**System and boundary.** $N$ molecules of a real gas in a container of volume $V$ at
temperature $T$. **Independent variables.** $N$, $V$, $T$, and two substance-specific
constants $a$, $b$ that we are about to introduce.

### Two corrections to the ideal gas law

:::{admonition} The ideal gas law, reviewed
:class: empirical-law
$$
PV = Nk_BT
$$

derived in [module 4](04-pressure.md) from point particles that never interact, and
equivalently obtainable from the zeroth and first laws plus the empirical observation that
dilute gases share one equation of state ([module 1](01-equilibrium.md)). It is exact only in
the limit of zero density, where molecules almost never come close enough to feel each other
or to notice each other's size.
:::

**Excluded volume.** A real molecule is not a point; it excludes other molecules from the
small region it occupies. If each molecule effectively reserves a volume $b$ for itself, the
volume actually available for the gas to move around in is not $V$ but $V - Nb$. Substituting
this reduced volume into the ideal gas law in place of $V$:

$$
P = \frac{Nk_BT}{V - Nb}.
$$

Because the denominator is *smaller* than $V$, this correction alone always *raises* the
pressure above the ideal value — molecules crowded into less usable room collide with the
walls more often.

:::{admonition} Attraction lowers the pressure
:class: model-assumption
A molecule deep inside the gas is pulled equally in every direction by its neighbours and
feels no net force. A molecule about to strike the wall has neighbours behind it and none
beyond the wall, so the net attraction pulls it *backwards*, slightly reducing the momentum
it delivers. [Module 4's advanced section](04-pressure.md#04-pressure-advanced) derives this
exactly as the virial correction $PV = Nk_BT + \frac{1}{d}\langle\sum_{i<j}
\mathbf{r}_{ij}\cdot\mathbf{F}_{ij}\rangle$; for a short-ranged attraction summed over every
pair, the mean-field estimate of that correction term is $-aN^2/V^2$, proportional to the
*square* of the density because it takes two molecules — one to attract, one to be
attracted — for the effect to occur at all.
:::

Adding both corrections to the ideal gas law gives the **van der Waals equation of state**:

$$
\boxed{\; P = \frac{Nk_BT}{V - Nb} - \frac{aN^2}{V^2} \;}
$$

equivalently written in the more familiar product form
$\left(P + \dfrac{aN^2}{V^2}\right)(V - Nb) = Nk_BT$. Setting $a = b = 0$ recovers the ideal
gas law exactly — not approximately, as the [Verify](#02-equations-of-state-verify) section
checks directly against `paths.ideal_gas_pressure`.

:::{admonition} A note on units: per particle, not per mole
:class: definition
Textbooks usually quote $a$ and $b$ per *mole*, with $n$ moles in place of $N$ particles and
$R$ in place of $k_B$. This course keeps $N$ a plain particle count everywhere, so `thermolab`
uses $a$, $b$ **per particle**: $a = a_{\text{molar}}/N_A^2$ and $b = b_{\text{molar}}/N_A$.
Both keep the same physical units as their molar counterparts — only the numeric value shrinks
enormously, since $N_A \approx 6\times10^{23}$. Mixing the two conventions is the single most
common arithmetic error this topic produces; the module's test suite pins the conversion
against argon's textbook values so it cannot silently drift.
:::

### Intensive versus extensive

:::{admonition} Intensive and extensive state variables
:class: definition
A state variable is **extensive** if it doubles when you double the size of the system at
fixed density — $V$, $N$, and the internal energy $U$ are extensive. A state variable is
**intensive** if it stays the same — $T$ and $P$ are intensive; they describe a *local*
property of the material, not how much of it there is.
:::

Pressure had better be intensive for "the pressure of the gas" to mean anything at all — two
adjacent litres of the same gas at the same temperature must report the same pressure, or a
single pressure gauge reading would be meaningless. Algebraically, replacing
$N \to \lambda N$ and $V \to \lambda V$ at fixed $T$ (the same substance, $\lambda$ times as
much of it) leaves every term in the boxed equation unchanged: $N/(V - Nb)$ and $N^2/V^2$ are
each ratios of something proportional to $\lambda$ (or $\lambda^2$) divided by something
proportional to $\lambda$ (or $\lambda^2$), so the $\lambda$'s cancel exactly. This holds for
the *real*-gas correction exactly as it does for the ideal gas, because $a$ and $b$ are
properties of the substance, not of the sample size — doubling how much argon you have does
not change what a single argon atom is like. The laboratory verifies this by direct
computation rather than proof by inspection; the algebra above is the proof.

### The critical point

Look again at the isotherm animation above. Above $T_c$, pressure falls monotonically as
volume grows — one volume for every pressure, exactly as for an ideal gas. Below $T_c$, the
curve is no longer monotonic: it rises where it should fall. The boundary between the two
behaviours is a single special point, found where the isotherm's slope and its curvature both
vanish at once:

$$
\left(\frac{\partial P}{\partial V}\right)_T = 0, \qquad
\left(\frac{\partial^2 P}{\partial V^2}\right)_T = 0.
$$

Writing the pressure per particle, with $x \equiv V/N$ the volume per molecule, makes
$P(x) = k_BT/(x - b) - a/x^2$ depend on $x$ alone — no explicit $N$ left in it, because we
just showed $P$ is intensive. Solving the two equations above for $x$ and $T$ together (a
standard but slightly tedious piece of algebra, omitted here) gives

$$
\boxed{\; V_c = 3Nb, \qquad k_BT_c = \frac{8a}{27b}, \qquad P_c = \frac{a}{27b^2} \;}
$$

$T_c$ and $P_c$ depend only on $a$ and $b$ — they are intensive, exactly as a property of a
*substance* (rather than of a particular sample) should be. $V_c$, by contrast, is
proportional to $N$: it is extensive, because it is the volume of a specific sample at its
critical point, and a bigger sample needs a bigger volume to reach it.

:::{admonition} What happens physically at the critical point
:class: definition
Below $T_c$, a real gas can coexist as liquid and vapour simultaneously, at a pressure that
depends only on $T$ — the flat part of a *true* isotherm that the van der Waals loop is a
smoothed-over approximation to. As $T$ rises toward $T_c$, the difference between the liquid
and vapour densities shrinks; at $T_c$ itself the two phases become identical, and above it
there is no distinction between "gas" and "liquid" at all — only a single **supercritical
fluid**. $(T_c, P_c, V_c)$ is the one point where this merger happens.
:::

:::{admonition} Where the van der Waals numbers are least trustworthy
:class: approximation
Fitting $a$ and $b$ to reproduce a real gas's measured $T_c$ and $P_c$ (as the laboratory
does for argon) reproduces those two numbers to within about a percent. It does *not*
reproduce $V_c$ nearly as well — the van der Waals equation predicts the same dimensionless
ratio $P_cV_c/(Nk_BT_c) = 3/8$ for every substance, while real gases scatter around
$0.27$–$0.29$. This is the clearest quantitative sign that mean-field theory is an
approximation, not an identity: it gets the *existence* and rough *location* of a critical
point right while getting its precise geometry wrong, exactly the failure mode the model
specification above names.
:::

(02-equations-of-state-verify)=
## Verify computationally

Deriving a formula and trusting it are different things. The laboratory checks the result
several ways, and each check is also a test in the project's test suite, so the claims on
this page cannot silently rot.

**1. The ideal-gas limit.** As $a, b \to 0$, `van_der_waals_pressure` converges on
`paths.ideal_gas_pressure` — the same function [module 4](04-pressure.md) and
[module 5](05-work-paths.md) already rely on, imported directly rather than re-derived a
third time.

**2. Real argon at ordinary density.** At $N = 5\times10^{22}$ particles in $2.0\ \mathrm{L}$
at $300\ \mathrm{K}$ — the same scenario as
[module 4's Problem 2](04-pressure-problems.md) — argon's measured $a$ and $b$ shift the
pressure away from the ideal value by about a tenth of a percent: small, but not zero, and in
the direction set by whichever correction dominates at this density.

**3. The critical point.** `critical_point` reproduces argon's measured $T_c$ and $P_c$ to
within about a percent from its $a$, $b$ alone, and the pressure formula evaluated exactly at
$(T_c, V_c)$ returns $P_c$ to machine precision — the closed-form relations and the pressure
formula they came from agree with each other exactly, not approximately.

**4. The critical point really is a stationary inflection.** A finite difference of the
pressure with respect to volume, evaluated at $V_c$, shrinks toward zero as the step size
shrinks — and shrinks at *second order*, the signature of a true vanishing derivative rather
than a numerical coincidence.

**5. Intensivity.** Pressure computed at $(N, V)$ and at $(\lambda N, \lambda V)$, same $T$,
agree to machine precision for every $\lambda$ tried, confirming the algebraic argument above
by direct computation.

:::{admonition} What the agreement does and does not establish
:class: open-question
Matching argon's $T_c$ and $P_c$ to a percent is evidence that the mean-field approximation
captures the right *physics* of a liquid-gas transition — an attraction that pulls molecules
together and a finite size that eventually pushes back. It is not evidence that the van der
Waals equation is quantitatively accurate everywhere; the $V_c$ mismatch above is the
built-in counter-example, and no amount of additional testing of *this* model can fix it,
because the discrepancy is a property of the model's mean-field assumption, not of any
particular calculation.
:::

(02-equations-of-state-transfer)=
## Transfer the idea

- **Gas liquefaction.** Industrial processes that liquefy air, natural gas, or helium work by
  cooling and compressing a real gas past the loop this module's second animation shows —
  the same physics, at an engineering scale.
- **Supercritical extraction.** Above $T_c$ and $P_c$, carbon dioxide is a single
  supercritical fluid — denser than a typical gas, more penetrating than a typical liquid —
  used to decaffeinate coffee and extract essential oils without the toxic solvents an
  ordinary liquid extraction would need.
- **The virial expansion.** The van der Waals equation is the simplest member of a more
  general family, $PV = Nk_BT\left(1 + \frac{B_2(T)N}{V} + \cdots\right)$, whose second virial
  coefficient $B_2(T)$ can be computed exactly from the intermolecular potential — a
  systematic refinement of the same mean-field idea, touched on again in module 12.
- **The law of corresponding states.** Measuring pressure, volume and temperature in units of
  $P_c$, $V_c$, $T_c$ collapses the van der Waals equation into one universal, substance-free
  form (the [Advanced section](#02-equations-of-state-advanced) derives it) — the reason a
  single reduced phase diagram, appropriately rescaled, describes argon and carbon dioxide
  about equally well despite wildly different $a$ and $b$.

:::{admonition} A word on "real gas"
:class: definition
This course uses **real gas** for any gas whose equation of state departs from
$PV = Nk_BT$ — not a technical classification, just a reminder that the ideal gas law is a
*limit*, approached as density falls, rather than a law every gas obeys everywhere.
:::

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

1. A student says: "Real gases deviate from the ideal gas law because real molecules take up
   space." Improve this sentence so that it is actually correct, and say precisely what it
   leaves out.
2. Explain, without writing an equation, why doubling both the amount of gas and the volume
   containing it — same substance, same temperature — leaves the pressure unchanged.
3. Two gases have the same $b$ but different $a$: gas A attracts more strongly than gas B.
   Which one has the higher critical temperature, and why does that follow from the physical
   meaning of $a$ rather than just from the formula?
4. The van der Waals loop below $T_c$ is described in this module as "unphysical." Explain
   what that word is doing there — what, precisely, does the model get wrong, and what does
   it still get right?

(02-equations-of-state-advanced)=
## Advanced: the law of corresponding states

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

Define **reduced** variables $P_r = P/P_c$, $V_r = V/V_c$, $T_r = T/T_c$ — pressure, volume
and temperature measured in units of the substance's own critical point. Substituting the
closed forms for $V_c$, $T_c$, $P_c$ from the derivation above into the van der Waals equation
and simplifying eliminates $a$, $b$ and $N$ entirely:

$$
\left(P_r + \frac{3}{V_r^2}\right)\left(V_r - \frac{1}{3}\right) = \frac{8}{3}T_r .
$$

Every van der Waals gas obeys this *same* equation, with no adjustable constants left at all.
Two different substances at the same reduced temperature and reduced pressure are said to be
in **corresponding states**, and — to the extent that the van der Waals approximation holds —
they share the same reduced volume, the same reduced vapour pressure curve, and even
approximately the same deviations from ideal-gas behaviour, despite having wildly different
$a$ and $b$.

:::{admonition} Why this is more than a curiosity
:class: numerical-observation
The law of corresponding states works better in practice than the van der Waals equation
itself does — real gases' reduced equations of state agree with each other, and with the
reduced van der Waals prediction, considerably more closely than their un-reduced pressures
agree with the un-reduced van der Waals formula. This is a general feature of mean-field
theories near a critical point, not a special property of this particular model, and it is
the historical starting point for the modern theory of critical phenomena and universality —
far beyond this course, but visible already in three lines of algebra.
:::

**The Maxwell construction, briefly.** Below $T_c$, the true isotherm replaces the
unphysical van der Waals loop with a horizontal segment at the substance's actual vapour
pressure, positioned so that the two areas the horizontal line cuts from the loop — one
where the loop's pressure exceeds the vapour pressure, one where it falls below — are
exactly equal. That equal-area condition follows from requiring the Gibbs free energy to be
single-valued along the isotherm, a piece of the fundamental relation this course reaches in
module 9. It is what turns the van der Waals equation from "predicts a phase transition
exists" into "predicts where it happens" — the gap between qualitative and quantitative that
mean-field theory leaves for later, more careful tools to close.
