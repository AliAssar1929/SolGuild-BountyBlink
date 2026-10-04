import { ref } from 'vue'
import { Keypair } from '@solana/web3.js'
import bs58 from 'bs58'

const STORAGE_KEY = 'bountyclink_devnet_wallet'

const publicKey = ref<string>('')
const secretKey = ref<string>('')
const balance = ref<number>(0.05)

export function useWallet() {
  const initWallet = () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        publicKey.value = parsed.publicKey
        secretKey.value = parsed.secretKey
      } catch (e) {
        generateNewKeypair()
      }
    } else {
      generateNewKeypair()
    }
    fetchFaucet()
  }

  const generateNewKeypair = () => {
    const kp = Keypair.generate()
    publicKey.value = kp.publicKey.toBase58()
    secretKey.value = bs58.encode(kp.secretKey)
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      publicKey: publicKey.value,
      secretKey: secretKey.value
    }))
  }

  const fetchFaucet = async () => {
    if (!publicKey.value) return
    try {
      const res = await fetch(`/api/wallet/faucet/${publicKey.value}`)
      const data = await res.json()
      if (data.status === 'ok') {
        balance.value = 0.05
      }
    } catch (e) {
      console.log('Faucet check:', e)
    }
  }

  return {
    publicKey,
    secretKey,
    balance,
    initWallet,
    fetchFaucet,
    generateNewKeypair
  }
}
