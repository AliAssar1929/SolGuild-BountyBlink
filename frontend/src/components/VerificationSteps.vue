<script setup lang="ts">
import { ref } from 'vue'
import { Check, X, Loader2, Lock, ChevronDown, ChevronUp } from 'lucide-vue-next'

const props = defineProps<{
  currentStep: number // 1: Intake, 2: Location, 3: Vision, 4: Settlement
  status?: string // 'PAID' | 'REJECTED' | string
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
        class="flex items-center justify-between p-3 rounded-[12px] border transition-all"
        :class="{
          'border-[#FECDCA] bg-[#FFF5F5]': status === 'REJECTED' && step.id === 3,
          'border-[#E3DFD6] bg-[#FFFFFF]': !(status === 'REJECTED' && step.id === 3) && currentStep !== step.id,
          'bg-[#FFFDF5] border-[#FFD60A] shadow-xs': !status && currentStep === step.id
        }"
      >
        <div class="flex items-center gap-3">
          <!-- Step icon circle -->
          <div 
            class="w-5 h-5 rounded-full flex items-center justify-center text-xs transition-colors"
            :class="{
              'bg-[#1E7B4F] text-white': (step.id === 1 && currentStep >= 1) || (step.id === 2 && currentStep >= 2) || (step.id === 3 && status === 'PAID') || (step.id === 4 && status === 'PAID'),
              'bg-[#D92D20] text-white': status === 'REJECTED' && step.id === 3,
              'bg-[#EAE6DC] text-[#78716C]': status === 'REJECTED' && step.id === 4,
              'bg-[#FFD60A] text-[#1A1A17]': !status && currentStep === step.id,
              'bg-[#E3DFD6] text-[#5E5B53]': !status && currentStep < step.id
            }"
          >
            <!-- Checkmark for completed steps -->
            <Check 
              v-if="
                (step.id === 1 && currentStep >= 1) ||
                (step.id === 2 && currentStep >= 2) ||
                (step.id === 3 && status === 'PAID') ||
                (step.id === 4 && status === 'PAID')
              " 
              class="w-3.5 h-3.5 stroke-[2.5]" 
            />
            
            <!-- Red X for rejected photo -->
            <X 
              v-else-if="status === 'REJECTED' && step.id === 3" 
              class="w-3.5 h-3.5 stroke-[2.5]" 
            />

            <!-- Lock for withheld reward on rejection -->
            <Lock 
              v-else-if="status === 'REJECTED' && step.id === 4" 
              class="w-3 h-3 text-[#78716C]" 
            />

            <!-- Spinner during active check -->
            <Loader2 
              v-else-if="!status && currentStep === step.id" 
              class="w-3.5 h-3.5 animate-spin" 
            />

            <!-- Step number for pending -->
            <span v-else class="text-[11px] font-medium">{{ step.id }}</span>
          </div>
          
          <span 
            class="text-[14px] font-medium"
            :class="status === 'REJECTED' && step.id === 3 ? 'text-[#D92D20]' : 'text-[#1A1A17]'"
          >
            {{ step.name }}
          </span>
        </div>

        <!-- Step state label -->
        <span 
          class="text-[13px] font-medium"
          :class="{
            'text-[#D92D20] font-semibold': status === 'REJECTED' && step.id === 3,
            'text-[#78716C]': status === 'REJECTED' && step.id === 4,
            'text-[#1E7B4F]': (step.id < 3 && currentStep > step.id) || (step.id === 3 && status === 'PAID') || (step.id === 4 && status === 'PAID'),
            'text-[#92400E]': !status && currentStep === step.id,
            'text-[#5E5B53]': !status && currentStep < step.id
          }"
        >
          <template v-if="status === 'REJECTED'">
            <span v-if="step.id < 3">Passed</span>
            <span v-else-if="step.id === 3">Rejected</span>
            <span v-else>Withheld in escrow</span>
          </template>
          <template v-else-if="status === 'PAID'">
            <span>Passed</span>
          </template>
          <template v-else>
            {{ currentStep > step.id ? 'Passed' : currentStep === step.id ? 'Checking...' : 'Pending' }}
          </template>
        </span>
      </div>
    </div>

    <!-- Technical details disclosure -->
    <div class="pt-2 border-t border-[#E3DFD6]">
      <button 
        @click="showTechnical = !showTechnical"
        class="flex items-center justify-between w-full text-[13px] text-[#5E5B53] hover:text-[#1A1A17] font-medium py-1 cursor-pointer"
      >
        <span>Technical verification audit</span>
        <ChevronUp v-if="showTechnical" class="w-4 h-4" />
        <ChevronDown v-else class="w-4 h-4" />
      </button>

      <div v-if="showTechnical" class="mt-2 p-3 bg-[#F7F5F0] rounded-[8px] text-[12px] font-mono text-[#5E5B53] space-y-1.5 leading-relaxed break-all">
        <div>Network: Solana Devnet (cluster=devnet)</div>
        <div v-if="txSig">Settlement Tx: {{ txSig }}</div>
        <div v-if="reason" class="text-[#1A1A17]"><strong>Verification Reason:</strong> {{ reason }}</div>
        <div>Escrow Lock: 100% on-chain native SOL vault</div>
        <div>Geofence: Haversine &le; 150 m tolerance</div>
      </div>
    </div>

  </div>
</template>
