import base64
import json
import os
import time
from typing import Optional, Tuple, Dict, Any
import httpx
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message
from solders.hash import Hash
from config import settings

class SolanaService:
    def __init__(self):
        self.keypair = self._load_or_generate_escrow_keypair()
        self.pubkey_str = str(self.keypair.pubkey())
        print(f"[SolanaService] Escrow Public Key: {self.pubkey_str}")

    def _load_or_generate_escrow_keypair(self) -> Keypair:
        path = settings.ESCROW_KEYPAIR_PATH
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    return Keypair.from_bytes(bytes(data))
            except Exception as e:
                print(f"[SolanaService] Error loading keypair: {e}. Generating new...")
        
        kp = Keypair()
        with open(path, "w") as f:
            json.dump(list(bytes(kp)), f)
        return kp

    def _rpc_call(self, method: str, params: list) -> Optional[dict]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        for url in settings.DEVNET_RPC_URLS:
            try:
                with httpx.Client(timeout=8.0) as client:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        if "result" in data:
                            return data["result"]
            except Exception as e:
                continue
        return None

    def get_latest_blockhash(self) -> Optional[Dict[str, Any]]:
        """Fetches fresh confirmed blockhash from Devnet."""
        result = self._rpc_call("getLatestBlockhash", [{"commitment": "confirmed"}])
        if result and "value" in result:
            return {
                "blockhash": result["value"]["blockhash"],
                "last_valid_block_height": result["value"].get("lastValidBlockHeight")
            }
        return None

    def get_balance(self, pubkey_str: Optional[str] = None) -> float:
        target = pubkey_str or self.pubkey_str
        result = self._rpc_call("getBalance", [target, {"commitment": "confirmed"}])
        if result and "value" in result:
            return result["value"] / 1_000_000_000.0
        return 0.0

    def broadcast_raw_transaction(self, raw_tx_base64: str) -> Tuple[bool, str, str]:
        """Broadcasts a client-signed raw transaction directly to Solana Devnet."""
        send_result = self._rpc_call("sendTransaction", [
            raw_tx_base64,
            {"encoding": "base64", "preflightCommitment": "confirmed"}
        ])
        if send_result and isinstance(send_result, str):
            sig = send_result
            explorer_url = f"https://explorer.solana.com/tx/{sig}{settings.DEVNET_CLUSTER_PARAM}"
            return True, sig, explorer_url
        
        # If preflight error returned
        raise ValueError(f"Solana Devnet rejected transaction: {send_result}")

    def request_airdrop(self, target_pubkey_str: str, amount_sol: float = 0.05) -> Tuple[bool, str, str]:
        """Funds target wallet with real Devnet SOL directly from the funded Escrow Vault."""
        ok, sig, explorer_url = self.transfer_sol(target_pubkey_str, amount_sol)
        if ok:
            return True, sig, explorer_url
        raise RuntimeError("Failed to transfer Devnet SOL from escrow vault")

    def transfer_sol(self, to_pubkey_str: str, amount_sol: float) -> Tuple[bool, str, str]:
        """Transfers SOL on-chain from backend escrow to worker or poster."""
        lamports = int(amount_sol * 1_000_000_000)
        to_pk = Pubkey.from_string(to_pubkey_str)
        
        # Try up to 3 times to get fresh blockhash and broadcast
        last_err = None
        for attempt in range(3):
            try:
                blockhash_info = self._rpc_call("getLatestBlockhash", [{"commitment": "confirmed"}])
                if not blockhash_info or "value" not in blockhash_info:
                    time.sleep(0.5)
                    continue

                recent_blockhash_str = blockhash_info["value"]["blockhash"]
                recent_blockhash = Hash.from_string(recent_blockhash_str)
                
                ix = transfer(TransferParams(
                    from_pubkey=self.keypair.pubkey(),
                    to_pubkey=to_pk,
                    lamports=lamports
                ))
                msg = Message([ix], self.keypair.pubkey())
                tx = Transaction([self.keypair], msg, recent_blockhash)
                tx_bytes = bytes(tx)
                tx_base64 = base64.b64encode(tx_bytes).decode("utf-8")
                
                send_result = self._rpc_call("sendTransaction", [
                    tx_base64,
                    {"encoding": "base64", "preflightCommitment": "confirmed"}
                ])
                if send_result and isinstance(send_result, str):
                    sig = send_result
                    explorer_url = f"https://explorer.solana.com/tx/{sig}{settings.DEVNET_CLUSTER_PARAM}"
                    return True, sig, explorer_url
            except Exception as e:
                last_err = e
                time.sleep(1.0)

        raise RuntimeError(f"On-chain transfer failed after 3 attempts: {last_err}")

solana_service = SolanaService()
