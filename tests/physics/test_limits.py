"""Accuracy category 3: known analytic cases and limiting regimes.

Every simulation in the course exists to make a derivation tangible, so each one is pinned
against the result it is supposed to reproduce: the ideal gas law from wall impulses, the
closed-form work integrals along standard paths, equipartition, and the Gaussian limit of
the binomial multiplicity.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import (
    equilibrium,
    forms,
    gases,
    kinetics,
    multiplicity,
    paths,
    sampling,
)
from thermolab.constants import K_B
from thermolab.validation import relative_error, seed_study

pytestmark = pytest.mark.analytic_limit

ARGON_MASS = 39.948 * 1.66053906660e-27
BOX_2D = (1e-6, 1e-6)


def measure_pressure(
    rng: np.random.Generator, n_particles: int = 400, temperature: float = 300.0
) -> float:
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
    predicted = [(0.5 * np.log(np.pi * n) - np.log(2.0)) / (2.0 * n * np.log(2.0)) for n in sizes]
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
    assert paths.ideal_gas_temperature(500, 1e5, 1e-3) == pytest.approx(1e5 * 1e-3 / (500 * K_B))


def test_kinetics_and_paths_ideal_gas_functions_are_gases_by_identity():
    """C4a dedup: kinetics.py and paths.py re-import gases.py's functions rather than
    redefining them, so the check is object identity, not merely equal output."""
    assert kinetics.ideal_gas_pressure is gases.ideal_gas_pressure
    assert paths.ideal_gas_pressure is gases.ideal_gas_pressure
    assert paths.ideal_gas_temperature is gases.ideal_gas_temperature


def test_die_mean_and_variance_match_the_hand_calculation():
    """μ = 7/2 and σ² = 35/12 are the numbers a student works out by summing six terms."""
    assert sampling.die_mean(6) == pytest.approx(3.5, rel=1e-12)
    assert sampling.die_variance(6) == pytest.approx(35.0 / 12.0, rel=1e-12)

    faces = np.arange(1, 7, dtype=float)
    assert sampling.die_mean(6) == pytest.approx(float(faces.mean()))
    assert sampling.die_variance(6) == pytest.approx(float(((faces - faces.mean()) ** 2).mean()))


def test_a_one_faced_die_has_no_spread_at_all():
    """The degenerate limit: a certain outcome has zero variance, so nothing to average away."""
    assert sampling.die_variance(1) == 0.0
    assert sampling.die_relative_spread(1) == 0.0
    assert sampling.predicted_relative_spread(1000, n_faces=1) == 0.0


def test_sample_average_converges_on_the_die_mean():
    """The law of large numbers as the module states it, with an error bar attached."""
    study = seed_study(
        lambda rng: float(sampling.sample_averages(2000, 20, rng).mean()), n_seeds=8
    )

    assert study.agrees_with(sampling.die_mean(6), n_sigma=3.0), (
        f"measured {study.mean:.5g} +/- {study.standard_error:.2g}"
    )


def test_single_die_relative_spread_is_the_coefficient_of_the_law():
    """σ₁/μ₁ ≈ 0.488 is the number in front of N^(-1/2), not a fitted fudge factor."""
    assert sampling.die_relative_spread(6) == pytest.approx(np.sqrt(35.0 / 12.0) / 3.5, rel=1e-12)
    assert sampling.predicted_relative_spread(100) == pytest.approx(
        sampling.die_relative_spread(6) / 10.0, rel=1e-12
    )


def test_inexact_form_gives_a_different_answer_on_every_route():
    """ω = y dx is not the differential of anything, and three routes prove it by disagreeing.

    Same start, same finish, three answers — 0, 1/2 and 1. This is the mathematics that
    module 5 will meet again as "work is a path function".
    """
    m, n = (lambda x, y: y), (lambda x, y: np.zeros_like(x))
    t = np.linspace(0.0, 1.0, 801)
    zero, one = np.zeros_like(t), np.ones_like(t)

    along_the_diagonal = forms.line_integral(m, n, t, t)
    across_then_up = forms.line_integral(m, n, t, zero) + forms.line_integral(m, n, one, t)
    up_then_across = forms.line_integral(m, n, zero, t) + forms.line_integral(m, n, t, one)

    assert along_the_diagonal == pytest.approx(0.5, abs=1e-9)
    assert across_then_up == pytest.approx(0.0, abs=1e-9)
    assert up_then_across == pytest.approx(1.0, abs=1e-9)


def test_mixed_partials_decide_exactness_without_integrating():
    """The criterion agrees with the integrals above: ω₁ is exact, ω₂ is not."""
    x = np.linspace(0.2, 2.0, 25)
    y = np.linspace(0.3, 1.7, 25)

    exact_gap = forms.mixed_partials_gap(lambda x, y: y, lambda x, y: x, x, y)
    inexact_gap = forms.mixed_partials_gap(lambda x, y: y, lambda x, y: np.zeros_like(x), x, y)

    assert np.allclose(exact_gap, 0.0, atol=1e-8)
    assert np.allclose(inexact_gap, 1.0, atol=1e-8)
    assert forms.is_exact(lambda x, y: y, lambda x, y: x, x, y)
    assert not forms.is_exact(lambda x, y: y, lambda x, y: np.zeros_like(x), x, y)


EQUILIBRIUM_QUANTUM = 20.0 * K_B


def make_equilibrium_state():
    """A modest pair whose relaxation time (~4400 steps) keeps the tests below quick."""
    return equilibrium.from_temperatures(150, 50, 500.0, 250.0, EQUILIBRIUM_QUANTUM)


def test_equilibrium_temperature_matches_simple_known_cases():
    """Equal heat capacities give the plain average; a dominant one pulls T_eq toward itself."""
    assert equilibrium.equilibrium_temperature(5.0, 400.0, 5.0, 300.0) == pytest.approx(350.0)
    assert equilibrium.equilibrium_temperature(1e6, 400.0, 1.0, 100.0) == pytest.approx(
        400.0, rel=1e-4
    )


def test_long_run_average_temperature_reaches_the_equilibrium_temperature():
    """The point of the module: a random exchange settles at (C_A T_A + C_B T_B)/(C_A+C_B)."""
    state = make_equilibrium_state()
    target = equilibrium.equilibrium_temperature(
        state.heat_capacity_a, state.temperature_a, state.heat_capacity_b, state.temperature_b
    )
    n_steps = int(8 * equilibrium.relaxation_time(state))

    def measure(rng: np.random.Generator) -> float:
        return float(equilibrium.simulate_energy_exchange(state, n_steps, rng).temperature_a[-1])

    study = seed_study(measure, n_seeds=12)
    assert study.agrees_with(target, n_sigma=3.5)


def test_mean_trajectory_matches_the_predicted_relaxation_curve():
    """The stochastic exchange's mean gap at one relaxation time matches the closed form exactly."""
    state = make_equilibrium_state()
    checkpoint = int(equilibrium.relaxation_time(state))
    predicted = float(equilibrium.predicted_relaxation(state, np.array([checkpoint]))[0])

    def measure(rng: np.random.Generator) -> float:
        result = equilibrium.simulate_energy_exchange(state, checkpoint, rng)
        return float(result.temperature_a[-1] - result.temperature_b[-1])

    study = seed_study(measure, n_seeds=16)
    assert study.agrees_with(predicted, n_sigma=3.5)


ARGON_A = 3.736e-49  # Pa m^6, per molecule (argon a_molar / N_A**2)
ARGON_B = 5.317e-29  # m^3, per molecule (argon b_molar / N_A)


def test_van_der_waals_pressure_at_a_b_zero_matches_the_ideal_gas_law_exactly():
    """At a = b = 0, gases.van_der_waals_pressure(v, ...) reduces to k_B T / v, which is exactly
    paths.ideal_gas_pressure(N, T, V) evaluated at the same state, v = V / N."""
    n_particles, temperature, volume = 1000, 300.0, 1e-3
    v = volume / n_particles
    ideal = paths.ideal_gas_pressure(n_particles, temperature, volume)

    vdw = gases.van_der_waals_pressure(v, temperature, 0.0, 0.0)

    assert relative_error(float(vdw), ideal) < 1e-12


def test_van_der_waals_pressure_converges_to_the_ideal_gas_law_as_a_and_b_shrink():
    """Real argon at STP-like density deviates from the ideal gas law by order 1e-3; shrinking
    its a, b by successive decades should shrink that deviation by roughly the same factor --
    the genuine a, b -> 0 limit, as opposed to the exact-zero sanity check above.
    """
    n_particles, temperature, volume = 5.0e22, 300.0, 2.0e-3
    v = volume / n_particles
    ideal = paths.ideal_gas_pressure(n_particles, temperature, volume)

    errors = []
    for factor in (1.0, 0.1, 0.01, 0.001):
        vdw = gases.van_der_waals_pressure(v, temperature, ARGON_A * factor, ARGON_B * factor)
        errors.append(relative_error(float(vdw), ideal))

    assert errors == sorted(errors, reverse=True)  # monotonically shrinking
    assert errors[0] < 1e-2  # real argon is already close to ideal at these conditions
    assert errors[-1] < 1e-4  # a thousandth of its a, b is utterly negligible


def test_compressibility_factor_approaches_one_as_v_grows():
    """Z = P v / (k_B T) -> 1 in the dilute limit, for any real gas -- the definition of "ideal"."""
    temperature = 300.0
    v_values = np.array([1e-2, 1.0, 1e2, 1e4])
    pressures = gases.van_der_waals_pressure(v_values, temperature, ARGON_A, ARGON_B)
    z = gases.compressibility_factor(pressures, v_values, temperature)

    errors = [relative_error(float(value), 1.0) for value in z]
    assert errors == sorted(errors, reverse=True)  # monotonically shrinking
    assert errors[-1] < 1e-6


def test_critical_point_matches_known_argon_values():
    """Argon's measured critical point is T_c = 150.9 K, P_c = 4.87 MPa (CRC values); the
    molecule-scale a, b converted from the textbook molar constants should reproduce it."""
    v_c, t_c, p_c = gases.vdw_critical_point(ARGON_A, ARGON_B)

    assert relative_error(t_c, 150.9) < 0.02
    assert relative_error(p_c, 4.87e6) < 0.02
    assert v_c > 0.0


def test_pressure_at_the_critical_point_equals_the_predicted_critical_pressure():
    """The closed-form P_c must be exactly what the pressure formula gives at (v_c, T_c)."""
    v_c, t_c, p_c = gases.vdw_critical_point(ARGON_A, ARGON_B)

    pressure_here = gases.van_der_waals_pressure(v_c, t_c, ARGON_A, ARGON_B)

    assert relative_error(float(pressure_here), p_c) < 1e-10


def test_critical_compressibility_factor_is_exactly_three_eighths():
    """Z_c = P_c v_c / (k_B T_c) = 3/8 for every van der Waals substance -- the model's one
    universal, substance-independent number (real gases scatter around 0.23-0.31)."""
    v_c, t_c, p_c = gases.vdw_critical_point(ARGON_A, ARGON_B)

    z_c = gases.compressibility_factor(p_c, v_c, t_c)

    assert relative_error(float(z_c), 3.0 / 8.0) < 1e-12


def test_reduced_pressure_equals_one_at_the_critical_point():
    """The parameter-free law of corresponding states evaluated at its own reference point."""
    assert relative_error(float(gases.vdw_pressure_reduced(1.0, 1.0)), 1.0) < 1e-12


def test_vdw_constants_from_critical_inverts_vdw_critical_point():
    """Fitting a, b from a critical point and reading the critical point back off them must
    round-trip exactly -- the two functions are algebraic inverses of one another."""
    v_c, t_c, p_c = gases.vdw_critical_point(ARGON_A, ARGON_B)

    a_fit, b_fit = gases.vdw_constants_from_critical(t_c, p_c)

    assert relative_error(a_fit, ARGON_A) < 1e-10
    assert relative_error(b_fit, ARGON_B) < 1e-10


@pytest.mark.parametrize("name", ["pm1", "biased", "uniform", "heavy"])
def test_walk_mean_and_variance_match_the_additivity_result(name):
    """<x_t> = mu_1 t and Var(x_t) = sigma_1^2 t, for any finite-variance step.

    This is module 00's additivity theorem read with t in the place of N, and it is the whole
    analytic content of a random walk. Four very different step distributions are checked
    because the claim is that only the first two moments of a step survive into the answer.
    """
    dist = sampling.step_distribution(name)
    rng = np.random.default_rng(4242)
    trajectories = sampling.random_walk(8000, 512, rng, step=dist)

    for t in (8, 64, 512):
        column = trajectories[:, t]
        standard_error = dist.std * np.sqrt(t / column.size)
        assert abs(float(column.mean()) - dist.mean * t) < 4.0 * standard_error
        assert relative_error(float(column.var(ddof=1)), dist.variance * t) < 0.08


def test_rescaling_every_step_rescales_the_spread_by_the_same_factor():
    """The dimensionless module's substitute for a dimensional check.

    Positions are counted in steps, so there is no unit to verify with pint. What can be
    verified is homogeneity: sigma_1 enters the answer linearly, so measuring a walk in units
    of half a step must give exactly half the spread — no offset, no stray additive term.
    """
    rng = np.random.default_rng(606)
    trajectories = sampling.random_walk(4000, 256, rng, step="uniform")

    spread = sampling.walker_spread(trajectories)
    halved = sampling.walker_spread(0.5 * trajectories)

    assert np.allclose(halved, 0.5 * spread, rtol=1e-12)


def _neighbour_alternation(centres: np.ndarray, density: np.ndarray) -> float:
    """Mean |d_i / mean(neighbours) - 1| across the core: ~0 for a smooth curve.

    A plain peak-to-peak spread will not do here — it is dominated by the genuine curvature of
    the distribution across the window. Comparing each bin with the average of its two
    neighbours cancels anything smooth and leaves only the bin-to-bin zigzag.
    """
    core = np.abs(centres) < 1.5
    values = density[core]
    return float(np.mean(np.abs(values[1:-1] / (0.5 * (values[:-2] + values[2:])) - 1.0)))


@pytest.mark.parametrize("n_terms", [250, 600])
def test_lattice_bins_leave_only_sampling_noise_between_neighbouring_bins(n_terms):
    """The regression guard for a bug that made the CLT animation contradict its own caption.

    Standardized coin sums live on a lattice of spacing 2/sqrt(n) — an irrational number, so
    a bin edge computed by repeated addition and a site computed by division disagree in their
    last bits. If the grid is offset so that sites can land *on* edges, which side each one
    falls to is then decided by that rounding, bins pick up 1, 2 or 3 sites at random, and the
    histogram alternates by tens of percent with nothing physical behind it. Rendered, that
    reads as the coin walk visibly refusing to converge — the opposite of what the module
    claims — while every number in the test suite stays green, because the sums themselves
    were never wrong.

    The bug is invisible on an integer lattice, where edges and sites are both exact. So the
    check is made here, in the standardized coordinates where it actually lives, against the
    shot noise of the bin populations rather than against a hand-picked constant.
    """
    z = sampling.clt_sum_distribution(n_terms, 20_000, np.random.default_rng(17), step="pm1")
    span, n_bins = (-4.0, 4.0), 49

    centres, density = sampling.walker_histogram(
        z, n_bins=n_bins, span=span, lattice=2.0 / np.sqrt(n_terms)
    )
    width = float(centres[1] - centres[0])
    core = np.abs(centres) < 1.5

    assert np.all(density[core] > 0.0), "an aligned bin in the core is empty"

    shot_noise = float(np.mean(1.0 / np.sqrt(density[core] * width * 20_000)))
    aligned = _neighbour_alternation(centres, density)
    unaligned = _neighbour_alternation(*sampling.walker_histogram(z, n_bins=n_bins, span=span))

    assert aligned < 3.0 * shot_noise, (
        f"n = {n_terms}: aligned bins alternate by {aligned:.1%}, shot noise {shot_noise:.1%}"
    )
    assert unaligned > 2.0 * aligned, (
        f"n = {n_terms}: alignment bought nothing ({unaligned:.1%} vs {aligned:.1%})"
    )


def test_lattice_binned_density_reproduces_the_exact_binomial():
    """With one site per bin the histogram is the pmf, so it can be checked against theory.

    This is the payoff of aligning the bins: each bar now corresponds to a definite set of
    reachable positions, so its height is a probability with a closed form rather than an
    artefact of where the edges happened to fall.
    """
    n_steps = 200
    rng = np.random.default_rng(9)
    positions = sampling.random_walk(40_000, n_steps, rng)[:, -1]

    centres, density = sampling.walker_histogram(
        positions, n_bins=201, span=(-40.0, 40.0), lattice=2.0
    )
    width = float(centres[1] - centres[0])
    assert width == pytest.approx(2.0)

    _, pmf, _ = sampling.binomial_to_gaussian(n_steps, 0.5)
    core = np.abs(centres) < 20.0
    for centre, measured in zip(centres[core], (density * width)[core], strict=True):
        exact = float(pmf[int(round((centre + n_steps) / 2))])
        standard_error = np.sqrt(exact * (1 - exact) / 40_000)
        assert abs(measured - exact) < 5.0 * standard_error, (
            f"bin at x = {centre}: measured {measured:.5f}, exact {exact:.5f}"
        )


def test_binomial_approaches_its_gaussian_as_n_grows():
    """de Moivre-Laplace, measured: the worst-case gap to the Gaussian shrinks with n.

    Comparing pmf against density needs the lattice spacing, which is 1 in k. The comparison
    is restricted to the central few sigma, where the theorem actually claims accuracy — the
    far tails are relatively wrong at every n, which is a separate and honest limitation.
    """
    worst = []
    for n in (25, 100, 400):
        k, pmf, gaussian = sampling.binomial_to_gaussian(n, 0.5)
        sigma = np.sqrt(n * 0.25)
        central = np.abs(k - n * 0.5) <= 3.0 * sigma
        worst.append(float(np.max(np.abs(pmf[central] - gaussian[central])) * sigma))

    assert worst[0] > worst[1] > worst[2]
    assert worst[-1] < 0.01


def test_de_moivre_laplace_peak_matches_the_closed_form():
    """At k = np the Gaussian is 1/sqrt(2 pi n p q); for n = 100, p = 1/2 that is 1/sqrt(50 pi).

    The exact binomial peak is 0.0796 against the approximation's 0.0798 — under a third of a
    percent, and the number the module's quiz asks a student to reproduce by hand.
    """
    k, pmf, gaussian = sampling.binomial_to_gaussian(100, 0.5)
    peak = int(np.argmin(np.abs(k - 50.0)))

    assert float(gaussian[peak]) == pytest.approx(1.0 / np.sqrt(50.0 * np.pi), rel=1e-12)
    assert relative_error(float(gaussian[peak]), float(pmf[peak])) < 0.005


def test_a_persistent_walk_with_zero_persistence_is_an_ordinary_walk():
    """q = 0 must recover the independent-step walk exactly in distribution.

    A counterexample is only worth something if it agrees with the thing it contradicts in
    the limit where they should agree; otherwise the disagreement at q = 0.95 could be a bug.
    """
    plain = sampling.random_walk(6000, 400, np.random.default_rng(7))
    persistent = sampling.correlated_walk(6000, 400, 0.0, np.random.default_rng(8))

    assert relative_error(
        float(sampling.walker_spread(persistent)[-1]),
        float(sampling.walker_spread(plain)[-1]),
    ) < 0.05


def test_persistent_walk_variance_is_inflated_by_the_correlation_factor():
    """Correlated steps do not destroy the sqrt(t) law; they change its coefficient.

    Successive steps have correlation exactly q, so summing the correlations gives
    Var(x_t) -> t (1 + q)/(1 - q) at long times. Quoting the number is what turns "the CLT
    failed" into "the independence hypothesis failed, and here is precisely what it cost".
    """
    rng = np.random.default_rng(2024)
    n_steps = 800

    for q in (0.5, 0.9):
        trajectories = sampling.correlated_walk(6000, n_steps, q, rng)
        measured = float(trajectories[:, -1].var(ddof=1))
        assert relative_error(measured, n_steps * (1.0 + q) / (1.0 - q)) < 0.12
