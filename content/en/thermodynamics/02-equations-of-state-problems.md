---
title: Problem set — equations of state
short_title: 02 · Problems
---

# Problem set: equations of state

Exam-style problems. Work them with a pen before touching a computer; the last one is meant
to be finished numerically. Solutions and marking rubrics live with the instructor material
and are deliberately not on this site.

Take $k_B = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$ and $N_A = 6.022\times10^{23}$
throughout. Argon's van der Waals constants, in this course's per-particle convention, are
$a = 3.736\times10^{-49}\ \mathrm{Pa\,m^6}$ and $b = 5.317\times10^{-29}\ \mathrm{m^3}$
(converted from the textbook molar values $a_{\text{molar}} = 0.1355\ \mathrm{Pa\,m^6/mol^2}$,
$b_{\text{molar}} = 3.201\times10^{-5}\ \mathrm{m^3/mol}$).

## Problem 1 — reading the equation of state

<!-- objectives: OBJ-02-1, OBJ-02-2 -->

A sealed rigid vessel of volume $2.0\ \mathrm{L}$ holds $N = 5.0\times10^{22}$ argon atoms at
$300\ \mathrm{K}$ — the same numbers as
[module 4's Problem 2](04-pressure-problems.md).

(a) Compute the pressure predicted by the ideal gas law.

(b) Compute the excluded-volume term $Nk_BT/(V-Nb)$ and the attraction term $aN^2/V^2$
separately, using argon's constants above.

(c) Combine them into the van der Waals pressure, and state the relative difference from
your answer in (a) as a percentage.

(d) Which of the two corrections dominates at this density? Would that still be true if the
vessel held the same number of atoms in a hundredth of the volume? Justify your answer
without recomputing everything from scratch.

## Problem 2 — building the corrections

<!-- objectives: OBJ-02-2 -->

(a) A student writes the excluded-volume correction as $P = Nk_BT/(V - b)$, without the
factor of $N$ multiplying $b$. Explain, in terms of what $b$ represents physically, why this
is wrong for any $N > 1$.

(b) Explain why the attraction correction is proportional to $N^2/V^2$ (density squared)
rather than to $N/V$ (density to the first power) — your answer should say what physical
event the term is counting.

(c) A textbook quotes carbon dioxide's van der Waals constants as
$a_{\text{molar}} = 0.3640\ \mathrm{Pa\,m^6/mol^2}$ and
$b_{\text{molar}} = 4.267\times10^{-5}\ \mathrm{m^3/mol}$. Convert both to the per-particle
convention `thermolab.equations_of_state` uses, and state the two conversion factors you
applied.

## Problem 3 — intensive and extensive

<!-- objectives: OBJ-02-3 -->

Argon at $N = 5.0\times10^{22}$, $V = 2.0\times10^{-3}\ \mathrm{m^3}$, $T = 300\ \mathrm{K}$
(Problem 1's scenario).

(a) Compute the van der Waals pressure at $(3N, 3V)$, same $T$, and compare it with your
answer to Problem 1(c).

(b) Explain algebraically, working directly from the boxed van der Waals equation, why *any*
simultaneous rescaling $N \to \lambda N$, $V \to \lambda V$ at fixed $T$ leaves the pressure
exactly unchanged — not just for $\lambda = 3$.

(c) The ideal gas's internal energy is $U = \tfrac{3}{2}Nk_BT$ (three dimensions). Is $U$
intensive or extensive? Compute $U$ at $(N,T)$ and at $(3N,T)$ to check your answer, and
state in one sentence what distinguishes a quantity like $U$ from a quantity like $P$.

## Problem 4 — the critical point

<!-- objectives: OBJ-02-4 -->

Using argon's constants above, for one mole of argon ($N = N_A$):

(a) Compute $T_c$, $P_c$, and $V_c$ from the closed-form relations.

(b) Argon's measured critical point is $T_c = 150.9\ \mathrm{K}$,
$P_c = 4.87\times10^{6}\ \mathrm{Pa}$, and a measured molar critical volume of about
$74.6\ \mathrm{cm^3}$. Compare each of your three answers to the corresponding measured
value as a percentage difference.

(c) One of the three comparisons in (b) should stand out as noticeably worse than the other
two. Which one, and — without redoing the algebra — what does the module page's discussion
of $P_cV_c/(Nk_BT_c)$ say about *why* that particular quantity is the least trustworthy?

(d) In one or two sentences, describe what is physically special about the point
$(T_c, P_c, V_c)$ — what distinguishes it from every other point on the P-V-T surface?

## Problem 5 — reading a P-V-T surface

<!-- objectives: OBJ-02-5 -->

Consider a family of van der Waals isotherms for a fixed substance, plotted at several
temperatures both above and below $T_c$.

(a) Describe, in words, how the shape of the isotherm changes as $T$ decreases through $T_c$.

(b) On an isotherm below $T_c$, part of the van der Waals curve has $(\partial P/\partial
V)_T > 0$ — pressure *rising* as volume *increases*. Explain why this region cannot describe
any stable equilibrium state of a real substance.

(c) The Maxwell construction (module page, Advanced section) replaces the unphysical loop
with a flat horizontal segment, positioned by requiring two areas cut from the loop to be
equal. Without deriving this, explain in one sentence what physical quantity being
single-valued is what forces the areas to match.

(d) State, in your own words, the two ingredients of the van der Waals model whose absence
would make it unable to predict a critical point at all.

## Problem 6 — computational

<!-- objectives: OBJ-02-1, OBJ-02-3, OBJ-02-4 -->

Using the module's laboratory notebook and `thermolab.equations_of_state`:

(a) Build a `pv_t_surface` for argon over a range of temperatures spanning $T_c$ and a range
of volumes down to just above the excluded volume. Compare it, on the same axes, with the
ideal-gas surface (`a = b = 0`) over the same grid, and report the volume at which the two
surfaces start to visibly disagree at $T = 300\ \mathrm{K}$.

(b) Verify numerically that `van_der_waals_pressure` is unchanged under
$(N,V) \to (\lambda N, \lambda V)$ at fixed $T$, for at least three values of $\lambda$, and
report the largest relative difference you measure.

(c) Compute `critical_point` for argon, then evaluate the pressure formula at a few volumes
close to $V_c$ (holding $T = T_c$) to confirm numerically that the pressure is stationary
there — that is, that $P(V_c - \delta)$ and $P(V_c + \delta)$ are both very close to $P_c$
for small $\delta$.

(d) State one thing your numerical result in (c) does *not* prove about the critical point.
