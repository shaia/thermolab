"""Thermodynamic potentials: one fundamental relation, read through different windows.

MODEL SPECIFICATION
    System:        a substance given by a smooth fundamental relation S(U, V, N) -- the
                   relations of `fundamental`, and the van der Waals gas defined here -- alone,
                   coupled to an ideal reservoir at T_r (and at P_r where a piston is free), or
                   pushed through a porous plug
    Dynamics:      none for the potentials themselves, which are functions of state; where an
                   internal constraint is released (`free_energy_minimization`), the composite
                   is stepped through a sequence of constrained equilibria while the reservoir
                   absorbs whatever heat keeps its temperature fixed
    Boundary:      a diathermal wall to the reservoir; a frictionless piston where P_r is held;
                   an insulated porous plug for throttling
    Ensemble:      not applicable -- the reservoir is a thermodynamic idealisation, and its
                   statistical version (a finite bath and the Boltzmann factor) is module 11's
    Ignored:       fluctuations, the finite size of any real bath, relaxation dynamics, and
                   every kind of work other than P dV unless a function says otherwise
    Valid when:    the reservoir is much larger than the system, and S is strictly concave
                   wherever it is used -- for the van der Waals gas, above its critical
                   temperature, or outside the loop below it
    Failure modes: non-concave relations, where a slope no longer names a single state and the
                   Legendre transform goes multivalued (`tangent_intercepts` shows it,
                   `legendre_transform` refuses it; module 14 repairs it); small baths
                   (module 11); processes too fast to pass through equilibrium states

WHAT A POTENTIAL IS
    Module 09's S(U, V, N), inverted to U(S, V, N), is complete: every property of the system is
    one of its derivatives. But its natural variables are entropy and volume, and no laboratory
    holds entropy fixed. A Legendre transform trades a variable for its conjugate slope without
    losing anything -- S for T, V for -P -- and each trade gives a new complete function:

        H = U + P V         natural variables (S, P, N)   dH =  T dS + V dP + mu dN
        F = U - T S         natural variables (T, V, N)   dF = -S dT - P dV + mu dN
        G = U - T S + P V   natural variables (T, P, N)   dG = -S dT + V dP + mu dN

    `NATURAL_VARIABLES` records these, with the constraint under which each is extremal.

LOCATING A STATE
    A relation is a function of (U, V, N), and a potential is asked for at (T, V, N), (T, P, N)
    or (S, P, N). So the first job is always to find the (U, V) that has the requested slopes,
    and every function here does it the same way: by bisection on a quantity that is monotone
    for a stable substance. T rises with U (a positive heat capacity), S rises with U, and P
    falls as V grows at fixed T or S (a positive compressibility). The bisections are
    vectorised, so a whole grid of states is located at once -- the Maxwell heatmaps depend on
    that -- and they read slopes by central differences, exactly as `fundamental` does.

    A relation evaluated outside its domain returns NaN: Sackur-Tetrode at U <= 0, the van der
    Waals gas at V <= N b. The bisections treat NaN as "too small", which is the right side of
    every bracket used here, so they can probe past the edge without special cases.

    Nothing here takes a generator except `gauge_readings`, which simulates a noisy instrument;
    everything else is a deterministic evaluation of state functions.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

import numpy as np

from . import forms
from .constants import K_B
from .fundamental import DEFAULT_REL_STEP, PLANCK_H, Relation

Field = Callable[[np.ndarray, np.ndarray], np.ndarray]

# Bisections stop when the bracket is this narrow relative to its ends: well below the ~1e-8
# accuracy of a central-difference slope, so locating a state never limits a result.
_BISECT_RTOL: Final[float] = 1e-13
_BISECT_MAX_ITER: Final[int] = 400
_EXPAND_MAX: Final[int] = 200

# Energy slopes use a step of at least this fraction of N k_B T (see `_slope`). Where no
# temperature is to hand -- along an isentrope, through a throttle -- 1 K stands in for it.
_ENERGY_FLOOR: Final[float] = 1e-3
_FLOOR_TEMPERATURE: Final[float] = 1.0


def _output(value) -> float | np.ndarray:
    """A float for scalar input, an array for array input."""
    value = np.asarray(value, dtype=float)
    return float(value) if value.ndim == 0 else value


# ---------------------------------------------------------------------------
# The van der Waals gas as a fundamental relation
# ---------------------------------------------------------------------------


def van_der_waals_entropy(u, v, n, mass: float, a: float, b: float) -> np.ndarray:
    """S(U, V, N) of a monatomic van der Waals gas [J/K]; NaN outside its domain.

        S = N k_B [ ln( ((V - N b)/N) (4 pi m (U + a N^2/V) / (3 N h^2))^(3/2) ) + 5/2 ]

    Sackur-Tetrode with two replacements: the volume each atom may roam is reduced by the
    excluded volume b, and the energy available as motion is U plus the attraction energy
    a N^2/V that the atoms' mutual pull has taken away. Its slopes return the two things this
    gas is known for,

        U = (3/2) N k_B T - a N^2 / V,        P = N k_B T / (V - N b) - a N^2 / V^2,

    so `gases.van_der_waals_pressure` is one of its equations of state. The constants are per
    particle, as in `gases` (a = a_molar / N_A^2, b = b_molar / N_A).

    It lives here rather than in `fundamental`, which is closed to extension, because this is
    the module that needs it: its energy depends on volume at fixed temperature, which is what
    lets U *rise* while F falls, and below its critical temperature F(V) has the dent that
    makes a Legendre transform go multivalued.
    """
    if mass <= 0 or a < 0 or b < 0:
        raise ValueError("mass must be positive and a, b non-negative")
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    n = np.asarray(n, dtype=float)
    free_volume = (v - n * b) / n
    kinetic = u + a * n**2 / v
    with np.errstate(invalid="ignore", divide="ignore"):
        thermal = 4.0 * np.pi * mass * kinetic / (3.0 * n * PLANCK_H**2)
        s = n * K_B * (np.log(free_volume) + 1.5 * np.log(thermal) + 2.5)
    return np.where((free_volume > 0) & (kinetic > 0), s, np.nan)


def van_der_waals_gas(mass: float, a: float, b: float) -> Relation:
    """The van der Waals gas as a relation s(u, v, n). At a = b = 0 it is Sackur-Tetrode."""
    if mass <= 0 or a < 0 or b < 0:
        raise ValueError("mass must be positive and a, b non-negative")

    def relation(u, v, n):
        return van_der_waals_entropy(u, v, n, mass, a, b)

    return relation


# ---------------------------------------------------------------------------
# Locating states: vectorised slopes and bisections
# ---------------------------------------------------------------------------


def _slope(relation: Relation, u, v, n, axis: int, rel_step: float,
           floor: float | np.ndarray = 0.0) -> np.ndarray:
    """dS/dx_axis at (u, v, n) by a central difference, vectorised.

    The step is `rel_step` times the variable's size, but never smaller than `rel_step` times
    `floor`. The floor matters for energies, which can pass through zero (the van der Waals
    gas does): a step that is a fraction of a vanishing |U| drops below the rounding of the
    terms S actually depends on, and the slope becomes noise. Energy slopes are therefore
    floored at a small fraction of N k_B T -- which is also why a solid so cold that its energy
    is below ~1e-5 N k_B T (the Einstein solid at k_B T < epsilon/14) is out of reach here.
    """
    args = [np.asarray(x, dtype=float) for x in (u, v, n)]
    size = np.maximum(np.abs(args[axis]), np.asarray(floor, dtype=float))
    step = rel_step * np.where(size > 0, size, 1.0)
    up, down = list(args), list(args)
    up[axis] = args[axis] + step
    down[axis] = args[axis] - step
    with np.errstate(invalid="ignore", divide="ignore"):
        return (np.asarray(relation(*up)) - np.asarray(relation(*down))) / (2.0 * step)


def _bisect(too_small: Callable[[np.ndarray], np.ndarray], lo, hi, log_space: bool = False
            ) -> np.ndarray:
    """Shrink [lo, hi] onto the point where `too_small` switches from True to False.

    `too_small(x)` must be True below the root and False above it, elementwise. Brackets are
    arrays, so every element is solved at once; iteration stops when all have converged.
    """
    lo = np.array(lo, dtype=float)
    hi = np.array(hi, dtype=float)
    lo, hi = np.broadcast_arrays(lo, hi)
    lo, hi = lo.copy(), hi.copy()
    for _ in range(_BISECT_MAX_ITER):
        mid = np.sqrt(lo * hi) if log_space else 0.5 * (lo + hi)
        with np.errstate(invalid="ignore", divide="ignore"):
            below = np.asarray(too_small(mid), dtype=bool)
        lo = np.where(below, mid, lo)
        hi = np.where(below, hi, mid)
        if np.all(np.abs(hi - lo) <= _BISECT_RTOL * np.maximum(np.abs(lo), np.abs(hi))):
            break
    return 0.5 * (lo + hi)


def _expand(too_small: Callable[[np.ndarray], np.ndarray], start, factor: float,
            upward: bool) -> np.ndarray:
    """Push a positive bracket end outward, by `factor` per try, until it is on the right side.

    Upward, the end must stop being "too small"; downward, it must become so.
    """
    x = np.array(start, dtype=float)
    for _ in range(_EXPAND_MAX):
        with np.errstate(invalid="ignore", divide="ignore"):
            below = np.asarray(too_small(x), dtype=bool)
        wrong = below if upward else ~below
        if not np.any(wrong):
            return x
        x = np.where(wrong, x * factor if upward else x / factor, x)
    raise ValueError("could not bracket the state: is the relation monotone here?")


def _energy_where(too_small: Callable[[np.ndarray], np.ndarray], scale) -> np.ndarray:
    """Bisect for an energy, from a bracket grown out of a positive `scale`.

    The lower end shrinks toward zero first, by factors of four, and only crosses into negative
    energies if the root is not positive. Order matters: a relation may return finite nonsense
    below its domain -- `fundamental.einstein_solid` does at U < 0 -- and a bracket that only
    reaches negative energies when the root demands it never consults that nonsense.
    Negative roots are real for the van der Waals gas at high density, where the attraction
    energy outweighs the motion.
    """
    scale = np.asarray(scale, dtype=float)
    hi = _expand(too_small, scale, 2.0, upward=True)

    def wrong_side(x):
        with np.errstate(invalid="ignore", divide="ignore"):
            return ~np.asarray(too_small(x), dtype=bool)

    lo = hi.copy()
    wrong = np.ones(lo.shape, dtype=bool)
    for _ in range(64):
        lo = np.where(wrong, lo / 4.0, lo)
        wrong = wrong_side(lo)
        if not np.any(wrong):
            break
    else:
        lo = np.where(wrong, -np.abs(hi), lo)
        for _ in range(_EXPAND_MAX):
            wrong = wrong_side(lo)
            if not np.any(wrong):
                break
            lo = np.where(wrong, 2.0 * lo, lo)
        else:
            raise ValueError("could not bracket the energy from below")
    return _bisect(too_small, lo, hi)


def energy_at_temperature(relation: Relation, temperature, volume, n,
                          rel_step: float = DEFAULT_REL_STEP):
    """U such that (dS/dU)_{V,N} = 1/T [J], vectorised over T, V and N.

    The inverse of `fundamental.temperature_of`. For a stable relation the slope falls as U
    rises, so there is exactly one such U; for a convex one there may be none or several, and
    the answer is whichever the bisection lands on.
    """
    t = np.asarray(temperature, dtype=float)
    if np.any(t <= 0):
        raise ValueError("temperature must be positive")
    v, n_arr = np.asarray(volume, dtype=float), np.asarray(n, dtype=float)
    target = 1.0 / t

    floor = _ENERGY_FLOOR * n_arr * K_B * t

    def too_small(u):
        slope = _slope(relation, u, v, n_arr, 0, rel_step, floor)
        return np.isnan(slope) | (slope > target)

    return _output(_energy_where(too_small, n_arr * K_B * t))


def energy_at_entropy(relation: Relation, entropy, volume, n):
    """U(S, V, N) [J]: the energy at which the relation reaches the given entropy.

    This is the fundamental relation in its energy form, U(S, V, N), which module 09 wrote down
    and module 10 transforms. S rises with U, so the inversion is a bisection.
    """
    s = np.asarray(entropy, dtype=float)
    v, n_arr = np.asarray(volume, dtype=float), np.asarray(n, dtype=float)

    def too_small(u):
        value = np.asarray(relation(u, v, n_arr), dtype=float)
        return np.isnan(value) | (value < s)

    return _output(_energy_where(too_small, n_arr * K_B * 300.0 + 0.0 * s))


def entropy_at(relation: Relation, temperature, volume, n):
    """S(T, V, N) [J/K]: the entropy of the state at temperature T and volume V."""
    u = energy_at_temperature(relation, temperature, volume, n)
    return _output(relation(u, volume, n))


def pressure_at(relation: Relation, temperature, volume, n,
                rel_step: float = DEFAULT_REL_STEP):
    """P(T, V, N) [Pa]: the equation of state, read off the relation's slopes."""
    u = energy_at_temperature(relation, temperature, volume, n, rel_step)
    floor = _ENERGY_FLOOR * np.asarray(n, dtype=float) * K_B * np.asarray(temperature)
    ds_du = _slope(relation, u, volume, n, 0, rel_step, floor)
    ds_dv = _slope(relation, u, volume, n, 1, rel_step)
    return _output(ds_dv / ds_du)


def _volume_where(too_small: Callable[[np.ndarray], np.ndarray], guess) -> np.ndarray:
    """Bisect in log V from a bracket around `guess`, widened as needed. V is always positive."""
    guess = np.asarray(guess, dtype=float)
    hi = _expand(too_small, 2.0 * guess, 4.0, upward=True)
    lo = _expand(too_small, 0.5 * guess, 4.0, upward=False)
    return _bisect(too_small, lo, hi, log_space=True)


def state_at_temperature_and_pressure(relation: Relation, temperature, pressure, n,
                                      rel_step: float = DEFAULT_REL_STEP):
    """(U, V) of the state at temperature T and pressure P [J, m^3], vectorised.

    Nested bisection: for each trial volume, the energy is fixed by T; the volume is then the
    one whose pressure is P. Pressure falls with volume at fixed T for a stable substance, so the
    outer search is monotone. A relation with no volume dependence (the Einstein solid) has zero
    pressure everywhere, cannot be put at any other pressure, and is refused.
    """
    t = np.asarray(temperature, dtype=float)
    p = np.asarray(pressure, dtype=float)
    n_arr = np.asarray(n, dtype=float)
    if np.any(p <= 0):
        raise ValueError("pressure must be positive")
    probe_v = n_arr * K_B * t / p
    if np.all(np.asarray(pressure_at(relation, t, probe_v, n_arr, rel_step)) == 0.0):
        raise ValueError("this relation has no volume dependence, so it has no pressure to set")

    def too_small(v):
        value = np.asarray(pressure_at(relation, t, v, n_arr, rel_step))
        return np.isnan(value) | (value > p)

    v = _volume_where(too_small, probe_v)
    u = energy_at_temperature(relation, t, v, n_arr, rel_step)
    return _output(u), _output(v)


def state_at_entropy_and_pressure(relation: Relation, entropy, pressure, n,
                                  rel_step: float = DEFAULT_REL_STEP):
    """(U, V) of the state at entropy S and pressure P [J, m^3] -- the natural variables of H.

    Along a line of constant entropy the pressure falls as the volume grows (an adiabatic
    expansion), so the outer search is monotone.
    """
    s = np.asarray(entropy, dtype=float)
    p = np.asarray(pressure, dtype=float)
    n_arr = np.asarray(n, dtype=float)
    if np.any(p <= 0):
        raise ValueError("pressure must be positive")

    floor = _ENERGY_FLOOR * n_arr * K_B * _FLOOR_TEMPERATURE

    def pressure_on_isentrope(v):
        u = energy_at_entropy(relation, s, v, n_arr)
        return (_slope(relation, u, v, n_arr, 1, rel_step)
                / _slope(relation, u, v, n_arr, 0, rel_step, floor))

    def too_small(v):
        value = np.asarray(pressure_on_isentrope(v))
        return np.isnan(value) | (value > p)

    # Any positive volume is a starting guess; the bracket widens by factors of four.
    guess = n_arr * K_B * 300.0 / p + 0.0 * s
    v = _volume_where(too_small, guess)
    return _output(energy_at_entropy(relation, s, v, n_arr)), _output(v)


# ---------------------------------------------------------------------------
# The potentials
# ---------------------------------------------------------------------------


def helmholtz_from(relation: Relation, temperature, volume, n):
    """F(T, V, N) = U - T S [J], at the state with temperature T and volume V."""
    t = np.asarray(temperature, dtype=float)
    u = energy_at_temperature(relation, t, volume, n)
    return _output(u - t * np.asarray(relation(u, volume, n)))


def gibbs_from(relation: Relation, temperature, pressure, n):
    """G(T, P, N) = U - T S + P V [J], at the state with temperature T and pressure P."""
    t = np.asarray(temperature, dtype=float)
    p = np.asarray(pressure, dtype=float)
    u, v = state_at_temperature_and_pressure(relation, t, p, n)
    return _output(u - t * np.asarray(relation(u, v, n)) + p * v)


def enthalpy_from(relation: Relation, entropy, pressure, n):
    """H(S, P, N) = U + P V [J], at the state with entropy S and pressure P."""
    p = np.asarray(pressure, dtype=float)
    u, v = state_at_entropy_and_pressure(relation, entropy, p, n)
    return _output(np.asarray(u) + p * np.asarray(v))


@dataclass(frozen=True)
class Ledger:
    """One equilibrium state, and every potential built from it.

    The natural-variables map's live display. U, S, P, V and T are the state; H, F and G are
    each a sum of three of the terms U, TS and PV, which is the whole of their definition.
    """

    temperature: float
    volume: float
    n: float
    energy: float
    entropy: float
    pressure: float

    @property
    def ts(self) -> float:
        return self.temperature * self.entropy

    @property
    def pv(self) -> float:
        return self.pressure * self.volume

    @property
    def enthalpy(self) -> float:
        return self.energy + self.pv

    @property
    def helmholtz(self) -> float:
        return self.energy - self.ts

    @property
    def gibbs(self) -> float:
        return self.energy - self.ts + self.pv


def ledger_at(relation: Relation, temperature: float, volume: float, n: float) -> Ledger:
    """The state at (T, V, N) with its energy, entropy and pressure read off the relation."""
    u = float(energy_at_temperature(relation, temperature, volume, n))
    return Ledger(
        temperature=float(temperature),
        volume=float(volume),
        n=float(n),
        energy=u,
        entropy=float(relation(u, volume, n)),
        pressure=float(pressure_at(relation, temperature, volume, n)),
    )


# ---------------------------------------------------------------------------
# Natural variables
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NaturalVariables:
    """What a potential is a function of, its differential, and when it is extremal."""

    symbol: str
    name: str
    definition: str
    variables: tuple[str, ...]
    differential: str
    held_fixed: str
    behaviour: str


NATURAL_VARIABLES: Final[dict[str, NaturalVariables]] = {
    "S": NaturalVariables(
        "S", "entropy", "S(U, V, N)", ("U", "V", "N"),
        "dS = (1/T) dU + (P/T) dV - (mu/T) dN",
        "U, V, N: an isolated system", "maximum at equilibrium"),
    "U": NaturalVariables(
        "U", "internal energy", "U(S, V, N)", ("S", "V", "N"),
        "dU = T dS - P dV + mu dN",
        "S, V, N", "minimum at equilibrium"),
    "H": NaturalVariables(
        "H", "enthalpy", "H = U + P V", ("S", "P", "N"),
        "dH = T dS + V dP + mu dN",
        "S, P, N; and across a throttle, where H in = H out", "minimum at fixed S, P"),
    "F": NaturalVariables(
        "F", "Helmholtz free energy", "F = U - T S", ("T", "V", "N"),
        "dF = -S dT - P dV + mu dN",
        "T, V, N: a rigid box in contact with a bath", "minimum at equilibrium"),
    "G": NaturalVariables(
        "G", "Gibbs free energy", "G = U - T S + P V", ("T", "P", "N"),
        "dG = -S dT + V dP + mu dN",
        "T, P, N: a bath and a free piston", "minimum at equilibrium"),
}


def natural_variables(symbol: str) -> NaturalVariables:
    """Look up S, U, H, F or G."""
    try:
        return NATURAL_VARIABLES[symbol]
    except KeyError:
        raise ValueError(f"unknown potential {symbol!r}; choose from "
                         f"{sorted(NATURAL_VARIABLES)}") from None


# ---------------------------------------------------------------------------
# Legendre transforms
# ---------------------------------------------------------------------------


def tangent_intercepts(f, x) -> tuple[np.ndarray, np.ndarray]:
    """(slope, intercept) of the tangent line at every sample of f(x): p = df/dx, g = f - p x.

    No check that the slopes are monotone -- this is the raw material of a Legendre transform,
    and on a relation with a dent it traces the multivalued curve that `legendre_transform`
    refuses. Slopes are second-order central differences (one-sided at the ends), on any
    increasing grid.
    """
    x = np.asarray(x, dtype=float)
    f = np.asarray(f, dtype=float)
    if x.ndim != 1 or x.shape != f.shape:
        raise ValueError("f and x must be one-dimensional samples of the same length")
    if x.size < 3:
        raise ValueError("a second-order slope needs at least three samples")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x must increase strictly")
    slope = np.gradient(f, x, edge_order=2)
    return slope, f - slope * x


def legendre_transform(f, x) -> tuple[np.ndarray, np.ndarray]:
    """The Legendre transform g(p) = f(x) - p x of a sampled, strictly convex or concave f.

    Returns the slopes p and the transform g at each sample. The sign convention is the one
    that turns U(S) into F(T) = U - T S and F(V) into G(P) = F + P V (there p = dF/dV = -P).

    Raises unless the slopes are strictly monotone. That is not fussiness: it is the condition
    under which a slope names exactly one point, so that the family of tangent lines carries all
    the information the curve did. Where it fails, two points share a slope and the transform
    cannot say which one it means -- the information-loss case that module 14 starts from.
    """
    slope, intercept = tangent_intercepts(f, x)
    steps = np.diff(slope)
    if not (np.all(steps > 0) or np.all(steps < 0)):
        raise ValueError(
            "the slopes are not strictly monotone, so the relation is not strictly convex or "
            "concave on this grid: one slope names more than one point, and the transform "
            "would forget which"
        )
    return slope, intercept


# ---------------------------------------------------------------------------
# Maxwell relations
# ---------------------------------------------------------------------------


def maxwell_check(m: Field, n: Field, x, y, rel_step: float = DEFAULT_REL_STEP):
    """Relative gap in (dm/dy)_x = (dn/dx)_y for the form m dx + n dy, at each (x, y).

    A Maxwell relation is the statement that a potential's differential, dPhi = m dx + n dy, is
    exact, so the two cross-derivatives agree. This is module 05's test, `forms.
    mixed_partials_gap`, with two changes that thermodynamic variables need. The differences are
    taken in log x and log y -- the form m x dlnx + n y dlny is the same form -- so the step is a
    fraction of each variable and one value serves temperatures of 300 and volumes of 1e-3. And
    the gap is reported relative to the size of the two cross-derivatives,

        gap = (dm/dy - dn/dx) / (|dm/dy| + |dn/dx|),

    dimensionless and in [-1, 1], so it is never compared with an absolute tolerance. A correct
    relation leaves only the truncation error of the central differences, which falls as
    rel_step^2; a pair of fields that did not come from one potential leaves a gap that does not.

    `x` and `y` must be positive; they are always so for T, V, P and a positive entropy.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x, y = np.broadcast_arrays(x, y)
    if np.any(x <= 0) or np.any(y <= 0):
        raise ValueError("maxwell_check works in log coordinates; x and y must be positive")

    def m_log(xi, eta):
        big_x, big_y = np.exp(xi), np.exp(eta)
        return big_x * np.asarray(m(big_x, big_y))

    def n_log(xi, eta):
        big_x, big_y = np.exp(xi), np.exp(eta)
        return big_y * np.asarray(n(big_x, big_y))

    def zero(xi, _eta):
        return np.zeros_like(xi)

    xi, eta = np.log(x), np.log(y)
    # d(x m)/d ln y = x y dm/dy, and d(y n)/d ln x = x y dn/dx: the same gap, scaled by x y.
    left = forms.mixed_partials_gap(m_log, zero, xi, eta, h=rel_step)
    right = -forms.mixed_partials_gap(zero, n_log, xi, eta, h=rel_step)
    size = np.abs(left) + np.abs(right)
    safe = np.where(size > 0, size, 1.0)
    # `forms` promotes scalars to length-1 arrays; hand back the shape the caller passed.
    return _output(np.where(size > 0, (left - right) / safe, 0.0).reshape(x.shape))


def helmholtz_form(relation: Relation, n: float) -> tuple[Field, Field]:
    """The coefficients of dF = -S dT - P dV at fixed N, as fields of (T, V).

    Built from the relation in two different ways -- S is a *value* of the relation at the
    located state, P is a *ratio of its slopes* there -- so the Maxwell relation
    (dS/dV)_T = (dP/dT)_V that `maxwell_check` tests on this pair is a statement connecting two
    different operations, not a derivative compared with itself.
    """

    def minus_entropy(t, v):
        return -np.asarray(entropy_at(relation, t, v, n))

    def minus_pressure(t, v):
        return -np.asarray(pressure_at(relation, t, v, n))

    return minus_entropy, minus_pressure


# ---------------------------------------------------------------------------
# Entropy from a pressure gauge
# ---------------------------------------------------------------------------


def gauge_readings(relation: Relation, n: float, temperatures, volumes, noise: float,
                   rng: np.random.Generator) -> np.ndarray:
    """Simulated pressure readings P(T, V) with relative Gaussian noise [Pa].

    Rows follow `volumes`, columns `temperatures`. Each reading is the relation's pressure times
    (1 + noise * z) with z standard normal: a gauge whose error is a fixed fraction of full
    scale would be closer to life for a real instrument, but a fractional error keeps the
    readings honest at every volume with one parameter.
    """
    if noise < 0:
        raise ValueError("noise must be non-negative")
    t = np.asarray(temperatures, dtype=float)
    v = np.asarray(volumes, dtype=float)
    true = np.asarray(pressure_at(relation, t[None, :], v[:, None], n), dtype=float)
    return true * (1.0 + noise * rng.standard_normal(true.shape))


@dataclass(frozen=True)
class GaugeEntropy:
    """Delta S along an isotherm, reconstructed from pressure-gauge data.

    `slopes` and `slope_errors` are the fitted (dP/dT)_V at each volume with their standard
    errors; `entropy_change` is Delta S from the first volume to each of the others, and
    `entropy_error` its standard error, propagated from the slopes as independent.
    """

    volumes: np.ndarray
    slopes: np.ndarray
    slope_errors: np.ndarray
    entropy_change: np.ndarray
    entropy_error: np.ndarray


def entropy_from_gauge(temperatures, volumes, pressures) -> GaugeEntropy:
    """Delta S(V) at fixed T from P(T, V) readings, by the Maxwell relation (dS/dV)_T = (dP/dT)_V.

    At each volume, a straight line through P against T gives (dP/dT)_V -- exact for the ideal
    and van der Waals gases, whose pressure is linear in T at fixed V, and a local slope for
    anything else. Integrating that slope over V gives the entropy change along an isotherm,

        Delta S = integral (dP/dT)_V dV,

    and nothing in it measured an entropy: a pressure gauge and a thermometer, only. The
    integral is taken in ln V, as the sum over (dP/dT)_V V d(ln V), by the trapezoid rule; for
    an ideal gas that integrand is constant, so a volume grid spaced evenly in ln V makes the
    rule exact and leaves the noise as the only error.
    """
    t = np.asarray(temperatures, dtype=float)
    v = np.asarray(volumes, dtype=float)
    p = np.asarray(pressures, dtype=float)
    if p.shape != (v.size, t.size):
        raise ValueError("pressures must have one row per volume and one column per temperature")
    if t.size < 3:
        raise ValueError("a slope with an error bar needs at least three temperatures")
    if np.any(np.diff(v) <= 0):
        raise ValueError("volumes must increase")

    slopes = np.empty(v.size)
    errors = np.empty(v.size)
    for i in range(v.size):
        coeffs, cov = np.polyfit(t, p[i], 1, cov=True)
        slopes[i] = coeffs[0]
        errors[i] = np.sqrt(cov[0, 0])

    integrand = slopes * v
    sigma = errors * v
    d_ln_v = np.diff(np.log(v))
    change = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[:-1] + integrand[1:]) * d_ln_v)])

    # Trapezoid weights for each prefix of the grid, then errors added in quadrature.
    variance = np.zeros(v.size)
    for k in range(1, v.size):
        weights = np.zeros(k + 1)
        weights[:-1] += 0.5 * d_ln_v[:k]
        weights[1:] += 0.5 * d_ln_v[:k]
        variance[k] = np.sum((weights * sigma[: k + 1]) ** 2)
    return GaugeEntropy(v, slopes, errors, change, np.sqrt(variance))


# ---------------------------------------------------------------------------
# Minimisation at fixed T and V: a piston between two samples, against a bath
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MinimizationTrace:
    """A composite at the bath's temperature, stepped from its prepared state to equilibrium.

    `share` is the fraction of the total volume on side A. `energy`, `entropy` and
    `free_energy` are the composite's totals over both sides. The bath's entropy change follows
    from its heat: the bath at T gives up whatever the composite's energy gains, so
    Delta S_bath = -Delta U / T, and the total over system and bath is
    Delta S - Delta U / T = -Delta F / T.
    """

    temperature: float
    share: np.ndarray
    energy: np.ndarray
    entropy: np.ndarray
    free_energy: np.ndarray
    pressure_a: np.ndarray
    pressure_b: np.ndarray

    @property
    def bath_entropy_change(self) -> np.ndarray:
        return -(self.energy - self.energy[0]) / self.temperature

    @property
    def system_entropy_change(self) -> np.ndarray:
        return self.entropy - self.entropy[0]

    @property
    def total_entropy_change(self) -> np.ndarray:
        return self.system_entropy_change + self.bath_entropy_change


_GOLDEN: Final[float] = (np.sqrt(5.0) - 1.0) / 2.0


def _golden_minimum(f: Callable[[float], float], lo: float, hi: float, tol: float) -> float:
    """Minimise a unimodal f on [lo, hi] by golden-section search."""
    x1 = hi - _GOLDEN * (hi - lo)
    x2 = lo + _GOLDEN * (hi - lo)
    f1, f2 = f(x1), f(x2)
    while hi - lo > tol:
        if f1 > f2:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + _GOLDEN * (hi - lo)
            f2 = f(x2)
        else:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - _GOLDEN * (hi - lo)
            f1 = f(x1)
    return 0.5 * (lo + hi)


def free_energy_minimization(relation: Relation, t_bath: float, volume: float, n_a: float,
                             n_b: float, start_share: float, n_steps: int = 201,
                             tolerance: float = 1e-10) -> MinimizationTrace:
    """Release a piston between two samples at the bath temperature, and trace the way down.

    A rigid box of volume V holds n_a particles on side A and n_b on side B of a piston, the
    whole box in contact with a bath at T. The piston is released from the share V_A/V =
    `start_share` and allowed to move, braked, until it stops -- at the share that minimises
    F_A + F_B. The trace steps through the constrained equilibria in between: each side at T,
    the piston held at each intermediate share in turn.

    The contract is that F is non-increasing along the trace and the total entropy of system
    plus bath non-decreasing -- two statements of one fact, since their changes are tied by
    Delta S_tot = -Delta F / T. What is *not* promised is anything about U: for a van der Waals
    gas, whose energy rises as its atoms move apart, U climbs to a maximum at exactly the point
    where F reaches its minimum.
    """
    if not 0.0 < start_share < 1.0:
        raise ValueError("start_share must lie strictly between 0 and 1")
    if n_steps < 2:
        raise ValueError("a trace needs at least two steps")

    def total_free_energy(share: float) -> float:
        return (float(helmholtz_from(relation, t_bath, share * volume, n_a))
                + float(helmholtz_from(relation, t_bath, (1.0 - share) * volume, n_b)))

    edge = 1e-6
    end_share = _golden_minimum(total_free_energy, edge, 1.0 - edge, tolerance)
    shares = np.linspace(start_share, end_share, n_steps)
    v_a, v_b = shares * volume, (1.0 - shares) * volume
    u_a = np.asarray(energy_at_temperature(relation, t_bath, v_a, n_a))
    u_b = np.asarray(energy_at_temperature(relation, t_bath, v_b, n_b))
    s_total = np.asarray(relation(u_a, v_a, n_a)) + np.asarray(relation(u_b, v_b, n_b))
    energy = u_a + u_b
    return MinimizationTrace(
        temperature=float(t_bath),
        share=shares,
        energy=energy,
        entropy=s_total,
        free_energy=energy - t_bath * s_total,
        pressure_a=np.asarray(pressure_at(relation, t_bath, v_a, n_a)),
        pressure_b=np.asarray(pressure_at(relation, t_bath, v_b, n_b)),
    )


# ---------------------------------------------------------------------------
# Throttling: H in = H out
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Throttled:
    """A gas pushed steadily through an insulated porous plug, inlet and outlet states."""

    pressure_in: float
    pressure_out: float
    temperature_in: float
    temperature_out: float
    volume_in: float
    volume_out: float
    energy_in: float
    energy_out: float

    @property
    def enthalpy_in(self) -> float:
        return self.energy_in + self.pressure_in * self.volume_in

    @property
    def enthalpy_out(self) -> float:
        return self.energy_out + self.pressure_out * self.volume_out

    @property
    def temperature_change(self) -> float:
        return self.temperature_out - self.temperature_in


def throttle(relation: Relation, n: float, temperature_in: float, pressure_in: float,
             pressure_out: float, rel_step: float = DEFAULT_REL_STEP) -> Throttled:
    """Joule-Thomson throttling: find the outlet state with the inlet's enthalpy.

    Push a parcel of N particles through the plug. The gas behind it does work P_in V_in on the
    parcel, the parcel does P_out V_out on the gas ahead, and no heat crosses the insulated
    walls, so U_out - U_in = P_in V_in - P_out V_out: H is the same on both sides. Nothing else
    is: not U, not the volume, and -- except for an ideal gas -- not the temperature.

    The outlet state is found in one bisection over its volume, with U = H - P_out V fixed at
    every trial volume by the conserved enthalpy.
    """
    if pressure_out <= 0 or pressure_in <= 0:
        raise ValueError("pressures must be positive")
    u_in, v_in = state_at_temperature_and_pressure(relation, temperature_in, pressure_in, n,
                                                   rel_step)
    h = float(u_in) + pressure_in * float(v_in)
    if h <= 0:
        raise ValueError("throttle needs a positive enthalpy (a gas, not a dense liquid)")

    floor = _ENERGY_FLOOR * n * K_B * _FLOOR_TEMPERATURE

    def pressure_given_volume(v):
        u = h - pressure_out * v
        return (_slope(relation, u, v, n, 1, rel_step)
                / _slope(relation, u, v, n, 0, rel_step, floor))

    def too_small(v):
        value = np.asarray(pressure_given_volume(v))
        return np.isnan(value) | (value > pressure_out)

    hi = h / pressure_out * (1.0 - 1e-9)
    v_out = float(_bisect(too_small, 1e-9 * hi, hi, log_space=True))
    u_out = h - pressure_out * v_out
    t_out = 1.0 / float(_slope(relation, u_out, v_out, n, 0, rel_step, floor))
    return Throttled(pressure_in, pressure_out, float(temperature_in), t_out,
                     float(v_in), v_out, float(u_in), u_out)
