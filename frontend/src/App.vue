<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useWallet } from './composables/useWallet'
import {
  Compass,
  PlusCircle,
  Clock,
  CheckCircle2,
  AlertCircle,
  Coins,
  MapPin,
  Camera,
  RefreshCw,
  ExternalLink,
  ChevronRight,
  Sparkles,
  Zap,
  Cpu,
  Search,
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

const currentView = ref<'feed' | 'create'>('feed')
const tasks = ref<Task[]>([])
const selectedTask = ref<Task | null>(null)
const loading = ref(false)
const searchQuery = ref('')

// Verification State
const isSubmitting = ref(false)
const verificationResult = ref<any>(null)
const currentStep = ref<number>(0)

// Post Form
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
    if (!selectedTask.value && tasks.value.length > 0) {
      selectedTask.value = tasks.value[0]
    }
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
      fetchTasks()
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
    currentView.value = 'feed'
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
  <div class="h-screen w-screen flex bg-[#0A0C11] text-[#E2E8F0] overflow-hidden select-none">
    
    <!-- 1. LEFT SIDEBAR (ElevenLabs Style Clean Navigation) -->
    <aside class="w-64 bg-[#07080B] border-r border-[#1B1E29] flex flex-col justify-between shrink-0">
      
      <!-- Brand & Top Sections -->
      <div class="p-4 space-y-6">
        
        <!-- App Wordmark -->
        <div class="flex items-center gap-3 px-2">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-600 via-indigo-500 to-teal-400 p-[1px] flex items-center justify-center">
            <div class="w-full h-full bg-[#0E1017] rounded-[7px] flex items-center justify-center">
              <Zap class="w-4 h-4 text-teal-400" />
            </div>
          </div>
          <div>
            <div class="font-extrabold text-sm tracking-tight text-white flex items-center gap-1.5">
              <span>BountyBlink</span>
              <span class="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">DEVNET</span>
            </div>
            <p class="text-[10px] text-slate-500 font-mono">Autonomous Physical Escrow</p>
          </div>
        </div>

        <!-- Navigation Menu -->
        <nav class="space-y-1">
          <button 
            @click="currentView = 'feed'"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all"
            :class="currentView === 'feed' ? 'bg-[#181B26] text-white shadow-sm border border-[#262C3E]' : 'text-slate-400 hover:text-white hover:bg-[#12141C]'"
          >
            <Compass class="w-4 h-4 text-teal-400" />
            <span>Active Bounties</span>
          </button>

          <button 
            @click="currentView = 'create'"
            class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all"
            :class="currentView === 'create' ? 'bg-[#181B26] text-white shadow-sm border border-[#262C3E]' : 'text-slate-400 hover:text-white hover:bg-[#12141C]'"
          >
            <PlusCircle class="w-4 h-4 text-purple-400" />
            <span>Create Bounty</span>
          </button>
        </nav>

      </div>

      <!-- Bottom Profile & Status -->
      <div class="p-4 border-t border-[#1B1E29] space-y-3 bg-[#0A0C11]">
        
        <div class="flex items-center justify-between text-xs font-mono">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
            <span class="text-slate-400 text-[11px]">{{ publicKey.slice(0, 4) }}...{{ publicKey.slice(-4) }}</span>
          </div>
          <div class="text-teal-400 font-bold flex items-center gap-1">
            <Coins class="w-3.5 h-3.5 text-purple-400" />
            <span>{{ balance.toFixed(2) }} SOL</span>
          </div>
        </div>

        <button 
          @click="resetDemo"
          class="w-full py-1.5 px-3 rounded-lg bg-[#141722] hover:bg-[#1C2030] border border-[#232738] text-[11px] font-mono text-slate-300 transition-colors flex items-center justify-center gap-1.5"
        >
          <RefreshCw class="w-3 h-3 text-purple-400" :class="loading ? 'animate-spin' : ''" />
          <span>Reset Demo State</span>
        </button>

      </div>

    </aside>

    <!-- 2. MAIN WORKSPACE (2-COLUMN HIGH DENSITY SAAS VIEW) -->
    <main class="flex-1 flex overflow-hidden">
      
      <!-- COLUMN A: TASK FEED / LIST (380px fixed width) -->
      <section class="w-96 border-r border-[#1B1E29] bg-[#0C0E14] flex flex-col shrink-0">
        
        <!-- Search & Filter Header -->
        <div class="p-4 border-b border-[#1B1E29] space-y-3">
          <div class="flex items-center justify-between">
            <h1 class="font-bold text-sm text-white">Physical Work Orders</h1>
            <span class="text-[10px] font-mono text-slate-500">{{ tasks.length }} available</span>
          </div>

          <!-- Search Input -->
          <div class="relative">
            <Search class="w-3.5 h-3.5 text-slate-500 absolute left-3 top-2.5" />
            <input 
              v-model="searchQuery"
              placeholder="Search by location, keyword..."
              class="w-full pl-8 pr-3 py-1.5 rounded-lg bg-[#141722] border border-[#202534] text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <!-- Task List Items -->
        <div class="flex-1 overflow-y-auto divide-y divide-[#171A24]">
          
          <div 
            v-for="task in tasks" 
            :key="task.id"
            @click="selectTask(task)"
            class="p-4 cursor-pointer transition-colors relative"
            :class="selectedTask?.id === task.id ? 'bg-[#151824] border-l-2 border-purple-500' : 'hover:bg-[#10121A]'"
          >
            <div class="flex justify-between items-start mb-1">
              <span class="text-[10px] font-mono text-slate-500 uppercase">#{{ task.id.slice(0, 6) }}</span>
              <span class="font-mono font-bold text-xs text-teal-400">{{ task.reward_sol }} SOL</span>
            </div>

            <h3 class="font-semibold text-xs text-slate-100 line-clamp-1 mb-1">{{ task.title }}</h3>
            <p class="text-[11px] text-slate-400 line-clamp-2 leading-relaxed mb-2.5">{{ task.instruction }}</p>

            <div class="flex items-center justify-between text-[10px] font-mono text-slate-500">
              <span class="flex items-center gap-1"><MapPin class="w-3 h-3 text-purple-400" /> {{ task.latitude.toFixed(2) }}, {{ task.longitude.toFixed(2) }}</span>
              <span 
                class="px-1.5 py-0.2 rounded font-bold uppercase"
                :class="{
                  'text-purple-400 bg-purple-500/10': task.status === 'OPEN',
                  'text-amber-400 bg-amber-500/10': task.status === 'CLAIMED',
                  'text-teal-400 bg-teal-500/10': task.status === 'PAID',
                  'text-rose-400 bg-rose-500/10': task.status === 'REJECTED',
                  'text-slate-500 bg-slate-800': task.status === 'REFUNDED'
                }"
              >
                {{ task.status }}
              </span>
            </div>
          </div>

        </div>

      </section>

      <!-- COLUMN B: DETAIL & INTERACTION CANVAS -->
      <section class="flex-1 bg-[#090A0F] overflow-y-auto p-6 md:p-8 flex flex-col items-center">
        
        <!-- View 1: Task Inspection & Autonomous Verification -->
        <div v-if="currentView === 'feed' && selectedTask" class="w-full max-w-2xl space-y-6">
          
          <!-- Top Order Header Card -->
          <div class="p-6 rounded-2xl bg-[#11131C] border border-[#1E2232] shadow-xl space-y-4">
            
            <div class="flex justify-between items-start border-b border-[#1E2232] pb-4">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-xs font-mono text-slate-500 uppercase tracking-wider">Work Order #{{ selectedTask.id.slice(0, 8) }}</span>
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
                <h2 class="text-xl font-bold text-white">{{ selectedTask.title }}</h2>
              </div>

              <div class="text-right">
                <span class="text-[10px] font-mono text-slate-500 uppercase block">Escrow Bounty</span>
                <span class="text-xl font-mono font-black text-teal-400">{{ selectedTask.reward_sol }} SOL</span>
              </div>
            </div>

            <!-- Physical Task Specifications -->
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="p-3.5 rounded-xl bg-[#161824] border border-[#202538] space-y-1">
                <span class="text-[10px] font-mono uppercase text-slate-400 block font-semibold">Physical Instruction</span>
                <p class="text-slate-200 text-xs leading-relaxed">{{ selectedTask.instruction }}</p>
              </div>

              <div class="p-3.5 rounded-xl bg-[#161824] border border-[#202538] space-y-1">
                <span class="text-[10px] font-mono uppercase text-teal-400 block font-semibold">Target Visual Criteria</span>
                <p class="text-slate-200 text-xs leading-relaxed">{{ selectedTask.target_description }}</p>
              </div>
            </div>

            <!-- Geolocation Spec Strip -->
            <div class="flex items-center gap-4 text-xs font-mono text-slate-400 pt-1">
              <span class="flex items-center gap-1.5"><MapPin class="w-3.5 h-3.5 text-purple-400" /> Target Lat {{ selectedTask.latitude.toFixed(4) }}, Lon {{ selectedTask.longitude.toFixed(4) }}</span>
              <span class="flex items-center gap-1.5"><Clock class="w-3.5 h-3.5 text-slate-500" /> 10m Lease Lock</span>
            </div>

            <!-- Action 1: Claim Task -->
            <div v-if="selectedTask.status === 'OPEN'" class="pt-2">
              <button 
                @click="claimTask"
                class="w-full py-3 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-mono font-bold text-xs uppercase tracking-wider transition-all shadow-lg shadow-purple-600/20 flex items-center justify-center gap-2"
              >
                <span>Claim Exclusive Lease & Lock 0.01 SOL</span>
                <ChevronRight class="w-4 h-4" />
              </button>
            </div>

            <!-- Action 2: Evidence Submission Presets & Camera -->
            <div v-else-if="selectedTask.status === 'CLAIMED' && !isSubmitting && !verificationResult" class="pt-2 space-y-3">
              
              <div class="p-3 rounded-xl bg-purple-950/20 border border-purple-500/20 text-xs text-purple-200">
                <p class="font-bold flex items-center gap-1.5 mb-1">
                  <Cpu class="w-3.5 h-3.5 text-teal-400" />
                  Autonomous Verification Engine
                </p>
                <p class="text-purple-300/80 text-[11px] leading-relaxed">
                  Verify the physical ground truth on Solana Devnet using judge presets or upload live evidence:
                </p>
              </div>

              <!-- Two Judge Testing Presets Required by Spec -->
              <div class="grid grid-cols-2 gap-3">
                <button 
                  @click="submitEvidence('VALID')"
                  class="p-4 rounded-xl bg-[#141A24] border border-teal-500/30 hover:border-teal-400 hover:bg-teal-500/10 transition-all text-left group"
                >
                  <div class="text-[10px] font-mono font-bold uppercase text-teal-400">Preset Fixture 1</div>
                  <div class="font-bold text-xs text-white group-hover:text-teal-300 mt-0.5">Test: Valid Photo</div>
                  <div class="text-[10px] text-slate-400 mt-1">Passes GPS + Vision ➔ Auto Payout</div>
                </button>

                <button 
                  @click="submitEvidence('FAKE')"
                  class="p-4 rounded-xl bg-[#1C141C] border border-rose-500/30 hover:border-rose-400 hover:bg-rose-500/10 transition-all text-left group"
                >
                  <div class="text-[10px] font-mono font-bold uppercase text-rose-400">Preset Fixture 2</div>
                  <div class="font-bold text-xs text-white group-hover:text-rose-300 mt-0.5">Test: Fake Photo</div>
                  <div class="text-[10px] text-slate-400 mt-1">Fails Vision ➔ Refund Trigger</div>
                </button>
              </div>

              <!-- Live File Upload / Camera Input -->
              <label class="w-full py-3.5 rounded-xl border border-dashed border-[#282E42] bg-[#12141E] hover:border-purple-500 flex flex-col items-center justify-center cursor-pointer transition-colors text-xs font-mono text-slate-300">
                <Camera class="w-5 h-5 text-purple-400 mb-1" />
                <span>Snap / Upload Real Camera Evidence</span>
                <span class="text-[10px] text-slate-500">Evaluates EXIF GPS + Gemini 2.5 Flash Multimodal Vision</span>
                <input type="file" accept="image/*" capture="environment" @change="handleFileUpload" class="hidden" />
              </label>

            </div>

            <!-- Verification Pipeline Stepper -->
            <div v-if="isSubmitting" class="p-4 rounded-xl bg-[#141724] border border-indigo-500/30 space-y-3">
              <div class="font-mono text-xs uppercase tracking-wider text-slate-400 border-b border-slate-800 pb-2 flex items-center justify-between">
                <span>Autonomous Verifier</span>
                <span class="text-teal-400 animate-pulse font-bold">Processing pipeline...</span>
              </div>

              <div class="space-y-2 text-xs font-mono">
                <div class="flex items-center gap-3" :class="currentStep >= 1 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep > 1 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep > 1" class="w-3.5 h-3.5" />
                    <span v-else>1</span>
                  </div>
                  <span>Tier 0: File Intake & Perceptual Hash Integrity</span>
                </div>

                <div class="flex items-center gap-3" :class="currentStep >= 2 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep > 2 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep > 2" class="w-3.5 h-3.5" />
                    <span v-else>2</span>
                  </div>
                  <span>Tier 1: Geofence Haversine Check (&lt;= 150m)</span>
                </div>

                <div class="flex items-center gap-3" :class="currentStep >= 3 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep > 3 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep > 3" class="w-3.5 h-3.5" />
                    <span v-else>3</span>
                  </div>
                  <span>Tier 2: Gemini 2.5 Flash Multimodal Scene Verification</span>
                </div>

                <div class="flex items-center gap-3" :class="currentStep >= 4 ? 'text-white' : 'text-slate-600'">
                  <div class="w-5 h-5 rounded-full flex items-center justify-center text-[10px]" :class="currentStep >= 4 ? 'bg-teal-500/20 text-teal-400 border border-teal-500/40' : 'bg-slate-800 text-slate-400'">
                    <Check v-if="currentStep >= 4" class="w-3.5 h-3.5" />
                    <span v-else>4</span>
                  </div>
                  <span>Tier 3: Solana Devnet On-Chain Settlement</span>
                </div>
              </div>
            </div>

            <!-- Verification Verdict -->
            <div v-if="verificationResult" class="p-5 rounded-xl border shadow-xl" :class="verificationResult.status === 'PAID' ? 'bg-teal-950/20 border-teal-500/40' : 'bg-rose-950/20 border-rose-500/40'">
              
              <div class="flex items-center gap-2 font-mono text-xs font-bold uppercase mb-2" :class="verificationResult.status === 'PAID' ? 'text-teal-400' : 'text-rose-400'">
                <CheckCircle2 v-if="verificationResult.status === 'PAID'" class="w-5 h-5" />
                <AlertCircle v-else class="w-5 h-5" />
                <span>{{ verificationResult.status === 'PAID' ? 'Settlement Confirmed: Escrow Paid' : 'Verification Rejected' }}</span>
              </div>

              <p class="text-xs text-slate-300 leading-relaxed mb-4">
                {{ verificationResult.verification.reason }}
              </p>

              <div v-if="verificationResult.payout_tx_sig" class="p-3 rounded-lg bg-[#0C0E14] border border-slate-800 text-xs font-mono mb-4">
                <span class="text-[10px] text-slate-500 uppercase block">Solana Devnet Transaction</span>
                <a 
                  :href="verificationResult.explorer_url" 
                  target="_blank" 
                  class="text-teal-400 hover:underline flex items-center gap-1.5 font-bold mt-1 break-all"
                >
                  <span>{{ verificationResult.payout_tx_sig }}</span>
                  <ExternalLink class="w-3.5 h-3.5 shrink-0" />
                </a>
              </div>

              <div v-if="verificationResult.status === 'REJECTED' && selectedTask.status !== 'REFUNDED'">
                <button 
                  @click="triggerRefund"
                  class="w-full py-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-mono text-xs font-bold uppercase tracking-wider transition-colors"
                >
                  Refund 0.01 SOL Escrow to Poster
                </button>
              </div>

              <div v-if="selectedTask.status === 'REFUNDED'" class="p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs font-mono text-slate-400">
                Deposit refunded back to task creator.
              </div>

            </div>

          </div>

        </div>

        <!-- View 2: Create Bounty Form -->
        <div v-else-if="currentView === 'create'" class="w-full max-w-xl space-y-6">
          
          <div class="p-6 rounded-2xl bg-[#11131C] border border-[#1E2232] shadow-xl space-y-5">
            
            <div class="border-b border-[#1E2232] pb-4">
              <h2 class="text-lg font-bold text-white flex items-center gap-2">
                <Sparkles class="w-5 h-5 text-purple-400" />
                <span>Deploy Autonomous Physical Bounty</span>
              </h2>
              <p class="text-xs text-slate-400 font-mono mt-0.5">Locks 0.01 SOL into Devnet escrow vault</p>
            </div>

            <!-- Quick Task Templates -->
            <div class="space-y-2">
              <span class="text-[10px] font-mono uppercase text-slate-400 tracking-wider">Quick Templates</span>
              <div class="grid grid-cols-2 gap-2.5">
                <button 
                  @click="applyPreset('EV Charger Availability Check', 'Photograph the screen and plug status of Allego charger #3.', 'Operational screen, intact cable connector, no error code')"
                  class="p-3 rounded-xl border border-[#202538] bg-[#161824] hover:border-purple-500 text-left transition-all text-xs font-mono text-slate-300"
                >
                  + EV Station Status
                </button>
                <button 
                  @click="applyPreset('Coffee Shop Hours Blackboard', 'Photograph the blackboard near the front door showing Sunday hours.', 'Chalkboard sign with readable opening hours text')"
                  class="p-3 rounded-xl border border-[#202538] bg-[#161824] hover:border-purple-500 text-left transition-all text-xs font-mono text-slate-300"
                >
                  + Shop Open Verification
                </button>
              </div>
            </div>

            <!-- Form -->
            <div class="space-y-3.5 text-xs font-mono">
              <div>
                <label class="block text-slate-400 uppercase text-[11px] mb-1">Task Title</label>
                <input 
                  v-model="postTitle"
                  placeholder="e.g. Verify Alexanderplatz EV Charger" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-[#161824] border border-[#202538] text-white placeholder-slate-600 focus:outline-none focus:border-purple-500 text-xs"
                />
              </div>

              <div>
                <label class="block text-slate-400 uppercase text-[11px] mb-1">Physical Verification Instructions</label>
                <textarea 
                  v-model="postInstruction"
                  rows="2"
                  placeholder="Specific camera angle or physical detail to inspect..." 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-[#161824] border border-[#202538] text-white placeholder-slate-600 focus:outline-none focus:border-purple-500 text-xs"
                ></textarea>
              </div>

              <div>
                <label class="block text-slate-400 uppercase text-[11px] mb-1">Target Description (Evaluated by Gemini Vision)</label>
                <input 
                  v-model="postTarget"
                  placeholder="e.g. Green operational display, undamaged cable" 
                  class="w-full px-3.5 py-2.5 rounded-xl bg-[#161824] border border-[#202538] text-white placeholder-slate-600 focus:outline-none focus:border-purple-500 text-xs"
                />
              </div>

              <div class="p-3.5 rounded-xl bg-[#161824] border border-[#202538] flex justify-between items-center">
                <span class="text-slate-400">Escrow Locked Amount</span>
                <span class="font-bold text-teal-400 text-sm">0.01 SOL</span>
              </div>

              <button 
                @click="createBounty"
                class="w-full py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-sm uppercase tracking-wider transition-all shadow-lg shadow-purple-600/20 flex items-center justify-center gap-2"
              >
                <span>Deposit & Post Bounty</span>
                <ChevronRight class="w-4 h-4" />
              </button>
            </div>

          </div>

        </div>

      </section>

    </main>

  </div>
</template>
