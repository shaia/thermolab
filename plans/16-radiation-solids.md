# Module 16 — Thermal radiation and solids — Implementation Plan

> **Brainstorm:** §3 module 16 (+ §5 blackbody laboratory, §6 misconceptions, §7 accuracy
> framework). **Module id:** `16-radiation-solids`.
> **Content path:** `content/en/advanced/16-radiation-solids.md`. **Status:** planned.
> Canonical map, invariants, and conflict log: [README.md](README.md).

## 1. Overview and narrative arc

Classical physics, applied honestly, makes two catastrophic predictions. A warm oven's cavity
supports infinitely many electromagnetic modes; equipartition hands each one $\kB T$, so every
oven should radiate infinite energy — the ultraviolet catastrophe. And a solid of $N$ atoms is
$3N$ oscillators, so equipartition fixes $C = 3 N \kB$ at every temperature — Dulong–Petit,
flatly contradicted by every cryogenic measurement. This module's through-line: both
catastrophes have the same one-line fix. An oscillator of frequency $\omega$ takes energy only
in quanta $\hbar\omega$, so modes with $\hbar\omega \gg \kB T$ cannot afford even one quantum
and drop out. One idea, two rescues — radiation and matter cured by the same formula.

The centrepiece is the brainstorm §5 blackbody laboratory, with its named lesson made central
rather than parenthetical: spectral radiance is shown *by frequency and by wavelength side by
side*, and the two peak markers visibly disagree — the Wien peak in $\nu$ is **not**
$c/(\text{Wien peak in }\lambda)$. "The peak of the spectrum" is not a property of the
radiation alone; a spectral density means nothing until integrated, and
$\mathrm{d}u = u_\nu\,\mathrm{d}\nu = u_\lambda\,\mathrm{d}\lambda$ puts the two peaks at
different photons. That boxed lesson is the module's conceptual signature.

Two spirals get their payoff here. The Einstein solid completes its course-long arc (C4c):
01 exchanged its quanta, 09 built its $S(U,N)$, 12 computed its oscillator $Z$ — and here that
same model finally yields a measurable curve, $C(T)$, fitted against real crystals; Debye then
repairs its low-$T$ failure. And the equipartition baseline of 04/06 is closed: the freeze-out
caveat planted there becomes quantitative. Forward, this module plants 17's seed (C4b): the
occupation derived inline here is Bose–Einstein at $\mu = 0$, recomputed there from
`quantum.bose_einstein` to close the loop.

## 2. Position in the course

- **Requires:** `12-partition-functions` — the single-oscillator canonical sum
  $Z = 1/(1 - e^{-\hbar\omega/\kB T})$ and the $U = -\partial \ln Z/\partial\beta$ machinery
  (`partition.py`), plus its freeze-out picture; `09-fundamental-relation` — $\mathrm{d}U =
  T\,\mathrm{d}S - P\,\mathrm{d}V$ and reading $S$ by integrating $C_V/T$;
  `04-pressure`/`06-processes` — equipartition with its degree-of-freedom counting and the
  momentum-flux pressure argument (the classical baseline that fails here); `01-equilibrium` —
  the Einstein-solid model itself (`equilibrium.py`), whose heat capacity was there *asserted*
  as $C = n \kB$.
- **Feeds:** `17-quantum-gases` — the occupation $1/(e^{\hbar\omega/\kB T} - 1)$ generalized:
  Planck is Bose–Einstein at $\mu = 0$; 17's verify section recomputes this module's Planck
  curve from `quantum.bose_einstein(mu=0)` (C4b closing), and `radiation.py`'s photon gas is
  its worked $\mu = 0$ example. `18-fluctuations-transport` — nothing direct; stated
  explicitly so no one hunts for a dependency.
- **Explicitly not assumed:** general Bose–Einstein statistics or a chemical potential for
  bosons (17's material — "Bose" appears only in the transfer teaser); photon quantum
  mechanics beyond $E = h\nu$ taken as an input (model-assumption box, not a derivation);
  band theory or electronic heat capacity (named as the metals-at-mK caveat only).

## 3. Module specification

- **Identity and scope** — brainstorm row 16 in full: Planck spectrum, photons, Einstein and
  Debye solids; blackbody and heat-capacity explorers. Covered: quantized-mode occupation
  (inline, C4b), cavity mode counting, Planck's law in both spectral variables, Wien
  displacement in both, Stefan–Boltzmann, brief photon-gas thermodynamics, Einstein and Debye
  heat capacities with real-data fits. Deferred: general BE/FD occupations, BEC, degenerate
  gases → 17; transport of heat → 18; electronic contribution to $C$ → outside the course.
- **Prerequisites** — 12: oscillator $Z$ and $U$ from $\ln Z$; 09: $T\,\mathrm{d}S$ relations;
  04/06: equipartition + $f$-counting, kinetic pressure as momentum flux; 01: the Einstein
  solid as a physical model.
- **Learning objectives** — frontmatter-verbatim, ASCII math:
  - `OBJ-16-1`: Derive the mean energy of one quantized mode, <E> = h nu / (exp(h nu/(k_B T))
    - 1), from the oscillator partition function, and recover the classical k_B T in the
    limit h nu << k_B T.
  - `OBJ-16-2`: Count standing-wave modes in a cavity to obtain g(nu) dnu = (8 pi V/c^3) nu^2
    dnu, and explain why equipartition over these modes predicts infinite energy density (the
    ultraviolet catastrophe).
  - `OBJ-16-3`: State Planck's law in both spectral variables, convert between them via
    u_lambda = u_nu |d nu/d lambda|, and explain why the frequency peak and wavelength peak
    of the same spectrum sit at different photons.
  - `OBJ-16-4`: Compute Wien peaks in both variables (nu_max = 2.821 k_B T/h, lambda_max T =
    2.898e-3 m K) and total energy density u = a T^4; predict how total radiated power scales
    when T changes.
  - `OBJ-16-5`: State the photon-gas relations P = u/3, S/V = (4/3) a T^3, mu = 0, and give
    the one-line reason photon number carries no chemical potential.
  - `OBJ-16-6`: Derive the Einstein heat capacity C(T) = 3 N k_B (theta_E/T)^2
    exp(theta_E/T)/(exp(theta_E/T) - 1)^2 and its limits: Dulong–Petit 3 N k_B at high T,
    exponential vanishing at low T.
  - `OBJ-16-7`: Explain Debye's phonon-mode repair, compute C(T) from the Debye integral,
    extract the T^3 low-temperature law, and fit theta_D to measured heat-capacity data.
- **Mathematical background** — already has: partial derivatives, $\ln Z$ differentiation
  (12), improper integrals (00/12). New here: change of variables for a *density* (the
  Jacobian $|\mathrm{d}\nu/\mathrm{d}\lambda|$ as the whole point, not a technicality);
  counting lattice points in an octant of $k$-space; the fixed integral
  $\int_0^\infty x^3/(e^x - 1)\,\mathrm{d}x = \pi^4/15$ quoted, checked numerically.
- **Physical intuition goals** — student can predict, without algebra: (1) doubling an oven's
  temperature multiplies total radiated power by 16, and shifts the peak — spectra are not
  rescaled copies of each other; (2) a mode with $\hbar\omega \gg \kB T$ holds essentially no
  energy — freeze-out is unaffordability, not stillness; (3) diamond (stiff bonds, light
  atoms, huge $\theta_D$) is far below Dulong–Petit at room temperature while lead sits on
  it; (4) asked "where does the Sun's spectrum peak?", the student first asks "per unit of
  what?".
- **Section skeleton seeds** — contract order:
  - *puzzle:* your kitchen oven at 500 K, by the physics of 04–12, should be a lethal
    ultraviolet lamp of infinite power — and its steel walls should hold heat capacity
    $3 N \kB$ down to absolute zero, which measurement flatly denies. Boxed question: what
    single assumption do both classical predictions share, and what one change kills both
    catastrophes at once?
  - *predict:* (1) heat an oven from 300 K to 600 K — total radiated energy grows 2×, 4×, 8×
    or 16×? (targets `hotter-rescaled-spectrum`); (2) the Sun peaks near 500 nm plotted per
    wavelength; per frequency, is the peak at $c/500\,\mathrm{nm}$? (targets
    `blackbody-peak-absolute`); (3) cool diamond from 300 K to 30 K — does $C$ drop ~10× or
    collapse by orders of magnitude? sketch $C(T)$ (targets `cold-solid-motion-stops`);
    (4) double a cavity's temperature — does the photon count double?
  - *explore:* the blackbody explorer — one $T$ slider (100 K–10000 K, log), two synced
    panels: $u_\nu(\nu)$ and $u_\lambda(\lambda)$ side by side, each with its live Wien peak
    marker plus a ghost marker showing the *other* panel's peak mapped through $\lambda =
    c/\nu$ — the mismatch is the lesson. Toggle: Rayleigh–Jeans overlay diverging in the UV.
    Second explorer: Einstein vs Debye $C(T)/3N\kB$ with $\theta_E$, $\theta_D$ sliders over
    measured diamond/silver/copper points.
  - *derive:* the seven-step route under core derivations: inline occupation (C4b theorem
    box) → mode counting → Planck in $\nu$ then $\lambda$ → Wien twice → Stefan–Boltzmann →
    photon gas briefly → Einstein $C(T)$ → Debye repair.
  - *verify:* numeric $\int u_\nu\,\mathrm{d}\nu$ vs $a T^4$ with $a$ from $\zeta(4)$ (the
    `numerical-observation` admonition); $\int u_\nu\,\mathrm{d}\nu = \int
    u_\lambda\,\mathrm{d}\lambda$ though the peaks differ; Einstein and Debye both → $3N\kB$
    at high $T$; log-log slope of Debye $C$ at low $T$ → 3, Einstein's → visibly steeper.
  - *transfer:* back to 01/09/12 — the Einstein solid's spiral closes: the model that opened
    the course now fits real crystals (C4c); back to 04/06 — equipartition recovered as the
    high-$T$ limit, its freeze-out caveat now quantitative; forward to 17 — the occupation is
    BE at $\mu = 0$, generalized there; 18 — explicitly nothing owed; outward — pyrometry,
    the CMB as thermal-history evidence, incandescent-lamp efficiency.
  - *quiz:* occupation limits; catastrophe mechanism; dual-peak trap; $T^4$ scaling; photon
    $\mu = 0$; Einstein limits; Einstein-vs-Debye verdict from data.
  - *explain:* (1) why "the peak of the blackbody spectrum" is ill-posed until a spectral
    variable is named; (2) why $C \to 0$ at low $T$ although atomic motion never stops;
    (3) how one hypothesis rescues both catastrophes — state the shared classical assumption
    it replaces; (4) in one sentence, why photons have $\mu = 0$.
  - *advanced (optional, always last):* the greenhouse two-layer energy-balance toy — bare
    Earth at 255 K, one shortwave-transparent/longwave-absorbing layer lifting the surface to
    ~303 K, pure Stefan–Boltzmann bookkeeping. Safe-to-skip boundary: nothing in core 16, in
    17, or in any test depends on it.
- **Core derivations** — ordered:
  1. *Occupation, inline (C4b):* from 12's $Z = 1/(1 - e^{-\hbar\omega/\kB T})$ per mode,
     $\langle E\rangle = -\dfrac{\partial \ln Z}{\partial \beta} =
     \dfrac{\hbar\omega}{e^{\hbar\omega/\kB T} - 1}$ — theorem box; zero-point $\hbar\omega/2$
     noted as a $T$-independent shift and set aside. Limits: $\kB T$ for
     $\hbar\omega \ll \kB T$, $\hbar\omega\,e^{-\hbar\omega/\kB T}$ for the opposite.
  2. *Mode counting:* standing waves in $L^3$, positive octant of $k$-space, two
     polarizations: $g(\nu)\,\mathrm{d}\nu = \dfrac{8\pi V}{c^3}\,\nu^2\,\mathrm{d}\nu$;
     equipartition then gives $u = \int (8\pi\nu^2/c^3)\,\kB T\,\mathrm{d}\nu = \infty$ — the
     catastrophe stated as a theorem *of the classical model*.
  3. *Planck's law:* $u_\nu = \dfrac{8\pi h \nu^3}{c^3}\,\dfrac{1}{e^{h\nu/\kB T} - 1}$;
     change of variables $u_\lambda = u_\nu\,|\mathrm{d}\nu/\mathrm{d}\lambda| =
     \dfrac{8\pi h c}{\lambda^5}\,\dfrac{1}{e^{hc/\lambda \kB T} - 1}$. Wien twice:
     $x = 3(1 - e^{-x})$ gives $\nu_{max} = 2.821\,\kB T/h$; $x = 5(1 - e^{-x})$ gives
     $\lambda_{max} T = 2.898\times10^{-3}\,\mathrm{m\,K}$ — and $\nu_{max}\lambda_{max}
     \approx 0.568\,c \ne c$: the boxed dual-peak lesson.
  4. *Stefan–Boltzmann:* $u = a T^4$, $a = \dfrac{8\pi^5 \kB^4}{15 h^3 c^3}$ via
     $\int_0^\infty x^3/(e^x-1)\,\mathrm{d}x = \pi^4/15 = 6\zeta(4)$; flux $\sigma T^4$ with
     $\sigma = ac/4$.
  5. *Photon gas, brief (pinned scope):* $P = u/3$ by 04's momentum-flux argument with
     $E = pc$; at constant $V$, $\dbar Q = T\,\mathrm{d}S = \mathrm{d}U$ so
     $S/V = \frac{4}{3} a T^3$ by integrating $C_V/T$ from 0; $\mu = 0$ because photon number
     is unconstrained — $(\partial F/\partial N)_{T,V} = 0$ at the minimum — one line + a
     forward pointer to 17. Compression work enters as $\dbar \Won = -P\,\mathrm{d}V$ with
     $P = u/3$: radiation pushes back (glossary's `radiation-pressure` cashed in).
  6. *Einstein solid (C4c payoff):* $3N$ modes at one $\omega_E$; with $x = \theta_E/T$,
     $\theta_E = \hbar\omega_E/\kB$: $C(T) = 3 N \kB\,\dfrac{x^2 e^{x}}{(e^{x} - 1)^2}$.
     High $T$ → $3N\kB$ (Dulong–Petit; equipartition and 06/12's freeze-out caveat closed);
     low $T$ → $3N\kB\,x^2 e^{-x}$ — exponential. But experiment says $T^3$: the model's
     single frequency is the culprit.
  7. *Debye's repair:* sound modes with $g(\omega) = 3V\omega^2/(2\pi^2 c_s^3)$ cut off so
     total modes $= 3N$, giving $\theta_D$; $C(T) = 9 N \kB\,(T/\theta_D)^3
     \int_0^{\theta_D/T} \dfrac{x^4 e^x}{(e^x - 1)^2}\,\mathrm{d}x$ (numeric); low $T$ →
     $\dfrac{12\pi^4}{5} N \kB (T/\theta_D)^3$; high $T$ → $3N\kB$. Approximation boxes
     compare Einstein vs Debye honestly: both are one-parameter caricatures of the true
     phonon spectrum; Debye wins at low $T$ because *low-frequency modes exist*.
- **Model specification draft** — for the blackbody explorer (Einstein/Debye explorer varies
  only System/Valid-when):
  - **System:** the electromagnetic field in a cavity of volume $V$ at temperature $T$, as
    independent harmonic modes with energies restricted to multiples of $h\nu$.
  - **Dynamics:** none — every rendered spectrum is thermal equilibrium; nothing evolves.
  - **Boundary:** rigid perfectly-reflecting walls at fixed $T$; a pinhole for "what an
    observer sees" (radiance ∝ energy density, factor $c/4$).
  - **Ensemble:** canonical per mode — each mode exchanges energy with the walls as its bath.
  - **Ignored:** zero-point energy (constant shift); photon–photon interaction (exact for
    EM); wall material and emissivity (< 1 rescales, never reshapes); polarization detail
    beyond the count of 2.
  - **Valid when:** cavity large enough that modes are dense, $V^{1/3} \gg hc/\kB T$;
    equilibrium radiation only.
  - **Failure modes:** small or cold cavities where discreteness of modes shows; non-thermal
    sources (lasers, LEDs); for the solids explorer — metals at very low $T$ (electronic
    $C \propto T$ term) and real phonon dispersion beyond the Debye caricature.
- **Epistemic classification** — boxed claims: energy in quanta $E_n = n h\nu$ →
  `model-assumption` (input, not derived — no quantum mechanics assumed, per the boundary
  with 17); mode occupation from $Z$ → `theorem` (the C4b inline box); $g(\nu)$ counting →
  `theorem`; UV catastrophe → `theorem` of the classical model; Planck's law and
  Stefan–Boltzmann → `theorem` given the model (with the historical `empirical-law` origin
  of $\sigma T^4$ noted); dual-peak lesson → `definition` (of spectral density) — the
  module's signature box; $\zeta(4)$ integral check → `numerical-observation`; Dulong–Petit
  → `empirical-law`; Debye $T^3$ → `approximation` (low-$T$ limit of a model); $\mu = 0$ →
  `model-assumption` with the one-line minimization argument and 17-pointer.
- **Misconceptions** — no existing registry entry is assigned here (`equilibrium-motion-stops`
  is 04's and stays there; its low-$T$ cousin below is distinct). Three NEW entries (no id
  collisions in `assessment/misconceptions.yml`):
  - `blackbody-peak-absolute` · "The peak of the blackbody spectrum is a property of the
    radiation alone." · falsifier: the explorer shows one spectrum, two variables, two peaks
    — $\nu_{max} \ne c/\lambda_{max}$ at every $T$, while the integrated energy agrees ·
    distractor: Q-16-3 option "$\nu_{max} = c/\lambda_{max}$ — same spectrum, same peak".
  - `hotter-rescaled-spectrum` · "Hotter bodies radiate more only because they are brighter
    versions of the same spectrum." · falsifier: explorer sweep shows total power ×16 on
    doubling $T$ *and* the peak migrating — curves at two temperatures never coincide under
    any vertical rescaling · distractor: Q-16-5 option "power doubles — brightness tracks
    temperature".
  - `cold-solid-motion-stops` · "A solid's atoms stop moving at low temperature, so its heat
    capacity falls to zero." · falsifier: zero-point motion persists at $T = 0$ (the set-aside
    $\hbar\omega/2$); $C$ vanishes because a whole quantum $\hbar\omega$ becomes unaffordable
    — occupation freezes, not motion · distractor: Q-16-8 option "atoms are frozen still, so
    no energy can be stored".
- **Glossary terms** — reused: `heat-capacity`, `energy-quantum`, `radiation-pressure`.
  NEW (key / en / suggested he / `he_reject`):
  - `blackbody` / blackbody / גוף שחור / —
  - `planck-law` / Planck's law / חוק פלאנק / [חוק פלנק]
  - `spectral-energy-density` / spectral energy density / צפיפות אנרגיה ספקטרלית / —
  - `photon` / photon / פוטון / —
  - `phonon` / phonon / פונון / —
  - `ultraviolet-catastrophe` / ultraviolet catastrophe / הקטסטרופה האולטרה-סגולה / —
  - `wien-displacement` / Wien displacement law / חוק ההסחה של וין / [ווין, וויין]
  - `stefan-boltzmann-law` / Stefan–Boltzmann law / חוק סטפן-בולצמן / [סטפן-בולטזמן]
  - `dulong-petit` / Dulong–Petit law / חוק דולונג-פטי / —
  - `einstein-temperature` / Einstein temperature / טמפרטורת איינשטיין / [אינשטיין]
  - `debye-temperature` / Debye temperature / טמפרטורת דבאי / [דביי, דבאיי]
  - `zero-point-energy` / zero-point energy / אנרגיית נקודת האפס / —
  - `density-of-modes` / density of modes / צפיפות האופנים / —
- **Interactive controls and simulations** — (1) *blackbody explorer:* log $T$ slider
  100 K–10000 K; twin panels $u_\nu$, $u_\lambda$ with own-peak and mapped-ghost-peak
  markers; Rayleigh–Jeans overlay toggle; log/linear axis toggle; visible-band tint.
  (2) *heat-capacity explorer:* $\theta_E$ and $\theta_D$ sliders (50–2500 K), Einstein and
  Debye $C/3N\kB$ curves over diamond/silver/copper data points, residual strip below,
  log-log toggle exposing the low-$T$ slopes 3 vs steeper-than-3. (3) *CMB fit cell (lab):*
  FIRAS points with a one-parameter Planck fit and live $\chi^2$.
- **Virtual lab outline** — `notebooks/en/labs/16-radiation-solids.ipynb`: (1) setup — import
  `radiation`, `partition`, `validation`, constants; (2) prediction cells (commit first);
  (3) build $u_\nu$ from `mode_occupation` × mode count, overlay `planck_u_nu` — the inline
  derivation re-enacted in code; (4) dual-peak experiment: locate both peaks numerically at
  several $T$, tabulate $\nu_{max}\lambda_{max}/c$ (falsifies `blackbody-peak-absolute`);
  (5) `stefan_boltzmann_check` — quadrature vs $aT^4$, log-log $u(T)$ slope → 4 via
  `validation.scaling_exponent` (falsifies `hotter-rescaled-spectrum`); (6) load
  diamond/silver/copper $C_P$ CSVs from `data/`, fit `fit_einstein_temperature` and
  `fit_debye_temperature`, compare residuals — Debye wins at low $T$; (7) low-$T$ log-log
  slope of the data → 3 (falsifies `cold-solid-motion-stops` via the occupation story);
  (8) FIRAS monopole spectrum: one-parameter fit; (9) *measurement:* $\theta_D$(diamond) =
  value ± error [K] and $T_{CMB}$ = value ± error [K], quoted against 2230 K and 2.725 K.
- **Real-experiment counterpart** — the pinned open question, recommendation **yes, real
  data** (settled below in §3 open questions): (a) low-$T$ heat-capacity tables for diamond,
  silver, copper — classic Debye-fit targets, diamond's huge $\theta_D \approx 2230\,$K the
  star exhibit — sourced from NIST-JANAF / CODATA-style compilations (US-government tables,
  public domain), shipped as small CSVs `data/heat-capacity-{diamond,silver,copper}.csv`;
  note honestly that tables give $C_P$ while the models give $C_V$ ($C_P - C_V$ negligible
  for solids at these $T$ — one-line approximation box). (b) COBE/FIRAS CMB monopole
  spectrum (NASA LAMBDA archive, public domain) as `data/cmb-firas-monopole.csv` — the most
  perfect blackbody ever measured, fit $T = 2.725\,$K. Fallback if licensing proves
  doubtful: `synthetic_heat_capacity` in `radiation.py` synthesizes Debye + noise via a
  passed `numpy` rng. No bench pairing beats an incandescent-bulb dimmer (colour shifts
  red-to-white as $T$ rises) — zero-cost, qualitative only.
- **Media assets** — `media/render/render_radiation.py`, language-neutral (no burned-in
  text): `radiation-dual-peak.mp4` (pre-rendered $T$ sweep of the twin panels, peak markers
  drifting apart, mapped ghost peak never landing on the true one); `radiation-catastrophe.mp4`
  (Rayleigh–Jeans hugging Planck at low $\nu$ then diverging); `radiation-solids.mp4`
  (Einstein and Debye curves sweeping $\theta$ over the data points, log-log flip at the end).
- **Quiz bank outline** — every objective covered; ASCII math:
  - `Q-16-1` (multiple-choice, OBJ-16-1): mean energy of a mode with h nu = 3 k_B T vs the
    classical k_B T; distractor "every mode carries k_B T regardless of frequency".
  - `Q-16-2` (multiple-choice, OBJ-16-2): what diverges classically — mode count grows as
    nu^2 while each mode keeps k_B T; distractors blame "infinite photon speed" and "walls".
  - `Q-16-3` (multiple-choice, OBJ-16-3): sun peaks at ~500 nm per wavelength; per frequency
    the peak photon is different — distractor from `blackbody-peak-absolute`.
  - `Q-16-4` (numeric, OBJ-16-4): lambda_max at T = 5772 K from 2.898e-3 m K, and nu_max from
    2.821 k_B T/h; verify nu_max lambda_max/c ≈ 0.57.
  - `Q-16-5` (numeric, OBJ-16-4): oven 300 K → 600 K, factor in total radiated energy (16);
    distractor from `hotter-rescaled-spectrum` (2).
  - `Q-16-6` (multiple-choice, OBJ-16-5): why mu = 0 for photons; distractor "photon number
    is conserved, so mu is fixed by it"; includes N/V ∝ T^3 as a checkable consequence.
  - `Q-16-7` (numeric, OBJ-16-6): Einstein C at T = theta_E/2 in units of 3 N k_B; limit
    check at T = 5 theta_E.
  - `Q-16-8` (multiple-choice, OBJ-16-7): data show log-log slope 3 at low T — which model
    survives and why; distractors "Einstein — both vanish at 0" and `cold-solid-motion-stops`.
  - `Q-16-9` (free, OBJ-16-1 + OBJ-16-6): state the one assumption that rescues both
    catastrophes, and explain why C -> 0 although atomic motion never stops.
- **Problem set outline** — `16-radiation-solids-problems.md`: *analytical* — derive both
  Wien conditions x = 3(1 - e^-x), x = 5(1 - e^-x) and explain why they differ (OBJ-16-3/4);
  derive S/V = (4/3) a T^3 from dU = \dbar Q at constant V (OBJ-16-5); expand Einstein C to
  order (theta_E/T)^2 and show Debye shares the leading correction's form (OBJ-16-6/7).
  *Computational* — fit theta_D for all three solids, report with uncertainties and compare
  residuals against Einstein fits (OBJ-16-7); FIRAS T_CMB fit with error (OBJ-16-3/4);
  photon count N/V ∝ T^3 by numeric integral, ratio to zeta(3) form (OBJ-16-5).
  *Challenge* — greenhouse two-layer balance: surface temperature with one absorbing layer
  (OBJ-16-4); estimate theta_E of diamond from bond stiffness and atomic mass, compare to
  the fit (OBJ-16-6).
- **Runtime budget** — all deterministic, vectorized NumPy, no Numba (Pyodide): spectral
  grids ≤ 2000 points × 2 panels, redrawn per slider tick — trivial; Debye integral by
  64-point Gauss–Legendre per temperature, $\le 200$ temperatures per curve — milliseconds;
  fits are 1-parameter scans (200 candidate $\theta$ values × 200 data points) — well under
  a second. The dual-peak page animation is a pre-rendered MP4; live twin panels run in the
  lab. Target: every lab cell interactive in-browser within seconds.
- **Validation gates** — the six README commands with `--module 16-radiation-solids`, plus:
  a physics test pinning `radiation.mode_occupation` against a brute-force Boltzmann sum
  from `partition.py` (the C4b consistency 17 will later re-verify from the BE side).
- **Open questions for the author** —
  1. Real data vs synthetic (the pinned question). **Recommend: real.** NIST-JANAF/CODATA
     heat-capacity tables and NASA LAMBDA FIRAS are public-domain US-government data; ship
     CSVs under `data/` with source citations in a header comment. Keep
     `synthetic_heat_capacity` as the documented fallback if a source's terms disappoint.
  2. Which spectral quantity to plot: energy density $u_\nu$ vs radiance $B_\nu = (c/4\pi)
     u_\nu$. **Recommend:** $u_\nu$ on page and in code (matches the derivation), one boxed
     line giving the radiance conversion for lab-instrument comparisons (FIRAS is radiance).
  3. Include the zero-point term as a toggle in the explorer? **Recommend:** no — one
     admonition line; a toggle invites confusing the constant shift with a measurable $C$.
  4. Greenhouse toy vs phonon dispersion for the advanced section. **Recommend:** the
     greenhouse toy — topical, one page, pure radiation balance reusing `photon_gas`
     scaling; dispersion needs lattice machinery the course never builds.

## 4. Library and tests

- **`src/thermolab` — existing used:** `constants.py` (`K_B`); `partition.py` (12's
  oscillator $Z$ and $U$-from-$\ln Z$, consumed for the inline occupation box and the lab's
  re-enactment); `validation.py` (`convergence_study`, `scaling_exponent`,
  `relative_error`); `units.py` (test-side dimensional checks).
- **`src/thermolab` — new:** `radiation.py` (ownership table: introduced by 16, extended by
  none; serves 16, 17). Since `constants.py` is never extended (README ownership), the SI
  2019 exact values live here as module constants: `H_PLANCK = 6.62607015e-34`,
  `HBAR = H_PLANCK/(2*pi)`, `C_LIGHT = 299792458.0`. Docstring header, 7 bullets in fixed
  order — System: cavity radiation as independent quantized modes, and crystals as $3N$
  quantized oscillators (one shared frequency: Einstein; sound-wave spectrum with cutoff:
  Debye) / Dynamics: none — equilibrium thermodynamics only / Boundary: modes thermalized by
  walls (or the lattice) acting as a canonical bath at $T$ / Ensemble: canonical per mode,
  $\mu = 0$ where number is unconstrained / Ignored: zero-point energy, emissivity < 1,
  photon interactions, real phonon dispersion, electronic heat capacity / Valid when: mode
  spacing $\ll \kB T$-scale features; insulating or high-$T$ solids / Failure modes: tiny or
  ultracold cavities, non-thermal light, metals at mK temperatures, strongly anharmonic
  crystals. Functions (signature + one-line contract):
  - `mode_occupation(hbar_omega: float, temperature: float) -> float` — mean quanta
    $1/(e^{\hbar\omega/\kB T} - 1)$; the C4b inline result, 17's BE-at-$\mu{=}0$ anchor.
  - `planck_u_nu(nu, temperature) -> np.ndarray` — $u_\nu$ [J s m^-3], vectorized over `nu`.
  - `planck_u_lambda(lam, temperature) -> np.ndarray` — $u_\lambda$ [J m^-4]; implemented via
    the Jacobian from `planck_u_nu`, so the change of variables is code, not a copy.
  - `wien_peak_nu(temperature) -> float` / `wien_peak_lambda(temperature) -> float` — peak
    locations from the two transcendental roots (2.821439, 4.965114), cached constants.
  - `stefan_boltzmann_check(temperature, n_points=2048) -> tuple[float, float]` — (numeric
    $\int u_\nu\,\mathrm{d}\nu$, closed-form $a T^4$); the verify section's engine.
  - `photon_gas(temperature) -> tuple[float, float, float]` — per-volume $(u, P, s)$ =
    $(aT^4,\, u/3,\, \frac{4}{3}aT^3)$.
  - `einstein_heat_capacity(temperature, theta_e: float, n: int) -> np.ndarray` — $C(T)$,
    overflow-safe at $T \ll \theta_E$ (returns 0.0, not NaN).
  - `debye_heat_capacity(temperature, theta_d: float, n: int, n_quad: int = 64) ->
    np.ndarray` — Debye integral by fixed Gauss–Legendre; exact $3N\kB$/$T^3$ limits honored.
  - `fit_einstein_temperature(temperatures, heat_capacities, n) -> tuple[float, float]` /
    `fit_debye_temperature(...) -> tuple[float, float]` — least-squares $\theta$ ± 1σ from
    the fit curvature; the lab's measurement cells.
  - `synthetic_heat_capacity(temperatures, theta_d, n, rng, noise=0.02) -> np.ndarray` —
    Debye curve + relative Gaussian noise; the documented real-data fallback.
- **`tests/physics/` additions** (six categories):
  - *dimensional:* `planck_u_nu` → J s m^-3 and `planck_u_lambda` → J m^-4 under `pint`
    re-evaluation; `photon_gas` → (J m^-3, Pa, J K^-1 m^-3); heat capacities → J/K.
  - *conservation:* $\int u_\nu\,\mathrm{d}\nu = \int u_\lambda\,\mathrm{d}\lambda$ to
    quadrature tolerance (same energy, either variable); photon-gas Euler identity
    $u = Ts - P$ (with $\mu = 0$) exact.
  - *analytic-limit:* Rayleigh–Jeans recovered — `planck_u_nu` → $8\pi\nu^2 \kB T/c^3$ for
    $h\nu \ll \kB T$; Wien-tail exponential for the opposite; `stefan_boltzmann_check`
    numeric vs $\zeta(4)$ closed form to 1e-10; `wien_peak_*` against a brute-force argmax
    on a fine grid; Einstein $C \to 3N\kB$ at $T = 100\,\theta_E$; Einstein ≡ Debye at high
    $T$; Debye low-$T$ value vs $(12\pi^4/5) N\kB (T/\theta_D)^3$.
  - *large-N (scaling):* `validation.scaling_exponent` of $u(T)$ → 4.0; of Debye $C(T)$ at
    $T \le \theta_D/50$ → 3.0; Einstein's same-window exponent ≫ 3 (the models are
    distinguishable in code, as in the data).
  - *convergence:* `convergence_study` on `debye_heat_capacity` over `n_quad` against a
    high-order reference — Gauss–Legendre's fast decay observed; `stefan_boltzmann_check`
    error shrinking with `n_points` at the expected order.
  - *seed-independence:* n/a for the physics — all deterministic, no RNG; the one stochastic
    helper `synthetic_heat_capacity` gets a `validation.seed_study` check that fitted
    $\theta_D$ agrees with the injected truth within 3σ across seeds.

## 5. Assessment hooks

Checkpoint synthesis (module-level, not one section): (a) 12 + 16 — from the oscillator $Z$
alone, rebuild the full chain $Z \to \langle E\rangle \to$ Planck $\to a T^4$ numerically and
flag each step's epistemic label; (b) 01 + 16 — revisit 01's two-body exchange with
temperature-dependent Einstein $C(T)$ replacing $C = n\kB$: recompute $T_{eq}$ and show 01's
answer is the high-$T$ limit; (c) data verdict — given one low-$T$ heat-capacity row, decide
Einstein / Debye / neither, tolerance stated first. Exam themes: dual-peak trap under time
pressure; $T^4$/$T^3$ scaling estimates; classify-the-claim on the quantization hypothesis.
Feeds forward: 17's occupation-explorer capstone opens with this module's Planck curve as the
$\mu = 0$ special case (C4b), and 17's BEC discussion reuses `photon_gas` as the "massless,
number-unconstrained" contrast.

## 6. Build order and validation gates

Builds after 12 (needs `partition.py` in place for the inline-occupation consistency test and
the lab's re-enactment) and before 17 (which recomputes the Planck curve from
`quantum.bose_einstein(mu=0)` — C4b forbids any import the other way). Lands together in one
change: page + problems + lab + quiz bank; `radiation.py` with its test file; the three NEW
misconception entries (status `addressed`) in `assessment/misconceptions.yml`; the thirteen
NEW glossary keys in `glossary/terms.yml` with `he_reject` candidates; the data CSVs under
`data/` with source-citation headers (or the synthetic fallback wired in the lab); the three
MP4s from `media/render/render_radiation.py`. HE mirror family (`.he.yml` quiz, HE
page/problems/lab with `en_source_hash` stamps) follows; until it lands the page is listed in
`translation-pending.txt`. Gates: the six README commands with `--module 16-radiation-solids`
plus the `mode_occupation`-vs-`partition.py` pin from §3.

## 7. Deviations from the brainstorm

- **C4b inline occupation (README conflict log).** The Planck/Bose occupation is derived
  self-contained here from 12's oscillator $Z$, because 17 does not exist yet at build time;
  17's verify section later recomputes the curve from `quantum.bose_einstein(mu=0)`.
  Rationale: no file introduced by a later module is imported by an earlier one.
- **Photon-gas thermodynamics kept brief (pinned scope).** $P = u/3$, $S \propto T^3$, and a
  one-line $\mu = 0$ only — the grand-canonical treatment belongs to 13/17. Rationale: the
  module's story is the quantization fix, not gas thermodynamics.
- **Dual-peak lesson promoted from §5 remark to module signature (enhancement).** The
  brainstorm notes the peak depends on the plotted variable; this plan makes it the boxed
  central lesson, a misconception entry, a quiz trap and the page's title animation.
- **Real data recommended over synthetic (addition, pinned open question).** NIST-JANAF/
  CODATA-style $C_P$ for diamond/silver/copper and the COBE/FIRAS CMB monopole are
  recommended as shipped CSVs (public-domain US-government sources), with a documented
  rng-based fallback. Rationale: "experiments decide" (invariant 4) deserves real points.
- **Physical constants placed in `radiation.py` (decision).** $h$, $\hbar$, $c$ live as
  module constants because README ownership forbids extending `constants.py`. One-line
  comment in the file points back to this plan.
- **Greenhouse toy added as the advanced section (addition).** Not in the brainstorm row;
  chosen over phonon dispersion as topical, one-page, and purely radiation-balance.
