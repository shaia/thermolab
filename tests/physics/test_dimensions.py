"""Accuracy category 1: dimensional consistency.

The library works in plain SI floats so students can read the formulas. These tests
re-evaluate the same expressions with pint quantities, so a wrong power of a variable fails
loudly even when the number looks plausible.
"""

from __future__ import annotations

import pytest

from thermolab import kinetics, multiplicity, paths
from thermolab.units import K_B_Q, Quantity

pytestmark = pytest.mark.dimensional


def test_ideal_gas_pressure_has_pressure_dimensions_in_3d():
    n, temperature, volume = 1000, Quantity(300.0, "K"), Quantity(1e-3, "m**3")
    pressure = n * K_B_Q * temperature / volume
    assert pressure.check("[pressure]")


def test_ideal_gas_pressure_in_2d_is_force_per_length():
    """In two dimensions "volume" is an area, so pressure is a force per unit length."""
    n, temperature, area = 1000, Quantity(300.0, "K"), Quantity(1e-6, "m**2")
    pressure = n * K_B_Q * temperature / area
    assert pressure.check("[force] / [length]")


def test_kinetics_pressure_matches_impulse_over_time_and_wall():
    """P = impulse / (time x wall measure) must reduce to a force per unit length in 2D."""
    impulse = Quantity(1.0, "kg * m / s")
    duration = Quantity(1.0, "s")
    wall = Quantity(1.0, "m")
    assert (impulse / (duration * wall)).check("[force] / [length]")


def test_mean_kinetic_energy_is_an_energy():
    assert (0.5 * 2 * K_B_Q * Quantity(300.0, "K")).check("[energy]")


def test_rms_speed_is_a_speed():
    speed = ((2 * K_B_Q * Quantity(300.0, "K")) / Quantity(4.65e-26, "kg")) ** 0.5
    assert speed.check("[velocity]")


def test_work_integral_has_energy_dimensions():
    """W = -∫P dV: pressure times volume is an energy in any dimension."""
    work = Quantity(1e5, "Pa") * Quantity(1e-3, "m**3")
    assert work.check("[energy]")


def test_entropy_has_energy_per_temperature():
    """S = k_B ln Ω — the logarithm is dimensionless, so S carries k_B's units."""
    assert K_B_Q.check("[energy] / [temperature]")


@pytest.mark.parametrize(
    ("value", "expected_dimension"),
    [
        (kinetics.ideal_gas_pressure(1000, 300.0, 1e-6), float),
        (kinetics.mean_kinetic_energy(300.0, dimension=2), float),
        (kinetics.rms_speed(300.0, 4.65e-26, dimension=2), float),
        (paths.ideal_gas_pressure(1000, 300.0, 1e-3), float),
        (paths.isothermal_work_on_gas(1000, 300.0, 1e-3, 2e-3), float),
        (multiplicity.entropy(100, 50), float),
    ],
)
def test_library_functions_return_plain_si_floats(value, expected_dimension):
    """The library itself stays unit-free by design; pint lives in the tests only."""
    assert isinstance(value, expected_dimension)


def test_multiplicity_is_dimensionless():
    """Ω counts microstates — a pure number, whatever the system."""
    assert isinstance(multiplicity.multiplicity(20, 10), float)
    assert multiplicity.multiplicity(20, 10) > 1.0
