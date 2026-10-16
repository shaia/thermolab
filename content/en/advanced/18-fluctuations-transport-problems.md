---
title: Problem set — fluctuations and transport
short_title: 18 · Problems
---

# Problem set: fluctuations and transport

Exam-style problems. Work them with a pen before touching a computer; problems 3 and 4 are meant
to be finished in the laboratory, problems 5 and 6 use its data files, and problem 8 — the
course's closing synthesis — is a challenge. Solutions and marking rubrics live with the instructor
material and are deliberately not on this site.

Constants: $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$, $N_A = 6.022 \times 10^{23}\ \mathrm{mol^{-1}}$,
$R = 8.314\ \mathrm{J\,mol^{-1}\,K^{-1}}$, $m_u = 1.661 \times 10^{-27}\ \mathrm{kg}$. Where needed,
$\int_0^\infty e^{-x^2}\,\mathrm{d}x = \sqrt{\pi}/2$ and the mean speed of a Maxwell–Boltzmann gas is
$\bar v = \sqrt{8\kB T/\pi m}$.

## Problem 1 — the noise is a heat capacity

<!-- objectives: OBJ-18-1, OBJ-18-2 -->

(a) Starting from $Z = \sum_s e^{-\beta E_s}$, show that $\langle E \rangle = -\partial\ln Z/\partial\beta$
and $\sigma_E^2 = \partial^2\ln Z/\partial\beta^2$, and hence that $\sigma_E^2 = \kB T^2 C_V$.

(b) For $N$ atoms of a monatomic ideal gas drawn from the canonical distribution, each velocity
component is Gaussian with variance $\kB T/m$. Compute $\sigma_E^2$ directly, without using (a), and
show that it gives $C_V = \tfrac32 N\kB$. If every sample's net momentum is set to zero before its
energy is recorded, what does the same calculation give, and why?

(c) For $N$ independent two-level systems with gap $\Delta$, show that $\sigma_E^2 = N\Delta^2 p(1 - p)$
with $p = 1/(e^{\Delta/\kB T} + 1)$, and that it reproduces module 12's Schottky heat capacity.

(d) Show that $\sigma_E/\langle E \rangle = \sqrt{(1 - p)/(Np)}$ for the systems of (c). Evaluate it at
$\kB T = \Delta$ for $N = 100$ and for a mole.

(e) A gas drawn microcanonically has no energy fluctuation at all, so (a) would assign it
$C_V = 0$. Explain what is wrong with that conclusion, and why it does not contradict the statement
that canonical and microcanonical descriptions agree for a mole of gas.

## Problem 2 — from random walk to the diffusion equation

<!-- objectives: OBJ-18-3, OBJ-18-4 -->

(a) A walker steps $\pm\ell$ with equal probability every $\tau$. Write the master equation for
$P(x, t)$ and, by expanding both sides, derive $\partial_t P = D\,\partial_x^2 P$ with $D = \ell^2/2\tau$.
State the order of the terms you neglect and the limit in which they vanish.

(b) Verify by substitution that $P(x,t) = (4\pi Dt)^{-1/2} e^{-x^2/4Dt}$ solves the diffusion
equation, that it stays normalised, and that its variance is $2Dt$.

(c) On a lattice of spacing $\ell$, derive Fick's law $j = -D\,\partial n/\partial x$ by counting
walkers crossing a plane between two sites in one step. Explain why there is a net flux down the
gradient although no force acts on any walker.

(d) Show that a step distribution with zero mean and variance $\langle s^2 \rangle$ gives
$D = \langle s^2 \rangle/2\tau$. What happens to the derivation for steps drawn from a Cauchy
distribution, and what would you expect a cloud of such walkers to look like?

(e) Oxygen in water has $D \approx 2 \times 10^{-9}\ \mathrm{m^2\,s^{-1}}$. Estimate the time for it to
diffuse across a cell $10\ \mu\mathrm{m}$ wide, across $1\ \mathrm{mm}$ of tissue, and across
$1\ \mathrm{m}$. What does this say about the size of an animal that could do without a circulation?

## Problem 3 — the diffusion coefficient, three ways

<!-- objectives: OBJ-18-5 -->

In the laboratory, generate $10^4$ independent walkers of $1000$ steps with
`transport.walker_trajectories` (step $\ell = 1$, $\tau = 1$).

(a) Measure $D$ with `d_from_msd`, `d_from_histogram` (with `lattice=2.0`) and `d_from_vacf`. Quote
each as value ± error and give your verdict on whether the three are consistent with each other and
with $\ell^2/2\tau$.

(b) Repeat (a) for $10^2$, $10^3$ and $10^4$ walkers. Show that each error bar falls as
$N^{-1/2}$, and explain why the batch method is used to compute them rather than the error bar of
a least-squares fit to $\langle x^2 \rangle$ against $t$.

(c) `d_from_histogram` fits the cloud at four snapshot times. Estimate $D$ from a single early
snapshot instead, at $t = 10\tau$, with `fit_gaussian_variance` (pass `lattice=2.0`) divided by $2t$,
and then from a single late one at $t = 1000\tau$. Does the estimate change? Explain what the fit is
sensitive to that the mean squared displacement is not.

(d) Now give the walkers a persistence $q = 0.9$: each step repeats the one before with probability
$q$, and is otherwise drawn afresh. Compute `d_from_vacf` with the integral cut off
at $K = 5$, $10$, $20$, $50$, $100$ and $500$ steps. Plot the value and its error against $K$, and
explain both trends.

(e) Which of the three estimators is the most precise, and why? Give one reason why a less precise
estimator is still worth computing.

## Problem 4 — memory: from ballistic flight to diffusion

<!-- objectives: OBJ-18-3, OBJ-18-4, OBJ-18-5 -->

(a) A particle's velocity autocorrelation is $C(s) = \langle v^2 \rangle e^{-|s|/\tau_c}$. Using
$\langle x(t)^2 \rangle = 2\int_0^t (t - s)\, C(s)\,\mathrm{d}s$, show that

$$
\langle x(t)^2 \rangle = 2\langle v^2 \rangle \tau_c \left[t - \tau_c\left(1 - e^{-t/\tau_c}\right)\right] .
$$

Find its limits for $t \ll \tau_c$ and $t \gg \tau_c$, and identify $D$.

(b) Sketch $\langle x^2 \rangle$ against $t$ on log-log axes and mark the crossover. Where would you
place it for a nitrogen molecule at room conditions, using $\nu \approx 5 \times 10^9\ \mathrm{s^{-1}}$?

(c) In the laboratory, measure the mean squared displacement of persistent walkers with $q = 0.9$
and $q = 0.98$. Find the time at which the log-log slope falls through $1.5$ and compare it with the
memory time $\tau/(1 - q)$.

(d) Module 04's gas has no collisions between its particles. Show that in a box of side $L$ the mean
squared displacement along one axis settles at $L^2/6$ at long times, by computing
$\langle (x - x')^2 \rangle$ for two independent positions uniform in $[0, L]$. Measure it with
`box_gas_trace` and explain the shape of its velocity autocorrelation.

(e) What would the same collisionless gas do in open space? Explain why "no collisions, no diffusion"
is true both with and without walls.

## Problem 5 — the mean free path, and three transport coefficients

<!-- objectives: OBJ-18-6 -->

(a) A molecule of a hard-sphere gas moves with speed $\bar v$ through a gas of stationary targets of
diameter $d$ at number density $n$. Show that it collides $n\pi d^2\bar v$ times per second. Explain
why the true rate is $\sqrt{2}$ times larger, and derive $\lambda = 1/(\sqrt{2}\, n\sigma)$.

(b) Module 02's van der Waals $b$ per molecule is $\kB T_c/8P_c$, and for hard spheres
$b = \tfrac{2\pi}{3} d^3$. The NIST Chemistry WebBook gives $T_c = 126.192\ \mathrm{K}$,
$P_c = 3.3958\ \mathrm{MPa}$ for nitrogen and $T_c = 150.687\ \mathrm{K}$, $P_c = 4.863\ \mathrm{MPa}$
for argon. Find $d$ for each, and the mean free path, mean speed and collision rate of nitrogen at
$0\,{}^\circ\mathrm{C}$ and one atmosphere. How many molecular diameters, and how many mean spacings,
is $\lambda$?

(c) Using step 8, estimate the viscosity and thermal conductivity of nitrogen ($c_v = \tfrac52\kB$
per molecule) and of argon ($\tfrac32\kB$) at $300\ \mathrm{K}$. The laboratory's data file gives
NIST's reference values at $0.1\ \mathrm{MPa}$: $\eta = 17.89$ and $22.74\ \mu\mathrm{Pa\,s}$,
$\kappa = 25.97$ and $17.84\ \mathrm{mW\,m^{-1}\,K^{-1}}$. Compute the ratios and comment.

(d) Show that $\eta$ and $\kappa$ do not depend on the density. Using the data file, find by what
fraction the viscosity of nitrogen changes between $0.1$ and $1\ \mathrm{MPa}$, and between $1$ and
$10\ \mathrm{MPa}$. Explain the second change. In what regime would you expect the viscosity to
*fall* as the pressure is lowered, and why does the data file not show it?

(e) For argon, NIST's $c_v = 0.3124\ \mathrm{J\,g^{-1}\,K^{-1}}$ at $0.1\ \mathrm{MPa}$. Compute
$\kappa/(\eta c_v)$ and compare it with step 8's prediction. Why does the comparison test the theory
more cleanly than (c) does?

## Problem 6 — Brownian motion and Avogadro's number

<!-- objectives: OBJ-18-8 -->

(a) Beads of buoyant mass $m^*$ in water sink at a drift velocity $m^* g/\zeta$. In sedimentation
equilibrium their number density is $n(z) = n_0 e^{-m^* g z/\kB T}$. By requiring that the drift
flux and Fick's diffusion flux cancel, derive the Einstein relation $D = \kB T/\zeta$.

(b) Derive it again from the Green–Kubo relation, assuming a bead forgets its velocity as
$C(s) = (\kB T/m)\,e^{-\zeta s/m}$. Why does the mass cancel?

(c) A bead of radius $0.50\ \mu\mathrm{m}$ is in water at $293\ \mathrm{K}$, viscosity
$1.00 \times 10^{-3}\ \mathrm{Pa\,s}$. Find $D$ from the Stokes–Einstein relation, the
root-mean-square displacement along one axis in $30\ \mathrm{s}$, and its memory time $m/\zeta$ if the
bead's density is $1200\ \mathrm{kg\,m^{-3}}$. Could Perrin, plotting positions every $30\ \mathrm{s}$,
have seen the ballistic regime?

(d) The laboratory's file `18-perrin-projections.csv` is Perrin's 1909 table of the sizes of the
horizontal projections of $30$-second displacements of gamboge granules, radius $0.212\ \mu\mathrm{m}$.
For the first series, in water at $17\,{}^\circ\mathrm{C}$ with viscosity $0.011$ poise, fit the
Gaussian with `binned_variance_estimate`, and obtain $D$ and Avogadro's number, each with its
uncertainty. Compare with the defined $N_A = 6.02214076 \times 10^{23}\ \mathrm{mol^{-1}}$.

(e) Perrin's own values of $\langle x^2 \rangle$ for the same series at $30$, $60$, $90$ and $120\ \mathrm{s}$
were $50.2$, $113.5$, $128$ and $144\ \mu\mathrm{m}^2$. Compute $N_A$ from each, and explain why they
scatter more than your error bar in (d) suggests. List three assumptions behind Perrin's $N_A$ that
no error bar computed from his table can include.

## Problem 7 — where transport theory stops

<!-- objectives: OBJ-18-7 -->

(a) Compute the Knudsen number $\lambda/L$ for nitrogen at $300\ \mathrm{K}$ in each of: a pipe of
diameter $1\ \mathrm{cm}$ at one atmosphere; a pore of diameter $100\ \mathrm{nm}$ at one atmosphere;
a vacuum chamber $30\ \mathrm{cm}$ across at $10^{-4}\ \mathrm{Pa}$. Take $d = 0.31\ \mathrm{nm}$. In
which can the gas be described by a viscosity?

(b) A strong shock wave in a gas is a few mean free paths thick. Explain why the local-equilibrium
assumption fails inside it, while it holds well on either side.

(c) When $\lambda$ is much larger than the gap between two parallel plates, one of them moving, the
drag on the moving plate is proportional to the pressure. Explain why, by thinking about where a
molecule that hits the moving plate last collided.

(d) A Pirani vacuum gauge measures the heat lost by a hot wire to the surrounding gas. Use (c)'s
argument to explain why it can measure pressure only below some pressure. The temperature gradient
is steepest within a few diameters of the wire, so take the wire's diameter as the length that
matters, and estimate that pressure for a wire $10\ \mu\mathrm{m}$ thick.

(e) Local equilibrium also requires that conditions change slowly compared with the collision
time. Estimate the collision time in air at room conditions, and the frequency above which a sound
wave would no longer be described by the equations of this module.

## Problem 8 — one gas, the whole course (challenge)

<!-- objectives: OBJ-18-1, OBJ-18-2 -->

A cylinder closed by a piston holds $N$ atoms of a monatomic ideal gas, of mass $m$, in contact with
a heat bath at temperature $T$.

(a) Following module 04, derive the pressure on the piston from the momentum the atoms deliver to
it, and show that $PV = N\kB T$.

(b) The gas is compressed slowly and isothermally from $V$ to $V/2$. Using
$\mathrm{d}U = \dbar Q + \dbar \Won$, find $W_{\mathrm{on}}$ and $Q$, and the entropy changes of the
gas, of the bath and of the two together (modules 05 and 08). What would change if the compression
were sudden?

(c) In contact with the bath the gas is in the canonical ensemble (module 11). Write its partition
function $Z = z^N/N!$ with $z = V/\lambda^3$, and obtain $U$ and $C_V$ from $\ln Z$ (module 12).

(d) Measure the same $C_V$ from the energy fluctuations of canonical samples with
`transport.gas_energy_samples` for $N = 10$, $100$ and $1000$, and check that $\sigma_E/\langle E \rangle$
falls as $N^{-1/2}$. Quote each measurement with its uncertainty.

(e) In one paragraph: what single idea connects (a), (b), (c) and (d)? Your answer should explain why
the steadiness of the pressure in (a) and the noise in (d) are the same fact seen from two sides.
