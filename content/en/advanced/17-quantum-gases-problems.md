---
title: Problem set — quantum statistics
short_title: 17 · Problems
---

# Problem set: quantum statistics

Exam-style problems. Work them with a pen before touching a computer; problems 3, 4 and 6 are
meant to be finished in the laboratory, and problems 7 and 8 are challenges. Solutions and marking
rubrics live with the instructor material and are deliberately not on this site.

Constants: $h = 6.626 \times 10^{-34}\ \mathrm{J\,s}$, $\hbar = 1.055 \times 10^{-34}\ \mathrm{J\,s}$,
$\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$, $m_e = 9.109 \times 10^{-31}\ \mathrm{kg}$,
$m_u = 1.661 \times 10^{-27}\ \mathrm{kg}$, $N_A = 6.022 \times 10^{23}\ \mathrm{mol^{-1}}$,
$R = 8.314\ \mathrm{J\,mol^{-1}\,K^{-1}}$, $G = 6.674 \times 10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$,
$1\ \mathrm{eV} = 1.602 \times 10^{-19}\ \mathrm{J}$. Where needed, take
$\int_0^\infty \sqrt{x}\,(e^x - 1)^{-1}\,\mathrm{d}x = (\sqrt{\pi}/2) \times 2.612$ and
$\int_0^\infty x^{3/2}(e^x - 1)^{-1}\,\mathrm{d}x = (3\sqrt{\pi}/4) \times 1.341$.

## Problem 1 — counting, and the occupation of one state

<!-- objectives: OBJ-17-1, OBJ-17-2 -->

(a) List every state of three particles in two single-particle states for classical (labelled)
particles, identical bosons and identical fermions. If all states are equally likely, what is the
probability that all three particles are in the same state, for classical particles and for
bosons? What does the count for fermions tell you?

(b) Show that $N$ identical bosons can be arranged in $M$ single-particle states in
$\binom{M+N-1}{N}$ ways and $N$ fermions in $\binom{M}{N}$ ways. Show that for $M \gg N$ both
counts approach $M^N/N!$, and explain what this says about module 12's division by $N!$.

(c) A single-particle state of energy $\varepsilon$ is in contact with a reservoir at temperature
$T$ and chemical potential $\mu$. Write its grand partition function $\Xi$ for bosons and for
fermions, and derive $n_{\mathrm{BE}}$ and $n_{\mathrm{FD}}$ from
$\langle n \rangle = \kB T\,\partial \ln\Xi/\partial\mu$.

(d) Show that the variance of the occupation is $n(1 + n)$ for bosons and $n(1 - n)$ for fermions.
What is it for classical particles, whose grand sum carries a factor $1/n!$? Interpret the three
results.

(e) Explain why a Bose gas needs $\mu < \varepsilon_0$, and why nothing of the kind constrains a
Fermi gas.

## Problem 2 — the density of states and the classical criterion

<!-- objectives: OBJ-17-3, OBJ-17-4 -->

(a) The single-particle states of a cube of side $L$ with hard walls have
$\mathbf{k} = (\pi/L)(n_x, n_y, n_z)$ with positive integers. Derive
$g(\varepsilon) = (g_s V/4\pi^2)(2m/\hbar^2)^{3/2}\sqrt{\varepsilon}$. Which step is an
approximation, and when does it fail?

(b) Show that $N = \int_0^\infty g(\varepsilon)\,n(\varepsilon)\,\mathrm{d}\varepsilon$ becomes
$n\lambda^3 = g_s F(\mu/\kB T)$ with $\lambda = h/\sqrt{2\pi m\kB T}$ and
$F(\eta) = (2/\sqrt{\pi})\int_0^\infty \sqrt{x}\,n(x - \eta)\,\mathrm{d}x$.

(c) For classical particles, evaluate $F$ and show $\mu = \kB T\ln(n\lambda^3/g_s)$. Compare with
module 13's $\mu = \kB T\ln(n/n_Q)$.

(d) Compute $n\lambda^3$ for: nitrogen at $300\ \mathrm{K}$ and one atmosphere (molecular mass
$28.0\ m_u$); liquid helium-4 at $2.2\ \mathrm{K}$, density $146\ \mathrm{kg\,m^{-3}}$; the conduction
electrons of copper at $300\ \mathrm{K}$, $n = 8.49 \times 10^{28}\ \mathrm{m^{-3}}$. Classify each.

(e) At the density of nitrogen at one atmosphere and $300\ \mathrm{K}$, below what temperature
would $n\lambda^3$ exceed $1$? Why has nobody ever seen degenerate nitrogen gas?

## Problem 3 — the chemical potential at fixed density

<!-- objectives: OBJ-17-4 -->

Use `quantum.solve_mu` in the laboratory, with the mass and density of liquid helium-4
($M_{\mathrm{He}} = 4.0026\ m_u$, $n = 2.198 \times 10^{28}\ \mathrm{m^{-3}}$) and $g_s = 1$ for all
three statistics.

(a) Plot $\mu/\kB T_c$ against $T/T_c$ from $0.5$ to $10$ for classical particles, bosons and
(hypothetical, spinless) fermions on one axis, with $T_c = 3.15\ \mathrm{K}$.

(b) At what $T/T_c$ does the classical $\mu$ cross zero? Show that the answer is $2.612^{2/3}$ and
explain what goes wrong with the classical description below it.

(c) Where does the bosons' $\mu$ reach zero, and what happens below that temperature? Measure how
$\mu$ approaches zero just above $T_c$: is it linear in $T - T_c$, or faster?

(d) Show that the fermions' $\mu$ tends to $\varepsilon_F$ as $T \to 0$, compute $\varepsilon_F/\kB T_c$
from the closed form, and compare with your curve. Check $\mu = \varepsilon_F[1 - (\pi^2/12)(T/T_F)^2]$
at $T = 0.1\,T_F$.

(e) At what $T/T_c$ do the three curves agree to within $0.01\,\kB T$? Express the answer as a
value of $n\lambda^3$.

## Problem 4 — Bose–Einstein condensation

<!-- objectives: OBJ-17-5 -->

(a) Using $F_{\mathrm{BE}}(0) = 2.612$, derive the condensation temperature and show that below it
$N_0/N = 1 - (T/T_c)^{3/2}$. Why must the ground state be added to the integral by hand?

(b) Show that below $T_c$ the energy is $U = \tfrac32 \times 1.341\, g_s \kB T\, V/\lambda^3$ and the
pressure $P = 1.341\, g_s \kB T/\lambda^3$, independent of the density. Compute $P/(n\kB T)$ at $T_c$.
What does the pressure tell you about the motion of the atoms below $T_c$?

(c) Atoms in experiments are held in a harmonic trap rather than a box. Its single-particle levels
are $\varepsilon = \hbar\omega(n_x + n_y + n_z)$, so the number of states below $\varepsilon$ is
about $\varepsilon^3/(6(\hbar\omega)^3)$. Find $g(\varepsilon)$, show that
$N = 1.202\,(\kB T_c/\hbar\omega)^3$ at condensation, where $1.202 = \zeta(3)$, and that below it
$N_0/N = 1 - (T/T_c)^3$.

(d) Liquid helium-4 at its transition has density $146.1\ \mathrm{kg\,m^{-3}}$. Compute the
ideal-gas $T_c$ and compare with the measured lambda point, $2.177\ \mathrm{K}$. Name two ways in
which liquid helium violates the model specification, and say in which direction you would expect
each to move $T_c$ — or say why you cannot tell.

(e) In the laboratory, compute $N_0/N$ at $T = T_c/2$ for $10^3$, $10^4$, $10^5$ and $10^6$ atoms in
a hard-walled box, using `finite_box_condensate_fraction`. By how much does each exceed the ideal
value? Test whether the excess scales as $N^{-1/3}$ or as $N^{-1/3}\ln N$, and explain why a
surface effect should give the $N^{-1/3}$.

## Problem 5 — the degenerate Fermi gas

<!-- objectives: OBJ-17-6 -->

(a) At $T = 0$ an ideal Fermi gas fills every state below $\varepsilon_F$. Derive
$\varepsilon_F = (\hbar^2/2m)(6\pi^2 n/g_s)^{2/3}$ and $U = \tfrac35 N\varepsilon_F$.

(b) Derive the degeneracy pressure twice: from $P = \tfrac23 U/V$ (module 04), and from the course's
sign convention, using $\dbar Q = 0$ and $\mathrm{d}U = \dbar \Won = -P\,\mathrm{d}V$ for a slow
compression at $T = 0$, with every level proportional to $V^{-2/3}$. Show that both give
$P = \tfrac25 n\varepsilon_F$.

(c) For copper ($n = 8.49 \times 10^{28}\ \mathrm{m^{-3}}$, $g_s = 2$), compute $\varepsilon_F$ in
electronvolts, $T_F$, the Fermi velocity $v_F = \hbar k_F/m_e$ and $P$. Compare $P$ with the
classical $n\kB T$ at $300\ \mathrm{K}$, and $v_F$ with the root-mean-square speed of a classical
electron at $300\ \mathrm{K}$.

(d) The bulk modulus is $B = -V\,\mathrm{d}P/\mathrm{d}V$. Show that the free-electron gas has
$B = \tfrac53 P$, compute it for copper, and compare with copper's measured bulk modulus, about
$1.4 \times 10^{11}\ \mathrm{Pa}$. What does the comparison suggest about what holds a metal up?

(e) A student says: "The electrons in copper resist compression because they repel one another
through the Pauli exclusion principle." Explain what is right and what is wrong in this sentence,
with reference to the model's Ignored line.

## Problem 6 — the electrons in silver, measured

<!-- objectives: OBJ-17-7 -->

The laboratory loads silver's heat capacity from $1$ to $300\ \mathrm{K}$, tabulated by NIST (Smith
and Fickett, 1995) in $\mathrm{J\,kg^{-1}\,K^{-1}}$; silver's molar mass is
$0.1078682\ \mathrm{kg\,mol^{-1}}$ and its density $10\,490\ \mathrm{kg\,m^{-3}}$.

(a) Estimate the electronic heat capacity by the shell argument: about $g(\varepsilon_F)\,\kB T$
electrons can each take up about $\kB T$. Show that $C_{\mathrm{el}} \sim N\kB T/T_F$, and compare
the order of magnitude with $\tfrac32 N\kB$ at $300\ \mathrm{K}$.

(b) Fit $C/T = \gamma + \beta T^2$ to the data below $6\ \mathrm{K}$ with `fit_metal_heat_capacity`.
Report $\gamma$ with its uncertainty, and how it changes if the window ends at $4$ or
$8\ \mathrm{K}$ instead.

(c) Assuming one conduction electron per atom, compute silver's $T_F$ and the free-electron
$\gamma = (\pi^2/2) R/T_F$. Compare with (b).

(d) Find the temperature below which the electrons carry more of silver's heat capacity than the
lattice does, and the fraction they carry at $300\ \mathrm{K}$.

(e) For copper the measured $\gamma$ is $0.695\ \mathrm{mJ\,mol^{-1}\,K^{-2}}$ (Kittel). Compute the
free-electron value and the ratio, called the thermal effective mass. Since
$C_{\mathrm{el}} = (\pi^2/3)\kB^2 T\, g(\varepsilon_F)$, what does the ratio measure?

## Problem 7 — a white dwarf (challenge)

<!-- objectives: OBJ-17-6 -->

A white dwarf of mass $M$ and radius $R$ is a ball of carbon and oxygen nuclei with
$N_e = M/(2m_u)$ degenerate electrons. Treat it as uniform.

(a) Write its energy as $E(R) = \tfrac35 N_e\varepsilon_F - \tfrac35 GM^2/R$, with $\varepsilon_F$
from the mean electron density. Show that $E$ has a minimum and find $R(M)$.

(b) Evaluate $R$ for one solar mass, $1.989 \times 10^{30}\ \mathrm{kg}$, and compare with the radius
of the Earth, $6371\ \mathrm{km}$, and with Sirius B: $1.018$ solar masses, radius
$5630\ \mathrm{km}$.

(c) Why do the nuclei contribute almost nothing to the pressure, although they carry nearly all
the mass?

(d) Compute the Fermi momentum $p_F = \hbar k_F$ at the mean density for one solar mass, and compare
it with $m_e c$. What does the comparison say about the validity of (a)?

(e) For fully relativistic electrons $\varepsilon = pc$, and the mean kinetic energy per electron is
$\tfrac34 p_F c$. Show that the kinetic term then scales as $1/R$, like gravity, and argue that
above some mass no radius gives a minimum. (Chandrasekhar's careful version of this argument gives
about $1.4$ solar masses.)

## Problem 8 — the photon gas as a Bose gas (challenge)

<!-- objectives: OBJ-17-8 -->

(a) Photons have $\varepsilon = \hbar c k$ and two polarizations. Using the box counting of
Problem 2(a), show that their density of states is $g(\varepsilon) = 8\pi V\varepsilon^2/(hc)^3$.

(b) With $\mu = 0$, write $U = \int \varepsilon\, g(\varepsilon)\, n_{\mathrm{BE}}(\varepsilon)\,
\mathrm{d}\varepsilon$ and show by substitution, without evaluating the remaining integral, that
$U \propto V T^4$. Then show that it reproduces module 16's Planck spectrum per unit frequency.

(c) Every photon level is proportional to $1/L = V^{-1/3}$. Repeat Problem 5(b)'s argument to show
$P = U/(3V)$ for photons, and explain the difference from $\tfrac23 U/V$.

(d) Explain why photons in a cavity cannot undergo Bose–Einstein condensation.

(e) In 2010 photons were made to condense in a tiny cavity filled with dye (Klaers and colleagues,
Bonn). There the photons are absorbed and re-emitted by the dye many times before they escape, the
cavity's mirrors give every photon a minimum energy, and the photon number is effectively fixed.
Explain why each of these features is needed for condensation, with reference to step 6 of the
module.
