"""Render the demonstrations for module 18 (fluctuations and transport).

Three animations and two stills, driven by `thermolab.transport`, module 03's walkers and the
module's two data files, so what a student watches is the code and the data they can load.

    transport-cloud.mp4   ten thousand independent walkers released at the origin. Left: the
                          histogram of their positions at time t, with the diffusion equation's
                          Green's function for D = l^2/(2 tau) drawn over it -- a prediction,
                          not a fit; right: the mean squared displacement against t on log-log
                          axes, growing along the slope-one line 2 D t. t runs from 10 to 1000
                          steps
    transport-fronts.mp4  a dye layer diffusing into clear water, against a front moving at a
                          constant speed chosen to match it at t = 1. Top: the concentration
                          profile (1/2) erfc(x / 2 sqrt(D t)) with the quarter-strength contour
                          marked, and the constant-speed front; bottom: the two positions
                          against time, sqrt(t) against t. By t = 9 the diffusive front has
                          gone 3 times as far as at t = 1, the other 9 times
    transport-msd.mp4     walkers that repeat their last step with probability 0.95 (and
                          otherwise step afresh at random), as a
                          molecule keeps its velocity between collisions. Left: the mean
                          squared displacement on log-log axes, with the ballistic line
                          <v^2> t^2 and the diffusive line 2 D t; right: the running integral
                          of the velocity autocorrelation, divided by the exact D, rising to a
                          plateau at 1, with the independent-step value l^2/(2 tau) marked far
                          below it. The left curve turns from slope 2 to slope 1 where the
                          right one levels off
    transport-viscosity.png   the viscosity of He, N2 and Ar at 300 K from 1 kPa to 10 MPa,
                          from the NIST WebBook's reference correlations (data/18-gas-transport.
                          csv), with the dashed kinetic estimate m vbar/(3 sqrt(2) sigma) for each
                          and the decade 0.1-1 MPa shaded
    transport-perrin.png  Perrin's 1909 counts of the 30-second |x| of gamboge granules, two
                          series (data/18-perrin-projections.csv), with the Gaussian fitted to each

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py`.

Run:  uv run python media/render/render_transport.py
"""

from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, ROOT, save, save_still  # noqa: E402
from thermolab import gases, sampling, transport  # noqa: E402
from thermolab.constants import K_B, N_A  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
LIGHT_BLUE = "#93c5fd"


def _style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)


def render_cloud() -> None:
    """Independent walkers melting into the Green's function, and their MSD's slope of one."""
    rng = np.random.default_rng(18)
    n_steps = 1000
    walkers = transport.walker_trajectories(10_000, n_steps, 1.0, rng)
    spread = transport.msd(walkers)
    d = transport.persistent_walk_d(1.0, 1.0)
    times = np.unique(np.geomspace(10, n_steps, 140).astype(int))
    span = (-110.0, 110.0)
    x = np.linspace(*span, 600)

    fig, (ax, ax_msd) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=DPI,
                                     gridspec_kw={"width_ratios": [1.45, 1.0]})
    bars = ax.bar([], [], color=LIGHT_BLUE, edgecolor="white", linewidth=0.3)
    (theory,) = ax.plot([], [], color=BLUE, lw=2.4)
    ax.set_xlim(*span)
    ax.set_ylim(0, 0.135)
    ax.set_xlabel(r"$x \,/\, \ell$")
    ax.set_ylabel(r"$P(x, t)\, \ell$")
    _style(ax)

    guide = np.array([1.0, 2.0 * n_steps])
    ax_msd.plot(guide, 2 * d * guide, color=BLUE, ls="--", lw=1.4)
    ax_msd.text(25, 2 * d * 25 * 3.0, r"$2Dt$", color=BLUE, fontsize=12)
    (curve,) = ax_msd.plot([], [], color=BLACK, lw=2.2)
    (dot,) = ax_msd.plot([], [], "o", color=AMBER, ms=7)
    ax_msd.set_xscale("log")
    ax_msd.set_yscale("log")
    ax_msd.set_xlim(8, 1.3 * n_steps)
    ax_msd.set_ylim(6, 2.0e3)
    ax_msd.set_xlabel(r"$t \,/\, \tau$")
    ax_msd.set_ylabel(r"$\langle x^2 \rangle \,/\, \ell^2$")
    _style(ax_msd)
    label = fig.text(0.5, 0.94, "", ha="center", fontsize=13)
    fig.subplots_adjust(top=0.86, bottom=0.15, left=0.07, right=0.96, wspace=0.26)

    def draw(i):
        nonlocal bars
        t = int(times[i])
        # One reachable site per bin (sites lie 2 l apart), so every bar is one site's share.
        centres, density = sampling.walker_histogram(walkers[:, t], n_bins=110, span=span,
                                                     lattice=2.0)
        # The retained fraction, not the in-span normalisation np.histogram applies, so the
        # bars and the curve keep the same area as walkers leave the frame.
        inside = np.mean((walkers[:, t] >= span[0]) & (walkers[:, t] <= span[1]))
        bars.remove()
        bars = ax.bar(centres, density * inside, width=centres[1] - centres[0],
                      color=LIGHT_BLUE, edgecolor="white", linewidth=0.3)
        theory.set_data(x, transport.diffusion_greens_function(x, t, d))
        curve.set_data(np.arange(10, t + 1), spread[10:t + 1])
        dot.set_data([t], [spread[t]])
        label.set_text(rf"$t = {t}\,\tau$")
        return bars, theory, curve, dot, label

    frames = [0] * 20 + list(range(len(times))) + [len(times) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "transport-cloud")
    plt.close(fig)
    late = np.arange(100, n_steps + 1)
    slope = np.polyfit(np.log(late), np.log(spread[late]), 1)[0]
    print(f"[cloud] log-log slope of the MSD from 100 to 1000 steps: {slope:.4f}")


def _quarter_front(t: float, d: float) -> float:
    """Where the layer's concentration has fallen to a quarter of the source, by bisection."""
    low, high = 0.0, 20.0 * np.sqrt(d * t)
    for _ in range(80):
        middle = 0.5 * (low + high)
        if transport.step_profile(middle, t, d) > 0.25:
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def render_fronts() -> None:
    """A diffusion front's sqrt(t) against a constant-speed front matched to it at t = 1."""
    d = 1.0
    speed = _quarter_front(1.0, d)   # the steady front reaches the same place at t = 1
    times = np.linspace(0.02, 9.0, 180)
    fronts = np.array([_quarter_front(t, d) for t in times])
    x = np.linspace(-3.0, 10.0, 700)

    fig, (ax, ax_pos) = plt.subplots(2, 1, figsize=(9.0, 6.4), dpi=DPI,
                                     gridspec_kw={"height_ratios": [1.0, 1.15]})
    fill = ax.fill_between(x, 0 * x, color=LIGHT_BLUE)
    (profile,) = ax.plot([], [], color=BLUE, lw=2.2)
    diffusive_mark = ax.axvline(0.0, color=BLUE, lw=1.6, ls="--")
    steady_mark = ax.axvline(0.0, color=RED, lw=2.0)
    ax.axhline(0.25, color=GREY, lw=1, ls=":")
    ax.text(9.2, 0.29, r"$c_0/4$", color=GREY, fontsize=11)
    ax.set_xlim(-3.0, 10.0)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$c \,/\, c_0$")
    _style(ax)

    ax_pos.plot(times, fronts, color=BLUE, lw=1.0, alpha=0.25)
    ax_pos.plot(times, speed * times, color=RED, lw=1.0, alpha=0.25)
    (diffusive,) = ax_pos.plot([], [], color=BLUE, lw=2.4)
    (steady,) = ax_pos.plot([], [], color=RED, lw=2.4)
    ax_pos.text(9.15, fronts[-1], r"$\propto \sqrt{t}$", color=BLUE, fontsize=12, va="center")
    ax_pos.text(9.15, speed * 9.0, r"$\propto t$", color=RED, fontsize=12, va="center")
    for t_mark in (1.0, 4.0, 9.0):
        ax_pos.axvline(t_mark, color=GREY, lw=0.8, ls=":")
    ax_pos.set_xlim(0, 10.2)
    ax_pos.set_ylim(0, 9.5)
    ax_pos.set_xticks([0, 1, 4, 9])
    ax_pos.set_xlabel(r"$t$")
    ax_pos.set_ylabel(r"$x_{\mathrm{front}}$")
    _style(ax_pos)
    label = fig.text(0.5, 0.955, "", ha="center", fontsize=13)
    fig.subplots_adjust(top=0.9, bottom=0.09, left=0.1, right=0.9, hspace=0.42)

    def draw(i):
        nonlocal fill
        t = float(times[i])
        c = transport.step_profile(x, t, d)
        fill.remove()
        fill = ax.fill_between(x, c, color=LIGHT_BLUE)
        profile.set_data(x, c)
        diffusive_mark.set_xdata([fronts[i], fronts[i]])
        steady_mark.set_xdata([speed * t, speed * t])
        diffusive.set_data(times[:i + 1], fronts[:i + 1])
        steady.set_data(times[:i + 1], speed * times[:i + 1])
        label.set_text(rf"$t = {t:.2f}$")
        return fill, profile, diffusive_mark, steady_mark, diffusive, steady, label

    frames = [0] * 15 + list(range(len(times))) + [len(times) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "transport-fronts")
    plt.close(fig)
    one, four, nine = (_quarter_front(t, d) for t in (1.0, 4.0, 9.0))
    print(f"[fronts] quarter contour at t = 1, 4, 9: {one:.4f}, {four:.4f}, {nine:.4f} "
          f"(ratios {four / one:.4f}, {nine / one:.4f})")


def render_msd() -> None:
    """Walkers with memory: ballistic, then diffusive, as the velocity integral levels off."""
    q, n_steps = 0.95, 3000
    rng = np.random.default_rng(1803)
    walkers = transport.walker_trajectories(4000, n_steps, 1.0, rng, persistence=q)
    spread = transport.msd(walkers)
    vacf = transport.velocity_autocorrelation(transport.walker_velocities(walkers, 1.0), 400)
    running = transport.green_kubo_running(vacf, 1.0)
    d = transport.persistent_walk_d(1.0, 1.0, q)
    naive = transport.persistent_walk_d(1.0, 1.0)
    times = np.unique(np.geomspace(1, n_steps, 150).astype(int))

    fig, (ax, ax_gk) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=DPI)
    guide = np.geomspace(1, n_steps, 50)
    ax.plot(guide, guide**2, color=RED, ls="--", lw=1.4)
    ax.plot(guide, 2 * d * guide, color=BLUE, ls="--", lw=1.4)
    ax.text(1.6, 8.0, r"$\langle v^2 \rangle t^2$", color=RED, fontsize=12)
    ax.text(700, 2 * d * 700 / 4.0, r"$2Dt$", color=BLUE, fontsize=12)
    (curve,) = ax.plot([], [], color=BLACK, lw=2.2)
    (dot,) = ax.plot([], [], "o", color=AMBER, ms=7)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.8, 1.3 * n_steps)
    ax.set_ylim(0.6, 3e5)
    ax.set_xlabel(r"$t \,/\, \tau$")
    ax.set_ylabel(r"$\langle x^2 \rangle \,/\, \ell^2$")
    _style(ax)

    ax_gk.axhline(1.0, color=BLUE, lw=1.2, ls="--")
    ax_gk.axhline(naive / d, color=GREY, lw=1.2, ls=":")
    ax_gk.text(330, naive / d + 0.04, r"$\ell^2 / 2\tau$", color=GREY, fontsize=11)
    (integral,) = ax_gk.plot([], [], color=BLACK, lw=2.2)
    (gk_dot,) = ax_gk.plot([], [], "o", color=AMBER, ms=7)
    ax_gk.set_xlim(0, 400)
    ax_gk.set_ylim(0, 1.15)
    ax_gk.set_xlabel(r"$K$")
    ax_gk.set_ylabel(r"$\tau \sum_{k \leq K} C(k) \,/\, D$")
    _style(ax_gk)
    label = fig.text(0.5, 0.94, "", ha="center", fontsize=13)
    fig.subplots_adjust(top=0.86, bottom=0.15, left=0.08, right=0.97, wspace=0.28)

    def draw(i):
        t = int(times[i])
        curve.set_data(np.arange(1, t + 1), spread[1:t + 1])
        dot.set_data([t], [spread[t]])
        k = min(t, running.size - 1)
        integral.set_data(np.arange(k + 1), running[:k + 1] / d)
        gk_dot.set_data([k], [running[k] / d])
        label.set_text(rf"$q = {q},\ t = {t}\,\tau$")
        return curve, dot, integral, gk_dot, label

    frames = [0] * 20 + list(range(len(times))) + [len(times) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "transport-msd")
    plt.close(fig)
    print(f"[msd] plateau {running[-1] / d:.4f} of the exact D = {d:.2f} l^2/tau; "
          f"l^2/(2 tau) is {naive / d:.4f} of it")


def _read_table(name: str) -> dict[str, np.ndarray]:
    """A data file as a dict of columns; every line starting with # is commentary."""
    lines = [line for line in (ROOT / "data" / name).read_text(encoding="utf-8").splitlines()
             if line and not line.startswith("#")]
    header = lines[0].split(",")
    columns = zip(*(line.split(",") for line in lines[1:]), strict=True)
    return {h: np.array(c) if h == "gas" else np.array(c, dtype=float)
            for h, c in zip(header, columns, strict=True)}


# Critical temperature [K], critical pressure [Pa], molar mass [kg/mol]: NIST Chemistry WebBook.
CRITICAL = {"He": (5.1953, 0.22832e6, 4.002602e-3), "N2": (126.192, 3.3958e6, 28.0134e-3),
            "Ar": (150.687, 4.863e6, 39.948e-3)}


def render_viscosity() -> None:
    """NIST viscosity against pressure at 300 K, flat over the dilute range, with the estimates."""
    nist = _read_table("18-gas-transport.csv")
    fig, ax = plt.subplots(figsize=(8.0, 4.4), dpi=DPI)
    ax.axvspan(1e5, 1e6, color="#e5e7eb", zorder=0)
    labels = {"He": "He", "N2": r"N$_2$", "Ar": "Ar"}
    for gas, colour in (("He", AMBER), ("N2", BLUE), ("Ar", BLACK)):
        rows = nist["gas"] == gas
        pressure, eta = nist["pressure_MPa"][rows] * 1e6, nist["viscosity_uPa_s"][rows]
        t_c, p_c, molar_mass = CRITICAL[gas]
        diameter = transport.diameter_from_vdw_b(gases.vdw_constants_from_critical(t_c, p_c)[1])
        estimate = transport.kinetic_estimates(1e5 / (K_B * 300.0), 300.0, molar_mass / N_A,
                                               transport.hard_sphere_cross_section(diameter))
        ax.semilogx(pressure, eta, color=colour, lw=2.4)
        ax.axhline(estimate.viscosity * 1e6, color=colour, lw=1.2, ls="--")
        # Helium and nitrogen end within half a micropascal second of each other at 10 MPa.
        nudge = {"He": 0.9, "N2": -0.6, "Ar": 0.0}[gas]
        ax.text(1.4e7, eta[-1] + nudge, labels[gas], color=colour, fontsize=12, va="center")
    ax.set_xlim(1e3, 1e7)
    ax.set_ylim(5, 28)
    ax.set_xlabel(r"$P$ (Pa)")
    ax.set_ylabel(r"$\eta$ ($\mu$Pa s)")
    _style(ax)
    fig.subplots_adjust(left=0.1, right=0.9, bottom=0.14, top=0.95)
    save_still(fig, "transport-viscosity")
    plt.close(fig)


def render_perrin() -> None:
    """Perrin's 1909 counts of |x| for gamboge granules, with the fitted Gaussian."""
    perrin = _read_table("18-perrin-projections.csv")
    edges = np.append(perrin["low_um"], perrin["high_um"][-1])
    centres = 0.5 * (edges[:-1] + edges[1:])
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.0), dpi=DPI, sharey=True)
    for ax, series in zip(axes, ("first", "second"), strict=True):
        found = perrin[f"{series}_found"]
        variance = transport.fit_binned_gaussian_variance(edges, found)
        cumulative = np.array([math.erf(e / math.sqrt(2.0 * variance)) for e in edges])
        model = np.diff(cumulative)
        ax.bar(centres, found, width=1.55, color=LIGHT_BLUE)
        ax.plot(centres, model / model.sum() * found.sum(), "o-", color=BLUE, lw=1.8, ms=5)
        ax.text(0.97, 0.92, rf"$\langle x^2 \rangle = {variance:.0f}\ \mu\mathrm{{m}}^2$",
                ha="right", transform=ax.transAxes, fontsize=12, color=BLUE)
        ax.set_xlabel(r"$|x|$ ($\mu$m)")
        _style(ax)
    axes[0].set_ylabel(r"$n$")
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.15, top=0.95, wspace=0.08)
    save_still(fig, "transport-perrin")
    plt.close(fig)


if __name__ == "__main__":
    render_cloud()
    render_fronts()
    render_msd()
    render_viscosity()
    render_perrin()
