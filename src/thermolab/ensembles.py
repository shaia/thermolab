"""A small system on a finite heat bath: where the Boltzmann factor comes from.

MODEL SPECIFICATION
    System:        a small system with a handful of energy levels -- a two-level system with
                   a gap of a whole number of quanta, or an Einstein solid of a few
                   oscillators, whose level k (k quanta) has degeneracy C(k + n - 1, k) --
                   sharing q_tot energy quanta with an Einstein-solid bath of N_bath oscillators
    Dynamics:      none -- every accessible joint microstate of system plus bath is enumerated
                   and weighted equally; there is no time evolution and no sampling, so no
                   random numbers appear anywhere in this module
    Boundary:      the composite is isolated, q_tot exactly fixed; the internal wall is rigid
                   and passes quanta only, so no work is done across it (dW_on = 0)
    Ensemble:      exactly microcanonical for the composite; the system's marginal is the
                   object that converges to the canonical (Boltzmann) form as N_bath grows
    Ignored:       the energy of the wall's coupling, unequal quantum sizes, any spatial
                   structure, and how fast quanta are actually exchanged
    Valid when:    system and bath share one quantum size and the composite is genuinely
                   isolated -- then the enumeration is exact at every size; the canonical form
                   additionally needs E_s << U_bath and a negligible bath curvature
    Failure modes: reading a "temperature" off a bath so small that ln Omega has no smooth
                   slope (a one-oscillator bath has Omega = 1 at every energy: beta = 0); and
                   E_s comparable to U_tot, where the marginal visibly departs from the
                   exponential -- the module measures this departure rather than hiding it

THE ARGUMENT, AS ARITHMETIC
    Module 08 postulated that every accessible microstate of an isolated system is equally
    probable. Apply that to system plus bath. A system microstate s holding k_s quanta leaves
    q_tot - k_s for the bath, which can hold them in Omega_bath(q_tot - k_s) ways, so

        P(s) = Omega_bath(q_tot - k_s) / sum_s' Omega_bath(q_tot - k_s')

    exactly, for a bath of any size (`enumerate_joint`, `marginal_occupation`). Expanding
    ln Omega_bath about q_tot gives -beta E_s, with beta = d ln Omega_bath / dU the bath's
    slope from module 09, plus a curvature term E_s^2 / 2 * d^2 ln Omega_bath / dU^2 =
    -E_s^2 / (2 k_B T^2 C_bath) that vanishes as 1/N_bath. Dropping it is the Boltzmann
    distribution (`boltzmann_distribution`); keeping it is the error bar on "an infinite bath"
    (`measured_log_correction`, `predicted_log_correction`).

THE BATH'S SLOPE, EXACTLY, WITHOUT SCIPY
    ln Omega_bath(N, q) = ln Gamma(q + N) - ln Gamma(q + 1) - ln Gamma(N). Its derivative in q
    is a difference of digamma functions, psi(q + N) - psi(q + 1), and because N is a whole
    number that difference telescopes into a finite sum:

        d ln Omega / dq = sum_{j=1}^{N-1} 1 / (q + j),
        d^2 ln Omega / dq^2 = -sum_{j=1}^{N-1} 1 / (q + j)^2.

    That is exact, needs nothing but NumPy, and is what `bath_beta_exact` and
    `bath_curvature_exact` evaluate. For N = 1 the sum is empty: a single oscillator holds its
    quanta in exactly one way whatever their number, and has no temperature to give.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np

from .constants import K_B
from .equilibrium import einstein_log_multiplicity
from .fundamental import einstein_solid_temperature

# ---------------------------------------------------------------------------
# The small system's levels
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Levels:
    """Energy levels of a small system, in whole numbers of the shared quantum.

    Level i has energy `quanta[i] * quantum` [J] and holds exp(`log_degeneracy[i]`)
    microstates. Degeneracies are stored as logarithms because an Einstein solid's grow like
    factorials. Energies must be whole numbers of quanta: the bath trades quanta only, so a
    level between two multiples could never be reached.
    """

    quanta: np.ndarray
    log_degeneracy: np.ndarray
    quantum: float

    def __post_init__(self) -> None:
        quanta = np.asarray(self.quanta)
        if quanta.ndim != 1 or quanta.size == 0:
            raise ValueError("levels need a non-empty one-dimensional list of energies")
        if not np.array_equal(quanta, np.round(quanta)) or np.any(quanta < 0):
            raise ValueError("level energies must be non-negative whole numbers of quanta")
        if np.asarray(self.log_degeneracy).shape != quanta.shape:
            raise ValueError("every level needs exactly one degeneracy")
        if self.quantum <= 0:
            raise ValueError("quantum must be positive")
        object.__setattr__(self, "quanta", quanta.astype(np.int64))
        object.__setattr__(self, "log_degeneracy",
                           np.asarray(self.log_degeneracy, dtype=float))

    def __len__(self) -> int:
        return int(self.quanta.size)

    @property
    def energies(self) -> np.ndarray:
        """E_s = k_s x quantum [J]."""
        return self.quanta * self.quantum

    @property
    def degeneracy(self) -> np.ndarray:
        """g_s, the number of microstates in each level (as floats)."""
        return np.exp(self.log_degeneracy)


def two_level(gap_quanta: int, quantum: float) -> Levels:
    """A ground state at zero energy and one excited state `gap_quanta` quanta above it."""
    if gap_quanta < 1 or int(gap_quanta) != gap_quanta:
        raise ValueError("the gap must be a positive whole number of quanta")
    return Levels(quanta=np.array([0, int(gap_quanta)]), log_degeneracy=np.zeros(2),
                  quantum=quantum)


def einstein_levels(n_oscillators: int, max_quanta: int, quantum: float) -> Levels:
    """Levels k = 0..max_quanta of an Einstein solid of `n_oscillators` oscillators.

    Level k is every way of spreading k quanta over the oscillators, C(k + n - 1, k) of them
    (module 01's stars and bars). The list is truncated at `max_quanta`; choose it well past
    where the Boltzmann weight has died away, since nothing above it is counted.
    """
    if n_oscillators < 1:
        raise ValueError("a solid needs at least one oscillator")
    if max_quanta < 0:
        raise ValueError("max_quanta must be non-negative")
    k = np.arange(max_quanta + 1)
    return Levels(quanta=k, log_degeneracy=einstein_log_multiplicity(k, n_oscillators),
                  quantum=quantum)


# ---------------------------------------------------------------------------
# Exact enumeration of system plus bath
# ---------------------------------------------------------------------------


def _log_sum_exp(values: np.ndarray) -> float:
    """ln sum exp(values), shifted by the largest finite entry so nothing overflows."""
    finite = np.isfinite(values)
    if not finite.any():
        return -np.inf
    shift = float(values[finite].max())
    return shift + float(np.log(np.exp(values[finite] - shift).sum()))


def bath_log_multiplicity(n_bath: int, quanta) -> np.ndarray:
    """ln Omega_bath(N, q) = ln C(q + N - 1, q), elementwise; -inf where q < 0.

    A negative q is not an error here: it is a system level the bath cannot pay for, and
    -inf is the log of the zero ways it has of doing so.
    """
    q = np.asarray(quanta, dtype=float)
    reachable = q >= 0
    out = np.full(q.shape, -np.inf)
    out[reachable] = einstein_log_multiplicity(q[reachable], n_bath)
    return out


@dataclass(frozen=True)
class JointEnumeration:
    """Every joint microstate of system plus bath, counted level by level.

    For each system level s: the quanta the bath is left with, ln Omega_bath of that, and
    ln of the number of joint microstates with the system in level s,
    ln g_s + ln Omega_bath(q_tot - k_s). Every one of those joint microstates has the same
    probability, 1 / Omega_total -- that is the postulate, and it is the flat panel of the
    module's centrepiece.
    """

    levels: Levels
    n_bath: int
    total_quanta: int
    bath_quanta: np.ndarray
    log_bath_multiplicity: np.ndarray
    log_joint_count: np.ndarray

    @property
    def accessible(self) -> np.ndarray:
        """Levels the bath can pay for (k_s <= q_tot)."""
        return self.bath_quanta >= 0

    @property
    def log_total_multiplicity(self) -> float:
        """ln Omega_total, the number of joint microstates of the isolated composite."""
        return _log_sum_exp(self.log_joint_count)

    @property
    def joint_microstate_probability(self) -> float:
        """The probability of any single joint microstate: the same number for all of them."""
        return float(np.exp(-self.log_total_multiplicity))


def enumerate_joint(levels: Levels, n_bath: int, total_quanta: int) -> JointEnumeration:
    """Count the joint microstates of `levels` sharing `total_quanta` with an Einstein bath."""
    if n_bath < 1:
        raise ValueError("the bath needs at least one oscillator")
    if total_quanta < 0 or int(total_quanta) != total_quanta:
        raise ValueError("total_quanta must be a non-negative whole number")
    bath_quanta = int(total_quanta) - levels.quanta
    log_bath = bath_log_multiplicity(n_bath, bath_quanta)
    return JointEnumeration(levels=levels, n_bath=int(n_bath), total_quanta=int(total_quanta),
                            bath_quanta=bath_quanta, log_bath_multiplicity=log_bath,
                            log_joint_count=levels.log_degeneracy + log_bath)


def marginal_occupation(joint: JointEnumeration) -> np.ndarray:
    """P(level s) = g_s Omega_bath(q_tot - k_s) / Omega_total: the system's own distribution.

    Summing the flat joint distribution over the bath's microstates. Exact at every bath
    size; computed in logarithms and shifted before exponentiating, so no setting overflows.
    """
    return np.exp(joint.log_joint_count - joint.log_total_multiplicity)


def explicit_joint_microstates(levels: Levels, n_bath: int, total_quanta: int,
                               limit: int = 100_000) -> list[tuple[int, int, tuple[int, ...]]]:
    """List every joint microstate one by one, for hand-checkable sizes only.

    Each entry is (level index, which of that level's g_s microstates, the bath's
    occupation numbers oscillator by oscillator). This is the enumeration a student does with
    a pencil; `enumerate_joint` is the same count done by formula, and the laboratory checks
    that they agree. Refuses when the list would exceed `limit` entries.
    """
    joint = enumerate_joint(levels, n_bath, total_quanta)
    if joint.log_total_multiplicity > math.log(limit):
        raise ValueError(f"more than {limit} joint microstates; use enumerate_joint instead")
    states: list[tuple[int, int, tuple[int, ...]]] = []
    for index, q_bath in enumerate(joint.bath_quanta):
        if q_bath < 0:
            continue
        g = int(round(levels.degeneracy[index]))
        for occupation in _compositions(int(q_bath), n_bath):
            states.extend((index, sub, occupation) for sub in range(g))
    return states


def _compositions(total: int, parts: int):
    """Every tuple of `parts` non-negative integers summing to `total` (stars and bars)."""
    for bars in itertools.combinations(range(total + parts - 1), parts - 1):
        edges = (-1, *bars, total + parts - 1)
        yield tuple(b - a - 1 for a, b in itertools.pairwise(edges))


# ---------------------------------------------------------------------------
# The canonical limit
# ---------------------------------------------------------------------------


def bath_temperature(quanta_per_oscillator: float, quantum: float) -> float:
    """T of an infinitely large Einstein bath holding `quanta_per_oscillator` quanta each [K].

    Module 09's T = quantum / (k_B ln(1 + n quantum / U)), per oscillator. This is the
    temperature a finite bath at the same energy density approaches as it grows, and the one
    every finite-bath marginal is compared against.
    """
    if quanta_per_oscillator <= 0:
        raise ValueError("an empty bath has no temperature; quanta_per_oscillator must be > 0")
    return float(einstein_solid_temperature(quanta_per_oscillator * quantum, 1.0, quantum))


def boltzmann_distribution(levels: Levels, temperature: float) -> np.ndarray:
    """P_s = g_s exp(-E_s / (k_B T)) / Z over the levels, Z = sum_s g_s exp(-E_s / (k_B T)).

    Z appears here only as the constant that makes the probabilities sum to one. What else it
    can do is module 12's business. Shifted in log space, so a large E_s / k_B T underflows
    to zero instead of overflowing.
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    log_weights = levels.log_degeneracy - levels.energies / (K_B * temperature)
    return np.exp(log_weights - _log_sum_exp(log_weights))


def sup_norm(p: np.ndarray, q: np.ndarray) -> float:
    """max_s |p_s - q_s|: the largest disagreement between two distributions on one set."""
    return float(np.max(np.abs(np.asarray(p, dtype=float) - np.asarray(q, dtype=float))))


@dataclass(frozen=True)
class BathSweep:
    """Marginals of one system on baths of growing size at a fixed energy density."""

    levels: Levels
    n_bath: np.ndarray
    total_quanta: np.ndarray
    quanta_per_oscillator: float
    marginals: np.ndarray
    temperature: float
    reference: np.ndarray
    distances: np.ndarray


def bath_size_sweep(levels: Levels, n_bath_values, quanta_per_oscillator: float) -> BathSweep:
    """The system's marginal on baths of each size, all at the same energy per oscillator.

    Fixed energy per oscillator is fixed temperature: each bath gets
    q_tot = round(quanta_per_oscillator x N_bath) quanta, and every marginal is compared with
    the Boltzmann distribution at `bath_temperature` -- the infinite bath's. `distances` is the
    sup-norm gap for each size; it falls as 1/N_bath (module 11's numerical observation).
    Rounding q_tot to a whole number shifts the energy density by up to 1/(2 N_bath), which
    is the same order as the effect being measured; choose sizes that make it exact when the
    exponent matters.
    """
    n_values = np.asarray(list(n_bath_values), dtype=np.int64)
    temperature = bath_temperature(quanta_per_oscillator, levels.quantum)
    reference = boltzmann_distribution(levels, temperature)
    totals = np.rint(quanta_per_oscillator * n_values).astype(np.int64)
    marginals = np.array([marginal_occupation(enumerate_joint(levels, int(n), int(q)))
                          for n, q in zip(n_values, totals, strict=True)])
    distances = np.array([sup_norm(m, reference) for m in marginals])
    return BathSweep(levels=levels, n_bath=n_values, total_quanta=totals,
                     quanta_per_oscillator=float(quanta_per_oscillator), marginals=marginals,
                     temperature=temperature, reference=reference, distances=distances)


# ---------------------------------------------------------------------------
# The bath's slope and curvature: beta, and the price of a finite bath
# ---------------------------------------------------------------------------


def _harmonic_terms(n_bath: int, quanta: float, power: int) -> float:
    if n_bath < 1:
        raise ValueError("the bath needs at least one oscillator")
    if quanta < 0:
        raise ValueError("quanta must be non-negative")
    j = np.arange(1, n_bath, dtype=float)
    return float(np.sum(1.0 / (quanta + j) ** power))


def bath_beta_exact(n_bath: int, quanta: float, quantum: float) -> float:
    """beta = d ln Omega_bath / dU at `quanta`, exactly: sum_{j=1}^{N-1} 1/(q + j) / quantum.

    In 1/J. This is module 09's 1/(k_B T) = (dS/dU) / k_B, evaluated on the bath's exact
    count rather than its Stirling form -- see the module docstring for the telescoping sum.
    """
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    return _harmonic_terms(n_bath, quanta, 1) / quantum


def bath_curvature_exact(n_bath: int, quanta: float, quantum: float) -> float:
    """d^2 ln Omega_bath / dU^2 at `quanta`, exactly [1/J^2]. Always negative (concave).

    Thermodynamically it is d(beta)/dU = -1 / (k_B T^2 C_bath): the bigger the bath's heat
    capacity, the flatter its beta, and the better the Boltzmann factor.
    """
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    return -_harmonic_terms(n_bath, quanta, 2) / quantum**2


def beta_of_bath(n_bath: int, quanta: int, quantum: float) -> float:
    """beta read off the bath by a central difference of its exact ln Omega [1/J].

        beta ~ [ln Omega(N, q + 1) - ln Omega(N, q - 1)] / (2 quantum)

    The measurement a student would make: count, step one quantum either way, divide. The
    step cannot be refined -- quanta are whole -- so its error, relative to the exact slope,
    falls instead as the bath grows: second order in 1/N_bath at fixed energy density.
    """
    if quanta < 1:
        raise ValueError("a central difference needs at least one quantum to remove")
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    up, down = bath_log_multiplicity(n_bath, np.array([quanta + 1, quanta - 1]))
    return float((up - down) / (2.0 * quantum))


def measured_log_correction(joint: JointEnumeration) -> np.ndarray:
    """What the exact count adds to -beta E_s: ln[Omega_b(q - k)/Omega_b(q)] + beta E_s.

    Evaluated for each accessible level, with beta the bath's exact slope when it holds all
    q_tot quanta; NaN for levels the bath cannot pay for. Zero would mean the Boltzmann
    factor is exact. It is not: see `predicted_log_correction`.
    """
    q_tot = joint.total_quanta
    beta = bath_beta_exact(joint.n_bath, q_tot, joint.levels.quantum)
    base = float(bath_log_multiplicity(joint.n_bath, q_tot))
    out = joint.log_bath_multiplicity - base + beta * joint.levels.energies
    return np.where(joint.accessible, out, np.nan)


def predicted_log_correction(joint: JointEnumeration) -> np.ndarray:
    """The second-order term the Boltzmann derivation drops: E_s^2 / 2 x d^2 ln Omega / dU^2.

    Equal to -E_s^2 / (2 k_B T^2 C_bath), which for a bath in its equipartition regime
    (C = N k_B) is -E_s^2 / (2 N_bath (k_B T)^2). It shrinks as 1/N_bath; the measured
    correction agrees with it up to terms smaller by another factor of E_s / U_bath.
    """
    curvature = bath_curvature_exact(joint.n_bath, joint.total_quanta, joint.levels.quantum)
    out = 0.5 * joint.levels.energies**2 * curvature
    return np.where(joint.accessible, out, np.nan)


# ---------------------------------------------------------------------------
# The two-level system, worked in closed form
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TwoLevelSystem:
    """A ground state at 0 and an excited state at `gap` [J], in contact with a bath at T.

    The canonical results, from P_s = exp(-E_s / (k_B T)) / Z with Z = 1 + exp(-gap/(k_B T)):

        p_excited = 1 / (exp(gap / (k_B T)) + 1),   <E> = gap x p_excited.

    As T -> 0 every system is in the ground state. As T -> infinity the two occupations
    approach 1/2 each and <E> approaches gap/2 from below -- never more. No positive
    temperature puts more systems in the upper level than the lower; module 12 takes up what
    an inverted population would mean.
    """

    gap: float

    def __post_init__(self) -> None:
        if self.gap <= 0:
            raise ValueError("gap must be positive")

    def _ratio(self, temperature) -> np.ndarray:
        t = np.asarray(temperature, dtype=float)
        if np.any(t <= 0):
            raise ValueError("temperature must be positive")
        return self.gap / (K_B * t)

    def excited_occupation(self, temperature):
        """1 / (exp(gap / k_B T) + 1), written to underflow cleanly at low T."""
        return np.exp(-np.logaddexp(0.0, self._ratio(temperature)))

    def ground_occupation(self, temperature):
        """1 / (1 + exp(-gap / k_B T))."""
        return np.exp(-np.logaddexp(0.0, -self._ratio(temperature)))

    def mean_energy(self, temperature):
        """<E> = gap / (exp(gap / k_B T) + 1) [J]."""
        return self.gap * self.excited_occupation(temperature)

    def levels(self, quantum: float) -> Levels:
        """The same system as a `Levels` list, when `gap` is a whole number of `quantum`."""
        k = self.gap / quantum
        if abs(k - round(k)) > 1e-9 * max(1.0, k):
            raise ValueError("the gap is not a whole number of quanta")
        return two_level(int(round(k)), quantum)


# ---------------------------------------------------------------------------
# Advanced: how sharp is a canonical system's energy?
# ---------------------------------------------------------------------------


def energy_moments(levels: Levels, temperature: float) -> tuple[float, float]:
    """Mean and standard deviation of the system's energy under the Boltzmann distribution [J].

    For an Einstein solid of n oscillators the relative spread std/mean falls as n^(-1/2):
    a large enough system in contact with a bath has a sharply defined energy after all,
    which is why canonical and microcanonical predictions agree in the thermodynamic limit.
    Truncate `levels` well past the mean or the spread comes out too small.
    """
    p = boltzmann_distribution(levels, temperature)
    e = levels.energies
    mean = float(np.sum(p * e))
    variance = float(np.sum(p * (e - mean) ** 2))
    return mean, math.sqrt(max(variance, 0.0))
