import { ref } from 'vue'

const WALLET_CONNECTED_KEY = 'bountyblink_phantom_connected'

const publicKey = ref<string>('')
const balance = ref<number>(0.0)
const isConnected = ref<boolean>(false)
const isConnecting = ref<boolean>(false)
const userProfile = ref<any>(null)
const isNewUser = ref<boolean>(false)
const networkNotice = ref<string>('')

export function useWallet() {
  const getProvider = () => {
    if (typeof window !== 'undefined' && 'solana' in window) {
      const provider = (window as any).solana
      if (provider?.isPhantom) {
        return provider
      }
    }
    return null
  }

  const initWallet = async () => {
    const wasConnected = localStorage.getItem(WALLET_CONNECTED_KEY)
    const provider = getProvider()
    
    if (provider && wasConnected === 'true') {
      try {
        // Eager connect if user already gave permission
        const resp = await provider.connect({ onlyIfTrusted: true })
        if (resp.publicKey) {
          handleConnected(resp.publicKey.toString())
        }
      } catch (err) {
        console.log('Phantom eager connection:', err)
      }
    }

    if (provider) {
      provider.on('accountChanged', (pk: any) => {
        if (pk) {
          handleConnected(pk.toString())
        } else {
          disconnect()
        }
      })
      provider.on('disconnect', () => {
        disconnect()
      })
    }
  }

  const connectPhantom = async () => {
    const provider = getProvider()
    if (!provider) {
      // Direct user to install Phantom
      window.open('https://phantom.app/', '_blank')
      return false
    }

    isConnecting.value = true
    try {
      const resp = await provider.connect()
      const address = resp.publicKey.toString()
      await handleConnected(address)
      return true
    } catch (err: any) {
      console.error('Phantom connect error:', err)
      return false
    } finally {
      isConnecting.value = false
    }
  }

  const handleConnected = async (address: string) => {
    publicKey.value = address
    isConnected.value = true
    localStorage.setItem(WALLET_CONNECTED_KEY, 'true')

    // 1. Authenticate / Join user account in database
    await authenticateUser(address)

    // 2. Fetch or trigger devnet gas airdrop
    await fetchFaucet()

    // 3. Sync user profile stats
    await refreshProfile()
  }

  const authenticateUser = async (address: string) => {
    try {
      // Get nonce
      const nonceRes = await fetch(`/api/auth/nonce/${address}`)
      const nonceData = await nonceRes.json()
      isNewUser.value = !!nonceData.is_new_user

      // Verify and register user session
      const verifyRes = await fetch('/api/auth/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          address: address,
          signature: 'phantom_devnet_verified'
        })
      })
      const verifyData = await verifyRes.json()
      if (verifyData.is_new_user) {
        isNewUser.value = true
      }
    } catch (e) {
      console.warn('Auth verify warning:', e)
    }
  }

  const refreshProfile = async () => {
    if (!publicKey.value) return
    try {
      const res = await fetch(`/api/user/${publicKey.value}`)
      const data = await res.json()
      userProfile.value = data
      balance.value = data.balance_sol || balance.value
    } catch (e) {
      console.warn('User profile refresh:', e)
    }
  }

  const fetchFaucet = async () => {
    if (!publicKey.value) return
    try {
      const res = await fetch(`/api/wallet/faucet/${publicKey.value}`)
      const data = await res.json()
      if (data.status === 'ok') {
        balance.value = Math.max(balance.value, 0.05)
      }
      await refreshProfile()
    } catch (e) {
      console.log('Faucet check:', e)
    }
  }

  const disconnect = () => {
    const provider = getProvider()
    if (provider) {
      provider.disconnect()
    }
    publicKey.value = ''
    balance.value = 0.0
    isConnected.value = false
    userProfile.value = null
    localStorage.removeItem(WALLET_CONNECTED_KEY)
  }

  return {
    publicKey,
    balance,
    isConnected,
    isConnecting,
    userProfile,
    isNewUser,
    networkNotice,
    initWallet,
    connectPhantom,
    fetchFaucet,
    refreshProfile,
    disconnect,
    getProvider
  }
}

