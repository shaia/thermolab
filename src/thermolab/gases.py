"""Equations of state: the ideal gas, the van der Waals correction, and the critical point.

MODEL SPECIFICATION
    System:        a fixed amount of gas described by macroscopic coordinates (P, v, T) alone
    Dynamics:      none -- every function evaluates equilibrium states
    Boundary:      closed, N fixed
    Ensemble:      not applicable -- macroscopic thermodynamics
    Ignored:       all microscopic detail; a and b are phenomenological constants
    Valid when:    dilute classical (ideal) and moderate-density near-critical (vdW) regimes
    Failure modes: the sub-critical (dP/dv)_T > 0 wiggle region (module 14) and
                   quantum-degenerate regimes (module 17)

CONVENTION: per-particle volume, per-particle constants.
    This module works in the per-particle volume v = V/N throughout, not the extensive volume
    V -- that is what makes v, alongside P and T, a genuinely intensive coordinate of the
    equilibrium surface. `van_der_waals_pressure` and everything built on it therefore take v
    directly rather than (n_particles, volume) separately.

    Textbooks quote the van der Waals constants a and b per mole: (P + a_m n^2/V^2)
    (V - n b_m) = n R T, with n in moles, a_m in Pa m^6/mol^2 and b_m in m^3/mol. This module
    instead takes a, b per PARTICLE, with k_B replacing R and v = V/N replacing V/n:

        P = k_B T / (v - b) - a / v^2

    Substituting v = V/N and n = N/N_A into the molar form and collecting terms gives the
    relation between the two conventions: a = a_m / N_A**2 and b = b_m / N_A. Both a and b keep
    the same *units* as their molar counterparts (Pa m^6 and m^3 respectively) -- only the
    numeric value shrinks, from a per-mole quantity to a per-molecule one.
"""

from __future__ import annotations

import numpy as np

from .constants import K_B


def ideal_gas_pressure(n_particles: int, temperature: float, volume: float) -> float:
    """P = N k_B T / V.

    Canonical home of this formula: `kinetics.py` and `paths.py` import it from here rather
    than each carrying their own copy (see the C4a dedup in the project's conflict log).
    """
    if volume <= 0:
        raise ValueError("volume must be positive")
    return n_particles * K_B * temperature / volume


def ideal_gas_temperature(n_particles: int, pressure: float, volume: float) -> float:
    """T = P V / (N k_B)."""
    return pressure * volume / (n_particles * K_B)


def van_der_waals_pressure(v, temperature, a: float, b: float) -> np.ndarray:
    """P = k_B T / (v - b) - a / v^2, vectorized over the per-particle volume `v` and `temperature`.

    `v` is the per-particle volume V/N, and `a`, `b` are per-particle constants (see the module
    docstring for the conversion from the per-mole values printed in textbooks). At a = b = 0
    this is exactly the per-particle ideal-gas pressure k_B T / v -- verified in the test suite
    as the model's analytic limit. Raises if any `v` does not exceed the excluded volume `b`.
    """
    v = np.asarray(v, dtype=float)
    temperature = np.asarray(temperature, dtype=float)
    if np.any(v <= b):
        raise ValueError(f"per-particle volume must exceed the excluded volume b = {b:.6e} m^3")
    return K_B * temperature / (v - b) - a / v**2


def vdw_critical_point(a: float, b: float) -> tuple[float, float, float]:
    """(v_c, T_c, P_c) from dP/dv = 0 and d^2P/dv^2 = 0 on the critical isotherm.

    Closed form: v_c = 3b, k_B T_c = 8a/(27b), P_c = a/(27b^2). All three are properties of the
    substance alone -- intensive, with no particle count anywhere in them -- exactly as the
    per-particle formulation of the equation of state promises.
    """
    if a <= 0 or b <= 0:
        raise ValueError("a and b must be positive for a critical point to exist")
    v_c = 3.0 * b
    t_c = 8.0 * a / (27.0 * K_B * b)
    p_c = a / (27.0 * b**2)
    return float(v_c), float(t_c), float(p_c)


def vdw_constants_from_critical(t_c: float, p_c: float) -> tuple[float, float]:
    """Invert `vdw_critical_point`: a = 27 (k_B T_c)^2 / (64 P_c), b = k_B T_c / (8 P_c).

    This is the path used to fit a substance's van der Waals constants from its measured
    critical point -- the way `a` and `b` are obtained for the NIST CO2 comparison in the
    laboratory, rather than looked up from a textbook table.
    """
    a = 27.0 * (K_B * t_c) ** 2 / (64.0 * p_c)
    b = K_B * t_c / (8.0 * p_c)
    return float(a), float(b)


def reduced_variables(pressure, v, temperature, a: float, b: float
                      ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(P_r, v_r, T_r) = (P/P_c, v/v_c, T/T_c), each scaled by its own critical value."""
    v_c, t_c, p_c = vdw_critical_point(a, b)
    pressure = np.asarray(pressure, dtype=float)
    v = np.asarray(v, dtype=float)
    temperature = np.asarray(temperature, dtype=float)
    return pressure / p_c, v / v_c, temperature / t_c


def vdw_pressure_reduced(v_r, t_r) -> np.ndarray:
    """The parameter-free law of corresponding states: P_r = 8 T_r/(3 v_r - 1) - 3/v_r^2.

    Every van der Waals substance obeys this same equation once P, v and T are measured in
    units of the substance's own critical point -- a and b have scaled out entirely.
    """
    v_r = np.asarray(v_r, dtype=float)
    t_r = np.asarray(t_r, dtype=float)
    return 8.0 * t_r / (3.0 * v_r - 1.0) - 3.0 / v_r**2


def compressibility_factor(pressure, v, temperature) -> np.ndarray:
    """Z = P v / (k_B T) -- exactly 1 for an ideal gas, and a real gas's distance from it."""
    pressure = np.asarray(pressure, dtype=float)
    v = np.asarray(v, dtype=float)
    temperature = np.asarray(temperature, dtype=float)
    return pressure * v / (K_B * temperature)


def isotherm_family(v_grid, temperatures, a: float = 0.0, b: float = 0.0) -> np.ndarray:
    """Pressure at every (temperature, v) combination, as a 2D array of shape (n_T, n_v).

    Defaults to the ideal-gas family (`a = b = 0`); passing a substance's van der Waals
    constants bends the same grid into its isotherm family, including the S-shaped isotherms
    that appear below the critical temperature (see `vdw_critical_point`).
    """
    v_grid = np.asarray(v_grid, dtype=float)
    temperatures = np.asarray(temperatures, dtype=float)
    t_column = temperatures[:, np.newaxis]
    v_row = v_grid[np.newaxis, :]
    return van_der_waals_pressure(v_row, t_column, a, b)


def pvt_surface(v_grid, t_grid, a: float = 0.0, b: float = 0.0
               ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Meshgrid (V, T, P) triple over `v_grid` x `t_grid`, for surface rendering.

    Defaults to the ideal-gas surface (`a = b = 0`); passing a substance's van der Waals
    constants bends the same grid into its P-v-T surface.
    """
    v_grid = np.asarray(v_grid, dtype=float)
    t_grid = np.asarray(t_grid, dtype=float)
    v_mesh, t_mesh = np.meshgrid(v_grid, t_grid, indexing="xy")
    p_mesh = van_der_waals_pressure(v_mesh, t_mesh, a, b)
    return v_mesh, t_mesh, p_mesh
