"""Two bodies exchanging energy quanta until they share one temperature.

MODEL SPECIFICATION
    System:        two Einstein solids in thermal contact, body A with n_a independent
                   oscillators and body B with n_b, exchanging identical energy quanta
    Dynamics:      one randomly chosen quantum hops per step: it leaves its current body
                   with probability proportional to that body's share of the quanta, then
                   lands on a uniformly random oscillator among both bodies -- the two-body,
                   energy-tracking generalisation of the Ehrenfest urn in
                   `multiplicity.sample_two_box`
    Boundary:      closed and isolated as a pair; the total number of quanta -- hence the
                   total energy -- is exactly conserved
    Ensemble:      microcanonical for the joint system, with the quanta counted as if they
                   were labelled particles: every assignment of the labelled quanta to the
                   oscillators of both bodies is equally probable, which is the hop rule's
                   own stationary law. A real Einstein solid's quanta are unlabelled and its
                   count is different -- see THE ENTROPY LEDGER below. Each body's own
                   temperature is read off its own quanta by equipartition,
                   T = (quanta x quantum)/(n k_B)
    Ignored:       the physical attempt rate of an exchange (time is measured in steps, not
                   seconds), any spatial structure inside a body, and any coupling besides
                   the quantum exchange itself
    Valid when:    both bodies are warm enough that their oscillators sit in the classical,
                   high-temperature equipartition regime, and the two bodies exchange quanta
                   of the same size
    Failure modes: low temperature (quantum statistics take over and equipartition fails),
                   unequal quantum sizes between the bodies, or so few oscillators that
                   "temperature" is not yet a meaningful macroscopic quantity

This is the discrete, stochastic cousin of Newton's law of cooling. The exchange rule above
looks arbitrary until its consequence is traced through: a quantum's chance of leaving A is
exactly q_a / (q_a + q_b), and its chance of then landing back in A is exactly
n_a / (n_a + n_b), so the expected change in q_a each step is EXACTLY linear in q_a (see
`predicted_relaxation`) -- not approximately, and for every state, not just near equilibrium,
because the total quanta Q = q_a + q_b never changes. That linear recursion has a geometric
solution, and converting quanta to temperatures leaves the shape unchanged, because
T_A - T_B is itself linear in q_a at fixed Q. The result is the macroscopic exponential
relaxation this module derives on the page, T_A(t) - T_B(t) = (T_A(0) - T_B(0)) exp(-t/tau),
with the pair settling at T_eq = (C_A T_A + C_B T_B) / (C_A + C_B). Module 8 stops at "the
even split dominates"; this module adds the dynamics that gets there and clocks how fast.

THE ENTROPY LEDGER (module 09)
    `entropy_produced` follows the pair's total entropy along a run, counting each body's
    microstates exactly: n oscillators holding q unlabelled quanta have C(q + n - 1, q) of them
    (stars and bars). Two things about that count and this dynamics are worth knowing before
    reading a ledger.

    The hop rule above moves one *labelled* quantum at a time, so its own stationary
    distribution of q_a is the binomial one of Q labelled quanta spread over n_a + n_b
    oscillators -- not the Einstein count. (Two oscillators a side sharing four quanta make
    the difference plain: the rule visits q_a = 0..4 in the ratio 1 : 4 : 6 : 4 : 1, where the
    Einstein count would give 5 : 8 : 9 : 8 : 5; a test pins this.) The two peak at almost the
    same partition: the binomial at q_a/n_a = q_b/n_b, the exact Einstein count at
    q_a/(n_a - 1) = q_b/(n_b - 1), a relative shift of order 1/n that vanishes for macroscopic
    bodies. They differ more in the spread about the peak, the labelled model's being narrower
    by a factor sqrt(1 + Q/(n_a + n_b)). So the ledger's rise and plateau are faithful; its
    jitter on the plateau is quieter than a real Einstein solid's would be.

    And the ledger ticks *down* on a large fraction of single steps -- every time a quantum
    happens to hop the "wrong" way. That is not a bug. It is module 08's point that the second
    law is a statement about overwhelming probability, not a rule obeyed step by step.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .constants import K_B

# ln Γ(x), elementwise, from the standard library -- see `multiplicity` for why not scipy.
_log_gamma_elementwise = np.frompyfunc(math.lgamma, 1, 1)


def _log_gamma(values) -> np.ndarray:
    return np.asarray(_log_gamma_elementwise(np.asarray(values, dtype=float)), dtype=float)


@dataclass(frozen=True)
class TwoBodyState:
    """Two Einstein solids in thermal contact, tracked by integer quantum counts.

    `n_a` and `n_b` are each body's oscillator count -- its "size", and in this model's
    classical high-temperature limit the source of its heat capacity, C = n k_B. `q_a` and
    `q_b` are the (integer) number of energy quanta of size `quantum` [J] each body currently
    holds; both bodies share the same quantum size because they are in direct contact.
    """

    n_a: int
    n_b: int
    q_a: int
    q_b: int
    quantum: float

    def __post_init__(self) -> None:
        if self.n_a < 1 or self.n_b < 1:
            raise ValueError("n_a and n_b must be positive")
        if self.q_a < 0 or self.q_b < 0:
            raise ValueError("q_a and q_b must be non-negative")
        if self.quantum <= 0:
            raise ValueError("quantum must be positive")

    @property
    def heat_capacity_a(self) -> float:
        """C_A = n_a k_B -- this model's classical (high-T, equipartition) heat capacity."""
        return self.n_a * K_B

    @property
    def heat_capacity_b(self) -> float:
        return self.n_b * K_B

    @property
    def energy_a(self) -> float:
        return self.q_a * self.quantum

    @property
    def energy_b(self) -> float:
        return self.q_b * self.quantum

    @property
    def temperature_a(self) -> float:
        """T_A = E_A / C_A, i.e. (q_a quantum) / (n_a k_B) -- equipartition per oscillator."""
        return self.energy_a / self.heat_capacity_a

    @property
    def temperature_b(self) -> float:
        return self.energy_b / self.heat_capacity_b

    @property
    def total_quanta(self) -> int:
        """Q = q_a + q_b, exactly conserved by `simulate_energy_exchange`."""
        return self.q_a + self.q_b

    @property
    def total_oscillators(self) -> int:
        return self.n_a + self.n_b


def from_temperatures(n_a: int, n_b: int, temperature_a: float, temperature_b: float,
                      quantum: float) -> TwoBodyState:
    """Build a state whose bodies start at the given temperatures, T = q quantum / (n k_B).

    Quanta are integers, so each q is rounded to the nearest one; the realised temperature
    therefore differs from the requested one by O(quantum / (n k_B)) -- negligible once n is
    large enough to deserve the word "macroscopic", the same caveat every module in this
    course attaches to a discrete model of a continuous quantity.
    """
    if temperature_a <= 0 or temperature_b <= 0:
        raise ValueError("temperature_a and temperature_b must be positive")
    if quantum <= 0:
        raise ValueError("quantum must be positive")
    q_a = int(round(n_a * K_B * temperature_a / quantum))
    q_b = int(round(n_b * K_B * temperature_b / quantum))
    return TwoBodyState(n_a=n_a, n_b=n_b, q_a=q_a, q_b=q_b, quantum=quantum)


def equilibrium_temperature(c_a: float, t_a: float, c_b: float, t_b: float) -> float:
    """T_eq = (C_A T_A + C_B T_B) / (C_A + C_B) -- from energy conservation alone.

    This is the macroscopic statement, independent of any microscopic model: whatever the
    exchange mechanism, a closed pair's total energy C_A T_A + C_B T_B is what the fixed total
    heat capacity C_A + C_B eventually shares out as a single common temperature.
    """
    if c_a <= 0 or c_b <= 0:
        raise ValueError("heat capacities must be positive")
    return (c_a * t_a + c_b * t_b) / (c_a + c_b)


@dataclass(frozen=True)
class ExchangeResult:
    """Per-step record of a quantum-exchange run: how many quanta body A held after each step."""

    steps: np.ndarray  # (n_steps,) step index, 1..n_steps
    q_a: np.ndarray  # (n_steps,) quanta in body A after each step
    initial: TwoBodyState

    @property
    def q_b(self) -> np.ndarray:
        return self.initial.total_quanta - self.q_a

    @property
    def temperature_a(self) -> np.ndarray:
        return self.q_a * self.initial.quantum / self.initial.heat_capacity_a

    @property
    def temperature_b(self) -> np.ndarray:
        return self.q_b * self.initial.quantum / self.initial.heat_capacity_b

    @property
    def final_state(self) -> TwoBodyState:
        return TwoBodyState(
            n_a=self.initial.n_a, n_b=self.initial.n_b,
            q_a=int(self.q_a[-1]), q_b=int(self.q_b[-1]), quantum=self.initial.quantum,
        )


def simulate_energy_exchange(state: TwoBodyState, n_steps: int,
                             rng: np.random.Generator) -> ExchangeResult:
    """Advance the pair by `n_steps` random single-quantum exchanges.

    Each step draws which quantum moves (so a body holding more quanta is proportionally more
    likely to be the source) and which oscillator receives it (uniformly over both bodies).
    Three outcomes follow: the quantum returns to the body it left (q_a unchanged), it crosses
    from A to B (q_a -= 1), or from B to A (q_a += 1). Total quanta -- hence total energy -- is
    untouched by construction, since every step only relabels one quantum's owner.
    """
    if n_steps < 1:
        raise ValueError("n_steps must be positive")
    total_quanta = state.total_quanta
    if total_quanta < 1:
        raise ValueError("the pair needs at least one energy quantum to exchange")
    total_oscillators = state.total_oscillators
    fraction_in_a = state.n_a / total_oscillators

    source_draw = rng.random(n_steps)
    dest_draw = rng.random(n_steps)

    q_a = np.empty(n_steps, dtype=np.int64)
    current = state.q_a
    for step in range(n_steps):
        leaves_a = source_draw[step] < (current / total_quanta)
        lands_in_a = dest_draw[step] < fraction_in_a
        if leaves_a and not lands_in_a:
            current -= 1
        elif not leaves_a and lands_in_a:
            current += 1
        q_a[step] = current

    return ExchangeResult(steps=np.arange(1, n_steps + 1), q_a=q_a, initial=state)


def predicted_relaxation(state: TwoBodyState, steps: np.ndarray) -> np.ndarray:
    """Closed-form E[T_A(n) - T_B(n)] = (T_A(0) - T_B(0)) (1 - 1/Q)^n.

    Exact, not approximate: the exchange rule in `simulate_energy_exchange` makes the expected
    change in q_a per step exactly linear in q_a (E[dq_a] = n_a/(n_a+n_b) - q_a/Q), for every
    state, because Q = q_a + q_b never changes. That linear recursion has the geometric
    solution above; see the module docstring and the page's Advanced section for the full
    derivation. `relaxation_time` gives the equivalent continuous-time time constant.
    """
    q = state.total_quanta
    delta_t0 = state.temperature_a - state.temperature_b
    return delta_t0 * (1.0 - 1.0 / q) ** np.asarray(steps, dtype=float)


def relaxation_time(state: TwoBodyState) -> float:
    """tau [steps], defined so that (1 - 1/Q)^n == exp(-n / tau) exactly.

    tau = -1 / ln(1 - 1/Q), which -> Q for Q >> 1 -- the discrete-step analogue of the
    Newton's-law-of-cooling time constant tau = C_A C_B / (kappa (C_A + C_B)), with this
    model's implicit per-step conductance kappa = k_B / Q.
    """
    q = state.total_quanta
    if q < 2:
        raise ValueError("relaxation_time needs at least two quanta to exchange")
    return float(-1.0 / np.log(1.0 - 1.0 / q))


# ---------------------------------------------------------------------------
# The entropy ledger (module 09)
# ---------------------------------------------------------------------------


def einstein_log_multiplicity(quanta, oscillators: int) -> np.ndarray:
    """Exact ln Omega = ln C(q + n - 1, q) for n oscillators sharing q quanta, elementwise.

    Stars and bars: arrange q identical quanta and n - 1 dividers in a row. Exact at every
    size, through log-gamma, so a ledger built from it carries no Stirling error at all -- the
    smooth `fundamental.einstein_solid_entropy` is then an approximation that can be measured
    against it, the way module 08 measured Stirling itself.
    """
    if oscillators < 1:
        raise ValueError("a solid needs at least one oscillator")
    q = np.asarray(quanta, dtype=float)
    if np.any(q < 0):
        raise ValueError("quanta must be non-negative")
    return _log_gamma(q + oscillators) - _log_gamma(q + 1.0) - math.lgamma(oscillators)


def total_entropy(state: TwoBodyState) -> float:
    """S_A + S_B = k_B (ln Omega_A + ln Omega_B) of the pair's current macrostate [J/K]."""
    return float(K_B * (einstein_log_multiplicity(state.q_a, state.n_a)
                        + einstein_log_multiplicity(state.q_b, state.n_b)))


def entropy_produced(result: ExchangeResult) -> np.ndarray:
    """Cumulative Delta S_total(t) along a run, one entry per step [J/K].

        Delta S_total(t) = k_B [ln Omega_A(q_a(t)) + ln Omega_B(q_b(t))] - S_total(0)

    The pair is isolated, so nothing crosses its outer boundary: every change in its total
    entropy is entropy produced, none of it received. Evaluated in one vectorised pass, and
    `result` is only read -- its arrays are not modified.

    Expect it to rise and flatten as the temperatures meet, and expect it to dip on single
    steps; see the module docstring. That it rises *overall* is an observation about this run,
    never a proof: the proof is the counting argument on the module-09 page.
    """
    initial = result.initial
    ln_omega = (einstein_log_multiplicity(result.q_a, initial.n_a)
                + einstein_log_multiplicity(result.q_b, initial.n_b))
    start = (einstein_log_multiplicity(initial.q_a, initial.n_a)
             + einstein_log_multiplicity(initial.q_b, initial.n_b))
    return K_B * (ln_omega - start)
