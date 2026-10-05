# implementation_plan.md — Verification Rejection Workflow, Locked Escrow Retention & Failed Attempt Counter

*Date: October 5, 2026 | Focus: Verification Stepper State, On-Chain Escrow Security, Reopen with Failed Counter*  
*Roles: Backend Architect & Frontend Developer*

---

## 1. Executive Summary & Root Cause Analysis

### 1.1 The User's Problem
When a worker claims a quest and submits a photo that does not match the quest description:
1. **Verification Stepper Hung on Step 4:**
   - Step 3 ("Photo checked") incorrectly displayed "Passed" with a checkmark.
   - Step 4 ("Reward released") hung in an infinite spinner with "Checking...", even though the AI verifier had already rejected the evidence.
   - The user had to click "Technical details" to even see the rejection message.
   - The user requested:
     - Clear loading wheel during the check.
     - Upon rejection: Step 3 marked "Rejected", Step 4 marked "Withheld in Escrow".
     - A prominent rejection verdict card displaying the reason description message for **5 seconds**.
2. **Escrow Funds Prematurely Refunded to Poster's Wallet:**
   - Instead of keeping the deposited bounty secured in the smart contract escrow, the UI displayed a prominent "Refund reward to poster" button.
   - Clicking this button initiated an on-chain transfer of SOL from the escrow vault directly back to the poster's personal wallet and marked the task `REFUNDED` ("Returned").
   - Combined with earlier test devnet airdrops, the user's wallet jumped by ~0.3 SOL, making it appear that they received multiple times their quest deposit.
   - **Correct Protocol**:
     - When a worker fails a photo check, the bounty funds **MUST REMAIN LOCKED IN ESCROW**.
     - The quest must **NOT** be labeled `Returned` or permanently closed.
     - The quest must be returned to the open guild board for **another user to claim**.
     - The quest must display a **`Failed 1x`** (or `Failed {n}x`) badge to show that an attempt was made and failed.

---

## 2. Flaw Detection & Architectural Mapping

| # | Component | Current State | Identified Flaw | Architectural Solution |
|---|---|---|---|---|
| **F-08** | **`VerificationSteps.vue`** | Stepper only checks `currentStep > step.id` and `currentStep === step.id`. | When rejection occurs, `currentStep` was set to 4. Step 3 falsely showed "Passed" and Step 4 showed a spinning `Loader2` ("Checking..."). | Update `VerificationSteps.vue` to receive `status` (`'PAID' | 'REJECTED' | 'CHECKING'`). If rejected, Step 3 displays a red `X` with "Rejected" and Step 4 displays "Reward withheld in escrow". |
| **F-09** | **Rejection UI & Feedback Timer** | Result verdict is immediately shown above a "Refund reward to poster" button; no timed transition. | Claimant / viewer is confused by the hanging stepper and is tempted to click the manual refund button. | Add an explicit 5-second countdown banner with the exact AI failure reason and an animated progress bar: "Verification Rejected. Reopening quest to guild board in 5s... Funds remain secured in escrow." |
| **F-10** | **Backend Verification Settlement (`/api/tasks/{task_id}/submit`)** | On `passed == False`, sets `task.status = "REJECTED"`, leaves `active_claim_id` occupied. | Task dies in `REJECTED` state and cannot be claimed by any other adventurer. Reward is orphaned until manual refund. | On `passed == False`: set `task.status = "OPEN"`, increment `task.failed_attempts += 1`, set claim status to `"FAILED"`, clear `task.active_claim_id = None`. Reward stays locked in escrow (`fund_tx_sig`). |
| **F-11** | **Database Schema (`tasks` table)** | `Task` table does not track failed attempts. | Frontend cannot know how many times a quest has failed verification. | Add `failed_attempts INTEGER DEFAULT 0` column to `tasks` table and update SQLAlchemy `Task` model. |
| **F-12** | **Frontend Badges & Labels** | `StatusWord.vue` and `StatusStamp.vue` only recognize `OPEN`, `CLAIMED`, `PAID`, `REFUNDED`. | Shows `Returned` if refunded, but no representation of `Failed 1x` for active re-opened quests. | Add `Failed 1x` amber/rose badge styling to `StatusWord.vue`, `StatusStamp.vue`, quest feed cards, and Activity drawer. |
| **F-13** | **Active User Task State** | Task `547e6289-dc3b-40c3-a7e3-7ef524b38b91` is currently in `REFUNDED` state. | Inconsistent with the intended workflow. | Migrate/update the task record: set `status = "OPEN"`, `failed_attempts = 1`, `refund_tx_sig = None`, `active_claim_id = None`. Funds stay locked under `fund_tx_sig`. |

---

## 3. Step-by-Step Implementation Plan

### Step 1: Database Schema & Migration
- Add `failed_attempts` column (`Integer, default=0`) to `Task` model in `backend/models.py`.
- Run SQLite `ALTER TABLE tasks ADD COLUMN failed_attempts INTEGER DEFAULT 0;` migration.
- Restore task `547e6289-dc3b-40c3-a7e3-7ef524b38b91` to `OPEN`, `failed_attempts = 1`, `refund_tx_sig = None`.

### Step 2: Backend Logic Update (`backend/main.py`)
- In `submit_evidence`:
  - If `passed == False`:
    - Increment `task.failed_attempts = (task.failed_attempts or 0) + 1`
    - Reset `task.status = "OPEN"` (reopened for guild claimants)
    - If `task.active_claim_id`: mark `Claim.status = "FAILED"`
    - Clear `task.active_claim_id = None`
    - Do NOT call `solana_service.transfer_sol` (funds remain in escrow)
    - Broadcast WebSocket event `SUBMISSION_VERIFIED` with `status: "OPEN"`, `passed: false`, `failed_attempts: task.failed_attempts`
  - In `get_tasks` & task serializer: ensure `failed_attempts` is returned in JSON payloads.

### Step 3: Stepper Component Overhaul (`VerificationSteps.vue`)
- Accept `status` prop (`'PAID' | 'REJECTED' | 'CHECKING'`).
- Step 3 ("Photo checked"):
  - If `currentStep === 3` and checking: Spinning loader + "Checking..."
  - If `currentStep >= 3` and `status === 'PAID'`: Green checkmark + "Passed"
  - If `status === 'REJECTED'`: Red `X` icon + "Rejected"
- Step 4 ("Reward released"):
  - If `status === 'PAID'`: Green checkmark + "Reward released"
  - If `status === 'REJECTED'`: Lock/Shield icon + "Reward withheld in escrow"
  - If pending: Gray number + "Pending"

### Step 4: Submission Feedback & 5-Second Countdown (`App.vue`)
- When `submitEvidence` receives `status === 'REJECTED'`:
  - Display the rejection card:
    - Red badge: `Verification Rejected`
    - Reason description: AI verifier explanation of why the evidence was rejected.
    - Animated 5-second countdown timer: `5s... 4s... 3s... 2s... 1s`
    - Subtext: `Bounty remains secured in Solana escrow. Re-opening quest for other adventurers.`
  - When the 5-second timer completes:
    - Clear `isSubmitting` and `verificationResult`
    - Refresh tasks from backend
    - Selected task updates to `status = 'OPEN'` with badge `Failed 1x`
    - Button resets to "Claim this task" (ready for another worker)
  - Remove the automatic `"Refund reward to poster"` button on failed worker submissions.

### Step 5: Badges & Display (`StatusWord.vue`, `StatusStamp.vue`, `App.vue`)
- When `task.failed_attempts > 0` and `task.status === 'OPEN'`:
  - Show amber/crimson badge: `Failed {n}x` (e.g. `Failed 1x`)
  - Tooltip/description: "Previous attempt failed photo verification. Bounty remains locked in escrow."
- In Activity view:
  - Display `Failed 1x` badge alongside "Held in Escrow".

### Step 6: Testing & Verification
- Verify database migration and state of user's task.
- Build frontend (`npm run build`).
- Verify via browser / API that submission failure triggers the 5-second countdown and reopens the task as `Failed 1x`.
- Commit changes atomically per Rule 1.

---

## 4. Constraints, Risks & Assumptions
- **No Lost Funds:** Escrow vault balance (~4.66 SOL) remains untouched during rejected submissions. No SOL leaves the vault unless an approved payout or explicit poster refund occurs.
- **Race Conditions:** `active_claim_id` is set to `None` so that any other worker can immediately claim the reopened quest without conflict.
