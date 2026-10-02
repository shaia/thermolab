---
title: Problem set — phase transitions and the Ising model
short_title: 15 · Problems
---

# Problem set: phase transitions and the Ising model

Exam-style problems. Work them with a pen before touching a computer; problems 4 and 5 are meant
to be finished in the laboratory, and problem 6 is a challenge. Solutions and marking rubrics
live with the instructor material and are deliberately not on this site.

Energies are in units of the coupling $J$, temperatures in units of $J/\kB$ and fields in units
of $J$, as in the module. The square lattice has $q = 4$ neighbours per site and Onsager's
critical temperature is $\kB T_c = 2J/\ln(1 + \sqrt{2}) = 2.2692\,J$.

## Problem 1 — the acceptance rule is a choice, within limits

<!-- objectives: OBJ-15-2 -->

A Markov chain proposes to flip one spin, chosen uniformly at random, and accepts the proposal
with probability $A(\Delta E)$, where $\Delta E$ is the energy change of the flip.

(a) Show that detailed balance with respect to $p_s \propto e^{-E_s/(\kB T)}$ holds if and only if
$A(\Delta E)/A(-\Delta E) = e^{-\Delta E/(\kB T)}$ for every $\Delta E$. Why does the proposal
step not appear in this condition?

(b) Verify that the Metropolis rule $A = \min(1, e^{-\Delta E/(\kB T)})$ and the Glauber rule
$A = 1/(1 + e^{\Delta E/(\kB T)})$ both satisfy it.

(c) A student proposes $A' = \tfrac12 \min(1, e^{-\Delta E/(\kB T)})$, "to be safe". Does it
sample the right distribution? What does it cost? Explain why no rule can use a constant
$c > 1$ in place of $\tfrac12$.

(d) For the square lattice at $h = 0$ and $\kB T = 2J$, list the possible values of $\Delta E$
for a single flip and the Metropolis and Glauber acceptance probabilities for each. Which rule
accepts more often, and does that make it more correct?

(e) Show that the chain with acceptance $A$ leaves the Boltzmann distribution stationary, by
summing detailed balance over the initial configuration. Then explain why stationarity does not
say how many sweeps the chain needs to reach it.

## Problem 2 — domain walls in one and two dimensions

<!-- objectives: OBJ-15-3 -->

(a) An open chain of $N$ spins at $h = 0$ is all up. Show that introducing one domain wall costs
$\Delta E = 2J$ and gains entropy $\Delta S \approx \kB \ln N$, and hence that $\Delta F < 0$
for $N > e^{2J/(\kB T)}$. Evaluate this threshold at $\kB T = 0.5\,J$ and $\kB T = 0.2\,J$.
What do you conclude about long-range order at any $T > 0$?

(b) The exact energy per spin of the infinite chain is $E/(NJ) = -\tanh(J/(\kB T))$. Show that
this corresponds to a density of domain walls $n_w = (1 - \tanh(J/(\kB T)))/2$ per bond, and
compare $1/n_w$ with the threshold of part (a) at $\kB T = 0.5\,J$.

(c) Now the square lattice, $L \times L$. A domain of reversed spins enclosed by a closed wall
of length $\ell$ bonds costs $2J\ell$. The number of closed walls of length $\ell$ through a
given bond is at most $3^{\ell}$. Show that the free energy of such walls is positive for
$\kB T < 2J/\ln 3$. Evaluate the bound and compare it with Onsager's $T_c$.

(d) Explain in two or three sentences why part (c) *permits* order in two dimensions but does
not *prove* it, and why the same argument cannot be repeated in one dimension.

## Problem 3 — mean field: what it gets right and how wrong it is

<!-- objectives: OBJ-15-4 -->

(a) Starting from a single spin in a field $h_{\mathrm{eff}}$, $\langle s \rangle =
\tanh(h_{\mathrm{eff}}/(\kB T))$, derive the mean-field equation
$m = \tanh((qJm + h)/(\kB T))$, naming the approximation precisely.

(b) Show graphically or by expansion that at $h = 0$ the equation has nonzero solutions only
below $\kB T_c^{\mathrm{MF}} = qJ$.

(c) Expand $\tanh x \approx x - x^3/3$ and show that just below $T_c^{\mathrm{MF}}$,
$m_0 \approx \sqrt{3(1 - T/T_c^{\mathrm{MF}})}$. What is the mean-field exponent $\beta$? What is
the exact exponent on the square lattice?

(d) Above $T_c^{\mathrm{MF}}$, linearize in small $h$ and show that
$\chi = \partial m/\partial h = 1/(\kB(T - T_c^{\mathrm{MF}}))$: the Curie–Weiss law. What is the
mean-field exponent $\gamma$?

(e) By what percentage does mean field overestimate the square lattice's transition
temperature? What does it predict for the chain ($q = 2$), and what is the truth there?

(f) At $\kB T = 2.0\,J$, mean field gives $m_0 = 0.958$ and Onsager–Yang give $0.911$; at
$1.5\,J$, $0.990$ and $0.987$. Explain why mean field is better at the lower temperature.

## Problem 4 — locating T_c from the susceptibility peak

<!-- objectives: OBJ-15-5, OBJ-15-6 -->

Use the laboratory's temperature sweep, or `thermolab.ising.temperature_scan`.

(a) For $L = 8$, $16$ and $32$, scan $\kB T$ from $2.20\,J$ to $2.80\,J$ in steps of $0.02\,J$,
with at least $10^4$ sweeps per temperature after burn-in. Record the temperature of the peak of
$\chi' = N\,\mathrm{Var}(|m|)/(\kB T)$ and its height. Repeat with three more seeds and quote
each peak position with an error.

(b) Finite-size scaling predicts $T_{\mathrm{peak}}(L) = T_c + a\,L^{-1/\nu}$ with $\nu = 1$ for
the square lattice. Fit your three peak positions against $1/L$ and extrapolate to
$L \to \infty$. Compare with Onsager's $T_c$, and state whether the difference is within your
error.

(c) Plot the peak height against $L$ on logarithmic axes and fit a power. The theory says
$\gamma/\nu = 7/4$; what do you find, and why might three small lattices disagree?

(d) A classmate fits $T_{\mathrm{peak}}(L)$ against $1/L^2$ instead and gets a different
extrapolation. What does the choice of the exponent assume, and which of your conclusions is
independent of that assumption?

## Problem 5 — measuring an exponent, and why the answer is biased

<!-- objectives: OBJ-15-6, OBJ-15-7 -->

(a) At $L = 64$, measure $\langle |m| \rangle$ at $\kB T = 1.8$, $1.9$, $2.0$, $2.1$, $2.15$,
$2.2$ and $2.25\,J$, with an error bar on each corrected for the autocorrelation time:
$\sigma/\sqrt{N_{\mathrm{eff}}}$ with $N_{\mathrm{eff}} = n/(2\tau)$. Report $\tau$ at each
temperature. Where is it largest?

(b) Fit $\ln\langle|m|\rangle$ against $\ln(T_c - T)$, using Onsager's $T_c$. What exponent do
you find? Compare with the exact $1/8$.

(c) Repeat the fit using only the three temperatures furthest from $T_c$, then only the three
closest. Explain the difference: name one bias that dominates far from $T_c$ and one that
dominates close to it.

(d) For your point at $2.25\,J$, compare the naive error $\sigma/\sqrt{n}$ with the corrected
one. By what factor were you about to overstate your precision?

(e) Run the $2.25\,J$ point with four different seeds. Do the four values agree within their
corrected error bars? Within the naive ones? What does this say about which error bar to quote?

## Problem 6 — the paramagnet hidden inside the Ising model (challenge)

<!-- objectives: OBJ-15-1, OBJ-15-5 -->

(a) Set $J = 0$. Show that the spins become independent, that the partition function factorizes
into module 12's single-spin form, and that $\langle m \rangle = \tanh(h/(\kB T))$ exactly.

(b) Take the exact chain magnetization from the module,
$m = \sinh(h/(\kB T))/\sqrt{\sinh^2(h/(\kB T)) + e^{-4J/(\kB T)}}$, and show that it reduces to
the result of part (a) as $J \to 0$. Then show that for small $h$ at fixed $J > 0$,
$\chi = \partial m/\partial h|_{h=0} = e^{2J/(\kB T)}/(\kB T)$, and explain physically why
coupling makes the chain *more* susceptible than free spins.

(c) For $J = 0$, verify the fluctuation identity $\chi = N\,\mathrm{Var}(m)/(\kB T)$ directly,
computing $\mathrm{Var}(m)$ for $N$ independent spins.

(d) At $h = 0$ and $J > 0$ on the square lattice, explain why the identity of part (c) still
holds for every finite $N$, but the estimator the laboratory uses below $T_c$ replaces $m$ by
$|m|$. What would go wrong, in a run of $10^4$ sweeps at $\kB T = 2.0\,J$ on an $8 \times 8$
lattice, if you used $m$?
