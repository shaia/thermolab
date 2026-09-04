"""Render the demonstration animations for module 06 (thermodynamic processes).

Same approach as the module 05 renderer: everything is computed by `thermolab.processes`, the
output is MP4 written by `_common.save`, and there is no text beyond axis labels, so one file
serves both language sites and the explanation lives in the translated caption. The colour
coding is therefore load-bearing — the captions on both module pages name the colours, so
changing one here means changing both pages.

Run:  uv run python media/render/render_processes.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from thermolab import processes  # noqa: E402

N_PARTICLES = 1000
TEMPERATURE = 300.0
V1 = 1.0e-3
VOLUME_RATIO = 2.0

START = processes.EquilibriumState.from_temperature(N_PARTICLES, TEMPERATURE, V1)
V2 = VOLUME_RATIO * V1

# One colour per process family, reused in both animations and named in both captions.
ISOCHORIC = "#2563eb"
ISOBARIC = "#d97706"
ISOTHERMAL = "#059669"
ADIABATIC = "#dc2626"


def render_families(n_frames: int = 180) -> None:
    """The four quasistatic families leaving one common state, with their ledgers filling in.

    Each family is one constraint; the three bar panels are the first law's three columns, so
    the viewer can watch which of them stay at zero. Only the adiabatic bar in the heat panel
    never moves, and only the isochoric bar in the work panel never moves.
    """
    results = [
        (processes.isochoric(START, 0.5 * START.pressure, n_points=129), ISOCHORIC),
        (processes.isobaric(START, V2, n_points=129), ISOBARIC),
        (processes.isothermal(START, V2, n_points=129), ISOTHERMAL),
        (processes.adiabatic(START, V2, n_points=129), ADIABATIC),
    ]
    colours = [colour for _, colour in results]
    fractions = np.linspace(0.02, 1.0, n_frames)

    # Every quantity accumulates linearly in the fraction of the path traversed except the
    # work, which is a genuine integral — so it is the one that gets integrated properly.
    works = np.array(
        [[result.partial_work_on_gas(f) for f in fractions] for result, _ in results]
    )
    heats = np.outer([result.heat for result, _ in results], fractions)
    energies = np.outer([result.internal_energy_change for result, _ in results], fractions)

    # Margins are set here rather than by tight_layout, which cannot lay out a gridspec whose
    # first column spans all three rows and warns that its result may be wrong.
    fig = plt.figure(figsize=(9.2, 4.4), dpi=DPI)
    grid = fig.add_gridspec(
        3, 2, width_ratios=[1.45, 1.0], hspace=0.45, wspace=0.30,
        left=0.095, right=0.985, top=0.94, bottom=0.13,
    )
    plane = fig.add_subplot(grid[:, 0])
    ledger = [fig.add_subplot(grid[row, 1]) for row in range(3)]

    plane.plot([V1 * 1e3], [START.pressure], "ko", ms=7, zorder=5)
    plane.set_xlim(0.93 * V1 * 1e3, 1.07 * V2 * 1e3)
    plane.set_ylim(0, 1.12 * START.pressure)
    plane.set_xlabel("volume (L)")
    plane.set_ylabel("pressure (Pa)")
    curves = [plane.plot([], [], lw=2.3, color=colour)[0] for colour in colours]

    series = [works, heats, energies]
    labels = ["work on gas (J)", "heat in (J)", "energy change (J)"]
    bar_sets = []
    for axis, values, label in zip(ledger, series, labels, strict=True):
        span = max(abs(values.min()), abs(values.max()))
        axis.set_ylim(-1.15 * span, 1.15 * span)
        axis.axhline(0.0, color="#94a3b8", lw=0.8)
        axis.set_xlim(-0.7, 3.7)
        axis.set_xticks([])
        axis.set_ylabel(label, fontsize=8)
        axis.tick_params(labelsize=7)
        bar_sets.append(axis.bar(range(4), [0, 0, 0, 0], width=0.6, color=colours))

    def update(frame: int):
        artists = []
        for curve, (result, _) in zip(curves, results, strict=True):
            path = result.quasistatic_path
            cut = max(2, int(fractions[frame] * path.volumes.size))
            curve.set_data(path.volumes[:cut] * 1e3, path.pressures[:cut])
            artists.append(curve)
        for bars, values in zip(bar_sets, series, strict=True):
            for bar, row in zip(bars, values, strict=True):
                bar.set_height(row[frame])
                artists.append(bar)
        return artists

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "processes-families")
    plt.close(fig)


def render_three_adiabats(n_frames: int = 180) -> None:
    """Three adiabatic expansions to one final volume: slow, against a load, and free.

    The shaded areas are the works and are drawn to the same scale, so the eye compares them
    directly. The right panel is the point of the module: the quasistatic route is the only one
    with a curve to draw, and the other two are two dots with nothing in between — which is
    what a process that leaves the set of equilibrium states actually looks like.
    """
    slow = processes.adiabatic(START, V2, n_points=n_frames + 1)
    slow_path = slow.quasistatic_path
    p_external = processes.external_pressure_for_equilibrium_at(START, VOLUME_RATIO)
    loaded = processes.adiabatic_against_constant_pressure(START, p_external)
    free = processes.free_expansion(START, V2)

    volumes = np.linspace(V1, V2, n_frames)
    slow_temperatures = processes.adiabatic_final_temperature(
        TEMPERATURE, V1, volumes, START.gamma
    )

    fig, (plane, bars, thermal) = plt.subplots(
        1, 3, figsize=(11.4, 3.6), dpi=DPI, gridspec_kw={"width_ratios": [1.35, 0.7, 1.1]}
    )

    # --- left: the P-V plane, with each route's work shaded to the same scale ---
    plane.set_xlim(0.93 * V1 * 1e3, 1.07 * V2 * 1e3)
    plane.set_ylim(0, 1.12 * START.pressure)
    plane.set_xlabel("volume (L)")
    plane.set_ylabel("pressure (Pa)")
    plane.axhline(p_external, color=ISOBARIC, lw=1.4, ls=":")
    plane.plot([V1 * 1e3], [START.pressure], "ko", ms=7, zorder=6)
    (slow_curve,) = plane.plot([], [], lw=2.3, color=ADIABATIC, zorder=5)
    shading = [
        plane.fill_between([], [], alpha=0.0),
        plane.fill_between([], [], alpha=0.0),
    ]
    endpoints = [
        plane.plot([], [], "o", ms=8, color=colour, zorder=6)[0]
        for colour in (ADIABATIC, ISOBARIC, ISOTHERMAL)
    ]
    final_states = [slow.end, loaded.end, free.end]

    # --- middle: the work each route delivers, growing as the volume sweeps ---
    delivered = np.array(
        [
            [-slow.partial_work_on_gas(f) for f in np.linspace(0.02, 1.0, n_frames)],
            p_external * (volumes - V1),
            np.zeros(n_frames),
        ]
    )
    bars.set_xlim(-0.7, 2.7)
    bars.set_ylim(0, 1.15 * delivered.max())
    bars.set_xticks([])
    bars.set_ylabel("work delivered (J)")
    work_bars = bars.bar(
        range(3), [0, 0, 0], width=0.6, color=[ADIABATIC, ISOBARIC, ISOTHERMAL]
    )

    # --- right: temperature. Only the slow route has states in between to draw. ---
    thermal.set_xlim(0.93 * V1 * 1e3, 1.07 * V2 * 1e3)
    thermal.set_ylim(0.9 * slow.end.temperature, 1.06 * TEMPERATURE)
    thermal.set_xlabel("volume (L)")
    thermal.set_ylabel("temperature (K)")
    thermal.plot([V1 * 1e3], [TEMPERATURE], "ko", ms=7, zorder=6)
    (slow_thermal,) = thermal.plot([], [], lw=2.3, color=ADIABATIC)
    thermal_endpoints = [
        thermal.plot([], [], "o", ms=8, color=colour, zorder=6)[0]
        for colour in (ADIABATIC, ISOBARIC, ISOTHERMAL)
    ]

    fig.tight_layout()

    reveal_from = int(0.82 * n_frames)

    def update(frame: int):
        cut = frame + 2
        slow_curve.set_data(slow_path.volumes[:cut] * 1e3, slow_path.pressures[:cut])
        slow_thermal.set_data(volumes[: frame + 1] * 1e3, slow_temperatures[: frame + 1])

        for patch in shading:
            patch.remove()
        shading[0] = plane.fill_between(
            slow_path.volumes[:cut] * 1e3, slow_path.pressures[:cut],
            alpha=0.22, color=ADIABATIC,
        )
        shading[1] = plane.fill_between(
            volumes[: frame + 1] * 1e3, p_external, alpha=0.22, color=ISOBARIC
        )

        # The endpoints are states, not stages: they exist only once the process is over, so
        # they are revealed at the end rather than tracked. The free expansion never acquires
        # anything else to draw, which is the whole point.
        visible = frame >= reveal_from
        for marker, thermal_marker, state in zip(
            endpoints, thermal_endpoints, final_states, strict=True
        ):
            marker.set_data(
                [V2 * 1e3] if visible else [], [state.pressure] if visible else []
            )
            thermal_marker.set_data(
                [V2 * 1e3] if visible else [], [state.temperature] if visible else []
            )

        for bar, row in zip(work_bars, delivered, strict=True):
            bar.set_height(row[frame])

        return [slow_curve, slow_thermal, *shading, *endpoints, *thermal_endpoints, *work_bars]

    save(
        FuncAnimation(fig, update, frames=n_frames, blit=False),
        fig,
        "processes-three-adiabats",
    )
    plt.close(fig)


def main() -> None:
    render_families()
    render_three_adiabats()


if __name__ == "__main__":
    main()
