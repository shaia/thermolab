"""Independent draws: sample averages, random walks, and the central limit theorem.

MODEL SPECIFICATION
    System:        N independent repetitions of one fixed random draw — read directly as the
                   face of a die, or accumulated into the position of a walker on a line; the
                   observables are the sample average, the ensemble histogram and its spread
    Dynamics:      none beyond accumulation — every draw is independent of every other, with
                   no memory between them and nothing that could pull a running total back
    Boundary:      none — the line is unbounded, and N, the number of steps and the step
                   distribution are all fixed for one experiment
    Ensemble:      independent trials: every die face equally probable by fiat, every walker
                   repeating the same experiment — the same kind of postulate the course will
                   later make about the microstates of a gas
    Ignored:       all physics — no energy, particles, medium or container; for dice also the
                   bounce dynamics, pip asymmetry and deterministic chaos that are the actual
                   reason a throw looks random
    Valid when:    draws are genuinely independent and have finite variance; a seeded
                   pseudo-random generator satisfies both by construction
    Failure modes: correlated draws (`correlated_walk` is the course's own counterexample),
                   loaded dice (non-uniform faces), infinite-variance steps such as Cauchy,
                   and any question about a *single* roll or path beyond its distribution

The point of dice and drunkards is that they are not physics. Strip away energy, particles
and containers, and the course's central mechanism is still there: individual outcomes stay
unpredictable while their average becomes reproducible, with a relative scatter that falls as
N^(-1/2) — and the *shape* the ensemble settles into is a Gaussian whatever the individual
draw looked like, which is the central limit theorem.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from .multiplicity import log_multiplicity_array


def die_mean(n_faces: int = 6) -> float:
    """Mean of one uniform die, (n_faces + 1) / 2 — for a six-sided die, 7/2."""
    _validate_faces(n_faces)
    return (n_faces + 1) / 2.0


def die_variance(n_faces: int = 6) -> float:
    """Variance of one uniform die, (n_faces^2 - 1) / 12 — for a six-sided die, 35/12.

    Worth deriving by hand once: it is the sum over faces of (k - mean)^2 / n_faces, and it
    collapses to this closed form. A one-faced die has zero variance, as it must.
    """
    _validate_faces(n_faces)
    return (n_faces**2 - 1) / 12.0


def die_relative_spread(n_faces: int = 6) -> float:
    """The dimensionless scatter of one die, sigma / mean — about 0.488 for six faces.

    This is the coefficient in front of N^(-1/2): the relative spread of an average of N dice
    is this number divided by sqrt(N). Being a ratio, it is what survives a change of units.
    """
    return float(np.sqrt(die_variance(n_faces)) / die_mean(n_faces))


def roll_dice(n_rolls: int, rng: np.random.Generator, n_faces: int = 6) -> np.ndarray:
    """Roll one die `n_rolls` times; return the faces shown as an integer array."""
    if n_rolls < 1:
        raise ValueError("n_rolls must be positive")
    _validate_faces(n_faces)
    return rng.integers(1, n_faces + 1, size=n_rolls)


def running_average(values: np.ndarray) -> np.ndarray:
    """Average of the first k entries, for every k — the curve that visibly settles.

    Nothing corrects an early run of high rolls; it is simply divided by an ever larger k
    until it no longer matters. The convergence is by dilution, not by compensation.
    """
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        raise ValueError("running_average needs at least one value")
    return np.cumsum(values) / np.arange(1, values.size + 1)


def sample_averages(n_per_sample: int, n_samples: int, rng: np.random.Generator,
                    n_faces: int = 6) -> np.ndarray:
    """Repeat the experiment "average `n_per_sample` dice" `n_samples` times.

    Returns one average per repetition, so the scatter *across* repetitions measures how
    reproducible a single experiment is — which is the quantity the whole module is about.
    """
    if n_per_sample < 1 or n_samples < 1:
        raise ValueError("n_per_sample and n_samples must be positive")
    _validate_faces(n_faces)
    draws = rng.integers(1, n_faces + 1, size=(n_samples, n_per_sample))
    return draws.mean(axis=1)


def relative_spread_of_average(n_per_sample: int, n_samples: int, rng: np.random.Generator,
                               n_faces: int = 6) -> float:
    """Measured standard deviation of the sample average, divided by its mean.

    Compare against `die_relative_spread(n_faces) / sqrt(n_per_sample)`. Reported as a ratio
    because an absolute spread carries the units of the underlying quantity and so cannot be
    compared between systems; this number can.
    """
    if n_samples < 2:
        raise ValueError("estimating a spread needs at least two repetitions")
    averages = sample_averages(n_per_sample, n_samples, rng, n_faces)
    return float(averages.std(ddof=1) / abs(averages.mean()))


def predicted_relative_spread(n_per_sample: int, n_faces: int = 6) -> float:
    """The analytic answer, (sigma_1 / mu_1) * n_per_sample^(-1/2).

    Derived on the module page from two facts only: means always add, and variances add for
    *independent* quantities.
    """
    if n_per_sample < 1:
        raise ValueError("n_per_sample must be positive")
    return die_relative_spread(n_faces) / np.sqrt(n_per_sample)


# ---------------------------------------------------------------------------
# Random walks and the central limit theorem
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StepDist:
    """One step distribution, carrying the exact moments its sampler was built from.

    Keeping `mean` and `variance` beside the sampler is what makes the Gaussian overlays
    honest: they are evaluated from the distribution's *known* moments, never estimated from
    the very sample they are about to be compared against. An overlay fitted to its own data
    agrees with anything and so tests nothing.
    """

    name: str
    mean: float
    variance: float
    sampler: Callable[[tuple[int, ...], np.random.Generator], np.ndarray]

    @property
    def std(self) -> float:
        """sigma_1, the standard deviation of one step."""
        return float(np.sqrt(self.variance))

    def draw(self, size: tuple[int, ...], rng: np.random.Generator) -> np.ndarray:
        """`size` independent steps, always as float64 so sums never wrap an integer type."""
        return np.asarray(self.sampler(size, rng), dtype=float)


# Student-t with 5 degrees of freedom has variance nu/(nu - 2) = 5/3: visibly heavy-tailed,
# yet finite-variance, so the CLT hypotheses still hold and the collapse still happens (just
# more slowly). Cauchy — nu = 1, no variance at all — is deliberately left to the problem set,
# where its failure is the point.
_STEP_DISTRIBUTIONS: dict[str, StepDist] = {
    "pm1": StepDist(
        "pm1", 0.0, 1.0, lambda size, rng: rng.integers(0, 2, size=size) * 2.0 - 1.0
    ),
    "biased": StepDist(
        "biased", 0.2, 0.96, lambda size, rng: np.where(rng.random(size) < 0.6, 1.0, -1.0)
    ),
    "uniform": StepDist(
        "uniform", 0.0, 1.0 / 3.0, lambda size, rng: rng.uniform(-1.0, 1.0, size=size)
    ),
    "heavy": StepDist(
        "heavy", 0.0, 5.0 / 3.0, lambda size, rng: rng.standard_t(5, size=size)
    ),
}


def step_distribution(name: str = "pm1") -> StepDist:
    """The named step distribution, with its exact mean and variance attached.

    "pm1"      +/-1 fair coin steps — the drunkard's walk, and the binomial's home ground
    "biased"   +/-1 with probability 0.6 to the right — drift and spread side by side
    "uniform"  steps drawn uniformly from [-1, 1] — continuous, no lattice
    "heavy"    Student-t with 5 degrees of freedom — heavy tails, still finite variance

    The four exist to make one point: they have wildly different shapes, and every walk built
    from them ends up Gaussian. Only mu_1 and sigma_1 survive into the answer.
    """
    try:
        return _STEP_DISTRIBUTIONS[name]
    except KeyError:
        known = ", ".join(sorted(_STEP_DISTRIBUTIONS))
        raise ValueError(f"unknown step distribution {name!r}; choose from {known}") from None


def random_walk(n_walkers: int, n_steps: int, rng: np.random.Generator,
                step: StepDist | str = "pm1", dim: int = 1) -> np.ndarray:
    """Trajectories of `n_walkers` independent walkers, each starting at the origin.

    Shape is (n_walkers, n_steps + 1) in one dimension and (n_walkers, n_steps + 1, dim)
    above it. Column 0 is x_0 = 0, so column t holds the sum of the first t steps — which is
    the whole model: a walker's position *is* a sum of independent draws.
    """
    if n_walkers < 1 or n_steps < 1:
        raise ValueError("n_walkers and n_steps must be positive")
    if dim < 1:
        raise ValueError("dim must be at least 1")

    steps = _as_step_dist(step).draw((n_walkers, n_steps, dim), rng)
    positions = np.zeros((n_walkers, n_steps + 1, dim))
    positions[:, 1:, :] = np.cumsum(steps, axis=1)
    return positions[:, :, 0] if dim == 1 else positions


def walker_spread(trajectories: np.ndarray) -> np.ndarray:
    """Cross-walker spread at every time — one number per column, the sqrt(t) curve.

    In one dimension this is the ordinary standard deviation across walkers. In higher
    dimensions the components' variances are added before the square root, which is the
    root-mean-square distance from the ensemble mean and reduces to the 1-D case exactly.
    """
    trajectories = np.asarray(trajectories, dtype=float)
    if trajectories.ndim == 2:
        return trajectories.std(axis=0, ddof=1)
    if trajectories.ndim == 3:
        return np.sqrt(trajectories.var(axis=0, ddof=1).sum(axis=-1))
    raise ValueError("trajectories must have shape (n_walkers, n_times[, dim])")


def walker_histogram(positions: np.ndarray, n_bins: int = 60,
                     span: tuple[float, float] | None = None,
                     lattice: float | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Bin centres and unit-area density of one time slice of the walker cloud.

    Normalised to unit area rather than to counts so it can be plotted against a probability
    density without a fudge factor — and so that the comparison survives changing n_walkers.

    `span` fixes the bin edges instead of letting the data choose them, which is what makes
    two histograms comparable: without it, a wider cloud silently gets wider bins and the
    spreading being measured is scaled away. Walkers outside the span are dropped, so the
    displayed area is then the retained fraction rather than exactly 1.

    `lattice` is the spacing of the underlying discrete positions, and passing it is not
    cosmetic. A +/-1 walk after t steps can only occupy sites 2 apart; bin an integer-valued
    sample like that on arbitrary edges and neighbouring bins capture different numbers of
    reachable sites, so the histogram alternates tall/short with a swing that has nothing to
    do with the data. Measured on the standardized coin sum at n = 250, arbitrary bins swing
    100% peak to peak where sampling noise accounts for 3%; some bins can even fall between
    two sites and be empty by construction. Given `lattice`, the edges are widened to a whole
    number of spacings and anchored so every bin holds exactly that many sites, which puts the
    residual back down at the sampling noise.
    """
    positions = np.asarray(positions, dtype=float).ravel()
    if positions.size < 2:
        raise ValueError("a histogram needs at least two walkers")
    if n_bins < 1:
        raise ValueError("n_bins must be positive")
    if lattice is not None and lattice <= 0.0:
        raise ValueError("lattice spacing must be positive")

    if lattice is None:
        density, edges = np.histogram(positions, bins=n_bins, range=span, density=True)
    else:
        density, edges = np.histogram(
            positions, bins=_lattice_edges(positions, n_bins, span, lattice), density=True
        )
    return 0.5 * (edges[:-1] + edges[1:]), density


def _lattice_edges(positions: np.ndarray, n_bins: int, span: tuple[float, float] | None,
                   lattice: float) -> np.ndarray:
    """Edges a whole number of lattice spacings wide, with a lattice site at every centre."""
    low, high = span if span is not None else (float(positions.min()), float(positions.max()))
    sites_per_bin = max(int(round((high - low) / n_bins / lattice)), 1)
    width = sites_per_bin * lattice

    # Any occupied site anchors the grid, so the parity of the walk (sites on the evens after
    # an even number of steps, on the odds after an odd number) never has to be worked out.
    #
    # The offset is half a LATTICE SPACING, not half a bin. Half a bin only centres the sites
    # when a bin holds one of them; with an even number per bin it puts every other site
    # exactly on an edge, and which side of that edge a site falls on is then decided by the
    # last bits of the float — so bins pick up 1, 2 or 3 sites at random and the histogram
    # alternates by ±50% for no physical reason at all. Half a spacing keeps every edge midway
    # between two sites whatever the bin holds.
    anchor = float(positions.min()) - 0.5 * lattice
    anchor -= float(np.ceil((anchor - low) / width)) * width
    return anchor + width * np.arange(int(np.ceil((high - anchor) / width)) + 1)


def gaussian_limit(x: np.ndarray, t: int, step: StepDist | str = "pm1") -> np.ndarray:
    """The CLT overlay: the N(mu_1 t, sigma_1^2 t) density evaluated on `x`.

    A prediction, not a fit. Both parameters come from the step distribution's exact moments
    and the elapsed time; nothing is read off the sample it will be drawn on top of.
    """
    if t < 1:
        raise ValueError("t must be at least one step")
    dist = _as_step_dist(step)
    x = np.asarray(x, dtype=float)
    mean, sigma = dist.mean * t, dist.std * np.sqrt(t)
    return np.exp(-0.5 * ((x - mean) / sigma) ** 2) / (sigma * np.sqrt(2.0 * np.pi))


def clt_sum_distribution(n_terms: int, n_samples: int, rng: np.random.Generator,
                         step: StepDist | str = "pm1") -> np.ndarray:
    """`n_samples` standardized sums (S_n - n mu_1) / (sigma_1 sqrt(n)) of `n_terms` steps.

    Standardizing is what makes the collapse visible: it divides out the two things the step
    distribution controls — where the sum sits and how wide it is — leaving only the shape,
    which is the central limit theorem's actual claim.
    """
    if n_terms < 1 or n_samples < 1:
        raise ValueError("n_terms and n_samples must be positive")
    dist = _as_step_dist(step)
    sums = dist.draw((n_samples, n_terms), rng).sum(axis=1)
    return (sums - n_terms * dist.mean) / (dist.std * np.sqrt(n_terms))


def binomial_to_gaussian(n: int, p: float = 0.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The de Moivre-Laplace bridge: k, the exact binomial pmf, and its Gaussian.

    The exact pmf is computed through log-gamma (`multiplicity.log_multiplicity_array`)
    rather than factorials, so it stays finite at n = 10^4, where C(n, k) itself overflows
    every float this machine has.
    """
    if n < 1:
        raise ValueError("n must be positive")
    if not 0.0 < p < 1.0:
        raise ValueError("p must lie strictly between 0 and 1")

    k = np.arange(n + 1, dtype=float)
    log_pmf = log_multiplicity_array(n, k) + k * np.log(p) + (n - k) * np.log1p(-p)
    mean, sigma = n * p, np.sqrt(n * p * (1.0 - p))
    gaussian = np.exp(-0.5 * ((k - mean) / sigma) ** 2) / (sigma * np.sqrt(2.0 * np.pi))
    return k, np.exp(log_pmf), gaussian


def correlated_walk(n_walkers: int, n_steps: int, persistence: float,
                    rng: np.random.Generator) -> np.ndarray:
    """A +/-1 walk that repeats its previous step with probability `persistence`.

    The one place in the course where a load-bearing assumption is broken on purpose. The
    steps are still identically distributed and still have finite variance; only independence
    is gone, and that alone is enough to break the naive CLT prediction — the standardized
    histogram at q = 0.95 is visibly too wide, and stays too wide as n grows.

    `persistence = 0` reproduces `random_walk(..., step="pm1")` exactly in distribution.
    Successive steps have correlation exactly q, so the long-time variance is inflated by
    (1 + q) / (1 - q): the walk is not un-Gaussian forever, it is Gaussian with a width the
    independent-step formula gets wrong. The advanced section of module 03 works this out.
    """
    if n_walkers < 1 or n_steps < 1:
        raise ValueError("n_walkers and n_steps must be positive")
    if not 0.0 <= persistence < 1.0:
        raise ValueError("persistence must lie in [0, 1)")

    fresh = rng.integers(0, 2, size=(n_walkers, n_steps)) * 2.0 - 1.0
    repeat = rng.random((n_walkers, n_steps)) < persistence

    steps = np.empty((n_walkers, n_steps))
    steps[:, 0] = fresh[:, 0]
    # One pass along the time axis, vectorised across all walkers at once. This loop is the
    # one that cannot be removed: a step is only decided once its predecessor is known.
    for t in range(1, n_steps):
        steps[:, t] = np.where(repeat[:, t], steps[:, t - 1], fresh[:, t])

    positions = np.zeros((n_walkers, n_steps + 1))
    positions[:, 1:] = np.cumsum(steps, axis=1)
    return positions


def _as_step_dist(step: StepDist | str) -> StepDist:
    return step if isinstance(step, StepDist) else step_distribution(step)


def _validate_faces(n_faces: int) -> None:
    if n_faces < 1:
        raise ValueError("a die needs at least one face")
