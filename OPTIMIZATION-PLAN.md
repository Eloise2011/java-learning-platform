# Java Learning Platform — Pedagogical Optimization Plan

**Created:** 2026-06-15
**Status:** Pillar 1-A shipped; remainder planned

## Guiding goal

The platform exists so learners genuinely **grasp the core ideas** of Java —
extending, implementing, encapsulation, polymorphism, OOP design — **cultivate
their own code taste**, and **map abstractions to real-world scenarios**. The
content (26 topics, ~28,600 lesson words) is already strong. The leverage is in
**assessment and feedback**: today the app cannot tell a correct design from
keyword soup, and neither can the learner. This plan closes that loop.

---

## Pillar 1 — Make assessment verify understanding *(highest leverage)*

The original coding-exercise grader (`checkExercise`) scored a free-text answer
by **case-insensitive substring matching** against `checkKeywords`. Pasting the
keywords into a comment scored 100%. Three layered fixes:

| Phase | What | Effort | Status |
|---|---|---|---|
| **1-A. Structural grading** | Strip comments/strings, token-aware + case-sensitive matching, reject prose, optional authored per-exercise `checks` (incl. negative `mustNotMatch` rules like "no setters"/"no public fields"). | Low (front-end only) | ✅ **Done** |
| **1-B. LLM rubric grader** | `POST /api/grade` sends learner code + per-exercise rubric to Claude; returns design-level feedback ("fields are public — that breaks encapsulation; expose behavior, not state"). Use `claude-haiku-4-5` for cheap inline grading, `claude-opus-4-8` for authoring rubrics. | Medium | ⬜ Planned |
| **1-C. JUnit judge** | Backend sandbox compiles with `javac` + runs hidden JUnit tests; exercises gain a `tests` field. True pass/fail for capstone-grade work. | High (sandboxing) | ⬜ Planned |
| **1-D. "Why" quiz items** | One design-judgment question per OOP topic ("Why prefer composition over inheritance here?") — tests understanding, not recall. | Low (content) | ⬜ Planned |

**Recommendation:** 1-A now (done), 1-B next (richest feedback per dollar), 1-C
later for the exercises that warrant execution.

## Pillar 2 — Cultivate code taste

Taste comes from comparing good vs. bad, not greenfield writing in a vacuum.

- **"Spot the smell / Refactor" exercise type.** Show working-but-bad code
  (public fields, god class, inheritance where composition fits); learner
  identifies the smell and rewrites it. New `codingExercise` fields:
  `smellExample`, `designNotes`.
- **Annotated model solutions.** `exampleSolution` is currently bare code; add a
  `solutionRationale` explaining *why* (private fields protect invariants;
  `accelerate()` is overridden, not redefined).
- **Design-principle callouts** woven into topics 10–14 (encapsulate state,
  program to interfaces, favour composition, Liskov substitution) reusing the
  existing `.key-point` style.
- **"Two solutions — which is better?"** mini-comparisons (inheritance vs.
  composition; exposing a `List` vs. an unmodifiable view).

## Pillar 3 — Real-world analogy that compounds

Instructions already use good analogies (Vehicle, Shape, MediaPlayer) but each
topic resets to a new domain, so concepts don't accumulate.

- **One thread-through capstone domain** (e.g. ride-share or library) built
  incrementally across topics 10→22: encapsulation defines `Account`,
  inheritance/polymorphism add roles, interfaces add `Payable`,
  collections/generics manage the fleet, streams/Optional handle queries.
- **Explicit "Real-World Mental Model" box** per OOP topic (interface =
  electrical-socket contract; abstract class = blueprint with some rooms built).

## Pillar 4 — Retention & active recall

- **Spaced repetition.** `quiz_answers` already records per-question
  correctness; resurface 1–2 previously-missed questions when a new topic opens.
- **Mastery view, not just completion.** Progress tab should show concept
  mastery (quiz accuracy, exercise check scores), not only topics ticked.
- **De-emphasise "Accept & Continue"** so engagement is the path of least
  resistance, not bypass.

## Pillar 5 — Engineering enablers

- **Schema evolution.** Pillars 1–3 add `codingExercise` fields: `checks` (done),
  `rubric`, `tests`, `smellExample`, `designNotes`, `solutionRationale`. Extend
  `validate_topics()` in `src/build.py` and keep `CLAUDE.md` in sync.
- **Remove the legacy root `build.py`** (dual-builder hazard) so content can't be
  rebuilt from stale 22-topic data.
- **Author-time generation.** Use the LLM to draft `checks`/rubrics/smells for
  all 26 existing exercises in bulk, then human-review.

---

## Suggested sequencing

1. **Done:** Pillar 1-A structural grader.
2. **Next:** Pillar 1-B (`/api/grade`) + annotated rationale on the 12 OOP-heavy
   exercises (Pillar 2).
3. **Then:** capstone domain thread (Pillar 3) + spaced repetition (Pillar 4).
4. **Later:** JUnit judge (1-C); mastery dashboard; remove legacy `build.py`.

---

## Pillar 1-A — Implementation notes (shipped 2026-06-15)

**Front-end (`src/templates/tail.html`, `checkExercise` and helpers):**
- `stripCodeNoise()` removes block/line comments, text blocks, and string/char
  literals **before** any matching — concepts can no longer be stuffed into a
  comment to game the checker.
- `looksLikeJavaCode()` requires a brace pair plus a code-shaped token, rejecting
  prose-only submissions.
- Matching is **token-aware** (word boundaries via `keywordToRegex`) and
  **case-sensitive** (Java is case-sensitive) — `Private`/partial substrings no
  longer pass.
- `buildExerciseChecks()` prefers authored `ex.checks` and falls back to
  token-aware checks derived from the legacy `checkKeywords` (so all 26 topics
  improved immediately, even those without authored checks).
- Feedback is itemised (per-check ✓/✗ lists) instead of a flat keyword count.

**Curriculum schema — new optional `codingExercise.checks` field:**
```python
"checks": [
  {"label": "Keeps balance private (encapsulation)", "pattern": r"\bprivate\b[\s\S]{0,60}\bbalance\b"},
  {"label": "Has NO setters (mutation forbidden)",   "pattern": r"\bset[A-Z]\w*\s*\(", "mustNotMatch": True}
]
```
- `pattern` is a JS-regex source string; write backslashes escaped for Python
  (`r"\bclass\b"`). `flags` is optional. `mustNotMatch: True` inverts the check
  (passes when the pattern is **absent**) — used for anti-patterns.

**Authored `checks` so far:** topics 10 (Classes & Objects), 11 (Encapsulation),
12 (Inheritance), 13 (Polymorphism), 14 (Abstract Classes & Interfaces). All
other topics use the improved `checkKeywords` fallback until authored.

**Verification:** every authored topic's `exampleSolution` scores ≥80% (pass);
comment-stuffing and prose-only submissions are rejected; built `index.html`
passes `node --check`.
