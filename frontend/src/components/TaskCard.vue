<script setup lang="ts">
import StatusStamp from './StatusStamp.vue'
import { MapPin } from 'lucide-vue-next'

defineProps<{
  task: {
    id: string
    title: string
    instruction: string
    reward_sol: number
    status: string
    latitude: number
    longitude: number
  }
  isSelected?: boolean
}>()

defineEmits<{
  (e: 'select'): void
}>()
</script>

<template>
  <div 
    @click="$emit('select')"
    class="p-4 rounded-[6px] border transition-all cursor-pointer text-left relative"
    :class="isSelected 
      ? 'border-[#14130F] dark:border-[#F5F2EB] bg-[#FFFFFF] dark:bg-[#1B1B18] shadow-xs' 
      : 'border-[#DDD8CC] dark:border-[#2E2D28] bg-[#FFFFFF] dark:bg-[#181815] hover:border-[#14130F] dark:hover:border-[#DDD8CC]'"
  >
    <!-- Ticket Header -->
    <div class="flex items-start justify-between gap-2 mb-1.5">
      <div class="flex items-center gap-2">
        <span class="font-mono text-[10px] uppercase text-[#6B675E] dark:text-[#9E9A90]">#{{ task.id.slice(0, 8) }}</span>
        <StatusStamp :status="task.status" />
      </div>
      <span class="font-mono font-bold text-xs text-[#E8590C]">
        {{ task.reward_sol.toFixed(2) }} SOL
      </span>
    </div>

    <!-- Title & Instruction -->
    <h3 class="font-semibold text-xs text-[#14130F] dark:text-[#F5F2EB] leading-snug line-clamp-1 mb-1">
      {{ task.title }}
    </h3>
    <p class="text-[11px] text-[#6B675E] dark:text-[#9E9A90] line-clamp-2 leading-relaxed mb-3">
      {{ task.instruction }}
    </p>

    <!-- Footer meta -->
    <div class="flex items-center justify-between pt-2 border-t border-[#DDD8CC] dark:border-[#2E2D28] text-[10px] font-mono text-[#6B675E] dark:text-[#9E9A90]">
      <span class="flex items-center gap-1">
        <MapPin class="w-3 h-3 text-[#E8590C]" />
        {{ task.latitude.toFixed(2) }}, {{ task.longitude.toFixed(2) }}
      </span>
      <span>~35m away</span>
    </div>
  </div>
</template>
