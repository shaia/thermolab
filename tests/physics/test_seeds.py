"""Accuracy category 6: independence from the random seed.

A physical conclusion may not depend on which random numbers happened to come up. Every
stochastic function in the library takes an explicit `rng`, and these tests confirm both that
the seed controls reproducibility and that the physics does not change with it.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import kinetics, multiplicity
from thermolab.validation import seed_study

pytestmark = pytest.mark.seed_independence

ARGON_MASS = 39.948 * 1.66053906660e-27
BOX_2D = (1e-6, 1e-6)


def test_same_seed_reproduces_the_same_gas():
    a = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(9))
    b = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(9))

    assert np.array_equal(a.positions, b.positions)
    assert np.array_equal(a.velocities, b.velocities)


def test_different_seeds_give_different_microstates():
    a = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(1))
    b = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(2))

    assert not np.allclose(a.positions, b.positions)


def test_measured_pressure_agrees_across_seeds_within_statistical_error():
    """The macroscopic answer is seed-independent even though every microstate differs."""
    def measure(rng: np.random.Generator) -> float:
        state = kinetics.initialise_gas(400, BOX_2D, 300.0, ARGON_MASS, rng)
        return kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=6000).pressure()

    study = seed_study(measure, n_seeds=8)
    expected = kinetics.ideal_gas_pressure(400, 300.0, float(np.prod(BOX_2D)))

    assert study.agrees_with(expected, n_sigma=3.0)
    assert study.relative_spread < 0.05


def test_kinetic_temperature_is_seed_independent_by_construction():
    """Drift removal rescales to the requested temperature, so every seed starts identical."""
    study = seed_study(
        lambda rng: kinetics.initialise_gas(
            500, BOX_2D, 300.0, ARGON_MASS, rng
        ).kinetic_temperature,
        n_seeds=6,
    )

    assert study.values == pytest.approx(300.0, rel=1e-9)


def test_two_box_equilibrium_occupancy_is_seed_independent():
    def mean_late_fraction(rng: np.random.Generator) -> float:
        occupancy = multiplicity.sample_two_box(300, n_steps=20_000, rng=rng)
        return float(occupancy[len(occupancy) // 2:].mean() / 300)

    study = seed_study(mean_late_fraction, n_seeds=8)

    assert study.agrees_with(0.5, n_sigma=3.0)


def test_maxwell_boltzmann_variance_is_seed_independent():
    """Each velocity component has variance k_B T / m, whatever the seed."""
    expected = kinetics.mean_kinetic_energy(300.0, dimension=1) * 2 / ARGON_MASS

    study = seed_study(
        lambda rng: float(
            np.var(kinetics.sample_maxwell_boltzmann(50_000, 300.0, ARGON_MASS, rng, 1))
        ),
        n_seeds=6,
    )

    assert study.agrees_with(expected, n_sigma=4.0)


def test_seed_study_detects_a_genuinely_biased_measurement():
    """The guard rail itself must work, or every test above is vacuous."""
    biased = seed_study(lambda rng: 1.0 + 0.5 + rng.normal(0, 1e-6), n_seeds=8)

    assert not biased.agrees_with(1.0, n_sigma=3.0)
