"""Thermal radiation and the heat capacity of solids: one quantum rule, two rescues.

MODEL SPECIFICATION
    System:        the electromagnetic field in a cavity of volume V, as independent
                   standing-wave modes; and a crystal of N atoms, as 3N independent
                   oscillators -- all at one frequency (Einstein) or spread over the
                   sound-wave spectrum, cut off at 3N modes (Debye). Every mode's energy comes
                   in whole quanta of h nu = hbar omega
    Dynamics:      none -- equilibrium averages, in closed form or by fixed quadrature; the
                   only random numbers anywhere are the noise `synthetic_heat_capacity` adds,
                   through a passed generator
    Boundary:      walls (or, for a crystal, the rest of the lattice) at temperature T act as
                   a heat bath for every mode; the cavity's walls reflect perfectly
    Ensemble:      canonical, mode by mode -- module 12's oscillator; the number of photons
                   is not conserved, so it carries no chemical potential (mu = 0)
    Ignored:       zero-point energy (a constant shift, invisible to C and to the spectrum);
                   photon-photon interaction; emissivity below 1; real phonon dispersion;
                   anharmonicity and thermal expansion (the difference C_P - C_V); the heat
                   capacity of a metal's conduction electrons
    Valid when:    the cavity is large compared with the thermal wavelength h c / (k_B T), so
                   that its modes form a continuum; the crystal is harmonic, and warm enough
                   that the electrons' gamma T is negligible beside the lattice term
    Failure modes: tiny or ultracold cavities, where single modes show; light that is not
                   thermal (lasers, LEDs, fluorescent tubes); metals below a few kelvin, where
                   gamma T dominates; crystals approaching melting, where anharmonicity adds
                   to C

THE ONE IDEA
    Module 12 summed one oscillator's Boltzmann factors. Measured from the ground state, its
    mean energy is hbar omega / (exp(hbar omega / k_B T) - 1): k_B T when the quantum is
    cheap, exponentially nothing when it is dear. Equipartition hands every mode k_B T
    regardless, which is why it predicts infinite radiation (a cavity has infinitely many
    modes) and a heat capacity 3 N k_B that never falls (a crystal's modes never stop being
    counted). `mode_occupation` is that one line, and everything else in this module is it
    summed over a list of modes: the cavity's (Planck), a single frequency (Einstein), or a
    sound spectrum (Debye). `planck_u_nu` is literally modes per unit volume times mean
    energy per mode, so the derivation and the code are the same product.

TWO SPECTRAL VARIABLES
    A spectral density is energy per unit of something. Per unit frequency and per unit
    wavelength are different densities of the same energy, related by the Jacobian
    u_lambda = u_nu |d nu / d lambda| = u_nu c / lambda^2, and that factor moves the peak.
    `planck_u_lambda` is written as `planck_u_nu` times the Jacobian, so the change of
    variables is code, not a second formula that could drift from the first. The peaks of
    the two curves fall at different photons: nu_max lambda_max = 0.568 c, never c.

THE CONSTANTS
    h comes from `fundamental.PLANCK_H` and hbar from `partition.H_BAR`; `constants` is
    consumed by this course and never extended. The speed of light is defined here, exact by
    the SI definition of the metre. The Wien roots are solved at import by Newton's method,
    so the 2.821 and 4.965 that the page quotes are computed, not typed.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

import numpy as np

from .constants import K_B
from .fundamental import PLANCK_H
from .partition import H_BAR, harmonic_heat_capacity

#: Speed of light in vacuum [m/s] (exact, by the SI definition of the metre).
C_LIGHT: Final[float] = 299_792_458.0

#: Apery's constant zeta(3) = sum 1/n^3, which sets the photon number density.
ZETA_3: Final[float] = 1.2020569031595942

#: Upper limit, in units of k_B T, of the spectral integrals. The integrand's tail past it is
#: x^3 e^-x at x = 50, a fraction 4e-18 of the whole: below double precision.
SPECTRUM_X_MAX: Final[float] = 50.0

#: Upper limit of the Debye integral. Past x = 60 its integrand x^4 e^-x is below 1e-19 of
#: the total, so a colder crystal (theta_D / T > 60) integrates [0, 60] and loses nothing.
DEBYE_X_MAX: Final[float] = 60.0


def wien_root(power: int) -> float:
    """The positive root of x = power (1 - e^-x), by Newton's method.

    Setting the derivative of x^power / (e^x - 1) to zero gives this equation. power = 3 is
    the peak of the frequency spectrum u_nu (x = h nu / k_B T), power = 5 the peak of the
    wavelength spectrum u_lambda (x = h c / (lambda k_B T)). Starting from x = power, the
    iteration converges in about five steps.
    """
    if power <= 1:
        raise ValueError("power must exceed 1 for a positive root to exist")
    x = float(power)
    for _ in range(50):
        step = (x - power * (1.0 - math.exp(-x))) / (1.0 - power * math.exp(-x))
        x -= step
        if abs(step) < 1e-15 * x:
            return x
    raise RuntimeError("Newton's method did not converge")  # pragma: no cover


#: x at the peak of u_nu: nu_max = 2.821 k_B T / h.
WIEN_X_NU: Final[float] = wien_root(3)

#: x at the peak of u_lambda: lambda_max = h c / (4.965 k_B T).
WIEN_X_LAMBDA: Final[float] = wien_root(5)

#: Wien's displacement constant b = lambda_max T [m K].
WIEN_B: Final[float] = PLANCK_H * C_LIGHT / (WIEN_X_LAMBDA * K_B)

#: nu_max lambda_max / c = 2.821 / 4.965 = 0.568: the two peaks are different photons.
DUAL_PEAK_RATIO: Final[float] = WIEN_X_NU / WIEN_X_LAMBDA

#: Radiation constant a in u = a T^4 [J m^-3 K^-4]: 8 pi^5 k_B^4 / (15 h^3 c^3).
RADIATION_CONSTANT: Final[float] = 8.0 * math.pi**5 * K_B**4 / (
    15.0 * PLANCK_H**3 * C_LIGHT**3)

#: Stefan-Boltzmann constant sigma = a c / 4 [W m^-2 K^-4]: the flux out of a hole.
STEFAN_BOLTZMANN: Final[float] = RADIATION_CONSTANT * C_LIGHT / 4.0


def _positive(name: str, value) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if np.any(array <= 0):
        raise ValueError(f"{name} must be positive")
    return array


def _non_negative(name: str, value) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    if np.any(array < 0):
        raise ValueError(f"{name} must be non-negative")
    return array


def _as_float_or_array(value):
    return float(value) if np.ndim(value) == 0 else value


def simpson(values, grid) -> float:
    """Composite Simpson integral of `values` sampled on a uniform `grid`.

    The grid must hold an odd number of points (an even number of intervals). The error falls
    as the fourth power of the spacing for a smooth integrand -- the order the convergence
    tests measure.
    """
    y = np.asarray(values, dtype=float)
    x = np.asarray(grid, dtype=float)
    if y.shape != x.shape or y.ndim != 1:
        raise ValueError("values and grid must be one-dimensional and of one length")
    if len(x) < 3 or len(x) % 2 == 0:
        raise ValueError("Simpson's rule needs an odd number of points, at least three")
    h = (x[-1] - x[0]) / (len(x) - 1)
    return float(h / 3.0 * (y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-1:2].sum()))


# ---------------------------------------------------------------------------
# One mode
# ---------------------------------------------------------------------------


def mode_occupation(quantum, temperature):
    """Mean number of quanta in one mode, <n> = 1 / (exp(quantum / (k_B T)) - 1).

    `quantum` is the energy of one quantum, hbar omega = h nu [J]. This is module 12's
    oscillator, -d ln Z / d beta divided by the quantum and measured from the ground state.
    Written as e^-x / (1 - e^-x), which is exact for small x and underflows quietly to zero
    for large x instead of overflowing. Dimensionless.
    """
    x = _positive("quantum", quantum) / (K_B * _positive("temperature", temperature))
    return _as_float_or_array(np.exp(-x) / -np.expm1(-x))


def mean_mode_energy(nu, temperature):
    """Mean energy of one mode of frequency nu above its ground state, h nu <n> [J].

    k_B T when h nu << k_B T -- equipartition -- and h nu exp(-h nu / k_B T) when h nu >> k_B T.
    At nu = 0 it returns the limit, k_B T, so that spectra can be sampled from zero.
    """
    nu = _non_negative("nu", nu)
    t = _positive("temperature", temperature)
    quantum = PLANCK_H * nu
    x = quantum / (K_B * t)
    with np.errstate(divide="ignore", invalid="ignore"):
        energy = np.where(x > 0, quantum * np.exp(-x) / -np.expm1(-x), K_B * t)
    return _as_float_or_array(energy)


# ---------------------------------------------------------------------------
# Counting the modes of a cavity
# ---------------------------------------------------------------------------


def mode_density(nu, volume: float = 1.0):
    """g(nu) = 8 pi V nu^2 / c^3: modes per unit frequency in a cavity of volume V [1/Hz].

    Two polarizations per wave vector, wave vectors filling the positive octant of k-space.
    With the default volume of one cubic metre, it is the number of modes per unit
    frequency per unit volume.
    """
    if volume <= 0:
        raise ValueError("volume must be positive")
    nu = _non_negative("nu", nu)
    return _as_float_or_array(8.0 * math.pi * volume * nu**2 / C_LIGHT**3)


def count_cavity_modes(side: float, nu_max: float) -> int:
    """Count the standing waves in a cube of side L with frequency at most nu_max, one by one.

    A standing wave between perfectly reflecting walls has k = (pi / L)(n_x, n_y, n_z) with
    every n a positive integer, and frequency nu = c |n| / (2 L). Each such wave vector
    carries two polarizations. This function enumerates the integer points explicitly -- no
    octant, no sphere, no continuum -- so that the smooth count (8 pi V / 3 c^3) nu^3 can be
    tested against the thing it approximates. Modes with an index equal to zero, which carry
    one polarization rather than two, lie on the octant's faces and are left out, as the
    smooth count leaves them out; they are a correction of relative order 1 / (L nu / c).
    """
    if side <= 0 or nu_max <= 0:
        raise ValueError("side and nu_max must be positive")
    radius = 2.0 * side * nu_max / C_LIGHT  # |n| at the cutoff frequency
    n_top = int(math.floor(radius))
    if n_top > 4000:
        raise ValueError("cutoff too high to enumerate; that many modes is a continuum")
    if n_top < 1:
        return 0
    n = np.arange(1, n_top + 1, dtype=float)
    remaining = radius**2 - n[:, None] ** 2 - n[None, :] ** 2
    nz = np.floor(np.sqrt(np.clip(remaining, 0.0, None)))
    return int(2 * nz[remaining >= 1.0].sum())


def mode_count_smooth(side: float, nu_max: float) -> float:
    """The continuum count N(nu) = (8 pi V / 3 c^3) nu^3 that `count_cavity_modes` tests."""
    if side <= 0 or nu_max <= 0:
        raise ValueError("side and nu_max must be positive")
    return 8.0 * math.pi * side**3 * nu_max**3 / (3.0 * C_LIGHT**3)


# ---------------------------------------------------------------------------
# The spectrum, in both variables
# ---------------------------------------------------------------------------


def planck_u_nu(nu, temperature):
    """Planck's law per unit frequency, u_nu = (8 pi h nu^3 / c^3) / (exp(h nu / k_B T) - 1).

    Built as modes per unit volume per unit frequency times mean energy per mode -- the
    derivation as a product. Units J s m^-3 (energy per unit volume per hertz).
    """
    return _as_float_or_array(mode_density(nu) * mean_mode_energy(nu, temperature))


def rayleigh_jeans_u_nu(nu, temperature):
    """The classical prediction u_nu = 8 pi nu^2 k_B T / c^3 [J s m^-3]: equipartition per mode.

    It agrees with Planck where h nu << k_B T and grows without bound at high frequency;
    its integral over all frequencies is infinite -- the ultraviolet catastrophe.
    """
    t = _positive("temperature", temperature)
    return _as_float_or_array(mode_density(nu) * K_B * t)


def planck_u_lambda(lam, temperature):
    """Planck's law per unit wavelength, u_lambda = u_nu |d nu / d lambda| [J m^-4].

    Evaluated as `planck_u_nu` at nu = c / lambda times the Jacobian c / lambda^2, which
    gives (8 pi h c / lambda^5) / (exp(h c / (lambda k_B T)) - 1).
    """
    lam = _positive("wavelength", lam)
    nu = C_LIGHT / lam
    return _as_float_or_array(planck_u_nu(nu, temperature) * C_LIGHT / lam**2)


def planck_radiance_nu(nu, temperature):
    """Spectral radiance B_nu = (c / 4 pi) u_nu [W m^-2 Hz^-1 sr^-1].

    What an instrument looking into a blackbody measures: power per unit area, per unit
    frequency, per unit solid angle. FIRAS reports this quantity (as MJy/sr).
    """
    return _as_float_or_array(C_LIGHT / (4.0 * math.pi) * np.asarray(planck_u_nu(nu, temperature)))


def wien_peak_nu(temperature):
    """Frequency at which u_nu peaks, nu_max = 2.821 k_B T / h [Hz]."""
    t = _positive("temperature", temperature)
    return _as_float_or_array(WIEN_X_NU * K_B * t / PLANCK_H)


def wien_peak_lambda(temperature):
    """Wavelength at which u_lambda peaks, lambda_max = b / T, b = 2.898e-3 m K [m]."""
    t = _positive("temperature", temperature)
    return _as_float_or_array(WIEN_B / t)


def energy_density(temperature):
    """Total energy density u = a T^4 [J/m^3], the integral of either spectrum."""
    t = _positive("temperature", temperature)
    return _as_float_or_array(RADIATION_CONSTANT * t**4)


def radiated_flux(temperature):
    """Power per unit area leaving a blackbody surface (or a hole), sigma T^4 [W/m^2]."""
    t = _positive("temperature", temperature)
    return _as_float_or_array(STEFAN_BOLTZMANN * t**4)


def integrate_u_nu(temperature: float, n_points: int = 4096) -> float:
    """Integral of `planck_u_nu` over frequency by Simpson's rule [J/m^3].

    Uniform grid on 0 <= nu <= 50 k_B T / h with `n_points` intervals; the tail beyond is
    below double precision. The verification compares it with a T^4.
    """
    if n_points < 2 or n_points % 2:
        raise ValueError("n_points must be an even number of intervals")
    t = float(_positive("temperature", temperature))
    nu = np.linspace(0.0, SPECTRUM_X_MAX * K_B * t / PLANCK_H, n_points + 1)
    return simpson(planck_u_nu(nu, t), nu)


def integrate_u_lambda(temperature: float, n_points: int = 4096) -> float:
    """Integral of `planck_u_lambda` over wavelength by Simpson's rule in ln(lambda) [J/m^3].

    The wavelength spectrum has a long tail, u_lambda ~ 8 pi k_B T / lambda^4, so the grid
    is uniform in ln(lambda), from a fiftieth of the peak wavelength's scale h c / (k_B T) to
    a million times it, and the integrand is u_lambda lambda. A computation in a different
    variable, on a different grid, of the same energy.
    """
    if n_points < 2 or n_points % 2:
        raise ValueError("n_points must be an even number of intervals")
    t = float(_positive("temperature", temperature))
    scale = PLANCK_H * C_LIGHT / (K_B * t)
    log_lam = np.linspace(math.log(scale / SPECTRUM_X_MAX), math.log(scale * 1e6), n_points + 1)
    lam = np.exp(log_lam)
    return simpson(planck_u_lambda(lam, t) * lam, log_lam)


def stefan_boltzmann_check(temperature: float, n_points: int = 4096) -> tuple[float, float]:
    """(numerical integral of u_nu over frequency, closed form a T^4) [J/m^3, J/m^3].

    The closed form rests on the integral of x^3 / (e^x - 1) from 0 to infinity, which is
    pi^4 / 15 = 6 zeta(4); the quadrature knows nothing of zeta functions.
    """
    return integrate_u_nu(temperature, n_points), float(energy_density(temperature))


def band_fraction(temperature: float, lam_short: float, lam_long: float,
                  n_points: int = 2048) -> float:
    """Fraction of a blackbody's energy that lies between two wavelengths. Dimensionless.

    Simpson's rule on u_lambda over [lam_short, lam_long], divided by a T^4. For the visible
    band, 380-750 nm, it is the best any thermal lamp can do at turning energy into light.
    """
    if not 0 < lam_short < lam_long:
        raise ValueError("need 0 < lam_short < lam_long")
    if n_points < 2 or n_points % 2:
        raise ValueError("n_points must be an even number of intervals")
    lam = np.linspace(lam_short, lam_long, n_points + 1)
    return simpson(planck_u_lambda(lam, temperature), lam) / float(energy_density(temperature))


# ---------------------------------------------------------------------------
# The photon gas
# ---------------------------------------------------------------------------


def photon_number_density(temperature):
    """Photons per unit volume, n = 16 pi zeta(3) (k_B T / (h c))^3 [1/m^3].

    The integral of g(nu) <n> over frequency: 8 pi (k_B T / h c)^3 times the integral of
    x^2 / (e^x - 1), which is 2 zeta(3). It grows as T^3: photons are not conserved.
    """
    t = _positive("temperature", temperature)
    return _as_float_or_array(16.0 * math.pi * ZETA_3 * (K_B * t / (PLANCK_H * C_LIGHT)) ** 3)


@dataclass(frozen=True)
class PhotonGas:
    """Equilibrium radiation in a cavity at one temperature, per unit volume (SI units)."""

    temperature: float
    energy_density: float     # u = a T^4 [J/m^3]
    pressure: float           # P = u / 3 [Pa]
    entropy_density: float    # s = (4/3) a T^3 [J K^-1 m^-3]
    number_density: float     # n = 16 pi zeta(3) (k_B T / h c)^3 [1/m^3]

    @property
    def free_energy_density(self) -> float:
        """f = u - T s = -u/3 [J/m^3]: equal to -P, as F = -P V requires when mu = 0."""
        return self.energy_density - self.temperature * self.entropy_density

    @property
    def energy_per_photon(self) -> float:
        """u / n = (pi^4 / (30 zeta(3))) k_B T = 2.701 k_B T [J]."""
        return self.energy_density / self.number_density


def photon_gas(temperature: float) -> PhotonGas:
    """The photon gas at temperature T: u = a T^4, P = u / 3, s = (4/3) a T^3, and n.

    P = u / 3 is module 04's momentum-flux argument with E = p c. The entropy follows from
    dU = T dS at fixed volume: integrating C_V / T = 4 a V T^2 from zero gives (4/3) a V T^3.
    The chemical potential is zero, so u = T s - P exactly (the Euler relation with mu = 0).
    """
    t = float(_positive("temperature", temperature))
    u = RADIATION_CONSTANT * t**4
    return PhotonGas(temperature=t, energy_density=u, pressure=u / 3.0,
                     entropy_density=4.0 * RADIATION_CONSTANT * t**3 / 3.0,
                     number_density=float(photon_number_density(t)))


# ---------------------------------------------------------------------------
# Solids: Einstein and Debye
# ---------------------------------------------------------------------------


def einstein_heat_capacity(temperature, theta_e: float, n: float):
    """C = 3 N k_B x^2 e^x / (e^x - 1)^2, x = theta_E / T [J/K]: module 12's oscillator, 3N times.

    `n` is the number of atoms (N_A for a mole). Dulong-Petit, 3 N k_B, when T >> theta_E;
    3 N k_B x^2 e^-x -- exponentially small -- when T << theta_E. Deep in the cold limit it
    returns a vanishingly small finite number, never NaN or an overflow.
    """
    if theta_e <= 0 or n <= 0:
        raise ValueError("theta_e and n must be positive")
    per_oscillator = harmonic_heat_capacity(K_B * theta_e, _positive("temperature", temperature))
    return _as_float_or_array(3.0 * n * np.asarray(per_oscillator))


def debye_integrand(x):
    """x^4 e^x / (e^x - 1)^2, written as x^4 / (4 sinh^2(x/2)); behaves as x^2 near zero."""
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        value = np.where(x > 0, x**4 / (4.0 * np.sinh(0.5 * np.minimum(x, 1400.0)) ** 2), 0.0)
    return _as_float_or_array(value)


def debye_heat_capacity(temperature, theta_d: float, n: float, n_quad: int = 64):
    """C = 9 N k_B (T / theta_D)^3 * integral_0^(theta_D / T) x^4 e^x / (e^x - 1)^2 dx [J/K].

    The integral has no closed form; it is done by `n_quad`-point Gauss-Legendre quadrature
    on [0, min(theta_D / T, 60)] -- past 60 the integrand is below 1e-19 of the total. The
    rule converges geometrically: 64 points reach about 1e-12 relative error even on the
    longest interval. Limits: 3 N k_B when T >> theta_D; (12 pi^4 / 5) N k_B (T / theta_D)^3
    when T << theta_D.
    """
    if theta_d <= 0 or n <= 0:
        raise ValueError("theta_d and n must be positive")
    if n_quad < 1:
        raise ValueError("n_quad must be at least one")
    t = _positive("temperature", temperature)
    x_d = theta_d / t
    upper = np.minimum(x_d, DEBYE_X_MAX)
    nodes, weights = np.polynomial.legendre.leggauss(n_quad)
    # Map [-1, 1] onto [0, upper] for every temperature at once.
    half = 0.5 * np.atleast_1d(upper)[:, None]
    x = half * (nodes[None, :] + 1.0)
    integral = (half[:, 0] * (weights[None, :] * np.asarray(debye_integrand(x))).sum(axis=1))
    c = 9.0 * n * K_B * integral.reshape(np.shape(x_d)) / x_d**3
    return _as_float_or_array(c)


def debye_low_t(temperature, theta_d: float, n: float):
    """The Debye T^3 law, C = (12 pi^4 / 5) N k_B (T / theta_D)^3 [J/K]; for T < theta_D / 50."""
    if theta_d <= 0 or n <= 0:
        raise ValueError("theta_d and n must be positive")
    t = _positive("temperature", temperature)
    return _as_float_or_array(12.0 * math.pi**4 / 5.0 * n * K_B * (t / theta_d) ** 3)


def debye_frequency_cutoff(n: float, volume: float, sound_speed: float) -> float:
    """omega_D from counting 3N modes: omega_D^3 = 6 pi^2 (N / V) c_s^3 [rad/s].

    Debye's three sound branches share one speed c_s, so g(omega) = 3 V omega^2 / (2 pi^2 c_s^3);
    the cutoff is wherever the integral of g reaches 3N. theta_D = hbar omega_D / k_B.
    """
    if n <= 0 or volume <= 0 or sound_speed <= 0:
        raise ValueError("n, volume and sound_speed must be positive")
    return (6.0 * math.pi**2 * n / volume) ** (1.0 / 3.0) * sound_speed


def debye_temperature(n: float, volume: float, sound_speed: float) -> float:
    """theta_D = hbar omega_D / k_B for `debye_frequency_cutoff` [K]."""
    return H_BAR * debye_frequency_cutoff(n, volume, sound_speed) / K_B


def synthetic_heat_capacity(temperatures, theta_d: float, n: float, rng: np.random.Generator,
                            noise: float = 0.02) -> np.ndarray:
    """A Debye curve with independent Gaussian noise of relative size `noise` [J/K].

    The documented fallback when no measured table is to hand, and the seed-independence
    test's subject: fitting theta_D to it should recover the value put in.
    """
    if noise < 0:
        raise ValueError("noise must be non-negative")
    clean = np.atleast_1d(np.asarray(debye_heat_capacity(temperatures, theta_d, n), dtype=float))
    return clean * (1.0 + noise * rng.standard_normal(clean.shape))


# ---------------------------------------------------------------------------
# Fitting one temperature to data
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OneParameterFit:
    """A least-squares fit of one parameter, with what the data say about its uncertainty.

    `residuals` are the weighted residuals at the best value: fractional, (model - data) /
    data, for a heat-capacity fit; in units of the stated error, (model - data) / sigma, for
    a spectrum fit. `sigma` is the 1-sigma uncertainty implied by the curvature of the sum
    of squares. It measures how tightly the data pin the parameter *if the model is right*;
    it says nothing about whether the model is right -- the residuals do.
    """

    value: float
    sigma: float
    residuals: np.ndarray

    @property
    def chi_squared(self) -> float:
        return float(np.sum(self.residuals**2))

    @property
    def degrees_of_freedom(self) -> int:
        return len(self.residuals) - 1

    @property
    def rms_residual(self) -> float:
        return float(np.sqrt(np.mean(self.residuals**2)))


def _fit_one_parameter(residuals_of: Callable[[float], np.ndarray], low: float, high: float,
                       scale_by_scatter: bool) -> OneParameterFit:
    """Minimise sum(residuals_of(p)^2) over p in [low, high]; return p and its 1-sigma error.

    A geometric scan of 241 values brackets the minimum; golden-section search then pins it.
    The error is the Gauss-Newton one, sigma^2 = 1 / sum((d r / d p)^2), multiplied by the
    reduced chi^2 when `scale_by_scatter` -- the convention when the per-point errors are not
    known and the scatter of the residuals has to stand in for them.
    """
    def cost(p: float) -> float:
        return float(np.sum(residuals_of(p) ** 2))

    grid = np.geomspace(low, high, 241)
    costs = np.array([cost(p) for p in grid])
    k = int(np.argmin(costs))
    a, b = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - ratio * (b - a), a + ratio * (b - a)
    fc, fd = cost(c), cost(d)
    for _ in range(200):
        if abs(b - a) < 1e-12 * abs(b):
            break
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - ratio * (b - a)
            fc = cost(c)
        else:
            a, c, fc = c, d, fd
            d = a + ratio * (b - a)
            fd = cost(d)
    best = 0.5 * (a + b)
    residuals = residuals_of(best)
    step = 1e-6 * best
    jacobian = (residuals_of(best + step) - residuals_of(best - step)) / (2.0 * step)
    variance = 1.0 / float(np.sum(jacobian**2))
    if scale_by_scatter:
        variance *= float(np.sum(residuals**2)) / max(len(residuals) - 1, 1)
    return OneParameterFit(value=best, sigma=math.sqrt(variance), residuals=residuals)


def _heat_capacity_data(temperatures, heat_capacities) -> tuple[np.ndarray, np.ndarray]:
    t = np.atleast_1d(_positive("temperature", temperatures))
    c = np.atleast_1d(_positive("heat capacity", heat_capacities))
    if t.shape != c.shape or len(t) < 2:
        raise ValueError("need matching arrays of at least two temperatures and heat capacities")
    return t, c


def fit_einstein_temperature(temperatures, heat_capacities, n: float,
                             theta_range: tuple[float, float] = (10.0, 10_000.0)
                             ) -> OneParameterFit:
    """Fit theta_E [K] to measured C(T) by minimising the squared *fractional* residuals.

    Fractional, because a heat capacity spans orders of magnitude: absolute residuals would
    let the high-temperature points, where every model is near 3 N k_B, decide everything.
    `n` must match the data: N_A for molar heat capacities.
    """
    t, c = _heat_capacity_data(temperatures, heat_capacities)
    return _fit_one_parameter(lambda theta: einstein_heat_capacity(t, theta, n) / c - 1.0,
                              *theta_range, scale_by_scatter=True)


def fit_debye_temperature(temperatures, heat_capacities, n: float,
                          theta_range: tuple[float, float] = (10.0, 10_000.0)
                          ) -> OneParameterFit:
    """Fit theta_D [K] to measured C(T), on squared fractional residuals; see the Einstein fit."""
    t, c = _heat_capacity_data(temperatures, heat_capacities)
    return _fit_one_parameter(lambda theta: debye_heat_capacity(t, theta, n) / c - 1.0,
                              *theta_range, scale_by_scatter=True)


def fit_blackbody_temperature(nu, radiance, sigma,
                              t_range: tuple[float, float] = (0.1, 1.0e5)) -> OneParameterFit:
    """Fit the temperature [K] of a measured spectrum B_nu with known 1-sigma errors.

    Minimises chi^2 = sum(((B_nu(T) - data) / sigma)^2); `nu` in Hz, `radiance` and `sigma`
    in W m^-2 Hz^-1 sr^-1. The returned sigma is the statistical error alone; chi_squared
    against degrees_of_freedom tests whether a Planck curve is the right shape at all.
    """
    nu = np.atleast_1d(_positive("nu", nu))
    data = np.atleast_1d(np.asarray(radiance, dtype=float))
    err = np.atleast_1d(_positive("sigma", sigma))
    if not nu.shape == data.shape == err.shape:
        raise ValueError("nu, radiance and sigma must have one shape")
    return _fit_one_parameter(lambda t: (planck_radiance_nu(nu, t) - data) / err,
                              *t_range, scale_by_scatter=False)


# ---------------------------------------------------------------------------
# Advanced: a planet's energy balance
# ---------------------------------------------------------------------------


def greenhouse_surface_temperature(n_layers: int = 0, solar_constant: float = 1361.0,
                                   albedo: float = 0.3) -> float:
    """Surface temperature [K] of a planet under `n_layers` layers that absorb all infrared.

    Each layer is transparent to sunlight and black to the planet's thermal radiation. The
    planet absorbs (1 - albedo) S / 4 per unit area (the factor 4 is the ratio of a sphere's
    area to its shadow's); with no layers it radiates that away at T_e, sigma T_e^4 =
    (1 - albedo) S / 4. Each layer re-radiates half of what it absorbs downward, and the
    balance of every layer gives T_surface = T_e (n_layers + 1)^(1/4). A toy, and labelled
    as one: real atmospheres absorb in bands, are partly transparent, and carry heat by
    convection.
    """
    if n_layers < 0 or int(n_layers) != n_layers:
        raise ValueError("n_layers must be a non-negative whole number")
    if solar_constant <= 0 or not 0 <= albedo < 1:
        raise ValueError("need a positive solar constant and 0 <= albedo < 1")
    t_e = ((1.0 - albedo) * solar_constant / (4.0 * STEFAN_BOLTZMANN)) ** 0.25
    return t_e * (n_layers + 1) ** 0.25

