"""The Ising model: order, symmetry breaking, and Monte Carlo sampling.

MODEL SPECIFICATION
    System:        a periodic lattice of N classical spins s_i = +1 or -1 -- an L x L square
                   lattice for the module, an L-site ring for the exact one-dimensional
                   anchor -- with nearest-neighbour coupling J > 0 and a uniform field h,
                   E = -J sum_<ij> s_i s_j - h sum_i s_i
    Dynamics:      a Markov chain, not equations of motion: checkerboard half-sweeps, each
                   site of one colour proposing to flip and accepting by the Metropolis rule
                   min(1, exp(-Delta E / (k_B T))) or the Glauber (heat-bath) rule
                   1 / (1 + exp(Delta E / (k_B T))); "time" is counted in sweeps, which no
                   physical constant converts into seconds
    Boundary:      periodic -- the lattice has no edges; T and h are imposed from outside by
                   an implicit heat bath
    Ensemble:      canonical at temperature T: P_s proportional to exp(-E_s / (k_B T)) is the
                   stationary distribution of the chain, by detailed balance (module 11's
                   Boltzmann distribution made executable)
    Ignored:       quantum spin, lattice vibrations, long-range dipolar forces, anisotropy,
                   disorder and domain-wall pinning -- everything that makes a real magnet a
                   material rather than a model
    Valid when:    the chain has run well past burn-in and many autocorrelation times
                   tau(T); fast away from T_c at moderate L
    Failure modes: near T_c, tau grows with L (critical slowing down) and error bars that
                   ignore it are illusory; below T_c at small |h| the chain stays in one
                   magnetization branch for longer than any run (practical ergodicity
                   breaking); a trace that keeps its burn-in biases every average

REDUCED UNITS -- THE MODULE'S ONE LICENSED EXCEPTION TO SI
    Energies are measured in units of J, temperature as k_B T / J and field as h / J. Critical
    behaviour is the one subject in the course where the material constants genuinely scale
    out -- universality is the claim that they do -- and k_B is still present in every formula
    through beta = 1 / (k_B T): only the display changes. In these units the totals of an
    h = 0 state are integers, which the conservation tests exploit.

WHY A CHECKERBOARD, AND WHAT IT DOES AND DOES NOT SATISFY
    Updating every site at once is wrong: two neighbours that both flip each computed Delta E
    against a configuration the other one changed, and the chain converges to some other
    distribution (at low T it famously oscillates between the two antiferromagnetic
    checkerboards). Colour the lattice like a chessboard instead: every neighbour of a black
    site is white. With the white sites frozen, the black sites do not interact with each
    other, so updating all of them at once is exactly the same as updating them one at a
    time -- and each such half-sweep satisfies detailed balance with respect to the Boltzmann
    distribution. A full sweep is black then white. The composition is no longer reversible
    (white-then-black is a different operator), but each factor leaves the Boltzmann
    distribution stationary, so the product does too, which is all that sampling needs.
    That requires an even side L, so that the colouring survives the periodic wrap.

THE ZERO-COST MOVE, AND WHY THE CHAIN TESTS USE GLAUBER
    Metropolis accepts a move with Delta E = 0 with certainty. On the h = 0 ring every move
    of a domain wall costs nothing, so under the checkerboard a wall is pushed one site per
    half-sweep, always the same way: walls travel ballistically instead of diffusing, and the
    chain forgets its starting point slowly. Measured on a 1024-site ring at T = 1, a cold
    start still sits 4 standard errors low after 100 sweeps of burn-in and needs thousands
    to settle; Glauber, which accepts the same move with probability 1/2, has settled in a
    hundred. The stationary distribution is the same -- this is a statement about the speed
    of an algorithm, which is exactly the module's point that sweeps are not physical time.
    The one-dimensional anchors therefore run Glauber; in two dimensions, where zero-cost
    moves are a minority, Metropolis mixes well and is the default.

THE SUSCEPTIBILITY ESTIMATOR
    Module 12's identity chi = N Var(m) / (k_B T) is exact in the ensemble. In a finite run
    below T_c, though, the chain crosses between +m and -m rarely and erratically, so Var(m)
    of a run measures how many crossings happened to fit inside it. `observables` therefore
    applies the same identity to |m|, which the run *can* sample: chi' = N Var(|m|) / (k_B T).
    It is the standard finite-size estimator; it peaks at a temperature that drifts toward
    T_c as L grows, which is the only use the module makes of it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final

import numpy as np

#: Coordination number q of the square lattice (and 2 for the ring): neighbours per site.
SQUARE_COORDINATION: Final[int] = 4

#: Sokal's window constant for the integrated autocorrelation time: sum the autocorrelation
#: function out to the first lag W with W >= C * tau(W). Larger C costs variance and buys
#: less truncation bias; 5 is the conventional compromise for traces that decay roughly
#: exponentially.
_WINDOW_C: Final[float] = 5.0

_RULES: Final[tuple[str, ...]] = ("metropolis", "glauber")


@dataclass(frozen=True)
class IsingState:
    """A spin configuration with its running totals.

    `energy` (in J) and `magnetization` (the total sum of spins, an integer) are kept up to
    date by every update rather than recomputed; the conservation tests check that the
    bookkeeping never drifts from a from-scratch recompute.
    """

    lattice: np.ndarray
    energy: float
    magnetization: int
    field: float

    @property
    def n_spins(self) -> int:
        return int(self.lattice.size)

    @property
    def m(self) -> float:
        """Magnetization per spin, m = (1/N) sum_i s_i, between -1 and +1."""
        return self.magnetization / self.lattice.size

    @property
    def e(self) -> float:
        """Energy per spin, in units of J."""
        return self.energy / self.lattice.size


@dataclass(frozen=True)
class IsingObservables:
    """Equilibrium estimates from a pair of per-spin traces.

    Both response functions come from fluctuations, module 12's identities applied to the
    traces: c = N Var(e) / (k_B T)^2 (heat capacity per spin, in units of k_B) and
    chi' = N Var(|m|) / (k_B T) (see THE SUSCEPTIBILITY ESTIMATOR in the module docstring).
    """

    abs_magnetization: float
    abs_magnetization_error: float
    energy: float
    energy_error: float
    susceptibility: float
    heat_capacity: float
    tau_abs_magnetization: float
    tau_energy: float


# ---------------------------------------------------------------------------
# States and energies
# ---------------------------------------------------------------------------


def _check_size(size: int) -> None:
    if size < 4 or size % 2:
        raise ValueError("the side L must be even and at least 4, so the checkerboard "
                         "colouring survives the periodic wrap")


def _shape(size: int, dimension: int) -> tuple[int, ...]:
    _check_size(size)
    if dimension not in (1, 2):
        raise ValueError("dimension must be 1 (a ring) or 2 (a square lattice)")
    return (size,) * dimension


def bond_sum(lattice: np.ndarray) -> int:
    """sum_<ij> s_i s_j over nearest-neighbour bonds, each bond counted once.

    Pairing every site with its successor along each axis visits each periodic bond exactly
    once: N bonds on a ring, 2N on a square lattice.
    """
    s = lattice.astype(np.int64)
    return int(sum((s * np.roll(s, -1, axis=a)).sum() for a in range(s.ndim)))


def lattice_energy(lattice: np.ndarray, field: float = 0.0) -> float:
    """E = -J sum_<ij> s_i s_j - h sum_i s_i, recomputed from scratch, in units of J."""
    return float(-bond_sum(lattice) - field * int(lattice.sum()))


def _state(lattice: np.ndarray, field: float) -> IsingState:
    return IsingState(lattice=lattice, energy=lattice_energy(lattice, field),
                      magnetization=int(lattice.sum()), field=float(field))


def random_state(size: int, rng: np.random.Generator, field: float = 0.0,
                 dimension: int = 2) -> IsingState:
    """A hot start: every spin independently up or down with probability 1/2."""
    lattice = rng.choice(np.array([-1, 1], dtype=np.int8), size=_shape(size, dimension))
    return _state(lattice, field)


def aligned_state(size: int, up: bool = True, field: float = 0.0,
                  dimension: int = 2) -> IsingState:
    """A cold start: every spin up (or every spin down)."""
    lattice = np.full(_shape(size, dimension), 1 if up else -1, dtype=np.int8)
    return _state(lattice, field)


def with_field(state: IsingState, field: float) -> IsingState:
    """The same configuration in a new field; only the field term of the energy changes."""
    delta = -(float(field) - state.field) * state.magnetization
    return IsingState(lattice=state.lattice, energy=state.energy + delta,
                      magnetization=state.magnetization, field=float(field))


def checkerboard(shape: tuple[int, ...]) -> np.ndarray:
    """Boolean mask of the 'black' sites: those whose index sum is even."""
    return (np.indices(shape).sum(axis=0) % 2) == 0


def _neighbour_sum(lattice: np.ndarray) -> np.ndarray:
    s = lattice.astype(np.int16)
    total = np.zeros_like(s)
    for a in range(s.ndim):
        total += np.roll(s, 1, axis=a) + np.roll(s, -1, axis=a)
    return total


# ---------------------------------------------------------------------------
# The Markov chain
# ---------------------------------------------------------------------------


def acceptance(delta_e, temperature: float, rule: str = "metropolis"):
    """Probability of accepting a proposed flip that changes the energy by Delta E.

    metropolis: A = min(1, exp(-Delta E / (k_B T)))
    glauber:    A = 1 / (1 + exp(Delta E / (k_B T)))

    Both satisfy detailed balance, A(Delta E) / A(-Delta E) = exp(-Delta E / (k_B T)), so
    both sample the same Boltzmann distribution -- and they relax toward it at different
    rates, which is why "sweeps" are not a physical time.
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    x = np.asarray(delta_e, dtype=float) / temperature
    if rule == "metropolis":
        return np.exp(-np.maximum(x, 0.0))
    if rule == "glauber":
        return 0.5 * (1.0 - np.tanh(0.5 * x))  # = 1 / (1 + e^x), without overflow
    raise ValueError(f"rule must be one of {_RULES}")


def _half_sweep(lattice: np.ndarray, colour: np.ndarray, temperature: float, field: float,
                rng: np.random.Generator, rule: str) -> tuple[float, int]:
    """Update every site of one colour in place; return the change in (E, M)."""
    delta_e = 2.0 * lattice * (_neighbour_sum(lattice) + field)
    flip = colour & (rng.random(lattice.shape) < acceptance(delta_e, temperature, rule))
    d_energy = float(delta_e[flip].sum())
    d_magnet = -2 * int(lattice[flip].sum(dtype=np.int64))
    lattice[flip] *= -1
    return d_energy, d_magnet


def sweep(state: IsingState, temperature: float, rng: np.random.Generator,
          rule: str = "metropolis") -> IsingState:
    """One full sweep -- a black half-sweep, then a white one. Returns a new state.

    Each site gets one flip attempt per sweep, which is the unit Monte Carlo "time" is
    counted in. See WHY A CHECKERBOARD in the module docstring for why the half-sweeps
    respect detailed balance and a simultaneous update of every site would not.
    """
    lattice = state.lattice.copy()
    energy, magnet = _sweep_in_place(lattice, state.energy, state.magnetization,
                                     temperature, state.field, rng, rule,
                                     checkerboard(lattice.shape))
    return IsingState(lattice=lattice, energy=energy, magnetization=magnet,
                      field=state.field)


def metropolis_sweep(state: IsingState, temperature: float,
                     rng: np.random.Generator) -> IsingState:
    """One checkerboard Metropolis sweep: `sweep` with the Metropolis rule."""
    return sweep(state, temperature, rng, rule="metropolis")


def _sweep_in_place(lattice, energy, magnet, temperature, field, rng, rule, black):
    for colour in (black, ~black):
        d_e, d_m = _half_sweep(lattice, colour, temperature, field, rng, rule)
        energy += d_e
        magnet += d_m
    return energy, magnet


def simulate(state: IsingState, temperature: float, n_sweeps: int,
             rng: np.random.Generator, burn_in: int = 200, thin: int = 1,
             rule: str = "metropolis") -> tuple[np.ndarray, np.ndarray, IsingState]:
    """Run the chain and record per-spin traces.

    Runs `burn_in` sweeps that are discarded, then `n_sweeps` more, recording m and e (per
    spin, m signed) after every `thin`-th one. Returns (m_trace, e_trace, final_state). The
    autocorrelation time of a trace is measured in recorded samples, so thinning by k divides
    it by roughly k; it never changes the averages.
    """
    if n_sweeps < 1 or burn_in < 0 or thin < 1:
        raise ValueError("need n_sweeps >= 1, burn_in >= 0 and thin >= 1")
    lattice = state.lattice.copy()
    energy, magnet = state.energy, state.magnetization
    black = checkerboard(lattice.shape)
    n = lattice.size
    n_records = n_sweeps // thin
    m_trace = np.empty(n_records)
    e_trace = np.empty(n_records)
    for _ in range(burn_in):
        energy, magnet = _sweep_in_place(lattice, energy, magnet, temperature, state.field,
                                         rng, rule, black)
    k = 0
    for i in range(1, n_records * thin + 1):
        energy, magnet = _sweep_in_place(lattice, energy, magnet, temperature, state.field,
                                         rng, rule, black)
        if i % thin == 0:
            m_trace[k] = magnet / n
            e_trace[k] = energy / n
            k += 1
    final = IsingState(lattice=lattice, energy=energy, magnetization=magnet,
                       field=state.field)
    return m_trace, e_trace, final


# ---------------------------------------------------------------------------
# Statistics of correlated traces
# ---------------------------------------------------------------------------


def autocorrelation(trace: np.ndarray, max_lag: int | None = None) -> np.ndarray:
    """Normalised autocorrelation rho(t) of a trace, rho(0) = 1, via FFT."""
    x = np.asarray(trace, dtype=float)
    n = x.size
    if n < 2:
        raise ValueError("need at least two samples")
    x = x - x.mean()
    variance = float(np.dot(x, x))
    if variance == 0.0:
        out = np.zeros(n if max_lag is None else min(max_lag + 1, n))
        out[0] = 1.0
        return out
    size = 1 << (2 * n - 1).bit_length()
    spectrum = np.fft.rfft(x, size)
    acf = np.fft.irfft(spectrum * np.conjugate(spectrum), size)[:n] / variance
    return acf if max_lag is None else acf[: max_lag + 1]


def autocorrelation_time(trace: np.ndarray) -> float:
    """Integrated autocorrelation time with Sokal's self-consistent window, in samples.

    tau = 1/2 + sum_{t=1}^{W} rho(t), with W the first lag satisfying W >= 5 tau(W). For
    independent samples tau = 1/2, and a trace of n samples carries about n / (2 tau)
    independent ones. The window is a bias-variance compromise: summing rho(t) all the way
    out adds noise without signal. If the trace is too short for the window to close, the
    estimate is a lower bound and should be read as "run longer".

    Returns at least 1/2: an anticorrelated trace (Metropolis at very high T flips most of
    a sublattice every sweep) has formally tau < 1/2, but claiming better-than-independent
    statistics from it is never the conservative choice.
    """
    rho = autocorrelation(trace)
    tau = 0.5
    for w in range(1, rho.size):
        tau += rho[w]
        if w >= _WINDOW_C * tau:
            break
    return max(float(tau), 0.5)


def effective_samples(n_samples: int, tau: float) -> float:
    """N_eff = N / (2 tau): how many independent samples a correlated trace is worth."""
    if tau < 0.5:
        raise ValueError("tau is at least 1/2")
    return n_samples / (2.0 * tau)


def mean_with_error(trace: np.ndarray) -> tuple[float, float, float]:
    """(mean, standard error, tau) of a correlated trace.

    The naive sigma / sqrt(N) assumes independent samples and is too small by
    sqrt(2 tau); this uses N_eff instead.
    """
    x = np.asarray(trace, dtype=float)
    tau = autocorrelation_time(x)
    error = float(x.std(ddof=1) / math.sqrt(effective_samples(x.size, tau)))
    return float(x.mean()), error, tau


def observables(m_trace: np.ndarray, e_trace: np.ndarray, temperature: float,
                n_spins: int) -> IsingObservables:
    """<|m|>, <e>, chi' and c from per-spin traces, with tau-corrected error bars."""
    abs_m = np.abs(np.asarray(m_trace, dtype=float))
    e = np.asarray(e_trace, dtype=float)
    m_mean, m_err, m_tau = mean_with_error(abs_m)
    e_mean, e_err, e_tau = mean_with_error(e)
    return IsingObservables(
        abs_magnetization=m_mean, abs_magnetization_error=m_err,
        energy=e_mean, energy_error=e_err,
        susceptibility=float(n_spins * abs_m.var() / temperature),
        heat_capacity=float(n_spins * e.var() / temperature**2),
        tau_abs_magnetization=m_tau, tau_energy=e_tau)


def branch_flips(m_trace: np.ndarray, threshold: float = 0.5) -> int:
    """How many times a trace crosses from m > threshold to m < -threshold or back.

    Thresholded so that noise around m = 0 above T_c is not counted: a flip is a full
    traverse between the two ordered branches.
    """
    if not 0 < threshold < 1:
        raise ValueError("threshold must lie strictly between 0 and 1")
    branch = 0
    flips = 0
    for m in np.asarray(m_trace, dtype=float):
        side = 1 if m > threshold else (-1 if m < -threshold else 0)
        if side and side != branch:
            flips += branch != 0
            branch = side
    return flips


# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------


def temperature_scan(size: int, temperatures, n_sweeps: int, rng: np.random.Generator,
                     burn_in: int = 200, field: float = 0.0,
                     dimension: int = 2) -> list[IsingObservables]:
    """Observables along a ladder of temperatures, each run seeded by the previous one.

    Starting each temperature from the last configuration (an annealing ladder) shortens
    burn-in without changing the equilibrium being sampled; the burn-in is still run at
    every temperature.
    """
    state = random_state(size, rng, field=field, dimension=dimension)
    results = []
    for t in np.asarray(temperatures, dtype=float):
        m, e, state = simulate(state, float(t), n_sweeps, rng, burn_in=burn_in)
        results.append(observables(m, e, float(t), state.n_spins))
    return results


def hysteresis_fields(field_max: float, n_steps: int) -> np.ndarray:
    """A closed field ladder +h_max -> -h_max -> +h_max, `n_steps` points per leg."""
    if field_max <= 0 or n_steps < 2:
        raise ValueError("need field_max > 0 and n_steps >= 2")
    down = np.linspace(field_max, -field_max, n_steps)
    return np.concatenate([down, down[::-1][1:]])


def hysteresis_sweep(state: IsingState, temperature: float, fields,
                     sweeps_per_step: int, rng: np.random.Generator, burn_in: int = 200,
                     rule: str = "metropolis") -> tuple[np.ndarray, np.ndarray, IsingState]:
    """Step the field along `fields`, running `sweeps_per_step` sweeps at each value.

    The state first runs `burn_in` sweeps at fields[0], so the loop starts from equilibrium
    rather than from however the state was prepared. Returns (fields, m after each step,
    final state). Below T_c the curve m(h) does not retrace itself: the magnetization lags
    the field, because reversing it needs a domain of the other sign to nucleate and grow.
    Slower sweeps (more sweeps per step) narrow the loop; above T_c they close it.
    """
    h = np.asarray(fields, dtype=float)
    m = np.empty(h.size)
    if burn_in:
        state = with_field(state, float(h[0]))
        _, _, state = simulate(state, temperature, burn_in, rng, burn_in=0, thin=burn_in,
                               rule=rule)
    for i, value in enumerate(h):
        state = with_field(state, float(value))
        _, _, state = simulate(state, temperature, sweeps_per_step, rng, burn_in=0,
                               thin=sweeps_per_step, rule=rule)
        m[i] = state.m
    return h, m, state


def loop_area(fields: np.ndarray, magnetization: np.ndarray) -> float:
    """|closed integral of m dh| around a hysteresis loop (shoelace on the polygon)."""
    h = np.asarray(fields, dtype=float)
    m = np.asarray(magnetization, dtype=float)
    return float(abs(np.sum(m * np.roll(h, -1) - h * np.roll(m, -1))) / 2.0)


# ---------------------------------------------------------------------------
# Exact anchors and the mean-field approximation
# ---------------------------------------------------------------------------


def onsager_tc() -> float:
    """Onsager's exact critical temperature of the 2-D square lattice at h = 0.

    k_B T_c / J = 2 / ln(1 + sqrt 2) = 2.269185... Stated, not derived: the proof is the
    1944 tour de force this course does not reproduce.
    """
    return 2.0 / math.log(1.0 + math.sqrt(2.0))


def onsager_magnetization(temperature):
    """Exact spontaneous magnetization of the infinite 2-D lattice (Onsager, Yang 1952).

    m_0 = (1 - sinh(2J / (k_B T))^-4)^(1/8) below T_c, and 0 above. The exponent 1/8 is
    the 2-D Ising beta; mean field says 1/2.
    """
    t = np.asarray(temperature, dtype=float)
    if np.any(t <= 0):
        raise ValueError("temperature must be positive")
    inner = 1.0 - np.sinh(2.0 / t) ** -4.0
    out = np.where(t < onsager_tc(), np.clip(inner, 0.0, None) ** 0.125, 0.0)
    return float(out) if out.ndim == 0 else out


def ising_1d_exact(temperature, field: float = 0.0):
    """(e, m) per spin of the infinite periodic chain, from the transfer matrix.

    With K = J / (k_B T) and b = h / (k_B T), the larger eigenvalue is
    lambda = e^K cosh b + sqrt(e^2K sinh^2 b + e^-2K), and f = -k_B T ln lambda. Then
    m = sinh b / sqrt(sinh^2 b + e^-4K) and e = -d ln lambda / d beta; at h = 0,
    e = -J tanh K and m = 0 at every T > 0 -- no transition. The derivation is the advanced
    section's; here it is the anchor the simulation is checked against.
    """
    t = np.asarray(temperature, dtype=float)
    if np.any(t <= 0):
        raise ValueError("temperature must be positive")
    k = 1.0 / t
    b = field / t
    root = np.sqrt(np.sinh(b) ** 2 + np.exp(-4.0 * k))
    m = np.sinh(b) / root
    # ln lambda = K + ln(cosh b + root); differentiate in beta with J = 1 and h fixed.
    d_root = (field * np.sinh(b) * np.cosh(b) - 2.0 * np.exp(-4.0 * k)) / root
    e = -(1.0 + (field * np.sinh(b) + d_root) / (np.cosh(b) + root))
    if e.ndim == 0:
        return float(e), float(m)
    return e, m


def mean_field_magnetization(temperature, field: float = 0.0,
                             coordination: int = SQUARE_COORDINATION):
    """The largest solution of m = tanh((q J m + h) / (k_B T)), by bisection.

    At h = 0 it is 0 above k_B T_c^MF = q J and nonzero below. The right side minus m is
    positive at m = 0+ (below T_c) or for h > 0 and negative at m = 1, so the root at the
    top of [0, 1] is bracketed. For h < 0 the answer is minus the h > 0 one.
    """
    t = np.atleast_1d(np.asarray(temperature, dtype=float))
    if np.any(t <= 0):
        raise ValueError("temperature must be positive")
    sign = -1.0 if field < 0 else 1.0
    h = abs(field)
    lo = np.full(t.shape, 1e-300 if h == 0 else 0.0)
    hi = np.ones(t.shape)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        above = np.tanh((coordination * mid + h) / t) > mid
        lo = np.where(above, mid, lo)
        hi = np.where(above, hi, mid)
    m = 0.5 * (lo + hi)
    if h == 0:
        m = np.where(t >= coordination, 0.0, m)
    m = sign * m
    return float(m[0]) if np.ndim(temperature) == 0 else m


def mean_field_tc(coordination: int = SQUARE_COORDINATION) -> float:
    """k_B T_c^MF / J = q: 4 on the square lattice, and a spurious 2 on the chain."""
    return float(coordination)
