---
title: The fundamental relation
short_title: 09 · Fundamental relation
module: 09-fundamental-relation
objectives:
  - id: OBJ-09-1
    text: State the entropy postulates (S extensive and additive, increasing in U, concave, maximized over unconstrained variables at equilibrium), classify them as model assumptions, and explain how 07's Clausius construction and 08's kB ln Omega each satisfy them.
  - id: OBJ-09-2
    text: Define temperature, pressure, and chemical potential as slopes of the entropy surface — 1/T = dS/dU at fixed V,N; P/T = dS/dV at fixed U,N; -mu/T = dS/dN at fixed U,V — and extract them numerically from a tabulated S(U,V,N).
  - id: OBJ-09-3
    text: Derive the equal-slope equilibrium conditions by maximizing S_total under U_1 + U_2 = const (and the V and N versions), predict flow directions from slope inequalities, and explain why temperatures equalize while energies generally do not.
  - id: OBJ-09-4
    text: Derive the Euler relation U = T S - P V + mu N from extensivity alone, and the Gibbs-Duhem relation S dT - V dP + N dmu = 0 from it.
  - id: OBJ-09-5
    text: Connect concavity of S to stability — C_V >= 0 and kappa_T >= 0 — and describe the runaway a convex patch would permit.
  - id: OBJ-09-6
    text: Compute entropy production for finite-Delta-T contact, Delta S_total = C_A ln(T_eq/T_A0) + C_B ln(T_eq/T_B0) > 0, and for free expansion, Delta S = N kB ln(V2/V1); distinguish entropy that flows from entropy that is produced.
  - id: OBJ-09-7
    text: Use the Einstein-solid S(U,n) to predict the equilibrium energy partition of unequal solids, verify it against module 01's exchange simulation via the entropy ledger, and state what the ledger's monotone rise does and does not prove.
---

# The fundamental relation

(09-fundamental-relation-puzzle)=
## The puzzle: why temperatures, and not energies?

Drop a hot pebble into a cold lake. A minute later the pebble is at the lake's temperature,
and it holds a vanishing share of the energy — the lake holds essentially all of it. Put two
identical blocks together, one hot and one cold, and they end at the same temperature *and*
with the same energy. Put a big block and a small one together, and they end at the same
temperature again, with energies that are not remotely equal.

Module 01 watched this happen quantum by quantum and wrote down where it stops. What it never
said is *why it stops there*. Nothing microscopic forbids the flow from carrying on past equal
temperatures. Quanta keep hopping in both directions for ever afterwards; each hop conserves
energy exactly; a state with more energy in the pebble is just as legal as the one the pebble
settles in.

:::{important} The question
Two bodies in contact, one huge and one tiny. Once their temperatures match, nothing stops
energy from flowing further. So what, exactly, is being maximised when the flow stops there —
and not at equal energies?
:::

This module answers it, and the answer turns out to be much larger than the question. There is
a single function of a system's state, its entropy written as $S(U, V, N)$. Its *slopes* are the
temperature, the pressure and the chemical potential. Its *maximum* under a constraint is the
equilibrium state. Its *curvature* decides whether that equilibrium is stable. And the one
property of being extensive forces two exact relations among everything else. Hand over
$S(U, V, N)$, and every property of the system follows from it.

(09-fundamental-relation-predict)=
## Predict before you calculate

Commit to an answer for each of these *before* reading on. Write them down.

1. A hot $2\ \mathrm{kg}$ block of copper is pressed against a cold $0.2\ \mathrm{kg}$ block of
   copper, and the pair is wrapped in insulation. When they stop changing, do they have equal
   energies, equal temperatures, both, or neither?
2. Module 01's simulation moves one quantum per step between two solids. Track their *total*
   entropy step by step as they relax. Can it ever tick down, even for a single step?
3. A gas doubles its volume by leaking into an empty chamber through a pinhole, with no heat
   exchanged and no work done. Does its entropy rise, fall, or stay fixed?
4. Suppose some substance had an entropy $S(U)$ that bulged the wrong way — curving upwards over
   some range of energy. Put two identical pieces of it in contact at the same temperature. What
   happens?

:::{note} Why we ask first
Question 1 is the one this module exists to settle, and many people answer "equal energies"
without noticing they have chosen. Question 2 is where the second law's statistical character
shows its face. Question 3 was left open by module 06 and answered in module 07; here it gets a
third, independent answer. Question 4 sounds abstract and describes every star in the sky.
Every answer is collected at the end of the module.
:::

(09-fundamental-relation-explore)=
## Explore the model

The laboratory's centrepiece is a composite: two subsystems inside one isolated box, separated
by an internal wall. The totals of energy, volume and particle number are fixed. The wall
decides which of them may be *redistributed*: a wall that conducts heat lets energy move, a wall
that slides like a piston lets volume move, and a wall with holes in it lets particles move.
The explorer asks one question over and over: of all the redistributions the wall now permits,
which one has the largest total entropy?

Here is the simplest version, two Einstein solids — module 01's model — with a wall that
conducts heat.

:::{figure} ../media/fundamental-partition-sweep.mp4
:alt: Above, the total entropy of two solids plotted against the energy held by the first solid, with a single peak. Below, the two solids' entropy slopes, one falling and one rising, crossing exactly beneath the peak. A dot sweeps back and forth along both.
:width: 100%

Two Einstein solids share a fixed total energy; the horizontal axis is the fraction of it that
solid A holds. Above: their total entropy, measured from its largest value, which peaks once.
Below: the slope of each solid's own entropy — the red one for A, the blue one for B — which is
each solid's $1/T$. A's slope falls as A takes more energy and warms, and B's rises as B is left
with less and cools. The dots sweep across the partitions, and the dotted segment is the gap
between the two slopes. Wherever the gap is open the total is still climbing toward the peak;
directly beneath the peak, and only there, the gap closes. Solid B is ten times the size of A,
and the peak sits at one-eleventh of the energy in A — not at half.
:::

The second picture is a gas in a box divided by a wall, and it releases the constraints one at
a time.

:::{figure} ../media/fundamental-constraint-release.mp4
:alt: A contour map of total entropy over the energy share and volume share of the left half of a divided gas. A dot starts at an off-peak point, moves horizontally to a ridge when the wall starts to conduct heat, then climbs to the summit when the wall is also freed to move.
:width: 90%

Contours of the total entropy of a divided monatomic gas, over the share of the energy and the
share of the volume on side A; brighter is higher. The dot starts where the gas was prepared,
off the summit. First the wall is made to conduct heat: only the energy share can move, so the
dot travels horizontally, and it stops where the temperatures agree — the dashed line. Then the
wall is also freed to slide: the dot climbs along that line to the summit, where the pressures
agree too. Punching holes in the wall after that moves nothing at all, for a reason the
derivation gives.
:::

And the third runs module 01's simulation again, this time keeping the entropy books.

:::{figure} ../media/fundamental-ledger.mp4
:alt: Two panels. Above, the temperatures of two solids converging over time. Below, the total entropy of the pair rising from zero and levelling off at a dashed ceiling at the same time as the temperatures meet.
:width: 100%

Above: module 01's two solids relaxing to a shared temperature, quantum by quantum. Below: the
pair's total entropy, counted exactly from the number of microstates of each solid at every
step, minus its starting value. It rises while the temperatures converge and flattens exactly
when they meet, just under the dashed line — the largest total entropy any partition of this
energy has. Nothing in the simulation knows about entropy; it only moves quanta at random.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** a fundamental relation $S(U, V, N)$ taken as the complete thermodynamic description of a system; concretely the Einstein solid's $S(U, n)$ and the monatomic ideal gas's Sackur–Tetrode $S(U, V, N)$, alone or as the two halves of a composite separated by an internal wall.
- **Dynamics:** none — the surface is static; "what happens" when a constraint is released is the maximisation of the composite's total entropy over the partitions the wall now permits. Module 01's exchange simulation supplies one dynamics that gets there.
- **Boundary:** the composite is isolated; the internal wall's character — adiabatic or diathermal, fixed or movable, impermeable or perforated — is the constraint being released.
- **Ensemble:** equilibrium thermodynamics — every point on the surface is an equilibrium state, and the maximum postulate stands in for any relaxation dynamics.
- **Ignored:** fluctuations about the maximum (relative size $N^{-1/2}$, module 08), surface and interface terms, and long-range forces, which would break extensivity.
- **Valid when:** each subsystem is macroscopic enough that $S$ is smooth and extensive; the Einstein form in the regime where Stirling's approximation holds; Sackur–Tetrode in the dilute classical regime.
- **Failure modes:** small systems, where $\ln N$ corrections spoil extensivity; low temperature, where the Sackur–Tetrode entropy falls without limit — unphysical, and repaired only by quantum statistics in module 17; and convex patches of the surface, which mark phase coexistence (module 14) or long-range forces.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 09 — the fundamental relation](/lite/lab/index.html?path=en/labs/09-fundamental-relation.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/09-fundamental-relation.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Make solid B ten times the size of solid A and find the peak of the total entropy. Read off
  the two temperatures there, and then the two energies.
- Start the partition far from the peak and let module 01's simulation run. Watch the entropy
  ledger climb. Then zoom in and look for a step where it goes *down*.
- Release the gas's constraints in the other order: holes in the wall first, piston second.
  Does the final state care?
- Put two identical "stars" — the convex relation — in contact and look for the peak of their
  total entropy at the even split. There is a valley there instead.

(09-fundamental-relation-derive)=
## Derive the result

**System and boundary.** A single system described by its energy $U$, volume $V$ and particle
number $N$, and, for most of the argument, a composite of two such systems inside one isolated
box, separated by an internal wall.

**Independent variables and constraint.** $U$, $V$ and $N$ of each subsystem. Isolation fixes
the three totals; the wall decides which of them may be shared out differently between the two
sides.

**Sign convention.** The course convention holds throughout,

$$
\mathrm{d}U = \dbar Q + \dbar \Won ,
$$

with $\dbar Q$ positive into the system and $\dbar \Won$ the work done *on* it.

**Route.** Eight steps, each using only the ones before it. First the four properties an entropy
function must have, and where modules 07 and 08 already established them. Then its slopes, which
turn out to be the temperature, pressure and chemical potential. Then the central result, that
equilibrium is where those slopes match; then a worked fundamental relation, the Einstein
solid's, which settles the puzzle. Then two exact identities that extensivity alone forces; then
why the surface must curve downwards; and finally how much entropy an irreversible process
produces.

### Step 1: what an entropy function has to do

Modules 07 and 08 built entropy twice, from opposite ends. Module 07 defined it by heat,

$$
\Delta S = \int_a^b \frac{\dbar Q_{\text{rev}}}{T} ,
$$

along any reversible path, and proved that the integral depends only on the endpoints.
Module 08 defined it by counting, $S = \kB \ln \Omega$, and proved that the logarithm is forced
by additivity. This module stops asking where entropy comes from and asks what it *does*. From
here on we take four of its properties as the starting point.

:::{admonition} The entropy postulates
:class: model-assumption
For every system in equilibrium there is a function $S(U, V, N)$ of its energy, volume and
particle number, with these properties:

1. **Additive and extensive.** The entropy of a composite is the sum of its parts' entropies,
   and scaling a system scales its entropy: a system twice the size, in every extensive
   variable, has twice the entropy.
2. **Increasing in energy.** At fixed $V$ and $N$, adding energy raises $S$.
3. **Concave.** The surface $S(U, V, N)$ curves downwards, or is flat, in every direction.
4. **Maximised.** When an internal constraint is removed from an isolated composite, the
   extensive variables it had held fixed settle at the values that maximise the total entropy.
:::

These are postulates in the sense that everything below is derived from them and nothing below
derives them. But they are not guesses. Each has already been met in this course.

- **Additivity** is module 08's theorem: independent subsystems have multiplicities that
  multiply, and the logarithm turns the product into a sum. Module 07's Clausius entropy is
  additive too, because heat flowing into a composite is the sum of the heat flowing into its
  parts.
- **Increasing in energy** is the statement, in module 07's language, that temperature is
  positive: adding heat reversibly at fixed volume raises $S$ by $\dbar Q_{\text{rev}}/T$.
- **Maximisation** is module 08's peak, read the other way round. There the even split won not
  because anything forbade the corner but because it had overwhelmingly more microstates; the
  macrostate with the largest $\Omega$ is the one with the largest $S$. Module 07 reached the
  same place from the other side: an isolated system's entropy can only rise.
- **Concavity** is the one that is new, and step 7 shows it is the condition for a
  system to be *stable*.

Extensivity deserves a warning. Module 08 measured that $\kB \ln \Omega$ is extensive only in the
limit of large $N$, with corrections of order $\ln N$ that never vanish exactly. The postulate
takes the limit as given. It is excellent for a gram of anything and wrong for a nanoparticle,
and it fails outright for a star — step 7 comes back to that.

### Step 2: the slopes of the surface are the intensive variables

Write the change in $S$ between two neighbouring equilibrium states as

$$
\mathrm{d}S =
\left(\frac{\partial S}{\partial U}\right)_{V,N} \mathrm{d}U
+ \left(\frac{\partial S}{\partial V}\right)_{U,N} \mathrm{d}V
+ \left(\frac{\partial S}{\partial N}\right)_{U,V} \mathrm{d}N .
$$

The three partial derivatives are properties of the state, like $S$ itself. Give them names.

:::{admonition} Temperature, pressure and chemical potential, as slopes
:class: definition
$$
\frac{1}{T} = \left(\frac{\partial S}{\partial U}\right)_{V,N} ,
\qquad
\frac{P}{T} = \left(\frac{\partial S}{\partial V}\right)_{U,N} ,
\qquad
-\frac{\mu}{T} = \left(\frac{\partial S}{\partial N}\right)_{U,V} .
$$

The third defines the **chemical potential** $\mu$, measured in joules per particle. It is
introduced here because the fundamental relation is incomplete without its third slope; module
13 is where it is put to work.
:::

The first two had better be the temperature and pressure you already know, and the definitions
have to be *checked* against them rather than assumed. Here is the check.

**Temperature.** Heat the system reversibly at fixed $V$ and $N$. No work is done, so the first
law and module 07's definition of entropy give

$$
\mathrm{d}U = \dbar Q_{\text{rev}} ,
\qquad
\mathrm{d}S = \frac{\dbar Q_{\text{rev}}}{T} .
$$

Divide one by the other: the slope $\partial S/\partial U$ is $1/T$, with $T$ the thermodynamic
temperature of module 07.

**Pressure.** Compress the system reversibly and adiabatically at fixed $N$. No heat flows, so
its entropy does not change, while the first law gives

$$
\mathrm{d}U = \dbar \Won = -P_{\text{mech}}\,\mathrm{d}V ,
$$

with $P_{\text{mech}}$ the force per area the piston feels. Setting $\mathrm{d}S$ to zero in the
expansion above,

$$
0 = \frac{1}{T}\left(-P_{\text{mech}}\,\mathrm{d}V\right)
+ \left(\frac{\partial S}{\partial V}\right)_{U,N} \mathrm{d}V ,
$$

so $T\,(\partial S/\partial V)$ is exactly the mechanical pressure.

Substituting the three slopes into $\mathrm{d}S$ and solving for $\mathrm{d}U$ gives the most
used equation in thermodynamics.

:::{admonition} The fundamental relation in differential form
:class: theorem
Between any two neighbouring equilibrium states,

$$
\mathrm{d}U = T\,\mathrm{d}S - P\,\mathrm{d}V + \mu\,\mathrm{d}N .
$$

It is an identity among functions of state, so it holds for *any* pair of neighbouring
equilibrium states, however the system travelled between them. What holds only for a
quasistatic change is the term-by-term reading: there, and only there, $T\,\mathrm{d}S$ is the
heat $\dbar Q_{\text{rev}}$ and $-P\,\mathrm{d}V$ is the work $\dbar \Won$. That is the
course's sign convention, now written with exact differentials on the right.
:::

**A test on a real relation.** For a monatomic ideal gas the fundamental relation is known in
closed form.

:::{admonition} The Sackur–Tetrode equation
:class: approximation
For $N$ atoms of mass $m$ in volume $V$ with energy $U$,

$$
S(U, V, N) = N \kB \left[
\ln\!\left( \frac{V}{N} \left( \frac{4 \pi m U}{3 N h^2} \right)^{3/2} \right)
+ \frac{5}{2} \right] ,
$$

where $h$ is Planck's constant. It is stated here, not derived: the derivation counts
states in phase space in cells of size $h$ and divides by $N!$ for identical atoms, which is
module 12's business. It holds for a dilute gas, where the atoms' quantum wavelength is small
compared with their spacing. Below that, the logarithm goes negative and eventually the entropy
does too, which no count of states can give — the formula's own warning that it has left its
regime.
:::

Take its slopes. Only one term depends on $U$, and only one on $V$:

$$
\frac{1}{T} = \frac{\partial S}{\partial U} = \frac{3}{2}\,\frac{N \kB}{U} ,
\qquad
\frac{P}{T} = \frac{\partial S}{\partial V} = \frac{N \kB}{V} .
$$

The first is module 04's kinetic temperature, and the second is module 02's ideal gas law:

$$
U = \tfrac{3}{2} N \kB T ,
\qquad
PV = N \kB T .
$$

Neither was put in. Both came out of a single function by differentiating it, which is the whole
claim of this module in miniature.

### Step 3: equilibrium is where the slopes match

Now the central result. Take the composite: two systems in an isolated box, with a wall between
them that conducts heat but does not move and has no holes. The total energy is fixed; how it
is shared is not. Give subsystem 1 the energy $U_1$, and subsystem 2 the rest:

$$
S_{\text{tot}}(U_1) = S_1(U_1) + S_2(U - U_1) .
$$

By the maximum postulate, the wall's energy settles where this is largest. At a maximum the
derivative vanishes, and by the chain rule the second term contributes a minus sign:

$$
\frac{\mathrm{d} S_{\text{tot}}}{\mathrm{d} U_1}
= \frac{\partial S_1}{\partial U_1} - \frac{\partial S_2}{\partial U_2}
= \frac{1}{T_1} - \frac{1}{T_2} = 0 .
$$

:::{admonition} Equilibrium conditions
:class: theorem
Maximising the total entropy of an isolated composite over what its internal wall lets move
gives one condition per released constraint:

- a wall that conducts heat: equal temperatures;
- a wall that also moves: equal pressures as well;
- a wall that also lets particles through: equal chemical potentials as well.
:::

The pressure and particle versions come the same way: release the volume at fixed total volume
and differentiate with respect to $V_1$, and the slopes $P/T$ must match; with the temperatures
already equal, so must the pressures. One caution the laboratory enforces: a wall that moves or
lets particles through always carries energy across too — a moving piston does work, and a
crossing particle takes its energy with it — so those constraints are only ever released
together with the energy one.

**Which way does energy flow?** Before equilibrium, the total entropy is still rising, so a
small transfer $\mathrm{d}U_1$ into subsystem 1 must have

$$
\mathrm{d} S_{\text{tot}}
= \left(\frac{1}{T_1} - \frac{1}{T_2}\right) \mathrm{d}U_1 > 0 .
$$

If $T_1 < T_2$, the bracket is positive, and so is $\mathrm{d}U_1$: energy flows into the colder
body. A steeper $S(U)$ — a larger $1/T$ — means a colder body, and giving it energy buys more
entropy than the hotter body loses by giving that energy up. Heat flowing from hot to cold is
not a separate law. It is the maximum postulate, applied one transfer at a time.

**The puzzle, resolved.** The condition is on *slopes*, and nothing ties a slope to a size. A big
body and a small body can have the same slope with wildly different energies, and at
equilibrium they do. The pebble ends at the lake's temperature holding almost none of the
energy; the lake's $S(U)$ is so gently curved that absorbing the pebble's heat barely changes its
slope, which is exactly what makes it a reservoir. What is maximised is the total entropy, and
the only thing that condition ever equalises is $\partial S/\partial U$.

**Is it really a maximum?** A vanishing derivative could be a minimum too. The second derivative
settles it:

$$
\frac{\mathrm{d}^2 S_{\text{tot}}}{\mathrm{d} U_1^2}
= \frac{\partial^2 S_1}{\partial U_1^2} + \frac{\partial^2 S_2}{\partial U_2^2} .
$$

By the concavity postulate both terms are negative or zero, so the equal-slope point is a
maximum. Step 7 shows what goes wrong without that postulate.

### Step 4: a fundamental relation worked through — the Einstein solid

Module 01's solid is $n$ oscillators sharing $q$ identical quanta of energy $\varepsilon$, so
its energy is $U = q\varepsilon$. How many ways can $q$ identical quanta be shared among $n$
oscillators? Line the quanta up as dots and separate the oscillators with $n - 1$ bars: every
arrangement of the dots and bars in a row is one microstate. With four quanta among three
oscillators, the row `●●|●|●` gives the first oscillator two quanta and each of the others
one. So the count is the number of ways to choose which of the $q + n - 1$ positions hold dots:

$$
\Omega(q, n) = \binom{q + n - 1}{q} .
$$

For four quanta among three oscillators that is $15$. For macroscopic $q$ and $n$, Stirling's
approximation from module 08 turns $\kB \ln \Omega$ into

$$
S(U, n) = \kB \Big[ (q + n) \ln (q + n) - q \ln q - n \ln n \Big] ,
\qquad q = \frac{U}{\varepsilon} .
$$

This is a fundamental relation. The solid has no volume to speak of, so $S$ depends on $U$ and
on its size $n$; scale both together and $S$ scales with them, so it is extensive. Its energy
slope is the temperature:

$$
\frac{1}{T} = \frac{\partial S}{\partial U}
= \frac{\kB}{\varepsilon} \ln\!\left(1 + \frac{n \varepsilon}{U}\right) .
$$

When the solid is hot, $U$ is much larger than $n\varepsilon$, so the logarithm's argument is
only slightly above one and the logarithm can be expanded in powers of the small excess.
Keeping the first two terms,

$$
T \approx \frac{U}{n \kB} + \frac{\varepsilon}{2 \kB} ,
$$

which is module 01's map from quanta to temperature, plus an offset of half a quantum that
matters less and less as the solid warms. Module 01 *assumed* that map by equipartition; here it
has come out of counting. Inverted, the exact slope gives

$$
U = \frac{n \varepsilon}{e^{\varepsilon / \kB T} - 1} ,
$$

Einstein's formula of 1907, whose falling heat capacity at low temperature module 16 takes up.

**Two unequal solids.** Put solid A, with $n_A$ oscillators, against solid B, with $n_B$. Equal
slopes means equal logarithms, and so

$$
\frac{n_A}{q_A} = \frac{n_B}{q_B}
\qquad\Longrightarrow\qquad
\frac{U_A}{U_B} = \frac{n_A}{n_B} .
$$

Each oscillator ends with the same average energy, so each solid's share of the energy is its
share of the oscillators. With $n_B = 10\,n_A$, solid A ends with one part in eleven. That is
prediction 1 answered: equal temperatures, and energies in the ratio of the sizes.

### Step 5: extensivity forces the Euler relation

The first postulate said that scaling a system scales its entropy. As an equation, for every
$\lambda > 0$,

$$
S(\lambda U, \lambda V, \lambda N) = \lambda\, S(U, V, N) .
$$

A function with this property is called **homogeneous of degree one**, and there is a short
theorem about such functions. Differentiate both sides with respect to $\lambda$. On the left
the chain rule gives one term per argument; on the right the result is just $S$:

$$
U \frac{\partial S}{\partial (\lambda U)}
+ V \frac{\partial S}{\partial (\lambda V)}
+ N \frac{\partial S}{\partial (\lambda N)}
= S(U, V, N) .
$$

This holds for every $\lambda$, so set $\lambda = 1$ and replace each slope by its name from
step 2:

$$
S = \frac{U}{T} + \frac{P V}{T} - \frac{\mu N}{T} .
$$

Multiply by $T$ and rearrange.

:::{admonition} The Euler relation
:class: theorem
For any system whose entropy is extensive,

$$
U = T S - P V + \mu N .
$$

It uses nothing but the scaling property and the definitions of the slopes, and it is exactly
as true as extensivity is.
:::

There is a second way to see it, which shows where extensivity enters. Build the system up from
nothing by adding more and more of it at a fixed temperature, pressure and chemical potential,
as a crystal grows in its own melt. Along that one path $T$, $P$ and $\mu$ never change, so the
differential form of step 2 integrates term by term, and it gives exactly the Euler relation.
What makes that path available is extensivity: only if a bigger piece of the same stuff has the
same intensive state can the system be grown without changing $T$, $P$ and $\mu$. Along any other
path they change, and the naive integration is wrong.

For one mole of argon at $298.15\ \mathrm{K}$ and $1\ \mathrm{bar}$, Sackur–Tetrode gives these
values, and the Euler relation can be checked with a calculator:

$$
\begin{gathered}
T S = 46\,167\ \mathrm{J} ,
\qquad
P V = 2479\ \mathrm{J} ,
\qquad
\mu N = -39\,970\ \mathrm{J} , \\
T S - P V + \mu N = 3718\ \mathrm{J} = \tfrac{3}{2} R T .
\end{gathered}
$$

### Step 6: the Gibbs–Duhem relation

Now there are two expressions for $U$ in hand. Differentiate the Euler relation, using the
product rule on each term:

$$
\mathrm{d}U = T\,\mathrm{d}S + S\,\mathrm{d}T - P\,\mathrm{d}V - V\,\mathrm{d}P
+ \mu\,\mathrm{d}N + N\,\mathrm{d}\mu .
$$

Subtract the differential form from step 2. The three terms of that equation cancel, and what is
left must vanish.

:::{admonition} The Gibbs–Duhem relation
:class: theorem
$$
S\,\mathrm{d}T - V\,\mathrm{d}P + N\,\mathrm{d}\mu = 0 .
$$

The three intensive variables of a one-component system cannot be changed independently: fix
the changes in any two, and the third is determined.
:::

This is why, in the second animation, punching holes in the wall moved nothing. Once the
temperatures and the pressures on the two sides agreed, the Gibbs–Duhem relation left the
chemical potentials no freedom to differ: the same gas at the same $T$ and $P$ has the same
$\mu$. The three equilibrium conditions of step 3 are not three independent demands.

A useful special case: hold the temperature fixed. Then the change in $\mu$ is $V/N$ times the
change in pressure, and for an ideal gas $V/N$ is $\kB T/P$, so

$$
\mu(T, P_2) - \mu(T, P_1) = \kB T \ln\frac{P_2}{P_1} .
$$

Module 13 builds on this line.

### Step 7: concavity is stability

The postulates asked for a concave $S$. Here is why a system that broke the rule could not
exist in equilibrium with anything.

Differentiate the temperature slope once more. With $1/T$ as the first derivative,

$$
\frac{\partial^2 S}{\partial U^2}
= \frac{\partial}{\partial U}\!\left(\frac{1}{T}\right)
= -\frac{1}{T^2}\,\frac{\partial T}{\partial U}
= -\frac{1}{T^2 C_V} ,
$$

where the heat capacity $C_V$ is the derivative $(\partial U/\partial T)_{V,N}$. So the sign of
the curvature is the sign of the heat capacity, reversed.

:::{admonition} Stability
:class: theorem
A concave entropy is a positive heat capacity: $\partial^2 S/\partial U^2 \le 0$ exactly when
$C_V \ge 0$. Concavity in the volume direction as well gives a positive isothermal
compressibility, $\kappa_T \ge 0$: squeeze a stable substance at fixed temperature and its
pressure rises. Both halves are derived below.
:::

**The runaway.** Take two identical pieces of a substance, each with energy $U$, in contact.
Move a small amount of energy $\delta$ from one to the other. The total entropy goes from
$2\,S(U)$ to

$$
S(U + \delta) + S(U - \delta) .
$$

If $S$ curves downwards, the chord between those two points lies below the curve, the new total
is smaller, and the transfer is undone: the fluctuation dies. If $S$ curves *upwards*, the new
total is larger, the maximum postulate rewards the transfer, and the next transfer in the same
direction is rewarded more. The energy segregates. In the language of temperature: with a
negative heat capacity, the piece that loses energy gets *hotter*, so heat flows back out of it
faster, and the difference grows instead of shrinking.

:::{figure} ../media/fundamental-concavity.png
:alt: Two plots of entropy against energy. Left, a curve bending downwards, with a chord between two points lying below the curve at the midpoint. Right, a curve bending upwards, with the chord lying above it.
:width: 85%

The runaway in one picture. Two identical pieces start at the middle energy $U$. Sharing out a
fluctuation $\pm\delta$ moves them to the two ends of the chord, and the chord's midpoint is
their new average entropy. (a) A concave $S$: the chord's midpoint is below the curve, so the
fluctuation lowers the total entropy and is undone. (b) A convex $S$: the midpoint is above the
curve, so the fluctuation raises the total entropy and grows.
:::

**The volume direction.** With two variables in play, "curves downwards in every direction"
has a precise meaning. Write $S_{UU}$, $S_{VV}$ and $S_{UV}$ for the second partial derivatives
of $S(U, V)$ at fixed $N$, the last being the mixed one. A small step $\mathrm{d}U$,
$\mathrm{d}V$ in any direction must change $S$, at second order, by a negative amount:

$$
S_{UU}\,\mathrm{d}U^2 + 2 S_{UV}\,\mathrm{d}U\,\mathrm{d}V + S_{VV}\,\mathrm{d}V^2 \le 0 .
$$

A quadratic expression like this is never positive, whatever the step, exactly when

$$
S_{UU} \le 0 ,
\qquad
S_{VV} \le 0 ,
\qquad
S_{UU} S_{VV} - S_{UV}^2 \ge 0 .
$$

Now squeeze the system at fixed temperature. Its first slope $S_U$ is $1/T$, so keeping $T$
fixed means an energy change must accompany the volume change and cancel its effect on that
slope:

$$
S_{UU}\,\mathrm{d}U + S_{UV}\,\mathrm{d}V = 0 .
$$

The volume slope $S_V$ is $P/T$, and with $T$ fixed its change is the change in pressure
divided by $T$. Substituting the energy change from the line above,

$$
\frac{\mathrm{d}P}{T} = S_{UV}\,\mathrm{d}U + S_{VV}\,\mathrm{d}V
= \left( S_{VV} - \frac{S_{UV}^2}{S_{UU}} \right) \mathrm{d}V ,
$$

and so

$$
\left(\frac{\partial P}{\partial V}\right)_T
= \frac{T\,\big(S_{UU} S_{VV} - S_{UV}^2\big)}{S_{UU}} \le 0 .
$$

The numerator is not negative and the denominator is negative, so compressing at fixed
temperature can only raise the pressure. That is the statement that the isothermal
compressibility,

$$
\kappa_T = -\frac{1}{V}\left(\frac{\partial V}{\partial P}\right)_T ,
$$

is never negative. On the Sackur–Tetrode surface the mixed derivative vanishes, and the formula
returns exactly one over the pressure — the ideal gas's compressibility, read off the curvature
of its entropy. The runaway argument has a mechanical twin here: if a substance's pressure
*fell* when it was squeezed, a movable wall between two identical samples would be pushed
further by any small displacement, and the pair would separate into a dense region and a dilute
one. That is exactly what the van der Waals loop below its critical temperature would do, and it
is why a real gas condenses there instead.

The energy runaway, for its part, is not hypothetical. A star is a ball of gas held together by its own gravity, and the
virial theorem says its total energy is minus its kinetic energy:

$$
U = -\tfrac{3}{2} N \kB T ,
\qquad
C = -\tfrac{3}{2} N \kB .
$$

A star that radiates energy away *heats up*. Two stars could never settle at a common
temperature, and a star cannot be put in equilibrium with a heat bath. It escapes the argument
by breaking the first postulate: gravity is long-ranged, a star twice the mass is not two stars,
and its entropy is not extensive. The laboratory includes this relation, and the Euler relation
of step 5 fails on it by exactly twice its energy.

### Step 8: entropy produced, computed

Module 07 defined the entropy produced by a process as the total change of the system and of
everything it exchanged heat with, and proved it is never negative. This step computes it for
two processes that module 07 could only bound.

**Two bodies at different temperatures.** Put body A, heat capacity $C_A$, at $T_{A,0}$ against
body B, $C_B$ at $T_{B,0}$, and insulate the pair. Energy conservation fixes where they end, as
module 01 found:

$$
T_{\text{eq}} = \frac{C_A T_{A,0} + C_B T_{B,0}}{C_A + C_B} .
$$

Each body's entropy change is module 07's constant-heat-capacity result, and nothing crosses the
pair's outer boundary, so their sum is all produced:

$$
\Delta S_{\text{tot}}
= C_A \ln\frac{T_{\text{eq}}}{T_{A,0}} + C_B \ln\frac{T_{\text{eq}}}{T_{B,0}} .
$$

Why is this positive? Divide by $C_A + C_B$ and write $w_A$ and $w_B$ for the two bodies' shares
of the total heat capacity. The final temperature is the weighted average of the starting ones,
and the entropy change is the logarithm of that average minus the weighted average of the
logarithms. The logarithm is concave, so the logarithm of an average always beats the average of
the logarithms — the same chord picture as step 7:

$$
\ln\!\big(w_A T_{A,0} + w_B T_{B,0}\big) \ge w_A \ln T_{A,0} + w_B \ln T_{B,0} ,
$$

with equality only when the two starting temperatures are equal.

:::{admonition} Contact across a temperature difference produces entropy
:class: theorem
Two bodies of constant heat capacity that reach a common temperature produce

$$
\Delta S_{\text{tot}}
= C_A \ln\frac{T_{\text{eq}}}{T_{A,0}} + C_B \ln\frac{T_{\text{eq}}}{T_{B,0}} \ge 0 ,
$$

with equality only if they started at the same temperature.
:::

**A free expansion.** A gas leaks from $V_1$ into an evacuated chamber until it fills $V_2$. No
heat, no work, so $U$ is unchanged, and so is $N$. The Sackur–Tetrode equation depends on $V$
through one term, $N \kB \ln V$, so

$$
\Delta S = N \kB \ln\frac{V_2}{V_1} .
$$

That makes three independent routes to one number. Module 07 took a reversible isotherm between
the same two end states and integrated $\dbar Q_{\text{rev}}/T$. Module 08 counted: each atom
has $V_2/V_1$ times the room, so $\Omega$ grows by that factor to the power $N$. And here it is a
difference of two values of one function. Prediction 3 is answered three times over: the entropy
rises, although nothing flowed in. Nothing in between was an equilibrium state, and it did not
need to be — $S$ belongs to the endpoints, and both endpoints are equilibrium states.

**Flow and production are different things.** It is tempting to think entropy is produced
wherever it moves. It is not.

:::{admonition} Entropy that flows and entropy that is produced
:class: definition
Heat $\dbar Q$ crossing a boundary at temperature $T$ carries entropy $\dbar Q / T$ with it —
entropy **flows**. Entropy is **produced** when the total over everything involved goes up.
Every change in a system's entropy is the sum of the two:

$$
\Delta S = \int \frac{\dbar Q}{T_{\text{boundary}}} + S_{\text{gen}} ,
\qquad
S_{\text{gen}} \ge 0 .
$$
:::

A gas expanding reversibly along an isotherm at $T$, in contact with a bath at the same $T$,
takes in heat $Q$. Entropy $Q/T$ flows into the gas and the same $Q/T$ flows out of the bath,
and nothing is produced: a great deal of flow, zero production. Now let the same heat $Q$ cross
from a body at $T_A$ into one at $T_B$ with $T_A > T_B$. It leaves A carrying $Q/T_A$ and
arrives in B bringing $Q/T_B$, which is more; the difference,

$$
S_{\text{gen}} = \frac{Q}{T_B} - \frac{Q}{T_A} > 0 ,
$$

was produced in the crossing. That is the whole of the contact formula above, one sliver of heat
at a time.

:::{note} The module in eight statements
1. An entropy function is additive and extensive, increasing in energy, concave, and maximised
   when a constraint is released. Modules 07 and 08 each established these properties from
   their own starting points; here they are the axioms.
2. Its slopes are the intensive variables: $1/T$, $P/T$ and $-\mu/T$. On the ideal gas they
   return the kinetic temperature and the ideal gas law without being told either.
3. Equilibrium between two systems is where their slopes match. Temperatures equalise because
   slopes do; energies are free to end as unequal as the systems' sizes.
4. Energy flows toward the steeper $S(U)$, the colder body, because that transfer raises the
   total entropy.
5. The Einstein solid's $S(U, n)$ follows from counting, and its slope reproduces module 01's
   temperature map in the hot limit.
6. Extensivity alone forces the Euler relation of step 5, and with it the Gibbs–Duhem
   relation: $T$, $P$ and $\mu$ cannot all be varied independently.
7. Concavity is stability: it is a positive heat capacity. A convex $S$ would let energy
   segregate without limit, and stars, which have one, escape only by not being extensive.
8. Entropy produced is computable: two bodies at different temperatures, a free expansion. It
   is not the same as entropy that flows.
:::

(09-fundamental-relation-verify)=
## Verify computationally

The derivation is a chain of exact statements. The laboratory checks that each link was
assembled correctly, on the two relations of this module and on a third, the star, that
deliberately breaks the rules. Each check is also a test in the project's suite.

**1. The slopes are the equations of state.** Numerical derivatives of the Sackur–Tetrode
function, with nothing else supplied, return the temperature and pressure the state was built
with to about one part in $10^{8}$, and a chemical potential that matches
$\kB T \ln(N \lambda^3 / V)$, with $\lambda$ the thermal wavelength, to one part in $10^{6}$.

**2. The Einstein slope is the Einstein temperature.** At every energy tried, from half a
quantum per oscillator to two hundred, the numerical slope of the Stirling-form $S(U, n)$ agrees
with the closed form of step 4 to one part in $10^{7}$. As the solid heats, the temperature
approaches module 01's map with an offset that settles at exactly half a quantum.

**3. The maximiser finds equal slopes.** Released through a heat-conducting wall, a solid of
40 oscillators and one of 400 end at the same temperature to one part in $10^{6}$, with the
energy split exactly $1 : 10$. The divided gas, with its wall freed to slide, ends with equal
temperatures and equal pressures; perforating the wall afterwards changes the total entropy by
less than one part in $10^{12}$.

**4. Euler and Gibbs–Duhem close — and can fail.** For both extensive relations, the Euler
relation balances to about one part in $10^{8}$ of $U$, and the Gibbs–Duhem sum along a small
displacement vanishes to one part in $10^{5}$ of its terms, shrinking fourfold every time the
displacement is halved. The star's Euler residual is not small. It is $2.000$, in units of
$|U|$: the relation misses exactly twice the energy, as its non-extensive entropy predicts.

**5. The curvature is the heat capacity.** The second derivative of Sackur–Tetrode gives a heat
capacity of $\tfrac{3}{2} N \kB$ to one part in $10^{5}$. The star gives $-\tfrac{3}{2} N \kB$,
and the stability test rejects it. The full curvature in energy and volume, fed through the
formula of step 7, gives the gas's isothermal compressibility as one over its pressure, again to
one part in $10^{5}$.

**6. The ledger of module 01's simulation.** Two solids of 300 and 100 oscillators, started at
$500\ \mathrm{K}$ and $250\ \mathrm{K}$ with quanta of $\varepsilon = (5\ \mathrm{K})\,\kB$, relax as in
module 01. The ledger counts each solid's microstates exactly at every step.

:::{admonition} The ledger rises, and it is not monotone
:class: numerical-observation
Over the relaxation the total entropy rises by about $15.27\,\kB$ and flattens exactly when the
temperatures meet, just below the largest total entropy any partition of that energy has. But
on about $18\%$ of individual steps it goes *down* — every time a quantum happens to hop the
"wrong" way, by at most about $0.01\,\kB$. The deepest it ever falls below its own previous best
is about $0.1\,\kB$, under one percent of the rise. So the answer to prediction 2 is yes, often.
The ledger is monotone *within noise*, and that is all a simulation can show: it illustrates the
maximum postulate on one run and proves nothing about the next. The proof is the counting in
module 08.
:::

The module-01 hop rule moves quanta as if they were labelled, so its own long-run distribution
is not exactly the Einstein count: it peaks at almost the same partition — here within two
tenths of a percent — but its jitter about the peak is narrower than a true Einstein solid's. The rise and the plateau, which are what the
ledger tests, are unaffected.

**7. Three entropies of one contact.** The same relaxation can be priced three ways. The exact
count says $15.27\,\kB$. The Stirling-form surface of step 4 says $15.69\,\kB$. The contact
formula of step 8, with module 01's heat capacities $C = n \kB$, says $15.90\,\kB$.

:::{admonition} Two approximations, each measured
:class: approximation
The gap between the Stirling surface and the contact formula is the high-temperature
approximation: it halves every time the quantum is halved, because it is the half-quantum
offset of step 4 at work. The gap between the exact count and the Stirling surface is Stirling's
$\ln N$ correction from module 08. It stays near $0.4\,\kB$ whatever the quantum, and it becomes
negligible only because the total grows in proportion to the size while the correction does
not.
:::

**8. Free expansion, three ways.** Doubling the volume of $10\,000$ atoms gives
$N \kB \ln 2$ from the Sackur–Tetrode difference, from module 07's ideal-gas formula, and from
the heat absorbed along a reversible isotherm divided by its temperature — to nine significant
figures in every case.

:::{admonition} Is any real substance exactly concave?
:class: open-question
Every stable phase of every substance that has been measured has a positive heat capacity and a
positive compressibility, so over any range where one phase is stable its entropy is concave.
But a model equation of state can produce a convex patch — the van der Waals gas does, below its
critical temperature — and a real substance does not follow it there: it splits into two phases
instead. Whether "convex patch" always means "two phases", and how the surface is repaired, is
module 14's question.
:::

(09-fundamental-relation-transfer)=
## Transfer the idea

Looking back:

- **Module 01** found that two bodies stop exchanging energy at equal temperatures and gave the
  equilibrium temperature a formula. The reason it stops there is now in hand: that partition
  maximises the total entropy, and temperature is the slope that the maximum equalises.
- **Module 06** left the free expansion's entropy as a question, and module 07 answered it with a
  reversible isotherm. Here it is a difference of two values of one function.
- **Module 07's** Clausius entropy and **module 08's** Boltzmann entropy are two constructions of
  one function. This module never needed to say which it was using, because both have the
  properties the postulates ask for.
- **Module 08's** narrow peak is why the maximum is all that matters: fluctuations about it are
  a fraction $N^{-1/2}$ of the whole, invisible in anything macroscopic.

Looking ahead:

- **Module 10** trades $S(U, V, N)$ for functions whose natural variables are the ones a
  laboratory controls — temperature and pressure rather than energy and volume. Everything there
  is built by differentiating the surface of this module.
- **Module 11** puts a small system against a huge one and reads the huge one's slope
  $\partial S/\partial U$, its $1/T$, as the only thing the small one ever feels. That is where
  the Boltzmann factor comes from.
- **Module 13** develops the chemical potential that was only named here.
- **Module 14** starts exactly where concavity fails.

And in the laboratory:

- **Calorimetry works because of step 3.** Mixing a hot sample into a known mass of water and
  reading the final temperature measures heat capacities only because the mixture settles at a
  single, reproducible temperature, fixed by energy conservation and equal slopes.
- **The entropy of argon.** The Sackur–Tetrode value for one mole of argon at
  $298.15\ \mathrm{K}$ and $1\ \mathrm{bar}$ is $154.85\ \mathrm{J\,K^{-1}}$, and the tabulated
  standard molar entropy is $154.8\ \mathrm{J\,K^{-1}}$. The same entropy can be measured with
  no formula at all, by calorimetry — integrating $C_P/T$ up from near absolute zero through
  melting and boiling — and for the noble gases the two agree to within a fraction of a
  percent. A formula with Planck's constant in it and a stack of heat-capacity measurements
  land on the same number.

:::{admonition} Why the maximum principle is worth its abstraction
:class: definition
A **fundamental relation** is a function that contains every thermodynamic property of a system:
$S(U, V, N)$, or equivalently $U(S, V, N)$. Knowing one is knowing everything thermodynamics can
say about the system. Every equation of state is one of its slopes, and every equilibrium it can
reach is one of its constrained maxima. What it does not contain is *how fast* anything happens.
That needs a model of the dynamics, like module 01's.
:::

### Worked examples

Try each one before opening its solution.

**Worked example 1 — sharing out the quanta.** Solid A has 100 oscillators and solid B has 300.
Together they hold 2000 quanta of size $\varepsilon$. At equilibrium, how many quanta does each
hold, and what is their common temperature?

:::{dropdown} Solution
Equal slopes means equal energy per oscillator:

$$
\frac{q_A}{100} = \frac{q_B}{300} ,
\qquad
q_A + q_B = 2000
\qquad\Longrightarrow\qquad
q_A = 500 , \quad q_B = 1500 .
$$

Each oscillator holds 5 quanta on average, so the temperature from step 4 is

$$
T = \frac{\varepsilon}{\kB \ln(1 + 1/5)} = \frac{\varepsilon}{0.1823\,\kB}
= 5.485\,\frac{\varepsilon}{\kB} .
$$

Module 01's map would say $5\,\varepsilon/\kB$; the difference is almost exactly the half-quantum
offset. B holds three times A's energy at the same temperature.
:::

**Worked example 2 — mixing water.** Half a kilogram of water at $360\ \mathrm{K}$ is poured into
$1.5\ \mathrm{kg}$ at $280\ \mathrm{K}$ in an insulated flask. Take the specific heat as
$4184\ \mathrm{J\,kg^{-1}\,K^{-1}}$. Find the final temperature, each part's entropy change, and
the entropy produced.

:::{dropdown} Solution
The heat capacities are $2092\ \mathrm{J\,K^{-1}}$ and $6276\ \mathrm{J\,K^{-1}}$, and the final
temperature is their weighted average:

$$
T_{\text{eq}} = \frac{0.5 \times 360 + 1.5 \times 280}{2.0} = 300.0\ \mathrm{K} .
$$

Each part's entropy change is $C \ln(T_{\text{eq}}/T_0)$:

$$
\begin{aligned}
\Delta S_{\text{hot}} &= 2092 \ln\frac{300}{360} = -381.4\ \mathrm{J\,K^{-1}} , \\
\Delta S_{\text{cold}} &= 6276 \ln\frac{300}{280} = +433.0\ \mathrm{J\,K^{-1}} , \\
\Delta S_{\text{tot}} &= 51.6\ \mathrm{J\,K^{-1}} .
\end{aligned}
$$

The hot water's entropy fell, and nothing is wrong: the second law constrains the total. The
same $125.5\ \mathrm{kJ}$ of heat left the hot water and entered the cold, but it left from
hotter water, carrying less entropy per joule than it delivered. The $51.6\ \mathrm{J\,K^{-1}}$
was produced in the crossing.
:::

**Worked example 3 — checking Euler on argon.** For one mole of argon at $298.15\ \mathrm{K}$ and
$1\ \mathrm{bar}$, Sackur–Tetrode gives $S = 154.85\ \mathrm{J\,K^{-1}}$. Find $U$, $PV$ and
$\mu N$, and check the Euler relation.

:::{dropdown} Solution
The slopes of step 2 give the energy and the product of pressure and volume:

$$
U = 1.5 \times 8.3145 \times 298.15 = 3718\ \mathrm{J} ,
\qquad
P V = 2479\ \mathrm{J} .
$$

For $\mu$, differentiate Sackur–Tetrode with respect to $N$. Every term of $S/N$ depends on $N$
only through $V/N$ and $U/N$, which together contribute $-\tfrac{5}{2}\kB$ per particle, so

$$
\mu = -T\left(\frac{S}{N} - \frac{5}{2}\kB\right) ,
\qquad
\mu N = -298.15 \times (154.85 - 20.79) = -39\,970\ \mathrm{J} .
$$

Then

$$
T S - P V + \mu N = 46\,167 - 2479 - 39\,970 = 3718\ \mathrm{J} ,
$$

which is $U$. Note what $\mu$ is doing: it is large and negative, because adding an atom to a
dilute gas at fixed energy and volume *raises* the entropy by a lot.
:::

**Worked example 4 — Gibbs–Duhem at work.** Argon at $298.15\ \mathrm{K}$ is compressed
isothermally from $1\ \mathrm{bar}$ to $2\ \mathrm{bar}$. By how much does its molar chemical
potential change?

:::{dropdown} Solution
At fixed temperature Gibbs–Duhem leaves

$$
N\,\mathrm{d}\mu = V\,\mathrm{d}P ,
$$

and for an ideal gas $V/N$ is $\kB T / P$. Per mole,

$$
\Delta \mu_{\text{molar}} = R T \ln\frac{P_2}{P_1} = 8.3145 \times 298.15 \times \ln 2
= 1718\ \mathrm{J\,mol^{-1}} .
$$

The chemical potential rises with pressure: squeezed atoms have less room, so each one added at
fixed energy and volume buys less entropy. Module 13 will show that particles move from higher
$\mu$ to lower, which is why a gas leaks from high pressure to low.
:::

**Worked example 5 — the price of a free expansion.** One mole of an ideal gas at
$300\ \mathrm{K}$ doubles its volume by leaking into a vacuum. How much entropy is produced, and
how much work was lost compared with the best possible route to the same final state?

:::{dropdown} Solution
The entropy change is

$$
\Delta S = R \ln 2 = 5.763\ \mathrm{J\,K^{-1}} ,
$$

and since nothing flowed in, all of it was produced. A reversible isothermal expansion against a
piston, drawing heat from surroundings at $300\ \mathrm{K}$, would have delivered

$$
R T \ln 2 = 8.3145 \times 300 \times 0.6931 = 1729\ \mathrm{J}
$$

of work — which is exactly the temperature times the entropy produced, the lost-work rule of
module 07.
:::

**Worked example 6 — a star.** A star of $N$ particles radiates away energy at a rate $L$. Use
its heat capacity to find how its temperature changes.

:::{dropdown} Solution
With the star's energy from step 7, losing energy at the rate $L$ means

$$
\frac{\mathrm{d}T}{\mathrm{d}t} = \frac{1}{C}\,\frac{\mathrm{d}U}{\mathrm{d}t}
= \frac{-L}{-\tfrac{3}{2} N \kB} = + \frac{2 L}{3 N \kB} .
$$

It heats up. The star contracts, its gravitational energy falls by twice what it radiates, and
half of that goes into making its gas hotter. Put it in contact with anything cooler and the
exchange runs away rather than settling — the convex picture of step 7, in the sky.
:::

:::{note} Your predictions, revisited
1. **Equal temperatures, unequal energies.** The copper blocks end at one temperature, with the
   big block holding ten times the small one's energy — see
   [the equilibrium conditions](#09-fundamental-relation-derive).
2. **Yes, often.** The ledger dips on almost a fifth of all single steps, by a tiny amount each
   time, while rising more than a hundred times further overall. The second law is a statement about
   overwhelming probability, not a rule each step obeys.
3. **It rises**, by $N \kB \ln 2$ for a doubling, although no heat flowed in: all of it is
   produced.
4. **They would not stay together at one temperature.** Any fluctuation that moved energy from
   one piece to the other would raise the total entropy and grow, and the pieces would separate
   into a hot one and a cold one. A substance whose entropy is convex cannot be in stable
   equilibrium.
:::

(09-fundamental-relation-quiz)=
## Check your understanding

```{include} ../_generated/quiz-09-fundamental-relation.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](09-fundamental-relation-problems.md).

(09-fundamental-relation-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. Why does a huge body make an ideal "reservoir"? Explain it using the shape of its $S(U)$ near
   the energy it holds, not the word "large".
2. A student says: "Entropy is produced whenever it flows." Give a process in which a great deal
   of entropy flows and none is produced, and repair the student's claim.
3. A free expansion passes through no equilibrium states at all. Why can its entropy change
   nevertheless be computed, and why does the answer not depend on how it was computed?
4. Two bodies in contact end at equal temperatures. Explain, without formulas, why "equal
   energies" was never a candidate for what they approach.
5. The Euler relation and the differential form of step 2 look similar. Explain what each one
   assumes, and why integrating the second gives the first along only one special kind of path.

(09-fundamental-relation-advanced)=
## Advanced: the fixed intensive variable, and the energy picture

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence depends on this section. It follows two threads: what
Gibbs–Duhem says about how many intensive variables are really free, and an equivalent way of
stating the maximum principle that module 10 will use.
:::

**One intensive variable is never free.** A one-component system has three intensive variables,
and Gibbs–Duhem ties them together: $\mu$ is a function of $T$ and $P$, and nothing else. So the
intensive state of a single phase has two degrees of freedom. Now let two phases of the same
substance coexist, liquid and vapour. Equilibrium between them demands equal $T$, equal $P$ and
equal $\mu$. With the first two built in, that is one equation — the second phase's $\mu(T, P)$
must equal the first's — in two unknowns, leaving one free: coexistence happens along a *line*
in the $T$–$P$ plane, the
boiling curve, and not over a region. Three phases leave none, which is why a triple point is a
point. This counting is Gibbs's phase rule, and module 14 derives it.

**The energy-minimum picture.** Invert the fundamental relation: since $S$ increases with $U$,
the surface can equally be written as $U(S, V, N)$. The maximum postulate then has a twin.

:::{admonition} The energy-minimum principle
:class: theorem
At fixed total entropy, the equilibrium value of any unconstrained internal variable minimises
the energy.
:::

The argument runs by contradiction. Suppose a composite were in equilibrium at fixed total
entropy with its energy *not* at the minimum. Then some rearrangement at the same entropy would
have lower energy. Carry that rearrangement out reversibly, drawing the excess energy off as work
and returning it as heat. The entropy rises, so the original state did not have the maximum
entropy for its energy, contradicting the maximum postulate. The two statements pick out the same
states, in the way a circle is both the shape with the largest area for a given perimeter and
the shape with the smallest perimeter for a given area. On the explorer's surface, minimising $U_1 + U_2$
along a line of constant total entropy lands on the same equal-temperature partition as
maximising $S_1 + S_2$ at constant total energy. The energy form is the one engineers use, and it
is the one module 10 transforms.

:::{admonition} What is still open here
:class: open-question
The postulates took extensivity as given, and for short-range forces the limit that justifies it
has been proved rigorously. For gravity it fails, as the star showed, and the thermodynamics of
self-gravitating systems — negative heat capacities, ensembles that disagree, states that never
equilibrate — remains an active research field rather than a closed chapter.
:::
