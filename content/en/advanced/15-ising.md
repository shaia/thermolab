---
title: Phase transitions and the Ising model
short_title: 15 · Phase transitions
module: 15-ising
objectives:
  - id: OBJ-15-1
    text: Write the Ising energy E = -J sum_<ij> s_i s_j - h sum_i s_i, define the order parameter m = (1/N) sum_i s_i, and state the up-down symmetry of the h = 0 model and what "spontaneously broken" means for it.
  - id: OBJ-15-2
    text: Derive the Metropolis acceptance rule A = min(1, e^(-DeltaE/(k_B T))) from detailed balance with respect to the Boltzmann distribution, and explain why the chain samples equilibrium rather than simulating the magnet's real time evolution.
  - id: OBJ-15-3
    text: Explain, via the domain-wall free energy DeltaF = 2J - k_B T ln N, why the 1-D Ising chain has no phase transition at any T > 0.
  - id: OBJ-15-4
    text: Derive the mean-field self-consistency equation m = tanh((q J m + h)/(k_B T)), extract k_B T_c^MF = q J, and quantify how badly mean field misses Onsager's exact 2-D result k_B T_c = 2 J / ln(1 + sqrt(2)) ~ 2.269 J.
  - id: OBJ-15-5
    text: Estimate <|m|>, chi = N Var(m)/(k_B T), and C from Monte Carlo traces using the fluctuation identities, and locate T_c from the susceptibility peak.
  - id: OBJ-15-6
    text: Describe hysteresis, finite-size rounding, and critical slowing down operationally — m lags a swept field below T_c; the transition sharpens as L grows; the autocorrelation time peaks at T_c — and state what finite-L simulations can and cannot establish about the N -> infinity singularity.
  - id: OBJ-15-7
    text: Attach a defensible uncertainty to a Monte Carlo observable using the autocorrelation time (N_eff = N_samples/(2 tau)) and independent-seed studies, and reject conclusions that do not survive a seed change.
---

# Phase transitions and the Ising model

(15-ising-puzzle)=
## The puzzle: who chooses the direction?

Hold a magnet in a flame and it stops being a magnet. Iron loses its magnetization at
$770\,{}^\circ\mathrm{C}$, its **Curie temperature**, and the loss is not a slow fading: just
below that temperature the iron is magnetized, just above it is not, and the magnetization
goes to zero continuously but with a vertical tangent. Let it cool again and, at the same
temperature, the magnetization comes back.

It has to come back pointing *somewhere*. And here is the trouble. The energy of a piece of
iron in zero field does not care which way its moments point, as long as neighbours agree:
flip every moment in the sample and the energy is exactly what it was. The equations are
symmetric between "up" and "down". The sample, cooled through its Curie point, is not — it
picks one.

:::{important} The question
The energy is exactly symmetric under flipping every spin, so every Boltzmann average of the
magnetization is exactly zero, at every temperature. Yet the magnet on the bench is magnetized.
Who chooses the direction — and where did the symmetry go?
:::

Module 14 left a second question at the same place. Its coexistence curve *ended*: at the
critical point the latent heat vanished and the liquid and gas densities merged as
$(1 - T/T_c)^{1/2}$, while real fluids merge as $(1 - T/T_c)^{0.32}$, an exponent the van der
Waals model cannot produce. This module answers both with one model, so simple it fits in a
line, and with a computer experiment: the Ising model and the Monte Carlo method. Along the way
it asks what a simulation of $4096$ spins can and cannot tell us about a transition that,
strictly, only happens in an infinite system.

(15-ising-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. A large square lattice of spins is cooled far below its transition temperature in zero
   field. In equilibrium, is its magnetization zero, close to $\pm 1$, or does it depend on how
   it was cooled?
2. A computer samples the lattice's equilibrium at three temperatures: well below the
   transition, at it, and well above it. At which temperature does the simulation take the
   longest to forget where it started?
3. The magnetization is computed against temperature for lattices of side $16$ and $64$. Which
   curve drops more sharply at the transition?
4. Below the transition, a field is swept slowly from strongly up to strongly down and back.
   Does the magnetization retrace the same curve on the way back, or not?

:::{note} Why we ask first
The first two are the ones most people get wrong. The first because "the average over all
states is zero" sounds like a statement about the sample; the second because a transition
"between" two phases sounds like the place where nothing holds the system back. Every answer
is collected at the end of the module.
:::

(15-ising-explore)=
## Explore the model

The laboratory runs a live $L \times L$ Ising lattice. You set the temperature, the field and
the size, watch the spins, and read the magnetization and energy traces as they are produced.
Then it runs the experiments this module is built on: a one-dimensional chain against its exact
solution, a temperature sweep for three sizes with the susceptibility and heat capacity read
from fluctuations, a measurement of how long the simulation takes to decorrelate, a field
swept up and down below and above the transition, and the same lattice run under two different
update rules.

:::{figure} ../media/ising-quench.mp4
:alt: Left, a square lattice of dark and light pixels. It starts as fine random speckle; dark and light patches form within a few frames and grow, their boundaries smoothing, until a single light band crosses a dark background; the band narrows and closes, leaving the lattice dark with a few scattered light pixels. Right, two curves against a logarithmic time axis: the energy per spin falls from 0 to just above minus 2 within a hundred sweeps and stays there, while the absolute magnetization stays near zero for two thousand sweeps and then shoots up to a grey dashed line near 1.
:width: 100%

A $128 \times 128$ lattice quenched from infinite temperature to $\kB T = 1.5\,J$, well below
the transition. Left: the spins, up dark and down light. Within a few sweeps the random
speckle organises into **domains** of each sign; then the domains coarsen, the small ones
shrinking and the large ones growing, because every boundary costs energy. Right: the absolute
magnetization per spin $|m|$ (blue) and the energy per spin $E/(NJ)$ (red), against the number
of sweeps $t$ on a logarithmic axis — each sweep offers every spin one chance to flip. The
energy is nearly settled within a hundred sweeps, because the domain walls are by then a small
fraction of the bonds. The magnetization is not: with large domains of both signs it stays
near zero for two thousand sweeps, until the last band of light spins narrows and closes and
$|m|$ jumps to the grey dashed line, the exact equilibrium value for the infinite lattice. In
about one run in four at this size the lattice instead freezes into two straight bands, one of
each sign, which outlast this window by far. Nothing chose which sign wins except the random
history of the run.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** an $L \times L$ square lattice of $N = L^2$ classical spins $s_i = \pm 1$, with nearest-neighbour coupling $J > 0$ and a uniform field $h$; for one experiment, a ring of $N$ spins instead.
- **Dynamics:** a Markov chain, not equations of motion: in each half-sweep every site of one colour of a checkerboard proposes to flip, and accepts with the Metropolis probability $\min(1, e^{-\Delta E/(\kB T)})$ (or, where stated, the Glauber probability). The count of sweeps is not a physical time.
- **Boundary:** periodic — the lattice has no edges; the temperature and field are imposed from outside by an implicit bath.
- **Ensemble:** canonical at temperature $T$: the Boltzmann distribution is the chain's stationary distribution, by detailed balance.
- **Ignored:** quantum spin, lattice vibrations, long-range dipolar forces, anisotropy, disorder and the pinning of domain walls — everything that makes a real magnet a material rather than a model.
- **Valid when:** the chain has run well past its burn-in and for many autocorrelation times $\tau(T)$, which is quick away from $T_c$ at moderate $L$.
- **Failure modes:** near $T_c$, $\tau$ grows with $L$ (critical slowing down) and error bars that ignore it are illusory; below $T_c$ at small $|h|$ the chain stays in one magnetization branch for longer than any run; a trace that keeps its burn-in biases every average.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 15 — the Ising model](/lite/lab/index.html?path=en/labs/15-ising.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/15-ising.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Set $\kB T = 1.5\,J$ and run a $64 \times 64$ lattice from a random start, then from an
  all-up start. Then set $\kB T = 3.5\,J$ and do the same. Which runs end up in the same place?
- Set the temperature just below $2.27\,J/\kB$ and watch the magnetization trace. Then set it
  just above. Compare how long the trace takes to wander across its range.
- Run an $8 \times 8$ lattice at $\kB T = 2.0\,J$ for a long time and watch the sign of the
  magnetization. Then a $32 \times 32$ lattice at the same temperature.
- Sweep the field from $+1$ to $-1$ and back at $\kB T = 1.5\,J$, then at $3.0\,J$.

(15-ising-derive)=
## Derive the result

**System and boundary.** $N$ spins on a lattice, each $s_i = +1$ or $-1$, held at temperature
$T$ by a bath and subject to a uniform external field $h$, measured as an energy per unit spin.
The lattice is periodic. The spins are classical: $s_i$ is a number, not an operator.

**Independent variables.** The temperature $T$ and the field $h$; the configuration
$s = (s_1, \dots, s_N)$ is a microstate, and the energy $E_s$, the total spin $M_s = \sum_i s_i$
and the magnetization per spin $m_s = M_s/N$ are functions of it.

**Sign convention.** The course convention, $\mathrm{d}U = \dbar Q + \dbar \Won$, holds and is
not exercised: nothing in this module computes a heat or a work. The heat capacity enters
only through module 12's fluctuation identity, which needs no sign convention.

**Units.** This module measures energies in units of $J$, temperature as $\kB T/J$ and field
as $h/J$. Critical behaviour is the one subject in the course where the material constants
genuinely scale out — that is what universality, below, claims — and $\kB$ stays in every
formula through $\beta = 1/(\kB T)$. To quote a number for a material, put $J$ and $\kB$
back: a coupling of $J = 2 \times 10^{-21}\ \mathrm{J}$ puts the square lattice's transition at
$2.269\,J/\kB = 329\ \mathrm{K}$.

**Route.** Six steps. Write the model and its symmetry; derive the Monte Carlo rule from module
11's Boltzmann distribution; show that one dimension cannot order; build the mean-field theory
of module 12's paramagnet with an effective field; state Onsager's exact answer in two
dimensions and measure how wrong mean field is; and read the critical behaviour from module 12's
fluctuation identities.

### Step 1: the model, the order parameter, and the symmetry

:::{admonition} The Ising model
:class: model-assumption
$N$ spins $s_i = \pm 1$ on a lattice, each interacting only with its $q$ nearest neighbours
($q = 2$ on a ring, $q = 4$ on the square lattice), with energy

$$
E_s = -J \sum_{\langle ij \rangle} s_i s_j - h \sum_i s_i ,
$$

where $\sum_{\langle ij \rangle}$ counts each nearest-neighbour bond once and $J > 0$, so
that aligned neighbours are favoured. Periodic boundaries; no other interaction.
:::

A bond costs $-J$ when its two spins agree and $+J$ when they disagree. The ground state at
$h = 0$ is all spins aligned, with $E = -J \times (\text{number of bonds})$ — on the square
lattice, $2N$ bonds and $E = -2NJ$. There are *two* ground states, all up and all down, and
they have the same energy.

:::{admonition} Order parameter
:class: definition
The **magnetization per spin**

$$
m = \frac{1}{N} \sum_i s_i
$$

is the order parameter of the Ising model: it is $\pm 1$ in a ground state and close to zero
in a random configuration, and it changes sign under the symmetry below.
:::

At $h = 0$ the energy is invariant under flipping every spin, $s_i \to -s_i$ for all $i$,
because each bond energy depends on the product $s_i s_j$. So the Boltzmann weight of a
configuration and of its flipped twin are equal, $p_{-s} = p_s$, while their magnetizations are
opposite. Pairing every configuration with its twin,

$$
\langle m \rangle = \sum_s p_s\, m_s = 0 \qquad (h = 0,\ \text{any } N,\ \text{any } T) .
$$

This is exact, and it is the puzzle sharpened. For any finite lattice, the canonical average
of the magnetization in zero field vanishes at every temperature. If there is a magnetized
phase, it cannot be found by computing $\langle m \rangle$ at $h = 0$ for finite $N$.

What *is* computable is how the average responds to a small field, and in which order the
limits are taken:

:::{admonition} Spontaneous magnetization
:class: definition
The spontaneous magnetization is

$$
m_0(T) = \lim_{h \to 0^+} \lim_{N \to \infty} \langle m \rangle .
$$

The **symmetry is spontaneously broken** when $m_0 \neq 0$: the equations are symmetric, but
an infinitesimal field applied to an infinite system selects one of two states, and the state
selected keeps its magnetization when the field is removed.
:::

The order of limits is the whole content. Take $h \to 0$ first at finite $N$ and the answer is
zero, by symmetry. Take $N \to \infty$ first, and below the transition an arbitrarily weak field
— a stray field, a single defect, the history of the sample — is enough to tip the whole system
one way. That is who chooses the direction: the system's own history, amplified by its size.

The finite-$N$ version of the same story is told in time rather than in limits. Below the
transition, a finite lattice in zero field does occasionally reverse its magnetization: it must,
or the average would not be zero. But to reverse, it has to pass through configurations with a
wall of reversed spins running all the way across it, which costs an energy that grows with $L$,
so the waiting time between reversals grows exponentially with the system's size. For a
magnet of $10^{20}$ spins it exceeds the age of the universe. The ensemble average is zero; the
sample, for every practical purpose, is not. This is **ergodicity breaking**: the dynamics no
longer explores all the states the ensemble averages over.

### Step 2: Monte Carlo from detailed balance

To see any of this, we need the canonical averages of a lattice of thousands of spins. The
partition function of a $64 \times 64$ lattice is a sum of $2^{4096}$ terms, and no closed form
exists outside special cases. The way around it is to *sample*: generate configurations with
the right probability and average over them.

Module 11 established the target. In equilibrium with a bath at temperature $T$, a
configuration $s$ occurs with probability

$$
p_s = \frac{e^{-E_s/(\kB T)}}{Z} .
$$

Build a random walk through configuration space: from the current configuration $s$, propose
flipping one spin, giving $s'$, and accept the proposal with some probability $A(s \to s')$.
Proposals are symmetric — choosing which spin to flip does not depend on the state. We want the
walk, run for long enough, to visit each configuration with probability $p_s$. A sufficient
condition is that in equilibrium the flow from $s$ to $s'$ balances the flow back, for every
pair:

:::{admonition} Detailed balance gives the Metropolis rule
:class: theorem
If the transition probabilities satisfy

$$
p_s\,P(s \to s') = p_{s'}\,P(s' \to s)
$$

for every pair of configurations, then $p$ is a stationary distribution of the chain. With
symmetric proposals this requires

$$
\frac{A(s \to s')}{A(s' \to s)} = \frac{p_{s'}}{p_s} = e^{-\Delta E/(\kB T)} ,
\qquad \Delta E = E_{s'} - E_s ,
$$

and the Metropolis acceptance rule

$$
A(s \to s') = \min\!\left(1,\, e^{-\Delta E/(\kB T)}\right)
$$

satisfies it: accept every move that lowers the energy, and accept a move that raises it by
$\Delta E$ with probability $e^{-\Delta E/(\kB T)}$.
:::

Check the rule in both cases. If $\Delta E > 0$, then $A(s \to s') = e^{-\Delta E/(\kB T)}$
and the reverse move lowers the energy, so $A(s' \to s) = 1$: the ratio is right. If
$\Delta E \le 0$ the roles swap and the ratio is $1/e^{\Delta E/(\kB T)}$, right again.
Stationarity follows by summing detailed balance over $s$:
$\sum_s p_s P(s \to s') = p_{s'} \sum_s P(s' \to s) = p_{s'}$, since the walk must go
somewhere. The partition function never appears: only *ratios* of Boltzmann weights do, which
is why sampling succeeds where summation is hopeless.

For the Ising model the energy change of flipping spin $i$ needs only its neighbours. Writing
$\sum_{j \in \mathrm{nn}(i)} s_j$ for the sum over the $q$ neighbours of site $i$,

$$
\Delta E_i = 2\,s_i \Big( J \sum_{j \in \mathrm{nn}(i)} s_j + h \Big) .
$$

On the square lattice at $h = 0$ it takes only five values, $-8J$, $-4J$, $0$, $4J$ and $8J$.

:::{admonition} Monte Carlo time is not physical time
:class: model-assumption
Detailed balance fixes *where* the chain goes — its stationary distribution — and says nothing
about *how fast* it gets there. Any acceptance rule with the same ratio does the same job. The
Glauber rule

$$
A(s \to s') = \frac{1}{1 + e^{\Delta E/(\kB T)}}
$$

satisfies detailed balance too, accepts less often than Metropolis, and relaxes more slowly,
to the same equilibrium. The order in which sites are visited is another free choice. A "sweep"
— one flip attempt per spin — is a unit of computation, and no physical constant converts it
into seconds. The chain samples equilibrium; it does not simulate the real magnet's motion.
:::

One practical point decides whether the method is right or wrong. Updating every spin at once,
each against the configuration before the update, breaks detailed balance: two neighbours that
both flip each computed $\Delta E$ against a neighbour that no longer exists. The laboratory
colours the lattice like a chessboard instead. Every neighbour of a black site is white, so
with the white sites held fixed the black sites do not interact, and updating all of them at
once is the same as updating them one at a time. A sweep is a black half-sweep followed by a
white one. Each half-sweep satisfies detailed balance, so each leaves the Boltzmann distribution
unchanged, and so does the sweep.

### Step 3: why a chain cannot order

Start a ring of $N$ spins all up at $h = 0$. The cheapest way to destroy its order is a
**domain wall** — a single bond whose two spins disagree, separating a block of up spins from a
block of down. On a ring walls come in pairs; take two, cutting the ring into two arcs. Each
wall costs $2J$, so two cost $\Delta E = 4J$, independent of where they are. But the first can
sit at any of $N$ bonds and the second at any of the others, roughly $N^2/2$ placements, each
a distinct microstate. In module 08's terms, the multiplicity of the two-wall states is about
$N^2/2$ and their entropy is $\kB \ln(N^2/2)$. The free energy cost of breaking the order is

$$
\Delta F = \Delta E - T\,\Delta S \approx 4J - \kB T \ln\frac{N^2}{2} .
$$

The energy is fixed; the entropy grows without bound as $N$ grows. For any $T > 0$ there is an
$N$ beyond which $\Delta F < 0$, walls appear spontaneously, and the order is destroyed. The
same accounting for a single wall in an open chain gives the form usually quoted,
$\Delta F = 2J - \kB T \ln N$.

:::{admonition} No order in one dimension
:class: theorem
The one-dimensional Ising chain with short-range coupling has no spontaneous magnetization at
any $T > 0$: $m_0(T) = 0$. Its exact solution, by the transfer matrix in the advanced section,
gives at $h = 0$

$$
\frac{E}{NJ} = -\tanh\frac{J}{\kB T} ,
$$

and in a field

$$
m = \frac{\sinh(h/(\kB T))}{\sqrt{\sinh^2(h/(\kB T)) + e^{-4J/(\kB T)}}} ,
$$

which goes to zero as $h \to 0$ at every $T > 0$, and approaches $\pm 1$ only as $T \to 0$.
:::

These two formulas are the module's first exact anchors: the laboratory's chain must reproduce
them, within its error bars, before anything it says about two dimensions is believed.

The argument fails in two dimensions, and the way it fails is instructive. A wall that cuts a
square lattice in two has a length of at least $L$, so its energy cost grows like $2JL$. Its
entropy grows like $L$ too — a wall is a path, and a path of length $\ell$ can wander in at most
$3^{\ell}$ ways — so energy and entropy now compete on equal terms, and at low enough
temperature the energy wins. The argument does not prove that the square lattice orders; it
shows that nothing like the one-dimensional catastrophe forbids it. Problem 2 makes it
quantitative.

### Step 4: mean field, and what it gets wrong

Module 12 solved a single spin in a field exactly: its average is $\langle s \rangle =
\tanh(h/(\kB T))$. A spin in the Ising model feels the field $h$ plus its neighbours. The
**mean-field approximation** replaces each neighbour by its average, so that spin $i$ sees
an effective field

$$
h_{\mathrm{eff}} = J \sum_{j \in \mathrm{nn}(i)} \langle s_j \rangle + h = qJm + h ,
$$

and responds to it as module 12's paramagnet. Consistency demands that the average it produces
be the $m$ that was assumed.

:::{admonition} The mean-field equation
:class: approximation
Neglecting the correlations between a spin and its neighbours,

$$
m = \tanh\!\left(\frac{qJm + h}{\kB T}\right) .
$$

At $h = 0$ it always has the solution $m = 0$. It has two more, $\pm m_0$, exactly when the
slope of the right side at the origin exceeds $1$, that is below

$$
\kB T_c^{\mathrm{MF}} = qJ .
$$
:::

Just below $T_c^{\mathrm{MF}}$, $m$ is small, and $\tanh x \approx x - x^3/3$ turns the
equation into $m^2 \approx 3\,(T_c^{\mathrm{MF}} - T)\,T^2/(T_c^{\mathrm{MF}})^3$, so that

$$
m_0 \approx \sqrt{3\left(1 - \frac{T}{T_c^{\mathrm{MF}}}\right)} .
$$

The magnetization vanishes as the square root of the distance to $T_c$: exponent $1/2$, the
same exponent the van der Waals model gave module 14 for $v_g - v_\ell$. That is not a
coincidence. Both are mean-field theories — every particle, or every spin, feels the average of
the others — and every mean-field theory gives $1/2$.

Mean field is a good guess far from $T_c$ and a bad one near it, and it is worst in low
dimensions. It predicts a transition for the chain, at $\kB T = 2J$, where step 3 proved there
is none. For the square lattice it predicts $\kB T_c = 4J$. The exact answer is next.

### Step 5: Onsager's exact answer

In 1944 Lars Onsager solved the two-dimensional Ising model in zero field exactly. The
derivation is one of the great calculations of theoretical physics and lies outside this
course; its results are the module's reference values.

:::{admonition} The two-dimensional Ising model, solved
:class: theorem
The square-lattice Ising model at $h = 0$ has a phase transition at

$$
\kB T_c = \frac{2J}{\ln\!\left(1 + \sqrt{2}\right)} \approx 2.269\,J ,
$$

and below it a spontaneous magnetization (announced by Onsager in 1949, first derived in print
by C. N. Yang in 1952)

$$
m_0(T) = \left[1 - \sinh^{-4}\!\left(\frac{2J}{\kB T}\right)\right]^{1/8} .
$$

Stated without proof.
:::

So mean field overestimates the transition temperature by a factor $4/2.269 = 1.763$, or
$76\%$. Its error is not one of detail. Near $T_c$ a spin's neighbours are not an average
— they are correlated with it and with each other over long distances — and mean field throws
away exactly those correlations. And the exponent is not $1/2$: Onsager–Yang's $m_0$ vanishes
as $(T_c - T)^{1/8}$, far more steeply.

### Step 6: critical behaviour, read from fluctuations

At the transition the system is neither ordered nor disordered: it is a patchwork of domains
of every size, from single spins to the whole lattice. That is what makes responses diverge,
and module 12's fluctuation identities are how a simulation sees it.

:::{admonition} Fluctuation identities for the Ising model
:class: theorem
In the canonical ensemble, the heat capacity per spin and the magnetic susceptibility per spin
are variances of the energy and of the magnetization:

$$
c = \frac{N\,\mathrm{Var}(e)}{\kB T^2} , \qquad
\chi = \frac{\partial \langle m \rangle}{\partial h} = \frac{N\,\mathrm{Var}(m)}{\kB T} ,
$$

where $e = E/N$ and $m = M/N$. The first is module 12's $C = \mathrm{Var}(E)/(\kB T^2)$ per
spin. The second follows the same way: $h$ enters the Boltzmann weight as $e^{\beta h M}$, so
$\langle M \rangle = \partial \ln Z/\partial(\beta h)$ and its derivative is
$\mathrm{Var}(M)$.
:::

Below $T_c$, a finite run does not sample the two branches $\pm m$ fairly — it crosses between
them rarely, at a rate that depends on how long the run happened to be — so $\mathrm{Var}(m)$
of a run measures luck. The laboratory applies the same identity to $|m|$, which a run *can*
sample, and reports $\chi' = N\,\mathrm{Var}(|m|)/(\kB T)$. It is the standard estimator for
finite lattices. Its peak is all the module uses.

Near $T_c$ the singular parts of the observables follow power laws in $|T - T_c|$, with
**critical exponents** conventionally called $\beta$, $\gamma$, $\alpha$ and $\nu$ (the first
has nothing to do with $1/(\kB T)$; context always tells them apart):

$$
m_0 \propto (T_c - T)^{\beta} , \qquad
\chi \propto |T - T_c|^{-\gamma} , \qquad
c \propto |T - T_c|^{-\alpha} , \qquad
\xi \propto |T - T_c|^{-\nu} ,
$$

where $\xi$ is the **correlation length**, the size of the largest correlated patches. For the
square lattice, from Onsager's solution, $\beta = 1/8$, $\gamma = 7/4$, $\nu = 1$, and the heat
capacity diverges logarithmically ($\alpha = 0$). Mean field gives $\beta = 1/2$, $\gamma = 1$,
$\nu = 1/2$ and a finite jump in $c$.

Three facts about these divergences decide what a simulation can see:

- **Nothing diverges on a finite lattice.** $\xi$ cannot exceed $L$, so on an $L \times L$
  lattice every peak is rounded and finite, its height grows with $L$, and its position drifts
  toward $T_c$ as $L$ grows. The singularity at $T_c$ is a property of the limit
  $N \to \infty$.
- **The transition is continuous.** Crossing $T_c$ at $h = 0$, the energy per spin is
  continuous — there is no latent heat, unlike module 14's boiling — and the heat capacity
  peaks instead. Crossing $h = 0$ below $T_c$, by contrast, the magnetization jumps from $+m_0$
  to $-m_0$: a first-order transition, the magnetic version of boiling, along a line that ends
  at the critical point.
- **Critical slowing down.** A local update rule changes a configuration one spin at a time,
  and a correlated patch of size $\xi$ takes a time that grows like $\xi^{z}$ to rearrange,
  with $z \approx 2$ for Metropolis. At $T_c$ on a finite lattice $\xi \approx L$, so the
  autocorrelation time grows like $L^{z}$: the simulation is slowest exactly where the physics
  is most interesting.

:::{figure} ../media/ising-tc-sweep.mp4
:alt: Top, three square lattices of dark and light pixels side by side, framed in amber, red and blue, the first coarse-grained and the last fine-grained. They start as fine speckle, develop patches of both colours of every size, and end almost uniformly one colour. Bottom, mean absolute magnetization against temperature with temperature decreasing to the right: three coloured curves grow point by point from right to left, low and flat at high temperature with the amber one highest, rising steeply near a dashed vertical line, and merging with a black curve near 1 at low temperature.
:width: 100%

Three lattices, $L = 16$ (amber), $32$ (red) and $64$ (blue), drawn at the same size and cooled
together from $\kB T = 3.5\,J$ to $1.5\,J$ through $41$ temperatures. Top: the spins at each step.
Bottom: $\langle |m| \rangle$ for each lattice, added point by point as the temperature falls
(temperature decreases to the right), against Onsager–Yang's exact curve for the infinite lattice
(black); the dashed line is $T_c$. Above $T_c$ each lattice keeps a small residual $|m|$, largest
for the smallest lattice — a finite patch of random spins is never exactly balanced. Near $T_c$
the lattices fill with patches of both signs at every size up to the lattice itself. Below, all
three order and their curves merge with the exact one. The rise is steepest for the largest
lattice, and no finite lattice reproduces the black curve's vertical drop.
:::

The last one sets the standard for every number this module reports. A trace of $n$ samples
whose **autocorrelation time** is $\tau$ (in samples) contains about

$$
N_{\mathrm{eff}} = \frac{n}{2\tau}
$$

independent samples, and its standard error is $\sigma/\sqrt{N_{\mathrm{eff}}}$, not
$\sigma/\sqrt{n}$. This is module 03's correlated walk again: the $n^{-1/2}$ law survives, with
$n$ replaced by the number of samples that are actually independent. The laboratory measures
$\tau$ as the integrated autocorrelation function,
$\tau = \tfrac12 + \sum_{t \ge 1} \rho(t)$, summed out to a window several times $\tau$ itself.

:::{admonition} Universality
:class: numerical-observation
Systems with nothing microscopic in common share critical exponents. The liquid–gas critical
point of every simple fluid that has been measured — carbon dioxide, xenon, water — has
$\beta \approx 0.32$–$0.33$, and so does the demixing point of binary liquid mixtures; both
agree, within their errors, with the three-dimensional Ising model, $\beta = 0.326$. Module 14's van der Waals fluid gets $1/2$ because it is a mean-field
theory, not because fluids differ from magnets. What sets the exponents is the dimension of
space and the symmetry of the order parameter — here, a single number with two equivalent
signs — and not the forces. The theory that explains why, the renormalization group, is beyond
this course.
:::

The dictionary between the two problems is direct. Divide a fluid into cells, each occupied by
a molecule ($s_i = +1$) or empty ($s_i = -1$), with an attraction between occupied neighbours:
that is an Ising model, the **lattice gas**. The magnetization is the density measured from its
critical value, the field is the chemical potential, the line $h = 0$ below $T_c$ is the
coexistence curve, and the jump in $m$ across it is the jump from gas to liquid density.

(15-ising-verify)=
## Verify computationally

Every number below comes from `thermolab.ising`, run under several independent seeds, with every
error bar computed from the effective number of independent samples rather than the raw count.
The laboratory repeats each experiment at a smaller scale.

**1. The bookkeeping.** The simulation never recomputes the energy: each accepted flip adds its
$\Delta E$ to a running total. After $1000$ sweeps of a $16 \times 16$ lattice at $h = 0$ — tens
of thousands of accepted flips — the running energy and total spin equal a from-scratch recount
exactly, as integers. In a field the energy carries $h$ and agrees to rounding.

**2. The chain against its exact solution.** A $1024$-site ring, eight seeds, $2000$ sweeps each
after $300$ of burn-in, under the Glauber rule. At $\kB T = J$ and $h = 0$ the energy per spin is
$-0.76156 \pm 0.00036$ against the exact $-\tanh 1 = -0.76159$; at $2J$, $-0.46228 \pm 0.00021$
against $-0.46212$. In a field $h = 0.3\,J$ at $\kB T = J$ the magnetization is
$0.91409 \pm 0.00036$ against the exact $0.91382$. All within one standard error. Under the
Metropolis rule the same ring forgets a cold start far more slowly — after $100$ sweeps of
burn-in it still sits four standard errors low — because at $h = 0$ in one dimension every
wall move costs nothing and Metropolis accepts all of them, so the walls are pushed one way like
beads on a wire instead of diffusing. Both rules reach the same answer eventually: a statement
about speed, not about equilibrium.

**3. Below $T_c$, against Onsager–Yang.** A $64 \times 64$ lattice, six seeds: at $\kB T = 1.5$,
$2.0$ and $2.2\,J$, $\langle |m| \rangle = 0.9866$, $0.9109 \pm 0.0002$ and $0.7871 \pm 0.0022$,
against the exact infinite-lattice $0.9865$, $0.9113$ and $0.7848$. Below $T_c$ a $64 \times 64$
lattice is already, to three decimals, infinite; the finite-size effects live near $T_c$. Mean
field at $2.0\,J$ says $0.958$.

**4. Far above $T_c$, against the high-temperature series.** At $\kB T = 20\,J$ in a weak
field, a free spin would give $\chi T = 1$. The square lattice's high-temperature series gives
$1 + 4v + 12v^2 + 36v^3 + 100v^4 + \dots = 1.235$, with $v = \tanh(J/(\kB T))$. The simulation
agrees with the series and rejects the free spin by many standard errors: even at ten times
$T_c$ the neighbours still matter at the $20\%$ level.

**5. The transition, located.** The figure below is the module's central measurement.

:::{figure} ../media/ising-finite-size.png
:alt: Three panels against temperature from 1.6 to 3.5, with a dashed vertical line at 2.27 in each. Left, the mean absolute magnetization for four lattice sizes in green, amber, red and blue: all four coincide near 1 at low temperature and fall through the dashed line, the larger lattices falling more steeply and lower above it; a black curve, the exact infinite-lattice result, drops vertically to zero at the dashed line. Middle, the susceptibility: four peaks, small and broad for the smallest lattice, tall and narrow for the largest, all just to the right of the dashed line. Right, the autocorrelation time on a logarithmic axis: four peaks near the dashed line, higher for larger lattices, from about 3 for the smallest to about 200 for the largest, all falling to about 1 at both ends.
:width: 100%

The square lattice at $L = 8$ (green), $16$ (amber), $32$ (red) and $64$ (blue), each point
from one run of $20\,000$ sweeps after burn-in at $L = 8$, falling to $5000$ at $L = 64$; the
dashed line is Onsager's $T_c$. Left:
$\langle |m| \rangle$ with $\tau$-corrected error bars, and Onsager–Yang's exact curve for the
infinite lattice (black). Below $T_c$ every size agrees with it; above, every finite lattice
keeps a residual $|m|$ that falls with $L$, and the shoulder sharpens without ever becoming the
black curve's vertical drop. Middle: the susceptibility $\chi' = N\,\mathrm{Var}(|m|)/(\kB T)$,
whose peak grows with $L$ and moves toward $T_c$ from above. Right: the autocorrelation time of
$|m|$, in sweeps: about one deep in either phase and peaking at $T_c$, higher for every larger
lattice — critical slowing down. The jagged points near the top of the right and middle panels
are honest: at $L = 64$ a run of $5000$ sweeps holds only some $25$ to $50$ autocorrelation
times there, and its fluctuation estimates scatter accordingly.
:::

:::{admonition} The susceptibility peak closes in on Onsager's T_c
:class: numerical-observation
Four seeds at each size, $4000$ to $6000$ sweeps per temperature on a grid of spacing $0.04$, the
peak located by a parabola through its three highest points: $\chi'$ peaks at
$\kB T = 2.503 \pm 0.022$, $2.416 \pm 0.003$, $2.329 \pm 0.013$ and $2.311 \pm 0.007$ (in units of
$J$) for $L = 8$, $16$, $32$ and $64$, every one above $T_c$ and each closer than the last. The
peak heights, $1.80$, $6.10$, $21.3$ and $69.4$, grow as $L^{1.76}$; the exact exponent is
$\gamma/\nu = 7/4$. Extrapolating the positions linearly in $1/L$ — which assumes the exact
$\nu = 1$ — gives $T_c = 2.280 \pm 0.008$ from all four sizes and $2.272 \pm 0.009$ leaving out
$L = 8$, against Onsager's $2.269$. The heat-capacity peak drifts the same way, from $2.327$ at
$L = 8$ to $2.285$ at $L = 64$. The quoted errors are the seed-to-seed scatter of four runs and
are themselves rough; the extrapolation's assumption is not in them.
:::

**6. Critical slowing down, measured.** On a $32 \times 32$ lattice (four seeds of $20\,000$
sweeps each), the autocorrelation time of $|m|$ is $0.7$ sweeps at $\kB T = 1.5\,J$, $2.8$ at
$2.0$, $41$ at $2.27$, $11.5$ at $2.5$, $1.7$ at $3.0$ and $1.0$ at $3.5$. At $T_c$ itself it
grows with the lattice: $3.1$, $9.6$, $42$ and $174 \pm 38$ sweeps at $L = 8$, $16$, $32$ and
$64$ — a power $\tau \propto L^{z}$ with fitted $z = 1.96$, near the value $z \approx 2.17$ that
large-scale studies of local update rules find. The settling time is largest *at* the
transition, not anywhere near either side of it, and every doubling of $L$ quadruples it.

**7. Who chooses the direction, measured.** At $\kB T = 2.0\,J$, from an all-up start, run for
$10^5$ sweeps: an $8 \times 8$ lattice reverses its magnetization $42$ times, its time average
of $m$ is $0.11$, and its $\langle |m| \rangle$ is $0.911$. A $16 \times 16$ lattice and a
$32 \times 32$ lattice never reverse: their time averages are $0.912$ and $0.911$, the
spontaneous magnetization. At $2.2\,J$, closer to $T_c$, the three lattices reverse $383$, $52$
and $3$ times. The ensemble average of $m$ is zero for all of them; how much of the ensemble one
run actually visits collapses as the system grows.

**8. Hysteresis.** A $32 \times 32$ lattice, field stepped $+1 \to -1 \to +1$ in $81$ steps, four
seeds. At $\kB T = 1.5\,J$ the area of the loop is $2.20 \pm 0.04$, $1.48 \pm 0.02$ and
$1.18 \pm 0.04$ for $5$, $20$ and $80$ sweeps per step: slower sweeps shrink it, and it stays
open. At $2.0\,J$, $0.98$, $0.51$ and $0.27$: still open, and narrowing faster. At $3.0\,J$,
above $T_c$, $0.013$, $0.015$ and $0.021$, which is noise: the curve retraces itself.

:::{figure} ../media/ising-hysteresis.mp4
:alt: Left, a square lattice that begins almost entirely dark. Right, magnetization against field: a grey S-shaped curve passes through the origin, and a blue curve traced by a red dot runs along the top at magnetization near 1 from field plus 1, past zero, to about minus 0.4, drops vertically to minus 1, runs along the bottom to minus 1, then on the way back stays at minus 1 past zero and jumps up near plus 0.4, closing a square loop. Each vertical jump happens as the lattice turns from dark to light, or back, within a few frames.
:width: 100%

A $64 \times 64$ lattice at $\kB T = 1.5\,J$ while the field is stepped from $+1$ to $-1$ and back,
$20$ sweeps per step. Left: the spins. Right: $m$ against $h$; the red dot is the current state
and the blue curve its history. The magnetization keeps its sign well past $h = 0$ — the state
with $m \approx +1$ in a negative field is metastable, module 14's superheated liquid in
magnetic form — until a reversed domain large enough to grow happens to form, and then the whole
lattice reverses in a few frames. The grey curve is the same sweep at $\kB T = 3.0\,J$, above
$T_c$: one smooth curve through the origin, the same in both directions.
:::

**9. Two update rules, one equilibrium.** Quench a random $64 \times 64$ lattice to
$\kB T = 1.5\,J$ under each rule, eight seeds: after $5$, $20$ and $100$ sweeps the energy per
spin is $-1.581$, $-1.804$, $-1.920$ under Metropolis and $-1.434$, $-1.675$, $-1.806$ under
Glauber. Glauber is visibly slower. At $\kB T = 2.8\,J$ in equilibrium ($32 \times 32$, eight
seeds), the two give $-0.9075 \pm 0.0007$ and $-0.9090 \pm 0.0006$: the same answer, within
$1.6$ combined standard errors. How fast the chain gets there is the algorithm's; where it gets
to is the Boltzmann distribution's.

**10. The error bar itself.** Sixteen independent runs at $\kB T = 2.35\,J$ on a $16 \times 16$
lattice, each reporting $\langle |m| \rangle$ with its $\tau$-corrected standard error: the
average reported error matches the actual scatter of the sixteen means, while the naive
$\sigma/\sqrt{n}$ is less than half of it. The test suite asserts both.

**The falsifying experiments.** Each misconception this module confronts has a measurement
above that it cannot survive. "The system settles fastest at $T_c$": item 6, where $\tau$ is
largest exactly there and grows with $L$. "Below $T_c$ the magnetization is zero because up and
down cancel": item 7, where every lattice large enough to be a magnet holds one sign for the whole
run, and item 8, where the reading depends on the history. "Monte Carlo shows the real time
evolution": item 9, where two equally valid rules take different numbers of sweeps to reach the
same equilibrium.

**Against reality.** No experiment on a bench pairs with this model: exchange couplings are
invisible, and no cheap apparatus reaches a clean magnetic transition. Iron's Curie temperature
is $1043\ \mathrm{K}$ and nickel's $627\ \mathrm{K}$, and the measured magnetization of both
vanishes continuously, with a vertical tangent, as the module says it must. But neither is a
two-dimensional Ising magnet: they are three-dimensional, and their moments can point in any
direction, not just up or down. Their measured exponent $\beta$ lies near $0.36$–$0.38$ — not
the square lattice's $1/8$, not mean field's $1/2$, and not even the three-dimensional Ising
value $0.326$. Which class a system falls into is decided by the dimension and the symmetry of
its order parameter, which is the content of universality.

:::{admonition} Does a finite simulation ever show a phase transition?
:class: open-question
No — not in the strict sense. A phase transition is a singularity of the free energy, and on a
lattice of $N$ spins the partition function is a finite sum of exponentials, an analytic function
of $T$: every observable above is smooth, every peak finite. What a simulation provides is the
*trend*: peaks that grow and sharpen and converge as $L$ grows, in exactly the way a singularity
at $N \to \infty$ would produce, consistent with an exact solution where one exists. That is
evidence, sometimes overwhelming evidence, and never proof. The singularity is a statement about
a limit, and the limit is established by derivation — here, Onsager's.
:::

(15-ising-transfer)=
## Transfer the idea

The Ising model is the simplest system with a phase transition, and the Metropolis algorithm the
simplest way to sample a distribution you cannot sum. Both travel far.

- **Back to module 11.** The Metropolis rule is module 11's Boltzmann distribution turned into an
  algorithm: the finite-bath argument said *what* the probabilities are, detailed balance says
  how to *produce* configurations with those probabilities one flip at a time.
- **Back to module 12.** The fluctuation identities were reused unchanged — $c$ and $\chi$ are
  variances — and the $J = 0$ limit of the Ising model is module 12's paramagnet, exactly.
  Problem 6 recovers it.
- **Back to module 14.** The field-driven reversal below $T_c$ is a first-order transition, with
  metastable states, nucleation and hysteresis — the magnetic version of the superheated liquid
  — along a line that ends at a critical point. Through the lattice gas the line *is* a
  coexistence curve, and the Ising critical point is a liquid–gas critical point. That is why
  module 14's van der Waals exponent $1/2$ was wrong and the real fluid's $0.32$ is the Ising one.
- **Back to module 03.** The autocorrelation time is the correlated walk's lesson made
  quantitative: correlated samples still obey the $n^{-1/2}$ law, but with $n$ replaced by
  $N_{\mathrm{eff}} = n/(2\tau)$, and an error bar that ignores it is too small by
  $\sqrt{2\tau}$.
- **Forward to module 18.** How long a fluctuation takes to die away — the correlation time —
  returns there as the time-correlation function of a transport process.
- **Critical opalescence.** A fluid at its critical point turns milky. Its correlation length,
  the size of the correlated density patches, grows past the wavelength of light, and the
  patches scatter it — the same divergence the susceptibility peak reports here.
- **Magnetic memory.** A bit on a hard disk is a small magnetized region whose reversal requires
  a field above its coercive field — the corner of the hysteresis loop. It keeps its bit for years
  because, like the large lattice of item 7, reversing it means crossing a barrier that grows
  with its size.
- **Monte Carlo everywhere.** The same algorithm, with a different "energy", samples the
  posterior distributions of Bayesian statistics (where it is called Markov chain Monte Carlo),
  folds proteins in simulation, and — with the temperature slowly lowered, "simulated annealing"
  — finds good solutions to optimization problems far too large to search. In every one of
  those, the autocorrelation time decides how much the output can be trusted.

Looking ahead:

- **Module 16** puts quantized energy levels into solids and radiation; its heat capacities are
  the smooth, transition-free cousins of this module's peak.
- **Module 17** finds a phase transition with no interactions at all: Bose–Einstein condensation,
  driven by quantum statistics alone.
- **Module 18** asks how fluctuations relax in time, with the correlation time as its central
  quantity.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — acceptance at the critical point.** On the square lattice at $h = 0$ and
$\kB T = \kB T_c = 2.269\,J$, find the Metropolis acceptance probabilities for flips with
$\Delta E = 4J$ and $8J$, and the Glauber probability for $\Delta E = 4J$.

:::{dropdown} Solution
Metropolis: $e^{-4/2.269} = 0.172$ and $e^{-8/2.269} = 0.029$. (In fact
$e^{-2J/(\kB T_c)} = \sqrt{2} - 1$ exactly, from Onsager's formula, so the first is
$(\sqrt{2} - 1)^2 = 3 - 2\sqrt{2} = 0.1716$.) Glauber: $1/(1 + e^{4/2.269}) = 0.146$, lower,
as it is for every $\Delta E$. Both satisfy detailed balance; Glauber also accepts a $\Delta E
= 0$ flip only half the time, where Metropolis always does.
:::

**Worked example 2 — domain walls in a chain.** For a ring at $\kB T = J$, how many sites must it
have before two domain walls lower its free energy? How far apart are the walls actually, in
equilibrium?

:::{dropdown} Solution
$\Delta F \approx 4J - \kB T \ln(N^2/2) < 0$ requires $N^2/2 > e^4$, so $N > \sqrt{2}\,e^2 =
10.4$: about ten sites. The exact energy per spin $-\tanh 1 = -0.762$ means a fraction
$(1 - \tanh 1)/2 = 0.119$ of the bonds are walls — one every $8.4$ bonds. The two estimates agree
on the scale: at $\kB T = J$ order survives over a handful of sites, and no further.
:::

**Worked example 3 — mean field above the true transition.** Solve the mean-field equation for
the square lattice at $\kB T = 3J$ and $h = 0$ by iteration, starting from $m = 0.5$. What is the
true spontaneous magnetization at this temperature?

:::{dropdown} Solution
Iterate $m \leftarrow \tanh(4m/3)$: $0.583$, $0.651$, $0.700$, $0.732$, $0.752$, $0.763, \dots$,
converging to $0.776$. Mean field says the lattice is strongly magnetized. In truth $3J$ is above
Onsager's $2.269\,J$, and $m_0 = 0$. Mean field ignores the fluctuations that, at this
temperature, destroy the order it predicts.
:::

**Worked example 4 — a heat capacity from a variance.** A $32 \times 32$ lattice at
$\kB T = 2.5\,J$ gives an energy-per-spin trace with variance $0.0055\,J^2$. Find the heat
capacity per spin.

:::{dropdown} Solution
$c = N\,\mathrm{Var}(e)/(\kB T^2)$; in reduced units $c/\kB = 1024 \times 0.0055/2.5^2 = 0.90$.
No derivative was taken: the response to heating is read off the spontaneous fluctuations,
exactly as in module 12.
:::

**Worked example 5 — an honest error bar.** A trace of $5000$ samples of $|m|$ has standard
deviation $0.08$ and autocorrelation time $40$ samples. Quote the mean's standard error, and the
naive one.

:::{dropdown} Solution
$N_{\mathrm{eff}} = 5000/80 = 62.5$, so the error is $0.08/\sqrt{62.5} = 0.010$. The naive
$0.08/\sqrt{5000} = 0.0011$ is nine times too small — the factor $\sqrt{2\tau} = \sqrt{80}$. A
result quoted with the naive bar would claim a precision the run does not have.
:::

**Worked example 6 — reading Onsager–Yang.** Compute the exact spontaneous magnetization at
$\kB T = 2J$.

:::{dropdown} Solution
$\sinh(2J/(\kB T)) = \sinh 1 = 1.1752$; $\sinh^{-4} 1 = 0.5243$; $1 - 0.5243 = 0.4757$; and
$0.4757^{1/8} = 0.911$. The $64 \times 64$ simulation gives $0.9109 \pm 0.0002$; mean field gives
$0.958$.
:::

:::{note} Your predictions, revisited
1. **Close to $\pm 1$, and which sign depends on the history.** The canonical average is zero by
   symmetry, but a large lattice below $T_c$ holds one sign for longer than any run: the
   ensemble average and the sample stop being the same thing. See
   [the derivation](#15-ising-derive), step 1, and item 7 of the verification.
2. **At the transition.** The autocorrelation time peaks at $T_c$ and grows with the lattice:
   critical slowing down. Deep in either phase the simulation forgets itself within a sweep or
   two.
3. **$L = 64$.** The larger lattice's curve drops more steeply; no finite lattice drops
   vertically, because the singularity belongs to $N \to \infty$.
4. **It loops.** Below $T_c$ the magnetization keeps its sign past $h = 0$ and reverses abruptly
   at a field that depends on the sweep rate; above $T_c$ the curve retraces itself.
:::

(15-ising-quiz)=
## Check your understanding

```{include} ../_generated/quiz-15-ising.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](15-ising-problems.md).

(15-ising-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. Why can a simulation never prove that a phase transition exists? What *can* it establish, and
   what else is needed?
2. The energy of the Ising model does not prefer up over down. Who, or what, chooses the
   direction of a magnet cooled through its Curie point?
3. Why is a Metropolis "sweep" not a unit of physical time? What would you need to know about a
   real magnet to say how long its domains take to coarsen?
4. Why does the one-dimensional chain refuse to order at any temperature, while the square
   lattice orders below $2.269\,J/\kB$? Answer without a formula.

(15-ising-advanced)=
## Advanced: the transfer matrix, and finite-size scaling

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence, or in later modules, depends on this section. Core verification
compared the susceptibility peaks with exponents it quoted; here the chain is solved exactly,
and the reason those comparisons work — finite-size scaling — is made explicit.
:::

**The chain, solved.** On a ring of $N$ spins, write the Boltzmann weight as a product over bonds,

$$
e^{-E_s/(\kB T)} = \prod_{i=1}^{N} T_{s_i s_{i+1}} ,
\qquad
T_{s s'} = \exp\!\left[K s s' + \frac{b}{2}(s + s')\right] ,
$$

with $K = J/(\kB T)$, $b = h/(\kB T)$ and $s_{N+1} = s_1$. $T$ is a $2 \times 2$ matrix indexed by
the two values of a spin,

$$
T = \begin{pmatrix} e^{K + b} & e^{-K} \\ e^{-K} & e^{K - b} \end{pmatrix} ,
$$

and summing over every spin is matrix multiplication around the ring:
$Z = \mathrm{Tr}\, T^N = \lambda_+^N + \lambda_-^N$, with eigenvalues

$$
\lambda_\pm = e^{K} \cosh b \pm \sqrt{e^{2K} \sinh^2 b + e^{-2K}} .
$$

As $N \to \infty$ the larger eigenvalue wins, $\ln Z \approx N \ln \lambda_+$, and every exact
result of step 3 follows by differentiation: $m = \partial \ln\lambda_+/\partial b$ gives the
magnetization in a field, and at $b = 0$, $\lambda_+ = 2\cosh K$ gives $E/(NJ) = -\tanh K$. The
eigenvalues never cross for real $K$, so $\ln \lambda_+$ is analytic at every $T > 0$: no
transition, now by a second route. The correction $(\lambda_-/\lambda_+)^N = \tanh^N K$ at
$h = 0$ is also the correlation between spins $N$ sites apart, so the correlation length is
$\xi = -1/\ln\tanh K$, finite at every $T > 0$ and diverging only as $T \to 0$.

**Finite-size scaling.** Near $T_c$ the only length that matters on an $L \times L$ lattice is the
ratio $L/\xi$, and $\xi \propto |T - T_c|^{-\nu}$. So an observable that diverges as
$|T - T_c|^{-\gamma}$ in the infinite system takes, on a finite one, the form

$$
\chi'(T, L) = L^{\gamma/\nu}\, \tilde{\chi}\!\left( (T - T_c)\, L^{1/\nu} \right) ,
$$

with one scaling function $\tilde{\chi}$ for every $L$. Two consequences: the peak height grows as
$L^{\gamma/\nu} = L^{7/4}$, and the peak sits where the argument takes a fixed value, so its
position drifts as $T_{\mathrm{peak}} - T_c \propto L^{-1/\nu} = L^{-1}$ — the extrapolation
used in problem 4 and in the laboratory. Plotted as $\chi' L^{-7/4}$ against
$(T - T_c) L$, the curves for every $L$ collapse onto one. The collapse is a sensitive test:
with the wrong exponents, or the wrong $T_c$, the curves fan apart.

**The cure for critical slowing down.** A local rule flips one spin at a time, and a correlated
domain of size $\xi$ takes a time growing like $\xi^{z}$ to rearrange. Cluster algorithms — the
Wolff algorithm is the simplest — instead build a whole correlated cluster of aligned spins by a
random rule chosen so that detailed balance still holds, and flip it at once. At $T_c$ on the
square lattice they bring $z$ from about $2.17$ down to about $0.25$. This course does not
implement one: the slowing-down measurement is the lesson, and a cure would hide it.

:::{admonition} What is still open here
:class: open-question
Why should a magnet whose moments can point only along one axis, a fluid and a liquid mixture
share the exponent $\beta \approx 0.326$ when their forces have nothing in common? The answer — that near a critical point the system looks the same
at every scale, and that repeatedly coarse-graining it flows to a fixed point whose properties
depend only on dimension and symmetry — is the renormalization group of Kadanoff and Wilson. It
is the theory behind universality, and it lies beyond this course.
:::
