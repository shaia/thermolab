"""Render the demonstrations for module 09 (the fundamental relation).

Three animations and one still, all built from `thermolab.fundamental` and
`thermolab.equilibrium`, so what a student watches is the model they can read and run:

    fundamental-partition-sweep.mp4     S_A, S_B and S_A + S_B along the energy partition, with
                                        the two tangents meeting in slope at the peak
    fundamental-constraint-release.mp4  the divided gas's total entropy over (energy share,
                                        volume share); the equilibrium point moves as the wall
                                        first conducts heat, then slides
    fundamental-ledger.mp4              module 01's relaxation with its exact entropy ledger
    fundamental-concavity.png           the chord picture behind stability, concave vs convex

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py` for the
format and its constraints.

Run:  uv run python media/render/render_fundamental.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save, save_still  # noqa: E402
from thermolab import equilibrium, fundamental  # noqa: E402
from thermolab.constants import AMU, K_B  # noqa: E402

RED, BLUE, BLACK, GREY = "#dc2626", "#2563eb", "#111827", "#94a3b8"
QUANTUM = 5.0 * K_B


def render_partition_sweep(n_frames: int = 240) -> None:
    """S_A(U_A), S_B(U - U_A) and their sum, with tangents sliding along both curves.

    Solid B has ten times A's oscillators, so the peak sits at U_A/U = 1/11 -- the page's
    answer to "equal energies?". The tangent segments are drawn with the *numerical* slope of
    each relation at the current partition, which is the module's claim: the peak is where the
    two slopes are equal.
    """
    solid = fundamental.einstein_solid(QUANTUM)
    n_a, n_b = 40.0, 400.0
    total = 5.0 * (n_a + n_b) * QUANTUM
    composite = fundamental.Composite(solid, solid, fundamental.Part(0.5 * total, 1.0, n_a),
                                      fundamental.Part(0.5 * total, 1.0, n_b))
    u_a, s_a, s_b = composite.energy_scan(n_points=801, margin=0.004)
    share = u_a / total
    s_a, s_b = s_a / K_B, s_b / K_B
    s_tot = s_a + s_b
    peak_share = composite.released("energy").a.energy / total

    # Sweep out and back so the loop is seamless; ease in and out at the ends.
    phase = 0.5 - 0.5 * np.cos(np.linspace(0.0, 2.0 * np.pi, n_frames, endpoint=False))
    sweep = 0.02 + 0.26 * phase

    # Top: the total relative to its maximum. The raw values sit near 1200 k_B, where a peak
    # of a few tens of k_B is invisible; subtracting the maximum is what makes it a peak.
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(6.6, 5.6), dpi=DPI, sharex=True)
    relative = s_tot - s_tot.max()
    top.plot(share, relative, color=BLACK, lw=2.2)
    top.axvline(peak_share, color=GREY, ls=":", lw=1.0)
    top.set_xlim(0.0, 0.3)
    top.set_ylim(-45.0, 5.0)
    top.set_ylabel(r"$(S_A + S_B - S_{\max}) / k_{\mathrm{B}}$")
    (dot,) = top.plot([], [], "o", color=BLACK, ms=8)

    # Bottom: the two slopes, dS_A/dU_A and dS_B/dU_B, in 1/K. They cross under the peak.
    inv_t_a = np.gradient(s_a, u_a / K_B)
    inv_t_b = -np.gradient(s_b, u_a / K_B)
    bottom.plot(share, inv_t_a, color=RED, lw=2.0, label=r"$\partial S_A/\partial U_A$")
    bottom.plot(share, inv_t_b, color=BLUE, lw=2.0, label=r"$\partial S_B/\partial U_B$")
    bottom.axvline(peak_share, color=GREY, ls=":", lw=1.0)
    peak_slope = float(np.interp(peak_share, share, inv_t_b))
    bottom.set_ylim(0.0, 2.5 * peak_slope)
    bottom.set_xlabel(r"$U_A / U$")
    bottom.set_ylabel(r"$1/T$ (K$^{-1}$)")
    bottom.legend(loc="upper right", frameon=False)
    (dot_a,) = bottom.plot([], [], "o", color=RED, ms=8)
    (dot_b,) = bottom.plot([], [], "o", color=BLUE, ms=8)
    (gap,) = bottom.plot([], [], color=BLACK, lw=1.4, ls=":")
    fig.tight_layout()

    def update(frame: int):
        i = int(np.clip(np.searchsorted(share, sweep[frame]), 0, share.size - 1))
        dot.set_data([share[i]], [relative[i]])
        dot_a.set_data([share[i]], [inv_t_a[i]])
        dot_b.set_data([share[i]], [inv_t_b[i]])
        gap.set_data([share[i], share[i]], [inv_t_a[i], inv_t_b[i]])
        return dot, dot_a, dot_b, gap

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig,
         "fundamental-partition-sweep")
    plt.close(fig)


def render_constraint_release(n_frames: int = 270) -> None:
    """The divided gas's S_total over (energy share, volume share), and the moving maximum.

    Side A holds a third of the atoms. The dot starts off-peak, moves horizontally when the
    wall conducts heat (energy may move, volume may not) and stops on the equal-temperature
    line, then climbs that line to the summit when the wall may also slide. The two
    intermediate equilibria are computed by `Composite.released`, not placed by hand.
    """
    gas = fundamental.monatomic_ideal_gas(39.948 * AMU)
    n_a, n_b = 1e20, 2e20
    u_total = 1.5 * (n_a + n_b) * K_B * 300.0
    v_total = 3e-3
    start = fundamental.Composite(
        gas, gas,
        fundamental.Part(0.62 * u_total, 0.12 * v_total, n_a),
        fundamental.Part(0.38 * u_total, 0.88 * v_total, n_b),
    )
    diathermal = start.released("energy")
    sliding = diathermal.released("energy", "volume")

    x = np.linspace(0.03, 0.80, 220)
    y = np.linspace(0.03, 0.80, 220)
    xx, yy = np.meshgrid(x, y)
    # Per particle: at 3e20 atoms the raw differences are ~1e19 k_B, and any fixed set of
    # contour levels either crowds the summit or paints the whole map one colour.
    s_total = (gas(xx * u_total, yy * v_total, n_a)
               + gas((1 - xx) * u_total, (1 - yy) * v_total, n_b)) / (K_B * (n_a + n_b))
    s_total -= s_total.max()

    def shares(c: fundamental.Composite) -> tuple[float, float]:
        return c.a.energy / u_total, c.a.volume / v_total

    p0, p1, p2 = shares(start), shares(diathermal), shares(sliding)

    fig, ax = plt.subplots(figsize=(5.8, 5.2), dpi=DPI)
    levels = -np.geomspace(2e-3, 1.5, 16)[::-1]
    ax.contourf(xx, yy, s_total, levels=np.r_[levels, 0.0], cmap="viridis", extend="min")
    ax.contour(xx, yy, s_total, levels=levels, colors="white", linewidths=0.4, alpha=0.5)
    ax.axvline(n_a / (n_a + n_b), color="white", ls="--", lw=1.2)
    ax.set_xlabel(r"$U_A / U$")
    ax.set_ylabel(r"$V_A / V$")
    ax.set_aspect("equal")
    (trail,) = ax.plot([], [], color="white", lw=1.6)
    (dot,) = ax.plot([], [], "o", color=RED, ms=10, mec="white", mew=1.5)
    fig.tight_layout()

    hold, move = 45, 70  # frames: pause, travel, pause, travel, pause
    path = [p0] * hold
    path += [tuple(np.array(p0) + (np.array(p1) - np.array(p0)) * s)
             for s in 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, move))]
    path += [p1] * hold
    path += [tuple(np.array(p1) + (np.array(p2) - np.array(p1)) * s)
             for s in 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, move))]
    path += [p2] * (n_frames - len(path))
    path_arr = np.array(path)

    def update(frame: int):
        trail.set_data(path_arr[: frame + 1, 0], path_arr[: frame + 1, 1])
        dot.set_data([path_arr[frame, 0]], [path_arr[frame, 1]])
        return trail, dot

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig,
         "fundamental-constraint-release")
    plt.close(fig)


def render_ledger(n_frames: int = 240) -> None:
    """Module 01's relaxation above, its exact total-entropy ledger below, on one time axis."""
    state = equilibrium.from_temperatures(300, 100, 500.0, 250.0, QUANTUM)
    n_steps = 6 * state.total_quanta
    result = equilibrium.simulate_energy_exchange(state, n_steps, np.random.default_rng(7))
    ledger = equilibrium.entropy_produced(result) / K_B

    total = state.total_quanta
    q = np.arange(total + 1)
    exact = (equilibrium.einstein_log_multiplicity(q, state.n_a)
             + equilibrium.einstein_log_multiplicity(total - q, state.n_b))
    ceiling = float(exact.max() - exact[state.q_a])

    stride = n_steps // n_frames
    sample = slice(stride - 1, None, stride)
    steps = result.steps[sample] / 1e3
    t_a = result.temperature_a[sample]
    t_b = result.temperature_b[sample]
    led = ledger[sample]

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(6.6, 5.4), dpi=DPI, sharex=True)
    (line_a,) = top.plot([], [], color=RED, lw=1.6, label=r"$T_A$")
    (line_b,) = top.plot([], [], color=BLUE, lw=1.6, label=r"$T_B$")
    top.set_ylim(220, 530)
    top.set_ylabel(r"$T$ (K)")
    top.legend(loc="center right", frameon=False)
    (line_s,) = bottom.plot([], [], color=BLACK, lw=1.6)
    bottom.axhline(ceiling, color=GREY, ls="--", lw=1.2)
    bottom.set_xlim(0, float(steps[-1]))
    bottom.set_ylim(-0.5, 1.12 * ceiling)
    bottom.set_xlabel(r"step ($\times 10^3$)")
    bottom.set_ylabel(r"$\Delta S_{\mathrm{tot}} / k_{\mathrm{B}}$")
    fig.tight_layout()

    def update(frame: int):
        line_a.set_data(steps[: frame + 1], t_a[: frame + 1])
        line_b.set_data(steps[: frame + 1], t_b[: frame + 1])
        line_s.set_data(steps[: frame + 1], led[: frame + 1])
        return line_a, line_b, line_s

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "fundamental-ledger")
    plt.close(fig)


def render_concavity() -> None:
    """The chord picture: a fluctuation +-delta about U, on a concave and on a convex S(U)."""
    u = np.linspace(0.2, 1.8, 200)
    concave = np.log(u) + 1.0
    convex = 0.55 * (u - 0.2) ** 2 + 0.3
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4), dpi=DPI)
    for ax, curve, label in zip(axes, (concave, convex), ("(a)", "(b)"), strict=True):
        ax.plot(u, curve, color=BLACK, lw=2.2)
        centre, delta = 1.0, 0.6
        ends = np.array([centre - delta, centre + delta])
        values = np.interp(ends, u, curve)
        mid_curve = float(np.interp(centre, u, curve))
        ax.plot(ends, values, color=BLUE, lw=1.6)
        ax.plot(ends, values, "o", color=BLUE, ms=6)
        ax.plot([centre], [mid_curve], "o", color=BLACK, ms=7)
        ax.plot([centre], [values.mean()], "s", color=RED, ms=7)
        ax.vlines(centre, min(mid_curve, values.mean()), max(mid_curve, values.mean()),
                  colors=RED, linestyles=":", lw=1.4)
        ax.set_xticks([centre - delta, centre, centre + delta],
                      [r"$U-\delta$", r"$U$", r"$U+\delta$"])
        ax.set_yticks([])
        ax.set_ylabel(r"$S$")
        ax.set_title(label, loc="left")
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.tight_layout()
    save_still(fig, "fundamental-concavity")
    plt.close(fig)


def main() -> None:
    render_concavity()
    render_partition_sweep()
    render_constraint_release()
    render_ledger()


if __name__ == "__main__":
    main()
