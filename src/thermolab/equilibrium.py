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
    Ensemble:      microcanonical for the joint system -- every accessible joint microstate
                   is equally probable, exactly as in module 8; each body's own temperature
                   is read off its own quanta by equipartition, T = (quanta x quantum)/(n k_B)
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
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import K_B


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
