"""Execute every laboratory notebook in the browser bundle that actually ships.

WHY THIS EXISTS, AND WHY THE OTHER CHECKS COULD NOT DO IT
    Five separate failures have reached the published site, all of one kind: the notebook runs
    on this machine and dies in the browser. A wrong bootstrap cell, a wheel that never got
    into the bundle, a `requires-python` ceiling that excluded Pyodide's CPython, a data file
    copied into one language tree but not the other, and a transitive `import scipy` inside
    `thermolab`. Every one was invisible to ruff, pytest, nbmake and all five content
    validators, because every one of those runs on the desktop, where the package is installed,
    the files are where the desktop expects them, and there is no Pyodide.

    Each was then fixed by writing a new validator aimed at that specific failure. That
    approach can only ever catch the failure already shipped, which is why there were five.
    This check is the other thing: it runs the artifact, in the environment the artifact is
    for, and fails on any cell that raises. It does not know what can go wrong, and does not
    need to.

WHAT IT DRIVES
    The real `_site/lite` bundle over HTTP — the same JupyterLite, the same piplite, the same
    wheel, the same per-language file layout the deployed site serves. Nothing here
    re-implements the bootstrap or substitutes a friendlier runtime; re-implementing the
    environment is the species of mistake that caused the bug in the first place.

TWO THINGS ABOUT JUPYTERLAB THAT MAKE THE OBVIOUS IMPLEMENTATION SILENTLY WRONG
    Both were found by writing the obvious thing and watching it pass on a notebook that was
    definitely broken.

    1. The notebook is *windowed*. Only cells near the viewport exist in the DOM; the other
       `.jp-Cell` nodes are empty placeholders with no prompt, no source and no output. And
       Run All scrolls to the **last** cell, so at the end the DOM holds the tail of the
       notebook and nothing else. A scan of `.jp-OutputArea-output` after Run All therefore
       looks at the last few cells, finds them clean, and reports a pass on a notebook that
       died in cell 2. Outputs do survive in the notebook model, so `harvest_outputs` scrolls
       from the top and collects them as the cells re-render.

    2. `.jp-InputPrompt` renders as an **empty string** in this bundle, for every cell. Every
       tutorial detects a running cell by the `[*]` in its prompt; here that condition is
       vacuously true from the first instant, so "wait until no prompt shows [*]" returns
       immediately and the check passes before the kernel has even booted. The execution
       indicator is used instead, and only a *sustained* idle counts, because it dips to idle
       between cells.

SKIPPING, DELIBERATELY
    `_site/` is a build output and is gitignored, so a fresh clone has none and this check
    reports "skipped" rather than failing — the same rule `check_assessment.py` follows for
    the gitignored `instructor/` tree. Run `.\\build.ps1` first, or let CI do it.

Run:  uv run python scripts/check_browser_labs.py [--lang en] [--notebook 07-second-law]
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import socket
import socketserver
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _findings import Finding, ensure_stdout_can_print_unicode, report  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
LANGUAGES = ("en", "he")

#: Pyodide boots and piplite installs four packages, all on the first cell. Generous on
#: purpose: a flaky timeout here would train people to ignore this check, which is worse than
#: not having it. A healthy lab settles in well under a minute once the kernel is up.
RUN_TIMEOUT_S = 600
LOAD_TIMEOUT_MS = 120_000

#: Execution counts as over once the indicator has read idle this many polls running. One
#: sample is not enough — it dips to idle in the gap after every cell.
POLL_S = 2.0
QUIESCENT_POLLS = 5

#: The notebook's scroll container, and how far to advance per step when harvesting.
SCROLLER = ".jp-WindowedPanel-outer"
SCROLL_STEP_PX = 400
SCROLL_SETTLE_S = 0.25
MAX_SCROLL_STEPS = 400

TRACEBACK_MARKER = "Traceback (most recent call last)"
EXCEPTION_RE = re.compile(r"\b(\w*(?:Error|Exception|Interrupt))\b")


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Serves the bundle without printing a line per request."""

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


def serve(directory: Path, port: int) -> socketserver.TCPServer:
    handler = functools.partial(QuietHandler, directory=str(directory))
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", port), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def lab_notebooks(lang: str) -> list[str]:
    """Notebook slugs for one language, from the source tree that feeds the bundle."""
    return sorted(p.stem for p in (ROOT / "notebooks" / lang / "labs").glob("*.ipynb"))


def kernel_status(page) -> str:
    return page.evaluate(
        """() => {
            const i = document.querySelector('.jp-Notebook-ExecutionIndicator');
            return i ? (i.dataset.status || '') : '';
        }"""
    )


def any_traceback_visible(page) -> bool:
    return page.evaluate(
        """(marker) => [...document.querySelectorAll('.jp-OutputArea-output')]
                       .some(o => o.textContent.includes(marker))""",
        TRACEBACK_MARKER,
    )


def wait_for_quiescence(page) -> bool:
    """Block until the run has settled or a cell has raised. False only on timeout."""
    deadline = time.monotonic() + RUN_TIMEOUT_S
    seen_busy = False
    quiet = 0

    while time.monotonic() < deadline:
        if any_traceback_visible(page):
            return True

        status = kernel_status(page)
        seen_busy = seen_busy or status == "busy"
        # The `seen_busy` guard matters: before Run All takes effect the kernel is already
        # idle, and without it the very first poll would call the notebook finished.
        if seen_busy and status == "idle":
            quiet += 1
            if quiet >= QUIESCENT_POLLS:
                return True
        else:
            quiet = 0
        time.sleep(POLL_S)

    return False


def harvest_outputs(page) -> tuple[list[str], bool]:
    """Every distinct cell output in the notebook, and whether the scroll reached the bottom.

    Scrolling is the whole point: see note 1 in the module docstring. Outputs are collected as
    cells re-render on the way down, because after Run All only the tail of the notebook is in
    the DOM.
    """
    page.evaluate(f"document.querySelector('{SCROLLER}').scrollTop = 0")
    seen: dict[str, None] = {}

    reached_bottom = False
    for _ in range(MAX_SCROLL_STEPS):
        for output in page.query_selector_all(".jp-OutputArea-output"):
            text = (output.inner_text() or "").strip()
            if text:
                seen.setdefault(text, None)
        reached_bottom = page.evaluate(
            f"""() => {{
                const e = document.querySelector('{SCROLLER}');
                const atBottom = e.scrollTop + e.clientHeight >= e.scrollHeight - 5;
                e.scrollTop += {SCROLL_STEP_PX};
                return atBottom;
            }}"""
        )
        if reached_bottom:
            break
        time.sleep(SCROLL_SETTLE_S)

    return list(seen), reached_bottom


def summarise(traceback_text: str) -> str:
    """The exception name and message, rather than eighty lines of frames."""
    flat = " ".join(traceback_text.split())
    match = EXCEPTION_RE.search(flat)
    if not match:
        return flat[:200]
    return flat[match.start():match.start() + 200]


def run_notebook(page, base_url: str, lang: str, slug: str) -> list[Finding]:
    """Open one lab in JupyterLite, run every cell, and report whatever raised."""
    path = ROOT / "notebooks" / lang / "labs" / f"{slug}.ipynb"
    url = f"{base_url}/lite/lab/index.html?path={lang}/labs/{slug}.ipynb"

    page.goto(url, timeout=LOAD_TIMEOUT_MS)
    try:
        page.wait_for_selector(".jp-Notebook .jp-Cell", timeout=LOAD_TIMEOUT_MS)
        # `runmenu:run-all` is the command id behind Run ▸ Run All Cells. Addressing the
        # command rather than the menu label survives translation and reordering between
        # JupyterLab versions. (`notebook:run-all-cells` does not exist; the menu was read out
        # of a live bundle to get this right.)
        page.click(".lm-MenuBar-item:has-text('Run')", timeout=LOAD_TIMEOUT_MS)
        page.click("[data-command='runmenu:run-all']", timeout=LOAD_TIMEOUT_MS)
    except Exception as error:  # noqa: BLE001 - any failure to start is the finding
        return [
            Finding(
                path, None, "error",
                f"the lab never started in JupyterLite ({type(error).__name__}). The bundle "
                f"serves {url} — check that build_site.py wrote it and that the notebook is "
                f"inside the tree JupyterLite packages.",
            )
        ]

    if not wait_for_quiescence(page):
        return [
            Finding(
                path, None, "error",
                f"no cell raised and execution never settled within {RUN_TIMEOUT_S}s. Either "
                f"the kernel never came up or a cell blocks in the browser.",
            )
        ]

    outputs, reached_bottom = harvest_outputs(page)
    failures = [text for text in outputs if TRACEBACK_MARKER in text]

    if failures:
        return [
            Finding(path, None, "error", f"raised in the browser: {summarise(text)}")
            for text in failures
        ]

    # Both of these say "this run proved less than it appears to", which is the failure mode
    # this check itself had twice while being written. Better a loud complaint than a pass
    # that looked at three cells out of twenty-four.
    if not reached_bottom:
        return [
            Finding(
                path, None, "error",
                f"gave up scrolling after {MAX_SCROLL_STEPS} steps without reaching the end "
                f"of the notebook, so later cells were never inspected.",
            )
        ]
    if not outputs:
        return [
            Finding(
                path, None, "error",
                "ran without producing a single output. Every lab here prints something, so "
                "this means the cells did not actually execute.",
            )
        ]

    return []


def check(languages: tuple[str, ...] = LANGUAGES, notebook: str | None = None,
          headed: bool = False) -> list[Finding]:
    if not (SITE / "lite").is_dir():
        print(f"skipped: no bundle at {SITE / 'lite'} — run build_site.py first")
        return []

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("skipped: playwright is not installed (uv sync --locked installs it)")
        return []

    findings: list[Finding] = []
    port = free_port()
    httpd = serve(SITE, port)
    base_url = f"http://127.0.0.1:{port}"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=not headed)
            try:
                for lang in languages:
                    for slug in [s for s in lab_notebooks(lang) if notebook in (None, s)]:
                        # One context per notebook: JupyterLite keeps the kernel and its
                        # installed packages in browser storage, and a reused one would hide
                        # exactly the bootstrap failures this check exists to find.
                        context = browser.new_context()
                        page = context.new_page()
                        started = time.monotonic()
                        try:
                            found = run_notebook(page, base_url, lang, slug)
                        finally:
                            context.close()
                        elapsed = time.monotonic() - started
                        status = "FAIL" if found else "ok"
                        print(f"  {lang}/{slug:<22} {status:<5} {elapsed:5.0f}s")
                        findings.extend(found)
            finally:
                browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

    return findings


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_can_print_unicode()
    parser = argparse.ArgumentParser(description="Run the laboratories in a real browser.")
    parser.add_argument("--lang", choices=LANGUAGES, help="only this language")
    parser.add_argument("--notebook", help="only this slug, e.g. 07-second-law")
    parser.add_argument("--headed", action="store_true", help="show the browser")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    languages = (args.lang,) if args.lang else LANGUAGES
    findings = check(languages, args.notebook, args.headed)
    return report(findings, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
