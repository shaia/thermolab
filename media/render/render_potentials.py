"""Render the demonstrations for module 10 (thermodynamic potentials).

Three animations and two stills, all built from `thermolab.potentials` and
`thermolab.fundamental`, so what a student watches is the model they can read and run:

    potentials-tangent-envelope.mp4  tangents sweep the Einstein solid's convex U(S); their
                                     intercepts trace F(T); then the tangents alone rebuild U(S)
    potentials-minimization.mp4      a piston between two samples of a van der Waals gas at the
                                     bath's temperature: F falls, U rises, S_total climbs
    potentials-maxwell-gap.mp4       the cross-derivative gap of dF shrinking as the step
                                     refines -- and a mismatched pair whose gap does not
    potentials-map.png               the four energy potentials and the trades between them
    potentials-dent.png              a dented F(V) below the critical temperature, and the
                                     multivalued G(P) its tangents trace

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py` for the
format and its constraints.

Run:  uv run python media/render/render_potentials.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
from matplotlib.colors import LogNorm  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from _common import DPI, save, save_still  # noqa: E402
from thermolab import fundamental, gases, potentials  # noqa: E402
from thermolab.constants import AMU, K_B, N_A  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
QUANTUM = 5.0 * K_B
ARGON_MASS = 39.948 * AMU
VDW_A = 0.1355 / N_A**2  # argon, per particle
VDW_B = 3.201e-5 / N_A


def render_tangent_envelope(n_frames: int = 300) -> None:
    """U(S) of an Einstein solid, per oscillator, with its tangent lines and their intercepts.

    First half: one tangent slides along the curve. Its slope is T and its intercept on the
    S = 0 axis is U - TS = F; the right panel traces F against T as it goes. Second half: the
    curve is hidden and the tangents are laid down one by one, each dotted into the right panel
    as a point (T, F) -- and their envelope rebuilds the curve they came from. That is the
    claim the page makes: the tangents, as a family, know everything the curve did.
    """
    n = 100.0
    solid = fundamental.einstein_solid(QUANTUM)
    q = np.linspace(0.02, 3.2, 1200) * n  # quanta
    u = q * QUANTUM
    s = np.asarray(solid(u, 1.0, n))
    temperature, helmholtz = potentials.legendre_transform(u, s)
    # Per oscillator, in the solid's own units: U/(n eps), S/(n k_B), T in eps/k_B.
    x, y = s / (n * K_B), u / (n * QUANTUM)
    tt, ff = temperature * K_B / QUANTUM, helmholtz / (n * QUANTUM)

    half = n_frames // 2
    sweep = 0.03 + 0.94 * (0.5 - 0.5 * np.cos(np.linspace(0.0, np.pi, half)))
    family = np.linspace(0.02, 0.98, 36)

    fig, (left, right) = plt.subplots(1, 2, figsize=(9.6, 4.2), dpi=DPI)
    (curve,) = left.plot(x, y, color=BLACK, lw=2.4)
    left.axvline(0.0, color=GREY, lw=1.0)
    left.axhline(0.0, color=GREY, lw=0.8)
    left.set_xlim(-0.1, 2.5)
    left.set_ylim(-5.4, 3.6)
    left.set_xlabel(r"$S / n k_{\mathrm{B}}$")
    left.set_ylabel(r"$U / n\varepsilon$")
    (tangent,) = left.plot([], [], color=RED, lw=1.6)
    (touch,) = left.plot([], [], "o", color=RED, ms=7)
    (intercept,) = left.plot([], [], "o", color=BLUE, ms=8)
    family_lines = [left.plot([], [], color=RED, lw=0.9, alpha=0.55)[0] for _ in family]

    right.plot(tt, ff, color=GREY, lw=1.0, ls=":")
    right.set_xlim(0.0, float(tt.max()) * 1.04)
    right.set_ylim(-5.4, 0.4)
    right.axhline(0.0, color=GREY, lw=0.8)
    right.set_xlabel(r"$k_{\mathrm{B}} T / \varepsilon$")
    right.set_ylabel(r"$F / n\varepsilon$")
    (trace,) = right.plot([], [], color=BLUE, lw=2.2)
    (dot,) = right.plot([], [], "o", color=BLUE, ms=8)
    (points,) = right.plot([], [], "o", color=RED, ms=4)
    fig.tight_layout()
    s_line = np.array([-0.1, 2.5])

    def index(fraction: float) -> int:
        return int(np.clip(round(fraction * (x.size - 1)), 0, x.size - 1))

    def update(frame: int):
        if frame < half:
            i = index(sweep[frame])
            curve.set_alpha(1.0)
            tangent.set_data(s_line, ff[i] + tt[i] * s_line)
            touch.set_data([x[i]], [y[i]])
            intercept.set_data([0.0], [ff[i]])
            upto = i + 1
            trace.set_data(tt[:upto], ff[:upto])
            dot.set_data([tt[i]], [ff[i]])
            for line in family_lines:
                line.set_data([], [])
            points.set_data([], [])
        else:
            k = int((frame - half) / (n_frames - half) * (family.size + 6))
            curve.set_alpha(0.12)
            tangent.set_data([], [])
            touch.set_data([], [])
            intercept.set_data([], [])
            trace.set_data([], [])
            dot.set_data([], [])
            shown = [index(f) for f in family[: min(k, family.size)]]
            for line, i in zip(family_lines, [index(f) for f in family], strict=True):
                line.set_data((s_line, ff[i] + tt[i] * s_line) if i in shown else ([], []))
            points.set_data(tt[shown], ff[shown])
        return (tangent, touch, intercept, trace, dot, points, curve, *family_lines)

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig,
         "potentials-tangent-envelope")
    plt.close(fig)


def render_minimization(n_frames: int = 240) -> None:
    """A braked piston between two samples of van der Waals argon, the box in a 300 K bath.

    Left: the box, shaded by density, with the piston moving from its prepared position to
    where the pressures agree. Right, above: the composite's energy, rising. Right, below: its
    free energy falling, and the total entropy of system plus bath, times T, rising by exactly
    as much. The trace is `potentials.free_energy_minimization`, not a sketch.
    """
    vdw = potentials.van_der_waals_gas(ARGON_MASS, VDW_A, VDW_B)
    t_bath, volume = 300.0, 4e-3
    trace = potentials.free_energy_minimization(vdw, t_bath, volume, 2 * N_A, N_A,
                                                start_share=0.25, n_steps=n_frames // 2)
    hold = n_frames - trace.share.size
    order = np.r_[np.zeros(hold // 2, dtype=int), np.arange(trace.share.size),
                  np.full(hold - hold // 2, trace.share.size - 1)]
    progress = np.linspace(0.0, 1.0, trace.share.size)
    d_u = trace.energy - trace.energy[0]
    d_f = trace.free_energy - trace.free_energy[0]
    t_ds = t_bath * trace.total_entropy_change

    fig = plt.figure(figsize=(9.6, 4.4), dpi=DPI)
    box = fig.add_axes((0.03, 0.12, 0.36, 0.78))
    top = fig.add_axes((0.52, 0.58, 0.45, 0.34))
    bottom = fig.add_axes((0.52, 0.12, 0.45, 0.40), sharex=top)

    box.set_xlim(-0.08, 1.08)
    box.set_ylim(-0.12, 1.12)
    box.axis("off")
    box.add_patch(Rectangle((-0.06, -0.10), 1.12, 1.20, color=AMBER, alpha=0.25, lw=0))
    box.add_patch(Rectangle((0.0, 0.0), 1.0, 1.0, fill=False, lw=2.4, ec=BLACK))
    side_a = Rectangle((0.0, 0.0), 0.25, 1.0, color=BLUE, lw=0)
    side_b = Rectangle((0.25, 0.0), 0.75, 1.0, color=BLUE, lw=0)
    box.add_patch(side_a)
    box.add_patch(side_b)
    (piston,) = box.plot([0.25, 0.25], [0.0, 1.0], color=BLACK, lw=5)
    density_a = 2.0 / trace.share
    density_b = 1.0 / (1.0 - trace.share)
    top_density = float(max(density_a.max(), density_b.max()))

    top.plot(progress, d_u, color=GREY, lw=1.0, ls=":")
    top.set_ylabel(r"$\Delta U$ (J)")
    top.set_ylim(-0.1 * d_u.max(), 1.2 * d_u.max())
    top.tick_params(labelbottom=False)
    (u_line,) = top.plot([], [], color=RED, lw=2.2)
    bottom.plot(progress, d_f, color=GREY, lw=1.0, ls=":")
    bottom.plot(progress, t_ds, color=GREY, lw=1.0, ls=":")
    bottom.axhline(0.0, color=GREY, lw=0.8)
    bottom.set_ylabel("J")
    bottom.set_xlabel(r"$(V_A - V_{A,0}) / (V_{A,\mathrm{eq}} - V_{A,0})$")
    (f_line,) = bottom.plot([], [], color=BLUE, lw=2.2, label=r"$\Delta F$")
    (s_line,) = bottom.plot([], [], color=BLACK, lw=2.2, label=r"$T\,\Delta S_{\mathrm{tot}}$")
    bottom.legend(loc="center right", frameon=False)

    def shade(density: float) -> float:
        return 0.15 + 0.8 * density / top_density

    def update(frame: int):
        i = int(order[frame])
        x = float(trace.share[i])
        side_a.set_width(x)
        side_b.set_x(x)
        side_b.set_width(1.0 - x)
        side_a.set_alpha(shade(float(density_a[i])))
        side_b.set_alpha(shade(float(density_b[i])))
        piston.set_data([x, x], [0.0, 1.0])
        u_line.set_data(progress[: i + 1], d_u[: i + 1])
        f_line.set_data(progress[: i + 1], d_f[: i + 1])
        s_line.set_data(progress[: i + 1], t_ds[: i + 1])
        return side_a, side_b, piston, u_line, f_line, s_line

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "potentials-minimization")
    plt.close(fig)


def render_maxwell_gap(n_frames: int = 180) -> None:
    """|gap| of dF = -S dT - P dV over (T, V) as the difference step shrinks, log colour scale.

    Above: van der Waals argon, S and P both read off its one relation -- the map darkens by a
    factor of four for every halving of the step, because what is left is truncation error.
    Below: the ideal gas's S paired with van der Waals P, two substances pretending to be one --
    the map does not darken at all. The step, shown on the right, sweeps from 1e-1 to 1e-3.
    """
    genuine = potentials.van_der_waals_gas(ARGON_MASS, VDW_A, VDW_B)
    ideal = fundamental.monatomic_ideal_gas(ARGON_MASS)
    n = N_A
    t_axis = np.linspace(200.0, 600.0, 48)
    v_axis = np.geomspace(1.5e-4, 5e-3, 48)
    tt, vv = np.meshgrid(t_axis, v_axis)
    m_true, n_true = potentials.helmholtz_form(genuine, n)
    m_fake, _ = potentials.helmholtz_form(ideal, n)

    half = n_frames // 2
    steps = np.r_[np.geomspace(1e-1, 1e-3, half), np.geomspace(1e-3, 1e-1, n_frames - half)]
    unique = np.geomspace(1e-1, 1e-3, half)
    gaps_true = [np.abs(potentials.maxwell_check(m_true, n_true, tt, vv, rel_step=h))
                 for h in unique]
    gap_fake = np.abs(potentials.maxwell_check(m_fake, n_true, tt, vv, rel_step=1e-3))
    worst_true = np.array([g.max() for g in gaps_true])

    norm = LogNorm(vmin=1e-7, vmax=1e-1)
    fig = plt.figure(figsize=(9.6, 5.6), dpi=DPI)
    above = fig.add_axes((0.08, 0.55, 0.42, 0.38))
    below = fig.add_axes((0.08, 0.09, 0.42, 0.38), sharex=above)
    curve = fig.add_axes((0.64, 0.18, 0.33, 0.66))
    extent = (t_axis[0], t_axis[-1], np.log10(v_axis[0]), np.log10(v_axis[-1]))
    image_true = above.imshow(gaps_true[0], origin="lower", aspect="auto", extent=extent,
                              norm=norm, cmap="magma")
    below.imshow(gap_fake, origin="lower", aspect="auto", extent=extent, norm=norm,
                 cmap="magma")
    for ax in (above, below):
        ax.set_ylabel(r"$\log_{10}(V / \mathrm{m^3})$")
    below.set_xlabel(r"$T$ (K)")
    above.tick_params(labelbottom=False)
    colour = fig.colorbar(image_true, ax=[above, below], pad=0.02, fraction=0.05)
    colour.set_label(r"$|\Delta|$")

    curve.loglog(unique, worst_true, color=GREY, lw=1.0, ls=":")
    curve.loglog(unique, np.full_like(unique, gap_fake.max()), color=GREY, lw=1.0, ls=":")
    curve.set_xlabel(r"$h$")
    curve.set_ylabel(r"$\max\,|\Delta|$")
    curve.set_xlim(1.2e-1, 8e-4)
    curve.set_ylim(1e-8, 1.0)
    (track,) = curve.loglog([], [], color=RED, lw=2.2)
    (dot_true,) = curve.loglog([], [], "o", color=RED, ms=8)
    (dot_fake,) = curve.loglog([], [], "s", color=BLACK, ms=7)

    def update(frame: int):
        h = steps[frame]
        k = int(np.argmin(np.abs(np.log(unique) - np.log(h))))
        image_true.set_data(gaps_true[k])
        track.set_data(unique[: k + 1], worst_true[: k + 1])
        dot_true.set_data([unique[k]], [worst_true[k]])
        dot_fake.set_data([unique[k]], [gap_fake.max()])
        return image_true, track, dot_true, dot_fake

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "potentials-maxwell-gap")
    plt.close(fig)


def render_map() -> None:
    """The four energy potentials at the corners of a square, and the trades between them.

    Moving right trades S for T (subtract TS); moving down trades V for P (add PV). Each box
    carries the potential's natural variables and its differential -- symbols only.
    """
    fig, ax = plt.subplots(figsize=(7.6, 5.2), dpi=DPI)
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(0.0, 7.0)
    ax.axis("off")
    d = r"\mathrm{d}"
    corners = {
        "U": (2.4, 5.2, r"$U(S, V, N)$", rf"${d}U = T\,{d}S - P\,{d}V + \mu\,{d}N$"),
        "F": (7.6, 5.2, r"$F(T, V, N)$", rf"${d}F = -S\,{d}T - P\,{d}V + \mu\,{d}N$"),
        "H": (2.4, 1.8, r"$H(S, P, N)$", rf"${d}H = T\,{d}S + V\,{d}P + \mu\,{d}N$"),
        "G": (7.6, 1.8, r"$G(T, P, N)$", rf"${d}G = -S\,{d}T + V\,{d}P + \mu\,{d}N$"),
    }
    colours = {"U": BLACK, "F": BLUE, "H": AMBER, "G": RED}
    for key, (x, y, head, diff) in corners.items():
        ax.add_patch(Rectangle((x - 2.2, y - 0.9), 4.4, 1.8, fill=False, lw=2.0,
                               ec=colours[key]))
        ax.text(x, y + 0.3, head, ha="center", va="center", fontsize=15, color=colours[key])
        ax.text(x, y - 0.4, diff, ha="center", va="center", fontsize=10.5, color=BLACK)

    def arrow(start, end, label, offset):
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16, lw=1.6,
                                     color=GREY))
        mid = ((start[0] + end[0]) / 2 + offset[0], (start[1] + end[1]) / 2 + offset[1])
        ax.text(*mid, label, ha="center", va="center", fontsize=13, color=BLACK)

    arrow((4.7, 5.2), (5.3, 5.2), r"$-TS$", (0.0, 0.35))
    arrow((4.7, 1.8), (5.3, 1.8), r"$-TS$", (0.0, 0.35))
    arrow((2.4, 4.2), (2.4, 2.8), r"$+PV$", (0.55, 0.0))
    arrow((7.6, 4.2), (7.6, 2.8), r"$+PV$", (0.55, 0.0))
    fig.tight_layout()
    save_still(fig, "potentials-map")
    plt.close(fig)


def render_dent() -> None:
    """Below T_c: van der Waals F(V) with a dent, and the G(P) its tangents trace -- a fold.

    Left: F against V at 0.85 T_c, tilted by the straight line P_bar V (P_bar midway between the
    loop's two turning pressures) so the dent is visible at all -- adding a straight line
    changes no curvature, and the stretch where F curves the wrong way is drawn in red.
    Right: each tangent's slope gives P = -dF/dV and its intercept F + PV gives G. Along the
    healthy stretches G(P) is a single curve; where the tangents come from the dent it folds
    back on itself, and three values of G share one pressure. The transform has not lost the
    dent -- it has lost the ability to say which of the three states it means.
    """
    vdw = potentials.van_der_waals_gas(ARGON_MASS, VDW_A, VDW_B)
    _, t_c, _ = gases.vdw_critical_point(VDW_A, VDW_B)
    temperature = 0.85 * t_c
    nb = N_A * VDW_B
    v = np.geomspace(1.45 * nb, 200.0 * nb, 6000)
    f = np.asarray(potentials.helmholtz_from(vdw, temperature, v, N_A))
    slope, g = potentials.tangent_intercepts(f, v)
    p = -slope
    dented = np.gradient(slope, v) < 0
    p_low, p_high = float(p[dented].min()), float(p[dented].max())
    p_bar = 0.5 * (p_low + p_high)

    fig, (left, right) = plt.subplots(1, 2, figsize=(9.6, 4.0), dpi=DPI)
    scale_f = N_A * K_B * temperature
    tilted = (f + p_bar * v) / scale_f
    window = v < 32.0 * nb
    left.plot(v[window] / nb, tilted[window], color=BLACK, lw=2.0)
    left.plot(np.where(dented & window, v / nb, np.nan), np.where(dented, tilted, np.nan),
              color=RED, lw=3.0)
    left.set_xlabel(r"$V / N b$")
    left.set_ylabel(r"$(F + \bar{P} V) / N k_{\mathrm{B}} T$")
    keep = (p > 0.4 * p_low) & (p < 1.25 * p_high)
    right.plot(np.where(keep & ~dented, p, np.nan) / 1e5,
               np.where(keep & ~dented, g, np.nan) / scale_f, color=BLACK, lw=2.0)
    right.plot(np.where(keep & dented, p, np.nan) / 1e5,
               np.where(keep & dented, g, np.nan) / scale_f, color=RED, lw=2.0)
    # Frame the fold: the gas branch's ln P tail would otherwise flatten it into a line.
    fold = keep & dented
    g_low, g_high = float(g[fold].min()) / scale_f, float(g[fold].max()) / scale_f
    span = g_high - g_low
    right.set_xlim(0.5 * p_low / 1e5, 1.15 * p_high / 1e5)
    right.set_ylim(g_low - 1.2 * span, g_high + 0.4 * span)
    right.set_xlabel(r"$P$ (bar)")
    right.set_ylabel(r"$G / N k_{\mathrm{B}} T$")
    for ax, label in ((left, "(a)"), (right, "(b)")):
        ax.set_title(label, loc="left")
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    fig.tight_layout()
    save_still(fig, "potentials-dent")
    plt.close(fig)


def main() -> None:
    render_map()
    render_dent()
    render_tangent_envelope()
    render_minimization()
    render_maxwell_gap()


if __name__ == "__main__":
    main()
