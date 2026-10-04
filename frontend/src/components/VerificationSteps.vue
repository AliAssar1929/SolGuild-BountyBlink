<script setup lang="ts">
import { ref } from 'vue'
import { Check, Loader2, ChevronDown, ChevronUp } from 'lucide-vue-next'

const props = defineProps<{
  currentStep: number // 1: Intake, 2: Location, 3: Vision, 4: Settlement
  status?: string
  txSig?: string
  reason?: string
}>()

const showTechnical = ref(false)

const steps = [
  { id: 1, name: 'Photo received' },
  { id: 2, name: 'Location checked' },
  { id: 3, name: 'Photo checked' },
  { id: 4, name: 'Reward released' }
]
</script>

<template>
  <div class="space-y-3 text-left">
    
    <!-- Step list -->
    <div class="space-y-2">
      <div 
        v-for="step in steps" 
        :key="step.id"
        class="flex items-center justify-between p-3 rounded-[12px] border border-[#E3DFD6] transition-all"
        :class="{
          'bg-[#FFFFFF]': currentStep !== step.id,
          'bg-[#FFFDF5] border-[#FFD60A] shadow-xs': currentStep === step.id
        }"
      >
        <div class="flex items-center gap-3">
          <div 
            class="w-5 h-5 rounded-full flex items-center justify-center text-xs"
            :class="{
              'bg-[#1E7B4F] text-white': currentStep > step.id || (step.id === 4 && status === 'PAID'),
              'bg-[#FFD60A] text-[#1A1A17]': currentStep === step.id,
              'bg-[#E3DFD6] text-[#5E5B53]': currentStep < step.id
            }"
          >
            <Check v-if="currentStep > step.id || (step.id === 4 && status === 'PAID')" class="w-3.5 h-3.5" />
            <Loader2 v-else-if="currentStep === step.id" class="w-3.5 h-3.5 animate-spin" />
            <span v-else class="text-[11px] font-medium">{{ step.id }}</span>
          </div>
          
          <span class="text-[15px] font-medium text-[#1A1A17]">
            {{ step.name }}
          </span>
        </div>

        <span class="text-[13px] text-[#5E5B53]">
          {{ 
            currentStep > step.id ? 'Passed' : 
            currentStep === step.id ? 'Checking...' : 'Pending' 
          }}
        </span>
      </div>
    </div>

    <!-- Technical details disclosure -->
    <div class="pt-2 border-t border-[#E3DFD6]">
      <button 
        @click="showTechnical = !showTechnical"
        class="flex items-center justify-between w-full text-[13px] text-[#5E5B53] hover:text-[#1A1A17] font-medium py-1"
      >
        <span>Technical details</span>
        <ChevronUp v-if="showTechnical" class="w-4 h-4" />
        <ChevronDown v-else class="w-4 h-4" />
      </button>

      <div v-if="showTechnical" class="mt-2 p-3 bg-[#F7F5F0] rounded-[8px] text-[12px] font-mono text-[#5E5B53] space-y-1.5 leading-relaxed break-all">
        <div>Network: Solana Devnet (cluster=devnet)</div>
        <div v-if="txSig">Transaction: {{ txSig }}</div>
        <div v-if="reason">Verification verdict: {{ reason }}</div>
        <div>Geofence: Haversine &le; 150 m tolerance</div>
      </div>
    </div>

  </div>
</template>
