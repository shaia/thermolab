"""Render the demonstrations for module 13 (chemical potential).

Three animations and one still, all built from `thermolab.chemical`, so what a student watches is
the code they can run:

    chemical-exchange.mp4     two lattice-gas boxes, B's floor raised by 2 k_B T: particles pile
                              into A until its density is about seven times B's, while two gauges
                              showing mu_A and mu_B converge
    chemical-mu-trace.mp4     the same run as numbers: N_A against proposed hops (with the mean of
                              eight runs and the exact equilibrium) and mu_A - mu_B decaying to zero
    chemical-barometric.mp4   a twelve-layer isothermal column filling from the bottom layer into
                              the exponential profile, each layer's mu gathering onto one value
    chemical-adsorption.png   (a) surface coverage against (mu - epsilon) / k_B T, simulated points
                              on the one-site occupation curve; (b) the same against reservoir
                              density, the Langmuir isotherm

No words are burned into the frames -- symbols and numbers only -- so one file serves both
language sites and the explanation lives in the translated caption. See `_common.py` for the
format and its constraints.

Run:  uv run python media/render/render_chemical.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from _common import DPI, save, save_still  # noqa: E402
from thermolab import chemical  # noqa: E402
from thermolab.constants import K_B  # noqa: E402

RED, BLUE, BLACK, GREY, AMBER = "#dc2626", "#2563eb", "#111827", "#94a3b8", "#d97706"
T = 300.0
KT = K_B * T

# The centrepiece, as on the page and in the laboratory.
SITES = 100_000
N_TOTAL = 2000
OFFSET = 2.0  # u_B - u_A in units of k_B T
BOXES = chemical.two_boxes(SITES, SITES, 0.0, OFFSET * KT)
TAU = chemical.relaxation_steps(BOXES, N_TOTAL, T)


def _centrepiece_run(seed: int, n_steps: int, record_every: int) -> chemical.ExchangeTrace:
    return chemical.particle_exchange_sim(BOXES, [0, N_TOTAL], T, n_steps,
                                          np.random.default_rng(seed), record_every=record_every)


def render_exchange(n_frames: int = 300, hold: int = 45, per_dot: int = 10) -> None:
    """Dots hop from B into A; the two mu gauges meet while the densities split."""
    live = n_frames - hold
    record_every = int(np.ceil(5.0 * TAU / live))
    trace = _centrepiece_run(0, (live - 1) * record_every, record_every)
    # The first frame shows the t = 0 state -- every particle in B -- not the first record.
    counts_a = np.concatenate([[0], trace.counts[:, 0]])
    start = chemical.lattice_gas_mu(np.array([0, N_TOTAL]), BOXES.sites, BOXES.energies, T)
    mus = np.vstack([np.asarray(start)[None, :], trace.chemical_potentials]) / KT

    rng = np.random.default_rng(1)
    n_dots = N_TOTAL // per_dot
    # Box A spans x in [0, 1], box B x in [1.25, 2.25]; B's floor is drawn raised.
    floor_b = 0.3
    in_a = np.zeros(n_dots, dtype=bool)
    x = rng.uniform(1.28, 2.22, n_dots)
    y = rng.uniform(floor_b + 0.03, 0.97, n_dots)

    fig = plt.figure(figsize=(9.6, 4.4), dpi=DPI)
    ax = fig.add_axes((0.02, 0.06, 0.66, 0.88))
    gauge = fig.add_axes((0.76, 0.12, 0.2, 0.8))
    ax.add_patch(Rectangle((0.0, 0.0), 1.0, 1.0, fill=False, lw=2, ec=BLACK))
    ax.add_patch(Rectangle((1.25, 0.0), 1.0, 1.0, fill=False, lw=2, ec=BLACK))
    ax.add_patch(Rectangle((1.25, 0.0), 1.0, floor_b, color=GREY, alpha=0.5, lw=0))
    ax.plot([1.0, 1.25], [0.5, 0.5], color=BLACK, lw=2)
    ax.text(0.5, 1.04, "A", ha="center", fontsize=14)
    ax.text(1.75, 1.04, "B", ha="center", fontsize=14)
    ax.annotate("", xy=(2.33, floor_b), xytext=(2.33, 0.0),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.2))
    ax.text(2.36, floor_b / 2, rf"${OFFSET:.0f}\,k_{{\mathrm{{B}}}}T$", va="center", fontsize=11)
    ax.set_xlim(-0.05, 2.62)
    ax.set_ylim(-0.05, 1.12)
    ax.axis("off")
    scatter = ax.scatter(x, y, s=9, color=BLUE)

    gauge.set_xlim(-0.6, 1.6)
    gauge.set_ylim(-13, 0)
    gauge.set_xticks([0, 1], [r"$\mu_A$", r"$\mu_B$"])
    gauge.set_ylabel(r"$\mu / k_{\mathrm{B}} T$")
    bars = gauge.bar([0, 1], [0, 0], bottom=[-13, -13], width=0.55, color=[BLUE, AMBER])
    (level_a,) = gauge.plot([-0.3, 0.3], [0, 0], color=BLACK, lw=2)
    (level_b,) = gauge.plot([0.7, 1.3], [0, 0], color=BLACK, lw=2)
    gauge.spines[["top", "right"]].set_visible(False)

    def update(frame: int):
        index = min(frame, live - 1)
        want_a = int(round(counts_a[index] / per_dot))
        have_a = int(in_a.sum())
        if want_a > have_a:
            movers = rng.choice(np.flatnonzero(~in_a), want_a - have_a, replace=False)
            in_a[movers] = True
            x[movers] = rng.uniform(0.03, 0.97, len(movers))
            y[movers] = rng.uniform(0.03, 0.97, len(movers))
        elif want_a < have_a:
            movers = rng.choice(np.flatnonzero(in_a), have_a - want_a, replace=False)
            in_a[movers] = False
            x[movers] = rng.uniform(1.28, 2.22, len(movers))
            y[movers] = rng.uniform(floor_b + 0.03, 0.97, len(movers))
        # A little thermal jiggle, kept inside each box.
        x[:] += rng.normal(0.0, 0.006, n_dots)
        y[:] += rng.normal(0.0, 0.006, n_dots)
        np.clip(x, np.where(in_a, 0.02, 1.27), np.where(in_a, 0.98, 2.23), out=x)
        np.clip(y, np.where(in_a, 0.02, floor_b + 0.02), 0.98, out=y)
        scatter.set_offsets(np.column_stack([x, y]))
        mu_a, mu_b = mus[index]
        for bar, mu in zip(bars, (mu_a, mu_b), strict=True):
            bar.set_height(mu + 13)
        level_a.set_ydata([mu_a, mu_a])
        level_b.set_ydata([mu_b, mu_b])
        return (scatter, *bars, level_a, level_b)

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "chemical-exchange")
    plt.close(fig)


def render_mu_trace(n_frames: int = 270, hold: int = 45, n_seeds: int = 8) -> None:
    """N_A(t) with the eight-run mean and exact equilibrium; mu_A - mu_B decaying to zero."""
    live = n_frames - hold
    record_every = int(np.ceil(8.0 * TAU / live))
    n_steps = live * record_every
    runs = [_centrepiece_run(seed, n_steps, record_every) for seed in range(n_seeds)]
    # Every run starts from all particles in B; prepend that t = 0 state to the records.
    steps = np.concatenate([[0.0], runs[0].steps / TAU])
    counts = np.concatenate([[0], runs[0].counts[:, 0]])
    mean_counts = np.concatenate([[0.0], np.mean([r.counts[:, 0] for r in runs], axis=0)])
    start = chemical.lattice_gas_mu(np.array([0, N_TOTAL]), BOXES.sites, BOXES.energies, T)
    mu = np.vstack([np.asarray(start)[None, :], runs[0].chemical_potentials]) / KT
    difference = mu[:, 0] - mu[:, 1]
    live += 1
    exact = chemical.exact_count_distribution(BOXES, N_TOTAL, T).mean

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(7.6, 6.0), dpi=DPI, sharex=True)
    top.axhline(exact, color=BLACK, lw=1)
    (mean_line,) = top.plot([], [], "--", color=GREY, lw=1.8)
    (count_line,) = top.plot([], [], color=BLUE, lw=1.4)
    top.set_ylim(0, N_TOTAL)
    top.set_ylabel(r"$N_A$")
    bottom.axhline(0.0, color=BLACK, lw=1)
    (mu_line,) = bottom.plot([], [], color=RED, lw=1.4)
    bottom.set_ylim(-11, 1.5)
    bottom.set_xlim(0, steps[-1])
    bottom.set_ylabel(r"$(\mu_A - \mu_B) / k_{\mathrm{B}} T$")
    bottom.set_xlabel(r"$t / \tau$")
    fig.tight_layout()

    def update(frame: int):
        end = min(frame, live - 1) + 1
        count_line.set_data(steps[:end], counts[:end])
        mean_line.set_data(steps[:end], mean_counts[:end])
        mu_line.set_data(steps[:end], difference[:end])
        return count_line, mean_line, mu_line

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "chemical-mu-trace")
    plt.close(fig)


def render_barometric(n_frames: int = 300, hold: int = 45, per_dot: int = 5) -> None:
    """A column filling from the bottom layer into the exponential; every layer's mu gathers."""
    n_layers, sites, step = 12, 50_000, 0.4
    n_total = 2000
    column = chemical.column(n_layers, sites, step * KT)
    live = n_frames - hold
    record_every = 400
    trace = chemical.particle_exchange_sim(column, [n_total] + [0] * (n_layers - 1), T,
                                           live * record_every, np.random.default_rng(5),
                                           record_every=record_every)
    mus = trace.chemical_potentials / KT
    layers = np.arange(n_layers)
    dilute = chemical.equilibrium_split(column, n_total, T)

    rng = np.random.default_rng(6)
    n_dots = n_total // per_dot
    layer_of = np.zeros(n_dots, dtype=int)
    x = rng.uniform(0.02, 0.98, n_dots)
    y = rng.uniform(0.05, 0.95, n_dots)

    fig, (left, middle, right) = plt.subplots(
        1, 3, figsize=(10.4, 5.2), dpi=DPI, sharey=True,
        gridspec_kw={"width_ratios": [1.0, 1.4, 1.0]})
    for k in range(n_layers + 1):
        left.axhline(k, color=GREY, lw=0.5)
    scatter = left.scatter(x, layer_of + y, s=5, color=BLUE)
    left.set_xlim(0, 1)
    left.set_ylim(0, n_layers)
    left.set_xticks([])
    left.set_yticks(layers + 0.5, [str(k) for k in layers])
    left.set_ylabel(r"$m g z / (0.4\, k_{\mathrm{B}} T)$")
    bars = middle.barh(layers + 0.5, np.zeros(n_layers), height=0.8, color=BLUE, alpha=0.8)
    fine = np.linspace(0, n_layers, 200)
    middle.plot(dilute[0] * np.exp(-step * (fine - 0.5)), fine, "--", color=BLACK, lw=1.5)
    middle.set_xlim(0, 800)
    middle.set_xlabel(r"$N_k$")
    (points,) = right.plot([], [], "o", color=RED, ms=6)
    right.set_xlim(-7.5, -2.5)
    right.set_xlabel(r"$\mu_k / k_{\mathrm{B}} T$")
    fig.tight_layout()

    def update(frame: int):
        index = min(frame, live - 1)
        want = np.rint(trace.counts[index] / per_dot).astype(int)
        # Keep the dot total fixed despite rounding: adjust the fullest layer.
        want[np.argmax(want)] += n_dots - want.sum()
        have = np.bincount(layer_of, minlength=n_layers)
        surplus = [np.flatnonzero(layer_of == k)[: max(0, have[k] - want[k])]
                   for k in range(n_layers)]
        pool = np.concatenate(surplus) if surplus else np.array([], dtype=int)
        cursor = 0
        for k in range(n_layers):
            need = max(0, want[k] - have[k])
            chosen = pool[cursor:cursor + need]
            cursor += need
            layer_of[chosen] = k
            x[chosen] = rng.uniform(0.02, 0.98, len(chosen))
            y[chosen] = rng.uniform(0.05, 0.95, len(chosen))
        scatter.set_offsets(np.column_stack([x, layer_of + y]))
        for bar, n in zip(bars, trace.counts[index], strict=True):
            bar.set_width(n)
        points.set_data(np.clip(mus[index], -7.4, None), layers + 0.5)
        return (scatter, *bars, points)

    save(FuncAnimation(fig, update, frames=n_frames, blit=False), fig, "chemical-barometric")
    plt.close(fig)


ADSORPTION_TOTALS = (20, 60, 150, 300, 600, 1000, 1600, 2400)


def adsorption_table() -> list[tuple[int, float, float, float, float]]:
    """(N_total, common mu / k_B T, exact coverage, occupation formula, simulated coverage)."""
    surface, reservoir, eps = 200, 20_000, -3.0 * KT
    rows = []
    for n_total in ADSORPTION_TOTALS:
        boxes = chemical.two_boxes(surface, reservoir, eps, 0.0)
        mu, _ = chemical.occupation_equilibrium(boxes, n_total, T)
        exact = chemical.exact_count_distribution(boxes, n_total, T).mean / surface
        trace = chemical.particle_exchange_sim(boxes, [0, n_total], T, 300_000,
                                               np.random.default_rng(n_total), record_every=50)
        simulated = float(trace.tail(0.5)[:, 0].mean() / surface)
        rows.append((n_total, mu / KT, exact,
                     float(chemical.site_occupation(mu, T, eps)), simulated))
    return rows


def render_adsorption() -> None:
    rows = adsorption_table()
    x = np.array([r[1] for r in rows]) + 3.0  # (mu - epsilon) / k_B T
    simulated = np.array([r[4] for r in rows])
    grid = np.linspace(-5, 4, 300)
    fig, (left, right) = plt.subplots(1, 2, figsize=(10.4, 4.0), dpi=DPI)
    left.plot(grid, 1 / (np.exp(-grid) + 1), color=BLACK, lw=1.8)
    left.plot(x, simulated, "o", color=BLUE, ms=7)
    left.axvline(0, color=GREY, ls=":")
    left.axhline(0.5, color=GREY, ls=":")
    left.set_xlabel(r"$(\mu - \varepsilon) / k_{\mathrm{B}} T$")
    left.set_ylabel(r"$\langle n \rangle$")
    left.set_ylim(0, 1)
    pressure = np.linspace(0, 4, 300)  # reservoir density in units of its half-coverage value
    right.plot(pressure, pressure / (1 + pressure), color=BLACK, lw=1.8)
    right.plot(np.exp(x), simulated, "o", color=BLUE, ms=7)
    right.set_xlabel(r"$P / P_0$")
    right.set_ylabel(r"$\theta$")
    right.set_ylim(0, 1)
    right.set_xlim(0, 4)
    fig.tight_layout()
    save_still(fig, "chemical-adsorption")
    plt.close(fig)
    for row in rows:
        print("[adsorption] N=%5d  mu/kT=%7.3f  exact=%.4f  formula=%.4f  simulated=%.4f" % row)


def main() -> None:
    render_exchange()
    render_mu_trace()
    render_barometric()
    render_adsorption()


if __name__ == "__main__":
    main()
