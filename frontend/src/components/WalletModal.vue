<script setup lang="ts">
import { Wallet, X, ShieldAlert, Sparkles, ExternalLink, ArrowRight } from 'lucide-vue-next'

const props = defineProps<{
  isOpen: boolean
  currentAddress: string
  balance: number
  isConnecting?: boolean
  isNewUser?: boolean
  userProfile?: any
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'connectPhantom'): void
  (e: 'faucet'): void
  (e: 'disconnect'): void
}>()
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-4 bg-black/35 backdrop-blur-xs">
    <div class="w-full max-w-md bg-white border border-[#E3DFD6] rounded-[16px] shadow-xl p-6 text-left space-y-5">
      
      <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
        <div class="flex items-center gap-2">
          <Wallet class="w-5 h-5 text-[#1A1A17]" />
          <h3 class="font-semibold text-[17px] text-[#1A1A17]">
            {{ currentAddress ? 'Your Phantom Account' : 'Connect Phantom Wallet' }}
          </h3>
        </div>
        <button @click="$emit('close')" class="p-1 hover:bg-[#F7F5F0] rounded-[6px] text-[#5E5B53]">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Devnet Auto-Switch Instructions -->
      <div class="p-3.5 bg-[#FFFBEA] border border-[#FFD60A] rounded-[10px] space-y-2 text-[13px] text-[#1A1A17]">
        <div class="flex items-start gap-2">
          <ShieldAlert class="w-4 h-4 text-[#1A1A17] shrink-0 mt-0.5" />
          <div class="space-y-1">
            <span class="font-semibold block">Devnet Testing Environment</span>
            <p class="text-[#5E5B53] text-[12px] leading-relaxed">
              BountyBlink executes on <strong>Solana Devnet</strong>. In your Phantom wallet:
            </p>
            <ol class="list-decimal list-inside text-[12px] text-[#1A1A17] space-y-0.5 pt-0.5">
              <li>Open <strong>Settings</strong> &rarr; <strong>Developer Settings</strong></li>
              <li>Toggle <strong>Testnet Mode: ON</strong></li>
              <li>Select <strong>Solana Devnet</strong></li>
            </ol>
          </div>
        </div>
      </div>

      <!-- If Not Connected: Phantom Connect / Join Action -->
      <div v-if="!currentAddress" class="space-y-3">
        <button 
          @click="$emit('connectPhantom')"
          :disabled="isConnecting"
          class="w-full p-4 rounded-[12px] border border-[#E3DFD6] bg-[#F7F5F0] hover:bg-[#EAE6DC] text-[#1A1A17] font-semibold text-[15px] flex items-center justify-between transition-transform active:scale-[0.99] cursor-pointer shadow-xs"
        >
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-[8px] bg-[#534BAE] flex items-center justify-center p-1.5 shadow-xs">
              <!-- Official Phantom Purple Ghost SVG -->
              <svg viewBox="0 0 128 128" class="w-full h-full text-white" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M112.5 64C112.5 90.7858 90.7858 112.5 64 112.5C48.0673 112.5 34.0203 104.793 25.2678 92.8944C23.7719 90.8609 25.1011 87.9733 27.6068 87.8767C37.0759 87.5118 45.4523 81.3323 48.7423 72.4839C49.9678 69.1882 48.3377 65.4853 45.1843 64.0954C34.5097 59.3907 27.0833 48.7619 27.0833 36.4167C27.0833 20.3168 40.1501 7.25 56.25 7.25C87.316 7.25 112.5 32.684 112.5 64Z" fill="white"/>
                <circle cx="53" cy="52" r="6" fill="#534BAE"/>
                <circle cx="79" cy="52" r="6" fill="#534BAE"/>
              </svg>
            </div>
            <div class="text-left">
              <div class="font-bold text-[#1A1A17]">{{ isConnecting ? 'Connecting Phantom...' : 'Connect Phantom Wallet' }}</div>
              <div class="text-[12px] text-[#5E5B53] font-normal">Connect or Join with your Solana address</div>
            </div>
          </div>
          <ArrowRight class="w-5 h-5 text-[#5E5B53]" />
        </button>

        <p class="text-center text-[12px] text-[#5E5B53]">
          Don't have Phantom? 
          <a href="https://phantom.app" target="_blank" class="underline font-medium text-[#1A1A17] hover:text-[#5E5B53] inline-flex items-center gap-0.5">
            Install extension <ExternalLink class="w-3 h-3" />
          </a>
        </p>
      </div>

      <!-- If Connected: Account Details & Live Devnet Balance -->
      <div v-else class="space-y-4">
        <div class="p-3.5 bg-[#F7F5F0] rounded-[10px] border border-[#E3DFD6] space-y-2 text-[13px]">
          <div class="flex justify-between items-center">
            <span class="text-[#5E5B53]">Connected Address</span>
            <span class="font-mono font-medium text-[#1A1A17]">{{ currentAddress.slice(0, 6) }}...{{ currentAddress.slice(-4) }}</span>
          </div>

          <div class="flex justify-between items-center">
            <span class="text-[#5E5B53]">Devnet Balance</span>
            <div class="flex items-center gap-1.5">
              <span class="font-semibold text-[#1A1A17]">{{ balance.toFixed(3) }} SOL</span>
              <button 
                @click="$emit('faucet')" 
                class="px-2 py-0.5 text-[11px] rounded-[6px] bg-[#1A1A17] text-white hover:bg-[#33332D] font-medium"
                title="Get free Devnet SOL for testing"
              >
                + AirDrop
              </button>
            </div>
          </div>

          <div v-if="userProfile" class="pt-2 border-t border-[#E3DFD6] flex justify-between items-center text-[12px]">
            <span class="text-[#5E5B53]">Tasks Posted: <strong>{{ userProfile.tasks_posted || 0 }}</strong></span>
            <span class="text-[#5E5B53]">Completed: <strong>{{ userProfile.tasks_completed || 0 }}</strong></span>
          </div>
        </div>

        <div class="flex items-center justify-between pt-1">
          <button 
            @click="$emit('faucet')"
            class="text-[13px] text-[#1A1A17] font-medium flex items-center gap-1.5 hover:underline"
          >
            <Sparkles class="w-3.5 h-3.5 text-[#FFD60A]" />
            <span>Request 0.05 Devnet Gas</span>
          </button>

          <button 
            @click="$emit('disconnect')" 
            class="text-[13px] text-[#B42318] font-medium hover:underline"
          >
            Disconnect
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

