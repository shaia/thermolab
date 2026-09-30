"""Render the demonstrations for module 12 (partition functions).

Three animations and two stills, all built from `thermolab.partition` (and, for the overlay,
module 01's `thermolab.equilibrium`), so what a student watches is the code they can run:

    partition-reconstruction.mp4     a harmonic oscillator's U, S, F and C against temperature:
                                     dots computed from ln Z alone by central differences in
                                     beta, whose step shrinks until they sit on the exact curves
    partition-spin-dome.mp4          the paramagnet's S(U) dome with a tangent sliding over it,
                                     and the tangent's slope beta changing sign at the top
    partition-freeze-out.mp4         an oscillator cooling: its level occupations collapse onto
                                     the ground level while C falls off the equipartition plateau
    partition-paramagnet.png         (a) M against mu B / k_B T with the Curie line and
                                     saturation; (b) the Schottky peak of C against temperature
    partition-einstein-overlay.png   module 01's simulated endpoints read two ways -- by the
                                     oscillator partition function and by equipartition

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py` for the
format and its constraints.

Run:  uv run python media/render/render_partition.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, save, save_still  # noqa: E402
from thermolab import equilibrium, partition  # noqa: E402
from thermolab.constants import K_B  # noqa: E402
from thermolab.validation import seed_study  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
QUANTUM = 1.0e-21  # J: the oscillator's hbar omega
MU = 9.274e-24  # J/T
FIELD = 1.0  # T


def _eased(lo: float, hi: float, n_frames: int) -> np.ndarray:
    """Log-spaced values from lo to hi, eased at both ends."""
    ease = 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, n_frames))
    return np.exp(np.log(lo) + ease * (np.log(hi) - np.log(lo)))


def render_reconstruction(n_frames: int = 240, hold: int = 60) -> None:
    """U, S, F, C of an oscillator from ln Z, the difference step shrinking frame by frame.

    At a relative step near one the central differences straddle a factor of ten in beta and
    the dots sit far from the curves; by 1e-3 they are indistinguishable from them. F is
    -k_B T ln Z itself -- no derivative -- so its dots never leave the curve.
    """
    x = np.geomspace(0.1, 10.0, 200)
    t = x * QUANTUM / K_B
    dots = np.geomspace(0.1, 10.0, 17)
    t_dots = dots * QUANTUM / K_B
    exact = (partition.harmonic_energy(QUANTUM, t) / QUANTUM,
             partition.harmonic_entropy(QUANTUM, t) / K_B,
             -K_B * t * partition.log_z_harmonic(QUANTUM, t) / QUANTUM,
             partition.harmonic_heat_capacity(QUANTUM, t) / K_B)
    labels = (r"$U / \varepsilon$", r"$S / k_{\mathrm{B}}$", r"$F / \varepsilon$",
              r"$C / k_{\mathrm{B}}$")
    steps = np.concatenate([_eased(0.9, 1e-3, n_frames - hold), np.full(hold, 1e-3)])

    def log_z(temp):
        return partition.log_z_harmonic(QUANTUM, temp)

    def rebuilt(step: float) -> tuple[np.ndarray, ...]:
        r = partition.thermo_from_z(log_z, t_dots, rel_step=step)
        return (r.energy / QUANTUM, r.entropy / K_B, r.free_energy / QUANTUM,
                r.heat_capacity / K_B)

    fig, axes = plt.subplots(4, 1, figsize=(7.2, 8.4), dpi=DPI, sharex=True)
    points = []
    for ax, curve, label in zip(axes, exact, labels, strict=True):
        ax.semilogx(x, curve, color=BLACK, lw=1.8)
        (p,) = ax.semilogx([], [], "o", color=BLUE, ms=6)
        points.append(p)
        ax.set_ylabel(label)
        span = curve.max() - curve.min()
        ax.set_ylim(curve.min() - 0.25 * span, curve.max() + 0.25 * span)
    axes[-1].set_xlabel(r"$k_{\mathrm{B}} T / \varepsilon$")
    title = axes[0].text(0.03, 0.85, "", transform=axes[0].transAxes, fontsize=12)
    fig.tight_layout()

    def update(frame: int):
        values = rebuilt(float(steps[frame]))
        for p, v in zip(points, values, strict=True):
            p.set_data(dots, v)
        title.set_text(rf"$h / \beta = {steps[frame]:.3f}$")
        return (*points, title)

    save(FuncAnimation(fig, update, frames=len(steps), blit=False), fig,
         "partition-reconstruction")
    plt.close(fig)


def render_spin_dome(n_spins: int = 100, n_frames: int = 300) -> None:
    """S(U) with a sliding tangent; beta(U) crossing zero at the top of the dome."""
    spins = partition.spin_entropy_of_energy(n_spins, MU, FIELD)
    u = spins.energy / (MU * FIELD)
    s = spins.entropy / K_B
    beta = spins.beta() * MU * FIELD  # beta in units of 1 / (mu B)
    positions = np.rint(np.linspace(3, n_spins - 3, n_frames - 40)).astype(int)
    positions = np.concatenate([np.full(20, 3), positions, np.full(20, n_spins - 3)])

    fig, (left, right) = plt.subplots(1, 2, figsize=(9.6, 4.0), dpi=DPI)
    left.plot(u, s, color=BLACK, lw=1.8)
    (tangent,) = left.plot([], [], color=RED, lw=2.2)
    (dot,) = left.plot([], [], "o", color=RED, ms=7)
    left.set_xlim(-n_spins * 1.05, n_spins * 1.05)
    left.set_ylim(-3, s.max() * 1.18)
    left.set_xlabel(r"$U / \mu B$")
    left.set_ylabel(r"$S / k_{\mathrm{B}}$")

    right.plot(u[1:-1], beta[1:-1], color=BLACK, lw=1.5)
    right.axhline(0.0, color=GREY, lw=1.0)
    right.axvline(0.0, color=GREY, lw=1.0, ls=":")
    (marker,) = right.plot([], [], "o", color=RED, ms=7)
    right.set_xlim(-n_spins * 1.05, n_spins * 1.05)
    right.set_xlabel(r"$U / \mu B$")
    right.set_ylabel(r"$\beta\, \mu B$")
    readout = right.text(0.97, 0.92, "", transform=right.transAxes, ha="right", fontsize=12)
    fig.tight_layout()

    def update(frame: int):
        n = int(positions[frame])
        slope = beta[n] * 1.0  # dS/dU in k_B per (mu B), which is beta mu B
        half = 18.0
        du = np.array([-half, half])
        tangent.set_data(u[n] + du, s[n] + slope * du)
        dot.set_data([u[n]], [s[n]])
        marker.set_data([u[n]], [beta[n]])
        readout.set_text(rf"$\beta\,\mu B = {beta[n]:+.3f}$")
        return tangent, dot, marker, readout

    save(FuncAnimation(fig, update, frames=len(positions), blit=False), fig,
         "partition-spin-dome")
    plt.close(fig)


def render_freeze_out(n_frames: int = 270, n_levels: int = 16) -> None:
    """Level occupations and C(T) of an oscillator cooled from 5 to 0.08 hbar omega / k_B."""
    ratios = np.concatenate([_eased(5.0, 0.08, n_frames - 50), np.full(50, 0.08)])
    x = np.geomspace(0.05, 10.0, 300)
    c_curve = partition.harmonic_heat_capacity(QUANTUM, x * QUANTUM / K_B) / K_B
    levels = np.arange(n_levels)

    fig, (left, right) = plt.subplots(1, 2, figsize=(9.6, 4.0), dpi=DPI)
    bars = left.bar(levels, np.zeros(n_levels), width=0.7, color=BLUE)
    left.set_xlim(-0.7, n_levels - 0.3)
    left.set_ylim(0.0, 1.02)
    left.set_xlabel(r"$n$")
    left.set_ylabel(r"$P_n$")
    readout = left.text(0.96, 0.92, "", transform=left.transAxes, ha="right", fontsize=12)

    right.semilogx(x, c_curve, color=BLACK, lw=1.8)
    right.axhline(1.0, color=GREY, lw=1.2, ls="--")
    (marker,) = right.plot([], [], "o", color=RED, ms=8)
    right.set_ylim(-0.03, 1.12)
    right.set_xlabel(r"$k_{\mathrm{B}} T / \hbar\omega$")
    right.set_ylabel(r"$C / k_{\mathrm{B}}$")
    fig.tight_layout()

    def update(frame: int):
        ratio = float(ratios[frame])
        p = np.exp(-levels / ratio) * (1.0 - np.exp(-1.0 / ratio))
        for bar, height in zip(bars, p, strict=True):
            bar.set_height(height)
        c = partition.harmonic_heat_capacity(QUANTUM, ratio * QUANTUM / K_B) / K_B
        marker.set_data([ratio], [c])
        readout.set_text(rf"$k_{{\mathrm{{B}}}} T / \hbar\omega = {ratio:.2f}$")
        return (*bars, marker, readout)

    save(FuncAnimation(fig, update, frames=len(ratios), blit=False), fig,
         "partition-freeze-out")
    plt.close(fig)


def render_paramagnet() -> None:
    """(a) M / (N mu) against mu B / k_B T; (b) C / (N k_B) against k_B T / mu B."""
    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=DPI)
    x = np.linspace(0.0, 4.0, 400)
    a.plot(x, np.tanh(x), color=BLACK, lw=2.0)
    a.plot(x[x <= 1.3], x[x <= 1.3], color=BLUE, lw=1.4, ls="--")
    a.axhline(1.0, color=GREY, lw=1.2, ls=":")
    a.set_xlim(0.0, 4.0)
    a.set_ylim(0.0, 1.15)
    a.set_xlabel(r"$\mu B / k_{\mathrm{B}} T$")
    a.set_ylabel(r"$M / N\mu$")
    a.text(-0.14, 1.02, "(a)", transform=a.transAxes, fontsize=12)

    ratio = np.geomspace(0.05, 20.0, 400)  # k_B T / mu B
    t = ratio * MU * FIELD / K_B
    c = partition.paramagnet_heat_capacity(1, MU, FIELD, t) / K_B
    b.semilogx(ratio, c, color=BLACK, lw=2.0)
    peak = ratio[np.argmax(c)]
    b.axvline(peak, color=GREY, lw=1.0, ls=":")
    b.set_ylim(-0.01, 0.5)
    b.set_xlabel(r"$k_{\mathrm{B}} T / \mu B$")
    b.set_ylabel(r"$C / N k_{\mathrm{B}}$")
    b.text(-0.14, 1.02, "(b)", transform=b.transAxes, fontsize=12)
    fig.tight_layout()
    save_still(fig, "partition-paramagnet")
    plt.close(fig)


def render_einstein_overlay(n_body: int = 40, n_seeds: int = 8) -> None:
    """Module 01's simulated endpoints, placed on the temperature axis two ways."""
    energies = (0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0)
    shared, t_z, t_err = [], [], []
    for index, per_oscillator in enumerate(energies):
        t_equipartition = per_oscillator * QUANTUM / K_B
        state = equilibrium.from_temperatures(n_body, n_body, 1.6 * t_equipartition,
                                              0.4 * t_equipartition, QUANTUM)

        def endpoint(rng, state=state):
            run = equilibrium.simulate_energy_exchange(state, 20 * state.total_quanta, rng)
            tail = run.q_a[len(run.q_a) // 2:]
            return float(partition.harmonic_temperature(tail.mean() / n_body * QUANTUM,
                                                        QUANTUM))

        study = seed_study(endpoint, n_seeds=n_seeds, base_seed=1200 + index)
        shared.append(state.total_quanta / state.total_oscillators)
        t_z.append(study.mean * K_B / QUANTUM)
        t_err.append(study.standard_error * K_B / QUANTUM)

    x = np.geomspace(0.05, 20.0, 400)
    fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=DPI)
    ax.axvspan(2.0, 20.0, color=BLUE, alpha=0.07, lw=0)
    ax.loglog(x, 1.0 / np.expm1(1.0 / x), color=BLACK, lw=2.0)
    ax.loglog(x, x, color=GREY, lw=1.4, ls="--")
    ax.errorbar(t_z, shared, xerr=t_err, fmt="o", color=BLUE, ms=6, capsize=3)
    ax.plot(shared, shared, "o", mfc="none", mec=GREY, ms=7)
    ax.set_xlim(0.05, 20.0)
    ax.set_ylim(1e-3, 20.0)
    ax.set_xlabel(r"$k_{\mathrm{B}} T / \hbar\omega$")
    ax.set_ylabel(r"$U / n\hbar\omega$")
    fig.tight_layout()
    save_still(fig, "partition-einstein-overlay")
    plt.close(fig)


def main() -> None:
    render_reconstruction()
    render_spin_dome()
    render_freeze_out()
    render_paramagnet()
    render_einstein_overlay()


if __name__ == "__main__":
    main()
