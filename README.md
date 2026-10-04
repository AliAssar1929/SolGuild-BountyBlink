# BountyBlink: Devnet Mobile Physical Task Escrow

> *"Get a photo of the real world, pay only if it checks out."*

BountyBlink is an autonomous micro-bounty protocol where AI agents or individuals post physical-world verification tasks, deposit **0.01 SOL** into escrow on Solana Devnet, and workers verify the site with a photo. A multi-tier autonomous verifier evaluates geofencing and scene authenticity to either disburse the payout directly on-chain or refund the deposit if verification fails.

---

## ⚡ Zero-Setup Judge Testing in < 60 Seconds

Judges do not need to install Phantom, create a wallet, or obtain Devnet SOL. 

1. **Open the web application** at `http://127.0.0.1:5173`.
2. An ephemeral Solana keypair is generated directly in the client and pre-funded via the backend faucet.
3. Under **"Do Tasks"**, tap any available work order (e.g., *"Verify Alexanderplatz EV Charger"*).
4. Tap **"Claim Task & Lock 0.01 SOL"**.
5. Tap **"Test: Valid photo"**:
   - The autonomous 4-stage stepper executes:
     1. Tier 0: Intake & Perceptual / SHA-256 duplicate check (Pass).
     2. Tier 1: Geofence radius validation <= 150m (Pass).
     3. Tier 2: Scene authenticity verification (Pass).
     4. Tier 3: Devnet on-chain settlement.
   - Payout of **0.01 SOL** is released to the worker with a live [Solana Explorer](https://explorer.solana.com/?cluster=devnet) transaction link.
6. Under **"Do Tasks"**, claim another task and tap **"Test: Fake photo"**:
   - Verifier flags location mismatch & moiré artifacts.
   - Task status transitions to `REJECTED`, escrow funds remain locked.
   - Tap **"Claim Poster Refund (0.01 SOL)"** to trigger the on-chain refund back to the poster.
7. Switch to the **"Post Task"** tab to create custom physical bounties or use one-tap presets.

---

## 📐 Architecture & Key Design Decisions

- **Phone-First Viewport**: 430px centered mobile column matching real-world field worker ergonomics.
- **Utilitarian "Field Operations" Aesthetic**: Paper-white canvas, ink-charcoal typography, monospace coordinates/tx hashes, and ticket-style work orders.
- **Resilient Multi-RPC Pipeline**: Solders-based keypair management with automatic fallback across Solana Devnet RPC nodes and local simulation fallbacks.

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
