---
title: Problem set — thermal radiation and the heat capacity of solids
short_title: 16 · Problems
---

# Problem set: thermal radiation and the heat capacity of solids

Exam-style problems. Work them with a pen before touching a computer; problems 4 and 5 are meant
to be finished in the laboratory, and problems 6 and 7 are challenges. Solutions and marking
rubrics live with the instructor material and are deliberately not on this site.

Constants: $h = 6.626 \times 10^{-34}\ \mathrm{J\,s}$, $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$,
$c = 2.998 \times 10^{8}\ \mathrm{m\,s^{-1}}$, $N_A = 6.022 \times 10^{23}\ \mathrm{mol^{-1}}$,
$\sigma = 5.670 \times 10^{-8}\ \mathrm{W\,m^{-2}\,K^{-4}}$, and
$a = 4\sigma/c = 7.566 \times 10^{-16}\ \mathrm{J\,m^{-3}\,K^{-4}}$.

## Problem 1 — the two Wien conditions

<!-- objectives: OBJ-16-3, OBJ-16-4 -->

(a) Starting from Planck's law $u_\nu = (8\pi h/c^3)\,\nu^3/(e^{h\nu/\kB T} - 1)$, show that the
maximum of $u_\nu$ lies at $x = h\nu/(\kB T)$ satisfying $x = 3(1 - e^{-x})$.

(b) Derive $u_\lambda$ from $u_\nu$ using $u_\lambda\,|\mathrm{d}\lambda| = u_\nu\,|\mathrm{d}\nu|$,
and show that its maximum lies at $y = hc/(\lambda \kB T)$ satisfying $y = 5(1 - e^{-y})$.

(c) Solve both equations to four significant figures by iterating $x \leftarrow 3(1 - e^{-x})$
from $x = 3$ (and likewise for $y$). Why does this iteration converge, and why so quickly?

(d) Show that $\nu_{\max}\lambda_{\max}/c$ is independent of $T$ and evaluate it. A student says:
"one of the two Wien laws must be wrong, because the peak photon can only have one wavelength."
Answer the student in three sentences.

(e) A spectrum is plotted per unit $\ln\nu$, that is, as $\nu\,u_\nu$. Find the condition for
its maximum and the corresponding $\lambda T$. Show that the same curve results from plotting
$\lambda\,u_\lambda$, and explain why this choice gives a single peak for both variables.

## Problem 2 — the photon gas

<!-- objectives: OBJ-16-4, OBJ-16-5 -->

(a) Using module 04's result that an isotropic gas exerts $P = \tfrac13 n \langle p\,v \rangle$,
show that radiation has $P = u/3$, and that a nonrelativistic monatomic gas has $P = \tfrac23 u$.
Which property of the photon makes the difference?

(b) At fixed volume, $\dbar Q = \mathrm{d}U = T\,\mathrm{d}S$. Starting from $u = aT^4$, derive
$S = \tfrac43 aVT^3$. Where in the derivation did you use the third law, and is the result
consistent with it?

(c) A cavity full of radiation expands slowly and adiabatically to twice its volume. By what
factor does its temperature fall, and by what factor does its energy fall? Where did the energy
go? Use the course's sign convention, and state the sign of the work.

(d) Verify the Euler relation $U = TS - PV + \mu N$ for the photon gas with $\mu = 0$. Then
explain in two sentences why $\mu = 0$ follows from the fact that the walls absorb and emit
photons, rather than from any property of light itself.

(e) Compute the photon number density at $300\ \mathrm{K}$ from $n = 16\pi\zeta(3)(\kB T/hc)^3$,
with $\zeta(3) = 1.202$, and the mean energy per photon in units of $\kB T$. Compare the heat
capacity per unit volume of the radiation in a room with that of the air,
$\approx 880\ \mathrm{J\,m^{-3}\,K^{-1}}$.

## Problem 3 — Einstein and Debye, expanded

<!-- objectives: OBJ-16-6, OBJ-16-7 -->

(a) Starting from $U = 3N\hbar\omega_E/(e^{\theta_E/T} - 1)$, derive the Einstein heat capacity
$C = 3N\kB\,x^2 e^x/(e^x - 1)^2$ with $x = \theta_E/T$.

(b) Expand it for small $x$ to show $C = 3N\kB\left(1 - x^2/12 + O(x^4)\right)$. What did module
01 assume about this solid's heat capacity, and how large is the error of that assumption at
$T = 2\theta_E$?

(c) Show that for large $x$, $C \approx 3N\kB\,x^2 e^{-x}$. Over what temperature range does $C$
fall by a factor of $1000$ if $\theta_E = 300\ \mathrm{K}$, starting from $T = 50\ \mathrm{K}$?
Compare with a $T^3$ law over the same factor.

(d) In the Debye model, $C/(3N\kB) = \langle x^2 e^x/(e^x - 1)^2 \rangle$, the Einstein function
averaged over the modes with weight $3\omega^2/\omega_D^3$ on $0 < \omega < \omega_D$. Use (b) to
show that at high temperature $C = 3N\kB\left(1 - x_D^2/20 + \dots\right)$, $x_D = \theta_D/T$.
Hence find the ratio $\theta_E/\theta_D$ at which the two models agree to this order.

(e) Show that the Debye model gives $C \propto T^3$ at low temperature, using
$\int_0^\infty x^4 e^x/(e^x - 1)^2\,\mathrm{d}x = 4\pi^4/15$, and find the coefficient. Explain
physically why no choice of $\theta_E$ lets the Einstein model do the same.

## Problem 4 — silver, measured

<!-- objectives: OBJ-16-7 -->

The laboratory loads the heat capacity of silver from $1$ to $300\ \mathrm{K}$ tabulated by NIST
(Smith and Fickett, 1995), in $\mathrm{J\,kg^{-1}\,K^{-1}}$; the molar mass of silver is
$0.1078682\ \mathrm{kg\,mol^{-1}}$.

(a) Plot $C/T$ against $T^2$ for $T \le 6\ \mathrm{K}$ and fit a straight line. Interpret the
intercept and the slope, and extract the electronic coefficient $\gamma$ and the Debye
temperature $\theta_D$, each with an uncertainty from the fit.

(b) Subtract $\gamma T$ from the whole table. Measure the log–log slope of the remainder between
$1$ and $5\ \mathrm{K}$, and of the raw data between $1$ and $3\ \mathrm{K}$. Explain the
difference.

(c) Fit the Debye and the Einstein models, one parameter each, to the lattice heat capacity
between $4$ and $100\ \mathrm{K}$, minimizing squared *fractional* residuals. Report each fitted
temperature and the root-mean-square residual. Why fractional residuals and not absolute ones?

(d) For each data point, solve for the $\theta_D$ that the Debye formula needs to reproduce it,
and plot this "running" $\theta_D(T)$ from $2$ to $120\ \mathrm{K}$. What does the drift tell you
about the Debye model? Why does the procedure fail above about $150\ \mathrm{K}$?

(e) Above about $260\ \mathrm{K}$ the measured $C_P$ exceeds $3R$. Name two reasons and estimate
which is larger at $300\ \mathrm{K}$, given for silver $\alpha = 5.7 \times 10^{-5}\ \mathrm{K^{-1}}$
(volume expansivity), $\kappa_T = 1.0 \times 10^{-11}\ \mathrm{Pa^{-1}}$ and molar volume
$1.03 \times 10^{-5}\ \mathrm{m^3\,mol^{-1}}$.

## Problem 5 — the cosmic microwave background

<!-- objectives: OBJ-16-3, OBJ-16-4, OBJ-16-5 -->

The laboratory loads the COBE/FIRAS monopole spectrum: $43$ frequencies, given as wavenumbers
$\tilde\nu$ in $\mathrm{cm^{-1}}$ (so $\nu = 100\,c\,\tilde\nu$), with the specific intensity in
$\mathrm{MJy\,sr^{-1}}$ ($1\ \mathrm{MJy\,sr^{-1}} = 10^{-20}\ \mathrm{W\,m^{-2}\,Hz^{-1}\,sr^{-1}}$)
and its uncertainty in $\mathrm{kJy\,sr^{-1}}$, a thousand times smaller units.

(a) Fit the temperature of a Planck radiance spectrum $B_\nu = (c/4\pi)\,u_\nu$ by minimizing
$\chi^2$. Report $T$, its statistical uncertainty, and $\chi^2$ per degree of freedom. What does
the last number test that the first does not?

(b) Read the data's own peak, in frequency and in $\mathrm{cm^{-1}}$. Convert the spectrum to a
density per unit wavelength and find where *that* peaks. Explain the factor between the two
wavelengths.

(c) The data file states that its spectrum column was built as a $2.725\ \mathrm{K}$ Planck curve
plus the measured residuals. What does this imply about what your fit in (a) can and cannot
establish? What limits the published absolute temperature?

(d) Compute the number density of background photons and their energy density, and compare the
latter with the energy density of starlight in our galaxy, about $10^{-13}\ \mathrm{J\,m^{-3}}$.

(e) The background's temperature falls in inverse proportion to the size of the universe. Using
Problem 2(c), explain why the spectrum stays exactly Planckian as it cools, rather than merely
shifting.

## Problem 6 — a planet's energy balance (challenge)

<!-- objectives: OBJ-16-4 -->

The Earth receives $S = 1361\ \mathrm{W\,m^{-2}}$ from the Sun and reflects a fraction $A = 0.30$.

(a) Explain the factor $4$ in $\sigma T_e^4 = (1 - A)S/4$, and compute $T_e$.

(b) Add one layer of atmosphere that is transparent to sunlight and absorbs all thermal
radiation. Write the energy balance of the layer and of the surface, and show that
$T_s = 2^{1/4}T_e$. Generalize to $n$ layers.

(c) Now let the layer absorb only a fraction $\varepsilon$ of the thermal radiation passing through
it (and, by Kirchhoff's law, emit $\varepsilon\sigma T_a^4$ from each face). Show that
$T_s = T_e\,[2/(2 - \varepsilon)]^{1/4}$, and find the $\varepsilon$ that gives the observed
$288\ \mathrm{K}$.

(d) Using Wien's law, explain why it is reasonable to treat the layer as transparent to sunlight
but absorbing to the planet's own radiation, and name one way in which a real atmosphere is not a
single layer at a single temperature.

## Problem 7 — the Debye temperature from the speed of sound (challenge)

<!-- objectives: OBJ-16-7 -->

Debye's model gives $\theta_D$ in terms of the number density $n = N/V$ and an average speed of
sound, $\omega_D^3 = 6\pi^2 n\,c_s^3$, $\theta_D = \hbar\omega_D/\kB$.

(a) Show that if the longitudinal speed $v_L$ and the two transverse speeds $v_T$ differ, the
density of modes requires the average $3/c_s^3 = 1/v_L^3 + 2/v_T^3$.

(b) Diamond has density $3515\ \mathrm{kg\,m^{-3}}$ and molar mass $12.011\ \mathrm{g\,mol^{-1}}$;
take $v_L = 18.0\ \mathrm{km\,s^{-1}}$ and $v_T = 12.4\ \mathrm{km\,s^{-1}}$. Compute $\theta_D$
and compare with the value $\approx 2230\ \mathrm{K}$ obtained from low-temperature heat capacity.

(c) Repeat for silver: density $10\,490\ \mathrm{kg\,m^{-3}}$, molar mass
$107.87\ \mathrm{g\,mol^{-1}}$, $v_L = 3.65\ \mathrm{km\,s^{-1}}$, $v_T = 1.66\ \mathrm{km\,s^{-1}}$.
Compare with the $\theta_D$ you found in Problem 4(a).

(d) The calculation in (b) and (c) used only elastic properties — a ruler, a balance and a
stopwatch — yet predicted a heat capacity. Explain which modes it is guaranteed to describe
correctly, and why the agreement is best for the low-temperature $\theta_D$.

(e) Using Problem 3(d), estimate the Einstein temperature of diamond that would match the Debye
model at high temperature. Compare it with the $\theta_E$ that reproduces diamond's measured
room-temperature heat capacity, $6.12\ \mathrm{J\,mol^{-1}\,K^{-1}}$, about $1310\ \mathrm{K}$.
What does the discrepancy say about a one-frequency model?
