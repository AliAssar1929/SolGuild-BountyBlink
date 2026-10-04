<script setup lang="ts">
defineProps<{
  status: string
  amount: number
}>()
</script>

<template>
  <div 
    class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-[4px] border text-[11px] font-mono font-medium tracking-tight"
    :class="{
      'border-[#DDD8CC] dark:border-[#2E2D28] bg-[#F6F3EC] dark:bg-[#121210] text-[#14130F] dark:text-[#F5F2EB]': status === 'OPEN',
      'border-[#DDD8CC] dark:border-[#2E2D28] bg-[#EAE6DC] dark:bg-[#252520] text-[#14130F] dark:text-[#F5F2EB]': status === 'CLAIMED',
      'border-[#1F7A4D] bg-[#EBF5EF] dark:bg-[#132A1C] text-[#1F7A4D] dark:text-[#51CF66]': status === 'PAID',
      'border-[#B3261E] bg-[#FAECEB] dark:bg-[#2C1412] text-[#B3261E] dark:text-[#FF8787]': status === 'REJECTED',
      'border-[#DDD8CC] dark:border-[#2E2D28] bg-[#EAE6DC] dark:bg-[#1B1B18] text-[#6B675E] dark:text-[#9E9A90]': status === 'REFUNDED'
    }"
  >
    <span class="w-1.5 h-1.5 rounded-full" :class="{
      'bg-[#E8590C]': status === 'OPEN',
      'bg-[#6B675E]': status === 'CLAIMED' || status === 'REFUNDED',
      'bg-[#1F7A4D]': status === 'PAID',
      'bg-[#B3261E]': status === 'REJECTED'
    }"></span>
    <span class="uppercase tracking-wider text-[10px]">
      {{ status === 'OPEN' ? 'Escrow Locked' : status }}
    </span>
    <span class="font-bold border-l border-current pl-1.5 ml-0.5">
      {{ amount.toFixed(2) }} SOL
    </span>
  </div>
</template>
