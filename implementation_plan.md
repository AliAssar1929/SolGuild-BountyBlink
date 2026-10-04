# implementation_plan.md — BountyBlink 3-Hour Devnet Mobile MVP (Ultra-Deep Architecture & Flaw Audit)
*Date: October 4, 2026 | Target: Solana Devnet Colosseum MVP | Stack: Vue 3 + FastAPI + Solana-py*

---

## 1. Deep Dive: Current State, Advantages & Exhaustive Flaw Analysis

### 1.1 Architectural Advantages
1. **Zero-Friction Judge Onboarding (Sub-60s Time to Payout)**:
   - Eliminates Phantom/Solflare extension installation hurdles by using an ephemeral client-side Devnet keypair stored in `localStorage`, pre-funded via the backend faucet.
   - Test fixture buttons ("Test: Valid photo" and "Test: Fake photo") guarantee reliable verification results during rapid judging without requiring field movement.
2. **Deterministic Settlement Flow on Solana Devnet**:
   - Uses native SOL transfers (0.01 SOL) rather than custom SPL tokens, completely bypassing associated token account (ATA) initialization overhead, rent fees, and token faucet rate-limits.
   - Direct on-chain confirmation links to Solana Explorer (`cluster=devnet`) provide unforgeable cryptographic proof of escrow lock and release.
3. **Targeted Mobile Viewport Experience**:
   - Constrained 430px mobile viewport matches real-world field worker ergonomics.
   - Eliminates layout fragmentation and ensures immediate responsive utility.
4. **Utilitarian "Field Operations" Design Stance**:
   - Distinct anti-AI look: avoids neon gradients, glassmorphism, floating cards, and dark blobs.
   - Embraces paper-white canvas, ticket-style perforated edges, high-contrast monospace financial data, and ink-black typography.

---

### 1.2 Identified Flaws, Bottlenecks & Critical Failure Modes (Pre-Mortem Audit)

| # | Flaw / Bottleneck Category | Technical Vulnerability | Impact | 10x Architectural Mitigation & Resolution |
|---|----------------------------|-------------------------|--------|-------------------------------------------|
| **F-01** | **Solana Devnet RPC Instability & Rate Limits** | Public `api.devnet.solana.com` frequently experiences 429 Too Many Requests, socket dropouts, or delays exceeding 15 seconds during transaction confirmation. | Demo fails or hangs with infinite spinners during judging. | **Multi-RPC Fallback Pool & Local Mock/Replay Fallback**: Configure a resilient RPC client with exponential backoff across multiple RPC endpoints (e.g. Ankr, QuickNode, Helius, Solana public). In the event of persistent network partition, seamlessly fall back to local cryptographic simulation with pre-cached Devnet explorer links and clear badge indicators. |
| **F-02** | **Custodial Trust & Key Exposure Risk** | Using a single backend escrow wallet without per-task derivation or transaction locking can lead to double-spend race conditions if two claims settle simultaneously. | Race condition / double-settlement of task bounty. | **Database Row-Level State Locks & Idempotency Keys**: Use SQLite atomic transactions (`BEGIN IMMEDIATE`) with state transitions strictly conditioned on `status == 'CLAIMED'`. Every settlement generates an idempotency key (`hash(task_id + claim_id + worker_address)`) checked before signing the payout transfer. |
| **F-03** | **Vision API Latency & Network Failure** | Relying synchronously on remote Multimodal Vision APIs (Gemini Flash / OpenAI Vision) introduces 2–6 second latency, payload size timeouts, and API quota risks. | Submission hangs at Tier 2 verification step; judges wait indefinitely. | **Three-Layer Vision Engine (API + Embedded Local Heuristic + Instant Preset Cache)**: Compute SHA-256 and perceptual hash immediately. If hash matches test fixtures, return verified result in <200ms. If live photo is uploaded, call Vision API with 8s strict timeout; if unavailable, seamlessly fall back to an on-device/backend image-integrity heuristic (EXIF luminance, sharpness, compression artifact audit) so verification never hangs. |
| **F-04** | **Browser Geolocation Stripping & Mobile HTTPS Requirements** | Modern browsers (especially Safari iOS and Chrome Mobile) strictly reject `navigator.geolocation` on non-HTTPS origins and silently strip EXIF metadata from file inputs (`<input type="file">`). | Real mobile capture fails to report coordinates or gets rejected for missing GPS. | **Dual Coordinate Intake Strategy**: Collect device coordinates directly via the browser Geolocation API at the moment of button tap, and merge with EXIF tags parsed via `piexif`/`exifread`. If metadata is stripped, mark confidence as `Device-Reported (Low Trust)` and allow verification if within 150m. Provide explicit mock location slider / preset pins for testing. |
| **F-05** | **Task Collisions & Unbounded Claims** | Multiple workers claiming the same bounty simultaneously, or a single worker abandoning a claimed task, locking funds indefinitely. | Deadlocked task bounties; poster cannot recover funds. | **Atomic Lease Timer (10-minute Lock Window)**: Claims include an explicit `expires_at` timestamp. Background query or lazy evaluation on list fetch auto-reverts expired claims back to `OPEN` state, freeing the bounty. |
| **F-06** | **Client Wallet State Desynchronization** | Browser localStorage gets cleared or out-of-sync with backend ledger; worker attempts claim without valid public key. | Client-side runtime crashes (`Invalid PublicKey`). | **Self-Healing Keypair Composable**: Validates base58 public/secret keys on app mount. If corrupted or missing, regenerates keypair and requests instant backend airdrop via internal faucet endpoint. |

---

## 2. Complete Technical Specification & Stack Definition

```
========================================================================================
BOUNTYBLINK SYSTEM ARCHITECTURE
========================================================================================
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                 FRONTEND (VUE 3 SPA)                                 │
│  - Max-Width: 430px (Centered Mobile Viewport with Paper-White Field Order Theme)     │
│  - Composition API, Vite, TypeScript, Tailwind CSS, Lucide Icons                     │
│  - Ephemeral Solana Web3 Demo Wallet (localStorage Base58 Keypair)                   │
├──────────────────────────────────────────┬───────────────────────────────────────────┤
│                TAB 1: DO TASKS           │               TAB 2: POST TASK            │
│  - Live Task Feed (Distance, Reward SOL) │  - Quick Preset Work Orders (EV, Shop)    │
│  - Perforated Ticket Task Details        │  - Custom Bounty Pin & Radius             │
│  - Camera & File Intake Flow             │  - Devnet 0.01 SOL Escrow Lock Action     │
│  - One-Tap Presets: Valid vs Fake Fixture│  - Direct Solana Explorer Transaction Link│
│  - Real-Time 4-Step Verification Stepper │  - Refund Trigger for Expired Bounties    │
└──────────────────────────────────────────┴───────────────────────────────────────────┘
                                   │ HTTP REST API / JSON-RPC
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                               BACKEND SERVICE (FASTAPI)                              │
│  - Python 3.12, FastAPI, Uvicorn, SQLite (SQLAlchemy / SQLModel)                      │
│  - Task & Claim State Machine Engine (Atomic Leases, Expiry Reversions)              │
│  - Multi-RPC Devnet Transaction Relayer (solders + solana-py)                         │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                             VERIFICATION PIPELINE SERVICE                            │
│  ┌────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Tier 0: Intake Sanity & SHA-256 / Perceptual Duplicate Hash Detection          │  │
│  ├────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Tier 1: Geofence (Haversine Formula <= 150m, EXIF vs Browser GPS Arbitrage)    │  │
│  ├────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Tier 2: Multimodal Vision Evaluation (Structured JSON, Prompt-Hardened, Cache) │  │
│  ├────────────────────────────────────────────────────────────────────────────────┤  │
│  │ Tier 3: Solana Devnet Settlement (Escrow Vault -> Worker Transfer on Chain)   │  │
│  └────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────┘
                                   │ On-Chain Transactions
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              SOLANA DEVNET CLUSTER                                   │
│  - Escrow Vault Keypair: holds locked 0.01 SOL bounties                              │
│  - Poster Wallet: transfers 0.01 SOL upon task creation                             │
│  - Worker Wallet: receives 0.01 SOL upon Tier 2 verification pass                    │
│  - Explorer Links: https://explorer.solana.com/tx/{sig}?cluster=devnet              │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Database Schema & Data Models (SQLite / SQLAlchemy)

### 3.1 Tables & Indices

#### 1. `tasks`
- `id` (VARCHAR(36), PK): UUID4 unique identifier.
- `title` (VARCHAR(120), NOT NULL): Short operational task name (e.g. *"Check Alexanderplatz EV Charger"*).
- `instruction` (TEXT, NOT NULL): Clear physical verification instruction.
- `target_description` (TEXT, NOT NULL): Specific visual cues expected by the vision model.
- `latitude` (FLOAT, NOT NULL): Target latitude coordinates.
- `longitude` (FLOAT, NOT NULL): Target longitude coordinates.
- `radius_meters` (INTEGER, DEFAULT 150): Geofence tolerance limit.
- `reward_sol` (FLOAT, DEFAULT 0.01): Bounty amount in native SOL.
- `poster_address` (VARCHAR(44), NOT NULL): Base58 public key of task creator.
- `status` (VARCHAR(20), NOT NULL): Enum (`OPEN`, `CLAIMED`, `PAID`, `REJECTED`, `REFUNDED`).
- `fund_tx_sig` (VARCHAR(88), NULL): On-chain transaction signature for escrow funding.
- `payout_tx_sig` (VARCHAR(88), NULL): On-chain transaction signature for worker payout.
- `refund_tx_sig` (VARCHAR(88), NULL): On-chain transaction signature for creator refund.
- `created_at` (DATETIME, NOT NULL): Creation timestamp.
- `expires_at` (DATETIME, NOT NULL): Bounty deadline (default 24h from creation).

#### 2. `claims`
- `id` (VARCHAR(36), PK): UUID4 identifier.
- `task_id` (VARCHAR(36), FK -> `tasks.id`, NOT NULL): Referenced task.
- `worker_address` (VARCHAR(44), NOT NULL): Base58 public key of claiming worker.
- `claimed_at` (DATETIME, NOT NULL): Claim initiation timestamp.
- `expires_at` (DATETIME, NOT NULL): Claim exclusive lease deadline (default 10 mins).
- `status` (VARCHAR(20), NOT NULL): Enum (`ACTIVE`, `SUBMITTED`, `EXPIRED`, `RELEASED`).

#### 3. `submissions`
- `id` (VARCHAR(36), PK): UUID4 identifier.
- `task_id` (VARCHAR(36), FK -> `tasks.id`, NOT NULL): Target task.
- `claim_id` (VARCHAR(36), FK -> `claims.id`, NOT NULL): Associated claim.
- `worker_address` (VARCHAR(44), NOT NULL): Submitting worker.
- `file_hash` (VARCHAR(64), NOT NULL): SHA-256 digest of uploaded evidence.
- `perceptual_hash` (VARCHAR(32), NULL): Image perceptual hash.
- `image_path` (VARCHAR(255), NOT NULL): Path to stored image on disk.
- `submitted_lat` (FLOAT, NULL): Geolocation latitude reported or extracted.
- `submitted_lon` (FLOAT, NULL): Geolocation longitude reported or extracted.
- `location_source` (VARCHAR(20), NOT NULL): Enum (`EXIF_GPS`, `BROWSER_GPS`, `FIXTURE`).
- `distance_meters` (FLOAT, NULL): Computed Haversine distance to target.
- `tier0_pass` (BOOLEAN, NOT NULL): Intake & anti-duplicate check.
- `tier1_pass` (BOOLEAN, NOT NULL): Geofence boundary check.
- `tier2_pass` (BOOLEAN, NOT NULL): Vision model validation.
- `vision_confidence` (FLOAT, NULL): Vision model score (0–100).
- `vision_reason` (TEXT, NULL): Structured reasoning from verifier.
- `final_status` (VARCHAR(20), NOT NULL): Enum (`PAID`, `REJECTED`).
- `created_at` (DATETIME, NOT NULL): Timestamp of submission.

---

## 4. API Endpoints Specification

| Method | Endpoint | Description | Request Body / Params | Response Payload |
|---|---|---|---|---|
| `GET` | `/api/tasks` | List all open and active tasks | `status?: string, lat?: float, lon?: float` | `TaskSummary[]` |
| `GET` | `/api/tasks/{task_id}` | Detailed task data, status & tx links | None | `TaskDetail` |
| `POST` | `/api/tasks` | Create new bounty & lock 0.01 SOL in escrow | `{ title, instruction, target_description, lat, lon, reward_sol, poster_address }` | `{ task: Task, fund_tx_sig: string, explorer_url: string }` |
| `POST` | `/api/tasks/{task_id}/claim` | Worker exclusively claims task for 10 mins | `{ worker_address: string }` | `{ claim: Claim, expires_at: string }` |
| `POST` | `/api/tasks/{task_id}/submit` | Submit evidence (multipart photo or fixture) | Multipart: `photo?: UploadFile, fixture_type?: "VALID" \| "FAKE", browser_lat?: float, browser_lon?: float, worker_address: string` | `{ result: SubmissionResult, payout_tx_sig?: string, reason: string }` |
| `POST` | `/api/tasks/{task_id}/refund` | Refund locked funds back to poster if failed/expired | `{ poster_address: string }` | `{ refund_tx_sig: string, explorer_url: string }` |
| `GET` | `/api/wallet/faucet/{address}` | Airdrop / transfer 0.02 Devnet SOL to demo wallet | None | `{ tx_sig: string, balance: float }` |
| `POST` | `/api/demo/reset` | Purge database & re-seed standard tasks & fixtures | None | `{ status: "ok", tasks_count: int }` |
| `GET` | `/api/demo/presets` | Get pre-packaged valid/fake image fixtures | None | `{ valid_fixture: FixtureMeta, fake_fixture: FixtureMeta }` |

---

## 5. UI/UX & Visual Design System (Anti-AI Utilitarian Stance)

### 5.1 Design Tokens & Colors
- **Canvas / Background**: `#F8F6F0` (warm off-white unbleached stock paper).
- **Secondary Surfaces**: `#EFECE4` (subtle contrast card backgrounds).
- **Ink / Text Primary**: `#161614` (dense deep charcoal ink, contrast ratio > 12:1).
- **Ink Secondary**: `#63625C` (muted slate annotations and metadata).
- **Signal Orange (Action Accent)**: `#EA580C` / `#D9480F` (high-visibility safety orange for primary CTA buttons).
- **Settlement Green (Pass Only)**: `#15803D` (deep forest green stamp).
- **Rejection Red (Fail Only)**: `#B91C1C` (crimson warning stamp).
- **Strictly Banned**: No purple/cyan gradients, no neon buttons, no frosted blurred glass panels, no floating angled 3D mockups.

### 5.2 Typography
- **Headlines**: `Fraunces`, `serif` — used sparingly for operational titles and screen headers.
- **Interface & Body**: `Inter Tight`, `-apple-system`, `sans-serif` — compact, legible UI typography.
- **Numbers, Hashes, Coordinates & Currency**: `JetBrains Mono` or `Geist Mono` — tabular numerals enabled (`font-variant-numeric: tabular-nums`).

### 5.3 Ergonomics & Layout
- Centered container with `max-w-[430px]`, full min-h-screen, safe-area insets (`env(safe-area-inset-bottom)`).
- Sticky bottom action bar within natural thumb reach (>48px touch targets).
- Perforated ticket styling: dashed separating rules (`border-dashed border-stone-300`), barcode/ID badges, and physical work-order stamps.

---

## 6. Execution Order & Implementation Phases

1. **Step 1: Backend Foundation & Multi-RPC Solana Service**:
   - Establish `/backend` virtualenv and install dependencies.
   - Configure SQLite models with automated seed migration.
   - Implement `solana_service.py` with multi-RPC fallback, Devnet transfer logic, balance queries, and explorer URL builders.
   - Implement `verifier_service.py` (Tier 0 duplicate hash, Tier 1 Haversine distance, Tier 2 vision analysis with fixture cache).
   - Expose and test all REST endpoints.
2. **Step 2: Seed Fixture Assets & Ground-Truth Test Cases**:
   - Prepare bundled high-res fixture images:
     - `valid_storefront.jpg`: Matching GPS within 50m of preset task, authentic daylight photo of shop.
     - `fake_screen_capture.jpg`: Moire patterns/mismatched coordinates/stock photo of storefront.
3. **Step 3: Frontend Scaffolding & Mobile Shell**:
   - Scaffold Vite + Vue 3 + TypeScript in `/frontend`.
   - Setup Tailwind theme tokens, typography, and mobile frame.
   - Implement in-app ephemeral Solana Keypair manager (`useWallet.ts`) with zero-friction airdrop check.
4. **Step 4: Do Tasks & Post Task Views**:
   - Build **Do Tasks** feed with ticket cards, distance calculators, and live status badges.
   - Build **Task Detail & Claim** flow with active 10-minute lease countdown.
   - Build **Submission & Verification Stepper**:
     - Live 4-step stepper with animated progress transitions.
     - One-click **"Test: Valid photo"** and **"Test: Fake photo"** fixture buttons alongside native camera upload.
   - Build **Post Task** form with one-tap presets, instant 0.01 SOL escrow lock, and Explorer link generation.
5. **Step 5: End-to-End Verification & Flaw Audit Validation**:
   - Verify valid flow: Task Claim -> Submit Valid Fixture -> Pass Tier 0/1/2 -> Escrow transfers 0.01 SOL to worker -> Valid Devnet tx hash verified.
   - Verify invalid flow: Task Claim -> Submit Fake Fixture -> Fail Tier 1/2 -> Reason displayed -> Refund button returns 0.01 SOL to poster -> Devnet tx hash verified.
   - Review and ensure compliance with all user rules.
