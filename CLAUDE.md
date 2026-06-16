# Java Learning Platform — Project Guide

Single-page interactive Java curriculum with **26 topics across 2 active phases** (6 phases planned), quizzes, coding exercises, resource tracking, and MySQL-backed persistence.

## Architecture

```
index.html              ← Self-contained SPA (deployable artifact, ~914 KB)
├── CSS (inline <style>)    ← Light theme with WCAG AA contrast
├── HTML structure          ← Sidebar + main content area
└── JS (inline <script>)    ← All application logic
    ├── CURRICULUM data     ← 26 topics embedded as JSON
    ├── PHASES metadata     ← 6 phases (2 active, 4 planned)
    ├── State management    ← STATE object + module-level globals
    ├── Rendering           ← renderSidebar(), renderLesson(), renderPractice(), etc.
    ├── Persistence         ← API-first (MySQL via Flask), localStorage fallback
    └── Mermaid.js          ← CDN-loaded (pinned mermaid@10.9.3) for site map diagram

src/                       ← Source of truth — build the SPA from here
├── build.py               ← CANONICAL build script (templates + curriculum → dist/index.html)
├── curriculum/
│   ├── phase1.py          ← Phase 1 data: 22 topics (Programming Fundamentals)
│   └── phase2.py          ← Phase 2 data: 4 topics (Developer Tools — Git & Maven)
├── templates/head.html    ← HTML/CSS up to the curriculum insertion point
├── templates/tail.html    ← JS app code + closing tags (the live app logic)
└── app.js                 ← Extracted JS (reference snapshot only; tail.html is authoritative)

backend/
├── app.py                 ← Flask REST API (port 5001)
├── db.py                  ← MySQL connection helper (env-var configurable)
└── requirements.txt       ← flask, flask-cors, mysql-connector-python

dist/index.html            ← Build output of src/build.py (then copied to root index.html)

build.py (root)            ← LEGACY monolithic builder (Phase 1 only, 22 topics inline). STALE — do not use.
Enhancement-In-Progress.html ← Human-readable status tracker for in-flight enhancements
ITERATION-2-PLAN.md        ← Optimization/audit backlog (agent-driven review findings)
```

## Build System — Read This First

There are **two `build.py` files**. They are not the same:

- **`src/build.py` — CANONICAL.** Loads every `src/curriculum/phase*.py` (each exposes a `TOPICS` list), validates them, injects the JSON into `templates/head.html` + `templates/tail.html`, and writes `dist/index.html`. This is the one to run.
- **`build.py` (root) — LEGACY/STALE.** A self-contained monolith with all curriculum inlined as `topic(...)` calls. Only contains Phase 1 (22 topics) and writes to the root `index.html`. Do NOT edit or run it for new work; prefer deleting/ignoring it over reviving it.

Build + deploy flow:

```bash
python3 src/build.py            # → dist/index.html (prints topic/word/hour stats)
cp dist/index.html index.html   # promote build output to the deployable artifact at repo root
```

The committed root `index.html` and `dist/index.html` are kept identical and reflect the `src/build.py` output (all 26 topics).

## Commands

```bash
# Build the SPA from curriculum data (canonical)
python3 src/build.py

# Start the backend API (MySQL required) — port 5001
cd backend && python3 app.py

# Test the API
curl http://localhost:5001/api/health
curl http://localhost:5001/api/progress
```

## Key Patterns

- **State:** The `STATE` global object holds `currentTopicId`, `completedTopics` (Set), and `expandedPhases` (Set). View routing and other UI flags live in **separate module-level globals** in `tail.html`, not on `STATE`:
  - `currentView` — `'welcome' | 'topic' | 'progress' | 'sitemap' | 'textbooks'`
  - `quizAnswers` — in-memory cache of quiz answers
  - `apiOnline` — set true by `apiFetch()` on the first successful API call
  - `API_BASE` — `http://localhost:5001/api`
- **Rendering:** All render functions use `innerHTML`. App-level views (Welcome, Progress, Site Map, Textbooks) are switched by `currentView`. Topic tab switching (`switchTab()`) manipulates `style.display` directly rather than relying on CSS classes.
- **Persistence:** API-first to `API_BASE`, with `localStorage` fallback. All API calls go through `apiFetch()`, which sets `apiOnline`. Storage keys: `java-learning-platform-progress`, `java-learning-quiz-answers`.
- **Quiz system:** Questions stored in `topic.quiz[]`. Answers persisted to `localStorage` and the MySQL `quiz_answers` table via `saveQuizAnswer()`. Previous answers restored via `getQuizAnswer()`. Note: the Practice tab presents a fresh quiz UI on reload (answers remain in the DB).
- **Coding-exercise grading (`checkExercise`, structural — Pillar 1-A):** Submissions are graded against the *real* code, not substrings. `stripCodeNoise()` removes comments and string/char literals first (so concepts can't be stuffed into a comment), `looksLikeJavaCode()` rejects prose, and matching is token-aware (word boundaries) and case-sensitive. `buildExerciseChecks()` prefers an authored `codingExercise.checks` array and falls back to token-aware checks derived from `checkKeywords`. See `OPTIMIZATION-PLAN.md` for the broader pedagogy roadmap.
- **Mermaid:** Lazy-rendered — diagram string built in `buildMermaidDiagram()`, with `mermaid.run()` deferred to `switchTab()` / `renderAppSiteMap()` so it only runs when the container is visible (avoids zero-dimension SVG). Configured with `securityLevel: 'strict'` and `htmlLabels: false`.
- **Curriculum data flow:** `src/curriculum/phaseN.py` → `src/build.py` → `dist/index.html` → `index.html`

## Editing Lessons

Do NOT manually edit the CURRICULUM JSON inside `index.html` / `dist/index.html`. Instead:

1. Edit the relevant phase file in `src/curriculum/` (`phase1.py` for topics 1–22, `phase2.py` for topics 23–26). Each file defines a `TOPICS` list.
2. Run `python3 src/build.py` to regenerate `dist/index.html`.
3. Copy `dist/index.html` to the repo root `index.html` to update the deployable artifact.

To add a new phase, create `src/curriculum/phaseN.py` exporting a `TOPICS` list; `src/build.py` auto-discovers it (sorted filename order). Make sure the phase name matches a key in the `PHASES` dict in `src/build.py`.

Each topic object has: `id`, `phase`, `phaseColor`, `phaseClass`, `title`, `hours`, `complexity`, `importance`, `textbook`, `summary`, `lesson` (HTML string), `quiz` (array of `{question, options, correct, explanation}`), and `codingExercise` (`{instruction, hint, checkKeywords, exampleSolution?, checks?}`).

**Layered lessons (Part A):** topics may also define `core` (optional HTML string — the 60-second core idea, shown first; falls back to `summary` when absent) and `example` (optional `{code, output, caption?}` — a minimal runnable snippet rendered as a "See it work" block). `renderLesson()` shows core → example → textbook → a collapsible **Full explanation** deep-dive containing `lesson` (collapsed by default; open/closed preference stored in `localStorage` key `java-learning-deepdive-pref`). Authored for topics 10–14 so far; `src/build.py` warns (non-fatally) for topics still missing `core`.

`codingExercise.checks` (optional) is the structural grader's rule list — `[{label, pattern, flags?, mustNotMatch?}]`, where `pattern` is a JS-regex source string (write backslashes escaped for Python, e.g. `r"\bclass\b"`) and `mustNotMatch: True` inverts the rule to flag an anti-pattern (e.g. "no setters"). When `checks` is absent the grader falls back to token-aware matching of `checkKeywords`.

## Backend API

Flask app in `backend/app.py` (port 5001). Endpoints:

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/progress` | List completed topic IDs |
| POST/DELETE | `/api/progress/<topic_id>` | Mark / unmark topic complete |
| GET/POST | `/api/quiz/<topic_id>` | Get / save quiz answers |
| GET/POST | `/api/resources/<topic_id>` | List / add extra-curriculum resources |
| DELETE | `/api/resources/<resource_id>` | Delete a resource |
| GET/POST | `/api/enhancements/<topic_id>` | Get / submit feedback/enhancements |

All write helpers use `query(..., fetch=False)` from `db.py`. The default user is hard-coded as `id=1`.

## Database

MySQL database `java_learning_platform`:
- `users` — default user (id=1)
- `topic_progress` — completed topics
- `quiz_answers` — per-question answers with correctness
- `topic_resources` — extra-curriculum resources (books, links, podcasts, videos) with author field
- `topic_enhancements` — user feedback/review submissions

Connection (`backend/db.py`) defaults, each overridable via environment variable:
`DB_HOST` (localhost), `DB_PORT` (3306), `DB_USER` (root), `DB_PASSWORD` (MyNewP@ssword20250317), `DB_NAME` (java_learning_platform). `autocommit=True`, `charset=utf8mb4`.

## Port Conflicts

- Port 5000 is used by macOS AirPlay Receiver, so the backend uses **5001**.
- Kill a stale backend: `lsof -i :5001` to find the PID, then `kill -9 <PID>`.

## Current State

- **Phase 1 — Programming Fundamentals:** 22 topics (IDs 1–22), ~25,500 lesson words.
- **Phase 2 — Developer Tools:** 4 topics (IDs 23–26): Git Fundamentals, Git Branching/Merging, Maven Fundamentals, Maven Lifecycle/Plugins.
- **Totals:** 26 topics, ~28,600 lesson words, 1,198 quiz questions, ~126 study hours.
- **Phases 3–6** (Data Structures & Algorithms, Database Fundamentals, Web Fundamentals, Spring Boot): defined in `PHASES` metadata but have no topics yet (show "Coming soon" in the sidebar).
- **App-level views:** Welcome, Overall Progress, Site Map, and Textbooks, reachable from the sidebar nav.
- **Topic tabs:** Lesson, Practice (quiz + coding exercise), Extra-Curriculum (resources), Notes (enhancements/feedback).
