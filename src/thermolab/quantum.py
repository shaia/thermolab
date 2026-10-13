"""Quantum statistics: identical particles, and the two ways they can share a state.

MODEL SPECIFICATION
    System:        an ideal gas of identical, noninteracting particles -- bosons, fermions, or
                   classical particles for comparison -- in a rigid cubic box of volume V;
                   each particle's states are the standing waves of the box, each one g_s-fold
                   degenerate in spin
    Dynamics:      none -- equilibrium occupations are evaluated directly; the only random
                   numbers anywhere are the ones `sample_occupation` and
                   `synthetic_metal_heat_capacity` draw, through a passed generator
    Boundary:      every single-particle state exchanges energy and particles with a reservoir
                   at temperature T and chemical potential mu; the mean particle number is
                   held fixed by solving for mu
    Ensemble:      grand canonical, state by state (module 13's one-site trick, applied to
                   every standing wave of the box)
    Ignored:       every interaction between the particles -- no collisions, no mean field, no
                   force of any kind; trap geometry (a uniform box only); relativity (except
                   where the white-dwarf estimate checks whether it may be ignored); for
                   electrons, the crystal lattice beyond a free-electron box (band structure,
                   effective masses)
    Valid when:    the spacing of the box's levels is far below k_B T (and, for fermions, below
                   eps_F), so a smooth density of states can replace the sum over levels; for
                   the condensation argument, N >> 1
    Failure modes: liquid helium-4, whose atoms interact strongly (the ideal-gas T_c is
                   3.13 K, the measured lambda point 2.17 K); real metals, whose electrons feel
                   the lattice (copper's measured gamma is 1.38 times the free-electron value);
                   a few hundred particles, where condensation is a smooth crossover rather than
                   a sharp transition; white dwarfs near the Chandrasekhar mass, where the
                   electrons are relativistic

THE ONE IDEA
    A single-particle state -- one standing wave of the box, with one spin orientation -- holds
    any number of identical bosons but at most one identical fermion. That is the only quantum
    input. Treat each state as module 13's one-site system in contact with a reservoir at
    (T, mu): its grand sum over the allowed occupations is module 12's geometric series for
    bosons, and two terms for fermions. The mean occupations follow in one line each,

        n_BE = 1 / (exp((eps - mu)/k_B T) - 1),     n_FD = 1 / (exp((eps - mu)/k_B T) + 1),

    and both become the classical exp(-(eps - mu)/k_B T) when that exponential is large.
    Everything else in this module is those occupations summed over the box's states, at the
    mu that makes the sum come out to the number of particles there are.

ONE INTEGRAL DOES ALL THE WORK
    With x = eps / (k_B T) and eta = mu / (k_B T), the number density of the gas is

        n lambda^3 = g_s F_{3/2}(eta),
        F_s(eta) = (1/Gamma(s)) integral_0^inf x^(s-1) n(x - eta) dx,

    lambda = h / sqrt(2 pi m k_B T) the thermal wavelength. F_s is a pure function of one
    number. For classical particles it is exp(eta) exactly, so mu = k_B T ln(n lambda^3 / g_s),
    module 13's formula with n_Q = 1 / lambda^3 now derived. For bosons F_{3/2}(eta) cannot
    exceed F_{3/2}(0) = zeta(3/2) = 2.612 -- the excited states fill up, and the ground state
    takes the rest: Bose-Einstein condensation. The energy and the pressure need F_{5/2}, the
    heat capacity F_{1/2} as well.

    `occupation_integral` evaluates F_s by quadrature, and knows nothing of zeta functions;
    that the quadrature at eta = 0 returns zeta(3/2) to thirteen digits is a test, not an input.

THE NUMERICAL CORE
    Substituting x = y^2 turns each integral into one over y of an even, smooth function that
    vanishes, with all its derivatives, at the far end. For exactly such integrands the plain
    trapezoidal rule is not second order but exponentially accurate -- every correction term
    of the Euler-Maclaurin formula vanishes -- with an error set by how close the integrand's
    nearest complex singularity lies to the real axis. One case puts a singularity close: a
    Bose gas just above T_c, where n_BE has a pole at x = -a, a = -eta -> 0. There the pole's
    part, exp(-u) / u with u = x + a, is subtracted from the integrand and integrated in closed
    form (it needs only the complementary error function), so the remainder is smooth at every
    temperature. Roots in eta are found by bisection between bounds that follow from comparing
    the three occupations, never by guessing.

THE CONSTANTS
    hbar comes from `partition.H_BAR` and c from `radiation.C_LIGHT`; `constants` is consumed
    by this course and never extended. The electron and helium-4 masses, the gravitational
    constant and the solar mass are defined here (CODATA 2018; IAU 2015), because only this
    module needs them. zeta(3/2) and zeta(5/2)
    are typed, to sixteen digits, and tested against the quadrature.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Final

import numpy as np

from .constants import AMU, K_B, N_A
from .partition import H_BAR, thermal_wavelength
from .radiation import C_LIGHT, debye_low_t

#: Electron mass [kg] (CODATA 2018).
M_ELECTRON: Final[float] = 9.1093837015e-31

#: Mass of a helium-4 atom [kg]: 4.002603254 u (AME 2016).
M_HELIUM4: Final[float] = 4.002603254 * AMU

#: Newtonian gravitational constant [m^3 kg^-1 s^-2] (CODATA 2018), for the white-dwarf estimate.
GRAVITATIONAL_CONSTANT: Final[float] = 6.67430e-11

#: Solar mass [kg]: the IAU 2015 nominal G M_sun = 1.3271244e20 m^3 s^-2, divided by G.
SOLAR_MASS: Final[float] = 1.3271244e20 / GRAVITATIONAL_CONSTANT

#: Riemann zeta(3/2) = sum 1/n^(3/2): the most the excited states of a Bose gas can hold, in
#: units of g_s V / lambda^3.
ZETA_3_2: Final[float] = 2.612375348685488

#: Riemann zeta(5/2): sets the energy and the pressure of a Bose gas below T_c.
ZETA_5_2: Final[float] = 1.341487257250917

#: The three statistics, by the name every function here accepts.
STATISTICS: Final[tuple[str, ...]] = ("be", "fd", "mb")

#: How far past max(eta, 0), in units of k_B T, the integrals run. The integrand there is
#: below exp(-60) = 1e-26 of its size near the top of the occupied range: below double precision.
X_TAIL: Final[float] = 60.0

#: Default number of trapezoid intervals in `occupation_integral`. Ample everywhere but deep
#: in a degenerate Fermi gas, whose occupation drops from 1 to 0 within a few k_B T of eps_F;
#: the grid must resolve that edge, so eta may not exceed a quarter of the interval count.
DEFAULT_POINTS: Final[int] = 4096

_BISECT_MAX_ITER: Final[int] = 400


def _check_statistics(statistics: str) -> None:
    if statistics not in STATISTICS:
        raise ValueError(f"statistics must be one of {STATISTICS}, got {statistics!r}")


def _check_spin(spin_degeneracy) -> None:
    """g_s = 2s + 1 counts spin states: a whole number, at least one. Every public function
    that takes it checks it here, so a zero or negative value never reaches a division."""
    if spin_degeneracy < 1 or int(spin_degeneracy) != spin_degeneracy:
        raise ValueError("spin_degeneracy must be a whole number, at least 1")


def _positive(name: str, value) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if np.any(array <= 0):
        raise ValueError(f"{name} must be positive")
    return array


def _as_float_or_array(value):
    return float(value) if np.ndim(value) == 0 else value


def _reduced_energy(eps, mu, temperature) -> np.ndarray:
    """x = (eps - mu) / (k_B T), the one number every occupation depends on."""
    t = _positive("temperature", temperature)
    return (np.asarray(eps, dtype=float) - np.asarray(mu, dtype=float)) / (K_B * t)


def _occupation_x(x: np.ndarray, statistics: str) -> np.ndarray:
    """Mean occupation as a function of x = (eps - mu) / (k_B T); no checks, for internal use."""
    if statistics == "be":
        return np.exp(-x) / -np.expm1(-x)
    if statistics == "fd":
        e = np.exp(-np.abs(x))
        return np.where(x >= 0, e / (1.0 + e), 1.0 / (1.0 + e))
    return np.exp(-x)


# ---------------------------------------------------------------------------
# Counting: the symmetry postulate
# ---------------------------------------------------------------------------


def count_states(n_levels: int, n_particles: int, statistics: str) -> int:
    """Number of distinct many-particle states of N particles in M single-particle levels.

    "mb": distinguishable particles, each placed independently, M^N. "be": identical bosons,
    any number per level, C(M + N - 1, N). "fd": identical fermions, at most one per level,
    C(M, N). Two particles in two levels give 4, 3 and 1.
    """
    _check_statistics(statistics)
    if n_levels < 1 or n_particles < 0:
        raise ValueError("need at least one level and a non-negative number of particles")
    if statistics == "mb":
        return n_levels**n_particles
    if statistics == "be":
        return math.comb(n_levels + n_particles - 1, n_particles)
    return math.comb(n_levels, n_particles)


def enumerate_states(n_levels: int, n_particles: int, statistics: str) -> np.ndarray:
    """Every many-particle state, written as its occupation numbers (one row per state).

    For "mb" the rows are the M^N ways of assigning each labelled particle to a level, so an
    occupation pattern appears once per assignment -- two particles split between two levels
    appear twice, as (particle 1 here, particle 2 there) and the reverse. For identical
    particles each pattern is one state, and fermions are allowed no entry above one.
    """
    count = count_states(n_levels, n_particles, statistics)
    if count > 1_000_000:
        raise ValueError("too many states to list; use count_states")
    if statistics == "mb":
        placements = itertools.product(range(n_levels), repeat=n_particles)
    elif statistics == "be":
        placements = itertools.combinations_with_replacement(range(n_levels), n_particles)
    else:
        placements = itertools.combinations(range(n_levels), n_particles)
    rows = [np.bincount(np.asarray(p, dtype=int), minlength=n_levels) for p in placements]
    return np.array(rows, dtype=int).reshape(count, n_levels)


# ---------------------------------------------------------------------------
# One state in contact with a reservoir at (T, mu)
# ---------------------------------------------------------------------------


def bose_einstein(eps, mu, temperature):
    """n_BE = 1 / (exp((eps - mu) / (k_B T)) - 1): mean number of bosons in a state of energy eps.

    The grand sum over n = 0, 1, 2, ... converges only if mu < eps, so this raises unless mu
    lies below every eps passed. mu = 0 is the photon (and phonon) case, module 16's <n>.
    Written as e^-x / (1 - e^-x), exact for small x and quietly zero for large x. Dimensionless.
    """
    x = _reduced_energy(eps, mu, temperature)
    if np.any(x <= 0):
        raise ValueError("a boson state at or below mu would hold infinitely many particles: "
                         "need mu < eps")
    return _as_float_or_array(_occupation_x(x, "be"))


def fermi_dirac(eps, mu, temperature):
    """n_FD = 1 / (exp((eps - mu) / (k_B T)) + 1): mean number of fermions in a state of energy eps.

    Between 0 and 1 for every eps and mu, which is the exclusion principle averaged; it is 1/2
    at eps = mu. Evaluated through exp(-|x|) on both sides, so neither tail overflows and the
    far tail keeps its full relative precision. Dimensionless.
    """
    return _as_float_or_array(_occupation_x(_reduced_energy(eps, mu, temperature), "fd"))


def maxwell_boltzmann(eps, mu, temperature):
    """n_MB = exp(-(eps - mu) / (k_B T)): the classical occupation, both quantum ones' dilute limit.

    It exceeds 1 when eps < mu, which is where it stops describing anything real. Dimensionless.
    """
    return _as_float_or_array(_occupation_x(_reduced_energy(eps, mu, temperature), "mb"))


def occupation(eps, mu, temperature, statistics: str):
    """The mean occupation under the named statistics: "be", "fd" or "mb". Dimensionless."""
    _check_statistics(statistics)
    return {"be": bose_einstein, "fd": fermi_dirac, "mb": maxwell_boltzmann}[statistics](
        eps, mu, temperature)


def occupation_variance(eps, mu, temperature, statistics: str):
    """Variance of the number of particles in one state: n(1 + n), n(1 - n) or n. Dimensionless.

    Bosons fluctuate more than classical particles (the geometric distribution), fermions less
    (a yes-or-no variable), and classical particles in between (Poisson). The extra n^2 for
    bosons is the "bunching" of photons that a photon counter measures.
    """
    n = np.asarray(occupation(eps, mu, temperature, statistics), dtype=float)
    sign = {"be": 1.0, "fd": -1.0, "mb": 0.0}[statistics]
    return _as_float_or_array(n * (1.0 + sign * n))


def explicit_occupation(eps: float, mu: float, temperature: float, statistics: str,
                        n_max: int = 4000) -> tuple[float, float]:
    """(mean, variance) of one state's occupation, by summing its grand-canonical weights.

    The weight of occupation n is exp(-n (eps - mu) / (k_B T)), divided by n! for classical
    particles; n runs over 0..n_max for bosons and classical particles and over {0, 1} for
    fermions. No closed form is used: this is what `bose_einstein` and its siblings are tested
    against. For bosons the truncation needs n_max (eps - mu) / (k_B T) well above 40.
    """
    _check_statistics(statistics)
    x = float(_reduced_energy(eps, mu, temperature))
    if statistics == "fd":
        n = np.array([0.0, 1.0])
        log_w = -n * x
    else:
        if statistics == "be" and x <= 0:
            raise ValueError("need mu < eps for bosons")
        if statistics == "be" and n_max * x < 40.0:
            raise ValueError("n_max too small for this occupation: need n_max (eps - mu) / kT > 40")
        n = np.arange(n_max + 1, dtype=float)
        log_w = -n * x
        if statistics == "mb":
            log_w = log_w - np.array([math.lgamma(k + 1.0) for k in n])
    w = np.exp(log_w - log_w.max())
    w /= w.sum()
    mean = float(np.sum(n * w))
    return mean, float(np.sum((n - mean) ** 2 * w))


def sample_occupation(eps: float, mu: float, temperature: float, statistics: str, size: int,
                      rng: np.random.Generator) -> np.ndarray:
    """Draw `size` independent occupations of one state from its grand-canonical distribution.

    Bosons: geometric, P(n) = (1 - e^-x) e^(-n x). Fermions: 0 or 1, with P(1) = n_FD.
    Classical: Poisson with mean e^-x. Every draw goes through the passed generator.
    """
    _check_statistics(statistics)
    x = float(_reduced_energy(eps, mu, temperature))
    if statistics == "be":
        if x <= 0:
            raise ValueError("need mu < eps for bosons")
        return rng.geometric(-math.expm1(-x), size) - 1
    if statistics == "fd":
        return (rng.random(size) < float(_occupation_x(np.array(x), "fd"))).astype(int)
    return rng.poisson(math.exp(-x), size)


# ---------------------------------------------------------------------------
# The states of a box
# ---------------------------------------------------------------------------


def box_level_unit(side: float, mass: float) -> float:
    """eps_1 = hbar^2 pi^2 / (2 m L^2) [J]: a standing wave (n_x, n_y, n_z) has energy eps_1 |n|^2.

    A particle's standing wave in a cube of side L with hard walls has k = (pi / L)(n_x, n_y,
    n_z), every n a positive integer -- module 16's cavity modes -- and energy hbar^2 k^2 / 2m.
    """
    if side <= 0 or mass <= 0:
        raise ValueError("side and mass must be positive")
    return (H_BAR * math.pi / side) ** 2 / (2.0 * mass)


def count_box_states(side: float, mass: float, eps_max: float, spin_degeneracy: int = 1) -> int:
    """Count the single-particle states of a cube with energy at most eps_max, one by one.

    Enumerates the positive-integer triples with eps_1 (n_x^2 + n_y^2 + n_z^2) <= eps_max, times
    the spin degeneracy -- no octant, no sphere, no continuum -- so that the smooth count can be
    tested against the thing it approximates. As for module 16's cavity, the smooth count
    overshoots by the states it pretends lie on the octant's faces, a relative error of order
    1 / |n|.
    """
    _check_spin(spin_degeneracy)
    radius = math.sqrt(eps_max / box_level_unit(side, mass)) if eps_max > 0 else 0.0
    n_top = int(math.floor(radius))
    if n_top > 4000:
        raise ValueError("too many states to enumerate; that many is a continuum")
    if n_top < 1:
        return 0
    n = np.arange(1, n_top + 1, dtype=float)
    remaining = radius**2 - n[:, None] ** 2 - n[None, :] ** 2
    nz = np.floor(np.sqrt(np.clip(remaining, 0.0, None)))
    return int(spin_degeneracy * nz[remaining >= 1.0].sum())


def smooth_state_count(side: float, mass: float, eps_max: float, spin_degeneracy: int = 1) -> float:
    """The continuum count N(eps) = g_s V (2 m eps / hbar^2)^(3/2) / (6 pi^2) that
    `count_box_states` tests."""
    _check_spin(spin_degeneracy)
    if side <= 0 or mass <= 0 or eps_max < 0:
        raise ValueError("side and mass must be positive and eps_max non-negative")
    return spin_degeneracy * side**3 * (2.0 * mass * eps_max / H_BAR**2) ** 1.5 / (6.0 * math.pi**2)


def density_of_states_3d(eps, volume: float, mass: float, spin_degeneracy: int = 1):
    """g(eps) = g_s V (2m / hbar^2)^(3/2) sqrt(eps) / (4 pi^2): states per unit energy [1/J].

    The derivative of `smooth_state_count`. The spin degeneracy is an explicit argument, never
    a hidden factor: 1 for spinless bosons such as helium-4, 2 for electrons.
    """
    _check_spin(spin_degeneracy)
    if volume <= 0 or mass <= 0:
        raise ValueError("volume and mass must be positive")
    eps = np.asarray(eps, dtype=float)
    if np.any(eps < 0):
        raise ValueError("eps must be non-negative")
    return _as_float_or_array(spin_degeneracy * volume * (2.0 * mass / H_BAR**2) ** 1.5
                              * np.sqrt(eps) / (4.0 * math.pi**2))


def box_level_degeneracies(s_max: int) -> np.ndarray:
    """d[s] = the number of positive-integer triples with n_x^2 + n_y^2 + n_z^2 = s, for s <= s_max.

    The levels of a cube are eps_1 s; the ground level is s = 3, (1, 1, 1). Built by counting
    the pairs n_x^2 + n_y^2 first, then adding each n_z^2 -- a sum of three squares as a
    convolution, done by shifting.
    """
    if s_max < 3:
        raise ValueError("s_max must be at least 3, the ground level")
    if s_max > 2_000_000:
        raise ValueError("s_max too large; that many levels is a continuum")
    squares = np.arange(1, math.isqrt(s_max) + 1) ** 2
    pair_sums = (squares[:, None] + squares[None, :]).ravel()
    pairs = np.bincount(pair_sums[pair_sums <= s_max], minlength=s_max + 1)
    triples = np.zeros(s_max + 1, dtype=np.int64)
    for q in squares:
        triples[q:] += pairs[: s_max + 1 - q]
    return triples


# ---------------------------------------------------------------------------
# Holding N fixed: the occupation integrals, and mu
# ---------------------------------------------------------------------------


def degeneracy_parameter(number_density, temperature, mass: float):
    """n lambda^3 = n / n_Q: the classical criterion. A gas is classical when it is << 1.

    lambda = h / sqrt(2 pi m k_B T) is module 12's thermal wavelength, and 1 / lambda^3 is
    module 13's quantum concentration. Dimensionless.
    """
    n = _positive("number_density", number_density)
    lam = np.asarray(thermal_wavelength(temperature, mass), dtype=float)
    return _as_float_or_array(n * lam**3)


def _check_order(order: float) -> None:
    if order < 0.5 or abs(2.0 * order - round(2.0 * order)) > 1e-12 or round(2 * order) % 2 == 0:
        raise ValueError("order must be a half-integer, at least 1/2")


def _trapezoid(values: np.ndarray, step: float) -> float:
    return float(step * (values.sum() - 0.5 * (values[0] + values[-1])))


def _bose_pole_integral(a: float, order: float) -> float:
    """K_s(a) = integral_0^inf x^(s-1) exp(-(x + a)) / (x + a) dx, in closed form, for a >= 0.

    K_{1/2}(a) = pi erfc(sqrt a) / sqrt a; K_{3/2}(a) = sqrt(pi) e^-a - pi sqrt(a) erfc(sqrt a);
    and K_{s+1}(a) = Gamma(s) e^-a - a K_s(a), since x / (x + a) = 1 - a / (x + a).
    """
    if order == 0.5:
        return math.inf if a == 0 else math.pi * math.erfc(math.sqrt(a)) / math.sqrt(a)
    value = math.sqrt(math.pi) * math.exp(-a) - math.pi * math.sqrt(a) * math.erfc(math.sqrt(a))
    s = 1.5
    while s < order - 1e-12:
        value = math.gamma(s) * math.exp(-a) - a * value
        s += 1.0
    return value


def occupation_integral(eta: float, statistics: str, order: float = 1.5,
                        n_points: int = DEFAULT_POINTS) -> float:
    """F_s(eta) = (1 / Gamma(s)) integral_0^inf x^(s-1) n(x - eta) dx, with eta = mu / (k_B T).

    The occupation-weighted count of states, made dimensionless: n lambda^3 = g_s F_{3/2}(eta)
    is the density, and F_{5/2} sets the energy and pressure, F_{1/2} the heat capacity.
    For "mb" it is exactly e^eta at every order. Bosons need eta <= 0, and F_{1/2} is infinite
    at eta = 0.

    Computed with x = y^2 by the trapezoidal rule on `n_points` intervals over
    0 <= y <= sqrt(max(eta, 0) + 60). The integrand in y is even and smooth, which makes the
    rule exponentially accurate; for bosons with -1 < eta <= 0 the pole of n_BE near the
    integration range is subtracted and integrated in closed form first (module docstring).
    Dimensionless.
    """
    _check_statistics(statistics)
    _check_order(order)
    if n_points < 16:
        raise ValueError("n_points must be at least 16")
    eta = float(eta)
    if statistics == "be" and eta > 0:
        raise ValueError("a Bose gas needs mu <= 0, the lowest state's energy")
    if statistics == "fd" and eta > n_points / 4:
        raise ValueError(f"eta = {eta:.0f} is too degenerate for {n_points} intervals: the "
                         f"Fermi edge would be unresolved. Raise n_points, or use the T = 0 forms")
    y_max = math.sqrt(max(eta, 0.0) + X_TAIL)
    y = np.linspace(0.0, y_max, n_points + 1)
    x = y * y
    weight = 2.0 * y ** (2.0 * order - 1.0)
    if statistics == "be" and eta > -1.0:
        a = -eta
        if order == 0.5 and a == 0.0:
            return math.inf
        u = x + a
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            direct = 1.0 / np.expm1(u) - np.exp(-u) / u
        # n_BE(u) - e^-u / u is smooth at u = 0; near it both terms are ~1/u, so use the series.
        series = 0.5 - 5.0 * u / 12.0 + u * u / 6.0 - 31.0 * u**3 / 720.0
        remainder = np.where(u < 1e-3, series, direct)
        integral = _trapezoid(weight * remainder, y_max / n_points) + _bose_pole_integral(a, order)
    else:
        integral = _trapezoid(weight * _occupation_x(x - eta, statistics), y_max / n_points)
    return integral / math.gamma(order)


def solve_eta(reduced_density: float, statistics: str, n_points: int = DEFAULT_POINTS) -> float:
    """The eta = mu / (k_B T) at which F_{3/2}(eta) equals n lambda^3 / g_s.

    Bisection, between bounds that come from comparing the occupations: n_BE >= n_MB >= n_FD
    term by term, so F_FD(eta) <= e^eta <= F_BE(eta), and the classical root ln(n lambda^3 / g_s)
    lies above every Bose root and below every Fermi root. A Bose gas whose density reaches
    zeta(3/2) has eta = 0: the excited states are full, and the rest is the condensate.
    """
    _check_statistics(statistics)
    target = float(reduced_density)
    if not target > 0:
        raise ValueError("reduced_density must be positive")
    log_t = math.log(target)
    if statistics == "be":
        if target >= ZETA_3_2:
            return 0.0
        # F_BE(eta) <= zeta(3/2) e^eta (geometric bound on the series), and >= e^eta.
        lo, hi = log_t - math.log(ZETA_3_2), min(log_t, 0.0)
    elif statistics == "mb":
        lo, hi = log_t - 1.0, log_t + 1.0
    else:
        # F_FD(eta) <= e^eta; F_FD(eta) >= e^eta / 2 for eta <= 0, and >= its T = 0 value
        # (4 / (3 sqrt pi)) eta^(3/2) for eta > 0 (the edge's excess outweighs its deficit).
        eta_zero_t = (0.75 * math.sqrt(math.pi) * target) ** (2.0 / 3.0)
        lo, hi = log_t, max(math.log(2.0 * target), eta_zero_t)

    for _ in range(_BISECT_MAX_ITER):
        mid = 0.5 * (lo + hi)
        if hi - lo <= 4.0 * np.finfo(float).eps * max(1.0, abs(lo), abs(hi)):
            break
        if occupation_integral(mid, statistics, 1.5, n_points) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def solve_mu(number_density: float, temperature: float, mass: float, statistics: str,
             spin_degeneracy: int = 1, n_points: int = DEFAULT_POINTS) -> float:
    """The chemical potential [J] at which the gas holds `number_density` particles per m^3.

    Solves n = integral g(eps) n(eps; mu, T) d eps / V for mu, the zero of energy at the bottom
    of the box. Classical: mu = k_B T ln(n lambda^3 / g_s), negative when the gas is dilute.
    Bosons: mu climbs toward 0 as T falls and stays there below T_c. Fermions: mu climbs to
    eps_F as T -> 0.
    """
    t = float(_positive("temperature", temperature))
    _check_spin(spin_degeneracy)
    reduced = float(degeneracy_parameter(number_density, t, mass)) / spin_degeneracy
    return K_B * t * solve_eta(reduced, statistics, n_points)


@dataclass(frozen=True)
class IdealQuantumGas:
    """An ideal gas at fixed density and temperature, with mu solved for (SI units).

    `condensate_fraction` is N_0 / N, nonzero only for bosons below T_c. Energies are per
    particle and measured from the bottom of the box; the heat capacity is C_V / N.
    """

    statistics: str
    temperature: float
    number_density: float
    spin_degeneracy: int
    mu: float                          # [J]
    degeneracy_parameter: float        # n lambda^3
    condensate_fraction: float
    energy_per_particle: float         # [J]
    pressure: float                    # [Pa]
    heat_capacity_per_particle: float  # [J/K]

    @property
    def classical_pressure(self) -> float:
        """n k_B T [Pa], the pressure the same gas would have if it were classical."""
        return self.number_density * K_B * self.temperature


def ideal_quantum_gas(number_density: float, temperature: float, mass: float, statistics: str,
                      spin_degeneracy: int = 1, n_points: int = DEFAULT_POINTS) -> IdealQuantumGas:
    """Solve for mu and evaluate the energy, pressure and heat capacity of an ideal gas.

    U / N = (3/2) k_B T g_s F_{5/2}(eta) / (n lambda^3); P = (2/3) U / V for every ideal
    nonrelativistic gas, whatever its statistics; and at fixed N and V,

        C_V / (N k_B) = (15/4) F_{5/2} / F_{3/2} - (9/4) F_{3/2} / F_{1/2},

    which is 3/2 for a classical gas. Below T_c a Bose gas has eta = 0, only its excited
    particles carry energy, U grows as T^(5/2), and
    C_V / (N k_B) = (15/4) g_s zeta(5/2) / (n lambda^3).
    """
    _check_statistics(statistics)
    _check_spin(spin_degeneracy)
    t = float(_positive("temperature", temperature))
    d = float(degeneracy_parameter(number_density, t, mass))
    eta = solve_eta(d / spin_degeneracy, statistics, n_points)
    f52 = occupation_integral(eta, statistics, 2.5, n_points)
    f32 = occupation_integral(eta, statistics, 1.5, n_points)
    energy = 1.5 * K_B * t * spin_degeneracy * f52 / d
    condensed = statistics == "be" and eta == 0.0
    if condensed:
        fraction = max(0.0, 1.0 - spin_degeneracy * f32 / d)
        heat_capacity = 2.5 * energy / t
    else:
        fraction = 0.0
        f12 = occupation_integral(eta, statistics, 0.5, n_points)
        heat_capacity = K_B * (3.75 * f52 / f32 - 2.25 * f32 / f12)
    return IdealQuantumGas(statistics=statistics, temperature=t,
                           number_density=float(number_density), spin_degeneracy=spin_degeneracy,
                           mu=K_B * t * eta, degeneracy_parameter=d, condensate_fraction=fraction,
                           energy_per_particle=energy,
                           pressure=2.0 / 3.0 * float(number_density) * energy,
                           heat_capacity_per_particle=heat_capacity)


# ---------------------------------------------------------------------------
# Bose-Einstein condensation
# ---------------------------------------------------------------------------


def bec_tc(number_density: float, mass: float, spin_degeneracy: int = 1) -> float:
    """T_c [K] from k_B T_c = (2 pi hbar^2 / m) (n / (g_s zeta(3/2)))^(2/3).

    Where n lambda^3 reaches g_s zeta(3/2): the temperature at which the excited states,
    filled to capacity, just hold every particle.
    """
    _check_spin(spin_degeneracy)
    if number_density <= 0 or mass <= 0:
        raise ValueError("number_density and mass must be positive")
    return (2.0 * math.pi * H_BAR**2 / (mass * K_B)
            * (number_density / (spin_degeneracy * ZETA_3_2)) ** (2.0 / 3.0))


def condensate_fraction(temperature, t_c: float):
    """N_0 / N = 1 - (T / T_c)^(3/2) below T_c, and 0 above it: the ideal gas in a box.

    The excited states hold at most g_s zeta(3/2) V / lambda^3, which falls as T^(3/2); the
    ground state takes whatever they cannot. Exact only as N -> infinity; see
    `finite_box_condensate_fraction`. Dimensionless.
    """
    if t_c <= 0:
        raise ValueError("t_c must be positive")
    t = np.asarray(temperature, dtype=float)
    if np.any(t < 0):
        raise ValueError("temperature must be non-negative")
    return _as_float_or_array(np.clip(1.0 - (t / t_c) ** 1.5, 0.0, None))


def finite_box_condensate_fraction(n_particles: int, t_over_tc, x_cut: float = 30.0):
    """N_0 / N for N spinless bosons in a hard-walled cube, from the explicit sum over its levels.

    No density of states and no integral: the levels eps_1 s with their degeneracies from
    `box_level_degeneracies`, each holding n_BE, and mu chosen so that the total is N. The
    temperature is given in units of the infinite system's T_c at the same density, for which
    k_B T_c / eps_1 = (4 / pi) (N / zeta(3/2))^(2/3). Levels more than `x_cut` k_B T above the
    ground level are dropped (their share is below e^-30).

    The unknown is solved as delta = (eps_ground - mu) / (k_B T) > 0, by bisection in ln(delta):
    the total N(delta) falls monotonically as delta grows, and the ground state alone holds N
    at delta = ln(1 + 1/N). As N grows the result approaches 1 - (T/T_c)^(3/2); at small N the
    transition is rounded into a crossover. (The grand canonical ensemble gets the ground
    state's mean occupation right and its fluctuations wrong below T_c; only the mean is used.)
    """
    if n_particles < 2 or n_particles > 1_000_000:
        raise ValueError("n_particles must lie between 2 and 1e6")
    temps = np.atleast_1d(np.asarray(t_over_tc, dtype=float))
    if np.any(temps < 0):
        raise ValueError("t_over_tc must be non-negative")
    tau_c = 4.0 / math.pi * (n_particles / ZETA_3_2) ** (2.0 / 3.0)
    s_max = 3 + int(math.ceil(x_cut * tau_c * max(float(temps.max()), 1e-9)))
    degeneracy = box_level_degeneracies(s_max)
    levels = np.nonzero(degeneracy)[0]
    levels = levels[levels > 3]
    weights = degeneracy[levels].astype(float)
    gaps = (levels - 3).astype(float)

    fractions = np.empty_like(temps)
    for i, t in enumerate(temps):
        if t == 0:
            fractions[i] = 1.0
            continue
        tau = t * tau_c

        def total(delta: float, tau=tau) -> float:
            # n_BE as e^-z / (1 - e^-z), which underflows quietly in the far tail.
            z = gaps / tau + delta
            excited = float(np.sum(weights * np.exp(-z) / -np.expm1(-z)))
            return math.exp(-delta) / -math.expm1(-delta) + excited

        lo = math.log(math.log1p(1.0 / n_particles))   # ln(delta): ground state alone holds N
        hi = lo
        while total(math.exp(hi)) > n_particles:
            hi += 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if hi - lo < 1e-13:
                break
            if total(math.exp(mid)) > n_particles:
                lo = mid
            else:
                hi = mid
        delta = math.exp(0.5 * (lo + hi))
        fractions[i] = math.exp(-delta) / -math.expm1(-delta) / n_particles
    return _as_float_or_array(fractions.reshape(np.shape(t_over_tc)))


# ---------------------------------------------------------------------------
# The degenerate Fermi gas
# ---------------------------------------------------------------------------


def fermi_wavevector(number_density, spin_degeneracy: int = 2):
    """k_F = (6 pi^2 n / g_s)^(1/3) [1/m]: (3 pi^2 n)^(1/3) for electrons."""
    _check_spin(spin_degeneracy)
    n = _positive("number_density", number_density)
    return _as_float_or_array((6.0 * math.pi**2 * n / spin_degeneracy) ** (1.0 / 3.0))


def fermi_energy(number_density, mass: float, spin_degeneracy: int = 2):
    """eps_F = (hbar^2 / 2m)(6 pi^2 n / g_s)^(2/3) [J]: the top of the T = 0 sea, hbar^2 k_F^2 / 2m.

    Fill the box's states from the bottom, g_s particles per standing wave, until N are placed;
    eps_F is the energy of the last. It depends on the density alone, not on the temperature.
    """
    if mass <= 0:
        raise ValueError("mass must be positive")
    k_f = np.asarray(fermi_wavevector(number_density, spin_degeneracy))
    return _as_float_or_array(H_BAR**2 * k_f**2 / (2.0 * mass))


def fermi_temperature(number_density, mass: float, spin_degeneracy: int = 2):
    """T_F = eps_F / k_B [K]. A Fermi gas is degenerate -- quantum -- when T << T_F."""
    return _as_float_or_array(np.asarray(fermi_energy(number_density, mass, spin_degeneracy)) / K_B)


def fermi_velocity(number_density, mass: float, spin_degeneracy: int = 2):
    """v_F = hbar k_F / m [m/s]: the speed of the fastest particles at T = 0."""
    if mass <= 0:
        raise ValueError("mass must be positive")
    return _as_float_or_array(H_BAR * np.asarray(fermi_wavevector(number_density, spin_degeneracy))
                              / mass)


def fermi_gas_energy(number_density, mass: float, spin_degeneracy: int = 2):
    """Mean energy per particle at T = 0, (3/5) eps_F [J]: the sea's average depth, never zero."""
    return _as_float_or_array(0.6 * np.asarray(fermi_energy(number_density, mass, spin_degeneracy)))


def fermi_gas_pressure(number_density, mass: float, spin_degeneracy: int = 2):
    """Degeneracy pressure at T = 0, P = (2/5) n eps_F [Pa].

    P = (2/3) U / V with U / N = (3/5) eps_F. The model behind it has no forces between the
    particles at all: the pressure is the kinetic energy that the exclusion rule forces the
    occupied states to have, delivered to the walls exactly as module 04 delivered it.
    """
    n = _positive("number_density", number_density)
    return _as_float_or_array(0.4 * n * np.asarray(fermi_energy(n, mass, spin_degeneracy)))


def electronic_heat_capacity(temperature, t_f: float, n: float = 1.0):
    """C_el = (pi^2 / 2) N k_B T / T_F [J/K]: the low-temperature heat capacity of a Fermi gas.

    The leading term of the Sommerfeld expansion, valid for T << T_F. Only a shell about k_B T
    deep at eps_F can be rearranged, so C is the classical (3/2) N k_B times a fraction of
    order T / T_F. `n` is the number of fermions (N_A for a mole of monovalent metal).
    """
    if t_f <= 0 or n <= 0:
        raise ValueError("t_f and n must be positive")
    t = np.asarray(temperature, dtype=float)
    if np.any(t < 0):
        raise ValueError("temperature must be non-negative")
    return _as_float_or_array(0.5 * math.pi**2 * n * K_B * t / t_f)


def free_electron_gamma(electron_density: float, electrons_per_atom: int = 1,
                        mass: float = M_ELECTRON) -> float:
    """The free-electron prediction for a metal's gamma in C_el = gamma T [J mol^-1 K^-2].

    Per mole of atoms, with z conduction electrons per atom: gamma = (pi^2 / 2) z R / T_F, T_F
    from the electron density for spin-1/2 electrons of the given mass.
    """
    if electrons_per_atom < 1:
        raise ValueError("electrons_per_atom must be at least one")
    t_f = float(fermi_temperature(electron_density, mass, 2))
    return 0.5 * math.pi**2 * electrons_per_atom * N_A * K_B / t_f


# ---------------------------------------------------------------------------
# A metal at low temperature: electrons plus lattice
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MetalFit:
    """A straight-line fit of C / T = gamma + beta T^2 to a metal's low-temperature heat capacity.

    gamma [J/K^2] is the electrons' coefficient and beta [J/K^4] the lattice's Debye T^3
    coefficient, each per `n` atoms (N_A: per mole). The sigmas are 1-sigma errors from the
    scatter of the points about the line; they assume the two-term model is right.
    """

    gamma: float
    gamma_sigma: float
    beta: float
    beta_sigma: float
    n: float
    residuals: np.ndarray   # (C/T measured) - (C/T fitted) [J/K^2]

    @property
    def debye_temperature(self) -> float:
        """theta_D from beta = (12 pi^4 / 5) N k_B / theta_D^3 [K]."""
        return (12.0 * math.pi**4 * self.n * K_B / (5.0 * self.beta)) ** (1.0 / 3.0)

    @property
    def debye_temperature_sigma(self) -> float:
        """1-sigma error of theta_D, propagated from beta: theta_D sigma_beta / (3 beta) [K]."""
        return self.debye_temperature * self.beta_sigma / (3.0 * self.beta)


def fit_metal_heat_capacity(temperatures, heat_capacities, n: float = N_A) -> MetalFit:
    """Least-squares line through C / T against T^2: intercept gamma, slope beta.

    For a metal well below its Debye temperature C = gamma T + beta T^3 -- this module's
    electrons plus module 16's phonons -- so C / T plotted against T^2 is a straight line.
    The errors scale the covariance by the residuals' scatter, sum(r^2) / (points - 2).
    """
    t = np.atleast_1d(_positive("temperature", temperatures))
    c = np.atleast_1d(_positive("heat capacity", heat_capacities))
    if t.shape != c.shape or len(t) < 3:
        raise ValueError("need matching arrays of at least three temperatures and heat capacities")
    design = np.column_stack([np.ones_like(t), t**2])
    y = c / t
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)
    residuals = y - design @ coefficients
    scatter = float(np.sum(residuals**2)) / (len(t) - 2)
    covariance = scatter * np.linalg.inv(design.T @ design)
    return MetalFit(gamma=float(coefficients[0]), gamma_sigma=float(math.sqrt(covariance[0, 0])),
                    beta=float(coefficients[1]), beta_sigma=float(math.sqrt(covariance[1, 1])),
                    n=float(n), residuals=residuals)


def synthetic_metal_heat_capacity(temperatures, gamma: float, theta_d: float,
                                  rng: np.random.Generator, n: float = N_A,
                                  noise: float = 0.02) -> np.ndarray:
    """gamma T plus module 16's Debye T^3 law, with Gaussian noise of relative size `noise` [J/K].

    The subject of the seed-independence test: a fit should recover the gamma put in, with an
    error bar that describes its scatter across generators.
    """
    if noise < 0:
        raise ValueError("noise must be non-negative")
    t = np.atleast_1d(_positive("temperature", temperatures))
    clean = gamma * t + np.asarray(debye_low_t(t, theta_d, n), dtype=float)
    return clean * (1.0 + noise * rng.standard_normal(clean.shape))


# ---------------------------------------------------------------------------
# Advanced: a star held up by degeneracy pressure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WhiteDwarf:
    """The order-of-magnitude white dwarf of a given mass (SI units)."""

    mass: float               # [kg]
    radius: float             # [m]
    electron_density: float   # mean n_e [1/m^3]
    fermi_energy: float       # at the mean density [J]

    @property
    def relativity(self) -> float:
        """p_F / (m_e c) at the mean density: the nonrelativistic estimate needs it << 1."""
        return float(math.sqrt(2.0 * M_ELECTRON * self.fermi_energy) / (M_ELECTRON * C_LIGHT))


def white_dwarf(mass: float, electrons_per_nucleon: float = 0.5) -> WhiteDwarf:
    """Radius at which a uniform ball of degenerate electrons balances its own gravity.

    The total energy is the electrons' (3/5) N_e eps_F, which grows as 1/R^2 when the star is
    squeezed, plus the gravitational -(3/5) G M^2 / R of a uniform sphere. The minimum is at

        R = (hbar^2 / m_e) (9 pi / 4)^(2/3) N_e^(5/3) / (G M^2),   N_e = Y_e M / m_u,

    so R falls as M^(-1/3): a heavier white dwarf is smaller. Uniform density, nonrelativistic
    electrons and zero temperature are all approximations; the answer is good to tens of
    percent, and `relativity` says how close the electrons are to the speed of light.
    """
    if mass <= 0 or not 0 < electrons_per_nucleon <= 1:
        raise ValueError("mass must be positive and electrons_per_nucleon in (0, 1]")
    n_e = electrons_per_nucleon * mass / AMU
    radius = (H_BAR**2 / M_ELECTRON * (9.0 * math.pi / 4.0) ** (2.0 / 3.0) * n_e ** (5.0 / 3.0)
              / (GRAVITATIONAL_CONSTANT * mass**2))
    density = n_e / (4.0 / 3.0 * math.pi * radius**3)
    return WhiteDwarf(mass=mass, radius=radius, electron_density=density,
                      fermi_energy=float(fermi_energy(density, M_ELECTRON, 2)))
