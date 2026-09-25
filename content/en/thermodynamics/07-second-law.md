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
  - id: OBJ-07-8
    text: Identify the common sources of irreversibility — heat crossing a finite temperature difference, friction, unrestrained expansion, mixing — and use the Kelvin or Clausius statement to show why none of them can be undone without trace.
  - id: OBJ-07-9
    text: Derive the Clausius inequality, show that it makes the integral of delta-Q_rev/T path-independent, and use the resulting state function S to compute entropy changes of an ideal gas, a reservoir and a body of constant heat capacity.
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
6. A process is carried out infinitely slowly, so that everything is in equilibrium at every
   instant. Is it therefore reversible — could it be undone leaving no trace at all?

:::{note} Why we ask first
Questions 2 and 3 are where most intuitions break, and in opposite directions: people expect
the substance to matter when it provably does not, and expect a "300 out for 100 in" machine
to be impossible when it is ordinary. Question 4 catches nearly everyone once. Question 6 is
the one the whole derivation turns on, and every answer is collected at the end of the
module.
:::

(07-second-law-explore)=
## Explore the model

A heat engine is a working substance taken around a **closed loop** — back to exactly the
state it started in — while touching a hot reservoir and a cold one. Closure is not a detail.
It is what makes the internal energy change vanish over a cycle, so that every joule of work
delivered has to have arrived as heat, and it is why the engine cannot simply keep some energy
back and call it output.

Every machine in this module is drawn the same way:

:::{figure} ../media/second-law-machines.png
:alt: Two energy-flow diagrams. Left, an engine takes heat Q_h from a hot reservoir, delivers work W, and passes heat Q_c to a cold reservoir. Right, the same machine run backwards takes in work W, lifts heat Q_c out of the cold reservoir and delivers heat Q_h to the hot one.
:width: 80%

Reservoirs are the long bars — red at $T_h$, blue at $T_c$ — and the circle is the working
substance, which goes round a closed cycle. (a) An engine: heat $Q_h$ in from the hot side,
work $W$ out, heat $Q_c$ down to the cold side. (b) The same machine run backwards: work in,
heat lifted out of the cold side and delivered to the hot one. It is a refrigerator if what you
want is the cold side, and a heat pump if what you want is the hot side. The labels are sizes;
the arrows say which way the energy goes.
:::

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
curve is the maximum-power efficiency $1 - \sqrt{T_c/T_h}$, which is where real plants live; the
advanced section derives it.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a fixed amount of ideal gas ($N$ particles, $f$ quadratic degrees of freedom) taken around a closed loop between heat reservoirs at fixed temperatures.
- **Dynamics:** quasistatic strokes — isothermal, adiabatic or isochoric — joined end to end into a closed curve in the $P$–$V$ plane, plus, for the Clausius-sum experiments, irreversible strokes known only by their end states, such as a free expansion; the reservoir each stroke touches is recorded separately from the gas's own temperature.
- **Boundary:** a frictionless piston, and a wall switched between diathermal (touching one named reservoir) and adiabatic.
- **Ensemble:** not applicable — this is thermodynamics; nothing here counts microstates.
- **Ignored:** friction, the piston's mass, gas non-ideality, heat leaking through the adiabatic strokes, the time a stroke takes, and the work spent moving the working substance between reservoirs.
- **Valid when:** every quasistatic stroke is slow compared with the gas's relaxation time, every irreversible one starts and ends in equilibrium, and each reservoir is large enough that absorbing its heat leaves its own temperature unchanged.
- **Failure modes:** finite-rate operation, where heat will not cross a vanishing temperature difference; regenerators, which store heat inside the engine between strokes — a Stirling engine with a perfect one reaches the Carnot bound on constant-volume strokes, and this model has no stroke that can represent the store; and any working substance near condensation, where the ideal-gas strokes are simply wrong.
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

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Try to design an engine that beats $1 - T_c/T_h$. Change the gas, the size, the shape of
  the loop. Watch the bound refuse to move.
- Shrink the temperature gap between the reservoirs and watch the efficiency collapse.
- Run the cycle backwards and read off what the machine has become.
- Put a free expansion into a cycle and watch the loop sum of heat over reservoir temperature
  turn negative. What that sum is will be the last idea of the derivation.

(07-second-law-derive)=
## Derive the result

**System and boundary.** The working substance, taken around a closed cycle. The reservoirs
are outside it, and we keep separate books for what they lose and gain.

**Independent variables and constraint.** The two reservoir temperatures $T_h$ and $T_c$,
which nothing in the cycle changes, and the gas's own volume and temperature, which the cycle
drives round the loop; every other state quantity follows from those through the equation of
state. The one constraint is closure: the gas ends each cycle in the state it began, so its
internal energy — and, once it has been defined, its entropy — returns to its starting value.
The argument is thermodynamic throughout: no microstate is counted anywhere in this section.

**Sign convention.** The course convention $\mathrm{d}U = \dbar Q + \dbar \Won$ holds
throughout, with $\dbar Q$ positive into the system. Engines are conventionally rated by the
work they *deliver*, and one clearly marked block below converts to it and converts back.

**Route.** The derivation runs in a straight line, and each step uses only the ones before it:
the second law as two prohibitions; what "reversible" means and why friction and heat leaks
are not; why an engine needs two reservoirs; Carnot's theorem and the number it puts on every
engine; and finally the Clausius inequality, which turns the whole story into a new function
of state, the entropy.

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
violation of the other, so either both hold or neither does. The argument is easiest to follow
as a picture.

:::{figure} ../media/second-law-equivalence.png
:alt: Two rows of energy-flow diagrams. Top, an impossible machine C lifting heat Q_c from cold to hot, beside an engine E that dumps the same Q_c, equals a single impossible machine turning Q_h minus Q_c from the hot reservoir entirely into work W. Bottom, an impossible machine K turning heat Q entirely into work W, driving a refrigerator F that lifts Q_c, equals a single impossible machine moving Q_c from cold to hot with no work.
:width: 90%

The equivalence, as two machines glued together. Dashed circles are the machines that cannot
exist; the dotted outline marks the pair being read as a single machine. (a) A Clausius
violator $C$ beside an ordinary engine $E$ sized to dump exactly the heat $C$ lifts: the cold
reservoir nets nothing, and what remains takes $Q_h - Q_c$ from one reservoir and turns all of
it into work — a Kelvin violator. (b) A Kelvin violator $K$ driving an ordinary refrigerator
$F$: no work leaves the pair, and $Q_c$ climbs from cold to hot on its own — a Clausius
violator.
:::

**Suppose Clausius fails** — panel (a).

1. Some device $C$ moves heat $Q_c$ from the cold body to the hot one with no other effect.
2. Run an ordinary engine $E$ alongside it: the engine draws $Q_h$ from the hot body, delivers
   work $W$, and is sized to dump exactly $Q_c$ into the cold one.
3. Now look at the pair as a single machine. The cold body received $Q_c$ from the engine and
   gave up $Q_c$ to the magic device — unchanged.
4. What is left is that the hot body lost $Q_h - Q_c$ and work $W$ appeared. A single
   reservoir, fully converted into work: Kelvin fails too.

**Suppose Kelvin fails** — panel (b).

1. Some device $K$ draws $Q$ from the hot body and turns all of it into work.
2. Feed that work to an ordinary refrigerator $F$, which uses it to move $Q_c$ from the cold
   body to the hot one.
3. Together: the cold body lost $Q_c$; the hot body gave up $Q$ and received $Q + Q_c$, for a
   net gain of $Q_c$; and no work is left over.
4. Heat has moved from cold to hot as the sole result: Clausius fails too.

:::{admonition} What "equivalent" buys you
:class: theorem
The two statements are logically equivalent, so we may use whichever is more convenient in a
given argument and call the result a consequence of "the second law". The proof of Carnot's
theorem below uses the Clausius form, because the machine it constructs is a heat pump; the
arguments about irreversibility and the Clausius inequality use the Kelvin form.
:::

(07-second-law-reversibility)=
### Reversible and irreversible processes

Carnot's theorem, coming next but one, compares every engine with a *reversible* one, so the
word has to be sharp before it is used. [Module 06](06-processes.md#06-processes-transfer)
defined it; the second law is what gives the definition teeth.

:::{admonition} Reversible
:class: definition
A process is **reversible** if it can be run backwards so that the system *and everything it
interacted with* return to their original states, leaving no trace anywhere. Returning the
system alone is not enough — a compressed gas can always be re-expanded; the question is what
the round trip left behind in the surroundings.
:::

In practice three conditions are needed together: the process is **quasistatic**, it involves
**no friction** or other dissipation, and **no heat crosses a finite temperature difference**.
Slowness delivers only the first. Here are the common ways a process fails, and in each case
it is the second law that proves the failure is permanent: assume the process *could* be
undone without trace, and a forbidden machine appears.

**1. Heat crossing a finite temperature difference.** Heat $Q$ flows by conduction from a body
at $T_h$ into one at $T_c < T_h$. To undo it without trace, $Q$ would have to go back from
$T_c$ to $T_h$ with nothing else changing — exactly what the Clausius statement forbids.
However slowly the heat leaks, the leak is irreversible, because slowness does not shrink the
temperature gap it crosses.

**2. Friction.** A block slides to rest, and its kinetic energy $W$ ends up as heat in a table
at temperature $T$. Undoing it means taking that heat out of the table and returning all of it
to the block as motion, with no other change: heat from a single reservoir converted entirely
into work, which is the Kelvin statement's forbidden result. Electrical resistance, magnetic
hysteresis and viscous stirring are the same thing in different clothes — work turned into
heat at one temperature.

**3. Unrestrained expansion.** A gas at temperature $T$ expands freely from $V$ into a vacuum
until it fills $2V$. Suppose some device could return it to $V$ at the same temperature,
leaving no other trace. Then let the gas expand again, this time *reversibly*, along the
isotherm at $T$ in contact with a reservoir: it absorbs $N \kB T \ln 2$ of heat and delivers
the same amount of work. Return it with the device. The gas has gone round a cycle, one
reservoir has lost heat, and exactly that much work has appeared: Kelvin again.

**4. Mixing.** Two different ideal gases sharing a box after a partition is removed behave as
two independent free expansions, each gas spreading into the whole volume as if the other were
absent. Unmixing them without trace would undo two free expansions at once, so mixing is
irreversible for the same reason as (3).
[Module 08](../statistical-mechanics/08-multiplicity.md) looks at it again by counting.

Module 06 ended with an ordering it could measure but not explain. Letting a gas expand
adiabatically to twice its volume, the slow route ended at $189.0\ \mathrm{K}$, the route
against a fixed load at $225.0\ \mathrm{K}$ and the free expansion at $300.0\ \mathrm{K}$ —
and the slow route delivered the most work. Compressing to half the volume, the slow route
ended at $476\ \mathrm{K}$ and slamming the piston at $900\ \mathrm{K}$, at 3.4 times the
cost. The Kelvin statement explains both at once.

:::{admonition} No adiabatic route ends colder than the quasistatic one
:class: theorem
Take a gas in state $A$ and change its volume to $V_B$ by *any* adiabatic process, however
violent. It cannot end colder than the quasistatic adiabat from $A$ would leave it at the same
volume.
:::

**Proof.** Call the quasistatic endpoint $B$, at temperature $T_B$, and suppose some adiabatic
route ended at the same volume but at $T' < T_B$. Close a cycle. First warm the gas at constant
volume from $T'$ to $T_B$, using any single reservoir at a temperature $T_R \ge T_B$ and
disconnecting it when the gas reaches $T_B$. That warming is itself irreversible — heat
crosses a gap — but nothing in the argument needs it not to be. The gas is now in state $B$,
so return it to $A$ along the quasistatic adiabat. Round the cycle $\Delta U = 0$, and the only
heat that crossed was $C_V (T_B - T')$, absorbed from the one reservoir; so the gas did exactly
that much net work on its surroundings. A cycle whose sole result turns one reservoir's heat
into work: Kelvin forbids it. $\blacksquare$

The argument never asked whether the volume went up or down, so it covers both of module 06's
experiments. For an adiabatic process $Q = 0$, so the work done on the gas is

$$
\Won = \Delta U = C_V \left(T_{\text{end}} - T_A\right) ,
$$

and a hotter endpoint means more work put in and less taken out. On the way out the
quasistatic route delivers the most work any adiabatic expansion can; on the way in it costs
the least any adiabatic compression can. Module 06's numbers are the theorem being obeyed, and
they could not have come out the other way round. The same statement will reappear below, in
one line, in the language of entropy.

(07-second-law-two-reservoirs)=
### Why an engine needs two reservoirs, and why Carnot's cycle has its shape

The Kelvin statement says a cyclic engine cannot run on one reservoir. For a gas you can see
why, and the picture also shows what the second reservoir is *for*.

:::{figure} ../media/second-law-two-reservoirs.png
:alt: Two pressure-volume diagrams. Left, a single red isotherm crossed once each by three grey adiabats. Right, a closed loop made of a red hot isotherm, a grey adiabat, a blue cold isotherm and a second grey adiabat, with the enclosed area shaded and arrows showing the direction of travel.
:width: 100%

(a) One reservoir at temperature $T$. Heat can move reversibly only along the red isotherm at
$T$; every other stroke is an adiabat (grey), and each adiabat crosses the isotherm exactly
once. No closed loop built from these pieces encloses any area. (b) Two reservoirs. Expansion
on the hot isotherm, adiabatic cooling, compression on the cold isotherm at lower pressure,
adiabatic warming back to the start. The shaded area between the outgoing and returning
branches is the work delivered.
:::

**One reservoir.** To stay reversible, the gas may exchange heat only while it is at the
reservoir's own temperature $T$ — any gap between them is source 1 above. So every stroke that
moves heat lies on the one isotherm at $T$, and every other stroke is adiabatic. But an
adiabat, along which $P V^{\gamma}$ stays constant, is steeper than an isotherm, along which
$P V$ stays constant, so the two cross exactly once (panel a): leave the isotherm along an adiabat and the only way
back onto it is the same adiabat. Every loop you can draw from these pieces retraces itself and
encloses no area. No area, no work. Sloppy thermal contact does not rescue it — that is the
Kelvin statement in general; the point here is only to see it happen to a gas.

**Two reservoirs.** Now add a colder reservoir at $T_c$ (panel b). The gas expands on the hot
isotherm, absorbing heat and doing work; an adiabatic expansion cools it to $T_c$ with no heat
flowing; it is compressed back on the *cold* isotherm; and an adiabatic compression returns it
to the start. The whole return journey runs at lower pressure than the outward one — the gas
is colder, and at a given volume a colder gas pushes back less — so pushing it back costs less
work than it delivered on the way out. The difference is the enclosed area, and it is the engine's output.

The price is paid on the cold isotherm. Compressing a gas heats it; to keep it at $T_c$ while
you compress it, that heat has to leave, and heat leaves only to something at or below the
gas's temperature. Only the cold reservoir will take it. That dumped heat is $Q_c$, and it is
not waste in the engineering sense: it is what makes the cheap compression possible.

**The shape is forced.** The same reasoning settles what a reversible two-reservoir engine must
look like, *provided its working substance exchanges heat with nothing but the two
reservoirs*. Heat may enter only while the substance is at $T_h$ and leave only while it is at
$T_c$, so those strokes are isotherms at exactly those temperatures; and the substance must
travel between the two temperatures without touching either reservoir, so those strokes are
adiabats. Two isotherms joined by two adiabats: the Carnot cycle. It is not one design among
many; under that proviso it is the only reversible one. (An engine with an internal heat store,
a *regenerator*, escapes the proviso — the advanced section shows how.)

:::{admonition} A gas picture, not a proof
:class: model-assumption
This argument uses an ideal gas: its isotherms, its adiabats and its equation of state. The Kelvin
statement needs none of that and covers every working substance — steam, a stretched rubber
band, a magnet, a box of light. The picture shows *why the law is reasonable* for the one
system whose every stroke you can draw; the law is what makes it general.
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

That is the whole conversion. Outside this box, $Q_h$, $Q_c$ and $W$ are *sizes*, as in the
diagrams, with the arrows or the prose saying which way the energy goes; every *signed*
quantity in this module, and every quantity in `thermolab.engines` other than `work_output`,
carries the project sign.
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

:::{figure} ../media/second-law-carnot-proof.png
:alt: Energy-flow diagram of Carnot's proof. An impossible engine X takes 500 J from the hot reservoir, dumps 200 J into the cold one, and passes 300 J of work to a reversible engine R running backwards, which lifts 300 J from the cold reservoir and delivers 600 J to the hot one. Together they equal a single impossible machine moving 100 J from cold to hot with no work.
:width: 90%

The proof with numbers. The hypothetical engine $X$ (dashed) claims efficiency $0.6$, and the
reversible engine $R$ has $0.5$ between the same reservoirs. $X$ draws $500\ \mathrm{J}$ from
the hot reservoir, dumps $200\ \mathrm{J}$ into the cold one, and hands its $300\ \mathrm{J}$
of work to $R$, run backwards as a heat pump. $R$ uses it to lift $300\ \mathrm{J}$ out of the
cold reservoir and deliver $600\ \mathrm{J}$ to the hot one. Read the pair as one machine
(dotted outline): no work enters or leaves, and $100\ \mathrm{J}$ has moved from cold to hot —
the Clausius statement's forbidden machine.
:::

**Why reversibility is the step that matters.** The proof runs $R$ backwards and assumes that,
backwards, it consumes exactly the work it used to deliver and moves exactly the heats it used
to move — every arrow flipped, every magnitude unchanged. That is what *reversible* means, and
only a reversible engine does it. Run an engine with friction backwards and the friction does
not turn round: it still eats work, now on the way in, and the reversed machine is a worse heat
pump than the forward one was an engine. That is why the theorem compares every engine with a
reversible one, and why reversibility had to be defined first.

:::{admonition} The step where the working substance vanishes
:class: theorem
Read back through the proof and notice what never appeared: what $X$ or $R$ is made of, how
big they are, what shape their cycles trace. The argument uses only that $X$ produces work
from two reservoirs and that $R$ can be reversed. So the maximum efficiency cannot depend on
the working substance — it can depend on nothing but the two temperatures. This is the answer
to prediction 2, and it is the part of the theorem that is genuinely surprising.
:::

Sadi Carnot published this argument in 1824, when heat was believed to be a conserved fluid,
*caloric*, falling from hot to cold through an engine the way water falls through a mill wheel.
That theory was wrong — heat is not conserved; part of it becomes the work — yet his conclusion
survived intact. Clausius and Kelvin rebuilt the proof around 1850 on energy conservation and
the second law, and the version above is theirs. A result that outlived the theory it was born
in is the historical face of what the proof shows: it never needed to know what heat is made
of.

### Putting a number on it

Carnot's theorem says the reversible efficiency is some universal function of the two
temperatures. To find the function we only need to evaluate it *once*, for any convenient
reversible engine — and the ideal gas is convenient.

Take the Carnot cycle: isothermal expansion from $V_1$ to $V_2$ at $T_h$; adiabatic expansion
to $V_3$, cooling the gas to $T_c$; isothermal compression at $T_c$ to $V_4$; adiabatic
compression back to the start.

On the hot isotherm $\Delta U = 0$, so all the absorbed heat leaves as work:

$$
Q_h = N \kB T_h \ln\!\frac{V_2}{V_1} .
$$

On the cold isotherm the gas is compressed, so work is done *on* it, and since $\Delta U = 0$
again the same amount leaves as heat. Its size is

$$
Q_c = N \kB T_c \ln\!\frac{V_3}{V_4} .
$$

Now the two adiabats do the essential work. Along an adiabat $T V^{\gamma - 1}$ is constant.
The expanding adiabat joins $V_2$ at $T_h$ to $V_3$ at $T_c$, and the compressing one joins
$V_4$ at $T_c$ to $V_1$ at $T_h$:

$$
T_h V_2^{\gamma-1} = T_c V_3^{\gamma-1} ,
\qquad
T_h V_1^{\gamma-1} = T_c V_4^{\gamma-1} .
$$

Both adiabats connect the same pair of temperatures, so both stretch the volume by the same
factor, and dividing one condition by the other gives

$$
\frac{V_3}{V_2} = \left(\frac{T_h}{T_c}\right)^{1/(\gamma-1)} = \frac{V_4}{V_1}
\qquad\Longrightarrow\qquad
\frac{V_3}{V_4} = \frac{V_2}{V_1} .
$$

Here is the whole cycle as a ledger, in the course's sign convention — heat into the gas and
work done on it both counted positive — with $C_V = \tfrac{f}{2} N \kB$ and $r = V_2/V_1$:

| Stroke | Touches | $Q$ (into gas) | $\Won$ | $\Delta U$ |
|---|---|---|---|---|
| isothermal expansion | $T_h$ | $+N \kB T_h \ln r$ | $-N \kB T_h \ln r$ | $0$ |
| adiabatic expansion | nothing | $0$ | $-C_V (T_h - T_c)$ | $-C_V (T_h - T_c)$ |
| isothermal compression | $T_c$ | $-N \kB T_c \ln r$ | $+N \kB T_c \ln r$ | $0$ |
| adiabatic compression | nothing | $0$ | $+C_V (T_h - T_c)$ | $+C_V (T_h - T_c)$ |

Two things to notice. The last column sums to zero, as it must round a closed loop. And the
two adiabats' works are equal and opposite, because each is $C_V$ times the same temperature
span: they cancel exactly, and every joule the cycle nets comes from the two isotherms. That is
the overshoot in the animation's middle bar — the adiabatic expansion adds work that the
adiabatic compression hands straight back.

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

Since 2019 the SI has pinned the scale down differently, by defining the Boltzmann constant to
be exactly $\kB = 1.380649 \times 10^{-23}\ \mathrm{J\,K^{-1}}$, so the triple point of water,
$273.16\ \mathrm{K}$, is now a measured value rather than a definition. The scale is the same
one; only the way it is anchored has changed.

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
A **coefficient of performance** is the heat a driven machine moves per unit of work it
consumes: the heat lifted out of the cold side for a refrigerator, the heat delivered to the
hot side for a heat pump. These are *not* efficiencies and are not bounded by 1. Nothing is being converted: energy is
being **moved**, and the work is what it costs to move it uphill. A kitchen refrigerator with
$T_c = 275\ \mathrm{K}$ and $T_h = 300\ \mathrm{K}$ has a ceiling of $275/25 = 11$. That is
the answer to prediction 3 — a value of 3 is not suspicious, it is mediocre. It is also why
heat pumps heat buildings for a fraction of what a resistive heater costs: the pump moves
heat that is already outside, while the heater manufactures it.
:::

Note the exact identity $\mathrm{COP}_{\text{pump}} = \mathrm{COP}_{\text{fridge}} + 1$. It
is energy conservation and nothing more: everything the machine lifts from the cold side, plus
the work it consumed, arrives on the hot side.

These are the coefficients of the *Carnot* refrigerator. That no other refrigerator can do
better is not yet proved — Carnot's theorem was about engines — and the next section proves it
along with a great deal else.

(07-second-law-clausius)=
### The Clausius inequality

Carnot's theorem is a statement about engines. The second law is broader than that — it
constrains refrigerators, heat leaks, and machines that touch a dozen reservoirs — and
Clausius found the form of it that covers all of them at once. It follows from the Kelvin
statement in a few steps.

**Signed heats.** For this section write $q$ for heat *into the device* from a reservoir,
positive or negative as it happens: the course's ordinary sign, applied to each reservoir
exchange separately. An engine has $q_h > 0$ and $q_c < 0$; a refrigerator has $q_h < 0$ and
$q_c > 0$.

**Two reservoirs.** Let any device run one cycle between reservoirs at $T_h$ and $T_c$,
exchanging $q_h$ and $q_c$. Attach a reversible Carnot machine $C$ between the same two
reservoirs, sized and run in whichever direction makes it return to the cold reservoir exactly
what the device took from it, so that the cold reservoir nets nothing: $C$ takes in
$c_c = -q_c$ on its cold side. A reversible machine's heats are in the ratio of the
temperatures — that is what the thermodynamic scale says — so $c_h / T_h + c_c / T_c = 0$, and
$C$ takes in $c_h = q_c T_h / T_c$ on its hot side.

Now read the device and $C$ together. After one cycle each is back where it started, the cold
reservoir is exactly as it was, and the only thing touched is the hot reservoir, which has
given up

$$
q_h + \frac{T_h}{T_c}\, q_c .
$$

If that were positive, the pair would be a cycle whose sole result turns one reservoir's heat
into work, and Kelvin forbids it. So it is zero or negative. Dividing by $T_h$:

$$
\frac{q_h}{T_h} + \frac{q_c}{T_c} \le 0 .
$$

**When does equality hold?** If the device is reversible, run it backwards: every $q$ flips
sign, so the same argument now gives $q_h/T_h + q_c/T_c \ge 0$, and the two together force
equality. Conversely, if equality holds, the pair leaves no trace at all — the hot
reservoir nets nothing either — so $C$ has undone everything the device did, which is exactly
what it means for the device to be reversible. Equality for reversible devices; strict
inequality for every other one.

**What it gives back.** For an engine, in the sizes used so far, $q_h = Q_h$ and $q_c = -Q_c$,
and the inequality reads $Q_c / Q_h \ge T_c / T_h$ — which is $\eta \le 1 - T_c/T_h$, Carnot's
bound again. For a refrigerator $q_c = Q_c$ and $q_h = -Q_h$, with $Q_h = Q_c + W$, and the
inequality becomes

$$
\mathrm{COP}_{\text{fridge}} = \frac{Q_c}{W} \le \frac{T_c}{T_h - T_c} ,
$$

a ceiling on *every* refrigerator, not only the Carnot one evaluated above.

**Many reservoirs.** A real device meets a whole range of temperatures — a gas heated at
constant volume passes through every temperature on the way up. Clausius handled this by
giving every exchange its own auxiliary machine.

:::{figure} ../media/second-law-clausius-inequality.png
:alt: A device D receives heat from several auxiliary engines C_1, C_2 up to C_n, each at its own temperature T_i. Every auxiliary engine draws heat from a single reference reservoir at T_0 and delivers work. A dotted outline encloses all the engines and the device, leaving only the reservoir at T_0 outside.
:width: 85%

Clausius's construction. The device $D$ goes round a cycle, taking in heat $\delta Q_i$ at
each of the temperatures $T_i$ it meets on the way. Each of those heats is supplied by its own
reversible engine $C_i$, which runs between a single reference reservoir at $T_0$ and the
temperature $T_i$, drawing $\delta Q_i\, T_0 / T_i$ from the reference. Everything inside the
dotted outline returns to its starting state, and the only thing outside it that it touches is
the reservoir at $T_0$.
:::

Each auxiliary engine $C_i$ supplies the device with exactly the heat $\delta Q_i$ it takes in
at temperature $T_i$ — negative where the device gives heat out — and, being reversible, draws
$\delta Q_i\, T_0 / T_i$ from the reference reservoir to do so. Over one cycle of everything
inside the outline, the only reservoir touched is the one at $T_0$, which gives up

$$
T_0 \sum_i \frac{\delta Q_i}{T_i} .
$$

Kelvin forbids this from being positive, and in the limit of many small exchanges the sum
becomes an integral around the cycle.

:::{admonition} The Clausius inequality
:class: theorem
For any device taken round a cycle,

$$
\oint \frac{\dbar Q}{T_{\text{res}}} \le 0 ,
$$

where $\dbar Q$ is the heat taken in from a reservoir at temperature $T_{\text{res}}$.
Equality holds exactly when the cycle is reversible.
:::

Note which temperature divides: the **reservoir's**, not the device's. For a cycle of
quasistatic strokes, dividing by the gas's own temperature instead gives zero whether or not
the heat crossed a gap on the way in, and proves nothing — the entire content of the
inequality lives in the gap between the two temperatures.

(07-second-law-entropy)=
### Entropy: a new function of state

Apply the inequality to a reversible cycle and it becomes an equality. For a reversible
exchange there is no gap between the system and its reservoir, so $T$ is simply the system's
own temperature:

$$
\oint \frac{\dbar Q_{\text{rev}}}{T} = 0 .
$$

Now take two equilibrium states $a$ and $b$ and any two reversible paths between them, I and
II. Out along I and back along II is a reversible cycle, and reversing a path flips the sign
of every $\dbar Q_{\text{rev}}$, so

$$
\int_{a\,(\mathrm{I})}^{b} \frac{\dbar Q_{\text{rev}}}{T}
= \int_{a\,(\mathrm{II})}^{b} \frac{\dbar Q_{\text{rev}}}{T} .
$$

The integral does not depend on which reversible path is taken, only on its endpoints — which
is precisely the condition for it to be the change in a function of state.

:::{admonition} Entropy
:class: definition
The **entropy** $S$ is the function of state whose change between two equilibrium states is

$$
\Delta S = S_b - S_a = \int_a^b \frac{\dbar Q_{\text{rev}}}{T} ,
\qquad
\mathrm{d}S = \frac{\dbar Q_{\text{rev}}}{T} ,
$$

evaluated along any reversible path from $a$ to $b$. Its unit is $\mathrm{J\,K^{-1}}$. Only
differences are defined here; fixing an absolute value takes a further law.
:::

The inexact differential $\dbar Q$ has been turned into an exact one by dividing by $T$ —
$1/T$ is an *integrating factor* for heat, in the sense [the conventions
page](../conventions.md) sets out. This is the payoff [module 05](05-work-paths.md) and the
[mathematics refresher](../foundations/math-refresher.md) were preparing for, and it has been
reached without a single mention of atoms.

:::{admonition} Entropy belongs to the state, not to the path
:class: theorem
Because $S$ is a function of state, $\Delta S$ between two equilibrium states is the same
however the system actually travelled between them — reversibly, irreversibly or violently.
The reversible path is only the *instrument* for computing it. To find $\Delta S$ for an
irreversible process, invent any reversible process with the same two endpoints and integrate
$\dbar Q_{\text{rev}}/T$ along that instead.
:::

**The ideal gas.** Along a reversible stroke

$$
\dbar Q_{\text{rev}} = \mathrm{d}U - \dbar \Won = C_V\,\mathrm{d}T + P\,\mathrm{d}V .
$$

Divide by $T$, use $P/T = N \kB / V$, and each term integrates on its own:

$$
\Delta S = N \kB \ln\frac{V_b}{V_a} + C_V \ln\frac{T_b}{T_a} ,
\qquad
C_V = \frac{f}{2} N \kB .
$$

Two special cases are worth knowing by name. Along an **isotherm** the change is
$N \kB \ln(V_b/V_a)$, which is the heat absorbed divided by $T$. Along a
**reversible adiabat**, $\Delta S = 0$ — no heat, no entropy change — which is why a reversible
adiabat is also called an *isentrope*. This is the formula `thermolab.engines.entropy_change_of_gas`
evaluates.

**A reservoir.** A reservoir stays at its fixed temperature $T$ while it exchanges heat, and it
is so large that it never leaves equilibrium, so every exchange is reversible *from its own
side*. If it receives heat $Q$,

$$
\Delta S_{\text{res}} = \frac{Q}{T} .
$$

**A body with a constant heat capacity.** Warm it reversibly from $T_1$ to $T_2$, one small
step at a time, with $\dbar Q_{\text{rev}} = C\,\mathrm{d}T$:

$$
\Delta S = \int_{T_1}^{T_2} \frac{C\,\mathrm{d}T}{T} = C \ln\frac{T_2}{T_1} .
$$

:::{admonition} Constant heat capacity
:class: model-assumption
The last formula takes $C$ to be the same at every temperature on the way. That is good for
liquid water between freezing and boiling, and for a solid well above its Debye temperature;
it fails near a phase transition, and at low temperature, where every heat capacity falls
towards zero.
:::

Now look again at the free expansion of module 06: $V$ to $2V$ at fixed temperature, no heat
and no work. No heat crossed, so a naive reading says no entropy change. But $S$ is a function
of state, and the reversible isotherm between the same two states gives an entropy change of
$N \kB \ln 2$, which is positive. The gas's entropy rose although nothing flowed in — which is what
it looks like when a process *produces* entropy rather than receiving it.

(07-second-law-ledger)=
### Entropy produced, and where the lost work goes

**Any process, not only cycles.** Take a system from state $a$ to state $b$ by any process at
all, exchanging heat with reservoirs, and bring it back along a reversible path. The round
trip is a cycle, so the Clausius inequality applies, and the reversible return from $b$ to $a$
contributes exactly $S_a - S_b$. So

$$
\Delta S \ge \int_a^b \frac{\dbar Q}{T_{\text{res}}} ,
$$

with equality exactly for a reversible process. A system's entropy can rise by more than the
heat it received brings in, never by less. Two consequences follow at once.

- For an **adiabatic** process nothing is received, so $\Delta S \ge 0$. For an ideal gas
  arriving at the quasistatic adiabat's final volume, the entropy formula gives a change of
  $C_V \ln(T'/T_B)$, so $\Delta S \ge 0$ says $T' \ge T_B$ — the theorem of the
  reversibility section, in one line.
- For an **isolated** system nothing is received either, so its entropy can only rise or stay
  the same. Why it rises to a *maximum*, and what that maximum picks out, is the business of
  module 09.

**The balance sheet.** Now include the reservoirs. Each reservoir's entropy changes by the heat
it receives divided by its temperature, the system's by its own $\Delta S$, and whatever is
left over is new.

:::{admonition} Entropy produced
:class: definition
The **entropy produced** by a process is the total entropy change of the system and of every
reservoir it touched,

$$
S_{\text{gen}} = \Delta S + \sum_i \frac{Q_i}{T_i} ,
$$

where $\Delta S$ is the system's own change and $Q_i$ is the heat that reservoir $i$, at
temperature $T_i$, *received*.
:::

The heat each reservoir received is the heat the system took from it with the sign flipped, so
the inequality above is a statement about this sum.

:::{admonition} The second law, as entropy produced
:class: theorem
Every process has $S_{\text{gen}} \ge 0$: zero if it is reversible, positive if it is not. Over
a complete cycle the system contributes nothing, and the entropy produced is minus the Clausius
sum,

$$
S_{\text{gen}} = -\oint \frac{\dbar Q}{T_{\text{res}}} .
$$
:::

**The refrigerator and its food — prediction 4.** A refrigerator holds its interior at $T_c$
by lifting heat $Q_c$ out of it, and the kitchen at $T_h$ receives $Q_h = Q_c + W$. The
interior loses entropy $Q_c / T_c$, and that is all the question noticed. The kitchen gains
$(Q_c + W)/T_h$, and the Clausius inequality says this is at least as much:

$$
S_{\text{gen}} = \frac{Q_c + W}{T_h} - \frac{Q_c}{T_c} \ge 0 .
$$

The second law constrains the total, not any one piece of it. A fall in entropy in one place
is always paid for by a larger rise somewhere else — here in the kitchen — and the payment is
the electricity.

**A heat leak.** Let heat $Q$ conduct straight from a reservoir at $T_h$ to one at $T_c$
through a rod that ends the process exactly as it began. Then

$$
S_{\text{gen}} = \frac{Q}{T_c} - \frac{Q}{T_h} > 0 ,
$$

strictly positive whenever $T_h > T_c$: source 1 of the reversibility section, now as a number.

**Where the lost work goes.** Compare a real engine with a reversible one drawing the same heat
$Q_h$ from the same hot reservoir. The reversible one delivers $Q_h (1 - T_c/T_h)$; the real
one delivers $W = Q_h - Q_c$, in sizes as throughout. The shortfall is

$$
\begin{aligned}
W_{\text{lost}} &= Q_h \left(1 - \frac{T_c}{T_h}\right) - (Q_h - Q_c) \\
&= Q_c - \frac{T_c}{T_h}\, Q_h
= T_c \left(\frac{Q_c}{T_c} - \frac{Q_h}{T_h}\right) ,
\end{aligned}
$$

and the bracket is exactly the cycle's entropy produced.

:::{admonition} Lost work is entropy produced, priced at the cold temperature
:class: theorem
For an engine between two reservoirs, the work it fails to deliver, compared with a reversible
engine taking in the same heat, is

$$
W_{\text{lost}} = T_c\, S_{\text{gen}} .
$$

This is the Gouy–Stodola theorem. Every irreversibility inside an engine produces entropy, and
every unit of entropy produced costs $T_c$ of work that can never be recovered.
:::

Apply it to the heat leak. The rod produced $Q/T_c - Q/T_h$, so it threw away

$$
T_c\, S_{\text{gen}} = Q \left(1 - \frac{T_c}{T_h}\right) ,
$$

exactly the work a Carnot engine placed across the same gap would have made. Heat that flows
downhill without an engine in the way does not merely
go unused. It destroys the opportunity it carried.

:::{note} The module in eight statements
1. Energy conservation permits turning heat into work; the second law restricts *how*, and it
   is not an equation but two equivalent prohibitions, Kelvin's and Clausius's.
2. "Cyclic" and "sole result" carry the weight: a single expansion can turn heat entirely into
   work, and a refrigerator can move heat uphill, because neither is a cycle with a sole result.
3. A process is reversible only if it can be undone leaving no trace anywhere. Heat crossing a
   finite temperature difference, friction, unrestrained expansion and mixing all fail, and the
   second law is what proves it.
4. A cyclic engine needs a second, colder reservoir: that is what lets it compress its working
   substance more cheaply than it expanded it.
5. Carnot's theorem: no engine beats a reversible one between the same reservoirs, and every
   reversible one does equally well — so the bound depends on the temperatures alone.
6. For an ideal gas the bound is $1 - T_c/T_h$. It defines an absolute temperature, and run
   backwards it bounds every refrigerator and heat pump.
7. The Clausius inequality, $\oint \dbar Q / T_{\text{res}} \le 0$, makes
   $\int \dbar Q_{\text{rev}}/T$ path-independent, and so defines a new function of state,
   the entropy.
8. Every irreversibility produces entropy, and an engine pays for each unit of it with $T_c$ of
   work it will never deliver.
:::

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
to make heat flow at a finite rate — and two numbers move together: the efficiency falls, and
the entropy produced per cycle, $S_{\text{gen}} = -\oint \dbar Q / T_{\text{res}}$, rises
from zero. Every stroke of this engine is quasistatic, so it is also the counterexample
prediction 6 was after: as slow as you like, and irreversible all the same, because its heat
crosses a finite temperature gap however slowly it moves.

:::{admonition} Lost work and produced entropy are one quantity
:class: numerical-observation
With reservoirs at $600\ \mathrm{K}$ and $300\ \mathrm{K}$ and a gap of $10\ \mathrm{K}$ at
each end, the efficiency falls from $0.5000$ to $0.4746$, and the cycle's
$\oint \dbar Q / T_{\text{res}}$ turns negative for the first time. At a gap of
$100\ \mathrm{K}$ the efficiency is $0.2000$ and the loop integral is negative by $0.6$ of the
entropy the hot reservoir gave up. Shrink the gaps and the shortfall vanishes linearly: halve
the gap, halve the entropy produced. At every gap, the work lost equals $T_c\, S_{\text{gen}}$
to within rounding.
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

**6. A real cycle falls short for a reason, not for lack of care.** The idealised petrol
engine — two adiabats and two constant-volume heat strokes, every one of them reversible —
reaches $\eta = 1 - r^{1-\gamma}$ for compression ratio $r$, to twelve figures, and always
less than $1 - T_{\min}/T_{\max}$ between its own coldest and hottest states. Ask the
laboratory for its Clausius sum and it refuses: its heat strokes happen while the gas's
temperature is changing, so no single reservoir temperature describes either of them. Worked
example 5 below explains the shortfall.

**7. No adiabatic route beats the quasistatic one.** Release the piston against a constant
load — any load, lighter than the gas's pressure so that it expands or heavier so that it is
compressed — and compare with the quasistatic adiabat to the same final volume. The loaded
route ends hotter every time, as the theorem of the reversibility section demands. This too is
a falsification test: one counterexample would mean the code, or the theorem, is wrong.

**8. Entropy is a function of state, and the Clausius sum is not.** Let a gas expand freely to
twice its volume, then push it back along the isotherm in contact with a reservoir at its own
temperature.

:::{admonition} Two numbers equal in size and opposite in sign
:class: numerical-observation
Over the free expansion the gas's entropy rises by exactly $N \kB \ln 2$ — the value the
reversible isotherm gives, although no heat crossed. Around the whole cycle the Clausius sum
is the same size with the opposite sign, $\oint \dbar Q / T_{\text{res}} = -N \kB \ln 2$:
strictly negative, because the reservoir received the recompression's heat
and nothing ever gave it back. The gas's entropy returns to where it started; the reservoir's
does not, and the difference is the entropy the free expansion produced.
:::

(07-second-law-transfer)=
## Transfer the idea

The pattern — a conversion that energy conservation permits but a second, independent law
forbids — reaches well past engines.

- **Power stations.** Steam at $550\,{}^\circ\mathrm{C}$ against a river at
  $20\,{}^\circ\mathrm{C}$ gives a Carnot bound of $0.64$, from $1 - 293/823$. Real plants
  reach about $0.40$. That is not a $24$-point engineering failure: the maximum-*power*
  efficiency $1 - \sqrt{T_c/T_h} = 0.40$, derived in the advanced section, lands almost exactly
  on it, because a plant optimised
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

**The bridge to counting.** [Module 08](../statistical-mechanics/08-multiplicity.md) defines
entropy completely differently, as $S = \kB \ln \Omega$ — a count of microstates, with no
engine anywhere in sight. Try it on the free expansion: doubling the volume doubles the
positions open to each of $N$ particles, so $\Omega$ grows by a factor $2^N$ and
$\Delta S = N \kB \ln 2$ — the number this page got from a reversible isotherm and a heat
integral. The two definitions agree, up to the additive constant that a counting argument
cannot fix and a Clausius integral never needed. The agreement is not a coincidence; it is why
the same word is used for both, and why a bound derived from steam engines turns out to govern
the mixing of gases and the folding of proteins. It also says what makes heat "low-grade":
heat is energy spread at random over some $10^{23}$ molecular coordinates, work is energy in
one coordinate — the piston — and herding the first back into the second is overwhelmingly
improbable. That is the Kelvin statement, read one level down.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — checking a claim.** A company proposes a geothermal plant that draws heat
from underground brine at $150\,{}^\circ\mathrm{C}$ and rejects it to air at
$25\,{}^\circ\mathrm{C}$, and advertises an efficiency of $30\%$. Should you invest?

:::{dropdown} Solution
Convert first: $T_h = 423.15\ \mathrm{K}$ and $T_c = 298.15\ \mathrm{K}$. The best any engine
can do between these is

$$
\eta_{\text{Carnot}} = 1 - \frac{298.15}{423.15} = 0.2954 .
$$

The claim exceeds it, so it is impossible however the plant is built. Check it on the balance
sheet as well: per $1000\ \mathrm{J}$ drawn from the brine the plant would deliver
$300\ \mathrm{J}$ and reject $700\ \mathrm{J}$, so

$$
\begin{aligned}
S_{\text{gen}} &= \frac{700}{298.15} - \frac{1000}{423.15} \\
&= 2.3478 - 2.3632 = -0.0154\ \mathrm{J\,K^{-1}} .
\end{aligned}
$$

Negative: the plant would destroy entropy, which is the same verdict in the other language.
The margin is narrow — the claim is half a percentage point over the bound — which is exactly
why it has to be computed rather than eyeballed. And note the trap: fed Celsius, the same
formula gives $0.833$, and the claim would look modest.
:::

**Worked example 2 — a Carnot cycle, stroke by stroke.** A monatomic ideal gas ($f = 3$), with
$N$ chosen so that $N \kB = 1.000\ \mathrm{J\,K^{-1}}$, runs a Carnot cycle between
$500\ \mathrm{K}$ and $300\ \mathrm{K}$, doubling its volume on the hot isotherm. Fill in the
ledger, find the efficiency, and follow the entropy.

:::{dropdown} Solution
The cold isotherm spans the same volume ratio as the hot one, and each adiabat spans the
same $200\ \mathrm{K}$, so

$$
\begin{aligned}
Q_h &= N \kB T_h \ln 2 = 500 \times 0.6931 = 346.6\ \mathrm{J} , \\
Q_c &= N \kB T_c \ln 2 = 300 \times 0.6931 = 207.9\ \mathrm{J} , \\
C_V (T_h - T_c) &= 1.500 \times 200 = 300.0\ \mathrm{J} ,
\end{aligned}
$$

the last being the work each adiabat moves, with $C_V = \tfrac{3}{2} N \kB$. With heat into the
gas and work done on it both positive:

| Stroke | $Q$ (J) | $\Won$ (J) | $\Delta U$ (J) | $\Delta S_{\text{gas}}$ (J/K) |
|---|---|---|---|---|
| hot isotherm | $+346.6$ | $-346.6$ | $0$ | $+0.6931$ |
| adiabatic expansion | $0$ | $-300.0$ | $-300.0$ | $0$ |
| cold isotherm | $-207.9$ | $+207.9$ | $0$ | $-0.6931$ |
| adiabatic compression | $0$ | $+300.0$ | $+300.0$ | $0$ |

The adiabats' $300\ \mathrm{J}$ is more than the whole cycle nets, and they cancel. The net
work done on the gas is $\Won = -138.6\ \mathrm{J}$, so the engine delivers $138.6\ \mathrm{J}$
and

$$
\eta = \frac{138.6}{346.6} = 0.400 = 1 - \frac{300}{500} .
$$

For the entropy: the gas's column sums to zero, as a function of state must round a loop. The
hot reservoir gave up $346.6\ \mathrm{J}$ and the cold one received $207.9\ \mathrm{J}$, so

$$
\begin{gathered}
\Delta S_h = -\frac{346.6}{500} = -0.6931\ \mathrm{J\,K^{-1}} , \\
\Delta S_c = \frac{207.9}{300} = 0.6931\ \mathrm{J\,K^{-1}} ,
\end{gathered}
$$

and $S_{\text{gen}} = 0$. A reversible engine is a conduit for entropy: each cycle it carries
$0.6931\ \mathrm{J\,K^{-1}}$ from the hot reservoir to the cold one and creates none. The heat
it must reject is exactly the heat needed to carry that entropy out at $T_c$ — which is how
$Q_c$ was computed above. That is the rejected heat of prediction 1, seen as a necessity rather
than a loss.
:::

**Worked example 3 — a heat leak is work thrown away.** A furnace wall at $900\ \mathrm{K}$
leaks $1000\ \mathrm{J}$ of heat through its insulation into a room at $300\ \mathrm{K}$. How
much entropy is produced, and how much work has been lost?

:::{dropdown} Solution
The wall and the room act as reservoirs, and the insulation ends as it began, so

$$
\begin{aligned}
S_{\text{gen}} &= \frac{1000}{300} - \frac{1000}{900} \\
&= 3.333 - 1.111 = 2.222\ \mathrm{J\,K^{-1}} .
\end{aligned}
$$

The lost work, and the check the other way — a Carnot engine across the same gap, fed the same
$1000\ \mathrm{J}$ — agree:

$$
\begin{gathered}
T_c\, S_{\text{gen}} = 300 \times 2.222 = 666.7\ \mathrm{J} , \\
1000 \times \left(1 - \frac{300}{900}\right) = 666.7\ \mathrm{J} .
\end{gathered}
$$

Two-thirds of the leaking heat's value is gone, though not one joule of energy was destroyed. That is what insulation is really
for.
:::

**Worked example 4 — a cooling cup of coffee.** A $0.25\ \mathrm{kg}$ cup of coffee — treat it
as water, with specific heat $4184\ \mathrm{J\,kg^{-1}\,K^{-1}}$ — cools from $353\ \mathrm{K}$
to the room's $293\ \mathrm{K}$. Find the entropy change of the coffee, of the room, and of the
two together, and the work that could have been extracted along the way.

:::{dropdown} Solution
The coffee's heat capacity is $1046\ \mathrm{J\,K^{-1}}$, which is $0.25 \times 4184$. Its
temperature changes, so it is not a reservoir; use the constant-heat-capacity result, which gives the
coffee

$$
\Delta S = C \ln\frac{293}{353} = 1046 \times (-0.1863) = -194.9\ \mathrm{J\,K^{-1}} .
$$

The room is a reservoir at $293\ \mathrm{K}$, and it receives all the heat the coffee gives up:

$$
\begin{aligned}
Q &= C \times 60\ \mathrm{K} = 62\,760\ \mathrm{J} , \\
\Delta S_{\text{res}} &= \frac{62\,760}{293} = 214.2\ \mathrm{J\,K^{-1}} , \\
S_{\text{gen}} &= 214.2 - 194.9 = 19.3\ \mathrm{J\,K^{-1}} .
\end{aligned}
$$

The coffee's entropy *fell*, and by a lot; nothing is wrong, because the room's rose by more.
The second law is about the total, and no part of a system is obliged to gain entropy.

A reversible engine running between the cooling coffee and the room would have turned each
slice of heat $C\,\mathrm{d}T$ into work with efficiency $1 - 293/T$:

$$
\begin{aligned}
W_{\max} &= \int_{293}^{353} \left(1 - \frac{293}{T}\right) C\,\mathrm{d}T
= C \times 60 - 293\, C \ln\frac{353}{293} \\
&= 62\,760 - 57\,096 = 5664\ \mathrm{J} .
\end{aligned}
$$

Multiply the entropy produced by the room's temperature and the same number comes back,

$$
293 \times 19.33 = 5664\ \mathrm{J} ,
$$

so the lost-work rule holds even for a hot side whose temperature fell the whole time.
:::

**Worked example 5 — the Otto engine.** An idealised petrol engine takes in air at
$T_1 = 300\ \mathrm{K}$, compresses it adiabatically by a factor $r = 8$ (air has
$\gamma = 7/5$), heats it at constant volume to $2000\ \mathrm{K}$ by burning the fuel, expands
it adiabatically back to the full volume, and exhausts the heat at constant volume. Find its
efficiency, compare it with the Carnot bound between $300\ \mathrm{K}$ and $2000\ \mathrm{K}$,
and explain the gap — every stroke is reversible.

:::{dropdown} Solution
Along both adiabats $T V^{\gamma-1}$ is constant, so each changes the temperature by the same
factor:

$$
\frac{T_2}{T_1} = \frac{T_3}{T_4} = r^{\gamma-1} = 8^{0.4} = 2.297 ,
$$

giving $T_2 = 689.2\ \mathrm{K}$ after compression and $T_4 = 870.6\ \mathrm{K}$ after
expansion. Heat enters only on the ignition stroke and leaves only on the exhaust stroke, both
at constant volume, so

$$
\begin{aligned}
\eta &= 1 - \frac{C_V (T_4 - T_1)}{C_V (T_3 - T_2)} = 1 - \frac{T_1}{T_2} \\
&= 1 - r^{1-\gamma} = 0.565 ,
\end{aligned}
$$

where the middle step uses the two adiabats once more:

$$
T_4 - T_1 = \frac{T_3 - T_2}{r^{\gamma-1}} .
$$

The Carnot bound between the same extremes is much higher:

$$
1 - \frac{300}{2000} = 0.850 .
$$

**Why the gap, when every stroke is reversible?** Slice the cycle with many adiabats, close
together. Each thin slice is a small cycle that takes in a sliver of heat on the ignition
stroke at some temperature $T$, and rejects a sliver on the exhaust stroke at $T/r^{\gamma-1}$,
the temperature the same adiabat reaches at the other volume. A thin slice exchanges heat at
essentially two temperatures, so it is a small Carnot engine, and its efficiency is
$1 - 1/r^{\gamma-1}$ — the same for every slice, which is why the whole engine has that value.
But the slice at the bottom of the ignition stroke works between $689\ \mathrm{K}$ and
$300\ \mathrm{K}$, and the one at the top between $2000\ \mathrm{K}$ and $871\ \mathrm{K}$. No
slice spans the full range. The Carnot bound is reached only by an engine that takes in *all*
its heat at the top temperature and rejects *all* of it at the bottom; the Otto engine takes
its heat in on the way up.

**The same point, in entropy.** Each heat stroke changes the gas's entropy by the same amount,
since $T_3/T_2$ and $T_4/T_1$ are the same ratio. Dividing each stroke's heat by that entropy
change gives the average temperature at which the heat crossed, on the way in and on the way
out:

$$
\begin{gathered}
\frac{T_3 - T_2}{\ln(T_3/T_2)} = 1230.4\ \mathrm{K} ,
\qquad
\frac{T_4 - T_1}{\ln(T_4/T_1)} = 535.6\ \mathrm{K} , \\
1 - \frac{535.6}{1230.4} = 0.565 .
\end{gathered}
$$

The Otto engine is a Carnot engine between those two averages. Real petrol engines, with friction, heat leaks and a
burn that takes time, reach about $0.3$.
:::

:::{note} Your predictions, revisited
1. **The other 600 J** is not waste a better design could recover. Every cyclic engine must
   reject heat to a colder reservoir — see
   [why an engine needs two reservoirs](#07-second-law-two-reservoirs) — and even a perfect
   engine rejects the fraction $T_c/T_h$ of what it takes in.
2. **Steam or helium:** neither. The best efficiency depends on the two temperatures alone,
   because the working substance drops out of Carnot's proof.
3. **300 J out for 100 J in** is ordinary. A coefficient of performance is not an efficiency,
   and the Carnot ceiling for a kitchen refrigerator is around 11.
4. **The refrigerator** lowers its interior's entropy and raises the kitchen's by more — see
   [the balance sheet](#07-second-law-ledger).
5. **The power station** could reach at most $0.64$ and actually reaches about $0.40$, close to
   the maximum-*power* efficiency — a deliberate choice, not an engineering failure.
6. **Infinitely slow is not enough.** A slow slide with friction, or a slow heat leak across a
   temperature gap, is exactly as irreversible as a fast one — see
   [reversible and irreversible processes](#07-second-law-reversibility).
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
6. Name four ways a process can fail to be reversible. For one of them, show step by step that
   undoing it without trace would violate the Kelvin or the Clausius statement.
7. A free expansion exchanges no heat, yet the gas's entropy rises. Explain why defining
   entropy requires a reversible path, and why it can nevertheless be assigned to the end of a
   violently irreversible process.

(07-second-law-advanced)=
## Advanced: power, regenerators, and where the temperature scale comes from

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It follows three threads the core left
loose: why real engines deliberately fall short of Carnot, how some engines reach the Carnot
bound without being Carnot cycles, and why the reversible heat ratio had to be a ratio of
temperatures in the first place.
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

**Regenerators: reaching Carnot without Carnot's shape.** A Stirling engine runs two isotherms
joined by two constant-volume strokes. Between the isotherms the gas has to be cooled from
$T_h$ to $T_c$, and later warmed back; done against the reservoirs, that would push heat
across large temperature gaps, which is irreversible and costs efficiency. A *regenerator*
avoids it: a matrix of fine wire that the gas passes through on its way down, leaving its heat
in layers graded from $T_h$ at one end to $T_c$ at the other, and picks back up on its way up,
each layer returning heat at the temperature it was deposited. For an ideal gas the two
constant-volume strokes move the same heat $C_V (T_h - T_c)$ in opposite directions, so a
perfect regenerator balances exactly, and the only heat crossing to the outside is on the two
isotherms, at $T_h$ and $T_c$. The engine is then reversible, exchanges heat externally with
two reservoirs only, and reaches $1 - T_c/T_h$ on constant-volume strokes. That is why the
core said the Carnot shape is forced only for an engine whose substance exchanges heat with
nothing but the reservoirs: the regenerator is a third thing to exchange with. The Clausius
inequality covers it without modification; the four-stroke picture of this module's laboratory
does not.

**Why the heat ratio must factorise.** The core defined thermodynamic temperature by the
reversible heat ratio and used the ideal gas to fix its form. There is an argument that needs
no gas. Carnot's theorem says the heat ratio of a reversible engine between two reservoirs is
a universal function of them alone, $Q_c/Q_h = f(t_c, t_h)$, where $t$ is any empirical
temperature. Stack two reversible engines: one between $t_1$ and $t_2$, and a second that takes
the heat the first rejects at $t_2$ and works on down to $t_3$. The pair is a reversible engine
between $t_1$ and $t_3$ that leaves the middle reservoir unchanged, so

$$
f(t_3, t_1) = f(t_3, t_2)\, f(t_2, t_1)
$$

for every $t_2$. Fix $t_2$ at a reference value and the right-hand side splits into a function
of $t_3$ times a function of $t_1$, so $f(t_c, t_h) = \theta(t_c)/\theta(t_h)$ for a single
increasing function $\theta$. That $\theta$ *is* the thermodynamic temperature, up to a
constant factor; the ideal-gas calculation only confirmed that $\theta$ is proportional to the
gas thermometer's $T$.

:::{admonition} What is still open here
:class: open-question
Reversing every molecular velocity in an engine would run it backwards, which means the
mechanics underneath has no preferred direction while the second law plainly does. Module 08
resolves this as a statement about counting, not about dynamics. What remains genuinely open
is *why the universe started in a low-entropy state at all* — the second law's arrow is
inherited from that initial condition, and thermodynamics does not explain it.
:::
