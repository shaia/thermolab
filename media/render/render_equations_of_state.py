"""Render the demonstration animations for module 02 (equations of state).

Animations are produced from `thermolab` itself, so what a student watches is the same model
they can read, run and test — never a hand-drawn impression of it.

Output is MP4, written by `_common.save`; see that module for why, and for the constraints the
format brings. The animations carry no words, so the same file serves both language sites; the
caption that explains each one is ordinary translated page prose rather than a subtitle track
that could silently drift from the text around it.

Run:  uv run python media/render/render_equations_of_state.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
from mpl_toolkits.mplot3d import Axes3D  # noqa: E402,F401  (registers the 3D projection)

from _common import DPI, save  # noqa: E402
from thermolab import equations_of_state  # noqa: E402

# Argon's van der Waals constants, converted to this course's per-particle convention (see
# equations_of_state.py's module docstring for the a_molar/N_A**2, b_molar/N_A conversion).
A_ARGON = 3.736e-49  # Pa m^6, per molecule
B_ARGON = 5.317e-29  # m^3, per molecule
N_PARTICLES = 5.0e22  # matches the STP-like scenario used throughout the module


def render_pvt_surface(n_frames: int = 90) -> None:
    """A rotating comparison of the ideal-gas surface (wireframe) and the van der Waals
    surface (coloured) over the same T, V grid -- the module page's centrepiece figure.
    """
    _t_c, _p_c, v_c = equations_of_state.critical_point(N_PARTICLES, A_ARGON, B_ARGON)
    v_min = 1.05 * v_c
    temperatures = np.linspace(120.0, 400.0, 30)
    volumes = np.linspace(v_min, 6.0 * v_min, 30)

    ideal = equations_of_state.pv_t_surface(N_PARTICLES, temperatures, volumes)
    vdw = equations_of_state.pv_t_surface(N_PARTICLES, temperatures, volumes, A_ARGON, B_ARGON)
    t_grid, v_grid = np.meshgrid(temperatures, volumes, indexing="ij")

    fig = plt.figure(figsize=(7.0, 5.5), dpi=DPI)
    ax = fig.add_subplot(projection="3d")
    ax.plot_wireframe(
        v_grid * 1e24, t_grid, ideal / 1e3, color="#94a3b8", linewidth=0.4, rstride=2, cstride=2
    )
    ax.plot_surface(
        v_grid * 1e24, t_grid, vdw / 1e3, cmap="viridis", alpha=0.9,
        rstride=1, cstride=1, linewidth=0,
    )
    ax.set_xlabel("V (1e-24 m^3)")
    ax.set_ylabel("T (K)")
    ax.set_zlabel("P (kPa)")
    ax.set_title("van der Waals surface (colour) vs the ideal-gas surface (wireframe)")
    fig.tight_layout()

    def update(frame: int):
        ax.view_init(elev=25, azim=frame * (360.0 / n_frames))
        return ()

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "pvt-surface-ideal-vs-vdw")
    plt.close(fig)


def render_isotherms_near_critical(n_frames: int = 150) -> None:
    """Sweep one isotherm's temperature through T_c and watch the van der Waals loop appear.

    Above T_c the isotherm is monotonic, exactly like the ideal gas; below T_c it develops a
    non-monotonic wiggle -- the unphysical region a Maxwell construction has to replace, and
    the clearest signature that mean-field theory is breaking down.
    """
    t_c, p_c, v_c = equations_of_state.critical_point(N_PARTICLES, A_ARGON, B_ARGON)
    excluded = N_PARTICLES * B_ARGON

    volumes = np.linspace(1.01 * excluded, 4.0 * v_c, 400)
    temperatures = np.linspace(0.6 * t_c, 1.6 * t_c, n_frames)

    p_ref = equations_of_state.van_der_waals_pressure(
        N_PARTICLES, temperatures.max(), volumes, A_ARGON, B_ARGON
    )

    fig, ax = plt.subplots(figsize=(6.0, 4.5), dpi=DPI)
    (line,) = ax.plot([], [], lw=1.6, color="#2563eb")
    ax.axhline(p_c / 1e6, color="crimson", ls="--", lw=1.0, label="$P_c$")
    ax.axvline(v_c * 1e24, color="crimson", ls="--", lw=1.0, label="$V_c$")
    ax.set_xlim(volumes.min() * 1e24, volumes.max() * 1e24)
    ax.set_ylim(-0.2 * p_c / 1e6, 1.0 * np.max(p_ref) / 1e6)
    ax.set_xlabel("V (1e-24 m^3)")
    ax.set_ylabel("P (MPa)")
    title = ax.set_title("")
    ax.legend(loc="upper right")
    fig.tight_layout()

    def update(frame: int):
        temperature = temperatures[frame]
        pressure = equations_of_state.van_der_waals_pressure(
            N_PARTICLES, temperature, volumes, A_ARGON, B_ARGON
        )
        line.set_data(volumes * 1e24, pressure / 1e6)
        title.set_text(f"T = {temperature:.0f} K  (T_c = {t_c:.0f} K)")
        return line, title

    save(
        FuncAnimation(fig, update, frames=n_frames, blit=False),
        fig,
        "pvt-isotherms-near-critical",
    )
    plt.close(fig)


def main() -> None:
    render_pvt_surface()
    render_isotherms_near_critical()


if __name__ == "__main__":
    main()
