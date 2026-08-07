"""Accuracy category 2: conservation laws.

Elastic wall collisions flip a velocity component's sign, so kinetic energy and particle
number must be conserved to machine precision — not approximately. Hypothesis explores the
initial conditions rather than trusting one hand-picked configuration.
"""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from thermolab import kinetics, multiplicity

pytestmark = pytest.mark.conservation


@given(
    n_particles=st.integers(min_value=2, max_value=60),
    temperature=st.floats(min_value=50.0, max_value=1000.0),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
)
@settings(max_examples=25, deadline=None)
def test_kinetic_energy_is_conserved_exactly(n_particles, temperature, seed):
    rng = np.random.default_rng(seed)
    state = kinetics.initialise_gas(n_particles, (1e-6, 1e-6), temperature, 4.65e-26, rng)
    initial = state.kinetic_energy

    result = kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=400)

    assert np.allclose(result.kinetic_energy, initial, rtol=1e-12)


@given(
    n_particles=st.integers(min_value=2, max_value=60),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
)
@settings(max_examples=25, deadline=None)
def test_particle_number_is_conserved(n_particles, seed):
    rng = np.random.default_rng(seed)
    state = kinetics.initialise_gas(n_particles, (1e-6, 1e-6), 300.0, 4.65e-26, rng)

    result = kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=200)

    assert result.final_state.n_particles == n_particles


@given(seed=st.integers(min_value=0, max_value=2**31 - 1))
@settings(max_examples=20, deadline=None)
def test_particles_never_leave_the_box(seed):
    """Containment is the geometric form of particle-number conservation."""
    rng = np.random.default_rng(seed)
    state = kinetics.initialise_gas(80, (1e-6, 2e-6), 300.0, 4.65e-26, rng)

    final = kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=500).final_state

    assert np.all(final.positions >= 0.0)
    assert np.all(final.positions <= final.box)


def test_simulation_refuses_a_step_that_would_lose_particles():
    """Reflection is exact only below max_stable_dt; beyond it the model must fail loudly."""
    rng = np.random.default_rng(7)
    state = kinetics.initialise_gas(50, (1e-6, 1e-6), 300.0, 4.65e-26, rng)

    with pytest.raises(RuntimeError, match="more than once"):
        kinetics.simulate(state, dt=100 * kinetics.max_stable_dt(state), n_steps=5)


@given(
    n_objects=st.integers(min_value=2, max_value=200),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
)
@settings(max_examples=25, deadline=None)
def test_two_box_model_conserves_particle_number(n_objects, seed):
    """Occupancy may wander, but nothing is created or destroyed: 0 <= n_left <= N always."""
    rng = np.random.default_rng(seed)
    occupancy = multiplicity.sample_two_box(n_objects, n_steps=500, rng=rng)

    assert np.all(occupancy >= 0)
    assert np.all(occupancy <= n_objects)
    assert np.all(np.abs(np.diff(occupancy)) == 1)  # exactly one object moves per step


def test_removing_drift_preserves_the_requested_temperature():
    """Subtracting the net momentum must not quietly change the temperature."""
    rng = np.random.default_rng(3)
    state = kinetics.initialise_gas(500, (1e-6, 1e-6), 300.0, 4.65e-26, rng)

    assert state.kinetic_temperature == pytest.approx(300.0, rel=1e-12)
    drift_tolerance = 1e-9 * np.abs(state.velocities).max()
    assert np.allclose(state.velocities.mean(axis=0), 0.0, atol=drift_tolerance)
