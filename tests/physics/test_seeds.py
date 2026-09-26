"""Accuracy category 6: independence from the random seed.

A physical conclusion may not depend on which random numbers happened to come up. Every
stochastic function in the library takes an explicit `rng`, and these tests confirm both that
the seed controls reproducibility and that the physics does not change with it.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import (
    engines,
    equilibrium,
    fundamental,
    kinetics,
    multiplicity,
    potentials,
    processes,
    sampling,
)
from thermolab.constants import K_B
from thermolab.validation import scaling_exponent, seed_study

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
        lambda rng: (
            kinetics.initialise_gas(500, BOX_2D, 300.0, ARGON_MASS, rng).kinetic_temperature
        ),
        n_seeds=6,
    )

    assert study.values == pytest.approx(300.0, rel=1e-9)


def test_two_box_equilibrium_occupancy_is_seed_independent():
    def mean_late_fraction(rng: np.random.Generator) -> float:
        occupancy = multiplicity.sample_two_box(300, n_steps=20_000, rng=rng)
        return float(occupancy[len(occupancy) // 2 :].mean() / 300)

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


def test_same_seed_reproduces_the_same_rolls():
    """The first thing the orientation lab asks a student to check about randomness here."""
    a = sampling.roll_dice(500, np.random.default_rng(23))
    b = sampling.roll_dice(500, np.random.default_rng(23))
    c = sampling.roll_dice(500, np.random.default_rng(24))

    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_measured_spread_of_the_average_agrees_across_seeds():
    """A different stream of random numbers must not change the physics being measured."""
    study = seed_study(lambda rng: sampling.relative_spread_of_average(64, 1500, rng), n_seeds=8)

    assert study.agrees_with(sampling.predicted_relative_spread(64), n_sigma=3.0), (
        f"measured {study.mean:.5g} +/- {study.standard_error:.2g}, "
        f"expected {sampling.predicted_relative_spread(64):.5g}"
    )


def test_two_independent_seed_families_give_the_same_spread():
    """Reproducibility across whole seed families, not just within one."""
    first = seed_study(
        lambda rng: sampling.relative_spread_of_average(100, 1200, rng), n_seeds=6, base_seed=1
    )
    second = seed_study(
        lambda rng: sampling.relative_spread_of_average(100, 1200, rng), n_seeds=6, base_seed=999
    )

    combined = np.hypot(first.standard_error, second.standard_error)
    assert abs(first.mean - second.mean) <= 3.0 * combined


def test_conditioning_on_a_lucky_start_does_not_bias_what_follows():
    """The falsifying experiment for "later rolls compensate earlier ones".

    Keep only the runs whose first ten rolls averaged well above 3.5, then look at the *next*
    rolls of those same runs. If the dice compensated, this conditioned mean would sit below
    3.5. It does not: convergence works by dilution, not by correction.
    """

    def mean_of_rolls_after_a_hot_start(rng: np.random.Generator) -> float:
        rolls = sampling.roll_dice(10, rng, n_faces=6)
        while rolls.mean() <= 4.5:  # keep drawing until this run starts hot
            rolls = sampling.roll_dice(10, rng, n_faces=6)
        return float(sampling.roll_dice(4000, rng, n_faces=6).mean())

    study = seed_study(mean_of_rolls_after_a_hot_start, n_seeds=12)

    assert study.agrees_with(sampling.die_mean(6), n_sigma=3.0), (
        f"rolls after a hot start averaged {study.mean:.4g} +/- {study.standard_error:.2g}; "
        "a compensating die would sit below 3.5"
    )


def test_same_seed_reproduces_the_same_walk():
    a = sampling.random_walk(200, 150, np.random.default_rng(55))
    b = sampling.random_walk(200, 150, np.random.default_rng(55))
    c = sampling.random_walk(200, 150, np.random.default_rng(56))

    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_the_fitted_spread_exponent_is_seed_independent():
    """Every walker cloud is different; the exponent 1/2 read off it is not."""

    def fitted_exponent(rng: np.random.Generator) -> float:
        spread = sampling.walker_spread(sampling.random_walk(3000, 1024, rng))
        times = [4, 16, 64, 256, 1024]
        return scaling_exponent(times, [float(spread[t]) for t in times])

    study = seed_study(fitted_exponent, n_seeds=8)

    assert study.agrees_with(0.5, n_sigma=3.0), (
        f"fitted exponent {study.mean:.5f} +/- {study.standard_error:.2g} across seeds"
    )


def test_the_spread_coefficient_agrees_across_seeds():
    """The coefficient as well as the exponent: sigma(t) = sigma_1 sqrt(t), sigma_1 = 1 here."""
    study = seed_study(
        lambda rng: float(sampling.walker_spread(sampling.random_walk(4000, 400, rng))[-1]),
        n_seeds=8,
    )

    assert study.agrees_with(sampling.step_distribution("pm1").std * np.sqrt(400), n_sigma=3.0)


def test_conditioning_on_a_walker_far_from_the_origin_does_not_pull_it_back():
    """The falsifying experiment for `walker-restoring-force`.

    Keep only the walkers standing at x >= +30 after 500 steps, then watch their *next* 500.
    If the walk were pulled back, this conditioned displacement would be negative. It is zero
    within its standard error: a walker far to the right has no idea it is far to the right.
    """

    def mean_later_displacement(rng: np.random.Generator) -> float:
        trajectories = sampling.random_walk(40_000, 1000, rng)
        far_right = trajectories[:, 500] >= 30.0
        assert far_right.sum() > 100, "not enough walkers survived the condition to average"
        return float((trajectories[far_right, 1000] - trajectories[far_right, 500]).mean())

    study = seed_study(mean_later_displacement, n_seeds=8)

    assert study.agrees_with(0.0, n_sigma=3.0), (
        f"walkers conditioned on x >= +30 went on to move {study.mean:.3f} "
        f"+/- {study.standard_error:.3f} steps; a restoring force would give about -30"
    )


def test_same_seed_reproduces_the_same_exchange_trajectory():
    state = equilibrium.from_temperatures(200, 80, 400.0, 300.0, 15.0 * K_B)
    a = equilibrium.simulate_energy_exchange(state, 500, np.random.default_rng(4))
    b = equilibrium.simulate_energy_exchange(state, 500, np.random.default_rng(4))

    assert np.array_equal(a.q_a, b.q_a)


def test_different_seeds_give_different_exchange_trajectories():
    state = equilibrium.from_temperatures(200, 80, 400.0, 300.0, 15.0 * K_B)
    a = equilibrium.simulate_energy_exchange(state, 500, np.random.default_rng(1))
    b = equilibrium.simulate_energy_exchange(state, 500, np.random.default_rng(2))

    assert not np.array_equal(a.q_a, b.q_a)


def test_relaxation_gap_agrees_across_seeds_within_statistical_error():
    """The macroscopic relaxation curve is seed-independent even though every trajectory differs."""
    quantum = 20.0 * K_B
    state = equilibrium.from_temperatures(150, 50, 500.0, 250.0, quantum)
    checkpoint = int(equilibrium.relaxation_time(state))
    predicted = float(equilibrium.predicted_relaxation(state, np.array([checkpoint]))[0])

    def measure(rng: np.random.Generator) -> float:
        result = equilibrium.simulate_energy_exchange(state, checkpoint, rng)
        return float(result.temperature_a[-1] - result.temperature_b[-1])

    study = seed_study(measure, n_seeds=10)
    assert study.agrees_with(predicted, n_sigma=3.5)


def test_seed_study_detects_a_genuinely_biased_measurement():
    """The guard rail itself must work, or every test above is vacuous."""
    biased = seed_study(lambda rng: 1.0 + 0.5 + rng.normal(0, 1e-6), n_seeds=8)

    assert not biased.agrees_with(1.0, n_sigma=3.0)


def test_a_microscopic_free_expansion_has_the_same_temperature_under_every_seed():
    """Not "agrees within error" — identical, for every seed, because no velocity is touched.

    This is the one measurement in the course with genuinely zero spread, and that is the
    point: a result that cannot vary with the seed is a property of the model rather than a
    sample from it. The pressure below is the honest measurement, and it does have a spread.
    """
    for seed in range(8):
        rng = np.random.default_rng(seed)
        gas = kinetics.initialise_gas(200, BOX_2D, 300.0, ARGON_MASS, rng)
        widened = processes.free_expansion_microstate(gas, 2.0)

        assert widened.kinetic_temperature == gas.kinetic_temperature


def test_the_measured_pressure_of_a_free_expansion_halves_across_independent_seeds():
    """P V is conserved: same particles, same speeds, twice the room, half the wall traffic.

    Measured from summed wall impulses rather than computed from the equation of state, so
    this is the microscopic model agreeing with the thermodynamic argument and not restating
    it. The initial transient is discarded because the widened box starts with every particle
    bunched in its old half.
    """
    def measure(rng: np.random.Generator) -> float:
        gas = kinetics.initialise_gas(300, BOX_2D, 300.0, ARGON_MASS, rng)
        widened = processes.free_expansion_microstate(gas, 2.0)
        packed = kinetics.simulate(gas, dt=kinetics.max_stable_dt(gas), n_steps=1200)
        spread = kinetics.simulate(widened, dt=kinetics.max_stable_dt(widened), n_steps=1200)
        return spread.pressure(discard_fraction=0.2) / packed.pressure(discard_fraction=0.2)

    study = seed_study(measure, n_seeds=8, base_seed=606)

    assert study.agrees_with(0.5)
    assert study.relative_spread < 0.1


def test_the_same_seed_reproduces_the_same_widened_gas():
    """The expansion carries no randomness of its own, so reproducibility must survive it."""
    first = processes.free_expansion_microstate(
        kinetics.initialise_gas(150, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(31)), 3.0
    )
    second = processes.free_expansion_microstate(
        kinetics.initialise_gas(150, BOX_2D, 300.0, ARGON_MASS, np.random.default_rng(31)), 3.0
    )

    assert np.array_equal(first.positions, second.positions)
    assert np.array_equal(first.velocities, second.velocities)
    assert np.array_equal(first.box, second.box)


def test_no_randomly_drawn_engine_ever_beats_the_carnot_bound():
    """The module's central claim, posed as an experiment over 32 independent engines.

    Each seed draws a different size, expansion ratio and quality of thermal contact. The
    bound is a theorem, so the interesting outcome is not that the mean respects it but that
    *every single draw* does — hence a hard assertion per seed rather than a statistic.
    """
    for seed in range(32):
        cycle = engines.random_two_reservoir_engine(np.random.default_rng(seed), 600.0, 300.0)
        assert cycle.efficiency <= cycle.carnot_bound
        assert cycle.entropy_produced / cycle.entropy_scale > -1e-12


def test_the_same_seed_builds_the_same_engine():
    """Reproducibility: the rng is the only source of variation, and it is passed explicitly."""
    a = engines.random_two_reservoir_engine(np.random.default_rng(7), 600.0, 300.0)
    b = engines.random_two_reservoir_engine(np.random.default_rng(7), 600.0, 300.0)

    assert a.efficiency == b.efficiency
    assert a.entropy_produced == b.entropy_produced


def test_different_seeds_really_do_build_different_engines():
    """Guards the test above from passing trivially because the draw was being ignored."""
    a = engines.random_two_reservoir_engine(np.random.default_rng(1), 600.0, 300.0)
    b = engines.random_two_reservoir_engine(np.random.default_rng(2), 600.0, 300.0)

    assert a.efficiency != b.efficiency


# ---------------------------------------------------------------------------
# Module 09: the entropy ledger
# ---------------------------------------------------------------------------

LEDGER_QUANTUM = 5.0 * K_B


def ledger_final(rng: np.random.Generator) -> float:
    state = equilibrium.from_temperatures(300, 100, 500.0, 250.0, LEDGER_QUANTUM)
    result = equilibrium.simulate_energy_exchange(state, 8 * state.total_quanta, rng)
    return float(equilibrium.entropy_produced(result)[-1])


def test_the_ledgers_final_value_agrees_across_seeds_with_its_exact_expectation():
    """The expectation over the hop rule's own stationary law (binomial, labelled quanta)."""
    state = equilibrium.from_temperatures(300, 100, 500.0, 250.0, LEDGER_QUANTUM)
    total = state.total_quanta
    q = np.arange(total + 1)
    ledger = K_B * (equilibrium.einstein_log_multiplicity(q, 300)
                    + equilibrium.einstein_log_multiplicity(total - q, 100)
                    - equilibrium.einstein_log_multiplicity(state.q_a, 300)
                    - equilibrium.einstein_log_multiplicity(state.q_b, 100))
    p = 300 / 400
    log_binomial = (multiplicity.log_multiplicity_array(total, q)
                    + q * np.log(p) + (total - q) * np.log(1 - p))
    expected = float((np.exp(log_binomial) * ledger).sum())

    study = seed_study(ledger_final, n_seeds=8)

    assert study.agrees_with(expected, n_sigma=3.5)


def test_the_ledger_is_monotone_within_noise_for_every_seed():
    """It dips on single steps -- by far less than it rises. Never 'proved' monotone."""
    state = equilibrium.from_temperatures(300, 100, 500.0, 250.0, LEDGER_QUANTUM)
    for seed in range(6):
        result = equilibrium.simulate_energy_exchange(state, 8 * state.total_quanta,
                                                      np.random.default_rng(seed))
        ledger = equilibrium.entropy_produced(result)
        drawdown = np.max(np.maximum.accumulate(ledger) - ledger)
        assert np.any(np.diff(ledger) < 0)  # it does tick down
        assert drawdown < 0.02 * ledger[-1]  # but never by more than 2% of the rise


# ---------------------------------------------------------------------------
# Module 10: entropy from a noisy pressure gauge
# ---------------------------------------------------------------------------

GAUGE_GAS = fundamental.monatomic_ideal_gas(ARGON_MASS)
GAUGE_N = 1e21
GAUGE_T = np.linspace(280.0, 320.0, 9)
GAUGE_V = 1e-3 * np.geomspace(1.0, 2.0, 9)


def gauge_entropy(rng: np.random.Generator) -> potentials.GaugeEntropy:
    readings = potentials.gauge_readings(GAUGE_GAS, GAUGE_N, GAUGE_T, GAUGE_V, 0.002, rng)
    return potentials.entropy_from_gauge(GAUGE_T, GAUGE_V, readings)


def test_the_same_seed_reproduces_the_same_gauge_readings():
    a = potentials.gauge_readings(GAUGE_GAS, GAUGE_N, GAUGE_T, GAUGE_V, 0.002,
                                  np.random.default_rng(3))
    b = potentials.gauge_readings(GAUGE_GAS, GAUGE_N, GAUGE_T, GAUGE_V, 0.002,
                                  np.random.default_rng(3))
    assert np.array_equal(a, b)


def test_gauge_entropy_agrees_with_n_k_ln_2_across_seeds():
    """The doubling's Delta S from noisy P(T) data: unbiased, whatever the noise drew."""
    study = seed_study(lambda rng: gauge_entropy(rng).entropy_change[-1], n_seeds=12)
    assert study.agrees_with(GAUGE_N * K_B * np.log(2.0), n_sigma=3.5)


def test_the_gauges_error_bar_matches_its_scatter_across_seeds():
    """An error bar is a claim about the next run; check the claim against twenty of them."""
    study = seed_study(lambda rng: gauge_entropy(rng).entropy_change[-1], n_seeds=20)
    claimed = gauge_entropy(np.random.default_rng(0)).entropy_error[-1]
    scatter = float(np.std(study.values, ddof=1))
    assert 0.6 < scatter / claimed < 1.6
