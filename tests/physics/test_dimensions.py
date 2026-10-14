"""Accuracy category 1: dimensional consistency.

The library works in plain SI floats so students can read the formulas. These tests
re-evaluate the same expressions with pint quantities, so a wrong power of a variable fails
loudly even when the number looks plausible.

One module has nothing to check here. Module 03's random walks are deliberately physics-free:
positions are counted in steps and steps are pure numbers, so there is no dimension for a
pint quantity to carry. Its analogue of this category is the *homogeneity* check in
test_limits.py — rescaling every step rescales the spread by the same factor — which is what
a dimensional argument reduces to once the units are gone.
"""

from __future__ import annotations

import numpy as np
import pytest

from thermolab import (
    chemical,
    engines,
    ensembles,
    equilibrium,
    forms,
    fundamental,
    gases,
    ising,
    kinetics,
    multiplicity,
    partition,
    paths,
    phases,
    potentials,
    processes,
    quantum,
    radiation,
    sampling,
    transport,
)
from thermolab.constants import AMU, N_A
from thermolab.units import K_B_Q, Quantity
from thermolab.validation import relative_error

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
        (sampling.die_mean(6), float),
        (sampling.die_variance(6), float),
        (sampling.predicted_relative_spread(100), float),
        (equilibrium.equilibrium_temperature(150.0, 500.0, 50.0, 250.0), float),
    ],
)
def test_library_functions_return_plain_si_floats(value, expected_dimension):
    """The library itself stays unit-free by design; pint lives in the tests only."""
    assert isinstance(value, expected_dimension)


def test_both_terms_of_a_one_form_must_carry_the_same_dimensions():
    """M dx + N dy is only meaningful when the two products agree — the rule behind δW = -P dV.

    Adding a pressure-times-volume to a temperature-times-entropy works because both are
    energies; adding a pressure to an energy would not, and pint says so.
    """
    m_dx = Quantity(1e5, "Pa") * Quantity(1e-3, "m**3")
    n_dy = Quantity(2.0, "J / K") * Quantity(0.5, "K")

    assert m_dx.check("[energy]")
    assert n_dy.check("[energy]")
    assert (m_dx + n_dy).check("[energy]")


def test_a_relative_spread_is_dimensionless_and_survives_a_change_of_units():
    """σ carries the units of the quantity; σ/μ does not — the only scale-free "steadiness".

    Re-expressing every measurement in different units multiplies both σ and μ by the same
    factor, so the ratio is untouched. This is why the course compares fractional differences
    and never absolute ones.
    """
    rng = np.random.default_rng(4)
    averages = sampling.sample_averages(n_per_sample=32, n_samples=500, rng=rng)
    rescaled = 1.609344 * averages  # the same readings, quoted in another unit

    original = averages.std(ddof=1) / averages.mean()
    converted = rescaled.std(ddof=1) / rescaled.mean()

    assert converted == pytest.approx(original, rel=1e-12)


def test_line_integral_returns_a_plain_float():
    """`forms` is pure mathematics on plain numbers; units live in the physics that uses it."""
    x = np.linspace(0.0, 1.0, 65)
    value = forms.line_integral(lambda x, y: y, lambda x, y: np.zeros_like(x), x, x)

    assert isinstance(value, float)


def test_multiplicity_is_dimensionless():
    """Ω counts microstates — a pure number, whatever the system."""
    assert isinstance(multiplicity.multiplicity(20, 10), float)
    assert multiplicity.multiplicity(20, 10) > 1.0


def test_equilibrium_temperature_has_temperature_dimensions():
    """T_eq = (C_A T_A + C_B T_B) / (C_A + C_B): energy over heat capacity, back to temperature."""
    c_a = Quantity(2.0, "J/K")
    c_b = Quantity(5.0, "J/K")
    t_a = Quantity(400.0, "K")
    t_b = Quantity(300.0, "K")
    t_eq = (c_a * t_a + c_b * t_b) / (c_a + c_b)
    assert t_eq.check("[temperature]")


def test_heat_capacity_of_an_einstein_solid_is_energy_per_temperature():
    """C = n k_B in the model's classical limit -- a count of oscillators times k_B."""
    n_oscillators = 300
    heat_capacity = n_oscillators * K_B_Q
    assert heat_capacity.check("[energy] / [temperature]")


def test_quantum_times_quanta_count_is_an_energy():
    """E = q * quantum -- a dimensionless count of quanta times one quantum's energy."""
    quantum = Quantity(2.76e-22, "J")
    n_quanta = 500
    assert (n_quanta * quantum).check("[energy]")


def test_van_der_waals_pressure_has_pressure_dimensions():
    """P = k_B T/(v - b) - a/v^2: both terms must independently be a pressure.

    `v` is the per-particle volume V/N, matching `gases.van_der_waals_pressure`'s signature.
    """
    v = Quantity(1e-3, "m**3")
    temperature = Quantity(300.0, "K")
    a = Quantity(3.736e-49, "Pa * m**6")
    b = Quantity(5.317e-29, "m**3")

    excluded_volume_term = K_B_Q * temperature / (v - b)
    attraction_term = a / v**2
    assert excluded_volume_term.check("[pressure]")
    assert attraction_term.check("[pressure]")
    assert (excluded_volume_term - attraction_term).check("[pressure]")


def test_vdw_critical_point_quantities_have_the_right_dimensions():
    """v_c = 3b, k_B T_c = 8a/(27 b), P_c = a/(27 b^2) -- one dimension check each."""
    a = Quantity(3.736e-49, "Pa * m**6")
    b = Quantity(5.317e-29, "m**3")
    v_c = 3 * b
    t_c = 8 * a / (27 * K_B_Q * b)
    p_c = a / (27 * b**2)
    assert v_c.check("[volume]")
    assert t_c.check("[temperature]")
    assert p_c.check("[pressure]")


def test_compressibility_factor_is_dimensionless():
    """Z = P v / (k_B T) -- a ratio of two pressures, or two volumes; either way, a pure number."""
    pressure = Quantity(1e5, "Pa")
    v = Quantity(1e-3, "m**3")
    temperature = Quantity(300.0, "K")
    z = pressure * v / (K_B_Q * temperature)
    assert z.dimensionless


def test_gases_functions_return_plain_si_floats():
    """The library itself stays unit-free by design, same as every other module here."""
    v_c, t_c, p_c = gases.vdw_critical_point(3.736e-49, 5.317e-29)
    assert isinstance(v_c, float)
    assert isinstance(t_c, float)
    assert isinstance(p_c, float)


def test_heat_capacities_are_energy_per_temperature():
    """C_V = (f/2) N k_B and C_P = C_V + N k_B: k_B carries the units, the counts do not."""
    n_particles, degrees_of_freedom = 1000, 3
    c_v = 0.5 * degrees_of_freedom * n_particles * K_B_Q
    c_p = c_v + n_particles * K_B_Q

    assert c_v.check("[energy] / [temperature]")
    assert c_p.check("[energy] / [temperature]")
    assert (c_p - c_v).check("[energy] / [temperature]")


def test_the_heat_capacity_ratio_is_dimensionless():
    """gamma = C_P/C_V is a pure number, which is what lets it sit in an exponent at all.

    An exponent that carried units would be meaningless, so this is the dimensional statement
    behind P V^gamma = constant being writable in the first place.
    """
    c_v = 1.5 * 1000 * K_B_Q
    c_p = 2.5 * 1000 * K_B_Q
    assert (c_p / c_v).dimensionless


def test_irreversible_work_against_a_constant_load_is_an_energy():
    """W_on = -P_ext ΔV. The external pressure is still a pressure, so the product is energy."""
    work = Quantity(9.35e4, "Pa") * Quantity(1e-2, "m**3")
    assert work.check("[energy]")


def test_the_constant_load_final_temperature_formula_is_a_temperature():
    """T_2 = (C_V T_1 + P_ext V_1)/C_P: an energy over a heat capacity, back to a temperature.

    Both terms in the numerator must independently be energies, which is exactly the check
    that catches a dropped volume or a C_V written where a C_P belongs.
    """
    c_v = Quantity(12.47, "J/K")
    c_p = Quantity(20.79, "J/K")
    stored = c_v * Quantity(300.0, "K")
    displaced = Quantity(9.35e4, "Pa") * Quantity(1e-2, "m**3")

    assert stored.check("[energy]")
    assert displaced.check("[energy]")
    assert ((stored + displaced) / c_p).check("[temperature]")


def test_processes_functions_return_plain_si_floats():
    """`processes` stays unit-free like the rest of the library; pint lives in the tests."""
    state = processes.EquilibriumState.from_temperature(1000, 300.0, 1e-3)
    result = processes.adiabatic(state, 2e-3)

    assert isinstance(processes.heat_capacity_constant_volume(1000), float)
    assert isinstance(processes.heat_capacity_constant_pressure(1000), float)
    assert isinstance(processes.gamma_from_dof(3), float)
    assert isinstance(state.temperature, float)
    assert isinstance(state.internal_energy, float)
    assert isinstance(result.work_on_gas, float)
    assert isinstance(result.first_law_residual, float)


def test_an_efficiency_is_dimensionless():
    """eta = 1 - T_c/T_h is a ratio of temperatures, so the result is a pure number.

    Worth stating dimensionally because the most common wrong form of this expression — one
    of the two temperatures left in Celsius — is not a ratio of absolute temperatures at all,
    and the ratio it does form is not the dimensionless quantity this check describes.
    """
    t_hot = Quantity(600.0, "K")
    t_cold = Quantity(300.0, "K")

    assert (t_cold / t_hot).dimensionless
    assert (1 - t_cold / t_hot).dimensionless


def test_a_coefficient_of_performance_is_dimensionless():
    """Heat moved per unit work: energy over energy, whatever the number comes out as."""
    lifted = Quantity(4.2e3, "J")
    driven = Quantity(1.4e3, "J")
    assert (lifted / driven).dimensionless


def test_the_clausius_sum_is_energy_per_temperature():
    """A sum of Q/T carries entropy's dimensions — which is what lets it define one."""
    total = Quantity(4.2e3, "J") / Quantity(600.0, "K") - Quantity(2.1e3, "J") / Quantity(
        300.0, "K"
    )
    assert total.check("[energy] / [temperature]")


def test_entropy_change_of_a_stroke_is_energy_per_temperature():
    """N k_B ln(V2/V1) + C_V ln(T2/T1): both terms must land on J/K independently.

    The logarithms are dimensionless because their arguments are ratios, so each term is a
    heat capacity times a pure number. A dropped k_B in either term fails here.
    """
    volume_term = 1000 * K_B_Q * float(np.log(2.0))
    thermal_term = 1.5 * 1000 * K_B_Q * float(np.log(1.4))

    assert volume_term.check("[energy] / [temperature]")
    assert thermal_term.check("[energy] / [temperature]")
    assert (volume_term + thermal_term).check("[energy] / [temperature]")


def test_engines_functions_return_plain_si_floats():
    """`engines` stays unit-free like the rest of the library; pint lives in the tests."""
    cycle = engines.carnot_cycle(1000, 600.0, 300.0, 1e-3, 2.5)

    assert isinstance(engines.carnot_efficiency(600.0, 300.0), float)
    assert isinstance(engines.cop_refrigerator(600.0, 300.0), float)
    assert isinstance(engines.cop_heat_pump(600.0, 300.0), float)
    assert isinstance(engines.curzon_ahlborn_efficiency(600.0, 300.0), float)
    assert isinstance(engines.otto_efficiency(9.0, 1.4), float)
    assert isinstance(cycle.efficiency, float)
    assert isinstance(cycle.work_output, float)
    assert isinstance(cycle.clausius_sum, float)


# ---------------------------------------------------------------------------
# Module 09: the fundamental relation
# ---------------------------------------------------------------------------

PLANCK_Q = Quantity(6.62607015e-34, "joule * second")


def test_the_sackur_tetrode_logarithm_is_dimensionless():
    """(V/N) (4 pi m U / (3 N h^2))^(3/2): a wrong power of h or m would leave a unit behind."""
    volume = Quantity(1e-3, "m**3")
    energy = Quantity(10.0, "J")
    mass = Quantity(6.6e-26, "kg")
    n = 1e22
    argument = (volume / n) * (4 * np.pi * mass * energy / (3 * n * PLANCK_Q**2)) ** 1.5
    assert argument.to("dimensionless").check("[]")


def test_the_entropy_slopes_are_inverse_temperature_pressure_over_temperature_and_mu_over_t():
    entropy = Quantity(1.0, "J/K")
    assert (entropy / Quantity(1.0, "J")).check("1/[temperature]")
    assert (entropy / Quantity(1.0, "m**3")).check("[pressure]/[temperature]")
    # N is a pure count, so -T dS/dN is an energy per particle.
    assert (Quantity(300.0, "K") * entropy / 1.0).check("[energy]")


def test_the_einstein_closed_form_temperature_is_a_temperature():
    quantum = Quantity(6.9e-23, "J")
    temperature = quantum / (K_B_Q * np.log1p(300 * 1.0 / 20.0))
    assert temperature.check("[temperature]")


def test_the_heat_capacity_from_curvature_is_energy_per_temperature():
    """C = -1/(T^2 d^2S/dU^2): (J/K) / (K^2 * (J/K)/J^2) = J/K."""
    curvature = Quantity(-1.0, "J/K") / Quantity(1.0, "J") ** 2
    capacity = -1.0 / (Quantity(300.0, "K") ** 2 * curvature)
    assert capacity.check("[energy]/[temperature]")


def test_contact_entropy_production_is_energy_per_temperature():
    capacity = Quantity(4184.0, "J/K")
    produced = capacity * np.log(320.0 / 350.0) + capacity * np.log(320.0 / 290.0)
    assert produced.check("[energy]/[temperature]")


def test_fundamental_functions_return_plain_si_floats():
    gas = fundamental.monatomic_ideal_gas(6.6e-26)
    point = (6.2, 4.1e-2, 1e21)
    assert isinstance(fundamental.temperature_of(gas, *point), float)
    assert isinstance(fundamental.pressure_of(gas, *point), float)
    assert isinstance(fundamental.chemical_potential_of(gas, *point), float)
    assert isinstance(fundamental.heat_capacity_of(gas, *point), float)
    assert isinstance(fundamental.euler_residual(gas, *point), float)
    assert isinstance(fundamental.contact_entropy_production(1.0, 300.0, 2.0, 200.0), float)
    assert isinstance(equilibrium.total_entropy(
        equilibrium.from_temperatures(30, 10, 400.0, 200.0, 7e-23)), float)


def test_the_compressibility_from_the_entropy_hessian_is_an_inverse_pressure():
    """kappa_T = -S_UU / (V T (S_UU S_VV - S_UV^2)) -- in the units the Hessian carries."""
    s_uu = Quantity(-1.0, "J/K") / Quantity(1.0, "J") ** 2
    s_vv = Quantity(-1.0, "J/K") / Quantity(1.0, "m**3") ** 2
    s_uv = Quantity(0.1, "J/K") / (Quantity(1.0, "J") * Quantity(1.0, "m**3"))
    kappa = -s_uu / (Quantity(1.0, "m**3") * Quantity(300.0, "K") * (s_uu * s_vv - s_uv**2))
    assert kappa.check("1/[pressure]")


# ---------------------------------------------------------------------------
# Module 10: thermodynamic potentials
# ---------------------------------------------------------------------------

# Per-particle van der Waals constants for argon (a_molar / N_A^2, b_molar / N_A).
VDW_A_Q = Quantity(0.1355 / 6.02214076e23**2, "Pa * m**6")
VDW_B_Q = Quantity(3.201e-5 / 6.02214076e23, "m**3")


def test_the_van_der_waals_logarithm_is_dimensionless():
    """The attraction term a N^2 / V must be an energy, or U + a N^2/V is meaningless."""
    volume = Quantity(1e-3, "m**3")
    n = 1e22
    attraction = VDW_A_Q * n**2 / volume
    assert attraction.check("[energy]")
    kinetic = Quantity(10.0, "J") + attraction
    thermal = 4 * np.pi * Quantity(6.6e-26, "kg") * kinetic / (3 * n * PLANCK_Q**2)
    argument = ((volume - n * VDW_B_Q) / n) * thermal**1.5
    assert argument.to("dimensionless").check("[]")


def test_every_potential_is_an_energy():
    u, t, s = Quantity(3741.5, "J"), Quantity(300.0, "K"), Quantity(155.0, "J/K")
    p, v = Quantity(1e5, "Pa"), Quantity(0.0249, "m**3")
    for potential in (u + p * v, u - t * s, u - t * s + p * v):
        assert potential.check("[energy]")


def test_each_maxwell_relation_equates_quantities_of_one_dimension():
    s, t = Quantity(1.0, "J/K"), Quantity(1.0, "K")
    v, p = Quantity(1.0, "m**3"), Quantity(1.0, "Pa")
    assert (t / v).dimensionality == (p / s).dimensionality  # from U
    assert (t / p).dimensionality == (v / s).dimensionality  # from H
    assert (s / v).dimensionality == (p / t).dimensionality  # from F
    assert (s / p).dimensionality == (v / t).dimensionality  # from G
    # The rubber band's: (dS/dL)_T = -(df/dT)_L, entropy per length against force per kelvin.
    assert (s / Quantity(1.0, "m")).dimensionality == (Quantity(1.0, "N") / t).dimensionality


def test_entropy_from_a_pressure_gauge_is_an_entropy():
    """Integral of (dP/dT)_V dV: (Pa/K) m^3 = J/K, from instruments that measure no entropy."""
    slope = Quantity(330.0, "Pa/K")
    assert (slope * Quantity(1e-3, "m**3")).check("[energy]/[temperature]")


def test_the_joule_thomson_coefficient_is_a_temperature_per_pressure():
    """(2a/(k_B T) - b) / c_P per particle: m^3 / (J/K) = K/Pa."""
    c_p = 2.5 * K_B_Q
    coefficient = (2 * VDW_A_Q / (K_B_Q * Quantity(300.0, "K")) - VDW_B_Q) / c_p
    assert coefficient.check("[temperature]/[pressure]")


def test_potentials_functions_return_plain_si_floats():
    gas = fundamental.monatomic_ideal_gas(6.6e-26)
    n = 1e22
    ledger = potentials.ledger_at(gas, 300.0, 4e-4, n)
    assert isinstance(potentials.helmholtz_from(gas, 300.0, 4e-4, n), float)
    assert isinstance(potentials.gibbs_from(gas, 300.0, 1e5, n), float)
    assert isinstance(potentials.enthalpy_from(gas, ledger.entropy, 1e5, n), float)
    assert isinstance(ledger.gibbs, float)
    assert potentials.helmholtz_from(gas, np.array([300.0, 400.0]), 4e-4, n).shape == (2,)
    # The ledger closes: U = F + TS, in joules, to rounding.
    assert abs(ledger.energy - (ledger.helmholtz + ledger.ts)) <= 1e-12 * abs(ledger.energy)


# ---------------------------------------------------------------------------
# Module 11: the Boltzmann factor
# ---------------------------------------------------------------------------

QUANTUM_11 = 1.0e-21


def test_the_boltzmann_exponent_is_dimensionless():
    """E / (k_B T) must be a pure number, or exp(-E / k_B T) means nothing."""
    exponent = Quantity(3 * QUANTUM_11, "J") / (K_B_Q * Quantity(104.5, "K"))
    assert exponent.to("dimensionless").check("[]")


def test_beta_is_an_inverse_energy_that_scales_inversely_with_the_quantum():
    """Homogeneity: the same count on quanta twice as large is half as steep per joule."""
    beta = ensembles.beta_of_bath(200, 200, QUANTUM_11)
    assert relative_error(ensembles.beta_of_bath(200, 200, 2 * QUANTUM_11), beta / 2) < 1e-14
    assert relative_error(ensembles.bath_beta_exact(200, 200, 2 * QUANTUM_11),
                          ensembles.bath_beta_exact(200, 200, QUANTUM_11) / 2) < 1e-14
    # 1 / (k_B beta) must come out a temperature.
    temperature = 1 / (K_B_Q * Quantity(beta, "1/J"))
    assert temperature.check("[temperature]")
    assert relative_error(ensembles.bath_temperature(1.0, 2 * QUANTUM_11),
                          2 * ensembles.bath_temperature(1.0, QUANTUM_11)) < 1e-14


def test_the_bath_curvature_is_an_inverse_energy_squared():
    """d^2 ln Omega / dU^2 = -1 / (k_B T^2 C): each side is 1/J^2."""
    heat_capacity = Quantity(200.0, "") * K_B_Q
    side = 1 / (K_B_Q * Quantity(100.0, "K") ** 2 * heat_capacity)
    assert side.check("1/[energy]**2")
    assert relative_error(ensembles.bath_curvature_exact(200, 200, 2 * QUANTUM_11),
                          ensembles.bath_curvature_exact(200, 200, QUANTUM_11) / 4) < 1e-14


def test_the_boltzmann_distribution_is_a_set_of_pure_probabilities():
    levels = ensembles.einstein_levels(3, 60, QUANTUM_11)
    p = ensembles.boltzmann_distribution(levels, 150.0)
    assert p.dtype == float
    assert abs(p.sum() - 1.0) < 1e-12
    assert np.all(p >= 0)
    # Rescaling every energy and the temperature together changes nothing.
    rescaled = ensembles.einstein_levels(3, 60, 3 * QUANTUM_11)
    assert np.max(np.abs(ensembles.boltzmann_distribution(rescaled, 450.0) - p)) < 1e-14


def test_ensembles_functions_return_plain_si_floats():
    two = ensembles.two_level(1, QUANTUM_11)
    joint = ensembles.enumerate_joint(two, 50, 50)
    assert isinstance(ensembles.beta_of_bath(50, 50, QUANTUM_11), float)
    assert isinstance(ensembles.bath_temperature(1.0, QUANTUM_11), float)
    assert isinstance(joint.log_total_multiplicity, float)
    mean, spread = ensembles.energy_moments(two, 100.0)
    assert isinstance(mean, float) and isinstance(spread, float)
    assert two.energies.dtype == float


# ---------------------------------------------------------------------------
# Module 12: partition functions
# ---------------------------------------------------------------------------

QUANTUM_12 = 1.0e-21
MU_12 = 9.274e-24  # J/T, one Bohr magneton


def test_every_exponent_inside_a_partition_function_is_dimensionless():
    """mu B / (k_B T) and hbar omega / (k_B T) must be pure numbers, or ln Z means nothing."""
    zeeman = Quantity(MU_12, "J/T") * Quantity(1.0, "T") / (K_B_Q * Quantity(2.0, "K"))
    oscillator = Quantity(QUANTUM_12, "J") / (K_B_Q * Quantity(300.0, "K"))
    assert zeeman.to("dimensionless").check("[]")
    assert oscillator.to("dimensionless").check("[]")


def test_magnetization_is_a_magnetic_moment_and_the_curie_form_agrees():
    """M = N mu tanh(...) and the Curie form N mu^2 B / (k_B T) both come out in J/T."""
    curie = 1000 * Quantity(MU_12, "J/T") ** 2 * Quantity(0.1, "T") / (
        K_B_Q * Quantity(300.0, "K"))
    assert curie.check("[energy]/[magnetic_field]") or curie.check("[current]*[area]")
    value = partition.curie_magnetization(1000, MU_12, 0.1, 300.0)
    assert relative_error(value, curie.to("J/T").magnitude) < 1e-12


def test_the_thermal_wavelength_is_a_length():
    lam = Quantity(partition.PLANCK_H, "J*s") / (
        2 * np.pi * Quantity(6.6e-26, "kg") * K_B_Q * Quantity(300.0, "K")) ** 0.5
    assert lam.check("[length]")
    value = partition.thermal_wavelength(300.0, 6.6e-26)
    assert relative_error(value, lam.to("m").magnitude) < 1e-12


def test_rescaling_every_level_and_the_temperature_together_rescales_only_energies():
    """Homogeneity: ln Z, S and C depend on E/(k_B T) only, U and F scale with the levels."""
    t = np.array([50.0, 150.0, 400.0])
    one = partition.thermo_from_z(lambda x: partition.log_z_harmonic(QUANTUM_12, x), t)
    three = partition.thermo_from_z(lambda x: partition.log_z_harmonic(3 * QUANTUM_12, x), 3 * t)
    assert np.max(np.abs(three.log_z - one.log_z)) < 1e-12
    assert np.max(np.abs(three.energy / (3 * one.energy) - 1)) < 1e-8
    assert np.max(np.abs(three.free_energy / (3 * one.free_energy) - 1)) < 1e-12
    assert np.max(np.abs(three.entropy / one.entropy - 1)) < 1e-8
    assert np.max(np.abs(three.heat_capacity / one.heat_capacity - 1)) < 1e-6


def test_partition_functions_return_plain_si_floats():
    assert isinstance(partition.log_z_two_level(QUANTUM_12, 100.0), float)
    assert isinstance(partition.log_z_paramagnet(100, MU_12, 1.0, 2.0), float)
    assert isinstance(partition.log_z_harmonic(QUANTUM_12, 100.0), float)
    assert isinstance(partition.log_z_harmonic(QUANTUM_12, 100.0, n_max=50), float)
    assert isinstance(partition.harmonic_temperature(2 * QUANTUM_12, QUANTUM_12), float)
    assert partition.log_z_harmonic(QUANTUM_12, np.array([10.0, 20.0]), n_max=50).shape == (2,)
    sums = partition.level_sums([0.0, QUANTUM_12], 100.0)
    assert isinstance(sums.energy, float) and isinstance(sums.entropy, float)


# ---------------------------------------------------------------------------
# Module 13: chemical potential
# ---------------------------------------------------------------------------

ARGON_13 = 39.95 * 1.66053906660e-27  # kg


def test_the_chemical_potential_is_an_energy_per_particle():
    """k_B T ln(n / n_Q): the logarithm's argument must be a pure number, so mu is in joules."""
    lam = Quantity(partition.PLANCK_H, "J*s") / (
        2 * np.pi * Quantity(ARGON_13, "kg") * K_B_Q * Quantity(300.0, "K")) ** 0.5
    n_q = 1 / lam**3
    assert n_q.check("1/[length]**3")
    ratio = Quantity(2.4e25, "1/m**3") / n_q
    assert ratio.to("dimensionless").check("[]")
    mu = K_B_Q * Quantity(300.0, "K") * np.log(ratio.to("dimensionless").magnitude)
    assert mu.check("[energy]")
    value = chemical.ideal_gas_mu(2.4e25, 300.0, ARGON_13)
    assert relative_error(value, mu.to("J").magnitude) < 1e-12
    assert relative_error(chemical.quantum_concentration(300.0, ARGON_13),
                          n_q.to("1/m**3").magnitude) < 1e-12


def test_van_t_hoff_osmotic_pressure_is_a_pressure():
    """Pi = n_s k_B T: a number density times an energy is a pressure."""
    pi = Quantity(6.0e25, "1/m**3") * K_B_Q * Quantity(298.0, "K")
    assert pi.check("[pressure]")
    assert relative_error(chemical.osmotic_pressure(6.0e25, 298.0), pi.to("Pa").magnitude) < 1e-12
    lattice = K_B_Q * Quantity(298.0, "K") / Quantity(chemical.WATER_MOLECULAR_VOLUME, "m**3")
    assert lattice.check("[pressure]")


def test_every_exponent_in_the_occupation_and_mass_action_laws_is_dimensionless():
    x = (Quantity(3e-21, "J") - Quantity(1e-21, "J")) / (K_B_Q * Quantity(300.0, "K"))
    assert x.to("dimensionless").check("[]")
    assert 0.0 < chemical.site_occupation(1e-21, 300.0, 3e-21) < 0.5


def test_chemical_functions_return_plain_si_floats():
    boxes = chemical.two_boxes(1000, 1000, 0.0, 1e-21)
    assert isinstance(chemical.ideal_gas_mu(1e25, 300.0, ARGON_13), float)
    assert isinstance(chemical.quantum_concentration(300.0, ARGON_13), float)
    assert isinstance(chemical.site_occupation(0.0, 300.0, 1e-21), float)
    assert isinstance(chemical.mass_action_ratio(1e-21, 300.0), float)
    assert isinstance(chemical.osmotic_pressure(1e25, 300.0), float)
    assert isinstance(chemical.relaxation_steps(boxes, 100, 300.0), float)
    mu, counts = chemical.occupation_equilibrium(boxes, 100, 300.0)
    assert isinstance(mu, float) and counts.shape == (2,)
    assert chemical.ideal_gas_mu(np.array([1e24, 1e25]), 300.0, ARGON_13).shape == (2,)


# ---------------------------------------------------------------------------
# Module 14: phase coexistence
# ---------------------------------------------------------------------------

CO2_A_14, CO2_B_14 = gases.vdw_constants_from_critical(304.13, 7.3773e6)


def test_the_maxwell_construction_returns_a_pressure_and_two_volumes():
    """P_sat is P_c times a pure number and each v is v_c times one, so the units are those
    of the critical point -- which pint builds from a and b alone."""
    a = Quantity(CO2_A_14, "Pa * m**6")
    b = Quantity(CO2_B_14, "m**3")
    p_c, v_c, t_c = a / (27 * b**2), 3 * b, 8 * a / (27 * K_B_Q * b)
    assert p_c.check("[pressure]") and v_c.check("[volume]") and t_c.check("[temperature]")
    v_c_value, t_c_value, p_c_value = gases.vdw_critical_point(CO2_A_14, CO2_B_14)
    assert relative_error(p_c_value, p_c.to("Pa").magnitude) < 1e-12
    assert relative_error(t_c_value, t_c.to("K").magnitude) < 1e-12
    p_sat, v_l, v_g = phases.maxwell_construction(280.0, CO2_A_14, CO2_B_14)
    assert 0.0 < p_sat < p_c_value
    assert CO2_B_14 < v_l < v_c_value < v_g


def test_the_latent_heat_is_an_energy_per_particle_by_both_routes():
    """k_B T ln((v_g - b)/(v_l - b)) takes the log of a volume ratio; Delta u + P Delta v adds
    a pressure times a volume to a / v, and a / v is Pa m^6 / m^3 = J."""
    t = 280.0
    p_sat, v_l, v_g = phases.maxwell_construction(t, CO2_A_14, CO2_B_14)
    b = Quantity(CO2_B_14, "m**3")
    ratio = (Quantity(v_g, "m**3") - b) / (Quantity(v_l, "m**3") - b)
    assert ratio.to("dimensionless").check("[]")
    from_entropy = K_B_Q * Quantity(t, "K") * np.log(ratio.to("dimensionless").magnitude)
    assert from_entropy.check("[energy]")
    assert relative_error(phases.latent_heat(t, CO2_A_14, CO2_B_14),
                          from_entropy.to("J").magnitude) < 1e-12
    delta_u = Quantity(CO2_A_14, "Pa * m**6") * (1 / Quantity(v_l, "m**3")
                                                 - 1 / Quantity(v_g, "m**3"))
    from_first_law = delta_u + Quantity(p_sat, "Pa") * Quantity(v_g - v_l, "m**3")
    assert from_first_law.check("[energy]")
    assert relative_error(phases.latent_heat_from_first_law(t, CO2_A_14, CO2_B_14),
                          from_first_law.to("J").magnitude) < 1e-12


def test_the_clausius_clapeyron_slope_is_a_pressure_per_kelvin():
    t = 280.0
    _, v_l, v_g = phases.maxwell_construction(t, CO2_A_14, CO2_B_14)
    slope = Quantity(phases.latent_heat(t, CO2_A_14, CO2_B_14), "J") / (
        Quantity(t, "K") * Quantity(v_g - v_l, "m**3"))
    assert slope.check("[pressure] / [temperature]")
    _, predicted = phases.clausius_clapeyron_check(t, CO2_A_14, CO2_B_14)
    assert relative_error(predicted, slope.to("Pa / K").magnitude) < 1e-12


def test_the_van_der_waals_chemical_potential_is_an_energy():
    """-k_B T ln((v - b)/b) + k_B T b/(v - b) - 2a/v: each term is J once (v - b)/b is a number."""
    v, t = 2.0 * CO2_B_14, 280.0
    b = Quantity(CO2_B_14, "m**3")
    free = (Quantity(v, "m**3") - b) / b
    assert free.to("dimensionless").check("[]")
    kt = K_B_Q * Quantity(t, "K")
    mu = (-kt * np.log(free.to("dimensionless").magnitude) + kt / free.to("dimensionless").magnitude
          - 2 * Quantity(CO2_A_14, "Pa * m**6") / Quantity(v, "m**3"))
    assert mu.check("[energy]")
    assert relative_error(phases.vdw_chemical_potential(v, t, CO2_A_14, CO2_B_14),
                          mu.to("J").magnitude) < 1e-12


def test_phases_functions_return_plain_si_floats_and_shaped_arrays():
    p_sat, v_l, v_g = phases.maxwell_construction(280.0, CO2_A_14, CO2_B_14)
    assert all(isinstance(x, float) for x in (p_sat, v_l, v_g))
    assert isinstance(phases.latent_heat(280.0, CO2_A_14, CO2_B_14), float)
    assert isinstance(phases.equilibrium_volume(3.0e6, 280.0, CO2_A_14, CO2_B_14), float)
    x_l, x_g = phases.lever_rule(0.5 * (v_l + v_g), v_l, v_g)
    assert isinstance(x_l, float) and isinstance(x_g, float)
    grid = np.array([270.0, 280.0, 290.0])
    assert all(np.shape(x) == (3,) for x in phases.maxwell_construction(grid, CO2_A_14, CO2_B_14))
    assert np.shape(phases.latent_heat(grid, CO2_A_14, CO2_B_14)) == (3,)
    assert all(np.shape(x) == (3,) for x in phases.coexistence_curve(grid, CO2_A_14, CO2_B_14))
    assert isinstance(phases.phase_rule(1, 2), int)


# ---------------------------------------------------------------------------
# Module 15: the Ising model
# ---------------------------------------------------------------------------
# `ising` is the course's one licensed exception to SI: energies in units of J, temperature
# as k_B T / J, field as h / J (plans/15-ising.md section 7). Critical behaviour is where the
# material constants scale out, so the module computes in those units and k_B returns only
# when a number is quoted for a material. The dimensional content of the convention is that
# every quantity the module computes is a pure number, and that restoring J and k_B turns
# the reduced critical temperature into a temperature.


def test_an_aligned_square_lattice_has_two_bonds_per_spin():
    """E = -J * (2N bonds) for all spins up: the reduced-units anchor, an exact integer."""
    for size in (4, 8, 16):
        state = ising.aligned_state(size)
        assert state.energy == -2 * size**2
        assert state.e == -2.0
        assert state.m == 1.0
    chain = ising.aligned_state(8, dimension=1)
    assert chain.energy == -8  # a ring has one bond per spin


def test_restoring_j_and_k_b_turns_the_reduced_t_c_into_a_temperature():
    coupling = Quantity(2.0e-21, "J")  # a typical exchange energy, about 12 meV
    t_c = ising.onsager_tc() * coupling / K_B_Q
    assert t_c.check("[temperature]")
    assert 300.0 < t_c.to("K").magnitude < 340.0


def test_the_fluctuation_identities_are_pure_numbers_in_reduced_units():
    """c = N Var(e) / T^2 is dimensionless once energies are in J and T in J / k_B; with the
    units restored the same identity, C = Var(E) / (k_B T^2), is an energy per temperature."""
    reduced_variance = Quantity(0.01, "J**2") / Quantity(1.0, "J**2")
    reduced_t = Quantity(2.0, "J") / Quantity(1.0, "J")
    assert (100 * reduced_variance / reduced_t**2).check("[]")
    heat_capacity = Quantity(0.01, "J**2") / (K_B_Q * Quantity(300.0, "K") ** 2)
    assert heat_capacity.check("[energy] / [temperature]")


# ---------------------------------------------------------------------------
# Module 16: radiation and solids
# ---------------------------------------------------------------------------

H_Q = Quantity(radiation.PLANCK_H, "J*s")
C_Q = Quantity(radiation.C_LIGHT, "m/s")


def test_every_exponent_in_planck_s_law_is_dimensionless():
    """h nu / (k_B T) and h c / (lambda k_B T) must be pure numbers, in either variable."""
    by_frequency = H_Q * Quantity(5e14, "Hz") / (K_B_Q * Quantity(5772.0, "K"))
    by_wavelength = H_Q * C_Q / (Quantity(500e-9, "m") * K_B_Q * Quantity(5772.0, "K"))
    assert by_frequency.to("dimensionless").check("[]")
    assert by_wavelength.to("dimensionless").check("[]")


def test_planck_u_nu_is_an_energy_per_volume_per_hertz():
    nu, t = Quantity(1e14, "Hz"), Quantity(3000.0, "K")
    x = (H_Q * nu / (K_B_Q * t)).to("dimensionless").magnitude
    u_nu = 8 * np.pi * H_Q * nu**3 / C_Q**3 / np.expm1(x)
    assert u_nu.check("[energy] / [length]**3 * [time]")
    assert relative_error(radiation.planck_u_nu(1e14, 3000.0),
                          u_nu.to("J*s/m**3").magnitude) < 1e-12


def test_planck_u_lambda_is_an_energy_per_volume_per_metre():
    lam, t = Quantity(1e-6, "m"), Quantity(3000.0, "K")
    x = (H_Q * C_Q / (lam * K_B_Q * t)).to("dimensionless").magnitude
    u_lambda = 8 * np.pi * H_Q * C_Q / lam**5 / np.expm1(x)
    assert u_lambda.check("[energy] / [length]**4")
    assert relative_error(radiation.planck_u_lambda(1e-6, 3000.0),
                          u_lambda.to("J/m**4").magnitude) < 1e-12


def test_the_radiation_constant_and_stefan_boltzmann_constant_carry_their_units():
    a = 8 * np.pi**5 * K_B_Q**4 / (15 * H_Q**3 * C_Q**3)
    sigma = a * C_Q / 4
    assert a.check("[energy] / [length]**3 / [temperature]**4")
    assert sigma.check("[power] / [length]**2 / [temperature]**4")
    assert relative_error(radiation.RADIATION_CONSTANT, a.to("J/m**3/K**4").magnitude) < 1e-12
    # CODATA 2018's exact sigma, since h, k_B and c are all exact in SI 2019.
    assert relative_error(radiation.STEFAN_BOLTZMANN, 5.670374419e-8) < 1e-9


def test_the_wien_constant_is_a_length_times_a_temperature():
    b = H_Q * C_Q / (radiation.WIEN_X_LAMBDA * K_B_Q)
    assert b.check("[length] * [temperature]")
    assert relative_error(radiation.WIEN_B, 2.897771955e-3) < 1e-9


def test_photon_gas_quantities_carry_their_units():
    t = Quantity(300.0, "K")
    a = Quantity(radiation.RADIATION_CONSTANT, "J/m**3/K**4")
    u, s = a * t**4, 4 * a * t**3 / 3
    n = 16 * np.pi * radiation.ZETA_3 * (K_B_Q * t / (H_Q * C_Q)) ** 3
    assert u.check("[pressure]") and (u / 3).check("[pressure]")
    assert s.check("[energy] / [temperature] / [length]**3")
    assert n.check("1 / [length]**3")
    gas = radiation.photon_gas(300.0)
    assert relative_error(gas.energy_density, u.to("J/m**3").magnitude) < 1e-12
    assert relative_error(gas.entropy_density, s.to("J/K/m**3").magnitude) < 1e-12
    assert relative_error(gas.number_density, n.to("1/m**3").magnitude) < 1e-12


def test_solid_heat_capacities_are_energies_per_kelvin():
    """3 N k_B is an energy per kelvin; per mole it is 3R = 24.94 J/(mol K)."""
    dulong_petit = 3 * Quantity(N_A, "1/mol") * K_B_Q
    assert dulong_petit.check("[energy] / [temperature] / [substance]")
    hot = radiation.einstein_heat_capacity(1e6, 300.0, N_A)
    assert relative_error(hot, dulong_petit.to("J/K/mol").magnitude) < 1e-6


def test_a_debye_temperature_from_the_speed_of_sound_is_a_temperature():
    """theta_D = hbar (6 pi^2 N / V)^(1/3) c_s / k_B."""
    number_density = Quantity(5.86e28, "1/m**3")   # silver
    speed = Quantity(1740.0, "m/s")
    hbar = Quantity(radiation.H_BAR, "J*s")
    theta = hbar * (6 * np.pi**2 * number_density) ** (1 / 3) * speed / K_B_Q
    assert theta.check("[temperature]")
    value = radiation.debye_temperature(5.86e28, 1.0, 1740.0)
    assert relative_error(value, theta.to("K").magnitude) < 1e-12


def test_radiation_functions_return_plain_si_floats_and_shaped_arrays():
    assert isinstance(radiation.mode_occupation(1e-21, 300.0), float)
    assert isinstance(radiation.planck_u_nu(1e14, 3000.0), float)
    assert isinstance(radiation.planck_u_lambda(1e-6, 3000.0), float)
    assert isinstance(radiation.wien_peak_nu(300.0), float)
    assert isinstance(radiation.debye_heat_capacity(100.0, 300.0, N_A), float)
    assert isinstance(radiation.einstein_heat_capacity(100.0, 300.0, N_A), float)
    temps = np.array([10.0, 100.0, 1000.0])
    assert radiation.debye_heat_capacity(temps, 300.0, N_A).shape == (3,)
    assert radiation.planck_u_nu(np.linspace(0, 1e15, 5), 3000.0).shape == (5,)


# ---------------------------------------------------------------------------
# Module 17: quantum statistics
# ---------------------------------------------------------------------------

HBAR_Q = Quantity(partition.H_BAR, "J*s")
M_E_Q = Quantity(quantum.M_ELECTRON, "kg")
M_HE_Q = Quantity(quantum.M_HELIUM4, "kg")
N_CU_17 = 8.49e28   # copper's conduction electrons, one per atom [1/m^3]


def test_the_fermi_energy_is_an_energy_and_degeneracy_pressure_a_pressure():
    n = Quantity(N_CU_17, "1/m**3")
    k_f = (3 * np.pi**2 * n) ** (1 / 3)
    eps_f = HBAR_Q**2 * k_f**2 / (2 * M_E_Q)
    assert k_f.check("1 / [length]")
    assert eps_f.check("[energy]")
    assert (eps_f / K_B_Q).check("[temperature]")
    assert (HBAR_Q * k_f / M_E_Q).check("[length] / [time]")
    pressure = 2 / 5 * n * eps_f
    assert pressure.check("[pressure]")
    m_e = quantum.M_ELECTRON
    assert relative_error(quantum.fermi_energy(N_CU_17, m_e), eps_f.to("J").magnitude) < 1e-12
    assert relative_error(quantum.fermi_gas_pressure(N_CU_17, m_e),
                          pressure.to("Pa").magnitude) < 1e-12
    assert relative_error(quantum.fermi_velocity(N_CU_17, m_e),
                          (HBAR_Q * k_f / M_E_Q).to("m/s").magnitude) < 1e-12


def test_the_condensation_temperature_is_a_temperature():
    n = Quantity(2.2e28, "1/m**3")
    t_c = 2 * np.pi * HBAR_Q**2 / (M_HE_Q * K_B_Q) * (n / quantum.ZETA_3_2) ** (2 / 3)
    assert t_c.check("[temperature]")
    assert relative_error(quantum.bec_tc(2.2e28, quantum.M_HELIUM4), t_c.to("K").magnitude) < 1e-12


def test_the_density_of_states_counts_states_per_joule():
    volume, eps = Quantity(1e-6, "m**3"), Quantity(1e-22, "J")
    g = volume * (2 * M_HE_Q / HBAR_Q**2) ** 1.5 * eps**0.5 / (4 * np.pi**2)
    assert g.check("1 / [energy]")
    assert relative_error(quantum.density_of_states_3d(1e-22, 1e-6, quantum.M_HELIUM4),
                          g.to("1/J").magnitude) < 1e-12


def test_the_degeneracy_parameter_and_every_occupation_exponent_are_pure_numbers():
    n, t = Quantity(2.2e28, "1/m**3"), Quantity(2.0, "K")
    h = Quantity(radiation.PLANCK_H, "J*s")
    lam = h / (2 * np.pi * M_HE_Q * K_B_Q * t) ** 0.5
    assert lam.check("[length]")
    assert (n * lam**3).check("[]")
    assert relative_error(quantum.degeneracy_parameter(2.2e28, 2.0, quantum.M_HELIUM4),
                          (n * lam**3).to("dimensionless").magnitude) < 1e-12
    exponent = (Quantity(3e-23, "J") - Quantity(-1e-23, "J")) / (K_B_Q * t)
    assert exponent.check("[]")


def test_a_metals_electronic_coefficient_is_an_energy_per_mole_per_kelvin_squared():
    t_f = Quantity(float(quantum.fermi_temperature(N_CU_17, quantum.M_ELECTRON)), "K")
    gamma = np.pi**2 / 2 * Quantity(N_A, "1/mol") * K_B_Q / t_f
    assert gamma.check("[energy] / [temperature]**2 / [substance]")
    assert relative_error(quantum.free_electron_gamma(N_CU_17),
                          gamma.to("J/mol/K**2").magnitude) < 1e-12


def test_the_white_dwarf_radius_is_a_length():
    mass = Quantity(quantum.SOLAR_MASS, "kg")
    g = Quantity(quantum.GRAVITATIONAL_CONSTANT, "m**3/kg/s**2")
    n_e = (0.5 * mass / Quantity(AMU, "kg")).to("dimensionless")
    radius = HBAR_Q**2 / M_E_Q * (9 * np.pi / 4) ** (2 / 3) * n_e ** (5 / 3) / (g * mass**2)
    assert radius.check("[length]")
    assert relative_error(quantum.white_dwarf(quantum.SOLAR_MASS).radius,
                          radius.to("m").magnitude) < 1e-12


def test_quantum_functions_return_plain_si_floats_and_shaped_arrays():
    t = 300.0
    assert isinstance(quantum.bose_einstein(1e-20, 0.0, t), float)
    assert isinstance(quantum.fermi_dirac(1e-20, 0.0, t), float)
    assert isinstance(quantum.fermi_energy(N_CU_17, quantum.M_ELECTRON), float)
    assert isinstance(quantum.solve_mu(1e25, t, quantum.M_HELIUM4, "be"), float)
    assert isinstance(quantum.occupation_integral(-1.0, "fd"), float)
    eps = np.linspace(1e-21, 1e-19, 7)
    for statistics in quantum.STATISTICS:
        assert quantum.occupation(eps, -1e-21, t, statistics).shape == (7,)
    assert quantum.condensate_fraction(np.array([0.1, 0.5, 2.0]), 1.0).shape == (3,)


# ---------------------------------------------------------------------------
# Module 18: fluctuations and transport
# ---------------------------------------------------------------------------

M_N2_18 = 28.0134 * AMU
N_STP_18 = 101325.0 / (1.380649e-23 * 273.15)   # number density at 0 C and one atmosphere [1/m^3]
SIGMA_N2_18 = np.pi * (3.7e-10) ** 2            # hard-sphere cross-section [m^2]
R_GAS_Q = Quantity(8.314462618, "J/(mol*K)")


def test_a_random_walks_diffusion_coefficient_is_an_area_per_time():
    step, tau = Quantity(1e-7, "m"), Quantity(1e-10, "s")
    d = step**2 / (2 * tau)
    assert d.check("[length]**2 / [time]")
    assert relative_error(transport.persistent_walk_d(1e-7, 1e-10),
                          d.to("m**2/s").magnitude) < 1e-12
    x, t = Quantity(3e-6, "m"), Quantity(2e-3, "s")
    exponent = x**2 / (4 * d * t)
    assert exponent.check("[]")
    density = (4 * np.pi * d * t) ** -0.5 * np.exp(-exponent.to("").magnitude)
    assert density.check("1 / [length]")
    assert relative_error(
        transport.diffusion_greens_function(3e-6, 2e-3, d.to("m**2/s").magnitude),
        density.to("1/m").magnitude) < 1e-12


def test_the_mean_free_path_is_a_length_and_the_collision_rate_a_frequency():
    n, sigma = Quantity(N_STP_18, "1/m**3"), Quantity(SIGMA_N2_18, "m**2")
    m, t = Quantity(M_N2_18, "kg"), Quantity(273.15, "K")
    path = 1 / (np.sqrt(2) * n * sigma)
    vbar = (8 * K_B_Q * t / (np.pi * m)) ** 0.5
    rate = vbar / path
    assert path.check("[length]")
    assert vbar.check("[length] / [time]")
    assert rate.check("1 / [time]")
    assert relative_error(kinetics.mean_free_path(N_STP_18, SIGMA_N2_18),
                          path.to("m").magnitude) < 1e-12
    assert relative_error(kinetics.mean_speed(273.15, M_N2_18), vbar.to("m/s").magnitude) < 1e-12
    assert relative_error(kinetics.collision_rate(N_STP_18, SIGMA_N2_18, 273.15, M_N2_18),
                          rate.to("1/s").magnitude) < 1e-12


def test_the_transport_trio_has_the_units_of_a_diffusivity_a_viscosity_and_a_conductivity():
    n, sigma = Quantity(N_STP_18, "1/m**3"), Quantity(SIGMA_N2_18, "m**2")
    m, t = Quantity(M_N2_18, "kg"), Quantity(273.15, "K")
    path = 1 / (np.sqrt(2) * n * sigma)
    vbar = (8 * K_B_Q * t / (np.pi * m)) ** 0.5
    d = vbar * path / 3
    eta = n * m * d
    kappa = n * (2.5 * K_B_Q) * d
    assert d.check("[length]**2 / [time]")
    assert eta.check("[pressure] * [time]")
    assert kappa.check("[power] / [length] / [temperature]")
    est = transport.kinetic_estimates(N_STP_18, 273.15, M_N2_18, SIGMA_N2_18, 2.5 * 1.380649e-23)
    assert relative_error(est.diffusion, d.to("m**2/s").magnitude) < 1e-12
    assert relative_error(est.viscosity, eta.to("Pa*s").magnitude) < 1e-12
    assert relative_error(est.thermal_conductivity, kappa.to("W/(m*K)").magnitude) < 1e-12


def test_a_heat_capacity_read_off_the_noise_is_an_energy_per_kelvin():
    energies = np.array([0.0, 2e-21, 1e-21, 3e-21])
    variance = Quantity(float(np.var(energies, ddof=1)), "J**2")
    temperature = Quantity(300.0, "K")
    c = variance / (K_B_Q * temperature**2)
    assert c.check("[energy] / [temperature]")
    assert relative_error(transport.energy_fluctuation_cv(energies, 300.0).value,
                          c.to("J/K").magnitude) < 1e-12


def test_the_einstein_relation_gives_a_diffusivity_and_perrin_a_count_per_mole():
    eta, a, t = Quantity(1.0e-3, "Pa*s"), Quantity(0.5e-6, "m"), Quantity(293.0, "K")
    zeta = 6 * np.pi * eta * a
    d = K_B_Q * t / zeta
    assert zeta.check("[mass] / [time]")
    assert d.check("[length]**2 / [time]")
    n_a = R_GAS_Q * t / (zeta * d)
    assert n_a.check("1 / [substance]")
    d_si = d.to("m**2/s").magnitude
    zeta_si = transport.stokes_friction(1e-3, 0.5e-6)
    assert relative_error(zeta_si, zeta.to("kg/s").magnitude) < 1e-12
    assert relative_error(transport.einstein_diffusion(293.0, zeta_si), d_si) < 1e-12
    assert relative_error(transport.avogadro_from_diffusion(d_si, 293.0, 1e-3, 0.5e-6),
                          n_a.to("1/mol").magnitude) < 1e-9


def test_a_molecular_diameter_from_the_van_der_waals_b_is_a_length():
    b = Quantity(6.4e-29, "m**3")
    d = (3 * b / (2 * np.pi)) ** (1 / 3)
    assert d.check("[length]")
    assert relative_error(transport.diameter_from_vdw_b(6.4e-29), d.to("m").magnitude) < 1e-12
    assert transport.knudsen_number(1e-7, 1e-3) == pytest.approx(1e-4, rel=1e-12)
