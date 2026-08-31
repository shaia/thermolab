---
title: Problem set — probability and emergence
short_title: 03 · Problems
---

# Problem set: probability and emergence

Exam-style problems. Work the first three with a pen before touching a computer; the last five
are meant to be finished numerically, in the module's laboratory notebook.

Throughout, a walk of $n$ steps has independent, identically distributed steps $s_i$ with mean
$\mu_1$ and variance $\sigma_1^2$, and $x_n = s_1 + \cdots + s_n$. Nothing in this problem set
carries a unit.

## Problem 1 — the binomial from the ground up

<!-- objectives: OBJ-03-2 -->

Write the number of right-steps in $n$ coin flips as $k = \sum_{i=1}^{n} b_i$, where each $b_i$
is $1$ with probability $p$ and $0$ otherwise.

(a) Compute $\langle b_i \rangle$ and $\operatorname{Var}(b_i)$ directly from the definition.

(b) Use additivity of means and of variances to obtain $\langle k \rangle = np$ and
$\operatorname{Var}(k) = np(1-p)$, stating clearly where independence is used and where it is
not.

(c) The walker's position is $x = 2k - n$. Deduce $\langle x \rangle$ and
$\operatorname{Var}(x)$, and check that the fair-coin case reproduces $\sigma_x = \sqrt{n}$.

(d) At fixed $n$, for which value of $p$ is $\operatorname{Var}(k)$ largest? Explain in one
sentence why that answer is intuitively right.

## Problem 2 — de Moivre–Laplace by hand

<!-- objectives: OBJ-03-4, OBJ-03-2 -->

Let $P(k) = \binom{n}{k} p^k q^{n-k}$ with $q = 1-p$.

(a) Using Stirling's approximation, show that $\ln P(k)$ is stationary at $k = np$.

(b) Expand $\ln P(k)$ to second order about that point and show that the coefficient of
$(k - np)^2$ is $-1/(2npq)$.

(c) Fix the prefactor by requiring the resulting Gaussian to have unit area, and hence obtain

$$
P(k) \approx \frac{1}{\sqrt{2\pi npq}} \exp\!\left[-\frac{(k-np)^2}{2npq}\right] .
$$

(d) Evaluate both the exact and the approximate $P(k = 50)$ for $n = 100$, $p = 1/2$, and
quote the relative error.

(e) Repeat (d) for $k = 90$. Explain why the relative error is now enormous, and say what that
implies about using this approximation for rare events.

## Problem 3 — deviation, error, and a mean of means

<!-- objectives: OBJ-03-5 -->

A quantity has standard deviation $\sigma_1$. You measure it $N$ times and average.

(a) Show that the standard error of the average is $\sigma_1/\sqrt{N}$.

(b) You now repeat that whole procedure $M$ times, obtaining $M$ averages, and average those.
What is the standard error of the final number? Show that it depends only on $MN$, and explain
why that had to be so.

(c) A student reports: "I took 400 measurements, so the standard deviation of my data is
$\sigma_1/20$." Identify the error precisely, and state what quantity *is* equal to
$\sigma_1/20$.

(d) You need to halve an error bar. By what factor must the number of measurements grow, and
what does that imply about buying precision by brute force?

## Problem 4 — computational: the exponent for a different step

<!-- objectives: OBJ-03-1, OBJ-03-5 -->

Using `thermolab.sampling`:

(a) Generate 5000 walkers taking 1024 steps drawn uniformly from $[-1, 1]$, and measure the
cloud's spread at $t = 4, 16, 64, 256, 1024$.

(b) Fit the exponent with `validation.scaling_exponent` and report it with an uncertainty
obtained from a seed study of at least eight seeds.

(c) Compare the measured coefficient with $\sigma_1$ for the uniform step, which you should
compute analytically first. State the agreement as a relative error.

(d) Repeat (a)–(c) for the biased coin. Which of the exponent and the coefficient changed, and
which did not?

## Problem 5 — computational: how often does a walker come home?

<!-- objectives: OBJ-03-6, OBJ-03-1 -->

(a) For a $\pm 1$ walk, measure the fraction of walkers standing exactly at the origin after
$t$ steps, for even $t$ from 2 to 1024, using at least $10^4$ walkers.

(b) Plot that fraction against $t$ on log-log axes and fit the exponent. Explain the value you
get in terms of the results derived on the module page. (Hint: the cloud has spread over
$\sim\sqrt{t}$ sites, and the walkers must be distributed among them somehow.)

(c) Explain why the answer to (b) says nothing about whether a walker *ever* returns to the
origin, and why those are genuinely different questions.

(d) Does a walker who has just returned to the origin behave any differently from one who has
never left it? Answer from the model specification, then test it numerically.

## Problem 6 — challenge: two dimensions

<!-- objectives: OBJ-03-1 -->

A walker takes independent steps in $x$ and in $y$, each drawn from the same distribution.

(a) Show analytically that $\langle r_t^2 \rangle = 2\sigma_1^2 t$, where $r_t$ is the distance
from the origin.

(b) Measure it with `random_walk(..., dim=2)` and confirm the coefficient $2$.

(c) Is the distribution of $r_t$ itself Gaussian? Compute it numerically, and explain what you
find. (The distribution of a distance and the distribution of a coordinate are not the same
object, and the difference is the point of this part.)

## Problem 7 — challenge: measuring the cost of correlation

<!-- objectives: OBJ-03-3 -->

The persistent walk repeats its previous step with probability $q$ and otherwise draws afresh.

(a) Show analytically that the correlation between steps separated by $j$ is $q^{\,j}$.

(b) Sum the covariance matrix to obtain the long-time variance $t(1+q)/(1-q)$.

(c) Measure $\operatorname{Var}(x_t)/t$ with `correlated_walk` for
$q \in \{0, 0.25, 0.5, 0.75, 0.9\}$ at $t = 2000$, and compare with (b). Report each as a
relative error.

(d) Standardise the $q = 0.9$ sums with the *correct* variance from (b) rather than with
$\sigma_1\sqrt{t}$, and show that the histogram now matches the Gaussian. State in one sentence
what this means about which part of the central limit theorem the correlation actually broke.

## Problem 8 — challenge: a failure of a different kind

<!-- objectives: OBJ-03-3 -->

Now replace the steps with draws from a Cauchy distribution (`rng.standard_cauchy`), whose
steps are independent and identically distributed but have no finite variance.

(a) Estimate the variance of a Cauchy sample of size $10^3$, then of $10^4$, then of $10^5$.
Describe what happens and explain it.

(b) Build a walk from Cauchy steps and measure the spread of the cloud at
$t = 4, 16, 64, 256$. Does it grow as $\sqrt{t}$? Determine the exponent you actually get and
account for it.

(c) Standardise the sums by $\sqrt{t}$ and plot the histogram for growing $t$. Does it collapse
onto anything at all?

(d) Both this problem and problem 7 break the central limit theorem, but they break different
hypotheses and fail in different ways. Contrast them in a short paragraph, and say which of the
two you would be more likely to meet without noticing in real data.
