<script setup lang="ts">
import { ref } from 'vue'

defineEmits<{
  (e: 'startApp'): void
  (e: 'openPostQuest'): void
}>()

// Interactive Hero / Pipeline Simulation State
const simStep = ref<number>(0)
const isSimulating = ref<boolean>(false)

const runSimulation = () => {
  if (isSimulating.value) return
  isSimulating.value = true
  simStep.value = 1
  
  setTimeout(() => {
    simStep.value = 2
    setTimeout(() => {
      simStep.value = 3
      setTimeout(() => {
        simStep.value = 4
        setTimeout(() => {
          isSimulating.value = false
        }, 2200)
      }, 1100)
    }, 1100)
  }, 900)
}

const resetSimulation = () => {
  simStep.value = 0
  isSimulating.value = false
}
</script>

<template>
  <div class="min-h-dvh bg-[#F7F5F0] text-[#1A1A17] flex flex-col justify-between selection:bg-[#FFD60A] selection:text-[#1A1A17] relative overflow-x-hidden font-sans">
    
    <!-- Subtle organic background pastel shapes (inspired by reference image) -->
    <div class="absolute top-0 left-0 w-96 h-96 bg-amber-100/40 rounded-full blur-3xl pointer-events-none -translate-x-1/2 -translate-y-1/2"></div>
    <div class="absolute top-72 right-0 w-80 h-80 bg-rose-100/35 rounded-full blur-3xl pointer-events-none translate-x-1/3"></div>
    <div class="absolute top-[1600px] left-10 w-96 h-96 bg-emerald-100/30 rounded-full blur-3xl pointer-events-none"></div>

    <!-- NAVBAR -->
    <header class="sticky top-0 z-40 bg-[#F7F5F0]/90 backdrop-blur-md border-b border-[#E3DFD6]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        
        <!-- Left: Custom Sun + Shield SVG Logo & Brand Name -->
        <div class="flex items-center gap-3 cursor-pointer" @click="$emit('startApp')">
          <div class="w-10 h-10 rounded-full bg-[#1A1A17] flex items-center justify-center p-1.5 shadow-xs">
            <!-- Custom Yellow Sun + Shield SVG Logo -->
            <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
              <!-- Sunburst Rays -->
              <circle cx="18" cy="18" r="14" fill="#FFD60A" fill-opacity="0.25"/>
              <path d="M18 2v3.5M18 30.5v3.5M2 18h3.5M30.5 18h3.5M6.69 6.69l2.47 2.47M26.84 26.84l2.47 2.47M6.69 29.31l2.47-2.47M26.84 9.16l2.47-2.47" stroke="#FFD60A" stroke-width="2.2" stroke-linecap="round"/>
              <!-- Central Shield -->
              <path d="M18 7.5L25 10.8V17.5C25 22.8 22 26.5 18 28.5C14 26.5 11 22.8 11 17.5V10.8L18 7.5Z" fill="#FFD60A" stroke="#1A1A17" stroke-width="1.2" stroke-linejoin="round"/>
              <!-- Inner Emblem -->
              <path d="M18 12V23M14 16H22" stroke="#1A1A17" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="flex items-center gap-2">
            <span class="font-bold text-[18px] tracking-tight">SolGuild</span>
            <span class="text-[11px] font-mono font-semibold px-2 py-0.5 rounded-full bg-[#FFD60A]/30 text-[#8F7400] border border-[#FFD60A]/60">
              devnet
            </span>
          </div>
        </div>

        <!-- Center Links (Desktop) -->
        <nav class="hidden md:flex items-center gap-8 text-[14px] text-[#5E5B53] font-medium">
          <a href="#guild-contracts" class="hover:text-[#1A1A17] transition-colors">Bounty Tiers</a>
          <a href="#numbers" class="hover:text-[#1A1A17] transition-colors">Protocol Metrics</a>
          <a href="#workflow" class="hover:text-[#1A1A17] transition-colors">Workflow</a>
          <a href="#ranks" class="hover:text-[#1A1A17] transition-colors">Guild Ranks</a>
          <a href="#faq" class="hover:text-[#1A1A17] transition-colors">FAQ</a>
        </nav>

        <!-- Right: Action CTA Buttons -->
        <div class="flex items-center gap-3">
          <button 
            @click="$emit('startApp')"
            class="hidden sm:inline-flex text-[14px] font-medium text-[#5E5B53] hover:text-[#1A1A17] transition-colors"
          >
            Audit Log
          </button>
          <button 
            @click="$emit('startApp')"
            class="h-10 px-5 rounded-full bg-[#1A1A17] text-white font-semibold text-[13px] hover:bg-[#33332D] active:scale-[0.98] transition-all shadow-xs flex items-center gap-1.5"
          >
            <span>Enter Guild Board</span>
            <span class="text-xs">→</span>
          </button>
        </div>

      </div>
    </header>

    <!-- MAIN BODY -->
    <main class="max-w-6xl mx-auto w-full px-4 sm:px-6 py-10 sm:py-16 md:py-20 space-y-20 sm:space-y-28">
      
      <!-- HERO SECTION (Exact 2-Column Split matching reference image 2) -->
      <section class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center text-left">
        
        <!-- Hero Left Column: Editorial Typography with Colored Accent -->
        <div class="lg:col-span-6 space-y-6 relative">
          
          <!-- Delicate decorative vector line doodle (top-right of left column) -->
          <div class="absolute -top-6 right-8 hidden sm:block text-[#C5C0B5]">
            <svg width="44" height="28" viewBox="0 0 44 28" fill="none">
              <circle cx="4" cy="4" r="3" stroke="currentColor" stroke-width="1.5"/>
              <path d="M7 4C20 4 22 24 37 24" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 3"/>
              <circle cx="40" cy="24" r="3" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>

          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-[#E3DFD6] shadow-2xs">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-[12px] font-medium text-[#5E5B53]">Live across 8 European capitals &middot; Solana Devnet</span>
          </div>

          <!-- Headline with Colored Accent Word (matching dit.io layout) -->
          <h1 class="text-4xl sm:text-5xl md:text-[54px] font-bold text-[#1A1A17] leading-[1.12] tracking-tight">
            Improve the way <br />
            <span class="text-[#E63946] relative inline-block">
              you quest,
              <!-- Hand-drawn curved underline -->
              <svg class="absolute -bottom-1.5 left-0 w-full h-2.5 text-[#E63946]/40" viewBox="0 0 100 12" preserveAspectRatio="none">
                <path d="M0 6 Q 50 14, 100 6" stroke="currentColor" stroke-width="3" fill="none"/>
              </svg>
            </span>
            with one click
          </h1>

          <p class="text-base sm:text-lg text-[#5E5B53] leading-relaxed max-w-lg">
            Post municipal bounties, verify physical proof with multimodal Gemini vision, and release locked <span class="font-semibold text-[#1A1A17]">SOL Devnet Escrow</span> in under 3 seconds.
          </p>

          <!-- Store / Action Dual Pill Buttons -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-2">
            <button 
              @click="$emit('startApp')"
              class="h-12 px-7 rounded-full bg-[#1A1A17] text-white font-bold text-[14px] hover:bg-[#33332D] active:scale-[0.98] transition-all shadow-sm flex items-center justify-center gap-2"
            >
              <span>Explore Quests</span>
              <span class="text-base">⚔️</span>
            </button>
            <button 
              @click="$emit('openPostQuest')"
              class="h-12 px-7 rounded-full bg-white border border-[#E3DFD6] text-[#1A1A17] font-semibold text-[14px] hover:bg-[#F9F7F2] active:scale-[0.98] transition-all shadow-2xs flex items-center justify-center gap-2"
            >
              <span>Issue a Bounty</span>
              <span class="text-xs text-[#5E5B53] font-mono">+0.01 SOL min</span>
            </button>
          </div>

          <div class="text-[12px] text-[#5E5B53] pt-1 flex items-center gap-2">
            <span>Operating across London, Berlin, Paris, Madrid, Rome & Amsterdam</span>
          </div>

          <!-- Bottom delicate node connector -->
          <div class="pt-4 text-[#C5C0B5] hidden sm:block">
            <svg width="60" height="16" viewBox="0 0 60 16" fill="none">
              <circle cx="4" cy="8" r="3" stroke="currentColor" stroke-width="1.5"/>
              <line x1="8" y1="8" x2="52" y2="8" stroke="currentColor" stroke-width="1.5"/>
              <circle cx="56" cy="8" r="3" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>

        </div>

        <!-- Hero Right Column: Layered Floating UI Mockup (Matching reference card stack) -->
        <div class="lg:col-span-6 flex justify-center relative">
          
          <!-- Background subtle floating pill badge -->
          <div class="absolute -top-4 -right-2 z-20 hidden sm:block animate-bounce" style="animation-duration: 4s;">
            <div class="px-3.5 py-1.5 rounded-full bg-white border border-[#E3DFD6] shadow-md flex items-center gap-2 text-[12px] font-semibold text-[#1A1A17]">
              <span class="w-2 h-2 rounded-full bg-[#1E7B4F]"></span>
              <span>Devnet Escrow: 100% Locked</span>
            </div>
          </div>

          <!-- Main Stacked Card Container -->
          <div class="w-full max-w-md bg-white rounded-[32px] p-6 sm:p-7 shadow-[0_20px_50px_rgba(0,0,0,0.06)] border border-[#E3DFD6] relative space-y-5">
            
            <!-- Top Card Row: Adventurer Profile -->
            <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-4">
              <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-full bg-[#1A1A17] text-[#FFD60A] font-bold flex items-center justify-center text-sm border-2 border-[#FFD60A] shadow-xs">
                  AV
                </div>
                <div>
                  <div class="flex items-center gap-1.5">
                    <span class="font-bold text-[15px] text-[#1A1A17]">Alex Vance</span>
                    <span class="px-1.5 py-0.2 rounded text-[10px] font-bold bg-[#FFD60A] text-[#1A1A17]">D-Rank</span>
                  </div>
                  <div class="text-[12px] text-[#5E5B53]">Scout Operative &middot; Berlin</div>
                </div>
              </div>
              <div class="text-right">
                <span class="text-[11px] text-[#5E5B53] font-mono block">Completed</span>
                <span class="font-mono font-bold text-sm text-[#1A1A17]">22 Quests</span>
              </div>
            </div>

            <!-- Active Bounty Snippet Box -->
            <div class="p-4 rounded-2xl bg-[#F9F7F2] border border-[#E3DFD6] space-y-3">
              <div class="flex items-start justify-between">
                <div>
                  <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                    Civil Help
                  </span>
                  <h4 class="font-bold text-[14px] text-[#1A1A17] mt-1 leading-snug">
                    Find Lost Calico Cat "Mochi"
                  </h4>
                  <div class="text-[11px] text-[#5E5B53]">Alexanderplatz, Berlin</div>
                </div>
                <div class="text-right">
                  <div class="font-mono font-bold text-[16px] text-[#1A1A17]">0.045 SOL</div>
                  <div class="text-[10px] text-[#5E5B53] font-mono">~$7.20 USD</div>
                </div>
              </div>

              <!-- Live Verification Circular Metric & Progress Status -->
              <div class="pt-2 border-t border-[#E3DFD6] flex items-center justify-between text-xs">
                <div class="flex items-center gap-3">
                  <!-- Circular SVG progress meter -->
                  <div class="relative w-10 h-10 flex items-center justify-center">
                    <svg class="w-full h-full -rotate-90" viewBox="0 0 36 36">
                      <circle cx="18" cy="18" r="14" fill="none" stroke="#E3DFD6" stroke-width="3" />
                      <circle cx="18" cy="18" r="14" fill="none" stroke="#FFD60A" stroke-width="3" stroke-dasharray="88" stroke-dashoffset="24" stroke-linecap="round" />
                    </svg>
                    <span class="absolute text-[10px] font-mono font-bold text-[#1A1A17]">73%</span>
                  </div>
                  <div>
                    <div class="font-semibold text-[#1A1A17]">Geofence Proximity</div>
                    <div class="text-[11px] text-[#5E5B53] font-mono">42m / 150m boundary</div>
                  </div>
                </div>

                <div class="text-right font-mono text-[11px]">
                  <span class="text-[#1E7B4F] font-bold block">✓ PASSED</span>
                  <span class="text-[#5E5B53]">2.8s speed</span>
                </div>
              </div>
            </div>

            <!-- Interactive Verification Simulation Control -->
            <div class="space-y-2 pt-1">
              <div class="flex items-center justify-between text-[11px] font-mono text-[#5E5B53]">
                <span>Gemini 3.1 Flash-Lite Arbiter</span>
                <span v-if="simStep === 4" class="text-emerald-700 font-bold">✓ ESCROW SETTLED</span>
                <span v-else-if="isSimulating" class="text-amber-700 font-bold animate-pulse">EVALUATING PROOF...</span>
                <span v-else>Ready</span>
              </div>

              <!-- 4-Stage Mini Indicator -->
              <div class="grid grid-cols-4 gap-1.5">
                <div class="h-1.5 rounded-full transition-colors" :class="simStep >= 1 ? 'bg-emerald-500' : 'bg-[#E3DFD6]'"></div>
                <div class="h-1.5 rounded-full transition-colors" :class="simStep >= 2 ? 'bg-emerald-500' : 'bg-[#E3DFD6]'"></div>
                <div class="h-1.5 rounded-full transition-colors" :class="simStep >= 3 ? 'bg-emerald-500' : 'bg-[#E3DFD6]'"></div>
                <div class="h-1.5 rounded-full transition-colors" :class="simStep >= 4 ? 'bg-[#FFD60A]' : 'bg-[#E3DFD6]'"></div>
              </div>

              <div class="pt-2 flex gap-2">
                <button 
                  v-if="simStep === 0"
                  @click="runSimulation"
                  class="w-full py-2.5 rounded-full bg-[#FFD60A] text-[#1A1A17] font-bold text-xs hover:brightness-95 active:scale-[0.98] transition-all text-center shadow-xs cursor-pointer"
                >
                  ⚡ Simulate 3s Verification Flow
                </button>
                <button 
                  v-else-if="simStep === 4"
                  @click="resetSimulation"
                  class="w-full py-2.5 rounded-full bg-emerald-600 text-white font-bold text-xs hover:bg-emerald-700 transition-all text-center cursor-pointer"
                >
                  ✓ 0.045 SOL Released! Click to Replay
                </button>
                <button 
                  v-else
                  disabled
                  class="w-full py-2.5 rounded-full bg-[#EAE6DC] text-[#5E5B53] font-bold text-xs text-center cursor-not-allowed animate-pulse"
                >
                  Checking Scene & Escrow...
                </button>
              </div>
            </div>

          </div>

          <!-- Bottom left floating speech bubble chip -->
          <div class="absolute -bottom-4 -left-4 z-20 hidden sm:block">
            <div class="px-4 py-2 rounded-2xl bg-white border border-[#E3DFD6] shadow-lg flex items-center gap-2 text-xs font-semibold text-[#1A1A17]">
              <span class="text-emerald-600">✓</span>
              <span>Vision Match: 98% Confirmed</span>
            </div>
          </div>

        </div>

      </section>

      <!-- SOCIAL PROOF / CITIES STRIP (Directly below hero matching image 2) -->
      <section class="border-y border-[#E3DFD6] py-8 text-center space-y-4">
        <p class="text-xs sm:text-sm font-medium text-[#5E5B53]">
          Active across <span class="font-bold text-[#1A1A17]">88+ verified guild bounties</span> in major European capitals
        </p>
        <div class="flex flex-wrap items-center justify-center gap-3 sm:gap-6 text-xs sm:text-sm font-semibold text-[#5E5B53]">
          <span class="px-3 py-1 rounded-full bg-white border border-[#E3DFD6]">📍 Berlin</span>
          <span class="px-3 py-1 rounded-full bg-white border border-[#E3DFD6]">📍 London</span>
          <span class="px-3 py-1 rounded-full bg-white border border-[#E3DFD6]">📍 Paris</span>
          <span class="px-3 py-1 rounded-full bg-white border border-[#E3DFD6]">📍 Madrid</span>
          <span class="px-3 py-1 rounded-full bg-white border border-[#E3DFD6]">📍 Rome</span>
          <span class="px-3 py-1 rounded-full bg-white border border-[#E3DFD6]">📍 Amsterdam</span>
          <span class="px-3 py-1 rounded-full bg-amber-50 text-amber-900 border border-amber-200">⚡ Solana Devnet</span>
          <span class="px-3 py-1 rounded-full bg-purple-50 text-purple-900 border border-purple-200">✨ Gemini 3.1 Flash-Lite</span>
        </div>
      </section>

      <!-- FEATURES SECTION ("The Product we work with" in reference image 2) -->
      <section id="guild-contracts" class="p-8 sm:p-12 rounded-[36px] bg-[#F9F7F2] border border-[#E3DFD6] space-y-8 text-center">
        
        <div class="space-y-2 max-w-xl mx-auto">
          <h2 class="text-2xl sm:text-3xl md:text-4xl font-bold text-[#1A1A17] tracking-tight">
            The <span class="text-[#E63946]">Guild Contracts</span> we arbitrate
          </h2>
          <p class="text-sm sm:text-base text-[#5E5B53]">
            Every real-world assignment is backed by cryptographic escrow and evaluated across 3 clear categories.
          </p>
        </div>

        <!-- 3 Feature Cards Side-by-Side (Matching image 2 layout) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          
          <!-- Card 1: Civil Assistance -->
          <div class="p-6 sm:p-7 bg-white rounded-2xl border border-[#E3DFD6] space-y-4 shadow-2xs hover:shadow-md transition-shadow">
            <div class="w-12 h-12 rounded-2xl bg-[#FEF2F2] text-[#E63946] flex items-center justify-center text-xl font-bold">
              🛡️
            </div>
            <div class="space-y-1">
              <h3 class="font-bold text-[17px] text-[#1A1A17]">Civil Help</h3>
              <div class="text-[11px] font-mono text-[#8F7400] font-semibold uppercase">Community Assistance</div>
            </div>
            <p class="text-sm text-[#5E5B53] leading-relaxed">
              Finding lost pets, recovering misplaced keys, checking venue queues, or safely driving home the car of an intoxicated patron.
            </p>
            <div class="pt-2 border-t border-[#E3DFD6] text-xs font-mono text-[#5E5B53] flex items-center justify-between">
              <span>Photo Evidence</span>
              <span class="font-bold text-[#1A1A17]">&lt; 150m GPS</span>
            </div>
          </div>

          <!-- Card 2: Sensitive Intelligence -->
          <div class="p-6 sm:p-7 bg-white rounded-2xl border border-[#E3DFD6] space-y-4 shadow-2xs hover:shadow-md transition-shadow">
            <div class="w-12 h-12 rounded-2xl bg-[#ECFDF5] text-[#059669] flex items-center justify-center text-xl font-bold">
              🔍
            </div>
            <div class="space-y-1">
              <h3 class="font-bold text-[17px] text-[#1A1A17]">Sensitive Intel</h3>
              <div class="text-[11px] font-mono text-[#8F7400] font-semibold uppercase">Field Sourcing & Recon</div>
            </div>
            <p class="text-sm text-[#5E5B53] leading-relaxed">
              Historical plaque verification, memorial inscriptions, source origin tracking. Requires both verifiable photography and a full investigation dossier letter.
            </p>
            <div class="pt-2 border-t border-[#E3DFD6] text-xs font-mono text-[#5E5B53] flex items-center justify-between">
              <span>Photo + Dossier Letter</span>
              <span class="font-bold text-amber-700">Source Intel</span>
            </div>
          </div>

          <!-- Card 3: Commercial Promotion -->
          <div class="p-6 sm:p-7 bg-white rounded-2xl border border-[#E3DFD6] space-y-4 shadow-2xs hover:shadow-md transition-shadow">
            <div class="w-12 h-12 rounded-2xl bg-[#F5F3FF] text-[#7C3AED] flex items-center justify-center text-xl font-bold">
              📢
            </div>
            <div class="space-y-1">
              <h3 class="font-bold text-[17px] text-[#1A1A17]">Commercial UGC</h3>
              <div class="text-[11px] font-mono text-[#8F7400] font-semibold uppercase">Merchant & Creator Reels</div>
            </div>
            <p class="text-sm text-[#5E5B53] leading-relaxed">
              Showcasing local bakery pastries, filming beverage tasting clips against urban landmarks, and inspecting retail storefront displays.
            </p>
            <div class="pt-2 border-t border-[#E3DFD6] text-xs font-mono text-[#5E5B53] flex items-center justify-between">
              <span>Product Visibility</span>
              <span class="font-bold text-[#7C3AED]">Video Reel Proof</span>
            </div>
          </div>

        </div>

      </section>

      <!-- ABOUT / NUMBERS SECTION ("Okay, Let's see dit.io in numbers" matching image 2) -->
      <section id="numbers" class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center text-left">
        
        <!-- Left: Headline & 4 Metrics -->
        <div class="lg:col-span-6 space-y-6">
          <div class="space-y-2">
            <span class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider">Protocol Metrics</span>
            <h2 class="text-2xl sm:text-3xl md:text-4xl font-bold text-[#1A1A17] tracking-tight">
              Okay, Let's see <br />
              <span class="text-[#E63946]">SolGuild in numbers</span>
            </h2>
            <p class="text-sm sm:text-base text-[#5E5B53] leading-relaxed">
              Built on Solana Devnet to eliminate escrow middlemen, escrow disputes, and manual payouts. The protocol runs autonomously 24/7.
            </p>
          </div>

          <!-- 4 Stats Grid (Matching 50.4K / 20K / 300+ / 10K+ in reference) -->
          <div class="grid grid-cols-2 gap-6 pt-2">
            <div class="space-y-1">
              <div class="text-3xl sm:text-4xl font-bold text-[#1A1A17] font-mono">88+</div>
              <div class="text-xs font-semibold text-[#5E5B53] uppercase tracking-wider">European Quests Live</div>
            </div>
            <div class="space-y-1">
              <div class="text-3xl sm:text-4xl font-bold text-[#1A1A17] font-mono">&lt; 2.8s</div>
              <div class="text-xs font-semibold text-[#5E5B53] uppercase tracking-wider">Verification Payout</div>
            </div>
            <div class="space-y-1">
              <div class="text-3xl sm:text-4xl font-bold text-[#1A1A17] font-mono">100%</div>
              <div class="text-xs font-semibold text-[#5E5B53] uppercase tracking-wider">Locked Smart Escrow</div>
            </div>
            <div class="space-y-1">
              <div class="text-3xl sm:text-4xl font-bold text-[#8F7400] font-mono">+50 XP</div>
              <div class="text-xs font-semibold text-[#5E5B53] uppercase tracking-wider">Per Successful Mission</div>
            </div>
          </div>
        </div>

        <!-- Right: Verification Audit Card (Matching Right Card in reference) -->
        <div class="lg:col-span-6 flex justify-center">
          <div class="w-full max-w-md bg-white rounded-3xl p-6 sm:p-7 border border-[#E3DFD6] shadow-md space-y-4">
            <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                <span class="font-bold text-sm text-[#1A1A17]">Live Escrow Audit Stream</span>
              </div>
              <span class="text-[11px] font-mono text-[#5E5B53]">Cluster: Devnet</span>
            </div>

            <!-- Mini Pipeline Rows -->
            <div class="space-y-2 text-xs">
              <div class="p-3 rounded-xl bg-[#F9F7F2] border border-[#E3DFD6] flex items-center justify-between">
                <span class="font-medium text-[#1A1A17]">1. Geofence Boundary Check</span>
                <span class="font-mono text-emerald-700 font-bold">MATCH (42m)</span>
              </div>
              <div class="p-3 rounded-xl bg-[#F9F7F2] border border-[#E3DFD6] flex items-center justify-between">
                <span class="font-medium text-[#1A1A17]">2. Gemini Vision Scene Analysis</span>
                <span class="font-mono text-emerald-700 font-bold">98% CONFIRMED</span>
              </div>
              <div class="p-3 rounded-xl bg-[#F9F7F2] border border-[#E3DFD6] flex items-center justify-between">
                <span class="font-medium text-[#1A1A17]">3. Anti-AI / Freshness Verification</span>
                <span class="font-mono text-amber-700 font-bold">MVP BYPASS ACTIVE</span>
              </div>
              <div class="p-3 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-between">
                <span class="font-bold text-emerald-900">4. Solana Escrow Transfer</span>
                <span class="font-mono text-emerald-800 font-bold">PAID TO WORKER</span>
              </div>
            </div>

            <button 
              @click="$emit('startApp')"
              class="w-full py-2.5 rounded-xl bg-[#1A1A17] text-white font-semibold text-xs hover:bg-[#33332D] transition-all text-center cursor-pointer"
            >
              Audit Live Transactions on Map →
            </button>
          </div>
        </div>

      </section>

      <!-- WORKFLOW BENTO GRID (Explicit User Mandate: Instead of review section it must only be a bento grid of workflow) -->
      <section id="workflow" class="space-y-8 text-left">
        
        <div class="space-y-2">
          <span class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider">Workflow Architecture</span>
          <h2 class="text-2xl sm:text-3xl md:text-4xl font-bold text-[#1A1A17] tracking-tight">
            The <span class="text-[#E63946]">4-Step Workflow</span> behind every quest
          </h2>
          <p class="text-sm sm:text-base text-[#5E5B53] max-w-xl">
            A mathematically guaranteed cycle of locking, reservation, autonomous arbitration, and zero-drain settlement.
          </p>
        </div>

        <!-- Bento Grid: 4 Asymmetric Cards (No clunky images, clean typography + mini components) -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
          
          <!-- Bento 1: Wide Card (7 cols) -->
          <div class="md:col-span-7 bg-white p-7 rounded-3xl border border-[#E3DFD6] space-y-4 shadow-2xs flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-9 h-9 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center font-mono font-bold text-sm text-[#1A1A17]">
                01
              </div>
              <h3 class="text-xl font-bold text-[#1A1A17]">Post & Lock Escrow</h3>
              <p class="text-sm text-[#5E5B53] leading-relaxed">
                Quest posters drop target GPS coordinates onto the European map, define what the photo must and must not show, and deposit SOL directly into the verifiable guild escrow contract.
              </p>
            </div>

            <!-- Mini Component: Simulated Coordinate & Lock Spec -->
            <div class="p-3 bg-[#F9F7F2] rounded-xl border border-[#E3DFD6] flex items-center justify-between text-xs font-mono">
              <span class="text-[#5E5B53]">Target: 52.5113° N, 13.4593° E</span>
              <span class="font-bold text-[#1A1A17] bg-white px-2 py-0.5 rounded border border-[#E3DFD6]">0.035 SOL Locked</span>
            </div>
          </div>

          <!-- Bento 2: Standard Card (5 cols) -->
          <div class="md:col-span-5 bg-white p-7 rounded-3xl border border-[#E3DFD6] space-y-4 shadow-2xs flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-9 h-9 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center font-mono font-bold text-sm text-[#1A1A17]">
                02
              </div>
              <h3 class="text-xl font-bold text-[#1A1A17]">10-Minute Lock</h3>
              <p class="text-sm text-[#5E5B53] leading-relaxed">
                A nearby adventurer claims an exclusive 10-minute countdown window. Competing claims are locked out to eliminate race conditions.
              </p>
            </div>

            <!-- Mini Component: Live Reservation Countdown -->
            <div class="p-3 bg-amber-50 rounded-xl border border-amber-200 flex items-center justify-between text-xs font-mono">
              <span class="text-amber-800 font-semibold">Active Reservation</span>
              <span class="font-bold text-[#1A1A17] bg-white px-2 py-0.5 rounded border border-amber-300">10:00 Window</span>
            </div>
          </div>

          <!-- Bento 3: Standard Card (5 cols) -->
          <div class="md:col-span-5 bg-white p-7 rounded-3xl border border-[#E3DFD6] space-y-4 shadow-2xs flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-9 h-9 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center font-mono font-bold text-sm text-[#1A1A17]">
                03
              </div>
              <h3 class="text-xl font-bold text-[#1A1A17]">Multimodal Arbiter</h3>
              <p class="text-sm text-[#5E5B53] leading-relaxed">
                Gemini 3.1 Flash-Lite inspects device GPS telemetry, visual scene match, and mandatory source letters (< 150m tolerance).
              </p>
            </div>

            <!-- Mini Component: Multi-gate Verification Status -->
            <div class="p-3 bg-[#F9F7F2] rounded-xl border border-[#E3DFD6] space-y-1 text-xs">
              <div class="flex justify-between font-mono">
                <span class="text-[#5E5B53]">GPS Proximity</span>
                <span class="text-emerald-700 font-bold">MATCH (42m)</span>
              </div>
              <div class="flex justify-between font-mono">
                <span class="text-[#5E5B53]">Scene Verification</span>
                <span class="text-emerald-700 font-bold">98% CONFIRMED</span>
              </div>
            </div>
          </div>

          <!-- Bento 4: Wide Card (7 cols) -->
          <div class="md:col-span-7 bg-white p-7 rounded-3xl border border-[#E3DFD6] space-y-4 shadow-2xs flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-9 h-9 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center font-mono font-bold text-sm text-[#1A1A17]">
                04
              </div>
              <h3 class="text-xl font-bold text-[#1A1A17]">Zero-Drain Settlement & XP</h3>
              <p class="text-sm text-[#5E5B53] leading-relaxed">
                If passed, escrow transfers SOL to worker + 50 XP. If rejected, <span class="font-semibold text-[#1A1A17]">funds remain safely locked in escrow</span>, and the quest is marked "Failed 1x" for another adventurer to claim!
              </p>
            </div>

            <!-- Mini Component: Zero-Drain Escrow Guarantee -->
            <div class="p-3 bg-emerald-50 rounded-xl border border-emerald-200 flex items-center justify-between text-xs font-mono">
              <span class="text-emerald-800 font-semibold">🔒 Zero-Drain Escrow</span>
              <span class="font-bold text-emerald-900 bg-white px-2 py-0.5 rounded border border-emerald-300">+50 XP Awarded</span>
            </div>
          </div>

        </div>

      </section>

      <!-- BIG MVP AI DISCLAIMER NOTICE (Mandatory) -->
      <section class="p-6 sm:p-7 bg-amber-50/70 rounded-3xl border border-amber-300 text-left space-y-3 shadow-2xs">
        <div class="flex items-center gap-2.5">
          <span class="text-xl">⚠️</span>
          <h3 class="font-bold text-[16px] text-amber-950">
            Important Notice: Hackathon MVP & AI-Generated Evidence
          </h3>
        </div>
        <p class="text-[13px] sm:text-[14px] text-amber-900/90 leading-relaxed">
          <strong>Why anti-AI image filters are currently disabled:</strong> SolGuild is a live decentralized MVP operating across London, Berlin, Paris, Madrid, Rome, and Amsterdam. In order for judges, developers, and evaluators around the world to test quest submissions without having to physically travel to Germany or the UK, <span class="underline font-semibold">anti-AI picture generation filters are temporarily bypassed</span>. You are encouraged to submit AI-generated or mock photos that accurately depict the requested scene to verify that the Gemini Arbiter and Solana Devnet smart contract payout pipelines function seamlessly!
        </p>
      </section>

      <!-- GUILD RANK LADDER (F to S Rank) -->
      <section id="ranks" class="space-y-6 text-left">
        <div>
          <span class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider">Adventurer License</span>
          <h2 class="text-2xl sm:text-3xl font-bold text-[#1A1A17]">Climb the Guild Rank Ladder</h2>
          <p class="text-sm text-[#5E5B53] mt-0.5">Every completed quest awards exactly +50 XP on your cryptographic Guild License.</p>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          <div class="p-4 bg-white rounded-2xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-[#5E5B53]">F</div>
            <div class="text-xs font-bold text-[#1A1A17]">Rookie</div>
            <div class="text-[11px] font-mono text-[#8F7400]">0 XP</div>
          </div>
          <div class="p-4 bg-white rounded-2xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-blue-600">E</div>
            <div class="text-xs font-bold text-[#1A1A17]">Novice</div>
            <div class="text-[11px] font-mono text-[#8F7400]">100 XP</div>
          </div>
          <div class="p-4 bg-white rounded-2xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-emerald-600">D</div>
            <div class="text-xs font-bold text-[#1A1A17]">Scout</div>
            <div class="text-[11px] font-mono text-[#8F7400]">300 XP</div>
          </div>
          <div class="p-4 bg-white rounded-2xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-purple-600">C</div>
            <div class="text-xs font-bold text-[#1A1A17]">Veteran</div>
            <div class="text-[11px] font-mono text-[#8F7400]">600 XP</div>
          </div>
          <div class="p-4 bg-white rounded-2xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-amber-600">B / A</div>
            <div class="text-xs font-bold text-[#1A1A17]">Champion</div>
            <div class="text-[11px] font-mono text-[#8F7400]">1,000 XP</div>
          </div>
          <div class="p-4 bg-[#1A1A17] text-[#FFD60A] rounded-2xl border-2 border-[#FFD60A] text-center space-y-1 shadow-xs">
            <div class="font-mono font-bold text-2xl text-[#FFD60A]">S</div>
            <div class="text-xs font-bold text-white">Sovereign</div>
            <div class="text-[11px] font-mono text-[#FFD60A]">2,500+ XP</div>
          </div>
        </div>
      </section>

      <!-- FAQ SECTION -->
      <section id="faq" class="space-y-6 text-left border-t border-[#E3DFD6] pt-12">
        <div>
          <span class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider">Protocol Guidance</span>
          <h2 class="text-2xl sm:text-3xl font-bold text-[#1A1A17]">Frequently Asked Questions</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">Do I need real Solana to use SolGuild?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              No! SolGuild runs entirely on <strong>Solana Devnet</strong>. You can connect your Phantom wallet or generate an instant browser burner wallet. Devnet SOL is free via our one-click faucet.
            </p>
          </div>

          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">What happens if verification fails?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              The failure reason is displayed for 5 seconds. The bounty stays safely locked in escrow, and the quest returns to the open board marked <strong>Failed 1x</strong> for another adventurer.
            </p>
          </div>

          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">Why does Sensitive Intel require a dossier letter?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              Discreet reconnaissance requires context (source origin, archives, witness statements). Gemini multimodal checks both the physical photo and the written report.
            </p>
          </div>

          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">Can an issuer cancel and refund their bounty?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              Yes. If a quest has not yet been claimed or successfully completed, the original poster can trigger an on-chain refund from their Guild License to reclaim their locked SOL from escrow.
            </p>
          </div>
        </div>
      </section>

      <!-- CTA SECTION (Soft Tinted Card matching bottom of image 2) -->
      <section class="p-8 sm:p-14 rounded-[36px] bg-[#F9F7F2] border border-[#E3DFD6] text-center space-y-6 relative overflow-hidden">
        
        <!-- Subtle corner halo -->
        <div class="absolute -top-10 -right-10 w-48 h-48 bg-amber-200/30 rounded-full blur-2xl pointer-events-none"></div>

        <div class="max-w-xl mx-auto space-y-3">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-[#E3DFD6] text-xs font-mono font-semibold text-[#8F7400]">
            ⚔️ Open Adventurer Dispatch
          </div>
          <h2 class="text-3xl sm:text-4xl md:text-5xl font-bold text-[#1A1A17] tracking-tight">
            Ready to take on your <br />
            <span class="text-[#E63946]">first quest</span>?
          </h2>
          <p class="text-sm sm:text-base text-[#5E5B53] leading-relaxed">
            Join the decentralized adventurer network on Solana Devnet. Solve real-world tasks, earn SOL, and forge your adventurer rank.
          </p>
        </div>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <button 
            @click="$emit('startApp')"
            class="h-12 px-8 rounded-full bg-[#1A1A17] text-white font-bold text-[14px] hover:bg-[#33332D] active:scale-[0.98] transition-all shadow-sm flex items-center justify-center gap-2"
          >
            <span>Explore Guild Board</span>
            <span>→</span>
          </button>
          <button 
            @click="$emit('openPostQuest')"
            class="h-12 px-7 rounded-full bg-white border border-[#E3DFD6] text-[#1A1A17] font-semibold text-[14px] hover:bg-[#F2EFE9] active:scale-[0.98] transition-all flex items-center justify-center gap-2 shadow-2xs"
          >
            <span>Issue a Bounty</span>
          </button>
        </div>

      </section>

    </main>

    <!-- FOOTER -->
    <footer class="border-t border-[#E3DFD6] bg-white py-10 text-xs text-[#5E5B53] space-y-4">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-6">
        
        <!-- Logo & Tagline -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-[#1A1A17] flex items-center justify-center p-1 shadow-2xs">
            <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
              <circle cx="18" cy="18" r="14" fill="#FFD60A" fill-opacity="0.3"/>
              <path d="M18 2v3M18 31v3M2 18h3M31 18h3" stroke="#FFD60A" stroke-width="2" stroke-linecap="round"/>
              <path d="M18 7.5L25 10.8V17.5C25 22.8 22 26.5 18 28.5C14 26.5 11 22.8 11 17.5V10.8L18 7.5Z" fill="#FFD60A"/>
              <path d="M18 12V23M14 16H22" stroke="#1A1A17" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </div>
          <div>
            <span class="font-bold text-[#1A1A17] text-[14px]">SolGuild</span>
            <span class="text-[#5E5B53] block text-[11px]">The Real-World Anime Adventurer Guild on Solana Devnet</span>
          </div>
        </div>

        <!-- Links -->
        <div class="flex items-center gap-6 text-[#5E5B53] font-medium">
          <button @click="$emit('startApp')" class="hover:text-[#1A1A17] transition-colors">Quests</button>
          <button @click="$emit('openPostQuest')" class="hover:text-[#1A1A17] transition-colors">Issue Quest</button>
          <a href="#guild-contracts" class="hover:text-[#1A1A17] transition-colors">Bounty Tiers</a>
          <a href="#workflow" class="hover:text-[#1A1A17] transition-colors">Workflow</a>
        </div>

      </div>
    </footer>

  </div>
</template>
