<script setup lang="ts">
defineEmits<{
  (e: 'startApp'): void
}>()
</script>

<template>
  <div class="min-h-screen bg-[#F7F5F0] text-[#1A1A17] flex flex-col justify-between">
    
    <!-- Header -->
    <header class="h-16 max-w-5xl mx-auto w-full px-6 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="font-bold text-[19px]">SolGuild</span>
        <span class="text-[13px] text-[#5E5B53]">Devnet</span>
      </div>
      <button 
        @click="$emit('startApp')"
        class="h-9 px-4 rounded-[12px] bg-[#FFD60A] text-[#1A1A17] font-semibold text-[15px] hover:brightness-95 transition-all"
      >
        Enter Guild Board
      </button>
    </header>

    <!-- Hero Section -->
    <main class="max-w-5xl mx-auto w-full px-6 py-12 md:py-16 space-y-16">
      
      <div class="grid grid-cols-1 md:grid-cols-12 gap-10 items-center">
        
        <!-- Left Column: Copy & Actions -->
        <div class="md:col-span-7 space-y-6 text-left">
          <h1 class="text-3xl sm:text-4xl md:text-[44px] font-bold text-[#1A1A17] leading-[1.15] tracking-tight">
            The on-chain adventurer guild for real life.
          </h1>
          <p class="text-[17px] text-[#5E5B53] leading-relaxed max-w-lg">
            Issue quests, rescue lost pets, recover forgotten items, and escort party members. SOL bounties locked in Solana Devnet escrow, released when photo evidence passes AI verification.
          </p>

          <div class="flex items-center gap-3 pt-2">
            <button 
              @click="$emit('startApp')"
              class="h-12 px-6 rounded-[12px] bg-[#FFD60A] text-[#1A1A17] font-semibold text-[15px] hover:brightness-95 transition-all shadow-xs"
            >
              Enter Guild Board
            </button>
            <a 
              href="https://github.com/VoltAgent/bountyblink"
              target="_blank"
              class="h-12 px-6 rounded-[12px] bg-white border border-[#E3DFD6] text-[#1A1A17] font-medium text-[15px] hover:bg-[#F7F5F0] transition-colors flex items-center justify-center"
            >
              GitHub repository
            </a>
          </div>
        </div>

        <!-- Right Column: Real Mobile App Mockup Frame -->
        <div class="md:col-span-5 flex justify-center">
          <div class="w-[280px] h-[520px] bg-white rounded-[36px] border-[6px] border-[#1A1A17] shadow-xl overflow-hidden flex flex-col relative text-left">
            <div class="w-24 h-4 bg-[#1A1A17] mx-auto rounded-b-xl mb-2"></div>
            
            <!-- Real app view inside phone frame -->
            <div class="flex-1 p-3 space-y-3 bg-[#F7F5F0]">
              <div class="h-28 bg-[#EAE6DC] rounded-xl flex items-center justify-center text-xs text-[#5E5B53] font-medium border border-[#E3DFD6]">
                Map with task pins
              </div>
              
              <div class="p-3 bg-white rounded-xl border border-[#E3DFD6] space-y-1 shadow-xs">
                <div class="flex justify-between font-semibold text-xs text-[#1A1A17]">
                  <span>EV charger status</span>
                  <span>0.01 SOL</span>
                </div>
                <p class="text-[11px] text-[#5E5B53] leading-snug">Check if Allego charger #3 is operational.</p>
                <div class="pt-2">
                  <div class="w-full py-1.5 bg-[#FFD60A] text-[#1A1A17] font-semibold text-[11px] rounded-lg text-center">
                    Claim this task
                  </div>
                </div>
              </div>
            </div>

            <div class="h-4 bg-white flex items-center justify-center">
              <div class="w-20 h-1 bg-[#E3DFD6] rounded-full"></div>
            </div>
          </div>
        </div>

      </div>

      <!-- 3-Step Horizontal Timeline -->
      <div class="pt-8 border-t border-[#E3DFD6] text-left">
        <h2 class="text-[22px] font-bold text-[#1A1A17] mb-8">How it works</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-5 bg-white rounded-[12px] border border-[#E3DFD6] space-y-2">
            <span class="text-xs font-semibold text-[#5E5B53]">Step 1</span>
            <h3 class="text-[17px] font-semibold text-[#1A1A17]">Post and deposit</h3>
            <p class="text-[15px] text-[#5E5B53] leading-relaxed">
              Create a task with location coordinates and deposit 0.01 SOL into escrow.
            </p>
          </div>

          <div class="p-5 bg-white rounded-[12px] border border-[#E3DFD6] space-y-2">
            <span class="text-xs font-semibold text-[#5E5B53]">Step 2</span>
            <h3 class="text-[17px] font-semibold text-[#1A1A17]">Claim and capture</h3>
            <p class="text-[15px] text-[#5E5B53] leading-relaxed">
              A nearby worker claims an exclusive 10-minute window and photographs the scene.
            </p>
          </div>

          <div class="p-5 bg-white rounded-[12px] border border-[#E3DFD6] space-y-2">
            <span class="text-xs font-semibold text-[#5E5B53]">Step 3</span>
            <h3 class="text-[17px] font-semibold text-[#1A1A17]">Check and settle</h3>
            <p class="text-[15px] text-[#5E5B53] leading-relaxed">
              Autonomous checks verify location and scene. Escrow pays the worker or refunds the creator.
            </p>
          </div>
        </div>
      </div>

      <!-- What gets checked rows -->
      <div class="pt-4 border-t border-[#E3DFD6] text-left space-y-4">
        <h2 class="text-[22px] font-bold text-[#1A1A17]">What gets checked</h2>
        <div class="divide-y divide-[#E3DFD6] bg-white rounded-[12px] border border-[#E3DFD6]">
          <div class="p-4 flex items-start gap-4">
            <span class="w-6 h-6 rounded-full bg-[#F7F5F0] flex items-center justify-center font-bold text-xs shrink-0">1</span>
            <div>
              <h4 class="font-semibold text-[15px]">Is it the right place?</h4>
              <p class="text-[13px] text-[#5E5B53]">Device GPS readings are matched to the task pin within a 150-meter tolerance.</p>
            </div>
          </div>
          <div class="p-4 flex items-start gap-4">
            <span class="w-6 h-6 rounded-full bg-[#F7F5F0] flex items-center justify-center font-bold text-xs shrink-0">2</span>
            <div>
              <h4 class="font-semibold text-[15px]">Is it the right thing?</h4>
              <p class="text-[13px] text-[#5E5B53]">Gemini multimodal vision checks that the requested scene or object is clearly visible.</p>
            </div>
          </div>
          <div class="p-4 flex items-start gap-4">
            <span class="w-6 h-6 rounded-full bg-[#F7F5F0] flex items-center justify-center font-bold text-xs shrink-0">3</span>
            <div>
              <h4 class="font-semibold text-[15px]">Is it a fresh, real photo?</h4>
              <p class="text-[13px] text-[#5E5B53]">The model checks for computer monitor lines, stock photos, or duplicate image hashes.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Honest Limits Section -->
      <div class="p-6 bg-white rounded-[12px] border border-[#E3DFD6] text-left space-y-2">
        <h3 class="text-[17px] font-bold text-[#1A1A17]">System limits</h3>
        <p class="text-[15px] text-[#5E5B53] leading-relaxed">
          Escrow is currently managed by a backend-held wallet on Solana Devnet. Location check from web browsers is best-effort and can be spoofed. Vision models can occasionally make errors. All settlements run on Devnet with test SOL only.
        </p>
      </div>

      <!-- FAQ Section -->
      <div class="pt-4 border-t border-[#E3DFD6] text-left space-y-4">
        <h2 class="text-[22px] font-bold text-[#1A1A17]">Frequently asked questions</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 bg-white rounded-[12px] border border-[#E3DFD6] space-y-1">
            <h4 class="font-semibold text-[15px]">Do I need a wallet extension to test?</h4>
            <p class="text-[13px] text-[#5E5B53]">No. The app generates a temporary Devnet wallet directly in your browser with test SOL included.</p>
          </div>
          <div class="p-4 bg-white rounded-[12px] border border-[#E3DFD6] space-y-1">
            <h4 class="font-semibold text-[15px]">What happens if verification fails?</h4>
            <p class="text-[13px] text-[#5E5B53]">The reward stays in escrow, and the task creator can claim an immediate on-chain refund.</p>
          </div>
        </div>
      </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-[#E3DFD6] py-8 text-center text-xs text-[#5E5B53]">
      <p>BountyBlink &middot; Solana Devnet MVP &middot; Open Source</p>
    </footer>

  </div>
</template>
