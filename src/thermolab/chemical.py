"""The chemical potential: what particles flow down, and where they stop.

MODEL SPECIFICATION
    System:        N identical, non-interacting particles distributed over a set of lattice-gas
                   boxes; box k has M_k sites, each holding at most one particle, all at the
                   site energy u_k (two boxes for the centrepiece, a stack of layers for the
                   barometric column, a small box of binding sites beside a large one for
                   adsorption)
    Dynamics:      one particle, chosen uniformly, proposes a hop to a site chosen uniformly
                   among *all* sites; a proposal into an occupied site or into the particle's
                   own box changes nothing, and a hop into another box is accepted with the
                   Metropolis probability min(1, exp(-(u_new - u_old) / (k_B T)))
    Boundary:      closed to particles as a whole (sum_k N_k is conserved exactly at every
                   step); an implicit bath at temperature T supplies or absorbs each hop's
                   energy difference
    Ensemble:      canonical for the whole set at fixed T and N; each box separately is
                   approximately grand canonical, with the other boxes as its particle
                   reservoir
    Ignored:       interactions between particles beyond single occupancy of a site, hop
                   *rates* (time is counted in proposals, not seconds), and any spatial
                   structure inside a box
    Valid when:    boxes are large enough for Stirling's approximation (M_k and N_k >> 1); the
                   dilute closed forms additionally need N_k << M_k, and the ideal-gas forms
                   need n << n_Q, the classical regime
    Failure modes: nearly full boxes (the dilute split fails; the exclusion form in
                   `occupation_equilibrium` still holds), interacting particles (module 15),
                   and the degenerate regime n >~ n_Q, where quantum statistics take over
                   (module 17)

WHY A LATTICE GAS
    A box of M sites holding N particles has Omega = C(M, N) arrangements, so its entropy is
    module 08's coin count and its chemical potential is a single logarithm,

        mu = u - T (dS/dN) = u + k_B T ln( N / (M - N) )          (Stirling),

    which in the dilute limit is u + k_B T ln(N/M): an energy plus an entropic term that grows
    with the density. The site count M plays the part that the quantum concentration n_Q plays
    for a gas, kT ln(n / n_Q). Nothing else about the model matters for the module's claim.

WHY THE TARGET SITE IS DRAWN FROM ALL SITES
    Drawing the target uniformly from the other box alone would make the proposal probability
    1/M_b one way and 1/M_a the other, and detailed balance would then settle on a split biased
    by M_a/M_b. Drawing it from all M_a + M_b sites makes the proposal symmetric, so the
    Metropolis factor alone decides, and the stationary distribution is exactly

        P(N_a) ~ C(M_a, N_a) C(M_b, N - N_a) exp(-(N_a u_a + N_b u_b) / (k_B T)),

    which `exact_count_distribution` enumerates. The price is proposals wasted inside a box,
    which cost time, not correctness.

WHAT IS DEFERRED
    The grand partition function Xi is module 17's. Everything here runs on entropy
    maximization plus the one-site grand-canonical weight, `site_occupation`. The quantum
    concentration n_Q = 1/lambda^3 is named, and computed from module 12's thermal wavelength;
    why it is the right reference density is module 17's business too.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

import numpy as np

from .constants import K_B, N_A
from .fundamental import DEFAULT_REL_STEP, Relation, temperature_of
from .multiplicity import log_multiplicity_array
from .partition import thermal_wavelength
from .potentials import gibbs_from

#: Standard gravitational acceleration [m/s^2], for the barometric column.
STANDARD_GRAVITY: Final[float] = 9.80665

_BISECT_MAX_ITER: Final[int] = 200


def _beta(temperature: float) -> float:
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    return 1.0 / (K_B * temperature)


def _as_float_or_array(value):
    return float(value) if np.ndim(value) == 0 else value


# ---------------------------------------------------------------------------
# The chemical potential as a slope, two ways
# ---------------------------------------------------------------------------


def mu_from_entropy(relation: Relation, energy: float, volume: float, n_particles: float,
                    dn: float | None = None) -> float:
    """mu = -T (dS/dN)_{U,V} [J], by a central difference in N on any relation S(U, V, N).

    `dn` is the step in particles; by default a fraction `DEFAULT_REL_STEP` of N. T itself is
    read off the same relation as 1/(dS/dU), module 09's definition, so nothing but S is used.
    """
    n = float(n_particles)
    step = DEFAULT_REL_STEP * n if dn is None else float(dn)
    if step <= 0 or step >= n:
        raise ValueError("dn must be positive and smaller than n_particles")
    ds_dn = float(relation(energy, volume, n + step) - relation(energy, volume, n - step)) / (
        2.0 * step)
    return -temperature_of(relation, energy, volume, n) * ds_dn


def mu_from_gibbs(relation: Relation, temperature: float, pressure: float, n_particles: float,
                  dn: float | None = None) -> float:
    """mu = (dG/dN)_{T,P} [J], by a central difference of module 10's G(T, P, N) in N."""
    n = float(n_particles)
    step = DEFAULT_REL_STEP * n if dn is None else float(dn)
    if step <= 0 or step >= n:
        raise ValueError("dn must be positive and smaller than n_particles")
    up = gibbs_from(relation, temperature, pressure, n + step)
    down = gibbs_from(relation, temperature, pressure, n - step)
    return float(up - down) / (2.0 * step)


def quantum_concentration(temperature, mass: float):
    """n_Q = 1 / lambda^3 = (2 pi m k_B T / h^2)^(3/2) [1/m^3].

    Named here, derived in module 17: the density at which the particles' thermal wavelengths
    begin to overlap. Nitrogen at 300 K has n_Q = 1.4e32 per cubic metre, about six million
    times the density of air.
    """
    lam = np.asarray(thermal_wavelength(temperature, mass), dtype=float)
    return _as_float_or_array(1.0 / lam**3)


def ideal_gas_mu(number_density, temperature: float, mass: float,
                 u_ext: float | np.ndarray = 0.0):
    """mu = k_B T ln(n / n_Q) + u_ext [J] for a classical monatomic ideal gas.

    The exact slope -T (dS/dN)_{U,V} of the Sackur-Tetrode entropy, plus any external energy
    per particle `u_ext` (gravity m g z, a wall's binding energy, an electrical offset). It is
    negative whenever the gas is classical, n < n_Q.
    """
    n = np.asarray(number_density, dtype=float)
    if np.any(n <= 0):
        raise ValueError("number_density must be positive")
    n_q = quantum_concentration(temperature, mass)
    return _as_float_or_array(K_B * temperature * np.log(n / n_q) + np.asarray(u_ext, float))


def density_at_mu(mu, temperature: float, mass: float, u_ext: float | np.ndarray = 0.0):
    """n = n_Q exp((mu - u_ext) / (k_B T)) [1/m^3]: `ideal_gas_mu` inverted."""
    n_q = quantum_concentration(temperature, mass)
    exponent = (np.asarray(mu, float) - np.asarray(u_ext, float)) * _beta(temperature)
    return _as_float_or_array(n_q * np.exp(exponent))


def barometric_profile(heights, temperature: float, mass: float, density_at_zero: float,
                       gravity: float = STANDARD_GRAVITY):
    """n(z) from a constant chemical potential in an isothermal column [1/m^3].

    Fix mu at the floor, where u_ext = 0 and n = `density_at_zero`, then ask every height for
    the density that has the same mu once u_ext = m g z is added. The answer is
    n(0) exp(-m g z / (k_B T)) -- module 11's Boltzmann-factor result, reached without a
    Boltzmann factor.
    """
    mu = ideal_gas_mu(density_at_zero, temperature, mass)
    z = np.asarray(heights, dtype=float)
    return density_at_mu(mu, temperature, mass, u_ext=mass * gravity * z)


# ---------------------------------------------------------------------------
# The lattice gas
# ---------------------------------------------------------------------------


def lattice_gas_entropy(count, sites: int):
    """S = k_B ln C(M, N) [J/K], exactly, for N particles on M single-occupancy sites."""
    counts = np.asarray(count, dtype=float)
    if np.any(counts < 0) or np.any(counts > sites):
        raise ValueError("count must lie between 0 and the number of sites")
    return _as_float_or_array(K_B * log_multiplicity_array(sites, counts))


def lattice_gas_mu(count, sites, site_energy, temperature: float):
    """mu = u + k_B T ln((N + 1/2) / (M - N + 1/2)) [J].

    Stirling's slope u + k_B T ln(N / (M - N)), with half-particle offsets that keep it finite
    for an empty or a full box -- where a simulation trace will sometimes be. The offsets shift
    mu by about k_B T / (2N), negligible once a box holds more than a few dozen particles.
    """
    n = np.asarray(count, dtype=float)
    if np.any(n < 0) or np.any(n > sites):
        raise ValueError("count must lie between 0 and the number of sites")
    return _as_float_or_array(
        site_energy + K_B * temperature * np.log((n + 0.5) / (sites - n + 0.5)))


@dataclass(frozen=True)
class Boxes:
    """A set of lattice-gas boxes: `sites[k]` single-occupancy sites at energy `energies[k]` [J]."""

    sites: np.ndarray
    energies: np.ndarray

    def __post_init__(self) -> None:
        if self.sites.shape != self.energies.shape or self.sites.ndim != 1:
            raise ValueError("sites and energies must be 1-D arrays of one length")
        if len(self.sites) < 2:
            raise ValueError("particles need at least two boxes to move between")
        if np.any(self.sites < 1):
            raise ValueError("every box needs at least one site")

    def __len__(self) -> int:
        return len(self.sites)

    @property
    def total_sites(self) -> int:
        return int(self.sites.sum())


def two_boxes(sites_a: int, sites_b: int, energy_a: float = 0.0, energy_b: float = 0.0) -> Boxes:
    """Box A and box B, the centrepiece. Raising `energy_b` is raising B's floor."""
    return Boxes(sites=np.array([sites_a, sites_b], dtype=np.int64),
                 energies=np.array([energy_a, energy_b], dtype=float))


def column(n_layers: int, sites_per_layer: int, layer_energy: float) -> Boxes:
    """An isothermal column: layer k sits at energy k * `layer_energy` (m g times its height)."""
    if n_layers < 2:
        raise ValueError("a column needs at least two layers")
    return Boxes(sites=np.full(n_layers, sites_per_layer, dtype=np.int64),
                 energies=layer_energy * np.arange(n_layers, dtype=float))


@dataclass(frozen=True)
class ExchangeTrace:
    """How many particles each box held, recorded every `record_every` proposals.

    `counts[i, k]` is box k's count at `steps[i]`; the row sums are all equal, the total N.
    """

    steps: np.ndarray
    counts: np.ndarray
    boxes: Boxes
    temperature: float

    @property
    def n_total(self) -> int:
        return int(self.counts[0].sum())

    @property
    def densities(self) -> np.ndarray:
        """Occupied fraction of each box's sites, N_k / M_k."""
        return self.counts / self.boxes.sites

    @property
    def chemical_potentials(self) -> np.ndarray:
        """mu_k at every record [J], by `lattice_gas_mu`."""
        return np.asarray(lattice_gas_mu(self.counts, self.boxes.sites[None, :],
                                         self.boxes.energies[None, :], self.temperature))

    def tail(self, fraction: float = 0.5) -> np.ndarray:
        """The last `fraction` of the recorded counts, for equilibrium averages."""
        start = int(len(self.counts) * (1.0 - fraction))
        return self.counts[start:]


def particle_exchange_sim(boxes: Boxes, initial_counts, temperature: float, n_steps: int,
                          rng: np.random.Generator, record_every: int = 1) -> ExchangeTrace:
    """Metropolis particle hops between lattice-gas boxes; see the module docstring.

    The loop tracks only the integer count in each box -- never a particle's position -- so a
    step costs the same for a hundred particles as for twenty thousand. Every random number is
    drawn before the loop: which particle moves (a uniform variate mapped onto the cumulative
    counts), which site it aims at (one over all sites), and the Metropolis test.
    """
    counts = np.array(initial_counts, dtype=np.int64)
    if counts.shape != boxes.sites.shape:
        raise ValueError("initial_counts needs one entry per box")
    if np.any(counts < 0) or np.any(counts > boxes.sites):
        raise ValueError("each initial count must lie between 0 and the box's sites")
    n_total = int(counts.sum())
    if n_total < 1:
        raise ValueError("there must be at least one particle")
    if n_steps < 1 or record_every < 1:
        raise ValueError("n_steps and record_every must be positive")
    beta = _beta(temperature)

    site_edges = np.cumsum(boxes.sites)
    target_box = np.searchsorted(site_edges, rng.integers(0, boxes.total_sites, n_steps),
                                 side="right")
    particle_draw = rng.integers(0, n_total, n_steps)
    accept_draw = rng.random(n_steps)
    target_draw = rng.random(n_steps)  # is the aimed-at site empty?

    sites = boxes.sites.tolist()
    energies = boxes.energies.tolist()
    current = counts.tolist()
    n_boxes = len(current)
    n_records = n_steps // record_every
    record = np.empty((n_records, n_boxes), dtype=np.int64)

    for step in range(n_steps):
        # Which box holds the chosen particle: walk the running counts.
        pick = int(particle_draw[step])
        source = 0
        while pick >= current[source]:
            pick -= current[source]
            source += 1
        dest = int(target_box[step])
        if dest != source and target_draw[step] * sites[dest] >= current[dest]:
            delta = energies[dest] - energies[source]
            if delta <= 0.0 or accept_draw[step] < math.exp(-beta * delta):
                current[source] -= 1
                current[dest] += 1
        if (step + 1) % record_every == 0:
            record[(step + 1) // record_every - 1] = current

    steps = record_every * np.arange(1, n_records + 1)
    return ExchangeTrace(steps=steps, counts=record, boxes=boxes, temperature=float(temperature))


@dataclass(frozen=True)
class CountDistribution:
    """The exact stationary distribution of box A's count in a two-box system."""

    n_a: np.ndarray
    probability: np.ndarray
    boxes: Boxes
    n_total: int
    temperature: float

    @property
    def mean(self) -> float:
        return float(np.sum(self.n_a * self.probability))

    @property
    def std(self) -> float:
        return float(np.sqrt(np.sum((self.n_a - self.mean) ** 2 * self.probability)))

    @property
    def most_probable(self) -> int:
        return int(self.n_a[np.argmax(self.probability)])

    def mu_difference_std(self) -> float:
        """Standard deviation of mu_a - mu_b over the distribution [J]."""
        (m_a, m_b), (u_a, u_b) = self.boxes.sites, self.boxes.energies
        diff = (np.asarray(lattice_gas_mu(self.n_a, int(m_a), float(u_a), self.temperature))
                - np.asarray(lattice_gas_mu(self.n_total - self.n_a, int(m_b), float(u_b),
                                            self.temperature)))
        mean = float(np.sum(diff * self.probability))
        return float(np.sqrt(np.sum((diff - mean) ** 2 * self.probability)))


def exact_count_distribution(boxes: Boxes, n_total: int, temperature: float) -> CountDistribution:
    """P(N_a) ~ C(M_a, N_a) C(M_b, N - N_a) exp(-beta (N_a u_a + N_b u_b)), every N_a counted.

    This is the stationary distribution of `particle_exchange_sim` for two boxes -- not an
    approximation to it -- so the simulation's long-run average must land on its mean.
    """
    if len(boxes) != 2:
        raise ValueError("the exact distribution is enumerated for two boxes")
    m_a, m_b = int(boxes.sites[0]), int(boxes.sites[1])
    if not 0 < n_total <= m_a + m_b:
        raise ValueError("n_total must be positive and fit in the sites")
    beta = _beta(temperature)
    n_a = np.arange(max(0, n_total - m_b), min(n_total, m_a) + 1)
    n_b = n_total - n_a
    log_weight = (log_multiplicity_array(m_a, n_a) + log_multiplicity_array(m_b, n_b)
                  - beta * (n_a * boxes.energies[0] + n_b * boxes.energies[1]))
    weight = np.exp(log_weight - log_weight.max())
    return CountDistribution(n_a=n_a, probability=weight / weight.sum(), boxes=boxes,
                             n_total=int(n_total), temperature=float(temperature))


def equilibrium_split(boxes: Boxes, n_total: float, temperature: float) -> np.ndarray:
    """Dilute closed form: N_k ~ M_k exp(-u_k / (k_B T)), normalized to `n_total`.

    Equal mu in the dilute limit, u_k + k_B T ln(N_k / M_k) the same in every box, gives
    densities n_a / n_b = exp(-(u_a - u_b) / (k_B T)). Valid when every box is far from full.
    """
    beta = _beta(temperature)
    log_w = np.log(boxes.sites.astype(float)) - beta * boxes.energies
    w = np.exp(log_w - log_w.max())
    return n_total * w / w.sum()


def relaxation_steps(boxes: Boxes, n_total: int, temperature: float) -> float:
    """tau [proposals]: the dilute two-box split relaxes as exp(-steps / tau).

    With both boxes far from full, the expected change of N_a per proposal is linear in N_a:
    (N_b/N)(M_a/M) a_ba - (N_a/N)(M_b/M) a_ab, with a_xy the Metropolis acceptance of a hop
    from x to y. Its time constant is tau = N M / (M_a a_ba + M_b a_ab): proportional to N,
    which is why a larger system needs proportionally more proposals.
    """
    if len(boxes) != 2:
        raise ValueError("the relaxation time is given for two boxes")
    beta = _beta(temperature)
    (m_a, m_b), (u_a, u_b) = boxes.sites.astype(float), boxes.energies
    a_ab = min(1.0, math.exp(-beta * (u_b - u_a)))
    a_ba = min(1.0, math.exp(-beta * (u_a - u_b)))
    return float(n_total * (m_a + m_b) / (m_a * a_ba + m_b * a_ab))


def site_occupation(mu, temperature: float, site_energy):
    """<n> = 1 / (exp((epsilon - mu) / (k_B T)) + 1): one site in contact with a particle reservoir.

    The grand-canonical weight exp(-(E_s - mu N_s) / (k_B T)) applied to a site with two states,
    empty (E = 0, N = 0) and filled (E = epsilon, N = 1). Module 17 will call this the
    Fermi-Dirac function.
    """
    x = (np.asarray(site_energy, float) - np.asarray(mu, float)) * _beta(temperature)
    return _as_float_or_array(np.exp(-np.logaddexp(0.0, x)))


def occupation_equilibrium(boxes: Boxes, n_total: float, temperature: float
                           ) -> tuple[float, np.ndarray]:
    """(mu, counts): the common mu at which sum_k M_k <n>(mu, u_k) = n_total, and the counts.

    Equal mu with single occupancy kept -- each site filled with `site_occupation`'s
    probability -- rather than the dilute form. It holds at any filling, and is what a large
    two-box system settles to when it is not dilute.
    """
    if not 0 < n_total < boxes.total_sites:
        raise ValueError("n_total must lie strictly between zero and the number of sites")
    kt = K_B * temperature

    def filled(mu: float) -> float:
        return float(np.sum(boxes.sites * site_occupation(mu, temperature, boxes.energies)))

    lo = float(boxes.energies.min()) - kt * (math.log(boxes.total_sites) + 50.0)
    hi = float(boxes.energies.max()) + kt * (math.log(boxes.total_sites) + 50.0)
    for _ in range(_BISECT_MAX_ITER):
        mid = 0.5 * (lo + hi)
        if filled(mid) < n_total:
            lo = mid
        else:
            hi = mid
        if hi - lo <= 1e-14 * kt:
            break
    mu = 0.5 * (lo + hi)
    return mu, boxes.sites * site_occupation(mu, temperature, boxes.energies)


# ---------------------------------------------------------------------------
# Mu balance, cashed in: reactions and osmosis
# ---------------------------------------------------------------------------


def mass_action_ratio(delta_epsilon: float, temperature: float, nq_ratio: float = 1.0) -> float:
    """n_B / n_A = (n_Q,B / n_Q,A) exp(-Delta epsilon / (k_B T)) for A <=> B.

    From mu_A = mu_B with mu_X = k_B T ln(n_X / n_Q,X) + epsilon_X: the toy reaction's law of
    mass action. `nq_ratio` carries any difference in the two species' internal state counts.
    """
    if nq_ratio <= 0:
        raise ValueError("nq_ratio must be positive")
    return float(nq_ratio * math.exp(-delta_epsilon * _beta(temperature)))


def osmotic_pressure(solute_density, temperature: float):
    """van 't Hoff: Pi = n_s k_B T [Pa], with n_s the solute number density [1/m^3].

    The dilute limit of `lattice_osmotic_pressure`. Formally the ideal-gas law, with the
    solute in the role of the gas -- which is a coincidence of the dilute expansion, not a
    statement that the solute pushes on the membrane.
    """
    n = np.asarray(solute_density, dtype=float)
    if np.any(n < 0):
        raise ValueError("solute_density must be non-negative")
    return _as_float_or_array(n * K_B * temperature)


def lattice_osmotic_pressure(solute_fraction, molecular_volume: float, temperature: float):
    """Pi = -(k_B T / v) ln(1 - x) [Pa] for an ideal lattice solution.

    Solvent molecules each occupy a volume v; a fraction x of the lattice sites hold solute.
    The solvent's mu on the solution side is lowered by k_B T ln(1 - x); pressure raises it by
    Pi v; equal solvent mu across the membrane fixes Pi. Expanding -ln(1 - x) = x + x^2/2 + ...
    with x/v = n_s gives van 't Hoff, and x/2 is the fractional error of stopping there.
    """
    if molecular_volume <= 0:
        raise ValueError("molecular_volume must be positive")
    x = np.asarray(solute_fraction, dtype=float)
    if np.any(x < 0) or np.any(x >= 1):
        raise ValueError("solute_fraction must lie in [0, 1)")
    return _as_float_or_array(-K_B * temperature * np.log1p(-x) / molecular_volume)


#: Volume of one water molecule in the liquid [m^3]: 18.015 g/mol at 997 kg/m^3.
WATER_MOLECULAR_VOLUME: Final[float] = 18.015e-3 / 997.0 / N_A


def osmosis_readings(molar_concentrations, temperature: float, noise: float,
                     rng: np.random.Generator) -> np.ndarray:
    """Synthetic osmotic-pressure readings [Pa] for sucrose-like solutions, with relative noise.

    A stand-in for a class's dialysis-tubing measurements, generated from the ideal lattice
    solution with water's molecular volume and a relative Gaussian error `noise` per reading.
    It is not data: it reproduces this module's model, including its departure from van 't
    Hoff, and nothing a real solution does beyond it.
    """
    if noise < 0:
        raise ValueError("noise must be non-negative")
    c = np.asarray(molar_concentrations, dtype=float)
    x = c * 1e3 * N_A * WATER_MOLECULAR_VOLUME  # solute's share of the lattice sites
    true = np.asarray(lattice_osmotic_pressure(x, WATER_MOLECULAR_VOLUME, temperature))
    return true * (1.0 + noise * rng.standard_normal(true.shape))
