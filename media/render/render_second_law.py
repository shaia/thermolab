"""Render the demonstration animations for module 07 (the second law and heat engines).

Same approach as the earlier renderers: every number comes from `thermolab.engines`, the
output is MP4 written by `_common.save`, and there is no text beyond axis labels, so one file
serves both language sites and the explanation lives in the translated caption.

The colour coding is load-bearing — the captions on both module pages name the colours, so
changing one here means changing both pages. Hot strokes are red, cold strokes blue, and the
two adiabats grey, because the point being made is *which reservoir is being touched*, which
is a different question from the process family that coloured module 06.

Run:  uv run python media/render/render_second_law.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from thermolab import engines  # noqa: E402

N_PARTICLES = 1000
T_HOT = 600.0
T_COLD = 300.0
V_START = 1.0e-3
EXPANSION_RATIO = 2.5

HOT = "#dc2626"
COLD = "#2563eb"
ADIABATIC = "#94a3b8"
BOUND = "#0f172a"
MAXPOWER = "#d97706"


def render_carnot_cycle(n_frames: int = 240) -> None:
    """The Carnot loop traced stroke by stroke, with its energy ledger filling in beside it.

    The third bar is the whole argument of the module: it starts at zero, and by the time the
    loop closes it has never come back. An engine that did not fill that bar would violate
    the Kelvin statement, and no arrangement of the other three panels can avoid it.
    """
    cycle = engines.carnot_cycle(
        N_PARTICLES, T_HOT, T_COLD, V_START, EXPANSION_RATIO, n_points=241
    )
    strokes = [stroke.process for stroke in cycle.strokes]
    colours = [HOT, ADIABATIC, COLD, ADIABATIC]

    # Frames are split evenly between the four strokes; `schedule` maps a frame to the stroke
    # it belongs to and how far along that stroke it is.
    per_stroke = n_frames // 4
    schedule = [(k, (i + 1) / per_stroke) for k in range(4) for i in range(per_stroke)]

    # The ledger accumulates. Along an isotherm dU = 0, so the heat crossing so far is exactly
    # minus the work done on the gas so far -- which is why a partial heat can be read off a
    # partial work at all. The adiabats contribute nothing to either heat bar.
    #
    # The work bar is a *running net*, and it genuinely overshoots: the two expansion strokes
    # deliver 1.38e-17 J before the two compression strokes hand 1.0e-17 J of it back, leaving
    # the loop area. That is worth seeing rather than hiding, but it means the axis has to be
    # sized from the running series and not from the per-cycle totals -- sized from the totals,
    # the work bar runs off the top of the plot for half the animation.
    def ledger(frame: int) -> tuple[float, float, float]:
        stroke_index, fraction = schedule[frame]
        work_out = 0.0
        heat_in = 0.0
        heat_out = 0.0
        for k, process in enumerate(strokes):
            if k < stroke_index:
                partial = process.work_on_gas
            elif k == stroke_index:
                partial = process.partial_work_on_gas(fraction)
            else:
                break
            work_out += -partial
            if k == 0:
                heat_in += -partial
            elif k == 2:
                heat_out += partial
        return heat_in, work_out, heat_out

    series = np.array([ledger(frame) for frame in range(len(schedule))])

    fig = plt.figure(figsize=(10.4, 4.4), dpi=DPI)
    grid = fig.add_gridspec(
        1, 2, width_ratios=[1.5, 1.0], wspace=0.28,
        left=0.085, right=0.985, top=0.95, bottom=0.14,
    )
    plane = fig.add_subplot(grid[0, 0])
    bars_axis = fig.add_subplot(grid[0, 1])

    all_volumes = np.concatenate([p.quasistatic_path.volumes for p in strokes])
    all_pressures = np.concatenate([p.quasistatic_path.pressures for p in strokes])
    plane.set_xlim(0.92 * all_volumes.min() * 1e3, 1.06 * all_volumes.max() * 1e3)
    plane.set_ylim(0.0, 1.10 * all_pressures.max())
    plane.set_xlabel("volume (L)")
    plane.set_ylabel("pressure (Pa)")
    plane.plot([V_START * 1e3], [strokes[0].start.pressure], "ko", ms=7, zorder=6)
    curves = [plane.plot([], [], lw=2.6, color=colour, zorder=5)[0] for colour in colours]
    shading = [plane.fill([], [], alpha=0.0)[0]]

    bars_axis.set_xlim(-0.7, 2.7)
    bars_axis.set_ylim(0.0, 1.08 * float(series.max()))
    bars_axis.set_xticks([])
    bars_axis.set_ylabel("energy per cycle (J)")
    energy_bars = bars_axis.bar(
        range(3), [0.0, 0.0, 0.0], width=0.6, color=[HOT, BOUND, COLD]
    )

    def update(frame: int):
        stroke_index, fraction = schedule[frame]
        traced_v: list[float] = []
        traced_p: list[float] = []
        for k, (curve, process) in enumerate(zip(curves, strokes, strict=True)):
            path = process.quasistatic_path
            if k < stroke_index:
                cut = path.volumes.size
            elif k == stroke_index:
                cut = max(2, int(fraction * path.volumes.size))
            else:
                cut = 0
            if cut:
                curve.set_data(path.volumes[:cut] * 1e3, path.pressures[:cut])
                traced_v.extend(path.volumes[:cut] * 1e3)
                traced_p.extend(path.pressures[:cut])
            else:
                curve.set_data([], [])

        # The shaded region is the polygon from the traced curve closed straight back to the
        # start, so it is the loop only once the final stroke is returning along the bottom.
        # Before that it cuts a chord across the diagram and overstates the area by roughly
        # threefold — so it stays invisible until the last stroke and fades in as the curve
        # actually closes. Shading a partial loop is the sort of picture that quietly teaches
        # the wrong number.
        shading[0].remove()
        closing = 0.13 * fraction if stroke_index == 3 else 0.0
        shading[0] = plane.fill(
            traced_v, traced_p, color=BOUND, alpha=closing, zorder=1, linewidth=0
        )[0]

        for bar, value in zip(energy_bars, series[frame], strict=True):
            bar.set_height(value)

        return [*curves, shading[0], *energy_bars]

    save(
        FuncAnimation(fig, update, frames=len(schedule), blit=False),
        fig,
        "second-law-carnot-cycle",
    )
    plt.close(fig)


def render_efficiency_bound(n_frames: int = 200) -> None:
    """Many engines, accumulating under the bound curve, and never once above it.

    Each point is a real cycle built by `engines`, not a sketch: its efficiency is measured
    from the strokes. The visual claim is the empty region above the curve, so the axes are
    deliberately generous above it — a plot clipped at the curve would be begging the
    question.
    """
    rng = np.random.default_rng(20260923)
    n_engines = 320

    cold = rng.uniform(80.0, 560.0, n_engines)
    gap_fraction = rng.uniform(0.0, 0.30, n_engines)
    efficiencies = np.empty(n_engines)
    for i, (t_cold, fraction) in enumerate(zip(cold, gap_fraction, strict=True)):
        span = T_HOT - t_cold
        efficiencies[i] = engines.endoreversible_cycle(
            N_PARTICLES, T_HOT, float(t_cold), V_START, 2.5,
            hot_gap=float(fraction * span * 0.5),
            cold_gap=float(fraction * span * 0.5),
        ).efficiency

    ratio = cold / T_HOT
    order = np.argsort(rng.random(n_engines))
    cold, ratio, efficiencies, gap_fraction = (
        cold[order], ratio[order], efficiencies[order], gap_fraction[order]
    )

    smooth = np.linspace(0.05, 0.98, 400)
    fig, axis = plt.subplots(figsize=(7.6, 4.6), dpi=DPI)
    axis.plot(smooth, 1.0 - smooth, lw=2.4, color=BOUND, zorder=4)
    axis.plot(smooth, 1.0 - np.sqrt(smooth), lw=1.8, ls="--", color=MAXPOWER, zorder=3)
    axis.set_xlim(0.05, 1.0)
    axis.set_ylim(0.0, 1.0)
    axis.set_xlabel(r"$T_c / T_h$")
    axis.set_ylabel("efficiency")

    scatter = axis.scatter(
        [], [], s=22, c=[], cmap="Blues_r", vmin=-0.10, vmax=0.32,
        edgecolors="none", zorder=5,
    )

    revealed = np.linspace(1, n_engines, n_frames).astype(int)

    def update(frame: int):
        count = revealed[frame]
        scatter.set_offsets(np.column_stack([ratio[:count], efficiencies[:count]]))
        scatter.set_array(gap_fraction[:count])
        return [scatter]

    fig.tight_layout()
    save(
        FuncAnimation(fig, update, frames=n_frames, blit=False),
        fig,
        "second-law-efficiency-bound",
    )
    plt.close(fig)


def main() -> None:
    render_carnot_cycle()
    render_efficiency_bound()


if __name__ == "__main__":
    main()
