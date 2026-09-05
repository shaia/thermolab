---
title: Thermodynamic processes
short_title: 06 · Processes
module: 06-processes
objectives:
  - id: OBJ-06-1
    text: Identify the four quasistatic process families and give the first-law signature of each.
  - id: OBJ-06-2
    text: Derive P V^gamma = constant for a quasistatic adiabatic process of an ideal gas.
  - id: OBJ-06-3
    text: Relate C_V, C_P and gamma for an ideal gas, and explain physically why C_P exceeds C_V.
  - id: OBJ-06-4
    text: Compute the work in an irreversible process from the pressure acting at the boundary.
  - id: OBJ-06-5
    text: Analyse the free expansion, and explain why it is adiabatic yet does not obey P V^gamma = constant.
---

# Thermodynamic processes

(06-processes-puzzle)=
## The puzzle: two ways to double a volume, neither of them heated

A cylinder of helium sits inside a perfect insulator. No heat can enter it and none can
leave. Whatever we do to this gas, $Q = 0$.

**First way.** The cylinder is closed by a piston carrying a pile of sand. Remove the grains
one at a time. The gas pushes the piston out grain by grain, and by the time the volume has
doubled, the helium has cooled from 300 K to 189 K.

**Second way.** The cylinder is one half of the insulated box; the other half is empty, and a
thin partition separates them. Pull the partition out. The gas rushes into the empty half.
Its volume has doubled. Its temperature is still 300 K, to the last decimal place.

Same gas, same insulation, same start, same finish volume. In the first case the temperature
fell by 37%; in the second it did not move at all.

:::{important} The question
Both processes are adiabatic — that is what "no heat crosses the boundary" means, and it is
true of both. Yet only one of them obeys the law every textbook prints as *the* adiabatic
law, $P V^{\gamma} = \text{constant}$. Which one, and why is the other one exempt?

And where did the first gas's energy go, if nothing left through the walls?
:::

The answer is not a subtlety about insulation. It is that "adiabatic" and "quasistatic" are
two independent conditions, and the famous law needs both. This module separates them, and
the separation turns out to be worth roughly half the work an engine could have produced.

(06-processes-predict)=
## Predict before you calculate

Commit to an answer for each before reading on. Write them down.

1. An insulated gas is compressed slowly to half its volume. Does its temperature rise, fall
   or stay put? Now the same gas, insulated, is allowed to expand slowly to twice its volume.
   By what factor does its temperature change?
2. A gas expands into a vacuum inside an insulated box. What are $Q$, $W_{\mathrm{on}}$,
   $\Delta U$ and $\Delta T$? Be careful with the third and fourth: they are not the same
   question.
3. You want to warm one mole of a gas by exactly one kelvin. Does it take more heat at
   constant volume or at constant pressure? Where does the difference go?
4. A gas is compressed by dropping a heavy weight onto its piston, so that it slams down to a
   new position and stops. Compare the work done on the gas with the work done in compressing
   it slowly between the same two volumes. Which is larger?

:::{note} Question 2 is the one to be honest about
Almost everybody knows that expanding gases cool — spray cans get cold, and clouds form over
mountains. That knowledge is correct and it is about to be applied in exactly the wrong place.
Write down your prediction before the next section rather than after it.
:::

(06-processes-explore)=
## Explore the model

The laboratory for this module runs a gas along each of the four quasistatic families out of
a common starting state, and then races the three *adiabatic* routes of the puzzle against
each other: slow expansion, expansion against a fixed load, and free expansion into a vacuum.

First, the four families. Every one of them leaves the same point in the $P$–$V$ plane, and
each is a different constraint on what is held fixed:

:::{figure} ../media/processes-families.mp4
:alt: Four curves fanning out from a common point in the P-V plane, beside three stacked bar panels showing work, heat and internal-energy change accumulating along each.
:width: 100%

Left, the four quasistatic families leaving one common state in the pressure–volume plane;
right, three stacked panels tracking the work done on the gas, the heat into it, and its change
of internal energy as each route is traversed. Blue is isochoric — a vertical line, since the
volume never changes — orange isobaric (horizontal), green isothermal, red adiabatic. Watch
which bars stay flat at zero: blue in the work panel, because a boundary that does not move
does no work; green in the energy panel, because an isotherm ends where it began in
temperature; and red in the heat panel, which is what "adiabatic" means. The red curve is the
steep one, falling below the green isotherm, because the energy it spends on the piston comes
out of the gas itself.
:::

Now the puzzle. Three routes, all adiabatic, all doubling the volume, and nothing in common
after that:

:::{figure} ../media/processes-three-adiabats.mp4
:alt: Three panels: a pressure-volume plane with two shaded work areas, a bar chart of work delivered, and a temperature-volume plane where only one route has a curve.
:width: 100%

Three adiabatic expansions from one state to one final volume, in three panels. **Left**, the
pressure–volume plane: the slow route (red) traces a curve and shades the largest area, the
work it delivers; the route against a fixed load (orange) shades the rectangle under its
constant external pressure, a third smaller; the free expansion (green) shades nothing, because
zero external pressure means zero work. **Middle**, the work delivered as a bar per route —
there are only two visible bars, and the missing green one is the point. **Right**, temperature
against volume: the slow route has a curve because it passes through equilibrium states and has
a temperature at every instant, while the other two have only a start dot and an end dot with
nothing drawn between them, because in between they have no temperature at all. The three final
temperatures are 189 K, 225 K and 300 K.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a fixed amount of ideal gas, $N$ particles with $f$ quadratic degrees of freedom each, in a cylinder closed by a piston — or in an insulated box divided by a removable partition.
- **Dynamics:** two regimes. Quasistatic, where the gas holds one $(P, V, T)$ throughout and passes through equilibrium states only; and irreversible, where only the endpoints are equilibrium states and the work follows the external pressure.
- **Boundary:** a frictionless piston set in a wall that is either diathermal (heat may cross) or adiabatic (it may not). The partition of the free expansion is adiabatic and does no work.
- **Ensemble:** not applicable to the thermodynamics; the microscopic free expansion in the laboratory is microcanonical, conserving energy exactly.
- **Ignored:** friction, the piston's own mass and inertia, gas non-ideality, heat leaking through an adiabatic wall, and the time the gas takes to re-equilibrate after each step.
- **Valid when:** quasistatic results — the process is slow compared with the gas's relaxation time; irreversible results — the external pressure is known and uniform at the moving boundary.
- **Failure modes:** real gases, whose internal energy depends on volume, so their free expansion *does* change the temperature; compressions fast enough that even the external pressure is not uniform; a wall that leaks, which makes "adiabatic" false rather than approximate.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 06 — thermodynamic processes](/lite/lab/index.html?path=en/labs/06-processes.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/06-processes.ipynb`.
:::

Three things worth doing before you read the derivation:

- Slide the number of degrees of freedom from 3 to 5 to 6 and watch the adiabat flatten
  towards the isotherm. Ask yourself what $f \to \infty$ would mean physically.
- Set the external pressure of the irreversible expansion to zero and check that it becomes
  the free expansion exactly, not approximately.
- Run the *microscopic* free expansion, where a box of particles is suddenly widened. Nothing
  in that code touches a single velocity — watch what the measured temperature does.

(06-processes-derive)=
## Derive the result

**System and boundary.** The gas in the cylinder; the piston is the moving boundary.

**Independent variables.** $N$, $V$, $T$ and the number of quadratic degrees of freedom $f$
per particle, with $P$ fixed by the equation of state. Every result below is macroscopic
thermodynamics — no microstate is counted anywhere in this section — except the final check in
the laboratory, which is kinetic.

**Sign convention.** As everywhere in this course,

$$
dU = \delta Q + \delta W_{\mathrm{on}},
\qquad
\delta W_{\mathrm{on}} = -P_{\mathrm{ext}}\, dV .
$$

Note which pressure appears there. Work is done *at the boundary*, by whatever the piston
pushes against, so the honest statement of the second equation carries $P_{\mathrm{ext}}$.
Module 5 wrote it with the gas's own $P$, which is correct only when the two are equal — and
that equality is the definition we are about to make precise.

### Heat capacities, and why there are two of them

The heat needed to raise a gas's temperature depends on what you hold fixed while you do it.
At constant volume the gas cannot expand, so no work is done and all the heat goes into
internal energy:

$$
C_V = \left(\frac{\partial U}{\partial T}\right)_V = \frac{f}{2} N k_B .
$$

At constant pressure the gas also pushes its piston out, and that expansion has to be paid
for. Writing $\delta Q = dU + P\,dV$ and using $P\,dV = N k_B\, dT$ along an isobar:

$$
C_P = C_V + N k_B .
$$

:::{admonition} Mayer's relation
:class: theorem
For an ideal gas the two heat capacities differ by exactly $N k_B$, independently of $f$ and
of the temperature. The excess is not a property of the substance but of the bookkeeping: it
is the expansion work per kelvin, and nothing else. The ratio

$$
\gamma \equiv \frac{C_P}{C_V} = \frac{f + 2}{f}
$$

is $5/3$ for a monatomic gas and $7/5$ for a diatomic one at room temperature, where its two
rotational degrees of freedom are active and its vibrational one is frozen out.
:::

### The adiabat

Now shut the heat off and move slowly. Slowly enough that the gas is in equilibrium at every
instant, so it has a single pressure and $P_{\mathrm{ext}} = P$. Then $\delta Q = 0$ gives

$$
C_V\, dT = -P\, dV .
$$

Differentiate the equation of state $PV = N k_B T$ to eliminate $dT$:

$$
P\, dV + V\, dP = N k_B\, dT .
$$

Substituting, and using $C_V = N k_B/(\gamma - 1)$:

$$
\frac{P\, dV + V\, dP}{\gamma - 1} = -P\, dV
\qquad\Longrightarrow\qquad
V\, dP = -\gamma P\, dV .
$$

Separate and integrate:

$$
\frac{dP}{P} = -\gamma \frac{dV}{V}
\qquad\Longrightarrow\qquad
\boxed{\; P V^{\gamma} = \text{constant} \;}
$$

and, folding the equation of state back in, the same law in the variables that matter for the
puzzle:

$$
T V^{\gamma - 1} = \text{constant} .
$$

For helium ($\gamma = 5/3$) doubling the volume multiplies the temperature by
$2^{-2/3} = 0.630$: from 300 K to 189 K, exactly as the first cylinder did.

:::{admonition} Which assumptions this derivation used
:class: model-assumption
Three, and only the first is about heat. (1) $\delta Q = 0$ throughout — adiabatic.
(2) The gas has a single pressure at every instant, so $P_{\mathrm{ext}} = P$ and $P\,dV$
means something — quasistatic. (3) The ideal-gas equation of state and a constant $f$.

Drop the second assumption and the derivation collapses at its first line, because $P$ has no
value to put there. That is the exemption the free expansion enjoys.
:::

### The four families, side by side

Each family is one constraint, and the first law does the rest.

| Process | Held fixed | $W_{\mathrm{on}}$ | $Q$ | $\Delta U$ |
|---|---|---|---|---|
| Isochoric | $V$ | $0$ | $C_V \Delta T$ | $C_V \Delta T$ |
| Isobaric | $P$ | $-P \Delta V$ | $C_P \Delta T$ | $C_V \Delta T$ |
| Isothermal | $T$ | $-N k_B T \ln(V_2/V_1)$ | $+N k_B T \ln(V_2/V_1)$ | $0$ |
| Adiabatic | $Q = 0$ | $\dfrac{P_2V_2 - P_1V_1}{\gamma - 1}$ | $0$ | $C_V \Delta T$ |

The last column is one expression, $C_V \Delta T$, in every row — the isotherm's zero is that
same expression with $\Delta T = 0$ — because $U$ is a state function and does not care which
row it is in. Everything that distinguishes the rows lives in the two path functions beside
it. Note in particular that $C_V$ appears in the isobaric row's $\Delta U$: the heat capacity
at constant *volume* is what converts a temperature change into an energy change, whatever the
process was.

### Irreversible processes: the work follows the external pressure

Now drop the quasistatic assumption. The gas is compressed by a weight slammed onto the
piston, or it expands into a vacuum. During the process the gas near the piston is at a
different pressure from the gas at the far end; there is no single $P$, no point in the
$P$–$V$ plane, and therefore no curve. What survives is the definition:

$$
W_{\mathrm{on}} = -\int P_{\mathrm{ext}}\, dV .
$$

For a constant external pressure this is just $-P_{\mathrm{ext}} (V_2 - V_1)$, whatever the
gas is doing internally.

**The free expansion.** Set $P_{\mathrm{ext}} = 0$: the gas expands into a vacuum, so nothing
pushes back on the piston — or, in the partition version, there is no piston at all. Then

$$
W_{\mathrm{on}} = 0,
\qquad Q = 0,
\qquad \Delta U = 0 .
$$

And for an ideal gas, whose internal energy depends on temperature alone,
$\Delta U = 0$ forces $\Delta T = 0$. The gas does not cool. It cannot: cooling would mean
losing energy, and there is no channel open for energy to leave through.

:::{admonition} Why "expanding gases cool" is true and irrelevant here
:class: approximation
Spray cans and rising air parcels cool because they *do work* on their surroundings while
insulated — case one of the puzzle. The cooling was never caused by the expansion; it was
caused by the paying. Remove the thing being pushed against and the expansion is free, in
both senses. For a real gas a small residual cooling survives, because pulling molecules
apart against their mutual attraction costs energy — that is the Joule–Thomson effect, and
it is a property of the interactions, not of the expansion.
:::

**Expansion against a fixed load.** Between the two extremes sits the case where the piston
carries a fixed weight, so $P_{\mathrm{ext}}$ is constant and non-zero. The gas expands until
its own pressure has fallen to meet the load, and

$$
T_2 = \frac{C_V T_1 + P_{\mathrm{ext}} V_1}{C_P} .
$$

Set the load so that the gas stops at exactly twice its volume, and this gives 225 K — between
the 189 K of the slow route and the 300 K of the free one.

:::{admonition} The three routes, in numbers
:class: numerical-observation
All three are adiabatic. All three start at 300 K and finish at twice the volume.

| Route | Final $T$ | $-W_{\mathrm{on}}$ in units of $P_1V_1$ |
|---|---|---|
| Slow (quasistatic adiabat) | 189.0 K | 0.555 |
| Against a fixed load | 225.0 K | 0.375 |
| Free expansion | 300.0 K | 0 |

The slow route delivers 48% more work than the loaded one and infinitely more than the free
one, for an identical change of volume. The ordering is not an accident of these numbers, and
the reason it can never reverse is the subject of module 7.
:::

**Now run it backwards, which is prediction 4.** Compress the same gas to *half* its volume,
insulated, two ways. Slowly, grain by grain: it ends at 476 K, having absorbed
$0.881\,P_1V_1$ of work. Or drop a block heavy enough to hold $P_{\mathrm{ext}} = 6P_1$ until
the piston stops — which is what "slamming" it means quantitatively — and it ends at 900 K,
having absorbed $3.000\,P_1V_1$.

The sudden compression costs **3.4 times the work** and leaves the gas 424 K hotter, for the
identical change of volume. Both facts are the same fact: $Q = 0$, so $\Delta U =
W_{\mathrm{on}}$, and work that went in had nowhere else to go. If you predicted that slamming
the piston was cheaper because it was quicker, this is the paragraph to reread.

So the slow route is the best of both worlds and it is not a coincidence: it extracts the most
work on the way out and costs the least on the way in. Every departure from quasistatic is
paid for, in the same direction, whichever way the piston is travelling.

(06-processes-verify)=
## Verify computationally

Six checks, each of which is also an automated test in the project's suite, so nothing on
this page can quietly rot.

**1. The closed forms.** Numerically integrating $-\int P\,dV$ along each family reproduces
the corresponding row of the table above to a relative error below $10^{-6}$, and the
trapezoid rule's error falls at second order as the sampling is refined.

**2. Mayer's relation, as a consistency check rather than an assumption.** Along an isobar
the work is computed from $-P\Delta V$ and the heat from $C_P \Delta T$, by two independent
formulae. The first law then has to close, and it does — which is a live test of
$C_P - C_V = N k_B$, since any other value would break it.

**3. The adiabatic invariants, and what that check is worth.** Sampling the adiabat and
evaluating $P V^{\gamma}$ and $T V^{\gamma-1}$ at every point gives two constants, flat to
machine precision along the whole curve. Be clear about how much of that is evidence: the
curve is *drawn* from $P V^{\gamma} = \text{constant}$, so the first invariant is true by
construction and only the second — that the temperature form follows through the equation of
state — is a result. A test that can only pass is worth naming as such rather than counting.

**4. The adiabat rebuilt from below, which is the check that is not circular.** Divide the
expansion into $n$ equal steps and let the gas expand irreversibly against a *constant* load
at each one, matched to its pressure at the start of that step. No step uses $P V^{\gamma}$
anywhere; each is nothing but the first law and the equation of state. One step lands at
100 K, sixteen at 185.6 K, and 256 within 0.11% of the quasistatic 189.0 K, with the error
falling as $1/n$.

That is the sand-grain argument made numerically, and it is the module's strongest single
verification: it shows the quasistatic adiabat is the *limit* of a sequence of irreversible
processes rather than a separate law, and it reaches the same 189 K by a route that never
assumes the answer.

**5. The ordering of the three routes.** The final temperatures come out 189.0 K, 225.0 K and
300.0 K, in that order, while the works run the other way. For the free expansion both
$W_{\mathrm{on}}$ and $Q$ are exactly zero — they are not computed, they are put in — and its
$\Delta U$ comes out within one part in $10^{15}$ of zero, which is as close to zero as a
float can get. Note that this is checked *fractionally*: these energies are around
$10^{-18}\,\mathrm{J}$, so an absolute tolerance would report every route's work as equal to
every other's.

**6. The free expansion from underneath.** This is the check worth running yourself.

:::{admonition} The free expansion, one level down
:class: numerical-observation
Take a box of particles from module 4's kinetic model, and widen it. That is all: no velocity
is touched, because removing a partition does not move a wall against a force. The kinetic
energy is therefore identical before and after, to machine precision, so the measured
temperature is unchanged — the microscopic statement of $\Delta U = 0$.

Then let the simulation run and measure the pressure. It has fallen by exactly the volume
ratio: the same particles, at the same speeds, now hit a given stretch of wall half as often.
$P$ halves, $T$ holds, and $PV$ is conserved. A model in which expansion *itself* cooled the
gas would have to make some velocity smaller, and there is nowhere in that code for it to
happen.
:::

:::{admonition} What the simulation has and has not established
:class: open-question
The microscopic run shows that *this* model's free expansion is isothermal, which is exactly
what an ideal gas should do — the particles never feel one another, so pulling them apart
costs nothing. It says nothing about real helium, whose atoms do attract, and which therefore
cools very slightly. Confirming an ideal-gas result in an ideal-gas simulation is a check on
the arithmetic, not evidence about nature. The experiment that decides is Joule's, and its
answer is "almost, but not exactly".
:::

(06-processes-transfer)=
## Transfer the idea

The quasistatic adiabat and its irreversible cousins are everywhere once you know the shape.

- **The atmosphere.** A parcel of air pushed up a mountainside expands as the pressure around
  it drops, does work on the air it displaces, and has no time to exchange heat — a
  quasistatic adiabat in the sky. The resulting lapse rate, near $10\ \mathrm{K/km}$ for dry
  air, follows from $T V^{\gamma-1}$ being constant and nothing else. Clouds form where the
  cooling reaches the dew point.
- **The diesel engine.** No spark plug. Air is compressed adiabatically by a factor of about
  20, which by $T V^{\gamma-1} = \text{constant}$ raises it past 700 K, and the fuel injected
  at that moment ignites on contact. The engine is a working demonstration that adiabatic
  compression heats.
- **A bicycle pump** gets hot at the barrel for the same reason, and a **spray can** gets cold
  for its mirror image. Both are the *work* channel, not the heat channel.
- **Throttling.** Push a gas slowly through a porous plug from high pressure to low. It is
  irreversible and adiabatic, and what is conserved is not $U$ but the enthalpy
  $H = U + PV$. For an ideal gas that still gives $\Delta T = 0$; for a real one it gives the
  cooling that liquefies air industrially. Enthalpy earns its own module (10).
- **Sound.** A sound wave compresses air far too fast for heat to diffuse between compression
  and rarefaction, so the compressions are adiabatic rather than isothermal. Newton assumed
  isothermal and got the speed of sound wrong by the factor $\sqrt{\gamma}$; Laplace supplied
  the $\gamma$ a century later.

:::{admonition} Quasistatic, reversible, and slow
:class: definition
**Quasistatic** means the system passes only through equilibrium states — slow compared with
its own relaxation time. **Reversible** means the process can be run backwards leaving *both*
system and surroundings unchanged. Every reversible process is quasistatic; the converse
fails as soon as friction is present, since a slow slide with friction passes through
equilibrium states and still cannot be undone. "Slow" alone means nothing without something
to compare against: nanoseconds is slow for a gas and instant for a glacier.
:::

(06-processes-quiz)=
## Check your understanding

```{include} ../_generated/quiz-06-processes.md
```

Exam-style problems for this module are collected in
[the problem set](06-processes-problems.md).

(06-processes-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A classmate says: "The free expansion doesn't cool the gas because it happens too fast for
   the temperature to change." Explain what is wrong with this, and give the correct reason.
2. Why is $C_P$ larger than $C_V$? Answer without writing an equation, in terms of what the
   heat is spent on.
3. Both the isothermal and the free expansion take an ideal gas from $V$ to $2V$ with
   $\Delta T = 0$. Describe every way in which they nonetheless differ.
4. A gas is compressed to half its volume, once slowly and once by slamming the piston. Both
   are insulated. Which ends hotter, and why does that not violate energy conservation?

(06-processes-advanced)=
## Advanced: one family, four members

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Polytropes.** The four families are not four separate objects. They are four values of one
parameter in

$$
P V^{n} = \text{constant},
$$

with $n = 0$ isobaric, $n = 1$ isothermal, $n = \gamma$ adiabatic, and $n \to \infty$
isochoric (the curve becomes vertical). The work along any of them is

$$
W_{\mathrm{on}} = \frac{P_2 V_2 - P_1 V_1}{n - 1},
$$

which reproduces every row of the table above except the isotherm — and the isotherm is not
an oversight but a genuine logarithm, since $\int dV/V$ is not a power. Evaluating the
rational form at $n = 1 + 10^{-9}$ to "get around" the singularity is how a plausible wrong
number gets produced; the course's implementation branches on $n = 1$ instead.

A real process with heat leaking through an imperfect insulator sits at some $n$ between 1
and $\gamma$, which is exactly how engineers fit measured compressor data.

**Why the free expansion has no path.** During it the gas is not in equilibrium, so it has no
pressure and no temperature — not "a rapidly changing one", but none at all, because those
quantities are defined for equilibrium states. The $P$–$V$ plane is a plane of *states*, and
a process that leaves the set of states cannot be a curve in it. Drawing a dashed line between
the endpoints is a common textbook habit and it is a lie; the honest picture has two dots and
nothing between them.

**Where the missing work went.** The three routes started identically and ended at the same
volume, yet delivered $0.555$, $0.375$ and $0$ of $P_1V_1$. Energy is conserved in all three —
the gas that did less work simply kept more internal energy. So no conservation law forbids
the free expansion; something else does. What distinguishes them is that only the slow route
can be run backwards without leaving a trace on the universe, and the quantity that measures
the trace is the entropy. All three have the same $\Delta U$; they have different $\Delta S$,
with the quasistatic adiabat alone at $\Delta S = 0$. That is where module 8's counting
argument and module 7's engines both begin.

**The Joule coefficient.** The statement "free expansion does not change $T$" is the ideal-gas
value of

$$
\left(\frac{\partial T}{\partial V}\right)_U ,
$$

which vanishes precisely when $U$ is independent of volume. For a van der Waals gas it is
negative and small, so a real free expansion cools a little. Joule's original 1845 experiment
could not resolve it — his water bath was too large — and the effect was found only when he
and Thomson switched to throttling, which amplifies it.
