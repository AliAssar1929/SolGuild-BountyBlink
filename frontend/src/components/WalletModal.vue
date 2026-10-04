<script setup lang="ts">
import { Wallet, X, Check, ShieldAlert } from 'lucide-vue-next'

const props = defineProps<{
  isOpen: boolean
  currentAddress: string
  balance: number
  connectedProvider: string // 'demo' | 'phantom' | 'solflare' | 'backpack'
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'selectWallet', provider: string): void
  (e: 'disconnect'): void
}>()

const providers = [
  { id: 'demo', name: 'Demo wallet (Instant Devnet)', desc: 'Built-in temporary keypair pre-funded for evaluation' },
  { id: 'phantom', name: 'Phantom', desc: 'Solana Wallet Standard extension or mobile app' },
  { id: 'solflare', name: 'Solflare', desc: 'Non-custodial Solana web3 wallet' },
  { id: 'backpack', name: 'Backpack', desc: 'xNFT and Solana crypto wallet' }
]
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4 bg-black/30 backdrop-blur-xs">
    <div class="w-full max-w-sm bg-white border border-[#E3DFD6] rounded-[16px] shadow-xl p-6 text-left space-y-5">
      
      <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
        <div class="flex items-center gap-2">
          <Wallet class="w-5 h-5 text-[#1A1A17]" />
          <h3 class="font-semibold text-[17px] text-[#1A1A17]">Solana wallet</h3>
        </div>
        <button @click="$emit('close')" class="p-1 hover:bg-[#F7F5F0] rounded-[6px] text-[#5E5B53]">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Devnet notice -->
      <div class="p-3 bg-[#FFFBEA] border border-[#FFD60A] rounded-[8px] flex items-start gap-2.5 text-[13px] text-[#1A1A17]">
        <ShieldAlert class="w-4 h-4 text-[#1A1A17] shrink-0 mt-0.5" />
        <p class="leading-snug">
          BountyBlink is strictly on <strong>Solana Devnet</strong>. Do not use real mainnet funds.
        </p>
      </div>

      <!-- Wallet List -->
      <div class="space-y-2">
        <button 
          v-for="p in providers"
          :key="p.id"
          @click="$emit('selectWallet', p.id)"
          class="w-full p-3.5 rounded-[10px] border border-[#E3DFD6] hover:border-[#1A1A17] bg-[#F7F5F0] hover:bg-[#FFFDF5] transition-all text-left flex items-start justify-between"
          :class="connectedProvider === p.id ? 'border-[#1A1A17] bg-[#FFFBEA]' : ''"
        >
          <div>
            <div class="font-semibold text-[14px] text-[#1A1A17] flex items-center gap-1.5">
              <span>{{ p.name }}</span>
              <Check v-if="connectedProvider === p.id" class="w-4 h-4 text-[#1E7B4F]" />
            </div>
            <div class="text-[12px] text-[#5E5B53] mt-0.5 leading-snug">{{ p.desc }}</div>
          </div>
        </button>
      </div>

      <!-- Disconnect if connected -->
      <div v-if="currentAddress" class="pt-2 border-t border-[#E3DFD6] flex justify-between items-center text-[13px]">
        <span class="font-mono text-[#5E5B53]">{{ currentAddress.slice(0, 4) }}...{{ currentAddress.slice(-4) }}</span>
        <button 
          @click="$emit('disconnect')" 
          class="text-[#B42318] font-medium hover:underline"
        >
          Disconnect
        </button>
      </div>

    </div>
  </div>
</template>
