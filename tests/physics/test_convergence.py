"""Accuracy category 5: numerical convergence under refinement.

A number produced by a computer is only physics if it stops moving when the numerics are
refined. These tests check the two refinement knobs the course exposes: the quadrature used
for work integrals, and the time step of the particle simulation.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import kinetics, paths
from thermolab.validation import convergence_study, relative_error

pytestmark = pytest.mark.convergence

ARGON_MASS = 39.948 * 1.66053906660e-27


def test_isothermal_work_quadrature_converges_at_second_order():
    """The trapezoid rule is O(h^2); measuring the exponent catches a silently wrong scheme."""
    n, temperature, v1, v2 = 1000, 300.0, 1e-3, 3e-3
    exact = paths.isothermal_work_on_gas(n, temperature, v1, v2)

    study = convergence_study(
        lambda points: paths.work_along(
            lambda v: paths.isothermal_pressure(v, n, temperature), v1, v2, n_points=points
        ),
        refinements=[17, 33, 65, 129, 257],
        exact=exact,
    )

    assert study.observed_order == pytest.approx(2.0, abs=0.2)
    assert study.errors[-1] < study.errors[0]


def test_adiabatic_work_quadrature_converges_at_second_order():
    gamma, p1, v1, v2 = 5.0 / 3.0, 1e5, 1e-3, 3e-3
    p2 = float(paths.adiabatic_pressure(np.array([v2]), p1, v1, gamma)[0])
    exact = paths.adiabatic_work_on_gas(p1, v1, p2, v2, gamma)

    study = convergence_study(
        lambda points: paths.work_along(
            lambda v: paths.adiabatic_pressure(v, p1, v1, gamma), v1, v2, n_points=points
        ),
        refinements=[17, 33, 65, 129, 257],
        exact=exact,
    )

    assert study.observed_order == pytest.approx(2.0, abs=0.2)


def test_refining_the_quadrature_reaches_the_analytic_answer():
    exact = paths.isothermal_work_on_gas(1000, 300.0, 1e-3, 2e-3)
    fine = paths.work_along(
        lambda v: paths.isothermal_pressure(v, 1000, 300.0), 1e-3, 2e-3, n_points=8193
    )

    assert relative_error(fine, exact) < 1e-7


def test_isobaric_work_is_exact_at_the_coarsest_sampling():
    """A straight line needs no refinement — the trapezoid rule is exact on it."""
    coarse = paths.isobaric_path(1e5, 1e-3, 2e-3, n_points=2).work_on_gas()
    fine = paths.isobaric_path(1e5, 1e-3, 2e-3, n_points=1001).work_on_gas()

    assert coarse == pytest.approx(fine, rel=1e-12)


@pytest.mark.parametrize("divisor", [1, 2, 4, 8])
def test_measured_pressure_is_independent_of_the_time_step(divisor):
    """Free flight plus mirror reflection integrates the exact trajectory.

    So refining dt must not move the answer at all — unlike an approximate integrator, where
    it would. Total simulated time is held fixed as dt shrinks.
    """
    rng = np.random.default_rng(31)
    state = kinetics.initialise_gas(300, (1e-6, 1e-6), 300.0, ARGON_MASS, rng)
    dt_max = kinetics.max_stable_dt(state)

    reference = kinetics.simulate(state, dt=dt_max, n_steps=2000).pressure()
    refined = kinetics.simulate(state, dt=dt_max / divisor, n_steps=2000 * divisor).pressure()

    assert relative_error(refined, reference) < 1e-9


def test_pressure_estimate_settles_as_the_averaging_window_grows():
    """Statistical convergence: a longer average is a better one, ~1/sqrt(duration)."""
    rng = np.random.default_rng(43)
    state = kinetics.initialise_gas(300, (1e-6, 1e-6), 300.0, ARGON_MASS, rng)
    dt = kinetics.max_stable_dt(state)
    expected = kinetics.ideal_gas_pressure(300, 300.0, 1e-12)

    errors = [
        relative_error(kinetics.simulate(state, dt=dt, n_steps=steps).pressure(), expected)
        for steps in (500, 2000, 8000, 32000)
    ]

    assert errors[-1] < errors[0]
    assert errors[-1] < 0.05
