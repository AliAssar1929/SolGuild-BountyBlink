<script setup lang="ts">
defineProps<{
  status: string
  amount: number
}>()
</script>

<template>
  <div class="flex items-center gap-1.5 text-[15px] text-[#1A1A17]">
    <span class="text-[#5E5B53]">Reward:</span>
    <span class="font-semibold">{{ amount.toFixed(2) }} SOL</span>
    <span class="text-[#5E5B53] text-[13px]">
      ({{ status === 'OPEN' ? 'held in escrow' : status === 'PAID' ? 'released' : 'returned to poster' }})
    </span>
  </div>
</template>
