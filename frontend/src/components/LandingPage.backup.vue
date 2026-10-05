<script setup lang="ts">
import {
  Shield,
  FileText,
  Camera,
  ArrowRight,
  Lock,
  AlertTriangle,
  MapPin
} from 'lucide-vue-next'

defineEmits<{
  (e: 'startApp'): void
  (e: 'openPostQuest'): void
}>()
</script>

<template>
  <div class="min-h-dvh bg-[#F7F5F0] text-[#1A1A17] flex flex-col justify-between selection:bg-[#FFD60A] selection:text-[#1A1A17] font-['Poppins',Arial,sans-serif]">
    
    <!-- NAVBAR -->
    <header class="sticky top-0 z-40 bg-[#F7F5F0]/95 backdrop-blur-md border-b-2 border-[#1A1A17]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        
        <!-- Logo & Wordmark -->
        <div class="flex items-center gap-3 cursor-pointer" @click="$emit('startApp')">
          <img 
            src="/guild-logo.jpg" 
            alt="SolGuild Sun Shield Logo" 
            class="w-10 h-10 rounded-full border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] object-cover"
          />
          <div class="flex items-center gap-2">
            <span class="font-extrabold text-[19px] tracking-tight">SolGuild</span>
            <span class="text-[11px] font-bold px-2 py-0.5 rounded border border-[#1A1A17] bg-[#FFD60A] text-[#1A1A17] shadow-[1px_1px_0px_#1A1A17]">
              DEVNET
            </span>
          </div>
        </div>

        <!-- Desktop Navigation Links -->
        <nav class="hidden md:flex items-center gap-7 text-[13px] font-semibold text-[#1A1A17]">
          <a href="#why-what" class="hover:underline underline-offset-4 decoration-2">Why & What</a>
          <a href="#about-boards" class="hover:underline underline-offset-4 decoration-2">Guild Boards</a>
          <a href="#how-it-works" class="hover:underline underline-offset-4 decoration-2">How It Works</a>
          <a href="#workflow" class="hover:underline underline-offset-4 decoration-2">Workflow</a>
          <a href="#ranks" class="hover:underline underline-offset-4 decoration-2">Ranks</a>
          <a href="#faq" class="hover:underline underline-offset-4 decoration-2">FAQ</a>
        </nav>

        <!-- Navbar Actions -->
        <div class="flex items-center gap-3">
          <button 
            @click="$emit('startApp')"
            class="hidden sm:inline-flex text-[13px] font-bold text-[#1A1A17] hover:underline underline-offset-4"
          >
            Audit Log
          </button>
          <button 
            @click="$emit('startApp')"
            class="h-10 px-5 rounded-lg bg-[#FFD60A] border-2 border-[#1A1A17] text-[#1A1A17] font-bold text-[13px] shadow-[3px_3px_0px_#1A1A17] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_#1A1A17] active:translate-x-[3px] active:translate-y-[3px] active:shadow-none transition-all flex items-center gap-2 cursor-pointer"
          >
            <span>Enter Guild Board</span>
            <ArrowRight class="w-4 h-4" />
          </button>
        </div>

      </div>
    </header>

    <!-- MAIN BODY -->
    <main class="max-w-6xl mx-auto w-full px-4 sm:px-6 py-10 sm:py-16 space-y-20 sm:space-y-28">
      
      <!-- HERO SECTION: WHY & WHAT (Exact 2-Column Split inspired by reference image) -->
      <section id="why-what" class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center text-left">
        
        <!-- Left: Why & What Product Explanation -->
        <div class="lg:col-span-6 space-y-6">
          
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded border-2 border-[#1A1A17] bg-[#FFD60A] text-[#1A1A17] font-bold text-[12px] shadow-[2px_2px_0px_#1A1A17]">
            <MapPin class="w-3.5 h-3.5" />
            <span>Active across 8 European cities on Solana Devnet</span>
          </div>

          <h1 class="text-3xl sm:text-4xl md:text-5xl font-black text-[#1A1A17] leading-[1.15] tracking-tight">
            The adventurer guild for real life. <br />
            <span class="inline-block bg-[#FFD60A] px-2 py-0.5 border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] mt-1">
              Post a quest, get paid for proof.
            </span>
          </h1>

          <!-- The "Why & What" from README.md -->
          <div class="space-y-3 text-[15px] sm:text-[16px] text-[#1A1A17] leading-relaxed">
            <p>
              <strong>The Problem:</strong> Small jobs in the real world are hard to hand off to strangers. You either trust someone blindly and pay first, or the helper does the work and hopes they get paid after. Someone always has to risk getting burned.
            </p>
            <p>
              <strong>The Solution:</strong> SolGuild eliminates the trust dilemma. The quest creator locks the reward upfront in Solana escrow. A nearby helper accepts the job and submits photo proof from the exact spot. Our multimodal AI verifier checks the proof, and the reward is released automatically.
            </p>
          </div>

          <!-- Dual Call to Action Buttons -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-2">
            <button 
              @click="$emit('startApp')"
              class="h-12 px-7 rounded-lg bg-[#FFD60A] border-2 border-[#1A1A17] text-[#1A1A17] font-extrabold text-[15px] shadow-[4px_4px_0px_#1A1A17] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[3px_3px_0px_#1A1A17] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>Explore Active Quests</span>
              <ArrowRight class="w-4 h-4" />
            </button>
            <button 
              @click="$emit('openPostQuest')"
              class="h-12 px-7 rounded-lg bg-[#FAF8F5] border-2 border-[#1A1A17] text-[#1A1A17] font-bold text-[15px] shadow-[4px_4px_0px_#1A1A17] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[3px_3px_0px_#1A1A17] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>Issue a Quest</span>
              <span class="text-xs font-mono text-[#5E5B53]">+0.01 SOL min</span>
            </button>
          </div>

          <div class="text-[12px] font-semibold text-[#5E5B53] pt-1">
            Zero platform fees on Devnet &middot; Instant faucet top-up included
          </div>

        </div>

        <!-- Right: Generated Guild Quest Card Graphic -->
        <div class="lg:col-span-6 flex justify-center">
          <div class="w-full max-w-md bg-[#FAF8F5] rounded-2xl border-2 border-[#1A1A17] shadow-[6px_6px_0px_#1A1A17] p-3 overflow-hidden">
            <img 
              src="/hero-quest-card.jpg" 
              alt="Authentic Adventurer Guild Quest Card Dispatch" 
              class="w-full h-auto rounded-xl border border-[#1A1A17]"
            />
            <div class="p-3 text-left space-y-1">
              <div class="flex items-center justify-between text-xs font-bold">
                <span>Solana Devnet Smart Contract Vault</span>
                <span class="bg-[#FFD60A] px-2 py-0.5 rounded border border-[#1A1A17]">100% Locked</span>
              </div>
              <p class="text-[12px] text-[#5E5B53]">
                Every quest deposit is an autonomous on-chain escrow lock. Payouts require verified photographic proof.
              </p>
            </div>
          </div>
        </div>

      </section>

      <!-- REGION & CITIES BAND -->
      <section class="border-y-2 border-[#1A1A17] py-6 bg-[#FAF8F5] text-center space-y-3">
        <div class="text-xs font-black uppercase tracking-wider text-[#1A1A17]">
          8 European Metropolitan Hubs &middot; 88 Starter Quests
        </div>
        <div class="flex flex-wrap items-center justify-center gap-2 sm:gap-3 text-xs sm:text-sm font-bold text-[#1A1A17]">
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">Berlin</span>
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">London</span>
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">Paris</span>
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">Madrid</span>
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">Rome</span>
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">Amsterdam</span>
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">Barcelona</span>
          <span class="px-3 py-1 rounded bg-[#F7F5F0] border border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">Vienna</span>
        </div>
      </section>

      <!-- ABOUT SECTION: DETAILED WHAT (The 3 Guild Boards from README) -->
      <section id="about-boards" class="space-y-8 text-left">
        
        <div class="space-y-2 max-w-2xl">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[#5E5B53]">About the Platform</div>
          <h2 class="text-2xl sm:text-3xl md:text-4xl font-black text-[#1A1A17] tracking-tight">
            The Three Guild Boards
          </h2>
          <p class="text-sm sm:text-base text-[#1A1A17] leading-relaxed">
            Every quest belongs to one of three boards. Each board has its own strict rules for what counts as acceptable proof before funds are released.
          </p>
        </div>

        <!-- 3 Board Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <!-- Board 1: Civil Help -->
          <div class="p-6 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-4 flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-lg bg-[#FFD60A] border-2 border-[#1A1A17] flex items-center justify-center font-bold text-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">
                <Shield class="w-5 h-5" />
              </div>
              <h3 class="font-extrabold text-[18px] text-[#1A1A17]">1. Civil Help</h3>
              <div class="text-xs font-bold text-[#5E5B53] uppercase">Everyday Local Assistance</div>
              <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
                Finding lost pets, recovering misplaced keys, checking venue queues, or safely driving home the car of an intoxicated friend.
              </p>
            </div>
            <div class="pt-3 border-t border-[#1A1A17]/30 text-xs font-bold space-y-1">
              <div class="text-[#1A1A17]">Required Evidence:</div>
              <div class="bg-[#F7F5F0] p-2 rounded border border-[#1A1A17] font-mono text-[11px]">
                One clear photo at the location + device GPS within 150m
              </div>
            </div>
          </div>

          <!-- Board 2: Sensitive -->
          <div class="p-6 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-4 flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-lg bg-[#FFD60A] border-2 border-[#1A1A17] flex items-center justify-center font-bold text-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">
                <FileText class="w-5 h-5" />
              </div>
              <h3 class="font-extrabold text-[18px] text-[#1A1A17]">2. Sensitive</h3>
              <div class="text-xs font-bold text-[#5E5B53] uppercase">Careful, Serious Field Work</div>
              <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
                Confirming vehicle ownership at a depot, tracing historical plaque origins, or discreet documentation of landmarks.
              </p>
            </div>
            <div class="pt-3 border-t border-[#1A1A17]/30 text-xs font-bold space-y-1">
              <div class="text-[#1A1A17]">Required Evidence:</div>
              <div class="bg-[#F7F5F0] p-2 rounded border border-[#1A1A17] font-mono text-[11px]">
                Photo + written investigation report (35+ chars) + declared intel source
              </div>
            </div>
          </div>

          <!-- Board 3: Commercial -->
          <div class="p-6 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-4 flex flex-col justify-between">
            <div class="space-y-3">
              <div class="w-10 h-10 rounded-lg bg-[#FFD60A] border-2 border-[#1A1A17] flex items-center justify-center font-bold text-[#1A1A17] shadow-[2px_2px_0px_#1A1A17]">
                <Camera class="w-5 h-5" />
              </div>
              <h3 class="font-extrabold text-[18px] text-[#1A1A17]">3. Commercial</h3>
              <div class="text-xs font-bold text-[#5E5B53] uppercase">Content & Product Verification</div>
              <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
                Filming a short promotion for a local bakery, photographing an item on a real shop shelf, or checking billboard installations.
              </p>
            </div>
            <div class="pt-3 border-t border-[#1A1A17]/30 text-xs font-bold space-y-1">
              <div class="text-[#1A1A17]">Required Evidence:</div>
              <div class="bg-[#F7F5F0] p-2 rounded border border-[#1A1A17] font-mono text-[11px]">
                Product showcase photo or short video clip at the storefront
              </div>
            </div>
          </div>

        </div>

        <!-- Failure & Locked Escrow Retention Policy Banner -->
        <div class="p-5 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[3px_3px_0px_#1A1A17] space-y-2">
          <div class="flex items-center gap-2 font-black text-sm">
            <Lock class="w-4 h-4 text-[#1A1A17]" />
            <span>Zero-Drain Protocol: What Happens When a Submission Fails</span>
          </div>
          <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
            If a helper's proof is rejected, <strong>the reward does NOT get refunded to arbitrary wallets</strong>. It stays securely locked in the guild escrow vault. The quest automatically returns to the open board marked <strong>"Failed 1x"</strong> so the next adventurer can try. The original poster can also trigger a full on-chain refund from their license at any time.
          </p>
        </div>

      </section>

      <!-- FEATURES SECTION: HOW IT WORKS (The 3 Verification Gates from README) -->
      <section id="how-it-works" class="space-y-8 text-left">
        
        <div class="space-y-2 max-w-2xl">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[#5E5B53]">Features & Architecture</div>
          <h2 class="text-2xl sm:text-3xl md:text-4xl font-black text-[#1A1A17] tracking-tight">
            How Proof Is Checked: The 3 Gates
          </h2>
          <p class="text-sm sm:text-base text-[#1A1A17]">
            Every submission passes through three automated gates in strict order. If it fails one gate, evaluation stops immediately.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div class="p-6 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-3">
            <div class="w-8 h-8 rounded bg-[#FFD60A] border-2 border-[#1A1A17] flex items-center justify-center font-black text-sm">
              1
            </div>
            <h4 class="font-bold text-[16px] text-[#1A1A17]">Gate 1: Intake & Integrity</h4>
            <div class="text-xs font-semibold text-[#5E5B53]">Is this a real image file?</div>
            <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
              Validates image format, prevents corrupted uploads, and calculates a SHA-256 fingerprint so duplicate photos cannot be reused.
            </p>
          </div>

          <div class="p-6 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-3">
            <div class="w-8 h-8 rounded bg-[#FFD60A] border-2 border-[#1A1A17] flex items-center justify-center font-black text-sm">
              2
            </div>
            <h4 class="font-bold text-[16px] text-[#1A1A17]">Gate 2: Location Proximity</h4>
            <div class="text-xs font-semibold text-[#5E5B53]">Were you actually there?</div>
            <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
              Reads GPS coordinates from device telemetry and compares distance to the quest pin. Submissions must be within <strong>150 metres</strong>.
            </p>
          </div>

          <div class="p-6 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-3">
            <div class="w-8 h-8 rounded bg-[#FFD60A] border-2 border-[#1A1A17] flex items-center justify-center font-black text-sm">
              3
            </div>
            <h4 class="font-bold text-[16px] text-[#1A1A17]">Gate 3: Multimodal Vision</h4>
            <div class="text-xs font-semibold text-[#5E5B53]">Is it the right scene?</div>
            <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
              <strong>Gemini 3.1 Flash-Lite</strong> evaluates the photo against the quest requirements. Rejecting screenshots and mismatched objects in under 3 seconds.
            </p>
          </div>

        </div>

      </section>

      <!-- WORKFLOW BENTO GRID (User mandate: Bento grid of workflow) -->
      <section id="workflow" class="space-y-8 text-left">
        
        <div class="space-y-2">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[#5E5B53]">Lifecycle Architecture</div>
          <h2 class="text-2xl sm:text-3xl md:text-4xl font-black text-[#1A1A17] tracking-tight">
            The 4-Step Quest Workflow
          </h2>
          <p class="text-sm sm:text-base text-[#1A1A17]">
            How a quest moves from creation to on-chain settlement.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-6">
          
          <!-- Bento Card 1: Wide (7 cols) -->
          <div class="md:col-span-7 bg-[#FAF8F5] p-7 rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-3 flex flex-col justify-between">
            <div class="space-y-2">
              <span class="inline-block px-2 py-0.5 rounded bg-[#FFD60A] border border-[#1A1A17] font-black text-xs">
                STEP 01
              </span>
              <h3 class="text-xl font-black text-[#1A1A17]">Write Quest & Lock Bounty</h3>
              <p class="text-sm text-[#1A1A17] leading-relaxed">
                The quest issuer picks a spot on the European map, writes the instruction, and deposits SOL into the escrow vault via their Phantom wallet.
              </p>
            </div>
            <div class="p-3 bg-[#F7F5F0] rounded border border-[#1A1A17] flex justify-between items-center text-xs font-mono">
              <span>On-Chain Deposit Verified</span>
              <span class="font-bold">Solana Explorer Signature</span>
            </div>
          </div>

          <!-- Bento Card 2: (5 cols) -->
          <div class="md:col-span-5 bg-[#FAF8F5] p-7 rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-3 flex flex-col justify-between">
            <div class="space-y-2">
              <span class="inline-block px-2 py-0.5 rounded bg-[#FFD60A] border border-[#1A1A17] font-black text-xs">
                STEP 02
              </span>
              <h3 class="text-xl font-black text-[#1A1A17]">10-Minute Lock</h3>
              <p class="text-sm text-[#1A1A17] leading-relaxed">
                An adventurer near the location claims the quest. A 10-minute timer starts to ensure no race conditions between helpers.
              </p>
            </div>
            <div class="p-3 bg-[#F7F5F0] rounded border border-[#1A1A17] flex justify-between items-center text-xs font-mono">
              <span>Exclusive Window</span>
              <span class="font-bold">10:00 Countdown</span>
            </div>
          </div>

          <!-- Bento Card 3: (5 cols) -->
          <div class="md:col-span-5 bg-[#FAF8F5] p-7 rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-3 flex flex-col justify-between">
            <div class="space-y-2">
              <span class="inline-block px-2 py-0.5 rounded bg-[#FFD60A] border border-[#1A1A17] font-black text-xs">
                STEP 03
              </span>
              <h3 class="text-xl font-black text-[#1A1A17]">Capture & Verify</h3>
              <p class="text-sm text-[#1A1A17] leading-relaxed">
                The helper photographs the target and uploads proof. The verifier checks GPS coordinates, scene match, and letter details in under 3 seconds.
              </p>
            </div>
            <div class="p-3 bg-[#F7F5F0] rounded border border-[#1A1A17] flex justify-between items-center text-xs font-mono">
              <span>Gemini 3.1 Flash-Lite</span>
              <span class="font-bold">&lt; 3s Verdict</span>
            </div>
          </div>

          <!-- Bento Card 4: Wide (7 cols) -->
          <div class="md:col-span-7 bg-[#FAF8F5] p-7 rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] space-y-3 flex flex-col justify-between">
            <div class="space-y-2">
              <span class="inline-block px-2 py-0.5 rounded bg-[#FFD60A] border border-[#1A1A17] font-black text-xs">
                STEP 04
              </span>
              <h3 class="text-xl font-black text-[#1A1A17]">Instant Payout or Safe Re-Open</h3>
              <p class="text-sm text-[#1A1A17] leading-relaxed">
                If valid, escrow automatically transfers the SOL bounty to the helper's wallet + 50 EXP. If rejected, funds remain locked and the quest re-opens as <strong>Failed 1x</strong>.
              </p>
            </div>
            <div class="p-3 bg-[#F7F5F0] rounded border border-[#1A1A17] flex justify-between items-center text-xs font-mono">
              <span>Automatic Settlement</span>
              <span class="font-bold">+50 EXP Awarded</span>
            </div>
          </div>

        </div>

      </section>

      <!-- BIG MVP DISCLAIMER (Word for word from README) -->
      <section class="p-6 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] text-left space-y-3">
        <div class="flex items-center gap-2">
          <AlertTriangle class="w-5 h-5 text-[#1A1A17]" />
          <h3 class="font-black text-[16px] text-[#1A1A17]">
            BIG NOTE: This is an MVP, and it has NO anti-AI-image detection
          </h3>
        </div>
        <p class="text-[13px] sm:text-[14px] text-[#1A1A17] leading-relaxed">
          <strong>SolGuild cannot currently tell a real photo from an AI-generated one.</strong> The verifier checks the place (GPS) and whether the photo matches the quest, and it tries to spot screenshots and photos of screens. It does <strong>not</strong> have a dedicated detector for images made by generative AI.
        </p>
        <p class="text-[13px] text-[#5E5B53] leading-relaxed">
          Until AI-image detection exists, this system cannot be considered proven to work in the real world. Everything here runs on Devnet with test SOL for exactly this reason. For hackathon testing, feel free to submit mock or AI images to test the payout pipeline!
        </p>
      </section>

      <!-- GUILD RANKS & EXPERIENCE SECTION -->
      <section id="ranks" class="space-y-6 text-left">
        
        <div class="space-y-2">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[#5E5B53]">Progression Ladder</div>
          <h2 class="text-2xl sm:text-3xl font-black text-[#1A1A17] tracking-tight">
            Guild Ranks & Experience
          </h2>
          <p class="text-sm text-[#1A1A17]">
            Every completed quest gives the helper <strong>50 EXP</strong>. EXP climbs a rank ladder, just like in the stories.
          </p>
        </div>

        <!-- Generated Ranks Graphic Banner -->
        <div class="bg-[#FAF8F5] p-3 rounded-2xl border-2 border-[#1A1A17] shadow-[4px_4px_0px_#1A1A17] overflow-hidden">
          <img 
            src="/guild-rank-ladder.jpg" 
            alt="Adventurer Guild Rank Badges F to S" 
            class="w-full h-auto rounded-xl border border-[#1A1A17]"
          />
        </div>

        <!-- Rank Stats Breakdown -->
        <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3 text-center">
          <div class="p-3 bg-[#FAF8F5] rounded border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] space-y-0.5">
            <div class="font-mono font-black text-xl text-[#1A1A17]">F</div>
            <div class="text-xs font-bold">Novice</div>
            <div class="text-[11px] font-mono text-[#5E5B53]">0 EXP</div>
          </div>
          <div class="p-3 bg-[#FAF8F5] rounded border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] space-y-0.5">
            <div class="font-mono font-black text-xl text-[#1A1A17]">E</div>
            <div class="text-xs font-bold">Apprentice</div>
            <div class="text-[11px] font-mono text-[#5E5B53]">100 EXP</div>
          </div>
          <div class="p-3 bg-[#FAF8F5] rounded border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] space-y-0.5">
            <div class="font-mono font-black text-xl text-[#1A1A17]">D</div>
            <div class="text-xs font-bold">Proven</div>
            <div class="text-[11px] font-mono text-[#5E5B53]">300 EXP</div>
          </div>
          <div class="p-3 bg-[#FAF8F5] rounded border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] space-y-0.5">
            <div class="font-mono font-black text-xl text-[#1A1A17]">C</div>
            <div class="text-xs font-bold">Skilled</div>
            <div class="text-[11px] font-mono text-[#5E5B53]">600 EXP</div>
          </div>
          <div class="p-3 bg-[#FAF8F5] rounded border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] space-y-0.5">
            <div class="font-mono font-black text-xl text-[#1A1A17]">B</div>
            <div class="text-xs font-bold">Veteran</div>
            <div class="text-[11px] font-mono text-[#5E5B53]">1,000 EXP</div>
          </div>
          <div class="p-3 bg-[#FAF8F5] rounded border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] space-y-0.5">
            <div class="font-mono font-black text-xl text-[#1A1A17]">A</div>
            <div class="text-xs font-bold">Elite</div>
            <div class="text-[11px] font-mono text-[#5E5B53]">1,600 EXP</div>
          </div>
          <div class="p-3 bg-[#FFD60A] rounded border-2 border-[#1A1A17] shadow-[2px_2px_0px_#1A1A17] space-y-0.5">
            <div class="font-mono font-black text-xl text-[#1A1A17]">S</div>
            <div class="text-xs font-bold">Grandmaster</div>
            <div class="text-[11px] font-mono text-[#1A1A17]">2,500+ EXP</div>
          </div>
        </div>

      </section>

      <!-- FAQ SECTION -->
      <section id="faq" class="space-y-6 text-left border-t-2 border-[#1A1A17] pt-12">
        
        <div class="space-y-2">
          <div class="text-xs font-mono font-bold uppercase tracking-wider text-[#5E5B53]">Help & Clarifications</div>
          <h2 class="text-2xl sm:text-3xl font-black text-[#1A1A17]">Frequently Asked Questions</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <div class="p-5 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[3px_3px_0px_#1A1A17] space-y-2">
            <h4 class="font-extrabold text-[15px] text-[#1A1A17]">Do I need real Solana to use SolGuild?</h4>
            <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
              No. SolGuild runs entirely on Solana Devnet. You can connect your Phantom wallet or generate an instant browser burner wallet. Devnet SOL is free and topped up with one click.
            </p>
          </div>

          <div class="p-5 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[3px_3px_0px_#1A1A17] space-y-2">
            <h4 class="font-extrabold text-[15px] text-[#1A1A17]">What happens if photo verification fails?</h4>
            <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
              The failure reason is shown on screen for 5 seconds. The bounty stays safely locked in escrow, and the quest returns to the open board marked <strong>Failed 1x</strong> for another adventurer.
            </p>
          </div>

          <div class="p-5 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[3px_3px_0px_#1A1A17] space-y-2">
            <h4 class="font-extrabold text-[15px] text-[#1A1A17]">Why do Sensitive quests ask for a letter?</h4>
            <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
              A photo alone is not enough proof for sensitive work. The helper also writes a brief field report (at least 35 characters) and states where the information came from (visual sighting, witness, or municipal record).
            </p>
          </div>

          <div class="p-5 bg-[#FAF8F5] rounded-xl border-2 border-[#1A1A17] shadow-[3px_3px_0px_#1A1A17] space-y-2">
            <h4 class="font-extrabold text-[15px] text-[#1A1A17]">Can an issuer cancel and refund their bounty?</h4>
            <p class="text-xs sm:text-sm text-[#1A1A17] leading-relaxed">
              Yes. If a quest has not yet been claimed or successfully completed, the original poster can trigger an on-chain refund from their Guild License to reclaim their locked SOL from escrow.
            </p>
          </div>

        </div>

      </section>

      <!-- CTA SECTION: ENCOURAGEMENT TO USE (Do small tasks, get paid safely) -->
      <section class="p-8 sm:p-14 bg-[#FAF8F5] rounded-2xl border-2 border-[#1A1A17] shadow-[6px_6px_0px_#1A1A17] text-center space-y-6">
        
        <div class="max-w-2xl mx-auto space-y-3">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded bg-[#FFD60A] border-2 border-[#1A1A17] font-black text-xs shadow-[2px_2px_0px_#1A1A17]">
            Ready to Start?
          </div>
          <h2 class="text-3xl sm:text-4xl md:text-5xl font-black text-[#1A1A17] tracking-tight">
            Take on real tasks. Get paid for proof.
          </h2>
          <p class="text-sm sm:text-base text-[#1A1A17] leading-relaxed max-w-lg mx-auto">
            Do small everyday jobs in your city, submit genuine photo proof, and receive your reward automatically in SOL without trusting strangers.
          </p>
        </div>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <button 
            @click="$emit('startApp')"
            class="h-12 px-8 rounded-lg bg-[#FFD60A] border-2 border-[#1A1A17] text-[#1A1A17] font-extrabold text-[15px] shadow-[4px_4px_0px_#1A1A17] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[3px_3px_0px_#1A1A17] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            <span>Open Guild Quest Map</span>
            <ArrowRight class="w-4 h-4" />
          </button>
          <button 
            @click="$emit('openPostQuest')"
            class="h-12 px-7 rounded-lg bg-[#F7F5F0] border-2 border-[#1A1A17] text-[#1A1A17] font-bold text-[15px] shadow-[4px_4px_0px_#1A1A17] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[3px_3px_0px_#1A1A17] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none transition-all flex items-center justify-center gap-2 cursor-pointer"
          >
            <span>Post a Bounty Quest</span>
          </button>
        </div>

      </section>

    </main>

    <!-- FOOTER -->
    <footer class="border-t-2 border-[#1A1A17] bg-[#FAF8F5] py-8 text-xs font-semibold text-[#1A1A17]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2.5">
          <img 
            src="/guild-logo.jpg" 
            alt="SolGuild Logo" 
            class="w-7 h-7 rounded-full border border-[#1A1A17]"
          />
          <span class="font-bold">SolGuild</span>
          <span>&middot;</span>
          <span>Real-world adventurer guild on Solana Devnet</span>
        </div>
        <div class="flex items-center gap-5">
          <button @click="$emit('startApp')" class="hover:underline">Quests</button>
          <button @click="$emit('openPostQuest')" class="hover:underline">Issue a Quest</button>
          <a href="#about-boards" class="hover:underline">Boards</a>
          <a href="#how-it-works" class="hover:underline">Verification</a>
          <a href="#workflow" class="hover:underline">Workflow</a>
        </div>
      </div>
    </footer>

  </div>
</template>
