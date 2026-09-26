---
title: Thermodynamic potentials
short_title: 10 · Potentials
module: 10-potentials
objectives:
  - id: OBJ-10-1
    text: Construct H = U + PV, F = U - TS and G = U - TS + PV as Legendre transforms of U(S,V,N) and write each differential (dH = T dS + V dP + mu dN; dF = -S dT - P dV + mu dN; dG = -S dT + V dP + mu dN).
  - id: OBJ-10-2
    text: Identify the natural variables of U, H, F and G and select the potential matched to a stated constraint — isolated -> S max; fixed T,V -> F min; fixed T,P -> G min; throttling -> H conserved.
  - id: OBJ-10-3
    text: Derive dF <= 0 at fixed T,V (and dG <= 0 at fixed T,P) from the second law applied to system plus reservoir, and account for what pays when U rises while F falls.
  - id: OBJ-10-4
    text: State the four Maxwell relations as equalities of mixed partials of U, H, F and G, and verify one numerically as a cross-derivative gap.
  - id: OBJ-10-5
    text: Use (dS/dV)_T = (dP/dT)_V to obtain an entropy change from pressure-gauge and thermometer data, Delta S = integral of (dP/dT)_V dV at fixed T.
  - id: OBJ-10-6
    text: Explain geometrically why the Legendre transform of a strictly convex (or concave) function preserves all information, via the envelope of its tangent lines.
  - id: OBJ-10-7
    text: Apply Delta H = Q_P to isobaric heating and throttling bookkeeping, and state precisely when Delta H = Q fails (work other than P dV present, or P not constant).
---

# Thermodynamic potentials

(10-potentials-puzzle)=
## The puzzle: three tables for one world

Open a chemistry handbook and the energy of every reaction is tabulated as a *Gibbs free
energy*. Open an engineer's steam tables and the column that matters is *enthalpy*. Open a
physics text on magnets or solids and the quantity being minimised is the *Helmholtz free
energy*. Three communities, three different functions, each of them called "the" energy of a
process — and all three are right.

Module 09 said that a single function, the entropy $S(U, V, N)$, contains everything
thermodynamics can say about a system. So the three tables cannot be telling three different
stories about the physics. Something else is different.

:::{important} The question
If one fundamental relation holds all the physics, why does every field tabulate a different
"energy" — and what, exactly, is each of them the right answer to?
:::

The answer has two halves. The first is about *what a laboratory holds fixed*: nobody can hold
a system's entropy constant, but a water bath holds its temperature and the atmosphere holds its
pressure. The second is a piece of mathematics, the Legendre transform, which trades a variable
for its slope without losing anything. Put together they produce three new complete functions,
one for each kind of laboratory. And they produce a bonus that is hard to believe until it has
been used: an entropy change, the least tangible quantity in the course, measured with a
pressure gauge and a thermometer.

(10-potentials-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* reading on. Write them down.

1. A gas sits in a rigid box that is in contact with a large heat bath. An internal constraint is
   released — a clamped piston inside the box is freed — and the gas settles into a new state.
   Must its energy have gone down?
2. Two cylinders of argon at room temperature hold exactly the same internal energy. Could one of
   them be able to do more work than the other?
3. Stretch a rubber band quickly and touch it to your lip. Does it feel warmer or cooler? Now
   hang a weight from it and warm it with a hair dryer: does it stretch further or contract?
4. Is the enthalpy change $\Delta H$ equal to the heat $Q$ for every process — or only under
   conditions, and if so, which?

:::{note} Why we ask first
Question 1 is where "systems minimise their energy", one of the most repeated half-truths in
science, meets a heat bath. Question 2 asks what "free energy" is free *for*. Question 3 can be
settled with a rubber band in the next thirty seconds, and the second half of it surprises almost
everyone. Question 4 is the enthalpy version of module 05's "heat stored in a body". Every answer
is collected at the end of the module.
:::

(10-potentials-explore)=
## Explore the model

The laboratory is built around three demonstrations, each an animation below and a live
experiment in the notebook.

The first is the mathematical heart of the module: a curve, and the family of its tangent lines.

:::{figure} ../media/potentials-tangent-envelope.mp4
:alt: Left, the convex curve of energy against entropy for an Einstein solid, with a tangent line sliding along it and its intercept on the vertical axis marked. Right, the intercept plotted against the tangent's slope, tracing a falling curve. Then the curve fades and many tangent lines are drawn, their envelope rebuilding the curve.
:width: 100%

Left: the energy of an Einstein solid against its entropy, per oscillator, at fixed volume. A
tangent slides along the curve. Its slope is the temperature $T$, and it meets the vertical axis,
$S = 0$, at the height $U - TS$ — marked by the blue dot. Right: that intercept, plotted against
the slope, traces a curve of its own, $F(T)$. In the second half the original curve fades and the
tangent lines are laid down one at a time, each also marked as a point $(T, F)$ on the right. The
lines by themselves rebuild the curve they came from: the curve is the edge that all of them
touch.
:::

The second is a piston inside a box, and a question about what the gas is minimising.

:::{figure} ../media/potentials-minimization.mp4
:alt: Left, a box surrounded by a heat bath, split by a piston; the dense left side expands as the piston moves right until both sides have the same shade. Right, above, the gas's energy change rising to about 280 joules; below, the free-energy change falling to about minus 2760 joules while the total entropy times temperature rises by the same amount.
:width: 100%

A rigid box, drawn in the orange heat bath at $300\ \mathrm{K}$, holds dense argon on both sides
of a piston: two moles in a quarter of the box on the left, one mole in the rest. Darker blue
means denser gas. The piston is released and drifts, braked, until the two densities match.
Upper right: the change in the gas's total energy, which *rises*, by about $280\ \mathrm{J}$.
Lower right: its free energy $F$ falls, by about $2760\ \mathrm{J}$, and the total entropy of gas
plus bath, multiplied by $T$, rises by exactly as much. The horizontal axis is how far the piston
has travelled toward where it stops.
:::

The third is a test that a numerical Maxwell relation can pass — and one that it fails.

:::{figure} ../media/potentials-maxwell-gap.mp4
:alt: Two colour maps over temperature and volume. The upper one darkens steadily as a step size shrinks; the lower one stays bright. Right, a log-log plot of the largest value in each map against the step size, one falling along a straight line and flattening at the bottom, the other flat near 0.1.
:width: 100%

The colour is the relative gap $|\Delta|$ between the two cross-derivatives of
$\mathrm{d}F = -S\,\mathrm{d}T - P\,\mathrm{d}V$, at each temperature and volume; darker is
smaller. Above: argon as a van der Waals gas, with $S$ and $P$ both read off its one fundamental
relation. As the difference step $h$ shrinks (right-hand axis), the map darkens fourfold with
every halving, until rounding error sets a floor near $10^{-7}$. Below: the ideal gas's entropy
paired with the van der Waals pressure — two substances pretending to be one. Its gap does not
shrink at all, and it is largest where the gas is densest.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a substance given by a smooth fundamental relation $S(U, V, N)$ — the Sackur–Tetrode ideal gas, the Einstein solid, or the van der Waals gas — alone, in contact with a heat bath, or pushed through a porous plug.
- **Dynamics:** none for the potentials themselves, which are functions of state; a released piston is stepped through a sequence of constrained equilibria while the bath absorbs whatever heat keeps its temperature fixed.
- **Boundary:** a heat-conducting wall to the bath; a frictionless piston wherever a pressure is held; an insulated porous plug for throttling.
- **Ensemble:** not applicable — the bath is a thermodynamic idealisation, and its statistical version, a finite bath and the Boltzmann factor, is module 11's starting point.
- **Ignored:** fluctuations, the finite size of any real bath, how fast anything relaxes, and every kind of work other than $P\,\mathrm{d}V$ unless it is named.
- **Valid when:** the bath is much larger than the system, and $S$ is strictly concave wherever it is used — for the van der Waals gas, above its critical temperature.
- **Failure modes:** a relation with a dent, where one slope names several states and the Legendre transform folds over (the advanced section, and module 14); small baths (module 11); processes too fast to pass through equilibrium states.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 10 — thermodynamic potentials](/lite/lab/index.html?path=en/labs/10-potentials.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/10-potentials.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Release the piston and watch the gas's energy. Then switch the gas to ideal and watch it again.
- Legendre-transform $U(S)$ on a coarse grid and ask how far each point is from the true $F(T)$ —
  and then how far the *curve* is.
- Feed the Maxwell check a pressure and an entropy from two different gases, and see whether
  refining the step rescues them.
- Load the rubber-band data and find the sign of the slope of tension against temperature.

(10-potentials-derive)=
## Derive the result

**System and boundary.** A single system described by module 09's fundamental relation, and, for
the central argument, that system in contact with a reservoir: a body so large that exchanging
heat (or volume) with the system does not change its temperature (or pressure).

**Independent variables and constraint.** At first $S$, $V$ and $N$, the natural variables of the
energy form $U(S, V, N)$. The whole module is about trading these for others. $N$ is held fixed
in every example; the $\mu\,\mathrm{d}N$ terms are kept in the formulas because module 13 needs
them.

**Sign convention.** The course convention holds throughout,

$$
\mathrm{d}U = \dbar Q + \dbar \Won ,
$$

with $\dbar Q$ positive into the system and $\dbar \Won$ the work done *on* it.

**Route.** Seven steps. First why a complete description in the wrong variables is a problem,
and why simply substituting new variables loses information. Then the Legendre transform, drawn
before it is written. Then the three potentials it builds, the four Maxwell relations they
imply, and the minimum principles that make them useful. Last, enthalpy as a bookkeeper, and the
module's showpiece: entropy from a pressure gauge.

### Step 1: a complete description in the wrong variables

Module 09 wrote the fundamental relation in its energy form, $U(S, V, N)$, with the differential

$$
\mathrm{d}U = T\,\mathrm{d}S - P\,\mathrm{d}V + \mu\,\mathrm{d}N .
$$

The slopes of $U$ are $T = (\partial U/\partial S)_{V,N}$ and $-P = (\partial U/\partial V)_{S,N}$.
Everything is there. But the variables are awkward: to use $U(S, V, N)$ you must control the
entropy, and there is no instrument that holds a system's entropy fixed while something else
happens. What a laboratory does control is temperature, with a water bath, and pressure, with the
atmosphere.

The obvious move is to substitute. For a monatomic ideal gas, $T = \partial U/\partial S$ can be
solved for $S$ and put back into $U$, giving

$$
U = \tfrac{3}{2} N \kB T .
$$

That is true, and it is useless as a fundamental relation. It does not depend on $V$ at all, so
no derivative of it can produce the pressure. Every gas whose energy is $\tfrac{3}{2} N \kB T$ has
this same $U(T, V)$, whatever its equation of state. Something was lost in the substitution.

What was lost can be seen in one variable. Suppose all you know about a curve $f(x)$ is its height
as a function of its slope, $p = f'(x)$. Then the curve $f(x - c)$, slid sideways by any $c$, has
exactly the same height at exactly the same slopes. Knowing "height as a function of slope" is a
differential equation for $f$, and its solution carries an undetermined constant. Substitution
throws away where along the $x$-axis the curve sits. The Legendre transform keeps it.

### Step 2: the Legendre transform, drawn

Take a curve $f(x)$ that is strictly convex: it curves upward everywhere, so its slope $p = f'(x)$
rises steadily with $x$. At each point draw the tangent line. It is fixed by two numbers, its
slope $p$ and the height $g$ at which it crosses the vertical axis $x = 0$:

$$
g(p) = f(x) - p\,x ,
\qquad
p = f'(x) .
$$

This is what the first animation draws. Two facts about it matter.

**Each slope names one point.** Because the slope rises steadily, each value of $p$ occurs at
exactly one $x$. So the list of tangent lines, labelled by their slopes, is in one-to-one
correspondence with the points of the curve.

**The lines rebuild the curve.** A convex curve lies above each of its tangent lines and touches
each at one point. So the curve is the upper edge of the whole family of lines — the *envelope*
the second half of the animation draws. Given only $g(p)$, the curve can be put back together:
$f(x)$ is the largest value, over all slopes $p$, of the line $g(p) + p\,x$.

Now the algebra. Differentiate $g = f - p\,x$, remembering that both $x$ and $p$ vary:

$$
\mathrm{d}g = \mathrm{d}f - p\,\mathrm{d}x - x\,\mathrm{d}p = -x\,\mathrm{d}p ,
$$

because $\mathrm{d}f = p\,\mathrm{d}x$. So the slope of $g$ is $-x$. Where $f$ had variable $x$
and slope $p$, $g$ has variable $p$ and slope $-x$. The roles have swapped and nothing is missing.

:::{admonition} The Legendre transform
:class: definition
For a function $f(x)$ whose slope $p = f'(x)$ is strictly monotonic, the **Legendre transform**
is the function of the slope

$$
g(p) = f(x) - p\,x ,
$$

with $x$ the point at which the slope is $p$. Its own slope is $g'(p) = -x$.
:::

:::{admonition} A Legendre transform loses nothing
:class: theorem
If $f$ is strictly convex or strictly concave, $f$ can be recovered from its transform:
$x = -g'(p)$ and then $f = g + p\,x$. The transform of the transform is the original function.
:::

For the energy, this is exactly what module 09's concavity buys. $S(U)$ is concave and
increasing, so its inverse $U(S)$ is convex: its second derivative is
$\partial T/\partial S = T/C_V$, positive for every stable substance. So the temperature — the
slope of $U(S)$ — rises steadily with entropy, and trading $S$ for $T$ is safe. Stability and
invertibility are the same property.

### Step 3: the three potentials

Apply the recipe to $U(S, V, N)$, one variable at a time or two at once.

**Trade $S$ for $T$.** The slope of $U$ with respect to $S$ is $T$, so the transform is
$F = U - TS$. Its differential follows from the product rule and module 09's $\mathrm{d}U$:

$$
\mathrm{d}F = \mathrm{d}U - T\,\mathrm{d}S - S\,\mathrm{d}T
= -S\,\mathrm{d}T - P\,\mathrm{d}V + \mu\,\mathrm{d}N .
$$

:::{admonition} The Helmholtz free energy
:class: definition
$$
F = U - TS ,
\qquad
\mathrm{d}F = -S\,\mathrm{d}T - P\,\mathrm{d}V + \mu\,\mathrm{d}N .
$$

Its natural variables are $T$, $V$ and $N$. Its slopes are $-S$, $-P$ and $\mu$.
:::

**Trade $V$ for $-P$.** The slope of $U$ with respect to $V$ is $-P$, so the transform is
$U - (-P)V = U + PV$.

:::{admonition} The enthalpy
:class: definition
$$
H = U + PV ,
\qquad
\mathrm{d}H = T\,\mathrm{d}S + V\,\mathrm{d}P + \mu\,\mathrm{d}N .
$$

Its natural variables are $S$, $P$ and $N$.
:::

**Trade both.** Doing both trades gives the third.

:::{admonition} The Gibbs free energy
:class: definition
$$
G = U - TS + PV ,
\qquad
\mathrm{d}G = -S\,\mathrm{d}T + V\,\mathrm{d}P + \mu\,\mathrm{d}N .
$$

Its natural variables are $T$, $P$ and $N$ — the two things a laboratory bench holds fixed,
and the amount of stuff.
:::

The four functions sit at the corners of a square, each reached from its neighbours by one trade.

:::{figure} ../media/potentials-map.png
:alt: Four boxes at the corners of a square. Top left, U of S, V, N with its differential; top right, F of T, V, N; bottom left, H of S, P, N; bottom right, G of T, P, N. Horizontal arrows are labelled minus T S, vertical arrows plus P V.
:width: 80%

The four energy potentials. Moving right subtracts $TS$ and trades entropy for temperature;
moving down adds $PV$ and trades volume for pressure. Each box gives the potential's natural
variables and its differential.
:::

Each of the three is as complete as $U(S, V, N)$ was, *provided it is written in its own natural
variables*: $F(T, V, N)$ is a fundamental relation, $F$ written as a function of anything else is
not. The ideal gas shows the difference. Written in terms of the thermal wavelength
$\lambda = h/\sqrt{2\pi m \kB T}$, Sackur–Tetrode gives

$$
F(T, V, N) = -N \kB T \left[ \ln\!\left(\frac{V}{N \lambda^3}\right) + 1 \right] .
$$

Its volume slope is $-N\kB T/V$, which is $-P$: the equation of state that $U(T, V)$ could not
supply is back.

**One more identity.** Module 09's Euler relation, $U = TS - PV + \mu N$, rearranges into

$$
G = U - TS + PV = \mu N .
$$

The Gibbs free energy of a one-component system is its chemical potential times the number of
particles. Module 13 starts from this line.

### Step 4: the Maxwell relations

Each potential is a function of state, so its differential is exact, and module 05's test
applies: the mixed second derivatives agree. For $F(T, V)$ at fixed $N$, the coefficients of
$\mathrm{d}T$ and $\mathrm{d}V$ are $-S$ and $-P$, so

$$
\frac{\partial}{\partial V}\left(\frac{\partial F}{\partial T}\right)
= \frac{\partial}{\partial T}\left(\frac{\partial F}{\partial V}\right)
\qquad\Longrightarrow\qquad
\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial P}{\partial T}\right)_V .
$$

The same step on the other three differentials gives the other three relations.

:::{admonition} Maxwell relation from $U(S, V)$
:class: theorem
$$
\left(\frac{\partial T}{\partial V}\right)_S = -\left(\frac{\partial P}{\partial S}\right)_V
$$
:::

:::{admonition} Maxwell relation from $H(S, P)$
:class: theorem
$$
\left(\frac{\partial T}{\partial P}\right)_S = \left(\frac{\partial V}{\partial S}\right)_P
$$
:::

:::{admonition} Maxwell relation from $F(T, V)$
:class: theorem
$$
\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial P}{\partial T}\right)_V
$$
:::

:::{admonition} Maxwell relation from $G(T, P)$
:class: theorem
$$
\left(\frac{\partial S}{\partial P}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_P
$$
:::

There is no need to memorise these. Each one is read off a differential in a line: the
variables held fixed tell you which potential, and the coefficients tell you what to
differentiate. Module 05's advanced section promised that exactness would stop looking like
an abstraction; this is the payoff. Work and heat were inexact, and nothing followed from them.
The potentials are exact, and every pair of their slopes is tied together.

The relation from $F$ is the remarkable one. Its left-hand side is how entropy changes with
volume — something no instrument reads. Its right-hand side is how pressure changes with
temperature in a sealed vessel — a pressure gauge and a thermometer. Step 7 puts it to work.

### Step 5: what is minimised when a bath holds the temperature

Module 09's maximum principle belongs to an isolated system. Put the system in contact with a
reservoir at temperature $T$ and it is not isolated any more — but system plus reservoir is, and
module 07's second law applies to the pair:

$$
\mathrm{d}S + \mathrm{d}S_{\text{res}} \ge 0 .
$$

The reservoir changes only by exchanging heat at its fixed temperature. If $\dbar Q$ flows into
the system, the reservoir loses entropy $\dbar Q / T$:

$$
\mathrm{d}S_{\text{res}} = -\frac{\dbar Q}{T} .
$$

Now hold the system's volume fixed, so no work is done on it, and $\dbar Q = \mathrm{d}U$ by the
first law. Substituting,

$$
\mathrm{d}S - \frac{\mathrm{d}U}{T} \ge 0
\qquad\Longrightarrow\qquad
\mathrm{d}U - T\,\mathrm{d}S \le 0 .
$$

At fixed $T$ the left side is exactly $\mathrm{d}F$.

:::{admonition} Minimum free energy at fixed temperature and volume
:class: theorem
A system in contact with a reservoir at temperature $T$, with its volume and particle number
fixed, can only change in ways that lower its Helmholtz free energy:

$$
\mathrm{d}F \le 0 ,
$$

with equality at equilibrium. The system's $F$ is at its minimum exactly when the total entropy
of system plus reservoir is at its maximum: $\Delta S_{\text{tot}} = -\Delta F / T$.
:::

Let the piston move against the atmosphere as well, at pressure $P$. Then the work done on the
system is $-P\,\mathrm{d}V$, the heat is $\dbar Q = \mathrm{d}U + P\,\mathrm{d}V$, and the same
three lines give $\mathrm{d}U + P\,\mathrm{d}V - T\,\mathrm{d}S \le 0$.

:::{admonition} Minimum Gibbs free energy at fixed temperature and pressure
:class: theorem
A system held at temperature $T$ by a reservoir and at pressure $P$ by a free piston can only
change in ways that lower its Gibbs free energy:

$$
\mathrm{d}G \le 0 ,
$$

with equality at equilibrium.
:::

This is the answer to the puzzle. A chemist's reactions run on a bench, at the room's temperature
and the atmosphere's pressure, so the chemist tabulates $G$. A physicist's crystal sits in a
cryostat at fixed temperature and fixed volume, so the physicist minimises $F$. Nobody is
disagreeing: each is quoting the potential that decides what happens under their own
constraints.

:::{admonition} The reservoir
:class: model-assumption
Every minimum principle here assumes an ideal reservoir: a body so large that the heat it
exchanges with the system leaves its temperature unchanged, and whose own entropy therefore
changes by exactly $-\dbar Q/T$. Real baths are finite. How large is large enough, and what a
small bath does instead, is module 11's opening question.
:::

**The energy can rise.** Nothing in the argument asks $U$ to fall. At fixed $T$ and $V$ the
requirement is only that $\Delta U < T\,\Delta S$. If the system's entropy rises by a lot, its
energy is free to rise too, with the reservoir supplying the difference. The second animation
shows exactly this: dense argon on both sides of a piston, its energy rising by
$282\ \mathrm{J}$ as the dense side spreads out and its atoms' mutual attraction weakens, while
$F$ falls by $2763\ \mathrm{J}$. The argon ends at the *largest* energy the piston can reach.
"Systems minimise their energy" is true for a ball rolling in a bowl with friction, and false for
anything whose entropy matters.

**What is free about free energy.** Let the system do work as well, with the reservoir still
holding its temperature. The first law now has a work term, $\Delta U = Q + \Won$, and the second
law still says $\Delta S - Q/T \ge 0$, so $Q \le T\,\Delta S$. Then

$$
\Won = \Delta U - Q \ge \Delta U - T\,\Delta S = \Delta F .
$$

:::{admonition} Maximum work at fixed temperature
:class: theorem
For a system in contact with a reservoir at temperature $T$, the work done on it is at least the
change in its Helmholtz free energy, $\Won \ge \Delta F$. The work it can deliver, $-\Won$, is
therefore at most $-\Delta F$, with equality for a reversible process.
:::

That is what "free" means: *available as work at fixed temperature*. It is not a quantity of
energy stored inside anything. Two cylinders of argon at the same temperature have the same
internal energy, and the compressed one can deliver more work, because its entropy is lower and
the reservoir will supply heat as it expands. At constant pressure the same argument, with the
work split into the $-P\,\Delta V$ spent pushing back the atmosphere and everything else, gives
the chemist's version: the work other than $P\,\mathrm{d}V$ that can be drawn from a process at
fixed $T$ and $P$ is at most $-\Delta G$.

### Step 6: enthalpy keeps the books on heat

At constant pressure, with no work other than $P\,\mathrm{d}V$, the first law reads

$$
\Delta U = Q_P - P\,\Delta V ,
$$

and moving the last term across gives

$$
Q_P = \Delta U + P\,\Delta V = \Delta H .
$$

The heat absorbed at constant pressure is the change in enthalpy. This is why chemists tabulate
$\Delta H$ for reactions, and why module 06's constant-pressure heat capacity is its slope,
$C_P = (\partial H/\partial T)_P$. It is also why $H$ is so often called "heat content" — a name
that is exactly as misleading as module 05's "heat stored in a body". $H$ is a function of state.
Heat is not, and the two coincide only under the two conditions in the derivation.

Break either one and they part. With work other than $P\,\mathrm{d}V$, say electrical work
$W_{\text{el}}$ done on the system, the first law gains a term and

$$
\Delta H = Q_P + W_{\text{el}} .
$$

Splitting a mole of liquid water into hydrogen and oxygen at $298\ \mathrm{K}$ and $1\ \mathrm{bar}$
has $\Delta H = 285.8\ \mathrm{kJ}$. Run reversibly in an electrolysis cell, the electrical work is
$\Delta G = 237.1\ \mathrm{kJ}$ — the reason a cell needs at least $1.23\ \mathrm{V}$ — and the
other $48.7\ \mathrm{kJ}$ arrives as heat drawn from the surroundings. $\Delta H$ is the same
whatever the route; the heat is not.

**Throttling.** Push a gas steadily through a porous plug in an insulated pipe. Follow one parcel
of $N$ particles across. The gas behind it pushes it through, doing work $P_1 V_1$ on it; on the
far side it pushes the gas ahead, doing work $P_2 V_2$; no heat crosses the insulation. So

$$
U_2 - U_1 = P_1 V_1 - P_2 V_2
\qquad\Longrightarrow\qquad
U_2 + P_2 V_2 = U_1 + P_1 V_1 .
$$

The enthalpy is the same on both sides of the plug; nothing else has to be. For an ideal gas, $H$
depends only on temperature, so the temperature is unchanged too. For a real gas it is not: the
van der Waals argon of the laboratory, throttled from $50$ to $1\ \mathrm{bar}$ at
$300\ \mathrm{K}$, cools by $18.3\ \mathrm{K}$ — while its internal energy *rises* by
$50\ \mathrm{J}$ per mole. This is the Joule–Thomson effect, and it is how air is liquefied.

### Step 7: entropy from a pressure gauge

Now the showpiece. Integrate the Maxwell relation from $F$ along an isotherm:

$$
\Delta S = \int_{V_1}^{V_2} \left(\frac{\partial S}{\partial V}\right)_T \mathrm{d}V
= \int_{V_1}^{V_2} \left(\frac{\partial P}{\partial T}\right)_V \mathrm{d}V .
$$

The right-hand side is a laboratory procedure. At each of several volumes, seal the gas and
record its pressure at several temperatures; the slope of each line is
$(\partial P/\partial T)_V$; add the slopes up across the volumes. No step reads an entropy.

For an ideal gas $(\partial P/\partial T)_V = N\kB/V$, and the integral gives

$$
\Delta S = N \kB \ln\frac{V_2}{V_1} ,
$$

module 09's free-expansion entropy, now reached a fourth way. For a van der Waals gas the
pressure is

$$
P = \frac{N \kB T}{V - N b} - \frac{a N^2}{V^2} ,
$$

and at fixed volume the attraction term does not depend on temperature, so it drops out of the
slope entirely:

$$
\Delta S = N \kB \ln\frac{V_2 - N b}{V_1 - N b} .
$$

The atoms' size shows up in the entropy and their attraction does not. The laboratory makes both
measurements from simulated noisy gauge readings.

**A rubber band.** Stretching a band by $\mathrm{d}L$ against its tension $f$ does work
$f\,\mathrm{d}L$ on it, so its fundamental relation is
$\mathrm{d}U = T\,\mathrm{d}S + f\,\mathrm{d}L$, its free energy obeys
$\mathrm{d}F = -S\,\mathrm{d}T + f\,\mathrm{d}L$, and its Maxwell relation is

$$
\left(\frac{\partial S}{\partial L}\right)_T = -\left(\frac{\partial f}{\partial T}\right)_L .
$$

Clamp a band at a fixed length, hang it from a force gauge, and warm it: the tension rises, by
about $5.8\ \mathrm{mN}$ per kelvin in the laboratory's data. So stretching the band at fixed
temperature *lowers* its entropy. The long molecules inside are pulled out of their tangled,
many-arrangement states into fewer, straighter ones — module 08's entropic force, measured with a
spring balance.

The rest of prediction 3 follows from that one sign. Stretched fast, the band has no time to lose
heat, so its entropy stays fixed; the arrangements the chains lose must be made up somewhere, and
they are made up by faster jiggling — the band warms your lip. And a band holding a weight pulls
harder when warmed, so it lifts the weight: it contracts on heating, the opposite of almost every
other material.

:::{note} The module in seven statements
1. $U(S, V, N)$ is complete but its variables cannot be controlled. Substituting $T$ for $S$
   throws information away.
2. The Legendre transform $g = f - p\,x$ trades a variable for its slope and loses nothing, as
   long as the function is strictly convex or concave. Stability is exactly that condition.
3. The transforms of $U$ are $H = U + PV$, $F = U - TS$ and $G = U - TS + PV$, each complete in
   its own natural variables. The Euler relation gives $G = \mu N$.
4. Every potential is a state function, so its mixed partials agree: four Maxwell relations.
5. In contact with a reservoir, $F$ falls to a minimum at fixed $T$ and $V$, and $G$ at fixed
   $T$ and $P$. The energy may rise while they fall.
6. At constant pressure with only $P\,\mathrm{d}V$ work, $Q = \Delta H$. Across a throttle $H$ is
   conserved.
7. $(\partial S/\partial V)_T = (\partial P/\partial T)_V$ turns a pressure gauge and a
   thermometer into an entropy meter.
:::

(10-potentials-verify)=
## Verify computationally

The derivation is a chain of exact statements. The laboratory checks each link numerically, on
the ideal gas, the Einstein solid and the van der Waals gas, and includes a test built to fail.
Each check is also a test in the project's suite.

**1. The potentials from the relation match their closed forms.** Located on the entropy surface
by bisection, with no formula for any potential supplied, $F$ agrees with the Sackur–Tetrode
closed form of step 3 and with the Einstein solid's $F = n \kB T \ln(1 - e^{-\varepsilon/\kB T})$
to better than one part in $10^{9}$. $G/N$ equals module 09's chemical potential, $H$ equals
$\tfrac{5}{2} N \kB T$, and differentiating each potential numerically returns its conjugate
variables, all to one part in $10^{6}$ or better.

**2. The Legendre transform, numerically.** On a grid of $10^4$ values of $S$, taking slopes of
$U(S)$ and subtracting gives $F$ from $25$ to $3600\ \mathrm{K}$ within $4 \times 10^{-15}$ of the
closed form. On coarse grids the transform shows a property worth knowing:

:::{admonition} The curve is more accurate than its points
:class: numerical-observation
With 25 to 400 grid points, each sample's temperature is off by an amount that falls at second
order in the spacing, as a central difference's should — yet the points lie on the true $F(T)$
curve to *fourth* order: $7 \times 10^{-7}$ at 25 points, $8 \times 10^{-12}$ at 400. The
intercept $f - p\,x$ is stationary in $x$ at the true tangent point, so an error in the slope
slides the point along the curve, and only its square moves it off.
:::

**3. A Maxwell relation holds — and can fail.** For the van der Waals relation, the relative gap
between $(\partial S/\partial V)_T$ and $(\partial P/\partial T)_V$ falls from
$1.3 \times 10^{-4}$ to $2.1 \times 10^{-6}$ as the step shrinks from $0.04$ to $0.005$, at an
observed order of exactly 2. That is the whole of what remains: the truncation error of the
differences, down to a rounding floor near $10^{-7}$. Pair the ideal gas's entropy with the van
der Waals pressure instead and the gap sits at $Nb/(2V - Nb)$ — $0.119$ at $0.15\ \mathrm{L}$ —
and does not move when the step is refined tenfold.

:::{admonition} Central differences
:class: approximation
Every slope in the laboratory is a central difference with a step that is a fixed fraction of
the variable, accurate to about one part in $10^{8}$ for a first derivative. The Maxwell check
differences those slopes once more, which is why its gap has a floor near $10^{-7}$ rather than
reaching zero. A floor that small is a limit of arithmetic, not of the physics.
:::

**4. Free energy falls while energy rises.** The piston run of the second animation, stepped
through 201 constrained equilibria:

$$
\begin{gathered}
\Delta U = +282.3\ \mathrm{J} ,
\qquad
\Delta F = -2763.0\ \mathrm{J} , \\
T\,\Delta S_{\text{argon}} = +3045.3\ \mathrm{J} ,
\qquad
T\,\Delta S_{\text{bath}} = -282.3\ \mathrm{J} .
\end{gathered}
$$

$F$ falls at every step and the total entropy rises at every step, by $9.210\ \mathrm{J\,K^{-1}}$
in all. That total equals $-\Delta F/T$ by construction, because the bath's entropy is booked from
the first law, so the agreement is bookkeeping rather than a test; what the run shows is that both
move one way only, and that $U$ climbs while they do. The piston stops where the pressures agree, at
$18.41\ \mathrm{bar}$ on both sides — which for one gas at one temperature means equal densities.
The same run on ideal argon changes the energy by nothing and lowers $F$ by
$2870\ \mathrm{J}$. Neither gas minimised its energy.

**5. Enthalpy keeps the books.** Module 06's isobaric heat, $C_P\,\Delta T$, and the enthalpy
difference between the two end states located on the entropy surface agree to one part in
$10^{8}$. Throttling from $50$ to $1\ \mathrm{bar}$ leaves ideal argon at $300.00\ \mathrm{K}$ and
cools van der Waals argon to $281.74\ \mathrm{K}$, with $H$ unchanged in both. For a small drop at
$1\ \mathrm{bar}$ the cooling is $0.3683\ \mathrm{K}$ per bar, against $0.3687$ from the textbook
formula for a dilute van der Waals gas.

**6. Entropy from a pressure gauge.** A simulated gauge that reads pressure to $0.2\%$ is read at
nine temperatures and nine volumes from $1$ to $2\ \mathrm{L}$, for $10^{21}$ atoms. The
reconstructed entropy change is

$$
\Delta S = (9.515 \pm 0.043) \times 10^{-3}\ \mathrm{J\,K^{-1}} ,
$$

against $N \kB \ln 2 = 9.570 \times 10^{-3}\ \mathrm{J\,K^{-1}}$: an uncertainty of $0.45\%$, and
$1.3$ error bars from the truth. Over twenty independent runs the mean lands $0.1\%$ from
$N \kB \ln 2$, and the runs scatter by $4.9 \times 10^{-5}$, against the $4.3 \times 10^{-5}$
each run reports about itself — the error bar is honest. For one mole of dense van der Waals
argon doubling from $0.2$ to $0.4\ \mathrm{L}$, the gauge gives $6.520\ \mathrm{J\,K^{-1}}$,
matching $N \kB \ln[(V_2 - Nb)/(V_1 - Nb)]$ to six digits, and $13\%$ more than the ideal gas's
$5.763$.

**7. The rubber band.** A straight line through all thirteen readings of the reference dataset
gives $(\partial f/\partial T)_L = 5.79 \pm 0.17\ \mathrm{mN\,K^{-1}}$, so
$(\partial S/\partial L)_T = -5.79\ \mathrm{mJ\,K^{-1}\,m^{-1}}$. At $295\ \mathrm{K}$ the band pulls
with $2.00\ \mathrm{N}$, of which $T\,(\partial f/\partial T)_L = 1.71\ \mathrm{N}$ is entropic:
the energy of stretched bonds accounts for about $15\%$ of the tension.

:::{admonition} A thermodynamic identity in rubber
:class: empirical-law
Natural rubber's tension at fixed extension rises almost in proportion to the absolute
temperature, with a small energetic part of order ten to twenty percent — a result measured
since the nineteenth century, and the experimental basis for treating rubber elasticity as
mainly entropic. The Maxwell relation turns the measurement into a statement about entropy;
the size of the energetic part is a property of the material, not of thermodynamics.
:::

(10-potentials-transfer)=
## Transfer the idea

Looking back:

- **Module 05** separated exact differentials from inexact ones and warned that the distinction
  would pay off. Heat and work, being inexact, have no Maxwell relations. The potentials, being
  exact, have four, and one of them measures entropy.
- **Module 06's** constant-pressure heat and $C_P$ are now $\Delta H$ and its slope. The
  bookkeeping was right; it now has a function of state behind it.
- **Module 07's** second law, applied to a system and its reservoir together, is the whole of
  step 5. The minimum principles are not new laws.
- **Module 08** ended with rubber elasticity as an entropic force. The rubber band's Maxwell
  relation is that claim with a number on it.
- **Module 09's** concavity is exactly the condition that makes the Legendre transform safe, and
  its Euler relation becomes $G = \mu N$.

Looking ahead:

- **Modules 11 and 12** meet $F$ a second time, from counting. A system in contact with a bath
  has a *partition function* $Z$, and $F = -\kB T \ln Z$. Module 12 checks that this $F$ and the
  one on this page are the same function for the Einstein solid.
- **Module 13** opens with $\mu = (\partial G/\partial N)_{T,P}$ and $G = \mu N$.
- **Module 14** takes a relation with a dent — the advanced section below — and shows that the
  fold in its $G(P)$ is two phases coexisting.

And sideways:

- **Chemistry tables** of $\Delta H$ and $\Delta G$ are this module institutionalised. Hess's law —
  that the heat of a reaction does not depend on the steps it is split into — is the statement
  that $\Delta H$ is a difference of a function of state, and it holds at constant pressure with no
  other work. A negative $\Delta G$ at the bench's temperature and pressure means a reaction *can*
  run; it says nothing about how fast.
- **Steam tables** list enthalpy because a turbine or a compressor is a steady-flow device, and
  the parcel argument of step 6 — with the shaft's work added — is exactly how engineers do their
  energy books.

:::{admonition} Choosing a potential
:class: definition
The **natural variables** of a potential are the variables in which it is a fundamental
relation. The potential that is extremal under a given set of constraints is the one whose
natural variables those constraints fix: $S$ for an isolated system (maximum), $F$ at fixed $T$
and $V$, $G$ at fixed $T$ and $P$ (minima), and $H$ across a throttle (conserved).
:::

### Worked examples

Try each one before opening its solution.

**Worked example 1 — heating at constant pressure.** One mole of argon is heated at a constant
$1\ \mathrm{bar}$ from $300$ to $400\ \mathrm{K}$. Find $\Delta U$, the work done on the gas, the
heat absorbed and $\Delta H$.

:::{dropdown} Solution
For a monatomic ideal gas,

$$
\Delta U = \tfrac{3}{2} R\,\Delta T = 1247.2\ \mathrm{J} .
$$

The volume grows by $R\,\Delta T/P = 8.314 \times 10^{-3}\ \mathrm{m^3}$, so the work done on the
gas is

$$
\Won = -P\,\Delta V = -831.4\ \mathrm{J} .
$$

The first law gives the heat, and it equals the enthalpy change:

$$
Q_P = \Delta U - \Won = 2078.6\ \mathrm{J} = \tfrac{5}{2} R\,\Delta T = \Delta H .
$$

Two-fifths of the heat went into pushing back the atmosphere.
:::

**Worked example 2 — the most work at fixed temperature.** One mole of an ideal gas at
$300\ \mathrm{K}$ expands from $10$ to $20\ \mathrm{L}$ against a piston, in contact with a bath at
$300\ \mathrm{K}$. What is the most work it can deliver, and where does the energy come from?

:::{dropdown} Solution
At fixed temperature the work it can deliver is at most $-\Delta F$. Only the volume term of $F$
changes:

$$
-\Delta F = R T \ln\frac{V_2}{V_1} = 8.314 \times 300 \times \ln 2 = 1729\ \mathrm{J} .
$$

The gas's energy does not change at all, so every one of those joules came from the bath, as heat
$Q = 1729\ \mathrm{J}$. The gas is a converter, not a store. If it expanded freely into a vacuum
instead, it would reach the same final state, deliver nothing, and produce
$R \ln 2 = 5.76\ \mathrm{J\,K^{-1}}$ of entropy — module 09's lost work.
:::

**Worked example 3 — entropy from a gauge, real gas.** One mole of argon doubles its volume from
$0.5$ to $1.0\ \mathrm{L}$ at fixed temperature. Treating it as a van der Waals gas with
$b = 3.20 \times 10^{-5}\ \mathrm{m^3\,mol^{-1}}$, find its entropy change and compare it with the
ideal gas's.

:::{dropdown} Solution
The Maxwell relation from $F$ gives $(\partial S/\partial V)_T = (\partial P/\partial T)_V$, and
for the van der Waals gas that slope is $R/(V - b)$ per mole. Integrating,

$$
\Delta S = R \ln\frac{V_2 - b}{V_1 - b} = 8.314 \ln\frac{0.968}{0.468} = 6.04\ \mathrm{J\,K^{-1}} ,
$$

against $R \ln 2 = 5.76\ \mathrm{J\,K^{-1}}$ for an ideal gas. The excluded volume makes the
doubling a larger fractional gain in the room each atom can actually use. The attraction constant
$a$ never appears: it lowers the pressure by the same amount at every temperature.
:::

**Worked example 4 — the rubber band's entropy.** The laboratory's band, clamped at twice its
slack length, has a tension of $2.00\ \mathrm{N}$ at $295\ \mathrm{K}$, rising at
$5.79\ \mathrm{mN}$ per kelvin. How much heat does it give off if stretched a further centimetre,
slowly, at $295\ \mathrm{K}$? What share of its tension is entropic?

:::{dropdown} Solution
By the Maxwell relation, $(\partial S/\partial L)_T = -5.79 \times 10^{-3}\ \mathrm{J\,K^{-1}\,m^{-1}}$.
Treating that slope as constant over the extra centimetre, the heat taken in reversibly is

$$
Q = T\,\Delta S = 295 \times (-5.79 \times 10^{-3}) \times 0.01 = -0.017\ \mathrm{J} ,
$$

so the band gives off $17\ \mathrm{mJ}$ to its surroundings. The entropic part of the tension is
$T\,(\partial f/\partial T)_L = 295 \times 5.79 \times 10^{-3} = 1.71\ \mathrm{N}$, which is
$85\%$ of the $2.00\ \mathrm{N}$.
:::

**Worked example 5 — splitting water.** For $\mathrm{H_2O(l)} \to \mathrm{H_2} + \tfrac{1}{2}\mathrm{O_2}$
at $298\ \mathrm{K}$ and $1\ \mathrm{bar}$, $\Delta H = 285.8\ \mathrm{kJ\,mol^{-1}}$ and
$\Delta G = 237.1\ \mathrm{kJ\,mol^{-1}}$. Two electrons pass through the cell per molecule. What is
the smallest voltage that can split water, and what heat flows when the cell runs reversibly? At
what voltage does it need no heat at all?

:::{dropdown} Solution
At fixed $T$ and $P$ the electrical work done on the system is at least $\Delta G$. Two moles of
electrons carry a charge $2F_{\mathrm{Far}}$, with $F_{\mathrm{Far}} = 96\,485\ \mathrm{C\,mol^{-1}}$
the Faraday constant, so

$$
V_{\min} = \frac{\Delta G}{2 F_{\mathrm{Far}}} = \frac{237\,100}{2 \times 96\,485} = 1.229\ \mathrm{V} .
$$

Run reversibly, $\Delta H = Q + W_{\text{el}}$ gives $Q = 285.8 - 237.1 = 48.7\ \mathrm{kJ}$ drawn
*in* from the surroundings. Raise the voltage and more of $\Delta H$ comes in as electrical work;
at

$$
\frac{\Delta H}{2 F_{\mathrm{Far}}} = 1.481\ \mathrm{V}
$$

the heat is zero. $\Delta H$ was the same throughout, and the heat was anything from
$48.7\ \mathrm{kJ}$ in to heat given off: enthalpy is not the heat of the process.
:::

**Worked example 6 — which potential?** For each situation, name the quantity that is extremal
or conserved: (a) a sealed steel bomb in a water bath; (b) a reaction in an open flask on a bench;
(c) a gas leaking through a crack in an insulated pipe; (d) a thermos of coffee, sealed.

:::{dropdown} Solution
(a) Fixed $T$ and $V$: $F$ falls to a minimum. (b) Fixed $T$ and $P$: $G$ falls to a minimum.
(c) A steady throttle: $H$ is the same on both sides. (d) An isolated system, near enough:
$S$ rises to a maximum, which is module 09's principle and the one all the others were derived
from.
:::

:::{note} Your predictions, revisited
1. **No.** At fixed temperature and volume what must fall is $F = U - TS$. The energy can rise,
   with the bath paying — and in the laboratory's piston it rises to the *largest* value the
   piston can reach. See [the minimum principles](#10-potentials-derive).
2. **Yes.** Equal energies, unequal free energies: the compressed cylinder can deliver
   $RT \ln 10$, about $5.7\ \mathrm{kJ}$ per mole at room temperature, more than one at a tenth of
   the pressure. Free energy is not energy stored inside; it is work available against the room.
3. **Warmer, and it contracts.** Stretching lowers a rubber band's entropy, because its tension
   rises with temperature: the Maxwell relation turns one fact into the other, and both follow.
4. **Only under conditions.** $Q = \Delta H$ at constant pressure when the only work is
   $P\,\mathrm{d}V$. Add electrical work, or let the pressure change, and they part.
:::

(10-potentials-quiz)=
## Check your understanding

```{include} ../_generated/quiz-10-potentials.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](10-potentials-problems.md).

(10-potentials-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A chemist asks why physicists keep writing $F$ where every chemistry table lists $G$. Explain
   the difference without calling either choice wrong.
2. What exactly is "free" in free energy, and what is not? Use the two argon cylinders of
   prediction 2.
3. Explain to a laboratory technician, without the word "entropy" in your first sentence, why
   measuring how a sealed gas's pressure rises with temperature tells you how its entropy grows
   with volume.
4. Why does substituting $T$ for $S$ in $U(S, V)$ lose information, while the Legendre transform
   to $F(T, V)$ does not?
5. A student says that because the piston's argon ended at higher energy, "energy must have been
   created". Find the flaw.

(10-potentials-advanced)=
## Advanced: a mnemonic, a second family, and a dent

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It covers a memory aid the course
deliberately does not rely on, the potentials built from entropy instead of energy, and what
happens to a Legendre transform when the relation is not convex.
:::

**The thermodynamic square.** Generations of students have memorised the four Maxwell relations
with a square whose corners carry potentials and whose sides carry variables, read off by walking
around its edges with sign rules for each direction. It works, and the course does not use it.
Every relation on this page was read off a differential in one line, and checked numerically in
the laboratory. A mnemonic stores four facts; the method produces any number of them, including
the rubber band's, which no square contains.

**Massieu functions.** The Legendre transforms of this module were all taken of the energy
$U(S, V, N)$. The entropy $S(U, V, N)$ can be transformed just as well, and its natural slope is
$1/T$. Trading $U$ for $1/T$ gives

$$
S - \frac{U}{T} = -\frac{F}{T} ,
$$

a **Massieu function**, whose natural variable is $1/T$. It carries the same information as $F$,
but its form is the one module 11 finds when it counts states: the logarithm of the partition
function, $\ln Z$, is exactly $-F/\kB T$.

**A relation with a dent.** Every transform on this page assumed strict convexity. Below its
critical temperature, about $151\ \mathrm{K}$ for argon, the van der Waals $F(V)$ does not have it:
over a range of volumes it curves the wrong way, and the pressure there *rises* as the gas is
compressed — the unstable stretch of module 02's loop.

:::{figure} ../media/potentials-dent.png
:alt: Left, a curve of free energy plus a straight-line tilt against volume, with two wells separated by a bump; the bump region is red. Right, Gibbs free energy against pressure, with two black branches crossing and a red branch joining their ends to form a narrow triangle with two sharp points.
:width: 100%

The van der Waals $F(V)$ of argon at $0.85\,T_c$. (a) $F + \bar{P} V$ against volume, where
$\bar{P}$ is a constant pressure chosen to make the dent visible — adding a straight line changes
no curvature. The red stretch is where $F$ curves the wrong way. (b) Each tangent to $F(V)$ has
slope $-P$ and meets the axis at $F + PV = G$. The tangents from the two healthy stretches give
the two black branches; those from the dent give the red one, joining the branches' ends in two
sharp points. Between about $2$ and $30\ \mathrm{bar}$, three values of $G$ share each pressure.
:::

The transform has not lost the dent: the red branch is there. What it has lost is the ability to
say which of three states a given pressure means, and so the laboratory's `legendre_transform`
refuses the calculation while `tangent_intercepts` draws the fold. The two black branches cross.
Past that crossing, the branch with the lower $G$ is the one the minimum principle of step 5
chooses — and a real substance, at that pressure, does something the smooth curve cannot: it
splits into liquid and vapour. Module 14 begins at that crossing.

:::{admonition} What is still open here
:class: open-question
The minimum principles of this module need a reservoir and a system that settles into
equilibrium with it. Many of the most interesting systems never settle: a living cell, a
driven chemical reactor, the climate. They sit in steady states that are held away from
equilibrium by a constant flow of energy through them. Whether such states are selected by the
extremum of some general potential — as equilibrium states are by $F$ and $G$ — is an active
research question. Several candidate principles have been proposed, and none holds in general.
:::
