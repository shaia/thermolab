"""Heat engines, refrigerators, and the bound the second law puts on both.

WHERE THE WORK CONVENTION FLIPS -- AND THE ONLY PLACE IT DOES
    The project convention is dU = δQ + δW_on: work done ON the gas is positive, so a gas
    that expands does negative work. Engines are rated by the work they *deliver*, and an
    efficiency with a negative numerator would be unreadable. This module is the one place
    in the course that converts, and it does so only by negating once, in
    `CycleResult.work_output` -- and, for the sampled loop area, through the helper
    `paths.work_by_system`, which exists for exactly this and is the only other negation in
    the library. Every other number here, including every `ProcessResult` in `strokes` and
    every heat, carries the project sign. Read an efficiency off `work_output`; read physics
    off the strokes.

WHAT THIS ADDS TO `processes`
    `processes` runs one stroke. An engine is a closed sequence of strokes, and the closure
    is the whole point: it forces the net internal-energy change to vanish, so the net work
    delivered equals the net heat absorbed, and it is what makes dumping heat unavoidable
    rather than merely wasteful. `CycleResult` joins `ProcessResult`s end to end, refuses a
    loop that does not actually close, and pairs each stroke with the reservoir it touched
    -- which is what makes the Clausius sum computable rather than guessed.

MODEL SPECIFICATION
    System:        a fixed amount of ideal gas (N particles, f quadratic degrees of freedom)
                   taken around a closed loop between heat reservoirs at fixed temperatures
    Dynamics:      quasistatic strokes from `processes` -- isothermal, adiabatic or
                   isochoric -- joined into a closed curve in the P-V plane; the reservoir a
                   stroke exchanges heat with is recorded separately from the gas's own
                   temperature, which is what lets the two differ
    Boundary:      a frictionless piston, and a wall switched between diathermal (touching
                   one named reservoir) and adiabatic
    Ensemble:      not applicable -- this is thermodynamics; nothing here counts microstates
    Ignored:       friction, the piston's mass, gas non-ideality, heat leaking through the
                   adiabatic strokes, the time a stroke takes, and the work spent moving the
                   working substance between reservoirs
    Valid when:    every stroke is slow compared with the gas's relaxation time, and each
                   reservoir is large enough that absorbing its heat leaves its temperature
                   unchanged
    Failure modes: finite-rate operation, where heat will not cross a vanishing temperature
                   difference and the efficiency falls toward the endoreversible value
                   (`curzon_ahlborn_efficiency`); regenerators, which store heat inside the
                   engine between strokes -- a Stirling engine with a perfect one reaches the
                   Carnot bound on constant-volume strokes, and no `Stroke` here can represent
                   the store; and any working substance near condensation, where the
                   ideal-gas strokes are simply wrong
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import paths, processes
from .constants import K_B

# Closure tolerance: a cycle is built by composing closed forms, so the loop should return to
# its starting state to within rounding of those forms, not to within anything physical. This
# is a fractional bound -- an absolute one would be meaningless at the 1e-18 J energies here.
CLOSURE_TOLERANCE = 1e-9


# ---------------------------------------------------------------------------
# Closed forms: the bounds, before any cycle is built
# ---------------------------------------------------------------------------


def _check_reservoirs(t_hot: float, t_cold: float) -> None:
    if t_cold <= 0.0:
        raise ValueError("a reservoir temperature must be positive (absolute scale)")
    if t_hot <= t_cold:
        raise ValueError(f"need t_hot > t_cold, got t_hot={t_hot}, t_cold={t_cold}")


def carnot_efficiency(t_hot: float, t_cold: float) -> float:
    """eta = 1 - T_c/T_h: the most work any engine can deliver per unit of heat absorbed.

    This is a *theorem*, not a property of a device. It follows from Carnot's theorem, which
    follows from the Kelvin statement alone -- no mention of the working substance, and no
    appeal to how well the engine is built. The bound is reached only by a reversible engine,
    which is also the one that delivers zero power, since a reversible stroke takes forever.
    """
    _check_reservoirs(t_hot, t_cold)
    return 1.0 - t_cold / t_hot


def cop_refrigerator(t_hot: float, t_cold: float) -> float:
    """Best possible heat-removed-per-work-in, T_c/(T_h - T_c).

    Note it exceeds 1 for any modest temperature span, which is why a "coefficient of
    performance" is not called an efficiency: nothing is being converted, energy is being
    moved, and moving it uphill costs less than the amount moved.
    """
    _check_reservoirs(t_hot, t_cold)
    return t_cold / (t_hot - t_cold)


def cop_heat_pump(t_hot: float, t_cold: float) -> float:
    """Best possible heat-delivered-per-work-in, T_h/(T_h - T_c) = cop_refrigerator + 1.

    The identity is exact, and it is just energy conservation: everything the refrigerator
    removes from the cold side, plus the work, arrives on the hot side.
    """
    _check_reservoirs(t_hot, t_cold)
    return t_hot / (t_hot - t_cold)


def curzon_ahlborn_efficiency(t_hot: float, t_cold: float) -> float:
    """eta = 1 - sqrt(T_c/T_h): the efficiency of an engine run at maximum *power*.

    Carnot's bound is reached only at zero power. Allow the engine finite time, require heat
    to cross a finite temperature difference in order to flow at a finite rate, and optimise
    for power rather than for efficiency, and this is what falls out. It is not a bound -- it
    is what optimising a different objective gives -- but it lands remarkably close to real
    plants, which is why it is worth meeting beside the Carnot number rather than long after.
    """
    _check_reservoirs(t_hot, t_cold)
    return 1.0 - float(np.sqrt(t_cold / t_hot))


def otto_efficiency(compression_ratio: float, gamma: float) -> float:
    """eta = 1 - r^(1 - gamma) for the idealised petrol engine.

    Depends on the compression ratio and the gas alone -- not on how much heat the fuel
    releases. Burning more fuel per cycle buys more work and more waste in the same
    proportion.
    """
    if compression_ratio <= 1.0:
        raise ValueError("compression ratio must exceed 1")
    if gamma <= 1.0:
        raise ValueError("gamma must exceed 1")
    return 1.0 - compression_ratio ** (1.0 - gamma)


def entropy_change_of_gas(process: processes.ProcessResult) -> float:
    """ΔS of the ideal gas across one stroke: N k_B ln(V2/V1) + C_V ln(T2/T1).

    A state function, so this is valid for any stroke whose endpoints are equilibrium states
    -- irreversible ones included, where no integral of δQ/T along the way would have meant
    anything. That separation is the point: the gas's entropy change is fixed by its
    endpoints, while what crossed the boundary is not.
    """
    start, end = process.start, process.end
    capacity = processes.heat_capacity_constant_volume(
        start.n_particles, start.degrees_of_freedom
    )
    return float(
        start.n_particles * K_B * np.log(end.volume / start.volume)
        + capacity * np.log(end.temperature / start.temperature)
    )


# ---------------------------------------------------------------------------
# A cycle: strokes, and the reservoir each one touched
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Stroke:
    """One process, plus the reservoir it exchanged heat with.

    `reservoir_temperature` is deliberately not read off the gas: an engine that transfers
    heat at a finite rate has a gas *colder* than the hot reservoir it draws from, and the
    gap between the two is exactly where the lost work goes.

    None means "no single reservoir temperature applies", which covers two different cases
    on purpose. An adiabatic stroke moves no heat at all. An isochoric heating stroke moves
    heat while the gas's own temperature climbs the whole way, so no one temperature
    characterises the transfer -- and naming its endpoint would be a quiet lie that
    `clausius_sum` would then dutifully turn into a wrong number. It refuses instead.
    """

    process: processes.ProcessResult
    reservoir_temperature: float | None = None

    def __post_init__(self) -> None:
        if self.reservoir_temperature is not None and self.reservoir_temperature <= 0.0:
            raise ValueError("a reservoir temperature must be positive (absolute scale)")


@dataclass(frozen=True)
class CycleResult:
    """A closed loop of strokes: an engine if it delivers work, a refrigerator if it eats it.

    The constructor refuses a loop that does not close. That is not fussiness -- an unclosed
    "cycle" silently has ΔU ≠ 0, so its net work is not its net heat, and every efficiency
    computed from it is then wrong by an amount nobody would notice.
    """

    label: str
    strokes: tuple[Stroke, ...]
    t_hot: float
    t_cold: float

    def __post_init__(self) -> None:
        if len(self.strokes) < 2:
            raise ValueError("a cycle needs at least two strokes")
        _check_reservoirs(self.t_hot, self.t_cold)
        start = self.strokes[0].process.start
        end = self.strokes[-1].process.end
        scale = abs(start.internal_energy)
        if abs(end.internal_energy - start.internal_energy) > CLOSURE_TOLERANCE * scale:
            raise ValueError(
                f"{self.label!r} does not close: it ends at T={end.temperature:.6g} K, "
                f"V={end.volume:.6g} m^3, having started at T={start.temperature:.6g} K, "
                f"V={start.volume:.6g} m^3"
            )

    @property
    def net_work_on_gas(self) -> float:
        """Sum of δW_on around the loop, in the project convention. Negative for an engine."""
        return float(sum(stroke.process.work_on_gas for stroke in self.strokes))

    @property
    def work_output(self) -> float:
        """The work the machine DELIVERS: -net_work_on_gas.

        *** This single line is the course's one conversion to the work-done-by convention. ***
        Positive for an engine, negative for a refrigerator, which is driven rather than
        driving.
        """
        return -self.net_work_on_gas

    @property
    def heat_absorbed(self) -> float:
        """Total heat taken IN from the reservoirs, counting only the strokes that gained."""
        return float(sum(s.process.heat for s in self.strokes if s.process.heat > 0.0))

    @property
    def heat_rejected(self) -> float:
        """Total heat dumped, as a positive magnitude."""
        return float(-sum(s.process.heat for s in self.strokes if s.process.heat < 0.0))

    @property
    def efficiency(self) -> float:
        """Work delivered per unit heat absorbed. Meaningful only when the loop is an engine."""
        if self.work_output <= 0.0:
            raise ValueError(
                f"{self.label!r} consumes work rather than delivering it — it is a "
                f"refrigerator or a heat pump; ask for a coefficient of performance instead"
            )
        return self.work_output / self.heat_absorbed

    @property
    def coefficient_of_performance(self) -> float:
        """Heat lifted from the cold side per unit work put in. For a driven cycle only."""
        if self.work_output >= 0.0:
            raise ValueError(
                f"{self.label!r} delivers work rather than consuming it — it is an engine; "
                f"ask for an efficiency instead"
            )
        return self.heat_absorbed / (-self.work_output)

    @property
    def clausius_sum(self) -> float:
        """The loop integral of δQ / T_reservoir. Zero if reversible, negative otherwise.

        Note which temperature divides: the *reservoir's*, not the gas's. Dividing by the
        gas's own temperature would give the gas's entropy change, which is zero around any
        closed loop whatever, reversible or not -- a tautology that proves nothing. The
        inequality lives entirely in the difference between the two temperatures.
        """
        total = 0.0
        for stroke in self.strokes:
            if stroke.process.heat == 0.0:
                continue
            if stroke.reservoir_temperature is None:
                raise ValueError(
                    f"stroke {stroke.process.label!r} names no reservoir, so the loop "
                    f"integral of δQ/T is not defined for {self.label!r}"
                )
            total += stroke.process.heat / stroke.reservoir_temperature
        return total

    @property
    def entropy_produced(self) -> float:
        """ΔS of the universe over one cycle, equal to minus the Clausius sum.

        The gas returns to its starting state and contributes nothing; every joule that left
        a reservoir lowered that reservoir's entropy by Q/T. What survives is the production,
        and the second law is the statement that it cannot be negative.

        For a reversible cycle the exact answer is zero, so what comes back is rounding noise
        of either sign, around 1e-19 of `entropy_scale`. Compare against that scale rather
        than against zero -- an absolute tolerance would either pass everything or be
        arbitrary, and testing `>= 0.0` on this is a flaky test waiting to happen.
        """
        return -self.clausius_sum

    @property
    def entropy_scale(self) -> float:
        """The size of a single term in the Clausius sum, for judging `entropy_produced`.

        Q_absorbed / T_hot: the entropy the hot reservoir gives up per cycle. Production is
        meaningful only relative to this, and it is what any tolerance here should multiply.
        """
        return self.heat_absorbed / self.t_hot

    @property
    def carnot_bound(self) -> float:
        """The efficiency this cycle's reservoirs permit."""
        return carnot_efficiency(self.t_hot, self.t_cold)

    @property
    def enclosed_area(self) -> float:
        """The area the loop encloses in the P-V plane, integrated from the sampled strokes.

        "The work is the area enclosed" is the picture every engine diagram is drawn to make,
        and this is that sentence evaluated. It should equal `work_output` -- but it arrives
        by a different route, trapezoid quadrature over the stored path rather than each
        stroke's closed form, so the two agreeing is a genuine check rather than an identity.
        It is also the only quantity here that `n_points` moves: refine the strokes and this
        converges on `work_output` at second order, while `work_output` itself never budges.

        Raises for a cycle containing an irreversible stroke, which encloses no area at all.
        """
        total = 0.0
        for stroke in self.strokes:
            path = stroke.process.quasistatic_path
            total += paths.work_by_system(path.volumes, path.pressures)
        return total

    @property
    def internal_energy_drift(self) -> float:
        """ΔU around the loop, which must vanish. Worth having as a number, not an assertion.

        Each stroke's endpoints come from its own closed form, so a non-zero drift is a real
        disagreement between four independently derived states rather than a tautology.
        """
        return (
            self.strokes[-1].process.end.internal_energy
            - self.strokes[0].process.start.internal_energy
        )

    @property
    def first_law_residual(self) -> float:
        """Q_net + W_on,net - ΔU around the loop. Zero if the bookkeeping is sound."""
        heat = float(sum(stroke.process.heat for stroke in self.strokes))
        return heat + self.net_work_on_gas - self.internal_energy_drift


# ---------------------------------------------------------------------------
# The cycles themselves
# ---------------------------------------------------------------------------


def carnot_cycle(n_particles: int, t_hot: float, t_cold: float, v_start: float,
                 expansion_ratio: float, degrees_of_freedom: int = 3,
                 n_points: int = 257) -> CycleResult:
    """The reversible two-reservoir engine: isotherm, adiabat, isotherm, adiabat.

    The two adiabats are not free. Both span the same temperature ratio, so both stretch the
    volume by the same factor (T V^(gamma-1) is constant), and that is what forces the two
    isotherms to span the *same* volume ratio. The logarithms then cancel in Q_c/Q_h, leaving
    T_c/T_h -- which is why the efficiency forgets everything about the gas and the size of
    the engine, and remembers only the two temperatures.
    """
    _check_reservoirs(t_hot, t_cold)
    if expansion_ratio <= 1.0:
        raise ValueError("the hot isotherm must expand: expansion_ratio > 1")
    gamma = processes.gamma_from_dof(degrees_of_freedom)

    state_1 = processes.EquilibriumState.from_temperature(
        n_particles, t_hot, v_start, degrees_of_freedom
    )
    v_2 = v_start * expansion_ratio
    # Both adiabats stretch the volume by this factor, from T V^(gamma-1) = constant.
    stretch = (t_hot / t_cold) ** (1.0 / (gamma - 1.0))

    hot_isotherm = processes.isothermal(state_1, v_2, n_points=n_points)
    expansion = processes.adiabatic(hot_isotherm.end, v_2 * stretch, n_points=n_points)
    cold_isotherm = processes.isothermal(expansion.end, v_start * stretch, n_points=n_points)
    compression = processes.adiabatic(cold_isotherm.end, v_start, n_points=n_points)

    return CycleResult(
        label="Carnot",
        strokes=(
            Stroke(hot_isotherm, t_hot),
            Stroke(expansion),
            Stroke(cold_isotherm, t_cold),
            Stroke(compression),
        ),
        t_hot=t_hot,
        t_cold=t_cold,
    )


def endoreversible_cycle(n_particles: int, t_hot: float, t_cold: float, v_start: float,
                         expansion_ratio: float, hot_gap: float, cold_gap: float,
                         degrees_of_freedom: int = 3, n_points: int = 257) -> CycleResult:
    """A Carnot cycle whose gas never quite reaches its reservoirs' temperatures.

    Heat will not cross a zero temperature difference at a finite rate, so a real engine
    draws from a reservoir at `t_hot` with its gas at `t_hot - hot_gap`, and dumps into one
    at `t_cold` with its gas at `t_cold + cold_gap`. Every stroke the gas performs is still
    reversible -- hence "endo", inside -- and all the irreversibility sits in the two heat
    transfers across the gaps.

    Two things follow, and together they are the module's argument in miniature. The
    efficiency is set by the *gas's* temperatures, so it falls short of the reservoirs'
    Carnot bound. And the loop integral of δQ/T over the *reservoirs* turns strictly
    negative, by exactly what the gaps cost -- the Clausius inequality arriving as a number
    rather than as a claim.
    """
    _check_reservoirs(t_hot, t_cold)
    if hot_gap < 0.0 or cold_gap < 0.0:
        raise ValueError("temperature gaps cannot be negative")
    working_hot = t_hot - hot_gap
    working_cold = t_cold + cold_gap
    if working_hot <= working_cold:
        raise ValueError(
            f"the gaps have closed the span: the gas would run between "
            f"{working_hot:.6g} K and {working_cold:.6g} K, which is no engine at all"
        )

    inner = carnot_cycle(
        n_particles, working_hot, working_cold, v_start, expansion_ratio,
        degrees_of_freedom, n_points,
    )
    # Same strokes; the reservoirs they touch are the *outer* ones. That relabelling is the
    # entire difference between this cycle and a Carnot cycle, and it is where the loss is.
    hot_isotherm, expansion, cold_isotherm, compression = inner.strokes
    return CycleResult(
        label="endoreversible",
        strokes=(
            Stroke(hot_isotherm.process, t_hot),
            Stroke(expansion.process),
            Stroke(cold_isotherm.process, t_cold),
            Stroke(compression.process),
        ),
        t_hot=t_hot,
        t_cold=t_cold,
    )


def otto_cycle(n_particles: int, t_intake: float, v_max: float, compression_ratio: float,
               heat_input: float, degrees_of_freedom: int = 5,
               n_points: int = 257) -> CycleResult:
    """The idealised petrol engine: adiabatic squeeze, ignite, adiabatic push, exhaust.

    Defaults to f = 5 because the working substance is air, a diatomic gas, and the
    compression ratio only buys what gamma lets it.

    The two heat strokes happen at constant volume while the gas's own temperature *changes*,
    so neither touches a reservoir at a single well-defined temperature. `clausius_sum` will
    therefore refuse to produce a number here, which is correct rather than unhelpful: Otto
    is not a two-reservoir engine, and the honest comparison with the Carnot bound is against
    the extreme temperatures the gas actually reaches, reported as `t_hot` and `t_cold`.
    """
    if compression_ratio <= 1.0:
        raise ValueError("compression ratio must exceed 1")
    if heat_input <= 0.0:
        raise ValueError("an engine needs heat put in: heat_input > 0")

    state_1 = processes.EquilibriumState.from_temperature(
        n_particles, t_intake, v_max, degrees_of_freedom
    )
    v_min = v_max / compression_ratio
    capacity = processes.heat_capacity_constant_volume(n_particles, degrees_of_freedom)

    compression = processes.adiabatic(state_1, v_min, n_points=n_points)
    ignited_temperature = compression.end.temperature + heat_input / capacity
    ignition = processes.isochoric(
        compression.end, n_particles * K_B * ignited_temperature / v_min, n_points=n_points
    )
    power = processes.adiabatic(ignition.end, v_max, n_points=n_points)
    exhaust = processes.isochoric(power.end, state_1.pressure, n_points=n_points)

    return CycleResult(
        label="Otto",
        strokes=(
            Stroke(compression),
            # No reservoir temperature on either heat stroke: the gas heats from T_2 to T_3
            # at constant volume, so the transfer has no single temperature to divide by.
            Stroke(ignition),
            Stroke(power),
            Stroke(exhaust),
        ),
        t_hot=ignition.end.temperature,
        t_cold=state_1.temperature,
    )


def reversed_carnot_cycle(n_particles: int, t_hot: float, t_cold: float, v_start: float,
                          expansion_ratio: float, degrees_of_freedom: int = 3,
                          n_points: int = 257) -> CycleResult:
    """The same four strokes run backwards: a refrigerator, driven by work.

    Every stroke of a reversible cycle can be reversed -- that is what the word means -- so
    the refrigerator is not a separate invention; it is the engine read right to left. Heat
    now leaves the cold reservoir and work is consumed, and the coefficient of performance
    comes out at T_c/(T_h - T_c), with the same logarithms cancelling as before.
    """
    forward = carnot_cycle(
        n_particles, t_hot, t_cold, v_start, expansion_ratio, degrees_of_freedom, n_points
    )
    reversed_strokes = tuple(
        Stroke(_reverse(stroke.process), stroke.reservoir_temperature)
        for stroke in reversed(forward.strokes)
    )
    return CycleResult(
        label="reversed Carnot",
        strokes=reversed_strokes,
        t_hot=t_hot,
        t_cold=t_cold,
    )


def _reverse(process: processes.ProcessResult) -> processes.ProcessResult:
    """Run one quasistatic stroke backwards: swap the endpoints, negate what crossed.

    Only a quasistatic stroke can be reversed. An irreversible one has no intermediate states
    to retrace, and running the piston the other way does not undo it -- which is the whole
    content of the word, and why this raises rather than quietly negating a number anyway.
    """
    if not process.quasistatic:
        raise ValueError(
            f"{process.label!r} is not quasistatic, so it cannot be run backwards: it has no "
            f"intermediate states to retrace"
        )
    path = process.quasistatic_path
    return processes.ProcessResult(
        label=f"{process.label} (reversed)",
        start=process.end,
        end=process.start,
        work_on_gas=-process.work_on_gas,
        heat=-process.heat,
        quasistatic=True,
        path=paths.Path(
            volumes=path.volumes[::-1].copy(),
            pressures=path.pressures[::-1].copy(),
            label=f"{path.label} (reversed)",
        ),
    )


def random_two_reservoir_engine(rng: np.random.Generator, t_hot: float, t_cold: float,
                                n_particles: int = 1000,
                                degrees_of_freedom: int = 3) -> CycleResult:
    """A randomly proportioned engine between two fixed reservoirs.

    Used to make the bound an experiment rather than an assertion: draw an engine of any
    size, any expansion ratio and any quality of thermal contact, and it still cannot beat
    1 - T_c/T_h. The gaps are drawn from zero upward, so a perfectly reversible engine is in
    the sample and the bound is approached but never crossed.
    """
    span = t_hot - t_cold
    return endoreversible_cycle(
        n_particles=n_particles,
        t_hot=t_hot,
        t_cold=t_cold,
        v_start=float(rng.uniform(0.5e-3, 2.0e-3)),
        expansion_ratio=float(rng.uniform(1.2, 4.0)),
        hot_gap=float(rng.uniform(0.0, 0.3 * span)),
        cold_gap=float(rng.uniform(0.0, 0.3 * span)),
        degrees_of_freedom=degrees_of_freedom,
    )
