"""ThermoLab — the physics behind the course.

Every model the notebooks and pages use lives here, in plain vectorized NumPy, so that a
student can read the implementation of any claim the course makes. Notebooks orchestrate
lessons; they never re-implement physics.

Modules:
    constants            physical constants and the fixed sign convention
    units                pint registry used by the dimensional tests
    sampling             independent draws: sample averages, random walks, and the CLT
    chemical             the chemical potential; particle exchange, adsorption, reactions, osmosis
    forms                differential forms in the plane; exact versus inexact, as pure mathematics
    equilibrium          two bodies exchanging energy quanta until they share one temperature
    fundamental          the fundamental relation S(U, V, N): slopes, extensivity, stability
    engines              closed cycles between reservoirs; efficiency and the second-law bound
    ensembles            a small system on a finite heat bath; where the Boltzmann factor comes from
    gases                the ideal gas, the van der Waals correction, and the critical point
    kinetics             free particles in a box; the microscopic origin of pressure
    paths                quasistatic paths in the P-V plane; work as a path function
    partition            partition functions; U, S, F and C from ln Z; the paramagnet and negative T
    potentials           H, F and G by Legendre transform; Maxwell relations; minimum principles
    processes            the named process families, heat capacities, and irreversible change
    multiplicity         microstate counting, entropy, and why equilibrium wins
    validation           the reusable accuracy checks (seeds, convergence, scaling)
"""

from __future__ import annotations

from . import (
    chemical,
    engines,
    ensembles,
    equilibrium,
    forms,
    fundamental,
    gases,
    kinetics,
    multiplicity,
    partition,
    paths,
    potentials,
    processes,
    sampling,
    units,
    validation,
)
from .constants import AMU, K_B, N_A, R_GAS, SIGN_CONVENTION

__all__ = [
    "AMU",
    "K_B",
    "N_A",
    "R_GAS",
    "SIGN_CONVENTION",
    "chemical",
    "engines",
    "ensembles",
    "equilibrium",
    "forms",
    "fundamental",
    "gases",
    "kinetics",
    "multiplicity",
    "partition",
    "paths",
    "potentials",
    "processes",
    "sampling",
    "units",
    "validation",
]
