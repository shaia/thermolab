"""Render the demonstration animations for module 03 (probability and emergence).

Animations are produced from `thermolab` itself, so what a student watches is the same model
they can run and read — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose.

Run:  uv run python media/render/render_random_walks.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save  # noqa: E402
from thermolab import sampling  # noqa: E402

# One palette across the three animations, so a colour means the same thing in all of them.
CLOUD = "#2563eb"
THEORY = "crimson"
BROKEN = "#7c3aed"
STEP_COLOURS = {"pm1": "#2563eb", "uniform": "#0d9488", "heavy": "#d97706"}


def render_walker_cloud(n_steps: int = 400, n_frames: int = 240) -> None:
    """One path alone, then four thousand of them, with the live position histogram.

    The two acts are the whole argument. Act one is a single walker: it wanders, and knowing
    where it is tells you nothing about where it will be. Act two replays the same clock with
    the ensemble, and a shape appears that was not in any individual path.
    """
    rng = np.random.default_rng(3)
    n_walkers, n_drawn = 4000, 120
    trajectories = sampling.random_walk(n_walkers, n_steps, rng)

    solo_frames = n_frames // 3
    cloud_frames = n_frames - solo_frames
    # Act two opens at a cloud that is already a few dozen steps old. Before that the walkers
    # occupy one or two bins and the density spikes off the panel, which would force the
    # histogram axis to be scaled for a frame nobody is looking at.
    t_start = max(n_steps // 12, 1)
    limit = 4.2 * np.sqrt(n_steps)
    edges_span = (-limit, limit)
    times = np.arange(n_steps + 1)

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(9.0, 3.8), dpi=DPI, sharey=True, width_ratios=[2.4, 1.0]
    )

    faint = [left.plot([], [], lw=0.7, color=CLOUD, alpha=0.10)[0] for _ in range(n_drawn)]
    (solo,) = left.plot([], [], lw=1.6, color="#0f172a")
    left.set_xlim(0, n_steps)
    left.set_ylim(-limit, limit)
    left.set_xlabel("steps")
    left.set_ylabel("position")
    left.axhline(0.0, color="#94a3b8", lw=0.8, ls=":")

    centres, _ = sampling.walker_histogram(trajectories[:, -1], n_bins=61, span=edges_span)
    bars = right.barh(centres, np.zeros_like(centres), height=(centres[1] - centres[0]),
                      color=CLOUD, alpha=0.55)
    (overlay,) = right.plot([], [], lw=1.6, color=THEORY)
    # Fixed at the density the cloud reaches early in act two, so the bars visibly flatten and
    # widen as sqrt(t) instead of being silently rescaled to fill the panel every frame.
    right.set_xlim(0, 1.35 * sampling.gaussian_limit(np.array([0.0]), t_start)[0])
    right.set_xlabel("density")
    right.tick_params(labelleft=False)
    fig.tight_layout()

    def update(frame: int):
        if frame < solo_frames:
            t = int(round((frame + 1) / solo_frames * n_steps))
            solo.set_data(times[: t + 1], trajectories[0, : t + 1])
            for line in faint:
                line.set_data([], [])
            for bar in bars:
                bar.set_width(0.0)
            overlay.set_data([], [])
            return [solo, overlay, *faint, *bars]

        progress = (frame - solo_frames + 1) / cloud_frames
        t = t_start + int(round(progress * (n_steps - t_start)))
        solo.set_data(times[: t + 1], trajectories[0, : t + 1])
        for index, line in enumerate(faint):
            line.set_data(times[: t + 1], trajectories[index + 1, : t + 1])

        _, density = sampling.walker_histogram(trajectories[:, t], n_bins=61, span=edges_span)
        for bar, width in zip(bars, density, strict=True):
            bar.set_width(width)
        overlay.set_data(sampling.gaussian_limit(centres, t), centres)
        return [solo, overlay, *faint, *bars]

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "walker-cloud")
    plt.close(fig)


def render_sqrt_spread(n_steps: int = 900, n_frames: int = 200) -> None:
    """The width climbing the sqrt(t) curve while the ensemble mean goes nowhere.

    Drift and spread are drawn on the same axes on purpose: the cloud is widening and the
    average is not moving, which is the pair of facts the `spread-means-drift` misconception
    fuses into one.
    """
    rng = np.random.default_rng(11)
    n_walkers = 20_000
    trajectories = sampling.random_walk(n_walkers, n_steps, rng)

    times = np.arange(n_steps + 1)
    spread = sampling.walker_spread(trajectories)
    mean = trajectories.mean(axis=0)
    predicted = sampling.step_distribution("pm1").std * np.sqrt(times)
    standard_error = np.sqrt(times / n_walkers)

    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=DPI)
    ax.plot(times, predicted, color=THEORY, ls="--", lw=1.3)
    ax.fill_between(times, -3.0 * standard_error, 3.0 * standard_error,
                    color="#94a3b8", alpha=0.35, lw=0)
    (measured,) = ax.plot([], [], color=CLOUD, lw=1.8)
    (average,) = ax.plot([], [], color="#0f172a", lw=1.4)
    ax.axhline(0.0, color="#94a3b8", lw=0.8, ls=":")
    ax.set_xlim(0, n_steps)
    ax.set_ylim(-6.0, 1.15 * predicted[-1])
    ax.set_xlabel("steps")
    ax.set_ylabel("position (spread and mean)")
    fig.tight_layout()

    def update(frame: int):
        t = max(int(round((frame + 1) / n_frames * n_steps)), 1)
        measured.set_data(times[: t + 1], spread[: t + 1])
        average.set_data(times[: t + 1], mean[: t + 1])
        return measured, average

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "sqrt-spread")
    plt.close(fig)


def render_clt_collapse(n_samples: int = 8000, frames_per_step: int = 5) -> None:
    """Three step distributions collapsing onto one curve — and one refusing to.

    The three independent-step families start wildly different and end indistinguishable. The
    persistent walk is standardized by the same independent-step formula and stays visibly too
    wide however many terms are added, which is what "independence is a hypothesis, not a
    decoration" looks like on an axis.
    """
    rng = np.random.default_rng(19)
    span = (-4.0, 4.0)
    n_bins = 49

    term_counts = sorted({int(round(1.22**k)) for k in range(int(np.log(600) / np.log(1.22)) + 1)})
    curves: dict[str, list[np.ndarray]] = {name: [] for name in (*STEP_COLOURS, "correlated")}
    centres = np.array([])
    for n_terms in term_counts:
        for name in STEP_COLOURS:
            standardized = sampling.clt_sum_distribution(n_terms, n_samples, rng, step=name)
            centres, density = sampling.walker_histogram(standardized, n_bins=n_bins, span=span)
            curves[name].append(density)
        persistent = sampling.correlated_walk(n_samples, n_terms, 0.9, rng)[:, -1]
        _, density = sampling.walker_histogram(
            persistent / np.sqrt(n_terms), n_bins=n_bins, span=span
        )
        curves["correlated"].append(density)

    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=DPI)
    gaussian = np.exp(-0.5 * centres**2) / np.sqrt(2.0 * np.pi)
    ax.plot(centres, gaussian, color=THEORY, ls="--", lw=1.6)

    lines = {
        name: ax.plot([], [], lw=1.5, color=colour, alpha=0.9)[0]
        for name, colour in STEP_COLOURS.items()
    }
    lines["correlated"] = ax.plot([], [], lw=1.8, color=BROKEN, ls=(0, (4, 2)))[0]
    ax.set_xlim(*span)
    ax.set_ylim(0, 0.72)
    ax.set_xlabel("standardized sum  $(S_n - n\\mu_1) / (\\sigma_1 \\sqrt{n})$")
    ax.set_ylabel("density")
    fig.tight_layout()

    def update(frame: int):
        index = min(frame // frames_per_step, len(term_counts) - 1)
        for name, line in lines.items():
            line.set_data(centres, curves[name][index])
        return list(lines.values())

    save(
        FuncAnimation(fig, update, frames=len(term_counts) * frames_per_step, blit=False),
        fig,
        "clt-collapse",
    )
    plt.close(fig)


def main() -> None:
    render_walker_cloud()
    render_sqrt_spread()
    render_clt_collapse()


if __name__ == "__main__":
    main()
