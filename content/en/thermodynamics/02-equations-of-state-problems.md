---
title: Problem set — equations of state
short_title: 02 · Problems
---

# Problem set: equations of state

Exam-style problems. Work them with a pen before touching a computer; problem 4 is meant to
be finished numerically. Solutions and marking rubrics live with the instructor material and
are deliberately not on this site.

Take $k_B = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ and $N_A = 6.022\times10^{23}$
throughout. Recall the per-particle van der Waals equation from the module page,
$P = k_BT/(v - b) - a/v^2$ with $v = V/N$, and its closed-form critical point
$v_c = 3b$, $k_BT_c = 8a/(27b)$, $P_c = a/(27b^2)$.

Argon's van der Waals constants, in this course's per-particle convention, are
$a = 3.736\times10^{-49}\ \mathrm{Pa\,m^6}$ and $b = 5.317\times10^{-29}\ \mathrm{m^3}$.
Carbon dioxide's measured critical point (NIST Chemistry WebBook) is
$T_c = 304.13\ \mathrm{K}$, $P_c = 7.3773\times10^{6}\ \mathrm{Pa}$.

## Problem 1 — deriving the critical point

<!-- objectives: OBJ-02-5 -->

(a) Starting from $P(v) = k_BT/(v - b) - a/v^2$ at fixed $T$, compute $(\partial P/\partial
v)_T$ and $(\partial^2 P/\partial v^2)_T$.

(b) Set both derivatives to zero simultaneously and solve for $v_c$ and $T_c$. (Hint: dividing
one equation by the other eliminates $T$ first, leaving an equation in $v$ alone.)

(c) Substitute your result back into $P(v)$ at $T = T_c$ to find $P_c$.

(d) Using argon's constants above, evaluate $v_c$, $T_c$ and $P_c$ numerically. Convert your
per-particle $v_c$ to a molar volume by multiplying by $N_A$, and compare all three numbers to
argon's measured critical point: $T_c = 150.9\ \mathrm{K}$, $P_c = 4.87\times10^{6}\
\mathrm{Pa}$, molar $V_c \approx 74.6\ \mathrm{cm^3/mol}$.

## Problem 2 — the universal $Z_c = 3/8$

<!-- objectives: OBJ-02-6 -->

(a) Using the boxed critical-point formulas from Problem 1(b)-(c), show that
$Z_c \equiv P_cv_c/(k_BT_c) = 3/8$ exactly — a number with no $a$ or $b$ left in it at all.

(b) Real gases' measured critical compressibility factors cluster around $0.23$–$0.31$
(argon $\approx 0.29$, carbon dioxide $\approx 0.274$, water $\approx 0.23$) rather than
exactly $3/8 = 0.375$. Is this discrepancy evidence against the state postulate (the module
page's opening claim), against the van der Waals model specifically, or against something
else? Justify your answer in a sentence or two.

(c) Compute the percentage difference between $3/8$ and argon's measured $0.29$.

## Problem 3 — deriving the reduced equation of state

<!-- objectives: OBJ-02-6 -->

(a) Substitute $P = P_rP_c$, $v = v_rv_c$, $T = T_rT_c$ into the boxed van der Waals equation,
using the closed forms for $v_c$, $T_c$, $P_c$ from Problem 1, and show the result simplifies
to $P_r = 8T_r/(3v_r - 1) - 3/v_r^2$ with $a$, $b$ and $k_B$ cancelling out completely.

(b) Confirm that your reduced equation gives $P_r = 1$ when $v_r = T_r = 1$ — that is, that it
is satisfied exactly at the critical point itself, as it must be by construction.

(c) Two different gases are held at the same reduced temperature and the same reduced
pressure. What does the equation you just derived say about their reduced volumes? Is this
something the *un-reduced* van der Waals equation, evaluated separately with each gas's own
$a$ and $b$, would tell you on its own, without first reducing the variables?

## Problem 4 — computational: fitting carbon dioxide from its critical point

<!-- objectives: OBJ-02-3, OBJ-02-4 -->

Using the module's laboratory notebook and `thermolab.gases`.

(a) From carbon dioxide's measured critical point above, compute $a$ and $b$ with
`gases.vdw_constants_from_critical`.

(b) Load `data/co2-isotherm-280k.csv` (representative published NIST Chemistry WebBook
values for carbon dioxide's isothermal pressure-volume behaviour at $280\ \mathrm{K}$). For
each tabulated molar volume, convert to the per-particle $v = V_m/N_A$ and compute both the
ideal pressure $P = k_BT/v$ and the van der Waals pressure using your fitted $a$, $b$ from
(a).

(c) For each tabulated point, report the percentage difference of each model's prediction
from the tabulated (measured) pressure. Over what range of $v$ does the *ideal* prediction
stay within $10\%$ of the measured value? Where does it first exceed $50\%$?

(d) The van der Waals prediction tracks the measured pressure considerably more closely than
the ideal prediction does, across the dilute-to-near-saturation vapour branch — but neither
model reproduces the flat condensation plateau in the tabulated data. State, in one sentence,
why a model built from a single, density-independent pair of constants $(a, b)$ cannot in
principle produce a genuinely flat plateau at any density.

## Problem 5 — challenge: a molecule's size, and dimensional analysis

<!-- objectives: OBJ-02-2, OBJ-02-4 -->

(a) Treat a $\mathrm{CO_2}$ molecule as a hard sphere of diameter $d \approx 3.3\times10^{-10}\
\mathrm{m}$ (an approximate kinetic diameter). Two such spheres cannot approach closer than
one diameter, centre to centre, so each *pair* of molecules excludes a sphere of radius $d$
around each other — volume $\tfrac{4}{3}\pi d^3$. That excluded volume belongs to the pair, not
to either molecule alone, so argue that the excluded volume *per molecule* is
$b \approx \tfrac{1}{2}\left(\tfrac{4}{3}\pi d^3\right) = \tfrac{2}{3}\pi d^3$, and evaluate it
numerically.

(b) Compare your geometric estimate of $b$ to the value fit from carbon dioxide's critical
point in Problem 4(a). Are the two the same order of magnitude?

(c) Inspect the boxed van der Waals equation term by term and confirm that $a$ must carry
units of $\mathrm{Pa\,m^6}$ and $b$ must carry units of $\mathrm{m^3}$ for the equation to be
dimensionally consistent. In one sentence, explain why this argument pins down the units of
$a$ and $b$ without needing to know either constant's numerical value.
