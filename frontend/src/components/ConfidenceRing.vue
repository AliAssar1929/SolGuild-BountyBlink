<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  score: number // 0 to 100
}>()

const strokeDashoffset = computed(() => {
  const circumference = 2 * Math.PI * 28
  return circumference - (props.score / 100) * circumference
})
</script>

<template>
  <div class="inline-flex items-center gap-2">
    <div class="relative w-16 h-16 flex items-center justify-center">
      <svg class="w-full h-full transform -rotate-90" viewBox="0 0 64 64">
        <circle
          cx="32"
          cy="32"
          r="28"
          stroke="currentColor"
          stroke-width="4"
          class="text-[#DDD8CC] dark:text-[#2E2D28]"
          fill="none"
        />
        <circle
          cx="32"
          cy="32"
          r="28"
          stroke="currentColor"
          stroke-width="4"
          :class="score >= 80 ? 'text-[#1F7A4D]' : 'text-[#B3261E]'"
          fill="none"
          stroke-dasharray="175.92"
          :stroke-dashoffset="strokeDashoffset"
          stroke-linecap="round"
          class="transition-all duration-700 ease-out"
        />
      </svg>
      <span class="absolute font-mono text-xs font-bold text-[#14130F] dark:text-[#F5F2EB]">
        {{ Math.round(score) }}%
      </span>
    </div>
    <div class="text-left font-mono">
      <span class="text-[10px] text-[#6B675E] dark:text-[#9E9A90] uppercase block">Vision Confidence</span>
      <span class="text-xs font-bold" :class="score >= 80 ? 'text-[#1F7A4D]' : 'text-[#B3261E]'">
        {{ score >= 80 ? 'Threshold Passed (>=80%)' : 'Below Threshold' }}
      </span>
    </div>
  </div>
</template>
