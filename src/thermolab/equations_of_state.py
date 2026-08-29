"""Equations of state: the ideal gas, the van der Waals correction, and the critical point.

MODEL SPECIFICATION
    System:        N structureless molecules of a real gas, in the van der Waals mean-field
                   approximation; the N-particle ideal gas is the a = b = 0 special case
    Dynamics:      none -- this is a static equation of state relating equilibrium state
                   variables, not a trajectory to integrate
    Boundary:      a rigid container of volume V at temperature T, or a piston varying V
                   quasistatically along an isotherm
    Ensemble:      implicit thermodynamic equilibrium -- P(N, V, T) is an equilibrium
                   equation of state; no microstate is sampled
    Ignored:       higher-order (beyond pairwise mean-field) interactions, quantum effects,
                   internal molecular structure, mixtures of species, and any density
                   dependence of a and b themselves
    Valid when:    the gas is dilute to moderately dense and classical, so that the mutual
                   attraction and the molecules' own volume are both small, additive
                   corrections to the ideal-gas pressure, away from the critical point
    Failure modes: very high density, where a single mean-field pairwise correction can no
                   longer capture the real interactions; at or below the critical
                   temperature, where density fluctuations that mean-field theory ignores
                   become large and the equation's van der Waals loop is unphysical (a
                   Maxwell construction is needed there, and is not implemented here)

CONVENTION: N-particle constants, not per-mole.
    Textbooks quote a and b per mole: (P + a_m n^2/V^2)(V - n b_m) = n R T, with n in moles,
    a_m in Pa m^6/mol^2 and b_m in m^3/mol. This module instead takes a, b per PARTICLE, so
    that N below is a plain particle count -- as everywhere else in this course -- and k_B
    replaces R:

        P = N k_B T / (V - N b) - a N^2 / V^2

    Substituting n = N/N_A into the molar form and collecting terms gives the relation
    between the two: a = a_m / N_A**2 and b = b_m / N_A. Both a and b keep the same *units*
    as their molar counterparts (Pa m^6 and m^3 respectively) -- only the numeric value
    shrinks, from a per-mole quantity to a per-molecule one.
"""

from __future__ import annotations

import numpy as np

from .constants import K_B
from .paths import ideal_gas_pressure


def van_der_waals_pressure(n_particles: float, temperature, volume, a: float, b: float):
    """P = N k_B T / (V - N b) - a N^2 / V^2, vectorized over `volume`.

    `a` and `b` are per-particle constants (see the module docstring for the conversion from
    the per-mole values printed in textbooks). As a, b -> 0 this reduces exactly to
    `paths.ideal_gas_pressure` -- verified in the test suite as the model's analytic limit.
    At a = b = 0 precisely, the ideal case is read off that function directly rather than
    re-deriving N k_B T / V a third time (`kinetics.py` already duplicates it once).
    """
    volume = np.asarray(volume, dtype=float)
    if a == 0.0 and b == 0.0:
        return np.vectorize(ideal_gas_pressure, otypes=[float])(n_particles, temperature, volume)

    excluded = n_particles * b
    if np.any(volume <= excluded):
        raise ValueError(f"volume must exceed the excluded volume N*b = {excluded:.6e} m^3")
    return n_particles * K_B * temperature / (volume - excluded) - a * n_particles**2 / volume**2


def critical_point(n_particles: float, a: float, b: float) -> tuple[float, float, float]:
    """(T_c, P_c, V_c) from dP/dV = 0 and d^2P/dV^2 = 0 at fixed N.

    Writing the pressure per particle, x = V/N, gives P(x) = k_B T/(x - b) - a/x^2 --
    independent of N -- so the critical relations are the textbook molar ones with R -> k_B
    and the molar volume v -> x = V/N:

        x_c = 3b,   k_B T_c = 8a / (27 b),   P_c = a / (27 b^2).

    T_c and P_c are therefore independent of N (both intensive), while V_c = N x_c = 3 N b
    is proportional to N (extensive) -- exactly as physically expected of a critical point.
    """
    if a <= 0 or b <= 0:
        raise ValueError("a and b must be positive for a critical point to exist")
    t_c = 8.0 * a / (27.0 * K_B * b)
    p_c = a / (27.0 * b**2)
    v_c = 3.0 * n_particles * b
    return float(t_c), float(p_c), float(v_c)


def pv_t_surface(n_particles: float, temperatures, volumes, a: float = 0.0, b: float = 0.0):
    """Pressure at every (temperature, volume) combination, as a 2D array.

    The returned array has shape (len(temperatures), len(volumes)). Defaults to the
    ideal-gas surface (`a = b = 0`); passing the van der Waals constants of a real gas bends
    the same grid into its P-V-T surface, including the S-shaped isotherms that appear below
    the critical temperature (see `critical_point`).
    """
    temperatures = np.asarray(temperatures, dtype=float)
    volumes = np.asarray(volumes, dtype=float)
    t_grid = temperatures[:, np.newaxis]
    v_grid = volumes[np.newaxis, :]
    return van_der_waals_pressure(n_particles, t_grid, v_grid, a, b)
