"""Render the demonstration animations for module 02 (equations of state).

Animations are produced from `thermolab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_gases.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
from mpl_toolkits.mplot3d import Axes3D  # noqa: E402,F401  (registers the 3D projection)

from _common import DPI, save  # noqa: E402
from thermolab import gases  # noqa: E402

# CO2's van der Waals constants, fit from its measured critical point (NIST Chemistry
# WebBook: T_c = 304.13 K, P_c = 7.3773e6 Pa) via `vdw_constants_from_critical` -- the same
# path the laboratory notebook uses, so the surface these animations show is exactly the one
# a student reproduces there.
CO2_T_C = 304.13  # K
CO2_P_C = 7.3773e6  # Pa
A_CO2, B_CO2 = gases.vdw_constants_from_critical(CO2_T_C, CO2_P_C)


def render_pvt_surface(n_frames: int = 120) -> None:
    """A rotating van der Waals P-v-T surface that morphs on from the flat ideal sheet.

    The first half of the animation interpolates a, b from 0 (the ideal gas) up to CO2's
    values while the camera keeps rotating, so the fold below T_c visibly grows out of a flat
    surface rather than appearing fully formed -- the module page's centrepiece figure.
    """
    v_min = 1.2 * B_CO2
    v_c, t_c, _p_c = gases.vdw_critical_point(A_CO2, B_CO2)
    v_grid = np.linspace(v_min, 6.0 * v_c, 45)
    t_grid = np.linspace(0.6 * t_c, 1.6 * t_c, 45)

    fig = plt.figure(figsize=(7.0, 5.5), dpi=DPI)
    ax = fig.add_subplot(projection="3d")

    n_morph = n_frames // 2
    p_full = gases.van_der_waals_pressure(
        v_grid[np.newaxis, :], t_grid[:, np.newaxis], A_CO2, B_CO2
    )
    z_max = np.max(p_full) / 1e3

    def update(frame: int):
        ax.cla()
        fraction = min(1.0, frame / n_morph)
        a, b = fraction * A_CO2, fraction * B_CO2
        v_mesh, t_mesh, p_mesh = gases.pvt_surface(v_grid, t_grid, a, b)
        ax.plot_surface(
            v_mesh * 1e6, t_mesh, p_mesh / 1e3, cmap="viridis", alpha=0.95,
            rstride=1, cstride=1, linewidth=0,
        )
        ax.set_xlabel("v (cm^3/mol-scale, 1e-6 m^3)")
        ax.set_ylabel("T (K)")
        ax.set_zlabel("P (kPa)")
        ax.set_zlim(0.0, z_max)
        ax.set_title("van der Waals P-v-T surface: ideal -> CO2" if fraction < 1.0
                     else "van der Waals P-v-T surface (CO2)")
        ax.view_init(elev=25, azim=frame * (360.0 / n_frames))
        return ()

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "gases-surface")
    plt.close(fig)


def render_isotherms(n_frames: int = 150) -> None:
    """Sweep one isotherm's temperature through T_c and watch the van der Waals loop appear.

    Above T_c the isotherm is monotonic, exactly like the ideal gas; below T_c it develops a
    non-monotonic wiggle -- the unphysical region a real substance never follows (module 14
    resolves it with the Maxwell construction), and the clearest signature that mean-field
    theory is breaking down.
    """
    v_c, t_c, p_c = gases.vdw_critical_point(A_CO2, B_CO2)

    v_grid = np.linspace(1.01 * B_CO2, 4.0 * v_c, 400)
    temperatures = np.linspace(0.6 * t_c, 1.6 * t_c, n_frames)

    p_ref = gases.van_der_waals_pressure(v_grid, temperatures.max(), A_CO2, B_CO2)

    fig, ax = plt.subplots(figsize=(6.0, 4.5), dpi=DPI)
    (line,) = ax.plot([], [], lw=1.6, color="#2563eb")
    ax.axhline(p_c / 1e6, color="crimson", ls="--", lw=1.0, label="$P_c$")
    ax.axvline(v_c * 1e6, color="crimson", ls="--", lw=1.0, label="$v_c$")
    ax.set_xlim(v_grid.min() * 1e6, v_grid.max() * 1e6)
    ax.set_ylim(-0.2 * p_c / 1e6, 1.0 * np.max(p_ref) / 1e6)
    ax.set_xlabel("v (1e-6 m^3)")
    ax.set_ylabel("P (MPa)")
    title = ax.set_title("")
    ax.legend(loc="upper right")
    fig.tight_layout()

    def update(frame: int):
        temperature = temperatures[frame]
        pressure = gases.van_der_waals_pressure(v_grid, temperature, A_CO2, B_CO2)
        line.set_data(v_grid * 1e6, pressure / 1e6)
        title.set_text(f"T = {temperature:.0f} K  (T_c = {t_c:.0f} K)")
        return line, title

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "gases-isotherms")
    plt.close(fig)


def _isobar_temperature(v: np.ndarray, pressure: float, a: float, b: float) -> np.ndarray:
    """T(v) along a fixed-pressure contour: invert P = k_B T/(v-b) - a/v^2 for T."""
    from thermolab.constants import K_B

    return (pressure + a / v**2) * (v - b) / K_B


def render_shadows(n_frames: int = 180) -> None:
    """A state point slides along a three-leg path on the surface -- an isotherm, then an
    isochore, then an isobar -- while its shadow on each of the three coordinate walls traces
    out that same curve: the isotherm on the P-v wall, the isochore on the P-T wall, and the
    isobar on the v-T floor.
    """
    v_c, t_c, _p_c = gases.vdw_critical_point(A_CO2, B_CO2)

    # Leg 1 (isotherm): T fixed above T_c, v sweeps down.
    t0 = 1.3 * t_c
    v_leg1 = np.linspace(4.5 * v_c, 1.3 * v_c, 60)
    t_leg1 = np.full_like(v_leg1, t0)
    p_leg1 = gases.van_der_waals_pressure(v_leg1, t0, A_CO2, B_CO2)

    # Leg 2 (isochore): v fixed at the end of leg 1, T sweeps down.
    v1 = v_leg1[-1]
    t_leg2 = np.linspace(t0, 0.85 * t_c, 60)
    v_leg2 = np.full_like(t_leg2, v1)
    p_leg2 = gases.van_der_waals_pressure(v1, t_leg2, A_CO2, B_CO2)

    # Leg 3 (isobar): P fixed at the end of leg 2, v sweeps back out and T follows.
    p1 = p_leg2[-1]
    v_leg3 = np.linspace(v1, 3.5 * v_c, 60)
    t_leg3 = _isobar_temperature(v_leg3, p1, A_CO2, B_CO2)
    p_leg3 = np.full_like(v_leg3, p1)

    v_path = np.concatenate([v_leg1, v_leg2, v_leg3])
    t_path = np.concatenate([t_leg1, t_leg2, t_leg3])
    p_path = np.concatenate([p_leg1, p_leg2, p_leg3])

    v_grid = np.linspace(1.2 * B_CO2, 5.0 * v_c, 45)
    t_grid = np.linspace(0.75 * t_c, 1.4 * t_c, 45)
    v_mesh, t_mesh, p_mesh = gases.pvt_surface(v_grid, t_grid, A_CO2, B_CO2)

    v_scale, t_scale, p_scale = 1e6, 1.0, 1e-3  # cm^3-like, K, kPa

    fig = plt.figure(figsize=(7.0, 5.5), dpi=DPI)
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(
        v_mesh * v_scale, t_mesh * t_scale, p_mesh * p_scale, cmap="viridis", alpha=0.35,
        rstride=1, cstride=1, linewidth=0,
    )

    x_wall = v_grid.max() * v_scale  # right wall: the P-T projection lives here (v = const)
    y_wall = t_grid.min() * t_scale  # left wall: the P-v projection lives here (T = const)
    p_floor = 0.0  # floor: the v-T projection (the isobar) lives here (P = 0)

    ax.set_xlim(v_grid.min() * v_scale, v_grid.max() * v_scale)
    ax.set_ylim(t_grid.min() * t_scale, t_grid.max() * t_scale)
    ax.set_zlim(p_floor, np.max(p_mesh) * p_scale)
    ax.set_xlabel("v (1e-6 m^3)")
    ax.set_ylabel("T (K)")
    ax.set_zlabel("P (kPa)")
    ax.set_title("A state point's shadows: isotherm, isochore, isobar")

    (trace_3d,) = ax.plot([], [], [], color="#2563eb", lw=2.0)
    (point_3d,) = ax.plot([], [], [], "o", color="#f97316", ms=6)
    (shadow_pv,) = ax.plot([], [], [], color="0.4", lw=1.4)  # P-v wall (T = const)
    (shadow_pt,) = ax.plot([], [], [], color="0.4", lw=1.4)  # P-T wall (v = const)
    (shadow_vt,) = ax.plot([], [], [], color="0.4", lw=1.4)  # v-T floor (P = const)
    fig.tight_layout()

    n_points = v_path.size

    def update(frame: int):
        k = 1 + int((n_points - 1) * frame / (n_frames - 1))
        v_k, t_k, p_k = v_path[:k], t_path[:k], p_path[:k]

        trace_3d.set_data_3d(v_k * v_scale, t_k * t_scale, p_k * p_scale)
        point_3d.set_data_3d([v_k[-1] * v_scale], [t_k[-1] * t_scale], [p_k[-1] * p_scale])

        shadow_pv.set_data_3d(v_k * v_scale, np.full(k, y_wall), p_k * p_scale)
        shadow_pt.set_data_3d(np.full(k, x_wall), t_k * t_scale, p_k * p_scale)
        shadow_vt.set_data_3d(v_k * v_scale, t_k * t_scale, np.full(k, p_floor))

        ax.view_init(elev=22, azim=200 + frame * (120.0 / n_frames))
        return trace_3d, point_3d, shadow_pv, shadow_pt, shadow_vt

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "gases-shadows")
    plt.close(fig)


def main() -> None:
    render_pvt_surface()
    render_isotherms()
    render_shadows()


if __name__ == "__main__":
    main()
