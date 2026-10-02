---
title: Phase coexistence
short_title: 14 · Phase coexistence
module: 14-coexistence
objectives:
  - id: OBJ-14-1
    text: Identify the segment of a sub-critical van der Waals isotherm where (dP/dv)_T > 0, explain why module 09's stability criterion forbids it, and locate the spinodal points where (dP/dv)_T changes sign.
  - id: OBJ-14-2
    text: State the coexistence conditions — equal T, equal P and equal mu between the two phases — and derive the Maxwell equal-area construction as a theorem by integrating d mu = v dP along the isotherm between the coexisting states.
  - id: OBJ-14-3
    text: Compute (P_sat, v_liq, v_gas) at a given T for a van der Waals fluid and use the lever rule x_gas = (v - v_liq)/(v_gas - v_liq) to find the phase fractions of a mixed state.
  - id: OBJ-14-4
    text: Derive the Clausius–Clapeyron equation dP_sat/dT = L/(T (v_gas - v_liq)) from mu equality along the coexistence curve, and use it to predict how the boiling point moves with the ambient pressure.
  - id: OBJ-14-5
    text: Compute the latent heat L = T (s_gas - s_liq) from the van der Waals model, and extract the latent heat of water from published P_sat(T) data by a Clausius–Clapeyron fit, with an error estimate and the fit's own assumptions named.
  - id: OBJ-14-6
    text: State the Gibbs phase rule F = C - P + 2, derive it by counting mu-equality constraints, and read F off each feature of a one-component phase diagram (area, curve, triple point, critical point).
  - id: OBJ-14-7
    text: Distinguish the binodal from the spinodal, explain why superheated and supercooled states between them are real but nucleation-limited, and state what the mean-field van der Waals model can and cannot say about them.
---

# Phase coexistence

(14-coexistence-puzzle)=
## The puzzle: who decides where the flat line goes?

Module 02 ended on a cliff-hanger. Below its critical temperature the van der Waals isotherm
does something no gas has ever been seen to do: between two points it *rises* as the volume
grows, so that squeezing the fluid would *lower* its pressure. Module 09 has since named the
crime. A state with $(\partial P/\partial v)_T > 0$ has a negative compressibility, its entropy
surface is convex there instead of concave, and the smallest fluctuation would tear it apart.
The segment between the loop's minimum and its maximum cannot be an equilibrium state of
anything.

Real carbon dioxide does something else entirely.

:::{figure} ../media/phases-wiggle-vs-data.png
:alt: Pressure against volume per particle on a logarithmic axis. Blue dots, the measured carbon dioxide isotherm at 280 kelvin, fall steeply at small volume, run dead flat across the middle at about 4.2 megapascals, and fall again at large volume. The black curve, the bare van der Waals isotherm at the same temperature, follows the data at both ends but between them dips and rises in a loop. A red horizontal line cuts the loop at about 5.3 megapascals.
:width: 100%

Carbon dioxide at $280\ \mathrm{K}$, well below its critical temperature of $304\ \mathrm{K}$. Blue dots:
the measured isotherm of module 02. Black: the bare van der Waals equation with $a$ and $b$ fitted
to the critical point. Red: the horizontal line this module will put through the loop. The data
do not loop. They run perfectly flat from $v = 0.4\,v_c$ to $3\,v_c$ at one pressure, because
across that whole range the cylinder holds liquid and vapour side by side, and compressing it
turns vapour into liquid without changing the pressure at all. The model's line sits $26\%$ too
high — the model is quantitatively poor for this substance — but it is the *right kind* of
answer, and this module is about why.
:::

So nature replaces the loop with a flat line. But the model offers a continuum of horizontal
chords through the loop, one for every pressure between the loop's minimum and its maximum.
Pick one too high and liquid sits in the cylinder next to vapour at a pressure the liquid
"prefers"; pick one too low and the vapour does. Something physical selects exactly one.

:::{important} The question
Between the loop's minimum and its maximum there are infinitely many horizontal lines. What law
of physics picks the one that nature draws — and is it a law, or a drawing rule?
:::

The answer is the payoff of the last three modules together. Two phases in a cylinder exchange
energy, volume and *particles*, so by modules 09 and 13 they must agree on $T$, on $P$ and on
the chemical potential $\mu$. The third condition is the one that chooses the line, and it does
so through module 13's Gibbs–Duhem relation: integrate $\mathrm{d}\mu = v\,\mathrm{d}P$ along
the model isotherm from the liquid state to the gas state, demand that $\mu$ come back to the
same value, and the famous "equal areas" fall out as a theorem. From that one line everything
else in the module follows: the fractions of liquid and vapour in a half-full cylinder, the slope
of the boiling curve, the latent heat, the number of things you can vary with two phases present
— and why water boils at $71\,{}^\circ\mathrm{C}$ on the top of Everest.

(14-coexistence-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. Where does the flat line sit: at the top of the loop, at the bottom, or somewhere forced by a
   rule? If a rule, what kind of rule — sketch where you think the line goes and say why.
2. Water boils on a mountain $3000\ \mathrm{m}$ high, where the air pressure is about $0.7$ of
   its sea-level value. Does it boil above $100\,{}^\circ\mathrm{C}$, below, or at exactly
   $100\,{}^\circ\mathrm{C}$?
3. A kettle is at a rolling boil with a thermometer in the water. The burner is turned up to
   double the heat. What does the thermometer do over the next minute?
4. A strong sealed container is half full of liquid carbon dioxide with its vapour above it, and
   is heated past the critical temperature. Does the liquid boil away? Does the vapour condense?
   Or does something stranger happen?

:::{note} Why we ask first
Questions 2 and 3 are the ones most people get wrong, and for the same reason: they picture
boiling as a property of water alone, with "$100\,{}^\circ\mathrm{C}$" written on the molecule.
Every answer is collected at the end of the module.
:::

(14-coexistence-explore)=
## Explore the model

The laboratory reopens module 02's sub-critical isotherm and lets you drag the temperature. For
each temperature it draws the loop, marks the two points where its slope changes sign, puts the
flat line through it with the two cut-off lobes shaded, and shows the chemical potential along
the isotherm plotted against the pressure, which crosses itself at exactly the line's height. It
then assembles the line's height at every temperature into the pressure–temperature diagram,
walks a state point across the flat segment to watch the liquid fraction follow the lever rule,
and finally fits the published vapour-pressure curve of water to extract its latent heat.

:::{figure} ../media/phases-maxwell.mp4
:alt: Two panels. Left, pressure against volume in units of the critical point. A black isotherm loops down and up between a steep liquid branch and a long gas tail; a red horizontal line cuts the loop, with the lobe below the line shaded blue and the lobe above it shaded red, and two orange dots mark the loop's minimum and maximum; a grey dashed dome is the coexistence curve. Right, the chemical potential along the same isotherm plotted against pressure traces a narrow swallowtail loop that crosses itself at a red dot, with a dotted line dropping from the crossing to the pressure axis. As the temperature rises toward the critical value both loops shrink and the whole construction collapses onto one point.
:width: 100%

One van der Waals isotherm as its temperature rises from $0.86\,T_c$ toward $T_c$. Left: the
loop (black), the flat line at the saturation pressure $P_{\mathrm{sat}}$ (red) cutting off two
lobes, blue below the line and red above it, which have equal areas at every temperature; the
orange dots are the spinodal points, where the slope $(\partial P/\partial v)_T$ changes sign;
the grey dashed dome is the locus of the line's two ends over all temperatures, the coexistence
curve, with the critical point at its top. Right: the chemical potential along the isotherm,
plotted against the pressure, as a loop with a self-crossing; the crossing (red dot) sits at
exactly $P_{\mathrm{sat}}$. As $T \to T_c$ the lobes shrink, the two ends of the line approach
each other as $\sqrt{1 - T/T_c}$, and the construction collapses onto the critical point.
:::

:::{figure} ../media/phases-coexistence.mp4
:alt: Two panels. Left, pressure against volume with a logarithmic volume axis: a grey dome shaded light blue, an orange dotted inner dome, a black isotherm passing through the dome, and a red flat line whose two ends ride on the dome. Right, pressure against temperature: a red curve traced from lower left toward a hollow circle at the critical point as a red dot climbs it. As the temperature rises the flat line on the left shortens and the dot on the right climbs until it reaches the circle, where the curve stops.
:width: 100%

The coexistence point climbing the boiling curve. Left: the $P$–$v$ plane with the binodal
(grey dome, shaded): every point inside it is a mixture of liquid and vapour, and the flat line
(red) at the current temperature spans it; the inner dotted orange dome is the spinodal, the
locus of the loop's minima and maxima, inside which no single phase can exist at all. Right:
the same red point in the $P$–$T$ plane. Its path is the saturation curve $P_{\mathrm{sat}}(T)$
— the boiling curve of the substance — and it *ends* at the critical point (hollow circle),
beyond which there is no line to cross and no distinction between liquid and gas.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** one van der Waals fluid — fixed $N$, constants $a$ and $b$ fitted to the substance's critical point — described by $(P, v, T)$, which below $T_c$ splits at coexistence into two homogeneous phases sharing $T$, $P$ and $\mu$.
- **Dynamics:** none. Every rendered state is an equilibrium state; moving the temperature re-solves the equilibrium conditions.
- **Boundary:** closed to matter. $T$ and, where asked, the total volume per particle or the pressure are set from outside; $P_{\mathrm{sat}}$ and the two coexisting volumes are solved for.
- **Ensemble:** not applicable — macroscopic thermodynamics on a mean-field equation of state.
- **Ignored:** interfaces and surface tension (the two phases meet at no cost); nucleation kinetics, which decide how long a metastable state survives; any solid phase; fluctuations near the critical point.
- **Valid when:** moderate densities and one component, for the structure of the answer — the flat line, the lever rule, Clausius–Clapeyron, $L \to 0$ at $T_c$; the numbers are those of the model, which for real substances are off by tens of percent near $T_c$ and by factors far below it. Metastable branches are statements of existence, not of lifetime.
- **Failure modes:** near $T_c$ the model's exponents are wrong (the shrinking of $v_g - v_l$ as $(1 - T/T_c)^{1/2}$ is module 15's story); deep sub-critical liquids, where the model misses real liquid structure; and there is no triple point, because the model has no solid.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 14 — phase coexistence](/lite/lab/index.html?path=en/labs/14-coexistence.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/14-coexistence.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Slide the temperature up toward $T_c$ and watch what happens to the two shaded lobes, to the
  distance between the ends of the flat line, and to the loop in the $\mu$–$P$ panel.
- Toggle the $\mu$–$P$ loop on, and check where it crosses itself against the height of the line.
- Walk the state point across the flat segment and watch the liquid fraction. Stop halfway
  and ask what, physically, is in the cylinder.
- Fit the water data over a narrow window of temperatures and over a wide one, and see which
  gives the latent heat closer to the tabulated value at $100\,{}^\circ\mathrm{C}$ — and why.

(14-coexistence-derive)=
## Derive the result

**System and boundary.** A fixed amount of one substance in a cylinder with a piston, held at
temperature $T$ by a bath, and free to separate into two homogeneous parts — a liquid and a
gas — that can exchange energy, volume and particles with each other across their common
surface. Interfaces cost nothing: the two phases are treated as two bulk systems in contact.

**Independent variables.** Per particle: the volume $v = V/N$, the entropy $s$, the energy $u$,
and the pressure and chemical potential as functions of them. Subscripts $\ell$ and $g$ mark the
liquid and the gas.

**Sign convention.** The course convention holds, $\mathrm{d}U = \dbar Q + \dbar \Won$, with
$\dbar \Won = -P\,\mathrm{d}V$ along the flat line; it enters only in step 6, where the latent
heat is a heat. Everything else below is a statement about state functions, and every
differential is an exact $\mathrm{d}$.

**Route.** Seven steps. Module 09's stability criterion condemns the loop; modules 09 and 13
give the three coexistence conditions; the third of them, integrated along the isotherm with
Gibbs–Duhem, is the equal-area theorem; the lever rule follows from counting particles;
differentiating $\mu$ equality *along* the boiling curve gives Clausius–Clapeyron; the model's
entropy gives the latent heat, twice; and counting constraints gives the phase rule.

### Step 1: the loop is forbidden, and where it ends

:::{admonition} The van der Waals equation of state
:class: model-assumption
Module 02's model, restated: a fluid of particles with an excluded volume $b$ and a mean
attraction that lowers the pressure by $a/v^2$,

$$
P = \frac{\kB T}{v - b} - \frac{a}{v^2} ,
$$

with critical point $v_c = 3b$, $\kB T_c = 8a/(27b)$, $P_c = a/(27 b^2)$. It is a mean-field
model: every particle feels the average of all the others. Nothing in this module tests the
equation against reality except the places where it is said to fail.
:::

Module 09 showed that a concave entropy surface is the condition for a stable equilibrium, and
that one of its consequences, read through module 10's potentials, is

:::{admonition} Mechanical stability
:class: theorem
A homogeneous phase is stable against splitting only where its isothermal compressibility is
positive:

$$
\left(\frac{\partial P}{\partial v}\right)_T \le 0 .
$$

A state with $(\partial P/\partial v)_T > 0$ amplifies any density fluctuation and cannot be
an equilibrium state of a homogeneous substance.
:::

Differentiate the model isotherm:

$$
\left(\frac{\partial P}{\partial v}\right)_T = -\frac{\kB T}{(v - b)^2} + \frac{2a}{v^3} .
$$

This vanishes where

$$
\kB T = \frac{2a\,(v - b)^2}{v^3} ,
$$

a condition with two solutions below $T_c$ — the loop's minimum, on the liquid side, and its
maximum, on the gas side — and none above it. The two solutions are the **spinodal points**
of the isotherm, and their locus over all temperatures is the **spinodal curve**. Between them
the isotherm is forbidden outright. Outside them the slope is negative again and the criterion
is satisfied; whether those outer segments are the *equilibrium* state is the next question,
and the answer is: not all of them.

### Step 2: the three conditions for coexistence

Let the cylinder hold $N_\ell$ particles of liquid and $N_g$ of gas. The two parts exchange
energy, volume and particles, and the whole is at fixed $T$ and $P$. Module 09's argument for
energy exchange gave $T_\ell = T_g$; its argument for a movable wall gave $P_\ell = P_g$; module
13's argument for particle exchange — maximize the total entropy over the split of $N$ at fixed
total energy — gave $\mu_\ell = \mu_g$. The same three conditions follow in one line from module
10: at fixed $T$ and $P$ the Gibbs free energy is minimal, and for two phases of one component
$G = N_\ell\,\mu_\ell(T, P) + N_g\,\mu_g(T, P)$ with $N_\ell + N_g$ fixed, which is minimal over
the split only if the two chemical potentials agree — or if one phase has vanished.

:::{admonition} Coexistence conditions
:class: theorem
Two phases of one substance coexist in equilibrium only if

$$
T_\ell = T_g , \qquad P_\ell = P_g , \qquad \mu_\ell(T, P) = \mu_g(T, P) .
$$

At a given temperature the third condition is one equation in the one unknown $P$: it fixes the
**saturation pressure** $P_{\mathrm{sat}}(T)$, the single pressure at which the two phases can
share a cylinder.
:::

The first two conditions are built into the picture of a flat line on an isotherm. The third is
the one that selects its height.

### Step 3: the equal-area theorem

Module 13's advanced section re-read the Gibbs–Duhem relation as a statement about $\mu$: per
particle, $\mathrm{d}\mu = -s\,\mathrm{d}T + v\,\mathrm{d}P$. At fixed temperature,

$$
\mathrm{d}\mu = v\,\mathrm{d}P .
$$

Now walk along the *model* isotherm from the liquid state $v_\ell$ to the gas state $v_g$,
through the loop, and add up the changes in $\mu$. The walk passes through the forbidden
segment, but $\mu(v)$ is a function the model defines at every $v$, and a line integral of a
state function does not care whether the states it passes through are stable. Along the walk,

$$
\mu_g - \mu_\ell = \int_{\ell}^{g} v\,\mathrm{d}P .
$$

Coexistence requires the left side to vanish. Integrate the right side by parts: the states at
both ends share the pressure $P_{\mathrm{sat}}$, so

$$
\int_{\ell}^{g} v\,\mathrm{d}P = \big[\,vP\,\big]_{\ell}^{g} - \int_{v_\ell}^{v_g} P\,\mathrm{d}v
= P_{\mathrm{sat}}\,(v_g - v_\ell) - \int_{v_\ell}^{v_g} P(v)\,\mathrm{d}v .
$$

:::{admonition} The Maxwell equal-area construction
:class: theorem
Given a model isotherm $P(v)$ at temperature $T < T_c$, and given that the chemical potential
along it obeys $\mathrm{d}\mu = v\,\mathrm{d}P$, the coexisting states $v_\ell < v_g$ and the
saturation pressure are fixed by

$$
P(v_\ell) = P(v_g) = P_{\mathrm{sat}} ,
\qquad
\int_{v_\ell}^{v_g} P(v)\,\mathrm{d}v = P_{\mathrm{sat}}\,(v_g - v_\ell) .
$$

The second equation says that the horizontal line at $P_{\mathrm{sat}}$ cuts the loop into two
lobes of equal area — the area of the lobe above the line equals the area of the lobe below it.
It is a consequence of $\mu_\ell = \mu_g$, not an aesthetic rule.
:::

The equation is one condition on one unknown. For a pressure between the loop's minimum and
maximum, the horizontal line cuts the isotherm three times; the outer two crossings are the
candidate liquid and gas. Raise the line and the lower lobe grows while the upper one shrinks,
so the difference of the areas is a decreasing function of $P$ and vanishes exactly once:
there is a unique $P_{\mathrm{sat}}$ at every $T < T_c$. The laboratory finds it by bisection.
The middle crossing, inside the forbidden segment, is never a state.

Two things are worth seeing in the laboratory's $\mu$–$P$ panel. Plotted against the pressure,
$\mu(v)$ along the isotherm is a curve that doubles back on itself twice — at the two spinodal
points, where $\mathrm{d}P = 0$ while $\mathrm{d}\mu = v\,\mathrm{d}P$ does too — and so
crosses itself exactly once. The crossing is at $P_{\mathrm{sat}}$: the theorem made visible.
And the two branches that continue *past* the crossing, the liquid branch above
$P_{\mathrm{sat}}$ carried on to lower pressure and the gas branch carried on to higher, are
states that satisfy the stability criterion but have the *higher* of the two available chemical
potentials. They are the **metastable** branches, and step 7 returns to them.

For the van der Waals model $\mu$ has a closed form, derived in the problem set:

$$
\mu(v, T) = -\kB T\ln\frac{v - b}{b} + \frac{\kB T\,b}{v - b} - \frac{2a}{v} + f(T) ,
$$

with $f(T)$ a function of temperature alone that drops out of any comparison at fixed $T$. So
the laboratory can find $P_{\mathrm{sat}}$ a second way, by bisecting $\mu_\ell(P) - \mu_g(P)$
directly with no areas in sight, and check that the two answers agree. They agree to rounding.

### Step 4: the lever rule

Inside the flat segment, a cylinder at total volume per particle $v$ holds a fraction
$x_\ell$ of its particles as liquid at $v_\ell$ and $x_g = 1 - x_\ell$ as gas at $v_g$. The
volumes add, $v = x_\ell v_\ell + x_g v_g$, and solving,

$$
x_g = \frac{v - v_\ell}{v_g - v_\ell} ,
\qquad
x_\ell = \frac{v_g - v}{v_g - v_\ell} .
$$

This is the **lever rule**: the state point on the flat line is a fulcrum, and the two phase
fractions are inversely proportional to the arms $v - v_\ell$ and $v_g - v$. Halfway across the
segment, $x_g = \tfrac12$ — half the particles are gas — but since $v_g > v_\ell$, by a large
factor well below $T_c$, the gas takes most of the room, and the cylinder looks mostly full of
vapour with a layer of liquid at the bottom. Nothing in the cylinder is "half evaporated": every particle is in one
phase or the other, and the two coexist.

:::{figure} ../media/phases-lever.mp4
:alt: Three panels. Left, a pressure-volume isotherm with the loop drawn dashed in grey and the real isotherm in black with its red flat segment; a blue dot slides from the steep liquid branch, along the flat line, and down the gas tail. Middle, a cylinder drawn as a tall rectangle whose height follows the volume, with a blue liquid layer at the bottom under pale yellow vapour; the liquid layer shrinks to nothing as the dot crosses the line. Right, a stacked bar of the liquid and vapour particle fractions in blue and orange rebalancing from all liquid to all vapour.
:width: 100%

A state point crossing the two-phase region at $T = 0.85\,T_c$. Left: the isotherm with the loop
dashed in grey and the equilibrium isotherm in black — flat (red) between $v_\ell$ and $v_g$ —
and the state point (blue) moving along it. Middle: the cylinder, drawn to scale in $v$, with the
liquid (blue) at the bottom and the vapour (pale) above it; the liquid occupies the volume
$x_\ell v_\ell$. Right: the particle fractions $x_\ell$ (blue) and $x_g$ (orange) from the lever
rule. Across the flat line the pressure does not move at all; only the proportions do, and
halfway across, where half the particles are liquid, the liquid is a thin layer because its
volume per particle is so much smaller.
:::

### Step 5: Clausius–Clapeyron

Step 2 fixed one pressure at each temperature. Follow it: along the boiling curve
$P_{\mathrm{sat}}(T)$ the two chemical potentials are equal at every point,
$\mu_\ell(T, P_{\mathrm{sat}}(T)) = \mu_g(T, P_{\mathrm{sat}}(T))$, so their *changes* along the
curve are equal too. Differentiate both sides along the curve with Gibbs–Duhem,
$\mathrm{d}\mu = -s\,\mathrm{d}T + v\,\mathrm{d}P$:

$$
-s_\ell + v_\ell\,\frac{\mathrm{d}P_{\mathrm{sat}}}{\mathrm{d}T}
= -s_g + v_g\,\frac{\mathrm{d}P_{\mathrm{sat}}}{\mathrm{d}T} .
$$

:::{admonition} Latent heat
:class: definition
The latent heat of vaporization, per particle, is the heat absorbed when one particle crosses
from liquid to gas at the coexistence temperature and pressure:

$$
L = T\,(s_g - s_\ell) .
$$

It is positive — the gas has the more entropy — and it is the quantity a kettle spends while the
thermometer stands still.
:::

:::{admonition} The Clausius–Clapeyron equation
:class: theorem
Along the coexistence curve of two phases of one substance,

$$
\frac{\mathrm{d}P_{\mathrm{sat}}}{\mathrm{d}T} = \frac{s_g - s_\ell}{v_g - v_\ell}
= \frac{L}{T\,(v_g - v_\ell)} .
$$

It holds for any pair of phases — liquid–gas, solid–liquid, solid–gas — with the corresponding
latent heat and volume change; it assumes only that $\mu$ is equal across the curve and that
Gibbs–Duhem holds in each phase.
:::

The slope of the boiling curve is set by the entropy the substance gains per unit of volume it
gains. For boiling, $L > 0$ and $v_g > v_\ell$, so $P_{\mathrm{sat}}$ always rises with $T$ —
hotter liquids have higher vapour pressures. Turn it around and it says how the **boiling
point** moves with pressure: a liquid boils at the temperature where $P_{\mathrm{sat}}(T)$ equals
the pressure pressing on it. Lower the pressure and the boiling point falls; raise it, in a
pressure cooker, and it rises. "$100\,{}^\circ\mathrm{C}$" is not a property of water. It is the
temperature at which water's $P_{\mathrm{sat}}$ happens to equal one atmosphere.

For a vapour dilute enough to be ideal and far less dense than the liquid, $v_g - v_\ell
\approx v_g = \kB T/P_{\mathrm{sat}}$, and the equation separates:

:::{admonition} The integrated form
:class: approximation
If the vapour is an ideal gas, $v_\ell \ll v_g$, and $L$ does not depend on temperature,

$$
\frac{\mathrm{d}\ln P_{\mathrm{sat}}}{\mathrm{d}T} = \frac{L}{\kB T^2}
\qquad\Longrightarrow\qquad
\ln P_{\mathrm{sat}} = \mathrm{const} - \frac{L}{\kB T} .
$$

A plot of $\ln P_{\mathrm{sat}}$ against $1/T$ is a straight line of slope $-L/\kB$. For water
between $0$ and $100\,{}^\circ\mathrm{C}$ the three assumptions hold to a few percent each, and
the laboratory measures what they cost.
:::

### Step 6: the latent heat of the model, two ways

The van der Waals gas has the entropy per particle (module 10, with the Sackur–Tetrode form
corrected for the excluded volume)

$$
s = \kB\left[\ln\!\big((v - b)\,n_Q\big) + \frac52\right] ,
$$

so at one temperature the two phases differ only through their free volumes $v - b$:

$$
L = T\,(s_g - s_\ell) = \kB T \ln\frac{v_g - b}{v_\ell - b} .
$$

As $T \to T_c$ the two volumes merge and $L \to 0$: above the critical temperature there is
nothing left to boil. A second route uses the first law. Along the flat line the pressure is
constant, the work done on the system in carrying one particle across is
$\dbar\Won = -P_{\mathrm{sat}}\,(v_g - v_\ell)$, and the heat is

$$
L = \dbar Q = \Delta u - \dbar\Won = (u_g - u_\ell) + P_{\mathrm{sat}}\,(v_g - v_\ell) ,
\qquad
u_g - u_\ell = a\left(\frac{1}{v_\ell} - \frac{1}{v_g}\right) ,
$$

since the model's energy per particle is $\tfrac32\kB T - a/v$ and the kinetic part cancels at
one temperature. The two expressions look nothing alike. They are equal — exactly — at the
equal-area pressure and at no other, because their difference is $\mu_g - \mu_\ell$ in disguise
(problem 2 asks you to show it). The laboratory asserts their equality to rounding; it is the
theorem of step 3 checked a third way.

### Step 7: the phase rule

How many intensive variables can be chosen freely while $P$ phases of $C$ components coexist?
Each phase has its temperature and pressure and $C - 1$ independent composition fractions, and
$T$ and $P$ are shared, so there are $2 + P(C - 1)$ knobs. Each component must have the same
chemical potential in every phase — $P - 1$ equations per component, $C(P - 1)$ in all. The
difference is the number of knobs left:

:::{admonition} Components, phases, and the number of freedoms
:class: definition
A **component** is an independently variable chemical species; a **phase** is a homogeneous
region with its own equation of state. The number of **degrees of freedom** $F$ is the number
of intensive variables that can be varied independently while the stated phases remain in
coexistence.
:::

:::{admonition} The Gibbs phase rule
:class: theorem
With $C$ components and $P$ coexisting phases,

$$
F = C - P + 2 .
$$
:::

For one component: a single phase has $F = 2$ and fills an *area* of the $P$–$T$ plane; two
phases have $F = 1$ and lie on a *curve* — fix $T$ and $P_{\mathrm{sat}}$ is determined, which
is step 2 again; three phases have $F = 0$ and meet at a *point*, the **triple point**, whose
temperature and pressure are properties of the substance ($273.16\ \mathrm{K}$ and
$611.657\ \mathrm{Pa}$ for water, by which the kelvin was defined until 2019). Four phases of one
component cannot coexist at all. The critical point is not a phase-rule feature: it is where the
liquid–gas curve stops being a boundary, because the two phases it separated have become one.

### Metastability: the states between the curves

Step 1 forbade only the segment between the spinodal points. Step 3 found that the liquid branch
continues below $P_{\mathrm{sat}}$ and the gas branch above it, each with a negative slope and a
positive compressibility, each a legitimate solution of the stability criterion — and each with
a chemical potential *higher* than the other phase's at the same $P$. Those are the states
between the **binodal** (the coexistence curve, the dome in the $P$–$v$ plane) and the
**spinodal** (the locus of the loop's extremes, the inner dome).

:::{admonition} Superheated and supercooled states
:class: model-assumption
The model says a homogeneous liquid can exist at a pressure below $P_{\mathrm{sat}}$ (or,
equivalently, at a temperature above its boiling point), and a homogeneous vapour above it, as
long as neither is pushed past its spinodal. They are *metastable*: locally stable against small
fluctuations, but with a higher $\mu$ than the phase they could become. The model says they
exist; it says nothing about how long.
:::

:::{admonition} What decides their lifetime is outside the model
:class: approximation
Turning a superheated liquid into vapour needs a bubble, and a small bubble costs surface energy
that the model set to zero. The rate at which a large enough bubble forms — **nucleation** — is
a kinetic question that depends on the surface tension, on impurities and on the walls. Water in
a smooth cup in a microwave routinely reaches $105$ to $110\,{}^\circ\mathrm{C}$ without boiling
and then erupts when disturbed; carefully cleaned water has been held to $280\,{}^\circ\mathrm{C}$
at one atmosphere, near the model's own spinodal. A bubble chamber *is* a superheated liquid,
and the track of a charged particle is the chain of bubbles it nucleates. The model describes
the states; the kinetics decide which of them you see.
:::

(14-coexistence-verify)=
## Verify computationally

Every number below comes from `thermolab.phases`, with carbon dioxide's $a$ and $b$ fitted to
its critical point as in module 02, so that $T_c = 304.13\ \mathrm{K}$. The working temperature
is $280\ \mathrm{K}$, which is $0.921\,T_c$.

**1. The anatomy of one isotherm.** At $280\ \mathrm{K}$ the loop's minimum is at
$v = 0.0955\ \mathrm{L/mol}$ and $4.121\ \mathrm{MPa}$, its maximum at $0.1862\ \mathrm{L/mol}$
and $5.693\ \mathrm{MPa}$; between those two volumes the slope is positive and the states are
forbidden. The construction puts the flat line at $P_{\mathrm{sat}} = 5.255\ \mathrm{MPa}$, with
$v_\ell = 0.0811$ and $v_g = 0.2672\ \mathrm{L/mol}$ — outside the spinodal points, as step 1
requires. The lobe above the line and the lobe below it each have area
$6.08 \times 10^{-23}\ \mathrm{J}$ per particle, $0.016\,\kB T$; they agree to one part in
$10^{10}$, the resolution of the quadrature used to check them.

**2. Equal areas is equal mu.** Bisecting the area difference and bisecting
$\mu_\ell(P) - \mu_g(P)$ — two different residuals, evaluated from two different formulas —
return the same $P_{\mathrm{sat}}$ and the same two volumes to the last digit at
$280\ \mathrm{K}$, and across the solver's whole domain, from $0.3\,T_c$ to $0.99999\,T_c$, to
better than $10^{-12}$ in the pressure. At the solution the chemical potentials of the two
phases differ by less than $10^{-15}\,\kB T$. The construction is the theorem, computed.

**3. The metastable branches.** The liquid branch can be followed below $P_{\mathrm{sat}}$ as
far as the loop's minimum, where its chemical potential has risen $0.042\,\kB T$ above the
coexistence value; the gas branch above $P_{\mathrm{sat}}$ to the maximum, $0.044\,\kB T$ above
it. They are small numbers: a superheated liquid is only slightly worse off than the vapour it
could become, which is why a seed is needed to tip it.

**4. Two latent heats.** From the entropies, $L = \kB T\ln[(v_g - b)/(v_\ell - b)] =
4.116\ \mathrm{kJ/mol}$, which is $1.77\,\kB T$ per molecule. From the first law,
$\Delta u + P_{\mathrm{sat}}\,\Delta v = 4.116\ \mathrm{kJ/mol}$; the two agree to $2 \times
10^{-16}$. Moving away from $P_{\mathrm{sat}}$ by one percent in either direction makes them
disagree, as step 6 says they must.

:::{admonition} Clausius–Clapeyron, checked
:class: numerical-observation
The slope of the model's boiling curve at $280\ \mathrm{K}$ by a central difference of
$P_{\mathrm{sat}}(T)$ with a half-step of $1\ \mathrm{mK}$ is $79.0129\ \mathrm{kPa/K}$;
$L/(T\,\Delta v)$ from the same construction is $79.0129\ \mathrm{kPa/K}$. They agree to
$10^{-12}$, and halving the step quarters the gap: the difference is the stencil's, not the
equation's.
:::

**5. The curve ends.** Sweeping the temperature toward $T_c$: at $0.75$, $0.85$, $0.95$, $0.99$
and $0.999\,T_c$ the latent heat is $6.69$, $5.46$, $3.31$, $1.51$ and $0.48\ \mathrm{kJ/mol}$,
and $(v_g - v_\ell)/v_c$ is $5.15$, $2.57$, $1.04$, $0.41$ and $0.127$ — the last three in the
ratio $\sqrt{0.05} : \sqrt{0.01} : \sqrt{0.001}$ to within a few percent. Both vanish at $T_c$,
the latent heat because the two phases it separates have become one. At $T_c$ exactly, the
construction returns $(P_c, v_c, v_c)$.

:::{figure} ../media/phases-around-critical.mp4
:alt: Two panels. Left, pressure against temperature in critical units, with the black coexistence curve ending at a hollow circle; a red dotted vertical path at 0.85 of the critical temperature crosses the curve, and a blue dotted rectangular path goes right past the critical temperature, up past the critical pressure, and back left above the curve's end. Two dots, red and blue, travel the two paths. Right, the density along each path against the path parameter: the red curve jumps vertically from about 0.3 to about 1.8 where its path crosses the curve; the blue curve rises from the same start to the same end without any jump.
:width: 100%

Two routes from gas to liquid. Left: the $P$–$T$ plane with the coexistence curve (black)
ending at the critical point (hollow circle). The red path crosses the curve at
$T = 0.85\,T_c$; the blue path goes around its end, out past $T_c$, up past $P_c$, and back.
Right: the density $\rho/\rho_c$ along each path. Where the red path crosses the curve the
density jumps by a factor of six — that is condensation. The blue path starts in the same gas
and ends in the same liquid, and its density rises steeply but *continuously* all the way.
Nothing is exhausted at the critical point and nothing boils there; the distinction between the
two phases simply stops existing, and a gas can be turned into a liquid without ever crossing
a boundary.
:::

**6. Against reality.** The model was built to reproduce the *structure* of coexistence, and
it does; its numbers are another matter. At $280\ \mathrm{K}$ the measured saturation pressure
of carbon dioxide is $4.161\ \mathrm{MPa}$ against the model's $5.255$ — $26\%$ high — and the
discrepancy grows as the temperature falls: a factor $1.04$ at $300\ \mathrm{K}$, $1.26$ at
$280$, $1.79$ at $250$ and $3.1$ at the triple point, $216.6\ \mathrm{K}$. The latent heat can
be checked with no model at all: Clausius–Clapeyron applied to the *measured* curve, whose slope
at $280\ \mathrm{K}$ is $105.2\ \mathrm{kPa/K}$, with the measured volume change read off module
02's plateau, $v_g - v_\ell = 3.30 \times 10^{-4}\ \mathrm{m^3/mol}$, gives
$L = T\,\Delta v\,\mathrm{d}P_{\mathrm{sat}}/\mathrm{d}T = 9.7\ \mathrm{kJ/mol}$ — more than
twice the model's $4.1$. A mean-field attraction $a/v^2$ fitted at the critical point is simply
too weak to hold a liquid together far below it.

:::{figure} ../media/phases-water-diagram.png
:alt: Pressure on a logarithmic axis from a tenth of a pascal to a billion pascals, against temperature from 200 to 680 kelvin. Three solid curves meet at a black dot near 273 kelvin and 600 pascals: a grey sublimation curve rising from the lower left, a blue melting curve going almost vertically upward and leaning slightly left, and a red vaporization curve rising to the right and ending at a hollow circle near 647 kelvin and 22 megapascals. The letters s, l and g mark the three regions. A red dashed curve runs above the red solid one, about fifteen times higher, and meets it only at the hollow circle.
:width: 100%

The real phase diagram of water, from the published boundary equations shipped with the
laboratory: sublimation of ice (grey), melting (blue, leaning *left* — ice melts under pressure,
which is why it contracts on melting), and vaporization (red), meeting at the triple point
(black dot, $273.16\ \mathrm{K}$, $611.657\ \mathrm{Pa}$) and the vaporization curve ending at
the critical point (hollow circle, $647.1\ \mathrm{K}$, $22.06\ \mathrm{MPa}$). The regions are
solid (s), liquid ($\ell$) and gas (g): areas have $F = 2$, the curves $F = 1$, the triple point
$F = 0$. The red dashed curve is the van der Waals boiling curve for water with $a$ and $b$ from
water's critical point: at $100\,{}^\circ\mathrm{C}$ it predicts $1.52\ \mathrm{MPa}$ instead of
$0.101$, fifteen times too high, and a latent heat of $16.7\ \mathrm{kJ/mol}$ against the real
$40.7$. Water is held together by hydrogen bonds, which a mean-field $a/v^2$ does not describe.
The model has no solid, so it has no melting curve and no triple point at all.
:::

**7. A measurement: the latent heat of water.** The laboratory fits $\ln P_{\mathrm{sat}}$
against $1/T$ to the published saturation curve of water — $31$ points from $275$ to
$425\ \mathrm{K}$, the equation behind every steam table — using the integrated form of step 5.

:::{admonition} The latent heat of water from its vapour-pressure curve
:class: numerical-observation
Over the full range, the fit gives $L = 42.49 \pm 0.13\ \mathrm{kJ/mol}$, which is
$2.36\ \mathrm{MJ/kg}$, and a boiling point at one atmosphere of $373.60\ \mathrm{K}$; the
tabulated latent heat at $100\,{}^\circ\mathrm{C}$ is $40.66\ \mathrm{kJ/mol}$,
$2.257\ \mathrm{MJ/kg}$, and the boiling point $373.12\ \mathrm{K}$. The residuals of the fit
are not random: they curve, reaching $0.07$ in $\ln P$ at the ends, because $L$ is not constant
— it falls from $45.0\ \mathrm{kJ/mol}$ at $0\,{}^\circ\mathrm{C}$ to $40.7$ at $100$ — and
the line is fitting an average. Restricted to $345$ to $405\ \mathrm{K}$ the fit gives
$41.32 \pm 0.08\ \mathrm{kJ/mol}$ and boils water at $373.26\ \mathrm{K}$: closer, with the
remaining $1.6\%$ the price of an ideal vapour and a neglected liquid volume. The quoted errors
are the fit's statistical errors and say nothing about those biases; the residuals do.
:::

The same narrow fit answers the predictions: at $0.7\ \mathrm{atm}$ water boils at
$363.5\ \mathrm{K} = 90\,{}^\circ\mathrm{C}$, at the $0.33\ \mathrm{atm}$ of Everest's summit at
$344.6\ \mathrm{K} = 71\,{}^\circ\mathrm{C}$, and in a pressure cooker at $2\ \mathrm{atm}$ at
$393.8\ \mathrm{K} = 121\,{}^\circ\mathrm{C}$.

**The falsifying experiments.** Two of this module's misconceptions can be tested with a kettle.
For "water boils at $100\,{}^\circ\mathrm{C}$, full stop": the saturation curve above *is* the
refutation — boiling happens where $P_{\mathrm{sat}}(T)$ meets the pressure on the liquid, and
every point of the curve is a boiling point at some pressure; a thermometer in boiling water at
$1600\ \mathrm{m}$ (Denver, $0.83\ \mathrm{atm}$) reads $95\,{}^\circ\mathrm{C}$. For "the heat
keeps raising the temperature": put a thermometer in a kettle, bring it to a rolling boil, and
log the reading every ten seconds while you turn the burner up — the temperature holds at the
boiling point to within the thermometer's resolution for as long as there is water, however
hard the burner runs. Only the *rate* of boiling changes. The heat is going into $L$, the
entropy difference between the two phases, at fixed $T$. The third misconception, "the
critical point is where the liquid runs out", is refuted by the blue path in the animation
above: nothing runs out, and gas becomes liquid without any event along the way.

:::{admonition} What the model does not prove
:class: open-question
Two things in this module are true of the model and not yet of the world. First, every
exponent near $T_c$ is mean-field: $v_g - v_\ell \propto (1 - T/T_c)^{1/2}$ here, while real
fluids show an exponent of about $0.32$, the same for carbon dioxide, water and xenon — a
universality that module 15 begins to explain. Second, the model places metastable states but
cannot time them; the superheat a real liquid reaches before it erupts is set by nucleation, a
kinetic theory this course names and does not develop.
:::

(14-coexistence-transfer)=
## Transfer the idea

Wherever two phases of one substance can trade particles, equilibrium is equal $\mu$, and
everything here follows.

- **Back to module 02.** The open question that module left — what the loop means — is closed:
  it is the model's attempt to interpolate through a region where no homogeneous state exists,
  and the construction replaces it by the flat line nature draws. The model's isotherms are
  reused unchanged; the only addition is $\mu$.
- **Back to modules 09 and 13.** Both did real work here: the stability criterion condemned
  the segment between the spinodals, and $\mu$ equality chose the line. A student who found
  the chemical potential abstract in module 13 has now watched it decide at what pressure a
  cylinder of carbon dioxide liquefies.
- **Forward to module 15.** The coexistence curve *ends*. Approaching its end the latent heat
  vanishes and the two densities merge as $(1 - T/T_c)^{1/2}$. What kind of transition has no
  latent heat, what the real exponent is, and why it is the same for a fluid and a magnet, is
  the next module's opening puzzle, with the Ising model as its laboratory.
- **Forward to module 17.** A Bose gas cooled past a critical temperature has its chemical
  potential pinned at the lowest level, the way $P_{\mathrm{sat}}$ is pinned on the flat line
  — and the macroscopic occupation of that level is a condensation in the same sense as this
  module's: Bose–Einstein condensation is a phase transition.
- **Pressure cookers and mountains.** At $2\ \mathrm{atm}$ water boils at
  $121\,{}^\circ\mathrm{C}$ and rice cooks in a third of the time; at $0.33\ \mathrm{atm}$ it
  boils at $71\,{}^\circ\mathrm{C}$ and an egg never sets. Both are the same curve read in the
  other direction.
- **Freeze-drying.** Below the triple point's pressure, $611\ \mathrm{Pa}$, there is no liquid
  water at any temperature: frozen food in a vacuum chamber loses its ice straight to vapour
  along the sublimation curve, which is how instant coffee is made without ever heating it.
- **Humidity and dew.** Air holds water vapour up to the partial pressure $P_{\mathrm{sat}}(T)$;
  relative humidity is the ratio, and the dew point is the temperature at which the vapour
  present reaches the curve. The exponential rise of $P_{\mathrm{sat}}$ with $T$ is why warm air
  holds so much more water, and why a $10\,{}^\circ\mathrm{C}$ night can wring it out.
- **Ice skating, in part.** Ice's melting curve leans left: pressure *lowers* its melting point,
  by $0.0074\ \mathrm{K}$ per bar, because ice is less dense than water and
  Clausius–Clapeyron has $v_\ell < v_s$. A skater's pressure accounts for a few hundredths of a
  degree, far too little to melt cold ice; the slipperiness of ice is mostly surface melting
  and friction, which is a different story.

Looking ahead:

- **Module 15** takes the end of the coexistence curve seriously: order parameters, critical
  exponents, and a model in which the transition can be simulated particle by particle.
- **Module 17** treats Bose–Einstein condensation as the phase transition this module makes it
  possible to recognize.
- **Module 18** asks how fast a system that has been pushed past its binodal finds its way to
  the new phase; this module has only said where it ends up.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — the lever rule.** At some temperature the coexisting volumes of a fluid
are $v_\ell = 0.080$ and $v_g = 0.270\ \mathrm{L/mol}$. A cylinder holds the fluid at an
average $0.150\ \mathrm{L/mol}$. What fraction of the molecules is vapour, and what fraction of
the *volume* does the liquid occupy?

:::{dropdown} Solution
$x_g = (0.150 - 0.080)/(0.270 - 0.080) = 0.070/0.190 = 0.368$, so $x_\ell = 0.632$. The liquid's
volume per mole of fluid is $x_\ell v_\ell = 0.632 \times 0.080 = 0.0506\ \mathrm{L/mol}$, which is
$0.0506/0.150 = 34\%$ of the cylinder. Two thirds of the molecules occupy a third of the room.
:::

**Worked example 2 — a pressure cooker.** Water boils at $373.15\ \mathrm{K}$ at
$1\ \mathrm{atm}$ with $L = 40.7\ \mathrm{kJ/mol}$. Estimate its boiling point at $2\ \mathrm{atm}$.

:::{dropdown} Solution
In the integrated form, $\ln(P_2/P_1) = (L/R)(1/T_1 - 1/T_2)$. So
$1/T_2 = 1/373.15 - (8.314/40\,700)\ln 2 = 2.680 \times 10^{-3} - 1.417 \times 10^{-4} =
2.538 \times 10^{-3}\ \mathrm{K^{-1}}$ and $T_2 = 394.0\ \mathrm{K} = 121\,{}^\circ\mathrm{C}$. The
laboratory's fit to the real curve gives $393.8\ \mathrm{K}$; the small difference is $L$'s
decrease with temperature.
:::

**Worked example 3 — a latent heat from two pressures.** Water's saturation pressure is
$70.18\ \mathrm{kPa}$ at $363.15\ \mathrm{K}$ and $101.42\ \mathrm{kPa}$ at $373.15\ \mathrm{K}$.
Estimate $L$.

:::{dropdown} Solution
$L = R\,\ln(P_2/P_1)/(1/T_1 - 1/T_2) = 8.314 \times 0.3683/(7.378 \times 10^{-5}) =
41.5\ \mathrm{kJ/mol}$. The tabulated value at $100\,{}^\circ\mathrm{C}$ is $40.7$; the $2\%$
excess is the ideal-vapour approximation and the $10\ \mathrm{K}$ average, in that order.
:::

**Worked example 4 — the model's latent heat.** For the van der Waals fluid at $280\ \mathrm{K}$
in the verification, $v_\ell = 0.0811$ and $v_g = 0.2672\ \mathrm{L/mol}$ with
$b = 0.0428\ \mathrm{L/mol}$. Find $L$ in $\kB T$ per molecule and in $\mathrm{kJ/mol}$.

:::{dropdown} Solution
$L = \kB T\ln[(v_g - b)/(v_\ell - b)] = \kB T\ln(0.2244/0.0383) = \kB T\ln 5.86 = 1.77\,\kB T$.
Per mole, $1.77 \times 8.314 \times 280 = 4.12\ \mathrm{kJ/mol}$. The real value for carbon
dioxide at this temperature is $9.7\ \mathrm{kJ/mol}$: the model's attraction is too weak.
:::

**Worked example 5 — counting freedoms.** How many intensive variables can be chosen freely
for (a) liquid water alone, (b) water boiling in an open kettle, (c) water, ice and vapour in a
sealed cell, (d) a salt solution in equilibrium with its vapour?

:::{dropdown} Solution
(a) $C = 1$, $P = 1$: $F = 2$, both $T$ and $P$. (b) $P = 2$: $F = 1$; the atmosphere fixes $P$,
so $T$ is fixed too, at $100\,{}^\circ\mathrm{C}$ at sea level. (c) $P = 3$: $F = 0$; the cell
sits at the triple point and nothing can be varied. (d) $C = 2$ (water and salt), $P = 2$:
$F = 2$ — at a given $T$ the vapour pressure can still be changed, by changing the
concentration, which is why salt water boils above $100\,{}^\circ\mathrm{C}$.
:::

**Worked example 6 — reading the spinodal.** For the van der Waals fluid the loop's extremes
obey $\kB T = 2a(v - b)^2/v^3$. Show that this has no solution above $T_c$.

:::{dropdown} Solution
The right-hand side, as a function of $v > b$, rises from zero, peaks, and falls back toward
zero as $v \to \infty$. Its maximum is where its derivative vanishes:
$2(v - b)v^3 - 3v^2(v - b)^2 = 0$, i.e. $2v = 3(v - b)$, $v = 3b = v_c$. There the right side is
$2a\,(2b)^2/(27b^3) = 8a/(27b) = \kB T_c$. So for $T > T_c$ the equation has no solution, the
slope never changes sign, and the isotherm has no loop — the critical point is where the two
spinodal points, and the two coexisting phases, meet.
:::

:::{note} Your predictions, revisited
1. **Forced by a rule, and the rule is equal chemical potential.** Neither the top nor the
   bottom of the loop: the line sits where the two lobes it cuts off have equal area, because
   $\mu_g - \mu_\ell = \int v\,\mathrm{d}P$ along the isotherm must vanish. See
   [the derivation](#14-coexistence-derive), step 3.
2. **Below — at about $90\,{}^\circ\mathrm{C}$.** Water boils where $P_{\mathrm{sat}}(T)$ equals
   the pressure on it, and at $0.7\ \mathrm{atm}$ that is $363.5\ \mathrm{K}$. Tea on a mountain
   is lukewarm by design.
3. **Nothing.** The thermometer stays at the boiling point; the kettle boils faster. The extra
   heat is spent on $L$, carrying molecules from liquid to vapour at fixed temperature.
4. **Something stranger.** The meniscus fades and disappears: the liquid's density falls and
   the vapour's rises until, at $T_c$, they are equal and there is one fluid filling the
   container. Nothing boils and nothing condenses; the distinction ends. Cool it again and the
   meniscus reappears.
:::

(14-coexistence-quiz)=
## Check your understanding

```{include} ../_generated/quiz-14-coexistence.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](14-coexistence-problems.md).

(14-coexistence-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A textbook says the flat line is drawn "so that the two areas are equal". Explain why, in
   this module, that is a theorem rather than a drawing rule, and say exactly where the chemical
   potential enters.
2. Why can boiling water not get hotter than its boiling point while the pressure on it holds,
   however hard it is heated? Where does the heat go?
3. If the flat line is "the" equilibrium, how can a superheated liquid exist at all? What is
   the difference between the binodal and the spinodal, and which of the two does a superheated
   liquid live between?
4. What dies at the critical point? Answer in one paragraph without a formula.

(14-coexistence-advanced)=
## Advanced: corresponding states for the coexistence curve

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence, or in modules 15 and 17, depends on this section. It cashes in
module 02's reduced variables for the boiling curve, and compares the result with two real
substances.
:::

Module 02 showed that every van der Waals substance obeys the same equation once pressure,
volume and temperature are measured in units of its own critical point:
$P_r = 8T_r/(3v_r - 1) - 3/v_r^2$. Every step of this module was carried out on that equation
— the construction, the lever rule, the latent heat — so every result is universal in reduced
variables too: there is one van der Waals coexistence curve $P_{r,\mathrm{sat}}(T_r)$, one
binodal dome, one function $L/(\kB T_c)$ of $T_r$, and the constants $a$ and $b$ do nothing but
scale the axes. The laboratory computes the curve for carbon dioxide, nitrogen and water and
finds them identical to one part in $10^{10}$.

Real substances are another matter. At $T_r = 0.85$ the model gives $P_{r,\mathrm{sat}} =
0.504$; measured carbon dioxide gives $0.314$ and water $0.277$. At $T_r = 0.95$ the three are
$0.812$, $0.703$ and $0.675$. Two things are visible in those numbers. The model is
quantitatively wrong by a margin that grows as $T$ falls — the mean-field attraction fitted at
the critical point is too weak everywhere below it. And the two *real* substances, chemically
nothing alike, are much closer to each other than either is to the model: a real law of
corresponding states, Guggenheim's, holds for many simple fluids to a few percent, with a
universal boiling curve that is *not* the van der Waals one. Its origin is the same as the
universality of the critical exponents in module 15 — the details of the molecule matter less
than the fact that there is a critical point — and it is one more hint that the right theory of
the critical region is not a mean field.

:::{admonition} What is still open here
:class: open-question
The model's coexistence curve ends at the critical point with $v_g - v_\ell \propto
(1 - T_r)^{1/2}$ and the latent heat vanishing linearly in the same quantity. Real fluids give
$v_g - v_\ell \propto (1 - T_r)^{0.32}$ — the same exponent for every one of them. No change of
$a$ and $b$ can produce that number; module 15 explains why.
:::
