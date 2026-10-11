"""Render the demonstrations for module 16 (thermal radiation and the heat capacity of solids).

Three animations and one still, all driven by `thermolab.radiation` and the module's two data
files, so what a student watches is the code and the data they can load.

    radiation-dual-peak.mp4     the blackbody spectrum per unit frequency and per unit wavelength,
                                side by side, as T climbs from 3000 K to 8000 K; each panel marks
                                its own peak (solid) and the other panel's peak carried across by
                                lambda = c / nu (dashed), which never coincide. Each curve is
                                drawn at its own peak height, so shapes and positions compare
    radiation-catastrophe.mp4   Planck's u_nu against the classical Rayleigh-Jeans parabola as T
                                climbs from 1000 K to 6000 K, scaled to Planck's peak: the two
                                agree at low frequency and part company where a quantum costs a
                                few k_B T, a frequency that moves up with T
    radiation-solids.mp4        Einstein and Debye heat capacities over silver's measured lattice
                                heat capacity while theta_D sweeps (theta_E = sqrt(3/5) theta_D,
                                so the two agree when hot); then the axes switch to log-log and
                                the low-temperature failure of the Einstein model shows
    radiation-data.png          the module's two real-data tests: silver's C(T) against the fitted
                                Einstein and Debye curves with fractional residuals, and the
                                COBE/FIRAS microwave background against its fitted Planck curve
                                with residuals in units of the stated error

No words are burned into the frames -- symbols, numbers and the element symbol only -- so one
file serves both language sites and the explanation lives in the translated caption. See
`_common.py` for the format and its constraints.

Run:  uv run python media/render/render_radiation.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402

from _common import DPI, ROOT, save, save_still  # noqa: E402
from thermolab import radiation  # noqa: E402
from thermolab.constants import N_A, R_GAS  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
VISIBLE = "#fde68a"
C = radiation.C_LIGHT
VISIBLE_NM = (380.0, 750.0)
SILVER_MOLAR_MASS = 0.1078682  # kg/mol


def _style(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)


def _silver_lattice() -> tuple[np.ndarray, np.ndarray, float]:
    """Silver's molar C_P with the electrons' gamma T removed (gamma from the C/T vs T^2 line)."""
    t, cp = np.genfromtxt(ROOT / "data" / "16-silver-heat-capacity.csv", delimiter=",",
                          comments="#").T
    c = cp * SILVER_MOLAR_MASS
    low = t <= 6.0
    _, gamma = np.polyfit(t[low] ** 2, c[low] / t[low], 1)
    return t, c - gamma * t, float(gamma)


def render_dual_peak() -> None:
    """Twin panels through a temperature sweep; own peaks solid, carried-over peaks dashed."""
    # The Sun's 5772 K is put on the grid exactly, so the frame the animation pauses on is it.
    temperatures = np.unique(np.append(np.geomspace(3000.0, 8000.0, 150), 5772.0))
    nu = np.linspace(1e12, 1500e12, 900)
    lam = np.linspace(50e-9, 2500e-9, 900)

    fig, (ax_nu, ax_lam) = plt.subplots(1, 2, figsize=(10.4, 4.2), dpi=DPI)
    ax_nu.axvspan(C / (VISIBLE_NM[1] * 1e-9) / 1e12, C / (VISIBLE_NM[0] * 1e-9) / 1e12,
                  color=VISIBLE, alpha=0.6, lw=0)
    ax_lam.axvspan(*VISIBLE_NM, color=VISIBLE, alpha=0.6, lw=0)
    (curve_nu,) = ax_nu.plot([], [], color=BLUE, lw=2.2)
    (curve_lam,) = ax_lam.plot([], [], color=RED, lw=2.2)
    own_nu = ax_nu.axvline(0, color=BLUE, lw=1.6)
    other_nu = ax_nu.axvline(0, color=RED, lw=1.6, ls="--")
    own_lam = ax_lam.axvline(0, color=RED, lw=1.6)
    other_lam = ax_lam.axvline(0, color=BLUE, lw=1.6, ls="--")
    ax_nu.set_xlim(0, 1500)
    ax_lam.set_xlim(0, 2500)
    for ax in (ax_nu, ax_lam):
        ax.set_ylim(0, 1.15)
        ax.set_yticks([0, 0.5, 1.0])
        _style(ax)
    ax_nu.set_xlabel(r"$\nu$ (THz)")
    ax_nu.set_ylabel(r"$u_\nu \,/\, u_\nu^{\max}$")
    ax_lam.set_xlabel(r"$\lambda$ (nm)")
    ax_lam.set_ylabel(r"$u_\lambda \,/\, u_\lambda^{\max}$")
    label = fig.text(0.5, 0.95, "", ha="center", fontsize=12)
    fig.subplots_adjust(top=0.86, bottom=0.15, wspace=0.28)

    def draw(i):
        t = temperatures[i]
        nu_peak, lam_peak = radiation.wien_peak_nu(t), radiation.wien_peak_lambda(t)
        u_nu = radiation.planck_u_nu(nu, t)
        u_lam = radiation.planck_u_lambda(lam, t)
        curve_nu.set_data(nu / 1e12, u_nu / radiation.planck_u_nu(nu_peak, t))
        curve_lam.set_data(lam * 1e9, u_lam / radiation.planck_u_lambda(lam_peak, t))
        own_nu.set_xdata([nu_peak / 1e12] * 2)
        other_nu.set_xdata([C / lam_peak / 1e12] * 2)
        own_lam.set_xdata([lam_peak * 1e9] * 2)
        other_lam.set_xdata([C / nu_peak * 1e9] * 2)
        label.set_text(rf"$T = {t:.0f}\ \mathrm{{K}}$     "
                       rf"$\nu_{{\max}}\lambda_{{\max}}/c = {radiation.DUAL_PEAK_RATIO:.3f}$")
        return curve_nu, curve_lam, own_nu, other_nu, own_lam, other_lam, label

    sun = int(np.argmin(np.abs(temperatures - 5772.0)))
    frames = list(range(sun + 1)) + [sun] * 40 + list(range(sun, len(temperatures)))
    frames += [len(temperatures) - 1] * 40
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "radiation-dual-peak")
    plt.close(fig)
    t = 5772.0
    print(f"[dual-peak] 5772 K: lambda_max {radiation.wien_peak_lambda(t) * 1e9:.0f} nm, "
          f"c/nu_max {C / radiation.wien_peak_nu(t) * 1e9:.0f} nm")


def render_catastrophe() -> None:
    """Planck against Rayleigh-Jeans as T climbs, scaled to Planck's peak."""
    temperatures = np.geomspace(1000.0, 6000.0, 150)
    nu = np.linspace(1e11, 1500e12, 1200)

    fig, ax = plt.subplots(figsize=(8.0, 4.4), dpi=DPI)
    ax.axvspan(C / (VISIBLE_NM[1] * 1e-9) / 1e12, C / (VISIBLE_NM[0] * 1e-9) / 1e12,
               color=VISIBLE, alpha=0.6, lw=0)
    (planck,) = ax.plot([], [], color=BLUE, lw=2.4)
    (classical,) = ax.plot([], [], color=RED, lw=1.8, ls="--")
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, 1.6)
    ax.set_yticks([0, 0.5, 1.0, 1.5])
    ax.set_xlabel(r"$\nu$ (THz)")
    ax.set_ylabel(r"$u_\nu \,/\, u_\nu^{\max}$")
    _style(ax)
    label = ax.text(0.98, 0.93, "", transform=ax.transAxes, ha="right", fontsize=12)
    fig.tight_layout()

    def draw(i):
        t = temperatures[i]
        peak = radiation.planck_u_nu(radiation.wien_peak_nu(t), t)
        planck.set_data(nu / 1e12, radiation.planck_u_nu(nu, t) / peak)
        classical.set_data(nu / 1e12, radiation.rayleigh_jeans_u_nu(nu, t) / peak)
        label.set_text(rf"$T = {t:.0f}\ \mathrm{{K}}$")
        return planck, classical, label

    frames = list(range(len(temperatures))) + [len(temperatures) - 1] * 45
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "radiation-catastrophe")
    plt.close(fig)
    print("[catastrophe] rendered")


def render_solids() -> None:
    """Debye and Einstein curves sweeping theta over silver's data; then log-log."""
    t_ag, lattice, _ = _silver_lattice()
    dulong_petit = 3 * R_GAS
    ratio = np.sqrt(0.6)  # theta_E / theta_D for agreement at high T
    thetas = np.concatenate([np.linspace(120.0, 320.0, 80), np.linspace(320.0, 218.5, 50)])
    grid = np.geomspace(0.8, 320.0, 400)

    fig, ax = plt.subplots(figsize=(8.0, 4.6), dpi=DPI)
    ax.plot(t_ag, lattice / dulong_petit, "o", color=BLACK, ms=4, zorder=3)
    ax.axhline(1.0, color=GREY, ls="--", lw=1.0)
    (debye,) = ax.plot([], [], color=BLUE, lw=2.2)
    (einstein,) = ax.plot([], [], color=RED, lw=2.2)
    ax.set_xlabel(r"$T$ (K)")
    ax.set_ylabel(r"$C \,/\, 3R$")
    _style(ax)
    label = ax.text(0.97, 0.06, "", transform=ax.transAxes, ha="right", fontsize=12)
    ax.text(0.03, 0.92, r"$\mathrm{Ag}$", transform=ax.transAxes, fontsize=13)
    fig.tight_layout()
    n_linear = len(thetas)

    def draw(i):
        theta = thetas[min(i, n_linear - 1)]
        debye.set_data(grid, radiation.debye_heat_capacity(grid, theta, N_A) / dulong_petit)
        einstein.set_data(grid, radiation.einstein_heat_capacity(grid, ratio * theta, N_A)
                          / dulong_petit)
        if i < n_linear + 30:
            ax.set_xscale("linear")
            ax.set_yscale("linear")
            ax.set_xlim(0, 310)
            ax.set_ylim(0, 1.12)
        else:
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlim(0.8, 320)
            ax.set_ylim(1e-6, 2)
        label.set_text(rf"$\theta_D = {theta:.0f}\ \mathrm{{K}}$   "
                       rf"$\theta_E = {ratio * theta:.0f}\ \mathrm{{K}}$")
        return debye, einstein, label

    frames = list(range(n_linear + 30)) + [n_linear + 30] * 120
    animation = FuncAnimation(fig, draw, frames=frames, blit=False)
    save(animation, fig, "radiation-solids")
    plt.close(fig)
    print(f"[solids] final theta_D {thetas[-1]:.1f} K, theta_E {ratio * thetas[-1]:.1f} K")


def render_data() -> None:
    """Silver against both models; FIRAS against Planck. Residual strips beneath each."""
    t_ag, lattice, gamma = _silver_lattice()
    window = (t_ag >= 4) & (t_ag <= 100)
    debye = radiation.fit_debye_temperature(t_ag[window], lattice[window], N_A)
    einstein = radiation.fit_einstein_temperature(t_ag[window], lattice[window], N_A)
    grid = np.geomspace(1.0, 300.0, 400)

    wavenumber, intensity, _, sigma_k, _ = np.genfromtxt(
        ROOT / "data" / "16-cmb-firas-monopole.csv", delimiter=",", comments="#").T
    nu = 100 * C * wavenumber
    cmb = radiation.fit_blackbody_temperature(nu, intensity * 1e-20, sigma_k * 1e-23)
    fine = np.linspace(nu.min() * 0.9, nu.max() * 1.02, 400)

    fig = plt.figure(figsize=(12.0, 5.2), dpi=DPI)
    outer = fig.add_gridspec(1, 2, wspace=0.28)
    left = outer[0].subgridspec(2, 1, height_ratios=[2.2, 1.0], hspace=0.08)
    right = outer[1].subgridspec(2, 1, height_ratios=[2.2, 1.0], hspace=0.08)

    ax_c = fig.add_subplot(left[0])
    ax_cr = fig.add_subplot(left[1], sharex=ax_c)
    ax_c.loglog(t_ag, lattice, "o", color=BLACK, ms=3.5, zorder=3)
    ax_c.loglog(grid, radiation.debye_heat_capacity(grid, debye.value, N_A), color=BLUE, lw=2,
                label=rf"$\theta_D = {debye.value:.0f}\ \mathrm{{K}}$")
    ax_c.loglog(grid, radiation.einstein_heat_capacity(grid, einstein.value, N_A), color=RED,
                lw=2, label=rf"$\theta_E = {einstein.value:.0f}\ \mathrm{{K}}$")
    ax_c.axhline(3 * R_GAS, color=GREY, ls="--", lw=1.0)
    ax_c.text(1.15, 3 * R_GAS * 1.35, r"$3R$", color=GREY, fontsize=11)
    ax_c.text(0.04, 0.70, r"$\mathrm{Ag}$", transform=ax_c.transAxes, fontsize=13)
    ax_c.set_ylim(1e-4, 60)
    ax_c.set_ylabel(r"$C$ (J mol$^{-1}$ K$^{-1}$)")
    ax_c.legend(frameon=False, loc="lower right", fontsize=10)
    plt.setp(ax_c.get_xticklabels(), visible=False)
    ax_cr.semilogx(t_ag[window], debye.residuals, "o-", color=BLUE, ms=3, lw=1)
    ax_cr.semilogx(t_ag[window], einstein.residuals, "o-", color=RED, ms=3, lw=1)
    ax_cr.axhline(0, color=GREY, lw=1)
    ax_cr.set_ylim(-1.1, 0.6)
    ax_cr.set_xlabel(r"$T$ (K)")
    ax_cr.set_ylabel(r"$C_{\mathrm{model}}/C - 1$")

    ax_s = fig.add_subplot(right[0])
    ax_sr = fig.add_subplot(right[1], sharex=ax_s)
    ax_s.plot(fine / (100 * C), radiation.planck_radiance_nu(fine, cmb.value) * 1e20,
              color=BLUE, lw=2, label=rf"$T = {cmb.value:.4f}\ \mathrm{{K}}$")
    ax_s.plot(wavenumber, intensity, "o", color=BLACK, ms=3.5, zorder=3)
    ax_s.set_ylabel(r"$I_\nu$ (MJy sr$^{-1}$)")
    ax_s.legend(frameon=False, fontsize=10)
    plt.setp(ax_s.get_xticklabels(), visible=False)
    ax_sr.errorbar(wavenumber, cmb.residuals, yerr=1.0, fmt="o", color=BLACK, ms=3, lw=0.8)
    ax_sr.axhline(0, color=BLUE, lw=1)
    ax_sr.set_ylim(-3.5, 3.5)
    ax_sr.set_xlabel(r"$\tilde\nu$ (cm$^{-1}$)")
    ax_sr.set_ylabel(r"$\Delta I_\nu / \sigma$")
    for ax in (ax_c, ax_cr, ax_s, ax_sr):
        _style(ax)
    save_still(fig, "radiation-data")
    plt.close(fig)
    print(f"[data] gamma {gamma * 1e3:.4f} mJ/(mol K^2); Debye {debye.value:.1f} +- "
          f"{debye.sigma:.1f} K, Einstein {einstein.value:.1f} +- {einstein.sigma:.1f} K; "
          f"T_CMB {cmb.value:.6f} K, chi2 {cmb.chi_squared:.1f}/{cmb.degrees_of_freedom}")


def main() -> None:
    render_dual_peak()
    render_catastrophe()
    render_solids()
    render_data()


if __name__ == "__main__":
    main()
