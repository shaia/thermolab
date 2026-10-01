---
title: Chemical potential
short_title: 13 · Chemical potential
module: 13-chemical-potential
objectives:
  - id: OBJ-13-1
    text: Define mu = -T (dS/dN) at fixed U and V, and evaluate it numerically for a model S(U, V, N) — in particular the Sackur–Tetrode gas, whose slope is k_B T ln(n/n_Q).
  - id: OBJ-13-2
    text: Show that mu = (dG/dN) at fixed T and P agrees with the entropic definition, and explain why G = mu N for a one-component system (the Euler relation) while F is not mu N.
  - id: OBJ-13-3
    text: Predict the direction of particle flow from the chemical potentials alone, including cases where the flow runs against the concentration difference or continues between systems with equal energy per particle.
  - id: OBJ-13-4
    text: Derive equal mu, at a common temperature, as the equilibrium condition for particle exchange by maximizing S_total under N_1 + N_2 = const, and show that particles flow from high mu to low mu.
  - id: OBJ-13-5
    text: Use mu = k_B T ln(n/n_Q) + u_ext for the ideal gas to re-derive the barometric formula as a constant-mu condition, and reconcile it with module 11's Boltzmann-factor derivation.
  - id: OBJ-13-6
    text: State the grand-canonical weight P(s) proportional to exp(-(E_s - mu N_s)/(k_B T)) with its hypotheses, and apply it to one adsorption site to obtain the occupation 1/(exp((epsilon - mu)/(k_B T)) + 1) and the Langmuir isotherm.
  - id: OBJ-13-7
    text: Apply mu balance to a toy reaction A <=> B (the law of mass action) and to osmotic equilibrium (van 't Hoff, Pi = n_s k_B T), stating the dilute limit each one needs.
---

# Chemical potential

(13-chemical-potential-puzzle)=
## The puzzle: what do particles flow down?

Heat flows from hot to cold, and stops when the temperatures are equal. A piston moves from high
pressure to low, and stops when the pressures are equal. Particles, you might say, flow from
where they are crowded to where they are sparse, and stop when the densities are equal. Ink
spreads through water that way; so does the smell of coffee through a room.

Now connect two boxes of gas, and make one change: the floor of box B sits higher in energy than
the floor of box A — by gravity, by an electric offset, or because the walls of A attract the
molecules. Nothing else is different.

:::{figure} ../media/chemical-exchange.mp4
:alt: Two boxes side by side, the right one drawn with a raised floor. Dots start crowded in the right box and drift into the left one until the left box is much denser. Two vertical gauges beside the boxes move toward each other and settle at the same level.
:width: 100%

Two boxes of $10^5$ sites each exchange $2000$ particles at temperature $T$; the floor of box B
(right) is raised by $2\,\kB T$. All particles start in B. Each dot stands for $10$ particles. The
two gauges show each box's chemical potential $\mu$ in units of $\kB T$, computed from its current
count. The particles do not spread out evenly: they pile into A until its density is about seven
times B's — and stay there. The gauge for A starts at the bottom of its scale: an empty box's
chemical potential is $-\infty$, because the first particle to enter it brings a great deal of
entropy. The two gauges end level.
:::

The densities end up *unequal*, by a factor of seven, and stay that way for as long as the
simulation runs. Particles are still hopping both ways; the traffic simply balances. Something
has become equal between the two boxes, and it is not the density.

:::{important} The question
Heat flows down a temperature difference. What do particles flow down — and why is it not the
concentration?
:::

The answer is the **chemical potential**, the third slope of module 09's entropy surface, which
has so far appeared only as a symbol. This module makes it concrete: it computes it, measures it
in a simulation, and uses it to explain the atmosphere, adsorption on a surface, a chemical
reaction and osmosis.

(13-chemical-potential-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. Two boxes like the ones above exchange particles, but this time they start with *equal*
   densities. Do particles flow at all? If so, which way?
2. Raise B's floor further, from $2\,\kB T$ to $4\,\kB T$. By roughly what factor does the final
   density ratio change? Try to guess a functional form.
3. Two boxes hold particles with the same energy per particle — no floors, no forces — but one box
   is ten times larger than the other, and they start with equal numbers of particles. Do
   particles flow when the boxes are connected?
4. A bag of sugar solution, whose wall lets water through but not sugar, sits in pure water. Which
   way does the *water* move, and what happens to the bag?

:::{note} Why we ask first
Questions 1 and 3 test whether density or energy per particle is what equalizes; most people
choose one of the two, and both are wrong. Every answer is collected at the end of the module.
:::

(13-chemical-potential-explore)=
## Explore the model

The laboratory runs the simulation above and lets you change everything in it: the floor offset,
the temperature, the number of particles and the sizes of the two boxes. For each run it plots the
count in each box against time and, beside it, the two chemical potentials. It then stacks twelve
boxes into a column to make an atmosphere, and shrinks one box to a few hundred binding sites to
make an adsorbing surface.

:::{figure} ../media/chemical-mu-trace.mp4
:alt: Two stacked panels against simulation steps. Top, the count in box A rises from zero and levels off near 1760 while a dashed curve rises smoothly to the same level. Bottom, the difference of the two chemical potentials starts near minus eight and decays to zero, then jitters about it.
:width: 100%

The run of the first animation, as numbers, against the number of proposed hops in units of the
relaxation time $\tau$ ($3500$ proposals here). Top: the number of particles in box A (blue), with
the average of eight runs (grey dashed) and the exact equilibrium value (horizontal line).
Bottom: the difference $\mu_A - \mu_B$ in units of $\kB T$. It starts at the bottom of the scale —
box A is empty, and an empty box's $\mu$ is $-\infty$ — climbs to zero as the count settles, and then jitters about zero by a few hundredths of $\kB T$ — the size of the
random traffic between the boxes.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** $N$ identical, non-interacting particles distributed over lattice-gas boxes; box $k$ has $M_k$ sites, each holding at most one particle, all at site energy $u_k$. Two boxes for the centrepiece, a stack of layers for the column, a small box of binding sites beside a large one for adsorption.
- **Dynamics:** one particle, chosen at random, proposes a hop to a site chosen at random among all sites. A proposal into an occupied site or into the particle's own box changes nothing; a hop into another box is accepted with the Metropolis probability $\min\!\big(1, e^{-\Delta u/(\kB T)}\big)$.
- **Boundary:** closed to particles as a whole — the total number is conserved exactly at every step. An implicit bath at temperature $T$ supplies or absorbs each hop's energy difference.
- **Ensemble:** canonical for the whole set at fixed $T$ and $N$. Each box separately is approximately grand canonical, with the other boxes as its particle reservoir.
- **Ignored:** interactions between particles beyond single occupancy of a site, hop *rates* (time is counted in proposed hops, not seconds), and any spatial structure inside a box.
- **Valid when:** boxes are large enough for Stirling's approximation, $M_k, N_k \gg 1$; the dilute closed forms need $N_k \ll M_k$ as well, and the ideal-gas formulas need $n \ll n_Q$, the classical regime.
- **Failure modes:** nearly full boxes (the dilute formulas fail, the exact count does not), interacting particles (module 15), and densities approaching the quantum concentration, where quantum statistics take over (module 17).
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 13 — chemical potential](/lite/lab/index.html?path=en/labs/13-chemical-potential.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/13-chemical-potential.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Start the two boxes at equal densities with B's floor raised, and watch which way the first
  particles go.
- Sweep the offset from $0$ to $3\,\kB T$ and plot the logarithm of the final density ratio against
  it.
- Make the boxes different sizes with no offset at all, start them with equal *numbers* of
  particles, and see what equalizes.
- Double the number of particles, then double it again, and watch how much $\mu_A - \mu_B$
  jitters once it has settled.

(13-chemical-potential-derive)=
## Derive the result

**System and boundary.** Two subsystems that can exchange energy and particles with each other
through a fixed, permeable wall, the pair isolated from everything else. Later, one of the two
becomes very large and plays the role of a reservoir.

**Independent variables.** Each subsystem's energy, volume and particle number, $U$, $V$, $N$ —
module 09's variables for the fundamental relation $S(U, V, N)$.

**Sign convention.** The course convention holds,

$$
\mathrm{d}U = \dbar Q + \dbar \Won ,
$$

for a closed system. A system that particles can enter gains a third term, $\mu\,\mathrm{d}N$, the
energy that arrives with the particles; quasistatically $\dbar Q = T\,\mathrm{d}S$ and
$\dbar \Won = -P\,\mathrm{d}V$, which is module 09's
$\mathrm{d}U = T\,\mathrm{d}S - P\,\mathrm{d}V + \mu\,\mathrm{d}N$.

**Route.** Six steps. The chemical potential is recalled from module 09 as a slope of $S$; the
maximum-entropy argument gives the equilibrium condition and the direction of flow; module 10's
potentials give its practical form; the ideal gas gives its value, and with it the barometric
formula a second time. Finally module 11's bath argument is repeated for a bath that exchanges
particles, and the resulting weight is spent on an adsorbing surface, a reaction and a membrane.

Steps 1 to 5 are thermodynamic arguments: they use nothing but the entropy function and its
slopes. Step 6 is statistical: it counts a reservoir's microstates. After the sign convention
above no heat or work appears, so every differential below is exact — an ordinary
$\mathrm{d}$ of a state function.

### Step 1: the chemical potential, as a slope

Module 09 read three quantities off the entropy surface. The first two became the temperature and
the pressure; the third was named and set aside.

:::{admonition} Chemical potential
:class: definition
For a system with fundamental relation $S(U, V, N)$,

$$
\mu = -T \left(\frac{\partial S}{\partial N}\right)_{U,V} .
$$

It is measured in joules per particle (or joules per mole, multiplied by Avogadro's number).
:::

The minus sign and the factor $T$ are there to make $\mu$ look like an energy. Read the
definition as a statement about entropy: $-\mu/T$ is how much entropy one more particle brings,
if it brings no energy and takes up no room. For most systems adding a particle adds microstates,
$\partial S/\partial N > 0$, and $\mu$ is *negative*.

That already rules out the naive reading. $\mu$ is not the energy of a particle, or the energy per
particle: it is a derivative of the *entropy*, and a particle that brings no energy at all can
still change the entropy a great deal.

### Step 2: equal chemical potentials, and which way particles flow

Let subsystems 1 and 2 share a total energy $U$ and a total particle number $N$. By the maximum
postulate of module 09 the pair settles where

$$
S_{\mathrm{tot}} = S_1(U_1, V_1, N_1) + S_2(U - U_1, V_2, N - N_1)
$$

is largest. At the maximum both partial derivatives vanish. The energy derivative gives
$1/T_1 = 1/T_2$, which is module 09's result. The particle derivative gives

$$
\frac{\partial S_{\mathrm{tot}}}{\partial N_1}
= \left(\frac{\partial S_1}{\partial N_1}\right)_{U_1,V_1} - \left(\frac{\partial S_2}{\partial N_2}\right)_{U_2,V_2}
= -\frac{\mu_1}{T_1} + \frac{\mu_2}{T_2} = 0 .
$$

:::{admonition} Equal chemical potentials
:class: theorem
Two systems that can exchange energy and particles are in equilibrium only if

$$
T_1 = T_2
\qquad \text{and} \qquad
\mu_1 = \mu_2 .
$$
:::

Away from equilibrium, the same derivative gives the direction. Let $\mathrm{d}N_1$ particles
move into subsystem 1 at a common temperature $T$:

$$
\mathrm{d}S_{\mathrm{tot}} = \frac{\mu_2 - \mu_1}{T}\,\mathrm{d}N_1 .
$$

The second law demands $\mathrm{d}S_{\mathrm{tot}} > 0$, so $\mathrm{d}N_1 > 0$ exactly when
$\mu_2 > \mu_1$. **Particles flow from high chemical potential to low**, just as energy flows
from high temperature to low. This is module 09's argument, bullet for bullet, with $N$ in place
of $U$.

Nothing in the argument mentions the density. Density matters only through $\mu$, and $\mu$
depends on other things too: the energy a particle has in each box, and how many ways there are
to place it. That is the answer to the puzzle, and step 4 makes it quantitative.

### Step 3: the practical face — mu from the Gibbs free energy

The definition of step 1 holds $U$ and $V$ fixed while adding a particle, which no experiment
does. Module 10 built the potential whose natural variables are the ones a laboratory controls:
the Gibbs free energy $G = U - TS + PV$, with

$$
\mathrm{d}G = -S\,\mathrm{d}T + V\,\mathrm{d}P + \mu\,\mathrm{d}N .
$$

Read off the coefficient of $\mathrm{d}N$:

$$
\mu = \left(\frac{\partial G}{\partial N}\right)_{T,P} .
$$

This is the same $\mu$ as step 1's, not a new quantity with the same name: module 10 obtained
$\mathrm{d}G$ from $\mathrm{d}U = T\,\mathrm{d}S - P\,\mathrm{d}V + \mu\,\mathrm{d}N$, whose
$\mathrm{d}N$ coefficient is, rearranged as
$\mathrm{d}S = \mathrm{d}U/T + (P/T)\,\mathrm{d}V - (\mu/T)\,\mathrm{d}N$, exactly step 1's slope.
A Legendre transform changes which variables are held fixed; it does not change the coefficient of
a variable it leaves alone. The laboratory checks the equality numerically.

Now use extensivity. Module 09 derived the Euler relation $U = TS - PV + \mu N$ from it alone.
Substituting into $G$:

:::{admonition} G is mu times N
:class: theorem
For a system of one component,

$$
G = U - TS + PV = \mu N ,
\qquad
\mu(T, P) = \frac{G}{N} .
$$
:::

The chemical potential of a pure substance is its Gibbs free energy per particle, and it depends
on $T$ and $P$ alone — not on how much substance there is. The Helmholtz free energy does not
share this property: $F = U - TS = \mu N - PV$. The difference is that $G$'s other natural
variables, $T$ and $P$, are both intensive, so $N$ is its only extensive variable; $F$'s natural
variables include the volume, which is extensive too.

### Step 4: the ideal gas, and a floor

Module 09 stated the Sackur–Tetrode entropy of a monatomic ideal gas, and module 12 derived it
from the partition function:

$$
S = N\kB\left[\ln\left(\frac{V}{N}\left(\frac{4\pi m U}{3 N h^2}\right)^{3/2}\right) + \frac52\right] .
$$

Differentiate at fixed $U$ and $V$. The $\tfrac52$ is cancelled exactly by the derivatives of the
two factors of $1/N$ inside the logarithm, and substituting $U = \tfrac32 N\kB T$ afterwards,

$$
\mu = -T\left(\frac{\partial S}{\partial N}\right)_{U,V} = \kB T \ln\left(\frac{N}{V}\left(\frac{h^2}{2\pi m \kB T}\right)^{3/2}\right) .
$$

The combination in the second bracket defines a density.

:::{admonition} Quantum concentration
:class: definition
The quantum concentration of particles of mass $m$ at temperature $T$ is

$$
n_Q = \left(\frac{2\pi m \kB T}{h^2}\right)^{3/2} = \frac{1}{\lambda^3} ,
$$

one particle per cube of module 12's thermal wavelength $\lambda$.
:::

:::{admonition} Why n_Q is the reference density
:class: model-assumption
This module uses $n_Q$ as a name, not as a result. It entered through the Sackur–Tetrode
entropy, which counts states in cells of size $h^3$. Why that counting is right, and what happens
when $n$ approaches $n_Q$, is module 17's subject.
:::

With $n = N/V$, the chemical potential of a classical ideal gas is

$$
\mu = \kB T \ln\frac{n}{n_Q} .
$$

For argon at $300\ \mathrm{K}$ and $1\ \mathrm{bar}$, $n/n_Q = 9.8 \times 10^{-8}$ and
$\mu = -16.1\,\kB T = -0.42\ \mathrm{eV}$. A gas is classical precisely when $n \ll n_Q$, so the
chemical potential of a classical gas is always *negative*, and it rises toward zero as the gas is
compressed toward the quantum concentration. That is the entropic term: the sparser the gas, the
more room each new particle has, and the more entropy it brings.

**A floor.** Now put the gas where each particle has an extra energy $u_{\mathrm{ext}}$ — a height
$z$ in gravity, $u_{\mathrm{ext}} = m g z$; a potential step; a binding site. The total energy is
$U = U_{\mathrm{kin}} + N u_{\mathrm{ext}}$, and the entropy depends only on the kinetic part:
$S(U, V, N) = S_{\mathrm{ST}}(U - N u_{\mathrm{ext}}, V, N)$. Differentiating at fixed $U$ picks up
one extra term, $-u_{\mathrm{ext}}\,\partial S_{\mathrm{ST}}/\partial U = -u_{\mathrm{ext}}/T$, so

$$
\mu = \kB T \ln\frac{n}{n_Q} + u_{\mathrm{ext}} .
$$

The chemical potential has two parts: an **energy** a particle carries, and an **entropic**
part set by the density. Particles flow down the sum.

Apply it to the puzzle. Two boxes at one temperature, floors $u_A$ and $u_B$, reach equilibrium
when $\kB T\ln(n_A/n_Q) + u_A = \kB T\ln(n_B/n_Q) + u_B$:

$$
\frac{n_A}{n_B} = e^{-(u_A - u_B)/(\kB T)} .
$$

With B's floor $2\,\kB T$ higher, $n_A/n_B = e^2 = 7.4$. The box with the lower floor ends up
denser, and the densities stay unequal for good — because the chemical potentials, not the
densities, are what equalize. The same formula holds for the laboratory's lattice-gas boxes, with
the site density in place of $n_Q$, as long as the boxes are far from full.

### Step 5: the barometric formula, a second time

Module 11 derived the density of the atmosphere from the Boltzmann factor: one molecule at height
$z$, with the rest of the air as its bath, is found there with probability proportional to
$e^{-m g z/(\kB T)}$. Now derive it again, with no molecule singled out and no probability.

Slice an isothermal column of air into thin horizontal layers. Neighbouring layers exchange
molecules, so in equilibrium every layer has the same chemical potential. With step 4's
$u_{\mathrm{ext}} = m g z$,

$$
\kB T \ln\frac{n(z)}{n_Q} + m g z = \text{const} ,
$$

and therefore

$$
n(z) = n(0)\, e^{-m g z/(\kB T)} .
$$

:::{admonition} Two derivations, one atmosphere
:class: theorem
In an isothermal column in gravity, the density falls as $n(z) = n(0)\,e^{-m g z/(\kB T)}$. Module
11 derived it from the Boltzmann factor of one molecule in contact with a bath; here it follows
from the chemical potential being the same at every height.
:::

The two routes rest on different hypotheses. Module 11's needs the rest of the atmosphere to act
as a bath for one molecule at a time. This one needs each layer to be an ideal gas in equilibrium
with its neighbours. Both need a single temperature. Their agreement is the first hint of what step
6 shows in general: the chemical potential *is* the Boltzmann factor's bookkeeping, done for
particles instead of energy.

### Step 6: a bath that exchanges particles

Module 11 derived the Boltzmann factor by placing a small system in contact with a large bath and
counting the bath's microstates. Repeat the argument, but let the bath — now a **particle
reservoir** as well as a heat bath — exchange particles with the system too.

The system is in microstate $s$, with energy $E_s$ and $N_s$ particles. The reservoir holds the
rest, $U_0 - E_s$ and $N_0 - N_s$, and the probability of $s$ is proportional to the number of
reservoir microstates, $e^{S_R(U_0 - E_s,\, N_0 - N_s)/\kB}$. The reservoir is large, so expand its
entropy to first order in both small quantities, using its slopes $\partial S_R/\partial U = 1/T$
and $\partial S_R/\partial N = -\mu/T$:

$$
S_R(U_0 - E_s, N_0 - N_s) \approx S_R(U_0, N_0) - \frac{E_s}{T} + \frac{\mu N_s}{T} .
$$

:::{admonition} The grand-canonical weight
:class: theorem
A system that exchanges energy and particles with a reservoir at temperature $T$ and chemical
potential $\mu$ is found in microstate $s$, holding $N_s$ particles at energy $E_s$, with
probability

$$
P(s) \propto e^{-(E_s - \mu N_s)/(\kB T)} ,
$$

provided the reservoir is large enough that the second-order terms of its entropy are negligible,
and the coupling is weak enough that energies and particle numbers simply add.
:::

This is the **grand canonical ensemble**. It is the canonical weight with one more term: each
particle a state holds counts in its favour by $e^{\mu/(\kB T)}$. The normalizing sum over every
state and every particle number is the grand partition function, and its machinery is module 17's.
Here one site is enough.

**One adsorption site.** A site on a surface can be empty — energy $0$, no particle — or hold one
molecule with binding energy $\varepsilon$ (negative for a site that attracts). The gas above is
the reservoir. The two weights are $1$ and $e^{-(\varepsilon - \mu)/(\kB T)}$, and the mean
occupation is

$$
\langle n \rangle = \frac{1}{e^{(\varepsilon - \mu)/(\kB T)} + 1} .
$$

:::{admonition} Independent sites
:class: model-assumption
Each site is filled or empty independently of the others: neighbouring molecules on the surface
do not attract or repel each other, and a site holds at most one molecule.
:::

When $\mu$ is far below $\varepsilon$ the site is almost always empty; when $\mu$ is far above it
the site is almost always full; at $\mu = \varepsilon$ it is filled half the time. The gas sets
$\mu$ through step 4, $e^{\mu/(\kB T)} = n/n_Q = P/(n_Q \kB T)$, and substituting gives the
fraction of the surface covered at pressure $P$:

$$
\theta = \frac{P}{P + P_0} ,
\qquad
P_0 = n_Q \kB T\, e^{\varepsilon/(\kB T)} .
$$

This is the **Langmuir isotherm**: linear in $P$ at low pressure, saturating at full coverage, and
half covered at $P = P_0$. A more strongly binding site, with more negative $\varepsilon$, has a
smaller $P_0$ and fills at lower pressure.

The function $1/(e^{x} + 1)$ will reappear in module 17 as the Fermi–Dirac function, the mean
occupation of a quantum state by electrons. Nothing about the formula will change but its name:
an electron state, too, is a site that holds at most one particle.

**A reaction.** A molecule that can exist in two forms, A and B, with ground energies
$\varepsilon_A$ and $\varepsilon_B$, is a particle that can hop between two "boxes". Converting
one molecule from A to B moves one particle from box A to box B, so equilibrium is $\mu_A = \mu_B$.
With step 4's ideal-gas form for each,
$\kB T\ln(n_A/n_{Q,A}) + \varepsilon_A = \kB T\ln(n_B/n_{Q,B}) + \varepsilon_B$, and

$$
\frac{n_B}{n_A} = \frac{n_{Q,B}}{n_{Q,A}}\, e^{-(\varepsilon_B - \varepsilon_A)/(\kB T)} .
$$

This is the **law of mass action** for the simplest reaction there is. Module 12 reached the same
ratio for two isomers from their partition functions. For a reaction that changes the number of
molecules, say $A + B \rightleftharpoons C$, the condition becomes $\mu_A + \mu_B = \mu_C$, and the
ratio $n_C/(n_A n_B)$ is fixed by the temperature alone: the equilibrium constant.

**A membrane.** A **semipermeable membrane** lets the solvent (water) through but not the solute
(sugar). Only the solvent can move, so only the solvent's chemical potential has to be equal on
the two sides. Adding solute lowers it.

:::{admonition} The ideal solution
:class: model-assumption
Solvent and solute molecules occupy the sites of one lattice at random, and the energy of the
mixture does not depend on how they are arranged. Then only the entropy of mixing changes when
solute is added, and a solvent molecule's chemical potential falls by $-\kB T\ln(1 - x)$, where $x$
is the fraction of the sites held by solute.
:::

The pure solvent side has the higher chemical potential, so water flows *into* the solution. It
stops when the solution side is at a higher pressure, $P + \Pi$, which raises the solvent's
chemical potential by $v\,\Pi$, with $v$ the volume per solvent molecule
($(\partial\mu/\partial P)_T = v$ from step 3's $\mathrm{d}G$). Equal solvent chemical potentials
then require

$$
\Pi\, v = -\kB T \ln(1 - x) .
$$

:::{admonition} The van 't Hoff law
:class: approximation
For a dilute solution, $x \ll 1$, $-\ln(1 - x) \approx x$, and with $n_s = x/v$ the number of
solute molecules per unit volume,

$$
\Pi = n_s \kB T .
$$

The fractional error of stopping at the first term is about $x/2$: $0.09\%$ for a $0.1$-molar sugar
solution, $0.9\%$ for a $1$-molar one — within the ideal-solution model. Real concentrated
solutions depart from the model itself.
:::

The formula is the ideal-gas law with the solute in the role of the gas, and that resemblance has
misled many people into picturing solute molecules pushing on the membrane. They do not: the
solute never crosses it. The pressure is the price of stopping the *solvent* from flowing down its
own chemical-potential difference.

(13-chemical-potential-verify)=
## Verify computationally

Every number below comes from `thermolab.chemical`. The temperature is $300\ \mathrm{K}$ unless
stated, and every energy is quoted in units of $\kB T$.

**1. Three routes to one mu.** For argon at $1\ \mathrm{bar}$, the laboratory computes the chemical
potential three ways: as $-T\,\partial S/\partial N$ by a central difference on the Sackur–Tetrode
$S(U, V, N)$, with $T$ itself read off the same surface; as $\partial G/\partial N$ by a central
difference on module 10's numerically built $G(T, P, N)$; and from the closed form
$\kB T\ln(n/n_Q)$. All three give $\mu = -16.139\,\kB T$; they agree to $3 \times 10^{-9}$ and
$8 \times 10^{-13}$, and $G/N$ matches $\mu$ to $4 \times 10^{-16}$. Refining the step of the
entropic difference by factors of two quarters its error each time: the stencil is second order.

**2. The puzzle, simulated.** Two boxes of $10^5$ sites, $2000$ particles, B's floor raised by
$2\,\kB T$, every particle starting in B. The time constant of the approach is $3500$ proposed
hops, and each run is twenty time constants long.

:::{admonition} Unequal densities, equal chemical potentials
:class: numerical-observation
Averaged over the second half of eight independent runs, box A holds $1755 \pm 2$ particles,
against $1758.4$ for the exact stationary distribution — every possible split counted and weighted
— and $1761.6$ for the dilute formula of step 4. The two boxes' densities differ by a factor of
$7.3$. Their chemical potentials started far apart — after the first twenty proposed hops they were
$-9.6$ and $-1.9\,\kB T$ — and now agree to within
$0.002\,\kB T$ on average.
:::

The dilute formula is off by $0.2\%$ because the boxes are $1.8\%$ full: with single occupancy,
the entropic term is $\kB T\ln[N/(M - N)]$ rather than $\kB T\ln(N/M)$, and the exact count uses
that form. At $1\%$ filling or less the difference is below the simulation's noise.

**3. Against the density difference.** Start the same boxes at *equal* densities, $1000$
particles each. Box A's chemical potential starts at $-4.6\,\kB T$ and B's at $-2.6\,\kB T$, so
particles flow from B into A — from the box that is exactly as crowded into the one that is
exactly as crowded — and keep flowing until A holds $1767$ and B $233$. This is the falsifying
experiment for "particles always flow from high to low concentration".

**4. Against the energy per particle.** No floors at all now: box A has $10^4$ sites, box B
$10^5$, and each starts with $1000$ particles. Every particle has the same energy, zero, in either
box. Yet A starts at $\mu = -2.2\,\kB T$ and B at $-4.6\,\kB T$, and particles flow from A to B
until A holds $178$ (exact: $181.8$) and the two *densities* are equal, $0.018$ in each. With the
energies equal, the entropic term alone decides — which is the falsifying experiment for "the
chemical potential is the energy per particle".

**5. The functional form.** Sweeping B's floor from $0$ to $3\,\kB T$ in steps of $0.5\,\kB T$ and
fitting $\ln(n_A/n_B)$ against the offset gives a slope of $0.996 \pm 0.002$ per $\kB T$:
each extra $\kB T$ of offset multiplies the density ratio by $e$.

**6. How steady is equal mu?** Once settled, $\mu_A - \mu_B$ fluctuates about zero. From the exact
distribution of the split, its standard deviation is $0.31$, $0.098$, $0.031$ and $0.0097\,\kB T$ for
$100$, $10^3$, $10^4$ and $10^5$ particles; the fitted exponent is $-0.502$. Equality of chemical
potentials, like equality of temperatures in module 08, is sharp only for large systems, and
sharpens as $N^{-1/2}$.

:::{figure} ../media/chemical-barometric.mp4
:alt: A tall column of dots, all starting in the bottom layer, spreading upward until they thin out exponentially with height. Beside it, a horizontal bar chart of the count in each layer grows toward a dashed exponential curve, and a vertical line of points shows each layer's chemical potential gathering onto one value.
:width: 100%

An isothermal column of twelve layers of $50\,000$ sites each; each layer sits $0.4\,\kB T$ above
the one below, as a layer of air sits $m g\,\Delta z$ above the one below it. All $2000$ particles
start in the bottom layer. Left: the particles, each dot standing for five. Middle: the count in
each layer (bars) and the exponential $n(z) \propto e^{-m g z/(\kB T)}$ (dashed). Right: each
layer's chemical potential in units of $\kB T$ (dots). They start far apart — a layer that is
still empty sits pinned at the left edge — and gather onto one vertical line.
:::

**7. The column.** Averaged over the second half of four runs, the fitted decay of $\ln n$ with
layer number is $-0.398 \pm 0.001$ per layer, against the $-0.4$ of the barometric formula; the
remaining half percent is single occupancy again, since the bottom layer is $1.3\%$ full. The
twelve layers' chemical potentials agree to within $0.03\,\kB T$. A column that knows nothing but
"hop, and accept by Metropolis" settles into the exponential atmosphere, with the chemical
potential constant up its height.

**8. The adsorption site.** A surface of $200$ binding sites at $\varepsilon = -3\,\kB T$ exchanges
particles with a reservoir of $20\,000$ sites at energy $0$. Changing the total number of particles
changes the reservoir's chemical potential; the laboratory measures the fraction of the surface
covered.

:::{figure} ../media/chemical-adsorption.png
:alt: Left, a sigmoid curve of occupation from zero to one against the chemical potential, with blue simulated points lying on it and a dotted vertical line at the half-filled point. Right, coverage against pressure rising steeply then flattening toward one, with the same points.
:width: 100%

(a) Fraction of surface sites occupied against the reservoir's chemical potential, relative to
the binding energy, $(\mu - \varepsilon)/\kB T$. The black curve is the one-site grand-canonical
result $1/(e^{(\varepsilon - \mu)/\kB T} + 1)$; the blue points are simulated, each the average
of the second half of one run, at eight particle numbers. (b) The same points against
$e^{(\mu - \varepsilon)/\kB T}$, which for a dilute gas is its pressure in units of $P_0$ — the
Langmuir isotherm $\theta = P/(P + P_0)$. The reservoir here is up to $11\%$ full, where its
density and $e^{\mu/\kB T}$ differ by more than a tenth; that is why the axis is not the density.
:::

| particles in total | $20$ | $150$ | $600$ | $1000$ | $2400$ |
|---|---|---|---|---|---|
| common $\mu$ ($\kB T$) | $-7.09$ | $-5.05$ | $-3.61$ | $-3.05$ | $-2.06$ |
| exact coverage | $0.0165$ | $0.1140$ | $0.3533$ | $0.4871$ | $0.7187$ |
| $1/(e^{(\varepsilon - \mu)/\kB T} + 1)$ | $0.0165$ | $0.1139$ | $0.3532$ | $0.4870$ | $0.7186$ |
| simulated | $0.0165$ | $0.109$ | $0.369$ | $0.474$ | $0.734$ |

The exact coverage counts every way of sharing the particles between surface and reservoir. The
formula needs only one number, the chemical potential that the two share, and reproduces it to
$10^{-4}$. The surface does not know how big the reservoir is, or how many particles are in it.
It responds only to $\mu$. The simulated coverages scatter about both by a few hundredths — two
hundred sites, each full or empty, averaged over a finite run.

**9. Osmosis.** For sucrose in water at $298\ \mathrm{K}$, with the ideal-solution model:

| concentration (mol/L) | $0.01$ | $0.1$ | $0.5$ | $1.0$ |
|---|---|---|---|---|
| van 't Hoff $\Pi$ (MPa) | $0.0248$ | $0.248$ | $1.239$ | $2.479$ |
| $-(\kB T/v)\ln(1 - x)$ (MPa) | $0.0248$ | $0.248$ | $1.245$ | $2.502$ |
| difference | $0.009\%$ | $0.09\%$ | $0.45\%$ | $0.91\%$ |

A $0.1$-molar solution — $34\ \mathrm{g}$ of sugar in a litre of water — has an osmotic pressure of $2.5\ \mathrm{bar}$, enough to hold up a column of water $25\ \mathrm{m}$ tall.

**The falsifying experiment for osmosis.** Which way something crosses a membrane can be
weighed. Dissolve the shell of a raw egg in vinegar, leaving the egg inside its own membrane,
which passes water far more readily than sugar. Left overnight in pure water, it swells and
gains mass. Left in concentrated sugar syrup instead, it shrivels and loses mass. If osmosis were
sugar pushed through the membrane, the egg in syrup would take up sugar and swell; it does the
opposite. What crosses is the water, moving toward the side where its chemical potential is
lower — into the egg from pure water, out of the egg into the syrup.

**10. A measurement.** The laboratory generates synthetic readings of $\Pi$ at six concentrations,
with a $3\%$ random error on each, standing in for a class's dialysis-tubing experiment. Fitting
$\Pi$ against the molar concentration gives a slope of $2560 \pm 47\ \mathrm{J\,mol^{-1}}$, against
$RT = 2479\ \mathrm{J\,mol^{-1}}$ at $298\ \mathrm{K}$: van 't Hoff's law turned around, an
estimate of the gas constant from sugar water, within two standard errors.

:::{admonition} What the simulations do not prove
:class: open-question
The lattice gas settles exactly where equal chemical potentials say it will — but it was built to
have an entropy $\kB\ln\binom{M}{N}$ and a Metropolis rule that respects it, so its agreement
confirms the arithmetic, not the model. Whether a real surface's sites are independent, or a real
sugar solution is ideal, is a question for experiment, and for both the answer is "only when
dilute": concentrated sucrose solutions have osmotic pressures measurably above van 't Hoff's —
by more than the ideal-solution correction in the table — because each sucrose molecule binds
several water molecules, an energy of mixing that the ideal-solution model leaves out.
:::

(13-chemical-potential-transfer)=
## Transfer the idea

Wherever particles — molecules, electrons, defects, photons — can move between two places or two
forms, equilibrium is equal chemical potential.

- **Phase coexistence.** Water and its vapour in a closed flask exchange molecules. They coexist
  when $\mu_{\mathrm{liquid}}(T, P) = \mu_{\mathrm{vapour}}(T, P)$ — two "boxes" that happen to be
  two phases of one substance. That single condition gives the boiling curve, and it is module 14's
  first equation.
- **The Fermi–Dirac function.** Step 6's site occupation, $1/(e^{(\varepsilon - \mu)/\kB T} + 1)$,
  is the occupation of an electron state in a metal, with the electrons' own chemical potential.
  Module 17 derives it for every quantum state and explains why the chemical potential of an
  electron gas is *positive*: for electrons in copper at room temperature $n/n_Q \approx 7000$,
  far outside the classical regime where $\mu < 0$.
- **The entropy of mixing.** Module 08 promised a quantitative account of mixing and of the Gibbs
  paradox. Step 6's ideal solution is that account: mixing two *different* species changes each
  one's chemical potential by $\kB T\ln x$ and produces the entropy $-\kB\sum N_i\ln x_i$; "mixing"
  two samples of the *same* gas changes no chemical potential, and produces none.
- **Semiconductors.** Electrons and holes in silicon are created in pairs and destroyed in pairs.
  Treating the reaction $\text{electron} + \text{hole} \rightleftharpoons \text{nothing}$ with the
  law of mass action gives $n_e n_h = n_i^2$, a constant fixed by temperature alone: doping that
  raises one carrier's density lowers the other's in proportion.
- **Defects in crystals.** A vacancy is a "particle" that can be created at the surface and moved
  into the bulk; equal chemical potential for vacancies gives module 11's
  $e^{-E_{\mathrm{v}}/(\kB T)}$ as a mass-action result.
- **Living cells.** A red blood cell in pure water swells and bursts; in concentrated salt water
  it shrivels. The osmotic pressure of blood, about $0.3$ moles of dissolved particles per litre
  at $310\ \mathrm{K}$, is $7.7\ \mathrm{bar}$ — which is why intravenous fluids are made to match it.
- **Reverse osmosis.** Seawater's dissolved ions give it an osmotic pressure near $27\ \mathrm{bar}$.
  Push harder than that on the seawater side of a membrane, and the solvent's chemical potential
  there rises above that of fresh water: water flows *out* of the brine. Desalination plants run
  at $50$ to $80\ \mathrm{bar}$.

Looking ahead:

- **Module 14** applies equal chemical potential between phases, and derives the
  Clausius–Clapeyron equation from it.
- **Module 17** normalizes the grand-canonical weight over every state and every particle number,
  derives $n_Q$, and follows $\mu(T)$ of quantum gases toward zero and beyond.
- **Module 18** asks how *fast* particles flow down a chemical-potential difference; this module
  has only said where they end up.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — the chemical potential of air.** Find $n_Q$ and $\mu$ for nitrogen
($m = 28\ \mathrm{u}$) at $300\ \mathrm{K}$ and $1\ \mathrm{bar}$.

:::{dropdown} Solution
$n = P/(\kB T) = 2.41 \times 10^{25}\ \mathrm{m^{-3}}$. With
$m = 28 \times 1.661 \times 10^{-27}\ \mathrm{kg}$,

$$
n_Q = \left(\frac{2\pi m \kB T}{h^2}\right)^{3/2} = 1.45 \times 10^{32}\ \mathrm{m^{-3}} ,
$$

so $n/n_Q = 1.67 \times 10^{-7}$ and $\mu = \kB T\ln(1.67 \times 10^{-7}) = -15.6\,\kB T = -0.40\ \mathrm{eV}$.
Air is six million times more dilute than the quantum concentration: deeply classical.
:::

**Worked example 2 — two boxes, one offset.** Box B's floor is $1.5\,\kB T$ above box A's; the boxes
are the same size and hold $1000$ particles between them, dilutely. How many end up in A?

:::{dropdown} Solution
$n_A/n_B = e^{1.5} = 4.48$, and with equal volumes $N_A/N_B = 4.48$ too. So
$N_A = 1000 \times 4.48/5.48 = 818$, and $N_B = 182$.
:::

**Worked example 3 — a mountain.** Using constant chemical potential, find the ratio of the
nitrogen density at the top of a $5\ \mathrm{km}$ mountain to that at sea level, for an isothermal
atmosphere at $288\ \mathrm{K}$.

:::{dropdown} Solution
$\kB T\ln n(z) + m g z$ is the same at both heights, so
$n(5\ \mathrm{km})/n(0) = e^{-m g z/(\kB T)}$. The scale height is
$\kB T/(m g) = 8.72\ \mathrm{km}$, so the ratio is $e^{-5/8.72} = 0.56$. The real atmosphere is
colder at altitude and the true ratio is somewhat different — the isothermal column is a model.
:::

**Worked example 4 — a site at its half-filling point.** A surface site binds a molecule with
$\varepsilon = -0.1\ \mathrm{eV}$, at $300\ \mathrm{K}$ ($\kB T = 0.0259\ \mathrm{eV}$). What
fraction of the time is it occupied when the gas has $\mu = -0.15\ \mathrm{eV}$? When
$\mu = -0.05\ \mathrm{eV}$?

:::{dropdown} Solution
$(\varepsilon - \mu)/\kB T = 0.05/0.0259 = 1.93$ in the first case, so
$\langle n \rangle = 1/(e^{1.93} + 1) = 0.127$. In the second it is $-1.93$, and
$\langle n \rangle = 1/(e^{-1.93} + 1) = 0.873$. The two answers add to one: the function is
symmetric about $\mu = \varepsilon$.
:::

**Worked example 5 — a reaction.** Molecules convert between forms A and B, with B higher by
$\Delta\varepsilon = 2\,\kB T$ and equal quantum concentrations. What fraction is B? What if B's
$n_Q$ is three times A's — for instance, because B has three internal states of the same energy?

:::{dropdown} Solution
$n_B/n_A = e^{-2} = 0.135$, so a fraction $0.135/1.135 = 0.119$ is B. With the factor three,
$n_B/n_A = 3e^{-2} = 0.406$, and B's share rises to $0.289$. Entropy — more ways of being B —
partly offsets energy.
:::

**Worked example 6 — how tall a column?** A bag of $0.1$-molar sugar solution is closed by a
membrane at the bottom of a tube and dipped in pure water at $298\ \mathrm{K}$. How high does the
solution rise in the tube?

:::{dropdown} Solution
$\Pi = n_s\kB T = (0.1 \times 10^3 \times 6.022 \times 10^{23}) \times (1.381 \times 10^{-23} \times 298) = 2.48 \times 10^5\ \mathrm{Pa}$.
The column stops rising when its hydrostatic pressure $\rho g h$ equals $\Pi$, so
$h = 2.48 \times 10^5/(1000 \times 9.81) = 25\ \mathrm{m}$ — ignoring the dilution caused by the
water that flows in, which lowers it in practice.
:::

:::{note} Your predictions, revisited
1. **Yes — from B into A.** At equal densities A's chemical potential is lower, because its floor
   is lower, and particles flow down $\mu$ until A is about seven times denser. See
   [the simulation](#13-chemical-potential-verify), item 3.
2. **By a factor of about $e^2 = 7.4$.** The ratio is $e^{\Delta u/\kB T}$: each extra $\kB T$
   multiplies it by $e$, so going from $2$ to $4\,\kB T$ takes it from $7.4$ to $55$.
3. **Yes.** With equal energies the entropic term decides: the small box is more crowded per site,
   its $\mu$ is higher, and particles flow out of it until the *densities* match. Equal energy
   per particle is not equilibrium.
4. **Water flows in, and the bag swells.** The solute lowers the water's chemical potential inside
   the bag; the water flows toward the lower value. The sugar does not cross at all.
:::

(13-chemical-potential-quiz)=
## Check your understanding

```{include} ../_generated/quiz-13-chemical-potential.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](13-chemical-potential-problems.md).

(13-chemical-potential-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. A chemist friend says that particles can only move from high to low concentration unless
   something pumps them. Explain why two connected boxes can hold particles at a seven-to-one
   density ratio with no pump at all.
2. Why is the chemical potential of a classical ideal gas negative? What would it signal if a
   gas's $\mu$ approached zero?
3. What does $\mu = (\partial G/\partial N)_{T,P}$ have to do with $\mu = -T(\partial S/\partial N)_{U,V}$?
   Why is $G = \mu N$ but $F \neq \mu N$?
4. In osmosis, what flows, what does not, and what is the osmotic pressure the price of?

(13-chemical-potential-advanced)=
## Advanced: fugacity, activity, and why mu is not a free variable

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It names two quantities that chemists and
engineers use in place of the chemical potential, and re-reads module 09's Gibbs–Duhem relation as
a statement about $\mu$.
:::

**Fugacity.** Step 4's ideal gas has $\mu = \kB T\ln(n/n_Q)$, or, per mole and in terms of the
pressure, $\mu = \mu^{\circ}(T) + RT\ln(P/P^{\circ})$, with $P^{\circ}$ a chosen reference
pressure. A real gas does not obey this. Rather than give up the convenient logarithm, chemical
engineers keep it and define a corrected pressure $f$, the **fugacity**, so that
$\mu = \mu^{\circ}(T) + RT\ln(f/P^{\circ})$ holds exactly. For a dilute gas $f \to P$. Fugacity is
therefore bookkeeping for $e^{\mu/RT}$ in the units of a pressure, and equal chemical potentials
become equal fugacities — which is how phase equilibria are tabulated in practice.

**Activity.** The same device applied to a solution: the **activity** $a$ of a component is
defined by $\mu = \mu^{\circ} + RT\ln a$. In step 6's ideal solution the solvent's activity is its
fraction, $a = 1 - x$. Real solutions have activity coefficients $\gamma = a/x$ that differ from
one, and measuring them — often by osmotic pressure — is how the departure from the ideal model is
quantified. The sucrose example at the end of the verification is exactly such a departure.

**Gibbs–Duhem, re-read.** Module 09 derived

$$
S\,\mathrm{d}T - V\,\mathrm{d}P + N\,\mathrm{d}\mu = 0
$$

from extensivity. For one component it says that $T$, $P$ and $\mu$ cannot be varied
independently: fix the temperature and the pressure, and the chemical potential is fixed too,
with $\mathrm{d}\mu = -s\,\mathrm{d}T + v\,\mathrm{d}P$ per particle. That is step 3's
$\mu = \mu(T, P)$ again, now with its derivatives: $(\partial\mu/\partial P)_T = v$ is the step
the osmotic derivation used. For a mixture of $r$ components the relation leaves $r + 1$
independent intensive variables, and counting them across coexisting phases gives module 14's
phase rule.

:::{admonition} What is still open here
:class: open-question
Chemical potentials are defined only up to a common constant — only differences between them
can be measured — and yet tables list absolute values of $\mu^{\circ}$ for thousands of
substances. Those values rest on conventions: a chosen reference state for each element, and, for
the entropy's constant, the third law. How those conventions are chosen, and how they are kept
consistent across chemistry, is outside this course.
:::
