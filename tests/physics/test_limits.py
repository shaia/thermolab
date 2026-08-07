"""Accuracy category 3: known analytic cases and limiting regimes.

Every simulation in the course exists to make a derivation tangible, so each one is pinned
against the result it is supposed to reproduce: the ideal gas law from wall impulses, the
closed-form work integrals along standard paths, equipartition, and the Gaussian limit of
the binomial multiplicity.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import kinetics, multiplicity, paths
from thermolab.constants import K_B
from thermolab.validation import relative_error, seed_study

pytestmark = pytest.mark.analytic_limit

ARGON_MASS = 39.948 * 1.66053906660e-27
BOX_2D = (1e-6, 1e-6)


def measure_pressure(rng: np.random.Generator, n_particles: int = 400,
                     temperature: float = 300.0) -> float:
    state = kinetics.initialise_gas(n_particles, BOX_2D, temperature, ARGON_MASS, rng)
    result = kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=4000)
    return result.pressure()


def test_simulated_pressure_reproduces_the_ideal_gas_law():
    """The point of the pressure laboratory: wall impulses give back P = N k_B T / V."""
    expected = kinetics.ideal_gas_pressure(400, 300.0, float(np.prod(BOX_2D)))

    study = seed_study(measure_pressure, n_seeds=8)

    assert study.agrees_with(expected, n_sigma=3.0), (
        f"measured {study.mean:.4g} +/- {study.standard_error:.2g}, expected {expected:.4g}"
    )


@pytest.mark.parametrize("temperature", [150.0, 300.0, 600.0])
def test_pressure_is_proportional_to_temperature(temperature):
    expected = kinetics.ideal_gas_pressure(300, temperature, float(np.prod(BOX_2D)))

    study = seed_study(lambda rng: measure_pressure(rng, 300, temperature), n_seeds=6)

    assert study.agrees_with(expected, n_sigma=3.5)


def test_equipartition_holds_for_the_sampled_velocities():
    """<E> = (d/2) k_B T is what makes the kinetic temperature meaningful."""
    rng = np.random.default_rng(11)
    velocities = kinetics.sample_maxwell_boltzmann(200_000, 300.0, ARGON_MASS, rng, dimension=2)

    mean_energy = 0.5 * ARGON_MASS * np.mean(np.sum(velocities**2, axis=1))

    assert relative_error(mean_energy, kinetics.mean_kinetic_energy(300.0, 2)) < 0.01


def test_isothermal_work_matches_the_closed_form():
    """W_on = -N k_B T ln(V2/V1), negative because the expanding gas does work on its piston."""
    n, temperature, v1, v2 = 1000, 300.0, 1e-3, 2e-3
    numeric = paths.work_along(
        lambda v: paths.isothermal_pressure(v, n, temperature), v1, v2, n_points=4097
    )
    exact = paths.isothermal_work_on_gas(n, temperature, v1, v2)

    assert relative_error(numeric, exact) < 1e-6
    assert exact < 0  # expansion takes energy out of the gas


def test_adiabatic_work_matches_the_closed_form():
    """Along an adiabat Q = 0, so W_on is exactly ΔU = (P2V2 - P1V1)/(gamma - 1)."""
    gamma, p1, v1, v2 = 5.0 / 3.0, 1e5, 1e-3, 2e-3
    p2 = float(paths.adiabatic_pressure(np.array([v2]), p1, v1, gamma)[0])

    numeric = paths.work_along(
        lambda v: paths.adiabatic_pressure(v, p1, v1, gamma), v1, v2, n_points=4097
    )
    exact = paths.adiabatic_work_on_gas(p1, v1, p2, v2, gamma)

    assert relative_error(numeric, exact) < 1e-6


def test_isobaric_work_matches_the_closed_form():
    numeric = paths.isobaric_path(1e5, 1e-3, 2e-3, n_points=2).work_on_gas()

    assert numeric == pytest.approx(paths.isobaric_work_on_gas(1e5, 1e-3, 2e-3))


def test_isochoric_path_does_no_work():
    """No volume change, no P dV — the cleanest case of work depending on the path taken."""
    assert paths.isochoric_path(1e-3, 1e5, 2e5).work_on_gas() == pytest.approx(0.0)


def test_work_differs_between_paths_with_the_same_endpoints():
    """The defining property of a path function, and the point of Prototype B."""
    n, temperature = 1000, 300.0
    v1, v2 = 1e-3, 2e-3
    p1 = paths.ideal_gas_pressure(n, temperature, v1)
    p2 = paths.ideal_gas_pressure(n, temperature, v2)

    isotherm = paths.isothermal_path(n, temperature, v1, v2)
    two_leg = paths.join(
        paths.isobaric_path(p1, v1, v2),
        paths.isochoric_path(v2, p1, p2),
    )

    assert isotherm.start == pytest.approx(two_leg.start)
    assert isotherm.end == pytest.approx(two_leg.end)
    # Compared as a fraction, not with pytest.approx: these energies are ~1e-18 J, well inside
    # approx's default absolute tolerance, which would call any two of them equal.
    assert relative_error(isotherm.work_on_gas(), two_leg.work_on_gas()) > 0.25


def test_internal_energy_change_is_the_same_for_both_paths():
    """The state function does not care which route was taken — the contrast that teaches."""
    n, temperature = 1000, 300.0
    v1, v2 = 1e-3, 2e-3
    p1 = paths.ideal_gas_pressure(n, temperature, v1)
    p2 = paths.ideal_gas_pressure(n, temperature, v2)

    isotherm = paths.isothermal_path(n, temperature, v1, v2)
    two_leg = paths.join(paths.isobaric_path(p1, v1, v2), paths.isochoric_path(v2, p1, p2))

    assert isotherm.internal_energy_change() == pytest.approx(
        two_leg.internal_energy_change(), abs=1e-30
    )
    # Isothermal ideal gas: U depends on T alone, so ΔU vanishes on both routes.
    assert isotherm.internal_energy_change() == pytest.approx(0.0, abs=1e-30)


def test_first_law_closes_on_every_path():
    """Q = ΔU - W_on is not an extra assumption; it must hold identically."""
    isotherm = paths.isothermal_path(1000, 300.0, 1e-3, 2e-3)

    assert isotherm.heat_into_gas() + isotherm.work_on_gas() == pytest.approx(
        isotherm.internal_energy_change(), rel=1e-12
    )


def test_multiplicity_matches_exact_binomial_for_small_systems():
    from math import comb

    for n in (1, 2, 10, 25):
        for k in range(n + 1):
            assert multiplicity.multiplicity(n, k) == pytest.approx(float(comb(n, k)), rel=1e-9)


def test_multiplicity_peak_is_the_even_split():
    counts = np.arange(0, 101)
    values = multiplicity.log_multiplicity_array(100, counts)

    assert int(counts[np.argmax(values)]) == 50


def test_stirling_approximation_error_shrinks_as_predicted():
    """The next term in the series is 1/(12N), which bounds the leading-order error."""
    from scipy.special import gammaln

    for n in (10, 100, 1000):
        exact = float(gammaln(n + 1))
        approx = multiplicity.stirling_log_factorial(n, order=1)
        assert abs(exact - approx) < 1.0 / (12.0 * n) * 1.01


def test_binomial_approaches_a_gaussian_for_large_n():
    """The central limit theorem in its most physical guise."""
    n = 4000
    counts = np.arange(n // 2 - 300, n // 2 + 301)
    exact = np.exp(multiplicity.log_multiplicity_array(n, counts) - n * np.log(2.0))
    gaussian = multiplicity.gaussian_multiplicity_fraction(n, counts)

    assert np.max(np.abs(exact - gaussian)) / np.max(exact) < 0.01


def test_entropy_becomes_extensive_in_the_thermodynamic_limit():
    """S(2N) = 2 S(N) is exact only as N grows.

    ln Ω(N, N/2) = N ln 2 - (1/2) ln(πN/2) + ..., so doubling the system leaves a sub-leading
    logarithmic discrepancy. Extensivity is a thermodynamic-limit statement, and this test
    says so by watching the discrepancy shrink rather than pretending it is zero.
    """
    sizes = (200, 2000, 20_000, 200_000)
    deviations = [
        relative_error(multiplicity.entropy(2 * n, n), 2.0 * multiplicity.entropy(n, n // 2))
        for n in sizes
    ]

    assert deviations == sorted(deviations, reverse=True)  # monotonically shrinking
    assert deviations[-1] < 1e-4

    # Stronger than "it shrinks": the size of the violation is the predicted correction,
    # [ln(pi N)/2 - ln 2] / (2 N ln 2), so we are seeing the known sub-leading term and not
    # some numerical artefact.
    predicted = [
        (0.5 * np.log(np.pi * n) - np.log(2.0)) / (2.0 * n * np.log(2.0)) for n in sizes
    ]
    assert np.allclose(deviations, predicted, rtol=0.05)


def test_entropy_of_a_fully_ordered_macrostate_vanishes():
    """One microstate, Ω = 1, S = 0 — the anchor of the entropy scale."""
    assert multiplicity.entropy(500, 0) == pytest.approx(0.0, abs=1e-30)
    assert multiplicity.entropy(500, 500) == pytest.approx(0.0, abs=1e-30)


def test_kinetic_temperature_recovers_the_sampling_temperature():
    rng = np.random.default_rng(5)
    state = kinetics.initialise_gas(5000, BOX_2D, 275.0, ARGON_MASS, rng)

    assert state.kinetic_temperature == pytest.approx(275.0, rel=1e-9)


def test_pressure_scales_inversely_with_area_at_fixed_temperature():
    """Boyle's law, measured rather than assumed."""
    rng = np.random.default_rng(19)
    small = kinetics.initialise_gas(300, (1e-6, 1e-6), 300.0, ARGON_MASS, rng)
    large = kinetics.initialise_gas(300, (2e-6, 1e-6), 300.0, ARGON_MASS, rng)

    p_small = kinetics.simulate(small, kinetics.max_stable_dt(small), 6000).pressure()
    p_large = kinetics.simulate(large, kinetics.max_stable_dt(large), 6000).pressure()

    assert p_small / p_large == pytest.approx(2.0, rel=0.15)


def test_ideal_gas_law_is_consistent_between_modules():
    """kinetics and paths must not drift apart on the equation of state."""
    assert kinetics.ideal_gas_pressure(500, 300.0, 1e-3) == pytest.approx(
        paths.ideal_gas_pressure(500, 300.0, 1e-3)
    )
    assert paths.ideal_gas_temperature(500, 1e5, 1e-3) == pytest.approx(
        1e5 * 1e-3 / (500 * K_B)
    )
