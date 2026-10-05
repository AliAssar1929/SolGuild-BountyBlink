<script setup lang="ts">
import { ref } from 'vue'

defineEmits<{
  (e: 'startApp'): void
  (e: 'openPostQuest'): void
}>()

// Interactive Hero Demo State
const demoStep = ref<number>(0)
const isSimulating = ref<boolean>(false)

const startInteractiveDemo = () => {
  if (isSimulating.value) return
  isSimulating.value = true
  demoStep.value = 1
  
  setTimeout(() => {
    demoStep.value = 2
    setTimeout(() => {
      demoStep.value = 3
      setTimeout(() => {
        demoStep.value = 4
        setTimeout(() => {
          isSimulating.value = false
        }, 2000)
      }, 1200)
    }, 1200)
  }, 1000)
}

const resetDemo = () => {
  demoStep.value = 0
  isSimulating.value = false
}

// Category Tabs for Interactive Showcase
const activeCategoryTab = ref<'civil' | 'sensitive' | 'commercial'>('civil')

const sampleQuests = {
  civil: {
    title: 'Find Lost Calico Cat "Mochi" near Alexanderplatz',
    bounty: '0.045 SOL',
    city: 'Berlin, Germany',
    badge: 'Civil Help',
    badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    desc: 'Mochi slipped past the café courtyard. Last seen wearing a red collar with a brass bell near the TV Tower.',
    reqs: 'Photograph cat with identifiable red collar + device GPS within 200m.',
    rewardExp: '+50 XP'
  },
  sensitive: {
    title: 'Verify Historic Blue Plaque & Archive Letter on Baker St',
    bounty: '0.080 SOL',
    city: 'London, UK',
    badge: 'Sensitive Intel',
    badgeColor: 'bg-amber-50 text-amber-700 border-amber-200',
    desc: 'Inspect the memorial inscription on Baker Street building facade and compile source origin details.',
    reqs: 'Clear photo of plaque engraving + mandatory full source letter / dossier.',
    rewardExp: '+50 XP'
  },
  commercial: {
    title: 'Film 10s UGC Sip Video with Club-Mate at Spree Canal',
    bounty: '0.060 SOL',
    city: 'Berlin, Germany',
    badge: 'Commercial Promo',
    badgeColor: 'bg-purple-50 text-purple-700 border-purple-200',
    desc: 'Record a brief crisp aesthetic clip holding a Club-Mate bottle against the canal background.',
    reqs: 'Photo proof of product bottle + video frame capture with canal water visible.',
    rewardExp: '+50 XP'
  }
}
</script>

<template>
  <div class="min-h-dvh bg-[#F7F5F0] text-[#1A1A17] flex flex-col justify-between selection:bg-[#FFD60A] selection:text-[#1A1A17]">
    
    <!-- Top Guild Navigation Bar -->
    <header class="sticky top-0 z-40 bg-[#F7F5F0]/90 backdrop-blur-md border-b border-[#E3DFD6]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-[#1A1A17] text-[#FFD60A] flex items-center justify-center font-bold text-lg shadow-xs">
            ⚔️
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-bold text-[18px] tracking-tight">SolGuild</span>
              <span class="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-[#FFD60A]/30 text-[#8F7400] border border-[#FFD60A]/60">
                Solana Devnet
              </span>
            </div>
            <p class="text-[11px] text-[#5E5B53] hidden sm:block">The Real-World Anime Adventurer Guild</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button 
            @click="$emit('startApp')"
            class="h-10 px-5 rounded-[12px] bg-[#FFD60A] text-[#1A1A17] font-semibold text-[14px] hover:brightness-95 active:scale-[0.98] transition-all shadow-xs flex items-center gap-2"
          >
            <span>Enter Guild Board</span>
            <span class="text-sm">→</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-6xl mx-auto w-full px-4 sm:px-6 py-8 sm:py-12 md:py-16 space-y-16 sm:space-y-24">
      
      <!-- HERO SECTION -->
      <section class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-center">
        
        <!-- Left: Hook, Anime Premise, CTA -->
        <div class="lg:col-span-7 space-y-6 text-left">
          
          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-[#E3DFD6] shadow-2xs">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-[12px] font-medium text-[#5E5B53]">Live across major European capitals</span>
          </div>

          <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-[#1A1A17] leading-[1.12] tracking-tight">
            The on-chain adventurer guild for real life.
          </h1>

          <p class="text-base sm:text-lg text-[#5E5B53] leading-relaxed max-w-xl">
            Post bounties for real-world tasks. Accept quests across Europe. When proof is submitted, our AI Guild Arbiter verifies the scene and releases locked <span class="font-semibold text-[#1A1A17]">SOL Devnet Escrow</span> in under 3 seconds.
          </p>

          <!-- Core Call to Action Buttons -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-2">
            <button 
              @click="$emit('startApp')"
              class="h-12 px-6 rounded-[12px] bg-[#FFD60A] text-[#1A1A17] font-bold text-[15px] hover:brightness-95 active:scale-[0.98] transition-all shadow-xs flex items-center justify-center gap-2"
            >
              <span>Explore Active Quests</span>
              <span class="text-base font-bold">⚔️</span>
            </button>
            <button 
              @click="$emit('openPostQuest')"
              class="h-12 px-6 rounded-[12px] bg-white border border-[#E3DFD6] text-[#1A1A17] font-semibold text-[15px] hover:bg-[#EAE6DC]/40 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
            >
              <span>Issue a Bounty Quest</span>
              <span class="text-xs text-[#5E5B53] font-mono">+0.01 SOL min</span>
            </button>
          </div>

          <!-- Trust Badges Strip -->
          <div class="pt-4 grid grid-cols-3 gap-3 border-t border-[#E3DFD6] max-w-lg">
            <div>
              <div class="font-mono font-bold text-lg text-[#1A1A17]">&lt; 3.0s</div>
              <div class="text-[12px] text-[#5E5B53]">AI Arbiter Payout</div>
            </div>
            <div>
              <div class="font-mono font-bold text-lg text-[#1A1A17]">100% Locked</div>
              <div class="text-[12px] text-[#5E5B53]">On-Chain Escrow</div>
            </div>
            <div>
              <div class="font-mono font-bold text-lg text-[#1A1A17]">F → S Rank</div>
              <div class="text-[12px] text-[#5E5B53]">+50 XP Progression</div>
            </div>
          </div>

        </div>

        <!-- Right: Interactive Live Guild Card & Verification Stepper -->
        <div class="lg:col-span-5 flex justify-center">
          <div class="w-full max-w-md bg-white rounded-2xl border-2 border-[#1A1A17] shadow-[6px_6px_0px_0px_#1A1A17] overflow-hidden text-left transition-all">
            
            <!-- Card Header -->
            <div class="p-4 bg-[#1A1A17] text-white flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-[#FFD60A] animate-ping"></span>
                <span class="font-mono text-xs text-[#FFD60A] font-semibold uppercase tracking-wider">Interactive Quest Simulator</span>
              </div>
              <span class="text-[11px] font-mono text-[#E3DFD6]">Berlin Guild Hall</span>
            </div>

            <!-- Card Body -->
            <div class="p-5 space-y-4">
              
              <div class="flex items-start justify-between gap-2">
                <div>
                  <span class="inline-block px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-emerald-100 text-emerald-800 mb-1">
                    Civil Help Quest
                  </span>
                  <h3 class="font-bold text-[16px] text-[#1A1A17] leading-snug">
                    Confirm Missing Cat Sighting at Alexanderplatz
                  </h3>
                </div>
                <div class="text-right shrink-0">
                  <div class="font-mono font-bold text-lg text-[#1A1A17]">0.045 SOL</div>
                  <div class="text-[11px] text-[#5E5B53] font-mono">Escrow Locked</div>
                </div>
              </div>

              <!-- Interactive Simulator Stepper Box -->
              <div class="p-4 bg-[#F7F5F0] rounded-xl border border-[#E3DFD6] space-y-3">
                <div class="text-xs font-semibold text-[#5E5B53] uppercase tracking-wider flex justify-between items-center">
                  <span>Gemini Multimodal Arbiter</span>
                  <span v-if="demoStep === 4" class="text-emerald-700 font-bold">✓ SETTLED</span>
                  <span v-else-if="isSimulating" class="text-amber-700 font-bold animate-pulse">VERIFYING...</span>
                  <span v-else class="text-xs text-[#5E5B53]">Ready</span>
                </div>

                <!-- 4 Step Mini Pipeline -->
                <div class="space-y-2">
                  <div class="flex items-center justify-between text-xs p-2 rounded-lg bg-white border border-[#E3DFD6]"
                       :class="demoStep >= 1 ? 'border-emerald-500 bg-emerald-50/50' : ''">
                    <span class="flex items-center gap-2">
                      <span v-if="demoStep >= 1" class="text-emerald-600 font-bold">✓</span>
                      <span v-else class="text-[#5E5B53]">1.</span>
                      <span>GPS Proximity Gate (&lt;150m)</span>
                    </span>
                    <span class="font-mono text-[11px]" :class="demoStep >= 1 ? 'text-emerald-700 font-semibold' : 'text-[#5E5B53]'">
                      {{ demoStep >= 1 ? 'MATCH (42m)' : 'Pending' }}
                    </span>
                  </div>

                  <div class="flex items-center justify-between text-xs p-2 rounded-lg bg-white border border-[#E3DFD6]"
                       :class="demoStep >= 2 ? 'border-emerald-500 bg-emerald-50/50' : ''">
                    <span class="flex items-center gap-2">
                      <span v-if="demoStep >= 2" class="text-emerald-600 font-bold">✓</span>
                      <span v-else class="text-[#5E5B53]">2.</span>
                      <span>Vision Scene Match</span>
                    </span>
                    <span class="font-mono text-[11px]" :class="demoStep >= 2 ? 'text-emerald-700 font-semibold' : 'text-[#5E5B53]'">
                      {{ demoStep >= 2 ? 'CONFIRMED (96%)' : 'Pending' }}
                    </span>
                  </div>

                  <div class="flex items-center justify-between text-xs p-2 rounded-lg bg-white border border-[#E3DFD6]"
                       :class="demoStep >= 3 ? 'border-emerald-500 bg-emerald-50/50' : ''">
                    <span class="flex items-center gap-2">
                      <span v-if="demoStep >= 3" class="text-emerald-600 font-bold">✓</span>
                      <span v-else class="text-[#5E5B53]">3.</span>
                      <span>Origin & Freshness Check</span>
                    </span>
                    <span class="font-mono text-[11px]" :class="demoStep >= 3 ? 'text-emerald-700 font-semibold' : 'text-[#5E5B53]'">
                      {{ demoStep >= 3 ? 'GENUINE PHOTO' : 'Pending' }}
                    </span>
                  </div>

                  <div class="flex items-center justify-between text-xs p-2 rounded-lg bg-white border border-[#E3DFD6]"
                       :class="demoStep >= 4 ? 'border-emerald-500 bg-emerald-50/50' : ''">
                    <span class="flex items-center gap-2">
                      <span v-if="demoStep >= 4" class="text-emerald-600 font-bold">✓</span>
                      <span v-else class="text-[#5E5B53]">4.</span>
                      <span>Solana Devnet Transfer</span>
                    </span>
                    <span class="font-mono text-[11px]" :class="demoStep >= 4 ? 'text-emerald-700 font-semibold' : 'text-[#5E5B53]'">
                      {{ demoStep >= 4 ? '0.045 SOL PAID' : 'Locked' }}
                    </span>
                  </div>
                </div>

              </div>

              <!-- Interactive Demo Control Button -->
              <div class="pt-1 flex gap-2">
                <button 
                  v-if="demoStep === 0"
                  @click="startInteractiveDemo"
                  class="flex-1 py-2.5 rounded-xl bg-[#FFD60A] text-[#1A1A17] font-bold text-xs hover:brightness-95 active:scale-[0.98] transition-all text-center shadow-xs"
                >
                  ⚡ Simulate AI Verification Flow
                </button>
                <button 
                  v-else-if="demoStep === 4"
                  @click="resetDemo"
                  class="flex-1 py-2.5 rounded-xl bg-emerald-600 text-white font-bold text-xs hover:bg-emerald-700 transition-all text-center"
                >
                  ✓ Payout Complete! Click to Replay
                </button>
                <button 
                  v-else
                  disabled
                  class="flex-1 py-2.5 rounded-xl bg-[#EAE6DC] text-[#5E5B53] font-bold text-xs text-center cursor-not-allowed animate-pulse"
                >
                  Evaluating Evidence...
                </button>
              </div>

            </div>

          </div>
        </div>

      </section>

      <!-- BIG MVP DISCLAIMER BANNER -->
      <section class="p-6 bg-amber-50/70 rounded-2xl border-2 border-amber-300 text-left space-y-3 shadow-xs">
        <div class="flex items-center gap-2.5">
          <span class="text-xl">⚠️</span>
          <h3 class="font-bold text-[16px] text-amber-950">
            Important Notice: Hackathon MVP & AI-Generated Evidence
          </h3>
        </div>
        <p class="text-[14px] text-amber-900/90 leading-relaxed">
          <strong>Why anti-AI image filters are currently disabled:</strong> SolGuild is a live decentralized MVP operating across London, Berlin, Paris, Madrid, and Rome. In order for judges, developers, and evaluators around the world to test quest submissions without having to physically travel to Germany or the UK, <span class="underline font-semibold">anti-AI picture generation filters are temporarily bypassed</span>. You are encouraged to submit AI-generated or mock photos that accurately depict the requested scene to verify that the Gemini Arbiter and Solana Devnet smart contract payout pipelines function seamlessly!
        </p>
      </section>

      <!-- 3 GUILD BOARDS / CATEGORIES SECTION -->
      <section class="space-y-8 text-left">
        <div>
          <div class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider mb-1">Guild Board Categories</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-[#1A1A17]">Three types of adventurer contracts.</h2>
          <p class="text-sm sm:text-base text-[#5E5B53] max-w-2xl mt-1">
            Whether helping a neighbor, gathering critical intelligence, or promoting a local product, every quest is protected by cryptographic escrow.
          </p>
        </div>

        <!-- Category Selector Buttons -->
        <div class="flex flex-wrap gap-2 border-b border-[#E3DFD6] pb-3">
          <button 
            @click="activeCategoryTab = 'civil'"
            class="px-4 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2"
            :class="activeCategoryTab === 'civil' ? 'bg-[#1A1A17] text-[#FFD60A] shadow-xs' : 'bg-white text-[#5E5B53] border border-[#E3DFD6] hover:bg-[#F7F5F0]'"
          >
            <span>🛡️ 1. Civil Help</span>
          </button>
          <button 
            @click="activeCategoryTab = 'sensitive'"
            class="px-4 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2"
            :class="activeCategoryTab === 'sensitive' ? 'bg-[#1A1A17] text-[#FFD60A] shadow-xs' : 'bg-white text-[#5E5B53] border border-[#E3DFD6] hover:bg-[#F7F5F0]'"
          >
            <span>🔍 2. Sensitive Intel</span>
          </button>
          <button 
            @click="activeCategoryTab = 'commercial'"
            class="px-4 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2"
            :class="activeCategoryTab === 'commercial' ? 'bg-[#1A1A17] text-[#FFD60A] shadow-xs' : 'bg-white text-[#5E5B53] border border-[#E3DFD6] hover:bg-[#F7F5F0]'"
          >
            <span>📢 3. Commercial UGC</span>
          </button>
        </div>

        <!-- Category Feature Showcase -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center bg-white p-6 sm:p-8 rounded-2xl border border-[#E3DFD6] shadow-xs">
          
          <div class="md:col-span-7 space-y-4">
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-1 rounded-full text-xs font-bold border" :class="sampleQuests[activeCategoryTab].badgeColor">
                {{ sampleQuests[activeCategoryTab].badge }}
              </span>
              <span class="text-xs font-mono text-[#5E5B53]">📍 {{ sampleQuests[activeCategoryTab].city }}</span>
            </div>

            <h3 class="text-xl sm:text-2xl font-bold text-[#1A1A17]">
              {{ sampleQuests[activeCategoryTab].title }}
            </h3>

            <p class="text-sm text-[#5E5B53] leading-relaxed">
              {{ sampleQuests[activeCategoryTab].desc }}
            </p>

            <div class="p-3.5 bg-[#F7F5F0] rounded-xl border border-[#E3DFD6] space-y-1">
              <div class="text-xs font-bold text-[#1A1A17]">Verification Criteria:</div>
              <div class="text-xs text-[#5E5B53] font-mono">{{ sampleQuests[activeCategoryTab].reqs }}</div>
            </div>

            <div class="flex items-center gap-4 pt-2">
              <div>
                <span class="text-[11px] text-[#5E5B53] uppercase font-mono">Bounty</span>
                <div class="font-mono font-bold text-lg text-[#1A1A17]">{{ sampleQuests[activeCategoryTab].bounty }}</div>
              </div>
              <div class="border-l border-[#E3DFD6] pl-4">
                <span class="text-[11px] text-[#5E5B53] uppercase font-mono">Guild Exp</span>
                <div class="font-mono font-bold text-lg text-[#8F7400]">{{ sampleQuests[activeCategoryTab].rewardExp }}</div>
              </div>
            </div>
          </div>

          <div class="md:col-span-5 p-6 bg-[#F7F5F0] rounded-xl border border-[#E3DFD6] space-y-3 text-xs text-[#5E5B53]">
            <div class="font-bold text-[#1A1A17] text-sm">Category Rules & Requirements</div>
            
            <div v-if="activeCategoryTab === 'civil'" class="space-y-2">
              <p>• <strong>Civil Quests</strong> cover real-world community assistance: lost pets, stranded bikes, checking venue queues, or escorting an intoxicated friend safely home.</p>
              <p>• <strong>Evidence:</strong> 1 clear photograph demonstrating the task outcome + device GPS proximity match.</p>
            </div>

            <div v-if="activeCategoryTab === 'sensitive'" class="space-y-2">
              <p>• <strong>Sensitive Intel Quests</strong> involve discreet observation, source tracing, or historical verification.</p>
              <p>• <strong>Mandatory Rule:</strong> Photo alone is rejected. Adventurers <span class="text-amber-900 font-semibold underline">must submit a full dossier letter</span> explaining source details, origin context, and findings.</p>
            </div>

            <div v-if="activeCategoryTab === 'commercial'" class="space-y-2">
              <p>• <strong>Commercial Quests</strong> reward community creators for product showcases, billboard photos, and creative UGC reels.</p>
              <p>• <strong>Evidence:</strong> Product visibility + location context + optional video proof URL.</p>
            </div>

            <button 
              @click="$emit('startApp')"
              class="w-full mt-2 py-2 rounded-lg bg-[#FFD60A] text-[#1A1A17] font-bold text-xs hover:brightness-95 transition-all text-center shadow-xs"
            >
              Browse Category on Map →
            </button>
          </div>

        </div>

      </section>

      <!-- HOW IT WORKS & LOCKED ESCROW POLICY -->
      <section class="space-y-8 text-left">
        <div>
          <div class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider mb-1">Guild Mechanics</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-[#1A1A17]">How quests resolve on Solana Devnet.</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div class="p-6 bg-white rounded-2xl border border-[#E3DFD6] space-y-3 shadow-xs">
            <div class="w-10 h-10 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center font-mono font-bold text-base text-[#1A1A17]">
              01
            </div>
            <h3 class="font-bold text-[17px] text-[#1A1A17]">Issue & Lock Escrow</h3>
            <p class="text-sm text-[#5E5B53] leading-relaxed">
              Quest posters pin coordinates on the European map, define criteria, and deposit SOL directly into the guild's verifiable escrow vault.
            </p>
          </div>

          <div class="p-6 bg-white rounded-2xl border border-[#E3DFD6] space-y-3 shadow-xs">
            <div class="w-10 h-10 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center font-mono font-bold text-base text-[#1A1A17]">
              02
            </div>
            <h3 class="font-bold text-[17px] text-[#1A1A17]">10-Minute Exclusive Claim</h3>
            <p class="text-sm text-[#5E5B53] leading-relaxed">
              An adventurer near the location locks the quest for 10 minutes, uploads live photo evidence (+ letter if Sensitive), and triggers the arbiter.
            </p>
          </div>

          <div class="p-6 bg-white rounded-2xl border border-[#E3DFD6] space-y-3 shadow-xs">
            <div class="w-10 h-10 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center font-mono font-bold text-base text-[#1A1A17]">
              03
            </div>
            <h3 class="font-bold text-[17px] text-[#1A1A17]">Arbiter Verdict & Payout</h3>
            <p class="text-sm text-[#5E5B53] leading-relaxed">
              If approved, escrow immediately releases SOL to the worker + 50 XP. If rejected, <span class="font-semibold text-[#1A1A17]">funds remain safely locked in escrow</span>, marked "Failed 1x" for another adventurer to try!
            </p>
          </div>

        </div>

        <!-- Failure & Locked Escrow Explanation Banner -->
        <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="font-bold text-sm text-[#1A1A17] flex items-center gap-2">
              <span>🔒 Zero-Drain Escrow Architecture</span>
            </div>
            <p class="text-xs text-[#5E5B53] max-w-2xl">
              Failed submissions never steal or refund escrow funds to arbitrary wallets. The reward stays locked in the smart contract until a valid submission arrives or the poster explicitly requests an on-chain refund.
            </p>
          </div>
          <button 
            @click="$emit('startApp')"
            class="px-4 py-2 rounded-xl bg-[#F7F5F0] border border-[#E3DFD6] hover:bg-white text-xs font-semibold text-[#1A1A17] shrink-0"
          >
            Audit Live Activity Log
          </button>
        </div>

      </section>

      <!-- ADVENTURER LICENSE & RANK PROGRESSION -->
      <section class="space-y-8 text-left">
        <div>
          <div class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider mb-1">Adventurer License</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-[#1A1A17]">Climb the Guild Rank Ladder.</h2>
          <p class="text-sm text-[#5E5B53]">
            Every completed quest awards exactly +50 XP on your cryptographic Guild License.
          </p>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          
          <div class="p-4 bg-white rounded-xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-[#5E5B53]">F</div>
            <div class="text-xs font-bold text-[#1A1A17]">Rookie</div>
            <div class="text-[11px] font-mono text-[#8F7400]">0 XP</div>
          </div>

          <div class="p-4 bg-white rounded-xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-blue-600">E</div>
            <div class="text-xs font-bold text-[#1A1A17]">Novice</div>
            <div class="text-[11px] font-mono text-[#8F7400]">100 XP</div>
          </div>

          <div class="p-4 bg-white rounded-xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-emerald-600">D</div>
            <div class="text-xs font-bold text-[#1A1A17]">Scout</div>
            <div class="text-[11px] font-mono text-[#8F7400]">300 XP</div>
          </div>

          <div class="p-4 bg-white rounded-xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-purple-600">C</div>
            <div class="text-xs font-bold text-[#1A1A17]">Veteran</div>
            <div class="text-[11px] font-mono text-[#8F7400]">600 XP</div>
          </div>

          <div class="p-4 bg-white rounded-xl border border-[#E3DFD6] text-center space-y-1 shadow-2xs">
            <div class="font-mono font-bold text-2xl text-amber-600">B / A</div>
            <div class="text-xs font-bold text-[#1A1A17]">Champion</div>
            <div class="text-[11px] font-mono text-[#8F7400]">1,000 XP</div>
          </div>

          <div class="p-4 bg-[#1A1A17] text-[#FFD60A] rounded-xl border-2 border-[#FFD60A] text-center space-y-1 shadow-xs">
            <div class="font-mono font-bold text-2xl text-[#FFD60A]">S</div>
            <div class="text-xs font-bold text-white">Sovereign</div>
            <div class="text-[11px] font-mono text-[#FFD60A]">2,500+ XP</div>
          </div>

        </div>
      </section>

      <!-- FREQUENTLY ASKED QUESTIONS -->
      <section class="space-y-6 text-left border-t border-[#E3DFD6] pt-12">
        <div>
          <div class="text-xs font-mono font-bold text-[#8F7400] uppercase tracking-wider mb-1">Got Questions?</div>
          <h2 class="text-2xl sm:text-3xl font-bold text-[#1A1A17]">Frequently Asked Questions</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">Do I need real Solana to use SolGuild?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              No! SolGuild operates exclusively on <strong>Solana Devnet</strong>. You can connect your Phantom wallet, or generate an instant burner wallet directly in the app. Devnet SOL is free and can be airdropped in one click.
            </p>
          </div>

          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">What happens if my quest evidence is rejected?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              The app shows the rejection explanation from the Gemini Arbiter for 5 seconds. The quest is marked "Failed 1x" and returned to the Guild Board so another adventurer can fulfill it, while the reward stays securely locked in escrow.
            </p>
          </div>

          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">Why does Sensitive Intel require a full letter?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              Discreet reconnaissance contracts require context (origin source, background details, witness quotes). A standalone image does not provide sufficient proof of intel gathering.
            </p>
          </div>

          <div class="p-5 bg-white rounded-2xl border border-[#E3DFD6] space-y-2">
            <h4 class="font-bold text-[15px] text-[#1A1A17]">Can I cancel a quest I posted and get my SOL back?</h4>
            <p class="text-xs sm:text-sm text-[#5E5B53] leading-relaxed">
              Yes. If a quest has not yet been claimed or completed, the original poster can trigger an on-chain refund from their Guild License to reclaim their locked SOL from escrow.
            </p>
          </div>

        </div>
      </section>

      <!-- FINAL CALL TO ACTION BANNER -->
      <section class="p-8 sm:p-12 bg-[#1A1A17] text-white rounded-3xl text-center space-y-6 shadow-xl relative overflow-hidden">
        <div class="max-w-2xl mx-auto space-y-3">
          <span class="inline-block px-3 py-1 rounded-full text-xs font-mono font-semibold bg-[#FFD60A]/20 text-[#FFD60A] border border-[#FFD60A]/40">
            Open Guild Dispatch
          </span>
          <h2 class="text-2xl sm:text-4xl font-bold tracking-tight text-white">
            Ready to claim your first bounty quest?
          </h2>
          <p class="text-sm sm:text-base text-[#E3DFD6] leading-relaxed">
            Join the decentralized adventurer network on Solana Devnet. Solve real-world tasks, earn SOL, and forge your adventurer legacy.
          </p>
        </div>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button 
            @click="$emit('startApp')"
            class="w-full sm:w-auto h-12 px-8 rounded-xl bg-[#FFD60A] text-[#1A1A17] font-bold text-sm hover:brightness-95 active:scale-[0.98] transition-all shadow-md flex items-center justify-center gap-2"
          >
            <span>Open Guild Quest Map</span>
            <span>→</span>
          </button>
          <button 
            @click="$emit('openPostQuest')"
            class="w-full sm:w-auto h-12 px-6 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-sm transition-all border border-white/20 flex items-center justify-center gap-2"
          >
            <span>Post a Bounty</span>
          </button>
        </div>
      </section>

    </main>

    <!-- Clean Footer -->
    <footer class="border-t border-[#E3DFD6] bg-white py-8 text-center text-xs text-[#5E5B53] space-y-2">
      <div class="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <span class="font-bold text-[#1A1A17]">SolGuild</span>
          <span>&middot;</span>
          <span>Solana Devnet Adventurer Protocol</span>
        </div>
        <div class="flex items-center gap-4 text-[#5E5B53]">
          <button @click="$emit('startApp')" class="hover:text-[#1A1A17] transition-colors">Quests</button>
          <button @click="$emit('openPostQuest')" class="hover:text-[#1A1A17] transition-colors">Issue Quest</button>
        </div>
      </div>
    </footer>

  </div>
</template>
