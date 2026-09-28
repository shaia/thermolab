"""Partition functions: everything a canonical system does, from one sum.

MODEL SPECIFICATION
    System:        discrete-level model systems whose levels are given inputs -- a two-level
                   system with gap Delta; N independent spin-1/2 moments mu in a field B, at
                   energies -mu B (aligned) and +mu B (anti-aligned); a harmonic ladder
                   E_n = hbar omega (n + 1/2) -- plus, for the advanced section only, the
                   semiclassical ideal gas, z = V / lambda^3
    Dynamics:      none -- equilibrium averages over the canonical distribution, evaluated as
                   closed forms or explicit sums; no sampling, and no random number anywhere
    Boundary:      contact with an infinite bath at temperature T (module 11's idealization,
                   whose error bar module 11 measured); at fixed levels no work is done, so
                   every change of U is heat
    Ensemble:      canonical, exactly: P_s = exp(-E_s / (k_B T)) / Z
    Ignored:       interactions between subsystems, level shifts beyond the linear Zeeman
                   term, and identical-particle exchange (which enters only the advanced
                   ideal gas, as the Gibbs 1/N!)
    Valid when:    the level spectrum is fixed and known, and the subsystems are independent,
                   so that Z_N = z^N
    Failure modes: interacting spins (module 15), quantum indistinguishability at high density
                   or low temperature (module 17), and levels that depend on the state
                   variables -- then ln Z's derivatives in beta are no longer the whole story

WHY THE NORMALIZATION KNOWS EVERYTHING
    ln Z(beta) is the generating function of the energy distribution: its first derivative is
    minus the mean energy and its second is the variance,

        U = -d ln Z / d beta,        Var(E) = d^2 ln Z / d beta^2 = k_B T^2 C,

    and F = -k_B T ln Z, S = (U - F) / T follow. `thermo_from_z` does exactly this, with
    nothing but a function returning ln Z: it never sees a level, a probability or a closed
    form. Every closed form in this module exists so that reconstruction can be checked.

LOGARITHMS, ALWAYS
    Every partition function here is returned as ln Z. Z_N of ten thousand spins is about
    2^10000, which overflows a float long before the physics becomes interesting; ln Z is a
    modest number and is all any thermodynamic quantity needs.

THE CONSTANT
    hbar is defined here from `fundamental.PLANCK_H` rather than added to `constants`, which
    this course consumes and does not extend. Modules 16 and 17 need it too; promote it if they
    agree.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

import numpy as np

from .constants import K_B
from .equilibrium import einstein_log_multiplicity
from .fundamental import PLANCK_H
from .multiplicity import log_multiplicity_array

#: Reduced Planck constant [J s] (SI 2019 exact h, divided by 2 pi).
H_BAR: Final[float] = PLANCK_H / (2.0 * math.pi)

#: Machine epsilon for float64, the roundoff floor every finite difference fights.
_EPS: Final[float] = float(np.finfo(float).eps)

#: Default relative steps in beta. A central first difference balances truncation (~h^2)
#: against roundoff (~eps/h) at h ~ eps^(1/3); a central second difference, whose roundoff
#: grows as eps/h^2, balances at h ~ eps^(1/4).
FIRST_DERIVATIVE_REL_STEP: Final[float] = _EPS ** (1.0 / 3.0)
SECOND_DERIVATIVE_REL_STEP: Final[float] = _EPS ** (1.0 / 4.0)


def _beta(temperature) -> np.ndarray:
    t = np.asarray(temperature, dtype=float)
    if np.any(t <= 0):
        raise ValueError("temperature must be positive")
    return 1.0 / (K_B * t)


def _log_one_minus_exp(x: np.ndarray) -> np.ndarray:
    """ln(1 - e^-x) for x > 0, accurate at both small and large x."""
    return np.log(-np.expm1(-x))


def _log_two_cosh(x: np.ndarray) -> np.ndarray:
    """ln(2 cosh x) without overflow: |x| + ln(1 + e^(-2|x|))."""
    a = np.abs(x)
    return a + np.log1p(np.exp(-2.0 * a))


def _as_float_or_array(value: np.ndarray):
    return float(value) if np.ndim(value) == 0 else value


# ---------------------------------------------------------------------------
# The two-level system (module 11's, now with its thermodynamics)
# ---------------------------------------------------------------------------


def log_z_two_level(gap: float, temperature):
    """ln z = ln(1 + exp(-Delta / (k_B T))), ground state at zero energy. Dimensionless."""
    if gap <= 0:
        raise ValueError("gap must be positive")
    return _as_float_or_array(np.logaddexp(0.0, -gap * _beta(temperature)))


def two_level_energy(gap: float, temperature):
    """U = Delta / (exp(Delta / (k_B T)) + 1) [J] -- module 11's <E>, in closed form."""
    x = gap * _beta(temperature)
    return _as_float_or_array(gap * np.exp(-np.logaddexp(0.0, x)))


def two_level_heat_capacity(gap: float, temperature):
    """C = k_B x^2 e^x / (e^x + 1)^2, x = Delta / (k_B T) [J/K] -- the Schottky peak.

    Written as k_B (x / (2 cosh(x/2)))^2, which neither overflows when cold nor loses
    precision when hot. It peaks near k_B T = 0.42 Delta and dies at both ends: cold, nothing
    is excited; hot, nothing more can be.
    """
    x = gap * _beta(temperature)
    return _as_float_or_array(K_B * (x / (2.0 * np.cosh(0.5 * x))) ** 2)


# ---------------------------------------------------------------------------
# The ideal paramagnet: N independent moments in a field
# ---------------------------------------------------------------------------


def _paramagnet_x(moment: float, field: float, temperature) -> np.ndarray:
    if moment <= 0:
        raise ValueError("moment must be positive")
    if field < 0:
        raise ValueError("field must be non-negative; point the axis along B")
    return moment * field * _beta(temperature)


def log_z_paramagnet(n_spins: int, moment: float, field: float, temperature):
    """ln Z_N = N ln(2 cosh(mu B / (k_B T))). Dimensionless.

    Each moment has levels -mu B and +mu B, so z = e^x + e^-x = 2 cosh x; the moments are
    independent, so Z_N = z^N and ln Z_N = N ln z. The sum over all 2^N microstates is never
    taken -- factorization makes it one line.
    """
    if n_spins < 1:
        raise ValueError("n_spins must be at least one")
    x = _paramagnet_x(moment, field, temperature)
    return _as_float_or_array(n_spins * _log_two_cosh(x))


def paramagnet_energy(n_spins: int, moment: float, field: float, temperature):
    """U = -N mu B tanh(mu B / (k_B T)) = -M B [J]."""
    x = _paramagnet_x(moment, field, temperature)
    return _as_float_or_array(-n_spins * moment * field * np.tanh(x))


def paramagnet_magnetization(n_spins: int, moment: float, field: float, temperature):
    """M = N mu tanh(mu B / (k_B T)) [J/T] -- the total moment along the field.

    Curie regime (mu B << k_B T): M ~ N mu^2 B / (k_B T), proportional to B / T.
    Saturation (mu B >> k_B T): M -> N mu, every moment aligned.
    """
    x = _paramagnet_x(moment, field, temperature)
    return _as_float_or_array(n_spins * moment * np.tanh(x))


def curie_magnetization(n_spins: int, moment: float, field: float, temperature):
    """The Curie-law approximation M = N mu^2 B / (k_B T) [J/T]; valid for mu B << k_B T."""
    x = _paramagnet_x(moment, field, temperature)
    return _as_float_or_array(n_spins * moment * x)


def paramagnet_heat_capacity(n_spins: int, moment: float, field: float, temperature):
    """C_B = N k_B x^2 / cosh^2 x, x = mu B / (k_B T) [J/K] -- a Schottky peak per spin."""
    x = _paramagnet_x(moment, field, temperature)
    return _as_float_or_array(n_spins * K_B * (x / np.cosh(np.minimum(np.abs(x), 350.0))) ** 2)


def paramagnet_entropy(n_spins: int, moment: float, field: float, temperature):
    """S = N k_B [ln(2 cosh x) - x tanh x] [J/K]; N k_B ln 2 hot, zero cold."""
    x = _paramagnet_x(moment, field, temperature)
    return _as_float_or_array(n_spins * K_B * (_log_two_cosh(x) - x * np.tanh(x)))


# ---------------------------------------------------------------------------
# The harmonic oscillator
# ---------------------------------------------------------------------------


def harmonic_cutoff(hbar_omega: float, temperature: float) -> int:
    """The level n_max past which a truncated oscillator sum may stop.

    ceil(30 k_B T / (hbar omega)): the first omitted Boltzmann factor is below e^-30 of the
    ground state's, about 1e-13, and the tail is a geometric series no larger than that
    divided by (1 - e^(-hbar omega / k_B T)). Capped at 10^4 levels.
    """
    if hbar_omega <= 0:
        raise ValueError("hbar_omega must be positive")
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    return int(min(10_000, math.ceil(30.0 * K_B * temperature / hbar_omega)))


def log_z_harmonic(hbar_omega: float, temperature, n_max: int | None = None,
                   zero_point: bool = True):
    """ln z of one oscillator with levels hbar omega (n + 1/2). Dimensionless.

    With `n_max` None, the closed form of the geometric series,

        z = e^(-x/2) / (1 - e^-x),    x = hbar omega / (k_B T).

    With an integer `n_max`, the explicit sum over n = 0..n_max -- the same series cut off,
    which is how the closed form is checked. `zero_point=False` drops the 1/2, measuring
    energies from the ground state as module 01 does; that shifts U and F by hbar omega / 2
    and leaves S and C untouched.
    """
    if hbar_omega <= 0:
        raise ValueError("hbar_omega must be positive")
    x = hbar_omega * _beta(temperature)
    offset = -0.5 * x if zero_point else 0.0
    if n_max is None:
        return _as_float_or_array(offset - _log_one_minus_exp(x))
    if n_max < 0 or int(n_max) != n_max:
        raise ValueError("n_max must be a non-negative whole number")
    n = np.arange(int(n_max) + 1, dtype=float)
    x_col = np.atleast_1d(x)[:, None]
    exponents = -x_col * n[None, :]
    shift = exponents.max(axis=1, keepdims=True)
    log_sum = shift[:, 0] + np.log(np.exp(exponents - shift).sum(axis=1))
    result = np.atleast_1d(offset) + log_sum
    return _as_float_or_array(result.reshape(np.shape(x)))


def harmonic_energy(hbar_omega: float, temperature, zero_point: bool = True):
    """U = hbar omega (1/2 + 1 / (e^x - 1)) [J]; without the zero point, the Planck term only.

    High T, with the zero point: U = k_B T + (hbar omega)^2 / (12 k_B T) + ... -> k_B T, the
    equipartition value (the zero point's +hbar omega/2 cancels the Planck term's -hbar omega/2).
    Low T: U -> hbar omega / 2, or 0 without the zero point.
    """
    x = hbar_omega * _beta(temperature)
    planck = hbar_omega / np.expm1(x)
    return _as_float_or_array(planck + (0.5 * hbar_omega if zero_point else 0.0))


def harmonic_heat_capacity(hbar_omega: float, temperature):
    """C = k_B (x / (2 sinh(x/2)))^2, x = hbar omega / (k_B T) [J/K] -- the Einstein function.

    High T: C -> k_B, equipartition. Low T: C ~ k_B x^2 e^-x -- exponentially frozen out.
    """
    x = hbar_omega * _beta(temperature)
    half = np.minimum(0.5 * x, 350.0)
    return _as_float_or_array(K_B * (x / (2.0 * np.sinh(half))) ** 2)


def harmonic_entropy(hbar_omega: float, temperature):
    """S = k_B [x / (e^x - 1) - ln(1 - e^-x)] [J/K]; independent of the zero point."""
    x = hbar_omega * _beta(temperature)
    return _as_float_or_array(K_B * (x / np.expm1(x) - _log_one_minus_exp(x)))


def harmonic_temperature(energy_per_oscillator, hbar_omega: float):
    """Invert U(T) without the zero point: T = hbar omega / (k_B ln(1 + hbar omega / U)) [K].

    The temperature the oscillator partition function assigns to an oscillator holding a mean
    energy U above its ground state. For U >> hbar omega it is U / k_B + hbar omega / (2 k_B):
    module 01's equipartition reading, T = U / k_B, plus half a quantum. Module 09 reached the
    same curve from the slope of S(U); `fundamental.einstein_solid_temperature` is that route.
    """
    u = np.asarray(energy_per_oscillator, dtype=float)
    if np.any(u <= 0):
        raise ValueError("an oscillator at its ground state has T = 0; energy must be > 0")
    if hbar_omega <= 0:
        raise ValueError("hbar_omega must be positive")
    return _as_float_or_array(hbar_omega / (K_B * np.log1p(hbar_omega / u)))


# ---------------------------------------------------------------------------
# Advanced: the semiclassical ideal gas
# ---------------------------------------------------------------------------


def thermal_wavelength(temperature, mass: float):
    """lambda = h / sqrt(2 pi m k_B T) [m]."""
    if mass <= 0:
        raise ValueError("mass must be positive")
    t = np.asarray(temperature, dtype=float)
    if np.any(t <= 0):
        raise ValueError("temperature must be positive")
    return _as_float_or_array(PLANCK_H / np.sqrt(2.0 * np.pi * mass * K_B * t))


def log_z_ideal_gas(n_particles: int, volume: float, temperature, mass: float,
                    gibbs_correction: bool = True):
    """ln Z_N = N ln(V / lambda^3) - ln N! for a monatomic ideal gas. Dimensionless.

    Each particle's z = V / lambda^3 counts its translational states in cells of size h^3 --
    stated, not derived: the counting of states in a box is module 17's. `gibbs_correction`
    divides by N! (computed exactly, by lgamma) because permuting identical particles does not
    make a new microstate. Without it, S fails to be extensive; with it, S is Sackur-Tetrode.
    """
    if n_particles < 1:
        raise ValueError("n_particles must be at least one")
    if volume <= 0:
        raise ValueError("volume must be positive")
    lam = np.asarray(thermal_wavelength(temperature, mass))
    value = n_particles * np.log(volume / lam**3)
    if gibbs_correction:
        value = value - math.lgamma(n_particles + 1.0)
    return _as_float_or_array(value)


# ---------------------------------------------------------------------------
# Reconstruction: U, S, F and C from ln Z alone
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ThermoFromZ:
    """Thermodynamics reconstructed from ln Z(T) by differentiating in beta.

    All arrays share the shape of `temperature`. Units: `log_z` dimensionless; `energy`,
    `free_energy` in J; `energy_variance` in J^2; `entropy`, `heat_capacity` in J/K.
    """

    temperature: np.ndarray
    log_z: np.ndarray
    energy: np.ndarray
    energy_variance: np.ndarray
    heat_capacity: np.ndarray
    free_energy: np.ndarray
    entropy: np.ndarray

    @property
    def ts(self) -> np.ndarray:
        """T S [J], so that U - TS can be compared with F term by term."""
        return self.temperature * self.entropy


def thermo_from_z(log_z: Callable[[np.ndarray], np.ndarray | float], temperature,
                  rel_step: float | None = None) -> ThermoFromZ:
    """Reconstruct U, Var(E), C, F and S from a function returning ln Z at given temperatures.

        U      = -d ln Z / d beta                    (central first difference)
        Var(E) =  d^2 ln Z / d beta^2               (central second difference)
        C      =  Var(E) / (k_B T^2)
        F      = -k_B T ln Z
        S      = (U - F) / T = k_B (ln Z + beta U)

    Differences are taken in beta, with a step proportional to each point's own beta, and
    `log_z` is called at beta +- h directly -- so there is no grid, and no endpoint needs a
    one-sided formula. Both stencils are second order: halve the step and the truncation error
    quarters. By default each uses its own roundoff-optimal step (`FIRST_DERIVATIVE_REL_STEP`,
    `SECOND_DERIVATIVE_REL_STEP`); pass `rel_step` to force one step on both, which is how the
    order is measured.

    `log_z` sees temperatures only; it may be any of this module's log_z functions with the
    other arguments fixed, or anything else that returns ln Z.

    Where the step is not the limit, roundoff is. The second difference subtracts three values
    of ln Z that agree to more and more digits as C becomes exponentially small -- far below
    the level spacing, and for a system with a top level, far above it -- so C degrades there
    while U, a first difference, does not. Across a tenth to ten times the gap U and S hold to
    about 1e-9; C holds to about 1e-5 from a fifth to five times the gap, and to nothing in
    particular at a tenth. Where C itself is what you need in a tail, sum over the levels
    (`level_sums`) instead.
    """
    t = np.asarray(temperature, dtype=float)
    beta = _beta(t)
    h1 = beta * (FIRST_DERIVATIVE_REL_STEP if rel_step is None else rel_step)
    h2 = beta * (SECOND_DERIVATIVE_REL_STEP if rel_step is None else rel_step)
    if np.any(h1 >= beta) or np.any(h2 >= beta):
        raise ValueError("rel_step must be below 1, or beta - h leaves the physical range")

    def at(b: np.ndarray) -> np.ndarray:
        return np.asarray(log_z(1.0 / (K_B * b)), dtype=float)

    centre = at(beta)
    energy = -(at(beta + h1) - at(beta - h1)) / (2.0 * h1)
    variance = (at(beta + h2) - 2.0 * centre + at(beta - h2)) / h2**2
    heat_capacity = variance / (K_B * t**2)
    free_energy = -K_B * t * centre
    entropy = K_B * (centre + beta * energy)
    return ThermoFromZ(temperature=t, log_z=centre, energy=energy, energy_variance=variance,
                       heat_capacity=heat_capacity, free_energy=free_energy, entropy=entropy)


@dataclass(frozen=True)
class LevelSums:
    """Canonical averages computed the long way: probabilities first, then sums over levels.

    `entropy` is the Gibbs form -k_B sum P ln P, computed from the probabilities without any
    reference to F; `free_energy_direct` is then U - T S. Comparing it with -k_B T ln Z is the
    check that F = -k_B T ln Z is the free energy of module 10, not a new definition.
    """

    temperature: float
    probabilities: np.ndarray
    log_z: float
    energy: float
    energy_variance: float
    entropy: float

    @property
    def free_energy_direct(self) -> float:
        """U - T S [J], with S the Gibbs entropy."""
        return self.energy - self.temperature * self.entropy

    @property
    def free_energy_from_z(self) -> float:
        """-k_B T ln Z [J]."""
        return -K_B * self.temperature * self.log_z


def level_sums(energies, temperature: float, degeneracy=None) -> LevelSums:
    """Sum over an explicit list of levels at one temperature: Z, U, Var(E), Gibbs S.

    Degenerate levels may be given once with their `degeneracy` g (then each of the g
    microstates carries probability P_level / g, which is what the Gibbs sum needs).
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    e = np.asarray(energies, dtype=float)
    g = np.ones_like(e) if degeneracy is None else np.asarray(degeneracy, dtype=float)
    if e.ndim != 1 or e.size == 0 or g.shape != e.shape:
        raise ValueError("energies must be a non-empty list, with one degeneracy per level")
    if np.any(g <= 0):
        raise ValueError("degeneracies must be positive")
    beta = 1.0 / (K_B * temperature)
    log_w = np.log(g) - beta * e
    shift = float(log_w.max())
    log_z = shift + float(np.log(np.exp(log_w - shift).sum()))
    p = np.exp(log_w - log_z)
    mean = float(np.sum(p * e))
    variance = float(np.sum(p * (e - mean) ** 2))
    per_state = p / g
    occupied = p > 0
    entropy = float(-K_B * np.sum(p[occupied] * np.log(per_state[occupied])))
    return LevelSums(temperature=float(temperature), probabilities=p, log_z=log_z,
                     energy=mean, energy_variance=variance, entropy=entropy)


# ---------------------------------------------------------------------------
# The paramagnet at fixed energy: S(U), and temperatures below zero
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SpinEntropy:
    """The exact S(U) of N moments in a field, one entry per macrostate.

    `n_flipped` counts anti-aligned moments (0..N); each costs 2 mu B, so
    U = mu B (2 n_flipped - N). S = k_B ln C(N, n_flipped), by module 08's counting.
    """

    n_spins: int
    moment: float
    field: float
    n_flipped: np.ndarray
    energy: np.ndarray
    entropy: np.ndarray

    @property
    def step(self) -> float:
        """The energy of one flip, 2 mu B [J]."""
        return 2.0 * self.moment * self.field

    def beta(self) -> np.ndarray:
        """beta = (1/k_B) dS/dU at each interior macrostate [1/J], by central difference.

        Positive below U = 0, zero at the peak, negative above it. The endpoints have no
        neighbour on one side and are returned as NaN.
        """
        ln_omega = self.entropy / K_B
        out = np.full(ln_omega.shape, np.nan)
        out[1:-1] = (ln_omega[2:] - ln_omega[:-2]) / (2.0 * self.step)
        return out

    def beta_stirling(self) -> np.ndarray:
        """The same slope from Stirling's form: beta = ln((N - n) / n) / (2 mu B) [1/J].

        n = n_flipped. It is the canonical relation n / (N - n) = exp(-2 beta mu B) solved for
        beta, and it is infinite at the fully aligned and fully flipped ends.
        """
        n = self.n_flipped.astype(float)
        with np.errstate(divide="ignore"):
            return np.log((self.n_spins - n) / n) / self.step


def spin_entropy_of_energy(n_spins: int, moment: float, field: float) -> SpinEntropy:
    """S(U) of an ideal paramagnet across its whole energy band, exactly.

    The band runs from -N mu B (all aligned) to +N mu B (all anti-aligned). Its entropy is a
    dome: zero at both ends, N k_B ln 2 at U = 0. Past the peak adding energy lowers S, so
    1/T = dS/dU is negative there. The system is bounded above in energy, which is what makes
    that possible -- an oscillator or a gas has no top level and no such branch.
    """
    if n_spins < 1:
        raise ValueError("n_spins must be at least one")
    if moment <= 0 or field <= 0:
        raise ValueError("moment and field must be positive")
    n = np.arange(n_spins + 1)
    return SpinEntropy(n_spins=int(n_spins), moment=float(moment), field=float(field),
                       n_flipped=n,
                       energy=moment * field * (2.0 * n - n_spins),
                       entropy=K_B * log_multiplicity_array(n_spins, n))


@dataclass(frozen=True)
class SpinSolidContact:
    """A paramagnet and an Einstein solid sharing energy, counted exactly.

    The solid's quantum is one spin flip, 2 mu B, so energy passes one flip at a time. The
    composite is isolated with `total_quanta` fixed; entry k of each array is the macrostate
    with k flipped spins and (total - k) quanta in the solid, and `log_omega_total` is
    ln[C(N, k) Omega_solid(total - k)].
    """

    n_spins: int
    n_oscillators: int
    initial_flipped: int
    total_quanta: int
    n_flipped: np.ndarray
    log_omega_total: np.ndarray

    @property
    def most_probable_flipped(self) -> int:
        """The flip count with the most joint microstates -- where the pair settles."""
        return int(self.n_flipped[np.argmax(self.log_omega_total)])

    @property
    def energy_to_solid(self) -> int:
        """Quanta the spins hand to the solid between start and the most probable state.

        Positive means heat left the spins.
        """
        return self.initial_flipped - self.most_probable_flipped

    def log_omega_change(self, flips: int = -1) -> float:
        """Change in ln Omega_total if the spins' flip count changes by `flips` from the start.

        -1 is one flip undone: a quantum from spins to solid. +1 is the reverse.
        """
        index = self.initial_flipped - int(self.n_flipped[0])
        target = index + flips
        if not 0 <= target < self.n_flipped.size:
            raise ValueError("that transfer is not available to the pair")
        return float(self.log_omega_total[target] - self.log_omega_total[index])


def spin_solid_contact(n_spins: int, n_flipped: int, n_oscillators: int,
                       solid_quanta: int) -> SpinSolidContact:
    """Put N spins with `n_flipped` anti-aligned against an Einstein solid, and count.

    The solid holds `solid_quanta` quanta of one flip each, so it is at a positive
    temperature for any amount of energy -- its ln Omega rises with every quantum. The
    function enumerates every split of the fixed total. Start the spins inverted
    (n_flipped > N/2, negative temperature) and the most probable split has *fewer* flipped
    spins than the start: energy leaves the spins, however hot the solid is.
    """
    if n_spins < 1 or n_oscillators < 1:
        raise ValueError("both bodies need at least one member")
    if not 0 <= n_flipped <= n_spins:
        raise ValueError("n_flipped must lie between 0 and n_spins")
    if solid_quanta < 0:
        raise ValueError("solid_quanta must be non-negative")
    total = int(n_flipped) + int(solid_quanta)
    k = np.arange(0, min(n_spins, total) + 1)
    log_total = (log_multiplicity_array(n_spins, k)
                 + einstein_log_multiplicity(total - k, n_oscillators))
    return SpinSolidContact(n_spins=int(n_spins), n_oscillators=int(n_oscillators),
                            initial_flipped=int(n_flipped), total_quanta=total, n_flipped=k,
                            log_omega_total=np.asarray(log_total, dtype=float))
