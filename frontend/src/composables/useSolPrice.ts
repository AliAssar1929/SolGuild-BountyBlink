import { ref, onMounted } from 'vue'

const solPriceUsd = ref<number>(155.0)
let intervalId: any = null

export function useSolPrice() {
  const fetchPrice = async () => {
    try {
      const res = await fetch('/api/price/sol')
      const data = await res.json()
      if (data && data.sol_usd) {
        solPriceUsd.value = data.sol_usd
      }
    } catch (e) {
      // Keep solid fallback price
    }
  }

  const formatSolWithUsd = (amountSol: number): string => {
    const usd = amountSol * solPriceUsd.value
    const usdFormatted = usd < 0.01 ? '<$0.01' : `$${usd.toFixed(2)}`
    return `${amountSol.toFixed(2)} SOL (${usdFormatted})`
  }

  const formatSolOnly = (amountSol: number): string => {
    return `${amountSol.toFixed(2)} SOL`
  }

  const getUsdValue = (amountSol: number): string => {
    const usd = amountSol * solPriceUsd.value
    return usd < 0.01 ? '<$0.01' : `$${usd.toFixed(2)}`
  }

  onMounted(() => {
    if (!intervalId) {
      fetchPrice()
      intervalId = setInterval(fetchPrice, 60000)
    }
  })

  return {
    solPriceUsd,
    fetchPrice,
    formatSolWithUsd,
    formatSolOnly,
    getUsdValue
  }
}
