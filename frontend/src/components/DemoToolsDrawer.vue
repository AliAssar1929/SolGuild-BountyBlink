<script setup lang="ts">
import { FlaskConical, X, RotateCcw, Coins } from 'lucide-vue-next'

defineProps<{
  isOpen: boolean
}>()

defineEmits<{
  (e: 'close'): void
  (e: 'submitFixture', type: 'VALID' | 'FAKE'): void
  (e: 'reset'): void
  (e: 'faucet'): void
}>()
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4 bg-black/30 backdrop-blur-xs">
    <div class="w-full max-w-md bg-white border border-[#E3DFD6] rounded-[16px] shadow-lg p-6 text-left space-y-5">
      
      <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
        <div class="flex items-center gap-2">
          <FlaskConical class="w-5 h-5 text-[#1A1A17]" />
          <h3 class="font-semibold text-[17px] text-[#1A1A17]">Demo tools</h3>
        </div>
        <button @click="$emit('close')" class="p-1 hover:bg-[#F7F5F0] rounded-[6px] text-[#5E5B53]">
          <X class="w-5 h-5" />
        </button>
      </div>

      <p class="text-[15px] text-[#5E5B53] leading-relaxed">
        Test fixtures for reviewers to evaluate the full escrow and verification loop in under two minutes without moving location.
      </p>

      <div class="space-y-2.5">
        <button 
          @click="$emit('submitFixture', 'VALID')"
          class="w-full p-4 rounded-[12px] bg-[#F7F5F0] hover:bg-[#FFFDF5] hover:border-[#FFD60A] border border-[#E3DFD6] transition-all text-left space-y-1"
        >
          <div class="font-medium text-[15px] text-[#1A1A17]">Submit valid test photo</div>
          <div class="text-[13px] text-[#5E5B53]">Matches location and scene. Escrow pays out 0.01 SOL immediately.</div>
        </button>

        <button 
          @click="$emit('submitFixture', 'FAKE')"
          class="w-full p-4 rounded-[12px] bg-[#F7F5F0] hover:bg-[#FFFDF5] hover:border-[#FFD60A] border border-[#E3DFD6] transition-all text-left space-y-1"
        >
          <div class="font-medium text-[15px] text-[#1A1A17]">Submit fake test photo</div>
          <div class="text-[13px] text-[#5E5B53]">Wrong location or screen capture. Fails check; reward remains refundable to poster.</div>
        </button>
      </div>

      <div class="pt-3 border-t border-[#E3DFD6] flex items-center justify-between">
        <button 
          @click="$emit('reset')"
          class="flex items-center gap-1.5 text-[13px] text-[#5E5B53] hover:text-[#1A1A17] font-medium"
        >
          <RotateCcw class="w-3.5 h-3.5" />
          <span>Reset demo tasks</span>
        </button>

        <button 
          @click="$emit('faucet')"
          class="flex items-center gap-1.5 text-[13px] text-[#5E5B53] hover:text-[#1A1A17] font-medium"
        >
          <Coins class="w-3.5 h-3.5" />
          <span>Get test SOL</span>
        </button>
      </div>

    </div>
  </div>
</template>
