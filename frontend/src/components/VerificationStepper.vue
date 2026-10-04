<script setup lang="ts">
import { Check, Loader2 } from 'lucide-vue-next'

defineProps<{
  currentStep: number // 1: Intake, 2: Location, 3: Vision, 4: Settlement
}>()

const steps = [
  { id: 1, name: 'Tier 0: Intake & Duplicate Check' },
  { id: 2, name: 'Tier 1: Geofence Validation (<= 150m)' },
  { id: 3, name: 'Tier 2: Gemini 2.5 Flash Vision Scene Verification' },
  { id: 4, name: 'Tier 3: Solana Devnet On-Chain Settlement' }
]
</script>

<template>
  <div class="space-y-2.5 font-mono text-xs">
    <div 
      v-for="step in steps" 
      :key="step.id"
      class="flex items-center gap-2.5 p-2 rounded-[4px] border transition-colors"
      :class="{
        'border-[#1F7A4D] bg-[#EBF5EF] dark:bg-[#132A1C] text-[#1F7A4D] dark:text-[#51CF66]': currentStep > step.id,
        'border-[#E8590C] bg-[#FDF8F5] dark:bg-[#201712] text-[#E8590C]': currentStep === step.id,
        'border-transparent text-[#6B675E] dark:text-[#9E9A90]': currentStep < step.id
      }"
    >
      <div class="w-4 h-4 rounded-full flex items-center justify-center shrink-0 text-[10px]">
        <Check v-if="currentStep > step.id" class="w-3.5 h-3.5" />
        <Loader2 v-else-if="currentStep === step.id" class="w-3.5 h-3.5 animate-spin" />
        <span v-else class="text-[#6B675E] dark:text-[#9E9A90]">{{ step.id }}</span>
      </div>
      <span class="leading-none">{{ step.name }}</span>
    </div>
  </div>
</template>
