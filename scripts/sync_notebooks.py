"""Create or refresh Hebrew notebooks from their English sources.

The rule this enforces is the one that keeps the two language trees honest: physics lives
once. Code cells are copied byte-for-byte from the English notebook — code is never
"translated" — while markdown cells are left alone so a human translation is never
overwritten. New Hebrew notebooks start as a copy with the markdown still in English, ready
to be translated cell by cell.

The `en_source_hash` stamped into `metadata.thermolab` is what `check_parity.py` compares
against, so running this after an English edit is what clears a staleness failure.

Data files beside the notebooks (`labs/data/`) are mirrored too — a lab needs its own
co-located copy in each language to run in the browser, and copying only the `.ipynb` is how
the Hebrew module-02 isotherm ended up reading a file that was not there.

Run:  uv run python scripts/sync_notebooks.py [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "notebooks" / "en"
HE_ROOT = ROOT / "notebooks" / "he"


def source_hash(path: Path) -> str:
    """sha256 of the file with line endings normalised, matching check_parity.py."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, notebook: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_one(en_path: Path, he_path: Path, check_only: bool) -> list[str]:
    """Return a list of human-readable changes (or would-be changes under --check)."""
    changes: list[str] = []
    english = load(en_path)

    if not he_path.exists():
        if check_only:
            return [f"{he_path.relative_to(ROOT)}: missing (would be created from English)"]
        hebrew = english
        hebrew.setdefault("metadata", {}).setdefault("thermolab", {})["language"] = "he"
        hebrew["metadata"]["thermolab"]["en_source_hash"] = source_hash(en_path)
        dump(he_path, hebrew)
        return [f"{he_path.relative_to(ROOT)}: created — markdown still needs translating"]

    hebrew = load(he_path)
    en_code = [c for c in english["cells"] if c["cell_type"] == "code"]
    he_code = [c for c in hebrew["cells"] if c["cell_type"] == "code"]

    if len(en_code) != len(he_code):
        return [
            f"{he_path.relative_to(ROOT)}: has {len(he_code)} code cells but English has "
            f"{len(en_code)} — cell structure diverged, resolve by hand"
        ]

    for index, (en_cell, he_cell) in enumerate(zip(en_code, he_code, strict=True)):
        if "".join(en_cell["source"]) != "".join(he_cell["source"]):
            changes.append(f"{he_path.relative_to(ROOT)}: code cell {index} differs from English")
            if not check_only:
                he_cell["source"] = en_cell["source"]

    stamped = ((hebrew.get("metadata") or {}).get("thermolab") or {}).get("en_source_hash")
    current = source_hash(en_path)
    if stamped != current:
        changes.append(f"{he_path.relative_to(ROOT)}: en_source_hash stale")
        if not check_only:
            thermolab = hebrew.setdefault("metadata", {}).setdefault("thermolab", {})
            thermolab["en_source_hash"] = current
            thermolab["language"] = "he"

    if changes and not check_only:
        dump(he_path, hebrew)
    return changes


def sync_data_files(check_only: bool) -> list[str]:
    """Mirror the `data/` directories that sit beside the notebooks.

    A notebook that reads a data file needs a copy co-located with it in *each* language:
    JupyterLite bundles only the notebooks/ tree and serves each language from its own
    directory, so the browser branch of the cell opens `data/<name>` next to the notebook it
    is running. Copying the `.ipynb` alone leaves the Hebrew lab opening a file that is not
    there — in the browser only, where nothing on this machine can see it.

    Only `data/` is mirrored. `_quiz/` next door is written per language by
    `render_quizzes.py` and its Hebrew copy must never be overwritten with the English one.
    """
    changes: list[str] = []
    for en_dir in sorted(p for p in EN_ROOT.rglob("data") if p.is_dir()):
        for en_file in sorted(en_dir.rglob("*")):
            if not en_file.is_file() or ".ipynb_checkpoints" in en_file.parts:
                continue
            he_file = HE_ROOT / en_file.relative_to(EN_ROOT)
            if he_file.exists() and he_file.read_bytes() == en_file.read_bytes():
                continue

            rel = he_file.relative_to(ROOT)
            reason = "differs from English" if he_file.exists() else "missing"
            if check_only:
                changes.append(f"{rel}: {reason} (would be copied from English)")
                continue
            he_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(en_file, he_file)
            changes.append(f"{rel}: {reason} — copied from English")
    return changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="report what would change without writing"
    )
    args = parser.parse_args(argv)

    if not EN_ROOT.exists():
        print("no English notebooks found")
        return 0

    all_changes: list[str] = []
    for en_path in sorted(EN_ROOT.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in en_path.parts:
            continue
        he_path = HE_ROOT / en_path.relative_to(EN_ROOT)
        all_changes.extend(sync_one(en_path, he_path, args.check))

    all_changes.extend(sync_data_files(args.check))

    for change in all_changes:
        print(change)
    if not all_changes:
        print("notebooks are in sync")
    return 1 if (all_changes and args.check) else 0


if __name__ == "__main__":
    sys.exit(main())
