<script setup lang="ts">
import { CheckCircle2, AlertCircle, RotateCcw, Clock } from 'lucide-vue-next'

defineProps<{
  status: string
  failedAttempts?: number
}>()
</script>

<template>
  <span 
    v-if="status === 'OPEN' && failedAttempts && failedAttempts > 0"
    class="inline-flex items-center gap-1 text-[11px] font-semibold text-[#B42318] bg-[#FEF3F2] border border-[#FECDCA] px-1.5 py-0.5 rounded-[4px]"
  >
    <AlertCircle class="w-3 h-3 text-[#B42318]" />
    <span>Failed {{ failedAttempts }}x</span>
  </span>

  <span 
    v-else
    class="inline-flex items-center gap-1 text-[12px] font-medium"
    :class="{
      'text-[#1E7B4F]': status === 'PAID',
      'text-[#B42318]': status === 'REJECTED',
      'text-[#5E5B53]': status === 'CLAIMED' || status === 'REFUNDED',
      'text-[#1A1A17]': status === 'OPEN'
    }"
  >
    <CheckCircle2 v-if="status === 'PAID'" class="w-3.5 h-3.5" />
    <AlertCircle v-else-if="status === 'REJECTED'" class="w-3.5 h-3.5" />
    <RotateCcw v-else-if="status === 'REFUNDED'" class="w-3.5 h-3.5" />
    <Clock v-else-if="status === 'CLAIMED'" class="w-3.5 h-3.5" />
    
    <span>
      {{ 
        status === 'PAID' ? 'Paid' : 
        status === 'REJECTED' ? 'Not approved' : 
        status === 'REFUNDED' ? 'Returned' : 
        status === 'CLAIMED' ? 'In progress' : 'Open' 
      }}
    </span>
  </span>
</template>
