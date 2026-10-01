---
title: Problem set — chemical potential
short_title: 13 · Problems
---

# Problem set: chemical potential

Exam-style problems. Work them with a pen before touching a computer; problems 4 and 5 are meant
to be finished in the laboratory, and problem 6 is a challenge. Solutions and marking rubrics
live with the instructor material and are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$, $h = 6.626 \times 10^{-34}\ \mathrm{J\,s}$,
$N_A = 6.022 \times 10^{23}\ \mathrm{mol^{-1}}$, $1\ \mathrm{u} = 1.661 \times 10^{-27}\ \mathrm{kg}$
and $g = 9.81\ \mathrm{m\,s^{-2}}$ throughout.

## Problem 1 — two exchanges at once

<!-- objectives: OBJ-13-4 -->

Two systems with fundamental relations $S_1(U_1, V_1, N_1)$ and $S_2(U_2, V_2, N_2)$ are
separated by a fixed wall that conducts heat and lets particles through. The pair is isolated,
with $U_1 + U_2 = U$ and $N_1 + N_2 = N$.

(a) Write $S_{\mathrm{tot}}$ as a function of $U_1$ and $N_1$, and show that its maximum requires
$T_1 = T_2$ and $\mu_1 = \mu_2$.

(b) Near equilibrium, with the temperatures already equal, show that
$\mathrm{d}S_{\mathrm{tot}} = (\mu_2 - \mu_1)\,\mathrm{d}N_1/T$. Which way do particles flow?

(c) Now suppose the temperatures are *not* equal and the wall passes particles but no heat. Show
that the quantity that equalizes is $\mu/T$, not $\mu$. Why can such a wall not really exist for
particles that carry energy?

(d) Explain in two sentences why this argument is "module 09's argument with $N$ in place of
$U$", and name the corresponding result for a movable wall.

## Problem 2 — G = mu N

<!-- objectives: OBJ-13-2 -->

(a) From $\mathrm{d}U = T\,\mathrm{d}S - P\,\mathrm{d}V + \mu\,\mathrm{d}N$ and $G = U - TS + PV$,
derive $\mathrm{d}G = -S\,\mathrm{d}T + V\,\mathrm{d}P + \mu\,\mathrm{d}N$ and hence
$\mu = (\partial G/\partial N)_{T,P}$.

(b) Show that this $\mu$ is the same as $-T(\partial S/\partial N)_{U,V}$.

(c) Using the Euler relation $U = TS - PV + \mu N$, show that $G = \mu N$. Why does it follow that
$\mu$ of a pure substance depends on $T$ and $P$ only?

(d) Show that $F = \mu N - PV$, and explain in one sentence why $F$ is not $\mu N$.

(e) For the ideal gas, write $\mu(T, P)$ explicitly, and show that $(\partial\mu/\partial P)_T = v$,
the volume per particle.

## Problem 3 — a column with a sticky floor

<!-- objectives: OBJ-13-5, OBJ-13-6 -->

A tall isothermal column of nitrogen ($m = 28\ \mathrm{u}$) at $T = 300\ \mathrm{K}$ stands on a
floor of area $A = 1\ \mathrm{cm^2}$ that carries $N_s = 10^{15}$ adsorption sites, each binding one
molecule with energy $\varepsilon = -0.25\ \mathrm{eV}$.

(a) Using $\mu = \kB T\ln(n/n_Q) + m g z$, show that the density in the column is
$n(z) = n(0)\,e^{-z/H}$, and find $H$.

(b) Evaluate $n_Q$ for nitrogen at $300\ \mathrm{K}$, and the chemical potential at the floor when
$n(0) = 2.4 \times 10^{25}\ \mathrm{m^{-3}}$.

(c) The floor's sites are in equilibrium with the gas at $z = 0$. Find the fraction of sites
occupied.

(d) Show that the total number of molecules in the gas above the floor is $n(0) A H$, and compare
it with the number adsorbed.

(e) At what floor density $n(0)$ is half the surface covered? Express the answer as a pressure.

## Problem 4 — how steady is equal mu?

<!-- objectives: OBJ-13-3 -->

This problem is meant to be finished in the laboratory.

Two lattice-gas boxes of $M$ sites each exchange $N$ particles, with box B's floor $\Delta u$ above
box A's.

(a) For a dilute system, find the mean number $\bar N_A$ in box A in terms of $N$ and $\Delta u$.

(b) Treat each particle as independently in A with probability $p = \bar N_A/N$. Show that the
standard deviation of $N_A$ is $\sqrt{N p (1 - p)}$, and that the chemical-potential difference
fluctuates by

$$
\sigma_{\mu_A - \mu_B} \approx \frac{\kB T}{\sqrt{N p (1 - p)}} .
$$

(c) Evaluate (b) for $\Delta u = 2\,\kB T$ and $N = 100$, $10^4$ and $10^{22}$.

(d) In the laboratory, run `chemical.particle_exchange_sim` for $N = 250$, $1000$, $4000$ and
$16\,000$ with $M = 100 N$ and $\Delta u = 2\,\kB T$, each for at least $20$ relaxation times
(`chemical.relaxation_steps`). Measure the standard deviation of $\mu_A - \mu_B$ in the second
half of each run, fit a power law in $N$, and compare the exponent and the prefactor with (b).

(e) Why does the simulated standard deviation come out *smaller* than (b) if the records are
taken too close together? What does this say about the error bar on a time average?

## Problem 5 — a Langmuir isotherm from a simulation

<!-- objectives: OBJ-13-6 -->

This problem is meant to be finished in the laboratory.

(a) A site that is empty (energy $0$) or holds one molecule (energy $\varepsilon$) is in contact
with a particle reservoir at $T$ and $\mu$. Using the grand-canonical weight, derive
$\langle n \rangle = 1/(e^{(\varepsilon - \mu)/\kB T} + 1)$. List the hypotheses you used.

(b) With the gas as the reservoir, $e^{\mu/\kB T} = P/(n_Q \kB T)$. Derive the Langmuir isotherm
$\theta = P/(P + P_0)$ and give $P_0$.

(c) In the laboratory, simulate a surface of $200$ sites at $\varepsilon = -2\,\kB T$ exchanging
particles with a reservoir of $20\,000$ sites at energy $0$, for at least eight total particle
numbers between $20$ and $4000$. For each run, record the surface coverage, the reservoir's mean
occupied fraction $c$, and its chemical potential (`chemical.lattice_gas_mu`).

(d) With $z = e^{\mu/\kB T}$, fit $\theta = z/(z + z_0)$ to your data, with $z_0$ the fit parameter.
Compare $z_0$ with the prediction $e^{\varepsilon/\kB T}$ and quote the fit's uncertainty. Is the
quoted uncertainty trustworthy?

(e) Repeat the fit with the occupied fraction $c$ in place of $z$. Why does $c_0$ come out
smaller than $z_0$, and at which of your particle numbers does the difference arise? What does
this say about using a gas's *density* in the Langmuir isotherm?

## Problem 6 — a membrane ladder (challenge)

<!-- objectives: OBJ-13-7 -->

Three compartments, 1, 2 and 3, sit side by side, separated by two membranes that pass water but
not sugar. Compartment 1 holds pure water; 2 holds a $0.1\ \mathrm{mol/L}$ sucrose solution; 3 holds
$0.3\ \mathrm{mol/L}$. Each compartment is open at the top to a vertical tube of the same
cross-section, and the whole system is at $298\ \mathrm{K}$.

(a) Using the ideal-solution model, show that the solvent's chemical potential in a solution of
solute fraction $x$ at pressure $P$ is $\mu_w^{\circ}(T, P) + \kB T\ln(1 - x)$, and derive
$\Pi = -(\kB T/v)\ln(1 - x) \approx n_s \kB T$.

(b) At equilibrium, which way does water cross each membrane? Rank the three final water levels.

(c) Neglecting the dilution caused by the water that crosses, find the equilibrium height
differences $h_2 - h_1$ and $h_3 - h_2$.

(d) Now include dilution: if each tube has cross-section $0.1\ \mathrm{cm^2}$, each compartment
initially holds $1\ \mathrm{L}$, and all three levels start equal, set up the equations for the
final levels. Solve them numerically, compare with (c), and find how much water leaves
compartment 1.

(e) Explain why the answer to (c) does not depend on the size of the solute molecules, and why a
$0.1\ \mathrm{mol/L}$ solution of sodium chloride would give almost twice the pressure.
