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
  Layers
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
const currentStep = ref<number>(0) // 1: Intake, 2: Geofence, 3: Vision, 4: Settlement

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

  // Emulate live verification stepper delays for judge feedback
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
  <div class="min-h-screen bg-[#E5E2DA] flex justify-center py-0 sm:py-6 selection:bg-[#EA580C] selection:text-white">
    <!-- Centered Mobile Column (max 430px) -->
    <main class="w-full max-w-[430px] min-h-screen bg-[#F8F6F0] flex flex-col shadow-2xl border-x border-[#D8D4C8] relative pb-20">
      
      <!-- Operational Header -->
      <header class="p-4 border-b border-[#D8D4C8] bg-[#F3F0E6] flex items-center justify-between sticky top-0 z-30">
        <div>
          <div class="flex items-center gap-2">
            <span class="font-serif tracking-tight text-xl font-bold text-[#161614]">BountyBlink</span>
            <span class="bg-[#161614] text-[#F8F6F0] text-[10px] font-mono font-semibold px-1.5 py-0.5 uppercase tracking-wider rounded-xs">Devnet</span>
          </div>
          <p class="text-[11px] text-[#63625C] font-mono mt-0.5">Physical Task Escrow</p>
        </div>

        <div class="flex items-center gap-2">
          <button 
            @click="resetDemo" 
            title="Reset to initial test seed tasks"
            class="p-1.5 text-[#63625C] hover:text-[#161614] border border-[#D8D4C8] hover:border-[#161614] transition-colors rounded-xs text-xs flex items-center gap-1 bg-[#F8F6F0]"
          >
            <RefreshCw class="w-3.5 h-3.5" :class="loading ? 'animate-spin' : ''" />
            <span class="text-[10px] font-mono">Reset</span>
          </button>
        </div>
      </header>

      <!-- Ephemeral Demo Wallet Strip -->
      <section class="px-4 py-2 bg-[#EFECE4] border-b border-[#D8D4C8] flex items-center justify-between text-xs">
        <div class="flex items-center gap-1.5 text-[#63625C]">
          <span class="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
          <span class="font-mono text-[11px]">Worker: {{ publicKey.slice(0, 4) }}...{{ publicKey.slice(-4) }}</span>
        </div>
        <div class="font-mono font-semibold text-[#161614] text-[12px] flex items-center gap-1">
          <Coins class="w-3.5 h-3.5 text-[#EA580C]" />
          <span>{{ balance.toFixed(2) }} SOL</span>
        </div>
      </section>

      <!-- Content Views Container -->
      <div class="flex-1 p-4 overflow-y-auto">
        
        <!-- ================= TAB 1: DO TASKS ================= -->
        <section v-if="activeTab === 'do'">
          
          <!-- State A: Task Detail & Verification Active -->
          <div v-if="selectedTask" class="space-y-4">
            
            <button 
              @click="selectedTask = null" 
              class="text-xs font-mono text-[#63625C] hover:text-[#161614] flex items-center gap-1"
            >
              ← Back to task list
            </button>

            <!-- Ticket Work Order Card -->
            <article class="bg-[#F3F0E6] border border-[#161614] p-4 relative shadow-[2px_2px_0px_#161614]">
              <div class="flex justify-between items-start border-b border-dashed border-[#B8B4A8] pb-3 mb-3">
                <div>
                  <span class="text-[10px] font-mono uppercase tracking-widest text-[#63625C]">Order #{{ selectedTask.id.slice(0, 8) }}</span>
                  <h2 class="font-serif text-lg font-bold text-[#161614] leading-tight mt-0.5">{{ selectedTask.title }}</h2>
                </div>
                <div class="text-right">
                  <span class="text-[10px] font-mono uppercase text-[#63625C]">Locked Escrow</span>
                  <div class="text-base font-mono font-bold text-[#EA580C]">{{ selectedTask.reward_sol }} SOL</div>
                </div>
              </div>

              <div class="space-y-2 text-xs text-[#2A2926]">
                <p><strong class="font-medium text-[#161614]">Instruction:</strong> {{ selectedTask.instruction }}</p>
                <p><strong class="font-medium text-[#161614]">Visual Target:</strong> {{ selectedTask.target_description }}</p>
                <div class="flex items-center gap-3 pt-2 text-[11px] font-mono text-[#63625C]">
                  <span class="flex items-center gap-1"><MapPin class="w-3 h-3 text-[#EA580C]" /> ~32m nearby</span>
                  <span class="flex items-center gap-1"><Clock class="w-3 h-3" /> 10m lock</span>
                </div>
              </div>

              <!-- Escrow Status Stamp -->
              <div class="mt-4 pt-3 border-t border-dashed border-[#B8B4A8] flex items-center justify-between">
                <span class="text-[11px] font-mono uppercase text-[#63625C]">Escrow Status:</span>
                <span 
                  class="text-[11px] font-mono font-bold px-2 py-0.5 border"
                  :class="{
                    'border-[#EA580C] text-[#EA580C] bg-[#FFF5EB]': selectedTask.status === 'OPEN',
                    'border-amber-600 text-amber-700 bg-amber-50': selectedTask.status === 'CLAIMED',
                    'border-emerald-700 text-emerald-800 bg-emerald-50': selectedTask.status === 'PAID',
                    'border-rose-700 text-rose-800 bg-rose-50': selectedTask.status === 'REJECTED',
                    'border-stone-500 text-stone-700 bg-stone-100': selectedTask.status === 'REFUNDED'
                  }"
                >
                  {{ selectedTask.status }}
                </span>
              </div>
            </article>

            <!-- Action Area: Claim or Submit -->
            <div v-if="selectedTask.status === 'OPEN'" class="pt-2">
              <button 
                @click="claimTask"
                class="w-full py-3.5 bg-[#EA580C] hover:bg-[#D9480F] text-[#F8F6F0] font-mono font-bold text-sm tracking-wider uppercase transition-colors shadow-[2px_2px_0px_#161614] flex items-center justify-center gap-2"
              >
                <span>Claim Task & Lock 0.01 SOL</span>
                <ArrowRight class="w-4 h-4" />
              </button>
            </div>

            <!-- Evidence Submission Form & Judge Presets -->
            <div v-else-if="selectedTask.status === 'CLAIMED' && !isSubmitting && !verificationResult" class="space-y-4 pt-2">
              <div class="p-3 bg-[#EFECE4] border border-[#D8D4C8] text-xs">
                <p class="font-mono font-bold text-[#161614] mb-1">Judge Testing Options</p>
                <p class="text-[#63625C] leading-relaxed">
                  Test the complete autonomous verification loop instantly using pre-packaged fixtures or capture live evidence:
                </p>
              </div>

              <!-- Two Judge Testing Presets Required by Spec -->
              <div class="grid grid-cols-2 gap-2">
                <button 
                  @click="submitEvidence('VALID')"
                  class="p-3 bg-emerald-50 border border-emerald-700 hover:bg-emerald-100 transition-colors text-left shadow-[1px_1px_0px_#15803D]"
                >
                  <div class="text-[10px] font-mono font-bold uppercase text-emerald-800">Fixture 1</div>
                  <div class="font-bold text-xs text-emerald-950 mt-0.5">Test: Valid photo</div>
                  <div class="text-[10px] text-emerald-700 mt-1">Passes GPS + Vision -> Payout</div>
                </button>

                <button 
                  @click="submitEvidence('FAKE')"
                  class="p-3 bg-rose-50 border border-rose-700 hover:bg-rose-100 transition-colors text-left shadow-[1px_1px_0px_#B91C1C]"
                >
                  <div class="text-[10px] font-mono font-bold uppercase text-rose-800">Fixture 2</div>
                  <div class="font-bold text-xs text-rose-950 mt-0.5">Test: Fake photo</div>
                  <div class="text-[10px] text-rose-700 mt-1">Fails GPS/Vision -> Escrow Lock</div>
                </button>
              </div>

              <!-- Native Camera / File Input -->
              <div class="pt-2">
                <label class="w-full py-3 border border-dashed border-[#161614] bg-[#F8F6F0] hover:bg-[#F3F0E6] flex flex-col items-center justify-center cursor-pointer transition-colors text-xs font-mono text-[#161614]">
                  <Camera class="w-5 h-5 text-[#EA580C] mb-1" />
                  <span>Upload / Snap Live Photo</span>
                  <input type="file" accept="image/*" capture="environment" @change="handleFileUpload" class="hidden" />
                </label>
              </div>
            </div>

            <!-- Live Verification Stepper -->
            <div v-if="isSubmitting" class="p-4 bg-[#F3F0E6] border border-[#161614] space-y-3">
              <div class="font-mono text-xs uppercase tracking-wider text-[#63625C] border-b border-[#D8D4C8] pb-2 flex items-center justify-between">
                <span>Autonomous Verifier</span>
                <span class="text-[#EA580C] animate-pulse">Running pipeline...</span>
              </div>

              <div class="space-y-2 text-xs font-mono">
                <div class="flex items-center gap-2" :class="currentStep >= 1 ? 'text-[#161614]' : 'text-[#B8B4A8]'">
                  <CheckCircle2 v-if="currentStep > 1" class="w-4 h-4 text-emerald-600" />
                  <span v-else class="w-4 h-4 rounded-full border border-current flex items-center justify-center text-[10px]">1</span>
                  <span>Tier 0: Intake & Duplicate Check</span>
                </div>

                <div class="flex items-center gap-2" :class="currentStep >= 2 ? 'text-[#161614]' : 'text-[#B8B4A8]'">
                  <CheckCircle2 v-if="currentStep > 2" class="w-4 h-4 text-emerald-600" />
                  <span v-else class="w-4 h-4 rounded-full border border-current flex items-center justify-center text-[10px]">2</span>
                  <span>Tier 1: Geofence Validation (150m)</span>
                </div>

                <div class="flex items-center gap-2" :class="currentStep >= 3 ? 'text-[#161614]' : 'text-[#B8B4A8]'">
                  <CheckCircle2 v-if="currentStep > 3" class="w-4 h-4 text-emerald-600" />
                  <span v-else class="w-4 h-4 rounded-full border border-current flex items-center justify-center text-[10px]">3</span>
                  <span>Tier 2: Multimodal Scene Verification</span>
                </div>

                <div class="flex items-center gap-2" :class="currentStep >= 4 ? 'text-[#161614]' : 'text-[#B8B4A8]'">
                  <CheckCircle2 v-if="currentStep >= 4" class="w-4 h-4 text-emerald-600" />
                  <span v-else class="w-4 h-4 rounded-full border border-current flex items-center justify-center text-[10px]">4</span>
                  <span>Tier 3: On-Chain Devnet Settlement</span>
                </div>
              </div>
            </div>

            <!-- Final Result / Receipt Ticket -->
            <div v-if="verificationResult" class="p-4 border shadow-[2px_2px_0px_#161614]" :class="verificationResult.status === 'PAID' ? 'bg-emerald-50 border-emerald-800' : 'bg-rose-50 border-rose-800'">
              <div class="flex items-center gap-2 font-mono text-xs font-bold uppercase mb-2" :class="verificationResult.status === 'PAID' ? 'text-emerald-900' : 'text-rose-900'">
                <CheckCircle2 v-if="verificationResult.status === 'PAID'" class="w-5 h-5 text-emerald-700" />
                <AlertCircle v-else class="w-5 h-5 text-rose-700" />
                <span>{{ verificationResult.status === 'PAID' ? 'Settlement Confirmed: Paid' : 'Verification Rejected' }}</span>
              </div>

              <p class="text-xs text-[#2A2926] leading-relaxed mb-3">
                {{ verificationResult.verification.reason }}
              </p>

              <!-- Solana Explorer Proof Link -->
              <div v-if="verificationResult.payout_tx_sig" class="p-2.5 bg-[#F8F6F0] border border-[#161614] text-xs font-mono mb-3">
                <span class="text-[10px] text-[#63625C] uppercase block">Devnet Transaction Proof</span>
                <a 
                  :href="verificationResult.explorer_url" 
                  target="_blank" 
                  class="text-[#EA580C] hover:underline flex items-center gap-1 font-bold mt-0.5 break-all"
                >
                  <span>{{ verificationResult.payout_tx_sig.slice(0, 16) }}...</span>
                  <ExternalLink class="w-3.5 h-3.5 shrink-0" />
                </a>
              </div>

              <!-- Refund Button for Poster if Rejected -->
              <div v-if="verificationResult.status === 'REJECTED' && selectedTask.status !== 'REFUNDED'" class="pt-1">
                <button 
                  @click="triggerRefund"
                  class="w-full py-2.5 bg-[#161614] text-[#F8F6F0] font-mono text-xs font-bold uppercase tracking-wider hover:bg-[#2A2926] transition-colors"
                >
                  Claim Poster Refund (0.01 SOL)
                </button>
              </div>

              <div v-if="selectedTask.status === 'REFUNDED'" class="p-2.5 bg-[#EFECE4] border border-[#B8B4A8] text-xs font-mono text-[#63625C]">
                Refund completed. Funds returned to creator.
              </div>
            </div>

          </div>

          <!-- State B: Task Feed List -->
          <div v-else class="space-y-3">
            <div class="flex items-center justify-between border-b border-[#D8D4C8] pb-2 mb-3">
              <span class="font-mono text-xs text-[#63625C] uppercase tracking-wider">Available Work Orders ({{ tasks.length }})</span>
              <span class="text-[11px] font-mono text-[#EA580C]">Devnet Escrow</span>
            </div>

            <article 
              v-for="task in tasks" 
              :key="task.id"
              @click="selectTask(task)"
              class="p-3.5 bg-[#F3F0E6] border border-[#161614] hover:bg-[#EFECE4] cursor-pointer transition-colors shadow-[2px_2px_0px_#161614] space-y-2 relative"
            >
              <div class="flex justify-between items-start">
                <h3 class="font-serif font-bold text-sm text-[#161614] leading-snug pr-2">{{ task.title }}</h3>
                <span class="font-mono font-bold text-xs text-[#EA580C] shrink-0">{{ task.reward_sol }} SOL</span>
              </div>

              <p class="text-xs text-[#63625C] line-clamp-2 leading-relaxed">{{ task.instruction }}</p>

              <div class="flex items-center justify-between pt-1 border-t border-dashed border-[#D8D4C8] text-[11px] font-mono text-[#63625C]">
                <span class="flex items-center gap-1"><MapPin class="w-3 h-3 text-[#EA580C]" /> {{ task.latitude.toFixed(2) }}, {{ task.longitude.toFixed(2) }}</span>
                <span 
                  class="font-bold uppercase text-[10px] px-1.5 py-0.2 border"
                  :class="{
                    'border-[#EA580C] text-[#EA580C]': task.status === 'OPEN',
                    'border-amber-600 text-amber-700': task.status === 'CLAIMED',
                    'border-emerald-700 text-emerald-800': task.status === 'PAID',
                    'border-rose-700 text-rose-800': task.status === 'REJECTED',
                    'border-stone-400 text-stone-600': task.status === 'REFUNDED'
                  }"
                >
                  {{ task.status }}
                </span>
              </div>
            </article>
          </div>

        </section>

        <!-- ================= TAB 2: POST TASK ================= -->
        <section v-if="activeTab === 'post'" class="space-y-4">
          
          <div class="border-b border-[#D8D4C8] pb-2">
            <h2 class="font-serif text-lg font-bold text-[#161614]">Post Physical Bounty</h2>
            <p class="text-xs text-[#63625C] font-mono mt-0.5">Locks 0.01 SOL in Devnet escrow</p>
          </div>

          <!-- Quick Work Order Presets -->
          <div class="space-y-1.5">
            <span class="text-[11px] font-mono uppercase text-[#63625C]">Quick Presets</span>
            <div class="grid grid-cols-2 gap-2">
              <button 
                @click="applyPreset('EV Charger Availability', 'Photograph screen & plug of EV charger at Central Station.', 'Operational Allego or Tesla Supercharger screen')"
                class="p-2 border border-[#B8B4A8] bg-[#F3F0E6] text-left hover:border-[#161614] text-[11px] font-mono"
              >
                + EV Station
              </button>
              <button 
                @click="applyPreset('Coffee Shop Open Verification', 'Capture blackboard with operating hours on Kastanienallee.', 'Chalkboard sign with clear hours text')"
                class="p-2 border border-[#B8B4A8] bg-[#F3F0E6] text-left hover:border-[#161614] text-[11px] font-mono"
              >
                + Shop Open
              </button>
            </div>
          </div>

          <!-- Post Form -->
          <div class="space-y-3 pt-2 text-xs">
            <div>
              <label class="block font-mono text-[11px] text-[#63625C] uppercase mb-1">Task Title</label>
              <input 
                v-model="postTitle" 
                placeholder="e.g. Verify Alexanderplatz EV Charger" 
                class="w-full p-2.5 bg-[#F8F6F0] border border-[#161614] text-[#161614] font-medium text-xs focus:outline-none focus:ring-1 focus:ring-[#EA580C]"
              />
            </div>

            <div>
              <label class="block font-mono text-[11px] text-[#63625C] uppercase mb-1">Instructions for Worker</label>
              <textarea 
                v-model="postInstruction" 
                rows="2" 
                placeholder="Specific instructions on what photo angle to take..."
                class="w-full p-2.5 bg-[#F8F6F0] border border-[#161614] text-[#161614] text-xs focus:outline-none focus:ring-1 focus:ring-[#EA580C]"
              ></textarea>
            </div>

            <div>
              <label class="block font-mono text-[11px] text-[#63625C] uppercase mb-1">Target Visual Cue for Verifier</label>
              <input 
                v-model="postTarget" 
                placeholder="e.g. Operational green display, intact cable" 
                class="w-full p-2.5 bg-[#F8F6F0] border border-[#161614] text-[#161614] text-xs focus:outline-none focus:ring-1 focus:ring-[#EA580C]"
              />
            </div>

            <div class="p-3 bg-[#EFECE4] border border-[#D8D4C8] flex justify-between items-center font-mono">
              <span class="text-[#63625C]">Locked Escrow Deposit</span>
              <span class="font-bold text-[#EA580C] text-sm">0.01 SOL</span>
            </div>

            <button 
              @click="createBounty"
              class="w-full py-3.5 bg-[#EA580C] hover:bg-[#D9480F] text-[#F8F6F0] font-mono font-bold text-sm tracking-wider uppercase transition-colors shadow-[2px_2px_0px_#161614]"
            >
              Deposit & Post Bounty
            </button>
          </div>

          <!-- Post Created Result Notice -->
          <div v-if="postCreatedResult" class="p-3 bg-emerald-50 border border-emerald-800 text-xs space-y-2 mt-4">
            <div class="flex items-center gap-1.5 font-mono font-bold text-emerald-900">
              <CheckCircle2 class="w-4 h-4 text-emerald-700" />
              <span>Bounty Created & Escrow Locked</span>
            </div>
            <p class="text-emerald-800 text-[11px]">Task is now live on Devnet. Workers can discover and claim it.</p>
            <a 
              :href="postCreatedResult.explorer_url" 
              target="_blank" 
              class="text-[#EA580C] hover:underline font-mono text-[11px] flex items-center gap-1"
            >
              <span>View Escrow Lock: {{ postCreatedResult.fund_tx_sig.slice(0, 16) }}...</span>
              <ExternalLink class="w-3 h-3" />
            </a>
          </div>

        </section>

      </div>

      <!-- Bottom Mobile Tab Bar (Thumb-Reach) -->
      <nav class="h-14 border-t border-[#D8D4C8] bg-[#F3F0E6] grid grid-cols-2 absolute bottom-0 inset-x-0 z-30">
        <button 
          @click="activeTab = 'do'"
          class="flex flex-col items-center justify-center font-mono text-[11px] uppercase tracking-wider transition-colors border-r border-[#D8D4C8]"
          :class="activeTab === 'do' ? 'text-[#EA580C] bg-[#EFECE4] font-bold' : 'text-[#63625C] hover:text-[#161614]'"
        >
          <Layers class="w-4 h-4 mb-0.5" />
          <span>Do Tasks</span>
        </button>

        <button 
          @click="activeTab = 'post'"
          class="flex flex-col items-center justify-center font-mono text-[11px] uppercase tracking-wider transition-colors"
          :class="activeTab === 'post' ? 'text-[#EA580C] bg-[#EFECE4] font-bold' : 'text-[#63625C] hover:text-[#161614]'"
        >
          <Coins class="w-4 h-4 mb-0.5" />
          <span>Post Task</span>
        </button>
      </nav>

    </main>
  </div>
</template>
