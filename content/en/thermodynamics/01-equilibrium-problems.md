---
title: Problem set — thermal equilibrium
short_title: 01 · Problems
---

# Problem set: thermal equilibrium

Exam-style problems. Work them with a pen before touching a computer; the last one is meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

## Problem 1 — reading the zeroth law

<!-- objectives: OBJ-01-1 -->

(a) State the zeroth law of thermodynamics precisely.

(b) A student argues: "If A is hotter than C, and B is hotter than C, then A and B must be at
the same temperature." Explain exactly what is wrong with this argument, and contrast it with
what the zeroth law actually says.

(c) Explain, in one sentence, why the zeroth law is what makes it meaningful to calibrate a
single thermometer once and then trust its reading on many different objects.

## Problem 2 — the equilibrium temperature

<!-- objectives: OBJ-01-3 -->

A cup containing $0.20\ \mathrm{kg}$ of coffee at $90\,^\circ\mathrm{C}$ (specific heat
$c = 4200\ \mathrm{J\,kg^{-1}\,K^{-1}}$) is poured into an empty mug of heat capacity
$C_{\text{mug}} = 150\ \mathrm{J/K}$, initially at $20\,^\circ\mathrm{C}$. Treat the pair as
isolated once the coffee is poured.

(a) Compute the coffee's heat capacity $C_A = mc$.

(b) Compute the equilibrium temperature using the heat-capacity-weighted formula.

(c) Compare your answer with the naive unweighted average of the two starting temperatures.
Which starting temperature does the true equilibrium sit closer to, and why?

## Problem 3 — solving the relaxation equation

<!-- objectives: OBJ-01-4 -->

Two bodies with $C_A = 40\ \mathrm{J/K}$ and $C_B = 120\ \mathrm{J/K}$ are connected through a
contact of conductance $\kappa = 0.50\ \mathrm{W/K}$. They start with a temperature gap of
$60\ \mathrm{K}$.

(a) Derive the relaxation time $\tau$ from the pair of rate equations for $dT_A/dt$ and
$dT_B/dt$, showing your algebra.

(b) Evaluate $\tau$ numerically for the values above.

(c) How long does it take for the gap to fall to $5\%$ of its initial value? Express your
answer both symbolically (in terms of $\tau$) and numerically.

## Problem 4 — forensic cooling

<!-- objectives: OBJ-01-2, OBJ-01-4 -->

A body is discovered in a room held at a constant $18\,^\circ\mathrm{C}$. Investigators
measure the body's temperature to be $30\,^\circ\mathrm{C}$, and one hour later measure it
again at $27\,^\circ\mathrm{C}$. Living human body temperature is $37\,^\circ\mathrm{C}$.

(a) Using $T(t) - T_{\text{room}} = (T_0 - T_{\text{room}})e^{-t/\tau}$, use the two
measurements to solve for $\tau$.

(b) Using $\tau$ from (a) and an assumed starting temperature of $37\,^\circ\mathrm{C}$ at the
moment of death, estimate how long before the first measurement death occurred.

(c) Name two assumptions of the model that are most likely to be violated in a real forensic
setting (consider: is $\kappa$ really constant? is the room temperature really constant? is
$37\,^\circ\mathrm{C}$ a safe assumption for every individual?), and say which direction each
violation would bias the estimated time of death.

## Problem 5 — where the model breaks

<!-- objectives: OBJ-01-5 -->

The laboratory's discrete exchange model assumes both bodies sit in the classical,
high-temperature equipartition regime and exchange quanta of equal size.

(a) Using the model specification's stated failure modes, explain what goes wrong as both
bodies' temperatures approach absolute zero.

(b) Explain why a body with only a handful of oscillators (say $n_A = 2$) makes "temperature"
a shaky concept even before quantum statistics enter the picture. Connect your answer to the
rounding step in `from_temperatures` described in the page's Advanced section.

(c) Two different real materials in direct contact do not literally exchange quanta of exactly
equal size. Give a physical argument for why this does not stop the *macroscopic* conclusions
of this module (the equilibrium temperature formula, the exponential relaxation) from holding,
even though it does invalidate the *specific* microscopic mechanism modelled in the
laboratory.

## Problem 6 — computational

<!-- objectives: OBJ-01-3, OBJ-01-4, OBJ-01-5 -->

Using the module's laboratory notebook and the `thermolab.equilibrium` module:

(a) Build a state with `from_temperatures`, choosing your own $n_A \ne n_B$ and starting
temperatures. Run many independent long simulations and verify that the mean final
temperature agrees with `equilibrium_temperature`, quoting an uncertainty on your estimate.

(b) At several checkpoints (roughly $0.5\tau$, $1\tau$, $2\tau$ and $4\tau$), measure the mean
temperature gap across independent seeds and compare it with `predicted_relaxation`. Does the
agreement hold at every checkpoint, or only near equilibrium?

(c) Repeat the exercise at two different system sizes (say ten times apart in oscillator
count) and measure the run-to-run relative spread of the gap one relaxation time in. Verify
that the spread shrinks as the system grows.

(d) State one thing your numerical result does *not* prove about real thermal contact.
