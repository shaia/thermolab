# Module 17 — Quantum statistics — Implementation Plan

> **Brainstorm:** §3 module 17 (+ §1 audience QM-budget promise, §5 blackbody laboratory
> tie-back, §6 misconceptions, §7 accuracy framework). **Module id:** `17-quantum-gases`.
> **Content path:** `content/en/advanced/17-quantum-gases.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

The course keeps asking how predictable macroscopic behaviour emerges from uncertain microscopic
behaviour — but until now the microscopic actors were merely *anonymous*. This module makes them
*identical* in the full quantum sense, and one postulate splits the world in two: a
single-particle state holds any number of bosons but at most one fermion. Nothing else is added —
no wavefunctions, no operators — yet two entire thermodynamics fall out: helium-4 atoms piling by
the mole into one state, and conduction electrons stacked into a Fermi sea whose effective
"thermal" energy is tens of thousands of kelvin at T = 0.

The through-line: **the classical world is a corner of the quantum one.** All three occupation
functions — Maxwell–Boltzmann, Bose–Einstein, Fermi–Dirac — collapse onto one curve when
$e^{(\varepsilon-\mu)/\kB T} \gg 1$, and the criterion for living in that corner is
$n \lambda_{\mathrm{th}}^3 \ll 1$. This cashes in module 13's IOU (the quantum concentration
$n_Q$ was *named* there, it is *derived* here), generalizes 13's independent-site grand-canonical
trick to every single-particle mode, reuses 12's geometric-series muscle for the boson mode sum,
and closes conflict C4b: 16's Planck curve is re-derived in one line as Bose–Einstein occupation
at $\mu = 0$ times the photon mode density — one occupation function, two chapters.

Beyond the brainstorm row, the plan pins the transfer application to conduction electrons in
metals (resolving the "missing" electronic heat capacity that Dulong–Petit-era physics could not
explain, and completing 16's solids story with the low-T $\gamma T$ term), continues the
honest-miss pattern (ideal-gas $T_c$ vs helium-4's measured lambda point), and holds the QM
budget to the course promise: state counting and the symmetry postulate yes, Schrödinger no.
This is the course's quantum capstone; 18 borrows only its vocabulary.

## 2. Position in the course

- **Requires:** `11-ensembles` — the Boltzmann factor $e^{-\varepsilon/\kB T}$ from the
  finite-bath argument; `12-partition-functions` — the Z machinery and the harmonic-oscillator
  geometric sum (reused verbatim as the boson mode sum); `13-chemical-potential` — $\mu$ as the
  particle-exchange price, the grand-canonical independent-site trick, the classical
  $\mu = \kB T \ln(n/n_Q)$ with $n_Q$ named but not derived; `16-radiation-solids` — mode
  counting in a box, `radiation.planck_u_nu` as the verify target, Debye $T^3$ for the metal
  heat-capacity link; `02-equations-of-state` — `gases.py` ideal law for classical comparisons.
- **Feeds:** `18-fluctuations-transport` lightly — degenerate-gas vocabulary and the Fermi
  velocity for transport estimates; course-end synthesis problems. Terminal otherwise.
- **Explicitly not assumed:** the Schrödinger equation, wavefunctions, operators (the §1 QM
  budget — banned from the prose); second quantization; interparticle interactions (ideal gases
  only, stated as a model assumption); band theory (the free-electron box is the only metal).

## 3. Module specification

- **Identity and scope** — brainstorm row 17 in full: Bose–Einstein and Fermi–Dirac
  distributions, BEC, degenerate Fermi gas; centrepiece "compare classical, Bose and Fermi
  occupation functions". Covered: symmetry postulate, single-mode grand-canonical occupations,
  3-D density of states, $\mu(T; N)$ solver story, BEC saturation and condensate fraction,
  Fermi energy / degeneracy pressure / electronic heat capacity sketch, classical-limit
  criterion. Deferred: interactions and real condensates (out of course scope, honesty check
  only); transport in degenerate gases → 18; full Sommerfeld expansion → advanced section.
- **Prerequisites** — 11: Boltzmann factor; 12: geometric series for oscillator Z; 13: $\mu$,
  grand-canonical single-site sum, classical ideal-gas $\mu$; 16: box mode counting and
  `planck_u_nu`; 02: ideal EOS for pressure comparisons.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-17-1`: State the symmetry postulate — a single-particle state holds any number of
    identical bosons but at most one identical fermion — and count the two-particle states of
    a two-level system under classical, Bose and Fermi rules (4 / 3 / 1).
  - `OBJ-17-2`: Derive the mean occupations n_BE = 1/(exp((eps - mu)/(k_B T)) - 1) and
    n_FD = 1/(exp((eps - mu)/(k_B T)) + 1) from the grand-canonical sum over one mode, and
    explain why a boson gas requires mu < eps_0 while n_FD needs no such bound.
  - `OBJ-17-3`: Show both occupations reduce to n_MB = exp(-(eps - mu)/(k_B T)) when
    exp((eps - mu)/(k_B T)) >> 1, and state the classical-limit criterion
    n lambda_th^3 << 1 with lambda_th = h/sqrt(2 pi m k_B T).
  - `OBJ-17-4`: Count states in a 3-D box to obtain g(eps) proportional to sqrt(eps), and use
    N = integral of g(eps) n(eps) d eps to determine mu(T; N) numerically, predicting its
    direction of travel as T falls for classical, Bose and Fermi gases.
  - `OBJ-17-5`: Explain BEC as saturation of the excited states — below
    T_c = (2 pi hbar^2 / (m k_B)) (n / zeta(3/2))^(2/3) the integral maxes out and the ground
    state takes the overflow, with N_0/N = 1 - (T/T_c)^(3/2).
  - `OBJ-17-6`: Compute eps_F = (hbar^2/(2m)) (3 pi^2 n)^(2/3), T_F = eps_F/k_B, the
    ground-state energy U = (3/5) N eps_F and the degeneracy pressure P = (2/5) n eps_F of an
    ideal Fermi gas, and compare P to the classical n k_B T at the same density.
  - `OBJ-17-7`: Explain why the electronic heat capacity of a metal is linear in T and small
    at room temperature — only the ~k_B T shell around eps_F can be excited — and estimate
    C_el/C_classical ~ T/T_F.
  - `OBJ-17-8`: Recompute the Planck spectral energy density as the mu = 0 Bose–Einstein
    occupation times the photon density of modes, and explain why photons have mu = 0
    (their number is not conserved).
- **Mathematical background** — already has: geometric series (12), constrained sums and
  Lagrange-free grand-canonical reasoning (13), improper integrals (16's Stefan–Boltzmann).
  New here: 1-D root finding as a physics tool ($\mu$ from fixed N); the dimensionless
  substitution $x = \varepsilon/\kB T$ turning $N$-integrals into pure numbers ($\zeta(3/2)$).
- **Physical intuition goals** — student can predict, without algebra: (1) at the same
  $(\varepsilon-\mu)/\kB T$ the occupations order BE > MB > FD, and all three merge when that
  argument is large; (2) cooling an electron gas to T = 0 does *not* stop it — mean kinetic
  energy tends to $(3/5)\varepsilon_F$, not zero; (3) classical vs quantum is decided by
  density as much as temperature — room-temperature electrons in copper are deeply quantum;
  (4) below $T_c$ a Bose gas still has pressure and excitations — condensation is an
  occupation statement, not an arrest.
- **Section skeleton seeds** — contract order:
  - *puzzle:* the conduction electrons in this laptop refuse to share a state even at absolute
    zero — their effective "thermal" energy is tens of thousands of kelvin. Helium-4 atoms,
    cooled far enough, do the opposite: they pile into a single quantum state by the mole.
    Boxed question: identical particles, opposite social behaviour — and classical statistics
    predicted neither. What decides?
  - *predict:* (1) cool an electron gas toward T = 0 — does the average kinetic energy go to
    zero as equipartition says? (2) rank $n_{\mathrm{MB}}$, $n_{\mathrm{BE}}$,
    $n_{\mathrm{FD}}$ at the same $(\varepsilon-\mu)/\kB T$; (3) are the electrons in copper
    at 300 K classical or quantum — and is that decided by T or by density? (targets
    `quantum-only-cold`); (4) below $T_c$, does the Bose gas still exert pressure? (targets
    `bec-atoms-stop`).
  - *explore:* the occupation explorer — three curves vs $(\varepsilon-\mu)/\kB T$ with T and
    $\mu$ sliders and a log toggle, dilute-limit collapse visible live; condensate-fraction
    panel $N_0/N$ vs $T/T_c$; Fermi-sea panel — $g(\varepsilon)$ shaded by $n_{\mathrm{FD}}$
    as T falls, the $\kB T$ shell at $\varepsilon_F$ highlighted.
  - *derive:* symmetry postulate (QM-input box) → single-mode grand-canonical sums → the three
    occupations and the $\mu < \varepsilon_0$ bound → box counting to
    $g(\varepsilon) \propto \sqrt{\varepsilon}$ (mirrors 16's mode counting — said explicitly)
    → fixing N: the $\mu(T; N)$ solver story → BEC saturation → degenerate Fermi gas →
    classical criterion $n\lambda_{\mathrm{th}}^3 \ll 1$. Full route under core derivations.
  - *verify:* (C4b) Planck curve recomputed as photon mode density $\times$
    `bose_einstein(mu=0)`, overlaid on `radiation.planck_u_nu` — the module's mandatory
    `numerical-observation` box, "one occupation function, two chapters"; MB-limit collapse of
    all three occupations to stated tolerance; $\mu$-solver consistency — integrating
    $n(\varepsilon)\,g(\varepsilon)\,\mathrm{d}\varepsilon$ at the solved $\mu$ recovers N;
    the honest miss — ideal-gas $T_c$ at liquid-helium density gives 3.1 K vs the measured
    2.17 K lambda point (interactions ignored, and it shows).
  - *transfer:* conduction electrons in metals (pinned primary — the missing electronic heat
    capacity resolved; total low-T metal $C = \gamma T + A T^3$ joins this module to 16's
    Debye term); back to 13 ($n_Q$ derived, $\mu(T)$ curves meet 13's classical formula);
    back to 16 (Planck as a corollary); forward to 18 (Fermi velocity in transport
    estimates); trapped-atom BEC as the modern laboratory realization (JILA data).
  - *quiz:* symmetry postulate counting; occupation derivations and the $\mu$ bound; classical
    criterion by density and temperature; $\mu(T)$ direction of travel; $T_c$ and condensate
    fraction; Fermi energy and degeneracy pressure; electronic heat capacity; photon $\mu = 0$.
  - *explain:* (1) why photons have $\mu = 0$ and what that makes the Planck law an instance
    of; (2) why degeneracy pressure is not a force — what in the model produces it; (3) in
    your own words, what decides classical vs quantum for a gas; (4) why only electrons near
    $\varepsilon_F$ participate in the heat capacity.
  - *advanced (optional, always last):* white-dwarf vignette — degeneracy pressure balancing
    gravity, order-of-magnitude radius, one page, Chandrasekhar name-checked; Sommerfeld
    expansion sketch upgrading the $\gamma T$ hand-wave to the $\pi^2/2$ coefficient.
    Safe-to-skip boundary: no core content, no quiz item, and nothing in 18 depends on either.
- **Core derivations** — ordered:
  1. Symmetry postulate stated (model-assumption / QM-input box): identical particles admit
     unlimited multi-occupancy (bosons) or at most single occupancy (fermions). No
     wavefunctions — the two-particle two-level counting table (4 / 3 / 1) is the whole
     evidence base offered.
  2. One mode at $(T, \mu)$ — 13's independent-site trick per single-particle state. Bosons:
     $\Xi = \sum_{n\ge 0} e^{-n(\varepsilon-\mu)/\kB T}$ (12's geometric series), giving
     $n_{\mathrm{BE}} = \dfrac{1}{e^{(\varepsilon-\mu)/\kB T} - 1}$, convergence forcing
     $\mu < \varepsilon_0$. Fermions: $\Xi = 1 + e^{-(\varepsilon-\mu)/\kB T}$, giving
     $n_{\mathrm{FD}} = \dfrac{1}{e^{(\varepsilon-\mu)/\kB T} + 1}$. Both `theorem` boxes.
  3. Dilute limit: $e^{(\varepsilon-\mu)/\kB T} \gg 1$ collapses both onto
     $n_{\mathrm{MB}} = e^{-(\varepsilon-\mu)/\kB T}$ — the classical corner.
  4. Box counting (mirrors 16): $g(\varepsilon) = \dfrac{g_s V}{4\pi^2}
     \left(\dfrac{2m}{\hbar^2}\right)^{3/2} \sqrt{\varepsilon}$, continuum approximation
     flagged (valid when $\kB T$ and $\varepsilon_F$ dwarf the level spacing).
  5. Fixing N: solve $N = \int_0^\infty g(\varepsilon)\, n(\varepsilon; \mu, T)\,
     \mathrm{d}\varepsilon$ for $\mu$. The solver story: $\mu$ dives negative at high T
     (classical), climbs toward $\varepsilon_0$ for bosons and toward $\varepsilon_F$ for
     fermions as T falls.
  6. BEC: the excited-state integral saturates at $n\lambda_{\mathrm{th}}^3 = \zeta(3/2)
     \approx 2.612$, defining $\kB T_c = \dfrac{2\pi\hbar^2}{m}\left(\dfrac{n}{\zeta(3/2)}
     \right)^{2/3}$; the ground state takes the overflow, $N_0/N = 1 - (T/T_c)^{3/2}$.
     `approximation` box: replacing the sum by the integral drops the ground state by hand;
     valid for $N \gg 1$ and T not within the finite-N rounding of $T_c$.
  7. Degenerate Fermi gas: $\varepsilon_F = \dfrac{\hbar^2}{2m}(3\pi^2 n)^{2/3}$,
     $T_F = \varepsilon_F/\kB$, $U = \dfrac{3}{5} N \varepsilon_F$,
     $P = \dfrac{2}{5} n \varepsilon_F$ — with zero interactions in the model. Heat capacity
     sketched: only the $\sim \kB T$ shell at $\varepsilon_F$ can rearrange, so
     $C_{\mathrm{el}} \sim N \kB \, T/T_F$, linear in T (`approximation` box; the $\pi^2/2$
     Sommerfeld coefficient quoted, derived only in the advanced section).
  8. Classical criterion: $n\lambda_{\mathrm{th}}^3 \ll 1$ with $\lambda_{\mathrm{th}} =
     h/\sqrt{2\pi m \kB T}$, i.e. $n \ll n_Q$ — module 13's named constant, finally earned.
- **Model specification draft** — for the occupation / condensate / Fermi-sea explorers:
  - **System:** an ideal gas of identical noninteracting particles (bosons, fermions, or
    classical for comparison) in a rigid 3-D box of volume V.
  - **Dynamics:** none — equilibrium occupations are evaluated directly; nothing evolves.
  - **Boundary:** each mode exchanges energy and particles with a reservoir at $(T, \mu)$;
    mean total N is held fixed by solving for $\mu$.
  - **Ensemble:** grand canonical, mode by mode; results reported at fixed mean N.
  - **Ignored:** all interparticle interactions (no scattering, no mean field), trap geometry
    (uniform box only), relativity, and — for electrons — the lattice beyond a free-electron
    box.
  - **Valid when:** ideal-gas regime; continuum density of states, i.e. level spacing far
    below $\kB T$ and $\varepsilon_F$; $N \gg 1$ for the BEC integral argument.
  - **Failure modes:** liquid helium-4 (strongly interacting — the 3.1 K vs 2.17 K miss);
    real metals' band structure (effective masses); the finite-N rounding right at $T_c$.
- **Epistemic classification** — boxed claims: symmetry postulate → `model-assumption` (the
  QM-input box; imported, not derived — the module's honesty anchor); $n_{\mathrm{BE}}$,
  $n_{\mathrm{FD}}$ and the $\mu < \varepsilon_0$ bound → `theorem` (given postulate +
  ensemble); MB as dilute limit with $n\lambda_{\mathrm{th}}^3 \ll 1$ → `theorem` +
  `approximation` criterion; $g(\varepsilon) \propto \sqrt{\varepsilon}$ → `theorem` with the
  continuum step flagged; BEC saturation and $N_0/N = 1 - (T/T_c)^{3/2}$ → `approximation`
  (validity stated); $(3/5) N \varepsilon_F$ and degeneracy pressure → `theorem` (given the
  model); linear-in-T electronic C → `approximation` (sketch); Planck overlay →
  `numerical-observation` (mandatory box, "one occupation function, two chapters").
- **Misconceptions** — no existing registry entry belongs here; three NEW entries (ids collide
  with nothing in `assessment/misconceptions.yml`):
  - `quantum-only-cold` · "Quantum effects matter only when it is cold." · falsifier: copper's
    conduction electrons at 300 K have $T/T_F \sim 0.004$ and $n\lambda_{\mathrm{th}}^3 \gg 1$
    — deeply degenerate at room temperature; degeneracy is set by $n\lambda_{\mathrm{th}}^3$,
    not by T alone · distractor: Q-17-4 option "at 300 K everything is classical".
  - `bec-atoms-stop` · "BEC is just the atoms stopping." · falsifier: the lab computes the
    condensed gas's pressure and excited-state population below $T_c$ — both nonzero;
    condensation is an occupation statement about one state, not an arrest of motion ·
    distractor: Q-17-10 option "all atoms are at rest, so P = 0".
  - `pauli-exclusion-force` · "A Pauli 'force' pushes fermions apart, causing degeneracy
    pressure." · falsifier: `fermi_gas_pressure` is derived from a model whose Ignored line
    lists *all* interparticle forces — the pressure survives with zero interaction terms; it
    is state-counting, not a force · distractor: Q-17-8 option "electron–electron repulsion".
- **Glossary terms** — reused: `indistinguishable`, `maxwell-boltzmann`, `energy-quantum`,
  plus 13's chemical-potential / grand-canonical keys and 16's mode/blackbody keys (landed by
  their plans). NEW (key / en / suggested he / `he_reject`):
  - `boson` / boson / בוזון / —
  - `fermion` / fermion / פרמיון / [פרמיאון]
  - `bose-einstein-distribution` / Bose–Einstein distribution / התפלגות בוזה–איינשטיין /
    [בוז-איינשטיין]
  - `fermi-dirac-distribution` / Fermi–Dirac distribution / התפלגות פרמי–דיראק / [פרמי דירק]
  - `bose-einstein-condensate` / Bose–Einstein condensate / עיבוי בוזה–איינשטיין / —
  - `occupation-number` / occupation number / מספר אכלוס / [מספר איכלוס]
  - `density-of-states` / density of states / צפיפות מצבים / —
  - `fermi-energy` / Fermi energy / אנרגיית פרמי / [אנרגית פרמי]
  - `fermi-temperature` / Fermi temperature / טמפרטורת פרמי / —
  - `degenerate-gas` / degenerate gas / גז מנוון / —
  - `degeneracy-pressure` / degeneracy pressure / לחץ ניוון / —
  - `pauli-exclusion` / Pauli exclusion principle / עקרון האיסור של פאולי / —
  - `thermal-wavelength` / thermal de Broglie wavelength / אורך גל דה-ברויי תרמי / [דה ברולי]
  - `quantum-concentration` / quantum concentration / ריכוז קוונטי / — (skip if 13 lands it)
- **Interactive controls and simulations** — (1) *occupation explorer*: three curves vs
  $(\varepsilon-\mu)/\kB T$; T and $\mu$ sliders, linear/log toggle; readouts of
  $n\lambda_{\mathrm{th}}^3$ for preset gases (He at STP, Rb in a trap, e⁻ in Cu). (2) *BEC
  panel*: $N_0/N$ vs $T/T_c$ with N slider showing finite-N rounding against the ideal
  $1-(T/T_c)^{3/2}$; bar chart of ground vs excited population. (3) *Fermi-sea panel*:
  $g(\varepsilon)\,n_{\mathrm{FD}}$ shaded under $g(\varepsilon)$, T slider hardening the edge
  into the step at $\varepsilon_F$; the participating $\kB T$ shell highlighted. (4) *mu
  tracker*: $\mu(T)$ at fixed n for all three statistics on one axis — the dive/climb story.
- **Virtual lab outline** — `notebooks/en/labs/17-quantum-gases.ipynb`: (1) imports —
  `quantum`, `radiation`, `constants`, `validation`; (2) prediction cells (commit first);
  (3) counting warm-up: enumerate two particles in two levels under the three rules — 4/3/1
  table grounds the postulate; (4) occupation curves; verify the MB collapse numerically;
  (5) `solve_mu` traced over T at fixed n for all three statistics (the dive/climb plot),
  cross-checked against 13's classical $\mu = \kB T \ln(n/n_Q)$ in the dilute regime;
  (6) BEC: integrate the excited states, watch saturation, measure $N_0/N$ vs T and fit the
  exponent with `validation.scaling_exponent` → 3/2; (7) Fermi: numerical $\varepsilon_F$ vs
  closed form; degeneracy pressure vs classical $n \kB T$ for copper's n; (8) the C4b overlay
  — `bose_einstein(h nu, 0, T)` × photon mode density vs `radiation.planck_u_nu`; (9) import
  the metals $\gamma$-coefficient CSV, fit $C/T = \gamma + A T^2$ on low-T copper data,
  compare $\gamma$ to the free-electron prediction; (10) *measurement:* $\gamma(\mathrm{Cu})$
  = value ± error from the fit, quoted against the tabulated 0.695 mJ mol⁻¹ K⁻²; secondary:
  BEC exponent = 1.50 ± error.
- **Real-experiment counterpart** — none practical at desk scale: BEC needs nanokelvin traps
  and degenerate-electron calorimetry needs cryogenics, so no bench pairing is honest here.
  Published-data pairing instead (import-optional): the metals electronic-$\gamma$ table
  (Cu, Ag, Au, Al; Kittel-style values) shipped as CSV under `data/` with the fit task —
  **recommended primary**, because it ties the module to tabulated reality with an actual
  measurement; JILA rubidium condensate-fraction data referenced for the BEC panel.
- **Media assets** — `media/render/render_quantum.py`, language-neutral (no burned-in text):
  `quantum-occupations.mp4` (three occupation curves collapsing as the dilute limit is
  approached); `quantum-bec.mp4` (excited-state saturation; the ground-state spike growing as
  T crosses $T_c$, fraction tracing $1-(T/T_c)^{3/2}$); `quantum-fermi-sea.mp4` (FD-shaded
  density of states hardening into the step at $\varepsilon_F$ as T falls, shell highlighted).
- **Quiz bank outline** — every objective covered at least once; ASCII math:
  - `Q-17-1` (multiple-choice, OBJ-17-1): two identical particles, two levels — count states
    under classical / Bose / Fermi rules; distractor "4 in every case".
  - `Q-17-2` (multiple-choice, OBJ-17-2): why must mu < eps_0 for bosons? distractor "because
    mu is always negative for any gas".
  - `Q-17-3` (numeric, OBJ-17-2): evaluate n_BE, n_FD, n_MB at (eps - mu) = 2 k_B T; rank them.
  - `Q-17-4` (numeric, OBJ-17-3): n lambda_th^3 for helium gas at STP and for electrons in
    copper at 300 K; classify each; distractor from `quantum-only-cold`.
  - `Q-17-5` (multiple-choice, OBJ-17-4): at fixed n, as T falls, mu of a Fermi gas tends
    toward — eps_F; of a Bose gas — eps_0; distractor "minus infinity for both".
  - `Q-17-6` (numeric, OBJ-17-5): T_c for a trapped-Rb-like uniform density; condensate
    fraction at T = 0.5 T_c (1 - 0.5^(3/2) ~ 0.65).
  - `Q-17-7` (numeric, OBJ-17-6): eps_F, T_F and degeneracy pressure for copper
    (n = 8.5e28 m^-3); compare P (~10^10 Pa) to atmospheric.
  - `Q-17-8` (multiple-choice, OBJ-17-7): why is the electronic heat capacity tiny at room T?
    distractors from `pauli-exclusion-force` ("repulsion locks them") and the classical repair
    "too few free electrons carry (3/2) k_B each".
  - `Q-17-9` (free, OBJ-17-8): why do photons have mu = 0, and what does that make the Planck
    spectrum an instance of?
  - `Q-17-10` (multiple-choice, OBJ-17-5): below T_c the Bose gas — still has pressure and
    excitations; distractor from `bec-atoms-stop` ("all atoms at rest, so P = 0").
- **Problem set outline** — `17-quantum-gases-problems.md`: *analytical* — derive both
  occupations from the mode sums (OBJ-17-2); derive $g(\varepsilon)$ from box counting
  (OBJ-17-4); derive $T_c$ and the 3/2 exponent (OBJ-17-5); derive $(3/5) N \varepsilon_F$
  and $P = (2/5) n \varepsilon_F$ (OBJ-17-6). *Computational* — $\mu(T)$ for all three
  statistics on one plot via `solve_mu` (OBJ-17-4); fit $\gamma$ from the low-T copper CSV
  and compare to free-electron theory (OBJ-17-7); ideal $T_c$ at liquid-helium density vs the
  2.17 K lambda point — quantify and discuss the miss (OBJ-17-5). *Challenge* — white-dwarf
  radius from degeneracy pressure balancing gravity, order of magnitude (OBJ-17-6; feeds the
  advanced vignette); the photon gas as the $\mu = 0$, $g \propto \varepsilon^2$ special case
  re-deriving Stefan–Boltzmann scaling (OBJ-17-8).
- **Runtime budget** — trivial by course standards: occupation grids 3 × 1000 points
  (microseconds); `solve_mu` is `scipy.optimize.brentq` on a 1-D function whose evaluation is
  a ~200-point quadrature — milliseconds per solve, ~100 T-points per $\mu(T)$ curve, well
  under a second; quadrature instead of polylogarithms everywhere ($\zeta(3/2)$ via
  `scipy.special.zeta` is the only special value) keeps the code readable and Pyodide-safe.
  No RNG, no Numba; vectorized NumPy + SciPy only. Redraw on slider release.
- **Validation gates** — the six README commands with `--module 17-quantum-gases`, plus: the
  C4b overlay test must import `radiation` *into* `quantum`'s test, never the reverse (the
  README's no-backward-import rule, mechanised).
- **Open questions for the author** —
  1. Where do $\hbar$, h and particle masses live? `constants.py` is never extended (README
     rule). **Recommend:** `quantum.py` defines `H_BAR`, `M_ELECTRON`, `M_HELIUM4` at module
     level and takes Planck's h from `radiation.py` (already a 17 dependency via C4b) —
     coordinate the split with plan 16 before either lands.
  2. Spin degeneracy: hidden factor 2 for electrons or explicit parameter? **Recommend:**
     explicit `spin_degeneracy` keyword, default 1 in `density_of_states_3d`, default 2 in the
     Fermi functions — no invisible factors anywhere.
  3. Advanced section: white-dwarf vignette, Sommerfeld sketch, or both? **Recommend:** the
     white-dwarf vignette (the irresistible payoff of degeneracy pressure, one page,
     order-of-magnitude only); Sommerfeld as a half-page appendix only if space allows.
  4. Helium-4 honest-miss placement — verify or transfer? **Recommend:** verify, mirroring
     02's NIST 4% miss: a computed number, a measured number, and a named ignored ingredient.

## 4. Library and tests

- **`src/thermolab` — existing used:** `constants.py` (`K_B`, `AMU` for the helium-4 mass);
  `gases.py` (`ideal_gas_pressure` for classical-vs-degenerate comparisons); `chemical.py`
  (13's classical ideal-gas $\mu$ for the dilute cross-check); `radiation.py`
  (`planck_u_nu`, the C4b overlay target); `multiplicity.py` (the counting warm-up frames the
  postulate against 08's machinery); `validation.py` (`scaling_exponent`,
  `convergence_study`, `relative_error`) in tests and the lab.
- **`src/thermolab` — new:** `quantum.py` (ownership table: introduced by 17, extended by
  none, serves 17). Docstring header, 7 bullets in fixed order — System: ideal gas of
  identical noninteracting particles (bosons, fermions, or classical) in a rigid 3-D box /
  Dynamics: none — equilibrium occupations evaluated directly / Boundary: modes exchange
  energy and particles with a reservoir at (T, mu); mean N fixed by solving for mu /
  Ensemble: grand canonical, mode by mode / Ignored: all interparticle interactions, trap
  geometry, relativity, band structure / Valid when: ideal regime, continuum density of
  states, N >> 1 / Failure modes: liquid helium-4, real band structures, finite-N rounding at
  T_c. Functions:
  - `bose_einstein(eps, mu, temperature) -> np.ndarray` — $1/(e^{(\varepsilon-\mu)/\kB T}-1)$;
    raises unless mu < min(eps); `mu=0` is the photon case.
  - `fermi_dirac(eps, mu, temperature) -> np.ndarray` — $1/(e^{(\varepsilon-\mu)/\kB T}+1)$;
    overflow-safe on both tails.
  - `maxwell_boltzmann(eps, mu, temperature) -> np.ndarray` — $e^{-(\varepsilon-\mu)/\kB T}$,
    the shared dilute limit.
  - `density_of_states_3d(eps, volume, mass, spin_degeneracy=1) -> np.ndarray` —
    $g_s V (2m/\hbar^2)^{3/2} \sqrt{\varepsilon} / (4\pi^2)$, per unit energy.
  - `solve_mu(n_density, temperature, statistics) -> float` — brentq root of
    $n - \int g\, n(\varepsilon;\mu)\,\mathrm{d}\varepsilon / V$; holds N fixed; `statistics`
    in {"be", "fd", "mb"}; boson bracket capped below eps_0 = 0.
  - `bec_tc(n_density, mass) -> float` — $\kB T_c = (2\pi\hbar^2/m)(n/\zeta(3/2))^{2/3}$.
  - `bec_condensate_fraction(temperature, t_c) -> np.ndarray` — max(0, 1 − (T/T_c)^{3/2}).
  - `fermi_energy(n_density, mass) -> float` — $(\hbar^2/2m)(3\pi^2 n)^{2/3}$ (spin-2).
  - `fermi_gas_energy(n_density, mass) -> float` — per-particle $(3/5)\varepsilon_F$ [J];
    `fermi_gas_pressure(n_density, mass) -> float` — $(2/5) n \varepsilon_F$ [Pa].
  - `electronic_heat_capacity_sketch(temperature, t_f) -> float` — per-particle
    $(\pi^2/2)\kB T/T_F$, the Sommerfeld-flavoured linear law.
  - `classical_criterion(n_density, temperature, mass) -> float` — $n\lambda_{\mathrm{th}}^3$;
    "quantum when ≳ 1".
- **`tests/physics/` additions** (six categories):
  - *dimensional:* `fermi_energy` in J, `fermi_gas_pressure` in Pa, `bec_tc` in K,
    `density_of_states_3d` in 1/J, `classical_criterion` dimensionless — pint re-evaluation.
  - *conservation:* particle number as code — integrating $g \cdot n$ at `solve_mu`'s root
    recovers `n_density` to quadrature tolerance, for all three statistics across a T sweep.
  - *analytic-limit:* all three occupations agree to tolerance when
    $e^{(\varepsilon-\mu)/\kB T} \ge 10^2$; Planck overlay — `bose_einstein(mu=0)` × photon
    mode density equals `radiation.planck_u_nu` pointwise (C4b; conservation-of-story, filed
    here); `fermi_energy` vs closed form and T → 0 FD step at $\varepsilon_F$;
    `bec_condensate_fraction` endpoints (1 at T = 0, 0 at $T_c$); solver-measured BEC exponent
    = 3/2 via `validation.scaling_exponent`; `solve_mu("mb")` matches 13's closed-form
    classical $\mu$.
  - *large-N:* the discrete sum over box modes approaches the $g(\varepsilon)$ integral as the
    box grows — continuum approximation quantified, error shrinking with system size.
  - *convergence:* `solve_mu` residual vs quadrature refinement at the expected order
    (`validation.convergence_study`); brentq bracket tolerance honoured across statistics.
  - *seed-independence:* n/a — the file is fully deterministic; no RNG anywhere.

## 5. Assessment hooks

Checkpoint synthesis (module-level, not per-section): (a) 13 + 17 — one plot of $\mu(T)$ at
fixed n where `solve_mu` meets 13's classical formula from above: say where and why they part;
(b) 16 + 17 — low-T metal heat capacity $C = \gamma T + A T^3$: fit both terms from the copper
CSV and assign each to its module (electrons here, Debye phonons in 16); (c) the degeneracy
ladder — compute $n\lambda_{\mathrm{th}}^3$ for air at STP, liquid helium at 2 K, copper's
electrons at 300 K, and classify each with one sentence. Exam themes: mode-sum derivations of
the occupations; $T_c$ and $\varepsilon_F$ order-of-magnitude estimates; classify-the-claim
across this module's unusually rich epistemic spread (postulate / theorem / approximation /
numerical observation). As the course's quantum capstone this module feeds the course-end
synthesis set; 18 consumes only the degenerate-gas vocabulary and Fermi velocity.

## 6. Build order and validation gates

Builds after 13 and 16 (it imports `chemical.py` and `radiation.py`; C4b's loop closes only
when this module lands) and independently of 18. Lands together in one change: page + problems
+ lab + quiz bank; `quantum.py` with its tests; the three NEW misconception entries (status
`addressed`) in `assessment/misconceptions.yml`; the ~14 NEW glossary keys in
`glossary/terms.yml` with `he_reject` candidates (dropping any 13 already landed); the metals
$\gamma$ CSV under `data/`; `media/render/render_quantum.py` and its three MP4s. HE mirror
family (`.he.yml` quiz, HE page/problems/lab with `en_source_hash` stamps) follows; until it
lands the page is listed in `translation-pending.txt`. Gates: the six README commands with
`--module 17-quantum-gases`, plus the no-backward-import check on the C4b overlay test.

## 7. Deviations from the brainstorm

- **QM budget held to the course promise (§1).** Quantum input is exactly the symmetry
  postulate plus state counting; wavefunctions, operators and the Schrödinger equation are
  banned from the prose. Rationale: the audience promise says QM is needed only here — and
  only this much of it.
- **Transfer application pinned to conduction electrons in metals.** Chosen over white dwarfs
  (which survive as the advanced vignette): it resolves a genuine historical anomaly (the
  missing electronic heat capacity), joins 16's solids story, and ends in a fit to tabulated
  data rather than an astrophysical estimate.
- **Full grand-canonical formalism introduced here (closes 13's deferral).** 13 uses the
  independent-site trick on one site; this module generalizes it to every single-particle mode
  and makes $\Xi$ a named object. Rationale: the formalism pays for itself only once
  occupations are the question.
- **BEC at ideal-gas level only (re-scope of "BEC" in row 17).** The integral-approximation
  argument is boxed with its validity; interacting condensates are out of scope, and the
  helium-4 lambda-point miss is shown deliberately as the model's failure mode.
- **Centrepiece extended (addition).** The brainstorm row asks only to "compare classical,
  Bose and Fermi occupation functions"; the plan adds the condensate-fraction and Fermi-sea
  panels plus the $\mu(T)$ tracker, because the occupation curves alone don't show either
  headline phenomenon.
