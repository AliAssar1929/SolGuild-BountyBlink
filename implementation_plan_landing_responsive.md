# implementation_plan_landing_responsive.md
## SolGuild / BountyBlink: Landing Page Redesign, Route Fix, Full Responsiveness Pass, and Project Completion Plan

*Date: October 5, 2026 · Roles: Frontend Developer + Backend Architect · Status: AWAITING APPROVAL (no code changed yet)*

---

## 1. Research Summary (what the web says, and what we take from it)

| Source theme | Key finding | How we apply it |
|---|---|---|
| Landing-page UX 2026 | Hero must answer *What is this? Why care? What next?* in 3 seconds, with one dominant CTA | Headline ≤ 8 words, one yellow CTA, secondary link is quiet |
| Web3 UX 2026 | "Utility over spectacle": drop neon gradients and floating coins, show real product state | Hero shows a **real-looking quest card + 4-step verifier**, in the app's own style |
| Trust structure | Right after the hero, reduce fear (verifiable data, honest limits) | Trust strip under hero + a dedicated "Honest limits" block with the big AI-image note |
| Layout | Split hero (copy left, product right) is the gold standard | Keep split hero, stack on mobile with the CTA visible above the fold |
| Performance | Speed is a design feature | No new libraries, CSS-only motion, lazy sections |
| Responsive audit | Mobile-first, ≥ 44×44 px touch targets, no horizontal scroll, use `dvh` not `vh`, never disable zoom | Drives every item in Section 3 |

**Design direction (must match the web app):** warm paper `#F7F5F0`, white surfaces, hairline borders `#E3DFD6`, signal yellow `#FFD60A`, ink `#1A1A17`, Hanken Grotesk + Geist Mono, 12 px radii, restrained shadows. Quiet, editorial, confident. Not generic crypto.

---

## 2. Current State Analysis & Identified Flaws

### 2.1 Tech stack & architecture (as found)
- **Frontend:** Vue 3 + TS + Vite + Tailwind 4. A **single 1,368-line [App.vue](file:///e:/BountyBlink/frontend/src/App.vue)** is the shell, router, state manager and view for 4 tabs. There is no vue-router; routing is hand-rolled with `history.pushState` + `popstate`.
- **Backend:** FastAPI + SQLAlchemy + SQLite, Solana Devnet vault, Gemini verifier, WebSocket feed.

### 2.2 Landing page and routing flaws

| # | Flaw | Evidence |
|---|---|---|
| L-1 | **`/` does not show the landing page.** `showLanding = ref(false)`, so `/` falls into the `else` branch of `syncRouteFromPath` and renders the quest feed. | [App.vue:84](file:///e:/BountyBlink/frontend/src/App.vue#L84), `syncRouteFromPath` |
| L-2 | Landing is a **state toggle, not a route**. Clicking the logo flips a boolean; URL stays the same, refresh and back button break. | `@click="showLanding = true"` |
| L-3 | Landing copy is stale and **contradicts the product**: "no wallet needed" (Phantom is required), "creator can claim an immediate refund" (funds now stay locked), "10-minute window", Berlin/EV-charger demo, `0.01 SOL`. | [LandingPage.vue](file:///e:/BountyBlink/frontend/src/components/LandingPage.vue) |
| L-4 | GitHub link points to `VoltAgent/bountyblink`, which is not this repo. | LandingPage.vue:46 |
| L-5 | Hero phone mock is a **grey box saying "Map with task pins"**: placeholder visuals, fixed `280×520`. | LandingPage.vue:57-63 |
| L-6 | Brand name inconsistent: SolGuild vs BountyBlink; `<title>` says "Anime Adventurer Guild". No meta description, no OG tags. | [index.html](file:///e:/BountyBlink/frontend/index.html) |
| L-7 | No honest "MVP / no AI-image detection" notice on the landing page (only in README). | n/a |
| L-8 | Landing tone is dry and technical; README tone (guild voice, plain words) is preferred by the owner. | n/a |

### 2.3 Responsiveness flaws (page by page)

**Critical (blocks mobile use)**
| # | Where | Problem |
|---|---|---|
| R-1 | App shell header nav | `nav class="hidden md:flex"`: **on phones there is no navigation at all** to Issue a Quest, Activity, or Guild License. |
| R-2 | `index.html` viewport | `maximum-scale=1.0, user-scalable=no` **disables pinch-zoom** (accessibility failure). |
| R-3 | App shell | `h-screen w-screen overflow-hidden`: on mobile browsers `100vh` includes the hidden URL bar, so the **bottom of every page, including the sticky Claim/Submit button, is cut off**. |
| R-4 | Post tab | Parent is `overflow-hidden` with `flex-col`: on mobile the form and the 420 px spec aside are stacked inside a non-scrolling parent, so the **spec/summary section is unreachable or clipped**. |
| R-5 | Activity tab | Same `flex-col + overflow-hidden` pattern; the detail drawer renders under the list with no scroll path. |
| R-6 | Feed tab on mobile | Map and list each get `h-1/2` of the leftover space (≈ 25% of the screen each). The task detail with Claim/Submit is cramped; no way to collapse the map. |

**High**
| # | Where | Problem |
|---|---|---|
| R-7 | Header right cluster | "Demo tools" + License chip + wallet chip + Connect have no wrapping or collapse; overflows at ≤ 400 px. |
| R-8 | [UserProfileModal.vue](file:///e:/BountyBlink/frontend/src/components/UserProfileModal.vue), [WalletModal.vue](file:///e:/BountyBlink/frontend/src/components/WalletModal.vue), [DemoToolsDrawer.vue](file:///e:/BountyBlink/frontend/src/components/DemoToolsDrawer.vue) | Modal cards have **no `max-height` / `overflow-y-auto`**, so on short phones and landscape the buttons fall off-screen and cannot be scrolled to. |
| R-9 | [SensitiveDossierModal.vue](file:///e:/BountyBlink/frontend/src/components/SensitiveDossierModal.vue) | Uses `max-h-[90vh]` (not `dvh`); keyboard on mobile overlaps the textarea. |
| R-10 | [PostTaskForm.vue](file:///e:/BountyBlink/frontend/src/components/PostTaskForm.vue) | `grid-cols-3` (categories) and `grid-cols-2` (reward / time) with no mobile fallback; cramped at 320-360 px. |
| R-11 | [ProfileView.vue](file:///e:/BountyBlink/frontend/src/components/ProfileView.vue) | `grid-cols-3` stats row, `md:w-[480px]` right pane; nested `overflow-hidden` means inner panes may not scroll on mobile. |

**Medium**
| # | Where | Problem |
|---|---|---|
| R-12 | Global | Most buttons are `h-8` (32 px) with 11-13 px text; below the 44 px touch-target guideline. |
| R-13 | [TaskFilters.vue](file:///e:/BountyBlink/frontend/src/components/TaskFilters.vue) | Horizontal scroll works but has no edge fade, so it is not discoverable. |
| R-14 | [MapCanvas.vue](file:///e:/BountyBlink/frontend/src/components/MapCanvas.vue) | Zero responsive logic; needs `resize()` on layout change and a min-height guard. Map CSS loaded from `unpkg` CDN while `maplibre-gl` is also a dependency. |
| R-15 | Global | No `prefers-reduced-motion`, no `:focus-visible` rings, icon-only buttons lack `aria-label`s. |
| R-16 | `Detail text` | Several 11 px labels; low legibility on phones. |

**Dead / duplicate components (report only, no deletion without approval):** `HelloWorld.vue`, `DemoDrawer.vue` (duplicate of `DemoToolsDrawer.vue`), `VerificationStepper.vue` (superseded by `VerificationSteps.vue`), `TaskCard.vue`, `ConfidenceRing.vue`, `EscrowChip.vue`, `StatusStamp.vue` appear unused.

---

## 3. Step-by-Step Implementation Plan

### Phase A: Routing (smallest change first)
1. Replace `showLanding` boolean with a `route`-derived computed: `isLanding = path === '/' || path === ''`.
2. `/` renders **LandingPage**. App lives at `/quests`, `/issue`, `/activity`, `/profile` (unchanged URLs).
3. Landing CTAs call `navigateTo('feed')` (`pushState('/quests')`); the app logo calls `pushState('/')`. Back/forward and refresh then work via the existing `popstate` listener.
4. Unknown paths redirect to `/` (simple 404 fallback).
5. Add the production note: static hosting needs an SPA rewrite to `index.html`.
- *No new library introduced (rule 8).*

### Phase B: Landing page rebuild (new `LandingPage.vue`, split into small presentational sections)
Sections, in the README's voice (guild tone, plain words):

| # | Section | Content |
|---|---|---|
| 1 | **Nav** | Logo + Devnet pill, anchor links, yellow "Enter the Guild Board" |
| 2 | **Hero** | H1: *"Post the quest. Lock the reward. Bring the proof."* Sub: guild-board story in one sentence. One yellow CTA + quiet "How it works" link. Right: **live product preview** (a real quest card + the 4-step verifier + escrow chip) |
| 3 | **Trust strip** | Solana Devnet · Every payout on Explorer · 8 European cities · live **88+ quests** count from `/api/tasks` |
| 4 | **The problem → our answer** | Three everyday examples (lost cat, drunk friend's car, shop video) and "nobody has to trust anybody" |
| 5 | **How a quest works** | 4 steps: Lock · Claim · Proof · Payout, with a vertical line on mobile |
| 6 | **Three guild boards** | Civil Help · Sensitive · Commercial cards with examples and what proof is needed |
| 7 | **Three proof gates** | Right place? Right thing? Real photo? |
| 8 | **When a quest fails** | "Reward stays locked, quest returns with Failed 1x" with the red rejection card shown as a visual |
| 9 | **Ranks** | F → S ladder, 50 EXP per quest |
| 10 | **Honest limits** | Big callout: *MVP, no anti-AI-image detection, Devnet only* (mirrors README) |
| 11 | **FAQ** | Rewritten to match reality (Phantom needed, funds stay locked on fail) |
| 12 | **Final CTA + footer** | Correct repo link (will ask for the real URL), Team placeholder removed |

**UX/visual rules**
- Only existing tokens (paper, white, hairline, yellow, ink). No gradients-for-decoration, no stock imagery.
- Motion: CSS-only scroll-reveal via `IntersectionObserver`, 150-250 ms, fully disabled under `prefers-reduced-motion`.
- Type: fluid `clamp()` headings, 16 px minimum body on mobile.
- Mobile-first: hero CTA visible without scrolling at 360×640; sticky bottom CTA bar on mobile after the hero scrolls away.
- SEO/a11y: one `h1`, landmark tags, `aria-label` on icon buttons, visible focus rings, update `<title>` + meta description + OG tags.
- Data: landing stats via a tiny `useLandingStats` composable (logic separate from presentation, rule 13).

### Phase C: Responsiveness fixes (by priority, matches Section 2.3)
| Item | Fix |
|---|---|
| R-1 | Add a **bottom tab bar on mobile** (Quests · Issue · Activity · License) with 44 px targets, hidden at `md+`; header nav stays on desktop |
| R-2 | Remove `maximum-scale` / `user-scalable=no` |
| R-3 | `h-screen` → `h-dvh`; sticky action bars respect `env(safe-area-inset-bottom)` |
| R-4 / R-5 | Mobile: tab body scrolls as one column (`overflow-y-auto`), `md:overflow-hidden` split panes kept on desktop only |
| R-6 | Mobile feed: **map/list toggle** (segmented control); list is default, map on demand; detail takes full height |
| R-7 | Header right cluster collapses: wallet chip only on mobile, Demo tools moves into an overflow/menu item |
| R-8 / R-9 | All modals: `max-h-[100dvh-2rem] overflow-y-auto`, bottom-sheet on mobile |
| R-10 / R-11 | Grids become `grid-cols-1 sm:grid-cols-2/3`; inner panes get their own scroll on mobile |
| R-12 | Min 44 px interactive height (visual size can stay, padding grows hit area) |
| R-13 | Edge-fade mask on filter chips |
| R-14 | `map.resize()` on tab/panel change; self-host maplibre CSS via package import |
| R-15 / R-16 | Global `:focus-visible`, `prefers-reduced-motion`, aria-labels, minimum 12 px text |

### Phase D: Verification
- `npm run build` clean (type-check).
- Browser pass at **320, 360, 390, 768, 1024, 1440** wide + landscape phone: no horizontal scroll, all CTAs reachable, modals scrollable.
- Check `/` → landing, `/quests` → app, refresh and back/forward on each route.
- Atomic commits per phase (A routing, B landing, C responsive, D docs), per Rule 1.

### Phase E: Documentation
- README: update screenshots section and routes note; keep the BIG NOTE.
- Comment non-trivial logic (route sync, mobile nav).

---

## 4. Full Plan to Complete the Project (beyond UI)

### 4.1 Must fix before any judge or public use (security / correctness)
| Priority | Item | Why |
|---|---|---|
| P0 | **Rotate the Gemini key**; remove hardcoded value from `config.py` (it is in git history) | Key leaked in repo |
| P0 | `/refund` and `/approve` must verify the caller owns the task (signed wallet message) and that refund goes to `task.poster_address`, not request body | Anyone can drain the vault today |
| P0 | `POST /api/tasks` must **verify the deposit tx on Solana** (amount, destination = vault, sender = poster, not reused); remove the `FUND_…` fallback | Fake quests / unfunded escrow |
| P1 | Real **wallet signature auth** (nonce flow already exists but accepts `phantom_devnet_verified`) | Anyone can impersonate any address |
| P1 | Remove `dev_code` from email API response; real email provider | OTP bypass |
| P1 | Lock `/api/demo/reset` and fixtures behind a `DEMO_MODE` env flag | Public wipe of data |
| P1 | CORS: restrict from `*` | Hardening |
| P1 | Rate-limit faucet (it spends real vault SOL) | Vault drain |

### 4.2 Product completeness
- **Anti-AI-image detection** (top product gap): provenance checks (C2PA), generated-image classifier, live in-app camera capture with a one-time challenge code.
- Move the vault logic into an **Anchor program** so rules are enforced on-chain.
- Poster-side review for Sensitive quests before payout; dispute path.
- Duplicate-hash enforcement across all submissions (hash is stored, not checked).
- Server-side claim expiry job (currently only on list fetch).
- Proper DB migrations (Alembic) instead of manual `ALTER TABLE`.
- Pagination for `/api/tasks`; index on `(city, category, status)`.
- Automated tests: verifier gates, claim/expire/reopen, payout idempotency.
- Split `App.vue` into route views (`FeedView`, `IssueView`, `ActivityView`) + composables (`useTasks`, `useActivity`, `useVerification`) per Rule 13. **Only with approval, as a separate step.**

### 4.3 Cleanup requiring explicit approval (Rule 7)
Delete or archive the unused components listed in Section 2.3.

---

## 5. Data-Flow Impact
- **No backend or schema changes** for Phases A-D. Landing stats reuse `GET /api/tasks`.
- Routing change affects only the client: initial paint on `/` becomes landing instead of the feed; deep links (`/quests/:id`, `/issue`, `/activity`, `/profile`) keep working.
- Mobile tab bar and map/list toggle are pure UI state (no new API).

## 6. Constraints, Risks & Assumptions
- **Scope discipline (Rule 2):** Phases A-D touch landing, routing and responsiveness only. Visual styling of the web app is preserved; only layout containers and sizing change where Section 2.3 requires it.
- **Risk:** `App.vue` is one large file; responsive edits there are the riskiest. Mitigation: small commits and a build after each.
- **Risk:** `h-dvh` needs modern browsers (all current evergreen); fallback `h-screen` kept via `supports`.
- **Assumption:** The brand shown to users stays **SolGuild** (with BountyBlink as the repo/project name) unless told otherwise.
- **Assumption:** No new dependencies (no vue-router) to respect Rule 8.

## 7. Open Questions (need your answer before execution)
1. Mobile navigation style: bottom tab bar (recommended) or hamburger menu?
2. Real GitHub repository URL for the landing page and footer link?
3. Include the **Phase 4.1 P0 security fixes** in this run, or only the landing + responsive work?
4. Approve deleting unused components, or keep them?
