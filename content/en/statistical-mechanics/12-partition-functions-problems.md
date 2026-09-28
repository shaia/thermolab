---
title: Problem set — partition functions
short_title: 12 · Problems
---

# Problem set: partition functions

Exam-style problems. Work them with a pen before touching a computer; problem 5 is meant to be
finished in the laboratory, and problems 6 and 7 are challenges. Solutions and marking rubrics
live with the instructor material and are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$, $h = 6.626 \times 10^{-34}\ \mathrm{J\,s}$,
$\mu_{\mathrm{B}} = 9.274 \times 10^{-24}\ \mathrm{J\,T^{-1}}$ and
$1\ \mathrm{eV} = 1.602 \times 10^{-19}\ \mathrm{J}$ throughout. Write $\beta = 1/(\kB T)$.

## Problem 1 — the mean energy from Z

<!-- objectives: OBJ-12-2 -->

(a) Starting from $Z = \sum_s e^{-\beta E_s}$ and $P_s = e^{-\beta E_s}/Z$, show that

$$
U = \sum_s E_s P_s = -\frac{\partial \ln Z}{\partial \beta} .
$$

(b) Use it to find the mean energy of a two-level system with levels $0$ and $\Delta$, and check
your result against module 11's.

(c) A system has three non-degenerate levels at $0$, $\varepsilon$ and $2\varepsilon$. Find $Z$ and
$U$, and give $U$ in the limits $\kB T \ll \varepsilon$ and $\kB T \gg \varepsilon$.

(d) Every energy level of a system is shifted by the same constant $E_0$. What happens to $Z$, to
$U$ and to the probabilities $P_s$? Which of these is physical?

(e) Show that $U$ can also be written $U = \kB T^2\, \partial \ln Z/\partial T$.

## Problem 2 — fluctuations and heat capacity

<!-- objectives: OBJ-12-3 -->

(a) Show that $\partial^2 \ln Z/\partial\beta^2 = \langle E^2 \rangle - \langle E \rangle^2$.

(b) Using $U = -\partial \ln Z/\partial\beta$ and the chain rule, show that the same quantity equals
$\kB T^2 C_V$. State where the assumption of fixed levels is used.

(c) Explain why (b) guarantees $C_V \ge 0$ for every system in canonical equilibrium.

(d) For $N$ independent, identical subsystems, show that $\sigma_E/|U| \propto N^{-1/2}$, and find
the constant of proportionality in terms of one subsystem's $\sigma_1$ and $u_1$.

(e) A paramagnet of $N$ moments at $\mu B = \kB T$: find $\sigma_E/|U|$ in terms of $N$, and
evaluate it for $N = 10^{4}$ and $N = 10^{22}$.

## Problem 3 — the entropy of the Boltzmann distribution

<!-- objectives: OBJ-12-4 -->

(a) Show that $F = -\kB T \ln Z$ satisfies $-(\partial F/\partial T)_{V,N} = (U - F)/T$.

(b) Substituting $\ln P_s = -\beta E_s - \ln Z$, show that

$$
-\kB \sum_s P_s \ln P_s = \kB \left(\ln Z + \beta U\right) .
$$

(c) Hence show that $F = U - TS$ with $S$ the Gibbs entropy of (b).

(d) Show that with fixed levels $\mathrm{d}S = \mathrm{d}U/T$, and explain why this, together with
(b), identifies $S$ as the thermodynamic entropy rather than a new quantity.

(e) A system has a doubly degenerate ground level and nothing else within $100\,\kB T$. What are
$Z$, $F$ and $S$ as $T \to 0$? Comment on the result.

(f) "$F = -\kB T \ln Z$ is the definition of the free energy." Write two or three sentences
correcting this statement.

## Problem 4 — the paramagnet, both ways

<!-- objectives: OBJ-12-6, OBJ-12-7 -->

$N$ independent spin-1/2 moments $\mu$ sit in a field $B$; each has energy $-\mu B$ (along the
field) or $+\mu B$ (against it). Write $x = \mu B/(\kB T)$.

(a) Find $z$, $\ln Z_N$, $U$ and the magnetization $M$ from $U = -MB$.

(b) Show that for $x \ll 1$, $M \approx N\mu^2 B/(\kB T)$ (Curie's law), and that $M \to N\mu$ for
$x \gg 1$. For electron moments in $2\ \mathrm{T}$, below what temperature does the Curie law
overestimate $M$ by more than $10\%$?

(c) Now isolate the paramagnet with exactly $n$ moments against the field. Write $U(n)$ and
$S(n) = \kB \ln\binom{N}{n}$, and sketch $S$ against $U$ over the whole range of $U$.

(d) Using Stirling's approximation, show that
$\beta = (1/\kB)\,\partial S/\partial U = \ln[(N - n)/n]/(2\mu B)$. Where is $\beta = 0$, and
where is it negative?

(e) Show that inverting (d) for $n < N/2$ reproduces the canonical ratio $n/(N - n) = e^{-2x}$
of part (a).

(f) A paramagnet with $n = 0.8N$ is put in contact with a large body at $300\ \mathrm{K}$. Using
$\mathrm{d}S_{\mathrm{tot}}/\kB = (\beta_1 - \beta_2)\,\mathrm{d}U_1$, decide which way energy
flows, and explain in one sentence why "negative temperature is colder than absolute zero" is
wrong.

## Problem 5 — where module 01's thermometer fails

<!-- objectives: OBJ-12-5, OBJ-12-8 -->

This problem is meant to be finished in the laboratory.

(a) For a harmonic oscillator with levels $\hbar\omega(n + 1/2)$, derive $z$, $U$ and $C$, and show
that $U \to \kB T$ and $C \to \kB$ for $\kB T \gg \hbar\omega$.

(b) Show that, measured above the ground state, the temperature of an oscillator with mean energy
$U$ is $T = \hbar\omega / [\kB \ln(1 + \hbar\omega/U)]$, and that for $U \gg \hbar\omega$ this is
$U/\kB + \hbar\omega/(2\kB)$.

(c) Run module 01's simulation (`equilibrium.simulate_energy_exchange`) for two solids of $40$
oscillators at energies of $0.05$, $0.1$, $0.2$, $0.5$, $1$, $2$, $5$ and $10$ quanta per
oscillator, with $8$ seeds each. For each energy, compare module 01's equipartition temperature
with (b)'s, and find the energy per oscillator below which the two differ by more than $10\%$.

(d) Reconstruct the oscillator's $C(T)$ from $\ln z$ alone with `partition.thermo_from_z`. Measure
the order of the stencil by refining the step, and find the step below which the error starts to
grow. Explain the growth.

(e) Module 01's model specification listed "low temperature" as a failure mode. State, in terms
of $\kB T$ and $\hbar\omega$, where that failure begins.

## Problem 6 — isomers and vacancies (challenge)

<!-- objectives: OBJ-12-1 -->

(a) A molecule exists as isomer A, whose ground level is at energy $0$ with degeneracy $g_A$, and
isomer B, whose ground level is at $\Delta$ with degeneracy $g_B$; excited levels of both lie far
above $\kB T$. Treating the molecule as one system, show that in equilibrium
$[B]/[A] = (g_B/g_A)\, e^{-\Delta/(\kB T)}$.

(b) Now include the vibrational excitations of each isomer, with partition functions $z_A$ and
$z_B$ measured from each isomer's own ground level. Show that
$[B]/[A] = (z_B/z_A)\, e^{-\Delta/(\kB T)}$, and explain why a "floppier" isomer (lower vibrational
frequencies) can be favoured at high temperature even if its ground level is higher.

(c) A lattice site is either occupied (energy $0$) or vacant (energy $E_{\mathrm{v}}$). Find the
vacant fraction as a function of $T$. For $E_{\mathrm{v}} = 1.28\ \mathrm{eV}$, evaluate it at
$1356\ \mathrm{K}$ and compare with module 11's estimate $e^{-E_{\mathrm{v}}/\kB T}$.

(d) Find the vacancies' contribution to the heat capacity of a crystal of $N$ sites, and the
temperature at which it peaks. Why is this peak never observed in copper?

## Problem 7 — Sackur–Tetrode from Z (challenge, advanced)

<!-- objectives: OBJ-12-4 -->

Take as given that one particle of mass $m$ in a volume $V$ has $z = V/\lambda^3$, with
$\lambda = h/\sqrt{2\pi m\kB T}$.

(a) Show that $U = \tfrac32 N\kB T$ follows from either $Z_N = z^N$ or $Z_N = z^N/N!$.

(b) With $Z_N = z^N$, compute $S$ and show that $S(2N, 2V) - 2S(N, V) = 2N\kB\ln 2$. Explain why
this is unphysical, and how it relates to module 08's Gibbs paradox.

(c) With $Z_N = z^N/N!$ and Stirling's approximation, derive
$S = N\kB[\ln(V/(N\lambda^3)) + 5/2]$.

(d) Evaluate $\lambda$ and $S/(N\kB)$ for argon ($m = 39.95\ \mathrm{u}$) at $300\ \mathrm{K}$ and
$1\ \mathrm{bar}$, and compare with the measured standard molar entropy,
$154.8\ \mathrm{J\,mol^{-1}\,K^{-1}}$.

(e) Show that the ideal-gas law follows from $P = -(\partial F/\partial V)_{T,N}$, and explain why
the $N!$ does not affect it.
