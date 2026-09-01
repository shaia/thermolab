---
title: Probability and emergence
short_title: 03 · Random walks
module: 03-random-walks
objectives:
  - id: OBJ-03-1
    text: Model a random walk as a sum of independent steps and compute <x_t> = mu_1 t and Var(x_t) = sigma_1^2 t, hence the RMS spread sigma_1 sqrt(t), for any step distribution with finite variance.
  - id: OBJ-03-2
    text: Define the binomial distribution P(k) = C(n,k) p^k (1-p)^(n-k), compute its mean np and variance np(1-p), and map the +/-1 coin walk onto it exactly.
  - id: OBJ-03-3
    text: State the central limit theorem with its hypotheses — independent, identically distributed steps of finite variance — and its conclusion, that (S_n - n mu)/(sigma sqrt(n)) approaches a standard Gaussian; identify which hypothesis fails in a given counterexample.
  - id: OBJ-03-4
    text: Apply the de Moivre-Laplace bridge — approximate the binomial pmf by a Gaussian of mean np and variance np(1-p) — and state where the approximation is trustworthy.
  - id: OBJ-03-5
    text: Distinguish the standard deviation of one quantity from the standard error of an estimated mean, and absolute spread growing as sqrt(N) from relative spread falling as N^(-1/2).
  - id: OBJ-03-6
    text: Explain how a reproducible Gaussian profile emerges from an ensemble of individually unpredictable walkers, without invoking a restoring force or compensation.
---

# Probability and emergence

There is no physics in this module. No energy, no particles, no container, no temperature —
not one symbol with a unit attached. That is deliberate. The course's guiding question is how
predictable macroscopic behaviour comes out of uncertain microscopic behaviour, and the
cleanest way to see the mechanism is to remove every physical prop and watch it work anyway.

(03-random-walks-puzzle)=
## The puzzle: order out of nothing but noise

A drunkard leaves a lamp post. Every second he takes one step, left or right, decided by a
fair coin. He has no destination, no memory of where he has been, and no tendency to return.
After a thousand seconds, where is he?

The honest answer is that nobody knows. Run the experiment and he might be four steps to the
left, or sixty to the right. Run it again and you get a different number. There is no
prediction to make about him at all.

Now put ten thousand independent drunkards under the same lamp post and let them all walk.
After a thousand seconds, count how many are standing at each position.

That histogram is the same every time. Not roughly the same — the same to a precision you can
set your watch by, a smooth bell-shaped curve of a definite width, reproducible to three
figures in an afternoon's computing. It is there whether the walkers flip coins, draw from a
uniform distribution, or use some lopsided rule you invented this morning.

:::{important} The question
Every walker is unpredictable, and no walker is coordinating with any other. Where does the
shape come from — and why is it the *same* shape no matter what the individual steps look
like?
:::

Two things have to be explained, and they are separate. The **width** of the cloud is the
easier one: it is module 0's law of large numbers, read in the other direction. The **shape**
is the harder one, and it is the central limit theorem — the most consequential theorem in
this course, and the reason the rest of it is possible at all.

(03-random-walks-predict)=
## Predict before you calculate

Commit to an answer for each before running anything. Write them down. The point is not to be
right; it is to find out which of your intuitions the simulation is about to overturn.

1. A walker takes 100 steps of $\pm 1$. Roughly how far from the lamp post do you expect to
   find him — about 0, about 10, or about 100?
2. After 500 steps one particular walker is standing at $+30$. Over his next 500 steps, is his
   motion biased back toward zero?
3. The cloud of walkers is visibly getting wider as time goes on. Does that mean the average
   position is drifting?
4. Replace the coin with steps drawn uniformly from $[-1, 1]$, and then with a heavy-tailed
   distribution that occasionally produces a large jump. Does the long-time histogram change
   its *shape*?

:::{note} Why we ask first
Question 2 is the one that catches almost everyone, and it catches them twice — once here and
once again in module 8, wearing a thermodynamic costume. A prediction you have committed to is
the only reliable way to notice you were wrong; reading the answer afterwards always feels
like you knew it.
:::

(03-random-walks-explore)=
## Explore the model

The laboratory notebook lets you set the number of walkers, the number of steps and the step
distribution, then watch the cloud, its histogram, and its width all at once.

Here is the phenomenon in one picture. First a single walker, alone: a jagged line that tells
you nothing. Then the ensemble on the same clock, with the profile of where its walkers are
standing drawn beside them.

:::{figure} ../media/walker-cloud.mp4
:alt: One random-walk path drawn alone, then a cloud of faint paths with a position profile beside it matching a Gaussian curve.
:width: 100%

One walker, then a cloud. On the left, a hundred and twenty paths are drawn — enough to see a
cloud, few enough to still see through it; the profile on the right is built from all four
thousand walkers, which is why it is so much smoother than the picture beside it looks. The
single dark path is present in both acts and behaves identically in both: nothing about it
changed when the others arrived. The red curve is not fitted to that profile — it is the
Gaussian predicted from the step distribution and the elapsed time alone, drawn on top.
:::

The cloud widens, and it widens at a particular rate. The next animation measures it: the blue
line is the spread of the cloud, the dashed red curve is $\sqrt{t}$, and the dark line running
along the bottom is the ensemble average.

:::{figure} ../media/sqrt-spread.mp4
:alt: The measured spread of a walker cloud climbing a square-root curve while the ensemble mean stays flat at zero inside a narrow grey band.
:width: 100%

Width and drift are independent facts. The spread climbs the square-root curve; the mean stays
flat inside the grey band, which is its own three-standard-error uncertainty. A cloud that is
spreading is not a cloud that is moving.
:::

And here is the shape claim, with its counterexample attached. Each coloured curve is a
different step distribution, standardised — shifted and scaled so only its shape remains — as
the number of steps grows.

:::{figure} ../media/clt-collapse.mp4
:alt: Four density curves as the number of summed steps grows; three collapse onto a dashed Gaussian while the fourth stays visibly too wide.
:width: 100%

Three step distributions with nothing in common — a two-point coin, a flat interval, a
heavy-tailed draw — collapse onto the dashed Gaussian as the number of steps grows. The fourth
curve, in violet, is a walk whose steps are *correlated*; it is standardised by the same
formula and stays stubbornly too wide. That curve is the point of the module as much as the
other three are.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** $N$ independent walkers on an unbounded line; each position is the running sum of that walker's own steps, and the observables are the ensemble histogram, its mean and its spread.
- **Dynamics:** at each tick every walker adds one fresh draw from the step distribution, independent across walkers and across time.
- **Boundary:** none — the line is unbounded, and $N$, the number of steps and the step distribution are fixed for one run.
- **Ensemble:** independent trials; each walker repeats the same experiment and nothing interacts with anything else.
- **Ignored:** everything physical — no medium, no collisions, no energy, no units. By design, so that nothing physical can be doing the work.
- **Valid when:** the steps are genuinely independent and have finite variance; a seeded pseudo-random generator satisfies both by construction.
- **Failure modes:** correlated steps (the module's own counterexample), infinite-variance steps such as Cauchy, and any question about one walker's individual path beyond its distribution.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 03 — probability and emergence](/lite/lab/index.html?path=en/labs/03-random-walks.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/03-random-walks.ipynb`.
:::

Three things are worth doing before you read on:

- Watch one walker for 1000 steps, then watch 10,000 of them. Note what changed and what did
  not.
- Switch the step distribution from the coin to the uniform draw and back. Watch the width
  change and the shape not change.
- Push the persistence slider up from 0 and find the value at which the curve visibly stops
  matching the Gaussian.

(03-random-walks-derive)=
## Derive the result

Everything below is mathematics. Nothing is approximated except where it says so.

**System and boundary.** One walker on an unbounded line, and behind it an ensemble of $N$
independent copies. There is no boundary: nothing reflects, absorbs or confines.

**Independent variables.** The number of steps $t$, the number of walkers $N$, and the step
distribution — which enters only through its mean $\mu_1$ and variance $\sigma_1^2$.

**Constraints and approximations.** Steps are independent and identically distributed with
finite variance. That is the whole list, and each item is load-bearing: the verify section
breaks the first one on purpose and the problem set breaks the third.

**Kind of argument.** Purely statistical. There is no sign convention to fix and no
differential to call exact or inexact, because no energy, heat or work appears anywhere in
this module — which is the point of putting it here, before any of them exist.

With that settled, a walker's position after $t$ steps is

$$
x_t = s_1 + s_2 + \cdots + s_t ,
$$

where the steps $s_i$ are independent draws from one fixed distribution with mean $\mu_1$ and
variance $\sigma_1^2$. That is the entire model: a position is a sum of independent draws.

### The width: means and variances add

Module 0 established the two facts we need, and we do not re-derive them here.

:::{admonition} Additivity of means and variances
:class: theorem
For any random variables, expectations add. For **independent** random variables, variances
add as well:

$$
\langle X + Y \rangle = \langle X \rangle + \langle Y \rangle ,
\qquad
\operatorname{Var}(X + Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) .
$$

The first statement needs no hypothesis at all. The second needs independence, and it is the
only place independence enters this section — which is why the counterexample later attacks
exactly here.
:::

Applying both to the sum of $t$ identical, independent steps:

$$
\langle x_t \rangle = \mu_1 t ,
\qquad
\operatorname{Var}(x_t) = \sigma_1^2 t ,
\qquad
\sigma_{x_t} = \sigma_1 \sqrt{t} .
$$

There is the width law, and there is the answer to prediction 1: after 100 coin steps
($\mu_1 = 0$, $\sigma_1 = 1$) the typical distance from the start is $\sqrt{100} = 10$. Not 0,
because the walk does spread; not 100, because the steps cancel far more often than they
conspire.

Notice that the mean and the spread grow at different rates and for different reasons. For a
fair coin $\mu_1 = 0$, so the cloud spreads without going anywhere. For a biased coin the
centre marches linearly while the width still only crawls as $\sqrt{t}$, and by $t = 1000$ the
drift has left the spread far behind. That answers prediction 3: widening and drifting are
independent, and a cloud can do either without the other.

:::{admonition} The walk is not pulled back
:class: model-assumption
Nothing in the model refers to the origin. A walker standing at $+30$ draws his next step
from exactly the same distribution as a walker standing at $-4$, so his expected displacement
over the next 500 steps is $\mu_1 \times 500$ — zero for a fair coin — regardless of where he
is now. The cloud's mean stays at zero not because stray walkers are recalled, but because
walkers who wander right are matched by walkers who wander left. That is prediction 2, and
the laboratory falsifies the alternative directly by conditioning on the far-right walkers and
measuring what they do next.
:::

### The coin walk is exactly binomial

For $\pm 1$ steps we can do better than the first two moments and write down the whole
distribution. In $n$ steps, let $k$ be the number taken to the right. The walker's position is

$$
x = k - (n - k) = 2k - n ,
$$

and $k$ is the number of successes in $n$ independent trials.

:::{admonition} The binomial distribution
:class: definition
For $n$ independent trials each succeeding with probability $p$, the probability of exactly
$k$ successes is

$$
P(k) = \binom{n}{k} p^{k} (1-p)^{n-k} ,
\qquad
\langle k \rangle = np ,
\qquad
\operatorname{Var}(k) = np(1-p) .
$$

The binomial coefficient counts the *orderings*: there are $\binom{n}{k}$ distinct routes that
arrive at the same $k$, and the model gives each route equal probability.
:::

That last sentence is worth pausing on, because module 8 is built on it. The reason the middle
of the histogram is tall is not that the walker prefers the middle. Every individual sequence
of $n$ coin flips is exactly as likely as every other. There are simply astronomically more
sequences with roughly equal numbers of lefts and rights than sequences with all rights.

### From binomial to Gaussian: de Moivre–Laplace

Factorials are awkward and they hide the shape. Take the logarithm of $P(k)$, expand it to
second order about its maximum at $k = np$, and exponentiate. With $q = 1 - p$:

$$
\binom{n}{k} p^{k} q^{n-k}
\;\approx\;
\frac{1}{\sqrt{2\pi n p q}}
\exp\!\left[-\frac{(k - np)^2}{2 n p q}\right] .
$$

:::{admonition} De Moivre–Laplace
:class: theorem
For fixed $p$ and large $n$, the binomial probabilities near the peak are approximated by a
Gaussian of mean $np$ and variance $npq$. The derivation is a second-order Taylor expansion of
$\ln P(k)$; the terms discarded are of relative size $1/\sqrt{n}$, so the approximation is a
statement about the *central* region, several standard deviations wide, and not about the far
tails.
:::

At $n = 100$, $p = 1/2$ the approximation gives the peak height

$$
\frac{1}{\sqrt{2\pi n p q}} = \frac{1}{\sqrt{50\pi}} \approx 0.0798 ,
$$

against the exact binomial value $0.0796$ — an error of a quarter of a percent. Work this one
out by hand once; it is the number the quiz asks for, and it is the first time in this course
that a factorial-free formula reproduces a combinatorial one.

:::{admonition} A Gaussian on a lattice
:class: approximation
The binomial lives on integers and the Gaussian is a continuous density, so the comparison is
between a bar of width 1 and a curve. That mismatch does not go away as $n$ grows — it shrinks
only relative to the width $\sqrt{npq}$ of the distribution. Module 8 uses this same
approximation for the multiplicity of a two-state system, where it is stated inline; this
section is where it comes from.
:::

### The shape: the central limit theorem

De Moivre–Laplace is one distribution's story. The remarkable fact is that the answer does not
depend on the step distribution at all.

:::{admonition} Central limit theorem
:class: theorem
Let $s_1, \ldots, s_n$ be independent, identically distributed random variables with finite
mean $\mu_1$ and finite variance $\sigma_1^2$, and let $S_n = s_1 + \cdots + s_n$. Then the
standardised sum

$$
Z_n = \frac{S_n - n\mu_1}{\sigma_1 \sqrt{n}}
$$

converges in distribution to a standard Gaussian $\mathcal{N}(0,1)$ as $n \to \infty$.

**The hypotheses are the content.** Independent. Identically distributed. Finite variance.
Nothing is assumed about the *shape* of the step distribution, and nothing about it survives
into the limit: only $\mu_1$ and $\sigma_1$ appear in the answer, and they only say where the
Gaussian sits and how wide it is.

The proof — characteristic functions, or a moment expansion — is beyond the core of this
course; a sketch is in the advanced section. What matters here is the statement, because the
statement is what you will use, and the hypotheses are what you will have to check.
:::

Standardising is the whole trick, and it is worth saying plainly what it does. Subtracting
$n\mu_1$ removes the drift; dividing by $\sigma_1\sqrt{n}$ removes the width. Whatever is left
is pure shape — and the theorem says the shape is always the same one.

### Deviation and error are different quantities

One more definition, small and constantly misused.

:::{admonition} Standard deviation and standard error
:class: definition
The **standard deviation** $\sigma_1$ describes the scatter of a single draw. The **standard
error** describes the scatter of an *estimated mean* of $N$ draws:

$$
\mathrm{SE} = \frac{\sigma_1}{\sqrt{N}} .
$$

Same algebra as everything above, applied to a different object. The standard deviation of a
population does not shrink when you measure more of it; your uncertainty about its mean does.
:::

This is the sentence that ties the module to every laboratory that follows. When a later
notebook reports a measurement as `value ± error`, that error is a standard error, and the
$\sqrt{N}$ under it comes from here.

(03-random-walks-verify)=
## Verify computationally

Deriving a formula and trusting it are different things. Each check below is also a test in
the project's suite, so the claims on this page cannot silently rot.

**1. The width law.** Measure the cloud's spread at $t = 4, 16, 64, 256, 1024$ and fit
$\sigma \propto t^{\alpha}$ on log-log axes. The fitted exponent is $0.500$ to within $0.02$,
and the coefficient comes out at $\sigma_1$ for each of the four step distributions — the
exponent is universal, the coefficient is not.

**2. Mean and spread, separately.** The ensemble mean of an unbiased walk stays at zero to
within its own standard error while the spread grows by a factor of eight; a biased walk drifts
linearly at $\mu_1 t$ beside a spread that still only grows as $\sqrt{t}$.

**3. De Moivre–Laplace.** The worst-case gap between the exact binomial and its Gaussian,
measured across the central three standard deviations, shrinks steadily from $n = 25$ to
$n = 400$.

**4. The collapse.** This is the answer to the opening puzzle.

:::{admonition} What the collapse measures
:class: numerical-observation
Standardised sums of coin, uniform and heavy-tailed steps are compared with a standard
Gaussian using the largest gap between their cumulative distributions. All three distances
fall as the number of summed terms grows. Against the floor of $0.006$ set by having only
20,000 samples — the distance a *genuine* Gaussian sample of that size sits from the Gaussian
it was drawn from — the heavy-tailed steps reach $0.004$ by $n = 256$, the uniform steps
$0.012$, and the coin $0.029$.

The coin is the interesting one, and it does not get better by adding samples. Its sums live
on a lattice, so its cumulative distribution is a staircase and a smooth curve can never match
it more closely than half a step. That residual falls as $n^{-1/2}$ — it is the same finite-$n$
lattice effect the approximation box above describes, not a failure of the theorem, and it is
why the honest statement is "these two distributions have reached the sampling floor and the
third is still walking down towards it".

Three distributions with nothing in common produce one curve. That agreement is a measurement,
not a proof; the proof is the theorem above.
:::

**5. The counterexample.** Now break a hypothesis on purpose. Give the walk *persistence*: at
each step it repeats its previous step with probability $q$, and otherwise draws afresh. The
steps are still identically distributed and still have finite variance; only independence is
gone.

:::{admonition} Independence is a hypothesis, not a decoration
:class: model-assumption
Standardised by the same independent-step formula $\sigma_1 \sqrt{n}$, the persistent walk at
$q = 0.9$ sits far from the standard Gaussian and *stays* there as $n$ grows — the distance
stops falling instead of shrinking to the sampling floor.

It is worth being precise about what broke. The shape is not ruined; the walk is still
Gaussian at long times. What is wrong is the width, by a factor

$$
\frac{\operatorname{Var}(x_t)}{t} \longrightarrow \frac{1 + q}{1 - q} ,
$$

which is $19$ at $q = 0.9$. Successive steps are correlated, so variances no longer simply add
and the formula $\sigma_1\sqrt{t}$ underestimates the spread by a factor of $\sqrt{19}$. The
theorem was not wrong; it was applied where its hypothesis does not hold.
:::

:::{admonition} What simulation can and cannot settle here
:class: open-question
Numerical agreement supports the central limit theorem; it cannot establish it. Every run uses
a finite $n$ and a finite sample, and no finite computation distinguishes "converges to a
Gaussian" from "converges to something within $10^{-6}$ of a Gaussian". The theorem is
established by proof, and the simulation shows you what the proof is about — and, in the
persistent walk, what it is not about.
:::

(03-random-walks-transfer)=
## Transfer the idea

- **Multiplicity, in module 8.** The coin walk's $P(k)$ *is* the two-box multiplicity fraction
  $\Omega(N, n)/2^N$ — the same binomial, read as a count of microstates rather than a count
  of routes. The sharp peak that makes a gas stay spread out through the room, and its relative
  width $N^{-1/2}$, are de Moivre–Laplace applied to particles.
- **Pressure, in module 4.** The steady pressure of a gas is an average over an enormous number
  of collisions, and its jitter falls as $N^{-1/2}$. That module measured the width; this one
  supplies the shape, and the reason the shape does not depend on the details of a collision.
- **Diffusion, in module 18.** Let the step size and the time between steps go to zero together
  and the walker cloud's density obeys the diffusion equation. The $\sqrt{t}$ spread is why a
  drop of ink takes minutes to cross a centimetre and years to cross a metre.
- **A Galton board.** Beads falling through a triangular array of pegs, going left or right at
  each one, pile up in a bell curve at the bottom. It is de Moivre–Laplace built out of wood,
  and it works whether or not anyone has proved the theorem.
- **Every error bar you will meet.** Polls, laboratory measurements, and every `value ± error`
  in this course quote a standard error. A poll of 1000 people has a margin near $3\%$
  regardless of the size of the country, because $1/\sqrt{1000} \approx 0.032$.

:::{admonition} Why "Gaussian" turns up everywhere
:class: definition
A quantity that is a **sum of many small independent contributions** is approximately Gaussian
regardless of what the contributions look like. That, and not any special property of the bell
curve itself, is why it appears in measurement errors, in heights, in noise, and in the energy
of a large system. When a quantity is *not* a sum of that kind — the largest of many draws, or
a product rather than a sum — it is generally not Gaussian, and expecting it to be is a
mistake with a name.
:::

(03-random-walks-quiz)=
## Check your understanding

```{include} ../_generated/quiz-03-random-walks.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](03-random-walks-problems.md).

(03-random-walks-explain)=
## Explain it in your own words

Answer in a few sentences each. No number will save you here.

1. A student says: "The walk comes back toward zero because steps to the left cancel steps to
   the right." Part of that sentence is right and part is badly wrong. Separate them.
2. The persistent walk has identically distributed steps with finite variance, and its
   histogram is still not the predicted Gaussian. Which hypothesis of the central limit theorem
   fails, and what exactly does its failure cost?
3. A pollster's margin of error shrinks as more people are surveyed, while the raw scatter in
   the number of votes counted grows. Explain how both can be true at once.
4. Explain, without writing an equation, why the shape of the long-time histogram does not
   depend on what a single step looks like — and name the one thing about the step that does
   survive.

(03-random-walks-advanced)=
## Advanced: three loose ends

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing later in the core course depends on this section.
:::

**Why the theorem is true.** The mechanism is easiest to see through the characteristic
function $\varphi(k) = \langle e^{ikX}\rangle$, which turns sums into products: the
characteristic function of a sum of independent variables is the product of theirs. Standardise
so that $\mu_1 = 0$ and $\sigma_1 = 1$, and expand for small $k$:

$$
\varphi(k) = 1 - \tfrac{1}{2}k^2 + o(k^2)
\quad\Longrightarrow\quad
\left[\varphi\!\left(\frac{k}{\sqrt{n}}\right)\right]^{n}
\longrightarrow e^{-k^2/2} .
$$

The limit is the characteristic function of a standard Gaussian. Read the calculation
backwards and you can see exactly what each hypothesis was for: independence let the
characteristic functions multiply, identical distribution let one $\varphi$ serve for all
$n$ factors, and finite variance is what makes the $k^2$ term exist and be the leading one.
The whole theorem is the statement that only the quadratic term survives the rescaling.

**Walks in two dimensions.** Give each walker an independent step in $x$ and in $y$. Every
result above applies to each coordinate separately, so the mean-square distance from the origin
is the sum of two identical contributions,

$$
\langle r_t^2 \rangle = \langle x_t^2 \rangle + \langle y_t^2 \rangle = 2\sigma_1^2 t ,
$$

and the cloud is a circular Gaussian widening as $\sqrt{t}$. The picture is prettier and the
mathematics is the same one twice, which is why the core sticks to a line.

**The persistent walk recovers.** The counterexample above is a broken width, not a broken
shape, and the repair is exact. Successive steps of the persistent walk have correlation $q^j$
at separation $j$, so summing the covariance matrix instead of just the diagonal gives

$$
\operatorname{Var}(x_t) = t\left(1 + 2\sum_{j=1}^{\infty} q^{\,j}\right) = t\,\frac{1+q}{1-q}
$$

in the long-time limit. Substituting this variance in place of $\sigma_1^2 t$ makes the
standardised histogram collapse onto the Gaussian after all. The general statement — a central
limit theorem for sequences with decaying correlations — is what lets statistical mechanics use
Gaussian fluctuation formulas for systems whose particles very much do interact, provided the
correlations die away fast enough.
