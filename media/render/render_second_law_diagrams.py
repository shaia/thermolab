"""Render the static diagrams for module 07 (the second law and heat engines).

The second law's central arguments are about *combining machines*: glue a hypothetical
violator to an ordinary engine and read off what the pair does. Every textbook draws these as
energy-flow diagrams — reservoirs as bars, machines as circles, arrows for every joule — and
the arguments are genuinely hard to follow in words alone. These are those diagrams.

They are PNG, not MP4: nothing in them moves. Like the animations they carry no words, only
symbols and numbers, so one file serves both language sites and the explanation lives in the
translated caption. The colour code matches `render_second_law.py` and the captions name it:
red for the hot side, blue for the cold side, dark for work, and a dashed outline for any
machine that cannot exist — which is the point of drawing it.

The P-V panel takes every curve from `thermolab.processes` and `thermolab.engines`; the
schematics contain no physics beyond the energy bookkeeping written on their arrows.

Run:  uv run python media/render/render_second_law_diagrams.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

from _common import save_still  # noqa: E402
from thermolab import engines, processes  # noqa: E402

HOT = "#dc2626"
HOT_FILL = "#fee2e2"
COLD = "#2563eb"
COLD_FILL = "#dbeafe"
INK = "#0f172a"
ADIABATIC = "#94a3b8"
IMPOSSIBLE_FILL = "#f1f5f9"
BOUNDARY = "#64748b"
AREA_FILL = "#e2e8f0"

LABEL_SIZE = 15
SYMBOL_SIZE = 17


# ---------------------------------------------------------------------------
# Drawing primitives for the energy-flow schematics
# ---------------------------------------------------------------------------


def blank_axes(ax: Axes, width: float, height: float) -> None:
    ax.set_xlim(0.0, width)
    ax.set_ylim(0.0, height)
    ax.set_aspect("equal")
    ax.axis("off")


def reservoir(ax: Axes, x0: float, x1: float, y: float, label: str, hot: bool,
              height: float = 0.8) -> None:
    """A reservoir: a long bar, because it is large enough that nothing we do moves its T."""
    colour, fill = (HOT, HOT_FILL) if hot else (COLD, COLD_FILL)
    ax.add_patch(
        FancyBboxPatch(
            (x0, y - height / 2), x1 - x0, height,
            boxstyle="round,pad=0.02,rounding_size=0.18",
            facecolor=fill, edgecolor=colour, linewidth=1.8,
        )
    )
    ax.text((x0 + x1) / 2, y, label, ha="center", va="center", fontsize=SYMBOL_SIZE,
            color=colour)


def machine(ax: Axes, x: float, y: float, label: str = "", impossible: bool = False,
            radius: float = 0.55) -> None:
    """A cyclic machine. Dashed and greyed when it is the hypothetical one being refuted."""
    ax.add_patch(
        Circle(
            (x, y), radius,
            facecolor=IMPOSSIBLE_FILL if impossible else "white",
            edgecolor=INK, linewidth=1.8, linestyle=(0, (4, 3)) if impossible else "-",
        )
    )
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=SYMBOL_SIZE, color=INK)


def flow(ax: Axes, start: tuple[float, float], end: tuple[float, float], label: str,
         colour: str, side: str = "right", offset: float = 0.18, at: float = 0.5) -> None:
    """An energy arrow with its magnitude written beside it; the arrow carries the sign.

    `at` is how far along the arrow the label sits, for arrows that converge and would
    otherwise print their labels on top of one another at their midpoints.
    """
    ax.add_patch(
        FancyArrowPatch(
            start, end, arrowstyle="-|>", mutation_scale=20, linewidth=2.4, color=colour,
            shrinkA=0, shrinkB=0,
        )
    )
    mid_x = start[0] + at * (end[0] - start[0])
    mid_y = start[1] + at * (end[1] - start[1])
    if side == "right":
        ax.text(mid_x + offset, mid_y, label, ha="left", va="center", fontsize=LABEL_SIZE,
                color=colour)
    elif side == "left":
        ax.text(mid_x - offset, mid_y, label, ha="right", va="center", fontsize=LABEL_SIZE,
                color=colour)
    else:  # above
        ax.text(mid_x, mid_y + offset, label, ha="center", va="bottom", fontsize=LABEL_SIZE,
                color=colour)


def boundary(ax: Axes, x0: float, y0: float, x1: float, y1: float) -> None:
    """The dotted line drawn round a combination, so it can be read as one machine."""
    ax.add_patch(
        FancyBboxPatch(
            (x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0.02,rounding_size=0.25",
            facecolor="none", edgecolor=BOUNDARY, linewidth=1.4, linestyle=(0, (1.5, 2.5)),
        )
    )


def equals(ax: Axes, x: float, y: float) -> None:
    ax.text(x, y, "$=$", ha="center", va="center", fontsize=30, color=INK)


def panel_tag(ax: Axes, x: float, y: float, tag: str) -> None:
    ax.text(x, y, tag, ha="left", va="top", fontsize=LABEL_SIZE, color=INK)


# Vertical layout shared by every schematic: hot bar on top, cold bar at the bottom, machines
# in between. Arrows stop at the circle's rim (radius 0.55) and at the bars' edges (half-height
# 0.4), so the numbers below are those two facts and nothing else.
HOT_Y, COLD_Y, MID_Y = 5.2, 0.8, 3.0
TOP_OF_MACHINE, BOTTOM_OF_MACHINE = MID_Y + 0.55, MID_Y - 0.55
UNDER_HOT, OVER_COLD = HOT_Y - 0.4, COLD_Y + 0.4


def down_from_hot(ax: Axes, x: float, label: str, side: str = "right") -> None:
    flow(ax, (x, UNDER_HOT), (x, TOP_OF_MACHINE), label, HOT, side)


def up_to_hot(ax: Axes, x: float, label: str, side: str = "right") -> None:
    flow(ax, (x, TOP_OF_MACHINE), (x, UNDER_HOT), label, HOT, side)


def down_to_cold(ax: Axes, x: float, label: str, side: str = "right") -> None:
    flow(ax, (x, BOTTOM_OF_MACHINE), (x, OVER_COLD), label, COLD, side)


def up_from_cold(ax: Axes, x: float, label: str, side: str = "right") -> None:
    flow(ax, (x, OVER_COLD), (x, BOTTOM_OF_MACHINE), label, COLD, side)


# ---------------------------------------------------------------------------
# The diagrams
# ---------------------------------------------------------------------------


def render_machines() -> None:
    """(a) an engine, (b) the same machine run backwards: refrigerator or heat pump."""
    fig, ax = plt.subplots(figsize=(10.0, 4.6))
    blank_axes(ax, 12.4, 6.0)

    # (a) Engine: heat in from the hot side, work out, the rest down to the cold side.
    panel_tag(ax, 0.2, 5.95, "(a)")
    reservoir(ax, 1.2, 4.8, HOT_Y, "$T_h$", hot=True)
    reservoir(ax, 1.2, 4.8, COLD_Y, "$T_c$", hot=False)
    machine(ax, 3.0, MID_Y)
    down_from_hot(ax, 3.0, "$Q_h$")
    down_to_cold(ax, 3.0, "$Q_c$")
    flow(ax, (3.55, MID_Y), (5.4, MID_Y), "$W$", INK, side="above")

    # (b) Refrigerator / heat pump: work in, heat lifted from cold, delivered to hot.
    panel_tag(ax, 6.6, 5.95, "(b)")
    reservoir(ax, 7.6, 11.2, HOT_Y, "$T_h$", hot=True)
    reservoir(ax, 7.6, 11.2, COLD_Y, "$T_c$", hot=False)
    machine(ax, 9.4, MID_Y)
    up_from_cold(ax, 9.4, "$Q_c$")
    up_to_hot(ax, 9.4, "$Q_h$")
    flow(ax, (11.8, MID_Y), (9.95, MID_Y), "$W$", INK, side="above")

    save_still(fig, "second-law-machines")
    plt.close(fig)


def render_equivalence() -> None:
    """Each statement's violator, combined with an ordinary machine, violates the other."""
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10.0, 9.0))

    # (a) A Clausius violator C plus an ordinary engine E is a Kelvin violator.
    blank_axes(top, 13.6, 6.0)
    panel_tag(top, 0.0, 5.95, "(a)")
    reservoir(top, 0.6, 6.6, HOT_Y, "$T_h$", hot=True)
    reservoir(top, 0.6, 6.6, COLD_Y, "$T_c$", hot=False)
    machine(top, 1.9, MID_Y, "$C$", impossible=True)
    up_from_cold(top, 1.9, "$Q_c$", side="left")
    up_to_hot(top, 1.9, "$Q_c$", side="left")
    machine(top, 4.6, MID_Y, "$E$")
    down_from_hot(top, 4.6, "$Q_h$")
    down_to_cold(top, 4.6, "$Q_c$")
    flow(top, (5.15, MID_Y), (7.0, MID_Y), "$W$", INK, side="above")
    boundary(top, 1.05, 2.15, 5.45, 3.85)
    equals(top, 7.9, MID_Y)
    reservoir(top, 8.8, 12.8, HOT_Y, "$T_h$", hot=True)
    reservoir(top, 8.8, 12.8, COLD_Y, "$T_c$", hot=False)
    machine(top, 10.8, MID_Y, impossible=True)
    down_from_hot(top, 10.8, "$Q_h - Q_c$", side="left")
    flow(top, (11.35, MID_Y), (13.3, MID_Y), "$W$", INK, side="above")

    # (b) A Kelvin violator K driving an ordinary refrigerator F is a Clausius violator.
    blank_axes(bottom, 13.6, 6.0)
    panel_tag(bottom, 0.0, 5.95, "(b)")
    reservoir(bottom, 0.6, 6.6, HOT_Y, "$T_h$", hot=True)
    reservoir(bottom, 0.6, 6.6, COLD_Y, "$T_c$", hot=False)
    machine(bottom, 1.9, MID_Y, "$K$", impossible=True)
    down_from_hot(bottom, 1.9, "$Q$", side="left")
    flow(bottom, (2.45, MID_Y), (4.05, MID_Y), "$W$", INK, side="above")
    machine(bottom, 4.6, MID_Y, "$F$")
    up_from_cold(bottom, 4.6, "$Q_c$")
    up_to_hot(bottom, 4.6, "$Q + Q_c$")
    boundary(bottom, 1.05, 2.15, 5.45, 3.85)
    equals(bottom, 7.9, MID_Y)
    reservoir(bottom, 8.8, 12.8, HOT_Y, "$T_h$", hot=True)
    reservoir(bottom, 8.8, 12.8, COLD_Y, "$T_c$", hot=False)
    machine(bottom, 10.8, MID_Y, impossible=True)
    up_from_cold(bottom, 10.8, "$Q_c$")
    up_to_hot(bottom, 10.8, "$Q_c$")

    fig.subplots_adjust(hspace=0.08)
    save_still(fig, "second-law-equivalence")
    plt.close(fig)


def render_carnot_proof() -> None:
    """Carnot's proof with the page's numbers: X (eta 0.6) driving a reversed R (eta 0.5)."""
    fig, ax = plt.subplots(figsize=(10.0, 4.6))
    blank_axes(ax, 13.6, 6.0)

    reservoir(ax, 0.6, 6.6, HOT_Y, "$T_h$", hot=True)
    reservoir(ax, 0.6, 6.6, COLD_Y, "$T_c$", hot=False)
    machine(ax, 1.9, MID_Y, "$X$", impossible=True)
    down_from_hot(ax, 1.9, r"$500\,\mathrm{J}$", side="left")
    down_to_cold(ax, 1.9, r"$200\,\mathrm{J}$", side="left")
    flow(ax, (2.45, MID_Y), (4.05, MID_Y), r"$300\,\mathrm{J}$", INK, side="above")
    machine(ax, 4.6, MID_Y, "$R$")
    up_from_cold(ax, 4.6, r"$300\,\mathrm{J}$")
    up_to_hot(ax, 4.6, r"$600\,\mathrm{J}$")
    boundary(ax, 1.05, 2.15, 5.45, 3.85)

    equals(ax, 7.9, MID_Y)
    reservoir(ax, 8.8, 12.8, HOT_Y, "$T_h$", hot=True)
    reservoir(ax, 8.8, 12.8, COLD_Y, "$T_c$", hot=False)
    machine(ax, 10.8, MID_Y, impossible=True)
    up_from_cold(ax, 10.8, r"$100\,\mathrm{J}$")
    up_to_hot(ax, 10.8, r"$100\,\mathrm{J}$")

    save_still(fig, "second-law-carnot-proof")
    plt.close(fig)


def render_clausius_inequality() -> None:
    """Clausius's construction: one auxiliary Carnot engine per temperature the device meets.

    Each auxiliary engine C_i runs between a single reference reservoir T_0 and the
    temperature T_i, and hands the device exactly the heat dQ_i it takes in there. The
    dotted boundary then touches only T_0, which is where the Kelvin statement bites.
    """
    fig, ax = plt.subplots(figsize=(10.0, 5.6))
    blank_axes(ax, 12.0, 7.0)

    top_y = 6.3
    aux_y = 3.9
    device_y = 1.0
    reservoir(ax, 0.8, 11.2, top_y, "$T_0$", hot=True)

    columns = [(2.2, "1"), (5.0, "2"), (9.8, "n")]
    ax.text(7.4, aux_y, r"$\cdots$", ha="center", va="center", fontsize=26, color=INK)
    for x, index in columns:
        machine(ax, x, aux_y, f"$C_{index}$", radius=0.6)
        flow(ax, (x, top_y - 0.4), (x, aux_y + 0.6),
             rf"$\delta Q_{index}\,T_0/T_{index}$", HOT, side="right")
        flow(ax, (x + 0.6, aux_y), (x + 1.5, aux_y), f"$W_{index}$", INK, side="above",
             offset=0.12)

    # Heat from each auxiliary engine into the device, at the temperature T_i it meets there.
    # Labels sit near the top of each converging arrow, where the arrows are still apart.
    machine(ax, 6.0, device_y, "$D$", radius=0.6)
    label_sides = {"1": "left", "2": "right", "n": "right"}
    for x, index in columns:
        end_x = 6.0 + 0.45 * np.sign(x - 6.0) if x != 6.0 else 6.0
        flow(ax, (x, aux_y - 0.6), (end_x, device_y + 0.45),
             rf"$\delta Q_{index},\ T_{index}$", COLD, side=label_sides[index], at=0.3)
    flow(ax, (6.6, device_y), (8.2, device_y), "$W$", INK, side="above")

    boundary(ax, 0.9, 0.15, 11.6, 4.9)
    save_still(fig, "second-law-clausius-inequality")
    plt.close(fig)


def render_two_reservoirs() -> None:
    """(a) one reservoir: every adiabat crosses the isotherm once, so no loop has area.
    (b) two reservoirs: compression on the colder isotherm runs at lower pressure.
    """
    n_particles, t_hot, t_cold, v_1 = 1000, 600.0, 300.0, 1.0e-3

    start = processes.EquilibriumState.from_temperature(n_particles, t_hot, v_1)
    p_1 = start.pressure
    isotherm = processes.isothermal(start, 3.0 * v_1).quasistatic_path

    fig, (left, right) = plt.subplots(1, 2, figsize=(10.4, 4.4), sharey=True)

    # (a) The single isotherm, and adiabats through three of its points, each continued a
    # little way on either side so the single crossing is visible.
    left.plot(isotherm.volumes / v_1, isotherm.pressures / p_1, color=HOT, linewidth=2.6)
    for v_cross in (1.3, 1.9, 2.6):
        point = processes.EquilibriumState.from_temperature(n_particles, t_hot, v_cross * v_1)
        for v_end in (0.72 * v_cross * v_1, 1.3 * v_cross * v_1):
            leg = processes.adiabatic(point, v_end).quasistatic_path
            left.plot(leg.volumes / v_1, leg.pressures / p_1, color=ADIABATIC, linewidth=1.8)
    left.text(2.95, isotherm.pressures[-1] / p_1 + 0.07, "$T$", color=HOT,
              fontsize=LABEL_SIZE, ha="right", va="bottom")

    # (b) The Carnot loop between two reservoirs, shaded, with the direction of travel.
    cycle = engines.carnot_cycle(n_particles, t_hot, t_cold, v_1, 2.0, n_points=257)
    colours = [HOT, ADIABATIC, COLD, ADIABATIC]
    loop_v = []
    loop_p = []
    for stroke, colour in zip(cycle.strokes, colours, strict=True):
        path = stroke.process.quasistatic_path
        v = path.volumes / v_1
        p = path.pressures / p_1
        right.plot(v, p, color=colour, linewidth=2.6)
        mid = v.size // 2
        right.annotate(
            "", xy=(v[mid + 1], p[mid + 1]), xytext=(v[mid - 1], p[mid - 1]),
            arrowprops={"arrowstyle": "-|>", "color": colour, "mutation_scale": 18,
                        "linewidth": 0},
        )
        loop_v.append(v)
        loop_p.append(p)
    right.fill(np.concatenate(loop_v), np.concatenate(loop_p), color=AREA_FILL, zorder=0)
    hot_path = cycle.strokes[0].process.quasistatic_path
    cold_path = cycle.strokes[2].process.quasistatic_path
    right.text(hot_path.volumes[-1] / v_1 + 0.05, hot_path.pressures[-1] / p_1 + 0.03,
               "$T_h$", color=HOT, fontsize=LABEL_SIZE, ha="left", va="bottom")
    right.text(cold_path.volumes[-1] / v_1 - 0.08, cold_path.pressures[-1] / p_1 - 0.03,
               "$T_c$", color=COLD, fontsize=LABEL_SIZE, ha="right", va="top")

    for ax, tag in ((left, "(a)"), (right, "(b)")):
        ax.set_xlabel("$V / V_1$", fontsize=LABEL_SIZE - 2)
        ax.text(0.02, 0.98, tag, transform=ax.transAxes, ha="left", va="top",
                fontsize=LABEL_SIZE, color=INK)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=11)
    left.set_ylabel("$P / P_1$", fontsize=LABEL_SIZE - 2)
    left.set_ylim(0.0, 1.35)
    fig.tight_layout()
    save_still(fig, "second-law-two-reservoirs")
    plt.close(fig)


if __name__ == "__main__":
    render_machines()
    render_equivalence()
    render_carnot_proof()
    render_clausius_inequality()
    render_two_reservoirs()
