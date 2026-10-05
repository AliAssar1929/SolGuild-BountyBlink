<script setup lang="ts">
import { useSolPrice } from '../composables/useSolPrice'

const props = defineProps<{
  status: string
  amount: number
  failedAttempts?: number
}>()

const { getUsdValue } = useSolPrice()
</script>

<template>
  <div class="flex items-center gap-1.5 text-[15px] text-[#1A1A17] flex-wrap">
    <span class="text-[#5E5B53]">Reward:</span>
    <span class="font-semibold">{{ amount.toFixed(2) }} SOL</span>
    <span class="text-[#5E5B53] font-medium text-[13px]">({{ getUsdValue(amount) }})</span>
    <span class="text-[#5E5B53] text-[13px]">
      &middot; {{ 
        status === 'OPEN' ? (failedAttempts && failedAttempts > 0 ? `held in escrow (failed ${failedAttempts}x)` : 'held in escrow') : 
        status === 'CLAIMED' ? 'held in escrow (in progress)' : 
        status === 'PAID' ? 'released to worker' : 
        status === 'REFUNDED' ? 'returned to poster' : 'held in escrow' 
      }}
    </span>
  </div>
</template>
