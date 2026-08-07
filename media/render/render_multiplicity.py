"""Render the demonstration animations for module 08 (entropy and multiplicity).

Animations are produced from `thermolab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is animated GIF via matplotlib's Pillow writer, which needs no ffmpeg and plays
everywhere. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_multiplicity.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

from thermolab import multiplicity  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LANGUAGES = ("en", "he")


def output_paths(name: str) -> list[Path]:
    """The same file in each language project — MyST resolves images inside its own tree."""
    return [ROOT / "content" / lang / "media" / f"{name}.gif" for lang in LANGUAGES]


def save(animation: FuncAnimation, name: str, fps: int = 20) -> None:
    targets = output_paths(name)
    first = targets[0]
    first.parent.mkdir(parents=True, exist_ok=True)
    animation.save(first, writer=PillowWriter(fps=fps))
    for other in targets[1:]:
        other.parent.mkdir(parents=True, exist_ok=True)
        other.write_bytes(first.read_bytes())
    print(f"[render] {name}.gif -> {', '.join(str(p.relative_to(ROOT)) for p in targets)}")


def render_two_box_relaxation(n_objects: int = 200, n_frames: int = 150,
                               steps_per_frame: int = 6) -> None:
    """The Ehrenfest urn: occupancy starting fully on one side, settling near the even split.

    Left: the two boxes' populations as a live bar chart. Right: the occupancy trace of the
    first box against step number, with a dashed line at the even split.
    """
    rng = np.random.default_rng(12)
    n_steps = n_frames * steps_per_frame
    occupancy = multiplicity.sample_two_box(n_objects, n_steps, rng)
    sampled = occupancy[steps_per_frame - 1 :: steps_per_frame][:n_frames]
    trace = np.concatenate([[n_objects], sampled])
    steps_axis = np.arange(trace.size) * steps_per_frame

    fig, (left, right) = plt.subplots(1, 2, figsize=(8.5, 3.6), dpi=110)

    bars = left.bar(["A", "B"], [n_objects, 0], color=["#2563eb", "#94a3b8"])
    left.set_ylim(0, n_objects)
    left.set_ylabel("occupancy")
    left.set_title(f"N = {n_objects}")

    (line,) = right.plot([], [], lw=1.4, color="#2563eb")
    right.axhline(n_objects / 2.0, color="crimson", ls="--", lw=1.2)
    right.set_xlim(0, steps_axis[-1])
    right.set_ylim(0, n_objects)
    right.set_xlabel("step")
    right.set_ylabel("box A occupancy")
    right.set_title("relaxation to the even split")
    fig.tight_layout()

    def update(frame: int):
        n_a = int(trace[frame])
        bars[0].set_height(n_a)
        bars[1].set_height(n_objects - n_a)
        line.set_data(steps_axis[: frame + 1], trace[: frame + 1])
        return (*bars, line)

    save(
        FuncAnimation(fig, update, frames=trace.size, blit=False, interval=50),
        "multiplicity-two-box",
    )
    plt.close(fig)


def render_peak_sharpens(n_frames: int = 90) -> None:
    """The relative multiplicity distribution narrowing as N grows.

    Each frame plots Omega(N,n)/Omega(N,N/2) against the fractional occupancy n/N for one
    value of N; the curve keeps the same peak height (1, by construction) but its width shrinks
    as N grows, which is the visual form of the N^(-1/2) law derived on the module page.
    """
    raw = np.round(np.geomspace(4, 400, n_frames * 2)).astype(int)
    raw = raw[raw % 2 == 0]
    n_values = np.unique(raw)

    frames_data = []
    for n in n_values:
        counts = np.arange(0, n + 1)
        log_omega = multiplicity.log_multiplicity_array(int(n), counts)
        peak = log_omega[n // 2]
        relative = np.exp(log_omega - peak)
        frames_data.append((counts / n, relative))

    fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=110)
    (line,) = ax.plot([], [], lw=1.6, color="#2563eb")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("n / N")
    ax.set_ylabel(r"$\Omega(N,n)/\Omega(N,N/2)$")
    title = ax.set_title("")
    fig.tight_layout()

    def update(frame: int):
        x, relative = frames_data[frame]
        line.set_data(x, relative)
        title.set_text(f"N = {int(n_values[frame])}")
        return line, title

    save(
        FuncAnimation(fig, update, frames=len(n_values), blit=False, interval=80),
        "multiplicity-peak",
    )
    plt.close(fig)


def main() -> None:
    render_two_box_relaxation()
    render_peak_sharpens()


if __name__ == "__main__":
    main()
