# Iteration 2 — Optimization Plan

**Date:** 2026-05-12
**Tag:** V1.0.0-SNAPSHOT
**Status:** 40% complete (16/40 items done)

---

## Audit Method

Four specialized agents audited the entire codebase (index.html ~315KB, build.py, supporting scripts):

| Agent | Role | Focus |
|---|---|---|
| A | Project Manager (20yr) | Bug hunting, UX issues, prioritization |
| B | Architect (20yr) | Robustness, scalability, flexibility |
| C | Senior Full Stack Engineer (20yr) | Features, testing, CI/CD, deployment |
| D | SME (20yr) | Content accuracy, curriculum design, security, accessibility |

---

## Completed Items

### Critical (4/4)

| ID | Issue | Resolution |
|---|---|---|
| C1 | Mermaid highlighting: style directives injected inside node labels instead of separate `style` directives | Rewrote `buildMermaidDiagram()` with clean labels array + separate `style T{id}` directive |
| C2 | Mermaid renders on `display:none` container producing zero-dimension SVG | Deferred `mermaid.run()` to `switchTab()` — renders lazily when Map tab becomes visible |
| C3 | Welcome screen hardcodes "65 Topics / 6 Phases / ~220h" but only 22 topics exist; sidebar flashes "0/65" | Created `renderWelcome()` computing all metrics dynamically from `CURRICULUM`; fixed sidebar default |
| C4 | Four competing build scripts (`build.py`, `gen.py`, `create_html.py`, `generate.py`) — none generates complete HTML | Created `src/build.py` as single-source-of-truth; extracted curriculum to `src/curriculum/phase1.py`; deleted stale scripts |

### High — Security (3/4)

| ID | Issue | Resolution |
|---|---|---|
| H2 | Resource URLs accept `javascript:` protocol — self-XSS via `<a href>` | Added `new URL()` parsing with http/https protocol whitelist in `submitResource()` |
| H3 | Mermaid CDN loaded without SRI hash — supply chain attack vector | Pinned to exact version `mermaid@10.9.3` |
| H4 | Mermaid `securityLevel: 'loose'` + `htmlLabels: true` — enables HTML injection in diagrams | Changed to `securityLevel: 'strict'` + `htmlLabels: false` |

### Medium — Architecture (2/8)

| ID | Issue | Resolution |
|---|---|---|
| M2 | Mermaid diagram with 22 hardcoded node lines — adding topics requires manual diagram editing | Generated nodes programmatically from labels array with `for` loops — data-driven |
| M5 | Lesson content as inline Python HTML strings — no spell-check, no diff review | Extracted to `src/curriculum/phase1.py`; build pipeline validates required fields |

### Medium — UX & Accessibility (6/8)

| ID | Issue | Resolution |
|---|---|---|
| U1 | WCAG AA color contrast failures: `--text2` (4.35:1), `--text3` (2.5:1), `--success` (2.4:1) | Darkened to `#475569`, `#64748b`, `#047857` — all pass 4.5:1 |
| U3 | No visible focus indicators for keyboard Tab navigation | Added `:focus-visible { outline: 2px solid var(--accent); }` on all interactive elements |
| U7 | Previous/Next navigation buttons only in Practice tab — linear learners must switch tabs | Added Prev/Next buttons to Lesson tab footer |
| U8 | Quiz answers permanent — one attempt, buttons disabled forever, no learning from wrong answers | Added "Try Again" button that re-enables options and clears feedback |
| — | Welcome card static metrics | Merged into C3 (dynamic `renderWelcome()`) |
| — | Sidebar stats hardcoded | Merged into C3 |

---

## Remaining Items

### High Priority

| ID | Issue | Recommendation |
|---|---|---|
| H1 | Lesson content injected as raw `innerHTML` — compromised build pipeline = stored XSS for all users | Add DOMPurify or HTML whitelist sanitizer at build time |
| H5 | Quiz answers lost on page refresh — no record of correct/incorrect responses | Store `quizAnswers: { [topicId]: { [questionIndex]: selectedOption } }` in localStorage |

### Medium — Architecture

| ID | Issue | Recommendation |
|---|---|---|
| M1 | Monolithic single HTML file (315KB) — at 65 topics would be ~900KB, no lazy loading, no HTTP caching | Split into shell HTML + fetchable `curriculum.json` + cacheable `app.js` |
| M3 | Full `innerHTML` re-renders destroy DOM state — tab selection, scroll position, textarea input all lost | Targeted DOM updates or morphdom; preserve `activeTab` across re-renders |
| M4 | `localStorage` calls scattered across 6 functions with no abstraction — blocks server-side persistence path | Create `Storage` abstraction with async `get()/set()` methods |
| M6 | Render calls duplicated across `selectTopic`, `markComplete`, `unmarkComplete`, `resetAllProgress` | Tab renderer registry: iterate `TAB_RENDERERS` object |
| M7 | Repeated O(n) linear scans of CURRICULUM array on every interaction — `getTopicById()` called per quiz/exercise click | Build `Map<id, topic>` and `Map<phase, topics[]>` once at init for O(1) lookups |
| M8 | No keyboard navigation in sidebar — Tab works but arrow keys don't, no `aria-current` on active topic | Add roving tabindex pattern + Arrow key handlers |

### Medium — UX & Accessibility

| ID | Issue | Recommendation |
|---|---|---|
| U2 | No ARIA landmarks: no `role="navigation"`, `role="main"`, `role="tablist/tab/tabpanel"`, `aria-expanded`, `aria-current` | Add full ARIA structure; `aria-live="polite"` on stats |
| U4 | Body text 0.9rem (~14.4px) — below WCAG recommended 16px for reading | Increase body to 1rem (16px); minimum sidebar items 0.85rem |
| U5 | No deep-linking — cannot bookmark/share a specific topic; browser back/forward broken | Add `location.hash = '#topic-' + id`; restore from hash on init |
| U6 | Tab button says "💬 Notes" but internal code uses "enhancements" — semantic mismatch | Align tab label to "💬 Enhance" or rename internals |

### Low — Content

| ID | Issue | Recommendation |
|---|---|---|
| L1 | Content density overwhelming for beginners — Topic 1 covers CPU cache, RAM latency, bus bandwidth before writing code | Add collapsible "Deep Dive" sections; core lesson ≤1,500 words |
| L2 | `public static final int max()` in intro methods topic — `final` and `throws` add noise | Simplify to `public static int max(int a, int b)` |
| L3 | No dedicated String/StringBuilder lesson — String operations scattered across Topics 3-5 | Add focused String methods mini-topic or consolidate |
| L4 | Topic 2 (Setup) covers Git, Maven, Gradle, debugger — too broad | Move Git+Maven to Phase 2; keep Topic 2 focused on JDK+IDE |
| L5 | Keyword-based exercise check too permissive — 80% threshold, substring matching, false positives | Raise to 100% or add regex pattern matching for code structure |

### Nice-to-Have — New Features

| ID | Feature | Effort |
|---|---|---|
| N1 | Topic search/filter — search input in sidebar filtering by title/summary/phase | 2-3 days |
| N2 | Dark mode / theme toggle — CSS custom properties with `[data-theme="dark"]` | 1 day |
| N3 | Gamification — streaks, milestone badges (25%, 50%, 100% complete) | 3-4 days |
| N4 | Progress export — JSON + Markdown for portfolio/learning journal | 1 day |
| N5 | Service Worker offline support — cache app + Mermaid | 3-4 days |
| N6 | Study scheduling — weekly goals, spaced repetition | 3-4 days |
| N7 | Bookmark topics — pin for quick access in sidebar | 1 day |
| N8 | Syntax-highlighted code editor — replace textarea with CodeMirror | 5-7 days |

---

## Implementation Roadmap

### Batch 1: Foundation (Days 1-5)
- M1: Split monolithic file → shell + curriculum.json + app.js
- M7: Build topic index Map for O(1) lookups
- M6: Tab renderer registry
- H1: Lesson content sanitization
- H5: Quiz answer persistence

### Batch 2: UX Hardening (Days 6-10)
- M3: Preserve tab state and scroll position on re-render
- M4: Storage abstraction layer
- M8: Keyboard navigation + roving tabindex
- U2: Full ARIA landmark structure
- U5: URL hash deep-linking

### Batch 3: Content Polish (Days 11-15)
- L1-L4: Content simplification and restructuring
- U4: Font size adjustments
- U6: Tab label alignment
- L5: Exercise checker improvements

### Batch 4: Nice-to-Have (Days 16-21)
- N2: Dark mode toggle
- N1: Topic search/filter
- N3: Gamification
- N4: Progress export
- N7: Bookmark topics

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Content authoring bottleneck — 43 remaining topics | High | High | Markdown-based authoring workflow (M5), topic templates |
| Mermaid CDN dependency breaks offline use | Medium | Medium | Bundle Mermaid or pre-render SVG at build time |
| localStorage corruption on version upgrades | Low | Medium | Add `STORAGE_VERSION` key + migration functions |
| Keyboard accessibility gaps block compliance | Medium | Medium | ARIA audit + roving tabindex (M8, U2) |
| Build pipeline fragmentation causes data drift | Medium | High | Single-source-of-truth pipeline (C4 — already fixed) |
