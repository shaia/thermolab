---
title: The second law and heat engines
short_title: 07 · Second law
module: 07-second-law
objectives:
  - id: OBJ-07-1
    text: State the Kelvin and Clausius forms of the second law and show that violating either one lets you violate the other.
  - id: OBJ-07-2
    text: Explain why a cyclic engine is forced to reject heat, and why the restriction is about cycles rather than about any single process.
  - id: OBJ-07-3
    text: Prove Carnot's theorem, and identify the step at which the working substance drops out of the argument.
  - id: OBJ-07-4
    text: Compute the Carnot efficiency 1 - T_c/T_h and use it as a bound on a real engine rather than as a prediction of its performance.
  - id: OBJ-07-5
    text: Analyse refrigerators and heat pumps, compute a coefficient of performance, and explain why a value above 1 violates nothing.
  - id: OBJ-07-6
    text: Explain how a reversible engine's heat ratio defines an absolute temperature scale that refers to no material at all.
  - id: OBJ-07-7
    text: Locate where an engine's lost work goes when its thermal contact is imperfect, and quantify it as entropy produced.
---

# The second law and heat engines

(07-second-law-puzzle)=
## The puzzle: the ocean is enormous and useless

The Atlantic holds something like $10^{24}\ \mathrm{J}$ of thermal energy. A ship that cooled
the water it passed through by a single kelvin, and turned that energy into forward motion,
would cross the ocean on the ocean itself and arrive with the sea imperceptibly cooler. No
fuel, no emissions, nothing consumed that anyone would miss.

Nothing in the first law forbids this. Energy would be conserved exactly: heat leaves the
water, work appears at the propeller, the books balance to the last joule. The engine is not a
perpetual-motion machine in the old sense — it is not creating energy, only borrowing some
that is already there and unimaginably abundant.

And it cannot be built. Not "has not been built yet", and not "is very hard to build": there
is a theorem against it, and the theorem is what this module is about.

:::{important} The question
If energy is conserved either way, what exactly is wrong with the ocean-powered ship? What
distinguishes the energy in warm seawater from the energy in a tank of diesel, when both are
just energy?
:::

The answer will not mention efficiency, engineering, or friction. It will turn out that a
heat engine needs *two* temperatures, that having only one is the entire defect, and that this
single requirement fixes the best possible performance of every engine that will ever be
built — from a number that knows nothing about what the engine is made of.

(07-second-law-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* reading on. Write them down.

1. An engine takes in $1000\ \mathrm{J}$ of heat from a furnace each cycle and delivers
   $400\ \mathrm{J}$ of work. Where is the other $600\ \mathrm{J}$, and could a better design
   recover some of it?
2. Two engines run between the same furnace and the same river. One uses steam, the other
   helium. Which can be made more efficient?
3. A refrigerator moves $300\ \mathrm{J}$ of heat out of its cold interior for every
   $100\ \mathrm{J}$ of electricity it draws. Is something wrong with that number?
4. Your kitchen refrigerator lowers the entropy of the food inside it. Does it violate the
   second law?
5. A power station's steam is at $550\,{}^\circ\mathrm{C}$ and its cooling river at
   $20\,{}^\circ\mathrm{C}$. Estimate the best efficiency it could possibly have. Now guess
   what it actually achieves.

:::{note} Why we ask first
Questions 2 and 3 are where most intuitions break, and in opposite directions: people expect
the substance to matter when it provably does not, and expect a "300 out for 100 in" machine
to be impossible when it is ordinary. Question 4 catches nearly everyone once.
:::

(07-second-law-explore)=
## Explore the model

A heat engine is a working substance taken around a **closed loop** — back to exactly the
state it started in — while touching a hot reservoir and a cold one. Closure is not a detail.
It is what makes the internal energy change vanish over a cycle, so that every joule of work
delivered has to have arrived as heat, and it is why the engine cannot simply keep some energy
back and call it output.

Here is the Carnot cycle running, with its energy ledger filling in beside it.

:::{figure} ../media/second-law-carnot-cycle.mp4
:alt: A Carnot cycle traced in the pressure-volume plane, beside three bars showing heat absorbed from the hot reservoir, work delivered, and heat dumped to the cold reservoir.
:width: 100%

The Carnot cycle in the $P$–$V$ plane: isothermal expansion in contact with the hot reservoir
(red), adiabatic expansion (grey), isothermal compression against the cold reservoir (blue),
adiabatic compression back to the start (grey). The shading appears only on the closing
stroke, because the area is the work delivered only once the loop is actually closed.

Beside it, three running totals: heat drawn from the hot reservoir, net work delivered so far,
and heat dumped into the cold one. Watch the middle bar overshoot — the two expansions deliver
far more work than the cycle nets, and the two compressions hand most of it back. What is left
when the loop closes is the enclosed area, and by then the third bar has risen too. It never
returns to zero, and no rearrangement of the other strokes can make it.
:::

Now watch what happens when the engine is asked to run between reservoirs whose temperatures
get closer together, and when its thermal contact is made deliberately sloppy:

:::{figure} ../media/second-law-efficiency-bound.mp4
:alt: Measured efficiencies of many differently proportioned engines plotted against the Carnot bound; every point lies on or below the curve, and points from engines with poor thermal contact lie further below.
:width: 100%

Every point is one engine, built with a randomly chosen size, expansion ratio and quality of
thermal contact, plotted against the curve $1 - T_c/T_h$. Engines with perfect contact
(dark) sit exactly on the curve; every degree of temperature gap they need in order to move
heat at a finite rate (lighter) pushes them below it. Nothing ever lands above. The dashed
curve is the maximum-power efficiency $1 - \sqrt{T_c/T_h}$, which is where real plants live.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a fixed amount of ideal gas ($N$ particles, $f$ quadratic degrees of freedom) taken around a closed loop between heat reservoirs at fixed temperatures.
- **Dynamics:** quasistatic strokes — isothermal, adiabatic or isochoric — joined end to end into a closed curve in the $P$–$V$ plane; the reservoir each stroke touches is recorded separately from the gas's own temperature.
- **Boundary:** a frictionless piston, and a wall switched between diathermal (touching one named reservoir) and adiabatic.
- **Ensemble:** not applicable — this is thermodynamics; nothing here counts microstates.
- **Ignored:** friction, the piston's mass, gas non-ideality, heat leaking through the adiabatic strokes, the time a stroke takes, and the work spent moving the working substance between reservoirs.
- **Valid when:** every stroke is slow compared with the gas's relaxation time, and each reservoir is large enough that absorbing its heat leaves its own temperature unchanged.
- **Failure modes:** finite-rate operation, where heat will not cross a vanishing temperature difference; regenerators, which recycle heat internally and break two-reservoir bookkeeping; and any working substance near condensation, where the ideal-gas strokes are simply wrong.
:::

:::{admonition} A reservoir is an idealisation, and a load-bearing one
:class: model-assumption
A **heat reservoir** is a body so large that it can absorb or supply the cycle's heat without
its own temperature moving. Every statement below is about reservoirs at *fixed* temperature,
and that is what lets us write one $T_h$ and one $T_c$ for the whole cycle. A real furnace
cools as you draw from it and a real river warms as you dump into it; treating them as
reservoirs is excellent for one cycle and wrong for a season.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 07 — the second law and heat engines](/lite/lab/index.html?path=en/labs/07-second-law.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/07-second-law.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Try to design an engine that beats $1 - T_c/T_h$. Change the gas, the size, the shape of
  the loop. Watch the bound refuse to move.
- Shrink the temperature gap between the reservoirs and watch the efficiency collapse.
- Run the cycle backwards and read off what the machine has become.

(07-second-law-derive)=
## Derive the result

**System and boundary.** The working substance, taken around a closed cycle. The reservoirs
are outside it, and we keep separate books for what they lose and gain.

**Sign convention.** The course convention $\mathrm{d}U = \dbar Q + \dbar \Won$ holds
throughout, with $\dbar Q$ positive into the system. Engines are conventionally rated by the
work they *deliver*, and one clearly marked block below converts to it and converts back.

### What the second law actually says

Unlike the first law, the second law is not an equation. It is a statement about what cannot
happen, and it comes in two historical forms that sound unrelated.

:::{admonition} The Kelvin statement
:class: empirical-law
No cyclic process can have as its *sole* result the complete conversion of heat drawn from a
single reservoir into work.
:::

:::{admonition} The Clausius statement
:class: empirical-law
No cyclic process can have as its *sole* result the transfer of heat from a colder body to a
hotter one.
:::

Both are empirical laws: they summarise that nobody has ever observed otherwise, and they are
not derived from mechanics. Two words in them do all the work. **Cyclic** means the machine
returns to its starting state, so that it can do the same thing again — a single expansion can
convert heat entirely into work, and an isothermal expansion does exactly that, but it leaves
the gas bigger, so it is not a cycle and cannot be repeated. **Sole result** means nothing
else is left changed anywhere; a refrigerator moves heat from cold to hot every day, but not
as its sole result, because it also consumes electricity.

That already answers the opening puzzle. The ocean-powered ship is a cyclic engine drawing
heat from one reservoir and producing work with no other change — precisely the Kelvin
statement's forbidden machine. What the ship lacks is not efficiency but a *second*, colder
reservoir to dump into.

### The two statements are the same statement

They look like claims about different machines. They are not: each one can be used to build a
violation of the other, so either both hold or neither does.

**Suppose Clausius fails.** Then some device moves heat $Q_c$ from the cold body to the hot
one with no other effect. Run an ordinary engine alongside it: the engine draws $Q_h$ from the
hot body, delivers work $W$, and dumps exactly $Q_c$ into the cold one. Now look at the pair
as a single machine. The cold body received $Q_c$ from the engine and gave up $Q_c$ to the
magic device — unchanged. What is left is that the hot body lost $Q_h - Q_c$ and work $W$
appeared. A single reservoir, fully converted into work: Kelvin fails too.

**Suppose Kelvin fails.** Then some device draws $Q$ from the hot body and turns all of it
into work. Feed that work to an ordinary refrigerator, which uses it to move $Q_c$ from the
cold body to the hot one. Together: the cold body lost $Q_c$; the hot body gave up $Q$ and
received $Q + Q_c$, for a net gain of $Q_c$; and no work is left over. Heat has moved from
cold to hot as the sole result: Clausius fails too.

:::{admonition} What "equivalent" buys you
:class: theorem
The two statements are logically equivalent, so we may use whichever is more convenient in a
given argument and call the result a consequence of "the second law". The proof of Carnot's
theorem below uses the Clausius form, because the machine it constructs is a heat pump.
:::

### Carnot's theorem

Now the central result, and it is remarkable for what it does not mention.

:::{admonition} Carnot's theorem
:class: theorem
No heat engine operating between two given reservoirs can be more efficient than a reversible
engine operating between the same two. All reversible engines between the same two reservoirs
have the *same* efficiency.
:::

Define efficiency as the fraction of absorbed heat that leaves as work.

<!-- sign-convention-exception -->
:::{admonition} The one place this course uses work-done-by
:class: definition
Throughout the course, $\Won$ is the work done *on* the system, so a gas that expands has
$\Won < 0$. An engine is rated by what it delivers, so for this module only we define

$$
W_{\mathrm{out}} \equiv -\Won^{\text{(net, per cycle)}} ,
\qquad
\eta \equiv \frac{W_{\mathrm{out}}}{Q_h} ,
$$

where $Q_h > 0$ is the heat absorbed from the hot reservoir per cycle. Around a closed cycle
$\Delta U = 0$, so the first law gives $W_{\mathrm{out}} = Q_h - Q_c$ with $Q_c > 0$ the heat
dumped to the cold reservoir, and

$$
\eta = 1 - \frac{Q_c}{Q_h} .
$$

That is the whole conversion. Every other equation in this module, and every quantity in
`thermolab.engines` other than `work_output`, carries the project sign.
:::
<!-- /sign-convention-exception -->

**The proof.** Suppose an engine $X$ had efficiency $\eta_X > \eta_R$, where $R$ is reversible
and runs between the same two reservoirs. Because $R$ is reversible, we can run it backwards
as a heat pump. Size the two machines so that the work $X$ delivers is exactly the work $R$
consumes, and connect them: $X$ drives $R$, and no work enters or leaves the combination.

Per cycle, $X$ draws $Q_h^X = W/\eta_X$ from the hot reservoir, and $R$ running backwards
returns $Q_h^R = W/\eta_R$ to it. Since $\eta_X > \eta_R$, we have $Q_h^X < Q_h^R$: the hot
reservoir ends each cycle with a net *gain* of $Q_h^R - Q_h^X > 0$. Energy is conserved, no
work crossed the boundary, so that energy came from the cold reservoir.

The combined machine's sole result is heat moved from cold to hot. Clausius forbids it, so no
such $X$ exists. And applying the argument with two reversible engines in each role gives
$\eta_{R_1} \le \eta_{R_2}$ and $\eta_{R_2} \le \eta_{R_1}$, hence equality. $\blacksquare$

:::{admonition} The step where the working substance vanishes
:class: model-assumption
Read back through the proof and notice what never appeared: what $X$ or $R$ is made of, how
big they are, what shape their cycles trace. The argument uses only that $X$ produces work
from two reservoirs and that $R$ can be reversed. So the maximum efficiency cannot depend on
the working substance — it can depend on nothing but the two temperatures. This is the answer
to prediction 2, and it is the part of the theorem that is genuinely surprising.
:::

### Putting a number on it

Carnot's theorem says the reversible efficiency is some universal function of the two
temperatures. To find the function we only need to evaluate it *once*, for any convenient
reversible engine — and the ideal gas is convenient.

Take the Carnot cycle: isothermal expansion from $V_1$ to $V_2$ at $T_h$; adiabatic expansion
to $T_c$; isothermal compression at $T_c$; adiabatic compression back to the start.

On the hot isotherm $\Delta U = 0$, so all the absorbed heat leaves as work:

$$
Q_h = N \kB T_h \ln\!\frac{V_2}{V_1} .
$$

On the cold isotherm, the same argument with the gas being compressed:

$$
Q_c = N \kB T_c \ln\!\frac{V_3}{V_4} .
$$

Now the two adiabats do the essential work. Along an adiabat $T V^{\gamma - 1}$ is constant,
and both adiabats connect the same pair of temperatures, so

$$
\frac{V_3}{V_2} = \left(\frac{T_h}{T_c}\right)^{1/(\gamma-1)} = \frac{V_4}{V_1}
\qquad\Longrightarrow\qquad
\frac{V_3}{V_4} = \frac{V_2}{V_1} .
$$

The two logarithms are therefore equal, and they cancel:

$$
\frac{Q_c}{Q_h} = \frac{T_c}{T_h}
\qquad\Longrightarrow\qquad
\boxed{\; \eta_{\text{Carnot}} = 1 - \frac{T_c}{T_h} \;}
$$

:::{admonition} What has and has not been shown
:class: approximation
The *bound* is general — Carnot's theorem established that without touching a working
substance. The *evaluation* used an ideal gas, quasistatic strokes and $T V^{\gamma-1}$
constant. Those assumptions fixed the function's form; they do not restrict what it applies
to. A steam plant is bounded by the same number even though steam is nothing like an ideal
gas.
:::

Two consequences fall straight out. Since $T_c > 0$ always, $Q_c > 0$ always: **a cyclic
engine must reject heat**, and the $600\ \mathrm{J}$ of prediction 1 is not recoverable
waste but a structural requirement. And $\eta \to 1$ would need $T_c \to 0$ or
$T_h \to \infty$, neither of which is available.

### Temperature without a thermometer

Here is a consequence worth pausing on. The ratio $Q_c/Q_h$ for a reversible engine depends
on nothing but the two reservoirs, and equals $T_c/T_h$. So that ratio can be used to
*define* temperature.

:::{admonition} Thermodynamic temperature
:class: definition
Fix one reference reservoir. For any other, run a reversible engine between the two and
measure the ratio of the heats exchanged; that ratio *is* the ratio of their absolute
temperatures. Fixing one point — the triple point of water, historically — fixes the scale.
:::

This is Kelvin's scale, and its virtue is that it mentions no substance at all: not the
expansion of mercury, not the pressure of a dilute gas, nothing that could behave differently
in a different material. Every empirical thermometer is a stand-in for this definition.

### Running the cycle backwards

Every stroke of a reversible cycle can be reversed — that is what the word means — so the
Carnot engine read right to left is a Carnot refrigerator. Work goes in, heat $Q_c$ comes out
of the cold reservoir, and $Q_h = Q_c + W$ goes into the hot one. Nothing new needs deriving;
the same cancelling logarithms give

$$
\mathrm{COP}_{\text{fridge}} = \frac{Q_c}{W} = \frac{T_c}{T_h - T_c} ,
\qquad
\mathrm{COP}_{\text{pump}} = \frac{Q_h}{W} = \frac{T_h}{T_h - T_c} .
$$

:::{admonition} Why a coefficient above 1 is unremarkable
:class: definition
These are *not* efficiencies and are not bounded by 1. Nothing is being converted: energy is
being **moved**, and the work is what it costs to move it uphill. A kitchen refrigerator with
$T_c = 275\ \mathrm{K}$ and $T_h = 300\ \mathrm{K}$ has a ceiling of $275/25 = 11$. That is
the answer to prediction 3 — a value of 3 is not suspicious, it is mediocre. It is also why
heat pumps heat buildings for a fraction of what a resistive heater costs: the pump moves
heat that is already outside, while the heater manufactures it.
:::

Note the exact identity $\mathrm{COP}_{\text{pump}} = \mathrm{COP}_{\text{fridge}} + 1$. It
is energy conservation and nothing more: everything the machine lifts from the cold side, plus
the work it consumed, arrives on the hot side.

(07-second-law-verify)=
## Verify computationally

The derivation above is a chain of exact statements, so the laboratory's job is to check that
the chain was assembled correctly — and to make the bound something you have tried and failed
to break rather than something you were told. Each check below is also a test in the project's
suite.

**1. The cycle closes.** Each of the four strokes computes its endpoint from its own closed
form. Coming back to the starting $(P, V, T)$ is four independent formulae agreeing, to
within $10^{-12}$ of the internal energy.

**2. The first law closes around the loop.** $Q_{\text{net}} + \Won^{\text{net}} = \Delta U = 0$
for every cycle built here, engine and refrigerator alike.

**3. The efficiency comes out at $1 - T_c/T_h$.** Nothing in the construction puts that number
in — the strokes know only volumes and temperatures. Recovering it is the check.

**4. Carnot's theorem, as an experiment.**

:::{admonition} The bound refuses to move
:class: numerical-observation
Build the cycle with a monatomic gas, a diatomic one and a polyatomic one; with expansion
ratios from 1.2 to 8; with particle numbers from 10 to $10^5$. Between $600\ \mathrm{K}$ and
$300\ \mathrm{K}$, every one of them returns $\eta = 0.500000000000$, to twelve figures. The
heats themselves scale linearly with $N$ over four decades — the engine really is bigger — and
their *ratio* does not move at all.
:::

**5. Imperfect contact costs exactly what it produces.** Give the engine a gas that sits
$\Delta T$ below the hot reservoir and $\Delta T$ above the cold one — which is what it takes
to make heat flow at a finite rate — and two numbers move together:

:::{admonition} Lost work and produced entropy are one quantity
:class: numerical-observation
With reservoirs at $600\ \mathrm{K}$ and $300\ \mathrm{K}$ and a gap of $10\ \mathrm{K}$ at
each end, the efficiency falls from $0.5000$ to $0.4746$, and the cycle's
$\oint \dbar Q / T_{\text{res}}$ turns negative for the first time. At a gap of
$100\ \mathrm{K}$ the efficiency is $0.2000$ and the loop integral is negative by $0.6$ of the
entropy the hot reservoir gave up. Shrink the gaps and the shortfall vanishes linearly: halve
the gap, halve the entropy produced.
:::

:::{admonition} What a numerical sweep can and cannot establish
:class: open-question
Thirty-two randomly proportioned engines all respecting the bound is not a proof that it
cannot be beaten — no finite sample could be. The proof is Carnot's theorem, and it is on this
page. What the sweep does is different and still worth having: it is a *falsification test* of
the code and of your own attempts to design around the bound. If you can make the simulated
engine exceed $1 - T_c/T_h$, either the code is wrong or the derivation is; you have found
something either way.
:::

(07-second-law-transfer)=
## Transfer the idea

The pattern — a conversion that energy conservation permits but a second, independent law
forbids — reaches well past engines.

- **Power stations.** Steam at $550\,{}^\circ\mathrm{C}$ against a river at
  $20\,{}^\circ\mathrm{C}$ gives $\eta_{\text{Carnot}} = 1 - 293/823 = 0.64$. Real plants
  reach about $0.40$. That is not a $24$-point engineering failure: the maximum-*power*
  efficiency $1 - \sqrt{T_c/T_h} = 0.40$ lands almost exactly on it, because a plant optimised
  for output rather than for thermodynamic virtue is solving a different problem.
- **Why aircraft run their turbines hot.** Every gain in $\eta$ has to come from raising
  $T_h$, since $T_c$ is the sky and is not negotiable. The history of the jet engine is very
  largely the history of materials that survive a hotter turbine inlet.
- **Heat pumps for buildings.** A COP of 4 means a kilowatt of electricity delivering four
  kilowatts of heating, which sounds like a violation and is not. It is the Clausius statement
  respected: heat moves uphill, but not as the sole result.
- **Biology.** Muscles are not heat engines — a cell is essentially isothermal, so a heat
  engine inside it would have $T_h = T_c$ and could do nothing at all. Life runs on chemical
  free energy instead, which is why module 10's potentials matter more to biochemistry than
  this module does.
- **Information.** Szilard's engine extracts $\kB T \ln 2$ of work per bit of information
  about a molecule's position, and Landauer's principle charges the same amount to erase the
  bit. The books balance only when information is included, which is one of the deepest places
  this law reaches.

:::{admonition} Available energy is not energy
:class: definition
The lesson underneath all of these is that a joule's *usefulness* depends on the temperature
it sits at. A joule in a $1000\ \mathrm{K}$ furnace can mostly become work; the same joule in
tepid seawater essentially cannot. Energy is conserved, but the capacity to do work with it is
not — and that quantity, not energy, is what fuel actually sells you.
:::

(07-second-law-quiz)=
## Check your understanding

```{include} ../_generated/quiz-07-second-law.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](07-second-law-problems.md).

(07-second-law-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you here.

1. A student says: "The second law says engines are inefficient because of friction and heat
   losses." Explain precisely what is wrong with this, and give a version that is correct.
2. Explain to someone who knows the first law why the ocean-powered ship fails, without using
   the word entropy.
3. Why can the maximum efficiency not depend on what the engine is made of? Point to the step
   in Carnot's argument that makes this inevitable.
4. Your refrigerator lowers the entropy of the food inside it. Say exactly why this is not a
   violation, and where the compensating increase happens.
5. A colleague proposes doubling a power plant's efficiency by improving its turbine blades.
   Under what circumstances could they be right, and what would you need to measure to find
   out?

(07-second-law-advanced)=
## Advanced: the Clausius inequality, and the bridge to counting

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It is here because it connects this
module's bound to the entropy of [module 08](../statistical-mechanics/08-multiplicity.md),
which approaches the same quantity from an entirely different direction.
:::

**From the bound to an inequality.** For a reversible cycle between two reservoirs,
$Q_c/Q_h = T_c/T_h$. Restoring signs — heat in positive, heat out negative — that is

$$
\frac{Q_h}{T_h} + \frac{Q_{c,\,\text{signed}}}{T_c} = 0 .
$$

For an irreversible engine, Carnot's theorem gives $\eta < 1 - T_c/T_h$, and the same
rearrangement turns the equality into a strict inequality. Chaining many reservoirs and taking
the limit gives the general statement:

$$
\oint \frac{\dbar Q}{T_{\text{res}}} \le 0 ,
$$

with equality exactly for a reversible cycle. Note which temperature divides: the
**reservoir's**, not the gas's. Dividing by the gas's own temperature gives zero around any
loop whatever, reversible or not, and proves nothing — the entire content of the inequality
lives in the gap between the two temperatures.

**From the inequality to a state function.** If the loop integral vanishes for every
reversible cycle, then $\int \dbar Q_{\text{rev}}/T$ between two states is independent of the
path taken, which is precisely the condition for a state function to exist. Define it:

$$
\mathrm{d}S = \frac{\dbar Q_{\text{rev}}}{T} .
$$

The inexact differential $\dbar Q$ has been turned into an exact one by dividing by $T$ —
$1/T$ is an *integrating factor* for heat, in the sense [the conventions
page](../conventions.md) sets out. This is the thermodynamic definition of entropy, and it was
reached without a single mention of atoms.

**The bridge.** Module 08 defines entropy completely differently, as
$S = \kB \ln \Omega$ — a count of microstates, with no engine anywhere in sight. The two
definitions agree, up to the additive constant that a counting argument cannot fix and a
Clausius integral never needed. The agreement is not obvious and it is not a coincidence; it
is why the same word is used for both, and why a bound derived from steam engines turns out to
govern the mixing of gases and the folding of proteins.

:::{admonition} What is still open here
:class: open-question
Reversing every molecular velocity in an engine would run it backwards, which means the
mechanics underneath has no preferred direction while the second law plainly does. Module 08
resolves this as a statement about counting, not about dynamics. What remains genuinely open
is *why the universe started in a low-entropy state at all* — the second law's arrow is
inherited from that initial condition, and thermodynamics does not explain it.
:::

**Endoreversible engines.** The engine with temperature gaps is worth a second look. Let heat
flow at a rate proportional to the temperature difference, and optimise the *power* rather
than the efficiency; the optimum sits at

$$
\eta_{\text{CA}} = 1 - \sqrt{\frac{T_c}{T_h}} ,
$$

the Curzon–Ahlborn efficiency. It is not a bound — it is the answer to a different question —
but its agreement with real plants is striking, and it makes a point worth carrying: the
Carnot bound is attained only by an engine that takes infinitely long per cycle and therefore
delivers zero power. Every real design trades efficiency for power on purpose.
