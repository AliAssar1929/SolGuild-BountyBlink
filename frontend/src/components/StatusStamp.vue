<script setup lang="ts">
import { CheckCircle2, AlertCircle, Clock, RotateCcw, Lock } from 'lucide-vue-next'

defineProps<{
  status: string
  failedAttempts?: number
}>()
</script>

<template>
  <span 
    v-if="status === 'OPEN' && failedAttempts && failedAttempts > 0"
    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-[4px] border border-[#FECDCA] text-[#B42318] bg-[#FEF3F2] font-mono text-[10px] font-bold uppercase tracking-wider"
  >
    <AlertCircle class="w-3 h-3 text-[#B42318]" />
    <span>Failed {{ failedAttempts }}x</span>
  </span>

  <span 
    v-else
    class="inline-flex items-center gap-1 px-2 py-0.5 rounded-[4px] border font-mono text-[10px] font-bold uppercase tracking-wider"
    :class="{
      'border-[#DDD8CC] dark:border-[#2E2D28] text-[#E8590C] bg-[#FDF8F5] dark:bg-[#201712]': status === 'OPEN',
      'border-[#DDD8CC] dark:border-[#2E2D28] text-[#6B675E] dark:text-[#9E9A90] bg-[#F6F3EC] dark:bg-[#121210]': status === 'CLAIMED',
      'border-[#1F7A4D] text-[#1F7A4D] dark:text-[#51CF66] bg-[#EBF5EF] dark:bg-[#132A1C]': status === 'PAID',
      'border-[#B3261E] text-[#B3261E] dark:text-[#FF8787] bg-[#FAECEB] dark:bg-[#2C1412]': status === 'REJECTED',
      'border-[#DDD8CC] dark:border-[#2E2D28] text-[#6B675E] dark:text-[#9E9A90] bg-[#EAE6DC] dark:bg-[#1B1B18]': status === 'REFUNDED'
    }"
  >
    <Lock v-if="status === 'OPEN'" class="w-3 h-3" />
    <Clock v-else-if="status === 'CLAIMED'" class="w-3 h-3" />
    <CheckCircle2 v-else-if="status === 'PAID'" class="w-3 h-3" />
    <AlertCircle v-else-if="status === 'REJECTED'" class="w-3 h-3" />
    <RotateCcw v-else-if="status === 'REFUNDED'" class="w-3 h-3" />
    <span>{{ status }}</span>
  </span>
</template>
