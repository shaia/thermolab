---
title: Thermal radiation and the heat capacity of solids
short_title: 16 · Radiation and solids
module: 16-radiation-solids
objectives:
  - id: OBJ-16-1
    text: Derive the mean energy of one quantized mode, <E> = h nu / (exp(h nu/(k_B T)) - 1), from the oscillator partition function, and recover the classical k_B T in the limit h nu << k_B T.
  - id: OBJ-16-2
    text: Count standing-wave modes in a cavity to obtain g(nu) dnu = (8 pi V/c^3) nu^2 dnu, and explain why equipartition over these modes predicts infinite energy density (the ultraviolet catastrophe).
  - id: OBJ-16-3
    text: State Planck's law in both spectral variables, convert between them via u_lambda = u_nu |d nu/d lambda|, and explain why the frequency peak and wavelength peak of the same spectrum sit at different photons.
  - id: OBJ-16-4
    text: Compute Wien peaks in both variables (nu_max = 2.821 k_B T/h, lambda_max T = 2.898e-3 m K) and total energy density u = a T^4; predict how total radiated power scales when T changes.
  - id: OBJ-16-5
    text: State the photon-gas relations P = u/3, S/V = (4/3) a T^3, mu = 0, and give the one-line reason photon number carries no chemical potential.
  - id: OBJ-16-6
    text: Derive the Einstein heat capacity C(T) = 3 N k_B (theta_E/T)^2 exp(theta_E/T)/(exp(theta_E/T) - 1)^2 and its limits, Dulong-Petit 3 N k_B at high T and exponential vanishing at low T.
  - id: OBJ-16-7
    text: Explain Debye's phonon-mode repair, compute C(T) from the Debye integral, extract the T^3 low-temperature law, and fit theta_D to measured heat-capacity data.
---

# Thermal radiation and the heat capacity of solids

(16-radiation-solids-puzzle)=
## The puzzle: two catastrophes, one assumption

Set a kitchen oven to $500\ \mathrm{K}$ and look inside. It is dark. Its walls radiate, and you can
feel it on your face, but nothing is visible: the radiation is infrared, peaking near
$6\ \mu\mathrm{m}$.

Now apply the physics of modules 04 to 12, honestly. The inside of the oven is a box full of
electromagnetic waves. Each standing wave that fits in the box is an oscillator, and
equipartition hands every oscillator $\kB T$. There is no shortest wave that fits, so there is
no last oscillator: the number of modes per unit frequency grows as the square of the frequency,
and the energy grows with it. At $500\ \mathrm{K}$ the classical theory puts more energy into the
visible band alone than the whole oven actually holds — by a factor of nineteen thousand — and
more still into the ultraviolet, without limit. Every warm oven should be an ultraviolet lamp of
infinite power.

The oven's steel walls have a second problem. A solid of $N$ atoms is $3N$ oscillators, one per
direction of vibration per atom. Each, again, holds $\kB T$, so the heat capacity is $3N\kB$ — the
**Dulong–Petit** value, about $25\ \mathrm{J\,mol^{-1}\,K^{-1}}$ — at every temperature. Measure
it. Silver at room temperature is close. Silver at $4\ \mathrm{K}$ has a heat capacity nearly
nineteen hundred times smaller. Diamond is a quarter of the Dulong–Petit value *at room temperature*.

:::{important} The question
Both predictions — infinite radiation and a heat capacity that never falls — follow from one
assumption the two have in common. What is it, and what single change to it kills both
catastrophes at once?
:::

Module 12 already met the answer for a single oscillator, and called it freeze-out. This module
takes the same idea to every mode of the electromagnetic field and every mode of a crystal, and
finds that it rescues both. Along the way it meets a smaller puzzle that catches nearly everyone:
the question "at what wavelength does the Sun shine brightest?" has two correct answers, and
which one you get depends on how you draw the graph.

(16-radiation-solids-predict)=
## Predict before you calculate

Commit to an answer for each of these before reading on. Write them down.

1. An oven is heated from $300\ \mathrm{K}$ to $600\ \mathrm{K}$. Does the total power its walls
   radiate grow by a factor of $2$, $4$, $8$ or $16$?
2. Plotted per unit wavelength, the Sun's spectrum peaks near $500\ \mathrm{nm}$. Plotted per unit
   frequency, does it peak at the frequency of $500\ \mathrm{nm}$ light,
   $c/500\ \mathrm{nm} = 600\ \mathrm{THz}$?
3. A diamond is cooled from $300\ \mathrm{K}$ to $30\ \mathrm{K}$. Does its heat capacity drop by a
   factor of about $10$, or by several orders of magnitude? Sketch $C(T)$.
4. The temperature of a cavity is doubled. Does the number of photons inside it double?

:::{note} Why we ask first
The second is the one almost everyone gets wrong, including people who use spectra every day; the
first is a close runner-up. Every answer is collected at the end of the module.
:::

(16-radiation-solids-explore)=
## Explore the model

The laboratory has two explorers. The first draws the blackbody spectrum at a temperature you
choose, per unit frequency and per unit wavelength side by side, with the classical prediction
on demand, and marks where each curve peaks — and where each peak *lands* when carried over to
the other graph. The second draws the heat capacity of the Einstein and Debye models against
measured data for silver from $1\ \mathrm{K}$ to $300\ \mathrm{K}$, with a slider for each
model's one parameter. Then the laboratory runs the experiments this module is built on: the
quantum formula rebuilt from module 12's sum, the total energy integrated numerically, the two
peaks located by brute force, both models fitted to silver, and a fit of the cosmic microwave
background.

:::{figure} ../media/radiation-dual-peak.mp4
:alt: Two side-by-side plots of the blackbody spectrum as the temperature rises from 3000 K to 8000 K, pausing at 5772 K. Left, a blue curve of energy density per unit frequency against frequency; right, a red curve of energy density per unit wavelength against wavelength, with the visible band tinted on both. Each curve is scaled to the height of its own peak. Each panel has a solid vertical line at its own peak and a dashed line, in the other panel's colour, where the other panel's peak falls. As the temperature rises the peaks move to higher frequency and shorter wavelength, and the dashed lines never coincide with the solid ones.
:width: 100%

The blackbody spectrum as the temperature climbs from $3000\ \mathrm{K}$ to $8000\ \mathrm{K}$,
pausing at the Sun's $5772\ \mathrm{K}$. Left: energy per unit volume per unit **frequency**,
$u_\nu$, against frequency (blue). Right: energy per unit volume per unit **wavelength**,
$u_\lambda$, against wavelength (red). The tinted band is visible light, $380$ to
$750\ \mathrm{nm}$. Each curve is drawn scaled to the height of its own peak, so that shapes and
positions can be compared; the energy under the real curves grows fiftyfold over the sweep, as
$T^4$. Each panel's solid line marks its own peak; the dashed line marks the other panel's peak,
carried over by $\lambda = c/\nu$. The dashed line never lands on the solid one: at every
temperature the frequency curve peaks at a photon whose wavelength is $1.76$ times the wavelength
at which the wavelength curve peaks — the ratio $\nu_{\max}\lambda_{\max}/c = 0.568$ printed above
the panels. Both curves describe the same radiation, and the energy under them is the same.
:::

:::{admonition} Model specification
:class: model-spec
- **System:** the electromagnetic field in a cavity of volume $V$ at temperature $T$, as independent standing-wave modes, each with energies restricted to whole multiples of $h\nu$; for the solids explorer, a crystal of $N$ atoms as $3N$ such oscillators, at one frequency (Einstein) or spread over a sound-wave spectrum (Debye).
- **Dynamics:** none — every curve is thermal equilibrium; nothing evolves.
- **Boundary:** rigid, perfectly reflecting walls held at temperature $T$; a small hole in a wall for what an observer sees, which emits a flux $c/4$ times the energy density.
- **Ensemble:** canonical, mode by mode — each mode exchanges energy with the walls (or the rest of the lattice) as its heat bath.
- **Ignored:** zero-point energy (a constant shift); photon–photon interaction (none, for light in vacuum); the material of the walls (the radiation inside a closed cavity does not depend on it; a real surface emits the cavity's spectrum multiplied by its emissivity, which is at most one and can vary with wavelength); polarization beyond its count of two; for solids, the conduction electrons and thermal expansion.
- **Valid when:** the cavity is much larger than the thermal wavelength $hc/(\kB T)$ — $48\ \mu\mathrm{m}$ at room temperature — so that its modes form a continuum; the radiation is in equilibrium with the walls.
- **Failure modes:** cavities so small or so cold that individual modes show; light that is not thermal (lasers, LEDs, fluorescent tubes); for the solids explorer, metals below a few kelvin, where the electrons' heat capacity dominates, and real phonon spectra beyond the Debye caricature.
:::

:::{admonition} Open the laboratory
:class: tip
Run it in your browser, no installation required:
[laboratory 16 — radiation and solids](/lite/lab/index.html?path=en/labs/16-radiation-solids.ipynb).
Python takes a few seconds to start the first time.

To run it locally instead: `uv run jupyter lab notebooks/en/labs/16-radiation-solids.ipynb`.
:::

Run the laboratory now, then come back. Four things are worth doing before you read on:

- Set the temperature to $5772\ \mathrm{K}$, the Sun's surface. Read off both peaks. Is the
  frequency peak's photon visible?
- Switch on the classical curve at $300\ \mathrm{K}$, then at $3000\ \mathrm{K}$. Where does it
  agree with the quantum one, and where does it stop agreeing?
- Double the temperature twice, and watch the area under the curves.
- In the solids explorer, find the Einstein temperature that best matches silver near
  $100\ \mathrm{K}$. Then switch to the log–log view and look at $5\ \mathrm{K}$.

(16-radiation-solids-derive)=
## Derive the result

**System and boundary.** Two systems with one structure. A cavity of volume $V$ whose walls are
held at temperature $T$, containing electromagnetic radiation; and a crystal of $N$ atoms at
temperature $T$. Both are collections of independent harmonic modes, each in contact with a heat
bath — the walls for the radiation, the rest of the crystal for each of its vibrations.

**Independent variables.** The temperature $T$ and the volume $V$. Everything else — the energy,
the spectrum, the pressure of the radiation, the number of photons — is a function of these two.

**Sign convention.** The course convention, $\mathrm{d}U = \dbar Q + \dbar \Won$, holds. It is
exercised once, in step 5: compressing radiation takes work, $\dbar \Won = -P\,\mathrm{d}V > 0$
when $\mathrm{d}V < 0$, because radiation has a pressure.

**Units.** SI throughout, with $\kB$, $h$ and $c$ written explicitly; $\hbar = h/2\pi$. A mode of
frequency $\nu$ (in hertz) has angular frequency $\omega = 2\pi\nu$ and quantum
$h\nu = \hbar\omega$. Spectra are energies per unit volume per unit frequency, in
$\mathrm{J\,s\,m^{-3}}$, or per unit wavelength, in $\mathrm{J\,m^{-4}}$.

**Route.** Seven steps. Find the mean energy of one quantized mode; count the modes of a cavity;
multiply, to get Planck's law, and change the spectral variable; integrate, to get the
Stefan–Boltzmann law; read off the thermodynamics of the photon gas; and then apply the same
mode-by-mode reasoning to a solid, first with one frequency (Einstein) and then with a spectrum
of them (Debye).

### Step 1: one mode, one formula

The single change that rescues both catastrophes is an assumption about energy, not about
statistics. It is taken here as an input.

:::{admonition} Energy comes in quanta
:class: model-assumption
A mode of frequency $\nu$ — a standing electromagnetic wave in a cavity, or a vibration of a
crystal — can hold energy only in whole multiples of $h\nu$:

$$
E_n = n\,h\nu , \qquad n = 0, 1, 2, \ldots
$$

with $h = 6.626 \times 10^{-34}\ \mathrm{J\,s}$, Planck's constant. Quantum mechanics adds a
ground-state energy $h\nu/2$ to every level; it is the same at every temperature, so it changes
no heat capacity and no measurable spectrum, and it is set aside here. This module does not
derive the rule. It shows what the rule does.
:::

Module 12 summed the Boltzmann factors of exactly this ladder. Measured from the ground state, the
oscillator's partition function is a geometric series,

$$
Z = \sum_{n=0}^{\infty} e^{-n h\nu/(\kB T)} = \frac{1}{1 - e^{-h\nu/(\kB T)}} ,
$$

and its mean energy is minus the derivative of $\ln Z$ with respect to $\beta = 1/(\kB T)$.

:::{admonition} The mean energy of a quantized mode
:class: theorem
A mode of frequency $\nu$ in equilibrium at temperature $T$ holds, on average,

$$
\langle E \rangle = -\frac{\partial \ln Z}{\partial \beta}
= \frac{h\nu}{e^{h\nu/(\kB T)} - 1} ,
$$

that is, a mean number of quanta

$$
\langle n \rangle = \frac{1}{e^{h\nu/(\kB T)} - 1} .
$$
:::

Both limits matter.

- **A cheap quantum, $h\nu \ll \kB T$.** Expanding $e^{x} - 1 \approx x$ gives
  $\langle E \rangle \to \kB T$. This is equipartition: the classical answer is the limit of the
  quantum one when the quantum is small compared with the thermal energy.
- **A dear quantum, $h\nu \gg \kB T$.** The $-1$ is negligible and
  $\langle E \rangle \approx h\nu\, e^{-h\nu/(\kB T)}$: exponentially small. The bath almost never
  supplies a whole quantum at once, and the mode sits in its ground state.

That second limit is the cure, and it is worth saying what it is not. A frozen-out mode is not
still. In its ground state an oscillator keeps its zero-point motion; what it cannot do is accept
energy in amounts smaller than $h\nu$. Freeze-out is unaffordability, not stillness.

### Step 2: counting the modes of a cavity

Take the cavity to be a cube of side $L$ with perfectly reflecting walls. A standing wave must
fit a whole number of half-wavelengths along each edge, so its wave vector is

$$
\mathbf{k} = \frac{\pi}{L}\,(n_x, n_y, n_z) , \qquad n_x, n_y, n_z = 1, 2, 3, \ldots
$$

and its frequency is $\nu = c\,|\mathbf{k}|/(2\pi) = c\,|\mathbf{n}|/(2L)$. Each allowed
$\mathbf{k}$ carries two independent polarizations. Counting modes is counting the points of an
integer lattice. The modes with frequency below $\nu$ are the lattice points inside a sphere of
radius $|\mathbf{n}| = 2L\nu/c$, restricted to the octant where all three integers are positive.
When the radius is large there is one lattice point per unit volume, and the count is the octant's
volume:

$$
N(\nu) = 2 \times \frac{1}{8} \times \frac{4\pi}{3}\left(\frac{2L\nu}{c}\right)^3
= \frac{8\pi V}{3c^3}\,\nu^3 .
$$

:::{admonition} The density of modes in a cavity
:class: theorem
The number of electromagnetic modes with frequency between $\nu$ and $\nu + \mathrm{d}\nu$ in a
cavity of volume $V$ is

$$
g(\nu)\,\mathrm{d}\nu = \frac{8\pi V}{c^3}\,\nu^2\,\mathrm{d}\nu ,
$$

independent of the cavity's shape once it is large compared with the wavelength.
:::

The approximation in "count the volume instead of the points" is checkable, and the laboratory
checks it: the count misses the lattice points on the octant's three flat faces — waves with one
index equal to zero, which exist but carry only one polarization — and the error is a
surface-to-volume ratio, of relative size about $(9/4)/|\mathbf{n}|$. For a $1\ \mathrm{cm}$ cavity
at room temperature the important modes have $|\mathbf{n}|$ of order a thousand.

Now hand every mode the classical $\kB T$. The energy per unit volume per unit frequency is

$$
u_\nu^{\mathrm{RJ}} = \frac{g(\nu)}{V}\,\kB T = \frac{8\pi \nu^2}{c^3}\,\kB T ,
$$

the **Rayleigh–Jeans law**. It describes real cavities well at low frequency. But it grows as
$\nu^2$ without limit, and the total energy is its integral over all frequencies.

:::{admonition} The ultraviolet catastrophe
:class: theorem
In classical physics — equipartition over the modes of the field — the energy density of
cavity radiation is

$$
u = \int_0^\infty \frac{8\pi \nu^2}{c^3}\,\kB T\,\mathrm{d}\nu = \infty
$$

at every temperature above zero. This is a theorem of the classical model, not an
approximation that went wrong: the model has infinitely many modes and gives each the same
energy.
:::

:::{figure} ../media/radiation-catastrophe.mp4
:alt: A plot of energy density per unit frequency against frequency, with a tinted visible band. A blue quantum curve rises, peaks and falls back to zero; a red dashed classical curve, a parabola, rises with it at low frequency and then keeps climbing, leaving the top of the plot. As the temperature rises from 1000 K to 6000 K the blue curve's peak moves to higher frequency, and the two curves agree over a wider range before separating.
:width: 100%

The classical spectrum (red, dashed) against the quantum one (blue) as the temperature rises from
$1000\ \mathrm{K}$ to $6000\ \mathrm{K}$, with the visible band tinted; both are scaled so that the
quantum curve's peak has the same height in every frame. The two agree at low frequency, where a
quantum is cheap and every mode holds close to $\kB T$. Above the peak the quantum curve turns
over, because modes whose quantum exceeds a few $\kB T$ are frozen out; the classical curve does
not, and the area under it is infinite. The frequency where they part company moves up in
proportion to the temperature.
:::

### Step 3: Planck's law, in two variables

The quantum version of the same product, modes per unit volume per unit frequency times mean
energy per mode, is the answer.

:::{admonition} Planck's law
:class: theorem
The energy per unit volume per unit frequency of radiation in equilibrium at temperature $T$ is

$$
u_\nu(\nu, T) = \frac{8\pi \nu^2}{c^3} \cdot \frac{h\nu}{e^{h\nu/(\kB T)} - 1}
= \frac{8\pi h}{c^3}\,\frac{\nu^3}{e^{h\nu/(\kB T)} - 1} .
$$
:::

At low frequency it becomes Rayleigh–Jeans, which is where the classical theory was right. At
high frequency it falls as $\nu^3 e^{-h\nu/(\kB T)}$, which is where the classical theory was
wrong. Planck found the formula in 1900 by fitting measured spectra, and then found the
quantization that produces it; it is the oldest result of quantum physics.

Spectra are also drawn against wavelength. The step from one to the other looks like
substitution, and it is not, because $u_\nu$ is not a function of the radiation alone. It is a
**density**: the energy in a narrow band is $u_\nu\,\mathrm{d}\nu$, and only that product is
physical.

:::{admonition} A spectral density is a density
:class: definition
The **spectral energy density** per unit frequency, $u_\nu$, and per unit wavelength,
$u_\lambda$, are defined by the energy each assigns to the same band of photons:

$$
u_\lambda\,|\mathrm{d}\lambda| = u_\nu\,|\mathrm{d}\nu| ,
\qquad\text{so}\qquad
u_\lambda = u_\nu \left|\frac{\mathrm{d}\nu}{\mathrm{d}\lambda}\right| = u_\nu\,\frac{c}{\lambda^2} .
$$

The factor $c/\lambda^2$, the Jacobian of the change of variable, differs from point to point.
So $u_\lambda$ is not $u_\nu$ relabelled: it is a different curve, with its maximum in a
different place. "The peak of the spectrum" means nothing until the variable is named.
:::

Applied to Planck's law,

$$
u_\lambda(\lambda, T) = \frac{8\pi h c}{\lambda^5}\,\frac{1}{e^{hc/(\lambda \kB T)} - 1} .
$$

Now find both peaks. Per unit frequency, write $x = h\nu/(\kB T)$; then $u_\nu \propto
x^3/(e^x - 1)$, and setting its derivative to zero gives

$$
x = 3\left(1 - e^{-x}\right) , \qquad x = 2.821 ,
$$

so

$$
\nu_{\max} = 2.821\,\frac{\kB T}{h} .
$$

Per unit wavelength, write $y = hc/(\lambda \kB T)$; then $u_\lambda \propto y^5/(e^y - 1)$ — two
more powers, from the Jacobian — and the same calculation gives

$$
y = 5\left(1 - e^{-y}\right) , \qquad y = 4.965 ,
$$

so

$$
\lambda_{\max} T = \frac{hc}{4.965\,\kB} = 2.898 \times 10^{-3}\ \mathrm{m\,K} .
$$

:::{admonition} Wien's displacement law, twice
:class: theorem
The two spectra of the same radiation peak at

$$
\nu_{\max} = 2.821\,\frac{\kB T}{h} , \qquad
\lambda_{\max} = \frac{2.898 \times 10^{-3}\ \mathrm{m\,K}}{T} ,
$$

the frequency peak moving up in proportion to the temperature and the wavelength peak down in
inverse proportion. But they are different photons:

$$
\frac{\nu_{\max}\,\lambda_{\max}}{c} = \frac{2.821}{4.965} = 0.568 ,
$$

at every temperature. The photon at the frequency peak has a wavelength $1/0.568 = 1.76$ times
$\lambda_{\max}$.
:::

For the Sun, at $5772\ \mathrm{K}$: $\lambda_{\max} = 502\ \mathrm{nm}$, green light. But
$\nu_{\max} = 339\ \mathrm{THz}$, the frequency of $883\ \mathrm{nm}$ light — in the infrared,
invisible. Both statements are correct. Neither is "where the Sun's light really peaks", because
there is no such place: the peak belongs to the graph, not to the light. The Jacobian $c/\lambda^2$
is largest at short wavelength, where a nanometre spans many terahertz, so per unit wavelength the
blue end of the spectrum is weighted up and the peak shifts toward it. A third choice —
per unit $\ln \nu$, equal ratios of frequency, which is also per unit $\ln \lambda$ — peaks
between the other two, at $x = 3.921$, $636\ \mathrm{nm}$ for the Sun.

### Step 4: the Stefan–Boltzmann law

The total energy density does not depend on the choice of variable. Integrating Planck's law over
frequency with $x = h\nu/(\kB T)$,

$$
u = \int_0^\infty u_\nu\,\mathrm{d}\nu
= \frac{8\pi (\kB T)^4}{h^3 c^3} \int_0^\infty \frac{x^3}{e^x - 1}\,\mathrm{d}x .
$$

The remaining integral is a pure number. It equals $\pi^4/15 = 6.494$ (it is $6\,\zeta(4)$,
where $\zeta$ is the Riemann zeta function); this module quotes the value and the laboratory
checks it numerically.

:::{admonition} The Stefan–Boltzmann law
:class: theorem
The energy density of equilibrium radiation is

$$
u = a\,T^4 , \qquad a = \frac{8\pi^5 \kB^4}{15\,h^3 c^3} = 7.566 \times 10^{-16}\ \mathrm{J\,m^{-3}\,K^{-4}} ,
$$

and the power leaving unit area of a small hole in the cavity — or of the surface of any
perfectly black body — is

$$
j = \sigma T^4 , \qquad \sigma = \frac{a c}{4} = 5.670 \times 10^{-8}\ \mathrm{W\,m^{-2}\,K^{-4}} .
$$
:::

The factor $c/4$ is kinetic theory's count of what crosses a hole: half the photons next to it
are moving toward the wall, and their mean velocity across it is $c/2$, so the flux is a quarter
of the density times the speed. Stefan found the fourth power in 1879 by reading other
people's measurements, as an empirical law; Boltzmann derived it from thermodynamics in 1884, but
could not get $a$, which needs $h$. The fourth power means that temperature is a powerful lever:
doubling it multiplies the radiated power by sixteen.

Instruments pointed at a source measure the **spectral radiance**, the power per unit area, per
unit frequency, per unit solid angle, $B_\nu = (c/4\pi)\,u_\nu$, in
$\mathrm{W\,m^{-2}\,Hz^{-1}\,sr^{-1}}$. It has the same shape as $u_\nu$.

The number of photons follows the same way, with one power of $x$ fewer:

$$
n = \int_0^\infty \frac{g(\nu)}{V}\,\langle n \rangle\,\mathrm{d}\nu
= 8\pi\left(\frac{\kB T}{hc}\right)^3 \int_0^\infty \frac{x^2}{e^x - 1}\,\mathrm{d}x
= 16\pi\,\zeta(3)\left(\frac{\kB T}{hc}\right)^3 ,
$$

with $\zeta(3) = 1.202$: about $2.03 \times 10^{7}\,T^3$ photons per cubic metre, $T$ in kelvin.
The photon number grows as $T^3$. Photons are not conserved; heating a cavity creates them.

### Step 5: the photon gas

Radiation in a cavity is a gas — of photons — and has a pressure, an entropy and a chemical
potential. Each takes a line.

**Pressure.** Module 04 found the pressure of a gas as a momentum flux: for an isotropic gas,
$P = \tfrac13\,n\,\langle p\,v \rangle$, a third of the density of the product of momentum and
speed. For a nonrelativistic particle $p v = m v^2$, twice the kinetic energy, and $P = \tfrac23 u$.
A photon has $v = c$ and momentum $p = E/c$, so $p v = E$, and

$$
P = \frac{u}{3} = \frac{a T^4}{3} .
$$

It is small at ordinary temperatures — $2\ \mu\mathrm{Pa}$ at $300\ \mathrm{K}$ — and it does
work: compressing the cavity takes $\dbar \Won = -P\,\mathrm{d}V$, positive as the volume
shrinks. That is radiation pressure, the pressure that holds up the most massive stars.

**Entropy.** At fixed volume no work is done, so $\dbar Q = \mathrm{d}U = T\,\mathrm{d}S$
(module 09). The heat capacity is $C_V = \mathrm{d}U/\mathrm{d}T = 4aVT^3$, and integrating
$C_V/T$ up from absolute zero,

$$
S = \int_0^T \frac{4aVT'^3}{T'}\,\mathrm{d}T' = \frac43\,a V T^3 .
$$

Under a slow adiabatic expansion $S$ stays fixed, so $VT^3$ is constant and $T \propto V^{-1/3}$:
radiation cools in inverse proportion to the size of its container. That is why the radiation
left over from the early universe is now at $2.7\ \mathrm{K}$.

**Chemical potential.**

:::{admonition} Photons carry no chemical potential
:class: model-assumption
The walls absorb and emit photons freely, so the number of photons is not conserved: it is not
a constraint but a variable, and at fixed $T$ and $V$ it settles wherever the free energy is
lowest. At that minimum

$$
\mu = \left(\frac{\partial F}{\partial N}\right)_{T,V} = 0 .
$$

The consistency check is the Euler relation of module 09, $U = TS - PV + \mu N$: with
$U = aVT^4$, $TS = \frac43 aVT^4$ and $PV = \frac13 aVT^4$, it holds with $\mu = 0$ exactly. Module
17 generalizes the occupation $\langle n \rangle$ of step 1 to particles whose number *is*
conserved, and finds that $\mu$ then enters it.
:::

### Step 6: the Einstein solid, measured at last

Module 01 let two Einstein solids exchange quanta; module 09 built the Einstein solid's
entropy; module 12 found its temperature from the oscillator partition function. The model was
always the same: $N$ atoms, each vibrating in three directions, as $3N$ independent oscillators
sharing one frequency. Here it finally makes a prediction that a calorimeter can test.

:::{admonition} The Einstein model of a solid
:class: model-assumption
A crystal of $N$ atoms is $3N$ independent harmonic oscillators, all with the same angular
frequency $\omega_E$, each obeying step 1. The **Einstein temperature**
$\theta_E = \hbar\omega_E/\kB$ is the temperature at which the thermal energy equals one quantum.
:::

With $x = \theta_E/T$, step 1 gives each oscillator $\hbar\omega_E/(e^x - 1)$ above its ground
state, so

$$
U = \frac{3N\hbar\omega_E}{e^{\theta_E/T} - 1} ,
$$

and differentiating with respect to $T$:

:::{admonition} The Einstein heat capacity
:class: theorem
In the Einstein model,

$$
C = 3N\kB\, \frac{x^2 e^x}{\left(e^x - 1\right)^2} , \qquad x = \frac{\theta_E}{T} .
$$
:::

This is module 12's oscillator heat capacity multiplied by $3N$; the laboratory checks that the
two are the same function to the last digit. Its limits:

- **Hot, $T \gg \theta_E$.** $C = 3N\kB\left(1 - x^2/12 + \cdots\right) \to 3N\kB$. Per mole,
  $3N_A\kB = 3R = 24.94\ \mathrm{J\,mol^{-1}\,K^{-1}}$.
- **Cold, $T \ll \theta_E$.** $C \approx 3N\kB\,x^2 e^{-x}$: exponentially small, every
  oscillator frozen out.

:::{admonition} The Dulong–Petit law
:class: empirical-law
In 1819 Dulong and Petit found that the heat capacity of many solid elements at room temperature
is close to the same value per mole of atoms, about $25\ \mathrm{J\,mol^{-1}\,K^{-1}}$. Silver
has $25.4$, lead $26.8$. Diamond, with $6.1$, is the conspicuous exception. In the Einstein model
the law is the high-temperature limit, $3R$, and diamond is simply a solid whose room temperature
is not yet "high".
:::

The high-temperature expansion also pays off a debt. Module 01 used a constant heat capacity,
one $\kB$ per oscillator, and warned that it was an approximation. The error is now known: a
fraction $(\theta_E/T)^2/12$ when $T$ is large, $8\%$ at $T = \theta_E$, $28\%$ at
$T = \theta_E/2$. The constant-$C$ picture is safe above about $\theta_E$ and fails, by
exponentially much, well below it.

And the low-temperature limit fails a different test. Measured heat capacities of insulating
crystals do vanish at low temperature, but as $T^3$, not exponentially. An exponential falls far
faster than any power: the Einstein model predicts far too little heat capacity when cold. The
culprit is its one frequency. A real crystal also vibrates slowly — sound waves of long
wavelength — and a mode of low enough frequency is never frozen out.

### Step 7: Debye's repair

The vibrations of a crystal are waves. At long wavelengths they are sound, travelling at a speed
$c_s$, with three polarizations — two transverse, one longitudinal — instead of light's two.
Their quanta are called **phonons**, and like photons their number is not conserved. Debye's
model counts them exactly as step 2 counted photons, with $c_s$ in place of $c$ and three
polarizations in place of two. In angular frequency,

$$
g(\omega)\,\mathrm{d}\omega = \frac{3V}{2\pi^2 c_s^3}\,\omega^2\,\mathrm{d}\omega .
$$

A crystal of $N$ atoms has only $3N$ modes — a wave shorter than twice the atomic spacing is no
new motion — so Debye cuts the spectrum off at the frequency $\omega_D$ where the count reaches
$3N$:

$$
\int_0^{\omega_D} g(\omega)\,\mathrm{d}\omega = 3N
\qquad\Longrightarrow\qquad
\omega_D^3 = 6\pi^2\,\frac{N}{V}\,c_s^3 ,
\qquad \theta_D = \frac{\hbar\omega_D}{\kB} .
$$

Summing step 1 over this spectrum and differentiating, with $x = \hbar\omega/(\kB T)$:

:::{admonition} The Debye heat capacity
:class: theorem
In the Debye model, with **Debye temperature** $\theta_D$,

$$
C = 9N\kB \left(\frac{T}{\theta_D}\right)^3 \int_0^{\theta_D/T} \frac{x^4 e^x}{\left(e^x - 1\right)^2}\,\mathrm{d}x .
$$

The integral has no closed form at intermediate temperatures and is evaluated numerically.
:::

- **Hot, $T \gg \theta_D$.** The integrand is $x^2$ over a short range, the integral is
  $(\theta_D/T)^3/3$, and $C \to 3N\kB$: Dulong–Petit again, with a correction
  $1 - (\theta_D/T)^2/20$.
- **Cold, $T \ll \theta_D$.** The upper limit can be taken to infinity, where the integral is
  $4\pi^4/15$.

:::{admonition} The Debye T³ law
:class: approximation
Well below the Debye temperature — in practice below about $\theta_D/50$ —

$$
C \approx \frac{12\pi^4}{5}\,N\kB \left(\frac{T}{\theta_D}\right)^3 .
$$

Per mole, the coefficient $\tfrac{12\pi^4}{5}R$ is $1944\ \mathrm{J\,mol^{-1}\,K^{-1}}$.
:::

The $T^3$ has a direct explanation. At low $T$ only modes with $\hbar\omega \lesssim \kB T$ are
active; there are about $(\kB T/\hbar c_s)^3 V$ of them, as for photons; each holds about $\kB T$.
So $U \propto T^4$ and $C \propto T^3$ — the Stefan–Boltzmann law of sound.

:::{admonition} Two one-parameter caricatures
:class: approximation
Neither model is the real crystal. A real phonon spectrum has several branches whose speeds
depend on direction and wavelength, with peaks and gaps that neither model has. Einstein puts
every mode at one frequency; Debye replaces the true spectrum by the long-wavelength sound
spectrum, cut off. Debye wins at low temperature for one reason — low-frequency modes exist, and
Einstein's model has none. At high temperature the two agree whenever
$\theta_E^2 = \tfrac35\,\theta_D^2$, because both corrections are
$1 - \langle(\hbar\omega/\kB T)^2\rangle/12$, and Debye's mean of $\omega^2$ is
$\tfrac35\,\omega_D^2$. The honest measure of either model is how much its one parameter has to
drift to fit data at different temperatures.
:::

:::{figure} ../media/radiation-solids.mp4
:alt: Heat capacity divided by 3R against temperature from 0 to 300 K, with black data points for silver rising and levelling off below a dashed line at 1. A blue Debye curve and a red Einstein curve sweep across the points as their temperatures change, both levelling off at the dashed line. Then the axes switch to logarithmic: at low temperature the black points fall on a straight line down to 1 K, the blue curve follows them, and the red curve plunges far below them under about 30 K, leaving the bottom of the plot.
:width: 100%

The Debye model (blue) and the Einstein model (red) against silver's measured heat capacity
(black, the electrons' $\gamma T$ removed), divided by $3R$. The Debye temperature sweeps from
$120$ to $320\ \mathrm{K}$ and settles at $218\ \mathrm{K}$; the Einstein temperature is tied to it
by $\theta_E = \sqrt{3/5}\,\theta_D$, so that the two models agree when hot. On linear axes the two
curves differ only near the foot of the rise, and either looks like a fair description. Then the
axes switch to logarithmic. Now
the measurements below about $10\ \mathrm{K}$ fall on a straight line of slope $3$ down to
$1\ \mathrm{K}$, Debye follows them, and Einstein falls away exponentially below about
$30\ \mathrm{K}$ — about $550$ times too low at $10\ \mathrm{K}$, and off the bottom of the plot
soon after. A linear plot hides the difference that decides between the models.
:::

Two corrections stand between these models and a table of measurements.

:::{admonition} What a calorimeter measures
:class: approximation
Tables give $C_P$, the models give $C_V$, and module 10 related them:
$C_P - C_V = TV\alpha^2/\kappa_T$, which vanishes as $T \to 0$. For silver it is about $1\%$ of
$C$ at $100\ \mathrm{K}$ and $4\%$ at room temperature. In a metal the conduction electrons add
a heat capacity $\gamma T$, linear in temperature; it is negligible above a few tens of kelvin,
and below about $2\ \mathrm{K}$ it is larger than the lattice's $T^3$. A fair test of either model
therefore uses the range between.
:::

(16-radiation-solids-verify)=
## Verify computationally

Every number below comes from `thermolab.radiation`. Nothing in this module is random; the
numbers are deterministic. The uncertainties quoted for the silver fits come from the scatter
of the data about the model curve; the one for the microwave background comes from the
published measurement errors. The laboratory repeats each experiment.

**1. The occupation, rebuilt from module 12's sum.** For a mode with quantum
$4 \times 10^{-21}\ \mathrm{J}$, the closed form $\langle n \rangle = 1/(e^{x} - 1)$ and an
explicit Boltzmann sum over $4000$ levels, using module 12's code, agree to $10^{-12}$ at
$30$, $300$ and $3000\ \mathrm{K}$. Step 1's formula is module 12's partition function, nothing
added.

**2. Counting standing waves one by one.** Enumerating the integer triples in a cube, mode by
mode, and comparing with the smooth count $8\pi V\nu^3/(3c^3)$: the explicit count falls short by
$11.2\%$ at $|\mathbf{n}| = 20$, $2.8\%$ at $80$ and $0.70\%$ at $320$. The shortfall halves
each time the radius doubles — the missing face modes, about $(9/4)/|\mathbf{n}|$ — and the
smooth formula is its limit.

**3. The Stefan–Boltzmann law by quadrature.**

:::{admonition} The T⁴ law and its constant, numerically
:class: numerical-observation
Integrating Planck's law over frequency by Simpson's rule on a uniform grid, with no reference to
$\zeta(4)$, reproduces $aT^4$ to a relative error of $6 \times 10^{-11}$ with $4096$ intervals.
The error falls by a factor of $16.0$ each time the grid is halved: the fourth-order convergence
Simpson's rule should give. A log–log fit of the integrated energy against temperature, from
$100$ to $3000\ \mathrm{K}$, has slope $4$ to within $3 \times 10^{-15}$. The number $\pi^4/15$ in the
closed form is confirmed, not assumed.
:::

**4. One energy, two densities, two peaks.** Integrating $u_\lambda$ over wavelength — a different
variable, on a logarithmic grid, sharing nothing with item 3's grid — reproduces $aT^4$ to
$10^{-16}$, and so agrees with item 3's frequency integral to that integral's own error,
$6 \times 10^{-11}$, at $2.725$, $300$ and $5772\ \mathrm{K}$. A brute-force search over $200\,001$ points
finds the maximum of $u_\nu$ at $2.8214\,\kB T/h$ and of $u_\lambda$ at
$hc/(4.9651\,\kB T)$; their product is $0.5683\,c$ at every temperature. The energy agrees and the
peaks do not, which is exactly what a density does.

**5. Hotter is not brighter.** Doubling the temperature from $300$ to $600\ \mathrm{K}$ multiplies
the integrated energy by $16.000$. At fixed frequency, though, the ratio of the two spectra is not
one number: it is $2$ at the low-frequency end, where both curves follow Rayleigh–Jeans, $120$ at
$60\ \mathrm{THz}$, and it grows without limit in the far tail, where the hotter body has photons
the colder one cannot afford. No
vertical rescaling turns one curve into the other. The peak moves, from $9.66$ to
$4.83\ \mu\mathrm{m}$.

**6. The two solids, against each other.** Both heat capacities reach $3N\kB$ at high
temperature, Einstein as $1 - x^2/12$ and Debye as $1 - x^2/20$, each confirmed to fourth order.
In the cold, the log–log slope of the Debye curve below $\theta_D/50$ is $3$ to within
$10^{-15}$, and the curve equals the $T^3$ law there to $10^{-11}$. Over the window $\theta/40$
to $\theta/10$ the Einstein curve's slope is about $19$. The models are told apart by a slope.

**7. Against reality: silver.** The data are the recommended heat capacities of silver from
$1$ to $300\ \mathrm{K}$ tabulated by the US National Institute of Standards and Technology
(Smith and Fickett, 1995), converted to a mole.

:::{figure} ../media/radiation-data.png
:alt: Two panels. Left, a log-log plot of the heat capacity of silver against temperature from 1 K to 300 K: black data points rise steeply and level off near a dashed horizontal line at 3R. A blue Debye curve follows the points from about 4 K upward; a red Einstein curve falls far below them at low temperature. Below it, a strip of residuals shows the blue points within about 10 percent and the red points plunging to minus 100 percent at low temperature. Right, the cosmic microwave background spectrum against frequency: black points on a blue Planck curve that peaks near 5.3 inverse centimetres, with a residual strip below scattered around zero.
:width: 100%

Left: silver's molar heat capacity $C_P$ (black points), with the electrons' $\gamma T$ subtracted,
against the best Debye curve (blue, $\theta_D = 218\ \mathrm{K}$) and the best Einstein curve
(red, $\theta_E = 123\ \mathrm{K}$), both fitted between $4$ and $100\ \mathrm{K}$; the dashed
line is $3R$. The strip beneath shows each model's fractional residual. Right: the cosmic
microwave background measured by COBE's FIRAS instrument (black points; their error bars,
smaller than the points, are not drawn) and the fitted Planck curve (blue), with the residuals beneath, magnified, in units
of each point's uncertainty.
:::

- **The low-temperature line.** Below $6\ \mathrm{K}$, $C/T$ plotted against $T^2$ is a straight
  line, $C/T = \gamma + \beta T^2$: the electrons' term plus Debye's $T^3$. Its intercept is
  $\gamma = 0.651\ \mathrm{mJ\,mol^{-1}\,K^{-2}}$, within $1.5\%$ of the paper's $0.641$, and its
  slope $\beta = 0.1685\ \mathrm{mJ\,mol^{-1}\,K^{-4}}$ gives, through
  $\beta = \tfrac{12\pi^4}{5}R/\theta_D^3$, a Debye temperature $\theta_D = 226.0\ \mathrm{K}$
  against the paper's $226.6\ \mathrm{K}$.
- **The slope.** With that $\gamma T$ subtracted, the log–log slope of the data between $1$ and
  $5\ \mathrm{K}$ is $3.00$: Debye's $T^3$. Without the subtraction it is $1.87$
  between $1$ and $3\ \mathrm{K}$, because the electrons' share is large there — $80\%$ of the heat
  capacity at $1\ \mathrm{K}$, half at $2\ \mathrm{K}$. That is the model specification's failure mode for metals,
  visible in real numbers.
- **The fits.** Fitting each model's one parameter to the lattice heat capacity between $4$ and
  $100\ \mathrm{K}$ by least squares on fractional residuals: Debye gives
  $\theta_D = 218.5 \pm 1.1\ \mathrm{K}$ with a root-mean-square residual of $6\%$ and none worse
  than $11\%$. Einstein gives $\theta_E = 123 \pm 5\ \mathrm{K}$ with a root-mean-square residual
  of $55\%$; at $4\ \mathrm{K}$ it predicts essentially nothing, and at $10\ \mathrm{K}$ a tenth of
  what is measured. The data reject Einstein at low temperature and accept Debye — to within
  $10\%$, not to within the data's precision.
- **The drift.** Solving the Debye formula for the $\theta_D$ that reproduces each measured point
  gives $226\ \mathrm{K}$ below $6\ \mathrm{K}$, $210\ \mathrm{K}$ at $25\ \mathrm{K}$ and
  $215\ \mathrm{K}$ at $80\ \mathrm{K}$. A one-parameter model fits the whole curve only by
  letting its parameter wander by $7\%$: this is the real phonon spectrum showing through the
  caricature, and the reason a fitted $\theta_D$ should be quoted with the temperature range it
  came from.

**8. Against reality: the cosmic microwave background.** COBE's FIRAS instrument measured the
radiation filling the universe at $43$ frequencies between $68$ and $640\ \mathrm{GHz}$. A
one-parameter fit of Planck's law, in radiance, gives
$T = 2.725\,015 \pm 0.000\,008\ \mathrm{K}$, with $\chi^2 = 45.1$ for $42$ degrees of freedom: a
Planck curve is the right shape, within the measurement's precision. All but the two noisiest
points sit within $60\ \mathrm{kJy\,sr^{-1}}$ of the curve, $1.5$ parts in $10^4$ of its peak.
Two cautions belong with the number. The quoted uncertainty is statistical only, and the
$\chi^2$ treats the published errors as independent, which they are not quite; FIRAS's
calibration limits the absolute temperature to $2.72548 \pm 0.00057\ \mathrm{K}$. And the archive
builds its spectrum column as a $2.725\ \mathrm{K}$ Planck curve plus the measured residuals, so a
fit recovers the temperature the residuals were taken against: what this data set tests is the
*shape*, and the shape is Planck's law. FIRAS plots its spectrum per unit frequency, where it
peaks at $160\ \mathrm{GHz}$, a wavelength of $1.87\ \mathrm{mm}$; per unit wavelength the same
radiation peaks at $1.06\ \mathrm{mm}$.

**9. Diamond and lead, at room temperature.** Measured at $298\ \mathrm{K}$, diamond's heat
capacity is $6.12\ \mathrm{J\,mol^{-1}\,K^{-1}}$ (DeSorbo, 1953; Victor, 1962) — $25\%$ of
Dulong–Petit — and lead's is $26.84$ (NIST-JANAF), $8\%$ *above* it, the excess being
$C_P - C_V$ and anharmonicity. Diamond's light atoms and stiff bonds give it a Debye temperature
near $2230\ \mathrm{K}$ from low-temperature data; lead's is about $105\ \mathrm{K}$. With those
values the Debye model puts diamond at $16\%$ of $3R$ at room temperature, too low: the
$\theta_D$ that reproduces the room-temperature value is $1860\ \mathrm{K}$. Diamond's Debye
temperature drifts with $T$ too.

**The falsifying experiments.** Each misconception this module confronts has a measurement above
that it cannot survive. "The peak of the spectrum is a property of the radiation": item 4, where
the two peaks differ by a factor $0.568$ at every temperature while the energies agree to
$6 \times 10^{-11}$, and item 8, where the cosmic background peaks at $1.87$ or $1.06\ \mathrm{mm}$
depending on the axis. "Hotter bodies are brighter versions of the same spectrum": item 5, where
doubling $T$ multiplies the energy by sixteen while the ratio of the two spectra runs from $2$
upward without limit. "A cold solid's atoms stop moving, so it stores no heat": items 6 and 7 — the heat
capacity vanishes as the quanta become unaffordable, at a rate set by how many cheap modes the
crystal has, while the zero-point motion that step 1 set aside persists at absolute zero.

(16-radiation-solids-transfer)=
## Transfer the idea

One idea — energy in quanta, so expensive modes freeze out — did two jobs in this module. It
travels much further.

- **Back to module 12.** Step 1 *is* module 12's oscillator: the occupation is
  $-\partial \ln Z/\partial\beta$ divided by the quantum. Module 12 called the cold limit
  freeze-out and predicted that it would rescue the solid; here it rescues radiation too.
- **Back to modules 01 and 09.** The Einstein solid's spiral closes. Module 01 exchanged its
  quanta and assumed a constant heat capacity; module 09 built its entropy; module 12 read its
  temperature from $Z$. Here the same model predicts a curve that a calorimeter measures, and its
  failure at low temperature is what sends us to Debye. Module 01's constant-$C$ approximation is
  now quantified: safe above $\theta_E$, wrong by $28\%$ at $\theta_E/2$.
- **Back to modules 04 and 06.** Equipartition is the high-temperature limit of step 1. The
  freeze-out caveat modules 04 and 06 attached to it — why air's vibrations do not count at room
  temperature — is the same exponential. Module 04's momentum-flux argument gave $P = u/3$ for
  photons with one change, $p = E/c$.
- **Back to module 10.** $C_P - C_V = TV\alpha^2/\kappa_T$ is why a table of $C_P$ can exceed
  Dulong–Petit at room temperature, as lead's does.
- **Forward to module 17.** The occupation $1/(e^{h\nu/(\kB T)} - 1)$ is the Bose–Einstein
  distribution with $\mu = 0$. Module 17 derives the general case, for particles whose number is
  conserved, and its verification recomputes this module's Planck curve from that general formula.
  The photon gas returns there as the example of a gas that cannot condense.
- **Module 18** owes this module nothing; transport of heat by radiation and by phonons is not
  treated there.
- **Pyrometry.** A pyrometer measures the temperature of a furnace or a star from its colour —
  from the shape of its spectrum, not its brightness, which also depends on distance and
  emissivity. Every pyrometer has to say which spectral variable its "peak" uses.
- **Thermal imaging.** A human body at $310\ \mathrm{K}$ radiates most strongly per unit
  wavelength near $9.3\ \mu\mathrm{m}$; thermal cameras are built for the band from $8$ to
  $14\ \mu\mathrm{m}$ for that reason.
- **The incandescent lamp.** A tungsten filament at $2800\ \mathrm{K}$ puts $8\%$ of its radiation
  into the visible band, $380$ to $750\ \mathrm{nm}$; the rest is infrared, which is why such
  lamps are inefficient and were phased out. Sunlight, at $5772\ \mathrm{K}$, puts $44\%$ there.
  Eyes evolved under the Sun.
- **The early universe.** The cosmic microwave background is the most perfect blackbody ever
  measured. Its spectrum shows that the universe was once hot, dense and in equilibrium; its
  temperature, $2.7\ \mathrm{K}$, falls as the universe expands, as step 5 requires of radiation
  expanding adiabatically.

Looking ahead:

- **Module 17** takes the occupation of step 1 to particles that cannot be created or
  destroyed — atoms, electrons — and finds Bose–Einstein condensation and the Fermi sea.
- **Module 18** turns from equilibrium to how it is reached: fluctuations, and the transport they
  drive.

### Worked examples

Try each one before opening its solution.

**Worked example 1 — the Sun's two peaks.** The Sun's surface radiates as a blackbody at
$5772\ \mathrm{K}$. Find the wavelength at which $u_\lambda$ peaks, and the frequency at which
$u_\nu$ peaks. What wavelength of light has that frequency?

:::{dropdown} Solution
$\lambda_{\max} = 2.898 \times 10^{-3}/5772 = 502\ \mathrm{nm}$. $\nu_{\max} = 2.821\,\kB T/h =
2.821 \times 1.381 \times 10^{-23} \times 5772/6.626 \times 10^{-34} = 3.39 \times 10^{14}\ \mathrm{Hz}$,
the frequency of light of wavelength $c/\nu_{\max} = 883\ \mathrm{nm}$, in the near infrared. The
ratio $502/883 = 0.568$, as it must be at any temperature.
:::

**Worked example 2 — an oven, doubled.** An oven's walls are raised from $300$ to
$600\ \mathrm{K}$. By what factor does the power they radiate grow, and where does the spectrum
per unit wavelength peak before and after?

:::{dropdown} Solution
Power scales as $T^4$: $2^4 = 16$. The peak moves from $2.898 \times 10^{-3}/300 =
9.66\ \mu\mathrm{m}$ to $4.83\ \mu\mathrm{m}$. A spectrum that only got brighter would have kept
its peak and grown by a factor of $2$, the ratio of temperatures — which is what it does at the
far infrared end, and nowhere else.
:::

**Worked example 3 — the photons in a room.** How many photons are there in a cubic centimetre
of a room at $300\ \mathrm{K}$, and in a cubic centimetre of intergalactic space, filled with the
$2.725\ \mathrm{K}$ background? What is a background photon's mean energy?

:::{dropdown} Solution
$n = 2.03 \times 10^{7}\,T^3\ \mathrm{m^{-3}}$ gives $5.5 \times 10^{14}\ \mathrm{m^{-3}}$ at
$300\ \mathrm{K}$, $5.5 \times 10^{8}$ per cubic centimetre, and $4.1 \times 10^{8}\ \mathrm{m^{-3}}$
— $411$ per cubic centimetre — at $2.725\ \mathrm{K}$. The mean energy per photon is
$u/n = (\pi^4/30\zeta(3))\,\kB T = 2.70\,\kB T$, $6.3 \times 10^{-4}\ \mathrm{eV}$ for the
background.
:::

**Worked example 4 — module 01's constant heat capacity.** Module 01 treated an Einstein solid as
having $C = \kB$ per oscillator. What fraction of that does the Einstein model give at
$T = \theta_E/2$, at $T = \theta_E$ and at $T = 5\theta_E$?

:::{dropdown} Solution
$C/(3N\kB) = x^2 e^x/(e^x - 1)^2$. At $x = 2$: $4 \times 7.389/6.389^2 = 0.724$. At $x = 1$:
$0.921$. At $x = 0.2$: $0.9967$, against the series $1 - 0.04/12 = 0.9967$. Module 01's
approximation is good to $8\%$ at $T = \theta_E$ and degrades quickly below it.
:::

**Worked example 5 — silver at 4 K.** From $\theta_D = 226\ \mathrm{K}$ and
$\gamma = 0.641\ \mathrm{mJ\,mol^{-1}\,K^{-2}}$, predict silver's molar heat capacity at
$4\ \mathrm{K}$, and compare with the tabulated $0.0134\ \mathrm{J\,mol^{-1}\,K^{-1}}$.

:::{dropdown} Solution
Lattice: $1944 \times (4/226)^3 = 1944 \times 5.54 \times 10^{-6} = 0.0108\ \mathrm{J\,mol^{-1}\,K^{-1}}$.
Electrons: $0.641 \times 10^{-3} \times 4 = 0.0026$. Total $0.0133$, against $0.0134$ measured.
Without the electrons the prediction would be $20\%$ low; at this temperature they are a fifth of
the answer.
:::

**Worked example 6 — the Sun's power.** The Sun's radius is $6.957 \times 10^8\ \mathrm{m}$ and its
surface temperature $5772\ \mathrm{K}$. Estimate its luminosity.

:::{dropdown} Solution
$L = 4\pi R^2 \sigma T^4 = 4\pi (6.957 \times 10^8)^2 \times 5.670 \times 10^{-8} \times 5772^4 =
3.83 \times 10^{26}\ \mathrm{W}$. The value adopted by the International Astronomical Union is
$3.828 \times 10^{26}\ \mathrm{W}$ — not a coincidence: the Sun's "effective temperature"
$5772\ \mathrm{K}$ is *defined* as the blackbody temperature that radiates its measured power.
:::

:::{note} Your predictions, revisited
1. **Sixteen.** Total power scales as $T^4$. See step 4 and item 5 of the verification.
2. **No.** Per unit frequency the Sun peaks at $339\ \mathrm{THz}$, the frequency of
   $883\ \mathrm{nm}$ light, not $600\ \mathrm{THz}$. The two peaks are different photons at every
   temperature, because a spectral density is a density. See step 3.
3. **By orders of magnitude.** With diamond's $\theta_D \approx 2230\ \mathrm{K}$, the Debye model
   gives a drop of about $870$ between $300$ and $30\ \mathrm{K}$ — close to the $1000$ of a pure
   $T^3$ law. An Einstein model with $\theta_E = 1310\ \mathrm{K}$, the value that matches
   diamond at room temperature, would give a factor of $10^{15}$; real diamond follows Debye.
4. **No — it grows eightfold.** The photon number scales as $T^3$, because photons are created by
   the walls, not conserved. See step 4.
:::

(16-radiation-solids-quiz)=
## Check your understanding

```{include} ../_generated/quiz-16-radiation-solids.md
```

Exam-style problems for this module — the ones worth doing with a pen — are collected in
[the problem set](16-radiation-solids-problems.md).

(16-radiation-solids-explain)=
## Explain it in your own words

Answer in a few sentences each.

1. Why is "the peak of the blackbody spectrum" not a well-posed quantity until a spectral
   variable is named? What *is* well-posed?
2. A solid's heat capacity falls to zero at low temperature, yet its atoms never stop moving.
   Explain both halves of that sentence.
3. Name the one classical assumption behind both the ultraviolet catastrophe and the failure of
   Dulong–Petit at low temperature, and explain how a single change to it rescues both.
4. In one sentence: why do photons have zero chemical potential?

(16-radiation-solids-advanced)=
## Advanced: a planet's energy balance

:::{admonition} Advanced — safe to skip on a first pass
:class: advanced
Nothing in the core sequence, or in later modules, depends on this section. It applies the
Stefan–Boltzmann law and Wien's law to the simplest model of a planet with an atmosphere.
:::

**The bare planet.** The Earth intercepts sunlight with its cross-section, $\pi R^2$, and radiates
from its whole surface, $4\pi R^2$. The **solar constant**, the flux of sunlight at the Earth's
distance, is $S = 1361\ \mathrm{W\,m^{-2}}$, and the planet reflects a fraction $A \approx 0.3$ of
it, its **albedo**. If the surface radiates as a blackbody at a single temperature $T_e$,
balancing what is absorbed against what is emitted,

$$
\sigma T_e^4 = \frac{(1 - A)\,S}{4} = 238\ \mathrm{W\,m^{-2}} ,
\qquad T_e = 255\ \mathrm{K} .
$$

That is $-19\,{}^\circ\mathrm{C}$. The measured mean surface temperature is about
$288\ \mathrm{K}$, $15\,{}^\circ\mathrm{C}$.

**One absorbing layer.** Add an atmosphere idealized as a single layer that lets sunlight through
and absorbs all thermal radiation. Wien's law is what makes the idealization reasonable: sunlight
peaks per unit wavelength near $0.5\ \mu\mathrm{m}$, a $255\ \mathrm{K}$ planet near
$11\ \mu\mathrm{m}$, and gases such as water vapour and carbon dioxide absorb strongly in the
second range and hardly in the first. The layer, at temperature $T_a$, radiates both up and down.
In equilibrium the top of the layer must emit to space what the planet absorbs, and the layer must
emit as much as it receives from the surface:

$$
\sigma T_a^4 = \frac{(1 - A)\,S}{4} ,
\qquad
\sigma T_s^4 = 2\,\sigma T_a^4 ,
$$

so $T_a = T_e$ and the surface sits at $T_s = 2^{1/4}\,T_e = 303\ \mathrm{K}$: warmer, because it
receives the layer's downward radiation as well as the Sun's. With $n$ such layers,
$T_s = (n + 1)^{1/4}\,T_e$.

:::{admonition} The greenhouse effect, as a toy
:class: model-assumption
Each layer is perfectly transparent to sunlight, perfectly black to thermal radiation, and at a
single temperature; heat moves only by radiation. A real atmosphere absorbs in bands — there is a
"window" from about $8$ to $13\ \mu\mathrm{m}$, near the peak of the Earth's emission, where it is
largely transparent — and carries heat upward by convection and by evaporating water. The toy
brackets the truth: no layer gives $255\ \mathrm{K}$, one black layer $303\ \mathrm{K}$, and the
real surface is at $288\ \mathrm{K}$.
:::

The toy explains the mechanism: an absorbing layer does not trap heat by blocking it, but by
re-emitting it at a temperature lower than the surface's, so that the planet must warm until the
top layer radiates enough. Adding absorbers raises the altitude from which the planet radiates to
space; because the atmosphere is colder higher up, that altitude must warm.

:::{admonition} What is still open here
:class: open-question
How much the Earth's surface eventually warms for a doubling of atmospheric carbon dioxide — the
equilibrium climate sensitivity — is not settled by radiation alone. The radiative part is well
understood: doubling CO₂ adds about $4\ \mathrm{W\,m^{-2}}$, roughly $1.2\ \mathrm{K}$ of warming
by itself. The rest comes from feedbacks — water vapour, the reflectivity of ice, and above all
clouds, whose response is the largest uncertainty. The Intergovernmental Panel on Climate Change
assessed the likely range in 2021 as $2.5$ to $4\ \mathrm{K}$, with a best estimate of $3\ \mathrm{K}$.
:::
