"""Render the demonstration animations for module 01 (thermal equilibrium).

Animations are produced from `thermolab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_equilibrium.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from thermolab import equilibrium  # noqa: E402
from thermolab.constants import K_B  # noqa: E402

QUANTUM = 20.0 * K_B  # an arbitrary but fixed energy quantum, shared by both bodies


def render_relaxation(n_frames: int = 240, steps_per_frame: int = 20) -> None:
    """Two bodies' temperatures converging, beside the analytic exponential prediction.

    The point of the pairing: both curves bend smoothly onto the dashed prediction, with no
    hand-tuning — the same closed form derived on the module page.
    """
    rng = np.random.default_rng(3)
    state = equilibrium.from_temperatures(300, 100, 500.0, 250.0, QUANTUM)
    n_steps = n_frames * steps_per_frame

    result = equilibrium.simulate_energy_exchange(state, n_steps, rng)
    sample = slice(steps_per_frame - 1, None, steps_per_frame)
    frame_steps = result.steps[sample]
    t_a = result.temperature_a[sample]
    t_b = result.temperature_b[sample]
    t_eq = equilibrium.equilibrium_temperature(
        state.heat_capacity_a, state.temperature_a, state.heat_capacity_b, state.temperature_b
    )
    predicted = t_eq + equilibrium.predicted_relaxation(state, frame_steps)

    fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=DPI)
    (line_a,) = ax.plot([], [], lw=1.8, color="#dc2626", label="body A")
    (line_b,) = ax.plot([], [], lw=1.8, color="#2563eb", label="body B")
    (line_pred,) = ax.plot([], [], lw=1.2, ls="--", color="black", label="predicted")
    ax.axhline(t_eq, color="grey", ls=":", lw=1.0)
    ax.set_xlim(0, float(frame_steps[-1]))
    ax.set_ylim(200, 550)
    ax.set_xlabel("step")
    ax.set_ylabel("temperature (K)")
    ax.set_title("two bodies relaxing to a shared temperature")
    ax.legend(loc="center right")
    fig.tight_layout()

    def update(frame: int):
        line_a.set_data(frame_steps[:frame], t_a[:frame])
        line_b.set_data(frame_steps[:frame], t_b[:frame])
        line_pred.set_data(frame_steps[:frame], predicted[:frame])
        return line_a, line_b, line_pred

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "equilibrium-relaxation")
    plt.close(fig)


def render_fluctuations(n_frames: int = 180, steps_per_frame: int = 20) -> None:
    """The same relaxation at three system sizes, each as a fraction of the initial gap.

    Plotting (T_A - T_B) / (T_A0 - T_B0) is what makes the comparison honest: the three runs
    share the same fractional starting point and analytic curve, and only the scatter around
    it differs.
    """
    rng = np.random.default_rng(11)
    sizes = ((30, 10), (300, 100), (3000, 1000))

    traces = []
    for n_a, n_b in sizes:
        state = equilibrium.from_temperatures(n_a, n_b, 500.0, 250.0, QUANTUM)
        n_steps = n_frames * steps_per_frame
        result = equilibrium.simulate_energy_exchange(state, n_steps, rng)
        sample = slice(steps_per_frame - 1, None, steps_per_frame)
        frame_steps = result.steps[sample]
        delta_t0 = state.temperature_a - state.temperature_b
        gap = (result.temperature_a - result.temperature_b)[sample] / delta_t0
        predicted = equilibrium.predicted_relaxation(state, frame_steps) / delta_t0
        traces.append((frame_steps, gap, predicted))

    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.0), dpi=DPI, sharey=True)
    lines = []
    for ax, (n_a, n_b), (steps, _, predicted) in zip(axes, sizes, traces, strict=True):
        (line,) = ax.plot([], [], lw=1.0, color="#2563eb")
        ax.plot(steps, predicted, lw=1.2, ls="--", color="crimson")
        ax.set_xlim(0, float(steps[-1]))
        ax.set_ylim(-0.3, 1.1)
        ax.set_title(f"N = {n_a + n_b}")
        ax.set_xlabel("step")
        lines.append(line)
    axes[0].set_ylabel("(T_A - T_B) / (T_A0 - T_B0)")
    fig.tight_layout()

    def update(frame: int):
        for line, (steps, gap, _) in zip(lines, traces, strict=True):
            line.set_data(steps[:frame], gap[:frame])
        return lines

    save(
        FuncAnimation(fig, update, frames=n_frames, blit=False),
        fig,
        "equilibrium-fluctuations",
    )
    plt.close(fig)


def main() -> None:
    render_relaxation()
    render_fluctuations()


if __name__ == "__main__":
    main()
