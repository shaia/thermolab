"""Render the demonstrations for module 17 (quantum statistics).

Three animations and one still, all driven by `thermolab.quantum` and the silver data module 16
ships, so what a student watches is the code and the data they can load.

    quantum-occupations.mp4   left: the mean occupation of a state against eps / (k_B T) for
                              bosons, classical particles and fermions, each at its own mu,
                              all three at the same density and temperature, on a logarithmic
                              axis; right: eta = mu / (k_B T) against n lambda^3 for the three,
                              with a marker at the current density. The degeneracy parameter
                              n lambda^3 falls from 2.5 to 0.001 (the gas is heated at fixed
                              density) and the three curves merge
    quantum-bec.mp4           an ideal Bose gas cooled from 1.6 T_c to 0.02 T_c: left, a column
                              split into the ground state's share and the excited states';
                              middle, how the excited particles are spread over energy (area =
                              their share); right, N_0 / N against T / T_c -- the ideal curve,
                              the finite-box curves for N = 10^3 and 10^5, and the current point
    quantum-fermi-sea.mp4     the density of states g(eps) with the occupied part g n_FD
                              filled, as T / T_F falls from 1 to 0.01; a band of width 2 k_B T
                              about mu marks the electrons that can still be excited. Right,
                              C / (N k_B) against T / T_F with the linear Sommerfeld law and the
                              classical 3/2, and the current point
    quantum-metals.png        silver: C / T against T^2 below 6 K with the fitted line and the
                              free-electron gamma; and the electrons' share gamma T / C of the
                              measured heat capacity from 1 K to 300 K

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py`.

Run:  uv run python media/render/render_quantum.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, ROOT, save, save_still  # noqa: E402
from thermolab import quantum  # noqa: E402
from thermolab.constants import K_B, N_A  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
LIGHT_BLUE, DARK_BLUE = "#93c5fd", "#1e3a8a"
SILVER_MOLAR_MASS = 0.1078682  # kg/mol
SILVER_DENSITY = 10490.0       # kg/m^3


def _style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)


def render_occupations() -> None:
    """Three occupations at one density and temperature, heated until they merge."""
    degeneracy = np.geomspace(2.5, 1e-3, 150)
    curve_d = np.geomspace(1e-3, 3.0, 300)
    etas = {s: np.array([quantum.solve_eta(d, s) for d in curve_d]) for s in ("be", "mb", "fd")}
    x = np.linspace(0.0, 10.0, 600)
    colours = {"be": BLUE, "mb": BLACK, "fd": RED}
    styles = {"be": "-", "mb": "--", "fd": "-"}
    labels = {"be": r"$n_{\mathrm{BE}}$", "mb": r"$n_{\mathrm{MB}}$", "fd": r"$n_{\mathrm{FD}}$"}
    mu_labels = {"be": r"$\mu_{\mathrm{BE}}$", "mb": r"$\mu_{\mathrm{MB}}$",
                 "fd": r"$\mu_{\mathrm{FD}}$"}

    fig, (ax, ax_eta) = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=DPI,
                                     gridspec_kw={"width_ratios": [1.35, 1.0]})
    lines = {s: ax.plot([], [], color=colours[s], ls=styles[s], lw=2.2)[0] for s in colours}
    for k, s in enumerate(("be", "mb", "fd")):
        ax.text(0.82, 0.90 - 0.09 * k, labels[s], color=colours[s], fontsize=13,
                transform=ax.transAxes)
    ax.set_yscale("log")
    ax.set_xlim(0, 10)
    ax.set_ylim(3e-5, 30)
    ax.set_xlabel(r"$\varepsilon \,/\, k_{\mathrm{B}}T$")
    ax.set_ylabel(r"$\langle n \rangle \,/\, n\lambda^3$")
    _style(ax)

    for s in colours:
        ax_eta.plot(curve_d, etas[s], color=colours[s], ls=styles[s], lw=2.0)
        ax_eta.text(3.15, etas[s][-1], mu_labels[s], color=colours[s], fontsize=11, va="center")
    ax_eta.axhline(0.0, color=GREY, lw=1, ls=":")
    ax_eta.axvline(quantum.ZETA_3_2, color=BLUE, lw=1, ls=":")
    marker = ax_eta.axvline(1.0, color=AMBER, lw=1.8)
    dots = {s: ax_eta.plot([], [], "o", color=colours[s], ms=6)[0] for s in colours}
    ax_eta.set_xscale("log")
    ax_eta.set_xlim(7e-4, 6.0)
    ax_eta.set_ylim(-8, 3.5)
    ax_eta.set_xlabel(r"$n\lambda^3$")
    ax_eta.set_ylabel(r"$\mu \,/\, k_{\mathrm{B}}T$")
    _style(ax_eta)
    label = fig.text(0.5, 0.94, "", ha="center", fontsize=13)
    fig.subplots_adjust(top=0.86, bottom=0.15, left=0.07, right=0.95, wspace=0.28)

    def draw(i):
        d = float(degeneracy[i])
        for s in colours:
            eta = quantum.solve_eta(d, s)
            # k_B T = 1 in these units, so eps and mu are x and eta; a boson state at eta = 0
            # cannot be evaluated at x = 0 itself, so the grid starts one step in.
            xs = x[1:] if s == "be" else x
            # Divided by n lambda^3, the classical curve is the same e^-x in every frame.
            values = np.asarray(quantum.occupation(xs, eta, 1.0 / K_B, s)) / d
            lines[s].set_data(xs, values)
            dots[s].set_data([d], [eta])
        marker.set_xdata([d, d])
        label.set_text(rf"$n\lambda^3 = {d:.3g}$")
        return (*lines.values(), *dots.values(), marker, label)

    frames = [0] * 30 + list(range(len(degeneracy))) + [len(degeneracy) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "quantum-occupations")
    plt.close(fig)


def render_bec() -> None:
    """Cool an ideal Bose gas through T_c: ground state, excited spread, and N_0 / N."""
    temperatures = np.concatenate([np.linspace(1.6, 1.0, 50), np.linspace(1.0, 0.02, 110)[1:]])
    energy = np.linspace(1e-4, 6.0, 500)            # eps / (k_B T_c)
    t_curve = np.linspace(0.0, 1.6, 161)
    finite = {n: np.asarray(quantum.finite_box_condensate_fraction(n, t_curve))
              for n in (1000, 100_000)}

    fig, (ax_bar, ax_spread, ax_frac) = plt.subplots(
        1, 3, figsize=(12.8, 4.3), dpi=DPI, gridspec_kw={"width_ratios": [0.35, 1.25, 1.25]})
    ground_bar = ax_bar.bar([0], [0], width=0.6, color=DARK_BLUE)[0]
    excited_bar = ax_bar.bar([0], [1], width=0.6, color=LIGHT_BLUE)[0]
    ax_bar.set_xlim(-0.5, 0.5)
    ax_bar.set_ylim(0, 1)
    ax_bar.set_xticks([])
    ax_bar.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_bar.set_ylabel(r"$N_0/N \;\;|\;\; N_{\mathrm{ex}}/N$")
    _style(ax_bar)

    fill = [ax_spread.fill_between(energy, 0 * energy, color=LIGHT_BLUE)]
    (outline,) = ax_spread.plot([], [], color=BLUE, lw=2)
    ax_spread.set_xlim(0, 6)
    ax_spread.set_ylim(0, 0.62)
    ax_spread.set_xlabel(r"$\varepsilon \,/\, k_{\mathrm{B}}T_c$")
    ax_spread.set_ylabel(r"$(1/N)\,\mathrm{d}N_{\mathrm{ex}}/\mathrm{d}\varepsilon$")
    _style(ax_spread)

    ax_frac.plot(t_curve, quantum.condensate_fraction(t_curve, 1.0), color=BLACK, lw=2.2)
    ax_frac.plot(t_curve, finite[1000], color=GREY, lw=1.6, ls="--")
    ax_frac.plot(t_curve, finite[100_000], color=AMBER, lw=1.6, ls="--")
    ax_frac.text(0.86, 0.47, r"$10^3$", color=GREY, fontsize=11)
    ax_frac.text(0.98, 0.21, r"$10^5$", color=AMBER, fontsize=11)
    ax_frac.text(0.08, 0.06, r"$1-(T/T_c)^{3/2}$", color=BLACK, fontsize=11)
    (point,) = ax_frac.plot([], [], "o", color=DARK_BLUE, ms=9)
    ax_frac.axvline(1.0, color=GREY, lw=1, ls=":")
    ax_frac.set_xlim(0, 1.6)
    ax_frac.set_ylim(0, 1.03)
    ax_frac.set_xlabel(r"$T \,/\, T_c$")
    ax_frac.set_ylabel(r"$N_0 \,/\, N$")
    _style(ax_frac)
    label = fig.text(0.5, 0.94, "", ha="center", fontsize=13)
    fig.subplots_adjust(top=0.86, bottom=0.15, left=0.06, right=0.98, wspace=0.42)
    norm = 2.0 / np.sqrt(np.pi) / quantum.ZETA_3_2

    def draw(i):
        t = temperatures[i]
        eta = quantum.solve_eta(float(quantum.ZETA_3_2 / t**1.5), "be")
        # (eps - mu) / (k_B T) = (energy - eta t) / t, with energies in units of k_B T_c.
        occupied = np.asarray(quantum.bose_einstein(energy, eta * t, t / K_B))
        spread = norm * np.sqrt(energy) * occupied
        fraction = float(quantum.condensate_fraction(t, 1.0))
        ground_bar.set_height(fraction)
        excited_bar.set_y(fraction)
        excited_bar.set_height(1.0 - fraction)
        fill[0].remove()
        fill[0] = ax_spread.fill_between(energy, spread, color=LIGHT_BLUE, lw=0)
        outline.set_data(energy, spread)
        point.set_data([t], [fraction])
        label.set_text(rf"$T/T_c = {t:.2f}$     $N_0/N = {fraction:.2f}$")
        return ground_bar, excited_bar, outline, point, label

    critical = 49
    frames = list(range(critical + 1)) + [critical] * 30 + list(range(critical, len(temperatures)))
    frames += [len(temperatures) - 1] * 40
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "quantum-bec")
    plt.close(fig)


def render_fermi_sea() -> None:
    """The Fermi sea hardening into a step as T / T_F falls, and the heat capacity it leaves."""
    ratios = np.geomspace(1.0, 0.01, 150)
    energy = np.linspace(0.0, 2.2, 700)               # eps / eps_F
    density = 1.5 * np.sqrt(energy)                   # g(eps) per particle, in units of 1/eps_F
    # Electrons at copper's density; only the dimensionless ratios are drawn.
    n_e, m_e = 8.49e28, quantum.M_ELECTRON
    t_f = float(quantum.fermi_temperature(n_e, m_e))
    c_grid = np.geomspace(1e-3, 3.0, 120)
    c_curve = np.array([quantum.ideal_quantum_gas(n_e, r * t_f, m_e, "fd", 2)
                        .heat_capacity_per_particle / K_B for r in c_grid])
    states = [quantum.ideal_quantum_gas(n_e, r * t_f, m_e, "fd", 2) for r in ratios]

    fig, (ax_sea, ax_c) = plt.subplots(1, 2, figsize=(11.6, 4.4), dpi=DPI,
                                       gridspec_kw={"width_ratios": [1.3, 1.0]})
    ax_sea.plot(energy, density, color=GREY, lw=1.8)
    ax_sea.axvline(1.0, color=BLACK, lw=1, ls="--")
    fill = [ax_sea.fill_between(energy, 0 * energy, color=LIGHT_BLUE)]
    shell = [ax_sea.axvspan(0.9, 1.1, color=AMBER, alpha=0.25, lw=0)]
    (occupied,) = ax_sea.plot([], [], color=BLUE, lw=2)
    (mu_mark,) = ax_sea.plot([], [], "v", color=AMBER, ms=10)
    ax_sea.set_xlim(0, 2.2)
    ax_sea.set_ylim(0, 2.45)
    ax_sea.set_xlabel(r"$\varepsilon \,/\, \varepsilon_F$")
    ax_sea.set_ylabel(r"$g(\varepsilon)\,\varepsilon_F / N$")
    ax_sea.text(1.02, 2.3, r"$\varepsilon_F$", fontsize=12)
    _style(ax_sea)

    ax_c.loglog(c_grid, c_curve, color=BLUE, lw=2.2)
    ax_c.loglog(c_grid, np.pi**2 / 2 * c_grid, color=RED, lw=1.5, ls="--")
    ax_c.axhline(1.5, color=BLACK, lw=1.2, ls=":")
    ax_c.text(1.2e-3, 1.75, r"$3/2$", fontsize=11)
    ax_c.text(2e-3, 3.2e-2, r"$\frac{\pi^2}{2}\,\frac{T}{T_F}$", color=RED, fontsize=12)
    (c_point,) = ax_c.plot([], [], "o", color=AMBER, ms=9)
    ax_c.set_xlim(1e-3, 3.0)
    ax_c.set_ylim(3e-3, 4.0)
    ax_c.set_xlabel(r"$T \,/\, T_F$")
    ax_c.set_ylabel(r"$C_V \,/\, N k_{\mathrm{B}}$")
    _style(ax_c)
    label = fig.text(0.5, 0.94, "", ha="center", fontsize=13)
    fig.subplots_adjust(top=0.86, bottom=0.15, left=0.07, right=0.97, wspace=0.28)

    def draw(i):
        r = ratios[i]
        gas = states[i]
        mu = gas.mu / (K_B * t_f)                     # in units of eps_F
        # Energies in units of eps_F, so k_B T = r and the temperature argument is r / k_B.
        filled = density * np.asarray(quantum.occupation(energy, mu, r / K_B, "fd"))
        fill[0].remove()
        fill[0] = ax_sea.fill_between(energy, filled, color=LIGHT_BLUE, lw=0)
        shell[0].remove()
        shell[0] = ax_sea.axvspan(max(mu - r, 0.0), mu + r, color=AMBER, alpha=0.25, lw=0)
        occupied.set_data(energy, filled)
        mu_mark.set_data([max(mu, 0.0)], [2.2])
        c_point.set_data([r], [gas.heat_capacity_per_particle / K_B])
        label.set_text(rf"$T/T_F = {r:.3f}$     $\mu/\varepsilon_F = {mu:.3f}$")
        return occupied, mu_mark, c_point, label

    frames = [0] * 25 + list(range(len(ratios))) + [len(ratios) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "quantum-fermi-sea")
    plt.close(fig)


def render_metals() -> None:
    """Silver's electrons, measured: the C/T line and the electrons' share of C."""
    t, cp = np.genfromtxt(ROOT / "data" / "16-silver-heat-capacity.csv", delimiter=",",
                          comments="#").T
    c = cp * SILVER_MOLAR_MASS
    low = t <= 6.0
    fit = quantum.fit_metal_heat_capacity(t[low], c[low])
    n_e = SILVER_DENSITY / SILVER_MOLAR_MASS * N_A
    gamma_free = quantum.free_electron_gamma(n_e)

    fig, (ax_line, ax_share) = plt.subplots(1, 2, figsize=(11.0, 4.2), dpi=DPI)
    t2 = np.linspace(0.0, 37.0, 50)
    ax_line.plot(t[low] ** 2, c[low] / t[low] * 1e3, "o", color=BLACK, ms=6)
    ax_line.plot(t2, (fit.gamma + fit.beta * t2) * 1e3, color=BLUE, lw=2)
    ax_line.plot([0.0], [gamma_free * 1e3], "D", color=RED, ms=8, clip_on=False)
    ax_line.text(2.0, 6.2, rf"$\gamma = {fit.gamma * 1e3:.3f}$", color=BLUE, fontsize=12)
    ax_line.text(2.0, 5.5, rf"$\gamma_{{\mathrm{{free}}}} = {gamma_free * 1e3:.3f}$", color=RED,
                 fontsize=12)
    ax_line.set_xlim(0, 37)
    ax_line.set_ylim(0, 7.0)
    ax_line.set_xlabel(r"$T^2\ (\mathrm{K}^2)$")
    ax_line.set_ylabel(r"$C/T\ (\mathrm{mJ\,mol^{-1}\,K^{-2}})$")
    ax_line.set_title("Ag", fontsize=12)
    _style(ax_line)

    share = fit.gamma * t / c
    ax_share.semilogx(t, share, "o", color=BLACK, ms=4)
    ax_share.axhline(0.5, color=GREY, lw=1, ls=":")
    ax_share.set_ylim(0, 1)
    ax_share.set_xlim(0.9, 330)
    ax_share.set_xlabel(r"$T\ (\mathrm{K})$")
    ax_share.set_ylabel(r"$\gamma T \,/\, C$")
    ax_share.set_title("Ag", fontsize=12)
    _style(ax_share)
    fig.tight_layout()
    save_still(fig, "quantum-metals")
    plt.close(fig)
    print(f"[metals] gamma = {fit.gamma * 1e3:.4f} +- {fit.gamma_sigma * 1e3:.4f} mJ/(mol K^2), "
          f"free electron {gamma_free * 1e3:.4f}; electrons' share at 1 K {share[0]:.2f}, "
          f"at 300 K {share[-1]:.4f}")


if __name__ == "__main__":
    render_occupations()
    render_bec()
    render_fermi_sea()
    render_metals()
