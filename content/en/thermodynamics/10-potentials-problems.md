---
title: Problem set — thermodynamic potentials
short_title: 10 · Problems
---

# Problem set: thermodynamic potentials

Exam-style problems. Work them with a pen before touching a computer; problems 4 and 5 are meant
to be finished in the laboratory, and problem 6 is a challenge. Solutions and marking rubrics
live with the instructor material and are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ and $R = 8.314\ \mathrm{J\,mol^{-1}\,K^{-1}}$
throughout.

## Problem 1 — the Gibbs Maxwell relation on an ideal gas

<!-- objectives: OBJ-10-4, OBJ-10-5 -->

(a) Starting from $\mathrm{d}G = -S\,\mathrm{d}T + V\,\mathrm{d}P$ at fixed $N$, derive the Maxwell
relation

$$
\left(\frac{\partial S}{\partial P}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_P .
$$

(b) Use it to show that for an ideal gas

$$
\left(\frac{\partial S}{\partial P}\right)_T = -\frac{N \kB}{P} ,
$$

and hence find the entropy change of one mole of an ideal gas compressed isothermally from
$1$ to $10\ \mathrm{bar}$.

(c) Check your answer to (b) against the volume form of the entropy change, using
$(\partial S/\partial V)_T = (\partial P/\partial T)_V$ instead.

(d) Explain in words why squeezing a gas at fixed temperature lowers its entropy, and where the
entropy goes.

## Problem 2 — the potentials and the Euler relation

<!-- objectives: OBJ-10-1, OBJ-10-2 -->

(a) Using the Euler relation $U = TS - PV + \mu N$, show that $G = \mu N$, and find the
corresponding expressions for $F$ and $H$.

(b) Starting from $F = U - TS$ and module 09's differential form of the fundamental relation,
derive $\mathrm{d}F = -S\,\mathrm{d}T - P\,\mathrm{d}V + \mu\,\mathrm{d}N$.

(c) For one mole of argon at $300\ \mathrm{K}$ and $1\ \mathrm{bar}$ the Sackur–Tetrode entropy is
$S = 155.0\ \mathrm{J\,K^{-1}}$. Compute $U$, $H$, $F$ and $G$. Module 09 found that for this
gas $\mu N = -T\,(S - \tfrac{5}{2} N \kB)$; check that your $G$ agrees with it.

(d) A student writes the ideal gas's energy as $U(T, V) = \tfrac{3}{2} N \kB T$ and differentiates
with respect to $V$ to find the pressure. What do they get, and what has gone wrong?

## Problem 3 — splitting water: heat versus enthalpy

<!-- objectives: OBJ-10-7, OBJ-10-3 -->

At $298\ \mathrm{K}$ and $1\ \mathrm{bar}$, splitting one mole of liquid water into hydrogen and
oxygen gas has $\Delta H = 285.8\ \mathrm{kJ}$ and $\Delta G = 237.1\ \mathrm{kJ}$.

(a) Show that at fixed $T$ and $P$ the electrical work done on the cell is at least $\Delta G$.

(b) Find the smallest voltage that can split water, given that two electrons pass per molecule
and the Faraday constant is $96\,485\ \mathrm{C\,mol^{-1}}$.

(c) A cell runs at $1.80\ \mathrm{V}$. Per mole of water split, find the electrical work, the
heat that crosses the boundary, and its direction.

(d) Explain why "$\Delta H$ is the heat of the reaction" is true for the same reaction run by
burning hydrogen in reverse at constant pressure, and false for the cell.

## Problem 4 — the Einstein solid's free energy, numerically

<!-- objectives: OBJ-10-1, OBJ-10-6 -->

The Einstein solid of module 09 has, per oscillator,

$$
U = \frac{\varepsilon}{e^{\varepsilon / \kB T} - 1} ,
\qquad
S = \kB \Big[ (1 + x) \ln (1 + x) - x \ln x \Big] ,
\qquad x = \frac{U}{\varepsilon} .
$$

(a) Show algebraically that $F = U - TS$ equals $\kB T \ln\left(1 - e^{-\varepsilon/\kB T}\right)$
per oscillator.

(b) In the laboratory, tabulate $U(S)$ on a grid of $N$ points and Legendre-transform it
numerically. Plot the largest error of the result against $N$, measured two ways: at the
temperature each point *should* have, and on the curve $F(T)$. Report both observed orders.

(c) Explain why the two orders differ, using the fact that $f - p\,x$ is stationary in $x$ at the
true tangent point.

(d) Why does the transform need $U(S)$ to be convex, and which property of the solid from module
09 guarantees it?

## Problem 5 — entropy from a pressure gauge: ideal versus real

<!-- objectives: OBJ-10-5, OBJ-10-4 -->

(a) Show that for the van der Waals gas

$$
\left(\frac{\partial P}{\partial T}\right)_V = \frac{N \kB}{V - N b} ,
$$

and integrate the Maxwell relation from $F$ to find the entropy change on an isothermal
expansion from $V_1$ to $V_2$.

(b) For one mole of carbon dioxide ($b = 4.27 \times 10^{-5}\ \mathrm{m^3\,mol^{-1}}$) expanding
from $0.20$ to $0.60\ \mathrm{L}$ at fixed temperature, compute the entropy change, and compare it
with the ideal-gas value.

(c) In the laboratory, simulate gauge readings with $0.5\%$ noise at five temperatures and a grid
of volumes, and reconstruct $\Delta S$ with its error bar. How many volumes do you need before the
error from the integration rule is smaller than the error from the noise?

(d) Explain why the attraction constant $a$ plays no part in the answer.

## Problem 6 — challenge: an ideal chain and the rubber band

<!-- objectives: OBJ-10-3, OBJ-10-4 -->

Model a polymer as a chain of $n$ links of length $\ell$, each pointing either left or right
along a line, with no energy cost for either direction. With $n_+$ links pointing right, the
chain's end-to-end length is $L = (2 n_+ - n)\,\ell$.

(a) Show that the number of arrangements with length $L$ is the binomial coefficient
$\binom{n}{n_+}$, and that for $|L| \ll n\ell$ the entropy is approximately

$$
S(L) = S(0) - \frac{\kB L^2}{2 n \ell^2} .
$$

(b) The chain's energy does not depend on $L$. Using $\mathrm{d}F = -S\,\mathrm{d}T + f\,\mathrm{d}L$,
show that the tension needed to hold it at length $L$ is

$$
f = -T\left(\frac{\partial S}{\partial L}\right)_T = \frac{\kB T L}{n \ell^2} .
$$

(c) Predict what a chain holding a fixed weight does when heated, and what happens to its
temperature when it is stretched quickly.

(d) The laboratory's rubber band gives $(\partial f/\partial T)_L = 5.79 \pm 0.17\ \mathrm{mN\,K^{-1}}$
at a tension of $2.00\ \mathrm{N}$ and $295\ \mathrm{K}$. The ideal chain predicts a tension exactly
proportional to $T$. How far does the band depart from that, and what does the departure measure?
