"""Render the demonstrations for module 15 (the Ising model).

Three animations and one still, all driven by `thermolab.ising`, so what a student watches is
the code they can run. Temperatures are k_B T / J and fields h / J (the module's reduced
units); spins up are drawn dark, spins down light.

    ising-quench.mp4        a hot (random) 128 x 128 lattice dropped to T = 1.5, below T_c:
                            domains of each sign form and coarsen, and |m| climbs while the
                            energy per spin falls, against a logarithmic sweep axis
    ising-hysteresis.mp4    a 64 x 64 lattice at T = 1.5 beside its m-h curve while the field
                            is swept from +1 to -1 and back: the magnetization holds its sign
                            past h = 0 and reverses abruptly, tracing a loop; the closed grey
                            curve behind it is the same sweep at T = 3.0, above T_c
    ising-tc-sweep.mp4      three lattices, L = 16, 32 and 64 drawn at one size, cooled from
                            T = 3.5 to 1.5 while <|m|>(T) is built point by point for each, with
                            Onsager's exact curve for the infinite lattice behind them
    ising-finite-size.png   the quantitative version: <|m|>, chi' and tau against T for
                            L = 8, 16, 32 and 64, with T_c marked

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py` for the
format and its constraints.

Run:  uv run python media/render/render_ising.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402

from _common import DPI, save, save_still  # noqa: E402
from thermolab import ising  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER, GREEN = ("#dc2626", "#2563eb", "#111827", "#94a3b8",
                                        "#d97706", "#059669")
SPINS = ListedColormap(["#e0f2fe", "#1e3a8a"])  # down light, up dark
SIZE_COLOURS = {8: GREEN, 16: AMBER, 32: RED, 64: BLUE}
T_C = ising.onsager_tc()


def _lattice_axis(ax, lattice, title=None):
    image = ax.imshow(lattice, cmap=SPINS, vmin=-1, vmax=1, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=11)
    return image


def render_quench() -> None:
    """Hot start, quenched below T_c: coarsening domains, against log sweeps."""
    temperature, size = 1.5, 128
    # Seed 1 shows domains competing for ~2000 sweeps before one sign wins. About one quench
    # in four at this size instead freezes into two straight stripes, one of each sign,
    # which survive far longer than this window; the caption says so.
    rng = np.random.default_rng(1)
    state = ising.random_state(size, rng)
    # Frame times grow geometrically: early frames are one sweep apart, late ones hundreds.
    times = np.unique(np.round(np.geomspace(1, 3000, 240)).astype(int))
    frames, m_trace, e_trace = [state.lattice.copy()], [state.m], [state.e]
    done = 0
    for t in times:
        for _ in range(t - done):
            state = ising.metropolis_sweep(state, temperature, rng)
        done = t
        frames.append(state.lattice.copy())
        m_trace.append(state.m)
        e_trace.append(state.e)
    times = np.concatenate([[0.7], times])  # sweep 0 placed just left of 1 on the log axis
    m_trace, e_trace = np.abs(np.array(m_trace)), np.array(e_trace)
    m_eq = float(ising.onsager_magnetization(temperature))

    fig = plt.figure(figsize=(9.6, 4.6), dpi=DPI)
    grid = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.15], hspace=0.35, wspace=0.25)
    ax_lat = fig.add_subplot(grid[:, 0])
    ax_m = fig.add_subplot(grid[0, 1])
    ax_e = fig.add_subplot(grid[1, 1], sharex=ax_m)
    image = _lattice_axis(ax_lat, frames[0])
    label = ax_lat.text(0.02, 1.02, "", transform=ax_lat.transAxes, fontsize=11)
    for ax in (ax_m, ax_e):
        ax.set_xscale("log")
        ax.set_xlim(0.6, 4000)
        ax.spines[["top", "right"]].set_visible(False)
    ax_m.set_ylim(0, 1.05)
    ax_m.set_ylabel(r"$|m|$")
    ax_m.axhline(m_eq, color=GREY, ls="--", lw=1.0)
    ax_e.set_ylim(-2.05, 0.1)
    ax_e.set_ylabel(r"$E/(NJ)$")
    ax_e.set_xlabel(r"$t$")
    (line_m,) = ax_m.plot([], [], color=BLUE, lw=1.8)
    (line_e,) = ax_e.plot([], [], color=RED, lw=1.8)
    plt.setp(ax_m.get_xticklabels(), visible=False)

    def draw(i):
        image.set_data(frames[i])
        line_m.set_data(times[: i + 1], m_trace[: i + 1])
        line_e.set_data(times[: i + 1], e_trace[: i + 1])
        label.set_text(rf"$k_BT/J = {temperature}$   $t = {int(times[i]) if i else 0}$")
        return image, line_m, line_e, label

    hold = [len(frames) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=list(range(len(frames))) + hold, blit=False)
    save(animation, fig, "ising-quench")
    plt.close(fig)
    print(f"[quench] final m = {m_trace[-1]:.3f}, e = {e_trace[-1]:.3f}; equilibrium "
          f"|m| = {m_eq:.3f}")


def render_hysteresis() -> None:
    """A field swept below T_c, with the above-T_c curve behind it for contrast."""
    size, cold, hot, per_step = 64, 1.5, 3.0, 20
    fields = ising.hysteresis_fields(1.0, 41)
    rng = np.random.default_rng(3)
    h_hot, m_hot, _ = ising.hysteresis_sweep(ising.aligned_state(size), hot, fields,
                                             per_step, rng)

    state = ising.with_field(ising.aligned_state(size), fields[0])
    _, _, state = ising.simulate(state, cold, 200, rng, burn_in=0, thin=200)
    frames, field_at, m_at = [], [], []
    sub = 4  # sweeps per frame
    for value in fields:
        state = ising.with_field(state, float(value))
        for _ in range(per_step // sub):
            _, _, state = ising.simulate(state, cold, sub, rng, burn_in=0, thin=sub)
            frames.append(state.lattice.copy())
            field_at.append(value)
            m_at.append(state.m)
    field_at, m_at = np.array(field_at), np.array(m_at)

    fig, (ax_lat, ax_loop) = plt.subplots(1, 2, figsize=(9.6, 4.6), dpi=DPI,
                                          gridspec_kw={"width_ratios": [1.0, 1.15]})
    image = _lattice_axis(ax_lat, frames[0])
    label = ax_lat.text(0.02, 1.02, "", transform=ax_lat.transAxes, fontsize=11)
    ax_loop.plot(h_hot, m_hot, color=GREY, lw=1.5)
    ax_loop.axhline(0, color=BLACK, lw=0.6)
    ax_loop.axvline(0, color=BLACK, lw=0.6)
    ax_loop.set_xlim(-1.1, 1.1)
    ax_loop.set_ylim(-1.1, 1.1)
    ax_loop.set_xlabel(r"$h/J$")
    ax_loop.set_ylabel(r"$m$")
    ax_loop.spines[["top", "right"]].set_visible(False)
    (trail,) = ax_loop.plot([], [], color=BLUE, lw=1.8)
    (dot,) = ax_loop.plot([], [], "o", color=RED, ms=7)

    def draw(i):
        image.set_data(frames[i])
        trail.set_data(field_at[: i + 1], m_at[: i + 1])
        dot.set_data([field_at[i]], [m_at[i]])
        label.set_text(rf"$k_BT/J = {cold}$   $h/J = {field_at[i]:+.2f}$")
        return image, trail, dot, label

    hold = [len(frames) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=list(range(len(frames))) + hold, blit=False)
    save(animation, fig, "ising-hysteresis")
    plt.close(fig)
    zero = np.argmin(np.abs(field_at[: len(field_at) // 2]))
    print(f"[hysteresis] cold loop area {ising.loop_area(field_at, m_at):.2f}, hot "
          f"{ising.loop_area(h_hot, m_hot):.3f}; m at h = 0 on the way down {m_at[zero]:.2f}")


def render_tc_sweep() -> None:
    """Three lattice sizes cooled through T_c, with <|m|>(T) built as they go."""
    sizes = (16, 32, 64)
    temperatures = np.round(np.linspace(3.5, 1.5, 41), 4)
    shown_per_t, sub, measure = 6, 10, 1500
    rng = np.random.default_rng(4)
    states = {s: ising.random_state(s, rng) for s in sizes}
    snaps = {s: [] for s in sizes}
    curve = {s: [] for s in sizes}
    for t in temperatures:
        for s in sizes:
            state = states[s]
            for _ in range(shown_per_t):
                _, _, state = ising.simulate(state, float(t), sub, rng, burn_in=0, thin=sub)
                snaps[s].append(state.lattice.copy())
            m, _, state = ising.simulate(state, float(t), measure, rng, burn_in=300)
            curve[s].append(np.abs(m).mean())
            states[s] = state
    t_fine = np.linspace(1.5, 3.5, 400)

    fig = plt.figure(figsize=(9.6, 6.4), dpi=DPI)
    grid = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.05], hspace=0.3, wspace=0.08)
    images = {}
    for k, s in enumerate(sizes):
        ax = fig.add_subplot(grid[0, k])
        images[s] = _lattice_axis(ax, snaps[s][0], title=rf"$L = {s}$")
        for spine in ax.spines.values():
            spine.set_edgecolor(SIZE_COLOURS[s])
            spine.set_linewidth(2.0)
    ax = fig.add_subplot(grid[1, :])
    ax.plot(t_fine, ising.onsager_magnetization(t_fine), color=BLACK, lw=1.4)
    ax.axvline(T_C, color=GREY, ls="--", lw=1.0)
    ax.text(T_C + 0.02, 1.0, r"$T_c$", fontsize=11, color=GREY)
    ax.set_xlim(3.55, 1.45)  # cooling runs left to right
    ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"$k_BT/J$")
    ax.set_ylabel(r"$\langle |m| \rangle$")
    ax.spines[["top", "right"]].set_visible(False)
    lines = {s: ax.plot([], [], "o-", color=SIZE_COLOURS[s], ms=4, lw=1.4)[0] for s in sizes}
    (marker,) = ax.plot([], [], "|", color=BLACK, ms=18, mew=2)

    def draw(i):
        k = i // shown_per_t
        for s in sizes:
            images[s].set_data(snaps[s][i])
            lines[s].set_data(temperatures[: k + 1], curve[s][: k + 1])
        marker.set_data([temperatures[k]], [0.02])
        return (*images.values(), *lines.values(), marker)

    n = len(temperatures) * shown_per_t
    hold = [n - 1] * 45
    animation = FuncAnimation(fig, draw, frames=list(range(n)) + hold, blit=False)
    save(animation, fig, "ising-tc-sweep", fps=20)
    plt.close(fig)
    at = int(np.argmin(np.abs(temperatures - 2.5)))
    print("[tc-sweep] <|m|> at T = 2.5: " + ", ".join(
        f"L={s}: {curve[s][at]:.3f}" for s in sizes))


def render_finite_size() -> None:
    """<|m|>, chi' and tau against T for four sizes: rounding, peaks, slowing down."""
    sizes = (8, 16, 32, 64)
    temperatures = np.round(np.concatenate([np.linspace(1.6, 2.1, 6),
                                            np.linspace(2.15, 2.75, 21),
                                            np.linspace(2.9, 3.5, 4)]), 4)
    sweeps = {8: 20000, 16: 12000, 32: 8000, 64: 5000}
    data = {}
    for s in sizes:
        rng = np.random.default_rng(100 + s)
        scan = ising.temperature_scan(s, temperatures[::-1], sweeps[s], rng,
                                      burn_in=1000)[::-1]
        data[s] = scan
        peak = temperatures[np.argmax([r.susceptibility for r in scan])]
        print(f"[finite-size] L = {s}: chi' peak at T = {peak:.3f}")
    t_fine = np.linspace(1.6, 3.5, 400)

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.9), dpi=DPI)
    ax_m, ax_chi, ax_tau = axes
    ax_m.plot(t_fine, ising.onsager_magnetization(t_fine), color=BLACK, lw=1.2)
    for s in sizes:
        scan = data[s]
        colour = SIZE_COLOURS[s]
        ax_m.errorbar(temperatures, [r.abs_magnetization for r in scan],
                      yerr=[r.abs_magnetization_error for r in scan], color=colour, ms=3,
                      fmt="o-", lw=1.0, capsize=0)
        ax_chi.plot(temperatures, [r.susceptibility for r in scan], "o-", color=colour,
                    ms=3, lw=1.0, label=rf"$L={s}$")
        ax_tau.plot(temperatures, [r.tau_abs_magnetization for r in scan], "o-",
                    color=colour, ms=3, lw=1.0)
    ax_m.set_ylabel(r"$\langle |m| \rangle$")
    ax_chi.set_ylabel(r"$\chi' J$")
    ax_tau.set_ylabel(r"$\tau_{|m|}$")
    ax_tau.set_yscale("log")
    ax_chi.legend(frameon=False, fontsize=9)
    for ax in axes:
        ax.axvline(T_C, color=GREY, ls="--", lw=1.0)
        ax.set_xlabel(r"$k_BT/J$")
        ax.set_xlim(1.55, 3.55)
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_still(fig, "ising-finite-size")
    plt.close(fig)


def main() -> None:
    render_quench()
    render_hysteresis()
    render_tc_sweep()
    render_finite_size()


if __name__ == "__main__":
    main()
