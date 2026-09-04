---
title: Problem set — thermodynamic processes
short_title: 06 · Problems
---

# Problem set: thermodynamic processes

Exam-style problems. Work them with a pen before touching a computer; the last one is meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Take $R = 8.314\ \mathrm{J\,mol^{-1}K^{-1}}$ and
$k_B = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ throughout, and use the sign convention
$dU = \delta Q + \delta W_{\mathrm{on}}$.

## Problem 1 — the four signatures

<!-- objectives: OBJ-06-1, OBJ-06-3 -->

One mole of a monatomic ideal gas starts at $300\ \mathrm{K}$ in a volume of
$10.0\ \mathrm{L}$.

(a) Compute $W_{\mathrm{on}}$, $Q$ and $\Delta U$ for each of the following, each taken on its
own from the same starting state: heating at constant volume to $600\ \mathrm{K}$; expanding
at constant pressure to $20.0\ \mathrm{L}$; expanding isothermally to $20.0\ \mathrm{L}$.

(b) One of the three has $Q$ and $W_{\mathrm{on}}$ of opposite sign and equal magnitude, and
one has $W_{\mathrm{on}} = 0$. Say which and why, without recomputing.

(c) Between the same two volumes, the isobaric expansion absorbed roughly three and a half
times the heat the isothermal one did, while doing less than one and a half times the work.
Account for the entire difference, and say which of the two channels the extra heat went into.

## Problem 2 — deriving the adiabat

<!-- objectives: OBJ-06-2 -->

(a) Starting from the first law with $\delta Q = 0$ and the ideal-gas equation of state,
derive $P V^{\gamma} = \text{constant}$ for a quasistatic adiabatic process. State clearly
the point at which you used the quasistatic assumption, and what would go wrong without it.

(b) Show that the same law can be written $T V^{\gamma - 1} = \text{constant}$ and
$T^{\gamma} P^{1 - \gamma} = \text{constant}$.

(c) A student argues: "$\gamma > 1$, so the adiabat is steeper than the isotherm at every
point." Turn this into a proof by comparing $(\partial P/\partial V)$ for the two curves
through a common point.

(d) Explain in one sentence why a diatomic gas ($\gamma = 7/5$) cools less on adiabatic
expansion than a monatomic one ($\gamma = 5/3$).

## Problem 3 — heat capacities

<!-- objectives: OBJ-06-3 -->

(a) Derive $C_P = C_V + n R$ for an ideal gas from $\delta Q = dU + P\,dV$, being explicit
about where the ideal-gas equation of state enters.

(b) Compute $C_V$, $C_P$ and $\gamma$ for a monatomic gas, a diatomic gas at room temperature
(two rotational degrees of freedom active), and a diatomic gas hot enough that its vibrational
mode counts as two more.

(c) The measured $\gamma$ of hydrogen is $1.41$ at $300\ \mathrm{K}$, $1.60$ at
$50\ \mathrm{K}$, and near $1.30$ at $2000\ \mathrm{K}$. Explain the trend, and say which of
the three values a purely classical theory can account for.

(d) Would $C_P - C_V = n R$ still hold for a van der Waals gas? Answer yes or no and justify
it from where the derivation in (a) used ideality.

## Problem 4 — three adiabatic expansions

<!-- objectives: OBJ-06-1, OBJ-06-4, OBJ-06-5 -->

One mole of helium at $300\ \mathrm{K}$ occupies $10.0\ \mathrm{L}$ inside a perfectly
insulated cylinder. In each of the following it ends at $20.0\ \mathrm{L}$.

(a) It expands quasistatically. Find the final temperature and pressure and
$W_{\mathrm{on}}$.

(b) The partition to an evacuated $10.0\ \mathrm{L}$ chamber is removed. Find the final
temperature and pressure and $W_{\mathrm{on}}$.

(c) It pushes a piston loaded to a constant external pressure, chosen so that the gas comes to
rest at exactly $20.0\ \mathrm{L}$. Find that external pressure, the final temperature, and
$W_{\mathrm{on}}$.

(d) All three have $Q = 0$. Rank them by $|W_{\mathrm{on}}|$ and by final temperature, and
state the single physical reason the two rankings are opposite.

(e) Which of the three obeys $P V^{\gamma} = \text{constant}$? For each of the other two,
name the assumption of the derivation that fails.

## Problem 5 — irreversible compression

<!-- objectives: OBJ-06-4 -->

An insulated cylinder holds $0.50\ \mathrm{mol}$ of argon at $300\ \mathrm{K}$ in
$8.0\ \mathrm{L}$. A block is dropped onto the piston so that the external pressure jumps
immediately to $4.0 \times 10^{5}\ \mathrm{Pa}$ and stays there until the piston comes to rest.

(a) Find the final temperature and volume. (Hint: the gas stops when its own pressure equals
the external one, and $\Delta U = W_{\mathrm{on}}$.)

(b) Compute $W_{\mathrm{on}}$, and compare it with the work required to reach the *same final
volume* quasistatically and adiabatically.

(c) Which of the two compressions leaves the gas hotter? Explain why this is what energy
conservation demands, given your answer to (b).

(d) A student computes the work as the area under the gas's own $P$–$V$ curve between the
initial and final states and gets a different number. Explain precisely which step of their
reasoning is invalid, and why the endpoints being equilibrium states is not enough to rescue
it.

## Problem 6 — the atmosphere

<!-- objectives: OBJ-06-2, OBJ-06-4 -->

A parcel of dry air rises through the atmosphere fast enough to exchange no heat with its
surroundings, but slowly enough to stay in mechanical equilibrium with them at all times.

(a) Explain why this is a quasistatic adiabatic process even though the parcel has no
container and no piston. Identify what plays the role of the external pressure.

(b) Using $\gamma = 1.4$ and hydrostatic balance $dP/dz = -\rho g$, show that the temperature
falls linearly with height and that the lapse rate is $g/c_p$ per unit mass. Evaluate it for
air, whose specific heat capacity at constant pressure is about
$1005\ \mathrm{J\,kg^{-1}K^{-1}}$.

(c) The observed average lapse rate in the troposphere is about $6.5\ \mathrm{K/km}$, not the
value you computed. Give one physical reason for the discrepancy.

## Problem 7 — computational

<!-- objectives: OBJ-06-1, OBJ-06-5 -->

Using the module's laboratory notebook and the `thermolab.processes` module:

(a) For $f \in \{3, 5, 6\}$, compute the final temperature of a quasistatic adiabatic
expansion by a factor of two, and check each against $T V^{\gamma - 1} = \text{constant}$.

(b) Sweep the external pressure of an irreversible expansion to $2V_1$ from zero up to the
largest value for which the piston still reaches $2V_1$ before coming to rest, and plot the
final temperature against it. Identify which end of your sweep is the free expansion. Then
explain why no *constant* external pressure whatever reproduces the quasistatic adiabat's
final temperature, and what would have to be done differently to reach it.

(c) Run the microscopic free expansion for at least five independent seeds. Report the ratio
of final to initial kinetic temperature with its spread across seeds, and the ratio of final
to initial measured pressure.

(d) Your temperature ratio in (c) should be exactly $1$, with zero spread. Explain why that is
a property of the code rather than a measurement, and state what would have to change in the
model for a free expansion to cool the gas.
