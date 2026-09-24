"""The shipped package may import only what the browser kernel actually has.

This exists because a green suite meant nothing here. `multiplicity.py` imported
`scipy.special.gammaln`, `thermolab/__init__.py` imports `multiplicity` eagerly, and so
`from thermolab import <anything>` raised `ModuleNotFoundError: No module named 'scipy'` in
JupyterLite — in every lab, in both languages — while ruff, pytest, nbmake and all five
content checkers passed. It surfaced only when a human opened a notebook in a browser.

THE MECHANISM, because the obvious guess is wrong
    Pyodide *has* a scipy build, so "Pyodide supplies scipy" reads as reassuring and is
    useless. JupyterLite's kernel auto-loads Pyodide packages by scanning the source of the
    *cell being executed* for import statements. It never sees a transitive import inside an
    installed package. A cell that says `import numpy as np` gets numpy; a cell that says
    `from thermolab import engines` gets `thermolab` and nothing thermolab itself needs.

    `piplite.install("thermolab", deps=False)` then skips the dependency graph on purpose —
    asking for the floors in pyproject.toml would send micropip to PyPI for packages with no
    WebAssembly wheels. So nothing anywhere installs a transitive dependency.

WHAT IS ALLOWED, AND WHY EACH ONE
    numpy  — every lab notebook writes `import numpy as np` in a cell, so the kernel's
             scanner loads it before `thermolab` is touched.
    pint   — the bootstrap cell installs it explicitly by name.

    Nothing else. Adding a third-party import to `src/thermolab/` means either adding it to
    the bootstrap cell of every notebook (and `check_notebooks.py`'s expected form), or not
    adding it at all. "It is pure Python" is not the test and never was; "the browser already
    has it" is not the test either. The test is whether something puts it in the kernel
    before `import thermolab` runs.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "src" / "thermolab"

#: Third-party roots the browser kernel is guaranteed to have when `import thermolab` runs.
ALLOWED_THIRD_PARTY = frozenset({"numpy", "pint"})


def imported_roots(source: str) -> set[str]:
    """Top-level module names this source imports, ignoring relative imports."""
    roots: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
    return roots


def package_modules() -> list[Path]:
    return sorted(p for p in PACKAGE.rglob("*.py") if "__pycache__" not in p.parts)


def test_the_package_has_modules_to_check():
    """Guards the rest of this file from passing because the glob found nothing."""
    modules = package_modules()
    assert len(modules) >= 10
    assert any(p.name == "multiplicity.py" for p in modules)


@pytest.mark.parametrize("path", package_modules(), ids=lambda p: p.name)
def test_module_imports_nothing_the_browser_kernel_lacks(path: Path):
    third_party = {
        root
        for root in imported_roots(path.read_text(encoding="utf-8"))
        if root not in sys.stdlib_module_names and root != "thermolab"
    }
    offenders = third_party - ALLOWED_THIRD_PARTY

    assert not offenders, (
        f"{path.relative_to(ROOT)} imports {sorted(offenders)}, which nothing installs into "
        f"the JupyterLite kernel before `import thermolab` runs. Every lab notebook in both "
        f"languages will raise ModuleNotFoundError on its first import cell, and no other "
        f"check in this repository can see it. Read this file's docstring before widening "
        f"ALLOWED_THIRD_PARTY."
    )


def test_the_check_detects_an_offender():
    """The failing fixture. Parametrized over real files, the check above can only pass.

    Feeds the detector the exact shape of the bug it exists for, so a refactor that quietly
    stopped looking at `from x.y import z` would be caught.
    """
    offending = (
        "from __future__ import annotations\n"
        "import numpy as np\n"
        "from scipy.special import gammaln\n"
    )
    roots = imported_roots(offending)

    assert "scipy" in roots
    assert roots - set(sys.stdlib_module_names) - ALLOWED_THIRD_PARTY == {"scipy"}

    # ...and relative imports, which are always fine, are not mistaken for third-party ones.
    assert imported_roots("from . import processes\nfrom .constants import K_B\n") == set()


def test_scipy_specifically_stays_out():
    """The concrete regression, named so the reason survives a refactor of the check above.

    `scipy.special.gammaln` is a one-line convenience for `math.lgamma`, which is stdlib and
    identical to the last bit. It is not worth a dead notebook.
    """
    for path in package_modules():
        assert "scipy" not in imported_roots(path.read_text(encoding="utf-8")), (
            f"{path.relative_to(ROOT)} imports scipy again — see multiplicity._log_gamma for "
            f"the stdlib replacement that removed it"
        )
