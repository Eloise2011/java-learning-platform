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

---

# P0 Build Spec — Layered Lessons + Spaced-Repetition Review

**Audience reframe:** the learner who has struggled with Java for a long time.
For them the two failure modes are **overwhelm at intake** and **no retention of
the hard parts**. These two features attack exactly those. Spec'd 2026-06-16,
ready to build.

## Part A — Layered Lessons (progressive disclosure)

### Problem
Each topic is a single ~1,100-word scroll (Topic 1 is several thousand). A
returning, frustrated learner hits a wall of text and bounces. The richness is
valuable but must become **opt-in**, not the default firehose.

### Schema — new optional fields on each topic (`src/curriculum/phaseN.py`)
Backward-compatible: the existing `lesson` HTML stays and becomes the deep-dive
body. Add two optional fields:

```python
"core": "<p>An <strong>interface</strong> is a <em>contract</em> ... </p>",   # 60-second core idea: mental model + one real-world analogy + the one sentence to keep. Target <= 120 words.
"example": {
    "code": "interface Playable { void play(); }\nclass Song implements Playable { public void play(){ System.out.println(\"\\u266a\"); } }",
    "output": "♪",
    "caption": "The smallest thing that demonstrates the idea."
}
```

- `core` absent → fall back to `summary` (so all 26 topics render today).
- `example` absent → the "See it work" block is skipped.
- `lesson` is unchanged and always present (the deep dive).

### Rendering (`renderLesson` in `templates/tail.html`)
Render order inside `#tab-lesson`:
1. Title + badges (unchanged).
2. **Core card** — always visible, visually distinct (reuse `.key-point` styling). From `core` (fallback `summary`).
3. **"See it work"** — `example.code` in a `.code-block` + the expected `output` + `caption`. Only if `example` present.
4. Textbook ref (unchanged).
5. **Deep dive** — `topic.lesson` inside a collapsible `<details>` (or a button-toggled div) labelled "Read the full explanation". **Collapsed by default.** Persist the open/closed preference in `localStorage` key `java-learning-deepdive-pref` so power users aren't re-collapsing every topic.
6. Prev / Complete / Next nav (unchanged).

The existing `animateIn()` fade already covers the transition.

### Build validation (`validate_topics` in `src/build.py`)
- Warn (don't fail) when `core` is missing — drives authoring without breaking builds.
- If `example` present: require `example.code` (str) and `example.output` (str); error otherwise.

### Authoring
Use the LLM (`claude-opus-4-8`) to draft `core` + `example` from each existing
`lesson`, then human-review. Author the 5 OOP topics (10–14) first, then the rest.

### Acceptance criteria
- A topic with no `core`/`example` renders exactly as today (regression-safe).
- A fully-authored topic shows: core card → runnable example → collapsed deep dive.
- Deep-dive open/closed choice survives navigation and reload.

### Rollout
- **L1:** schema + validation + `renderLesson` restructure + collapsible + pref; author topics 10–14.
- **L2:** author `core`/`example` for all 26 topics.

---

## Part B — Spaced-Repetition Review Queue

### Problem
Struggling learners forget the hard parts and never re-encounter them. We
already store per-question correctness in `quiz_answers` and carry `complexity`
/ `importance` on every topic — enough to drive a forgetting-curve scheduler.

### Unit of review
A **review item = one quiz question** identified by `(topic_id, question_index)`.
(v1 scope: quiz questions only; coding-exercise recall can come later.)

### New table — `review_schedule`
```sql
CREATE TABLE review_schedule (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  user_id        INT NOT NULL,
  topic_id       INT NOT NULL,
  question_index INT NOT NULL,
  ease           DOUBLE   NOT NULL DEFAULT 2.5,   -- SM-2 ease factor
  interval_days  DOUBLE   NOT NULL DEFAULT 0,
  repetitions    INT      NOT NULL DEFAULT 0,
  due_at         DATETIME NOT NULL,
  last_grade     INT      NULL,
  updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uniq_item (user_id, topic_id, question_index)
);
```

### Scheduling algorithm (SM-2, simplified)
Map the binary quiz result (+ optional self-rated confidence) to a quality `q`:
- incorrect → `q = 2` (lapse)
- correct → `q = 4` (or `5` if the learner marks "easy")

Update on each review:
```
if q < 3:                      # lapse
    repetitions = 0
    interval_days = 0          # re-show later this session (due_at = now + 10 min)
else:
    repetitions += 1
    if   repetitions == 1: interval_days = 1
    elif repetitions == 2: interval_days = 6
    else:                  interval_days = round(interval_days * ease)
    ease = max(1.3, ease + (0.1 - (5-q)*(0.08 + (5-q)*0.02)))
due_at = now + interval_days   # (now + 10 min when interval_days == 0)
```

**Difficulty weighting** (serves "review the hard points more"): scale the
interval by topic metadata so harder/critical concepts recur sooner —
`interval_days /= weight`, where `weight = 1.3 if complexity=="intermediate" else 1.0`,
times `1.15 if importance=="critical"`. Clamp to a sane minimum.

### API (Flask, `backend/app.py`, port 5001, user id=1)
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/review/due` | Items with `due_at <= now`, ordered by `due_at` then difficulty weight; `?limit=20`. |
| POST | `/api/review/<topic_id>/<question_index>` | Body `{isCorrect: bool, confidence?: "easy"\|"normal"}`; applies SM-2, upserts the row, returns `{dueAt, intervalDays}`. |
| GET | `/api/review/stats` | Counts `{dueNow, learning, mature}` for the sidebar badge. |

**Seeding/backfill:** on first deploy, create `review_schedule` rows for every
existing `quiz_answers` record (due now) so returning learners get an immediate
queue. New answers in the Practice tab upsert a schedule row on save.

### Front-end
- New app-level view `review` — add `'review'` to the `currentView` set and a
  sidebar nav item **"🔁 Review"** with a **due-count badge** (from `/api/review/stats`).
- `renderAppReview()` — flashcard loop: show question → reveal correct answer +
  explanation → self-grade (**Again** / **Good** / **Easy**) → POST result → next.
  Show session progress and "next due in …".
- **Offline parity (API-first + localStorage fallback, per house pattern):**
  implement the SM-2 update once in JS; persist to `localStorage` key
  `java-learning-review-schedule`; when `apiOnline`, mirror to the API and treat
  the server as source of truth. The Review view works with the backend down.
- Optional nudge: a "You have N reviews due" prompt on the Welcome screen.

### Acceptance criteria
- Answering a review question reschedules it (lapse → minutes; pass → growing days).
- `complexity: intermediate` + `importance: critical` items resurface measurably sooner than easy ones.
- Sidebar badge reflects due count; Review view runs fully offline via localStorage.
- Backfill creates a non-empty queue for a user who already has `quiz_answers`.

### Rollout
- **R1:** table + 3 endpoints + JS SM-2 + Review view + sidebar badge + backfill.
- **R2:** difficulty/importance weighting + stats dashboard + Welcome nudge.

### Metrics to watch
% of due items reviewed within 24h; re-answer accuracy on *mature* items
(retention); review-session completion rate.

---

## Cross-cutting notes
- **Schema doc:** update `CLAUDE.md` (topic object fields + DB tables) when A and B land.
- **Order:** ship A and B together — A cuts intake overwhelm, B guarantees the hard parts come back. Each is useful alone, but the pair is what addresses why this persona fails.
- **Deliberately deferred:** new phases/topics and longer lessons (see "What I would explicitly say no to") until this learning loop is proven.
