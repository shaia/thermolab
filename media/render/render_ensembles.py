"""Render the demonstrations for module 11 (statistical ensembles).

Two animations and two stills, all built from `thermolab.ensembles`, so what a student watches
is the exact enumeration they can read and run:

    ensembles-bath-growth.mp4     a three-oscillator solid on a bath growing from 3 to 3000
                                  oscillators at one quantum per oscillator: its level
                                  populations settle onto g(k) exp(-beta E_k) / Z, and the log
                                  of the per-microstate probability straightens into a line
    ensembles-joint-marginal.mp4  the same composite, drawn twice: every joint microstate at the
                                  same height (flat), and the system's marginal, which is not
    ensembles-convergence.png     (a) the gap to the Boltzmann curve against bath size, slope -1;
                                  (b) the measured correction to -beta E against the predicted
                                  curvature term, for three bath sizes
    ensembles-two-level.png       the two-level system's occupations and mean energy against
                                  temperature, with both limits drawn

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py` for the
format and its constraints.

Run:  uv run python media/render/render_ensembles.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from _common import DPI, save, save_still  # noqa: E402
from thermolab import ensembles  # noqa: E402
from thermolab.constants import K_B  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
QUANTUM = 1.0e-21
N_SYSTEM = 3  # oscillators in the small solid
# Levels drawn. The solid's ladder is capped here, which makes it a slightly different system:
# above k = 14 the Boltzmann distribution holds 0.12% of the probability, too little to see.
MAX_LEVEL = 14
PER_OSCILLATOR = 1.0  # quanta per bath oscillator: k_B T = eps / ln 2


def _bath_sizes(n_frames: int, lo: float = 3.0, hi: float = 3000.0) -> np.ndarray:
    """Log-spaced bath sizes, eased at both ends, rounded to whole oscillators."""
    ease = 0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, n_frames))
    return np.rint(np.exp(np.log(lo) + ease * (np.log(hi) - np.log(lo)))).astype(int)


def _level_colours(n_levels: int) -> list:
    """Distinct colours for the levels that carry the probability, grey for the thin tail.

    A sequential map made neighbouring levels -- the only ones a small bath can reach -- almost
    indistinguishable, and those are exactly the blocks the joint panel asks the eye to compare.
    """
    palette = plt.get_cmap("tab10").colors
    return [palette[k] if k < len(palette) else GREY for k in range(n_levels)]


def render_bath_growth(n_frames: int = 270) -> None:
    """The system's level populations, and ln of the probability per microstate, as N grows.

    Left: P(level k) as bars, against the Boltzmann g(k) exp(-beta E_k)/Z of the infinite bath
    at the same energy density (black dots). Right: ln[P(k)/g(k)], the log probability of one
    system microstate at level k. For a Boltzmann distribution it is a straight line of slope
    -beta eps; the finite bath's points bend downward -- the curvature term the derivation
    drops -- and straighten as the bath grows. Unreachable levels (k > q_tot) are not drawn.
    """
    levels = ensembles.einstein_levels(N_SYSTEM, MAX_LEVEL, QUANTUM)
    temperature = ensembles.bath_temperature(PER_OSCILLATOR, QUANTUM)
    reference = ensembles.boltzmann_distribution(levels, temperature)
    k = levels.quanta
    sizes = np.concatenate([_bath_sizes(n_frames - 60), np.full(60, 3000)])

    fig, (left, right) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=DPI)
    bars = left.bar(k, np.zeros_like(reference), width=0.72, color=BLUE, alpha=0.85)
    left.plot(k, reference, "o", color=BLACK, ms=5, zorder=3)
    left.set_xlim(-0.7, MAX_LEVEL + 0.7)
    left.set_ylim(0.0, 0.34)
    left.set_xlabel(r"$E_k / \varepsilon$")
    left.set_ylabel(r"$P_k$")
    title = left.text(0.97, 0.94, "", transform=left.transAxes, ha="right", va="top",
                      fontsize=12)

    log_micro = np.log(reference / levels.degeneracy)
    right.plot(k, log_micro, color=BLACK, lw=1.8)
    (points,) = right.plot([], [], "o-", color=BLUE, ms=6, lw=1.2)
    right.set_xlim(-0.7, MAX_LEVEL + 0.7)
    right.set_ylim(-13.0, 0.5)
    right.set_xlabel(r"$E_k / \varepsilon$")
    right.set_ylabel(r"$\ln\,(P_k / g_k)$")
    fig.tight_layout()

    def update(frame: int):
        n_bath = int(sizes[frame])
        joint = ensembles.enumerate_joint(levels, n_bath, int(round(PER_OSCILLATOR * n_bath)))
        marginal = ensembles.marginal_occupation(joint)
        for bar, height in zip(bars, marginal, strict=True):
            bar.set_height(height)
        reach = joint.accessible
        points.set_data(k[reach], np.log(marginal[reach] / levels.degeneracy[reach]))
        title.set_text(rf"$N_{{\mathrm{{bath}}}} = {n_bath}$")
        return (*bars, points, title)

    save(FuncAnimation(fig, update, frames=len(sizes), blit=False), fig,
         "ensembles-bath-growth")
    plt.close(fig)


def render_joint_marginal(n_frames: int = 300) -> None:
    """Every joint microstate at one height; the system's marginal at many.

    Left: all joint microstates of system plus bath laid side by side, sorted by the system's
    level and coloured by it, each drawn at the same height -- the postulate. The horizontal
    axis is the fraction of all joint microstates, so each colour's width is that level's
    marginal probability. While there are few enough (up to 220), white lines separate the
    individual microstates. Right: the same widths as bars, with the Boltzmann values dotted.
    """
    levels = ensembles.einstein_levels(N_SYSTEM, MAX_LEVEL, QUANTUM)
    colours = _level_colours(len(levels))
    temperature = ensembles.bath_temperature(PER_OSCILLATOR, QUANTUM)
    reference = ensembles.boltzmann_distribution(levels, temperature)
    hold = 45
    grown = _bath_sizes(n_frames - 2 * hold, lo=3.0, hi=1000.0)
    sizes = np.concatenate([np.full(hold, 3), grown, np.full(hold, 1000)])

    fig, (left, right) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=DPI,
                                      gridspec_kw={"width_ratios": [1.35, 1.0]})
    left.set_xlim(0.0, 1.0)
    left.set_ylim(0.0, 1.35)
    left.set_yticks([0.0, 1.0])
    left.set_yticklabels(["0", r"$1/\Omega_{\mathrm{tot}}$"])
    left.set_xlabel(r"$j / \Omega_{\mathrm{tot}}$")
    label = left.text(0.98, 1.27, "", ha="right", va="top", fontsize=12)

    k = levels.quanta
    bars = right.bar(k, np.zeros(len(levels)), width=0.72, color=colours)
    right.plot(k, reference, "o", color=BLACK, ms=5, zorder=3)
    right.set_xlim(-0.7, len(levels) - 0.3)
    right.set_ylim(0.0, 0.34)
    right.set_xlabel(r"$E_k / \varepsilon$")
    right.set_ylabel(r"$P_k$")
    fig.tight_layout()

    def update(frame: int):
        n_bath = int(sizes[frame])
        joint = ensembles.enumerate_joint(levels, n_bath, int(round(PER_OSCILLATOR * n_bath)))
        marginal = ensembles.marginal_occupation(joint)
        for artist in list(left.patches) + list(left.lines):
            artist.remove()
        start = 0.0
        for colour, width in zip(colours, marginal, strict=True):
            if width > 0:
                left.add_patch(Rectangle((start, 0.0), width, 1.0, color=colour, lw=0))
            start += width
        # Decide in log space: the count itself overflows a float by N_bath ~ 500.
        exponent = joint.log_total_multiplicity / np.log(10.0)
        if exponent < 6.0:
            total = float(np.exp(joint.log_total_multiplicity))
            if total <= 220:
                for edge in np.arange(1, round(total)) / total:
                    left.plot([edge, edge], [0.0, 1.0], color="white", lw=0.7)
            omega = rf"\Omega_{{\mathrm{{tot}}}} = {round(total)}"
        else:
            omega = rf"\Omega_{{\mathrm{{tot}}}} \approx 10^{{{exponent:.0f}}}"
        left.plot([0.0, 1.0], [1.0, 1.0], color=BLACK, lw=1.4)
        for bar, height in zip(bars, marginal, strict=True):
            bar.set_height(height)
        label.set_text(rf"$N_{{\mathrm{{bath}}}} = {n_bath},\ \ {omega}$")
        return (*bars, label)

    save(FuncAnimation(fig, update, frames=len(sizes), blit=False), fig,
         "ensembles-joint-marginal")
    plt.close(fig)


def render_convergence() -> None:
    """(a) sup-norm gap against bath size; (b) measured versus predicted log correction."""
    sizes = np.unique(np.rint(np.geomspace(10, 3000, 22)).astype(int))
    two = ensembles.two_level(1, QUANTUM)
    solid = ensembles.einstein_levels(N_SYSTEM, 40, QUANTUM)

    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 4.0), dpi=DPI)
    for levels, colour, name in ((two, BLUE, r"$\Delta = \varepsilon$"),
                                 (solid, AMBER, r"$n_{\mathrm{sys}} = 3$")):
        sweep = ensembles.bath_size_sweep(levels, sizes, PER_OSCILLATOR)
        a.loglog(sweep.n_bath, sweep.distances, "o", color=colour, ms=5, label=name)
        guide = sweep.distances[0] * sweep.n_bath[0] / sizes
        a.loglog(sizes, guide, color=colour, lw=1.0, alpha=0.6)
    a.set_xlabel(r"$N_{\mathrm{bath}}$")
    a.set_ylabel(r"$\max_k\,|P_k - P_k^{\mathrm{B}}|$")
    a.text(0.05, 0.06, r"$\propto N_{\mathrm{bath}}^{-1}$", transform=a.transAxes, fontsize=11)
    a.legend(frameon=False)
    a.text(-0.16, 1.02, "(a)", transform=a.transAxes, fontsize=12)

    levels = ensembles.einstein_levels(N_SYSTEM, 8, QUANTUM)
    fine = np.linspace(0.0, 8.0, 200)
    for n_bath, colour in ((30, RED), (100, AMBER), (300, BLUE)):
        joint = ensembles.enumerate_joint(levels, n_bath, n_bath)
        curvature = ensembles.bath_curvature_exact(n_bath, n_bath, QUANTUM)
        b.plot(fine, 0.5 * (fine * QUANTUM) ** 2 * curvature, color=colour, lw=1.4)
        b.plot(levels.quanta, ensembles.measured_log_correction(joint), "o", color=colour,
               ms=5, label=rf"$N_{{\mathrm{{bath}}}} = {n_bath}$")
    b.set_xlabel(r"$E_k / \varepsilon$")
    b.set_ylabel(r"$\ln\frac{\Omega_{\mathrm{b}}(q - k)}{\Omega_{\mathrm{b}}(q)} + \beta E_k$")
    b.legend(frameon=False, loc="lower left")
    b.text(-0.16, 1.02, "(b)", transform=b.transAxes, fontsize=12)
    fig.tight_layout()
    save_still(fig, "ensembles-convergence")
    plt.close(fig)


def render_two_level() -> None:
    """Occupations and mean energy of a two-level system against k_B T / Delta."""
    gap = 1.0e-21
    system = ensembles.TwoLevelSystem(gap=gap)
    x = np.geomspace(0.05, 100.0, 400)  # k_B T / Delta
    temperatures = x * gap / K_B

    fig, (a, b) = plt.subplots(1, 2, figsize=(9.6, 3.8), dpi=DPI)
    a.semilogx(x, system.ground_occupation(temperatures), color=BLUE, lw=2.0, label=r"$p_0$")
    a.semilogx(x, system.excited_occupation(temperatures), color=RED, lw=2.0, label=r"$p_1$")
    a.axhline(0.5, color=GREY, lw=1.0, ls="--")
    a.set_ylim(-0.02, 1.02)
    a.set_xlabel(r"$k_{\mathrm{B}} T / \Delta$")
    a.set_ylabel(r"$p$")
    a.legend(frameon=False, loc="upper right")
    a.text(-0.14, 1.02, "(a)", transform=a.transAxes, fontsize=12)

    b.semilogx(x, system.mean_energy(temperatures) / gap, color=BLACK, lw=2.0)
    b.axhline(0.5, color=GREY, lw=1.0, ls="--")
    b.set_ylim(-0.01, 0.55)
    b.set_xlabel(r"$k_{\mathrm{B}} T / \Delta$")
    b.set_ylabel(r"$\langle E \rangle / \Delta$")
    b.text(-0.14, 1.02, "(b)", transform=b.transAxes, fontsize=12)
    fig.tight_layout()
    save_still(fig, "ensembles-two-level")
    plt.close(fig)


def main() -> None:
    render_bath_growth()
    render_joint_marginal()
    render_convergence()
    render_two_level()


if __name__ == "__main__":
    main()
