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

from thermolab import equilibrium, forms, gases, kinetics, multiplicity, sampling
from thermolab.validation import relative_error

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


@given(
    n_rolls=st.integers(min_value=1, max_value=500),
    n_faces=st.integers(min_value=1, max_value=20),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
)
@settings(max_examples=25, deadline=None)
def test_every_roll_lands_on_a_real_face(n_rolls, n_faces, seed):
    """Probability's version of a conservation law: the outcomes account for every trial."""
    rng = np.random.default_rng(seed)
    rolls = sampling.roll_dice(n_rolls, rng, n_faces)

    assert rolls.size == n_rolls
    assert np.all(rolls >= 1)
    assert np.all(rolls <= n_faces)
    assert int(np.bincount(rolls, minlength=n_faces + 1).sum()) == n_rolls


def test_running_average_ends_on_the_plain_mean():
    """The last point of the settling curve is the ordinary average — no drift, no bias."""
    rng = np.random.default_rng(17)
    rolls = sampling.roll_dice(2000, rng)

    curve = sampling.running_average(rolls)

    assert curve[-1] == pytest.approx(float(rolls.mean()), rel=1e-12)
    assert curve[0] == pytest.approx(float(rolls[0]), rel=1e-12)


def test_integral_of_an_exact_form_depends_only_on_the_endpoints():
    """d(xy) = y dx + x dy, so three different routes to (1,1) must all return f(1,1) - f(0,0).

    This is the mathematical skeleton of "internal energy is a state function": what makes ΔU
    route-blind is exactness, nothing physical.
    """
    m, n = (lambda x, y: y), (lambda x, y: x)
    t = np.linspace(0.0, 1.0, 401)
    zero, one = np.zeros_like(t), np.ones_like(t)

    diagonal = forms.line_integral(m, n, t, t)
    along_x_then_y = forms.line_integral(m, n, t, zero) + forms.line_integral(m, n, one, t)
    via_a_curve = forms.line_integral(m, n, t, t**2)

    expected = 1.0 * 1.0 - 0.0  # f(1,1) - f(0,0) with f = xy
    for value in (diagonal, along_x_then_y, via_a_curve):
        assert value == pytest.approx(expected, abs=1e-9)


@given(
    n_a=st.integers(min_value=1, max_value=500),
    n_b=st.integers(min_value=1, max_value=500),
    q_a=st.integers(min_value=1, max_value=2000),
    q_b=st.integers(min_value=0, max_value=2000),
    n_steps=st.integers(min_value=1, max_value=300),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
)
@settings(max_examples=25, deadline=None)
def test_energy_exchange_conserves_total_quanta(n_a, n_b, q_a, q_b, n_steps, seed):
    """Every step only relabels one quantum's owner, so q_a + q_b must never move."""
    state = equilibrium.TwoBodyState(n_a=n_a, n_b=n_b, q_a=q_a, q_b=q_b, quantum=1.0)
    rng = np.random.default_rng(seed)

    result = equilibrium.simulate_energy_exchange(state, n_steps, rng)

    assert np.all(result.q_a + result.q_b == state.total_quanta)
    assert np.all(result.q_a >= 0)
    assert np.all(result.q_a <= state.total_quanta)


def test_an_exact_form_integrates_to_zero_around_a_closed_loop():
    """The other face of path-independence: no energy can be extracted from a cycle of ΔU."""
    m, n = (lambda x, y: y), (lambda x, y: x)
    angle = np.linspace(0.0, 2.0 * np.pi, 2001)

    loop = forms.line_integral(m, n, 2.0 + np.cos(angle), 1.0 + np.sin(angle))

    assert loop == pytest.approx(0.0, abs=1e-9)


def test_ideal_gas_pressure_temperature_roundtrip_is_exact():
    """No dynamics to conserve energy over here, so invariance stands in: P -> T -> P is exact.

    `ideal_gas_temperature` is the algebraic inverse of `ideal_gas_pressure`, so composing them
    must return the starting temperature to machine precision, for any (N, V) pair.
    """
    n_particles, volume = 1000, 1.0e-3
    for temperature in (150.0, 300.0, 600.0):
        pressure = gases.ideal_gas_pressure(n_particles, temperature, volume)
        recovered = gases.ideal_gas_temperature(n_particles, pressure, volume)
        assert relative_error(recovered, temperature) < 1e-12


def test_reduced_variables_roundtrip_recovers_the_absolute_state():
    """reduced_variables is a pure rescaling by the critical point, so it must invert exactly:
    multiplying each reduced coordinate back by its critical value returns the input state."""
    a, b = 3.736e-49, 5.317e-29
    v_c, t_c, p_c = gases.vdw_critical_point(a, b)
    v, temperature = 2.0 * v_c, 1.1 * t_c
    pressure = gases.van_der_waals_pressure(v, temperature, a, b)

    p_r, v_r, t_r = gases.reduced_variables(pressure, v, temperature, a, b)

    assert relative_error(float(p_r) * p_c, float(pressure)) < 1e-12
    assert relative_error(float(v_r) * v_c, v) < 1e-12
    assert relative_error(float(t_r) * t_c, temperature) < 1e-12


def test_binomial_probabilities_sum_to_one():
    """Nothing physical is conserved in a coin walk, but probability still is.

    The pmf is assembled from log-gammas and exponentiated, which is exactly the arrangement
    where a dropped term hides: every individual value stays plausible while the total drifts.
    """
    for n, p in ((10, 0.5), (100, 0.5), (100, 0.6), (2000, 0.5)):
        _k, pmf, _gaussian = sampling.binomial_to_gaussian(n, p)
        assert pmf.sum() == pytest.approx(1.0, abs=1e-12)


def test_the_walker_histogram_has_unit_area():
    """A density that does not integrate to 1 cannot be compared with the CLT overlay."""
    rng = np.random.default_rng(808)
    trajectories = sampling.random_walk(5000, 200, rng)

    centres, density = sampling.walker_histogram(trajectories[:, -1], n_bins=50)
    width = float(centres[1] - centres[0])

    assert float(density.sum() * width) == pytest.approx(1.0, abs=1e-9)


def test_lattice_binned_histogram_still_has_unit_area():
    """Aligning the bins to the lattice must not quietly change the normalisation."""
    rng = np.random.default_rng(4242)
    positions = sampling.random_walk(5000, 300, rng)[:, -1]

    for n_bins in (31, 61, 91):
        centres, density = sampling.walker_histogram(
            positions, n_bins=n_bins, span=(-90.0, 90.0), lattice=2.0
        )
        width = float(centres[1] - centres[0])
        assert float(density.sum() * width) == pytest.approx(1.0, abs=1e-9)


def test_a_walk_neither_creates_nor_loses_walkers():
    """Walker number is this model's particle number: fixed, and every walker starts at 0."""
    rng = np.random.default_rng(99)
    trajectories = sampling.random_walk(300, 120, rng, step="uniform")

    assert trajectories.shape == (300, 121)
    assert np.all(trajectories[:, 0] == 0.0)
    assert np.all(np.isfinite(trajectories))


def test_every_walk_position_is_the_running_sum_of_its_own_steps():
    """The model's defining identity: x_t - x_(t-1) is one step, so differencing must give
    back a valid step sequence — for the coin walk, exactly +/-1 every time."""
    rng = np.random.default_rng(1234)
    trajectories = sampling.random_walk(200, 80, rng)

    steps = np.diff(trajectories, axis=1)

    assert np.all(np.abs(steps) == 1.0)
    assert np.allclose(np.cumsum(steps, axis=1), trajectories[:, 1:])
