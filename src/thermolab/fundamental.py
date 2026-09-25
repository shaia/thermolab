"""The fundamental relation S(U, V, N): one function from which everything else follows.

MODEL SPECIFICATION
    System:        a fundamental relation S(U, V, N) taken as the complete thermodynamic
                   description of a system; concretely the Einstein solid's S(U, n) and the
                   monatomic ideal gas's Sackur-Tetrode S(U, V, N), alone or as the two halves
                   of a composite separated by an internal wall
    Dynamics:      none -- the surface is static; "what happens" when a constraint is released
                   is the maximisation of the composite's total entropy over the partitions the
                   wall now permits (module 01's exchange simulation supplies one dynamics that
                   gets there)
    Boundary:      the composite is isolated; the internal wall's character -- adiabatic or
                   diathermal, fixed or movable, impermeable or perforated -- is the constraint
                   being released
    Ensemble:      equilibrium thermodynamics -- every point on the surface is an equilibrium
                   state, and the maximum postulate stands in for any relaxation dynamics
    Ignored:       fluctuations about the maximum (relative size N^(-1/2), module 08), surface
                   and interface terms, and long-range forces, which would break extensivity
    Valid when:    each subsystem is macroscopic enough that S is smooth and extensive; the
                   Einstein form in the classical regime where Stirling's approximation holds
                   for both the quanta and the oscillators; Sackur-Tetrode in the dilute
                   classical regime, where the thermal wavelength is small against the spacing
    Failure modes: small systems (ln N corrections to extensivity, measured in module 08); low
                   temperature, where Sackur-Tetrode's S falls to minus infinity -- unphysical,
                   and repaired only by quantum statistics (module 17); and convex patches of
                   the surface, which a stable substance cannot have and which mark
                   coexistence (module 14) or long-range forces (`self_gravitating_entropy`)

A RELATION IS A FUNCTION
    Everything here takes a *relation*: a callable s(u, v, n) returning the entropy in J/K,
    vectorised over NumPy arrays. The factories `einstein_solid`, `monatomic_ideal_gas` and
    `self_gravitating_gas` close over their material constants and return one. The Einstein
    solid has no volume, so its relation ignores `v`; its `n` counts oscillators rather than
    particles.

    Temperature, pressure and chemical potential are not supplied with a relation. They are
    *read off it* as slopes, by central differences:

        1/T = (dS/dU)_{V,N},   P/T = (dS/dV)_{U,N},   -mu/T = (dS/dN)_{U,V}.

    That is the module's claim made executable: hand over S(U, V, N) and nothing else, and
    every equation of state comes back out. The tests check the slopes against the closed
    forms each relation implies, so a slope that disagreed would be a bug in one or the other.

WHY NUMERICAL SLOPES AT ALL
    The closed forms exist for both named relations, and `einstein_solid_temperature` gives one
    for comparison. The numerical route is kept because it works on *any* relation -- a
    tabulated one, a student's guess, the convex star -- and because the Euler and
    Gibbs-Duhem checks below are only tests of extensivity if nothing about the relation's
    algebra was used to build them. Steps are fractional (`rel_step` times the variable) so a
    single default serves joules at 1e-18 and volumes at 1e-3.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from typing import Final

import numpy as np

from .constants import K_B

#: Planck constant [J s] (SI 2019 exact definition). It lives here rather than in `constants`,
#: which is closed to extension, because Sackur-Tetrode is the only place in the classical
#: modules that needs it -- and needing it at all is the formula's warning label: an entropy
#: whose zero is set by h cannot be derived by classical counting alone (see module 12/17).
PLANCK_H: Final[float] = 6.62607015e-34

# s(u, v, n) -> S [J/K]; each argument a float or an array, broadcast together.
Relation = Callable[..., np.ndarray]

# Default fractional step for the central differences. The truncation error is ~rel_step^2
# and the rounding error ~1e-16/rel_step, so 1e-4 sits near the bottom of that valley with
# plenty of room either side: about 1e-8 relative error in every slope.
DEFAULT_REL_STEP: Final[float] = 1e-4

CHANNELS: Final[tuple[str, ...]] = ("energy", "volume", "particles")


# ---------------------------------------------------------------------------
# The relations
# ---------------------------------------------------------------------------


def _x_log_x(x: np.ndarray) -> np.ndarray:
    """x ln x with its limit 0 at x = 0, elementwise."""
    x = np.asarray(x, dtype=float)
    safe = np.where(x > 0, x, 1.0)
    return np.where(x > 0, x * np.log(safe), 0.0)


def einstein_solid_entropy(u, n, quantum: float) -> np.ndarray:
    """S(U, n) of an Einstein solid, in the Stirling form [J/K].

    n oscillators sharing q = U/quantum identical quanta have Omega = C(q + n - 1, q)
    microstates (stars and bars). Stirling's approximation, with q and n both large, turns
    k_B ln Omega into

        S = k_B [ (q + n) ln(q + n) - q ln q - n ln n ].

    This form is exactly extensive -- scale U and n together and S scales with them -- which
    the exact count is not (module 08 measured the ln N correction). `equilibrium` keeps the
    exact count for the entropy ledger; this is the smooth surface whose slopes are the
    temperature.
    """
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    q = np.asarray(u, dtype=float) / quantum
    n = np.asarray(n, dtype=float)
    return K_B * (_x_log_x(q + n) - _x_log_x(q) - _x_log_x(n))


def einstein_solid_temperature(u, n, quantum: float) -> np.ndarray:
    """Closed-form T(U, n) = quantum / (k_B ln(1 + n quantum / U)) of the Einstein solid.

    The slope of `einstein_solid_entropy`, inverted. For U >> n quantum the logarithm
    expands to n quantum/U - (n quantum/U)^2/2, giving T = U/(n k_B) + quantum/(2 k_B): module
    01's equipartition map T = q quantum/(n k_B), plus a constant offset of half a quantum that
    matters less and less as the solid warms.
    """
    u = np.asarray(u, dtype=float)
    return quantum / (K_B * np.log1p(np.asarray(n, dtype=float) * quantum / u))


def sackur_tetrode_entropy(u, v, n, mass: float) -> np.ndarray:
    """S(U, V, N) of a monatomic classical ideal gas -- the Sackur-Tetrode equation [J/K].

        S = N k_B [ ln( (V/N) (4 pi m U / (3 N h^2))^(3/2) ) + 5/2 ]

    A stated result here, not derived: deriving it needs phase-space counting with a cell of
    size h per degree of freedom and the 1/N! of indistinguishable particles, which is module
    12's business. Its slopes are nevertheless checkable with no quantum mechanics at all --
    they return U = (3/2) N k_B T and P V = N k_B T -- and that is how this module uses it.
    Below the dilute classical regime the logarithm's argument, (V/N)/lambda^3, falls under 1
    and S turns negative: the formula's own failure flag.
    """
    if mass <= 0:
        raise ValueError("mass must be positive")
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    n = np.asarray(n, dtype=float)
    per_particle_volume = v / n
    thermal = 4.0 * np.pi * mass * u / (3.0 * n * PLANCK_H**2)
    return n * K_B * (np.log(per_particle_volume) + 1.5 * np.log(thermal) + 2.5)


def self_gravitating_entropy(u, n, energy_scale: float) -> np.ndarray:
    """S(U) of a self-gravitating ball of gas -- the textbook convex relation [J/K].

    A gas held together by its own gravity obeys the virial theorem, 2K + U_grav = 0, so its
    total energy is U = -K = -(3/2) N k_B T: negative, and *falling* as the gas heats. Its
    size is not a free variable either -- gravity sets the radius, R ~ G N m^2 / (k_B T) -- so
    the ideal-gas entropy N k_B ln(V T^(3/2)), with V ~ R^3, becomes, up to a constant,

        S = -(3/2) N k_B ln( -U / (N^3 energy_scale) ),   U < 0.

    Its slope 1/T = -(3/2) N k_B / U is positive and its curvature is positive too. It is
    convex, its heat capacity is -(3/2) N k_B, and it is included as the counterexample to the
    stability argument: a star loses energy and gets hotter. The N^3 is where it violates the
    Ignored field above -- gravity is long-ranged, and doubling the gas does not double S --
    which is exactly why it escapes the concavity that extensivity would otherwise force, and
    why `euler_residual` reports it as far from zero.
    """
    if energy_scale <= 0:
        raise ValueError("energy_scale must be positive")
    u = np.asarray(u, dtype=float)
    if np.any(u >= 0):
        raise ValueError("a bound self-gravitating gas has negative total energy")
    n = np.asarray(n, dtype=float)
    return -1.5 * n * K_B * np.log(-u / (n**3 * energy_scale))


def einstein_solid(quantum: float) -> Relation:
    """The Einstein solid as a relation s(u, v, n); `v` is ignored and `n` counts oscillators."""
    if quantum <= 0:
        raise ValueError("quantum must be positive")

    def relation(u, v, n):
        return einstein_solid_entropy(u, n, quantum) + 0.0 * np.asarray(v, dtype=float)

    return relation


def monatomic_ideal_gas(mass: float) -> Relation:
    """The Sackur-Tetrode ideal gas as a relation s(u, v, n)."""
    if mass <= 0:
        raise ValueError("mass must be positive")

    def relation(u, v, n):
        return sackur_tetrode_entropy(u, v, n, mass)

    return relation


def self_gravitating_gas(energy_scale: float) -> Relation:
    """The convex self-gravitating relation s(u, v, n); `v` is ignored."""
    if energy_scale <= 0:
        raise ValueError("energy_scale must be positive")

    def relation(u, v, n):
        return self_gravitating_entropy(u, n, energy_scale) + 0.0 * np.asarray(v, dtype=float)

    return relation


def entropy_surface(relation: Relation, u_grid, v_grid, n: float) -> np.ndarray:
    """Tabulate S on a (U, V) grid at fixed N; rows follow `v_grid`, columns `u_grid`."""
    uu, vv = np.meshgrid(np.asarray(u_grid, dtype=float), np.asarray(v_grid, dtype=float))
    return np.asarray(relation(uu, vv, np.full_like(uu, n)), dtype=float)


# ---------------------------------------------------------------------------
# Slopes: the intensive variables, read off the surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Slopes:
    """The three first derivatives of S at one point: 1/T, P/T and -mu/T."""

    ds_du: float
    ds_dv: float
    ds_dn: float

    @property
    def temperature(self) -> float:
        return 1.0 / self.ds_du

    @property
    def pressure(self) -> float:
        return self.ds_dv / self.ds_du

    @property
    def chemical_potential(self) -> float:
        return -self.ds_dn / self.ds_du


def _central(relation: Relation, point: Sequence[float], axis: int, rel_step: float) -> float:
    step = rel_step * abs(point[axis])
    if step == 0.0:
        raise ValueError("cannot take a fractional step from a variable that is zero")
    up = list(point)
    down = list(point)
    up[axis] += step
    down[axis] -= step
    return float((relation(*up) - relation(*down)) / (2.0 * step))


def entropy_slopes(relation: Relation, u: float, v: float, n: float,
                   rel_step: float = DEFAULT_REL_STEP) -> Slopes:
    """(dS/dU, dS/dV, dS/dN) at (u, v, n), each by a second-order central difference.

    A relation with no volume dependence returns exactly zero for dS/dV, and therefore zero
    pressure: the two function values differ in nothing.
    """
    point = (float(u), float(v), float(n))
    return Slopes(
        ds_du=_central(relation, point, 0, rel_step),
        ds_dv=_central(relation, point, 1, rel_step),
        ds_dn=_central(relation, point, 2, rel_step),
    )


def temperature_of(relation: Relation, u: float, v: float, n: float,
                   rel_step: float = DEFAULT_REL_STEP) -> float:
    """T = 1 / (dS/dU)_{V,N} [K]."""
    return 1.0 / _central(relation, (float(u), float(v), float(n)), 0, rel_step)


def pressure_of(relation: Relation, u: float, v: float, n: float,
                rel_step: float = DEFAULT_REL_STEP) -> float:
    """P = T (dS/dV)_{U,N} [Pa]."""
    return entropy_slopes(relation, u, v, n, rel_step).pressure


def chemical_potential_of(relation: Relation, u: float, v: float, n: float,
                          rel_step: float = DEFAULT_REL_STEP) -> float:
    """mu = -T (dS/dN)_{U,V} [J per particle]. Named here; module 13 develops it."""
    return entropy_slopes(relation, u, v, n, rel_step).chemical_potential


# ---------------------------------------------------------------------------
# Curvature: stability
# ---------------------------------------------------------------------------


def _second(relation: Relation, point: Sequence[float], i: int, j: int,
            rel_step: float) -> float:
    """d^2 S / dx_i dx_j by central differences."""
    h_i = rel_step * abs(point[i])
    h_j = rel_step * abs(point[j])

    def at(di: float, dj: float) -> float:
        p = list(point)
        p[i] += di
        p[j] += dj
        return float(relation(*p))

    if i == j:
        return (at(h_i, 0.0) - 2.0 * at(0.0, 0.0) + at(-h_i, 0.0)) / h_i**2
    return (at(h_i, h_j) - at(h_i, -h_j) - at(-h_i, h_j) + at(-h_i, -h_j)) / (4.0 * h_i * h_j)


# Curvatures need a larger step than slopes: a second difference loses two powers of the step
# to rounding, so the valley between truncation (~h^2) and rounding (~1e-16/h^2) bottoms out
# near h ~ 1e-4 in *squared* terms -- rel_step 1e-3 gives about 1e-6 relative error.
CURVATURE_REL_STEP: Final[float] = 1e-3


def entropy_curvature(relation: Relation, u: float, v: float, n: float,
                      rel_step: float = CURVATURE_REL_STEP) -> float:
    """(d^2 S / dU^2)_{V,N} -- must be <= 0 for a stable system."""
    return _second(relation, (float(u), float(v), float(n)), 0, 0, rel_step)


def heat_capacity_of(relation: Relation, u: float, v: float, n: float,
                     rel_step: float = CURVATURE_REL_STEP) -> float:
    """C_V = -1 / (T^2 d^2S/dU^2) [J/K], from the curvature of S(U).

    From 1/T = dS/dU, differentiating once more gives d^2S/dU^2 = -(1/T^2) dT/dU = -1/(T^2 C_V).
    So the sign of the heat capacity *is* the sign of the curvature, reversed: a concave S
    is a positive heat capacity, and a convex one is a negative heat capacity.
    """
    t = temperature_of(relation, u, v, n)
    return -1.0 / (t**2 * entropy_curvature(relation, u, v, n, rel_step))


def concavity_check(relation: Relation, u_grid, v: float, n: float) -> np.ndarray:
    """Second differences of S(U) along `u_grid` at fixed (v, n); all <= 0 where S is concave.

    Returns one value per interior grid point, S[i-1] - 2 S[i] + S[i+1], so its sign is what
    matters rather than its size. The grid must be evenly spaced.
    """
    u_grid = np.asarray(u_grid, dtype=float)
    if u_grid.size < 3:
        raise ValueError("a second difference needs at least three grid points")
    s = np.asarray(relation(u_grid, np.full_like(u_grid, v), np.full_like(u_grid, n)))
    return s[:-2] - 2.0 * s[1:-1] + s[2:]


def is_stable(relation: Relation, u: float, v: float, n: float,
              rel_step: float = CURVATURE_REL_STEP) -> bool:
    """True when S is locally concave in (U, V) at fixed N.

    Three conditions: d^2S/dU^2 <= 0 (positive heat capacity), d^2S/dV^2 <= 0, and a
    non-negative Hessian determinant, which with the other two gives a positive isothermal
    compressibility. Tolerances are relative to the size of the terms, so a relation with no
    volume dependence (the Einstein solid, where two of the three vanish) is judged on its
    energy curvature alone.
    """
    point = (float(u), float(v), float(n))
    s_uu = _second(relation, point, 0, 0, rel_step)
    s_vv = _second(relation, point, 1, 1, rel_step)
    s_uv = _second(relation, point, 0, 1, rel_step)
    scale = abs(s_uu * s_vv) + s_uv**2
    determinant_ok = s_uu * s_vv - s_uv**2 >= -1e-6 * scale
    return bool(s_uu < 0.0 and s_vv <= 1e-6 * abs(s_vv) and determinant_ok)


# ---------------------------------------------------------------------------
# Extensivity: the Euler and Gibbs-Duhem relations
# ---------------------------------------------------------------------------


def euler_residual(relation: Relation, u: float, v: float, n: float,
                   rel_step: float = DEFAULT_REL_STEP) -> float:
    """Relative residual of U - T S + P V - mu N = 0.

    Zero, to the accuracy of the slopes, exactly when the relation is extensive: the Euler
    relation is what S(lambda U, lambda V, lambda N) = lambda S says after differentiating at
    lambda = 1, and nothing else. Reported as a fraction of |U| -- the share of the energy the
    three terms fail to account for -- never as an absolute number at the 1e-18 J scale. The
    individual terms T S and mu N are each many times U for a gas, so a correct relation shows
    the slopes' rounding here magnified by that factor: ~1e-7, not ~1e-8.
    """
    slopes = entropy_slopes(relation, u, v, n, rel_step)
    s = float(relation(u, v, n))
    t, p, mu = slopes.temperature, slopes.pressure, slopes.chemical_potential
    return float(abs(u - t * s + p * v - mu * n) / abs(u))


def gibbs_duhem_residual(relation: Relation, u: float, v: float, n: float,
                         du: float, dv: float, dn: float,
                         rel_step: float = DEFAULT_REL_STEP) -> float:
    """Relative residual of S dT - V dP + N dmu = 0 across a small displacement.

    The intensive variables are read off at both ends of the displacement and differenced;
    S, V and N are taken at the midpoint, which makes the discrete sum accurate to second
    order in the displacement. Relative to the sizes of the three terms.
    """
    start = entropy_slopes(relation, u, v, n, rel_step)
    end = entropy_slopes(relation, u + du, v + dv, n + dn, rel_step)
    mid = (u + du / 2.0, v + dv / 2.0, n + dn / 2.0)
    s_mid = float(relation(*mid))
    terms = np.array([
        s_mid * (end.temperature - start.temperature),
        -mid[1] * (end.pressure - start.pressure),
        mid[2] * (end.chemical_potential - start.chemical_potential),
    ])
    size = np.abs(terms).sum()
    if size == 0.0:
        return 0.0
    return float(abs(terms.sum()) / size)


# ---------------------------------------------------------------------------
# Composites: equilibrium as constrained maximisation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Part:
    """One side of a composite: its energy [J], volume [m^3] and particle number."""

    energy: float
    volume: float
    number: float

    def extensive(self, channel: str) -> float:
        return {"energy": self.energy, "volume": self.volume, "particles": self.number}[channel]

    def with_value(self, channel: str, value: float) -> Part:
        field = {"energy": "energy", "volume": "volume", "particles": "number"}[channel]
        return replace(self, **{field: value})


@dataclass(frozen=True)
class Composite:
    """Two subsystems behind an internal wall, isolated together.

    The totals of energy, volume and particle number are fixed; the wall decides which of them
    may be *redistributed* between the sides. `released` answers what the new distribution is
    once some of them may move -- the partition with the largest total entropy -- and returns
    it as a new `Composite`, leaving this one untouched.
    """

    relation_a: Relation
    relation_b: Relation
    a: Part
    b: Part

    @property
    def entropy_a(self) -> float:
        return float(self.relation_a(self.a.energy, self.a.volume, self.a.number))

    @property
    def entropy_b(self) -> float:
        return float(self.relation_b(self.b.energy, self.b.volume, self.b.number))

    @property
    def total_entropy(self) -> float:
        """S_A + S_B: entropy is additive over subsystems (a postulate, and 08's theorem)."""
        return self.entropy_a + self.entropy_b

    def total(self, channel: str) -> float:
        return self.a.extensive(channel) + self.b.extensive(channel)

    def slopes_a(self) -> Slopes:
        return entropy_slopes(self.relation_a, self.a.energy, self.a.volume, self.a.number)

    def slopes_b(self) -> Slopes:
        return entropy_slopes(self.relation_b, self.b.energy, self.b.volume, self.b.number)

    def with_share(self, channel: str, share_a: float) -> Composite:
        """The same composite with a fraction `share_a` of one conserved total on side A.

        Side B receives `total - value_a`, computed once, so the total is conserved to the
        last bit of the subtraction rather than by two independent multiplications.
        """
        total = self.total(channel)
        value_a = share_a * total
        return replace(
            self,
            a=self.a.with_value(channel, value_a),
            b=self.b.with_value(channel, total - value_a),
        )

    def released(self, *channels: str, tolerance: float = 1e-12) -> Composite:
        """Maximise the total entropy over the partitions of the released `channels`.

        "energy" makes the wall diathermal, "volume" frees it to move as a piston, and
        "particles" perforates it. Two combinations are refused.

        Volume or particles *without* energy. A piston that moves does work on both sides,
        and a particle that crosses carries its energy with it, so neither can be released
        while each side's energy stays fixed. Maximising anyway gives equal P/T rather than
        equal P -- the adiabatic-piston problem, which has no answer from entropy alone
        (Callen, section 2-7). The diathermal versions are well posed, and they are what
        `released` accepts: ("energy",), ("energy", "volume"), ("energy", "particles").

        All three at once. With every constraint gone the wall is not there, and only the
        intensive state -- not how much matter sits on "each side" of a wall that does not
        exist -- is determined.

        The maximisation is a nested golden-section search over each released channel's
        share, which is safe because the total entropy of two concave relations is concave in
        the shares. It is not safe for a convex relation, and nothing here pretends otherwise:
        for one of those the "maximum" is an edge of the allowed range -- see
        `self_gravitating_entropy`.
        """
        channels = tuple(dict.fromkeys(channels))
        unknown = [c for c in channels if c not in CHANNELS]
        if unknown:
            raise ValueError(f"unknown channel(s) {unknown}; choose from {CHANNELS}")
        if not channels:
            return self
        if "energy" not in channels:
            raise ValueError(
                "a movable or perforated wall also moves energy between the sides; release "
                "'energy' with it, or the maximum is the ill-posed adiabatic-piston answer"
            )
        if len(channels) == len(CHANNELS):
            raise ValueError(
                "releasing energy, volume and particles together removes the wall entirely; "
                "the partition is then undetermined, not maximal"
            )
        share, _ = _maximise(self, channels, tolerance)
        return share

    def energy_scan(self, n_points: int = 401, margin: float = 1e-3
                    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """(U_A, S_A, S_B) along the energy partition, the other channels held where they are.

        The explorer's central picture: S_A rising, S_B falling, and their sum peaking where
        the two slopes agree. `margin` keeps both ends a hair inside (0, total) so neither
        side is left with exactly zero energy.
        """
        if n_points < 3:
            raise ValueError("a scan needs at least three points")
        total = self.total("energy")
        shares = np.linspace(margin, 1.0 - margin, n_points)
        u_a = shares * total
        u_b = total - u_a
        s_a = np.asarray(self.relation_a(u_a, np.full_like(u_a, self.a.volume),
                                         np.full_like(u_a, self.a.number)), dtype=float)
        s_b = np.asarray(self.relation_b(u_b, np.full_like(u_b, self.b.volume),
                                         np.full_like(u_b, self.b.number)), dtype=float)
        return u_a, s_a, s_b


_GOLDEN: Final[float] = (np.sqrt(5.0) - 1.0) / 2.0


def _golden_section(f: Callable[[float], tuple[float, Composite]], lo: float, hi: float,
                    tolerance: float) -> tuple[Composite, float]:
    """Maximise a unimodal f on [lo, hi]; f returns (value, the composite it evaluated)."""
    x1 = hi - _GOLDEN * (hi - lo)
    x2 = lo + _GOLDEN * (hi - lo)
    f1, c1 = f(x1)
    f2, c2 = f(x2)
    while hi - lo > tolerance:
        if f1 < f2:
            lo, x1, f1, c1 = x1, x2, f2, c2
            x2 = lo + _GOLDEN * (hi - lo)
            f2, c2 = f(x2)
        else:
            hi, x2, f2, c2 = x2, x1, f1, c1
            x1 = hi - _GOLDEN * (hi - lo)
            f1, c1 = f(x1)
    return (c1, f1) if f1 >= f2 else (c2, f2)


def _maximise(composite: Composite, channels: tuple[str, ...],
              tolerance: float) -> tuple[Composite, float]:
    """Nested golden-section search: the last channel innermost."""
    channel, rest = channels[0], channels[1:]
    edge = 1e-9

    def objective(share: float) -> tuple[float, Composite]:
        trial = composite.with_share(channel, share)
        if rest:
            best, value = _maximise(trial, rest, tolerance)
            return value, best
        return trial.total_entropy, trial

    best, value = _golden_section(objective, edge, 1.0 - edge, tolerance)
    return best, value


# ---------------------------------------------------------------------------
# Entropy production: the closed form for two bodies of constant heat capacity
# ---------------------------------------------------------------------------


def contact_entropy_production(c_a: float, t_a: float, c_b: float, t_b: float) -> float:
    """Delta S_total when two bodies of constant heat capacity reach a common temperature [J/K].

        Delta S_total = C_A ln(T_eq / T_A) + C_B ln(T_eq / T_B),
        T_eq = (C_A T_A + C_B T_B) / (C_A + C_B).

    Each term is the body's own reversible-path entropy change, C ln(T_2/T_1) from module 07.
    The sum is zero when T_A = T_B and strictly positive otherwise, because ln is strictly
    concave and T_eq is the heat-capacity-weighted average of the two starting temperatures
    (Jensen's inequality). No heat crosses the pair's outer boundary, so all of it is
    produced, none received.
    """
    if c_a <= 0 or c_b <= 0:
        raise ValueError("heat capacities must be positive")
    if t_a <= 0 or t_b <= 0:
        raise ValueError("temperatures must be positive")
    t_eq = (c_a * t_a + c_b * t_b) / (c_a + c_b)
    return float(c_a * np.log(t_eq / t_a) + c_b * np.log(t_eq / t_b))
