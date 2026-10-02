---
title: Problem set — phase coexistence
short_title: 14 · Problems
---

# Problem set: phase coexistence

Exam-style problems. Work them with a pen before touching a computer; problems 4 and 5 are meant
to be finished in the laboratory, and problem 6 is a challenge. Solutions and marking rubrics
live with the instructor material and are deliberately not on this site.

Take $\kB = 1.381 \times 10^{-23}\ \mathrm{J\,K^{-1}}$, $R = 8.314\ \mathrm{J\,mol^{-1}\,K^{-1}}$
and $N_A = 6.022 \times 10^{23}\ \mathrm{mol^{-1}}$ throughout. Carbon dioxide has
$T_c = 304.13\ \mathrm{K}$ and $P_c = 7.3773\ \mathrm{MPa}$; water has $T_c = 647.10\ \mathrm{K}$ and
$P_c = 22.064\ \mathrm{MPa}$.

## Problem 1 — the spinodal and where it ends

<!-- objectives: OBJ-14-1 -->

The van der Waals isotherm is $P = \kB T/(v - b) - a/v^2$.

(a) Show that $(\partial P/\partial v)_T = 0$ exactly where $\kB T = 2a(v - b)^2/v^3$, and
explain, using module 09's stability criterion, why the states between the two solutions of this
equation cannot exist.

(b) Show that the right-hand side has its maximum at $v = 3b$, that the maximum equals
$\kB T_c$, and hence that the equation has two solutions for $T < T_c$, one for $T = T_c$ and
none above. What are the two solutions called, and what do they become at $T_c$?

(c) Show that the loop's minimum sits at *negative* pressure for $T < \tfrac{27}{32}\,T_c$.
(Hint: $P = 0$ and $\partial P/\partial v = 0$ together.) What does a negative pressure mean for
a liquid, and why is it not absurd?

(d) Using $a$ and $b$ from carbon dioxide's critical point, find the two spinodal volumes and the
corresponding pressures at $280\ \mathrm{K}$. Express the volumes in $\mathrm{L/mol}$ and compare
with the critical volume $v_c = 3b$.

## Problem 2 — equal areas is equal mu

<!-- objectives: OBJ-14-2, OBJ-14-5 -->

The van der Waals gas has energy per particle $u = \tfrac32\kB T - a/v$ and entropy per particle
$s = \kB[\ln((v - b)\,n_Q) + \tfrac52]$, with $n_Q(T)$ the quantum concentration.

(a) From $\mu = f + Pv$ with $f = u - Ts$ the Helmholtz free energy per particle, show that

$$
\mu(v, T) = -\kB T\ln\frac{v - b}{b} + \frac{\kB T\,b}{v - b} - \frac{2a}{v} + g(T) ,
$$

and give $g(T)$ explicitly.

(b) Verify directly that $(\partial\mu/\partial v)_T = v\,(\partial P/\partial v)_T$, which is
Gibbs–Duhem at fixed $T$.

(c) Integrate $\mathrm{d}\mu = v\,\mathrm{d}P$ along the isotherm from $v_\ell$ to $v_g$, both at
pressure $P_{\mathrm{sat}}$, and show by parts that $\mu_g = \mu_\ell$ is equivalent to
$\int_{v_\ell}^{v_g} P\,\mathrm{d}v = P_{\mathrm{sat}}(v_g - v_\ell)$. Explain in one sentence why
the line integral is legitimate even though it passes through states that do not exist.

(d) Define $L_s = T(s_g - s_\ell)$ and $L_u = (u_g - u_\ell) + P_{\mathrm{sat}}(v_g - v_\ell)$,
both evaluated at any pressure $P$ for which the isotherm has three crossings, with $v_\ell$ and
$v_g$ the outer two. Show that $L_u - L_s = \mu_g - \mu_\ell$, so that the two latent heats agree
exactly at $P_{\mathrm{sat}}$ and nowhere else.

(e) Sketch $\mu$ against $P$ along a sub-critical isotherm. Mark the two spinodal points, the
crossing, and the two metastable branches, and explain why the middle crossing of the horizontal
line is never a state of the fluid.

## Problem 3 — Clausius–Clapeyron, and the end of the curve

<!-- objectives: OBJ-14-4, OBJ-14-5 -->

(a) Starting from $\mu_\ell(T, P_{\mathrm{sat}}(T)) = \mu_g(T, P_{\mathrm{sat}}(T))$ and
Gibbs–Duhem, derive $\mathrm{d}P_{\mathrm{sat}}/\mathrm{d}T = L/(T\,\Delta v)$ with
$\Delta v = v_g - v_\ell$.

(b) Near $T_c$ the van der Waals coexisting volumes are $v_{g,\ell} \approx v_c\,(1 \pm 2\sqrt{t})$
with $t = 1 - T/T_c$. Show that $L \approx 6\,\kB T_c\sqrt{t}$ and $\Delta v \approx 4v_c\sqrt{t}$,
so that both vanish at the critical point while the slope of the coexistence curve stays finite.

(c) Show that the limiting slope is $\mathrm{d}P_{\mathrm{sat}}/\mathrm{d}T \to \kB/(2b)$, i.e.
$\mathrm{d}P_r/\mathrm{d}T_r \to 4$ in reduced variables. Check this against the values
$P_r = 0.9960$ at $T_r = 0.999$ and $P_r = 0.9605$ at $T_r = 0.99$ from the laboratory.

(d) Water boils at $373.15\ \mathrm{K}$ at $1\ \mathrm{atm}$ with $L = 40.7\ \mathrm{kJ/mol}$.
Estimate its boiling point at $0.5\ \mathrm{atm}$, stating the approximations you use.

(e) Ice melts at $273.15\ \mathrm{K}$ at $1\ \mathrm{atm}$ with $L_{\mathrm{fus}} = 6.01\ \mathrm{kJ/mol}$,
and its molar volume exceeds the liquid's by $1.63\ \mathrm{cm^3/mol}$. Find the slope of the
melting curve in $\mathrm{K/bar}$, and explain its sign. Does a $70\ \mathrm{kg}$ skater on blades of
total contact area $2\ \mathrm{cm^2}$ melt ice at $-5\,{}^\circ\mathrm{C}$?

## Problem 4 — one curve for every substance, and how far it is from the truth

<!-- objectives: OBJ-14-3, OBJ-14-2 -->

This problem is meant to be finished in the laboratory.

(a) Explain why the van der Waals coexistence curve, expressed in reduced variables
$P_{\mathrm{sat}}/P_c$ against $T/T_c$, is the same for every substance.

(b) In the laboratory, compute `phases.coexistence_curve` for carbon dioxide and for nitrogen
($T_c = 126.19\ \mathrm{K}$, $P_c = 3.3958\ \mathrm{MPa}$) on the same grid of $T/T_c$ from $0.6$
to $1$, and show that the reduced curves coincide. Report the largest relative difference.

(c) Overlay the measured saturation curve of carbon dioxide, shipped as `data/14-co2-saturation.csv`,
in the same reduced variables. Report the ratio of the model's $P_{\mathrm{sat}}$ to the measured
one at $T/T_c = 0.75$, $0.85$ and $0.95$, and describe how the discrepancy depends on temperature.

(d) A rigid $1\ \mathrm{L}$ cylinder holds $5\ \mathrm{mol}$ of carbon dioxide at $280\ \mathrm{K}$. Using
the model's coexisting volumes at that temperature, find the fraction of the molecules that is
vapour. Repeat using the measured plateau of module 02's isotherm, $v_\ell = 0.0532$ and
$v_g = 0.3834\ \mathrm{L/mol}$. Which number would you trust, and why?

(e) The model's latent heat at $280\ \mathrm{K}$ is $4.12\ \mathrm{kJ/mol}$. Using the measured
slope of the saturation curve, which you can take from the data file by a central difference,
and the measured $\Delta v$ of (d), compute the real latent heat by Clausius–Clapeyron. What
does the comparison say about the model's attraction term?

## Problem 5 — the latent heat of water, with its error bar audited

<!-- objectives: OBJ-14-5, OBJ-14-4 -->

This problem is meant to be finished in the laboratory.

(a) Show that if the vapour is ideal, $v_\ell \ll v_g$ and $L$ is constant,
$\ln P_{\mathrm{sat}} = C - L/(\kB T)$. Which of the three assumptions would you expect to fail
first for water between $0$ and $150\,{}^\circ\mathrm{C}$, and in which direction does each one
bias a fitted $L$?

(b) In the laboratory, fit `phases.clausius_clapeyron_fit` to the $31$ points of
`data/14-water-saturation.csv` and report $L$ with its standard error, in $\mathrm{kJ/mol}$ and in
$\mathrm{MJ/kg}$. Compare with the tabulated $40.66\ \mathrm{kJ/mol}$ at $100\,{}^\circ\mathrm{C}$.

(c) Plot the residuals $\ln P_{\mathrm{data}} - \ln P_{\mathrm{fit}}$ against $T$. Are they random?
What shape do they have, and what does the shape say about the assumption of constant $L$?

(d) Repeat the fit on $275$–$325\ \mathrm{K}$ and on $345$–$405\ \mathrm{K}$. Report both values of
$L$ with their errors, and the boiling point at $1\ \mathrm{atm}$ each fit predicts. Explain why the
two $L$ values differ by far more than their quoted errors, and what the quoted error does and
does not measure.

(e) From the two table rows closest to $373\ \mathrm{K}$ alone, estimate $L$ by the two-point
formula of worked example 3, and explain why this "measurement" from two numbers is closer to
the tabulated value than the fit to all thirty-one.

## Problem 6 — how hot can water get without boiling? (challenge)

<!-- objectives: OBJ-14-7, OBJ-14-1 -->

Microwaved water in a smooth cup is regularly observed to reach $105$ to
$110\,{}^\circ\mathrm{C}$ at atmospheric pressure without boiling, and then to erupt when a spoon or
sugar is dropped in. In careful laboratory experiments, clean water at $1\ \mathrm{atm}$ has been
superheated to about $300\,{}^\circ\mathrm{C}$.

(a) Where, in the $P$–$v$ plane, does a superheated liquid at $1\ \mathrm{atm}$ sit relative to the
binodal and the spinodal? Why is it not forbidden by the stability criterion?

(b) Using $a$ and $b$ for water from its critical point, the van der Waals model's liquid
spinodal reaches $P = 1\ \mathrm{atm}$ at $546\ \mathrm{K}$. Reproduce this number in the laboratory
(the spinodal pressure as a function of $T$ is available from `phases.spinodal_volumes` and the
equation of state), and compare it with the observed limit of $\sim 575\ \mathrm{K}$. Given what
problem 4 showed about the model, is the agreement meaningful?

(c) Why does microwaved water stop at $110\,{}^\circ\mathrm{C}$, a hundred and sixty degrees short
of either number? Estimate the radius of the smallest bubble that can grow at
$110\,{}^\circ\mathrm{C}$ and $1\ \mathrm{atm}$, given water's surface tension
$\sigma = 0.057\ \mathrm{N/m}$ and $P_{\mathrm{sat}}(383\ \mathrm{K}) = 143\ \mathrm{kPa}$: a bubble of
radius $r$ is in mechanical balance when $P_{\mathrm{inside}} - P_{\mathrm{outside}} = 2\sigma/r$.

(d) The work to form that critical bubble is $W^* = 16\pi\sigma^3/(3\,\Delta P^2)$. Evaluate it in
units of $\kB T$ and comment on the probability of its forming by thermal fluctuation alone.
What, then, makes the water in the cup erupt when a spoon is dropped in — and what does this say
about which of the two numbers in (b) a *model of the states* can ever be expected to predict?
