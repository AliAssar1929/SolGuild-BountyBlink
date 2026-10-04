<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useWallet } from './composables/useWallet'
import {
  MapPin,
  Camera,
  Coins,
  ArrowRight,
  RefreshCw,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  Clock,
  Layers,
  Sparkles,
  Zap,
  Cpu,
  ChevronRight,
  Shield,
  Eye,
  Check
} from 'lucide-vue-next'

const { publicKey, balance, initWallet } = useWallet()

interface Task {
  id: string
  title: string
  instruction: string
  target_description: string
  latitude: number
  longitude: number
  reward_sol: number
  poster_address: string
  status: string
  fund_tx_sig?: string
  payout_tx_sig?: string
  refund_tx_sig?: string
}

const activeTab = ref<'do' | 'post'>('do')
const tasks = ref<Task[]>([])
const selectedTask = ref<Task | null>(null)
const loading = ref(false)

// Verification Stepper State
const isSubmitting = ref(false)
const verificationResult = ref<any>(null)
const currentStep = ref<number>(0)

// Post Task Form State
const postTitle = ref('')
const postInstruction = ref('')
const postTarget = ref('')
const postLat = ref(52.5200)
const postLon = ref(13.4050)
const postCreatedResult = ref<any>(null)

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/tasks')
    tasks.value = await res.json()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const selectTask = (task: Task) => {
  selectedTask.value = task
  verificationResult.value = null
  currentStep.value = 0
}

const claimTask = async () => {
  if (!selectedTask.value) return
  loading.value = true
  try {
    const res = await fetch(`/api/tasks/${selectedTask.value.id}/claim`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ worker_address: publicKey.value })
    })
    const data = await res.json()
    if (res.ok) {
      selectedTask.value.status = 'CLAIMED'
    } else {
      alert(data.detail || 'Could not claim task')
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const submitEvidence = async (fixtureType?: 'VALID' | 'FAKE', file?: File) => {
  if (!selectedTask.value) return
  isSubmitting.value = true
  currentStep.value = 1

  const formData = new FormData()
  formData.append('worker_address', publicKey.value)
  if (fixtureType) formData.append('fixture_type', fixtureType)
  if (file) formData.append('photo', file)

  setTimeout(() => { currentStep.value = 2 }, 600)
  setTimeout(() => { currentStep.value = 3 }, 1200)

  try {
    const res = await fetch(`/api/tasks/${selectedTask.value.id}/submit`, {
      method: 'POST',
      body: formData
    })
    const data = await res.json()
    setTimeout(() => {
      currentStep.value = 4
      verificationResult.value = data
      if (selectedTask.value) {
        selectedTask.value.status = data.status
        selectedTask.value.payout_tx_sig = data.payout_tx_sig
      }
      isSubmitting.value = false
      fetchTasks()
    }, 1800)
  } catch (err) {
    console.error(err)
    isSubmitting.value = false
  }
}

const triggerRefund = async () => {
  if (!selectedTask.value) return
  loading.value = true
  try {
    const res = await fetch(`/api/tasks/${selectedTask.value.id}/refund`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ poster_address: selectedTask.value.poster_address })
    })
    const data = await res.json()
    if (res.ok) {
      selectedTask.value.status = 'REFUNDED'
      selectedTask.value.refund_tx_sig = data.refund_tx_sig
      fetchTasks()
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleFileUpload = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    submitEvidence(undefined, target.files[0])
  }
}

const resetDemo = async () => {
  loading.value = true
  try {
    await fetch('/api/demo/reset', { method: 'POST' })
    selectedTask.value = null
    verificationResult.value = null
    fetchTasks()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const applyPreset = (title: string, inst: string, target: string) => {
  postTitle.value = title
  postInstruction.value = inst
  postTarget.value = target
}

const createBounty = async () => {
  if (!postTitle.value || !postInstruction.value) return
  loading.value = true
  try {
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: postTitle.value,
        instruction: postInstruction.value,
        target_description: postTarget.value || postTitle.value,
        latitude: postLat.value,
        longitude: postLon.value,
        reward_sol: 0.01,
        poster_address: publicKey.value
      })
    })
    const data = await res.json()
    postCreatedResult.value = data
    fetchTasks()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  initWallet()
  fetchTasks()
})
</script>

<template>
  <div class="min-h-screen bg-[#08090D] bg-grid-pattern text-slate-100 flex flex-col items-center justify-start selection:bg-purple-600 selection:text-white">
    
    <!-- Top Modern Web3 Navigation Bar -->
    <header class="w-full border-b border-slate-800/80 bg-[#0C0E14]/90 backdrop-blur-md sticky top-0 z-40 px-4 py-3">
      <div class="max-w-6xl mx-auto flex items-center justify-between">
        
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 via-indigo-500 to-teal-400 p-[1px] shadow-lg shadow-purple-500/20">
            <div class="w-full h-full bg-[#0E1017] rounded-[11px] flex items-center justify-center">
              <Zap class="w-5 h-5 text-teal-400" />
            </div>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">BountyBlink</span>
              <span class="px-2 py-0.5 text-[10px] font-mono font-bold tracking-wider uppercase rounded-full bg-purple-500/10 text-purple-400 border border-purple-500/30">
                Solana Devnet
              </span>
            </div>
            <p class="text-[11px] text-slate-400 font-mono hidden sm:block">AI-to-Human Physical Task Escrow</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <!-- Ephemeral Wallet Status Chip -->
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#141722] border border-slate-800 text-xs shadow-inner">
            <div class="w-2 h-2 rounded-full bg-teal-400 shadow-[0_0_8px_#14F195]"></div>
            <span class="font-mono text-slate-300 hidden md:inline">{{ publicKey.slice(0, 4) }}...{{ publicKey.slice(-4) }}</span>
            <span class="text-slate-600 hidden md:inline">|</span>
            <div class="flex items-center gap-1 font-mono font-bold text-teal-300">
              <Coins class="w-3.5 h-3.5 text-purple-400" />
              <span>{{ balance.toFixed(2) }} SOL</span>
            </div>
          </div>

          <button 
            @click="resetDemo"
            class="px-3 py-1.5 rounded-lg bg-[#141722] hover:bg-[#1A1E2C] border border-slate-800 text-xs font-mono text-slate-300 hover:text-white transition-all flex items-center gap-1.5 shadow-sm active:scale-95"
            title="Reset to default seed bounties"
          >
            <RefreshCw class="w-3.5 h-3.5 text-purple-400" :class="loading ? 'animate-spin' : ''" />
            <span class="hidden sm:inline">Reset</span>
          </button>
        </div>

      </div>
    </header>

    <!-- Main Container Layout (Modern Desktop Responsive View with Centered Focus) -->
    <main class="w-full max-w-4xl px-4 py-6 md:py-8 flex flex-col items-center flex-1">
      
      <!-- Segmented Tab Navigation Bar (Magic UI Glass Pill) -->
      <div class="p-1 rounded-2xl bg-[#11131B] border border-slate-800/90 flex gap-1 shadow-2xl mb-6 w-full max-w-md">
        <button 
          @click="activeTab = 'do'"
          class="flex-1 py-2.5 px-4 rounded-xl text-xs font-mono font-semibold tracking-wide flex items-center justify-center gap-2 transition-all"
          :class="activeTab === 'do' ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'"
        >
          <Layers class="w-4 h-4" />
          <span>Fulfill Bounties</span>
        </button>

        <button 
          @click="activeTab = 'post'"
          class="flex-1 py-2.5 px-4 rounded-xl text-xs font-mono font-semibold tracking-wide flex items-center justify-center gap-2 transition-all"
          :class="activeTab === 'post' ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-600/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'"
        >
          <Sparkles class="w-4 h-4" />
          <span>Create Bounty</span>
        </button>
      </div>

      <!-- ================= TAB 1: DO TASKS ================= -->
      <section v-if="activeTab === 'do'" class="w-full max-w-2xl space-y-4">
        
        <!-- State A: Task Detail View & Live Verification -->
        <div v-if="selectedTask" class="space-y-4 animate-in fade-in zoom-in-95 duration-200">
          
          <button 
            @click="selectedTask = null" 
            class="text-xs font-mono text-purple-400 hover:text-purple-300 flex items-center gap-1.5 transition-colors"
          >
            ← Return to Bounty Feed
          </button>

          <!-- Magic UI Bento Card for Task -->
          <div class="p-6 rounded-2xl bg-[#11131B] border border-slate-800 shadow-2xl relative overflow-hidden magic-glow">
            
            <div class="flex justify-between items-start border-b border-slate-800/80 pb-4 mb-4">
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-mono uppercase tracking-widest text-slate-500">ID: {{ selectedTask.id.slice(0, 8) }}</span>
                  <span 
                    class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border"
                    :class="{
                      'bg-purple-500/10 border-purple-500/30 text-purple-400': selectedTask.status === 'OPEN',
                      'bg-amber-500/10 border-amber-500/30 text-amber-400': selectedTask.status === 'CLAIMED',
                      'bg-teal-500/10 border-teal-500/30 text-teal-400': selectedTask.status === 'PAID',
                      'bg-rose-500/10 border-rose-500/30 text-rose-400': selectedTask.status === 'REJECTED',
                      'bg-slate-800 border-slate-700 text-slate-400': selectedTask.status === 'REFUNDED'
                    }"
                  >
                    {{ selectedTask.status }}
                  </span>
                </div>
                <h2 class="text-xl font-bold text-white mt-1.5 leading-tight">{{ selectedTask.title }}</h2>
              </div>

              <div class="text-right">
                <span class="text-[10px] font-mono uppercase text-slate-400">Escrow Reward</span>
                <div class="text-xl font-mono font-black text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-emerald-400">
                  {{ selectedTask.reward_sol }} SOL
                </div>
              </div>
            </div>

            <!-- Task Operational Specs -->
            <div class="space-y-3 text-sm text-slate-300">
              <div class="p-3.5 rounded-xl bg-[#161822] border border-slate-800/60">
                <div class="text-xs font-mono text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                  <Shield class="w-3.5 h-3.5 text-indigo-400" />
                  <span>Physical Instruction</span>
                </div>
                <p class="text-slate-200 text-xs leading-relaxed">{{ selectedTask.instruction }}</p>
              </div>

              <div class="p-3.5 rounded-xl bg-[#161822] border border-slate-800/60">
                <div class="text-xs font-mono text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                  <Eye class="w-3.5 h-3.5 text-teal-400" />
                  <span>Target Visual Cues (Gemini Vision)</span>
                </div>
                <p class="text-slate-200 text-xs leading-relaxed">{{ selectedTask.target_description }}</p>
              </div>

              <div class="flex items-center gap-4 text-xs font-mono text-slate-400 pt-1">
                <span class="flex items-center gap-1"><MapPin class="w-3.5 h-3.5 text-purple-400" /> Lat {{ selectedTask.latitude.toFixed(4) }}, Lon {{ selectedTask.longitude.toFixed(4) }}</span>
                <span class="flex items-center gap-1"><Clock class="w-3.5 h-3.5 text-slate-500" /> 10m lock</span>
              </div>
            </div>

            <!-- Claim Button -->
            <div v-if="selectedTask.status === 'OPEN'" class="mt-6">
              <button 
                @click="claimTask"
                class="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-purple-600 via-indigo-600 to-teal-500 hover:from-purple-500 hover:to-teal-400 text-white font-mono font-bold text-sm tracking-wide uppercase transition-all shadow-lg shadow-purple-600/30 flex items-center justify-center gap-2 active:scale-98 shimmer-btn"
              >
                <span>Claim Bounty & Lock Escrow</span>
                <ArrowRight class="w-4 h-4" />
              </button>
            </div>

            <!-- Submission Area: Camera Capture & Presets -->
            <div v-else-if="selectedTask.status === 'CLAIMED' && !isSubmitting && !verificationResult" class="mt-6 space-y-4">
              
              <div class="p-3.5 rounded-xl bg-purple-950/20 border border-purple-500/20 text-xs text-purple-200">
                <p class="font-bold flex items-center gap-1.5 mb-1">
                  <Cpu class="w-3.5 h-3.5 text-teal-400" />
                  Autonomous Verification Ready
                </p>
                <p class="text-purple-300/80 leading-relaxed text-[11px]">
                  Submit evidence using the live camera or test fixtures to verify the physical ground truth on Solana Devnet:
                </p>
              </div>

              <!-- Two Judge Testing Presets (Modernized Web3 Buttons) -->
              <div class="grid grid-cols-2 gap-3">
                <button 
                  @click="submitEvidence('VALID')"
                  class="p-4 rounded-xl bg-[#141A24] border border-teal-500/30 hover:border-teal-400 hover:bg-teal-500/10 transition-all text-left shadow-lg group"
                >
                  <div class="text-[10px] font-mono font-bold uppercase text-teal-400 tracking-wider">Preset Fixture 1</div>
                  <div class="font-bold text-xs text-white group-hover:text-teal-300 mt-0.5">Test: Valid Photo</div>
                  <div class="text-[10px] text-slate-400 mt-1">Passes GPS + Vision ➔ Auto Payout</div>
                </button>

                <button 
                  @click="submitEvidence('FAKE')"
                  class="p-4 rounded-xl bg-[#1C141C] border border-rose-500/30 hover:border-rose-400 hover:bg-rose-500/10 transition-all text-left shadow-lg group"
                >
                  <div class="text-[10px] font-mono font-bold uppercase text-rose-400 tracking-wider">Preset Fixture 2</div>
                  <div class="font-bold text-xs text-white group-hover:text-rose-300 mt-0.5">Test: Fake Photo</div>
                  <div class="text-[10px] text-slate-400 mt-1">Fails Vision ➔ Refund Trigger</div>
                </button>
              </div>

              <!-- Native Camera Upload Card -->
              <label class="w-full py-4 rounded-xl border border-dashed border-slate-700 bg-[#141722]/50 hover:bg-[#141722] hover:border-purple-500 flex flex-col items-center justify-center cursor-pointer transition-all text-xs font-mono text-slate-300 group">
                <Camera class="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform mb-1.5" />
                <span>Snap / Upload Real Photo</span>
                <span class="text-[10px] text-slate-500 mt-0.5">Inspects EXIF GPS + Gemini 2.5 Flash Vision</span>
                <input type="file" accept="image/*" capture="environment" @change="handleFileUpload" class="hidden" />
              </label>

            </div>

            <!-- Live Verification Stepper (Modern Glowing Pipeline) -->
            <div v-if="isSubmitting" class="mt-6 p-5 rounded-xl bg-[#141724] border border-indigo-500/30 space-y-4">
              <div class="font-mono text-xs uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-2 flex items-center justify-between">
                <span class="flex items-center gap-1.5">
                  <Cpu class="w-4 h-4 text-purple-400" />
                  Autonomous Pipeline
                </span>
                <span class="text-teal-400 animate-pulse font-bold">Verifying...</span>
              </div>

              <div class="space-y-3 text-xs font-mono">
                <div class="flex items-center gap-3 transition-colors" :class="currentStep >= 1 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep > 1 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep > 1" class="w-3.5 h-3.5" />
                    <span v-else>1</span>
                  </div>
                  <span>Tier 0: File Intake & Perceptual Hash Integrity</span>
                </div>

                <div class="flex items-center gap-3 transition-colors" :class="currentStep >= 2 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep > 2 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep > 2" class="w-3.5 h-3.5" />
                    <span v-else>2</span>
                  </div>
                  <span>Tier 1: Geofence Validation (Haversine &lt;= 150m)</span>
                </div>

                <div class="flex items-center gap-3 transition-colors" :class="currentStep >= 3 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep > 3 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep > 3" class="w-3.5 h-3.5" />
                    <span v-else>3</span>
                  </div>
                  <span>Tier 2: Gemini 2.5 Flash Multimodal Vision</span>
                </div>

                <div class="flex items-center gap-3 transition-colors" :class="currentStep >= 4 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep >= 4 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep >= 4" class="w-3.5 h-3.5" />
                    <span v-else>4</span>
                  </div>
                  <span>Tier 3: On-Chain Solana Devnet Settlement</span>
                </div>
              </div>
            </div>

            <!-- Verification Final Result Panel -->
            <div v-if="verificationResult" class="mt-6 p-5 rounded-xl border shadow-xl" :class="verificationResult.status === 'PAID' ? 'bg-teal-950/20 border-teal-500/40' : 'bg-rose-950/20 border-rose-500/40'">
              
              <div class="flex items-center gap-2 font-mono text-xs font-bold uppercase mb-2" :class="verificationResult.status === 'PAID' ? 'text-teal-400' : 'text-rose-400'">
                <CheckCircle2 v-if="verificationResult.status === 'PAID'" class="w-5 h-5" />
                <AlertCircle v-else class="w-5 h-5" />
                <span>{{ verificationResult.status === 'PAID' ? 'Settlement Confirmed: Escrow Paid' : 'Verification Rejected' }}</span>
              </div>

              <p class="text-xs text-slate-300 leading-relaxed mb-4">
                {{ verificationResult.verification.reason }}
              </p>

              <!-- Solana Explorer Link -->
              <div v-if="verificationResult.payout_tx_sig" class="p-3 rounded-lg bg-[#0C0E14] border border-slate-800 text-xs font-mono mb-4">
                <span class="text-[10px] text-slate-500 uppercase block">Solana Devnet Signature</span>
                <a 
                  :href="verificationResult.explorer_url" 
                  target="_blank" 
                  class="text-teal-400 hover:text-teal-300 hover:underline flex items-center gap-1.5 font-bold mt-1 break-all"
                >
                  <span>{{ verificationResult.payout_tx_sig.slice(0, 24) }}...</span>
                  <ExternalLink class="w-3.5 h-3.5 shrink-0" />
                </a>
              </div>

              <!-- Refund Button for Rejected Task -->
              <div v-if="verificationResult.status === 'REJECTED' && selectedTask.status !== 'REFUNDED'">
                <button 
                  @click="triggerRefund"
                  class="w-full py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-mono text-xs font-bold uppercase tracking-wider transition-colors shadow-md flex items-center justify-center gap-2"
                >
                  <RefreshCw class="w-3.5 h-3.5 text-rose-400" />
                  <span>Refund Deposit (0.01 SOL) to Poster</span>
                </button>
              </div>

              <div v-if="selectedTask.status === 'REFUNDED'" class="p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-400 flex items-center gap-2">
                <CheckCircle2 class="w-4 h-4 text-slate-500" />
                <span>Escrow refunded back to task creator.</span>
              </div>

            </div>

          </div>

        </div>

        <!-- State B: Modern Web3 Task Feed Grid -->
        <div v-else class="space-y-4">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <span class="font-mono text-xs text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-purple-500"></span>
              Available Physical Bounties ({{ tasks.length }})
            </span>
            <span class="text-[11px] font-mono text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded-full border border-teal-500/20">
              Escrow Guaranteed
            </span>
          </div>

          <!-- Bento Grid of Tasks -->
          <div class="grid grid-cols-1 gap-3.5">
            <div 
              v-for="task in tasks" 
              :key="task.id"
              @click="selectTask(task)"
              class="p-5 rounded-2xl bg-[#11131B] border border-slate-800/90 hover:border-purple-500/50 hover:bg-[#141724] cursor-pointer transition-all shadow-xl hover:shadow-purple-500/10 space-y-3 group relative overflow-hidden"
            >
              <div class="flex justify-between items-start">
                <div class="space-y-1">
                  <div class="flex items-center gap-2">
                    <span class="text-[10px] font-mono uppercase text-slate-500">Task #{{ task.id.slice(0, 6) }}</span>
                    <span 
                      class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full border"
                      :class="{
                        'bg-purple-500/10 border-purple-500/30 text-purple-400': task.status === 'OPEN',
                        'bg-amber-500/10 border-amber-500/30 text-amber-400': task.status === 'CLAIMED',
                        'bg-teal-500/10 border-teal-500/30 text-teal-400': task.status === 'PAID',
                        'bg-rose-500/10 border-rose-500/30 text-rose-400': task.status === 'REJECTED',
                        'bg-slate-800 border-slate-700 text-slate-400': task.status === 'REFUNDED'
                      }"
                    >
                      {{ task.status }}
                    </span>
                  </div>
                  <h3 class="font-bold text-base text-white group-hover:text-purple-300 transition-colors leading-snug">{{ task.title }}</h3>
                </div>

                <div class="text-right shrink-0">
                  <span class="text-[10px] font-mono uppercase text-slate-500 block">Reward</span>
                  <span class="font-mono font-black text-sm text-teal-400">{{ task.reward_sol }} SOL</span>
                </div>
              </div>

              <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed">{{ task.instruction }}</p>

              <div class="flex items-center justify-between pt-2 border-t border-slate-800/80 text-[11px] font-mono text-slate-500">
                <span class="flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-purple-400" /> Lat {{ task.latitude.toFixed(2) }}, Lon {{ task.longitude.toFixed(2) }}</span>
                <span class="flex items-center gap-1 text-slate-400 group-hover:text-teal-400 transition-colors">
                  <span>Inspect</span>
                  <ChevronRight class="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          </div>

        </div>

      </section>

      <!-- ================= TAB 2: POST TASK ================= -->
      <section v-if="activeTab === 'post'" class="w-full max-w-xl space-y-5 animate-in fade-in zoom-in-95 duration-200">
        
        <div class="p-6 rounded-2xl bg-[#11131B] border border-slate-800 shadow-2xl space-y-5 magic-glow">
          
          <div class="border-b border-slate-800/80 pb-3">
            <h2 class="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles class="w-5 h-5 text-purple-400" />
              <span>Deploy Autonomous Physical Bounty</span>
            </h2>
            <p class="text-xs text-slate-400 font-mono mt-0.5">Locks 0.01 SOL into Devnet escrow vault</p>
          </div>

          <!-- Quick Templates -->
          <div class="space-y-2">
            <span class="text-[10px] font-mono uppercase text-slate-400 tracking-wider">Quick Task Templates</span>
            <div class="grid grid-cols-2 gap-2.5">
              <button 
                @click="applyPreset('EV Charger Availability Check', 'Photograph the screen and plug status of Allego charger #3.', 'Operational screen, intact cable connector, no error code')"
                class="p-2.5 rounded-xl border border-slate-800 bg-[#161822] hover:border-purple-500 hover:bg-[#1A1E2C] text-left transition-all text-xs font-mono text-slate-300"
              >
                + EV Station Status
              </button>
              <button 
                @click="applyPreset('Coffee Shop Hours Blackboard', 'Photograph the blackboard near the front door showing Sunday hours.', 'Chalkboard sign with readable opening hours text')"
                class="p-2.5 rounded-xl border border-slate-800 bg-[#161822] hover:border-purple-500 hover:bg-[#1A1E2C] text-left transition-all text-xs font-mono text-slate-300"
              >
                + Shop Open Verification
              </button>
            </div>
          </div>

          <!-- Inputs -->
          <div class="space-y-3.5 text-xs font-mono">
            <div>
              <label class="block text-slate-400 uppercase text-[11px] mb-1">Task Title</label>
              <input 
                v-model="postTitle"
                placeholder="e.g. Verify Alexanderplatz EV Charger" 
                class="w-full px-3.5 py-2.5 rounded-xl bg-[#161822] border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-purple-500 text-xs"
              />
            </div>

            <div>
              <label class="block text-slate-400 uppercase text-[11px] mb-1">Physical Verification Instructions</label>
              <textarea 
                v-model="postInstruction"
                rows="2"
                placeholder="Specific camera angle or physical detail to inspect..." 
                class="w-full px-3.5 py-2.5 rounded-xl bg-[#161822] border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-purple-500 text-xs"
              ></textarea>
            </div>

            <div>
              <label class="block text-slate-400 uppercase text-[11px] mb-1">Target Description (Evaluated by Gemini Vision)</label>
              <input 
                v-model="postTarget"
                placeholder="e.g. Green operational display, undamaged cable" 
                class="w-full px-3.5 py-2.5 rounded-xl bg-[#161822] border border-slate-800 text-white placeholder-slate-600 focus:outline-none focus:border-purple-500 text-xs"
              />
            </div>

            <div class="p-3.5 rounded-xl bg-[#161822] border border-slate-800 flex justify-between items-center">
              <span class="text-slate-400">Escrow Locked Amount</span>
              <span class="font-bold text-teal-400 text-sm">0.01 SOL</span>
            </div>

            <button 
              @click="createBounty"
              class="w-full py-3.5 rounded-xl bg-gradient-to-r from-purple-600 via-indigo-600 to-teal-500 hover:from-purple-500 hover:to-teal-400 text-white font-bold text-sm uppercase tracking-wider transition-all shadow-lg shadow-purple-600/30 flex items-center justify-center gap-2 active:scale-98 shimmer-btn"
            >
              <span>Lock Escrow & Post Bounty</span>
              <ArrowRight class="w-4 h-4" />
            </button>
          </div>

          <!-- Created Result Proof -->
          <div v-if="postCreatedResult" class="p-4 rounded-xl bg-teal-950/20 border border-teal-500/40 text-xs space-y-2">
            <div class="flex items-center gap-2 font-mono font-bold text-teal-400">
              <CheckCircle2 class="w-4 h-4" />
              <span>Bounty Deployed & Escrow Funded</span>
            </div>
            <p class="text-slate-300 text-[11px]">Task is live for nearby workers on Solana Devnet.</p>
            <a 
              :href="postCreatedResult.explorer_url" 
              target="_blank" 
              class="text-teal-400 hover:underline font-mono text-[11px] flex items-center gap-1.5"
            >
              <span>View Escrow Lock: {{ postCreatedResult.fund_tx_sig.slice(0, 20) }}...</span>
              <ExternalLink class="w-3.5 h-3.5" />
            </a>
          </div>

        </div>

      </section>

    </main>
  </div>
</template>
