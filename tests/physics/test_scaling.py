"""Accuracy category 4: large-N behaviour.

The course's central claim is that macroscopic steadiness emerges from microscopic noise.
Quantitatively that means relative fluctuations fall off as N^(-1/2) — so these tests measure
the exponent rather than accepting a qualitative "the jitter looks smaller".
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import (
    chemical,
    engines,
    ensembles,
    equilibrium,
    fundamental,
    gases,
    ising,
    kinetics,
    multiplicity,
    partition,
    phases,
    potentials,
    processes,
    sampling,
)
from thermolab.constants import K_B
from thermolab.validation import relative_error, scaling_exponent

pytestmark = pytest.mark.large_n

ARGON_MASS = 39.948 * 1.66053906660e-27
BOX_2D = (1e-6, 1e-6)


def sampled_pressure(n_particles: int, rng: np.random.Generator, n_steps: int = 3000) -> float:
    """Pressure of one independently drawn microstate at 300 K.

    `fix_temperature=False` keeps the raw Maxwell-Boltzmann draw, so the energy — and hence
    the pressure — differs from sample to sample exactly as a canonical system's does.
    Rescaling to an exact temperature would erase the fluctuation being measured.
    """
    state = kinetics.initialise_gas(
        n_particles, BOX_2D, 300.0, ARGON_MASS, rng, fix_temperature=False
    )
    return kinetics.simulate(state, dt=kinetics.max_stable_dt(state), n_steps=n_steps).pressure()


def relative_pressure_fluctuation(
    n_particles: int, n_samples: int = 24, base_seed: int = 0
) -> float:
    """Spread of the pressure across independent microstates, relative to its mean."""
    seeds = np.random.SeedSequence(base_seed).spawn(n_samples)
    pressures = np.array([sampled_pressure(n_particles, np.random.default_rng(s)) for s in seeds])
    return float(pressures.std(ddof=1) / pressures.mean())


@pytest.mark.slow
def test_relative_pressure_fluctuation_falls_as_one_over_sqrt_n():
    """The course's central quantitative claim, measured rather than asserted.

    For a 2D ideal gas the time-averaged pressure of a microstate is proportional to the sum
    of 2N squared velocity components, so it is chi-square distributed with 2N degrees of
    freedom and its relative spread is exactly N^(-1/2).
    """
    sizes = [25, 50, 100, 200, 400]
    fluctuations = [relative_pressure_fluctuation(n, n_samples=40, base_seed=7) for n in sizes]

    exponent = scaling_exponent(sizes, fluctuations)

    assert exponent == pytest.approx(-0.5, abs=0.12), (
        f"fitted exponent {exponent:.3f} from fluctuations {fluctuations}"
    )


def test_fluctuation_magnitude_matches_the_chi_square_prediction():
    """Not just the exponent: the coefficient is 1, i.e. sigma_P/<P> = 1/sqrt(N)."""
    for n in (50, 200):
        assert relative_pressure_fluctuation(n, n_samples=40, base_seed=3) == pytest.approx(
            1.0 / np.sqrt(n), rel=0.3
        )


def test_larger_systems_have_steadier_pressure():
    """The cheap version of the same statement, kept out of the slow set."""
    small = relative_pressure_fluctuation(25, n_samples=16, base_seed=101)
    large = relative_pressure_fluctuation(400, n_samples=16, base_seed=101)

    assert large < small


def test_ideal_gas_pressure_is_unchanged_by_doubling_n_and_v():
    """The doubling test, mechanised: pressure is intensive, so joining two identical samples
    of the same gas -- N -> 2N, V -> 2V, same T -- must leave the pressure exactly unchanged,
    the falsifier for the `doubling-doubles-everything` misconception."""
    temperature, n_particles, volume = 300.0, 1000, 1e-3

    base = gases.ideal_gas_pressure(n_particles, temperature, volume)
    doubled = gases.ideal_gas_pressure(2 * n_particles, temperature, 2 * volume)

    assert doubled == base


def test_multiplicity_peak_narrows_as_one_over_sqrt_n():
    sizes = [100, 1000, 10_000, 100_000]
    widths = [multiplicity.peak_relative_width(n) for n in sizes]

    assert scaling_exponent(sizes, widths) == pytest.approx(-0.5, abs=1e-9)


def test_odds_of_a_ten_percent_excess_fall_exponentially_in_system_size():
    """Why a gas never gathers in one corner.

    Near the peak, ln[P(n)/P(N/2)] = -2(n - N/2)^2/N, so holding the *fractional* excess at
    10% makes the log-odds fall linearly in N: -0.02 N. Ten thousand particles already put
    the ratio near 1e-87; a mole makes it unreachable.
    """
    sizes = np.array([1000, 5000, 10_000])
    log_ratios = np.array(
        [
            np.log(multiplicity.probability(int(n), int(0.6 * n)))
            - np.log(multiplicity.probability(int(n), int(n) // 2))
            for n in sizes
        ]
    )

    assert np.all(np.diff(log_ratios) < 0)
    assert np.allclose(log_ratios / sizes, -0.02, atol=2e-3)
    assert multiplicity.probability(10_000, 6000) / multiplicity.probability(10_000, 5000) < 1e-80


def test_two_box_occupancy_settles_near_the_even_split():
    """Started from every object on one side, the system drifts to equilibrium and stays."""
    rng = np.random.default_rng(77)
    n_objects = 400
    occupancy = multiplicity.sample_two_box(n_objects, n_steps=40_000, rng=rng)

    late = occupancy[len(occupancy) // 2 :]
    mean_fraction = late.mean() / n_objects
    spread_fraction = late.std() / n_objects

    assert mean_fraction == pytest.approx(0.5, abs=0.02)
    assert spread_fraction < 0.05


def test_relative_spread_of_a_sample_average_falls_as_one_over_sqrt_n():
    """The same law as the pressure fluctuation, stripped of all physics.

    Dice have no energy, no container and no dynamics, so an N^(-1/2) here can only come from
    independence plus the additivity of variance — which is exactly the module's derivation.
    """
    rng = np.random.default_rng(2718)
    sizes = [4, 16, 64, 256, 1024]
    spreads = [sampling.relative_spread_of_average(n, n_samples=800, rng=rng) for n in sizes]

    exponent = scaling_exponent(sizes, spreads)

    assert exponent == pytest.approx(-0.5, abs=0.06), (
        f"fitted exponent {exponent:.3f} from spreads {spreads}"
    )


def test_sample_average_spread_matches_the_predicted_coefficient():
    """Not just the exponent: the prefactor is σ₁/μ₁, measured to a few percent."""
    rng = np.random.default_rng(31415)

    for n in (25, 400):
        measured = sampling.relative_spread_of_average(n, n_samples=2000, rng=rng)
        assert relative_error(measured, sampling.predicted_relative_spread(n)) < 0.1


def test_the_sum_gets_noisier_while_the_average_gets_steadier():
    """The distinction the module's third prediction is built on.

    Absolute scatter of the sum grows as sqrt(N); relative scatter of the average falls as
    1/sqrt(N). Both come from the same line of algebra, and confusing them is the usual error.
    """
    rng = np.random.default_rng(9001)
    sizes = [16, 64, 256, 1024]

    absolute_sum_spreads = []
    relative_average_spreads = []
    for n in sizes:
        averages = sampling.sample_averages(n, 800, rng)
        absolute_sum_spreads.append(float((n * averages).std(ddof=1)))
        relative_average_spreads.append(float(averages.std(ddof=1) / averages.mean()))

    assert scaling_exponent(sizes, absolute_sum_spreads) == pytest.approx(0.5, abs=0.06)
    assert scaling_exponent(sizes, relative_average_spreads) == pytest.approx(-0.5, abs=0.06)


def _relative_spread_of_gap_after_one_tau(n_a: int, n_b: int, n_samples: int, base_seed: int
                                          ) -> float:
    """Seed-to-seed relative spread of T_A - T_B, measured one relaxation time in.

    Bigger bodies (more oscillators, hence more exchanged quanta Q) should make the outcome
    at a fixed *fraction* of the relaxation time more predictable, the same steadying every
    other module's large-N test measures -- here for the approach to equilibrium rather than
    for a value already at equilibrium.
    """
    quantum = 20.0 * K_B
    state = equilibrium.from_temperatures(n_a, n_b, 500.0, 250.0, quantum)
    checkpoint = max(int(round(equilibrium.relaxation_time(state))), 1)
    seeds = np.random.SeedSequence(base_seed).spawn(n_samples)
    gaps = []
    for s in seeds:
        result = equilibrium.simulate_energy_exchange(state, checkpoint, np.random.default_rng(s))
        gaps.append(float(result.temperature_a[-1] - result.temperature_b[-1]))
    gaps = np.array(gaps)
    return float(gaps.std(ddof=1) / abs(gaps.mean()))


def test_equilibration_gets_more_predictable_as_the_bodies_grow():
    """More oscillators (bigger C_A, C_B, more exchanged quanta) means less run-to-run scatter
    in the temperature gap measured one relaxation time in -- the N^(-1/2)-flavoured steadying
    this course keeps rediscovering, now for a relaxation process rather than a static average.
    """
    small = _relative_spread_of_gap_after_one_tau(30, 10, n_samples=20, base_seed=11)
    large = _relative_spread_of_gap_after_one_tau(1000, 300, n_samples=20, base_seed=11)

    assert large < small


def test_walker_cloud_widens_as_the_square_root_of_time():
    """The other face of N^(-1/2): a *sum* of t steps spreads as t^(+1/2).

    Same algebra as the sample average, read in the opposite direction — which is exactly the
    confusion the `spread-means-drift` misconception lives in. Fitting the exponent rather
    than eyeballing the curve is what makes "widens" a measurement.
    """
    rng = np.random.default_rng(31337)
    trajectories = sampling.random_walk(6000, 1024, rng)
    spread = sampling.walker_spread(trajectories)
    times = [4, 16, 64, 256, 1024]
    spreads = [float(spread[t]) for t in times]

    exponent = scaling_exponent(times, spreads)

    assert exponent == pytest.approx(0.5, abs=0.02), (
        f"fitted exponent {exponent:.4f} from spreads {spreads}"
    )


@pytest.mark.parametrize("name", ["pm1", "uniform", "heavy"])
def test_the_spread_coefficient_is_the_standard_deviation_of_one_step(name):
    """Not just the exponent: sigma(t) = sigma_1 sqrt(t), with sigma_1 the step's own spread.

    This is the sentence that makes the CLT useful rather than decorative — the shape is
    universal, and the one number that is not universal is fixed by the step distribution.
    """
    dist = sampling.step_distribution(name)
    rng = np.random.default_rng(515)
    trajectories = sampling.random_walk(8000, 400, rng, step=dist)

    measured = float(sampling.walker_spread(trajectories)[-1])

    assert relative_error(measured, dist.std * np.sqrt(400)) < 0.05


def test_drift_and_spread_of_a_biased_walk_grow_at_different_rates():
    """The falsifier for "the cloud is widening, so the average must be moving".

    A biased walk does both at once, and the two are visibly independent: the mean marches
    linearly at mu_1 t while the width crawls as sigma_1 sqrt(t). By t = 1024 the drift has
    outrun the spread by a factor of twenty, which is why a drifting cloud looks nothing like
    a spreading one once you plot them together.
    """
    dist = sampling.step_distribution("biased")
    rng = np.random.default_rng(20250831)
    trajectories = sampling.random_walk(4000, 1024, rng, step=dist)
    spread = sampling.walker_spread(trajectories)
    times = [16, 64, 256, 1024]

    means = [float(trajectories[:, t].mean()) for t in times]
    spreads = [float(spread[t]) for t in times]

    assert scaling_exponent(times, means) == pytest.approx(1.0, abs=0.03)
    assert scaling_exponent(times, spreads) == pytest.approx(0.5, abs=0.03)


def test_an_unbiased_cloud_widens_without_its_mean_going_anywhere():
    """The same statement with the drift switched off: sigma(t) grows, <x_t> does not.

    The mean is compared against its own standard error, sigma_1 sqrt(t)/sqrt(n_walkers) --
    the only honest way to assert that a measured mean is zero.
    """
    rng = np.random.default_rng(4004)
    n_walkers = 20_000
    trajectories = sampling.random_walk(n_walkers, 1024, rng)
    spread = sampling.walker_spread(trajectories)

    for t in (16, 256, 1024):
        standard_error = np.sqrt(t / n_walkers)
        assert abs(float(trajectories[:, t].mean())) < 4.0 * standard_error

    assert spread[1024] > 7.0 * spread[16]


@pytest.mark.slow
def test_two_box_equilibrium_spread_scales_as_one_over_sqrt_n():
    """σ_n/N = 1/(2 sqrt(N)) for the Ehrenfest urn, the same law as the pressure fluctuation."""
    rng = np.random.default_rng(5150)
    sizes = [100, 400, 1600, 6400]
    spreads = []
    for n in sizes:
        occupancy = multiplicity.sample_two_box(n, n_steps=60 * n, rng=rng, n_in_first_state=n // 2)
        late = occupancy[len(occupancy) // 2 :]
        spreads.append(float(late.std() / n))

    assert scaling_exponent(sizes, spreads) == pytest.approx(-0.5, abs=0.12)


def test_the_first_law_ledger_is_extensive_while_the_state_ratios_are_not():
    """Doubling N at fixed T and V/N doubles W, Q and ΔU and leaves every ratio alone.

    This is the large-N statement for macroscopic thermodynamics, and it is worth measuring
    rather than assuming: the exponent of W against N is fitted, so a stray N inside gamma or
    inside a temperature ratio would show up as an exponent that is not 1.
    """
    sizes = [500, 1000, 2000, 4000, 8000]
    works, ratios = [], []
    for n in sizes:
        start = processes.EquilibriumState.from_temperature(n, 300.0, n * 1e-6)
        result = processes.adiabatic(start, 2.0 * start.volume)
        works.append(abs(result.work_on_gas))
        ratios.append(result.end.temperature / start.temperature)

    assert scaling_exponent(sizes, works) == pytest.approx(1.0, abs=1e-6)
    assert np.ptp(ratios) / np.mean(ratios) < 1e-12


def test_the_three_adiabatic_routes_keep_their_ordering_at_every_system_size():
    """The 189 / 225 / 300 K ordering is a statement about the process, not about N.

    Every temperature here is intensive, so the whole comparison must be flat in N. If any of
    the three drifted with system size, an extensive quantity would have leaked into a place
    where only ratios belong.
    """
    finals = []
    for n in (100, 1000, 10000, 100000):
        start = processes.EquilibriumState.from_temperature(n, 300.0, n * 1e-6)
        load = processes.external_pressure_for_equilibrium_at(start, 2.0)
        finals.append(
            (
                processes.adiabatic(start, 2.0 * start.volume).end.temperature,
                processes.adiabatic_against_constant_pressure(start, load).end.temperature,
                processes.free_expansion(start, 2.0 * start.volume).end.temperature,
            )
        )
        assert finals[-1][0] < finals[-1][1] < finals[-1][2]

    columns = np.array(finals)
    for column in columns.T:
        assert np.ptp(column) / column.mean() < 1e-12


def test_carnot_efficiency_does_not_move_with_the_size_of_the_engine():
    """N cancels out of the efficiency: it multiplies Q_h and Q_c identically.

    The large-N statement for this module is not a fluctuation law — an engine here is
    thermodynamics, with no microstates to fluctuate — but an *extensivity* one: the heats
    scale with N and their ratio does not, over four decades of engine size.
    """
    for n_particles in (10, 100, 1000, 10_000, 100_000):
        cycle = engines.carnot_cycle(n_particles, 600.0, 300.0, 1e-3, 2.5)
        assert relative_error(cycle.efficiency, 0.5) < 1e-12


def test_the_heats_themselves_scale_linearly_with_the_number_of_particles():
    """Q_h = N k_B T_h ln(r): doubling the working substance doubles what it moves.

    Measured as a fitted exponent rather than asserted, so a stray N^2 or a missing N fails
    loudly instead of hiding inside a ratio that cancels it either way.

    The range spans four decades because that is what the module page claims of it; a test
    covering two would leave the page's "over four decades" unbacked.
    """
    sizes = np.array([10.0, 100.0, 1000.0, 10_000.0, 100_000.0])
    heats = np.array(
        [engines.carnot_cycle(int(n), 600.0, 300.0, 1e-3, 2.5).heat_absorbed for n in sizes]
    )

    assert relative_error(scaling_exponent(sizes, heats), 1.0) < 1e-6


def test_entropy_production_scales_with_the_engine_but_its_relative_cost_does_not():
    """A bigger sloppy engine wastes proportionally more, not proportionally worse.

    The production is extensive; the efficiency shortfall it corresponds to is intensive.
    Keeping those two apart is what makes "entropy produced per cycle" a usable number.
    """
    sizes = np.array([100.0, 1000.0, 10_000.0])
    cycles = [
        engines.endoreversible_cycle(int(n), 600.0, 300.0, 1e-3, 2.5, 40.0, 25.0)
        for n in sizes
    ]
    produced = np.array([c.entropy_produced for c in cycles])

    assert relative_error(scaling_exponent(sizes, produced), 1.0) < 1e-6
    for cycle in cycles:
        assert relative_error(cycle.efficiency, cycles[0].efficiency) < 1e-12


# ---------------------------------------------------------------------------
# Module 09: the maximum sharpens, and production is extensive
# ---------------------------------------------------------------------------


def exact_partition_width(scale: int) -> tuple[float, float]:
    """Mean and standard deviation of q_a under P(q_a) ~ Omega_A Omega_B, exactly counted."""
    n_a, n_b = 3 * scale, scale
    total = 20 * (n_a + n_b)
    q = np.arange(total + 1)
    log_weight = (equilibrium.einstein_log_multiplicity(q, n_a)
                  + equilibrium.einstein_log_multiplicity(total - q, n_b))
    weight = np.exp(log_weight - log_weight.max())
    weight /= weight.sum()
    mean = float((q * weight).sum())
    return mean, float(np.sqrt(((q - mean) ** 2 * weight).sum()))


def test_the_total_entropy_peak_narrows_as_n_to_the_minus_one_half():
    """Why the maximum is all that matters: its relative width falls as N^(-1/2)."""
    scales = np.array([25, 100, 400, 1600])
    widths = []
    for scale in scales:
        mean, spread = exact_partition_width(int(scale))
        widths.append(spread / mean)

    assert abs(scaling_exponent(4 * scales, widths) + 0.5) < 0.02


def test_the_entropy_produced_by_contact_is_extensive():
    """Double both bodies at the same temperatures and the entropy produced doubles."""
    quantum = 5.0 * K_B
    produced = []
    for scale in (100, 200, 400):
        state = equilibrium.from_temperatures(3 * scale, scale, 500.0, 250.0, quantum)
        produced.append(fundamental.contact_entropy_production(
            state.heat_capacity_a, state.temperature_a,
            state.heat_capacity_b, state.temperature_b) / scale)
    assert relative_error(produced[0], produced[-1]) < 1e-2


def test_the_ledgers_final_value_is_relatively_sharper_for_bigger_bodies():
    """Seed-to-seed spread of the plateau is O(k_B) while its mean grows ~N: relative ~ 1/N."""
    quantum = 5.0 * K_B
    sizes, relative_spreads = [], []
    for scale in (25, 100, 400):
        finals = []
        for seed in range(8):
            state = equilibrium.from_temperatures(3 * scale, scale, 500.0, 250.0, quantum)
            result = equilibrium.simulate_energy_exchange(state, 8 * state.total_quanta,
                                                          np.random.default_rng(seed))
            finals.append(equilibrium.entropy_produced(result)[-1])
        finals = np.array(finals)
        sizes.append(4 * scale)
        relative_spreads.append(finals.std(ddof=1) / finals.mean())

    exponent = scaling_exponent(sizes, relative_spreads)
    assert exponent < -0.6  # at least as fast as N^(-1/2); the argument above says ~ -1


# ---------------------------------------------------------------------------
# Module 10: the potentials are extensive
# ---------------------------------------------------------------------------

ARGON_10 = fundamental.monatomic_ideal_gas(ARGON_MASS)
VDW_10 = potentials.van_der_waals_gas(ARGON_MASS, 0.1355 / 6.02214076e23**2,
                                      3.201e-5 / 6.02214076e23)


@pytest.mark.parametrize("relation", [ARGON_10, VDW_10])
def test_helmholtz_doubles_when_the_system_doubles(relation):
    """F(T, 2V, 2N) = 2 F(T, V, N) across three decades of N."""
    for n in (1e19, 1e21, 1e23):
        v = n * K_B * 300.0 / 1e5
        single = potentials.helmholtz_from(relation, 300.0, v, n)
        double = potentials.helmholtz_from(relation, 300.0, 2 * v, 2 * n)
        assert relative_error(double, 2 * single) < 1e-9


def test_gibbs_and_enthalpy_double_when_the_system_doubles():
    for n in (1e19, 1e22):
        g1 = potentials.gibbs_from(VDW_10, 300.0, 1e6, n)
        g2 = potentials.gibbs_from(VDW_10, 300.0, 1e6, 2 * n)
        assert relative_error(g2, 2 * g1) < 1e-7
        s = float(ARGON_10(1.5 * n * K_B * 300.0, n * K_B * 300.0 / 1e5, n))
        h1 = potentials.enthalpy_from(ARGON_10, s, 1e5, n)
        h2 = potentials.enthalpy_from(ARGON_10, 2 * s, 1e5, 2 * n)
        assert relative_error(h2, 2 * h1) < 1e-7


def test_the_joule_thomson_cooling_does_not_depend_on_how_much_gas_is_throttled():
    """An intensive answer: the temperature drop across the plug is the same for any N."""
    drops = [potentials.throttle(VDW_10, n, 300.0, 20e5, 1e5).temperature_change
             for n in (1e20, 1e22, 1e24)]
    assert relative_error(drops[0], drops[-1]) < 1e-6
    assert drops[0] < 0


# ---------------------------------------------------------------------------
# Module 11: an infinite bath is an approximation with an error bar
# ---------------------------------------------------------------------------

QUANTUM_11 = 1.0e-21
BATH_SIZES_11 = [20, 40, 80, 160, 320, 640]


@pytest.mark.parametrize("quanta_per_oscillator", [0.5, 1.0, 2.0])
def test_the_finite_bath_error_falls_as_one_over_the_bath_size(quanta_per_oscillator):
    """Doubling the bath at fixed temperature halves the gap to the Boltzmann curve."""
    sweep = ensembles.bath_size_sweep(ensembles.two_level(1, QUANTUM_11), BATH_SIZES_11,
                                      quanta_per_oscillator)
    alpha = scaling_exponent(sweep.n_bath, sweep.distances)

    assert abs(alpha + 1.0) < 0.02, f"sup-norm exponent {alpha:.4f}"
    halving = sweep.distances[:-1] / sweep.distances[1:]
    assert np.all(np.abs(halving - 2.0) < 0.03)


def test_the_finite_bath_error_of_a_small_solid_also_falls_as_one_over_the_bath_size():
    sweep = ensembles.bath_size_sweep(ensembles.einstein_levels(3, 40, QUANTUM_11),
                                      BATH_SIZES_11, 1.0)
    assert abs(scaling_exponent(sweep.n_bath, sweep.distances) + 1.0) < 0.02


def test_the_measured_correction_tracks_the_predicted_curvature_term():
    """ln P beyond -beta E is -E^2 / (2 k_B T^2 C_bath), up to a relative 1/N_bath."""
    levels = ensembles.einstein_levels(3, 6, QUANTUM_11)
    misfit = []
    for n in (50, 100, 200, 400, 800):
        joint = ensembles.enumerate_joint(levels, n, n)
        measured = ensembles.measured_log_correction(joint)[1:]
        predicted = ensembles.predicted_log_correction(joint)[1:]
        assert np.all(measured < 0) and np.all(predicted < 0)
        misfit.append(float(np.max(np.abs(measured / predicted - 1.0))))
        # The correction itself shrinks as 1/N: n times it is fixed.
        assert relative_error(n * float(predicted[0]), -1.0 / 4.0) < 2.0 / n

    assert misfit[-1] < 5e-3  # the remainder is relatively ~ E_s / U_bath: largest at k = 6
    assert abs(scaling_exponent([50, 100, 200, 400, 800], misfit) + 1.0) < 0.05


def test_a_canonical_solids_relative_energy_spread_falls_as_n_to_the_minus_one_half():
    """Advanced: why canonical and microcanonical agree for a big enough system."""
    temperature = ensembles.bath_temperature(1.0, QUANTUM_11)
    sizes = [4, 16, 64, 256]
    spreads = []
    for n in sizes:
        levels = ensembles.einstein_levels(n, int(n + 40 * np.sqrt(n) + 60), QUANTUM_11)
        mean, spread = ensembles.energy_moments(levels, temperature)
        spreads.append(spread / mean)

    assert abs(scaling_exponent(sizes, spreads) + 0.5) < 1e-6


def test_the_exact_bath_temperature_reaches_the_infinite_bath_value_as_one_over_n():
    target = np.log(2.0)
    gaps = [abs(ensembles.bath_beta_exact(n, n, QUANTUM_11) * QUANTUM_11 - target)
            for n in BATH_SIZES_11]
    assert abs(scaling_exponent(BATH_SIZES_11, gaps) + 1.0) < 0.02


# ---------------------------------------------------------------------------
# Module 12: partition functions
# ---------------------------------------------------------------------------

MU_12 = 9.274e-24


def test_the_paramagnets_relative_energy_fluctuation_falls_as_n_to_the_minus_half():
    """sqrt(Var E) / |U| from the second derivative of ln Z, across four decades of N."""
    sizes = [10, 100, 1000, 10_000, 100_000]
    temperature = np.array([1.0])
    ratios = []
    for n in sizes:
        rebuilt = partition.thermo_from_z(
            lambda t, n=n: partition.log_z_paramagnet(n, MU_12, 1.0, t), temperature)
        ratios.append(float(np.sqrt(rebuilt.energy_variance[0]) / abs(rebuilt.energy[0])))
    assert abs(scaling_exponent(sizes, ratios) + 0.5) < 1e-4


def test_ln_z_of_independent_spins_is_additive():
    for temperature in (0.3, 3.0, 30.0):
        one = partition.log_z_paramagnet(1, MU_12, 1.0, temperature)
        many = partition.log_z_paramagnet(4096, MU_12, 1.0, temperature)
        assert relative_error(many, 4096 * one) < 1e-13


def test_the_spin_entropy_peak_approaches_n_k_ln_2_per_spin():
    """ln C(N, N/2) = N ln 2 - (1/2) ln(pi N / 2) + ...: the shortfall per spin ~ ln N / N."""
    shortfall = []
    sizes = [100, 1000, 10_000, 100_000]
    for n in sizes:
        spins = partition.spin_entropy_of_energy(n, MU_12, 1.0)
        per_spin = spins.entropy.max() / (n * K_B)
        shortfall.append(np.log(2.0) - per_spin)
        assert relative_error(n * np.log(2.0) - spins.entropy.max() / K_B,
                              0.5 * np.log(np.pi * n / 2)) < 0.01
    assert shortfall == sorted(shortfall, reverse=True)


# ---------------------------------------------------------------------------
# Module 13: chemical potential
# ---------------------------------------------------------------------------


def test_mu_difference_fluctuations_shrink_as_n_to_the_minus_half():
    """At equilibrium mu_a - mu_b jitters by ~k_B T / sqrt(N): exactly, from the distribution."""
    kt = K_B * 300.0
    sizes = [100, 1000, 10_000, 100_000]
    spreads = []
    for n in sizes:
        boxes = chemical.two_boxes(100 * n, 100 * n, 0.0, 2.0 * kt)
        spreads.append(chemical.exact_count_distribution(boxes, n, 300.0).mu_difference_std())
    assert abs(scaling_exponent(sizes, spreads) + 0.5) < 0.01


def test_the_relative_split_fluctuation_falls_as_n_to_the_minus_half():
    kt = K_B * 300.0
    sizes = [100, 1000, 10_000, 100_000]
    relative = []
    for n in sizes:
        boxes = chemical.two_boxes(100 * n, 100 * n, 0.0, kt)
        dist = chemical.exact_count_distribution(boxes, n, 300.0)
        relative.append(dist.std / dist.mean)
    assert abs(scaling_exponent(sizes, relative) + 0.5) < 0.01


# ---------------------------------------------------------------------------
# Module 14: phase coexistence
# ---------------------------------------------------------------------------
# No particle number appears anywhere in `phases`: it analyses an intensive equation of
# state, so the large-N category has nothing to measure here. What scales instead is the
# substance -- a and b set the units of the critical point and nothing else -- and the test
# below records that the coexistence curve is one curve across four decades of both.


def test_the_reduced_coexistence_curve_is_independent_of_a_and_b():
    a_0, b_0 = gases.vdw_constants_from_critical(304.13, 7.3773e6)
    t_r = np.linspace(0.5, 0.99, 25)
    reference = None
    for scale_a, scale_b in ((1.0, 1.0), (1e-2, 1e-1), (1e2, 1e1), (1e2, 1e-2)):
        a, b = scale_a * a_0, scale_b * b_0
        v_c, t_c, p_c = gases.vdw_critical_point(a, b)
        p_sat, v_l, v_g = phases.coexistence_curve(t_r * t_c, a, b)
        reduced = np.stack([p_sat / p_c, v_l / v_c, v_g / v_c,
                            phases.latent_heat(t_r * t_c, a, b) / (K_B * t_c)])
        if reference is None:
            reference = reduced
        assert np.all(np.abs(reduced / reference - 1.0) < 1e-10)


# ---------------------------------------------------------------------------
# Module 15: the Ising model
# ---------------------------------------------------------------------------


def test_disordered_magnetization_falls_as_n_to_the_minus_half():
    """Above T_c spins are correlated over a finite length, so |m| is a sum of effectively
    independent blocks: <|m|> ~ N^(-1/2), the module-03 law, at T = 4 J."""
    sizes = np.array([8, 16, 32])
    means = []
    for size in sizes:
        rng = np.random.default_rng(int(size))
        m, _, _ = ising.simulate(ising.random_state(int(size), rng), 4.0, 2000, rng,
                                 burn_in=100)
        means.append(np.abs(m).mean())
    assert abs(scaling_exponent(sizes**2, means) + 0.5) < 0.05


def test_branch_crossings_die_out_as_the_lattice_grows():
    """Below T_c a small lattice hops between +m and -m; a larger one at the same T stays
    put for the whole run. The ensemble average is zero; the sample is not."""
    temperature = 2.0
    flips = []
    for size in (8, 16):
        rng = np.random.default_rng(15)
        m, _, _ = ising.simulate(ising.aligned_state(size), temperature, 10_000, rng,
                                 burn_in=0)
        flips.append(ising.branch_flips(m))
    assert flips[0] >= 3
    assert flips[1] == 0


@pytest.mark.slow
def test_the_susceptibility_peak_grows_and_drifts_toward_onsager():
    """chi' peaks higher and closer to T_c as L grows: 8, 16, 32. The growth exponent is
    gamma/nu = 7/4 in the limit; at these sizes we demand only that it is clearly positive,
    and that the peak approaches T_c from above."""
    temperatures = np.linspace(2.2, 2.9, 15)
    heights, locations = [], []
    for size in (8, 16, 32):
        rng = np.random.default_rng(size)
        scan = ising.temperature_scan(size, temperatures[::-1], 4000, rng, burn_in=500)[::-1]
        chi = np.array([r.susceptibility for r in scan])
        heights.append(chi.max())
        locations.append(temperatures[chi.argmax()])
    assert heights[0] < heights[1] < heights[2]
    assert scaling_exponent([8, 16, 32], heights) > 1.0
    assert locations[0] > locations[2] >= ising.onsager_tc() - 0.05
