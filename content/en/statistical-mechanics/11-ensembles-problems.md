---
title: Problem set — statistical ensembles
short_title: 11 · Problems
---

# Problem set: statistical ensembles

Exam-style problems. Work them with a pen before touching a computer; problems 4 and 5 are meant
to be finished in the laboratory, and problem 6 is a challenge. Solutions and marking rubrics
live with the instructor material and are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$, $g = 9.81\ \mathrm{m\,s^{-2}}$ and
$1\ \mathrm{u} = 1.661 \times 10^{-27}\ \mathrm{kg}$ throughout. An Einstein solid of $N$
oscillators holds $q$ quanta in $\Omega(N, q) = \binom{q + N - 1}{q}$ ways.

## Problem 1 — a bath you can count

<!-- objectives: OBJ-11-2, OBJ-11-4 -->

A two-level system with a gap of one quantum shares $q$ quanta with a bath of three oscillators.

(a) For $q = 1, 2, \ldots, 6$, count the joint microstates with the system in each state and
find the probability that it is excited.

(b) Show that for a bath of $N$ oscillators holding $q$ quanta when the system is in its ground
state, the exact ratio of the system's occupations is

$$
\frac{p_1}{p_0} = \frac{q}{q + N - 1} .
$$

(c) The bath's exact slope at $q$ quanta is $\beta\varepsilon = \sum_{j=1}^{N-1} 1/(q + j)$.
For $N = 3$ and $q = 3$, compare $e^{-\beta\varepsilon}$ with the exact ratio of (b). Which is
larger, and why must it be that one?

(d) What is the probability that the system is excited when $q = 0$? What does the bath's
"temperature" mean then?

(e) Module 01's two Einstein solids, A with $n_a$ oscillators and B with $n_b$, share $Q$
quanta. Write down the exact probability that A holds $q_a$ of them, and explain why, once
$n_b \gg n_a$, it takes the form $g(q_a)\, e^{-\beta q_a \varepsilon}/Z$. Which body's
temperature is $\beta$?

## Problem 2 — the next term

<!-- objectives: OBJ-11-3, OBJ-11-6 -->

(a) Expand $\ln\Omega_{\mathrm{bath}}(U_{\mathrm{tot}} - E_s)$ to second order in $E_s$, and
show that the second derivative is

$$
\frac{\partial^2 \ln \Omega_{\mathrm{bath}}}{\partial U^2} = -\frac{1}{\kB T^2\, C_{\mathrm{bath}}} .
$$

(b) Hence write the probability of a state to second order, and show that for a bath in its
equipartition regime the correction to $\ln P_s$ is $-E_s^2/(2 N_{\mathrm{bath}} (\kB T)^2)$.

(c) State the two hypotheses of the Boltzmann distribution, and explain what goes wrong with the
derivation when each fails.

(d) From (b), predict how the largest gap between the exact finite-bath distribution and the
Boltzmann distribution should scale with $N_{\mathrm{bath}}$ at fixed temperature. By what factor
should it fall when the bath is doubled?

(e) For a system whose relevant energies reach $5\,\kB T$, how many oscillators must a bath in
its equipartition regime have for the correction to stay below $0.5\%$?

## Problem 3 — a spin in a magnetic field

<!-- objectives: OBJ-11-7, OBJ-11-8 -->

An electron's magnetic moment, $\mu = 9.274 \times 10^{-24}\ \mathrm{J\,T^{-1}}$, in a field $B$
points either along the field, with energy $-\mu B$, or against it, with energy $+\mu B$. A crystal
holds $N$ such moments, independent of one another, at temperature $T$.

(a) Treat one moment as a two-level system. What is its gap $\Delta$, and what are the
probabilities of the two orientations?

(b) Show that the mean moment along the field is $\langle m \rangle = \mu \tanh(\mu B/(\kB T))$,
so that the crystal's magnetization is $M = N\mu \tanh(\mu B/(\kB T))$.

(c) Show that for $\mu B \ll \kB T$ the magnetization is proportional to $B/T$ — Curie's law —
and find the constant of proportionality.

(d) Evaluate $\mu B/(\kB T)$ and the fraction of moments aligned with a $1\ \mathrm{T}$ field at
$300\ \mathrm{K}$ and at $1\ \mathrm{K}$.

(e) Can any positive temperature make more moments point against the field than along it? What
would a crystal in such a state have to be?

## Problem 4 — measuring the finite-bath exponent

<!-- objectives: OBJ-11-6 -->

This problem is meant to be finished in the laboratory.

(a) Use `ensembles.bath_size_sweep` to compute the largest gap between the exact marginal and
the Boltzmann distribution for a two-level system with a gap of one quantum, on baths of $20$,
$40$, $80$, $160$, $320$ and $640$ oscillators, at two quanta per oscillator.

(b) Fit the exponent $\alpha$ in $\max_k |P_k - P_k^{\mathrm{B}}| \propto N_{\mathrm{bath}}^{\alpha}$ with
`validation.scaling_exponent`. Compare with your prediction in problem 2(d).

(c) Repeat at one quantum per oscillator for a three-oscillator Einstein solid. Does the exponent
depend on the system? Does the prefactor?

(d) Why does the laboratory ask for bath sizes at which $q_{\mathrm{tot}}$ is a whole number
exactly, rather than any bath size at all?

## Problem 5 — the atmosphere as a Boltzmann factor

<!-- objectives: OBJ-11-8 -->

(a) A molecule of mass $m$ in an atmosphere at uniform temperature $T$ has gravitational energy
$m g h$. Use the Boltzmann factor to show that the pressure falls as $P(h) = P(0)\, e^{-h/H}$,
and give $H$.

(b) Derive the same result from hydrostatic equilibrium, $\mathrm{d}P/\mathrm{d}h = -\rho g$,
and the ideal-gas law. What does the agreement tell you?

(c) Estimate the scale height of nitrogen at $288\ \mathrm{K}$, and of helium at the same
temperature. Why is there almost no helium in the lower atmosphere, yet some high up?

(d) The laboratory's standard-atmosphere table is isothermal at $216.65\ \mathrm{K}$ between
$11$ and $20\ \mathrm{km}$. Fit $\ln P$ against $h$ there, and deduce the mean molecular mass of
air from the slope. Then explain why the same fit from $0$ to $11\ \mathrm{km}$ is not a
straight line.

## Problem 6 — why temperature is universal (challenge)

<!-- objectives: OBJ-11-4, OBJ-11-5 -->

Two different small systems, A (levels $E_a$, degeneracies $g_a$) and B (levels $E_b$,
degeneracies $g_b$), are both in contact with one Einstein bath, and the three together are
isolated.

(a) Write the exact probability $P(a, b)$ that A is in level $a$ and B in level $b$.

(b) Show that for a large bath $P(a, b)$ factorizes into a function of $a$ times a function of
$b$, and that both factors carry the *same* $\beta$. Identify $\beta$.

(c) For a bath of only three oscillators, show that $P(a, b)$ does not factorize. What physical
statement about A and B does the failure of factorization make?

(d) Using (b), explain why two thermometers made of different materials, placed in the same bath,
read the same temperature — and why a thermometer never needs to know what the bath is made of.

(e) Assemble the whole argument of this module in three steps — one postulate, one derivative,
one exponential — and label each step with its epistemic status: assumed, defined, or derived.
