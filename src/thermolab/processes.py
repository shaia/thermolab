"""Named thermodynamic processes: the four quasistatic families, and the irreversible ones.

SIGN CONVENTION (project-wide): dU = δQ + δW_on. Work done ON the gas is positive, so an
expansion carries negative work. Every function here returns work done on the system.

WHAT THIS ADDS TO `paths`
    `paths` answers "what is the work along this curve in the P-V plane?". It can only ask
    that of a quasistatic process, because only then does the gas have one pressure to
    integrate. This module names the four families that curve can belong to, supplies the
    heat capacities that fix their shapes, and then handles the case `paths` explicitly
    disclaims in its own failure modes: a process with no curve at all. The work is always

        δW_on = -P_ext dV,

    with the pressure that actually acts AT THE BOUNDARY. Quasistatic means P_ext = P, and
    only then is the area under the gas's own curve the work. A free expansion has P_ext = 0
    and therefore does no work whatever the gas's own pressure is doing.

MODEL SPECIFICATION
    System:        a fixed amount of ideal gas, N particles, with f quadratic degrees of
                   freedom each
    Dynamics:      two regimes -- quasistatic, where the gas holds a single (P, V, T)
                   throughout; and irreversible, where only the endpoints are equilibrium
                   states and the work follows the external pressure
    Boundary:      a frictionless piston in a wall that is either diathermal (heat may
                   cross) or adiabatic (it may not)
    Ensemble:      not applicable to the thermodynamics; the microscopic free expansion in
                   `free_expansion_microstate` is microcanonical, conserving energy exactly
    Ignored:       friction, the piston's own mass and inertia, gas non-ideality, heat
                   leaking through an adiabatic wall, and the time the gas takes to
                   re-equilibrate after each step
    Valid when:    quasistatic results -- the process is slow compared with the gas's
                   relaxation time; irreversible results -- the external pressure is known
                   and uniform at the moving boundary
    Failure modes: real gases, whose internal energy depends on volume, so their free
                   expansion DOES change the temperature; compressions fast enough that even
                   P_ext is not uniform; a wall that leaks, which makes "adiabatic" false
                   rather than approximate
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import kinetics, paths
from .constants import K_B

# ---------------------------------------------------------------------------
# Heat capacities: what fixes the shape of every curve below
# ---------------------------------------------------------------------------


def heat_capacity_constant_volume(n_particles: int, degrees_of_freedom: int = 3) -> float:
    """C_V = (f/2) N k_B, from U = (f/2) N k_B T and C_V = (dU/dT) at fixed V."""
    return 0.5 * degrees_of_freedom * n_particles * K_B


def heat_capacity_constant_pressure(n_particles: int, degrees_of_freedom: int = 3) -> float:
    """C_P = C_V + N k_B -- Mayer's relation.

    The extra N k_B is not a property of the gas but of the bookkeeping: heating at constant
    pressure also pays for the expansion work the gas does on its way, and for an ideal gas
    that work is exactly N k_B per kelvin.
    """
    return heat_capacity_constant_volume(n_particles, degrees_of_freedom) + n_particles * K_B


def gamma_from_dof(degrees_of_freedom: int = 3) -> float:
    """gamma = C_P/C_V = (f + 2)/f: 5/3 monatomic, 7/5 diatomic at room temperature."""
    if degrees_of_freedom < 1:
        raise ValueError("a particle needs at least one quadratic degree of freedom")
    return (degrees_of_freedom + 2.0) / degrees_of_freedom


def dof_from_gamma(gamma: float) -> float:
    """Invert `gamma_from_dof`: f = 2/(gamma - 1). Not required to be an integer."""
    if gamma <= 1.0:
        raise ValueError("gamma must exceed 1 for an ideal gas")
    return 2.0 / (gamma - 1.0)


# ---------------------------------------------------------------------------
# Equilibrium states
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EquilibriumState:
    """An ideal gas sitting still: the only kind of state a process may start or end in.

    A process may pass through states that are not of this kind -- that is precisely what
    makes it irreversible, and why `ProcessResult.path` is None for those.
    """

    n_particles: int
    pressure: float
    volume: float
    degrees_of_freedom: int = 3

    def __post_init__(self) -> None:
        if self.n_particles < 1 or self.pressure <= 0 or self.volume <= 0:
            raise ValueError("an equilibrium state needs N >= 1 and positive P and V")

    @classmethod
    def from_temperature(cls, n_particles: int, temperature: float, volume: float,
                         degrees_of_freedom: int = 3) -> EquilibriumState:
        return cls(
            n_particles=n_particles,
            pressure=n_particles * K_B * temperature / volume,
            volume=volume,
            degrees_of_freedom=degrees_of_freedom,
        )

    @property
    def temperature(self) -> float:
        """T = PV / (N k_B)."""
        return self.pressure * self.volume / (self.n_particles * K_B)

    @property
    def internal_energy(self) -> float:
        """U = (f/2) N k_B T = (f/2) PV -- a function of the state and nothing else."""
        return 0.5 * self.degrees_of_freedom * self.pressure * self.volume

    @property
    def gamma(self) -> float:
        return gamma_from_dof(self.degrees_of_freedom)


@dataclass(frozen=True)
class ProcessResult:
    """One process, start to finish: where it began, where it ended, and what crossed.

    `quasistatic` is the field that matters most. When it is False the gas had no single
    pressure while the process ran, `path` is None, and no area in the P-V plane is the work
    -- a distinction the rest of this module exists to keep visible.
    """

    label: str
    start: EquilibriumState
    end: EquilibriumState
    work_on_gas: float
    heat: float
    quasistatic: bool
    path: paths.Path | None = None

    @property
    def internal_energy_change(self) -> float:
        return self.end.internal_energy - self.start.internal_energy

    @property
    def temperature_change(self) -> float:
        return self.end.temperature - self.start.temperature

    @property
    def quasistatic_path(self) -> paths.Path:
        """The curve this process traces in the P-V plane.

        Raises for an irreversible process rather than returning None quietly. Reaching for
        the path of a process that has none is this module's central error committed in code,
        and a silent None would let a plot or an integral be built on nothing.
        """
        if self.path is None:
            raise ValueError(
                f"{self.label!r} is not quasistatic: it has no curve in the P-V plane, "
                f"because the gas has no single pressure while it runs"
            )
        return self.path

    def partial_work_on_gas(self, fraction: float) -> float:
        """Work accumulated along the first `fraction` of the path, for `fraction` in [0, 1].

        Meaningful only for a quasistatic process, and so routed through `quasistatic_path`:
        an irreversible process has no intermediate states to accumulate along, however
        well-defined its total work is.

        A fraction outside [0, 1] is an error rather than something to clamp. Past 1 a plain
        slice would silently return the whole path's work, and below 0 it would return the
        first sample interval's — both plausible-looking numbers for a caller that has got its
        arithmetic wrong, which is the worst way for this to fail.

        Zero returns exactly zero: no path traversed, no work. Any positive fraction too small
        to select two samples still integrates over the first interval, because that is the
        finest step a sampled path can resolve — sampling the path more densely is the way to
        ask a finer question.
        """
        if not 0.0 <= fraction <= 1.0:
            raise ValueError(f"fraction must lie in [0, 1], got {fraction}")
        if fraction == 0.0:
            return 0.0
        path = self.quasistatic_path
        cut = max(2, int(fraction * path.volumes.size))
        return paths.work_on_gas(path.volumes[:cut], path.pressures[:cut])

    @property
    def first_law_residual(self) -> float:
        """δQ + δW_on - ΔU, which must vanish.

        Worth having as a number rather than an assertion: for the isobaric, isothermal and
        adiabatic constructors below, the heat and the work are each evaluated from their own
        closed form and the endpoints from the equation of state, so a non-zero residual is a
        real disagreement between three independent formulae -- Mayer's relation among them
        -- and not a tautology.
        """
        return self.heat + self.work_on_gas - self.internal_energy_change


# ---------------------------------------------------------------------------
# The four quasistatic families
# ---------------------------------------------------------------------------


def isochoric(state: EquilibriumState, p_end: float, n_points: int = 2) -> ProcessResult:
    """Heat or cool at fixed volume: W_on = 0 exactly, so Q = ΔU = C_V ΔT."""
    end = EquilibriumState(state.n_particles, p_end, state.volume, state.degrees_of_freedom)
    capacity = heat_capacity_constant_volume(state.n_particles, state.degrees_of_freedom)
    return ProcessResult(
        label="isochoric",
        start=state,
        end=end,
        work_on_gas=0.0,
        heat=capacity * (end.temperature - state.temperature),
        quasistatic=True,
        path=paths.isochoric_path(state.volume, state.pressure, p_end, n_points=n_points),
    )


def isobaric(state: EquilibriumState, v_end: float, n_points: int = 2) -> ProcessResult:
    """Expand or compress at fixed pressure: W_on = -P ΔV and Q = C_P ΔT.

    The two are computed independently, so `first_law_residual` is a live check of Mayer's
    relation rather than a restatement of it.
    """
    end = EquilibriumState(state.n_particles, state.pressure, v_end, state.degrees_of_freedom)
    capacity = heat_capacity_constant_pressure(state.n_particles, state.degrees_of_freedom)
    return ProcessResult(
        label="isobaric",
        start=state,
        end=end,
        work_on_gas=paths.isobaric_work_on_gas(state.pressure, state.volume, v_end),
        heat=capacity * (end.temperature - state.temperature),
        quasistatic=True,
        path=paths.isobaric_path(state.pressure, state.volume, v_end, n_points=n_points),
    )


def isothermal(state: EquilibriumState, v_end: float, n_points: int = 257) -> ProcessResult:
    """Expand or compress in contact with a reservoir: ΔU = 0, so Q = -W_on = N k_B T ln(V2/V1)."""
    temperature = state.temperature
    end = EquilibriumState.from_temperature(
        state.n_particles, temperature, v_end, state.degrees_of_freedom
    )
    work = paths.isothermal_work_on_gas(state.n_particles, temperature, state.volume, v_end)
    return ProcessResult(
        label="isothermal",
        start=state,
        end=end,
        work_on_gas=work,
        heat=state.n_particles * K_B * temperature * float(np.log(v_end / state.volume)),
        quasistatic=True,
        path=paths.isothermal_path(
            state.n_particles, temperature, state.volume, v_end, n_points=n_points
        ),
    )


def adiabatic(state: EquilibriumState, v_end: float, n_points: int = 257) -> ProcessResult:
    """Expand or compress with the heat shut off, slowly: Q = 0 and P V^gamma stays constant.

    The gas pays for the work out of its own internal energy, so it cools as it expands. That
    is the whole difference from `isothermal`, and it is why the adiabat is the steeper curve.
    """
    gamma = state.gamma
    p_end = float(adiabatic_final_pressure(state.pressure, state.volume, v_end, gamma))
    end = EquilibriumState(state.n_particles, p_end, v_end, state.degrees_of_freedom)
    return ProcessResult(
        label="adiabatic",
        start=state,
        end=end,
        work_on_gas=paths.adiabatic_work_on_gas(
            state.pressure, state.volume, p_end, v_end, gamma
        ),
        heat=0.0,
        quasistatic=True,
        path=paths.adiabatic_path(
            state.pressure, state.volume, v_end, gamma, n_points=n_points
        ),
    )


def adiabatic_final_pressure(p_start: float, v_start: float, v_end, gamma: float) -> np.ndarray:
    """P_2 from P V^gamma = constant. Vectorized over `v_end` so a whole adiabat comes at once."""
    return np.asarray(p_start * (v_start / np.asarray(v_end, dtype=float)) ** gamma)


def adiabatic_final_temperature(t_start: float, v_start: float, v_end,
                                gamma: float) -> np.ndarray:
    """T_2 from T V^(gamma-1) = constant -- the same law with the equation of state folded in.

    Vectorized over `v_end` like its pressure counterpart: the temperature along an adiabat is
    what module 06's animation and its laboratory both plot, and neither should have to
    re-derive the exponent to get an array of it.
    """
    return np.asarray(
        t_start * (v_start / np.asarray(v_end, dtype=float)) ** (gamma - 1.0)
    )


# ---------------------------------------------------------------------------
# Polytropes: the one-parameter family the four above are special cases of
# ---------------------------------------------------------------------------


def polytropic_pressure(volumes, p_ref: float, v_ref: float, index: float) -> np.ndarray:
    """P(V) along P V^n = constant. n = 0, 1, gamma, infinity gives the four named families."""
    volumes = np.asarray(volumes, dtype=float)
    return p_ref * (v_ref / volumes) ** index


#: Where the rational polytropic work stops beating its own limit, in the only variable that
#: matters: |(n - 1) ln(V_2/V_1)|. The rational form subtracts two nearly equal numbers, so it
#: loses relative accuracy like eps_machine/|(n-1) ln(V2/V1)|, while the logarithm is the
#: (n - 1) -> 0 limit and is wrong by about half that same product. The two cross where the
#: product is sqrt(2 * 2.2e-16) ~ 2e-8, measured and confirmed against 60-digit arithmetic.
#: Below this, take the logarithm; above it, the rational form is the more accurate of the two.
_POLYTROPE_LOG_CUTOFF = 1.0e-8


def polytropic_work_on_gas(p_start: float, v_start: float, v_end: float,
                           index: float) -> float:
    """W_on = (P_2 V_2 - P_1 V_1)/(n - 1), with the n = 1 isotherm handled by its logarithm.

    n = 1 is not a removable singularity to be nudged past numerically: the integral of
    dV/V genuinely is a logarithm, and evaluating the rational form at n = 1 + 1e-9 is how
    a plausible-looking wrong number gets produced.

    The branch is on |(n - 1) ln(V_2/V_1)|, not on n alone, because that product is what
    controls both errors -- see `_POLYTROPE_LOG_CUTOFF`. Guarding with `np.isclose(index, 1)`
    instead, as this once did, is wrong in the other direction: its default tolerance swallows
    everything out to n = 1.00001, where the rational form is accurate to 5e-12 and the
    logarithm it substitutes is only good to 5e-6. A caller who deliberately asks for a
    near-isothermal polytrope should get the polytrope.
    """
    log_ratio = float(np.log(v_end / v_start))
    if abs((index - 1.0) * log_ratio) < _POLYTROPE_LOG_CUTOFF:
        return -p_start * v_start * log_ratio
    p_end = polytropic_pressure(v_end, p_start, v_start, index)
    return float((p_end * v_end - p_start * v_start) / (index - 1.0))


# ---------------------------------------------------------------------------
# Irreversible processes: no curve, and the work follows the external pressure
# ---------------------------------------------------------------------------


def free_expansion(state: EquilibriumState, v_end: float) -> ProcessResult:
    """Pull the partition: the gas expands into vacuum inside an insulated box.

    Nothing pushes back, so W_on = 0; nothing conducts, so Q = 0; therefore ΔU = 0 and, for
    an ideal gas whose energy depends on temperature alone, ΔT = 0. The gas ends colder in
    NO sense whatever, and its final pressure is P_1 V_1/V_2 -- the isothermal value, reached
    without following the isotherm, without a reservoir, and without exchanging anything at
    all.

    This is the process the phrase "adiabatic means P V^gamma = constant" fails on. It is
    adiabatic by any definition (no heat crosses the boundary) and it obeys P V = constant.
    """
    if v_end <= state.volume:
        raise ValueError("a free expansion must increase the volume")
    end = EquilibriumState.from_temperature(
        state.n_particles, state.temperature, v_end, state.degrees_of_freedom
    )
    return ProcessResult(
        label="free expansion",
        start=state,
        end=end,
        work_on_gas=0.0,
        heat=0.0,
        quasistatic=False,
        path=None,
    )


def against_constant_external_pressure(state: EquilibriumState, p_external: float,
                                       v_end: float) -> ProcessResult:
    """Adiabatic change of volume against a fixed external pressure: W_on = -P_ext ΔV.

    The gas's own pressure appears nowhere in the work. That is not an approximation — it is
    the definition of work applied at the boundary, where the external agent is what the
    piston pushes against. Setting `p_external` to the gas's own pressure at every instant is
    what `adiabatic` does, and only then do the two agree.

    The end state follows from the first law (Q = 0, so ΔU = W_on), which means
    `first_law_residual` is zero by construction here — unlike the quasistatic constructors
    above. `adiabatic_against_constant_pressure` is the version with an independent closed
    form.
    """
    if p_external < 0:
        raise ValueError("external pressure cannot be negative")
    work = -p_external * (v_end - state.volume)
    capacity = heat_capacity_constant_volume(state.n_particles, state.degrees_of_freedom)
    t_end = state.temperature + work / capacity
    if t_end <= 0:
        raise ValueError(
            "the gas would have to give up more energy than it has — check p_external"
        )
    end = EquilibriumState.from_temperature(
        state.n_particles, t_end, v_end, state.degrees_of_freedom
    )
    return ProcessResult(
        label="against constant external pressure",
        start=state,
        end=end,
        work_on_gas=work,
        heat=0.0,
        quasistatic=False,
        path=None,
    )


def adiabatic_against_constant_pressure(state: EquilibriumState,
                                        p_external: float) -> ProcessResult:
    """Release the piston against a constant load and let it come to rest.

    The gas stops when its own pressure has fallen to the external one, which fixes the final
    state without any appeal to P V^gamma:

        T_2 = (C_V T_1 + P_ext V_1) / C_P,      V_2 = N k_B T_2 / P_ext.

    Derived from ΔU = -P_ext (V_2 - V_1) together with P_ext V_2 = N k_B T_2, so the work
    computed from -P_ext ΔV and the energy change computed from C_V ΔT are two independent
    routes to the same number — which is what `first_law_residual` then measures.
    """
    if p_external <= 0:
        raise ValueError("the piston needs something to push against: p_external must be > 0")
    c_v = heat_capacity_constant_volume(state.n_particles, state.degrees_of_freedom)
    c_p = heat_capacity_constant_pressure(state.n_particles, state.degrees_of_freedom)
    t_end = (c_v * state.temperature + p_external * state.volume) / c_p
    v_end = state.n_particles * K_B * t_end / p_external
    end = EquilibriumState(state.n_particles, p_external, v_end, state.degrees_of_freedom)
    return ProcessResult(
        label="against constant external pressure",
        start=state,
        end=end,
        work_on_gas=-p_external * (v_end - state.volume),
        heat=0.0,
        quasistatic=False,
        path=None,
    )


def external_pressure_for_equilibrium_at(state: EquilibriumState,
                                         volume_ratio: float) -> float:
    """The constant load an adiabatic expansion must push against to stop at `volume_ratio`.

    Inverting `adiabatic_against_constant_pressure`: with r = V_2/V_1 and x = P_ext/P_1,
    x = C_V / (r C_P - N k_B). Used to line up the three adiabatic routes of this module at
    one common final volume, so their final temperatures can be read against each other.
    """
    if volume_ratio <= 0:
        raise ValueError("volume ratio must be positive")
    c_v = heat_capacity_constant_volume(state.n_particles, state.degrees_of_freedom)
    c_p = heat_capacity_constant_pressure(state.n_particles, state.degrees_of_freedom)
    denominator = volume_ratio * c_p - state.n_particles * K_B
    if denominator <= 0:
        raise ValueError("no positive external pressure stops the gas at that volume ratio")
    return float(state.pressure * c_v / denominator)


def free_expansion_microstate(state: kinetics.GasState, factor: float,
                              axis: int = 0) -> kinetics.GasState:
    """The same free expansion, one level down: widen the box and touch nothing else.

    Removing a partition does not move a wall against a force, so no particle's velocity
    changes and the kinetic energy — hence the temperature — is exactly what it was. The
    positions are left where they are, inside the old sub-volume, and the gas spreads out on
    its own under `kinetics.simulate`.

    This is the falsifying experiment for "expanding gases cool": the model that says the
    temperature must drop makes a prediction about numbers this function leaves untouched by
    construction, and `simulate` then measures a pressure that has fallen by exactly the
    volume ratio.

    `axis` chooses which wall moves; negative indices count from the last, as elsewhere in
    NumPy. It is checked here rather than left to raise an IndexError from the assignment,
    because the useful thing to say is which axes this box actually has.
    """
    dimension = state.dimension
    if not -dimension <= axis < dimension:
        raise ValueError(
            f"axis {axis} is out of range for a {dimension}-dimensional box: "
            f"expected -{dimension} <= axis < {dimension}"
        )
    if factor <= 1.0:
        raise ValueError("a free expansion must enlarge the box")
    box = state.box.copy()
    box[axis] *= factor
    return kinetics.GasState(
        positions=state.positions.copy(),
        velocities=state.velocities.copy(),
        box=box,
        mass=state.mass,
    )
