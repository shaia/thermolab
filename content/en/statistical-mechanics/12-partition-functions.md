---
title: Partition functions
short_title: 12 · Partition functions
module: 12-partition-functions
objectives:
  - id: OBJ-12-1
    text: Compute Z = sum_s exp(-E_s/(k_B T)) for a system with given levels, and explain why the normalization determines everything — the derivatives of ln Z with respect to beta are the moments of the energy distribution.
  - id: OBJ-12-2
    text: Derive U = -d(ln Z)/d(beta) and apply it analytically and numerically to the two-level system, the paramagnet and the harmonic oscillator.
  - id: OBJ-12-3
    text: Prove Var(E) = d^2(ln Z)/d(beta)^2 = k_B T^2 C_V, and show that the relative energy fluctuation of N independent subsystems scales as N^(-1/2).
  - id: OBJ-12-4
    text: Derive F = -k_B T ln Z by checking it against module 10's F = U - TS and S = -(dF/dT)_V, and classify it as a theorem connecting the ensemble to thermodynamics, not as a definition.
  - id: OBJ-12-5
    text: Reconstruct U(T), S(T), F(T) and C_V(T) from Z by controlled numerical differentiation; state the stencil's order, verify it, and explain the truncation–roundoff trade-off in choosing the step.
  - id: OBJ-12-6
    text: Use Z_N = z^N for independent distinguishable subsystems to work the paramagnet — M = N mu tanh(mu B/(k_B T)), the Curie limit M = N mu^2 B/(k_B T), and saturation M -> N mu.
  - id: OBJ-12-7
    text: Read the paramagnet's S(U) dome — beta = (1/k_B) dS/dU crosses zero at the peak and is negative beyond it — and predict that an inverted population gives heat to any body at positive temperature, so that negative temperature is hotter than T = infinity, not colder than absolute zero.
  - id: OBJ-12-8
    text: Recover equipartition, U -> k_B T, as the harmonic oscillator's high-temperature limit, and predict freeze-out (C_V exponentially small) when k_B T << hbar omega.
---

# Partition functions

(12-partition-functions-puzzle)=
## The puzzle: the number you divide by

Module 11 introduced the partition function almost as an afterthought. A system in contact with a
bath at temperature $T$ is found in microstate $s$ with probability $e^{-\beta E_s}/Z$, and $Z$ is
whatever makes those probabilities add up to one:

$$
Z = \sum_s e^{-\beta E_s} ,
\qquad
\beta = \frac{1}{\kB T} .
$$

A bookkeeping constant, it seemed. Now do something that looks pointless with it: take its
logarithm, and differentiate with respect to $\beta$.

:::{figure} ../media/partition-reconstruction.mp4
:alt: Four stacked panels against temperature on a logarithmic axis, for a harmonic oscillator. Dots computed from the partition function start scattered off four smooth curves and settle exactly onto them.
:width: 100%

A harmonic oscillator of level spacing $\varepsilon$, against $\kB T/\varepsilon$ on a
logarithmic axis. The four panels are, top to bottom, the mean energy $U$, the entropy $S$, the
free energy $F$ (all three in units of $\varepsilon$ or $\kB$) and the heat capacity $C$ in units
of $\kB$. The black curves are the exact results, computed from the probabilities level by
level. The blue dots are computed from nothing but the single number $\ln Z$ at each temperature
and its neighbours, by the difference formulas this module derives. The step between neighbours
shrinks as the animation runs (its size relative to $\beta$ is printed in the top panel), and
the dots settle onto the curves. The free energy needs no derivative, only $\ln Z$ itself, so
its dots sit on the curve from the start.
:::

Nothing in the dots knows the levels, the probabilities or the energy. Each dot comes from $\ln Z$
evaluated at three nearby temperatures, and yet the mean energy, the entropy, the free energy and
the heat capacity all come out exactly.

:::{important} The question
$Z$ was introduced as a normalization constant — the number you divide by. Why does it contain
the mean energy, the heat capacity, the entropy and the free energy of the system?
:::

The answer is a short calculation, and it makes $Z$ the central object of equilibrium
statistical mechanics. Once you have it, every thermodynamic quantity follows by
differentiation; the rest of the course computes $Z$ for one system after another.

(12-partition-functions-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. What does $\partial \ln Z/\partial\beta$ give — a quantity you already know, or something new?
   With what sign?
2. A salt of independent magnetic moments sits in a weak magnetic field. You halve the
   temperature at fixed field. Does its magnetization rise or fall, and by roughly what factor?
3. Keep adding energy to that salt until more moments point *against* the field than along it.
   Does its temperature rise without limit, jump to infinity, or turn negative? And if you then
   touch it to a body at room temperature, which way does heat flow?
4. A harmonic oscillator is very hot, $\kB T \gg \hbar\omega$. How much energy does it hold on
   average? And when it is very cold?

:::{note} Why we ask first
Question 3 has an answer that sounds absurd until it is derived; most people get the heat flow
backwards. Question 4 asks you to recall module 06's counting of quadratic terms. Every answer is
collected at the end of the module.
:::

(12-partition-functions-explore)=
## Explore the model

The laboratory has one machine at its centre: a function that is handed $\ln Z$ and nothing else,
and returns $U$, $S$, $F$ and $C$. It is run on three systems — a two-level system, a paramagnet
of many independent moments, and a harmonic oscillator — and every output is checked against
the system's closed-form result. The laboratory then turns the paramagnet upside down, and last
puts module 01's simulated Einstein solid under the oscillator's partition function.

The first animation follows the paramagnet's entropy as energy is poured into it.

:::{figure} ../media/partition-spin-dome.mp4
:alt: Left, a dome-shaped curve of entropy against energy with a tangent line sliding over it from left to right; the tangent tilts up, flattens at the top and tilts down. Right, the tangent's slope against energy, a falling curve that crosses zero at the centre.
:width: 100%

A paramagnet of $N = 100$ moments. Left: its entropy $S/\kB = \ln\Omega$ against its energy in
units of $\mu B$, from all moments along the field ($U = -100\,\mu B$) to all against it
($U = +100\,\mu B$). The red segment is the tangent at the current energy (red dot). Right: the
slope of that tangent, $\beta = (1/\kB)\,\mathrm{d}S/\mathrm{d}U$, in units of $1/(\mu B)$. It
is positive on the left half, zero at the top of the dome, and negative on the right half, where
adding energy *removes* microstates.
:::

The second animation cools an oscillator.

:::{figure} ../media/partition-freeze-out.mp4
:alt: Left, a bar chart of the occupation probabilities of an oscillator's levels, broad at first and collapsing onto the lowest level. Right, heat capacity against temperature on a logarithmic axis, a marker sliding down the curve from a plateau at one to almost zero.
:width: 100%

A harmonic oscillator of level spacing $\hbar\omega$, cooled from $\kB T = 5\,\hbar\omega$ to
$\kB T = 0.08\,\hbar\omega$. Left: the probability of each level $n$ (bars). Right: the heat
capacity $C/\kB$ against $\kB T/\hbar\omega$ (black curve); the dashed line is the equipartition
value $C = \kB$, and the red dot marks the current temperature. While several levels are
occupied the heat capacity sits near the plateau; once only the ground level is left, it
collapses.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** discrete-level model systems whose levels are given inputs — a two-level system with gap $\Delta$; $N$ independent magnetic moments $\mu$ in a field $B$, each at energy $-\mu B$ (along the field) or $+\mu B$ (against it); a harmonic ladder $E_n = \hbar\omega\,(n + 1/2)$. The advanced section adds the ideal gas.
- **Dynamics:** none. Equilibrium averages over the canonical distribution, evaluated as closed forms or as explicit sums; nothing is sampled. (The overlay on module 01's simulation inherits that simulation's random numbers.)
- **Boundary:** contact with an infinite bath at temperature $T$ — module 11's idealization, whose error bar module 11 measured. The levels are held fixed, so no work is done and every change in $U$ is heat.
- **Ensemble:** canonical, exactly: $P_s = e^{-\beta E_s}/Z$.
- **Ignored:** interactions between the subsystems, any shift of the levels beyond the linear Zeeman term, and the exchange of identical particles (it enters only the advanced section's ideal gas).
- **Valid when:** the level spectrum is fixed and known, and the subsystems are independent, so that $Z_N = z^N$.
- **Failure modes:** interacting moments (module 15), identical particles at high density or low temperature (module 17), and levels that move with the state variables.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 12 — partition functions](/lite/lab/index.html?path=en/labs/12-partition-functions.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/12-partition-functions.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Hand the machine $\ln Z$ of a two-level system and compare its $U$ with module 11's closed form.
- Shrink the difference step by factors of two and watch the error; then keep shrinking it, and
  watch the error *grow*.
- Halve the paramagnet's temperature in a weak field, then in a strong one.
- Put an inverted paramagnet in contact with a solid, make the solid as hot as you like, and
  find out which way the energy goes.

(12-partition-functions-derive)=
## Derive the result

**System and boundary.** A system with a fixed list of energy levels — the level energies depend
on nothing that changes during the argument — in contact with a large bath at temperature $T$.
Where the system has a volume, it is held fixed; where it sits in a field, the field is held
fixed.

**Independent variable.** The temperature, through $\beta = 1/(\kB T)$. Everything is a function
of $\beta$ at fixed levels.

**Sign convention.** The course convention holds,

$$
\mathrm{d}U = \dbar Q + \dbar \Won ,
$$

and with the levels fixed no work is done, $\dbar \Won = 0$: every change in the system's mean
energy is heat exchanged with the bath.

**Route.** Seven steps. The partition function is recalled; its first derivative gives $U$, its
second the energy fluctuations and $C_V$; the free energy follows and is checked against module
10; independent subsystems factorize; and two systems are worked in full — the paramagnet, which
leads to negative temperatures, and the harmonic oscillator, which leads back to equipartition.

### Step 1: the partition function, recalled

:::{admonition} The levels are given
:class: model-assumption
Each system in this module is specified by a list of microstates $s$ and their energies $E_s$,
taken as known inputs. Where those levels come from — quantum mechanics, in every case here — is
not derived. A level of energy $E$ holding $g$ microstates is counted $g$ times.
:::

:::{admonition} The partition function
:class: definition
For a system in contact with a bath at temperature $T$,

$$
Z(\beta) = \sum_s e^{-\beta E_s} ,
\qquad
P_s = \frac{e^{-\beta E_s}}{Z} .
$$

$Z$ is dimensionless: every exponent $\beta E_s$ is a ratio of two energies.
:::

$Z$ is a sum of Boltzmann factors, one per microstate. At low temperature only the lowest levels
contribute; as $T$ rises more terms join in. So $Z$ counts, roughly, *how many microstates are
thermally accessible* — which already suggests it knows something.

**Which levels matter.** A level contributes to $Z$ in proportion to $e^{-\beta E}$. A level
$5\,\kB T$ above the ground state is occupied less than one time in a hundred ($e^{-5} = 0.0067$);
one $10\,\kB T$ up, less than once in twenty thousand. At any temperature only the levels within
a few $\kB T$ of the ground state matter, and the rest of the spectrum might as well not exist.

### Step 2: the mean energy

Differentiate $Z$ term by term. Each term's derivative brings down its own energy:

$$
\frac{\partial Z}{\partial \beta} = -\sum_s E_s \, e^{-\beta E_s} .
$$

Divide by $Z$, and the right-hand side becomes the average of $E_s$ over the Boltzmann
distribution.

:::{admonition} The mean energy from Z
:class: theorem
For a system with fixed levels in the canonical ensemble,

$$
U = \langle E \rangle = \sum_s E_s P_s = -\frac{\partial \ln Z}{\partial \beta} .
$$
:::

The logarithm is not decoration: $\partial \ln Z/\partial\beta = (\partial Z/\partial\beta)/Z$,
and dividing by $Z$ is what turns the weighted sum into an average. That is the whole reason $Z$
knows the energy. It is a sum of exponentials in $\beta$, and differentiating an exponential
brings its exponent down.

For module 11's two-level system, $Z = 1 + e^{-\beta\Delta}$ and

$$
U = -\frac{\partial}{\partial\beta} \ln\left(1 + e^{-\beta\Delta}\right)
= \frac{\Delta\, e^{-\beta\Delta}}{1 + e^{-\beta\Delta}}
= \frac{\Delta}{e^{\beta\Delta} + 1} ,
$$

module 11's result, obtained this time without writing down a single probability.

### Step 3: the heat capacity, and the fluctuations

Differentiate once more. $U = -\partial\ln Z/\partial\beta$ is itself a ratio, so

$$
\frac{\partial^2 \ln Z}{\partial \beta^2}
= \frac{1}{Z}\frac{\partial^2 Z}{\partial\beta^2} - \left(\frac{1}{Z}\frac{\partial Z}{\partial\beta}\right)^2
= \langle E^2 \rangle - \langle E \rangle^2 .
$$

The second derivative is the *variance* of the energy: in the canonical ensemble the system's
energy is not fixed, and this is how widely it spreads. The same second derivative is also
$-\partial U/\partial\beta$, and converting from $\beta$ to $T$ with
$\mathrm{d}\beta = -\mathrm{d}T/(\kB T^2)$ gives

$$
-\frac{\partial U}{\partial \beta} = \kB T^2 \frac{\partial U}{\partial T} .
$$

With the levels fixed — fixed volume and particle number — every change of $U$ is heat, so
$\partial U/\partial T$ is the heat capacity at constant volume, $C_V = (\partial U/\partial T)_{V,N}$.

:::{admonition} Fluctuations and heat capacity
:class: theorem
For a system with fixed levels in the canonical ensemble,

$$
\sigma_E^2 = \langle E^2 \rangle - \langle E \rangle^2 = \frac{\partial^2 \ln Z}{\partial\beta^2}
= \kB T^2 \, C_V .
$$
:::

Two consequences follow at once. First, $C_V \ge 0$ for *every* system in canonical equilibrium,
because a variance cannot be negative: the thermal stability that module 09 demanded of $S(U)$
is automatic here. Second, a quantity that describes the *response* of a system — how much heat it
takes to warm it — is fixed by how much its energy *fluctuates* when left alone. Module 18 is
built on that idea; here it costs three lines.

This is why $\ln Z$ rather than $Z$ is the natural object. Its derivatives in $\beta$ are, up to
sign, the **cumulants** of the energy distribution — the mean, the variance and the higher ones in turn. A
function whose derivatives produce a distribution's moments is called a **generating function**,
and $\ln Z$ is the generating function of the canonical energy distribution. That is the answer
to the puzzle: the normalization is not a single number but a *function* of $\beta$, and its
shape encodes every moment of the distribution it normalizes.

### Step 4: the free energy — derived, not defined

The mean energy and its fluctuations came out of $\ln Z$ directly. The entropy and the free
energy need one more step, and it is worth doing slowly, because it is where the statistical and
the thermodynamic descriptions have to meet.

Module 10 defined the Helmholtz free energy $F = U - TS$, with no mention of microstates, and
showed that $S = -(\partial F/\partial T)_{V,N}$. Consider the candidate

$$
F_Z \equiv -\kB T \ln Z .
$$

Take its temperature derivative. Using $\partial\ln Z/\partial T = (\partial\ln Z/\partial\beta)(\mathrm{d}\beta/\mathrm{d}T) = U/(\kB T^2)$,

$$
-\frac{\partial F_Z}{\partial T} = \kB \ln Z + \kB T \frac{U}{\kB T^2}
= \frac{U - F_Z}{T} .
$$

So if we define $S_Z = -\partial F_Z/\partial T$, then $F_Z = U - T S_Z$, with $U$ the mean
energy of step 2: the candidate has exactly the structure of module 10's free energy. That is
necessary, but it is not yet proof, because $S_Z$ has so far only been *named*. What has to be
shown is that $S_Z$ is the *thermodynamic* entropy — the one module 07 defined through heat, and
module 08 through counting. Two checks settle it.

**It obeys Clausius.** With the levels fixed,
$S_Z = \kB(\ln Z + \beta U)$, so

$$
\mathrm{d}S_Z = \kB\left(\frac{\partial\ln Z}{\partial\beta}\,\mathrm{d}\beta + U\,\mathrm{d}\beta + \beta\,\mathrm{d}U\right)
= \kB\beta\,\mathrm{d}U = \frac{\dbar Q}{T} ,
$$

since the first two terms cancel ($\partial\ln Z/\partial\beta = -U$) and $\mathrm{d}U = \dbar Q$
at fixed levels. Module 07's entropy is defined, up to a constant, by exactly
$\mathrm{d}S = \dbar Q_{\mathrm{rev}}/T$.

**It counts microstates.** Substituting $\ln P_s = -\beta E_s - \ln Z$ into $-\sum_s P_s \ln P_s$
gives $\beta U + \ln Z$, so

$$
S_Z = -\kB \sum_s P_s \ln P_s ,
$$

the **Gibbs entropy** of the Boltzmann distribution. When all $\Omega$ accessible microstates are
equally probable, $P_s = 1/\Omega$ and this is module 08's $\kB\ln\Omega$ — which also fixes the
constant that Clausius leaves free. As $T \to 0$ the system settles into its $g_0$ ground
microstates and $S_Z \to \kB\ln g_0$, their count.

:::{admonition} The free energy from Z
:class: theorem
For a system with fixed levels in the canonical ensemble at temperature $T$,

$$
F = -\kB T \ln Z ,
\qquad
S = -\left(\frac{\partial F}{\partial T}\right)_{V,N} = \kB\left(\ln Z + \frac{U}{\kB T}\right)
= -\kB\sum_s P_s \ln P_s ,
$$

where $F$ is module 10's Helmholtz free energy $U - TS$ and $S$ is the thermodynamic entropy.
:::

That is a theorem, and it is worth being precise about why. Module 10's $F$ was already defined —
as a Legendre transform of $U$, with nothing statistical about it. The statement
$F = -\kB T\ln Z$ says that a quantity computed from a list of energy levels *equals* that
thermodynamic function, and it had to be checked: the entropy it implies had to obey Clausius and
agree with the count of microstates. Writing $F = -\kB T\ln Z$ as a definition would skip exactly
the step that connects statistical mechanics to thermodynamics.

The payoff is enormous. Module 10 showed that $F(T, V, N)$ is a fundamental relation: every
equilibrium property at fixed temperature follows from it. So $\ln Z$, computed from the levels,
*is* the fundamental relation of the system — pressure, chemical potential and all, once the
levels are allowed to depend on $V$ and $N$.

### Step 5: independent subsystems factorize

Most systems of interest are made of many parts. Suppose a system consists of $N$ subsystems that
do not interact, so that a microstate of the whole is a list $(s_1, s_2, \ldots, s_N)$ of one
microstate for each part and its energy is the sum $E = E_{s_1} + E_{s_2} + \cdots + E_{s_N}$. The
Boltzmann factor of a sum is a product, and the sum over all lists breaks into a product of sums.

:::{admonition} Factorization
:class: theorem
If a system consists of $N$ independent, distinguishable subsystems, each with partition function
$z$, then

$$
Z_N = z^N ,
\qquad
\ln Z_N = N \ln z .
$$
:::

Because $\ln Z_N$ is $N$ times $\ln z$, so is everything derived from it: $U$, $S$, $F$, $C$ and
the variance $\sigma_E^2$ are all extensive. The spread, though, grows only as the square root:

$$
\frac{\sigma_E}{|U|} = \frac{\sqrt{N}\,\sigma_1}{N\,|u_1|} \propto N^{-1/2} ,
$$

the same $N^{-1/2}$ that narrowed module 08's multiplicity peak and module 11's canonical energy
distribution, now arriving from a derivative of $\ln Z$.

"Distinguishable" matters. A crystal's magnetic moments sit on labelled lattice sites, and
swapping two of them gives a different microstate. Identical gas molecules are not labelled, and
counting every permutation as a new microstate overcounts by $N!$. That correction is the subject
of [the advanced section](#12-partition-functions-advanced); nothing in the core needs it.

### Step 6: the paramagnet, worked in full

A **paramagnet** is a material whose atoms carry permanent magnetic moments that do not interact
with one another. In a field $B$, a moment $\mu$ pointing along the field has energy $-\mu B$ and
one pointing against it $+\mu B$ (a spin-1/2 moment, like an unpaired electron, has only these
two orientations). One moment is a two-level system with gap $2\mu B$, and with $x = \mu B/(\kB T)$,

$$
z = e^{x} + e^{-x} = 2\cosh x ,
\qquad
\ln Z_N = N \ln(2\cosh x) .
$$

The energy follows from step 2, and the net moment along the field — the **magnetization**
$M$ — from $U = -MB$:

$$
U = -N\mu B \tanh x ,
\qquad
M = N\mu \tanh\left(\frac{\mu B}{\kB T}\right) .
$$

:::{figure} ../media/partition-paramagnet.png
:alt: Left, magnetization against field over temperature, an S-shaped curve rising linearly then flattening at one, with a straight dashed line along its initial slope. Right, heat capacity against temperature on a logarithmic axis, a single peak.
:width: 100%

(a) The paramagnet's magnetization, $M/(N\mu)$, against $\mu B/(\kB T)$ (black), with the Curie
law $M = N\mu^2 B/(\kB T)$ (dashed) and saturation at $M = N\mu$ (dotted). (b) Its heat capacity
per moment, $C/(N\kB)$, against $\kB T/(\mu B)$ on a logarithmic axis: a single peak — the
**Schottky anomaly** — near $\kB T = 0.83\,\mu B$, dying at both ends.
:::

The two limits are the physics.

- **Weak field or high temperature, $\mu B \ll \kB T$.** $\tanh x \approx x$, so
  $$
  M \approx \frac{N\mu^2 B}{\kB T} .
  $$
  This is **Curie's law**: the magnetization is proportional to $B/T$. Halve the temperature and
  it doubles. The field tries to align the moments, the bath tries to scramble them, and the
  outcome depends only on the ratio of the two.
- **Strong field or low temperature, $\mu B \gg \kB T$.** $\tanh x \to 1$, so $M \to N\mu$: every
  moment is aligned, and no further field can add to it. This is **saturation**.

:::{admonition} Curie's law
:class: approximation
$M = N\mu^2 B/(\kB T)$ is the first term of $N\mu\tanh(\mu B/\kB T)$, valid when
$\mu B \ll \kB T$. For an electron moment in $1\ \mathrm{T}$ at room temperature
$\mu B/(\kB T) = 0.0022$, and the law holds to a few parts per million; at $1\ \mathrm{K}$ it
overestimates the magnetization by $15\%$.
:::

The heat capacity, from step 3, is a two-level system's for each moment, $C = N\kB\,x^2/\cosh^2 x$.
It vanishes when cold (every moment aligned, nothing to excite) and when hot (the moments already
split half and half, and further heating changes nothing), with a peak in between. Such a peak in
the measured heat capacity of a solid is the fingerprint of a set of two-level systems hidden in
it.

**The paramagnet at fixed energy.** So far the paramagnet has been in contact with a bath. Now
isolate it and count instead, as module 08 did for coins. With $n$ of the $N$ moments pointing
against the field, the energy is

$$
U = \mu B\,(2n - N) ,
$$

running from $-N\mu B$ (all aligned) to $+N\mu B$ (all reversed), and the number of microstates
is the binomial coefficient $\Omega = \binom{N}{n}$. The entropy $S = \kB \ln\binom{N}{n}$ is the
dome of the second animation: zero at both ends, where there is only one way to arrange the
moments, and largest at $U = 0$, where half point each way.

Now apply module 09's definition of temperature, $1/T = \partial S/\partial U$. A moment reversed
costs $2\mu B$, and by Stirling $\partial \ln\binom{N}{n}/\partial n = \ln[(N - n)/n]$, so

$$
\beta = \frac{1}{\kB}\frac{\partial S}{\partial U} = \frac{1}{2\mu B}\ln\frac{N - n}{n} .
$$

For $n < N/2$ — more moments along the field than against — $\beta$ is positive, and inverting
gives $n/(N - n) = e^{-2\beta\mu B}$, the Boltzmann ratio of the canonical calculation. At
$n = N/2$ the dome is flat: $\beta = 0$, an infinite temperature. And for $n > N/2$ the dome
slopes *down*: adding energy removes microstates, $\beta$ is negative, and so is $T$.

:::{admonition} Negative temperature
:class: definition
A system whose entropy *decreases* as its energy increases, $\partial S/\partial U < 0$, has a
**negative temperature** by module 09's definition $1/T = \partial S/\partial U$. This needs an
energy spectrum bounded above, so that there are fewer ways to hold more energy near the top — a
paramagnet has one, a gas or an oscillator does not.
:::

What does a negative temperature *mean*? Not what the number suggests. The honest way to find out
is to ask what temperature is for: deciding which way heat flows.

Put the paramagnet (body 1) in contact with any other body (body 2), the pair isolated. Energy
$\mathrm{d}U_1$ passes into body 1 and $\mathrm{d}U_2 = -\mathrm{d}U_1$ leaves body 2, and the
total entropy changes by

$$
\frac{\mathrm{d}S_{\mathrm{tot}}}{\kB} = \beta_1\,\mathrm{d}U_1 + \beta_2\,\mathrm{d}U_2
= (\beta_1 - \beta_2)\,\mathrm{d}U_1 .
$$

The second law, in module 08's counting form, says the pair moves toward more microstates,
$\mathrm{d}S_{\mathrm{tot}} > 0$.
So energy flows *into* body 1 when $\beta_1 > \beta_2$ and *out* of it when $\beta_1 < \beta_2$:
**heat flows from the body with the smaller $\beta$ to the body with the larger one.** For two
positive temperatures this is the familiar rule, hot to cold. But now take an inverted paramagnet,
$\beta_1 < 0$, and any ordinary body at any positive temperature, $\beta_2 > 0$.

:::{admonition} Negative temperatures are hotter than all positive ones
:class: theorem
A system at negative temperature, placed in thermal contact with a system at any positive
temperature, gives energy to it: $\beta_1 < 0 < \beta_2$ makes $\mathrm{d}S_{\mathrm{tot}} > 0$
only for $\mathrm{d}U_1 < 0$. Ordered from cold to hot, the temperature scale runs

$$
+0\ \mathrm{K} \;\to\; +300\ \mathrm{K} \;\to\; +\infty \;=\; -\infty \;\to\; -300\ \mathrm{K} \;\to\; -0\ \mathrm{K} ,
$$

which is simply $\beta$ decreasing from $+\infty$ to $-\infty$.
:::

A negative temperature is not below absolute zero. It is *above* infinite temperature. The
paramagnet with more moments reversed than aligned holds more energy than it would at any
positive temperature — at $T = +\infty$ the moments split exactly half and half — and it will give
some of that energy to anything at a positive temperature it touches, however hot. The quantity
that orders hotness is $-\beta$, not $T$; $T$ merely has an awkward jump from $+\infty$ to
$-\infty$ in the middle, at the top of the dome, where nothing physical happens at all.

This is also why [module 11](11-ensembles.md) found that heating never inverts a two-level
population: a bath at positive temperature has $\beta > 0$ and can only bring the system to
$\beta > 0$. An inverted population is not a very hot equilibrium with a positive-temperature
bath; it has to be made some other way, and [the advanced section](#12-partition-functions-advanced)
says how.

### Step 7: the harmonic oscillator, and equipartition recovered

The last system has infinitely many levels, equally spaced: $E_n = \hbar\omega\,(n + 1/2)$ for
$n = 0, 1, 2, \ldots$ — a quantum harmonic oscillator, and one of module 01's Einstein-solid
oscillators, with $\hbar\omega$ its energy quantum. With $x = \hbar\omega/(\kB T)$ the partition
function is a geometric series,

$$
z = \sum_{n=0}^{\infty} e^{-x(n + 1/2)} = \frac{e^{-x/2}}{1 - e^{-x}} ,
$$

and step 2 gives

$$
U = \hbar\omega\left(\frac{1}{2} + \frac{1}{e^{\hbar\omega/(\kB T)} - 1}\right) .
$$

The $\hbar\omega/2$ is the **zero-point energy**, the ground level's own energy. It shifts $U$ and
$F$ by a constant and changes neither $S$ nor $C$; module 01, counting quanta above the ground
state, simply left it out. Step 3 gives the heat capacity,

$$
C = \kB \left(\frac{\hbar\omega/(\kB T)}{2\sinh\big(\hbar\omega/(2\kB T)\big)}\right)^2 .
$$

- **Hot, $\kB T \gg \hbar\omega$.** Expanding the exponential,
  $U = \kB T + (\hbar\omega)^2/(12\,\kB T) + \cdots \to \kB T$, and $C \to \kB$. This is
  **equipartition**. Module 06 counted $\tfrac12\kB T$ for every quadratic term in the energy;
  an oscillator has two, its kinetic and its potential energy, and holds $\kB T$. The rule
  modules 04 and 06 used by assumption is here a *limit* of a partition function.
- **Cold, $\kB T \ll \hbar\omega$.** The first excited level is out of reach, the oscillator sits
  in its ground state, and
  $$
  C \approx \kB \left(\frac{\hbar\omega}{\kB T}\right)^2 e^{-\hbar\omega/(\kB T)} ,
  $$
  exponentially small. The oscillator can no longer absorb heat in small amounts: its smallest
  bite is a whole quantum $\hbar\omega$, which the bath almost never supplies. The degree of
  freedom has **frozen out**.

:::{admonition} Equipartition
:class: approximation
$U = \kB T$ per oscillator, and $\tfrac12 \kB T$ per quadratic term generally, is the
high-temperature limit of the oscillator's partition function. Its fractional error is about
$(\hbar\omega/\kB T)^2/12$ for $U$; it fails entirely once $\kB T$ falls below the level spacing.
:::

A solid of $N$ atoms has $3N$ vibrational modes. If each held $\kB T$, its heat capacity would be
$3N\kB$ at every temperature — the **Dulong–Petit law**, which fits many solids at room temperature
and fails for all of them when cold, because the modes freeze out. How they freeze out, mode by
mode, is module 16.

(12-partition-functions-verify)=
## Verify computationally

Every number below comes from `thermolab.partition`. Level spacings are
$\varepsilon = 10^{-21}\ \mathrm{J}$ for the two-level gap and the oscillator quantum
($\varepsilon/\kB = 72.4\ \mathrm{K}$), and the paramagnet's moments are Bohr magnetons,
$\mu = 9.274 \times 10^{-24}\ \mathrm{J\,T^{-1}}$, in $B = 1\ \mathrm{T}$
($\mu B/\kB = 0.672\ \mathrm{K}$).

**1. The machine.** `thermo_from_z` is handed a function returning $\ln Z(T)$, and nothing else.
It differentiates in $\beta$ with central differences,

$$
U \approx -\frac{\ln Z(\beta + h) - \ln Z(\beta - h)}{2h} ,
\qquad
\sigma_E^2 \approx \frac{\ln Z(\beta + h) - 2\ln Z(\beta) + \ln Z(\beta - h)}{h^2} ,
$$

then sets $C = \sigma_E^2/(\kB T^2)$, $F = -\kB T \ln Z$ and $S = (U - F)/T$. The step $h$ is a
fixed fraction of $\beta$ itself.

:::{admonition} Reconstruction from ln Z alone
:class: numerical-observation
Across a thousand temperatures from a tenth of the level gap to ten times it, the reconstructed
$U$ agrees with the closed form to $6 \times 10^{-10}$ for the two-level system, $7 \times 10^{-9}$
for a paramagnet of $10^4$ moments and $8 \times 10^{-11}$ for the oscillator, and $S$ to
$2 \times 10^{-7}$. The heat capacity agrees to $2.2 \times 10^{-6}$ between a fifth of the gap and
five times it, and loses precision beyond — to $6 \times 10^{-5}$ at the edges — for a reason
item 2 explains.
:::

**2. The step, and why it cannot be too small.** Both difference formulas are second order: their
truncation error falls as $h^2$. Measured on the oscillator at $\kB T = \hbar\omega$, halving the
step from $\beta/10$ to $\beta/160$ divides the error of $U$ by $4.02$, $4.00$, $4.00$, $4.00$.

:::{admonition} The stencil is second order — until roundoff wins
:class: numerical-observation
Fitted on a log–log plot, the order is $2.002 \pm 0.001$ for $U$ and $2.002 \pm 0.001$ for $C$.
Shrinking the relative step further, the error of $U$ is $3 \times 10^{-7}$ at $h = 10^{-3}\beta$,
$3 \times 10^{-9}$ at $10^{-4}\beta$, $3 \times 10^{-11}$ at $10^{-5}\beta$ — and then *rises*:
$5 \times 10^{-10}$ at $10^{-7}\beta$, $10^{-7}$ at $10^{-9}\beta$. For $C$ the turn comes sooner:
$7 \times 10^{-9}$ at $10^{-4}\beta$, $3 \times 10^{-4}$ at $10^{-6}\beta$, and $400\%$ at
$10^{-8}\beta$.
:::

The rise is **roundoff error**. The formulas subtract values of $\ln Z$ that agree in more and
more of their sixteen significant digits as $h$ shrinks, and the difference is left with fewer and
fewer correct ones. The first difference divides that loss by $h$, the second by $h^2$, which is
why $C$ suffers first. The best step balances the two errors: about $\epsilon^{1/3}\beta$ for $U$
and $\epsilon^{1/4}\beta$ for $C$, with $\epsilon = 2.2 \times 10^{-16}$ the float's relative
precision, and those are the defaults. The same cancellation is what degrades $C$ in item 1's
tails. Where $C$ is exponentially small, $\ln Z$ barely curves, and its curvature is buried
under the digits it shares at three neighbouring points. There a sum over the levels, which never
subtracts, is the better tool.

**3. $F = -\kB T\ln Z$, tested against module 10's $F$.** The laboratory computes the oscillator's
free energy twice. Once from $\ln Z$. Once as $U - TS$, with $U = \sum_n E_n P_n$ and the Gibbs
entropy $S = -\kB \sum_n P_n \ln P_n$ both summed from the probabilities, so that no $\ln Z$
appears in the second computation at all. At $20$, $72.4$ and $300\ \mathrm{K}$ the two agree to
$2 \times 10^{-16}$, $2 \times 10^{-15}$ and exactly — rounding in the last digit. The entropy that
$\ln Z$ implies is the entropy the probabilities carry, which is step 4's second check made
numerical.

**4. The paramagnet's magnetization.** For $10^4$ electron moments in $1\ \mathrm{T}$:

| $T$ (K) | $300$ | $150$ | $10$ | $1$ | $0.3$ | $0.1$ |
|---|---|---|---|---|---|---|
| $M/(N\mu)$ | $0.00224$ | $0.00448$ | $0.0671$ | $0.586$ | $0.978$ | $1.000$ |
| Curie law | $0.00224$ | $0.00448$ | $0.0672$ | $0.672$ | $2.24$ | $6.72$ |

Halving the temperature from $300$ to $150\ \mathrm{K}$ multiplies $M$ by $1.99999$. Below about
$1\ \mathrm{K}$ the Curie law predicts more than every moment can give, and the true curve
saturates.

**5. Fluctuations shrink as $N^{-1/2}$.** From the reconstructed second derivative of
$\ln Z_N$ at $1\ \mathrm{K}$, the relative energy fluctuation $\sigma_E/|U|$ of the paramagnet is
$0.437$ for $10$ moments, $0.0437$ for $1000$ and $0.00138$ for $10^6$. The fitted exponent is
$-0.5000000$, and going from $10^4$ to $10^6$ moments divides the fluctuation by $10.0000$.

**6. The dome, and the heat that leaves it.** For $N = 100$ moments the entropy rises from
$0$ to $66.78\,\kB$ at $U = 0$ (against the $N\ln 2 = 69.31\,\kB$ of Stirling's leading term),
and the slope read off by central difference gives

| moments reversed | $10$ | $30$ | $49$ | $50$ | $51$ | $70$ | $85$ |
|---|---|---|---|---|---|---|---|
| $T$ (K) | $0.62$ | $1.60$ | $33.9$ | $\pm\infty$ | $-33.9$ | $-1.60$ | $-0.79$ |

— symmetric about the peak, with the sign flipping as the tangent passes over the top.

:::{admonition} An inverted paramagnet heats every solid it touches
:class: numerical-observation
Start the paramagnet with $85$ of its $100$ moments reversed, $T = -0.79\ \mathrm{K}$, and put it
in contact with an Einstein solid of $200$ oscillators whose quantum is one reversal, $2\mu B$.
Counting every way the pair can share its energy, the most probable split leaves the paramagnet
with $22$, $36$, $48$ and $50$ moments reversed when the solid starts at $0.56$, $1.94$, $14.1$
and $1344\ \mathrm{K}$: in every case $63$, $49$, $37$ or $35$ quanta pass *from the paramagnet
to the solid*. Moving one quantum that way raises $\ln\Omega_{\mathrm{tot}}$ by between $1.7$ and
$4.0$; moving it the other way lowers it.
:::

Even the $1344\ \mathrm{K}$ solid, whose own temperature is more than a thousand times the
magnitude of the paramagnet's, takes energy from it. The count settles the paramagnet at
$50$ reversed moments — as close to $T = \pm\infty$ as a finite system gets — never at a positive
temperature below the solid's, which would mean giving up still more.

**7. Equipartition, and freeze-out.** The oscillator's mean energy per $\kB T$, measured above the
ground state, is $0.9950$ at $\kB T = 100\,\hbar\omega$, $0.951$ at $10\,\hbar\omega$, $0.582$ at
$\hbar\omega$ and $0.0005$ at $0.1\,\hbar\omega$. Its heat capacity is $0.9992\,\kB$, $0.921\,\kB$,
$0.171\,\kB$ and $0.0045\,\kB$ at $10$, $1$, $0.2$ and $0.1\,\hbar\omega$.

**8. Module 01's solid, under the oscillator's partition function.** Module 01 simulated two
Einstein solids trading quanta and read each one's temperature by equipartition, $T = U/(n\kB)$
per oscillator. Its model specification warned that this reading fails when cold. The oscillator
partition function supplies the exact reading: inverting $U(T)$ above the ground state,

$$
T = \frac{\hbar\omega}{\kB \ln\big(1 + n\hbar\omega/U\big)} ,
$$

which is also module 09's temperature, from the slope of the Einstein solid's $S(U)$ — the two
agree to $10^{-14}$. For $\kB T \gg \hbar\omega$ it is equipartition's reading plus half a
quantum.

:::{figure} ../media/partition-einstein-overlay.png
:alt: Energy per oscillator against temperature, both on logarithmic axes. A black curve bends down away from a straight dashed line at low temperature; blue points with small error bars lie on the black curve; open grey circles lie on the dashed line.
:width: 100%

Mean quanta per oscillator against $\kB T/\hbar\omega$. Black: the oscillator partition function's
$U(T)$ above the ground state. Dashed: equipartition, $U = \kB T$, module 01's reading. Blue: the
endpoints of module 01's simulation at seven energies — two solids of $40$ oscillators, $8$ seeds
each — placed at the temperature the partition function assigns them. Grey circles: the same
endpoints at the temperature module 01's equipartition reading assigns. The shaded band,
$\kB T > 2\hbar\omega$, is where the two readings differ by less than about a quarter.
:::

:::{admonition} Module 01's temperatures, re-read
:class: numerical-observation
Two solids of $40$ oscillators, started at different temperatures and run to equilibrium in
module 01's simulation, settle at the energy per oscillator the pair shares; averaged over eight
seeds, the partition function's temperature of that energy is recovered within its standard error
at all seven energies tried. At $8$ quanta per oscillator module 01's reading is $579\ \mathrm{K}$
against the partition function's $615\ \mathrm{K}$ — the half-quantum offset, $36\ \mathrm{K}$. At
$0.1$ quanta per oscillator it reads $7.2\ \mathrm{K}$ against $30.2\ \mathrm{K}$: four times too
cold, exactly where module 01's model specification said equipartition would fail.
:::

The simulation supplies the energies; the partition function supplies the thermometer. The
simulation cannot choose between the two thermometers: both say that two solids of one quantum
size settle at equal energy per oscillator, and that is all it shows. What decides between them
is module 09's slope of $S(U)$, which the partition function reproduces and equipartition only
approaches. The overlay illustrates, and the derivation of step 7 establishes: nothing in these numbers proves the
oscillator formula, which rests on the levels being $\hbar\omega(n + 1/2)$.

:::{admonition} What the reconstruction does not prove
:class: open-question
Every check above confirms that the computer differentiates $\ln Z$ correctly and that the model
systems behave as derived. None of it confirms that a real salt's moments are independent, or
that a real crystal's vibrations are harmonic. Those are questions for experiment — and for
real paramagnets the independence assumption does fail at low temperature, where the moments'
interactions order them (module 15).
:::

(12-partition-functions-transfer)=
## Transfer the idea

The recipe — list the levels, sum the Boltzmann factors, differentiate the logarithm — works for
any system whose levels you know.

- **Frozen molecular vibrations.** A nitrogen molecule vibrates with a quantum of
  $\hbar\omega/\kB = 3353\ \mathrm{K}$. At $300\ \mathrm{K}$ its vibrational heat capacity is
  $0.0017\,\kB$ — frozen out — which is why module 06 could treat air as a diatomic gas with
  $C_V = \tfrac52 N\kB$, counting rotations and not vibrations. At $1000\ \mathrm{K}$ the vibration
  contributes $0.42\,\kB$ and at $3000\ \mathrm{K}$ $0.90\,\kB$: the heat capacity of hot air
  climbs as the mode thaws.
- **The Schottky anomaly.** Any solid containing a set of two-level systems — impurity moments,
  tunnelling defects — shows a bump in its heat capacity near $\kB T \approx 0.42\,\Delta$, peaking
  at $0.44\,\kB$ per two-level system. Measuring the bump's position reads off the hidden gap.
- **Defect concentrations.** A lattice site that is either filled (energy $0$) or vacant (energy
  $E_{\mathrm{v}}$) is a two-level system, and the vacant fraction is
  $e^{-E_{\mathrm{v}}/\kB T}/(1 + e^{-E_{\mathrm{v}}/\kB T})$ — module 11's Arrhenius factor,
  corrected for the denominator. For $1\ \mathrm{eV}$ at $1000\ \mathrm{K}$ the correction is one
  part in $10^5$.
- **Chemical equilibrium.** A molecule that can exist as isomer A or isomer B, the latter
  $\Delta$ higher, is one system with two groups of levels, and the ratio of the two populations is
  the ratio of the two groups' partition functions — with non-degenerate ground levels,
  $[B]/[A] = e^{-\Delta/\kB T}$. Module 13 generalizes this to reactions that change the number of
  molecules.
- **Magnetic refrigeration.** Magnetize a paramagnet at low temperature, let the heat of
  magnetization flow away, isolate it and switch the field off: its entropy cannot change, but the
  entropy of a paramagnet depends only on $\mu B/(\kB T)$, so $T$ falls in proportion to $B$.
  This is how laboratories reach millikelvin temperatures, and every step of it is a statement
  about $\ln Z$.

Looking ahead:

- **Module 13** lets the bath exchange particles as well as energy, and the Boltzmann factor gains
  a term for the particles each state holds, $e^{-\beta(E_s - \mu N_s)}$.
- **Module 15** meets moments that interact: $Z$ no longer factorizes, and the paramagnet becomes a
  magnet.
- **Module 16** sums oscillator partition functions over every mode of a solid (Einstein and
  Debye) and of the electromagnetic field (Planck).
- **Module 17** trades single-system levels for single-particle levels.
- **Module 18** takes $\sigma_E^2 = \kB T^2 C_V$ from here and uses it.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — everything from one sum.** A two-level system has gap $\Delta = 2\,\kB T$.
Find $\ln Z$, $U$, $F$, $S$ and $C$.

:::{dropdown} Solution
$Z = 1 + e^{-2} = 1.1353$, so $\ln Z = 0.1269$. Then

$$
U = \frac{\Delta}{e^{2} + 1} = 0.1192\,\Delta ,
\qquad
F = -\kB T\ln Z = -0.1269\,\kB T ,
$$

$$
\frac{S}{\kB} = \ln Z + \frac{U}{\kB T} = 0.1269 + 2 \times 0.1192 = 0.365 ,
\qquad
\frac{C}{\kB} = \frac{x^2 e^x}{(e^x + 1)^2}\bigg|_{x=2} = 0.420 .
$$

Check: $U - TS = (0.2384 - 0.3653)\,\kB T = -0.1269\,\kB T = F$.
:::

**Worked example 2 — aligning electron moments.** Electron moments in a $1\ \mathrm{T}$ field. What
fraction of the saturation magnetization is reached at $300\ \mathrm{K}$? How cold must the salt
be for $90\%$?

:::{dropdown} Solution
At $300\ \mathrm{K}$, $x = \mu B/(\kB T) = 9.274 \times 10^{-24}/(1.381 \times 10^{-23} \times 300) = 0.00224$,
and $\tanh x = 0.00224$: about two moments in a thousand, net. For $90\%$, $\tanh x = 0.9$ gives
$x = 1.472$, so

$$
T = \frac{\mu B}{1.472\,\kB} = 0.46\ \mathrm{K} .
$$

A field of $1\ \mathrm{T}$ is a weak perturbation at room temperature; aligning electron moments
takes a fraction of a kelvin.
:::

**Worked example 3 — why air has five, not seven.** Nitrogen's vibration has
$\hbar\omega/\kB = 3353\ \mathrm{K}$. Estimate its contribution to $C_V$ per molecule at
$300\ \mathrm{K}$ and $1000\ \mathrm{K}$.

:::{dropdown} Solution
With $x = 3353/T$, $C/\kB = x^2 e^x/(e^x - 1)^2$. At $300\ \mathrm{K}$, $x = 11.18$ and
$C = 0.0017\,\kB$. At $1000\ \mathrm{K}$, $x = 3.35$ and $C = 0.42\,\kB$. Equipartition would give
the full $\kB$ — the two quadratic terms that would lift a diatomic gas from $\tfrac52$ to
$\tfrac72\,\kB$ per molecule. At room temperature they are frozen out.
:::

**Worked example 4 — which way does the heat go?** A crystal's nuclear moments are prepared with
$85\%$ of them reversed; its temperature is $-0.79\ \mathrm{K}$. It is touched to a copper block
at $300\ \mathrm{K}$. Which way does heat flow, and does the answer change if the copper is at
$3\ \mathrm{K}$?

:::{dropdown} Solution
The moments have $\beta_1 = 1/(\kB \times (-0.79\ \mathrm{K})) < 0$; the copper has $\beta_2 > 0$
at either temperature. Heat flows from smaller $\beta$ to larger, so it flows from the moments to
the copper in both cases. The negative-temperature system is hotter than the copper at any
positive temperature. The reversed moments relax back toward alignment and the copper warms.
:::

**Worked example 5 — a zero-point question.** An oscillator of quantum $\hbar\omega$ is at
$\kB T = \hbar\omega$. What is its mean energy with the zero point, and without it? Which of $U$,
$F$, $S$ and $C$ depend on the choice?

:::{dropdown} Solution
$U = \hbar\omega\,(1/2 + 1/(e - 1)) = \hbar\omega\,(0.5 + 0.582) = 1.082\,\hbar\omega$ with the zero
point, $0.582\,\hbar\omega$ without. Removing the zero point multiplies every Boltzmann factor by
$e^{\beta\hbar\omega/2}$, so $\ln Z$ gains $\beta\hbar\omega/2$: $U$ and $F$ both drop by
$\hbar\omega/2$, and $S = (U - F)/T$ and $C$ are unchanged. Only differences of energy are
physical here.
:::

**Worked example 6 — how steady is a macroscopic magnet?** The laboratory finds
$\sigma_E/|U| = 1.382/\sqrt{N}$ for the paramagnet at $1\ \mathrm{K}$ in $1\ \mathrm{T}$. What is it
for a sample of $10^{20}$ moments?

:::{dropdown} Solution
$1.382/\sqrt{10^{20}} = 1.4 \times 10^{-10}$. The energy of a macroscopic sample in canonical
equilibrium is sharp to about a part in ten billion, even though each moment's own energy swings
between $-\mu B$ and $+\mu B$.
:::

:::{note} Your predictions, revisited
1. **$\partial\ln Z/\partial\beta = -U$.** The mean energy, with a minus sign: raising $\beta$
   cools the system and lowers its energy. The second derivative gives the fluctuations and
   $C_V$. See [the derivation](#12-partition-functions-derive).
2. **It doubles.** In a weak field $M = N\mu^2 B/(\kB T)$, Curie's law. In a strong field the
   moments are already nearly all aligned, and it hardly changes.
3. **Negative — and the heat flows out of it.** Past the top of the entropy dome
   $\partial S/\partial U < 0$ and $T < 0$. A negative-temperature body gives heat to any body at
   positive temperature: it is hotter than infinite temperature, not colder than zero.
4. **$\kB T$ when hot** — equipartition, two quadratic terms at $\tfrac12\kB T$ each. When cold, only
   its zero-point energy $\hbar\omega/2$, and it can no longer absorb heat.
:::

(12-partition-functions-quiz)=
## Check your understanding

```{include} ../_generated/quiz-12-partition-functions.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](12-partition-functions-problems.md).

(12-partition-functions-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A classmate says: "$Z$ is just the normalization constant; the physics is in the Boltzmann
   factors." Convince them otherwise, using step 2.
2. Rewrite this sentence so that it is correct: "Negative temperature means colder than absolute
   zero." Say what $\partial S/\partial U$ has to do with it.
3. Is $F = -\kB T \ln Z$ a definition or a theorem? What had to be checked before it could be
   written down?
4. Why does a harmonic oscillator stop absorbing heat when it is cold, while a classical
   oscillator — module 06's — never does?

(12-partition-functions-advanced)=
## Advanced: the ideal gas, the Gibbs factor, and real negative temperatures

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It derives the Sackur–Tetrode entropy that
module 09 stated without proof, meets the $N!$ that module 08's Gibbs paradox anticipated, and
describes how negative temperatures are made in a laboratory.
:::

**One particle in a box.** A particle of mass $m$ in a box of volume $V$ has translational levels
too closely spaced to see individually at ordinary temperatures. Counting them — one state per
cell of volume $h^3$ in position–momentum space, a result stated here and derived in module 17 —
turns the sum into an integral with the value

$$
z = \frac{V}{\lambda^3} ,
\qquad
\lambda = \frac{h}{\sqrt{2\pi m \kB T}} ,
$$

where $\lambda$ is the **thermal wavelength**: $1.6 \times 10^{-11}\ \mathrm{m}$ for argon at
$300\ \mathrm{K}$. So $z$ is, roughly, the number of thermal-wavelength cubes that fit in the box.
Step 2 gives $U = \tfrac32 \kB T$ at once, since $\ln z = \ln V + \tfrac32\ln T + \text{const}$ —
equipartition for three quadratic terms.

**N particles, and the factor N!** If the particles were distinguishable, step 5 would give
$Z_N = z^N$. But identical particles are not labelled: exchanging two of them does not produce a
new microstate, and $z^N$ counts each configuration $N!$ times. The corrected partition function is

$$
Z_N = \frac{z^N}{N!} = \frac{1}{N!}\left(\frac{V}{\lambda^3}\right)^N .
$$

The correction is not cosmetic. Without it the entropy is not extensive: doubling $N$ and $V$
together should double $S$, but with $Z_N = z^N$ it overshoots by $2N\kB\ln 2$ — the entropy of
mixing two samples of the *same* gas, which is module 08's Gibbs paradox. With the $1/N!$ and
Stirling's $\ln N! \approx N\ln N - N$, step 4 gives

$$
S = N\kB\left[\ln\left(\frac{V}{N\lambda^3}\right) + \frac52\right] ,
$$

the **Sackur–Tetrode equation** that module 09 stated. For argon at $300\ \mathrm{K}$ and
$1\ \mathrm{bar}$, $V/(N\lambda^3) = 1.0 \times 10^7$ and $S = 18.6\,N\kB$. The test suite checks
that `thermo_from_z` applied to this $\ln Z_N$ reproduces module 09's formula, and that dropping
the $1/N!$ breaks extensivity by exactly $2N\kB\ln 2$.

The derivation also says when it fails. $V/(N\lambda^3) \gg 1$ means the particles are far apart
compared with their thermal wavelength, so that no two ever compete for one state and dividing by
$N!$ is enough. When $N\lambda^3$ approaches $V$ — dense, cold gases, electrons in a metal — it is
not, and module 17's quantum statistics take over.

**Negative temperatures in the laboratory.** A population with more moments against the field
than along it cannot be reached by heating, but it can be reached by reversing the field faster
than the moments can follow. Purcell and Pound did exactly this in 1951 with the nuclear moments
of lithium in a LiF crystal: after a sudden reversal of the field, the nuclear spins were at a
negative temperature and relaxed back through $\pm\infty$ over minutes, the timescale on which
they exchanged energy with the lattice. Every laser relies on a **population inversion** in
the same sense: its working levels are held at a negative temperature, and the light it emits is
the energy that flows out of them.

Two caveats keep this honest. The spins can be assigned a temperature only because they reach
equilibrium *among themselves* much faster than they reach it with the lattice; the spin system
is then isolated enough to have its own $S(U)$. And negative temperatures exist only for
degrees of freedom with an energy ceiling. The same crystal's vibrations have none, so the
crystal as a whole is never at a negative temperature.

:::{admonition} What is still open here
:class: open-question
Whether negative temperatures are genuine thermodynamic temperatures has been argued in the
research literature as recently as the 2010s. The disagreement is over which entropy to use for
a small isolated system: $\kB\ln\Omega(U)$ counting states *at* energy $U$, as this module did, or
counting all states *up to* $U$ — which never decreases, and therefore never gives a negative
temperature. For large systems the two agree everywhere except in the inverted region, and the
heat-flow argument of step 6 favours the first. Experiments with ultracold atoms, which can be
prepared at negative temperature in their motional degrees of freedom, have kept the debate
empirical.
:::
