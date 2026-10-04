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
          class="w-full p-4 rounded-[12px] border-2 border-[#1A1A17] bg-[#FFD60A] hover:bg-[#F2CA00] text-[#1A1A17] font-semibold text-[15px] flex items-center justify-between transition-transform active:scale-[0.99] cursor-pointer"
        >
          <div class="flex items-center gap-2.5">
            <div class="w-7 h-7 rounded-full bg-[#1A1A17] flex items-center justify-center text-white text-[11px] font-bold">
              👻
            </div>
            <div class="text-left">
              <div>{{ isConnecting ? 'Connecting...' : 'Connect Phantom' }}</div>
              <div class="text-[11px] text-[#1A1A17]/80 font-normal">Connect or Join with your Solana address</div>
            </div>
          </div>
          <ArrowRight class="w-5 h-5" />
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

