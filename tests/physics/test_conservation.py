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

from thermolab import (
    chemical,
    engines,
    ensembles,
    equilibrium,
    forms,
    fundamental,
    gases,
    kinetics,
    multiplicity,
    partition,
    phases,
    potentials,
    processes,
    sampling,
)
from thermolab.constants import K_B
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


@given(
    degrees_of_freedom=st.integers(min_value=3, max_value=8),
    volume_ratio=st.floats(min_value=1.05, max_value=6.0),
    temperature=st.floats(min_value=50.0, max_value=1200.0),
)
@settings(max_examples=30, deadline=None)
def test_the_first_law_closes_on_every_quasistatic_family(
    degrees_of_freedom, volume_ratio, temperature
):
    """δQ + δW_on - ΔU must vanish for all four families, for any gas and any expansion.

    This is not a tautology. `isobaric` computes its work from -P ΔV and its heat from
    C_P ΔT — two formulae that never consult each other — so the residual vanishing is a live
    check of Mayer's relation C_P - C_V = N k_B. Give C_P any other value and this fails.
    """
    start = processes.EquilibriumState.from_temperature(
        1000, temperature, 1e-3, degrees_of_freedom
    )
    v_end = volume_ratio * start.volume

    for result in (
        processes.isochoric(start, 0.5 * start.pressure),
        processes.isobaric(start, v_end),
        processes.isothermal(start, v_end),
        processes.adiabatic(start, v_end),
    ):
        scale = max(abs(result.work_on_gas), abs(result.internal_energy_change), 1e-30)
        assert abs(result.first_law_residual) / scale < 1e-12, result.label


@given(
    degrees_of_freedom=st.integers(min_value=3, max_value=8),
    volume_ratio=st.floats(min_value=1.05, max_value=6.0),
)
@settings(max_examples=25, deadline=None)
def test_a_free_expansion_conserves_internal_energy_exactly(
    degrees_of_freedom, volume_ratio
):
    """No work, no heat, so ΔU = 0 — and for an ideal gas that pins ΔT to zero as well.

    The two path functions are compared with `== 0.0` because they are literals in the
    constructor, not results. ΔU is not: it is the difference of two energies each rebuilt
    from P and V, so it lands within an ulp of zero rather than on it. Comparing it
    fractionally is the same rule the rest of this suite follows — these energies are around
    1e-18 J, so an absolute tolerance would prove nothing at all.
    """
    start = processes.EquilibriumState.from_temperature(
        1000, 300.0, 1e-3, degrees_of_freedom
    )
    result = processes.free_expansion(start, volume_ratio * start.volume)

    assert result.work_on_gas == 0.0
    assert result.heat == 0.0
    assert relative_error(result.end.internal_energy, start.internal_energy) < 1e-15
    assert result.end.temperature == pytest.approx(start.temperature, rel=1e-15)


@given(
    degrees_of_freedom=st.integers(min_value=3, max_value=8),
    load_fraction=st.floats(min_value=0.05, max_value=0.95),
)
@settings(max_examples=25, deadline=None)
def test_an_expansion_against_a_constant_load_stops_in_mechanical_equilibrium(
    degrees_of_freedom, load_fraction
):
    """The closed form must land the gas at exactly the external pressure it pushed against.

    `adiabatic_against_constant_pressure` solves for the stopping state analytically, then the
    work is recomputed from -P_ext ΔV; the residual therefore compares two independent routes
    to the same energy rather than restating one of them.
    """
    start = processes.EquilibriumState.from_temperature(
        1000, 300.0, 1e-3, degrees_of_freedom
    )
    p_external = load_fraction * start.pressure

    result = processes.adiabatic_against_constant_pressure(start, p_external)

    assert result.end.pressure == pytest.approx(p_external, rel=1e-12)
    scale = max(abs(result.work_on_gas), 1e-30)
    assert abs(result.first_law_residual) / scale < 1e-12


@given(
    n_particles=st.integers(min_value=2, max_value=60),
    factor=st.floats(min_value=1.1, max_value=8.0),
    seed=st.integers(min_value=0, max_value=2**31 - 1),
)
@settings(max_examples=25, deadline=None)
def test_a_microscopic_free_expansion_touches_no_velocity(n_particles, factor, seed):
    """Removing a partition moves no wall against a force, so the kinetic energy is untouched.

    This is the free expansion's ΔU = 0 established one level down, without thermodynamics.
    The equality is exact rather than approximate because the velocity array is copied, not
    recomputed — and that is precisely why "expanding gases cool" has nowhere to act here.
    """
    rng = np.random.default_rng(seed)
    gas = kinetics.initialise_gas(n_particles, (1e-6, 1e-6), 300.0, 4.65e-26, rng)

    widened = processes.free_expansion_microstate(gas, factor)

    assert np.array_equal(widened.velocities, gas.velocities)
    assert widened.kinetic_energy == gas.kinetic_energy
    assert widened.kinetic_temperature == gas.kinetic_temperature
    assert widened.volume == pytest.approx(factor * gas.volume, rel=1e-12)


def test_a_free_expansion_widens_the_axis_it_was_asked_to():
    """Either wall may be the one that moves, and a negative axis counts from the last.

    An out-of-range axis is refused with the box's actual dimensionality rather than left to
    raise NumPy's IndexError, which names neither the argument nor the range.
    """
    rng = np.random.default_rng(11)
    gas = kinetics.initialise_gas(40, (1e-6, 2e-6), 300.0, 4.65e-26, rng)

    for axis, expected in ((0, (3e-6, 2e-6)), (1, (1e-6, 6e-6)), (-1, (1e-6, 6e-6))):
        widened = processes.free_expansion_microstate(gas, 3.0, axis=axis)
        assert np.allclose(widened.box, expected, rtol=1e-12)
        assert widened.kinetic_temperature == gas.kinetic_temperature

    for bad_axis in (2, -3, 7):
        with pytest.raises(ValueError, match="out of range for a 2-dimensional box"):
            processes.free_expansion_microstate(gas, 2.0, axis=bad_axis)


@pytest.mark.parametrize("degrees_of_freedom", [3, 5, 6])
def test_a_carnot_cycle_returns_the_gas_to_its_starting_state(degrees_of_freedom):
    """Closure is what makes an engine an engine, and it is measured here rather than assumed.

    Each of the four strokes takes its endpoint from its own closed form, so agreement at the
    end is four independent formulae meeting — not a loop that was forced shut.
    """
    cycle = engines.carnot_cycle(1000, 600.0, 300.0, 1e-3, 2.5, degrees_of_freedom)
    start = cycle.strokes[0].process.start
    end = cycle.strokes[-1].process.end

    assert relative_error(end.volume, start.volume) < 1e-12
    assert relative_error(end.temperature, start.temperature) < 1e-12
    assert relative_error(end.pressure, start.pressure) < 1e-12


@pytest.mark.parametrize(
    "build",
    [
        lambda: engines.carnot_cycle(1000, 600.0, 300.0, 1e-3, 2.5),
        lambda: engines.endoreversible_cycle(1000, 600.0, 300.0, 1e-3, 2.5, 40.0, 25.0),
        lambda: engines.reversed_carnot_cycle(1000, 600.0, 300.0, 1e-3, 2.5),
        lambda: engines.otto_cycle(1000, 300.0, 5e-4, 9.0, 2e-17),
    ],
    ids=["carnot", "endoreversible", "refrigerator", "otto"],
)
def test_the_first_law_closes_around_every_cycle(build):
    """Q_net + W_on,net = ΔU = 0 around any closed loop, engine or refrigerator.

    Compared against the internal energy rather than against zero: at 1e-17 J a naive
    absolute tolerance would pass a cycle whose bookkeeping was entirely wrong.
    """
    cycle = build()
    scale = abs(cycle.strokes[0].process.start.internal_energy)

    assert abs(cycle.internal_energy_drift) / scale < 1e-12
    assert abs(cycle.first_law_residual) / scale < 1e-12


def test_the_work_delivered_is_the_net_heat_absorbed():
    """W_out = Q_h - Q_c, which is the first law with ΔU = 0 and the sign convention flipped.

    This is the one place in the course that converts to work-done-by, so it is worth pinning
    that the conversion is a sign and nothing more.
    """
    cycle = engines.carnot_cycle(1000, 600.0, 300.0, 1e-3, 2.5)

    assert relative_error(cycle.work_output, cycle.heat_absorbed - cycle.heat_rejected) < 1e-12
    assert cycle.work_output == -cycle.net_work_on_gas


def test_the_gas_entropy_change_vanishes_around_a_closed_cycle():
    """Entropy is a state function, so the gas's own ΔS is zero around any loop.

    True of the irreversible cycle too — which is exactly why the gas's entropy is the wrong
    thing to watch for the second law, and the reservoirs' entropy is the right one.
    """
    for cycle in (
        engines.carnot_cycle(1000, 600.0, 300.0, 1e-3, 2.5),
        engines.endoreversible_cycle(1000, 600.0, 300.0, 1e-3, 2.5, 40.0, 25.0),
    ):
        total = sum(engines.entropy_change_of_gas(s.process) for s in cycle.strokes)
        assert abs(total) / cycle.entropy_scale < 1e-12


# ---------------------------------------------------------------------------
# Module 09: releasing a constraint redistributes, never creates
# ---------------------------------------------------------------------------

ARGON_09 = fundamental.monatomic_ideal_gas(39.948 * 1.66053906660e-27)


@settings(max_examples=40, deadline=None)
@given(
    share_u=st.floats(0.05, 0.95),
    share_v=st.floats(0.05, 0.95),
    channels=st.sampled_from([("energy",), ("energy", "volume"), ("energy", "particles")]),
)
def test_releasing_a_wall_conserves_every_total(share_u, share_v, channels):
    u_total, v_total, n_side = 1e-2, 1e-4, 1e20
    start = fundamental.Composite(
        ARGON_09, ARGON_09,
        fundamental.Part(share_u * u_total, share_v * v_total, n_side),
        fundamental.Part((1 - share_u) * u_total, (1 - share_v) * v_total, n_side),
    )

    end = start.released(*channels)

    for channel in fundamental.CHANNELS:
        assert relative_error(end.total(channel), start.total(channel)) < 1e-15
    assert end.total_entropy >= start.total_entropy


def test_releasing_a_wall_leaves_the_original_composite_untouched():
    solid = fundamental.einstein_solid(5.0 * 1.380649e-23)
    before = fundamental.Part(1e-19, 1.0, 40.0)
    start = fundamental.Composite(solid, solid, before, fundamental.Part(1e-20, 1.0, 400.0))

    start.released("energy")

    assert start.a == before


def test_the_entropy_ledger_does_not_modify_the_run_it_reads():
    state = equilibrium.from_temperatures(60, 20, 500.0, 250.0, 5.0 * 1.380649e-23)
    result = equilibrium.simulate_energy_exchange(state, 3000, np.random.default_rng(2))
    q_before = result.q_a.copy()

    equilibrium.entropy_produced(result)

    np.testing.assert_array_equal(result.q_a, q_before)
    assert result.initial == state


def test_the_isolated_pair_conserves_energy_along_the_whole_ledger():
    """The ledger is entropy *produced* only because nothing crosses the boundary: check that."""
    state = equilibrium.from_temperatures(60, 20, 500.0, 250.0, 5.0 * 1.380649e-23)
    result = equilibrium.simulate_energy_exchange(state, 3000, np.random.default_rng(3))

    assert np.all(result.q_a + result.q_b == state.total_quanta)
    assert equilibrium.entropy_produced(result).shape == result.q_a.shape


# ---------------------------------------------------------------------------
# Module 10: what the potentials keep
# ---------------------------------------------------------------------------

ARGON_10 = fundamental.monatomic_ideal_gas(39.948 * 1.66053906660e-27)


def test_the_heat_of_isobaric_heating_is_the_enthalpy_change_of_the_relation():
    """Q_P = Delta H: energy bookkeeping at constant pressure, from two sources that share nothing.

    Module 06's heat is C_P times the temperature rise. The enthalpy is U + PV of two states
    located on the Sackur-Tetrode surface. They agree because the first law, with -P Delta V as
    the only work, leaves no room for them not to.
    """
    n = 10**22
    start = processes.EquilibriumState.from_temperature(n, 300.0, 4e-4)
    heating = processes.isobaric(start, 6e-4)
    h_start, h_end = (potentials.ledger_at(ARGON_10, s.temperature, s.volume, n).enthalpy
                      for s in (heating.start, heating.end))

    assert relative_error(h_end - h_start, heating.heat) < 1e-8


def test_the_legendre_transform_loses_nothing_transformed_twice():
    """U(S) -> F(T) = U - TS -> back: slope -S and intercept F + TS = U return the original."""
    n, v = 1e22, 4e-4
    s_mid = float(ARGON_10(1.5 * n * 1.380649e-23 * 300.0, v, n))
    s_grid = np.linspace(0.9 * s_mid, 1.1 * s_mid, 4001)
    u_grid = np.asarray(potentials.energy_at_entropy(ARGON_10, s_grid, v, n))

    temperature, helmholtz = potentials.legendre_transform(u_grid, s_grid)
    minus_entropy, energy_back = potentials.legendre_transform(helmholtz, temperature)

    assert np.max(np.abs(-minus_entropy - s_grid) / s_grid) < 1e-6
    assert np.max(np.abs(energy_back - u_grid) / u_grid) < 1e-6


def test_throttling_conserves_enthalpy_but_not_energy_for_a_real_gas():
    """H in = H out across the plug; U does not survive the trip, because P V changes."""
    vdw = potentials.van_der_waals_gas(39.948 * 1.66053906660e-27, 0.1355 / 6.02214076e23**2,
                                       3.201e-5 / 6.02214076e23)
    result = potentials.throttle(vdw, 6.02214076e23, 300.0, 50e5, 1e5)

    assert relative_error(result.enthalpy_out, result.enthalpy_in) < 1e-12
    assert relative_error(result.energy_out, result.energy_in) > 1e-2


# ---------------------------------------------------------------------------
# Module 11: the composite keeps every quantum
# ---------------------------------------------------------------------------

QUANTUM_11 = 1.0e-21


@given(
    n_system=st.integers(1, 6),
    n_bath=st.integers(1, 400),
    total=st.integers(0, 600),
)
@settings(max_examples=60, deadline=None)
def test_every_joint_row_leaves_the_bath_exactly_the_quanta_the_system_does_not_hold(
    n_system, n_bath, total
):
    levels = ensembles.einstein_levels(n_system, total + 3, QUANTUM_11)
    joint = ensembles.enumerate_joint(levels, n_bath, total)

    assert np.all(levels.quanta + joint.bath_quanta == total)
    # Levels above the total are counted as unreachable, not as negative energy for the bath.
    assert np.all(np.isneginf(joint.log_joint_count[levels.quanta > total]))
    assert abs(ensembles.marginal_occupation(joint).sum() - 1.0) < 1e-12


@pytest.mark.parametrize(("n_system", "n_bath", "total"), [(1, 3, 3), (3, 50, 40), (5, 800, 900)])
def test_the_joint_counts_add_up_to_the_count_of_the_whole_composite(n_system, n_bath, total):
    """System and bath together are one Einstein solid of n + N oscillators.

    Summing g(k) Omega_bath(q - k) over every split must give C(q + n + N - 1, q): no joint
    microstate is lost or counted twice by splitting the composite in two (Vandermonde).
    """
    levels = ensembles.einstein_levels(n_system, total, QUANTUM_11)
    joint = ensembles.enumerate_joint(levels, n_bath, total)
    whole = float(equilibrium.einstein_log_multiplicity(total, n_system + n_bath))

    assert relative_error(joint.log_total_multiplicity, whole) < 1e-12


def test_the_hand_list_of_joint_microstates_matches_the_count_and_conserves_quanta():
    levels = ensembles.einstein_levels(2, 4, QUANTUM_11)
    joint = ensembles.enumerate_joint(levels, 3, 4)
    states = ensembles.explicit_joint_microstates(levels, 3, 4)

    assert len(states) == round(np.exp(joint.log_total_multiplicity))
    assert len(set(states)) == len(states)
    for level, _, bath in states:
        assert levels.quanta[level] + sum(bath) == 4
    per_level = np.bincount([s[0] for s in states], minlength=len(levels))
    assert np.array_equal(per_level, np.rint(np.exp(joint.log_joint_count)).astype(int))


# ---------------------------------------------------------------------------
# Module 12: partition functions
# ---------------------------------------------------------------------------

# Nothing flows in a deterministic equilibrium calculation, so most of module 12 has no
# conservation law to check; the identity F = U - TS, the nearest thing, is filed under the
# analytic limits. What does conserve something is the spin-solid contact, which counts every
# split of a fixed total energy.


def test_every_split_of_the_spin_solid_contact_conserves_the_total_energy():
    contact = partition.spin_solid_contact(60, 45, 40, 300)
    solid_quanta = contact.total_quanta - contact.n_flipped
    assert np.all(solid_quanta >= 0)
    assert np.all(contact.n_flipped + solid_quanta == 45 + 300)
    assert contact.n_flipped[0] == 0 and contact.n_flipped[-1] == 60


def test_canonical_probabilities_sum_to_one_at_every_temperature():
    levels = 1.0e-21 * (np.arange(400) + 0.5)
    for temperature in (1.0, 30.0, 300.0, 3000.0):
        sums = partition.level_sums(levels, temperature)
        assert abs(sums.probabilities.sum() - 1.0) < 1e-12


# ---------------------------------------------------------------------------
# Module 13: chemical potential
# ---------------------------------------------------------------------------


def test_particle_hops_conserve_the_total_number_at_every_step():
    boxes = chemical.two_boxes(500, 2000, 0.0, 2.0 * K_B * 300.0)
    trace = chemical.particle_exchange_sim(boxes, [0, 400], 300.0, 20_000,
                                           np.random.default_rng(13))
    assert np.all(trace.counts.sum(axis=1) == 400)
    assert np.all(trace.counts >= 0) and np.all(trace.counts <= boxes.sites)
    # Single hops only: no record differs from the previous by more than one particle.
    assert np.max(np.abs(np.diff(trace.counts[:, 0]))) == 1


def test_the_column_conserves_particles_across_every_layer():
    boxes = chemical.column(8, 300, 0.5 * K_B * 300.0)
    trace = chemical.particle_exchange_sim(boxes, [200, 0, 0, 0, 0, 0, 0, 100], 300.0, 30_000,
                                           np.random.default_rng(7), record_every=10)
    assert np.all(trace.counts.sum(axis=1) == 300)
    assert np.all(trace.counts >= 0)


def test_the_exact_split_distribution_is_normalized():
    boxes = chemical.two_boxes(300, 900, 0.0, K_B * 300.0)
    dist = chemical.exact_count_distribution(boxes, 500, 300.0)
    assert abs(dist.probability.sum() - 1.0) < 1e-12
    assert dist.n_a.min() == 0 and dist.n_a.max() == 300


# ---------------------------------------------------------------------------
# Module 14: phase coexistence
# ---------------------------------------------------------------------------
# Nothing is transported here -- the module has no dynamics -- so what the construction must
# keep exactly is bookkeeping: the particle count behind the lever rule, the pressure and the
# chemical potential shared by the two phases, and the two lobe areas it declares equal.

CO2_A_14, CO2_B_14 = gases.vdw_constants_from_critical(304.13, 7.3773e6)


def test_the_lever_rule_conserves_particles_and_volume_exactly():
    """x_l + x_g = 1, and x_l v_l + x_g v_g returns the v it was given, across the whole dome."""
    _, v_l, v_g = phases.maxwell_construction(280.0, CO2_A_14, CO2_B_14)
    for v in np.linspace(v_l, v_g, 101):
        x_l, x_g = phases.lever_rule(v, v_l, v_g)
        assert abs(x_l + x_g - 1.0) < 1e-15
        assert relative_error(x_l * v_l + x_g * v_g, v) < 1e-14
    assert phases.lever_rule(v_l, v_l, v_g) == (1.0, 0.0)
    assert phases.lever_rule(v_g, v_l, v_g) == (0.0, 1.0)
    with pytest.raises(ValueError):
        phases.lever_rule(0.5 * v_l, v_l, v_g)


def test_the_chord_at_p_sat_cuts_two_lobes_of_equal_area():
    """The integral of P - P_sat from v_l to v_g vanishes: measured with a fine trapezoid rule
    that knows nothing of the solver's own antiderivative."""
    for t in (250.0, 280.0, 300.0):
        p_sat, v_l, v_g = phases.maxwell_construction(t, CO2_A_14, CO2_B_14)
        v = np.linspace(v_l, v_g, 400_001)
        excess = gases.van_der_waals_pressure(v, t, CO2_A_14, CO2_B_14) - p_sat
        area = float(np.sum(0.5 * (excess[1:] + excess[:-1]) * np.diff(v)))
        assert abs(area) < 1e-9 * p_sat * (v_g - v_l)
        # ... and each lobe on its own is not small: the chord really does cut a loop.
        lobe = float(np.sum(np.where(excess > 0, excess, 0.0)[:-1] * np.diff(v)))
        assert lobe > 1e-3 * p_sat * (v_g - v_l)


def test_the_coexisting_phases_share_pressure_and_chemical_potential():
    for t in (240.0, 280.0, 303.0):
        p_sat, v_l, v_g = phases.maxwell_construction(t, CO2_A_14, CO2_B_14)
        for v in (v_l, v_g):
            assert relative_error(gases.van_der_waals_pressure(v, t, CO2_A_14, CO2_B_14),
                                  p_sat) < 1e-10
        gap = (phases.vdw_chemical_potential(v_l, t, CO2_A_14, CO2_B_14)
               - phases.vdw_chemical_potential(v_g, t, CO2_A_14, CO2_B_14))
        assert abs(gap) < 1e-12 * K_B * t
