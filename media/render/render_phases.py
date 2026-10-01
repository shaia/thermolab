"""Render the demonstrations for module 14 (phase coexistence).

Four animations and one still, all built from `thermolab.phases` and `thermolab.gases`, so
what a student watches is the code they can run. Everything is drawn in reduced variables
(P / P_c, v / v_c, T / T_c), which is why one van der Waals substance serves for all:

    phases-maxwell.mp4          one sub-critical isotherm as T sweeps up toward T_c: the loop,
                                the flat line at P_sat, the two equal-area lobes shaded, the
                                spinodal points marked -- and beside it the mu-P loop crossing
                                itself at exactly P_sat; the whole construction collapses onto
                                the critical point
    phases-coexistence.mp4      the P-T diagram traced by the coexistence point as T rises,
                                with a synchronized P-v panel showing the binodal and spinodal
                                domes and the current flat line; the curve ends at (T_c, P_c)
    phases-lever.mp4            a state point crossing the dome at fixed T, with a cylinder
                                whose liquid level and a bar of phase fractions follow the
                                lever rule
    phases-around-critical.mp4  two paths in the P-T plane from gas to liquid: one across the
                                coexistence curve, where the density jumps, and one around its
                                end, where the density changes smoothly
    phases-wiggle-vs-data.png   the opening puzzle: module 02's real CO2 isotherm at 280 K,
                                flat across its plateau, against the bare van der Waals loop
                                and the flat line the construction puts through it
    phases-water-diagram.png    water's real P-T diagram (sublimation, melting, vaporization,
                                from data/14-water-phase-boundaries.csv) with its triple and
                                critical points, and the van der Waals vaporization curve
                                fitted from water's critical point, for contrast

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py` for the
format and its constraints.

Run:  uv run python media/render/render_phases.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from _common import DPI, ROOT, save, save_still  # noqa: E402
from thermolab import gases, phases  # noqa: E402
from thermolab.constants import K_B  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
LIGHT_BLUE, LIGHT_RED = "#bfdbfe", "#fecaca"

# CO2's constants from its critical point, as in modules 02 and the laboratory. Every axis
# is reduced, so the choice of substance never shows.
A, B = gases.vdw_constants_from_critical(304.13, 7.3773e6)
V_C, T_C, P_C = gases.vdw_critical_point(A, B)


def _ease(u: np.ndarray) -> np.ndarray:
    """Smooth start and stop for a sweep parameter in [0, 1]."""
    return 0.5 - 0.5 * np.cos(np.pi * u)


def _isotherm_r(t_r: float, v_r: np.ndarray) -> np.ndarray:
    return gases.vdw_pressure_reduced(v_r, t_r)


def _mu_r(v_r: np.ndarray, t_r: float) -> np.ndarray:
    """mu / (P_c v_c) along the isotherm, from the SI function so nothing is re-derived here."""
    return phases.vdw_chemical_potential(v_r * V_C, t_r * T_C, A, B) / (P_C * V_C)


def _dome(n: int = 300) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(T_r, v_r, P_r) around the binodal: liquid branch up to T_c, gas branch back down."""
    t_r = np.linspace(phases.T_RATIO_MIN, phases.T_RATIO_MAX, n)
    p_sat, v_l, v_g = phases.coexistence_curve(t_r * T_C, A, B)
    v_r = np.concatenate([v_l / V_C, [1.0], v_g[::-1] / V_C])
    p_r = np.concatenate([p_sat / P_C, [1.0], p_sat[::-1] / P_C])
    return np.concatenate([t_r, [1.0], t_r[::-1]]), v_r, p_r


def render_maxwell(n_frames: int = 330, hold: int = 60) -> None:
    """The loop flattens, the lobes shrink, and the construction lands on the critical point."""
    live = n_frames - hold
    # Above T_r = 27/32 the loop's minimum is at positive pressure, so the whole lower lobe
    # is on the page and the two areas can be seen to be equal; below it the axis would clip it.
    t_start, t_end = 0.86, 0.9995
    sweep = t_start + (t_end - t_start) * _ease(np.linspace(0.0, 1.0, live))
    v_grid = np.geomspace(0.36, 6.0, 1500)
    _, dome_v, dome_p = _dome()

    fig, (left, right) = plt.subplots(1, 2, figsize=(10.4, 4.6), dpi=DPI,
                                      gridspec_kw={"width_ratios": [1.5, 1.0]})
    left.plot(dome_v, dome_p, color=GREY, lw=1.0, ls="--")
    left.plot([1.0], [1.0], "o", color=BLACK, ms=5)
    (isotherm,) = left.plot([], [], color=BLACK, lw=1.6)
    (flat,) = left.plot([], [], color=RED, lw=2.2)
    spinodals = left.scatter([], [], s=28, color=AMBER, zorder=5)
    left.set_xlim(0.3, 5.0)
    left.set_ylim(0.0, 1.15)
    left.set_xlabel(r"$v / v_c$")
    left.set_ylabel(r"$P / P_c$")
    left.spines[["top", "right"]].set_visible(False)

    (loop,) = right.plot([], [], color=BLACK, lw=1.4)
    (cross,) = right.plot([], [], "o", color=RED, ms=7)
    (p_line,) = right.plot([], [], color=RED, lw=1.0, ls=":")
    right.axhline(0.0, color=GREY, lw=0.8)
    right.set_xlim(0.0, 1.15)
    right.set_ylim(-0.6, 0.6)
    right.set_xlabel(r"$P / P_c$")
    right.set_ylabel(r"$(\mu - \mu_{\mathrm{sat}}) / (P_c v_c)$")
    right.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fills: list = []

    def update(frame: int):
        t_r = float(sweep[min(frame, live - 1)])
        for artist in fills:
            artist.remove()
        fills.clear()
        p_iso = _isotherm_r(t_r, v_grid)
        isotherm.set_data(v_grid, p_iso)
        p_sat, v_l, v_g = (x / s for x, s in zip(
            phases.maxwell_construction(t_r * T_C, A, B), (P_C, V_C, V_C), strict=True))
        flat.set_data([v_l, v_g], [p_sat, p_sat])
        inside = (v_grid >= v_l) & (v_grid <= v_g)
        fills.append(left.fill_between(v_grid[inside], p_iso[inside], p_sat,
                                       where=p_iso[inside] <= p_sat, color=LIGHT_BLUE, lw=0))
        fills.append(left.fill_between(v_grid[inside], p_iso[inside], p_sat,
                                       where=p_iso[inside] >= p_sat, color=LIGHT_RED, lw=0))
        v_min, v_max = (v / V_C for v in phases.spinodal_volumes(t_r * T_C, A, B))
        spinodals.set_offsets(np.column_stack([[v_min, v_max],
                                               [_isotherm_r(t_r, v_min), _isotherm_r(t_r, v_max)]]))
        # The mu-P loop: parametric in v, shifted so the crossing sits at zero.
        mu = _mu_r(v_grid, t_r) - _mu_r(np.array([v_l]), t_r)[0]
        keep = (p_iso > 0.0) & (p_iso < 1.15)
        loop.set_data(p_iso[keep], mu[keep])
        cross.set_data([p_sat], [0.0])
        p_line.set_data([p_sat, p_sat], [-0.6, 0.0])
        return (isotherm, flat, spinodals, loop, cross, p_line, *fills)

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "phases-maxwell")
    plt.close(fig)


def render_coexistence(n_frames: int = 330, hold: int = 60) -> None:
    """The coexistence point climbs the P-T curve and stops where the curve ends."""
    live = n_frames - hold
    t_lo = 0.5
    t_path = t_lo + (1.0 - t_lo) * _ease(np.linspace(0.0, 1.0, live))
    t_path[-1] = 1.0
    p_path, vl_path, vg_path = phases.coexistence_curve(np.minimum(t_path, phases.T_RATIO_MAX)
                                                        * T_C, A, B)
    p_path[-1], vl_path[-1], vg_path[-1] = P_C, V_C, V_C
    _, dome_v, dome_p = _dome()
    sp_t, sp_v, sp_p = phases.spinodal_curve(A, B, n_points=200, t_min=t_lo)
    v_grid = np.geomspace(0.36, 80.0, 2000)

    fig, (left, right) = plt.subplots(1, 2, figsize=(10.4, 4.6), dpi=DPI)
    left.fill(dome_v, dome_p, color="#f1f5f9", lw=0)
    left.plot(dome_v, dome_p, color=GREY, lw=1.2)
    left.plot(sp_v / V_C, sp_p / P_C, color=AMBER, lw=1.0, ls=":")
    left.plot([1.0], [1.0], "o", color=BLACK, ms=5)
    (isotherm,) = left.plot([], [], color=BLACK, lw=1.4)
    (flat,) = left.plot([], [], color=RED, lw=2.2)
    (ends,) = left.plot([], [], "o", color=RED, ms=6)
    left.set_xscale("log")
    left.set_xlim(0.36, 60.0)
    left.set_ylim(0.0, 1.2)
    left.set_xlabel(r"$v / v_c$")
    left.set_ylabel(r"$P / P_c$")
    left.spines[["top", "right"]].set_visible(False)

    (curve,) = right.plot([], [], color=RED, lw=2.0)
    (point,) = right.plot([], [], "o", color=RED, ms=8)
    right.plot([1.0], [1.0], "o", mfc="white", mec=BLACK, mew=1.5, ms=8, zorder=6)
    right.axvline(1.0, color=GREY, lw=0.8, ls=":")
    right.set_xlim(0.45, 1.2)
    right.set_ylim(0.0, 1.2)
    right.set_xlabel(r"$T / T_c$")
    right.set_ylabel(r"$P / P_c$")
    right.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    def update(frame: int):
        index = min(frame, live - 1)
        t_r = float(t_path[index])
        isotherm.set_data(v_grid, _isotherm_r(t_r, v_grid))
        v_l, v_g, p_sat = vl_path[index] / V_C, vg_path[index] / V_C, p_path[index] / P_C
        flat.set_data([v_l, v_g], [p_sat, p_sat])
        ends.set_data([v_l, v_g], [p_sat, p_sat])
        curve.set_data(t_path[: index + 1], p_path[: index + 1] / P_C)
        point.set_data([t_r], [p_sat])
        return isotherm, flat, ends, curve, point

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "phases-coexistence")
    plt.close(fig)


def render_lever(n_frames: int = 300, hold: int = 45, t_r: float = 0.85) -> None:
    """A state point crosses the flat line; the cylinder's liquid level follows the lever rule."""
    live = n_frames - hold
    p_sat, v_l, v_g = (x / s for x, s in zip(
        phases.maxwell_construction(t_r * T_C, A, B), (P_C, V_C, V_C), strict=True))
    v_path = np.exp(np.log(0.75 * v_l) + (np.log(1.6 * v_g) - np.log(0.75 * v_l))
                    * _ease(np.linspace(0.0, 1.0, live)))
    v_grid = np.geomspace(0.36, 8.0, 1500)
    p_iso = _isotherm_r(t_r, v_grid)
    p_real = np.where((v_grid > v_l) & (v_grid < v_g), p_sat, p_iso)

    fig = plt.figure(figsize=(10.4, 4.6), dpi=DPI)
    left = fig.add_axes((0.07, 0.14, 0.50, 0.80))
    cyl = fig.add_axes((0.64, 0.14, 0.12, 0.80))
    bar = fig.add_axes((0.84, 0.14, 0.12, 0.80))
    left.plot(v_grid, p_iso, color=GREY, lw=1.0, ls="--")
    left.plot(v_grid, p_real, color=BLACK, lw=1.6)
    left.plot([v_l, v_g], [p_sat, p_sat], color=RED, lw=2.2)
    (point,) = left.plot([], [], "o", color=BLUE, ms=9, zorder=6)
    left.set_xscale("log")
    left.set_xlim(0.36, 8.0)
    left.set_ylim(0.0, 1.0)
    left.set_xticks([0.5, 1.0, 2.0, 5.0], ["0.5", "1", "2", "5"])
    left.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    left.set_xlabel(r"$v / v_c$")
    left.set_ylabel(r"$P / P_c$")
    left.spines[["top", "right"]].set_visible(False)

    # The cylinder: its height is v (per particle), the liquid fills x_l v_l of it.
    v_top = 1.6 * v_g
    cyl.set_xlim(0.0, 1.0)
    cyl.set_ylim(0.0, v_top)
    cyl.set_xticks([])
    cyl.set_ylabel(r"$v / v_c$")
    cyl.spines[["top", "right", "bottom"]].set_visible(False)
    gas_box = Rectangle((0.15, 0.0), 0.7, 0.0, color="#fde68a", lw=0)
    liquid_box = Rectangle((0.15, 0.0), 0.7, 0.0, color=BLUE, alpha=0.75, lw=0)
    frame_box = Rectangle((0.15, 0.0), 0.7, 0.0, fill=False, lw=1.5, ec=BLACK)
    for patch in (gas_box, liquid_box, frame_box):
        cyl.add_patch(patch)

    bar.set_xlim(0.0, 1.0)
    bar.set_ylim(0.0, 1.0)
    bar.set_xticks([])
    bar.set_ylabel(r"$x_\ell$ , $x_g$")
    bar.spines[["top", "right", "bottom"]].set_visible(False)
    liquid_bar = Rectangle((0.15, 0.0), 0.7, 0.0, color=BLUE, alpha=0.75, lw=0)
    gas_bar = Rectangle((0.15, 0.0), 0.7, 0.0, color=AMBER, alpha=0.9, lw=0)
    bar.add_patch(liquid_bar)
    bar.add_patch(gas_bar)

    def update(frame: int):
        v = float(v_path[min(frame, live - 1)])
        if v <= v_l:
            x_l, p = 1.0, float(_isotherm_r(t_r, np.array([v]))[0])
        elif v >= v_g:
            x_l, p = 0.0, float(_isotherm_r(t_r, np.array([v]))[0])
        else:
            x_l, _ = phases.lever_rule(v, v_l, v_g)
            p = p_sat
        point.set_data([v], [p])
        liquid_height = x_l * v_l
        liquid_box.set_height(liquid_height)
        gas_box.set_y(liquid_height)
        gas_box.set_height(v - liquid_height)
        frame_box.set_height(v)
        liquid_bar.set_height(x_l)
        gas_bar.set_y(x_l)
        gas_bar.set_height(1.0 - x_l)
        return point, liquid_box, gas_box, frame_box, liquid_bar, gas_bar

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "phases-lever")
    plt.close(fig)


def render_around_critical(n_frames: int = 330, hold: int = 60) -> None:
    """Across the curve the density jumps; around its end it never does."""
    live = n_frames - hold
    t_r = np.linspace(phases.T_RATIO_MIN, phases.T_RATIO_MAX, 300)
    p_sat, _, _ = phases.coexistence_curve(t_r * T_C, A, B)
    # Path B must pass ABOVE P_c as well as beyond T_c: at any pressure below P_c a leg that
    # returns to T_r = 0.85 still crosses the coexistence curve.
    t_a, p_lo, p_hi = 0.85, 0.30, 1.15
    t_far = 1.20
    s = np.linspace(0.0, 1.0, live)
    # Path A: straight up at T_r = 0.85, through P_sat.
    path_a = np.column_stack([np.full(live, t_a), p_lo + (p_hi - p_lo) * s])
    # Path B: right, up past the critical point, back left -- three legs of equal length.
    leg = np.clip(3.0 * s[:, None] - np.arange(3)[None, :], 0.0, 1.0)
    path_b = np.column_stack([
        t_a + (t_far - t_a) * leg[:, 0] - (t_far - t_a) * leg[:, 2],
        p_lo + (p_hi - p_lo) * leg[:, 1],
    ])

    def density(path: np.ndarray) -> np.ndarray:
        v = phases.equilibrium_volume(path[:, 1] * P_C, path[:, 0] * T_C, A, B)
        return V_C / v

    rho_a, rho_b = density(path_a), density(path_b)

    fig, (left, right) = plt.subplots(1, 2, figsize=(10.4, 4.6), dpi=DPI)
    left.plot(t_r, p_sat / P_C, color=BLACK, lw=2.0)
    left.plot([1.0], [1.0], "o", mfc="white", mec=BLACK, mew=1.5, ms=8, zorder=6)
    left.plot(path_a[:, 0], path_a[:, 1], color=RED, lw=1.0, ls=":")
    left.plot(path_b[:, 0], path_b[:, 1], color=BLUE, lw=1.0, ls=":")
    (dot_a,) = left.plot([], [], "o", color=RED, ms=9)
    (dot_b,) = left.plot([], [], "o", color=BLUE, ms=9)
    left.set_xlim(0.6, 1.27)
    left.set_ylim(0.0, 1.3)
    left.set_xlabel(r"$T / T_c$")
    left.set_ylabel(r"$P / P_c$")
    left.spines[["top", "right"]].set_visible(False)

    (trace_a,) = right.plot([], [], color=RED, lw=2.0)
    (trace_b,) = right.plot([], [], color=BLUE, lw=2.0)
    (head_a,) = right.plot([], [], "o", color=RED, ms=8)
    (head_b,) = right.plot([], [], "o", color=BLUE, ms=8)
    right.set_xlim(0.0, 1.0)
    right.set_ylim(0.0, 1.05 * max(rho_a.max(), rho_b.max()))
    right.set_xlabel(r"$s$")
    right.set_ylabel(r"$\rho / \rho_c$")
    right.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    def update(frame: int):
        end = min(frame, live - 1) + 1
        dot_a.set_data([path_a[end - 1, 0]], [path_a[end - 1, 1]])
        dot_b.set_data([path_b[end - 1, 0]], [path_b[end - 1, 1]])
        trace_a.set_data(s[:end], rho_a[:end])
        trace_b.set_data(s[:end], rho_b[:end])
        head_a.set_data([s[end - 1]], [rho_a[end - 1]])
        head_b.set_data([s[end - 1]], [rho_b[end - 1]])
        return dot_a, dot_b, trace_a, trace_b, head_a, head_b

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "phases-around-critical")
    plt.close(fig)


def render_wiggle_vs_data() -> None:
    """The opening puzzle: module 02's real CO2 plateau against the bare loop at 280 K."""
    rows = np.loadtxt(ROOT / "data" / "co2-isotherm-280k.csv", delimiter=",", comments="#")
    t, p_data, v_molar = rows[:, 0], rows[:, 1], rows[:, 2]
    v_data = v_molar / 6.02214076e23
    v_grid = np.geomspace(1.08 * B, 7.0e-4 / 6.02214076e23, 1500)
    p_model = gases.van_der_waals_pressure(v_grid, 280.0, A, B)
    p_sat, v_l, v_g = phases.maxwell_construction(280.0, A, B)

    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=DPI)
    ax.plot(v_grid / V_C, p_model / 1e6, color=BLACK, lw=1.6)
    ax.plot([v_l / V_C, v_g / V_C], [p_sat / 1e6, p_sat / 1e6], color=RED, lw=2.2)
    ax.plot(v_data / V_C, p_data / 1e6, "o", color=BLUE, ms=5)
    ax.set_xscale("log")
    ax.set_xlim(0.35, 6.0)
    ax.set_ylim(0.0, 8.0)
    ax.set_xticks([0.5, 1.0, 2.0, 5.0], ["0.5", "1", "2", "5"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel(r"$v / v_c$")
    ax.set_ylabel(r"$P$ (MPa)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_still(fig, "phases-wiggle-vs-data")
    plt.close(fig)
    print(f"[wiggle] T = {t[0]:.0f} K: model P_sat = {p_sat / 1e6:.3f} MPa, "
          f"data plateau = {p_data[np.argmin(np.abs(v_molar - 2e-4))] / 1e6:.3f} MPa")


def render_water_diagram() -> None:
    """Water's real phase diagram beside the van der Waals vaporization curve for water."""
    rows = np.genfromtxt(ROOT / "data" / "14-water-phase-boundaries.csv", delimiter=",",
                         comments="#")
    boundary, t, p = rows[:, 0].astype(int), rows[:, 1], rows[:, 2]
    a_w, b_w = gases.vdw_constants_from_critical(647.096, 22.064e6)
    t_model = np.linspace(0.45 * 647.096, phases.T_RATIO_MAX * 647.096, 200)
    p_model, _, _ = phases.coexistence_curve(t_model, a_w, b_w)

    fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=DPI)
    for which, color in ((0, GREY), (1, BLUE), (2, RED)):
        sel = boundary == which
        ax.plot(t[sel], p[sel], color=color, lw=2.0)
    ax.plot(t_model, p_model, color=RED, lw=1.2, ls="--")
    ax.plot([273.16], [611.657], "o", color=BLACK, ms=6)
    ax.plot([647.096], [22.064e6], "o", mfc="white", mec=BLACK, mew=1.5, ms=8)
    ax.text(230.0, 2e4, r"$\mathrm{s}$", fontsize=16, ha="center")
    ax.text(330.0, 3e7, r"$\ell$", fontsize=16, ha="center")
    ax.text(450.0, 2e3, r"$\mathrm{g}$", fontsize=16, ha="center")
    ax.annotate(r"$T_t$", (273.16, 611.657), xytext=(255.0, 60.0), fontsize=11,
                arrowprops=dict(arrowstyle="-", color=BLACK, lw=0.8))
    ax.annotate(r"$T_c$", (647.096, 22.064e6), xytext=(600.0, 1.5e8), fontsize=11,
                arrowprops=dict(arrowstyle="-", color=BLACK, lw=0.8))
    ax.set_yscale("log")
    ax.set_xlim(200.0, 680.0)
    ax.set_ylim(1e-1, 1e9)
    ax.set_xlabel(r"$T$ (K)")
    ax.set_ylabel(r"$P$ (Pa)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_still(fig, "phases-water-diagram")
    plt.close(fig)
    t_boil = 373.124
    p_boil, _, _ = phases.maxwell_construction(t_boil, a_w, b_w)
    print(f"[water] van der Waals P_sat at {t_boil} K: {p_boil / 1e3:.0f} kPa against 101 kPa;"
          f" L = {phases.latent_heat(t_boil, a_w, b_w) * 6.02214076e23 / 1e3:.1f} kJ/mol "
          f"against 40.7")


def main() -> None:
    render_wiggle_vs_data()
    render_maxwell()
    render_coexistence()
    render_lever()
    render_around_critical()
    render_water_diagram()
    print(f"[info] k_B T_c for CO2: {K_B * T_C:.3e} J")


if __name__ == "__main__":
    main()
