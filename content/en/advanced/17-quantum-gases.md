---
title: Quantum statistics — Bose–Einstein and Fermi–Dirac gases
short_title: 17 · Quantum gases
module: 17-quantum-gases
objectives:
  - id: OBJ-17-1
    text: State the symmetry postulate — a single-particle state holds any number of identical bosons but at most one identical fermion — and count the two-particle states of a two-level system under classical, Bose and Fermi rules (4 / 3 / 1).
  - id: OBJ-17-2
    text: Derive the mean occupations n_BE = 1/(exp((eps - mu)/(k_B T)) - 1) and n_FD = 1/(exp((eps - mu)/(k_B T)) + 1) from the grand-canonical sum over one state, and explain why a boson gas requires mu < eps_0 while n_FD needs no such bound.
  - id: OBJ-17-3
    text: Show that both occupations reduce to n_MB = exp(-(eps - mu)/(k_B T)) when exp((eps - mu)/(k_B T)) >> 1, and state the classical-limit criterion n lambda^3 << 1 with lambda = h/sqrt(2 pi m k_B T).
  - id: OBJ-17-4
    text: Count states in a 3-D box to obtain g(eps) proportional to sqrt(eps), and use N = integral of g(eps) n(eps) d eps to determine mu(T; N) numerically, predicting its direction of travel as T falls for classical, Bose and Fermi gases.
  - id: OBJ-17-5
    text: Explain Bose–Einstein condensation as saturation of the excited states — below T_c = (2 pi hbar^2/(m k_B)) (n/zeta(3/2))^(2/3) the excited states cannot hold every particle and the ground state takes the overflow, with N_0/N = 1 - (T/T_c)^(3/2).
  - id: OBJ-17-6
    text: Compute eps_F = (hbar^2/(2m)) (3 pi^2 n)^(2/3), T_F = eps_F/k_B, the ground-state energy U = (3/5) N eps_F and the degeneracy pressure P = (2/5) n eps_F of an ideal Fermi gas, and compare P to the classical n k_B T at the same density.
  - id: OBJ-17-7
    text: Explain why the electronic heat capacity of a metal is linear in T and small at room temperature — only the shell about k_B T deep at eps_F can be excited — and estimate C_el/C_classical ~ T/T_F.
  - id: OBJ-17-8
    text: Recompute the Planck spectral energy density as the mu = 0 Bose–Einstein occupation times the photon density of modes, and explain why photons have mu = 0 (their number is not conserved).
---

# Quantum statistics: Bose–Einstein and Fermi–Dirac gases

(17-quantum-gases-puzzle)=
## The puzzle: identical particles, opposite habits

The copper in a phone charger is a box full of gas. Each copper atom gives up one electron to the
metal as a whole, and those **conduction electrons** — $8.5 \times 10^{28}$ of them in every cubic
metre — move through the crystal much as molecules move through a container. Module 04 knows what
to do with a gas: give every particle $\tfrac32\kB T$ of kinetic energy, and the gas has a heat
capacity of $\tfrac32 R$ per mole. A mole of copper atoms therefore ought to need $3R$ for its
lattice (module 16's Dulong–Petit value) plus another $\tfrac32 R$ for its electrons: half as much
again.

It does not. Measured at room temperature, metals sit at Dulong–Petit, and the electrons' share of
the heat capacity is less than one part in a hundred. A gas that should dominate the heat capacity
of every metal barely registers. Where does its heat capacity go?

The second gas goes the other way. Cool liquid helium-4 below $2.17\ \mathrm{K}$ and it turns into
a **superfluid**: it flows without friction through pores so fine that the ordinary liquid is
held back, and creeps up the walls of its container. In 1995 a cloud of rubidium-87 atoms was cooled to a few
hundred billionths of a kelvin, and a large fraction of the atoms — all identical — was found in
one and the same quantum state, the lowest one the trap allowed.

:::{important} The question
Electrons and helium atoms are both gases of identical particles. One refuses to take up heat
even at room temperature; the other, when cold enough, piles by the million into a single state.
Nothing in modules 11 to 13 predicts either. What single rule about identical particles produces
two opposite behaviours — and why does it never show in the air of this room?
:::

The answer adds exactly one thing to the course: a rule for how many identical particles may share
a state. No wave functions, no operators. Everything else is counting, and module 13's
chemical potential.

(17-quantum-gases-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. A gas of electrons is cooled toward absolute zero at fixed density. Equipartition says the mean
   kinetic energy per electron, $\tfrac32\kB T$, goes to zero. Does it?
2. Three single-particle states share the same value of $(\varepsilon - \mu)/\kB T$: one in a
   classical gas, one in a gas of bosons, one in a gas of fermions. Rank the mean number of
   particles each holds.
3. Are the conduction electrons in copper at room temperature a classical gas or a quantum one?
   And is that decided by the temperature, or by something else?
4. Below the condensation temperature a large fraction of a Bose gas sits in the lowest state,
   which has no kinetic energy. Does the gas still push on its walls? If it does, how does the
   pressure depend on how much gas there is?

:::{note} Why we ask first
The first and third are the ones that catch nearly everyone: both rest on the intuition that
"quantum" means "cold". Every answer is collected at the end of the module.
:::

(17-quantum-gases-explore)=
## Explore the model

The laboratory has four explorers. The first draws the mean occupation of a state against its
energy for bosons, fermions and classical particles, with sliders for the temperature and the
chemical potential, and a logarithmic view. The second follows a Bose gas through condensation,
both for the ideal infinite gas and for a box of a thousand to a hundred thousand atoms counted
level by level. The third fills a Fermi sea and shows which electrons can still take up heat. The
fourth tracks the chemical potential of all three gases at one density as the temperature falls.
Then the laboratory runs the experiments this module is built on: the occupations rebuilt from
explicit sums, the states of a box counted one by one, the chemical potential solved for at fixed
density, module 16's Planck spectrum rebuilt from a boson occupation, and a measurement of the
conduction electrons of silver.

:::{figure} ../media/quantum-occupations.mp4
:alt: Two plots. Left, the mean occupation of a state divided by n lambda cubed, on a logarithmic axis, against energy over k_B T from 0 to 10, for bosons (blue), classical particles (black, dashed) and fermions (red). The classical curve is a straight line that never moves. At first the blue curve shoots up near zero energy and lies below the black line further out, while the red curve is flat near zero energy and lies above the black line further out. As n lambda cubed falls from 2.5 to 0.001 the blue and red curves close in on the black line until all three coincide. Right, mu over k_B T against n lambda cubed on a logarithmic axis for the three gases: the curves coincide at low n lambda cubed and separate above about 0.1, the blue one flattening at zero, the red one rising above the black. A vertical marker moves left as the animation runs.
:width: 100%

Three gases at the same density and temperature: bosons (blue), classical particles (black,
dashed) and fermions (red), each with its own chemical potential, as the gas is heated at fixed
density so that $n\lambda^3$ falls from $2.5$ to $0.001$. Left: the mean occupation of a state
against its energy, divided by $n\lambda^3$ so that the classical curve, $e^{-\varepsilon/\kB T}$,
stays put. In the dense gas the bosons crowd into the lowest states and the fermions, barred from
crowding, are pushed out to higher energies; as the gas thins, both fall onto the classical line.
Right: $\mu/\kB T$ for each gas against $n\lambda^3$, with a marker at the current value. The three
agree when the gas is dilute; above $n\lambda^3 \approx 0.1$ the fermions' $\mu$ climbs above the
classical one and the bosons' flattens at zero, which it reaches at $n\lambda^3 = 2.612$ (dotted).
:::

:::{admonition} Model specification
:class: model-spec
- **System:** an ideal gas of identical particles — bosons, fermions, or classical particles for comparison — in a rigid cubic box of volume $V$; each particle's states are the standing waves of the box, each $g_s$-fold degenerate in spin.
- **Dynamics:** none — every curve is thermal equilibrium; nothing evolves.
- **Boundary:** every single-particle state exchanges energy and particles with a reservoir at temperature $T$ and chemical potential $\mu$; the mean number of particles is held fixed by solving for $\mu$.
- **Ensemble:** grand canonical, state by state — module 13's one-site argument applied to every standing wave of the box.
- **Ignored:** every interaction between the particles (no collisions, no attraction, no repulsion, no force of any kind); the shape of a real trap (a uniform box only); relativity; for electrons, the crystal lattice beyond a free-electron box.
- **Valid when:** the spacing of the box's levels is far below $\kB T$ (and below $\varepsilon_F$ for fermions), so a smooth density of states can replace the sum over levels; $N \gg 1$ for the condensation argument.
- **Failure modes:** liquid helium-4, whose atoms interact strongly; real metals, whose electrons feel the lattice; a few hundred atoms, where condensation is a smooth crossover; white dwarfs near the Chandrasekhar mass, where the electrons are relativistic.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 17 — quantum gases](/lite/lab/index.html?path=en/labs/17-quantum-gases.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/17-quantum-gases.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- In the occupation explorer, set $\mu$ well below zero and switch to the logarithmic view. Then
  raise $\mu$ toward zero. Where do the three curves part company?
- Try to push the bosons' $\mu$ above the lowest energy. What does the explorer do, and why?
- In the condensation explorer, compare a box of a thousand atoms with one of a hundred thousand
  near $T_c$.
- In the Fermi-sea explorer, lower $T/T_F$ from $1$ to $0.01$ and watch which part of the sea
  changes.

(17-quantum-gases-derive)=
## Derive the result

**System and boundary.** An ideal gas of $N$ identical particles of mass $m$ in a cubic box of
side $L$ and volume $V = L^3$ with rigid walls, in contact with a heat bath at temperature $T$.
Each single-particle state is treated as a subsystem that exchanges energy and particles with the
rest of the gas, which acts as its reservoir.

**Independent variables.** The temperature $T$, the volume $V$ and the number of particles $N$ —
equivalently the density $n = N/V$. The chemical potential $\mu$ is not an independent variable
here: it is whatever value makes the gas hold $N$ particles.

**Sign convention.** The course convention, $\mathrm{d}U = \dbar Q + \dbar \Won$, holds. It is
exercised in step 7: squeezing a Fermi gas at absolute zero takes work,
$\dbar \Won = -P\,\mathrm{d}V > 0$ when $\mathrm{d}V < 0$, and with $\dbar Q = 0$ all of it
becomes energy of the gas.

**Units.** SI throughout, with $\kB$, $h$ and $\hbar = h/2\pi$ written explicitly. Energies are in
joules; the electronvolt, $1\ \mathrm{eV} = 1.602 \times 10^{-19}\ \mathrm{J}$, appears only as a
convenience in quoted numbers.

**Route.** Nine steps. State the rule for identical particles and see what it does to counting;
put one state in contact with a reservoir and find its mean occupation, for bosons and for
fermions; take the dilute limit, which is classical physics; count the states of a box; fix the
number of particles, which fixes $\mu$; and then follow the consequences — condensation for bosons,
the Fermi sea and its pressure for fermions, the heat capacity of a metal, and, as a corollary,
module 16's photons.

### Step 1: identical particles

Module 08 counted microstates of coins and module 12 of molecules, and both times a question was
left hanging: when two particles are of the same kind, is swapping them a new microstate? Module 12
answered "no" by dividing by $N!$, and justified it only for a gas so thin that no two particles
ever compete for one state. Quantum mechanics answers the question exactly, and the answer is the
only quantum input this module needs.

:::{admonition} The symmetry postulate
:class: model-assumption
Identical particles are not merely hard to tell apart: they carry no labels at all. A many-particle
state of identical particles is specified completely by its **occupation numbers** — how many
particles are in each single-particle state — and nothing else. Nature allows exactly two rules.

- **Bosons:** any number of particles may occupy a single-particle state. Photons, helium-4 atoms
  and rubidium-87 atoms are bosons.
- **Fermions:** at most one particle may occupy a single-particle state — the **Pauli exclusion
  principle**. Electrons, protons, neutrons and helium-3 atoms are fermions.

Which rule a particle obeys is fixed by its spin: integer spin makes a boson, half-integer spin a
fermion. Relativistic quantum field theory derives that connection (the spin–statistics theorem);
this module takes it as given and shows what it does.
:::

Count the states of two particles shared between two single-particle states, $a$ and $b$.

| | classical (labelled) | bosons | fermions |
|---|---|---|---|
| both in $a$ | 1 | 1 | 0 |
| one in each | 2 | 1 | 1 |
| both in $b$ | 1 | 1 | 0 |
| **total** | **4** | **3** | **1** |

Classical particles carry labels, so "particle 1 in $a$, particle 2 in $b$" and the reverse are two
microstates. For identical particles they are one. The exclusion rule then removes the states with
two fermions together. If every microstate is equally likely, as module 08 assumed, the chance of
finding the two particles in the same state is $\tfrac24 = \tfrac12$ classically, $\tfrac23$ for
bosons and $0$ for fermions. Bosons bunch and fermions avoid one another — and no force is
involved. It is counting.

The same counting explains module 12's $1/N!$. Spread $N$ particles over $M$ single-particle states.
Classical particles have $M^N$ arrangements, and module 12's corrected count is $M^N/N!$. Bosons
have $\binom{M+N-1}{N}$ and fermions $\binom{M}{N}$. When the states far outnumber the particles,
$M \gg N$, both quantum counts approach $M^N/N!$: three particles in a hundred states give $1.03$
and $0.97$ times it, in a thousand states $1.003$ and $0.997$. Dividing by $N!$ was quantum
statistics in the limit where it does not matter which kind it is.

### Step 2: one state in contact with a reservoir

Module 13 put a single adsorption site in contact with a gas and weighted each of its states by
$e^{-(E - \mu N)/\kB T}$, where $N$ is the number of particles the site holds. Apply the same
argument to one single-particle state of energy $\varepsilon$: holding $n$ particles, it has energy
$n\varepsilon$, and its weight is $e^{-n(\varepsilon - \mu)/\kB T}$.

:::{admonition} The grand partition function of one state
:class: definition
The **grand partition function** of a single-particle state of energy $\varepsilon$, in contact
with a reservoir at temperature $T$ and chemical potential $\mu$, is the sum of its weights over the
occupations the symmetry postulate allows:

$$
\Xi = \sum_{n} e^{-n(\varepsilon - \mu)/\kB T} ,
$$

and the mean occupation is
$\langle n \rangle = \sum_n n\, e^{-n(\varepsilon - \mu)/\kB T} \big/ \Xi$.
:::

For **bosons** $n$ runs over $0, 1, 2, \ldots$ and the sum is module 12's geometric series. Write
$x = (\varepsilon - \mu)/\kB T$:

$$
\Xi_{\mathrm{BE}} = \sum_{n=0}^{\infty} e^{-nx} = \frac{1}{1 - e^{-x}} ,
$$

which converges only if $x > 0$. The mean occupation is the same derivative that gave module 12 its
mean energy, $\langle n \rangle = -\partial \ln \Xi / \partial x$.

:::{admonition} The Bose–Einstein distribution
:class: theorem
A single-particle state of energy $\varepsilon$ in a gas of bosons holds, on average,

$$
n_{\mathrm{BE}}(\varepsilon) = \frac{1}{e^{(\varepsilon - \mu)/\kB T} - 1}
$$

particles. The sum exists only if $\mu < \varepsilon$, so in a Bose gas the chemical potential lies
below the energy $\varepsilon_0$ of the lowest single-particle state: $\mu < \varepsilon_0$.
:::

As $\mu$ rises toward $\varepsilon_0$, the lowest state's occupation $1/(e^{(\varepsilon_0 -
\mu)/\kB T} - 1)$ grows without limit. The bound is not a technicality: step 6 is what happens when
a gas presses against it.

For **fermions** $n$ is $0$ or $1$, and the sum has two terms:

$$
\Xi_{\mathrm{FD}} = 1 + e^{-x} .
$$

:::{admonition} The Fermi–Dirac distribution
:class: theorem
A single-particle state of energy $\varepsilon$ in a gas of fermions holds, on average,

$$
n_{\mathrm{FD}}(\varepsilon) = \frac{1}{e^{(\varepsilon - \mu)/\kB T} + 1}
$$

particles: between $0$ and $1$ for every $\varepsilon$ and $\mu$, and exactly $\tfrac12$ at
$\varepsilon = \mu$. No bound on $\mu$ is needed.
:::

This is module 13's site occupation, unchanged: an electron state is a site that holds at most one
particle. Module 13 said the function would come back under this name, and here it is.

The mean is not the whole story. The occupation of a state fluctuates, and its variance is
$n(1 + n)$ for bosons, $n(1 - n)$ for fermions, and $n$ for classical particles. Bosons fluctuate
more than classical particles — the bunching of the counting table, seen in a single state — and
fermions less. The laboratory draws occupations at random from each distribution and checks all
three.

### Step 3: the classical corner

Both distributions differ from each other only in the sign of the $1$ in the denominator. When
$e^{(\varepsilon - \mu)/\kB T}$ is large, that $1$ does not matter.

:::{admonition} Maxwell–Boltzmann as the dilute limit
:class: theorem
When $e^{(\varepsilon - \mu)/\kB T} \gg 1$ both quantum occupations reduce to the classical one,

$$
n_{\mathrm{BE}} \approx n_{\mathrm{FD}} \approx n_{\mathrm{MB}} = e^{-(\varepsilon - \mu)/\kB T} \ll 1 .
$$

At the same value of $(\varepsilon - \mu)/\kB T$ they are always ordered
$n_{\mathrm{BE}} > n_{\mathrm{MB}} > n_{\mathrm{FD}}$, because $e^x - 1 < e^x < e^x + 1$.
:::

When $e^x = 100$ the three agree to $1\%$: $n_{\mathrm{BE}}/n_{\mathrm{MB}} = 100/99$ and
$n_{\mathrm{FD}}/n_{\mathrm{MB}} = 100/101$. The condition holds for every state at once when $\mu$
lies far below the lowest energy — when every state is so sparsely occupied that no two particles
ever compete for one, and whether they could share it never comes up. That is classical physics.
Step 5 turns "$\mu$ far below zero" into a statement about density and temperature.

### Step 4: counting the states of a box

The single-particle states of a cube with hard walls are standing waves, exactly as module 16's
cavity modes were. Each has wave vector

$$
\mathbf{k} = \frac{\pi}{L}\,(n_x, n_y, n_z) , \qquad n_x, n_y, n_z = 1, 2, 3, \ldots
$$

and, for a particle of mass $m$, kinetic energy $\varepsilon = \hbar^2 k^2/2m$. Counting the states
with energy below $\varepsilon$ is counting integer points inside an octant of a sphere of radius
$|\mathbf{n}| = (L/\pi)\sqrt{2m\varepsilon}/\hbar$, one point per unit volume when the radius is
large. With $g_s$ spin states for each wave,

$$
N(\varepsilon) = g_s \times \frac{1}{8} \times \frac{4\pi}{3}\,|\mathbf{n}|^3
= \frac{g_s V}{6\pi^2}\left(\frac{2m\varepsilon}{\hbar^2}\right)^{3/2} .
$$

:::{admonition} The density of states of a box
:class: theorem
The number of single-particle states with energy between $\varepsilon$ and
$\varepsilon + \mathrm{d}\varepsilon$ in a box of volume $V$ is $g(\varepsilon)\,\mathrm{d}\varepsilon$,
with

$$
g(\varepsilon) = \frac{g_s V}{4\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\sqrt{\varepsilon} .
$$

$g_s = 1$ for a spinless boson such as helium-4, $g_s = 2$ for an electron.
:::

The count is module 16's, with one change: there, $\varepsilon = \hbar c k$ for a photon, and the
density of modes grew as $\varepsilon^2$; here $\varepsilon \propto k^2$, and it grows as
$\sqrt{\varepsilon}$. The approximation of counting volume instead of points misses the states on
the octant's faces, a relative error of about $(9/4)/|\mathbf{n}|$, and the laboratory measures it.
It is negligible: for helium in a $1\ \mathrm{cm}$ box the lowest level spacing is
$6 \times 10^{-15}\ \mathrm{K}$ in temperature units, and at $1\ \mathrm{K}$ the states that matter
have $|\mathbf{n}|$ of about ten million.

### Step 5: holding the number of particles fixed

Multiply the number of states by their mean occupation and integrate:

$$
N = \int_0^\infty g(\varepsilon)\, n(\varepsilon)\, \mathrm{d}\varepsilon .
$$

For a given $N$, $V$ and $T$ this is one equation for one unknown, $\mu$. Substituting
$x = \varepsilon/\kB T$ collects the constants into one length, module 12's thermal wavelength.

:::{admonition} The thermal wavelength and the occupation integral
:class: definition
The **thermal wavelength** of a particle of mass $m$ at temperature $T$ is

$$
\lambda = \frac{h}{\sqrt{2\pi m \kB T}} ,
$$

and the **occupation integral** of order $\tfrac32$ is the pure number

$$
F(\eta) = \frac{2}{\sqrt{\pi}}\int_0^\infty \sqrt{x}\; n(x - \eta)\,\mathrm{d}x ,
\qquad \eta = \frac{\mu}{\kB T} ,
$$

where $n(x - \eta)$ is the occupation of a state with $(\varepsilon - \mu)/\kB T = x - \eta$, under
whichever statistics the gas obeys.
:::

With these, the integral over states becomes one line:

:::{admonition} The density fixes the chemical potential
:class: theorem
For an ideal gas of identical particles in a box,

$$
n\lambda^3 = g_s\, F(\mu/\kB T) .
$$

$F$ increases steadily with $\eta$, so each density and temperature fix exactly one $\mu$.
:::

For classical particles the integral can be done by hand: $F_{\mathrm{MB}}(\eta) = e^{\eta}$, and

$$
\mu = \kB T \ln\frac{n\lambda^3}{g_s} .
$$

This is module 13's $\mu = \kB T\ln(n/n_Q)$, with $n_Q = g_s/\lambda^3$. Module 13 named the
quantum concentration and promised that this module would derive it: here it is, the density at
which the gas has one particle per spin state in each cube of side $\lambda$.

For bosons and fermions there is no closed form, and $\mu$ is found numerically: given $n\lambda^3$,
find the $\eta$ at which $F(\eta) = n\lambda^3/g_s$. The laboratory does it by bisection, and its
result, which knows nothing of module 13, reproduces module 13's classical formula to sixteen
digits in the dilute limit.

:::{admonition} The classical criterion
:class: approximation
A gas is classical — every state sparsely occupied, $\mu$ far below the lowest energy, and the
three distributions indistinguishable — when

$$
n\lambda^3 \ll 1 ,
$$

that is, when the particles are much farther apart than their thermal wavelength. At $n\lambda^3 =
0.01$ the three values of $\mu/\kB T$ agree to within $0.01$. Above $n\lambda^3 \approx 1$ the
gas is quantum, or **degenerate**, and the statistics decide everything.
:::

The criterion involves the density, the mass and the temperature together. Air at room
temperature has $n\lambda^3 = 2 \times 10^{-7}$, and helium gas at $0\,{}^\circ\mathrm{C}$ and one
atmosphere $4 \times 10^{-6}$: profoundly classical. Liquid helium at $2.2\ \mathrm{K}$ has
$4.5$. The conduction electrons in copper at room temperature have $6800$: an electron is $7300$
times lighter than a helium atom, so its thermal wavelength at $300\ \mathrm{K}$ is
$4.3\ \mathrm{nm}$, nineteen times the spacing between electrons.

Which way does $\mu$ move as a gas is cooled at fixed density? $n\lambda^3$ grows as $T^{-3/2}$, so
$F$ must grow, and $\eta = \mu/\kB T$ must climb. How far it can climb depends on the statistics:

| $n\lambda^3$ (with $g_s = 1$) | $0.01$ | $0.1$ | $1$ | $2.612$ | $10$ |
|---|---|---|---|---|---|
| classical, $\mu/\kB T$ | $-4.605$ | $-2.303$ | $0$ | $0.960$ | $2.303$ |
| bosons, $\mu/\kB T$ | $-4.609$ | $-2.338$ | $-0.359$ | $0$ | $0$ |
| fermions, $\mu/\kB T$ | $-4.602$ | $-2.267$ | $0.349$ | $1.852$ | $5.456$ |

The classical formula takes $\mu$ above zero once $n\lambda^3 > 1$; it then predicts more than one
particle in the lowest states, which is the classical theory leaving the domain it was derived in.
The bosons' $\mu$ climbs to zero — the lowest energy — and stops there, at $n\lambda^3 = 2.612$. The
fermions' climbs without limit; as $T \to 0$, step 7 shows, $\mu$ tends to a fixed positive energy,
$\varepsilon_F$.

Two more integrals give the energy and the pressure. The energy is
$U = \int \varepsilon\, g(\varepsilon)\, n(\varepsilon)\,\mathrm{d}\varepsilon$, and the pressure
needs no new calculation at all.

:::{admonition} The pressure of an ideal gas is two-thirds of its energy density
:class: theorem
For an ideal nonrelativistic gas of any statistics — classical, Bose or Fermi —

$$
P = \frac{2}{3}\,\frac{U}{V} .
$$
:::

Module 04 derived it from the momentum carried to the walls: $P = \tfrac13 n\langle p\,v\rangle$,
and $p\,v = mv^2$ is twice the kinetic energy. Nothing in that argument asks how many particles
share a state. For a classical gas $U = \tfrac32 N\kB T$ and it is the ideal gas law.

### Step 6: Bose–Einstein condensation

The bosons' $\mu$ stops at zero, and $F_{\mathrm{BE}}$ stops with it. The largest value the
occupation integral can take is

$$
F_{\mathrm{BE}}(0) = \frac{2}{\sqrt{\pi}}\int_0^\infty \frac{\sqrt{x}}{e^{x} - 1}\,\mathrm{d}x = 2.612 ,
$$

a pure number — it is $\zeta(3/2)$, where $\zeta$ is the Riemann zeta function; this module quotes
the value and the laboratory computes it by quadrature.

:::{admonition} The excited states fill up
:class: theorem
In an ideal Bose gas the states above the ground state can hold at most

$$
N_{\mathrm{ex}}^{\max} = 2.612\,\frac{g_s V}{\lambda^3} \propto V T^{3/2}
$$

particles. This capacity shrinks as $T$ falls. It equals $N$ at the **condensation temperature**
$T_c$, where $n\lambda^3 = 2.612\, g_s$:

$$
\kB T_c = \frac{2\pi\hbar^2}{m}\left(\frac{n}{2.612\, g_s}\right)^{2/3} .
$$
:::

Below $T_c$ the excited states are full and cannot take the rest. The particles have one place
left to go: the ground state, which the integral never counted — its density of states
$g(\varepsilon) \propto \sqrt{\varepsilon}$ gives it zero weight at $\varepsilon = 0$, although it
is a perfectly good state that can hold any number of bosons. The ground state takes the overflow.

:::{admonition} The condensate fraction
:class: approximation
Below $T_c$ the fraction of the particles in the single lowest state is

$$
\frac{N_0}{N} = 1 - \frac{N_{\mathrm{ex}}^{\max}}{N} = 1 - \left(\frac{T}{T_c}\right)^{3/2} ,
$$

and above $T_c$ it is zero. This is a **Bose–Einstein condensate**. The derivation replaced the sum
over levels by an integral and then restored the ground state by hand; it becomes exact as
$N \to \infty$. In a box of finitely many atoms the transition is rounded: condensation starts
early and gradually, and the laboratory measures by how much.
:::

:::{figure} ../media/quantum-bec.mp4
:alt: Three panels as an ideal Bose gas is cooled from 1.6 T_c to 0.02 T_c. Left, a single column from 0 to 1: at first entirely light blue; after T_c a dark blue section grows from the bottom until it fills the column. Middle, a light-blue filled curve of the excited particles against energy over k_B T_c, which at first spreads out to high energy and peaks sharply near zero at T_c, then shrinks and squeezes toward zero energy as the gas cools further. Right, N_0 over N against T over T_c: a black curve that is zero above T_c and rises to 1 at T = 0; two dashed curves for boxes of a thousand and a hundred thousand atoms lie above it and rise smoothly through T_c; a dot moves along the black curve.
:width: 100%

An ideal Bose gas cooled at fixed density from $1.6\,T_c$ to $0.02\,T_c$, pausing at $T_c$. Left:
the share of the particles in the ground state (dark blue) and in all the excited states together
(light blue). Middle: how the excited particles are spread over energy, in units of $\kB T_c$; the
area under the curve is their share. At $T_c$ the curve rises sharply toward zero energy, but its
area is still all the particles; below $T_c$ it shrinks, as $T^{3/2}$, and the ground state holds
the rest. Right: the condensate fraction $N_0/N$ against $T/T_c$ — the ideal $1 - (T/T_c)^{3/2}$
(black, with the moving dot), and the exact result for a box of $10^3$ atoms (grey, dashed) and of
$10^5$ atoms (amber, dashed), computed level by level. The finite boxes condense earlier and more
gradually, and approach the ideal curve as they grow.
:::

Condensation is a statement about occupation, not about motion. Below $T_c$ the excited particles
are exactly as many as the excited states can hold at that temperature, and they move and collide
with the walls as before. Only they carry energy, so by step 5

$$
P = \frac{2}{3}\frac{U}{V} = 1.341\, g_s\,\frac{\kB T}{\lambda^3} \qquad (T < T_c),
$$

where $1.341$ is $\zeta(5/2)$. This pressure is not zero, and it does not depend on the density at
all: add atoms to a condensed gas at fixed temperature and they join the condensate, which carries
no momentum to the walls. At $T_c$ the pressure is $51\%$ of the classical $n\kB T$. The heat
capacity, $\tfrac32 N\kB$ for a hot gas, rises as the gas cools toward $T_c$, peaks there at
$1.93\,N\kB$ with a sharp corner, and falls below it as $T^{3/2}$.

### Step 7: the degenerate Fermi gas

Fermions cannot condense: each state takes one. Cool a Fermi gas to $T = 0$ and the occupation
becomes a step — every state below $\mu$ is full, every state above it empty. The particles fill
the box's states from the bottom, $g_s$ per standing wave, and the energy of the last one filled is
the **Fermi energy** $\varepsilon_F$. Step 4's count gives it at once: $N(\varepsilon_F) = N$.

:::{admonition} The Fermi sea at absolute zero
:class: theorem
An ideal gas of fermions of mass $m$, spin degeneracy $g_s$ and density $n$ at $T = 0$ fills every
state up to the Fermi energy

$$
\varepsilon_F = \frac{\hbar^2}{2m}\left(\frac{6\pi^2 n}{g_s}\right)^{2/3}
= \frac{\hbar^2}{2m}\left(3\pi^2 n\right)^{2/3} \quad (g_s = 2) ,
$$

with Fermi temperature $T_F = \varepsilon_F/\kB$. Its energy and pressure are

$$
U = \int_0^{\varepsilon_F} \varepsilon\, g(\varepsilon)\,\mathrm{d}\varepsilon = \frac35 N\varepsilon_F ,
\qquad
P = \frac{2}{5}\, n\, \varepsilon_F .
$$
:::

The energy follows from $g \propto \sqrt{\varepsilon}$: the mean of $\varepsilon$ weighted by
$\sqrt{\varepsilon}$ over $0$ to $\varepsilon_F$ is $\tfrac35\varepsilon_F$. The pressure is worth
deriving a second way, with the course's sign convention. Every level of the box is proportional
to $L^{-2} = V^{-2/3}$, so the energy of the filled sea is $U \propto V^{-2/3}$. At absolute zero
the sea stays in its ground state as it is squeezed slowly — the occupations cannot change — so no
heat flows, $\dbar Q = 0$, and $\mathrm{d}U = \dbar \Won = -P\,\mathrm{d}V$:

$$
P = -\frac{\mathrm{d}U}{\mathrm{d}V} = \frac{2}{3}\,\frac{U}{V} = \frac{2}{5}\, n\,\varepsilon_F .
$$

This is the **degeneracy pressure**. Squeezing the sea raises every level, and the work done on it
is stored as the energy of the raised levels.

For copper, with one conduction electron per atom, $n = 8.49 \times 10^{28}\ \mathrm{m^{-3}}$, and
with $g_s = 2$ and the electron's mass:

- $\varepsilon_F = 7.04\ \mathrm{eV}$, so $T_F = 81\,700\ \mathrm{K}$;
- the fastest electrons move at $v_F = \hbar k_F/m = 1.57 \times 10^6\ \mathrm{m\,s^{-1}}$, the
  **Fermi velocity**;
- the mean kinetic energy is $\tfrac35\varepsilon_F = 4.2\ \mathrm{eV}$ — a classical gas would
  need $33\,000\ \mathrm{K}$ to have it;
- the degeneracy pressure is $3.8 \times 10^{10}\ \mathrm{Pa}$, $380\,000$ atmospheres, against
  $3.5 \times 10^{8}\ \mathrm{Pa}$ for a classical gas of the same density at room temperature —
  more than a hundred times larger.

All of this is at absolute zero, and none of it involves a force: the model's Ignored line lists
every interaction between the electrons. The pressure is kinetic energy, delivered to the walls as
in module 04. What holds the electrons in a real metal is the attraction of the positive ions,
which the model's rigid walls stand in for.

:::{figure} ../media/quantum-fermi-sea.mp4
:alt: Two plots. Left, a grey square-root curve of the density of states against energy over the Fermi energy, from 0 to 2.2, with a dashed vertical line at 1. Under it a blue filled region, the occupied states: at first a low hump spreading far past the dashed line; as the temperature falls it rises to fill the grey curve below the dashed line and drops to nothing above it, ending as a sharp step at the Fermi energy. An amber band about the step narrows as it sharpens, and an amber triangle marks the chemical potential, moving onto the dashed line. Right, a log-log plot of heat capacity per particle over k_B against T over T_F: a blue curve levelling off at a dotted line at 3/2 when hot and following a red dashed straight line when cold; an amber dot slides down the blue curve.
:width: 100%

A Fermi gas cooled from $T = T_F$ to $T = 0.01\,T_F$ at fixed density. Left: the density of states
$g(\varepsilon)$ (grey) and the occupied part of it, $g(\varepsilon)\,n_{\mathrm{FD}}(\varepsilon)$
(blue), against $\varepsilon/\varepsilon_F$; the dashed line is the Fermi energy and the amber
triangle the chemical potential. The amber band, $2\kB T$ wide, centred on $\mu$, marks the
electrons that a temperature $T$ can still move: below it every state is full and above it every
state is empty. As the gas cools, the edge hardens into a step at $\varepsilon_F$, $\mu$ climbs to
$\varepsilon_F$, and the band narrows, while the bulk of the sea does not change. Right: the heat
capacity per particle, $C_V/N\kB$, on logarithmic axes, against $T/T_F$ (blue, with the moving
dot): it is the classical $\tfrac32$ when hot (dotted) and follows the straight line
$(\pi^2/2)\,T/T_F$ (red, dashed) when cold.
:::

### Step 8: why a metal's electrons store almost no heat

Heating a Fermi gas by $\mathrm{d}T$ offers every electron an extra energy of order $\kB T$. An
electron deep in the sea cannot accept it: every state within $\kB T$ of its own is already taken.
Only the electrons within about $\kB T$ of the top of the sea have empty states above them to move
into, and they are a fraction of order $T/T_F$ of the whole.

:::{admonition} The electronic heat capacity
:class: approximation
Only the shell about $\kB T$ deep at the top of the Fermi sea can be excited, and each excited
electron takes up of order $\kB T$. So

$$
C_{\mathrm{el}} \sim N\kB\,\frac{T}{T_F} ,
$$

linear in the temperature and smaller than the classical $\tfrac32 N\kB$ by a factor of order
$T/T_F$. The careful calculation (the Sommerfeld expansion, sketched in the advanced section) gives
the coefficient:

$$
C_{\mathrm{el}} = \frac{\pi^2}{2}\, N\kB\,\frac{T}{T_F} \qquad (T \ll T_F) .
$$

Valid while $T \ll T_F$ — for metals, at every temperature below melting.
:::

For copper at room temperature, $T/T_F = 0.0037$: the electrons' heat capacity is $1.2\%$ of the
classical $\tfrac32 N\kB$, and $0.6\%$ of the lattice's $3R$. That is the puzzle's missing heat
capacity. It was never missing: it was frozen out, not by quantization of the energy, as in module
16, but by exclusion.

At low temperature the lattice's contribution falls as $T^3$ (module 16) and the electrons' only as
$T$, so in every metal there is a temperature below which the electrons dominate. Per mole of atoms
with $z$ conduction electrons each,

$$
C = \gamma\, T + \beta\, T^3 , \qquad \gamma = \frac{\pi^2}{2}\,\frac{z R}{T_F} ,
$$

with $\beta$ module 16's Debye coefficient. Plotting $C/T$ against $T^2$ gives a straight line whose
intercept measures the electrons and whose slope measures the lattice. The verification below does
this with real data.

### Step 9: photons, the bosons with μ = 0

Module 16 derived Planck's law from the oscillator, mode by mode. The same result follows from this
module in one line. Photons are bosons, so a mode of frequency $\nu$ holds on average
$n_{\mathrm{BE}}(h\nu)$ of them. But the walls absorb and emit photons freely, so their number is not
conserved: there is no $N$ to hold fixed, and no step 5. As module 16 showed, the free energy is
then lowest at $\mu = 0$.

:::{admonition} Planck's law is the Bose–Einstein distribution at μ = 0
:class: theorem
With $\mu = 0$, a photon mode of frequency $\nu$ holds $n_{\mathrm{BE}} = 1/(e^{h\nu/\kB T} - 1)$
photons of energy $h\nu$. Multiplying by module 16's density of modes per unit volume,

$$
u_\nu = \frac{8\pi\nu^2}{c^3}\cdot h\nu \cdot \frac{1}{e^{h\nu/\kB T} - 1} ,
$$

which is Planck's law. One occupation function serves both chapters.
:::

A photon gas cannot condense, for the same reason it has $\mu = 0$. Condensation needed a fixed
number of particles pressing $\mu$ against its bound; photons that do not fit are simply absorbed
by the walls.

(17-quantum-gases-verify)=
## Verify computationally

Every number below comes from `thermolab.quantum`, which evaluates the occupation integrals by
quadrature and solves for $\mu$ by bisection, with no special functions. Nothing in this module is
random except two checks that sample on purpose. The laboratory repeats each experiment.

**1. The occupations, rebuilt from explicit sums.** Summing a state's grand-canonical weights term
by term — $n$ from $0$ to $4000$ for bosons, with $1/n!$ for classical particles, two terms for
fermions — reproduces the closed forms of step 2 to $4 \times 10^{-16}$ at
$(\varepsilon - \mu)/\kB T = 0.05$, $0.5$, $2$ and $10$, and the variances $n(1 + n)$, $n(1 - n)$
and $n$ to the same precision. Drawing $100\,000$ occupations at random at
$(\varepsilon - \mu)/\kB T = 0.5$ gives a boson mean of $1.539$ and variance $3.89$, against
$1.541$ and $3.92$.

**2. Counting, one state at a time.** Listing every arrangement of two particles in two states
gives $4$, $3$ and $1$. Listing the states of a cube one by one and comparing with step 4's smooth
count: the explicit count falls short by $11.2\%$ at $|\mathbf{n}| = 20$, $2.8\%$ at $80$ and
$0.70\%$ at $320$. The shortfall times $|\mathbf{n}|$ settles at $2.25 = 9/4$: the missing states
on the octant's faces, and nothing else.

**3. The classical corner.** Across $e^{(\varepsilon - \mu)/\kB T}$ from $100$ to $e^{40}$ the boson
and fermion occupations never differ from the classical one by more than $1/99$ and $1/101$, and
below $100$ they are ordered $n_{\mathrm{BE}} > n_{\mathrm{MB}} > n_{\mathrm{FD}}$ everywhere.

**4. The density fixes μ.**

:::{admonition} One occupation function, two chapters
:class: numerical-observation
Module 16's Planck spectrum, rebuilt here as the photon density of modes times $h\nu$ times
`bose_einstein(h nu, 0, T)`, agrees with module 16's `planck_u_nu` to $4 \times 10^{-16}$ — the
last digit of a double — at every frequency from $10^{-3}$ to $30\,\kB T/h$, at $2.725$, $300$ and
$5772\ \mathrm{K}$. The occupation integral at $\mu = 0$, computed by quadrature with no reference to
zeta functions, returns $2.6123753486854877$; $\zeta(3/2)$ is $2.612375348685488$. The quadrature
reaches that precision with $32$ intervals, where a fourth-order rule would need thousands: the
integrand is smooth and even, which makes the trapezoidal rule converge faster than any power of
the step. Neither agreement proves anything that steps 6 and 9 did not; both confirm that the code
and the derivations say the same thing.
:::

The classical solver, which inverts the quadrature and knows nothing of module 13, reproduces
module 13's $\mu = \kB T\ln(n/n_Q)$ to $4 \times 10^{-16}$. And particle number is conserved in the
code: for each statistics, at temperatures from $0.02\,T_F$ to $30\,T_c$, integrating
$g(\varepsilon)\,n(\varepsilon)$ afresh at the solved $\mu$ — on a different grid, with Simpson's
rule — returns the density that was put in, to $10^{-9}$.

**5. Condensation in a real box.** The ideal condensate fraction is a limit. The laboratory also
computes it exactly, for spinless bosons in a hard-walled cube, by summing $n_{\mathrm{BE}}$ over the
box's levels one by one, with no density of states and no integral. At $T = T_c/2$, where the ideal
fraction is $0.646$:

| atoms | $10^3$ | $10^4$ | $10^5$ | $10^6$ |
|---|---|---|---|---|
| $N_0/N$ at $T_c/2$ | $0.782$ | $0.732$ | $0.698$ | $0.676$ |
| $N_0/N$ at $T_c$ | $0.323$ | $0.198$ | $0.116$ | $0.066$ |
| fitted exponent of $1 - N_0/N$ | $1.68$ | $1.61$ | $1.56$ | $1.54$ |

A finite box condenses early, because its hard walls remove the states on the octant's faces and
the excited states fill sooner. The excess shrinks slowly — the fraction at $T_c/2$ exceeds the
ideal by $0.20\,N^{-1/3}\ln N$ to within $10\%$ across the whole table, a surface effect — and the
fitted exponent drifts down toward $\tfrac32$. The ideal theory is the large-$N$ limit of the real
count, approached at the rate a surface correction allows.

**6. The degenerate Fermi gas.** For electrons at copper's density, the numerically solved $\mu$ at
$T = 0.001\,T_F$ is $\varepsilon_F$ to within $10^{-6}$, and the energy per particle and the
pressure exceed $\tfrac35\varepsilon_F$ and $\tfrac25 n\varepsilon_F$ by four parts in a million —
the size of the correction the Sommerfeld expansion predicts. The heat
capacity, obtained from the occupation integrals, is $(\pi^2/2)\,T/T_F$ to $1$ part in $10^{4}$ at
$T = 0.002\,T_F$, still $99.97\%$ of it at $0.01\,T_F$, and falls below the line from about
$0.05\,T_F$, levelling off at $\tfrac32$ above $T_F$.

**7. Against reality: the electrons in silver.** Module 16 fitted silver's measured heat capacity,
tabulated by NIST (Smith and Fickett, 1995), below $6\ \mathrm{K}$ to $C/T = \gamma + \beta T^2$,
and set the electrons' term aside. Here it is the measurement.

:::{figure} ../media/quantum-metals.png
:alt: Two panels for silver. Left, C over T against T squared from 0 to 36 kelvin squared: six black data points on a straight blue line, which meets the vertical axis at 0.651; a red diamond at 0.643 on the axis, the free-electron prediction, sits almost on the intercept. Right, the electrons' share gamma T over C of the measured heat capacity against temperature on a logarithmic axis from 1 to 300 K: 0.8 at 1 K, about one half at 2 K, falling steeply to near zero above 20 K.
:width: 100%

Left: silver's molar heat capacity below $6\ \mathrm{K}$, as $C/T$ against $T^2$ (black points),
with the least-squares line (blue). Its intercept is the electrons' coefficient
$\gamma = 0.651\ \mathrm{mJ\,mol^{-1}\,K^{-2}}$; the red diamond on the axis is the free-electron
prediction, $0.643$, computed from silver's density alone. The slope is the lattice's Debye term.
Right: the electrons' share of the measured heat capacity, $\gamma T/C$, from $1$ to
$300\ \mathrm{K}$: $80\%$ at $1\ \mathrm{K}$, about half at $2\ \mathrm{K}$, and $0.8\%$ at room
temperature.
:::

- **The measurement.** The fit gives $\gamma = 0.651 \pm 0.001\ \mathrm{mJ\,mol^{-1}\,K^{-2}}$
  (statistical; ending the window at $4\ \mathrm{K}$ instead of $6$ gives $0.649$, the systematic
  scale of the number).
- **The prediction.** Silver has one conduction electron per atom; its density,
  $10\,490\ \mathrm{kg\,m^{-3}}$, and molar mass, $107.87\ \mathrm{g\,mol^{-1}}$, give
  $n = 5.86 \times 10^{28}\ \mathrm{m^{-3}}$, $\varepsilon_F = 5.50\ \mathrm{eV}$ and
  $T_F = 63\,800\ \mathrm{K}$, and so $\gamma_{\mathrm{free}} = (\pi^2/2) R/T_F =
  0.643\ \mathrm{mJ\,mol^{-1}\,K^{-2}}$. The measurement is $1.01$ times the prediction.
- **The share.** The electrons carry $80\%$ of silver's heat capacity at $1\ \mathrm{K}$ and half
  of it at $2\ \mathrm{K}$, where $\gamma T = \beta T^3$; at room temperature they carry $0.8\%$ —
  the puzzle's "missing" heat capacity, measured.

Silver is the best case. A metal's electrons feel its lattice, and the ratio of measured to
free-electron $\gamma$, called the thermal effective mass, records how much. With measured values
from Kittel's table (8th edition, p. 139) and free-electron values computed here from each metal's
room-temperature density:

| metal | $z$ | measured $\gamma$ | free-electron $\gamma$ | ratio |
|---|---|---|---|---|
| Ag | 1 | 0.646 | 0.643 | 1.00 |
| Au | 1 | 0.729 | 0.640 | 1.14 |
| Cu | 1 | 0.695 | 0.502 | 1.38 |
| Al | 3 | 1.35 | 0.910 | 1.48 |

(in $\mathrm{mJ\,mol^{-1}\,K^{-2}}$). The free-electron gas gets the size and the linearity right
for all four and the coefficient right to within a factor of $1.5$; the rest is band structure,
which this model ignores by name.

**8. Against reality: liquid helium-4.** Is the superfluid transition of helium a Bose–Einstein
condensation? At the density of liquid helium at its transition, $0.1461\ \mathrm{g\,cm^{-3}}$
(Donnelly and Barenghi, 1998), step 6 gives

$$
T_c = 3.15\ \mathrm{K} ,
$$

against the measured transition, the **lambda point**, at $2.177\ \mathrm{K}$. The ideal gas misses
by $45\%$. It misses in a telling way: it is the right order of magnitude, from nothing but the
mass and the density, and liquid helium is the least ideal gas imaginable. Its atoms sit $0.36\ \mathrm{nm}$ apart, closer than their thermal wavelength of
$0.59\ \mathrm{nm}$ and close enough to repel strongly. London proposed the connection in 1938 from
this very estimate; the modern view is that the superfluid is a condensate, strongly modified by
interactions — neutron scattering finds less than a tenth of the atoms in the zero-momentum state
even at absolute zero, where the ideal gas would put them all. The ideal model locates the
phenomenon; it does not describe the liquid. That is its Failure modes line, measured.

**The falsifying experiments.** Each misconception this module confronts has a measurement above
that it cannot survive. "Quantum effects matter only when it is cold": copper's electrons at room
temperature have $n\lambda^3 = 6800$ and $T/T_F = 0.004$, and silver's measured $\gamma$, set by the
Fermi temperature of $63\,800\ \mathrm{K}$, confirms it — degeneracy is set by $n\lambda^3$, not by
$T$ alone. "Condensation is the atoms stopping": below $T_c$ the excited states hold $N(T/T_c)^{3/2}$
particles and the pressure is $1.341\,\kB T/\lambda^3$, nonzero and independent of how many atoms
are in the condensate (item 5 and step 6). "A Pauli force pushes fermions apart": the degeneracy
pressure of item 6, $3.8 \times 10^{10}\ \mathrm{Pa}$ for copper, comes out of a model whose
Ignored line lists every interaction; it is counting and kinetic energy, not a force.

(17-quantum-gases-transfer)=
## Transfer the idea

One rule — how many identical particles may share a state — split the ideal gas into two gases
with nothing classical about them. It reaches back through the course and out into the world.

- **Back to modules 08 and 12.** The Gibbs $1/N!$, which module 12 justified for a dilute gas only,
  is the common dilute limit of the Bose and Fermi counts (step 1).
- **Back to module 13.** The quantum concentration is derived: $n_Q = g_s/\lambda^3$, and module
  13's $\mu = \kB T\ln(n/n_Q)$ is the dilute limit of $n\lambda^3 = g_s F(\mu/\kB T)$. Module 13's
  one-site argument, applied to every standing wave, is this module's step 2, and its Langmuir site
  occupation is the Fermi–Dirac function.
- **Back to module 16.** Planck's law is the Bose–Einstein distribution at $\mu = 0$ (step 9), and
  the $\gamma T$ that module 16 subtracted from silver's heat capacity is the Fermi sea's (step 8).
  A metal at low temperature is both modules at once: $C = \gamma T + \beta T^3$.
- **Back to module 04.** $P = \tfrac23 U/V$ is module 04's momentum-flux pressure, for any
  statistics. Degeneracy pressure is delivered to the walls exactly as the pressure of air is.
- **Forward to module 18.** Transport in a metal is carried by electrons at the Fermi velocity,
  $1.57 \times 10^6\ \mathrm{m\,s^{-1}}$ in copper, not at the thermal speed of a classical gas:
  the only electrons that can be scattered into a new state are those at the top of the sea.
- **Semiconductors.** The conduction electrons of pure silicon at room temperature number about
  $10^{16}$ per cubic metre, a ten-trillionth of copper's. Their $n\lambda^3$ is tiny, and they
  obey Maxwell–Boltzmann statistics. The same particles are quantum in one material and classical
  in another: density decides.
- **Ultracold atoms.** The first gaseous condensates were made in 1995, of rubidium-87 at about
  $170$ billionths of a kelvin (Cornell and Wieman, Boulder) and of sodium (Ketterle, MIT), work
  recognized by the 2001 Nobel Prize. Those atoms were held in a magnetic trap, roughly a harmonic
  bowl rather than a box; there the density of states grows as $\varepsilon^2$, not
  $\sqrt{\varepsilon}$, and the condensate fraction as $1 - (T/T_c)^3$ — the problem set derives it.
  Since 2013 atoms have also been condensed in uniform, box-shaped traps (Gaunt and colleagues,
  Cambridge), the geometry of this module.
- **Helium-3.** The lighter isotope of helium is a fermion. It does not condense at
  $2\ \mathrm{K}$; it becomes a superfluid only within a few thousandths of a kelvin of absolute
  zero, when its atoms pair up into bosons. The two isotopes of one element are this module's two gases.
- **Stars.** A white dwarf — the core a sun-like star leaves behind — is held up against its own
  gravity by the degeneracy pressure of its electrons; a neutron star by that of its neutrons. The
  advanced section estimates a white dwarf's size.

Looking ahead:

- **Module 18** turns from equilibrium to the fluctuations around it and the transport they drive,
  and uses this module's Fermi velocity for the electrons of a metal.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — three particles, three states.** Three particles share three single-particle
states. How many microstates are there for classical particles, bosons and fermions? If every
microstate is equally likely, how probable is it that all three particles are in the same state?

:::{dropdown} Solution
Classical: $3^3 = 27$. Bosons: $\binom{5}{3} = 10$. Fermions: $\binom{3}{3} = 1$. All three in the
same state: $3$ microstates out of $27$ classically ($\tfrac19$), $3$ out of $10$ for bosons
($\tfrac{3}{10}$), and none for fermions. Bosons are almost three times as likely to be found piled
up as classical particles, with no force between them.
:::

**Worked example 2 — the three occupations, side by side.** A state lies one $\kB T$ above the
chemical potential. What is its mean occupation under each statistics? And at ten $\kB T$?

:::{dropdown} Solution
At $x = 1$: $n_{\mathrm{BE}} = 1/(e - 1) = 0.582$, $n_{\mathrm{MB}} = e^{-1} = 0.368$,
$n_{\mathrm{FD}} = 1/(e + 1) = 0.269$ — very different. At $x = 10$: $4.540 \times 10^{-5}$,
$4.540 \times 10^{-5}$ and $4.540 \times 10^{-5}$ to four figures; they differ in the fifth, by
$e^{-10} = 4.5 \times 10^{-5}$ of themselves.
:::

**Worked example 3 — copper's Fermi sea.** Copper has density $8960\ \mathrm{kg\,m^{-3}}$, molar
mass $63.55\ \mathrm{g\,mol^{-1}}$ and one conduction electron per atom. Find $n$, $\varepsilon_F$,
$T_F$ and the degeneracy pressure.

:::{dropdown} Solution
$n = 8960/0.06355 \times 6.022 \times 10^{23} = 8.49 \times 10^{28}\ \mathrm{m^{-3}}$.
$(3\pi^2 n)^{2/3} = (2.51 \times 10^{30})^{2/3} = 1.85 \times 10^{20}\ \mathrm{m^{-2}}$, and
$\hbar^2/2m = 6.10 \times 10^{-39}\ \mathrm{J\,m^2}$, so $\varepsilon_F = 1.13 \times 10^{-18}\
\mathrm{J} = 7.04\ \mathrm{eV}$ and $T_F = 81\,700\ \mathrm{K}$.
$P = \tfrac25 n\varepsilon_F = 0.4 \times 8.49 \times 10^{28} \times 1.13 \times 10^{-18} =
3.8 \times 10^{10}\ \mathrm{Pa}$.
:::

**Worked example 4 — the electrons' share at room temperature.** Using example 3, find copper's
electronic heat capacity per mole at $300\ \mathrm{K}$ and compare it with Dulong–Petit and with
what a classical electron gas would contribute.

:::{dropdown} Solution
$C_{\mathrm{el}} = (\pi^2/2) R\,T/T_F = 4.935 \times 8.314 \times 300/81\,700 =
0.151\ \mathrm{J\,mol^{-1}\,K^{-1}}$. Dulong–Petit is $3R = 24.9$, so the electrons add $0.6\%$. A
classical electron gas would add $\tfrac32 R = 12.5$, half of Dulong–Petit again — eighty-three
times more than is there.
:::

**Worked example 5 — a condensate of sodium.** A uniform gas of sodium-23 atoms (mass
$3.82 \times 10^{-26}\ \mathrm{kg}$, $g_s = 1$) has density $10^{20}\ \mathrm{m^{-3}}$. Find $T_c$,
and the fraction of the atoms in the condensate at half that temperature.

:::{dropdown} Solution
$\kB T_c = (2\pi\hbar^2/m)(n/2.612)^{2/3}$. With $2\pi\hbar^2/m = 1.83 \times 10^{-42}\
\mathrm{J\,m^2}$ and $(n/2.612)^{2/3} = (3.83 \times 10^{19})^{2/3} = 1.14 \times 10^{13}\
\mathrm{m^{-2}}$, $\kB T_c = 2.08 \times 10^{-29}\ \mathrm{J}$ and $T_c = 1.51\ \mu\mathrm{K}$. At
$T_c/2$, $N_0/N = 1 - 0.5^{3/2} = 0.65$.
:::

**Worked example 6 — the classical criterion.** Compute $n\lambda^3$ for helium gas at
$0\,{}^\circ\mathrm{C}$ and one atmosphere, and for helium gas at its boiling point,
$4.2\ \mathrm{K}$, at one atmosphere. Is either quantum?

:::{dropdown} Solution
$\lambda = h/\sqrt{2\pi m\kB T}$ with $m = 6.65 \times 10^{-27}\ \mathrm{kg}$: $0.0528\ \mathrm{nm}$
at $273\ \mathrm{K}$ and $0.425\ \mathrm{nm}$ at $4.2\ \mathrm{K}$. $n = P/\kB T$:
$2.69 \times 10^{25}$ and $1.75 \times 10^{27}\ \mathrm{m^{-3}}$. So $n\lambda^3 = 4.0 \times 10^{-6}$
and $0.135$. The first is deeply classical; the second is within an order of magnitude of
degeneracy, and the liquid, about eleven times denser, crosses it.
:::

:::{note} Your predictions, revisited
1. **No.** The mean kinetic energy of a Fermi gas tends to $\tfrac35\varepsilon_F$, not zero —
   $4.2\ \mathrm{eV}$ in copper, which a classical gas would need $33\,000\ \mathrm{K}$ to match. The
   lowest states are full, and the rest must go higher. See step 7.
2. **Bosons, then classical, then fermions:** $n_{\mathrm{BE}} > n_{\mathrm{MB}} > n_{\mathrm{FD}}$,
   because the denominators are $e^x - 1 < e^x < e^x + 1$. All three agree within $1\%$ once
   $e^x \ge 100$. See step 3.
3. **Quantum — deeply.** $n\lambda^3 \approx 6800$ and $T/T_F = 0.004$. It is decided by
   $n\lambda^3$, which involves the density and the mass as much as the temperature: helium gas at
   room temperature is classical with $n\lambda^3 = 4 \times 10^{-6}$. See step 5.
4. **Yes, and independently of the amount.** Below $T_c$ the pressure is
   $1.341\, g_s\kB T/\lambda^3$, set by the temperature alone; at $T_c$ it is $51\%$ of the classical
   $n\kB T$. Extra atoms join the condensate, which exerts none. See step 6.
:::

(17-quantum-gases-quiz)=
## Check your understanding

```{include} ../_generated/quiz-17-quantum-gases.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](17-quantum-gases-problems.md).

(17-quantum-gases-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. Why do photons have zero chemical potential, and what does that make Planck's law an instance
   of?
2. Degeneracy pressure is often described as a force that pushes fermions apart. Explain what in
   the model actually produces it, and why "force" is the wrong word.
3. In your own words: what decides whether a gas is classical or quantum? Give one example of a hot
   quantum gas and one of a cold classical one.
4. Why do only the electrons near the Fermi energy contribute to a metal's heat capacity?

(17-quantum-gases-advanced)=
## Advanced: white dwarfs, and the Sommerfeld expansion

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence, or in later modules, depends on this section. It applies
degeneracy pressure to a star, and derives the coefficient $\pi^2/2$ that step 8 quoted.
:::

### A star held up by counting

When a star like the Sun exhausts its fuel, its core contracts until something stops it. The core
is a plasma of carbon and oxygen nuclei and their electrons, and as it is squeezed the electrons'
density rises and their Fermi energy with it, as $n^{2/3}$, faster than gravity can win. The star
settles at the radius where the two balance: a **white dwarf**.

Treat it as a uniform ball of mass $M$ and radius $R$, with $N_e = M/(2m_u)$ electrons (one per two
nucleons, for carbon and oxygen; $m_u$ is the atomic mass unit), cold enough to be degenerate. Its
energy is the electrons' kinetic energy plus the gravitational energy of a uniform sphere:

$$
E(R) = \frac35 N_e\, \varepsilon_F - \frac35\,\frac{G M^2}{R} ,
\qquad
\varepsilon_F = \frac{\hbar^2}{2m_e}\left(\frac{9\pi N_e}{4R^3}\right)^{2/3} .
$$

The first term grows as $1/R^2$ when the star shrinks, the second only as $1/R$, so there is a
minimum. Setting $\mathrm{d}E/\mathrm{d}R = 0$,

$$
R = \frac{\hbar^2}{m_e}\left(\frac{9\pi}{4}\right)^{2/3}\frac{N_e^{5/3}}{G M^2} \propto M^{-1/3} .
$$

:::{admonition} The size of a white dwarf, as an estimate
:class: approximation
For one solar mass this gives $R \approx 7200\ \mathrm{km}$ — the size of the Earth, for an object
as heavy as the Sun, with a mean density of a tonne per cubic centimetre. The uniform density,
zero temperature and nonrelativistic electrons are all approximations. The best-measured white
dwarf, Sirius B, has $1.018$ solar masses and a radius of $5630\ \mathrm{km}$ (Bond and colleagues,
2017); the estimate is $28\%$ too large, the right order of magnitude from the Fermi energy alone.
:::

Two features of the formula are striking. A heavier white dwarf is *smaller*, $R \propto M^{-1/3}$.
And the estimate is close to its own breaking point: at one solar mass the electrons' Fermi
momentum is $0.86\,m_e c$, and relativity cannot be ignored. As the mass grows, the electrons
become fully relativistic, their energy grows as $p$ rather than $p^2$, the kinetic term falls only
as $1/R$ — like gravity — and above a critical mass nothing stops the collapse. Chandrasekhar found
that mass in 1930: about $1.4$ solar masses. No white dwarf heavier than it has ever been found.

### Where π²/2 comes from

Every quantity of a Fermi gas is an integral of the form $\int_0^\infty \phi(\varepsilon)\,
n_{\mathrm{FD}}(\varepsilon)\,\mathrm{d}\varepsilon$. At low temperature $n_{\mathrm{FD}}$ differs
from a step at $\mu$ only within a few $\kB T$, and the difference is odd about $\mu$: as many states
are emptied just below as are filled just above. Integrating by parts turns the integral into an
average of $\Phi(\varepsilon) = \int_0^{\varepsilon}\phi$ over the slope of the edge,
$-\partial n_{\mathrm{FD}}/\partial\varepsilon$: a narrow peak at $\mu$, even about it, of unit
area. Expanding $\Phi$ about $\mu$, the linear term averages to zero and the quadratic one
survives, which gives **Sommerfeld's expansion**:

$$
\int_0^\infty \phi(\varepsilon)\, n_{\mathrm{FD}}(\varepsilon)\,\mathrm{d}\varepsilon
\approx \int_0^{\mu} \phi(\varepsilon)\,\mathrm{d}\varepsilon
+ \frac{\pi^2}{6}\,(\kB T)^2\, \phi'(\mu) .
$$

The $\pi^2/6$ is half the peak's second moment: measured in units of $\kB T$, its mean squared
width is $\pi^2/3$. Apply the expansion twice. With $\phi = g$, holding $N$ fixed gives $\mu = \varepsilon_F\left[1 -
\tfrac{\pi^2}{12}(T/T_F)^2\right]$. With $\phi = \varepsilon g$, and that $\mu$,

$$
U = \frac35 N\varepsilon_F + \frac{\pi^2}{6}\,(\kB T)^2\, g(\varepsilon_F) ,
$$

and since $g(\varepsilon_F) = \tfrac{3N}{2\varepsilon_F}$,

$$
C_{\mathrm{el}} = \frac{\mathrm{d}U}{\mathrm{d}T} = \frac{\pi^2}{3}\,\kB^2 T\, g(\varepsilon_F)
= \frac{\pi^2}{2}\, N\kB\,\frac{T}{T_F} .
$$

The heat capacity measures $g(\varepsilon_F)$, the density of states at the top of the sea — which is
why the measured $\gamma$ of a real metal, divided by the free-electron one, measures how its band
structure changes that density. The laboratory confirms both the $\mu$ and the $C$ to the order the
expansion claims.
