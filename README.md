# SolGuild: Solana Adventurer Guild Protocol (Devnet)

> *"Post a real-world adventurer quest, lock SOL in escrow, and release bounty upon verified proof."*

**SolGuild** is an anime adventurer guild-inspired protocol deployed on Solana Devnet. Guild Masters (issuers) post physical quests (lost pet rescues, item recovery, safe escorts, urgent errands) across Berlin, Paris, London, and Tokyo. Adventurers claim quests, submit photo proof within geofenced boundaries, undergo autonomous multi-tier verifier validation, and receive on-chain payouts directly released from escrow.

---

## ⚡ Key Features

1. **Adventurer Guild Boards**: Real-life adventurer quests categorized into *Pet Rescue*, *Lost Item*, *Safety Escort*, *Errand*, and *Community Help*.
2. **Balanced Split-Screen Quest Issuer**: Full-height edge-to-edge layout with a 3-stage wizard and live 12-item parchment specification card.
3. **Real-time Event Broadcasting**: Native WebSocket feed (`/ws/quests`) instantly syncing new quests, claims, proofs, and approvals across all adventurers.
4. **Guild License & Approvals Hub**: Dedicated `/profile` route for adventurers to manage verification, review reputation, and approve pending verified quest claims.
5. **Authentic Phantom Wallet Integration**: Devnet gas airdrops, mobile deep-linking (`phantom.app/ul/browse`), and on-chain escrow deposits.

---

## 📜 Smart Contract Architecture (Solana Escrow Program)

The on-chain escrow mechanism is built using the Solana Anchor framework:

```rust
// Program Accounts & State
#[account]
pub struct QuestEscrow {
    pub quest_id: [u8; 32],
    pub guild_master: Pubkey,   // Quest creator / poster
    pub adventurer: Pubkey,     // Claimer / worker
    pub bounty_lamports: u64,   // Locked reward in SOL
    pub state: QuestStatus,     // Open | Claimed | Verified | Released | Refunded
    pub deadline: i64,          // Expiration timestamp
    pub bump: u8,
}

// Program Instructions
1. initialize_quest(ctx, quest_id, bounty_lamports, deadline)
   - Transfers `bounty_lamports` from Guild Master to a Program Derived Address (PDA) vault.
2. claim_quest(ctx, quest_id)
   - Assigns adventurer pubkey and sets claim deadline.
3. submit_proof(ctx, quest_id, proof_hash)
   - Verifier oracle or guild master registers evidence verification.
4. release_escrow(ctx, quest_id)
   - Releases bounty lamports from PDA vault directly to adventurer wallet.
5. refund_escrow(ctx, quest_id)
   - If quest expires without verified completion, refunds bounty lamports back to Guild Master.
```

---

## 🔑 External API Keys & Services Required for Production

To take SolGuild from local Devnet into public staging or production:

1. **Google Gemini API Key (`GEMINI_API_KEY`)**:
   - For autonomous vision verification of submitted photos (evaluating scenery match, anti-screen moiré detection, and disqualifier checks).
2. **Dedicated Solana Devnet / Mainnet RPC URL (`SOLANA_RPC_URL`)**:
   - E.g., Helius, QuickNode, or Alchemy endpoint for high throughput transaction broadcast without rate limits.
3. **SMTP / Resend API Key (`RESEND_API_KEY` optional)**:
   - For delivery of 6-digit confirmation codes to adventurer email accounts (local console logging active by default in dev mode).

---

## 🚀 Running Locally

### Backend (FastAPI + Python 3.12)
```bash
cd backend
python -m venv venv
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

### Frontend (Vue 3 + Vite + Tailwind)
```bash
cd frontend
npm install
npm run dev -- --port 5173
```
