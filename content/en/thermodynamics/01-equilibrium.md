---
title: Thermal equilibrium
short_title: 01 · Thermal equilibrium
module: 01-equilibrium
objectives:
  - id: OBJ-01-1
    text: State the zeroth law of thermodynamics and explain why it is what makes "temperature" a well-defined, transitive property.
  - id: OBJ-01-2
    text: Explain thermal equilibrium as the state at which net heat flow between two bodies in contact stops, and identify what continues at the microscopic level.
  - id: OBJ-01-3
    text: Derive the equilibrium temperature T_eq = (C_A T_A + C_B T_B)/(C_A+C_B) from conservation of energy, and predict how it depends on the two heat capacities.
  - id: OBJ-01-4
    text: Derive and interpret the exponential relaxation law T_A(t) - T_B(t) = (T_A(0)-T_B(0)) e^{-t/tau}, and state what determines the relaxation time tau.
  - id: OBJ-01-5
    text: Verify computationally that a discrete stochastic energy-exchange model converges to the analytic relaxation law as the system size grows, and state what the simulation does and does not establish.
---

# Thermal equilibrium

(01-equilibrium-puzzle)=
## The puzzle: what makes two temperatures "the same"?

Walk into a room and touch a metal table leg, then the wooden tabletop beside it. The metal
feels distinctly colder, even though a thermometer says both are at exactly the same
temperature as the room. Nothing here is a trick of thermometers: your hand is not measuring
temperature directly, it is measuring how fast heat leaves *it*, and metal conducts that heat
away far faster than wood does. Temperature itself — the quantity a thermometer reports — is
untouched by which material is in your hand.

So what *is* the quantity that a thermometer reports, precisely enough that two wildly
different objects — a table leg and a room full of air — can be said to share it? And why does
heat, once two objects are placed in contact, flow spontaneously from the hotter one to the
colder one, slow down, and stop *exactly* at the point where the two temperatures are equal —
never before, never after?

:::{important} The question
What does it mean for two bodies to be "at the same temperature"? Why does heat flow
spontaneously from hot to cold, and why does it stop precisely at equality rather than at some
other balance?
:::

The answer starts with something almost too obvious to state, and it is where this module
begins.

(01-equilibrium-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* running anything. Write them down.

1. A block of copper at $80\,^\circ\mathrm{C}$ is pressed against an identical block of copper
   at $20\,^\circ\mathrm{C}$, and the pair is otherwise isolated. Where do you expect the final
   common temperature to sit? Now suppose the second block is ten times more massive — does
   the final temperature move toward the hot block's starting value, the cold block's, or stay
   at the midpoint?
2. Sketch what you expect $T_A(t)$ and $T_B(t)$ to look like once the two blocks are in
   contact: straight lines crossing, curves that overshoot and ping back, or curves that bend
   over smoothly and flatten out? Does the gap between them ever change sign?
3. At the moment the two blocks reach a common temperature, has heat flow between them
   stopped, or merely balanced in both directions?
4. You double *both* heat capacities while keeping the two starting temperatures fixed. Does
   the final equilibrium temperature change? Does the *time* it takes to get there change?

:::{note} Why we ask first
Question 3 is deliberately the same shape as a question module 4 will ask about pressure:
does equilibrium mean the microscopic activity has stopped, or only that it has balanced?
Committing to an answer first is the only way to notice which intuition the derivation below
is about to correct.
:::

(01-equilibrium-explore)=
## Explore the model

The laboratory notebook lets you set two bodies' sizes and starting temperatures, then watch
individual quanta of energy hop back and forth between them while the two temperatures settle
onto a common value.

Here is the phenomenon in one picture: two bodies of unequal size, starting far apart in
temperature, relaxing onto a shared value that sits closer to the larger body's starting
temperature than to the smaller one's.

:::{figure} ../media/equilibrium-relaxation.mp4
:alt: Two temperature traces, body A starting hot and body B starting cold, both curving smoothly toward a common equilibrium value with no overshoot.
:width: 100%

Two bodies exchanging energy quanta at random, one step at a time. Body A (red) starts hot,
body B (blue) starts cold; both curves bend smoothly onto the dashed equilibrium temperature,
and the black dashed curve is the analytic prediction derived below. Nothing here was
smoothed — the curves are the raw simulation output.
:::

Watch what changes when the two bodies get bigger, at fixed starting temperatures. The three
panels below run the identical measurement with the pair's total size scaled up by roughly a
factor of ten each time, plotted as a *fraction* of the initial temperature gap so the
comparison is fair:

:::{figure} ../media/equilibrium-fluctuations.mp4
:alt: Three panels showing the fractional temperature gap decaying toward zero, with visibly larger random scatter around the smooth predicted curve for the smallest pair of bodies than for the largest.
:width: 100%

The same relaxation, run at three system sizes, each drawn as $(T_A - T_B)/(T_{A,0} -
T_{B,0})$ against the analytic prediction (dashed). The scatter around the smooth curve does
not come from anything getting gentler — it shrinks because there are more energy quanta to
average over, the same phenomenon that will return in module 4 as pressure fluctuations and
in module 8 as the multiplicity peak.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** two bodies A and B in thermal contact, modelled as Einstein solids with $N_A$
  and $N_B$ independent oscillators.
- **Dynamics:** one randomly chosen energy quantum hops per step, leaving its current body
  with probability proportional to that body's share of the quanta, and landing on a
  uniformly random oscillator among both bodies.
- **Boundary:** the pair is closed and isolated together; nothing enters or leaves the
  combined system, so the total number of quanta — the total energy — is exactly conserved.
- **Ensemble:** microcanonical for the joint system, exactly as in module 8: every accessible
  joint microstate is equally probable, and each body's own temperature is read off its own
  quanta by equipartition.
- **Ignored:** the physical rate at which exchanges are attempted (time is counted in steps,
  not seconds), any spatial structure inside a body, and any coupling besides the quantum
  exchange itself.
- **Valid when:** both bodies sit in the classical, high-temperature equipartition regime, and
  the quanta exchanged are the same size on both sides.
- **Failure modes:** low temperature, where quantum statistics replace equipartition; unequal
  quantum sizes between the bodies; and too few oscillators for "temperature" to be a
  meaningful macroscopic quantity.
:::

:::{admonition} What this model cannot do
:class: model-assumption
The quantum-hopping rule above is one specific, clean microscopic mechanism for exchanging
energy — not a model of any particular real material's conduction. Real thermal contact
between a table leg and a hand happens through phonons, electrons and molecular collisions,
none of which look like a single quantum jumping between two idealised solids. What the model
*can* show is that a mechanism built from nothing but "a random exchange, more likely from the
fuller side" reproduces the same macroscopic law derived below — evidence that the law is
robust to microscopic detail, not a claim that this is how any specific material actually
conducts heat.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 01 — thermal equilibrium](/lite/lab/index.html?path=en/labs/01-equilibrium.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/01-equilibrium.ipynb`.
:::

Run the laboratory now, then come back. Three things are worth doing before you read on:

- Start the two bodies at the same size but different temperatures, then repeat with one body
  ten times larger than the other. Watch which starting temperature the equilibrium value sits
  closer to.
- Watch the gap $T_A - T_B$ over time. Note whether it ever crosses zero and keeps going, or
  only ever shrinks toward it.
- Compare a small pair of bodies against a much larger pair, and watch how much noisier the
  approach to equilibrium looks for the small one.

(01-equilibrium-derive)=
## Derive the result

**System and boundary.** The pair of bodies A and B, isolated together as a whole; no work is
exchanged (the boundary is rigid), so all energy transfer between them is heat.

**Independent variables.** The two heat capacities $C_A$, $C_B$ and the two starting
temperatures $T_{A,0}$, $T_{B,0}$.

:::{admonition} The zeroth law of thermodynamics
:class: empirical-law
If body A is in thermal equilibrium with body C, and body B is separately in thermal
equilibrium with body C, then A and B are in thermal equilibrium with each other. This is an
empirical fact about the world, not a logical necessity — nothing forbids a universe in which
"equilibrium with" fails to be transitive, and the law is stated as an axiom precisely because
it cannot be derived from the other laws. It is what makes **temperature** a well-defined
property in the first place: without it, a thermometer (body C) reading the same value on two
different objects would tell you nothing about whether those two objects agree with each
other.
:::

### Energy conservation gives the equilibrium temperature

The pair is isolated, so whatever energy body A loses, body B gains, and vice versa: there is
nowhere else for it to go. Over any heat capacity's operating range small enough that $C$ can
be treated as constant, a body's internal energy change is $\Delta U = C\,\Delta T$ — the
working definition of heat capacity. Conservation of the pair's total energy is then

$$
C_A (T_{\text{eq}} - T_{A,0}) + C_B (T_{\text{eq}} - T_{B,0}) = 0 ,
$$

which rearranges to

$$
\boxed{\; T_{\text{eq}} = \frac{C_A T_{A,0} + C_B T_{B,0}}{C_A + C_B} \;}
$$

a heat-capacity-*weighted* average of the two starting temperatures — not the plain average
unless $C_A = C_B$. This is why the ten-times-more-massive block in prediction 1 pulls the
final temperature toward its own starting value: it takes proportionally more energy to move
its temperature by one degree, so it "wins" the average.

:::{admonition} Constant heat capacity is an approximation
:class: approximation
Real heat capacities depend on temperature, sometimes strongly (module 16 meets this for
solids at low temperature). Treating $C_A$ and $C_B$ as constants is exact only in the limit
of a small temperature range, and is otherwise an approximation whose error grows with
$|T_{A,0} - T_{B,0}|$. Nothing else in this derivation depends on that approximation, so it is
worth isolating here rather than letting it hide inside the algebra.
:::

### Newton's law of cooling gives the relaxation in time

Energy conservation fixes *where* the pair ends up but says nothing about *how fast*. The
missing ingredient is a statement about the rate of heat flow:

:::{admonition} Newton's law of cooling
:class: empirical-law
The rate of heat flow between two bodies in contact is proportional to their temperature
difference, and flows from the hotter body to the colder one:

$$
\frac{\delta Q_{\text{into }A}}{dt} = \kappa (T_B - T_A) ,
$$

for some positive constant $\kappa$ (the thermal conductance of the contact, in $\mathrm{W/K}$).
Like the ideal gas law, this is an empirical statement about how real materials behave near
equilibrium, not a theorem — it is the linear-response idealisation of heat conduction, and it
fails once the temperature difference is large enough that $\kappa$ itself starts to depend on
$T_A - T_B$.
:::

Combining this with $C_A\,dT_A = \delta Q_{\text{into }A}$ and the mirror statement for B,

$$
\frac{dT_A}{dt} = \frac{\kappa}{C_A}(T_B - T_A) ,
\qquad
\frac{dT_B}{dt} = \frac{\kappa}{C_B}(T_A - T_B) .
$$

Subtracting the second equation from the first gives a single closed equation for the gap
$\Delta T = T_A - T_B$:

$$
\frac{d(\Delta T)}{dt} = -\kappa\left(\frac{1}{C_A} + \frac{1}{C_B}\right)\Delta T
= -\frac{\Delta T}{\tau} ,
\qquad
\tau = \frac{C_A C_B}{\kappa\,(C_A + C_B)} .
$$

This is a first-order linear ODE with the standard exponential solution:

$$
\boxed{\; T_A(t) - T_B(t) = \big(T_{A,0} - T_{B,0}\big)\, e^{-t/\tau} \;}
$$

Note what determines $\tau$: a *larger* thermal conductance $\kappa$ (better contact) makes
$\tau$ *smaller* (faster equilibration), while larger heat capacities make $\tau$ *larger*
(more thermal mass to move). Both bodies converge on $T_{\text{eq}}$ from the boxed formula
above — the shape of the approach is exponential, but the destination was already fixed by
energy conservation alone.

:::{admonition} The discrete simulation realises exactly this law
:class: numerical-observation
The quantum-hopping model in the laboratory is not merely *consistent* with the exponential
law above — for that specific mechanism, the expected gap $T_A(t) - T_B(t)$ follows it
**exactly**, with no approximation beyond replacing a step count by continuous time. The full
argument is in the [Advanced section](#01-equilibrium-advanced): the probability that a
quantum leaves body A is exactly proportional to how many quanta A currently holds, which
makes the expected change in A's quanta an exactly linear function of the current state, at
every step, not merely close to equilibrium.
:::

(01-equilibrium-verify)=
## Verify computationally

Deriving a formula and trusting it are different things. The laboratory checks the result
several ways, and each check is also a test in the project's test suite, so the claims on this
page cannot silently rot.

**1. Energy conservation.** Every step in the simulation only relabels which body owns one
quantum, so the total number of quanta — and hence the total energy — is conserved to the
last bit, not approximately.

**2. The equilibrium temperature.** Averaged over many independent runs, the long-time
temperature of body A converges on $T_{\text{eq}} = (C_A T_{A,0} + C_B T_{B,0})/(C_A + C_B)$,
within the statistical error of the measurement.

**3. The relaxation curve.** The mean temperature gap across independent runs, measured one
relaxation time in, matches the closed-form $e^{-t/\tau}$ prediction — not just its shape, but
its value.

**4. Convergence with system size.** Run-to-run scatter around the analytic curve shrinks as
the two bodies grow, the same $N$-dependent steadying met throughout this course.

:::{admonition} A caution about what the simulation proves
:class: open-question
The discrete quantum-exchange model demonstrates that *one* simple microscopic mechanism —
random exchange, weighted by occupation — reproduces Newton's law of cooling exactly. It does
not establish that Newton's law of cooling holds for every real thermal-contact mechanism, nor
does it derive the conductance $\kappa$ of any actual material from first principles; that
requires knowing the specific physics of the contact (phonon transport, radiation, convection),
which this module deliberately does not model. Agreement here supports the macroscopic law's
plausibility; it does not prove the law the way the ODE derivation does.
:::

The one check no simulation can supply is a real thermal contact, which is what Part 6 of the
laboratory asks for: a mug of hot water, a kitchen thermometer, a reading every couple of
minutes, and a $\tau$ fitted in minutes rather than in steps.

(01-equilibrium-transfer)=
## Transfer the idea

The pattern here — two reservoirs exchanging a conserved quantity at a rate proportional to
their difference, relaxing exponentially to a weighted-average equilibrium — reappears
throughout physics and beyond it.

- **Calorimetry.** Mixing a measured mass of hot water into a measured mass of cold water and
  reading off the final temperature is a direct application of the boxed $T_{\text{eq}}$
  formula, with heat capacities in place of $C_A$, $C_B$ — the standard method for measuring
  an unknown heat capacity.
- **Forensic cooling.** A body's temperature after death follows the same exponential
  relaxation toward ambient room temperature; estimating time of death from a single
  temperature reading is exactly the inverse problem of solving $T(t) - T_{\text{room}} =
  (T_0 - T_{\text{room}})e^{-t/\tau}$ for $t$.
- **RC circuits.** A charged capacitor discharging through a resistor obeys the identical
  linear equation, with charge in place of energy and $RC$ in place of $\tau$ — the same
  mathematics wherever a quantity flows down its own difference.
- **Building heat loss.** A building's indoor temperature relaxes toward the outdoor
  temperature with a time constant set by its thermal mass and insulation — the same $\tau =
  C/\kappa$ structure, now with one "body" (outdoors) so large that its own temperature barely
  moves.

The two Einstein solids themselves also come back, three times, each visit settling something
this module has to leave open:

- **The entropy ledger (module 9).** The very trajectories the laboratory generates here are
  replayed there with an entropy ledger attached, hop by hop. That ledger answers the question
  this module poses and cannot yet answer: energy conservation fixes *where* the pair may
  settle, but says nothing about why it settles *there* rather than at some other balance. The
  answer is that the pair's total entropy climbs while a temperature difference remains and
  stops climbing exactly when that difference vanishes.
- **The partition function (module 12).** The same oscillators are handed to the machinery of
  the canonical ensemble, and the temperature map used throughout this module,
  $T = q\,\varepsilon/(n k_B)$, drops out of the partition function $Z$ alone — the same
  number, reached from a direction that assumes no equipartition.
- **Heat capacity that varies (module 16).** The Einstein solid's $C_V(T)$ is derived there,
  which is what finally pays off the constant-$C$ approximation box above: it says how large
  that approximation's error is, and at what temperature the approximation stops being safe.

:::{admonition} A word on relaxation time
:class: definition
The **relaxation time** $\tau$ of a system approaching equilibrium is the time over which a
deviation from equilibrium shrinks by a factor of $e$. It says nothing about *whether* the
system reaches equilibrium — only how fast, once it is heading there. This is the first of
several relaxation times in this course; module 8 revisits the same idea from a purely
combinatorial angle, with no rate equation in sight, and reaches the same exponential shape.
:::

(01-equilibrium-quiz)=
## Check your understanding

```{include} ../_generated/quiz-01-equilibrium.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](01-equilibrium-problems.md).

(01-equilibrium-explain)=
## Explain it in your own words

Answer in a few sentences each. These are the questions that reveal whether the ideas landed;
no number will save you.

1. A student says: "The two bodies reach the same temperature because heat stops flowing once
   they touch." Improve this sentence so that it is actually correct, and say precisely what
   was wrong with it.
2. Explain, without writing an equation, why a much larger heat capacity on one side pulls the
   equilibrium temperature toward that side's starting value.
3. Two pairs of bodies start with identical heat capacities and identical starting
   temperatures, but pair 2 has better thermal contact (a larger $\kappa$) than pair 1.
   Compare their equilibrium temperatures and their relaxation times.
4. Explain why "the two bodies are at equilibrium" does not mean the exchange of energy quanta
   between them has stopped.

(01-equilibrium-advanced)=
## Advanced: from a random hop to an exact exponential

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

The laboratory's exchange rule looks arbitrary until its consequence is traced through
exactly. Let $q_A$ and $q_B$ be the number of quanta held by bodies A and B, with $n_A$, $n_B$
their oscillator counts and $Q = q_A + q_B$ the (conserved) total. At each step, one of the $Q$
quanta is chosen uniformly at random to move, so the chance it currently belongs to A is
$q_A/Q$; it is then reassigned to a uniformly random oscillator among the $n_A + n_B$
available, landing back in A with probability $n_A/(n_A + n_B)$. The expected change in
$q_A$ over one step is therefore

$$
\mathbb{E}[\Delta q_A] = \frac{n_A}{n_A+n_B} - \frac{q_A}{Q} ,
$$

which is **exactly linear** in $q_A$ — not approximately, and not only near equilibrium,
because $Q$ never changes. A linear recursion of this form has the geometric solution

$$
\mathbb{E}[q_A(n)] - q_A^{\text{eq}} = \big(q_A(0) - q_A^{\text{eq}}\big)\left(1 -
\frac{1}{Q}\right)^{n} , \qquad q_A^{\text{eq}} = \frac{Q\,n_A}{n_A+n_B} .
$$

Converting quanta to temperatures ($T = q\,\varepsilon/(n k_B)$ for quantum size
$\varepsilon$) leaves the shape of the decay unchanged, because $T_A - T_B$ is itself a linear
function of $q_A$ at fixed $Q$. The result is

$$
\mathbb{E}[T_A(n) - T_B(n)] = \big(T_A(0) - T_B(0)\big)\left(1 - \frac{1}{Q}\right)^{n} ,
$$

which becomes the continuous exponential $e^{-n/\tau}$ once $Q \gg 1$, with
$\tau = -1/\ln(1 - 1/Q) \to Q$ — the discrete-step analogue of the Newton's-law-of-cooling
time constant, with this model's implicit conductance $\kappa = k_B / Q$ per step.

:::{admonition} A discretisation caveat
:class: model-assumption
Because $q_A$ and $q_B$ are integers, the laboratory's `from_temperatures` helper rounds to
the nearest quantum when building a state from requested starting temperatures. The realised
starting temperature therefore differs from the requested one by $O(\varepsilon / (n k_B))$ —
negligible once $n$ is large, but worth knowing about if a very small system's numbers look
slightly off from a hand calculation.
:::
