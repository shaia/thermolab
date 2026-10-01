"""Phase equilibrium of a van der Waals fluid: where the flat line goes, and why.

MODEL SPECIFICATION
    System:        one van der Waals fluid -- fixed N, constants a and b per particle --
                   described by (P, v, T), which below T_c splits into two homogeneous
                   phases, liquid and gas, that share T, P and the chemical potential mu
    Dynamics:      none -- every function solves equilibrium conditions
    Boundary:      closed to matter; T (and, where asked, the total v or the pressure) is set
                   from outside, and the saturation pressure and the two coexisting volumes
                   are solved for
    Ensemble:      not applicable -- macroscopic thermodynamics on a mean-field equation of
                   state
    Ignored:       interfaces and surface tension (the two phases meet at no cost),
                   nucleation kinetics (how long a metastable state survives), any solid
                   phase, and fluctuations near the critical point
    Valid when:    0 < T < T_c for the construction routines, which are tested up to
                   T = T_RATIO_MAX * T_c; metastable branches are statements of existence,
                   not of lifetime
    Failure modes: T -> T_c, where the three roots of the isotherm coalesce and the equal-area
                   residual loses its contrast (see CONDITIONING below); T >= T_c, where
                   there is no coexistence and `maxwell_construction` raises; the exponents
                   near T_c, which mean-field theory gets wrong (module 15); and there is no
                   triple point, because the model has no solid

THE ONE EQUATION
    At fixed T, module 09's Gibbs-Duhem relation reads d mu = v dP per particle. Integrated
    along the model isotherm from the liquid state to the gas state,

        mu_g - mu_l = integral of v dP = P_sat (v_g - v_l) - integral of P(v) dv,

    so equal chemical potentials -- module 13's condition for two phases that exchange
    particles -- is the same statement as "the chord at P_sat cuts the loop into two lobes
    of equal area". `maxwell_construction` solves the second form, `coexistence_from_mu`
    the first, and the test suite checks that they agree to rounding. Neither is a drawing
    rule: both are mu equality.

WHY REDUCED VARIABLES
    Every van der Waals fluid obeys the same equation once P, v and T are measured in units
    of its own critical point (module 02's law of corresponding states),

        P_r = 8 T_r / (3 v_r - 1) - 3 / v_r^2 ,

    so the coexistence curve is one universal curve, and a and b only scale the axes. All the
    solving here happens in reduced variables, where every quantity is of order one and the
    cubic's coefficients are well conditioned; the public functions scale the answer back.

CONDITIONING NEAR T_c
    Below T_c an isotherm crosses a horizontal line three times. As T -> T_c the three
    crossings coalesce: the coexisting volumes approach each other as (1 - T_r)^(1/2), and
    the loop's height, which is what the equal-area residual measures, shrinks as
    (1 - T_r)^(3/2). The cubic is solved in closed form (the trigonometric method, exact for
    three real roots), the lobe areas use the exact antiderivative rather than a quadrature,
    and the bisection is on log P, so what limits the solver is the contrast of the residual
    in double precision. `T_RATIO_MAX` records how close to T_c the tests hold the solver to
    its tolerance; beyond it `maxwell_construction` raises rather than returning noise, and
    `coexistence_curve` reports NaN there while pinning T = T_c itself to the critical point.

    Nothing here takes a random generator: the whole module is deterministic root-finding.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import numpy as np

from .constants import K_B
from .gases import vdw_critical_point

#: The solver's documented domain, as a fraction of T_c. See CONDITIONING in the docstring.
T_RATIO_MAX: Final[float] = 0.99999

#: Lowest reduced temperature the coexistence routines accept. P_sat / P_c is 3e-12 at
#: T_r = 0.3 and falls roughly as exp(-c / T_r); well below this the saturation pressure
#: is too small a number to carry the bisection's bracket.
T_RATIO_MIN: Final[float] = 0.3

_BISECT_MAX_ITER: Final[int] = 300
_BISECT_RTOL: Final[float] = 4.0 * np.finfo(float).eps
_P_FLOOR: Final[float] = 1e-14  # of the loop's maximum, when the loop's minimum is negative


def _output(value) -> float | np.ndarray:
    value = np.asarray(value, dtype=float)
    return float(value) if value.ndim == 0 else value


def _critical(a: float, b: float) -> tuple[float, float, float]:
    """(v_c, T_c, P_c), and the checks on a and b that go with them."""
    return vdw_critical_point(a, b)


def _reduced_temperature(temperature, a: float, b: float, allow_critical: bool = False):
    """T / T_c as an array, having checked that coexistence exists at every entry."""
    _, t_c, _ = _critical(a, b)
    t_r = np.asarray(temperature, dtype=float) / t_c
    if np.any(t_r <= 0):
        raise ValueError("temperature must be positive")
    if np.any(t_r >= 1.0) and not allow_critical:
        raise ValueError("no coexistence at or above the critical temperature")
    if np.any(t_r > T_RATIO_MAX) and not allow_critical:
        raise ValueError(f"the construction is only trusted up to T = {T_RATIO_MAX} T_c: "
                         "closer to T_c the three roots coalesce and the residual is noise")
    if np.any(t_r < T_RATIO_MIN):
        raise ValueError(f"the construction needs T >= {T_RATIO_MIN} T_c: below it P_sat "
                         "underflows the pressure's double precision")
    return t_r


# ---------------------------------------------------------------------------
# The reduced equation of state and its cubic
# ---------------------------------------------------------------------------


def _p_r(v_r, t_r):
    """P_r = 8 T_r / (3 v_r - 1) - 3 / v_r^2."""
    return 8.0 * t_r / (3.0 * v_r - 1.0) - 3.0 / v_r**2


def _antiderivative_r(v_r, t_r):
    """The integral of P_r dv_r: (8 T_r / 3) ln(3 v_r - 1) + 3 / v_r."""
    return (8.0 * t_r / 3.0) * np.log(3.0 * v_r - 1.0) + 3.0 / v_r


def _mu_r(v_r, t_r):
    """mu / (P_c v_c) up to a function of T alone: -(8T/3) ln(3v-1) + (8T/3)/(3v-1) - 6/v.

    The SI form is `vdw_chemical_potential`; this is the same expression with
    k_B T = (8/3) P_c v_c T_r, b/(v - b) = 1/(3 v_r - 1) and 2a/v = 6 P_c v_c / v_r.
    """
    return (-(8.0 * t_r / 3.0) * np.log(3.0 * v_r - 1.0) + (8.0 * t_r / 3.0) / (3.0 * v_r - 1.0)
            - 6.0 / v_r)


def _real_cubic_roots(a2, a1, a0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Real roots of x^3 + a2 x^2 + a1 x + a0 = 0, vectorised: (lowest, middle, highest).

    Three real roots come from the trigonometric form of Cardano's solution, which is exact
    in exact arithmetic and loses nothing when the roots are close -- the eigenvalue route
    `numpy.roots` takes is not vectorised and is worse conditioned at a near-double root.
    With one real root the middle and highest slots are NaN and the root sits in the lowest.
    """
    a2, a1, a0 = np.broadcast_arrays(*(np.asarray(x, dtype=float) for x in (a2, a1, a0)))
    p = a1 - a2**2 / 3.0
    q = 2.0 * a2**3 / 27.0 - a2 * a1 / 3.0 + a0
    shift = -a2 / 3.0
    discriminant = -(4.0 * p**3 + 27.0 * q**2)
    three = discriminant >= 0.0

    low = np.full(p.shape, np.nan)
    mid = np.full(p.shape, np.nan)
    high = np.full(p.shape, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        # Three real roots (p < 0 there): 2 sqrt(-p/3) cos(theta - 2 pi k / 3).
        amplitude = 2.0 * np.sqrt(np.maximum(-p, 0.0) / 3.0)
        cos_arg = np.clip(1.5 * q / p * np.sqrt(-3.0 / np.where(p < 0, p, -1.0)), -1.0, 1.0)
        theta = np.arccos(cos_arg) / 3.0
        r_high = amplitude * np.cos(theta)
        r_mid = amplitude * np.cos(theta - 2.0 * np.pi / 3.0)
        r_low = amplitude * np.cos(theta - 4.0 * np.pi / 3.0)
        # One real root: the hyperbolic forms, one for each sign of p.
        neg = p < 0
        p_neg = np.where(neg, p, -1.0)
        cosh_arg = -1.5 * np.abs(q) / p_neg * np.sqrt(-3.0 / p_neg)
        r_one_neg = (-2.0 * np.sign(q) * np.sqrt(np.maximum(-p, 0.0) / 3.0)
                     * np.cosh(np.arccosh(np.maximum(cosh_arg, 1.0)) / 3.0))
        pos = p > 0
        sinh_arg = 1.5 * q / np.where(pos, p, 1.0) * np.sqrt(3.0 / np.where(pos, p, 1.0))
        r_one_pos = -2.0 * np.sqrt(np.maximum(p, 0.0) / 3.0) * np.sinh(np.arcsinh(sinh_arg) / 3.0)
        r_one = np.where(neg, r_one_neg, np.where(pos, r_one_pos, -np.cbrt(q)))

    low = np.where(three, r_low, r_one) + shift
    mid = np.where(three, r_mid + shift, np.nan)
    high = np.where(three, r_high + shift, np.nan)
    return low, mid, high


_VOLUME_MAX_ITER: Final[int] = 120
# The liquid bracket starts just inside the excluded volume, where P_r is about 8 T_r / 1e-9:
# larger than any pressure a root is ever asked for.
_V_FLOOR: Final[float] = (1.0 / 3.0) * (1.0 + 1e-9)


def _bisect_volume(p_r, t_r, lo, hi, increasing: bool) -> np.ndarray:
    """v_r with P_r(v_r, T_r) = p_r on [lo, hi], where P_r is monotone; bisection in log v.

    Bisection, not the cubic's closed form: the closed form writes every root as a large
    shift plus a cosine, and when the pressure is tiny (a low-temperature saturation pressure
    is 1e-12 P_c) the small liquid root is the difference of two numbers near 1e12 and
    comes out as noise. A bracket whose ends are known to straddle the root cannot do that,
    and the brackets are known: the spinodal volumes, where the slope changes sign.
    """
    lo = np.array(lo, dtype=float)
    hi = np.array(hi, dtype=float)
    lo, hi = np.broadcast_arrays(lo, hi)
    lo, hi = lo.copy(), hi.copy()
    for _ in range(_VOLUME_MAX_ITER):
        mid = np.sqrt(lo * hi)
        with np.errstate(invalid="ignore", divide="ignore"):
            f = _p_r(mid, t_r) - p_r
            root_is_above = (f < 0.0) if increasing else (f > 0.0)
        lo = np.where(root_is_above, mid, lo)
        hi = np.where(root_is_above, hi, mid)
        if np.all(hi - lo <= _BISECT_RTOL * hi):
            break
    return 0.5 * (lo + hi)


def _isotherm_roots_r(p_r, t_r) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """v_r where P_r(v_r, T_r) = p_r, as (lowest, middle, highest), NaN where absent.

    Below T_c the isotherm falls from +infinity to its minimum at the liquid spinodal, rises
    to its maximum at the gas spinodal, and falls again toward zero, so a pressure between
    the two extremes is crossed three times and each crossing is bracketed by the spinodal
    volumes. A pressure outside that range is crossed once, on the liquid side above the
    maximum or the gas side below the minimum, and so is any pressure at or above T_c, where
    there are no spinodals; that single root is returned in the first slot. The gas-side
    bracket ends at (8 T_r / p_r + 1) / 3, above which P_r < 8 T_r / (3 v_r - 1) < p_r.
    """
    p_r, t_r = np.broadcast_arrays(np.asarray(p_r, dtype=float), np.asarray(t_r, dtype=float))
    v_top = (8.0 * t_r / p_r + 1.0) / 3.0
    sub = t_r < 1.0
    with np.errstate(invalid="ignore", divide="ignore"):
        v_min, v_max = _spinodal_volumes_r(np.where(sub, t_r, 0.5))
        p_min, p_max = _p_r(v_min, t_r), _p_r(v_max, t_r)
    three = sub & (p_r > p_min) & (p_r < p_max)
    liquid_only = ~three & (~sub | (p_r >= p_max))

    low = _bisect_volume(p_r, t_r, _V_FLOOR, np.where(three, v_min, v_top), increasing=False)
    high = _bisect_volume(p_r, t_r, np.where(sub, v_max, _V_FLOOR), v_top, increasing=False)
    mid = _bisect_volume(p_r, t_r, np.where(sub, v_min, _V_FLOOR),
                         np.where(sub, v_max, v_top), increasing=True)
    lowest = np.where(three | liquid_only, low, high)
    middle = np.where(three, mid, np.nan)
    highest = np.where(three, high, np.nan)
    return lowest, middle, highest


def _spinodal_volumes_r(t_r) -> tuple[np.ndarray, np.ndarray]:
    """(v_r at the loop's minimum, v_r at its maximum): dP_r/dv_r = 0 below T_c.

    dP/dv = 0 is 4 T_r v^3 - 9 v^2 + 6 v - 1 = 0, a cubic whose smallest root lies below
    v_r = 1/3 (inside the excluded volume) and whose other two are the spinodal volumes.
    """
    t_r = np.asarray(t_r, dtype=float)
    _, v_min, v_max = _real_cubic_roots(-9.0 / (4.0 * t_r), 6.0 / (4.0 * t_r), -1.0 / (4.0 * t_r))
    return v_min, v_max


def _bisect_on_pressure(t_r, residual) -> np.ndarray:
    """Log-bisection on p_r between the two spinodal pressures for `residual(p_r, t_r) = 0`.

    `residual` must be positive when p_r is below the solution and negative above it. The
    lower end of the bracket is the loop's minimum pressure, or a tiny positive pressure
    when that minimum is negative -- which it is below T_r = 27/32: a negative pressure is a
    stretched liquid, not a bracket end for a saturation pressure.
    """
    v_min, v_max = _spinodal_volumes_r(t_r)
    hi = _p_r(v_max, t_r)
    lo = np.maximum(_p_r(v_min, t_r), _P_FLOOR * hi)
    for _ in range(_BISECT_MAX_ITER):
        mid = np.sqrt(lo * hi)
        with np.errstate(invalid="ignore", divide="ignore"):
            below = residual(mid, t_r) > 0.0
        lo = np.where(below, mid, lo)
        hi = np.where(below, hi, mid)
        if np.all(hi - lo <= _BISECT_RTOL * hi):
            break
    return 0.5 * (lo + hi)


def _equal_area_residual(p_r, t_r) -> np.ndarray:
    """Integral of P_r dv_r from v_l to v_g, minus p_r (v_g - v_l): right lobe minus left lobe."""
    v_l, _, v_g = _isotherm_roots_r(p_r, t_r)
    return (_antiderivative_r(v_g, t_r) - _antiderivative_r(v_l, t_r)) - p_r * (v_g - v_l)


def _equal_mu_residual(p_r, t_r) -> np.ndarray:
    """mu_l - mu_g along the isotherm at pressure p_r: positive below P_sat, negative above."""
    v_l, _, v_g = _isotherm_roots_r(p_r, t_r)
    return _mu_r(v_l, t_r) - _mu_r(v_g, t_r)


def _reduced_coexistence(t_r, residual=_equal_area_residual
                         ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(p_r_sat, v_r_liq, v_r_gas) at every reduced temperature in `t_r`, all below one."""
    t_r = np.asarray(t_r, dtype=float)
    p_sat = _bisect_on_pressure(t_r, residual)
    v_l, _, v_g = _isotherm_roots_r(p_sat, t_r)
    return p_sat, v_l, v_g


# ---------------------------------------------------------------------------
# Public: the isotherm's anatomy
# ---------------------------------------------------------------------------


def vdw_chemical_potential(v, temperature, a: float, b: float):
    """mu(v, T) [J] of a van der Waals fluid, up to an additive function of T alone.

        mu = -k_B T ln((v - b) / b) + k_B T b / (v - b) - 2 a / v .

    It is the Helmholtz free energy per particle plus P v, with the term -k_B T ln(n_Q b)
    that fixes the absolute scale left out: at fixed T it is a constant, and nothing in this
    module compares chemical potentials at different temperatures. Its v-derivative is
    v dP/dv, which is Gibbs-Duhem at fixed T, so mu(P) along a sub-critical isotherm traces
    a loop that crosses itself at exactly P_sat.
    """
    if a <= 0 or b <= 0:
        raise ValueError("a and b must be positive")
    v = np.asarray(v, dtype=float)
    t = np.asarray(temperature, dtype=float)
    if np.any(v <= b):
        raise ValueError(f"per-particle volume must exceed the excluded volume b = {b:.6e} m^3")
    kt = K_B * t
    return _output(-kt * np.log((v - b) / b) + kt * b / (v - b) - 2.0 * a / v)


def spinodal_volumes(temperature, a: float, b: float):
    """(v at the loop's minimum, v at its maximum) [m^3] -- where (dP/dv)_T changes sign.

    Between them the isotherm has (dP/dv)_T > 0, which module 09's stability criterion
    forbids. On the liquid side of the minimum and the gas side of the maximum the slope is
    negative again, but the state may still be metastable: that is `maxwell_construction`'s
    business. Vectorised over `temperature`; raises at or above T_c, where the two coincide.
    """
    t_r = _reduced_temperature(temperature, a, b)
    v_c, _, _ = _critical(a, b)
    v_min, v_max = _spinodal_volumes_r(t_r)
    return _output(v_c * v_min), _output(v_c * v_max)


def spinodal_curve(a: float, b: float, n_points: int = 200, t_min: float = 0.5
                   ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(temperature, v, pressure) along the spinodal, liquid branch up to T_c and gas branch down.

    The locus of (dP/dv)_T = 0, as one closed arc in the P-v plane ending where it started
    in temperature. `t_min` is the lowest T / T_c drawn; the liquid branch's pressure goes
    negative below T_r = 27/32, which is physical (a stretched liquid) but ugly on a plot.
    """
    if n_points < 2:
        raise ValueError("n_points must be at least 2")
    if not 0.0 < t_min < 1.0:
        raise ValueError("t_min must lie in (0, 1)")
    v_c, t_c, p_c = _critical(a, b)
    t_r = np.linspace(t_min, 1.0, n_points)
    v_min, v_max = _spinodal_volumes_r(t_r)
    v_r = np.concatenate([v_min, v_max[::-1]])
    t_both = np.concatenate([t_r, t_r[::-1]])
    return t_c * t_both, v_c * v_r, p_c * _p_r(v_r, t_both)


def isotherm_volumes(pressure, temperature, a: float, b: float
                     ) -> tuple[float | np.ndarray, float | np.ndarray, float | np.ndarray]:
    """(v_low, v_mid, v_high) [m^3]: every v at which the isotherm passes through `pressure`.

    Three values where the horizontal line cuts the loop three times; otherwise the single
    crossing sits in the first slot and the other two are NaN. The outer pair are the
    candidate liquid and gas; the middle one has (dP/dv)_T > 0 and is never a state.
    """
    v_c, t_c, p_c = _critical(a, b)
    p = np.asarray(pressure, dtype=float)
    t = np.asarray(temperature, dtype=float)
    if np.any(p <= 0) or np.any(t <= 0):
        raise ValueError("pressure and temperature must be positive")
    low, mid, high = _isotherm_roots_r(p / p_c, t / t_c)
    return _output(v_c * low), _output(v_c * mid), _output(v_c * high)


# ---------------------------------------------------------------------------
# Public: coexistence
# ---------------------------------------------------------------------------


def maxwell_construction(temperature, a: float, b: float
                         ) -> tuple[float | np.ndarray, float | np.ndarray, float | np.ndarray]:
    """(P_sat, v_liq, v_gas) [Pa, m^3, m^3] at `temperature`, by the equal-area condition.

    The pressure is bisected between the loop's minimum and maximum until the two lobes cut
    off by the chord have equal area -- which, by the module docstring's one equation, is
    mu_liq = mu_gas. Vectorised over `temperature`. Raises at or above T_c, above
    `T_RATIO_MAX` T_c, and below `T_RATIO_MIN` T_c.
    """
    t_r = _reduced_temperature(temperature, a, b)
    v_c, _, p_c = _critical(a, b)
    p_sat, v_l, v_g = _reduced_coexistence(t_r, _equal_area_residual)
    return _output(p_c * p_sat), _output(v_c * v_l), _output(v_c * v_g)


def coexistence_from_mu(temperature, a: float, b: float
                        ) -> tuple[float | np.ndarray, float | np.ndarray, float | np.ndarray]:
    """(P_sat, v_liq, v_gas) by bisecting mu_liq(P) = mu_gas(P) directly, with no areas at all.

    The same answer as `maxwell_construction`, reached from the other side of the theorem:
    the chemical potential of each outer root of the isotherm is evaluated with
    `vdw_chemical_potential`, and the pressure at which they agree is found. The two routes
    agreeing to rounding is the test suite's check that equal areas *is* equal mu.
    """
    t_r = _reduced_temperature(temperature, a, b)
    v_c, _, p_c = _critical(a, b)
    p_sat, v_l, v_g = _reduced_coexistence(t_r, _equal_mu_residual)
    return _output(p_c * p_sat), _output(v_c * v_l), _output(v_c * v_g)


def coexistence_curve(temperatures, a: float, b: float
                      ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(P_sat, v_liq, v_gas) arrays over a grid of temperatures: the binodal and the P-T curve.

    Entries above T_c are NaN -- there is nothing to coexist -- and so are those between
    `T_RATIO_MAX` T_c and T_c, where the solver is not trusted. A grid point at exactly T_c
    is pinned to the critical point (P_c, v_c, v_c), where the curve ends.
    """
    v_c, t_c, p_c = _critical(a, b)
    t = np.asarray(temperatures, dtype=float)
    if t.ndim != 1:
        raise ValueError("temperatures must be a 1-D array")
    p_sat = np.full(t.shape, np.nan)
    v_liq = np.full(t.shape, np.nan)
    v_gas = np.full(t.shape, np.nan)
    t_r = t / t_c
    inside = (t_r >= T_RATIO_MIN) & (t_r <= T_RATIO_MAX)
    if np.any(inside):
        p_in, l_in, g_in = _reduced_coexistence(t_r[inside], _equal_area_residual)
        p_sat[inside], v_liq[inside], v_gas[inside] = p_c * p_in, v_c * l_in, v_c * g_in
    critical = t_r == 1.0
    p_sat[critical], v_liq[critical], v_gas[critical] = p_c, v_c, v_c
    return p_sat, v_liq, v_gas


def equilibrium_volume(pressure, temperature, a: float, b: float):
    """The stable per-particle volume [m^3] at (P, T): the phase with the lower mu.

    Above T_c the isotherm crosses `pressure` once and that is the answer. Below T_c, where
    it crosses three times, the outer two are compared by `vdw_chemical_potential` and the
    lower wins -- liquid above P_sat, gas below it, so v(P) jumps at exactly the saturation
    pressure. The branch that loses is the metastable one; this function never returns it.
    Vectorised over both arguments.
    """
    v_c, t_c, p_c = _critical(a, b)
    p_r = np.asarray(pressure, dtype=float) / p_c
    t_r = np.asarray(temperature, dtype=float) / t_c
    if np.any(p_r <= 0) or np.any(t_r <= 0):
        raise ValueError("pressure and temperature must be positive")
    low, _, high = _isotherm_roots_r(p_r, t_r)
    with np.errstate(invalid="ignore"):
        gas_wins = _mu_r(high, t_r) < _mu_r(low, t_r)
    chosen = np.where(np.isnan(high), low, np.where(gas_wins, high, low))
    return _output(v_c * chosen)


def lever_rule(v, v_liq, v_gas) -> tuple[float | np.ndarray, float | np.ndarray]:
    """(x_liq, x_gas): the phase fractions of a mixed state with mean volume per particle `v`.

    From v = x_l v_l + x_g v_g and x_l + x_g = 1: x_g = (v - v_l) / (v_g - v_l). Raises
    for a `v` outside [v_liq, v_gas], which is a single phase and not a mixture.
    """
    v = np.asarray(v, dtype=float)
    v_l = np.asarray(v_liq, dtype=float)
    v_g = np.asarray(v_gas, dtype=float)
    if np.any(v_g <= v_l):
        raise ValueError("v_gas must exceed v_liq")
    if np.any(v < v_l) or np.any(v > v_g):
        raise ValueError("v must lie between v_liq and v_gas to be a mixture of the two")
    x_gas = (v - v_l) / (v_g - v_l)
    return _output(1.0 - x_gas), _output(x_gas)


# ---------------------------------------------------------------------------
# Public: latent heat and Clausius-Clapeyron
# ---------------------------------------------------------------------------


def latent_heat(temperature, a: float, b: float):
    """L = T (s_gas - s_liq) = k_B T ln((v_gas - b) / (v_liq - b)) [J per particle].

    The van der Waals entropy per particle is k_B [ln((v - b) n_Q) + 5/2], so at one
    temperature the two phases differ only through their free volumes v - b. L vanishes as
    T -> T_c, where the two volumes merge: there is nothing left to boil.
    """
    t_r = _reduced_temperature(temperature, a, b)
    _, v_l, v_g = _reduced_coexistence(t_r, _equal_area_residual)
    _, t_c, _ = _critical(a, b)
    kt = K_B * t_c * t_r
    return _output(kt * np.log((3.0 * v_g - 1.0) / (3.0 * v_l - 1.0)))


def latent_heat_from_first_law(temperature, a: float, b: float):
    """L = Delta u + P_sat Delta v [J per particle]: the heat of the isobaric, isothermal crossing.

    With dU = delta Q + delta W_on and delta W_on = -P dV along the flat line,
    delta Q = dU + P dV, so the heat to carry one particle from liquid to gas is
    (u_g - u_l) + P_sat (v_g - v_l), with u = (3/2) k_B T - a / v for the van der Waals gas
    and the kinetic part cancelling at one temperature. It equals `latent_heat` exactly when
    mu_liq = mu_gas -- the two routes are the same theorem -- and the laboratory checks it.
    """
    p_sat, v_l, v_g = maxwell_construction(temperature, a, b)
    delta_u = a * (1.0 / np.asarray(v_l) - 1.0 / np.asarray(v_g))
    return _output(delta_u + np.asarray(p_sat) * (np.asarray(v_g) - np.asarray(v_l)))


def clausius_clapeyron_check(temperature: float, a: float, b: float, dt: float = 1e-3
                             ) -> tuple[float, float]:
    """(dP_sat/dT by central difference, L / (T Delta v)) [Pa/K] at one temperature.

    Clausius-Clapeyron says the two are equal. `dt` is the half-step in kelvin; the
    difference is second order in it, and the test suite measures that order.
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    t = float(temperature)
    p_up, _, _ = maxwell_construction(t + dt, a, b)
    p_down, _, _ = maxwell_construction(t - dt, a, b)
    numeric = (p_up - p_down) / (2.0 * dt)
    _, v_l, v_g = maxwell_construction(t, a, b)
    predicted = latent_heat(t, a, b) / (t * (v_g - v_l))
    return float(numeric), float(predicted)


@dataclass(frozen=True)
class SaturationFit:
    """ln P_sat = log_prefactor - L / (k_B T) fitted to data: Clausius-Clapeyron, ideal vapour.

    `latent_heat` is per particle [J], with its standard error from the fit's covariance;
    `residuals` are ln(P_data) - ln(P_fit), the record of what a constant L and an ideal
    vapour miss.
    """

    latent_heat: float
    latent_heat_error: float
    log_prefactor: float
    log_prefactor_error: float
    residuals: np.ndarray

    def pressure(self, temperature):
        """The fitted P_sat(T) [Pa]."""
        t = np.asarray(temperature, dtype=float)
        return _output(np.exp(self.log_prefactor - self.latent_heat / (K_B * t)))

    def boiling_temperature(self, pressure):
        """The T [K] at which the fitted P_sat equals `pressure`: where a liquid boils."""
        p = np.asarray(pressure, dtype=float)
        if np.any(p <= 0):
            raise ValueError("pressure must be positive")
        return _output(self.latent_heat / (K_B * (self.log_prefactor - np.log(p))))


def clausius_clapeyron_fit(temperatures, pressures) -> SaturationFit:
    """Fit ln P_sat against 1/T, the integrated Clausius-Clapeyron equation for an ideal vapour.

    With v_gas >> v_liq and the vapour ideal, dP/dT = L P / (k_B T^2), so
    ln P = const - L / (k_B T) if L is constant: a straight line whose slope is -L / k_B. The
    fit is weighted equally in ln P, and its covariance gives the error on L. Both
    approximations bias the answer, and the residuals show it.
    """
    t = np.asarray(temperatures, dtype=float)
    p = np.asarray(pressures, dtype=float)
    if t.shape != p.shape or t.ndim != 1 or len(t) < 3:
        raise ValueError("temperatures and pressures must be matching 1-D arrays of 3+ points")
    if np.any(t <= 0) or np.any(p <= 0):
        raise ValueError("temperatures and pressures must be positive")
    x, y = 1.0 / t, np.log(p)
    (slope, intercept), cov = np.polyfit(x, y, 1, cov=True)
    return SaturationFit(latent_heat=float(-slope * K_B),
                         latent_heat_error=float(np.sqrt(cov[0, 0]) * K_B),
                         log_prefactor=float(intercept),
                         log_prefactor_error=float(np.sqrt(cov[1, 1])),
                         residuals=y - (intercept + slope * x))


def phase_rule(components: int, phases: int) -> int:
    """F = C - P + 2: the number of intensive variables free to vary with P phases coexisting.

    Each phase has C - 1 independent composition variables, plus T and P shared by all:
    P (C - 1) + 2 knobs. Each of the C species must have the same chemical potential in
    every phase: C (P - 1) constraints. The difference is F.
    """
    if components < 1 or phases < 1:
        raise ValueError("components and phases must be positive")
    freedom = components - phases + 2
    if freedom < 0:
        raise ValueError(f"{phases} phases of {components} component(s) cannot coexist")
    return freedom
