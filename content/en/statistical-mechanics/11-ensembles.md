---
title: Statistical ensembles
short_title: 11 · Ensembles
module: 11-ensembles
objectives:
  - id: OBJ-11-1
    text: State what the microcanonical and canonical ensembles each describe (an isolated system at fixed total energy; a subsystem exchanging energy with a bath) and which probability rule applies to each — equal weights, or P_s = exp(-E_s/(k_B T))/Z.
  - id: OBJ-11-2
    text: Derive P(s) proportional to Omega_bath(U_tot - E_s) from the fundamental assumption by counting alone, and explain why this form is exact for a bath of any size.
  - id: OBJ-11-3
    text: Derive the Boltzmann distribution P_s = exp(-beta E_s)/Z by expanding ln Omega_bath to first order, stating both hypotheses (E_s << U_bath; bath curvature negligible) and identifying what breaks when they fail.
  - id: OBJ-11-4
    text: Explain how "all accessible microstates are equally probable" and "high-energy states are exponentially rare" are both true at once — equal weights govern the isolated whole, the exponential governs the subsystem's marginal.
  - id: OBJ-11-5
    text: Identify beta = 1/(k_B T) as the bath's d(ln Omega)/dU slope from module 09 and compute it by finite difference for an Einstein-solid bath, in units of 1/J.
  - id: OBJ-11-6
    text: Quantify the finite-bath error — show that the leading correction to ln P_s scales as 1/N_bath and verify it against exact enumeration, so that "infinite bath" is an approximation with a measurable error bar.
  - id: OBJ-11-7
    text: Work the two-level system fully — occupations, mean energy <E> = Delta/(exp(Delta/(k_B T)) + 1), and the T -> 0 and T -> infinity limits.
  - id: OBJ-11-8
    text: Transfer the Boltzmann factor to new contexts — the barometric formula exp(-m g h/(k_B T)), Arrhenius factors and defect concentrations, molecular excitation ratios.
---

# Statistical ensembles

(11-ensembles-puzzle)=
## The puzzle: two pillars that seem to disagree

Module 08 boxed one statement as the foundation of statistical mechanics: *every accessible
microstate of an isolated system is equally probable.* No microstate is favoured, whatever its
energy.

Every physicist also quotes a second statement, just as often: *high-energy states are
exponentially rare.* Only about one nitrogen molecule in seventy thousand is vibrationally
excited at room temperature; a sodium atom in a flame emits yellow light only because a small,
exponentially suppressed fraction of the atoms is excited; the air thins with altitude by a
factor $e$ every eight kilometres. That exponential is the **Boltzmann factor**, and it is
everywhere.

Put side by side, the two sound like a contradiction. Equal probability, or exponential
weighting — which is it?

:::{important} The question
How can "every microstate is equally probable" and "high-energy states are exponentially rare"
both be true of the same matter at the same time?
:::

They can, and the resolution is the whole of this module. The two statements are about
different things. The first is about an *isolated whole*. The second is about a *small part* of
that whole, one that trades energy with the rest. The step from one to the other involves no
new physics: no collisions, no dynamics, no new postulate. It is counting — the same counting as
module 08, applied to a system and the bath it sits in.

(11-ensembles-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. A two-level system — a ground state and one excited state — sits in equilibrium with a large
   heat bath. Module 08 said every microstate is equally probable. Are the system's two states
   equally likely?
2. Keep the bath at a fixed temperature but make it bigger and bigger. Does the system's
   occupation histogram change its *slope*, or does it only get *cleaner*?
3. System and bath together are isolated, so every *joint* microstate — the system's state and
   every bath oscillator's state — is equally probable. With that given, which is more
   probable: the system excited, or the system in its ground state? Why?
4. Heat the bath without limit, $T \to \infty$. Does the excited state's population approach
   $1$, $1/2$ or $0$?

:::{note} Why we ask first
Question 1 is where most students first meet the idea that "canonical" means something other
than "equal". Question 3 already contains the whole answer, if you look at it the right way.
Question 4 has a famously wrong intuition that module 12 will return to. Every answer is
collected at the end of the module.
:::

(11-ensembles-explore)=
## Explore the model

The laboratory is built around a single experiment with no dynamics in it at all. A small
system shares energy quanta with a bath made of Einstein oscillators — module 01's solid,
returning for the third time. Nothing moves. The computer lists every way the whole composite
can hold its fixed number of quanta, gives each one the same weight, and asks how often the
small system is found in each of its states.

The first animation grows the bath while keeping its temperature fixed.

:::{figure} ../media/ensembles-bath-growth.mp4
:alt: Left, bar chart of the probabilities of a small solid's energy levels, with black dots marking the Boltzmann values; the bars start far from the dots and settle onto them as the bath grows from 3 to 3000 oscillators. Right, the logarithm of the probability per microstate against energy, with a straight black line; the blue points start above the line and bent, and straighten onto it.
:width: 100%

A solid of three oscillators on a bath whose size (upper right of the left panel) grows from $3$ to $3000$
oscillators, always holding one quantum per oscillator, which fixes the bath's temperature at
$k_{\mathrm{B}} T = \varepsilon/\ln 2$. Left: the probability $P_k$ that the small solid holds $k$
quanta (blue bars), against the Boltzmann values for an infinitely large bath at that
temperature (black dots). Right: the logarithm of the probability of *one* microstate of the
small solid at level $k$, $\ln(P_k/g_k)$, where $g_k$ counts the solid's microstates at that
level. For the Boltzmann distribution this is the straight black line. The finite bath's blue
points begin bent downward and straighten onto the line as the bath grows. Levels above
$k = 14$ are not shown.
:::

The second animation draws the same composite twice: once as the whole, once as the part.

:::{figure} ../media/ensembles-joint-marginal.mp4
:alt: Left, a flat band of equal-height strips filling a horizontal axis from 0 to 1, coloured in blocks by the small system's energy level; at first 56 thin separate strips, later continuous colour blocks. Right, a bar chart in the same colours, approaching black dots.
:width: 100%

Left: every joint microstate of system plus bath, laid side by side and each drawn at the same
height, $1/\Omega_{\mathrm{tot}}$ — the equal-probability postulate, applied to the isolated
whole. They are sorted by how many quanta the small solid holds, and coloured by it. At the
start the bath has three oscillators and there are only $56$ joint microstates, separated by
white lines; by the end there are about $10^{601}$. The horizontal axis is the fraction of all
joint microstates, so the *width* of each colour is the probability of that level. Right: those
widths as bars, with the Boltzmann values dotted. The left panel is flat at every size. The
right panel is not flat at any size.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a small system with a few energy levels — a two-level system whose gap is a whole number of quanta, or an Einstein solid of a few oscillators, whose level $k$ holds $g_k = \binom{k + n - 1}{k}$ microstates — sharing $q_{\mathrm{tot}}$ quanta with an Einstein-solid bath of $N_{\mathrm{bath}}$ oscillators.
- **Dynamics:** none. Every accessible joint microstate is counted and given the same weight; there is no time evolution, no sampling and no random number anywhere.
- **Boundary:** the composite is isolated, with $q_{\mathrm{tot}}$ exactly fixed; the wall between system and bath is rigid and passes only quanta, so no work crosses it.
- **Ensemble:** exactly microcanonical for the composite; the system's marginal is the object that approaches the canonical form as $N_{\mathrm{bath}}$ grows.
- **Ignored:** the energy of the wall's coupling itself, unequal quantum sizes, any spatial structure, and how fast quanta are actually exchanged.
- **Valid when:** system and bath share one quantum size and the composite is genuinely isolated. The enumeration is then exact at every size; the canonical form additionally needs $E_s \ll U_{\mathrm{bath}}$ and a negligible curvature of the bath's $\ln\Omega$.
- **Failure modes:** a bath so small that $\ln\Omega$ has no smooth slope to read a temperature from (a single oscillator has $\Omega = 1$ at every energy); and $E_s$ comparable to the total energy, where the marginal visibly departs from the exponential — the module measures this departure rather than hiding it.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 11 — statistical ensembles](/lite/lab/index.html?path=en/labs/11-ensembles.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/11-ensembles.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- List by hand every joint microstate of a two-level system on a bath of three oscillators
  sharing three quanta, and check the computer's list against yours.
- Grow the bath at fixed temperature and read off how the gap to the Boltzmann curve shrinks
  each time the bath doubles.
- Keep the bath's *energy* fixed and change its *size* instead. Does the system notice?
- Heat a two-level system as far as you like, and see whether you can ever make the upper
  level the more populated one.

(11-ensembles-derive)=
## Derive the result

**System and boundary.** A small system in contact with a much larger one, the *bath*, through
a rigid wall that passes energy but no volume and no particles. The two together are isolated.

**Independent variables and constraint.** The total energy $U_{\mathrm{tot}}$ is fixed. The
system's state $s$ is free, and the bath takes whatever energy the system leaves it:
$U_{\mathrm{bath}} = U_{\mathrm{tot}} - E_s$.

**Sign convention.** The course convention holds,

$$
\mathrm{d}U = \dbar Q + \dbar \Won ,
$$

and here the wall is rigid, so $\dbar \Won = 0$ for the system: every change in its energy is
heat, drawn from or given to the bath.

**Route.** Six steps. First the postulate, applied to the composite. Then an exact counting
result, true for a bath of any size. Then the one approximation — an expansion of the bath's
$\ln\Omega$ — stated with its hypotheses. That gives the Boltzmann distribution. Then the price
of the approximation, computed rather than waved away, and last the two-level system worked in
full.

### Step 1: the whole is microcanonical

System and bath together are an isolated system at fixed energy. Module 08's postulate applies
to it directly.

:::{admonition} The fundamental assumption, applied to the composite
:class: model-assumption
Every accessible microstate of the isolated composite — a microstate of the system *together
with* a microstate of the bath, whose energies add up to $U_{\mathrm{tot}}$ — is equally
probable. This is module 08's postulate, unchanged. Nothing in this module derives it, and every
result below rests on it.
:::

:::{admonition} The microcanonical ensemble
:class: definition
The **microcanonical ensemble** describes an isolated system with its energy fixed: every
accessible microstate at that energy carries the same probability, $1/\Omega$.
:::

A **joint microstate** names the state of everything: which state the system is in, and how
many quanta each bath oscillator holds. That is the level at which probabilities are equal.

### Step 2: the exact counting result

Fix one particular microstate $s$ of the system, with energy $E_s$. How many joint microstates
have the system in exactly that state? The system's part is fixed, so the count is the number of
ways the *bath* can hold what is left over, $\Omega_{\mathrm{bath}}(U_{\mathrm{tot}} - E_s)$.
Every joint microstate has the same probability, so the probability of finding the system in
$s$ is the fraction of all joint microstates that have it there:

:::{admonition} The system's probability is the bath's multiplicity
:class: theorem
$$
P(s) = \frac{\Omega_{\mathrm{bath}}(U_{\mathrm{tot}} - E_s)}
{\sum_{s'} \Omega_{\mathrm{bath}}(U_{\mathrm{tot}} - E_{s'})} .
$$

This follows from the postulate by counting alone, and it is **exact** for a bath of any size —
no approximation has been made.
:::

Read it slowly, because it holds the whole answer to the puzzle. A system state with more energy
leaves *less* for the bath. The bath's multiplicity rises steeply with its energy — that is what
a positive temperature means — so the bath has *fewer* ways to hold the remainder. The
high-energy system state is not disfavoured by anything it does; it is simply paired with fewer
joint microstates.

:::{admonition} Joint and marginal distributions
:class: definition
The **joint distribution** assigns a probability to every joint microstate of system plus bath.
The system's **marginal distribution** assigns a probability to each state of the system alone,
by adding up the joint probabilities of every joint microstate that has the system in that state.
:::

A marginal of a flat distribution need not be flat. It is flat only if every system state is
paired with the same number of bath microstates, and here it is not.

**Worked by hand.** Take a two-level system whose gap is one quantum, and a bath of three
oscillators, with three quanta in all. For an Einstein bath of $N$ oscillators holding $q$
quanta, module 01's stars and bars give

$$
\Omega_{\mathrm{bath}}(N, q) = \binom{q + N - 1}{q} .
$$

If the system is in its ground state, the bath holds all three quanta, in
$\binom{5}{3} = 10$ ways. If it is excited, the bath holds two, in $\binom{4}{2} = 6$ ways.
There are $16$ joint microstates, each with probability $1/16$, so the probabilities of the
ground state and the excited state are

$$
p_0 = \frac{10}{16} = 0.625 ,
\qquad
p_1 = \frac{6}{16} = 0.375 .
$$

Every joint microstate is equally likely. The system's two states are not.

When the system has several microstates at the same energy — a **degenerate** level — they
each pair with the same number of bath microstates, so the probability of the *level* $k$ is
$g_k$ times the probability of any one of them, where $g_k$ counts them.

### Step 3: expanding the bath's logarithm

For a large bath, $\Omega_{\mathrm{bath}}$ is astronomically large and varies astronomically
fast. Expanding it directly in powers of $E_s$ fails: removing a single quantum from a
thousand-oscillator bath at one quantum per oscillator cuts its multiplicity roughly in half, a
change of fifty percent from the smallest possible step. Its logarithm, by contrast, falls by
almost the same amount for every quantum removed. The logarithm is the smooth quantity, so that
is what gets expanded:

$$
\ln \Omega_{\mathrm{bath}}(U_{\mathrm{tot}} - E_s)
= \ln \Omega_{\mathrm{bath}}(U_{\mathrm{tot}})
- E_s \, \frac{\partial \ln \Omega_{\mathrm{bath}}}{\partial U}
+ \frac{E_s^2}{2} \, \frac{\partial^2 \ln \Omega_{\mathrm{bath}}}{\partial U^2}
- \cdots
$$

The first slope is not new. Module 08 defined $S = \kB \ln\Omega$, and module 09 defined
temperature as the slope $1/T = (\partial S/\partial U)_{V,N}$. Put together, the slope of
$\ln\Omega_{\mathrm{bath}}$ is the bath's $1/(\kB T)$.

:::{admonition} Inverse temperature
:class: definition
$$
\beta \equiv \frac{\partial \ln \Omega_{\mathrm{bath}}}{\partial U} = \frac{1}{\kB T} ,
$$

in units of $\mathrm{J^{-1}}$. It is the **bath's** slope, evaluated at the bath's energy. The
system contributes nothing to it.
:::

For an Einstein bath this slope can be computed exactly. The logarithm of the binomial
coefficient is a difference of log-gamma functions, and since $N$ is a whole number its
derivative with respect to $q$ collapses into a finite sum:

$$
\beta\,\varepsilon = \sum_{j=1}^{N-1} \frac{1}{q + j} ,
$$

which approaches module 09's $\ln(1 + N/q)$ as the bath grows. One oscillator alone gives an
empty sum, $\beta = 0$: a single oscillator holds any number of quanta in exactly one way, its
$\ln\Omega$ is flat, and it has no temperature to give anything.

### Step 4: the Boltzmann distribution

Keep the first two terms of the expansion and exponentiate:

$$
\Omega_{\mathrm{bath}}(U_{\mathrm{tot}} - E_s)
\approx \Omega_{\mathrm{bath}}(U_{\mathrm{tot}}) \, e^{-\beta E_s} .
$$

The factor $\Omega_{\mathrm{bath}}(U_{\mathrm{tot}})$ is the same for every $s$, so it cancels
between the numerator and the denominator of step 2. What is left is the central result of the
module.

:::{admonition} The Boltzmann distribution
:class: theorem
A system in contact with a bath at temperature $T$ is found in microstate $s$ with probability

$$
P_s = \frac{e^{-\beta E_s}}{Z} ,
\qquad
\beta = \frac{1}{\kB T} ,
$$

**provided** (i) the bath is large enough that every $E_s$ of importance is small compared
with the bath's energy, so the expansion about $U_{\mathrm{tot}}$ makes sense; and (ii) the
curvature term is negligible,

$$
E_s^2 \, \left| \frac{\partial^2 \ln \Omega_{\mathrm{bath}}}{\partial U^2} \right| \ll 1 .
$$

When (ii) fails the distribution is still exact in the form of step 2, but no longer
exponential.
:::

The exponential $e^{-\beta E_s}$ is the **Boltzmann factor**. Two states differing in energy by
$\Delta E$ are occupied in the ratio $e^{-\Delta E/(\kB T)}$, whatever else is true of them.

:::{admonition} The partition function, as a normalization
:class: definition
$$
Z = \sum_s e^{-\beta E_s} = \sum_k g_k \, e^{-\beta E_k} ,
$$

the first sum over microstates, the second over levels with degeneracies $g_k$. For now $Z$ is
nothing but the constant that makes the probabilities add up to one. (The letter is for the
German *Zustandssumme*, "sum over states".) Module 12 shows that this one number contains all
of the system's thermodynamics.
:::

:::{admonition} The canonical ensemble
:class: definition
The **canonical ensemble** describes a system in contact with a bath at temperature $T$: its
microstates are *not* equally probable, but weighted by the Boltzmann factor,
$P_s = e^{-\beta E_s}/Z$. Its energy is not fixed; it is exchanged with the bath.
:::

**The puzzle, resolved.** Both pillars are true, of different things. Equal probability holds
for the isolated composite, microstate by microstate. The exponential holds for the small
system's marginal, and it arises *because* of the equal probability: each system state is
weighted by the number of bath microstates it leaves room for, and that number falls off
exponentially with the energy the system takes.

**Temperature belongs to the bath.** $\beta$ is a slope of the bath's multiplicity. The system
does not have a temperature of its own to bring; it inherits the bath's. Put two different
systems on one bath and both are weighted by the same $e^{-\beta E}$ — the reason a
thermometer, whatever it is made of, reads the temperature of what it touches.

**No dynamics was used.** Nothing in steps 1 to 4 mentions collisions, rates or time. The
Boltzmann factor is a consequence of counting. Collisions are one way a real system explores its
joint microstates, but they are not where the exponential comes from.

### Step 5: the price of an infinite bath

The Boltzmann distribution dropped the second-order term. That term can be computed, so the
approximation carries a measurable error bar rather than a promise.

The curvature of $\ln\Omega_{\mathrm{bath}}$ is the rate at which its slope changes:

$$
\frac{\partial^2 \ln \Omega_{\mathrm{bath}}}{\partial U^2}
= \frac{\partial \beta}{\partial U}
= -\frac{1}{\kB T^2} \frac{\partial T}{\partial U}
= -\frac{1}{\kB T^2 \, C_{\mathrm{bath}}} ,
$$

with $C_{\mathrm{bath}}$ the bath's heat capacity. So the correction to $\ln P_s$ is

$$
\delta \ln P_s = -\frac{E_s^2}{2 \kB T^2 \, C_{\mathrm{bath}}} ,
$$

and for a bath in its equipartition regime, $C_{\mathrm{bath}} = N_{\mathrm{bath}} \kB$,

$$
\delta \ln P_s = -\frac{E_s^2}{2 N_{\mathrm{bath}} (\kB T)^2} .
$$

:::{admonition} The infinite bath
:class: approximation
Treating the bath as infinite drops a correction to $\ln P_s$ of relative size
$E_s^2/(2 \kB T^2 C_{\mathrm{bath}})$, which falls as $1/N_{\mathrm{bath}}$. For a system
energy of a few $\kB T$ it is about $1/N_{\mathrm{bath}}$; it becomes important only when $E_s$
approaches $\kB T \sqrt{2 C_{\mathrm{bath}}/\kB}$. A bath of one mole could therefore tolerate a
system energy of about $10^{12}\,\kB T$ before the Boltzmann factor went wrong. "Large enough"
is not a matter of taste; it is this inequality.
:::

The sign is worth a sentence. The correction is always negative: a finite bath's temperature
*drops* as the system takes energy from it, so the next quantum is dearer than the last, and
high-energy system states are a little rarer than the exponential says — as
[the verification below](#11-ensembles-verify) measures.

### Step 6: the two-level system, worked in full

The simplest system with a Boltzmann factor to show has two states: a ground state at energy
$0$ and an excited state at $\Delta$. Its partition function has two terms,

$$
Z = 1 + e^{-\beta \Delta} ,
$$

and its occupations are

$$
p_0 = \frac{1}{1 + e^{-\beta \Delta}} ,
\qquad
p_1 = \frac{e^{-\beta \Delta}}{1 + e^{-\beta \Delta}} = \frac{1}{e^{\beta \Delta} + 1} .
$$

Its mean energy is the excited energy times the chance of being there,

$$
\langle E \rangle = \Delta \, p_1 = \frac{\Delta}{e^{\Delta/(\kB T)} + 1} .
$$

:::{figure} ../media/ensembles-two-level.png
:alt: Left, the ground-state occupation falling from 1 and the excited-state occupation rising from 0, both approaching one half as temperature increases on a logarithmic axis. Right, the mean energy rising from zero toward one half of the gap.
:width: 100%

The two-level system against $\kB T/\Delta$, on a logarithmic axis. (a) The ground-state
occupation $p_0$ (blue) and the excited-state occupation $p_1$ (red); the dashed line is
$1/2$. (b) The mean energy in units of the gap, approaching $1/2$ (dashed) from below.
:::

The limits are the point.

- **Cold, $\kB T \ll \Delta$.** $p_1 \approx e^{-\Delta/(\kB T)}$, which vanishes: every system
  is in its ground state, and $\langle E \rangle \to 0$. Almost nothing happens until
  $\kB T$ reaches about a fifth of the gap, which is why panel (a) is flat on its left.
- **Hot, $\kB T \gg \Delta$.** $e^{-\beta\Delta} \to 1$, so $p_0$ and $p_1$ both approach
  $1/2$, and $\langle E \rangle \to \Delta/2$. The bath is so hot that one quantum more or less
  hardly changes its multiplicity, and the two states become equally likely.
- **Never inverted.** For any positive temperature $p_1/p_0 = e^{-\Delta/(\kB T)} < 1$. Heating
  brings the populations toward equality, and no amount of heating passes it. What a population
  with *more* systems excited than not would mean is a question module 12 takes up.

(11-ensembles-verify)=
## Verify computationally

Every number below comes from `thermolab.ensembles`, which counts joint microstates exactly and
contains no random numbers. The energy quantum is $\varepsilon = 10^{-21}\ \mathrm{J}$ throughout;
one quantum per bath oscillator puts the bath at $\kB T = \varepsilon/\ln 2$, that is
$104.5\ \mathrm{K}$.

**1. The hand count.** For the two-level system of step 2 on a bath of three oscillators with
three quanta, listing the joint microstates one by one gives $16$ of them: $10$ with the system
in its ground state and $6$ with it excited, matching the binomial counts exactly.

**2. Flat joint, curved marginal.** With a bath of six oscillators and six quanta there are
$714$ joint microstates, each with probability exactly $1/714$. The system is in its ground
state in $462$ of them and excited in $252$: probabilities $0.647$ and $0.353$. On a bath of a
thousand oscillators the excited probability is $0.33344$, against the Boltzmann value $1/3$.
For this system the exact ratio is $p_1/p_0 = q/(q + N - 1)$, which sits just above
$e^{-\beta\varepsilon} = 1/2$ and approaches it as the bath grows.

**3. The finite bath converges, at a rate you can quote.**

:::{admonition} The error of an infinite bath falls as 1/N
:class: numerical-observation
At one quantum per bath oscillator, the largest gap between the exact marginal and the Boltzmann
distribution, $\max_k |P_k - P_k^{\mathrm{B}}|$, falls from $5.65 \times 10^{-3}$ at
$N_{\mathrm{bath}} = 20$ to $1.74 \times 10^{-4}$ at $640$ for the two-level system, and from
$1.89 \times 10^{-2}$ to $5.86 \times 10^{-4}$ for the three-oscillator solid. Every doubling of
the bath divides the gap by $2.00$ to $2.02$; fitted on a log–log plot, the exponents are
$-1.004$ and $-1.002$.
:::

**4. The dropped term, measured.** Step 5 predicted the correction to $\ln P_s$ beyond
$-\beta E_s$. The exact count measures it directly, level by level, as

$$
\ln \frac{\Omega_{\mathrm{bath}}(q - k)}{\Omega_{\mathrm{bath}}(q)} + \beta E_k .
$$

:::{admonition} The measured correction is the predicted one
:class: numerical-observation
For the three-oscillator solid on a bath of $100$ oscillators, the measured correction at
$k = 1$ is $-0.00248$ against a predicted $-0.00247$, and at $k = 4$ it is $-0.0403$ against
$-0.0395$. On a bath of $1000$ they agree to $0.2\%$ at $k = 4$. The small remaining gap is the
next term of the expansion, of relative size $E_k/U_{\mathrm{bath}}$; it is plainly visible for
a bath of $30$, where eight quanta are a quarter of the bath's energy.
:::

:::{figure} ../media/ensembles-convergence.png
:alt: Left, a log-log plot of the gap to the Boltzmann distribution against bath size for two systems, both falling on straight lines of slope minus one. Right, the correction to the log probability against energy, with curves for three bath sizes and dots lying on them, except at high energy for the smallest bath.
:width: 100%

(a) The largest gap between the finite-bath marginal and the Boltzmann distribution, against
bath size, for the two-level system with $\Delta = \varepsilon$ (blue) and the three-oscillator
solid (orange); the lines have slope $-1$. (b) What the exact count adds to $-\beta E_k$ (dots),
against the curvature term of step 5 (lines), for baths of $30$ (red), $100$ (orange) and $300$
(blue) oscillators.
:::

**5. Reading $\beta$ off a bath.** A student with only the counts can estimate the slope by
adding and removing one quantum,

$$
\beta \approx \frac{\ln\Omega(q + 1) - \ln\Omega(q - 1)}{2\varepsilon} .
$$

At one quantum per oscillator this differs from the exact slope by $1.7 \times 10^{-3}$ of itself at
$N_{\mathrm{bath}} = 10$, $1.1 \times 10^{-4}$ at $40$, $7.0 \times 10^{-6}$ at $160$ and
$4.4 \times 10^{-7}$ at $640$ — a sixteenfold drop for every fourfold growth, second order. The
exact slope itself differs from the infinite bath's $\ln 2/\varepsilon$ by $10.7\%$ at $10$
oscillators and $0.17\%$ at $640$: first order, the same $1/N$ as item 3.

**6. The bath's energy is not what sets the occupations.** Put the same two-level system on
three baths that each hold $100$ quanta, but with $25$, $100$ and $400$ oscillators. The excited
occupation is $0.446$, $0.334$ and $0.167$. The three baths have the same energy and very
different slopes: their temperatures are $338$, $106$ and $45\ \mathrm{K}$, and in each case
the occupation matches the Boltzmann factor at *that* temperature to better than half a percent.

**7. Two systems, one temperature.** Put a two-level system with a gap of two quanta and a
three-oscillator solid on the same bath of $5000$ oscillators, and read each one's own
exponent off its own marginal. The two-level system gives $\beta\varepsilon = 0.6934$, the solid
$0.6931$ to $0.6933$ from its first three level ratios, and the bath's own slope is $0.6930$.
Neither system has a temperature of its own.

:::{admonition} What the enumeration does not prove
:class: open-question
Every number above follows from the equal-probability postulate, applied to one kind of bath.
The enumeration shows that the postulate *implies* the Boltzmann factor; it does not show that
real matter obeys the postulate. That evidence is experimental — the Boltzmann factor is tested
every time a spectroscopist measures a population ratio — and the question of *why* isolated
systems explore their microstates evenly (ergodicity) is still not settled in general.
:::

(11-ensembles-transfer)=
## Transfer the idea

The Boltzmann factor applies to *any* system in contact with *any* large bath, and "energy of
the state" can be any energy at all. That generality is its power.

- **The barometric formula.** A molecule in the atmosphere at height $h$ has gravitational
  energy $m g h$. Treat the rest of the atmosphere as its bath, at temperature $T$: the chance of
  finding it at height $h$ carries the factor $e^{-m g h/(\kB T)}$, so the density, and with it
  the pressure, falls exponentially with height,

  $$
  P(h) = P(0)\, e^{-h/H} ,
  \qquad
  H = \frac{\kB T}{m g} .
  $$

  For nitrogen at $288\ \mathrm{K}$ the scale height is $H = 8.7\ \mathrm{km}$. The same result
  follows from hydrostatics plus the ideal-gas law; the counting argument and the macroscopic
  one agree, which is the point.
- **Arrhenius factors and defects.** A reaction whose molecules must borrow an energy
  $E_{\mathrm{a}}$ from their surroundings to get over a barrier proceeds at a rate carrying
  $e^{-E_{\mathrm{a}}/(\kB T)}$. A crystal site left empty costs a vacancy energy
  $E_{\mathrm{v}}$, so the fraction of empty sites is about $e^{-E_{\mathrm{v}}/(\kB T)}$ — about
  $10^{-5}$ for $E_{\mathrm{v}} = 1\ \mathrm{eV}$ at $1000\ \mathrm{K}$. Both are why chemistry
  and materials science are so sensitive to temperature.
- **Molecular and atomic excitation.** The fraction of sodium atoms in a flame that are excited
  and can emit the yellow line is a Boltzmann factor with the degeneracies of the two levels in
  front, and it is small — under two in ten thousand. Astronomers read stellar temperatures from
  exactly such ratios.
- **Back to module 04.** The Maxwell–Boltzmann distribution of molecular speeds that module 04
  assumed is the Boltzmann factor applied to kinetic energy, $e^{-m v^2/(2\kB T)}$. Module 12
  derives it properly.
- **Back to module 10.** "The reservoir" was an idealization there, "a body so large" that its
  temperature does not change. Step 5 says what large means, in numbers.

Looking ahead:

- **Module 12** takes $Z$ from normalization constant to master key: $U$, $S$, $F$ and $C_V$ all
  follow from it, and $F = -\kB T \ln Z$ is the free energy of module 10.
- **Module 13** repeats the counting of step 2 for a bath that trades particles as well as
  energy, and finds $e^{-\beta(E_s - \mu N_s)}$.
- **Module 15's** Monte Carlo simulation accepts a move with probability set by a ratio of
  Boltzmann factors — this module is its justification.
- **Module 17** replaces the levels of a single system with the levels of single particles, and
  the counting changes in an instructive way.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — a bath of four.** A two-level system with a gap of one quantum shares four
quanta with a bath of three oscillators. Find the probability that it is excited, and compare
with the value on a bath of three oscillators holding three quanta.

:::{dropdown} Solution
Ground: the bath holds four quanta in $\binom{6}{4} = 15$ ways. Excited: three quanta in
$\binom{5}{3} = 10$ ways. So the excited probability is

$$
p_1 = \frac{10}{25} = 0.400 .
$$

With three quanta it was $6/16 = 0.375$. The extra quantum warmed the bath, and a warmer bath
excites the system more often. The exact ratio $p_1/p_0 = q/(q + N - 1)$ gives $4/6$ here and
$3/5$ before.
:::

**Worked example 2 — a population ratio at room temperature.** A molecule has an excited state
$0.10\ \mathrm{eV}$ above its ground state, both non-degenerate. What fraction of molecules is
excited at $300\ \mathrm{K}$?

:::{dropdown} Solution
At $300\ \mathrm{K}$, $\kB T = 0.02585\ \mathrm{eV}$, so $\Delta/(\kB T) = 3.87$ and

$$
\frac{p_1}{p_0} = e^{-3.87} = 0.0209 ,
\qquad
p_1 = \frac{1}{e^{3.87} + 1} = 0.0205 .
$$

About two molecules in a hundred. A gap of $0.10\ \mathrm{eV}$ is only four times $\kB T$, and
that is already enough to empty the upper level almost completely.
:::

**Worked example 3 — the scale height.** Estimate the scale height of an isothermal nitrogen
atmosphere at $288\ \mathrm{K}$, and the pressure at the summit of a $4.8\ \mathrm{km}$ mountain
if it is $101\ \mathrm{kPa}$ at sea level.

:::{dropdown} Solution
A nitrogen molecule has mass $28.0 \times 1.661 \times 10^{-27} = 4.65 \times 10^{-26}\ \mathrm{kg}$, so

$$
H = \frac{\kB T}{m g}
= \frac{1.381 \times 10^{-23} \times 288}{4.65 \times 10^{-26} \times 9.81}
= 8.7\ \mathrm{km} .
$$

At $4.8\ \mathrm{km}$, $P = 101 \times e^{-4.8/8.7} = 58\ \mathrm{kPa}$. The real atmosphere is
colder aloft, which makes it thin a little faster; the international standard atmosphere, which
builds that cooling in, gives $55\ \mathrm{kPa}$. The isothermal assumption is the error, not
the Boltzmann factor.
:::

**Worked example 4 — vacancies.** Creating a vacancy in copper costs about $1.28\ \mathrm{eV}$.
Estimate the fraction of empty lattice sites just below the melting point, $1356\ \mathrm{K}$,
and at room temperature.

:::{dropdown} Solution
At $1356\ \mathrm{K}$, $\kB T = 0.1169\ \mathrm{eV}$, so the fraction is
$e^{-1.28/0.1169} = e^{-10.95} = 1.7 \times 10^{-5}$, about one site in sixty thousand. At
$300\ \mathrm{K}$ it is $e^{-49.5} \approx 3 \times 10^{-22}$ — which is why vacancies
frozen in by quenching from a high temperature are far more numerous than room-temperature
equilibrium allows.
:::

**Worked example 5 — how big a bath?** You want the Boltzmann distribution to be accurate to
$1\%$ in $\ln P$ for system energies up to $3\,\kB T$. How many oscillators must an Einstein bath
in its equipartition regime have?

:::{dropdown} Solution
The dropped term is $E_s^2/(2 N_{\mathrm{bath}} (\kB T)^2)$. At $E_s = 3\,\kB T$ it is
$9/(2 N_{\mathrm{bath}})$, and requiring it to be below $0.01$ gives

$$
N_{\mathrm{bath}} > 450 .
$$

A few hundred oscillators already make an excellent bath for a system that only ever holds a few
$\kB T$. The bath does not need to be macroscopic; it needs to be large *compared with the
system's energies*.
:::

**Worked example 6 — sodium in a flame.** The sodium D line comes from atoms in the $3p$ level,
$2.104\ \mathrm{eV}$ above the ground $3s$ level. The $3p$ level holds six states and the $3s$
level two. What fraction of sodium atoms is in the $3p$ level in a flame at $2500\ \mathrm{K}$?

:::{dropdown} Solution
At $2500\ \mathrm{K}$, $\kB T = 0.2154\ \mathrm{eV}$, so

$$
\frac{N_{3p}}{N_{3s}} = \frac{g_{3p}}{g_{3s}} \, e^{-2.104/0.2154}
= 3 \times e^{-9.77} = 1.7 \times 10^{-4} .
$$

Fewer than two atoms in ten thousand are excited, and yet the flame glows bright yellow: there
are a great many atoms. Leaving out the degeneracy factor would understate the population
threefold.
:::

:::{note} Your predictions, revisited
1. **No.** The excited state is less likely, by the factor $e^{-\Delta/(\kB T)}$. Equal
   probability holds for the joint microstates of system plus bath, not for the system's own
   states. See [the derivation](#11-ensembles-derive).
2. **Only cleaner.** At fixed temperature the slope of $\ln P$ is $-\beta$, which the bath's
   energy per oscillator sets. Growing the bath removes the curvature, and doubling it halves
   the remaining gap.
3. **The ground state.** When the system keeps no energy, the bath keeps all of it, and a bath
   with more energy has more microstates. Each joint microstate is equally likely, so the ground
   state wins by the ratio of bath multiplicities — which is the Boltzmann factor.
4. **$1/2$.** At infinite temperature the two states become equally likely; no positive
   temperature puts more systems in the upper state than the lower.
:::

(11-ensembles-quiz)=
## Check your understanding

```{include} ../_generated/quiz-11-ensembles.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](11-ensembles-problems.md).

(11-ensembles-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A student writes: "In the canonical ensemble every microstate is equally probable." Rewrite
   the sentence so that it is correct, and say precisely what was wrong with it.
2. Explain why temperature is a property of the bath that the system inherits, rather than a
   property the system brings. Use the three equal-energy baths of the verification.
3. The Boltzmann factor is often described as the result of molecules colliding and sharing
   energy. What does the counting argument deliver without any collisions, and what — if
   anything — are collisions still needed for?
4. Why does the derivation expand $\ln\Omega_{\mathrm{bath}}$ rather than
   $\Omega_{\mathrm{bath}}$ itself? What would go wrong the other way?

(11-ensembles-advanced)=
## Advanced: when the choice of ensemble stops mattering

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It shows why the canonical and
microcanonical descriptions give the same answers for large systems — the agreement module 04
leaned on — and names the result module 18 will prove.
:::

The canonical ensemble lets the system's energy fluctuate; the microcanonical ensemble fixes it
exactly. For a small system the difference is enormous: a two-level system on a bath is sometimes
excited and sometimes not. So why can module 04 be casual about which ensemble a real experiment
realizes?

Because the canonical energy distribution of a *large* system is extraordinarily narrow.
Consider an Einstein solid of $n$ oscillators on a bath. Each oscillator is independently
Boltzmann-distributed, so the means and the variances of the oscillators add. With
$b = \varepsilon/(\kB T)$, one oscillator has mean energy $\varepsilon/(e^{b} - 1)$ and variance
$\varepsilon^2 e^{b}/(e^{b} - 1)^2$, so for the whole solid

$$
\frac{\sigma_E}{\langle E \rangle} = \sqrt{\frac{e^{b}}{n}} = \sqrt{\frac{1 + x}{n\,x}} ,
$$

with $x$ the mean number of quanta per oscillator. At one quantum per oscillator this is
$\sqrt{2/n}$: $1.41$ for one oscillator, $0.14$ for a hundred, $0.045$ for a thousand, and
about $4.5 \times 10^{-12}$ for $10^{23}$. The library's `energy_moments` computes these spreads
directly from the Boltzmann distribution over the solid's levels, with no independence assumed,
and the test suite checks that it finds exactly this $n^{-1/2}$ law.

At that point, fixing the energy exactly (microcanonical) or letting it fluctuate by a part in
$10^{12}$ (canonical) changes nothing any instrument can detect, and every thermodynamic quantity
computed either way agrees. This is the **equivalence of ensembles** in the thermodynamic limit.
It is the same $N^{-1/2}$ that narrowed module 08's multiplicity peak and module 04's pressure
fluctuations, arriving by a third road.

The width is not a detail to be thrown away, though. Module 18 shows that for any system it is
fixed by the heat capacity, $\sigma_E^2 = \kB T^2 C_V$ — a fluctuation, measured at
equilibrium, that tells you how the system responds when pushed. The Einstein result above is
one instance of that relation.

:::{admonition} What is still open here
:class: open-question
This module ignored the energy of the wall between system and bath. For macroscopic bodies that
is harmless: the coupling lives at the surface and is tiny compared with either bulk. For a
single molecule bound to a surface, a nanoscale device, or a quantum system strongly coupled to
its environment, the interaction energy is not small, and it is not even clear how to split the
total energy into "system" and "bath". How to define heat, work and free energy for such
strongly coupled systems — and whether the Boltzmann factor survives in a modified form — is an
active research question.
:::
