"""Transport: the fluctuations that carry particles, momentum and heat.

MODEL SPECIFICATION
    System:        an ensemble of independent random walkers on a line, standing in for tagged
                   molecules of a dilute gas; each walker's position, and from it its velocity,
                   is recorded at equally spaced times dt
    Dynamics:      steps of +/- l every tau -- independent (`sampling.random_walk`), or
                   repeating the previous step with probability q and otherwise drawn afresh
                   (`sampling.correlated_walk`, module 03's counterexample), so that steps k
                   apart have correlation q^k; the estimators here are dynamics-free
                   functions of whatever traces they are handed
    Boundary:      an unbounded line -- no walls, so the spreading is never confined
    Ensemble:      independent walkers realise the ensemble average directly; time and ensemble
                   averages agree by construction (independence), not by an ergodic argument
    Ignored:       walker-walker interactions, hydrodynamic backflow, convection and drift, and
                   any memory beyond what a supplied velocity trace carries
    Valid when:    times long compared with the velocity-correlation time; many walkers; step
                   distributions of finite variance
    Failure modes: correlated steps (D = l^2/(2 tau) fails, while D as the integral of the
                   velocity autocorrelation does not); times comparable to the correlation time
                   (ballistic spreading, the mean squared displacement growing as t^2); drift or
                   convection contaminating the mean squared displacement; walls, which
                   saturate it (module 04's box gas, `box_gas_trace`)

Three other things live here, each with narrower assumptions stated where it is defined: the
canonical energy samplers and the heat capacity read off their fluctuations (module 12's
identity Var(E) = k_B T^2 C_V, used as an instrument); the Einstein relation and Stokes drag
behind Perrin's measurement of Avogadro's number; and the mean-free-path estimates of D, eta
and kappa for a dilute hard-sphere gas, which are order-of-magnitude approximations by design.

THE IDEA
    A tagged molecule's displacement is the time integral of its velocity, so how far a cloud
    of them spreads is fixed by how long each one remembers its velocity:

        <x^2> -> 2 D t,        D = integral from 0 to infinity of <v(0) v(t)> dt.

    For independent steps the memory lasts one step and D = l^2/(2 tau); for module 03's
    persistent walk it lasts longer and D grows by (1 + q)/(1 - q). The same random flight,
    carrying momentum or energy instead of the molecule's identity, gives the viscosity and
    the thermal conductivity of a dilute gas.

ERROR BARS BY BATCHES
    Every estimator returns an `Estimate`, a value with one standard error. The error is not
    read off a fit's residuals: the points along one mean-squared-displacement curve are made
    of the same walkers and are strongly correlated, so a least-squares error bar would be far
    too small. Instead the walkers are split into independent batches, the estimator is run on
    each, and the scatter of the batch values sets the error -- the N^(-1/2) law of modules 00
    and 03, used as an instrument.

DIMENSIONS
    Walkers live on a line, so their D is one-dimensional: <x^2> = 2 D t. The kinetic-theory
    estimates are for a real gas in three dimensions, where <r^2> = 6 D t; a three-dimensional
    random flight is three one-dimensional walks, one per axis, sharing the same D.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Final

import numpy as np

from . import kinetics, partition, sampling
from .constants import K_B, R_GAS

#: Batches an error bar is estimated from. Twenty gives the error bar itself a relative
#: uncertainty of about 1/sqrt(2 x 19) = 16%, which is as well as an error bar needs knowing.
DEFAULT_BATCHES: Final[int] = 20

#: Walkers per FFT block in `velocity_autocorrelation`, which bounds its working memory.
_FFT_BLOCK: Final[int] = 1000


# ---------------------------------------------------------------------------
# A measured value with its error bar
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Estimate:
    """A measured value with one standard error -- the course's `value +- error`."""

    value: float
    error: float

    def consistent_with(self, other: Estimate, n_sigma: float = 2.0) -> bool:
        """True when the two differ by at most `n_sigma` standard errors, combined in quadrature.

        Quadrature is right for independent measurements. Two estimators run on the *same*
        walkers are positively correlated, so their difference scatters less than this
        assumes: the test errs towards calling them consistent, never against.
        """
        return abs(self.value - other.value) <= n_sigma * math.hypot(self.error, other.error)

    def agrees_with(self, expected: float, n_sigma: float = 3.0) -> bool:
        """True when `expected` lies within `n_sigma` standard errors of the value."""
        return abs(self.value - expected) <= n_sigma * self.error

    def __str__(self) -> str:
        return f"{self.value:.4g} +- {self.error:.2g}"


def _batched(estimator: Callable[[np.ndarray], float], data: np.ndarray, n_batches: int,
             linear: bool = False) -> Estimate:
    """The estimator on all the walkers, with an error bar from independent batches of them.

    A `linear` estimator -- one whose value on all the walkers is the walker-weighted mean of
    its values on the batches, as a slope fitted to a mean squared displacement is -- is not
    run a second time on the whole ensemble: the weighted mean is that value, exactly.
    """
    data = np.asarray(data)
    if n_batches < 2:
        raise ValueError("an error bar needs at least two batches")
    if data.shape[0] < 2 * n_batches:
        raise ValueError("need at least two walkers per batch")
    chunks = np.array_split(data, n_batches)
    batches = np.array([estimator(chunk) for chunk in chunks])
    if linear:
        sizes = np.array([chunk.shape[0] for chunk in chunks], dtype=float)
        value = float(np.sum(sizes * batches) / sizes.sum())
    else:
        value = float(estimator(data))
    return Estimate(value, float(batches.std(ddof=1) / math.sqrt(n_batches)))


# ---------------------------------------------------------------------------
# Walkers with physics attached
# ---------------------------------------------------------------------------


def walker_trajectories(n_walkers: int, n_steps: int, step_length: float,
                        rng: np.random.Generator, persistence: float = 0.0) -> np.ndarray:
    """Positions [m] of independent walkers stepping +/- `step_length`, each starting at 0.

    Shape (n_walkers, n_steps + 1); column k is the position after k steps. With
    `persistence = 0` this is module 03's coin walk (`sampling.random_walk`); otherwise each
    step repeats the one before with probability `persistence` and is drawn afresh -- left or
    right, at random -- the rest of the time: module 03's correlated walk
    (`sampling.correlated_walk`) -- a walker that keeps its velocity for a while, as a
    molecule does between collisions. Either way the positions lie on a lattice of spacing
    2 x step_length, which `d_from_histogram` needs to be told.
    """
    if step_length <= 0:
        raise ValueError("step_length must be positive")
    if persistence == 0.0:
        positions = sampling.random_walk(n_walkers, n_steps, rng, "pm1")
    else:
        positions = sampling.correlated_walk(n_walkers, n_steps, persistence, rng)
    positions *= step_length
    return positions


def walker_velocities(trajectories: np.ndarray, dt: float) -> np.ndarray:
    """Velocity [m/s] during each step, (x_{k+1} - x_k) / dt: shape (n_walkers, n_steps)."""
    if dt <= 0:
        raise ValueError("dt must be positive")
    return np.diff(np.asarray(trajectories, dtype=float), axis=1) / dt


def msd(trajectories: np.ndarray) -> np.ndarray:
    """Mean squared displacement <(x(t) - x(0))^2> at every recorded time, over all walkers.

    Displacements are measured from each walker's own start, and every walker counts at every
    time. Worked through in blocks of walkers, so a large ensemble never needs a second copy
    of itself in memory.
    """
    trajectories = np.asarray(trajectories, dtype=float)
    if trajectories.ndim != 2 or trajectories.shape[0] < 1:
        raise ValueError("trajectories must have shape (n_walkers, n_times)")
    total = np.zeros(trajectories.shape[1])
    for start in range(0, trajectories.shape[0], _FFT_BLOCK):
        block = trajectories[start:start + _FFT_BLOCK]
        displacement = block - block[:, :1]
        total += np.einsum("ij,ij->j", displacement, displacement)
    return total / trajectories.shape[0]


def diffusion_greens_function(x, t: float, d: float):
    """The diffusion equation's point-source solution, (4 pi D t)^(-1/2) exp(-x^2/(4 D t)) [1/m].

    Normalised to one, with variance 2 D t: a cloud released at the origin at t = 0. A
    prediction, never a fit -- D is an input.
    """
    if t <= 0 or d <= 0:
        raise ValueError("t and D must be positive")
    x = np.asarray(x, dtype=float)
    width = 4.0 * d * t
    result = np.exp(-x**2 / width) / np.sqrt(np.pi * width)
    return float(result) if result.ndim == 0 else result


_erfc = np.frompyfunc(math.erfc, 1, 1)
_erf = np.frompyfunc(math.erf, 1, 1)


def step_profile(x, t: float, d: float):
    """Concentration relative to the source, (1/2) erfc(x / (2 sqrt(D t))): a layer diffusing out.

    The solution for a dye layer filling x < 0 at t = 0 and clear water above it. It depends
    on x and t only through x / sqrt(D t), so every contour -- the place where the dye has
    reached a quarter of its source strength, say -- advances as sqrt(t). That, not a speed,
    is what a diffusion front has.
    """
    if t <= 0 or d <= 0:
        raise ValueError("t and D must be positive")
    x = np.asarray(x, dtype=float)
    result = 0.5 * np.asarray(_erfc(x / (2.0 * math.sqrt(d * t))), dtype=float)
    return float(result) if result.ndim == 0 else result


def persistent_walk_d(step_length: float, tau: float, persistence: float = 0.0) -> float:
    """Exact D [m^2/s] of the walk `walker_trajectories` draws: (l^2/(2 tau)) (1 + q)/(1 - q).

    At q = 0 this is the independent-step D = l^2/(2 tau) of the diffusion equation. A step
    that repeats its predecessor with probability q, and is otherwise drawn afresh, has
    correlation q^k with the step k later, and summing that geometric series is module 03's
    variance inflation -- or, equivalently, the integral of the velocity autocorrelation.
    """
    if step_length <= 0 or tau <= 0:
        raise ValueError("step_length and tau must be positive")
    if not 0.0 <= persistence < 1.0:
        raise ValueError("persistence must lie in [0, 1)")
    return step_length**2 / (2.0 * tau) * (1.0 + persistence) / (1.0 - persistence)


def persistent_walk_msd(n_steps, step_length: float, persistence: float = 0.0):
    """Exact <x^2> [m^2] after n steps: l^2 [n (1 + q)/(1 - q) - 2 q (1 - q^n)/(1 - q)^2].

    Ballistic, n^2 l^2, while n is small compared with 1/(1 - q); diffusive, a straight line
    of slope 2 D tau with a small negative offset, long after. At q = 0 it is n l^2 at every n.
    """
    if not 0.0 <= persistence < 1.0:
        raise ValueError("persistence must lie in [0, 1)")
    n = np.asarray(n_steps, dtype=float)
    q = persistence
    result = step_length**2 * (n * (1.0 + q) / (1.0 - q) - 2.0 * q * (1.0 - q**n) / (1.0 - q) ** 2)
    return float(result) if result.ndim == 0 else result


# ---------------------------------------------------------------------------
# Three independent measurements of D
# ---------------------------------------------------------------------------


def d_from_msd(trajectories: np.ndarray, dt: float, start: float = 0.1,
               n_batches: int = DEFAULT_BATCHES) -> Estimate:
    """D [m^2/s] from the slope of the mean squared displacement, <x^2> = 2 D t + c.

    The intercept c is fitted too, and the first `start` fraction of the record is left out:
    a walker with memory spreads ballistically at first, and its straight diffusive line is
    offset from the origin (`persistent_walk_msd`). For independent steps c is zero and
    nothing is lost.
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    if not 0.0 <= start < 1.0:
        raise ValueError("start must lie in [0, 1)")

    def estimate(walkers: np.ndarray) -> float:
        curve = msd(walkers)
        first = max(1, int(start * (curve.size - 1)))
        times = np.arange(curve.size) * dt
        return float(np.polyfit(times[first:], curve[first:], 1)[0] / 2.0)

    return _batched(estimate, trajectories, n_batches, linear=True)


def _bin_edges(positions: np.ndarray, n_bins: int, lattice: float | None) -> np.ndarray:
    """Edges spanning +/-4 standard deviations, a whole number of lattice sites per bin."""
    spread = float(positions.std())
    low, high = -4.0 * spread, 4.0 * spread
    if lattice is None:
        return np.linspace(low, high, n_bins + 1)
    # The trap module 03 documents: bins of arbitrary width over a lattice-valued sample hold
    # alternately more and fewer reachable sites. Anchoring every edge half a spacing from an
    # occupied site, and making each bin a whole number of sites wide, removes it.
    width = max(round((high - low) / n_bins / lattice), 1) * lattice
    anchor = float(positions[0]) - 0.5 * lattice
    first = anchor + math.floor((low - anchor) / width) * width
    return first + width * np.arange(int(math.ceil((high - first) / width)) + 1)


def fit_gaussian_variance(positions: np.ndarray, n_bins: int = 40,
                          lattice: float | None = None) -> float:
    """Variance [m^2] of the zero-mean Gaussian that best fits the histogram of `positions`.

    Least squares on the fraction of the walkers in each bin, against the Gaussian's
    probability integrated exactly over that bin. This reads the *shape* of the cloud -- it is
    dominated by the well-populated middle -- where the mean squared displacement is
    dominated by the tails, which is what makes the two estimators of D different
    measurements and not one measurement done twice. Pass `lattice` for walker positions
    (2 x step_length); see `_bin_edges` for why.
    """
    positions = np.asarray(positions, dtype=float).ravel()
    if positions.size < 2:
        raise ValueError("a histogram fit needs at least two walkers")
    edges = _bin_edges(positions, n_bins, lattice)
    fractions = np.histogram(positions, bins=edges)[0] / positions.size
    return _fit_variance_to_bins(edges, fractions, float(np.mean(positions**2)),
                                 conditional=False)


def fit_binned_gaussian_variance(edges, counts) -> float:
    """Variance of the zero-mean Gaussian that best fits a histogram given as edges and counts.

    For data that arrive already binned -- a published table, such as Perrin's counts of
    displacements falling between successive multiples of 1.7 micrometres. The model is
    normalised over the range the table covers, so a table that stops before its tail is
    fitted as what it is, not as if the missing tail were empty. The same normalisation makes
    a table of |x|, with bins from zero up, need no special treatment: a Gaussian in |x| is the
    Gaussian in x on the positive side, doubled, and the factor of two cancels.
    """
    edges = np.asarray(edges, dtype=float)
    counts = np.asarray(counts, dtype=float)
    if edges.ndim != 1 or counts.shape != (edges.size - 1,):
        raise ValueError("need one count per bin: len(counts) == len(edges) - 1")
    if np.any(np.diff(edges) <= 0):
        raise ValueError("edges must increase")
    if counts.sum() <= 0 or np.any(counts < 0):
        raise ValueError("counts must be non-negative and not all zero")
    centres = 0.5 * (edges[:-1] + edges[1:])
    guess = float(np.sum(counts * centres**2) / counts.sum())
    return _fit_variance_to_bins(edges, counts / counts.sum(), guess, conditional=True)


def binned_variance_estimate(edges, counts, rng: np.random.Generator,
                             n_resamples: int = 400) -> Estimate:
    """`fit_binned_gaussian_variance` with an error bar from resampling the counts.

    A published table has no walkers to split into batches, so the error comes from the
    bootstrap instead: draw new tables of the same total from the observed bin fractions
    (multinomially), refit each, and take the scatter of the fits. It measures the counting
    noise of a finite table -- for Perrin's two hundred displacements, about ten per cent in the
    variance -- and nothing about how the displacements were measured.
    """
    counts = np.asarray(counts, dtype=float)
    value = fit_binned_gaussian_variance(edges, counts)
    if n_resamples < 2:
        raise ValueError("need at least two resamples")
    total = int(round(counts.sum()))
    resampled = rng.multinomial(total, counts / counts.sum(), size=n_resamples)
    fits = np.array([fit_binned_gaussian_variance(edges, row) for row in resampled])
    return Estimate(value, float(fits.std(ddof=1)))


def _fit_variance_to_bins(edges: np.ndarray, fractions: np.ndarray, guess: float,
                          conditional: bool) -> float:
    """Least squares of bin fractions against a zero-mean Gaussian's exact bin probabilities."""

    def misfit(log_variance: float) -> float:
        cumulative = np.asarray(_erf(edges / math.sqrt(2.0 * math.exp(log_variance))),
                                dtype=float)
        model = 0.5 * np.diff(cumulative)   # P(a < x < b) for x ~ N(0, variance)
        if conditional:
            model = model / model.sum()
        return float(np.sum((fractions - model) ** 2))

    # Golden-section search on ln(variance), bracketing a factor of four either side of the
    # guess. The misfit has a single minimum there, and no scipy is needed.
    guess = math.log(guess)
    low, high = guess - math.log(4.0), guess + math.log(4.0)
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    left, right = high - ratio * (high - low), low + ratio * (high - low)
    f_left, f_right = misfit(left), misfit(right)
    for _ in range(60):
        if f_left < f_right:
            high, right, f_right = right, left, f_left
            left = high - ratio * (high - low)
            f_left = misfit(left)
        else:
            low, left, f_left = left, right, f_right
            right = low + ratio * (high - low)
            f_right = misfit(right)
    return math.exp(0.5 * (low + high))


def d_from_histogram(trajectories: np.ndarray, dt: float,
                     snapshots: Sequence[float] = (0.25, 0.5, 0.75, 1.0), n_bins: int = 40,
                     lattice: float | None = None,
                     n_batches: int = DEFAULT_BATCHES) -> Estimate:
    """D [m^2/s] from fitting the cloud's histogram to the Green's function at several times.

    At each snapshot -- a fraction of the record -- the fitted Gaussian variance is found
    (`fit_gaussian_variance`); D is half the slope of variance against time. Using the slope
    rather than variance / (2t) at one time makes the estimate immune to the constant offset a
    walker with memory carries (`persistent_walk_msd`).
    """
    if dt <= 0:
        raise ValueError("dt must be positive")
    fractions = np.asarray(list(snapshots), dtype=float)
    if fractions.size < 2 or np.any(fractions <= 0) or np.any(fractions > 1):
        raise ValueError("need at least two snapshots, each a fraction in (0, 1]")

    def estimate(walkers: np.ndarray) -> float:
        n_steps = walkers.shape[1] - 1
        columns = np.unique(np.maximum(1, np.round(fractions * n_steps).astype(int)))
        variances = [fit_gaussian_variance(walkers[:, k] - walkers[:, 0], n_bins, lattice)
                     for k in columns]
        return float(np.polyfit(columns * dt, variances, 1)[0] / 2.0)

    return _batched(estimate, trajectories, n_batches)


def velocity_autocorrelation(velocities: np.ndarray, max_lag: int) -> np.ndarray:
    """C(k) = <v(t) v(t + k dt)> [m^2/s^2] for k = 0 ... max_lag, over walkers and time origins.

    Averaging over every time origin, not only t = 0, assumes the velocities are stationary --
    true of the walks here and of an equilibrium gas, false of a cloud still settling. Each
    lag is divided by its own number of pairs, so long lags are not biased towards zero. The
    products are summed by FFT, block by block, which is what keeps ten thousand walkers by a
    thousand steps to well under a second.
    """
    v = np.asarray(velocities, dtype=float)
    if v.ndim != 2:
        raise ValueError("velocities must have shape (n_walkers, n_steps)")
    n_walkers, n_steps = v.shape
    if not 0 <= max_lag < n_steps:
        raise ValueError("max_lag must lie in [0, n_steps)")
    size = 1 << int(math.ceil(math.log2(2 * n_steps)))  # zero-padded: no wrap-around
    total = np.zeros(max_lag + 1)
    for start in range(0, n_walkers, _FFT_BLOCK):
        spectrum = np.fft.rfft(v[start:start + _FFT_BLOCK], n=size, axis=1)
        products = np.fft.irfft(spectrum * np.conj(spectrum), n=size, axis=1)
        total += products[:, :max_lag + 1].sum(axis=0)
    return total / (n_walkers * (n_steps - np.arange(max_lag + 1)))


def green_kubo_running(vacf: np.ndarray, dt: float) -> np.ndarray:
    """Running integral dt [C(0)/2 + C(1) + ... + C(K)] [m^2/s] for every cut-off K.

    The trapezoid rule for the integral of the velocity autocorrelation, which for velocities
    held constant over each step is exact, not an approximation: x after n steps is dt times
    the sum of n velocities, and its mean square, divided by 2 n dt, tends to exactly this
    sum. Plotted against K it rises and levels off; the plateau is D.
    """
    c = np.asarray(vacf, dtype=float)
    if dt <= 0:
        raise ValueError("dt must be positive")
    return dt * (np.cumsum(c) - 0.5 * c[0])


def d_from_vacf(velocities: np.ndarray, dt: float, max_lag: int | None = None,
                n_batches: int = DEFAULT_BATCHES) -> Estimate:
    """D [m^2/s] as the integral of the velocity autocorrelation -- Green-Kubo, in miniature.

    No positions are used at all: only how long each walker remembers its velocity.
    `max_lag` (default a tenth of the record) is where the integral is cut off. Too short
    misses memory that has not yet decayed; too long sums pure noise, since every lag beyond
    the memory adds a random term and nothing else. The running integral
    (`green_kubo_running`) shows where the plateau begins.
    """
    v = np.asarray(velocities, dtype=float)
    if max_lag is None:
        max_lag = max(1, v.shape[1] // 10)

    def estimate(walkers: np.ndarray) -> float:
        return float(green_kubo_running(velocity_autocorrelation(walkers, max_lag), dt)[-1])

    return _batched(estimate, v, n_batches, linear=True)


# ---------------------------------------------------------------------------
# Module 04's box, which cannot diffuse
# ---------------------------------------------------------------------------


def box_gas_trace(state: kinetics.GasState, dt: float,
                  n_steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Positions and velocities of module 04's gas after every step: two (n_steps + 1, N, d) arrays.

    Runs `kinetics.simulate` one step at a time, so the dynamics are exactly module 04's --
    free flight and specular walls, no collisions between particles. Nothing randomises a
    velocity, so nothing diffuses: a particle flies straight until a wall reverses it, its
    velocity autocorrelation turns negative instead of decaying, and its mean squared
    displacement stops growing at L^2/6 per axis, the value for two independent uniform
    positions in a box of side L.
    """
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    positions = np.empty((n_steps + 1,) + state.positions.shape)
    velocities = np.empty_like(positions)
    positions[0], velocities[0] = state.positions, state.velocities
    for step in range(1, n_steps + 1):
        state = kinetics.simulate(state, dt, 1).final_state
        positions[step], velocities[step] = state.positions, state.velocities
    return positions, velocities


# ---------------------------------------------------------------------------
# A heat capacity from the noise alone
# ---------------------------------------------------------------------------
#
# Module 12's identity, Var(E) = k_B T^2 C_V, holds for a system whose energy is free to
# fluctuate -- the canonical ensemble. These samplers draw canonical energies of the course's
# two simplest systems; `energy_fluctuation_cv` turns any set of independent canonical
# energies into a heat capacity, without heating anything.


def gas_energy_samples(n_particles: int, temperature: float, mass: float, n_samples: int,
                       rng: np.random.Generator, dimension: int = 3,
                       fix_temperature: bool = False,
                       remove_drift: bool = False) -> np.ndarray:
    """Total kinetic energies [J] of `n_samples` independently drawn copies of module 04's gas.

    Each copy comes from `kinetics.initialise_gas` with the two flags passed through, so the
    ensemble is chosen exactly as module 04 chooses it. `fix_temperature=False` is the
    canonical draw; `True` rescales every copy to the same energy, the microcanonical one,
    whose energy does not fluctuate at all. `remove_drift=True` subtracts each copy's net
    momentum, which freezes `dimension` of its degrees of freedom -- and the fluctuations
    notice: C_V comes out (d/2)(N - 1) k_B instead of (d/2) N k_B.
    """
    if n_samples < 2:
        raise ValueError("a fluctuation needs at least two samples")
    box = (1.0,) * dimension
    return np.array([
        kinetics.initialise_gas(n_particles, box, temperature, mass, rng,
                                remove_drift=remove_drift,
                                fix_temperature=fix_temperature).kinetic_energy
        for _ in range(n_samples)
    ])


def two_level_energy_samples(n_systems: int, gap: float, temperature: float, n_samples: int,
                             rng: np.random.Generator) -> np.ndarray:
    """Energies [J] of `n_samples` canonical draws of `n_systems` independent two-level systems.

    Each system is excited with module 11's probability 1/(exp(gap/k_B T) + 1), independently,
    so the number excited is binomial and the energy is gap times it.
    """
    if n_systems < 1 or n_samples < 2:
        raise ValueError("need at least one system and two samples")
    excited = partition.two_level_energy(gap, temperature) / gap
    return gap * rng.binomial(n_systems, excited, size=n_samples).astype(float)


def energy_fluctuation_cv(energies: np.ndarray, temperature: float) -> Estimate:
    """C_V = Var(E) / (k_B T^2) [J/K]: a heat capacity read off the noise, with no heating at all.

    The samples must be independent canonical energies: a microcanonical sample has no
    variance to read, and a correlated time series would make the error bar too small by the
    factor module 15 measured. The error is the standard error of the sample variance,
    sqrt((m_4 - s^4) / n), with m_4 the fourth central moment -- it shrinks as the samples
    grow; the variance itself does not.
    """
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    e = np.asarray(energies, dtype=float).ravel()
    if e.size < 2:
        raise ValueError("a fluctuation needs at least two samples")
    deviation = e - e.mean()
    variance = float(deviation @ deviation / (e.size - 1))
    fourth = float(np.mean(deviation**4))
    scale = K_B * temperature**2
    return Estimate(variance / scale, math.sqrt(max(fourth - variance**2, 0.0) / e.size) / scale)


# ---------------------------------------------------------------------------
# The Einstein relation, Stokes drag, and Perrin's Avogadro number
# ---------------------------------------------------------------------------


def stokes_friction(viscosity: float, radius: float) -> float:
    """Drag coefficient zeta = 6 pi eta a [kg/s] of a sphere of radius a moving slowly in a fluid.

    Valid when the flow round the sphere is slow and smooth (Reynolds number far below one,
    which a micron bead in water satisfies by a factor of a million) and the sphere is large
    compared with the fluid's molecules.
    """
    if viscosity <= 0 or radius <= 0:
        raise ValueError("viscosity and radius must be positive")
    return 6.0 * math.pi * viscosity * radius


def einstein_diffusion(temperature: float, friction: float) -> float:
    """The Einstein relation, D = k_B T / zeta [m^2/s]: diffusion fixed by drag and temperature.

    A fluctuation (how fast a particle wanders) set by a dissipation (how hard the fluid
    resists a push), with k_B T as the exchange rate.
    """
    if temperature <= 0 or friction <= 0:
        raise ValueError("temperature and friction must be positive")
    return K_B * temperature / friction


def avogadro_from_diffusion(d: float, temperature: float, viscosity: float,
                            radius: float) -> float:
    """N_A = R T / (6 pi eta a D) [1/mol]: Perrin's route from a wandering bead to atoms.

    Inverts the Einstein relation with Stokes drag for k_B, and divides the gas constant --
    measured with a balance and a manometer, with no reference to molecules -- by it.
    """
    if d <= 0:
        raise ValueError("D must be positive")
    return R_GAS * temperature / (stokes_friction(viscosity, radius) * d)


# ---------------------------------------------------------------------------
# Mean-free-path estimates for a dilute gas
# ---------------------------------------------------------------------------


def hard_sphere_cross_section(diameter: float) -> float:
    """sigma = pi d^2 [m^2]: two spheres of diameter d collide when their centres pass within d."""
    if diameter <= 0:
        raise ValueError("diameter must be positive")
    return math.pi * diameter**2


def diameter_from_vdw_b(b: float) -> float:
    """Molecular diameter d = (3 b / (2 pi))^(1/3) [m] from the van der Waals b per molecule [m^3].

    Two spheres of diameter d keep their centres d apart, so each pair excludes a sphere of
    volume (4 pi/3) d^3; shared between the two, that is b = (2 pi/3) d^3 per molecule. Module
    02's equation of state thereby measures the size of a molecule; `gases.
    vdw_constants_from_critical` gets b from the critical point.
    """
    if b <= 0:
        raise ValueError("b must be positive")
    return (3.0 * b / (2.0 * math.pi)) ** (1.0 / 3.0)


@dataclass(frozen=True)
class KineticEstimates:
    """Mean-free-path estimates for a dilute hard-sphere gas in three dimensions, in SI units.

    Order of magnitude only: every molecule is given the mean speed and the mean free path,
    and the 1/3 counts directions crudely. Real dilute gases differ by factors of order one --
    for a monatomic gas the measured kappa / (eta c_v / m) is close to 5/2, where these give 1.
    """

    mean_free_path: float  # m
    collision_rate: float  # 1/s
    mean_speed: float  # m/s
    diffusion: float  # m^2/s: self-diffusion, (1/3) vbar lambda
    viscosity: float  # Pa s: (1/3) n m vbar lambda
    thermal_conductivity: float  # W/(m K): (1/3) n c_v vbar lambda


def kinetic_estimates(n_density: float, temperature: float, mass: float, sigma: float,
                      heat_capacity_per_particle: float = 1.5 * K_B) -> KineticEstimates:
    """The transport trio of a dilute gas, from one random flight carrying three things.

    A molecule crossing a plane brings with it whatever it carried from about a mean free path
    away: its identity (diffusion), its share of the flow's momentum (viscosity), its thermal
    energy (conduction). The flux of each is -(1/3) n vbar lambda times the gradient of the
    per-molecule quantity, so D = vbar lambda / 3, eta = n m D and kappa = n c_v D. Since
    lambda = 1/(sqrt(2) n sigma), eta and kappa do not depend on n at all. The default c_v is
    (3/2) k_B per molecule, a monatomic gas; pass (5/2) k_B for a diatomic one.
    """
    if heat_capacity_per_particle <= 0:
        raise ValueError("heat capacity per particle must be positive")
    path = kinetics.mean_free_path(n_density, sigma)
    speed = kinetics.mean_speed(temperature, mass)
    diffusion = speed * path / 3.0
    return KineticEstimates(
        mean_free_path=path,
        collision_rate=speed / path,
        mean_speed=speed,
        diffusion=diffusion,
        viscosity=n_density * mass * diffusion,
        thermal_conductivity=n_density * heat_capacity_per_particle * diffusion,
    )


def knudsen_number(mean_free_path: float, length: float) -> float:
    """Kn = lambda / L: the mean free path against the scale on which anything changes.

    Every transport coefficient here assumes Kn << 1 -- that a molecule collides many times
    before it meets a gradient's worth of change, so each small parcel is nearly in
    equilibrium. Near Kn ~ 1 molecules fly from wall to wall without colliding, and viscosity
    and conductivity stop being properties of the gas.
    """
    if mean_free_path <= 0 or length <= 0:
        raise ValueError("lengths must be positive")
    return mean_free_path / length
