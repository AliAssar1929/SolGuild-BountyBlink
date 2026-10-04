<script setup lang="ts">
import StatusWord from './StatusWord.vue'

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
    class="px-4 py-3.5 cursor-pointer transition-colors text-left flex items-start justify-between gap-3 border-b border-[#E3DFD6]"
    :class="isSelected ? 'bg-[#FFFBEA]' : 'hover:bg-[#FBF9F5] bg-white'"
  >
    <div class="space-y-1 min-w-0 flex-1">
      <div class="flex items-center gap-2">
        <h3 class="font-medium text-[15px] text-[#1A1A17] truncate leading-tight">
          {{ task.title }}
        </h3>
        <StatusWord v-if="task.status !== 'OPEN'" :status="task.status" />
      </div>
      
      <p class="text-[13px] text-[#5E5B53] line-clamp-1 leading-snug">
        {{ task.instruction }}
      </p>

      <div class="flex items-center gap-2 text-[13px] text-[#5E5B53] pt-0.5">
        <span>~35 m away</span>
        <span>&middot;</span>
        <span>10 min window</span>
      </div>
    </div>

    <div class="text-right shrink-0 pt-0.5">
      <span class="font-semibold text-[15px] text-[#1A1A17]">
        {{ task.reward_sol.toFixed(2) }} SOL
      </span>
    </div>
  </div>
</template>
