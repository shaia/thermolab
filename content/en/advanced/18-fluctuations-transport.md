---
title: Fluctuations and transport — the noise that carries heat
short_title: 18 · Fluctuations and transport
module: 18-fluctuations-transport
objectives:
  - id: OBJ-18-1
    text: Use Var(E) = k_B T^2 C_V (module 12) to measure a heat capacity from the energy fluctuations of canonical samples alone, and explain why a longer run measures the fluctuation more precisely but never makes it smaller.
  - id: OBJ-18-2
    text: Show that sigma_E/<E> ~ N^(-1/2) follows from Var(E) = k_B T^2 C_V for any system whose E and C_V are extensive, and explain why canonical and microcanonical descriptions therefore agree for macroscopic N although the identity itself holds only when the energy is free to fluctuate.
  - id: OBJ-18-3
    text: Derive the diffusion equation dP/dt = D d^2P/dx^2 as the continuum limit of an unbiased random walk, with D = l^2/(2 tau) in one dimension, stating the hypotheses (independent steps, finite variance) and naming what breaks under correlated steps.
  - id: OBJ-18-4
    text: Use the Green's function P(x,t) = (4 pi D t)^(-1/2) exp(-x^2/(4 D t)) to predict <x^2> = 2 D t and the sqrt(t) advance of a diffusion front, and distinguish diffusive spreading (slope 1 on a log-log plot of the mean squared displacement) from ballistic spreading (slope 2).
  - id: OBJ-18-5
    text: Measure D three independent ways — the slope of the mean squared displacement, a Green's-function fit to the histogram, and the integral of the velocity autocorrelation (Green–Kubo) — quote each as value ± error, and judge whether they are consistent.
  - id: OBJ-18-6
    text: Estimate the mean free path lambda = 1/(sqrt(2) n sigma), the collision rate, and the transport trio D ~ (1/3) vbar lambda, eta ~ (1/3) n m vbar lambda, kappa ~ (1/3) n c_v vbar lambda as order-of-magnitude estimates, and explain why the viscosity of a dilute gas does not depend on its density.
  - id: OBJ-18-7
    text: State the local-equilibrium assumption behind every transport coefficient, and identify when it fails (temperature or flow speed changing appreciably over a mean free path, Knudsen number lambda/L not small).
  - id: OBJ-18-8
    text: Derive the Einstein relation D = k_B T/zeta from the balance of drift and diffusion in sedimentation equilibrium, and use it with Stokes drag zeta = 6 pi eta a to obtain Avogadro's number from the Brownian motion of a bead.
---

# Fluctuations and transport

(18-fluctuations-transport-puzzle)=
## The puzzle: the noise we kept throwing away

For seventeen modules the course has treated fluctuations as noise around the signal. Module 03's
walkers scattered about their average, module 04's pressure gauge jittered, and the energy of
module 11's small system on a bath wandered up and down. Each time the lesson was the same: the
relative scatter falls as $N^{-1/2}$, so for anything macroscopic it can be averaged away and
forgotten.

Now put a drop of ink into a glass of perfectly still water, or warm one end of a metal rod, or
stir honey and watch it drag. Ink spreads with no current to carry it. Heat crosses the rod with
nothing flowing. The honey resists being sheared. Nothing pushes in any of these: there is no
pressure difference behind the ink and no wind across the rod. The only thing moving is the
molecules, at random, in exactly the motion the course has been averaging away.

And the numbers are strange. A dye molecule in water moves at over a hundred metres per second,
yet a dye cloud takes about a day to spread over a centimetre, and would need decades to cross a
metre. Module 12 adds a stranger fact still: for a system on a heat bath, the size of its energy
noise is fixed by its heat capacity, $\sigma_E^2 = \kB T^2 C_V$. The noise is a property of the
material.

:::{important} The question
How can the chaos we spent seventeen modules averaging away be what carries dye, momentum and
heat? Why does it carry them so slowly, when the molecules themselves are so fast? And if the
size of the noise is a material property, can a heat capacity be measured from noise alone?
:::

The answer adds one idea to the course: **memory**. How far a cloud of molecules spreads, how hard
a gas resists shearing and how well it conducts heat are all fixed by how long a molecule remembers
its velocity before a collision makes it forget.

(18-fluctuations-transport-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. A simulation of $N$ two-level systems on a heat bath shows the total energy fluctuating. You
   double $N$. Does the relative fluctuation $\sigma_E/\langle E \rangle$ halve, fall by a factor
   of $\sqrt{2}$, or stay the same?
2. A layer of dye at the bottom of a tall jar of set gelatin, where nothing can flow, has after one
   day coloured the gelatin up to $1\ \mathrm{cm}$ above the layer. How high will the colour reach
   after four days?
3. You pump half of the gas out of a sealed container at fixed temperature. Does the viscosity of
   the gas that remains halve, stay the same, or double?
4. You run the same simulation of a system on a bath ten times longer. Does the fluctuation of its
   energy get smaller?

:::{note} Why we ask first
The second and the fourth catch almost everyone, and the third catches physicists too: James Clerk
Maxwell predicted the answer in 1860 and found it so surprising that he measured it himself. Every
answer is collected at the end of the module.
:::

(18-fluctuations-transport-explore)=
## Explore the model

The laboratory has four explorers. The first releases a cloud of up to ten thousand random walkers
at the origin and shows its histogram at a time you choose, with the diffusion equation's
prediction drawn over it, and its mean squared displacement on linear or logarithmic axes; a switch
gives the walkers a memory of their last step. The second measures the relative energy fluctuation
of $N$ two-level systems for $N$ from $16$ to $4096$. The third estimates the mean free path,
collision rate, viscosity and thermal conductivity of helium, nitrogen or argon at the temperature
and pressure you choose, against measured values. The fourth races a diffusion front against a
front moving at a steady speed. Then the laboratory runs the experiments this module is built on:
a heat capacity read off the noise, the $N^{-1/2}$ law, the diffusion coefficient measured three
ways for walkers with and without memory, module 04's gas failing to diffuse, the transport
coefficients of real gases, and Avogadro's number from Brownian motion.

:::{figure} ../media/transport-cloud.mp4
:alt: Two plots. Left, a histogram of the positions of ten thousand random walkers, with a blue bell curve drawn over it, from x = -110 to 110 steps. At first the histogram is a narrow tall peak at the origin; as time runs from 10 to 1000 steps it spreads and flattens, and the blue curve, which is computed and not fitted, follows it throughout. Right, the mean squared displacement against time on logarithmic axes, a black curve growing along a dashed blue straight line labelled 2Dt, with an orange dot at the current time.
:width: 100%

Ten thousand independent walkers, each stepping one step length $\ell$ left or right every time
$\tau$, all released at the origin, as time runs from $10\tau$ to $1000\tau$. Left: the histogram of
their positions, one bar per reachable site, with the diffusion equation's point-source solution
for $D = \ell^2/2\tau$ drawn over it in blue — computed from $D$ and $t$, not fitted to the bars.
The cloud spreads and flattens and its area stays one. Right: the mean squared displacement on
logarithmic axes, growing along the slope-one line $2Dt$ (dashed). Its fitted slope from $100$ to
$1000$ steps is $1.005$.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** an ensemble of independent random walkers on a line, standing in for tagged molecules of a dilute gas; each walker's position, and from it its velocity, is recorded at equally spaced times.
- **Dynamics:** steps of $\pm\ell$ every $\tau$ — independent of one another, or (with memory switched on) repeating the previous step with probability $q$ and otherwise taking a fresh random step, as a molecule keeps its velocity between collisions; the estimators of $D$ use nothing but the recorded positions and velocities.
- **Boundary:** an unbounded line — no walls, so the spreading is never confined.
- **Ensemble:** many independent walkers realise the ensemble average directly; averages over walkers and over time agree by construction, because the walkers are independent.
- **Ignored:** interactions between walkers, the motion of the fluid itself (backflow, convection, drift), and any memory beyond the one-step persistence the switch provides.
- **Valid when:** times are long compared with the time a walker remembers its velocity; there are many walkers; a single step has finite variance.
- **Failure modes:** correlated steps, for which $D = \ell^2/2\tau$ is wrong; times comparable with the memory, when spreading is ballistic; any drift or convection, which adds to the mean squared displacement; walls, which stop it growing.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 18 — fluctuations and transport](/lite/lab/index.html?path=en/labs/18-fluctuations-transport.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/18-fluctuations-transport.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- In the cloud explorer, compare the histogram at $250$ steps with the one at $1000$. How much
  wider is it? How much lower is its peak?
- Switch the logarithmic axes on for the mean squared displacement, then give the walkers a strong
  memory. What happens to the slope at early times?
- In the fluctuation explorer, multiply $N$ by four. By what factor does the relative fluctuation
  fall?
- In the transport calculator, lower the pressure of nitrogen from $10^5$ to $10^3\ \mathrm{Pa}$ and
  watch the mean free path and the viscosity.

(18-fluctuations-transport-derive)=
## Derive the result

**System and boundary.** Two kinds of system. For the fluctuations: a body of fixed volume and
particle number in contact with a heat bath at temperature $T$, so that its energy is free to
fluctuate (module 11's canonical ensemble). For transport: a dilute gas, or a suspension of small
particles in a liquid, in which one species is tagged and followed; the tagged particles do not
interact with one another.

**Independent variables.** The temperature $T$, the number density $n$, the molecular mass $m$ and
size $d$; for the random walk, the step length $\ell$, the step time $\tau$ and the persistence $q$.

**Sign convention.** The course convention, $\mathrm{d}U = \dbar Q + \dbar \Won$, holds. It is
exercised in step 8: heat conducted into a rigid slab does no work, $\dbar \Won = 0$, so every
joule that crosses its face down the temperature gradient becomes internal energy,
$\mathrm{d}U = \dbar Q > 0$.

**Units.** SI throughout, with $\kB$ explicit. Walkers live on a line, so their $D$ is
one-dimensional, $\langle x^2 \rangle = 2Dt$. A real gas is three-dimensional, where
$\langle r^2 \rangle = 6Dt$ — three one-dimensional walks, one per axis, with the same $D$. The
dimension is stated beside every formula that depends on it.

**Route.** Nine steps. Read module 12's fluctuation identity as an instrument, and see why it makes
big systems steady. Take module 03's random walk to its continuum limit, which is the diffusion
equation, and solve it. Give the walker a memory of its velocity, which brings in the
Green–Kubo relation and explains both the ballistic start and the slowness of diffusion. Balance
drift against diffusion to get the Einstein relation, which turned Brownian motion into a
measurement of Avogadro's number. Then count collisions in a gas — the mean free path that module
04's model left out — and use one random flight to estimate all three transport coefficients,
before naming the assumption all of them share.

### Step 1: the noise is a heat capacity

Module 12 derived it in three lines. The canonical mean energy is $U = -\partial \ln Z/\partial\beta$,
the second derivative of $\ln Z$ is the variance of the energy, and converting from $\beta = 1/\kB T$
to $T$ gives

$$
\sigma_E^2 = \langle E^2 \rangle - \langle E \rangle^2
= \frac{\partial^2 \ln Z}{\partial \beta^2}
= -\frac{\partial U}{\partial \beta}
= \kB T^2 \, C_V .
$$

:::{admonition} Fluctuation and response (module 12)
:class: theorem
For a system with fixed levels in the canonical ensemble, the variance of the energy is

$$
\sigma_E^2 = \kB T^2 \, C_V .
$$

The left side is measured at a single temperature, by watching the energy of a system left alone.
The right side is how much its energy changes when the temperature is changed. They are equal.
:::

Module 12 drew one consequence: $C_V \ge 0$, because a variance cannot be negative. This module
draws another. The identity is an instrument. Record the energy of a system on a bath — in a
simulation, or for a nanoscale object, in a laboratory — and its heat capacity follows from the
scatter, at one temperature, with nothing heated:

$$
C_V = \frac{\sigma_E^2}{\kB T^2} .
$$

Take module 04's ideal gas, drawn canonically. Each of its $f$ quadratic degrees of freedom per
particle — three for a monatomic gas — carries an energy $\tfrac12 m v_x^2$ whose variance is
$\tfrac12(\kB T)^2$, and for independent degrees of freedom variances add. So
$\sigma_E^2 = \tfrac{f}{2} N (\kB T)^2$, and the instrument reads $C_V = \tfrac{f}{2} N \kB$:
equipartition, measured from noise.

Two warnings come with the instrument. First, the identity is canonical. A system whose energy is
fixed — microcanonical, like module 04's gas drawn with its energy rescaled to an exact value — has
no energy fluctuation at all, and the instrument would read $C_V = 0$, which is wrong. The bath is
part of the measurement. Second, the fluctuation is not an error. A longer record measures
$\sigma_E^2$ more precisely; it does not make it smaller, because it is not a property of the
record. It is $\kB T^2 C_V$.

### Step 2: why large systems look steady

$U$ and $C_V$ are extensive: for $N$ independent subsystems, or for any large system made of
weakly coupled parts, both grow in proportion to $N$. Then

$$
\frac{\sigma_E}{\langle E \rangle} = \frac{\sqrt{\kB T^2 C_V}}{U} \propto \frac{\sqrt{N}}{N} = N^{-1/2} .
$$

:::{admonition} Relative energy fluctuations fall as N^(-1/2)
:class: theorem
If $U$ and $C_V$ are both proportional to $N$, the relative energy fluctuation of a canonical
system is proportional to $N^{-1/2}$. Doubling $N$ divides it by $\sqrt{2}$.
:::

For $N$ two-level systems at $\kB T = \Delta$, where a fraction $p = 1/(e + 1) = 0.269$ of them is
excited, the ratio is $\sqrt{(1-p)/(Np)}$: $0.41$ for $16$ systems, $0.026$ for $4096$, and
$2 \times 10^{-12}$ for a mole. Module 11's advanced section found the same law for an Einstein solid
by a direct calculation; here it follows for any system from the identity alone. At a part in
$10^{12}$ no instrument can tell whether the energy is fixed (microcanonical) or merely almost
fixed (canonical), and the two ensembles give the same thermodynamics. That is the equivalence of
ensembles, and the reason the course could use whichever was convenient.

The identity holds only for the ensemble whose energy fluctuates; the agreement between ensembles
holds only for large $N$. They are compatible because the fluctuation the identity measures,
although it equals a material property, is too small to matter for anything else.

### Step 3: from random walk to the diffusion equation

Module 03's walker steps a distance $\ell$ to the left or to the right, with equal probability,
every time $\tau$. Let $P(x, t)$ be the probability of finding it at $x$ at time $t$. To be at $x$ at
time $t + \tau$ it must have been one step to either side at time $t$, and taken the step that brought
it here:

$$
P(x, t + \tau) = \tfrac12 P(x - \ell, t) + \tfrac12 P(x + \ell, t) .
$$

This is a **master equation**: a bookkeeping rule for probability, nothing more. Now look at it on
scales much longer than $\ell$ and times much longer than $\tau$, where $P$ changes smoothly, and
expand both sides by Taylor's theorem:

$$
P + \tau\, \frac{\partial P}{\partial t} + \ldots
= P + \frac{\ell^2}{2}\, \frac{\partial^2 P}{\partial x^2} + \ldots
$$

The first-derivative terms in $x$ cancel between the two sides of the walker — that is where
"unbiased" enters. Divide by $\tau$ and let $\ell$ and $\tau$ shrink together with $\ell^2/\tau$ held
fixed. The omitted terms, of order $\tau\,\partial^2 P/\partial t^2$ and
$\ell^4\,\partial^4 P/\partial x^4/\tau$, vanish in that limit, and what remains is

$$
\frac{\partial P}{\partial t} = D\, \frac{\partial^2 P}{\partial x^2},
\qquad
D = \frac{\ell^2}{2\tau} .
$$

:::{admonition} The diffusion equation is the continuum limit of a random walk
:class: theorem
If a walker's steps are independent and have finite variance — module 03's conditions for the
central limit theorem — then on scales long compared with a step, its probability density obeys
$\partial_t P = D\,\partial_x^2 P$, with $D = \ell^2/2\tau$ in one dimension. For any step distribution
with zero mean and variance $\langle s^2 \rangle$, the same expansion gives
$D = \langle s^2 \rangle / 2\tau$.
:::

The same equation holds for the number density $n(x, t)$ of many independent walkers. Look at it
from the point of view of a single plane between two sites. In one step, half the walkers just to
its left cross it to the right, and half of those just to its right cross to the left. The net flow
per unit time is half the difference, which on a smooth profile is

$$
j = -D \, \frac{\partial n}{\partial x} .
$$

That is **Fick's law**, and it explains the flux down a concentration gradient without any force.
Nothing pushes the walkers away from the crowded side; there are simply more of them there to
step across. (This is the flux of independent particles. For interacting ones, module 13 showed
that the gradient that drives the flow is the chemical potential's, not the concentration's.)
Combined with the conservation of walkers, $\partial n/\partial t = -\partial j/\partial x$, Fick's law
gives the diffusion equation again.

Both hypotheses matter. If a step depends on the one before, as in module 03's persistent walk,
the probability of being at $x$ at time $t + \tau$ depends on which way the walker was moving, and
the master equation needs a second variable; step 5 shows what the memory does to $D$. If a step
has no finite variance, as for module 03's Cauchy walker, the Taylor expansion has no second-order
term to keep, and there is no diffusion equation at all.

### Step 4: the spreading cloud, and why diffusion is slow

Release a cloud of walkers at the origin at $t = 0$. The solution of the diffusion equation that
starts as a point is the **Green's function**

$$
P(x, t) = \frac{1}{\sqrt{4\pi D t}} \exp\!\left(-\frac{x^2}{4Dt}\right) ,
$$

a Gaussian of variance $2Dt$ — module 03's central limit theorem, now with physical units. (Check
it by differentiating: $\partial_t P$ and $D\,\partial_x^2 P$ both equal
$P\,[x^2/(4Dt^2) - 1/(2t)]$.) Its mean squared displacement is

$$
\langle x^2 \rangle = 2Dt .
$$

:::{admonition} Diffusion spreads as the square root of time
:class: theorem
The diffusion equation has only one parameter, $D$, with units of length squared per time. When
the starting distribution has no length of its own — a point source, or a sharp step — every length
in the solution is therefore a multiple of $\sqrt{Dt}$: the width of a spreading cloud, and the
position of any feature of a spreading front, grow as $\sqrt{t}$. On a log-log plot the mean
squared displacement has slope $1$.
:::

A front, defined as the place where the concentration has reached a given fraction of its source,
moves the same way. A layer of dye filling $x < 0$ at $t = 0$, with clear water above it, spreads as

$$
\frac{c(x, t)}{c_0} = \frac12 \, \mathrm{erfc}\!\left(\frac{x}{2\sqrt{Dt}}\right) ,
$$

which depends on $x$ and $t$ only through $x/\sqrt{Dt}$. The quarter-strength contour sits at
$x = 0.954\sqrt{Dt}$: four times as long, twice as far.

That is why diffusion is fast over short distances and hopelessly slow over long ones. The time to
spread over a distance $L$ grows as $L^2/2D$. A small molecule in water has
$D \approx 10^{-9}\ \mathrm{m^2\,s^{-1}}$: it spreads across a $10\ \mu\mathrm{m}$ cell in about
$0.05\ \mathrm{s}$, across a centimetre in about fourteen hours, and across a metre in some
fifteen years.
Cells can rely on diffusion; animals larger than a few millimetres need blood.

:::{figure} ../media/transport-fronts.mp4
:alt: Two plots. Top, the concentration of a dye layer against height, a blue falling curve shaded underneath, starting as a sharp step at x = 0 and spreading out; a dashed blue vertical line marks where the concentration is a quarter of the source's, and a red vertical line marks a front moving at a constant speed. Bottom, the positions of the two fronts against time from 0 to 9: the red line rises straight and the blue curve rises as a square root, the two crossing at t = 1; dotted lines mark t = 1, 4 and 9.
:width: 100%

A dye layer diffusing into clear water, against a front that moves at a steady speed chosen to
match it at $t = 1$. Top: the concentration profile $\tfrac12\,\mathrm{erfc}(x/2\sqrt{Dt})$ (blue), with
the quarter-strength contour marked (dashed) and the steady front (red). Bottom: both positions
against time. The diffusive front is ahead at first; by $t = 4$ it has gone twice as far as at
$t = 1$ and the steady one four times, and by $t = 9$ three times against nine.
:::

### Step 5: memory, and the Green–Kubo relation

A real molecule does not jump: it flies. Between collisions it keeps its velocity, and its
displacement is the time integral of that velocity, $x(t) = \int_0^t v(t')\,\mathrm{d}t'$. Squaring
and averaging gives a double integral over the **velocity autocorrelation** $C(s) = \langle v(0)\,v(s)
\rangle$, the average product of the velocity now and the velocity a time $s$ later. Two limits follow
at once.

At times shorter than the memory, the velocity has not changed: $x = vt$ and
$\langle x^2 \rangle = \langle v^2 \rangle t^2$. That is **ballistic** motion, slope $2$ on a log-log
plot. At times much longer than the memory, the double integral grows linearly in $t$ (the advanced
section shows why), and its slope is fixed by the total memory.

:::{admonition} The Green–Kubo relation for diffusion
:class: theorem
For a particle whose velocity autocorrelation $C(s) = \langle v(0)\,v(s) \rangle$ decays fast enough,
the mean squared displacement grows at late times as $2Dt$ with

$$
D = \int_0^\infty \langle v(0)\, v(s) \rangle \, \mathrm{d}s
$$

in one dimension. The diffusion coefficient is the integral of the velocity memory. The proof is
in the advanced section.
:::

Apply it to two walkers and a molecule. The independent walker moves at $\pm\ell/\tau$ for one
step and then forgets: its memory is $\langle v^2 \rangle = \ell^2/\tau^2$ for one step, and the
discrete integral, the trapezoid rule over steps, is $\tfrac12\tau\,\ell^2/\tau^2$. That is
$D = \ell^2/2\tau$ again, by a different road. Module 03's persistent walker repeats its last step
with probability $q$ and otherwise takes a fresh random step, left or right, so its velocity is
correlated with the one $k$ steps later by $q^k$. The integral becomes a geometric series:

$$
D = \tau\,\frac{\ell^2}{\tau^2}\left(\frac12 + q + q^2 + \ldots\right)
= \frac{\ell^2}{2\tau}\,\frac{1 + q}{1 - q} .
$$

That is module 03's variance inflation, by another road: the hypothesis of independence broken,
and $D = \ell^2/2\tau$ wrong by exactly the memory. And a molecule that forgets its velocity
gradually, as $C(s) = \langle v_x^2 \rangle e^{-s/\tau_c}$, has $D = \langle v_x^2 \rangle \tau_c =
(\kB T/m)\,\tau_c$: thermal speed squared times the time it remembers.

This is the answer to the puzzle's second question. A molecule may be fast, but if its velocity is
forgotten after a tiny time $\tau_c$, its displacements add up like a random walk's: as $\sqrt{t}$, not
as $t$. A dye molecule in water, jostled by its neighbours, forgets its velocity in about
$10^{-13}\ \mathrm{s}$, and its hundred metres per second buy it a diffusion coefficient of order
$10^{-9}\ \mathrm{m^2\,s^{-1}}$.

The relation also says what happens with no forgetting at all. Module 04's gas has no collisions
between particles. In open space its velocities would never change, $C(s)$ would never decay, the
integral would grow without limit and the gas would spread ballistically forever. In module 04's box
a wall reverses each velocity instead, $C(s)$ turns negative, and the integral falls back to zero:
the mean squared displacement stops growing at $L^2/6$ per axis, the value for two independent
positions in a box of side $L$. Either way there is no diffusion. Its model specification promised
this failure — "particles do not interact with one another" — and here it is, measured.

:::{figure} ../media/transport-msd.mp4
:alt: Two plots. Left, the mean squared displacement of walkers with a strong memory, on logarithmic axes from 1 to 3000 steps: a black curve that first follows a red dashed line of slope 2, then bends over and follows a blue dashed line of slope 1 labelled 2Dt. Right, the running integral of the velocity autocorrelation divided by the exact D, against the cut-off K from 0 to 400: a black curve that rises steeply and levels off close to a dashed line at 1, far above a dotted line near 0.03 labelled l squared over 2 tau.
:width: 100%

Four thousand walkers that repeat their last step with probability $q = 0.95$, and otherwise step
afresh at random, so that each one remembers its velocity for about twenty steps. Left: the mean squared displacement on logarithmic
axes, with the ballistic line $\langle v^2 \rangle t^2$ (red, dashed) and the diffusive line $2Dt$
for the exact $D = (\ell^2/2\tau)(1+q)/(1-q)$ (blue, dashed). Right: the running integral of the
measured velocity autocorrelation up to a cut-off of $K$ steps, divided by that $D$. It levels off
near $1$ — $0.98$ for these walkers — where the left curve turns from slope $2$ to slope $1$; the
independent-step value $\ell^2/2\tau$ (dotted) is $39$ times too small.
:::

### Step 6: drift against diffusion — the Einstein relation

In 1905 Einstein asked what the random walk of a small particle in a liquid — the **Brownian
motion** botanists had watched since 1827 — would say about molecules. His argument needs only
an equilibrium and two fluxes.

Suspend beads of buoyant mass $m^*$ in water. Gravity pulls each with a force $F = m^* g$; the water
resists with a drag proportional to the velocity, $\zeta v$, where $\zeta$ is the **friction
coefficient**. A bead therefore sinks at the drift velocity $F/\zeta$, and the beads carry a downward
flux $nF/\zeta$. Diffusion carries an upward flux $-D\,\mathrm{d}n/\mathrm{d}z$ as they spread up
from the crowded bottom. In equilibrium the two cancel. And the equilibrium distribution is already
known: it is the barometric formula of modules 11 and 13, a Boltzmann factor in the potential
energy, $n(z) = n_0 \exp(-Fz/\kB T)$, so that $\mathrm{d}n/\mathrm{d}z = -(F/\kB T)\, n$. Zero net flux,

$$
-\frac{nF}{\zeta} + D\,\frac{F}{\kB T}\, n = 0 ,
$$

gives

:::{admonition} The Einstein relation
:class: theorem
A particle in a fluid that drifts at $F/\zeta$ under a steady force $F$ diffuses with

$$
D = \frac{\kB T}{\zeta} .
$$

The wandering of a particle left alone (a fluctuation) is fixed by how strongly the fluid resists
a push (a dissipation), with $\kB T$ as the rate of exchange. The derivation assumes linear drag and
a Boltzmann distribution in equilibrium; nothing about the particle's size or the fluid's
molecules enters.
:::

The same result follows from step 5. Drag makes a particle forget its velocity in the time
$\tau_c = m/\zeta$ it takes to stop a push, and equipartition gives $\langle v_x^2 \rangle = \kB T/m$, so
Green–Kubo gives $D = (\kB T/m)(m/\zeta) = \kB T/\zeta$. The mass cancels: a heavier bead remembers
its velocity for longer, but its thermal velocity is smaller, in exact compensation. This is the oldest and simplest
**fluctuation–dissipation relation**. Step 1 was another, read in energy: how much a system's
energy fluctuates at rest fixes how it responds when heated.

For a sphere of radius $a$ moving slowly through a liquid of viscosity $\eta$, the friction
coefficient was calculated by Stokes in 1851:

:::{admonition} Stokes drag
:class: approximation
A sphere of radius $a$ moving at speed $v$ through a liquid of viscosity $\eta$ feels a drag
$6\pi\eta a\, v$, so $\zeta = 6\pi\eta a$. It holds when the flow around the sphere is slow and
smooth (Reynolds number much less than one — for a micrometre bead in water, by a factor of about a
million) and the sphere is large compared with the liquid's molecules.
:::

Together they give the **Stokes–Einstein relation**, $D = \kB T/6\pi\eta a$, and turn it around:
measure a bead's $D$ from the spread of its displacements, $\langle x^2 \rangle = 2Dt$, with its radius,
the viscosity and the temperature known, and $\kB = 6\pi\eta a D/T$ follows. Divide it into the gas
constant $R$, measured with a balance and a pressure gauge and no reference to molecules, and

$$
N_A = \frac{R}{\kB} = \frac{RT}{6\pi\eta a D} .
$$

Jean Perrin did exactly this in 1908 and 1909, with grains of gamboge resin less than a micrometre
across, and found $N_A$ near $7 \times 10^{23}$ per mole. Agreement within tens of percent with
values from the viscosity of gases, from radioactivity and from the blue of the sky persuaded the
last sceptics that atoms are real. Perrin received the 1926 Nobel Prize in Physics for his work on
the discontinuous structure of matter.

### Step 7: collisions — the mean free path

For a gas, the forgetting is done by collisions, and they can be counted. Model the molecules as
hard spheres of diameter $d$. Two of them collide when their centres pass within $d$ of each other,
so a molecule sweeps out a cylinder of cross-section $\sigma = \pi d^2$, the **collision
cross-section**, and hits every centre inside it. Moving at the mean relative speed — which for two
Maxwell–Boltzmann molecules is $\sqrt{2}$ times the mean speed $\bar v = \sqrt{8\kB T/\pi m}$, because
the targets move too — it collides $\nu = \sqrt{2}\, n\sigma\bar v$ times per second, and flies on
average

$$
\lambda = \frac{\bar v}{\nu} = \frac{1}{\sqrt{2}\, n\sigma}
$$

between collisions: the **mean free path**.

:::{admonition} The mean free path and collision rate of a dilute gas
:class: approximation
For hard spheres of cross-section $\sigma = \pi d^2$ at number density $n$, in three dimensions,
$\lambda = 1/(\sqrt{2}\, n\sigma)$ and the collision rate is $\nu = \bar v/\lambda$. Real molecules are
not hard spheres, and $d$ depends on what measures it, so both are estimates to a factor of order
one.
:::

The molecular size can come from somewhere this module has not used: module 02's van der Waals
$b$, the excluded volume per molecule, which is half a sphere of radius $d$ around each molecule,
$b = \tfrac{2\pi}{3} d^3$. Module 02 obtained $b$ from the critical point. For nitrogen, with
$T_c = 126.19\ \mathrm{K}$ and $P_c = 3.396\ \mathrm{MPa}$, it gives $d = 0.31\ \mathrm{nm}$. At
$0\,{}^\circ\mathrm{C}$ and one atmosphere, where $n = 2.69 \times 10^{25}\ \mathrm{m^{-3}}$, a nitrogen
molecule then flies

$$
\lambda = 86\ \mathrm{nm}
$$

between collisions — about $270$ of its own diameters and $26$ times the mean spacing between
molecules — and collides $5.3 \times 10^9$ times a second. That is module 04's dilute regime,
quantified: collisions are rare on the scale of the molecules and frequent on the scale of anything
a person can see. Module 04's model ignored them because it was asking about pressure, which does
not need them. Transport cannot do without them.

### Step 8: one random flight, three transport coefficients

A molecule between collisions is a walker whose step is a free flight. In three dimensions, the
flights have random directions and lengths spread exponentially about $\lambda$, so the mean
square of a flight is $\langle s^2 \rangle = 2\lambda^2$, a third of it along each axis. With
$\nu = \bar v/\lambda$ flights per second, step 3's $\langle s_x^2 \rangle/2\tau$ gives

$$
D = \frac{2\lambda^2/3}{2\lambda/\bar v} = \frac{\bar v\lambda}{3} .
$$

The same random flight carries more than the molecule's identity. Picture a plane at height $z$ in a
gas, with molecules crossing it in both directions. Each arrives carrying whatever it had at its
last collision, about a mean free path away. If some quantity $Q$ per molecule varies with height,
those from below bring $Q(z - \lambda)$ and those from above $Q(z + \lambda)$. In a crude count where a
sixth of the molecules move up and a sixth down, each at $\bar v$, the net flux of $Q$ is

$$
J_Q = \tfrac16 n\bar v\,\big[Q(z - \lambda) - Q(z + \lambda)\big] = -\tfrac13 n\bar v\lambda\,\frac{\mathrm{d}Q}{\mathrm{d}z} .
$$

Choose $Q$ three ways:

- $Q$ = the fraction of molecules that are tagged: the flux of tagged molecules, Fick's law with
  $D = \tfrac13 \bar v\lambda$, as from the random flight.
- $Q = m u_x(z)$, the momentum of a gas flowing along $x$ with a speed $u_x$ that changes with
  height: a flux of momentum across the plane, which is a shear stress. Its coefficient is the
  **viscosity**, $\eta = \tfrac13 n m\bar v\lambda$.
- $Q = c_v T(z)$, the thermal energy of a molecule with heat capacity $c_v$: a heat flux down the
  temperature gradient, $j = -\kappa\, \mathrm{d}T/\mathrm{d}z$, which is **Fourier's law**. Its
  coefficient is the **thermal conductivity**, $\kappa = \tfrac13 n c_v \bar v\lambda$.

:::{admonition} The transport coefficients of a dilute gas
:class: approximation
In three dimensions, for hard spheres,

$$
D \approx \tfrac13 \bar v \lambda, \qquad
\eta \approx \tfrac13 n m \bar v \lambda, \qquad
\kappa \approx \tfrac13 n c_v \bar v \lambda ,
$$

with $c_v$ the heat capacity per molecule ($\tfrac32\kB$ for a monatomic gas). These are
order-of-magnitude estimates: every molecule is given the mean speed and the mean free path, and
the factor $\tfrac13$ counts directions crudely. The careful theory changes each by a factor of
order one.
:::

Now substitute $\lambda = 1/(\sqrt{2}\, n\sigma)$:

$$
\eta \approx \frac{m\bar v}{3\sqrt{2}\,\sigma}, \qquad \kappa \approx \frac{c_v\bar v}{3\sqrt{2}\,\sigma} .
$$

The density has cancelled. Halve the number of molecules and each one flies twice as far between
collisions, carrying momentum from twice as far away: half as many carriers, each twice as
effective. The viscosity and the thermal conductivity of a dilute gas do not depend on its
pressure. Maxwell derived this in 1860, doubted it, and in 1866 measured the damping of discs
swinging in air over a wide range of pressures, down to a small fraction of an atmosphere. The
damping did not change. Both coefficients grow as $\sqrt{T}$, through $\bar v$ — the opposite of a liquid,
whose viscosity falls on heating.

In the sign convention, heat conducted into a cold rigid slab arrives down the gradient,
$\dbar Q > 0$, and with no work done, $\mathrm{d}U = \dbar Q$: the slab warms. Fourier's law says
which way and how fast; the first law says where it goes.

### Step 9: the assumption behind every coefficient

Steps 3 to 8 talked about "the temperature at height $z$" and "the flow speed at height $z$" as if a
gas with a gradient in it still had a temperature at each point. That is an assumption, and every
transport coefficient rests on it.

:::{admonition} Local equilibrium
:class: model-assumption
Transport theory assumes that every small parcel of the system is almost in equilibrium, with its
own temperature, density and flow velocity, which change smoothly from one parcel to the next. For
a gas this requires that a molecule collide many times before it meets an appreciable change: the
gradients must be gentle on the scale of a mean free path, $\lambda/L \ll 1$, where $L$ is the
length over which anything changes. The ratio $\lambda/L$ is the **Knudsen number**. When it is not
small — a gas in a vacuum chamber, in a nanometre pore, or inside the few mean free paths of a
shock wave — molecules fly from wall to wall without colliding, viscosity and conductivity stop
being properties of the gas, and this course has nothing more to say. What lies beyond is
nonequilibrium statistical mechanics: Boltzmann's transport equation, and the linear-response
theory of Kubo and Onsager, of which step 5's relation is the simplest case.
:::

At one atmosphere and room temperature $\lambda$ is about $0.1\ \mu\mathrm{m}$, and every gradient
anyone could set up in a jar is gentle. In a vacuum chamber at $10^{-4}\ \mathrm{Pa}$ the mean free
path of nitrogen is about a hundred metres, larger than any chamber. Maxwell's flat viscosity ends there:
once $\lambda$ reaches the size of the apparatus, the molecules carry momentum and energy straight
from wall to wall, and the drag on a moving surface and the heat carried off a hot wire both fall
with the pressure. Vacuum gauges of both kinds measure pressure that way.

(18-fluctuations-transport-verify)=
## Verify computationally

Every number below comes from `thermolab.transport` and `thermolab.kinetics`, run with fixed seeds;
the laboratory repeats each experiment. Simulated numbers are quoted with one standard error,
estimated from independent batches of walkers or samples, never from the residuals of a fit.

**1. A heat capacity from the noise.** Module 04's gas of $100$ argon atoms, drawn canonically
$10^4$ times at $300\ \mathrm{K}$, has an energy whose scatter reads $C_V = (1.469 \pm 0.021)\, N\kB$,
against equipartition's $1.5$. Four atoms, with each copy's net momentum removed, read
$(1.126 \pm 0.015)\, N\kB$: the fluctuations count out the three frozen degrees of freedom, and
$\tfrac32 (N-1)/N = 1.125$. The same gas drawn microcanonically reads $9 \times 10^{-30}\, N\kB$ — zero to
rounding, because nothing fluctuates. For $1000$ two-level systems, in units of $N\kB$:

| $\kB T/\Delta$ | $0.25$ | $0.42$ | $1$ | $3$ |
|---|---|---|---|---|
| from the noise, at one temperature | $0.273 \pm 0.006$ | $0.440 \pm 0.009$ | $0.200 \pm 0.004$ | $0.0279 \pm 0.0006$ |
| by heating, $\Delta U/\Delta T$ over $\pm 5\%$ | $0.288 \pm 0.003$ | $0.446 \pm 0.004$ | $0.198 \pm 0.003$ | $0.0274 \pm 0.0011$ |
| module 12's closed form | $0.283$ | $0.439$ | $0.197$ | $0.0270$ |

**2. A longer run measures the noise; it does not remove it.** At $\kB T = 0.42\,\Delta$, with
$100$, $10^3$, $10^4$ and $10^5$ samples, the standard deviation of the energy is $9.64$, $8.98$,
$8.80$ and $8.81\,\Delta$ — settling on $\sqrt{\kB T^2 C_V} = 8.80\,\Delta$ — while the uncertainty of
the mean energy falls from $0.96\,\Delta$ to $0.028\,\Delta$, and the heat capacity read off the
noise from $1.20 \pm 0.16$ to $1.001 \pm 0.005$ times the exact one.

**3. Large systems are steady.** For $N$ from $16$ to $4096$ two-level systems at $\kB T = \Delta$,
the fitted exponent of $\sigma_E/\langle E \rangle$ is $-0.502$; the relative fluctuation falls from
$0.418$ to $0.0253$.

**4. The diffusion coefficient, three ways.** Ten thousand independent walkers of $1000$ steps:
the log-log slope of the mean squared displacement from $10$ to $1000$ steps is $1.004$, and the
width at $1000$ steps is $1.986$ times that at $250$.

:::{admonition} Three measurements of D, one answer
:class: numerical-observation
For the independent walkers, whose $D$ is exactly $\ell^2/2\tau = 0.5$ in their units, the slope of
the mean squared displacement gives $0.507 \pm 0.008$, a least-squares fit of the histogram to the
Green's function at four times gives $0.496 \pm 0.014$, and the Green–Kubo integral of the velocity
autocorrelation gives $0.502 \pm 0.004$. Every pair agrees within two combined errors, and each lies
within one error of the exact value. The three read different features of the data — the cloud's
tails, its shape, and its velocities without any positions — so their agreement checks the
estimators and the derivation against each other. The velocity route is the most precise here for
a reason worth knowing: every step is exactly $\pm\ell$, so $C(0) = \ell^2/\tau^2$ carries no noise,
and only the lags that should be zero contribute any. For these walkers it tests that the steps
are independent; the walkers with memory (item 5) are the harder test. None of this proves anything
the derivation did not; it shows that nothing was lost in turning it into code.
:::

**5. Memory.** Walkers that repeat their last step with probability $q = 0.9$, and otherwise step
afresh at random: the log-log slope
of the mean squared displacement is $1.92$ over the first three steps and $1.04$ from $300$ to
$1000$, the velocity autocorrelation follows $q^k$ to within $0.002$, and the exact $D$ is
$(\ell^2/2\tau)(1+q)/(1-q) = 9.5$, nineteen times the independent-step formula. One run of $5000$
walkers gives $9.98 \pm 0.18$ from the mean squared displacement, $10.06 \pm 0.37$ from the histogram
and $9.51 \pm 0.06$ from the velocity integral. The first is $2.7$ errors high — the kind of
excursion one run in a hundred produces. Six independent repeats of $2000$ walkers average
$9.37 \pm 0.19$, $9.34 \pm 0.15$ and $9.49 \pm 0.04$. A single disagreement at two or three error
bars is a reason to repeat the experiment, not yet a reason to distrust a method.

**6. Module 04's box cannot diffuse.** Two hundred argon atoms in module 04's $1\ \mu\mathrm{m}$ box,
followed for $672\ \mathrm{ns}$ — about $270$ box crossings: the mean squared displacement settles at
$0.96\,L^2/6$, the velocity autocorrelation swings down to $-0.44$ of its starting value after
$2.4\ \mathrm{ns}$, about one crossing time, and its running integral rises to $0.11\,\bar v L$ and falls
back to $-0.01\,\bar v L$. No collisions, no diffusion.

**7. Against reality: the transport coefficients of gases.** The NIST Chemistry WebBook's
reference correlations — equations fitted to many measurements, with stated uncertainties of
$0.5\%$ for the viscosity of nitrogen and argon and $10\%$ for helium — against step 8's estimates
with the van der Waals diameters of step 7, at $300\ \mathrm{K}$ and $0.1\ \mathrm{MPa}$:

| | He | N$_2$ | Ar |
|---|---|---|---|
| van der Waals diameter (nm) | $0.266$ | $0.313$ | $0.294$ |
| viscosity, estimate ÷ NIST | $0.45$ | $0.95$ | $1.01$ |
| thermal conductivity, estimate ÷ NIST | $0.18$ | $0.49$ | $0.40$ |
| NIST $\kappa/(\eta c_v)$, $c_v$ per kilogram | $2.51$ | $1.95$ | $2.51$ |
| NIST viscosity, $0.1 \to 1\ \mathrm{MPa}$ | $+0.16\%$ | $+0.69\%$ | $+0.70\%$ |

:::{figure} ../media/transport-viscosity.png
:alt: The viscosity of helium (orange), nitrogen (blue) and argon (black) at 300 K against pressure on a logarithmic axis from 1 kPa to 10 MPa. Each solid curve is flat up to about 1 MPa and rises above it, by about 12 per cent at 10 MPa for nitrogen and argon and by under 2 per cent for helium; the decade from 0.1 to 1 MPa is shaded. Dashed horizontal lines mark the kinetic estimates: almost on the nitrogen and argon curves, and well below the helium curve.
:width: 85%

The viscosity of helium (orange), nitrogen (blue) and argon (black) at $300\ \mathrm{K}$ from
$1\ \mathrm{kPa}$ to $10\ \mathrm{MPa}$, from the NIST Chemistry WebBook's reference correlations,
with the kinetic estimate $m\bar v/(3\sqrt{2}\,\sigma)$ for each (dashed). Across the shaded decade
from $0.1$ to $1\ \mathrm{MPa}$ — a tenfold change of density — each changes by less than one per
cent; nitrogen and argon rise by about $12\%$ by $10\ \mathrm{MPa}$, where the gas is no longer
dilute. Below $0.1\ \mathrm{MPa}$ the curves are flat by construction, the dilute-gas form the
correlations assume.
:::

:::{admonition} The viscosity of a dilute gas does not depend on its pressure
:class: empirical-law
Measured from Maxwell's swinging discs in 1866 to the reference correlations of today, the
viscosity of a dilute gas at fixed temperature is independent of its pressure, from well below an
atmosphere to about ten — until the mean free path reaches the size of the apparatus at low
pressure, or the gas stops being dilute at high pressure. Kinetic theory predicted it before it was
measured.
:::

Read the table honestly. The density independence is the robust prediction, and it holds. The
estimates themselves are good to a factor of order one, and their near-perfect agreement for
nitrogen and argon is partly luck: the careful theory's coefficient is about $1.5$ times the crude
one (advanced section), and the van der Waals diameter happens to be smaller than a collision
diameter by about the amount that compensates. For helium the two errors add, and the estimate is
low by half. The ratio $\kappa/(\eta c_v)$ is the cleaner test, because the molecular size cancels
from it: the crude estimates give exactly $1$, and both monatomic gases give $2.51$ — the careful
theory's $\tfrac52$ — because the fastest molecules carry the most energy and also fly the furthest.
The measured self-diffusion coefficients at $0\,{}^\circ\mathrm{C}$ and one atmosphere,
$1.56 \times 10^{-5}$ (argon) and $1.72$ to $1.85 \times 10^{-5}\ \mathrm{m^2\,s^{-1}}$ (nitrogen)
(Winn 1950, Hutchinson 1949 and Winter 1951, as tabulated by Hirschfelder, Curtiss and Bird), are
$1.3$ and $1.4$ times the estimates.

**8. Against reality: Perrin's atoms.** Perrin's 1909 memoir tabulates how many of the horizontal
projections of $30$-second displacements of gamboge granules, radius $0.212\ \mu\mathrm{m}$, fell
between successive multiples of $1.7\ \mu\mathrm{m}$, as counted by his student Chaudesaigues for
two series of fifty granules.

:::{figure} ../media/transport-perrin.png
:alt: Two bar charts side by side, counts of displacements against their size from 0 to 17 micrometres in ten bins of 1.7 micrometres, for Perrin's first and second series. The bars fall from about 40 in the first bins to a few in the last; a blue line with dots, the fitted Gaussian, follows them, with a fitted mean square of 50 square micrometres on the left and 37 on the right.
:width: 100%

The sizes of the $30$-second horizontal projections of gamboge granules, radius
$0.212\ \mu\mathrm{m}$, counted in bins of $1.7\ \mu\mathrm{m}$ by Chaudesaigues for Perrin's 1909 memoir
(bars): left, the first series, $221$ projections in water at $17\,{}^\circ\mathrm{C}$; right, the
second, $205$. The blue points are the Gaussian fitted to each table by `fit_binned_gaussian_variance`,
the estimator that measured the walkers' histograms.
:::

The fit to the first series gives $\langle x^2 \rangle = 50.4 \pm 6.7\ \mu\mathrm{m}^2$, the error from
resampling the table. So $D = (8.4 \pm 1.1) \times 10^{-13}\ \mathrm{m^2\,s^{-1}}$, and with the
viscosity Perrin gives, $0.011$ poise, the Stokes–Einstein relation turns it into

$$
N_A = (6.5 \pm 0.9) \times 10^{23}\ \mathrm{mol^{-1}} ,
$$

against the value fixed since 2019 by the definition of the mole, $6.022 \times 10^{23}$. The
$\pm 0.9$ is the counting noise of $221$ numbers and nothing else, and the table supports other
honest readings: its second moment, taken from the bin centres, is $42\ \mu\mathrm{m}^2$, and its
mean $|x|$ gives $45$ — Perrin himself found $50.2$ from the mean length of the displacements. The
least-squares fit leans on one over-full bin ($35$ found between $6.8$ and $8.5\ \mu\mathrm{m}$, where
the fit expects $23$). The three readings give $N_A$ from $6.5$ to $7.8 \times 10^{23}$; the second
series, whose temperature Perrin does not give, fits to $37$ against his $45$. Two hundred and
twenty-one numbers written down by hand in 1908 weigh an atom to within about $15\%$, with a choice
of estimator that matters as much as their counting noise. Perrin's summary of seven displacement
measurements (*Atoms*, 1916, p. 123) — granule radii from $0.21$ to $5.5\ \mu\mathrm{m}$, masses
differing fifteen-thousand-fold, viscosities more than a hundredfold — gives values from $5.5$ to
$8.0 \times 10^{23}$, with a mean of $7.0 \times 10^{23}$ and a scatter of $12\%$. A number that does
not care what it is measured with is a property of the world.

**The falsifying experiments.** Each misconception this module confronts has a measurement above
that it cannot survive. "Fluctuations in a simulation are numerical error, which a longer run would
remove": a thousandfold longer run left $\sigma_E$ at $8.80\,\Delta$ (item 2), the value a heat
capacity fixes, and the noise of a single temperature measured that heat capacity as well as
heating did (item 1). "Diffusion carries particles at a steady speed": the cloud's width grew by
$1.99$ in four times the time (item 4), and a diffusion front's position depends on $x/\sqrt{Dt}$
alone (step 4). "A rarefied gas is less viscous": a tenfold change of density moved the viscosity
of nitrogen by $0.7\%$ (item 7).

(18-fluctuations-transport-transfer)=
## Transfer the idea

One idea — that how far things spread, and how much they carry, is fixed by how long their motion
is remembered — reaches back through the whole course and out into the world.

- **Back to module 03.** The diffusion equation's hypotheses are the central limit theorem's:
  independent steps of finite variance. The persistent walk's $(1 + q)/(1 - q)$, which module 03
  found in a variance, is here a Green–Kubo integral.
- **Back to module 04.** Its model specification listed "high density (particle–particle collisions
  matter)" as a failure mode. This module put numbers on the collisions it left out — $\lambda$ and
  $\nu$ — and measured the consequence: a gas without them never diffuses.
- **Back to module 08.** A spreading cloud is entropy increasing in real time. A Gaussian of
  variance $2Dt$ has an entropy per walker of $\tfrac12\kB\ln(4\pi e Dt)$, up to a constant fixed by the
  unit of length, which grows as $\tfrac12\kB\ln t$ without end until a wall stops it — the second
  law, watched.
- **Back to modules 11 and 12.** The identity $\sigma_E^2 = \kB T^2 C_V$ that module 12 derived became
  a measurement, and the equivalence of ensembles that module 11 found for one solid followed for any
  system with extensive $U$ and $C_V$.
- **Back to module 13.** Fick's law is the dilute case of a more general rule: particles drift down
  the gradient of the chemical potential, $j = -(D n/\kB T)\,\partial\mu/\partial x$. With module 13's
  $\mu = \kB T\ln n + \text{const}$ it is Fick's law exactly; with interactions or an external
  potential it is not, which is how particles can flow towards higher concentration. The factor
  $D/\kB T = 1/\zeta$ is the Einstein relation.
- **Back to module 15.** Its autocorrelation time, the reason correlated samples are worth fewer
  independent ones, is a Green–Kubo sum: $N_{\mathrm{eff}} = n/2\tau$ is the same arithmetic as
  $D = \tau\,\langle v^2 \rangle(\tfrac12 + q + q^2 + \ldots)$.
- **Back to module 17.** A metal conducts heat with its electrons, at the Fermi velocity rather than a
  thermal one. Step 8's estimate with module 17's electronic heat capacity per volume,
  $\kappa \approx \tfrac13 c_{\mathrm{el}} v_F \lambda$, and copper's measured conductivity of about
  $400\ \mathrm{W\,m^{-1}\,K^{-1}}$ gives an electron mean free path of about $40\ \mathrm{nm}$, a hundred
  atomic spacings.
- **Thermal noise in electronics.** A resistor at temperature $T$ produces a fluctuating voltage
  whose mean square in a bandwidth $\Delta f$ is $4\kB T R\,\Delta f$ (Johnson and Nyquist, 1928): the
  electrical Einstein relation, with the resistance as the dissipation. It sets the floor of every
  sensitive amplifier, and has been used to measure $\kB$.
- **Double glazing.** The gap between two panes is filled with argon rather than air because argon
  conducts heat about $30\%$ less: its atoms are heavier and slower, and carry only translational
  energy. NIST's values at $300\ \mathrm{K}$, from item 7's data, are $17.8$ for argon and
  $26.0\ \mathrm{mW\,m^{-1}\,K^{-1}}$ for nitrogen, the main part of air.
- **Biology.** Diffusion supplies a cell in hundredths of a second and a millimetre of tissue in
  minutes, and
  would need months to cross a human body. Lungs, gills and blood vessels exist because diffusion is
  fast only over short distances.

Looking ahead — beyond this course:

- **Nonequilibrium statistical mechanics.** Every result here assumed local equilibrium. Without it
  come Boltzmann's transport equation, which follows the full velocity distribution of a gas;
  Onsager's reciprocal relations, which tie together the coefficients of coupled flows; and Kubo's
  linear response theory, of which the Green–Kubo relation for $D$ is the simplest case. The course
  ends at that door.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — a heat capacity from the noise.** A cluster of $1000$ atoms in contact with a
gas at $300\ \mathrm{K}$ has an energy that fluctuates with a standard deviation of
$2.27 \times 10^{-19}\ \mathrm{J}$. What is its heat capacity per atom, in units of $\kB$? What is the
relative fluctuation of its energy, if $U = 3N\kB T$?

:::{dropdown} Solution
$C = \sigma_E^2/\kB T^2 = (2.27 \times 10^{-19})^2 / (1.381 \times 10^{-23} \times 300^2) =
5.15 \times 10^{-38}/1.243 \times 10^{-18} = 4.15 \times 10^{-20}\ \mathrm{J\,K^{-1}}$, which is
$4.15 \times 10^{-23}\ \mathrm{J\,K^{-1}} = 3.0\,\kB$ per atom: Dulong and Petit, read off the noise.
$U = 3N\kB T = 1.24 \times 10^{-17}\ \mathrm{J}$, so $\sigma_E/U = 1.8\%$; for a gram of the same solid
it would be about $10^{-11}$.
:::

**Worked example 2 — what diffusion can supply.** Oxygen in water has
$D \approx 2 \times 10^{-9}\ \mathrm{m^2\,s^{-1}}$. How long does it take to spread across a cell
$10\ \mu\mathrm{m}$ wide, across $1\ \mathrm{mm}$, and across $1\ \mathrm{m}$?

:::{dropdown} Solution
$t \approx L^2/2D$: $10^{-10}/4 \times 10^{-9} = 0.025\ \mathrm{s}$; $10^{-6}/4 \times 10^{-9} =
250\ \mathrm{s}$, about four minutes; $1/4 \times 10^{-9} = 2.5 \times 10^8\ \mathrm{s}$, eight years.
Tenfold the distance is a hundredfold the time.
:::

**Worked example 3 — a vacuum chamber.** Estimate the mean free path of nitrogen at
$300\ \mathrm{K}$ and $10^{-4}\ \mathrm{Pa}$, with $d = 0.31\ \mathrm{nm}$, and the Knudsen number in a
chamber $30\ \mathrm{cm}$ across.

:::{dropdown} Solution
$n = P/\kB T = 10^{-4}/(1.381 \times 10^{-23} \times 300) = 2.4 \times 10^{16}\ \mathrm{m^{-3}}$ and
$\sigma = \pi d^2 = 3.0 \times 10^{-19}\ \mathrm{m^2}$, so
$\lambda = 1/(\sqrt{2}\, n\sigma) = 97\ \mathrm{m}$ and $\lambda/L \approx 300$. A molecule crosses the
chamber hundreds of times between collisions with other molecules: the gas has no viscosity in the
sense of step 8, and its "flow" is molecules flying from wall to wall.
:::

**Worked example 4 — the viscosity of argon.** Estimate the viscosity of argon at $300\ \mathrm{K}$
from step 8, with $m = 6.63 \times 10^{-26}\ \mathrm{kg}$ and the van der Waals diameter
$d = 0.294\ \mathrm{nm}$, and compare with the measured $22.7\ \mu\mathrm{Pa\,s}$.

:::{dropdown} Solution
$\bar v = \sqrt{8\kB T/\pi m} = \sqrt{8 \times 1.381 \times 10^{-23} \times 300/(\pi \times 6.63 \times
10^{-26})} = 399\ \mathrm{m\,s^{-1}}$ and $\sigma = \pi d^2 = 2.72 \times 10^{-19}\ \mathrm{m^2}$, so
$\eta = m\bar v/(3\sqrt{2}\,\sigma) = 2.65 \times 10^{-23}/1.15 \times 10^{-18} = 2.3 \times 10^{-5}\
\mathrm{Pa\,s}$. Within a per cent of the measurement — more closely than the method deserves, as
item 7 of the verification explains.
:::

**Worked example 5 — a bead under the microscope.** A bead of radius $0.50\ \mu\mathrm{m}$ wanders in
water at $293\ \mathrm{K}$, viscosity $1.00 \times 10^{-3}\ \mathrm{Pa\,s}$. Find its $D$, the
root-mean-square displacement along one axis in $30\ \mathrm{s}$, and the time it needs to wander
$1\ \mathrm{mm}$.

:::{dropdown} Solution
$D = \kB T/6\pi\eta a = 4.05 \times 10^{-21}/9.42 \times 10^{-9} = 4.3 \times 10^{-13}\
\mathrm{m^2\,s^{-1}}$. In $30\ \mathrm{s}$, $\sqrt{2Dt} = 5.1\ \mu\mathrm{m}$ — five bead diameters,
easy to see in a microscope. To wander $1\ \mathrm{mm}$ it needs $t = x^2/2D = 1.2 \times
10^6\ \mathrm{s}$, about two weeks.
:::

:::{note} Your predictions, revisited
1. **It falls by $\sqrt{2}$.** $\sigma_E$ grows as $\sqrt{N}$ and $\langle E \rangle$ as $N$, because
   variances of independent parts add. See step 2 and item 3.
2. **To $2\ \mathrm{cm}$, not $4$.** Every feature of a diffusion front sits at a fixed multiple of
   $\sqrt{Dt}$: four times as long, twice as far. See step 4. (In water left to itself, convection
   would carry the dye far faster; gelatin is what makes the experiment one of diffusion.)
3. **It stays the same.** Half as many molecules, each flying twice as far between collisions; the
   density cancels. See step 8 and item 7.
4. **No.** A longer run measures the fluctuation more precisely; the fluctuation itself is
   $\sqrt{\kB T^2 C_V}$, a property of the system on its bath. See item 2.
:::

(18-fluctuations-transport-quiz)=
## Check your understanding

```{include} ../_generated/quiz-18-fluctuations-transport.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](18-fluctuations-transport-problems.md).

(18-fluctuations-transport-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A skeptic says that the energy fluctuation in a simulation is numerical error and will vanish if
   the simulation is run long enough. Convince them otherwise, using a measurement they could make.
2. A dye front slows down as it advances, although nothing slows the molecules. Explain why.
3. Why does removing half of a gas leave its viscosity unchanged? Explain it in terms of what a
   single molecule does.
4. The course began by asking how macroscopic order emerges from microscopic chaos. In what sense
   does this module say the chaos is not merely tolerated by the order but does the work?

(18-fluctuations-transport-advanced)=
## Advanced: the Green–Kubo relation, and the careful coefficients

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It proves the Green–Kubo relation that
step 5 stated, works out the persistent walk exactly, and says what the careful theory changes in
step 8's coefficients.
:::

### Where the Green–Kubo relation comes from

Write the displacement as the integral of the velocity and square it:

$$
\langle x(t)^2 \rangle = \int_0^t \!\! \int_0^t \langle v(t_1)\, v(t_2) \rangle \,\mathrm{d}t_1\,\mathrm{d}t_2 .
$$

In a steady state the correlation depends only on the separation, $\langle v(t_1)\, v(t_2) \rangle =
C(t_1 - t_2)$, and $C$ is even. The integrand is constant along every diagonal of the square
$[0, t]^2$, and the diagonal at separation $s$ has length proportional to $t - s$, so

$$
\langle x(t)^2 \rangle = 2\int_0^t (t - s)\, C(s)\,\mathrm{d}s ,
\qquad
\frac{\mathrm{d}\langle x^2 \rangle}{\mathrm{d}t} = 2\int_0^t C(s)\,\mathrm{d}s .
$$

At short times $C(s) \approx C(0) = \langle v^2 \rangle$ and $\langle x^2 \rangle \approx \langle v^2
\rangle t^2$. At long times the slope tends to $2\int_0^\infty C(s)\,\mathrm{d}s$, which is $2D$,
provided the integral converges — provided the memory dies faster than $1/s$. For velocities that
are constant over steps of length $\tau$ the same argument, with sums for integrals, gives
$D = \tau\,[\tfrac12 C(0) + C(1) + C(2) + \ldots]$ exactly: the trapezoid rule is no approximation
there, which is why the laboratory's third estimate needs no correction.

The proviso is not a formality. In 1970 Alder and Wainwright found, in computer simulations of hard
disks and spheres, that a tagged particle's velocity memory in a dense fluid does not die
exponentially: it decays as a power, $s^{-d/2}$ in $d$ dimensions, because the particle's own
momentum, shared with the fluid around it, comes back to it as a slowly spreading vortex. In three
dimensions $s^{-3/2}$ is integrable and $D$ exists. In two it is $1/s$, the integral diverges
logarithmically, and a two-dimensional fluid strictly has no diffusion coefficient at all.

### The persistent walk, exactly

For module 03's persistent walk, $C(k) = (\ell/\tau)^2 q^{|k|}$, and the double sum can be done in
closed form:

$$
\langle x_n^2 \rangle = \ell^2\left[n\,\frac{1 + q}{1 - q} - \frac{2q\,(1 - q^n)}{(1 - q)^2}\right] .
$$

For $n \ll 1/(1-q)$ it is $n^2\ell^2$, ballistic; for $n \gg 1/(1-q)$ it is a straight line of slope
$2D\tau$ with $D = (\ell^2/2\tau)(1+q)/(1-q)$, offset below the origin by $2q\ell^2/(1-q)^2$. That
offset is why `d_from_msd` fits the slope of the late-time line with a free intercept rather than
dividing $\langle x^2 \rangle$ by $2t$, and why `d_from_histogram` fits the growth of the variance
between snapshots rather than its value at one. The crossover from slope $2$ to slope $1$ sits at
about twice the memory time $\tau/(1-q)$: for $q = 0.9$ the log-log slope falls through $1.5$ at
$21$ steps.

### What the careful theory changes

Step 8's argument gives every molecule the mean speed and the mean free path. Chapman and Enskog,
solving Boltzmann's transport equation for hard spheres to first order, gave the careful results:

$$
\eta = \frac{5}{16 d^2}\sqrt{\frac{m\kB T}{\pi}} , \qquad
\kappa = \frac52\,\eta\, \frac{c_v}{m} , \qquad
D = \frac{3}{8 n d^2}\sqrt{\frac{\kB T}{\pi m}} .
$$

At the same diameter these are $1.47$, $3.7$ and $1.77$ times step 8's estimates. The viscosity
keeps its independence of the density; the thermal conductivity's extra factor $\tfrac52$ — the
measured $2.51$ of item 7 for helium and argon — comes from the fastest molecules carrying both the
most energy and the longest flights. Fitted to the measured viscosity at $300\ \mathrm{K}$, the
Chapman–Enskog formula gives hard-sphere diameters of $0.215\ \mathrm{nm}$ for helium,
$0.370\ \mathrm{nm}$ for nitrogen and $0.358\ \mathrm{nm}$ for argon, against the van der Waals
values $0.266$, $0.313$ and $0.294\ \mathrm{nm}$ — larger for nitrogen and argon, smaller for
helium. A molecule has no single size. The van der Waals $b$ is fitted at the critical point, where
the attraction between molecules matters as much as their repulsion; the viscosity probes the
repulsive core in collisions at room-temperature energies. Neither is a hard-sphere diameter, because
molecules are not hard spheres, and each measurement of $d$ reports the size its own process sees.
