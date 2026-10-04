<script setup lang="ts">
import { FlaskConical, X } from 'lucide-vue-next'

defineProps<{
  isOpen: boolean
}>()

defineEmits<{
  (e: 'close'): void
  (e: 'submitFixture', type: 'VALID' | 'FAKE'): void
}>()
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
    <div class="w-full max-w-md bg-[#FFFFFF] dark:bg-[#1B1B18] border border-[#DDD8CC] dark:border-[#2E2D28] rounded-[6px] shadow-lg p-5 text-left space-y-4">
      
      <div class="flex items-center justify-between border-b border-[#DDD8CC] dark:border-[#2E2D28] pb-3">
        <div class="flex items-center gap-2">
          <FlaskConical class="w-4 h-4 text-[#E8590C]" />
          <h3 class="font-bold text-sm text-[#14130F] dark:text-[#F5F2EB]">Judge Testing Presets (Demo Drawer)</h3>
        </div>
        <button @click="$emit('close')" class="p-1 hover:bg-[#F6F3EC] dark:hover:bg-[#252520] rounded-[4px] text-[#6B675E]">
          <X class="w-4 h-4" />
        </button>
      </div>

      <p class="text-xs text-[#6B675E] dark:text-[#9E9A90] leading-relaxed">
        Test fixtures designed for hackathon judges to verify the end-to-end loop in &lt;60s without needing field movement:
      </p>

      <div class="space-y-2.5">
        <button 
          @click="$emit('submitFixture', 'VALID')"
          class="w-full p-3 rounded-[4px] border border-[#1F7A4D] bg-[#EBF5EF] dark:bg-[#132A1C] hover:opacity-90 transition-opacity text-left font-mono text-xs flex flex-col gap-0.5"
        >
          <span class="font-bold text-[#1F7A4D] dark:text-[#51CF66] uppercase text-[10px]">Preset Fixture 1</span>
          <span class="font-bold text-[#14130F] dark:text-[#F5F2EB]">Test: Valid Photo</span>
          <span class="text-[11px] text-[#6B675E] dark:text-[#9E9A90]">Passes GPS (&lt;150m) & Gemini Vision ➔ Instant 0.01 SOL Payout</span>
        </button>

        <button 
          @click="$emit('submitFixture', 'FAKE')"
          class="w-full p-3 rounded-[4px] border border-[#B3261E] bg-[#FAECEB] dark:bg-[#2C1412] hover:opacity-90 transition-opacity text-left font-mono text-xs flex flex-col gap-0.5"
        >
          <span class="font-bold text-[#B3261E] dark:text-[#FF8787] uppercase text-[10px]">Preset Fixture 2</span>
          <span class="font-bold text-[#14130F] dark:text-[#F5F2EB]">Test: Fake Photo</span>
          <span class="text-[11px] text-[#6B675E] dark:text-[#9E9A90]">Fails Tier 1 & Moiré check ➔ Escrow stays locked, refund enabled</span>
        </button>
      </div>

      <div class="text-[10px] font-mono text-[#6B675E] dark:text-[#9E9A90] pt-1 border-t border-[#DDD8CC] dark:border-[#2E2D28]">
        Note: Escrow runs on Solana Devnet. Location checks are best-effort.
      </div>

    </div>
  </div>
</template>
