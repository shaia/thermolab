---
title: Problem set — the fundamental relation
short_title: 09 · Problems
---

# Problem set: the fundamental relation

Exam-style problems. Work them with a pen before touching a computer; problems 4 and 5 are
meant to be finished in the laboratory, and problem 6 numerically. Solutions and marking rubrics
live with the instructor material and are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ and $R = 8.314\ \mathrm{J\,mol^{-1}\,K^{-1}}$
throughout.

## Problem 1 — the Einstein solid from scratch

<!-- objectives: OBJ-09-2, OBJ-09-7 -->

A solid is modelled as $n$ independent oscillators, each holding a whole number of energy quanta
of size $\varepsilon$, with $q$ quanta in total.

(a) Show that the number of microstates is

$$
\Omega(q, n) = \frac{(q + n - 1)!}{q!\,(n - 1)!} ,
$$

and check it by listing every microstate for $q = 3$ and $n = 2$.

(b) Using Stirling's approximation, and treating $q$ and $n$ as large, show that

$$
S(U, n) = \kB \Big[ (q + n) \ln (q + n) - q \ln q - n \ln n \Big] ,
\qquad q = \frac{U}{\varepsilon} .
$$

(c) Differentiate to find $1/T$, and invert to find $U(T)$.

(d) Show that for $U \gg n\varepsilon$ your result reduces to $U \approx n \kB T$, and find the
next correction. Explain what module 01 assumed that this calculation has now derived.

(e) Sketch $C_V(T)$ from your $U(T)$ and describe what happens to it as $T \to 0$.

## Problem 2 — Euler and Gibbs–Duhem on an ideal gas

<!-- objectives: OBJ-09-4, OBJ-09-2 -->

The Sackur–Tetrode entropy of a monatomic ideal gas is

$$
S(U, V, N) = N \kB \left[
\ln\!\left( \frac{V}{N} \left( \frac{4 \pi m U}{3 N h^2} \right)^{3/2} \right)
+ \frac{5}{2} \right] .
$$

(a) Show that

$$
S(\lambda U, \lambda V, \lambda N) = \lambda S(U, V, N) .
$$

(b) Compute all three slopes, and hence $T$, $P$ and $\mu$ as functions of $U$, $V$ and $N$.

(c) Verify the Euler relation term by term.

(d) Express $\mu$ as a function of $T$ and $P$ alone. Use your expression to verify the
Gibbs–Duhem relation directly.

(e) For one mole of helium ($m = 6.646 \times 10^{-27}\ \mathrm{kg}$) at $300\ \mathrm{K}$ and
$1\ \mathrm{bar}$, compute $S$, $U$, $PV$ and $\mu N$, and check that they satisfy the Euler
relation to the precision you carried.

## Problem 3 — curvature and stability

<!-- objectives: OBJ-09-5 -->

(a) Starting from the definition of temperature as the slope $(\partial S/\partial U)_{V,N}$,
which is $1/T$, show that

$$
\left(\frac{\partial^2 S}{\partial U^2}\right)_{V,N} = -\frac{1}{T^2 C_V} .
$$

(b) Two identical pieces of a substance, each with energy $U$, are in thermal contact. Write the
total entropy after an amount $\delta$ of energy has moved from one to the other, expand it to
second order in $\delta$, and show that the equal split is a maximum of the total entropy if and
only if $C_V > 0$.

(c) A gravitationally bound ball of gas has, by the virial theorem, $U = -\tfrac{3}{2} N \kB T$.
Find its heat capacity. Describe in words what happens to two such balls placed in thermal
contact at slightly different temperatures, and explain which of this module's postulates such a
system violates.

(d) Give a physical argument, without calculation, that a stable substance must have
$\kappa_T \ge 0$: imagine a movable wall between two identical samples at the same temperature.

## Problem 4 — unequal solids and the ledger

<!-- objectives: OBJ-09-3, OBJ-09-6, OBJ-09-7 -->

Two Einstein solids with quanta of size $\varepsilon = (5\ \mathrm{K})\,\kB$ are put in thermal contact: solid A has $n_A = 300$ oscillators and starts at
$500\ \mathrm{K}$, solid B has $n_B = 100$ and starts at $250\ \mathrm{K}$, by module 01's map
$T = q\varepsilon/(n\kB)$.

(a) Use the equal-slope condition to predict how many quanta each solid holds at equilibrium.

(b) Treating each solid as having constant heat capacity $n\kB$, compute the entropy produced in
units of $\kB$.

(c) In the laboratory, confirm your partition with the composite maximiser, then run module 01's
simulation and apply the entropy ledger. Report the ledger's final value, its largest single-step
decrease, and the largest amount by which it ever falls below its own previous maximum.

(d) Your answer to (b) and the ledger's final value differ by a few percent. Identify the two
separate approximations responsible, and describe a laboratory experiment that measures each one
on its own.

(e) State carefully what the ledger's behaviour does, and does not, establish about the second
law.

## Problem 5 — releasing constraints on a gas

<!-- objectives: OBJ-09-2, OBJ-09-3 -->

A rigid, insulated box of total volume $3.0\ \mathrm{L}$ is divided by a wall. Side A holds
$0.010\ \mathrm{mol}$ of argon in $0.5\ \mathrm{L}$ at $600\ \mathrm{K}$; side B holds
$0.020\ \mathrm{mol}$ of argon in $2.5\ \mathrm{L}$ at $300\ \mathrm{K}$.

(a) The wall is made to conduct heat but stays fixed and impermeable. Find the final
temperature and the final pressure on each side.

(b) The wall is now also freed to slide. Find the final volumes and the common pressure.

(c) The wall is now perforated. Explain, using the Gibbs–Duhem relation, why nothing changes.

(d) Compute the entropy produced in each of steps (a) and (b), and check your answers against the
laboratory's composite maximiser.

(e) Explain why the laboratory refuses to free the wall to slide *without* also letting it
conduct heat.

## Problem 6 — challenge: calorimetry with a varying heat capacity

<!-- objectives: OBJ-09-6 -->

A $0.20\ \mathrm{kg}$ block of aluminium at $373\ \mathrm{K}$ is dropped into $0.50\ \mathrm{kg}$
of water at $283\ \mathrm{K}$ in an insulated cup. Take water's specific heat as constant,
$4184\ \mathrm{J\,kg^{-1}\,K^{-1}}$. Aluminium's specific heat depends on temperature; over this
range it is well described by

$$
c_{\text{Al}}(T) = 765 + 0.459\,T \quad \mathrm{J\,kg^{-1}\,K^{-1}} .
$$

(a) Find the final temperature by requiring that the heat lost by the aluminium equals the heat
gained by the water. Solve the resulting equation numerically.

(b) Compute the entropy produced, integrating

$$
\mathrm{d}S = \frac{C(T)\,\mathrm{d}T}{T}
$$

for the aluminium.

(c) Repeat (a) and (b) with a constant aluminium specific heat evaluated at $300\ \mathrm{K}$, and
state the size of the error that approximation introduces in each answer.

(d) A student measures the final temperature to $\pm 0.05\ \mathrm{K}$. Estimate the resulting
uncertainty in the entropy produced, and say whether it is larger or smaller than the error in
(c).
