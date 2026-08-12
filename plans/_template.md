# Module <NN> — <Title> — Implementation Plan

> **Brainstorm:** §3 module <n> (+ any other §s this plan draws on). **Module id:** `<NN-slug>`.
> **Content path:** `content/en/<dir>/<NN-slug>.md`. **Status:** <planned / built>.
> Canonical map, invariants, and conflict log: [README.md](README.md).

<!--
One plan file per module. This template folds the brainstorm's structure (§4 notebook
rhythm, §5 laboratories, §6 misconceptions, §7 accuracy framework, §8 assessment) into
the repo's module contract. Every plan follows this skeleton with these exact top-level
headings. Built modules replace the §3 bullet block with an as-built summary + gap list.
Formulas must be seeded pre-compliant with the course conventions — sign convention
dU = \dbar Q + \dbar \Won and the myst.yml macros \dbar, \Won, \kB — so they can be
pasted into content/ untouched. Objectives and quiz outlines use ASCII math (they are
copied verbatim into frontmatter and YAML quiz banks).
-->

## 1. Overview and narrative arc

2–4 paragraphs. This is the enhancement layer over the brainstorm: the module's
through-line as a story, its place in the spiral (which macroscopic idea it revisits
microscopically or vice versa), what this plan deepens or adds relative to the
brainstorm's one-row description, which earlier ideas get their payoff here, and which
later modules this one plants seeds for.

## 2. Position in the course

- **Requires:** module ids + the *specific results* assumed (not "knows entropy" but
  "uses S = kB ln Omega for the two-box system from 08").
- **Feeds:** later module ids + what they consume from here.
- **Explicitly not assumed:** common over-assumptions to keep out of the prose.

## 3. Module specification

For a **planned** module, the following bullet block. For a **built** module (00, 01,
04, 05, 08): a `**As-built summary.**` paragraph describing what the page, lab, and quiz
actually do (from reading the real files), then a numbered `**Gap list**` (missing
artifacts, brainstorm-centrepiece shortfalls, forward-pointer work owed to later
modules — no content rewrite), then one-line validation gates.

- **Identity and scope** — brainstorm content covered; what is deliberately deferred
  and to which module.
- **Prerequisites** — module ids + the specific results used.
- **Learning objectives** — `OBJ-<NN>-1..K`, testable phrasing, ASCII math (these go
  into page frontmatter verbatim).
- **Mathematical background** — already has / introduced here.
- **Physical intuition goals** — 2–4 "student can predict without algebra" statements.
- **Section skeleton seeds** — one or two bullets per mandatory section, in contract
  order:
  - *puzzle:* the hook phenomenon and the boxed question.
  - *predict:* the 3–4 commit-first questions (at least one targeting a misconception).
  - *explore:* the interactive controls — parameters, ranges, what updates live.
  - *derive:* the derivation route (see core derivations).
  - *verify:* which numerical checks, which becomes a `numerical-observation` admonition.
  - *transfer:* the 3–5 transfer targets (forward/backward module links).
  - *quiz:* themes the quiz bank must cover.
  - *explain:* the in-your-own-words questions.
  - *advanced (optional, always last):* what it contains, and the "safe to skip"
    boundary — no core content may depend on it.
- **Core derivations** — ordered: starting point → route → result. Key formulas written
  out, convention-compliant (`\dbar`, `\Won`, `\kB`; `dU = \dbar Q + \dbar \Won`).
- **Model specification draft** — the 7 bullets, fixed order: System / Dynamics /
  Boundary / Ensemble / Ignored / Valid when / Failure modes.
- **Epistemic classification** — the module's key claims, each tagged
  `definition | empirical-law | theorem | model-assumption | approximation |
  numerical-observation | open-question` (at least one admonition is mandatory in the
  page; list which claims get boxes).
- **Misconceptions** — registry ids addressed here (falsifying experiment + quiz
  distractor), and NEW entries as: id · statement · falsifying experiment · distractor.
- **Glossary terms** — key / en / suggested he / `he_reject` candidates.
- **Interactive controls and simulations** — beyond the explore bullets: each
  simulation, its parameters and ranges, what it renders.
- **Virtual lab outline** — `notebooks/en/labs/<NN-slug>.ipynb` cell-by-cell sketch:
  model setup, predictions, measured quantities, analysis, ending in a *measurement:*
  cell producing value ± error.
- **Real-experiment counterpart** — cheap physical pairing + how data imports into the
  lab notebook (or "none practical" with a sentence why).
- **Media assets** — `media/render/render_<topic>.py`: MP4 shot list, language-neutral
  (no text burned into frames).
- **Quiz bank outline** — `Q-<NN>-1..M`: per question, type (multiple-choice / numeric /
  free), objectives covered, misconception distractor if any. Every `OBJ-<NN>-K` covered
  at least once.
- **Problem set outline** — `<NN-slug>-problems.md`: analytical / computational /
  challenge problems, one-line statements, objective tags.
- **Runtime budget** — JupyterLite/Pyodide cost notes: grid sizes, particle counts,
  animation frame counts, target "runs in seconds in the browser". Numba is unavailable
  in Pyodide — vectorized NumPy only.
- **Validation gates** — the per-module commands (README bottom) + anything extra.
- **Open questions for the author** — decisions deliberately left to content-writing
  time, each with a recommendation.

## 4. Library and tests

- **`src/thermolab` — existing used:** which functions from which files.
- **`src/thermolab` — new / extended:** the file this module introduces or extends
  (must match the README ownership table), with a function-level sketch — signature +
  one-line contract each. Include the 7-bullet model-spec docstring header for a new
  file. Extenders spec only their own functions.
- **`tests/physics/` additions:** one line per test, filed under the six categories
  (dimensional / conservation / analytic-limit / large-N / convergence /
  seed-independence).

## 5. Assessment hooks

Cross-module synthesis problems that belong to this module's checkpoint rather than a
single section; exam-style themes; which later capstones or synthesis problems this
module feeds and with what.

## 6. Build order and validation gates

Where this module sits in the build sequence and why; what must land in
`glossary/terms.yml` and `assessment/misconceptions.yml` alongside it; the HE-mirror
artifact family (page, problems, lab, quiz bank, `en_source_hash` stamp) and
`translation-pending.txt` workflow; the gate commands.

## 7. Deviations from the brainstorm

Explicit log: merges, re-scopes, terminology changes, additions — one line of rationale
each. Empty section allowed but must be present.
