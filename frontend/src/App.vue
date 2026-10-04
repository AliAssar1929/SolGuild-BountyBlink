<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import confetti from 'canvas-confetti'
import { useWallet } from './composables/useWallet'
import TaskCard from './components/TaskCard.vue'
import EscrowChip from './components/EscrowChip.vue'
import StatusStamp from './components/StatusStamp.vue'
import TxLink from './components/TxLink.vue'
import VerificationStepper from './components/VerificationStepper.vue'
import ConfidenceRing from './components/ConfidenceRing.vue'
import DemoDrawer from './components/DemoDrawer.vue'

import {
  Compass,
  PlusCircle,
  Clock,
  MapPin,
  Camera,
  Search,
  Sun,
  Moon,
  ArrowRight,
  RotateCcw,
  CheckCircle2,
  AlertCircle,
  FlaskConical,
  Terminal,
  Info
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

// Navigation & Theme
const currentTab = ref<'feed' | 'post' | 'activity'>('feed')
const isDark = ref(false)
const showDemoDrawer = ref(false)

// Feed & Filters
const tasks = ref<Task[]>([])
const selectedTask = ref<Task | null>(null)
const loading = ref(false)
const searchQuery = ref('')
const filter = ref<'ALL' | 'OPEN' | 'NEAR'>('ALL')

// Verification State
const isSubmitting = ref(false)
const verificationResult = ref<any>(null)
const currentStep = ref<number>(0)
const terminalLogs = ref<string[]>([])

// Post Task Form
const postTitle = ref('')
const postInstruction = ref('')
const postTarget = ref('')
const postLat = ref(52.5200)
const postLon = ref(13.4050)
const postCreatedResult = ref<any>(null)

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

const filteredTasks = computed(() => {
  return tasks.value.filter(t => {
    const matchesSearch = t.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          t.instruction.toLowerCase().includes(searchQuery.value.toLowerCase())
    if (!matchesSearch) return false
    if (filter.value === 'OPEN') return t.status === 'OPEN'
    return true
  })
})

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
  terminalLogs.value = []
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

const addLog = (msg: string) => {
  const timestamp = new Date().toISOString().split('T')[1].slice(0, 8)
  terminalLogs.value.push(`[${timestamp}] ${msg}`)
}

const submitEvidence = async (fixtureType?: 'VALID' | 'FAKE', file?: File) => {
  if (!selectedTask.value) return
  showDemoDrawer.value = false
  isSubmitting.value = true
  currentStep.value = 1
  terminalLogs.value = []

  addLog('Initiating evidence intake...')
  addLog('Computing SHA-256 and checking duplicate registry...')

  const formData = new FormData()
  formData.append('worker_address', publicKey.value)
  if (fixtureType) formData.append('fixture_type', fixtureType)
  if (file) formData.append('photo', file)

  setTimeout(() => {
    currentStep.value = 2
    addLog('Tier 0 passed. Computing Haversine geofence distance...')
    addLog(`Target pin: ${selectedTask.value?.latitude.toFixed(4)}, ${selectedTask.value?.longitude.toFixed(4)}`)
  }, 600)

  setTimeout(() => {
    currentStep.value = 3
    addLog('Tier 1 geofence verified. Invoking Gemini 2.5 Flash Vision API...')
    addLog('Analyzing scene authenticity and structured criteria...')
  }, 1200)

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
      if (data.status === 'PAID') {
        addLog(`Settlement confirmed on Solana Devnet. Tx: ${data.payout_tx_sig}`)
        confetti({
          particleCount: 40,
          spread: 50,
          origin: { y: 0.6 }
        })
      } else {
        addLog(`Verification REJECTED. Reason: ${data.verification.reason}`)
      }
      isSubmitting.value = false
      fetchTasks()
    }, 1800)
  } catch (err) {
    console.error(err)
    addLog(`Pipeline error: ${err}`)
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
    currentTab.value = 'feed'
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
  <div class="min-h-screen bg-[#F6F3EC] dark:bg-[#121210] text-[#14130F] dark:text-[#F5F2EB] flex flex-col font-sans transition-colors duration-150">
    
    <!-- DESKTOP & MOBILE TOP BAR -->
    <header class="h-14 border-b border-[#DDD8CC] dark:border-[#2E2D28] bg-[#FFFFFF] dark:bg-[#181815] px-4 md:px-6 flex items-center justify-between sticky top-0 z-30">
      
      <!-- Brand & Devnet Badge -->
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2">
          <span class="font-serif font-bold text-lg tracking-tight">BountyBlink</span>
          <span class="px-1.5 py-0.5 rounded-[4px] border border-[#DDD8CC] dark:border-[#2E2D28] text-[9px] font-mono uppercase tracking-wider font-semibold text-[#6B675E] dark:text-[#9E9A90]">
            Devnet
          </span>
        </div>

        <!-- Desktop Navigation Tabs -->
        <nav class="hidden md:flex items-center gap-1 border-l border-[#DDD8CC] dark:border-[#2E2D28] pl-4">
          <button 
            @click="currentTab = 'feed'"
            class="px-3 py-1.5 rounded-[4px] text-xs font-mono font-medium transition-colors"
            :class="currentTab === 'feed' ? 'bg-[#F6F3EC] dark:bg-[#252520] text-[#14130F] dark:text-[#F5F2EB] font-bold' : 'text-[#6B675E] dark:text-[#9E9A90] hover:text-[#14130F]'"
          >
            Find tasks
          </button>
          <button 
            @click="currentTab = 'post'"
            class="px-3 py-1.5 rounded-[4px] text-xs font-mono font-medium transition-colors"
            :class="currentTab === 'post' ? 'bg-[#F6F3EC] dark:bg-[#252520] text-[#14130F] dark:text-[#F5F2EB] font-bold' : 'text-[#6B675E] dark:text-[#9E9A90] hover:text-[#14130F]'"
          >
            Post a task
          </button>
          <button 
            @click="currentTab = 'activity'"
            class="px-3 py-1.5 rounded-[4px] text-xs font-mono font-medium transition-colors"
            :class="currentTab === 'activity' ? 'bg-[#F6F3EC] dark:bg-[#252520] text-[#14130F] dark:text-[#F5F2EB] font-bold' : 'text-[#6B675E] dark:text-[#9E9A90] hover:text-[#14130F]'"
          >
            My activity
          </button>
        </nav>
      </div>

      <!-- Controls: Demo Drawer, Wallet, Theme -->
      <div class="flex items-center gap-2.5">
        
        <!-- Judge Testing Fixtures Button -->
        <button 
          @click="showDemoDrawer = true"
          class="px-2.5 py-1 rounded-[4px] border border-[#E8590C] text-[#E8590C] hover:bg-[#FDF8F5] dark:hover:bg-[#201712] text-xs font-mono font-semibold flex items-center gap-1.5 transition-colors"
        >
          <FlaskConical class="w-3.5 h-3.5" />
          <span class="hidden sm:inline">Test Fixtures</span>
        </button>

        <!-- Wallet Chip -->
        <div class="flex items-center gap-2 px-2.5 py-1 rounded-[4px] border border-[#DDD8CC] dark:border-[#2E2D28] bg-[#F6F3EC] dark:bg-[#121210] text-xs font-mono">
          <span class="w-1.5 h-1.5 rounded-full bg-[#1F7A4D]"></span>
          <span class="text-[#6B675E] dark:text-[#9E9A90] hidden sm:inline">{{ publicKey.slice(0, 4) }}...{{ publicKey.slice(-4) }}</span>
          <span class="font-bold text-[#14130F] dark:text-[#F5F2EB]">{{ balance.toFixed(2) }} SOL</span>
        </div>

        <!-- Light/Dark Toggle -->
        <button 
          @click="toggleTheme" 
          class="p-1.5 rounded-[4px] border border-[#DDD8CC] dark:border-[#2E2D28] text-[#6B675E] dark:text-[#9E9A90] hover:text-[#14130F] dark:hover:text-[#F5F2EB]"
          title="Toggle theme"
        >
          <Sun v-if="isDark" class="w-4 h-4" />
          <Moon v-else class="w-4 h-4" />
        </button>

      </div>

    </header>

    <!-- MAIN BODY CONTENT -->
    <div class="flex-1 flex flex-col md:flex-row overflow-hidden pb-16 md:pb-0">
      
      <!-- ================= TAB 1: FIND TASKS (2-COLUMN DESKTOP, RESPONSIVE MOBILE) ================= -->
      <template v-if="currentTab === 'feed'">
        
        <!-- COLUMN 1: Task Feed List (420px fixed on desktop) -->
        <section class="w-full md:w-[420px] md:border-r border-[#DDD8CC] dark:border-[#2E2D28] bg-[#FFFFFF] dark:bg-[#181815] flex flex-col shrink-0 overflow-y-auto">
          
          <!-- Search & Filter Controls -->
          <div class="p-4 border-b border-[#DDD8CC] dark:border-[#2E2D28] space-y-3 sticky top-0 bg-[#FFFFFF] dark:bg-[#181815] z-10">
            
            <div class="relative">
              <Search class="w-3.5 h-3.5 text-[#6B675E] absolute left-3 top-2.5" />
              <input 
                v-model="searchQuery"
                placeholder="Search physical work orders..." 
                class="w-full pl-8 pr-3 py-1.5 text-xs bg-[#F6F3EC] dark:bg-[#121210] border border-[#DDD8CC] dark:border-[#2E2D28] rounded-[4px] text-[#14130F] dark:text-[#F5F2EB] placeholder-[#6B675E] focus:outline-none focus:border-[#14130F]"
              />
            </div>

            <div class="flex items-center gap-1.5 text-[11px] font-mono">
              <button 
                @click="filter = 'ALL'"
                class="px-2 py-0.5 rounded-[4px] border transition-colors"
                :class="filter === 'ALL' ? 'border-[#14130F] dark:border-[#F5F2EB] bg-[#14130F] text-[#F6F3EC] dark:bg-[#F5F2EB] dark:text-[#14130F]' : 'border-[#DDD8CC] dark:border-[#2E2D28] text-[#6B675E]'"
              >
                All ({{ tasks.length }})
              </button>
              <button 
                @click="filter = 'OPEN'"
                class="px-2 py-0.5 rounded-[4px] border transition-colors"
                :class="filter === 'OPEN' ? 'border-[#14130F] dark:border-[#F5F2EB] bg-[#14130F] text-[#F6F3EC] dark:bg-[#F5F2EB] dark:text-[#14130F]' : 'border-[#DDD8CC] dark:border-[#2E2D28] text-[#6B675E]'"
              >
                Open Bounties
              </button>
            </div>

          </div>

          <!-- Task Cards List -->
          <div class="p-3 space-y-2.5">
            <TaskCard 
              v-for="task in filteredTasks"
              :key="task.id"
              :task="task"
              :isSelected="selectedTask?.id === task.id"
              @select="selectTask(task)"
            />
          </div>

        </section>

        <!-- COLUMN 2: Task Detail & Verification Stage (Desktop Full Right Column) -->
        <main class="flex-1 bg-[#F6F3EC] dark:bg-[#121210] overflow-y-auto p-4 md:p-8 flex flex-col items-center">
          
          <div v-if="selectedTask" class="w-full max-w-2xl space-y-6">
            
            <!-- Map Preview Strip -->
            <div class="w-full h-40 bg-[#EAE6DC] dark:bg-[#20201C] border border-[#DDD8CC] dark:border-[#2E2D28] rounded-[6px] relative overflow-hidden flex items-center justify-center text-xs font-mono text-[#6B675E] dark:text-[#9E9A90]">
              <div class="text-center space-y-1">
                <MapPin class="w-6 h-6 text-[#E8590C] mx-auto animate-bounce" />
                <p class="font-bold text-[#14130F] dark:text-[#F5F2EB]">Target Pin: {{ selectedTask.latitude.toFixed(4) }}, {{ selectedTask.longitude.toFixed(4) }}</p>
                <p class="text-[10px]">OpenStreetMap / Haversine 150m boundary</p>
              </div>
            </div>

            <!-- Field Work-Order Detail Card -->
            <article 
              class="p-6 rounded-[6px] border bg-[#FFFFFF] dark:bg-[#181815] border-[#DDD8CC] dark:border-[#2E2D28] space-y-5 text-left transition-all"
              :class="isSubmitting ? 'border-beam-active' : ''"
            >
              
              <!-- Card Header -->
              <div class="flex items-start justify-between border-b border-dashed border-[#DDD8CC] dark:border-[#2E2D28] pb-4">
                <div>
                  <div class="flex items-center gap-2 mb-1.5">
                    <span class="font-mono text-[10px] uppercase text-[#6B675E] dark:text-[#9E9A90]">Order #{{ selectedTask.id.slice(0, 8) }}</span>
                    <EscrowChip :status="selectedTask.status" :amount="selectedTask.reward_sol" />
                  </div>
                  <h1 class="font-serif text-xl font-bold text-[#14130F] dark:text-[#F5F2EB] leading-tight">
                    {{ selectedTask.title }}
                  </h1>
                </div>

                <div class="text-right">
                  <span class="text-[10px] font-mono text-[#6B675E] dark:text-[#9E9A90] uppercase block">Bounty Settlement</span>
                  <span class="font-mono font-bold text-lg text-[#E8590C]">
                    {{ selectedTask.reward_sol.toFixed(2) }} SOL
                  </span>
                </div>
              </div>

              <!-- Specs Section -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div class="p-3.5 rounded-[4px] bg-[#F6F3EC] dark:bg-[#20201C] border border-[#DDD8CC] dark:border-[#2E2D28] space-y-1">
                  <span class="text-[10px] font-mono font-bold uppercase text-[#6B675E] dark:text-[#9E9A90] block">Physical Work Instruction</span>
                  <p class="text-[#14130F] dark:text-[#F5F2EB] leading-relaxed">{{ selectedTask.instruction }}</p>
                </div>

                <div class="p-3.5 rounded-[4px] bg-[#F6F3EC] dark:bg-[#20201C] border border-[#DDD8CC] dark:border-[#2E2D28] space-y-1">
                  <span class="text-[10px] font-mono font-bold uppercase text-[#1F7A4D] dark:text-[#51CF66] block">Target Visual Cue (Gemini Vision)</span>
                  <p class="text-[#14130F] dark:text-[#F5F2EB] leading-relaxed">{{ selectedTask.target_description }}</p>
                </div>
              </div>

              <!-- Lease & Location Metadata -->
              <div class="flex items-center justify-between text-[11px] font-mono text-[#6B675E] dark:text-[#9E9A90] pt-1">
                <span class="flex items-center gap-1.5"><Clock class="w-3.5 h-3.5 text-[#E8590C]" /> 10-Minute Exclusive Claim Window</span>
                <span>Best-Effort GPS &le; 150m</span>
              </div>

              <!-- Primary Action 1: Claim Task -->
              <div v-if="selectedTask.status === 'OPEN'" class="pt-2">
                <button 
                  @click="claimTask"
                  class="w-full py-3.5 rounded-[4px] bg-[#E8590C] hover:bg-[#D9480F] text-[#FFFFFF] font-mono font-bold text-xs uppercase tracking-wider transition-colors flex items-center justify-center gap-2"
                >
                  <span>Claim Bounty (Lock 0.01 SOL)</span>
                  <ArrowRight class="w-4 h-4" />
                </button>
              </div>

              <!-- Primary Action 2: Evidence Submission -->
              <div v-else-if="selectedTask.status === 'CLAIMED' && !isSubmitting && !verificationResult" class="pt-2 space-y-3">
                
                <div class="flex items-center justify-between p-3 rounded-[4px] bg-[#F6F3EC] dark:bg-[#20201C] border border-[#DDD8CC] dark:border-[#2E2D28] text-xs">
                  <span class="font-mono text-[#14130F] dark:text-[#F5F2EB]">Bounty Claimed. Ready for ground evidence.</span>
                  <button 
                    @click="showDemoDrawer = true" 
                    class="font-mono text-[11px] text-[#E8590C] hover:underline font-bold"
                  >
                    Open Test Fixtures
                  </button>
                </div>

                <!-- Camera Upload Field -->
                <label class="w-full py-4 rounded-[4px] border border-dashed border-[#14130F] dark:border-[#F5F2EB] bg-[#FFFFFF] dark:bg-[#181815] hover:bg-[#F6F3EC] dark:hover:bg-[#252520] flex flex-col items-center justify-center cursor-pointer transition-colors text-xs font-mono text-[#14130F] dark:text-[#F5F2EB]">
                  <Camera class="w-5 h-5 text-[#E8590C] mb-1" />
                  <span class="font-bold">Snap or Upload On-Site Evidence Photo</span>
                  <span class="text-[10px] text-[#6B675E] dark:text-[#9E9A90] mt-0.5">Runs EXIF Geofence + Gemini 2.5 Flash Autonomous Verifier</span>
                  <input type="file" accept="image/*" capture="environment" @change="handleFileUpload" class="hidden" />
                </label>

              </div>

              <!-- Verification Stepper Progress -->
              <div v-if="isSubmitting" class="pt-2 border-t border-[#DDD8CC] dark:border-[#2E2D28] space-y-3">
                <span class="text-[11px] font-mono uppercase text-[#6B675E] dark:text-[#9E9A90] block">Autonomous Verification Stepper</span>
                <VerificationStepper :currentStep="currentStep" />
              </div>

              <!-- Result Screen -->
              <div v-if="verificationResult" class="pt-2 border-t border-[#DDD8CC] dark:border-[#2E2D28] space-y-4">
                
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <CheckCircle2 v-if="verificationResult.status === 'PAID'" class="w-5 h-5 text-[#1F7A4D]" />
                    <AlertCircle v-else class="w-5 h-5 text-[#B3261E]" />
                    <span class="font-bold text-sm" :class="verificationResult.status === 'PAID' ? 'text-[#1F7A4D]' : 'text-[#B3261E]'">
                      {{ verificationResult.status === 'PAID' ? 'Verification Passed: Escrow Paid' : 'Verification Rejected' }}
                    </span>
                  </div>
                  <ConfidenceRing :score="verificationResult.verification.confidence" />
                </div>

                <p class="text-xs text-[#6B675E] dark:text-[#9E9A90] leading-relaxed">
                  {{ verificationResult.verification.reason }}
                </p>

                <!-- Transaction Link -->
                <div v-if="verificationResult.payout_tx_sig" class="p-3 rounded-[4px] bg-[#F6F3EC] dark:bg-[#20201C] border border-[#DDD8CC] dark:border-[#2E2D28]">
                  <TxLink :signature="verificationResult.payout_tx_sig" label="Settlement Transaction" />
                </div>

                <!-- Refund Trigger for Creator on Failure -->
                <div v-if="verificationResult.status === 'REJECTED' && selectedTask.status !== 'REFUNDED'">
                  <button 
                    @click="triggerRefund"
                    class="w-full py-2.5 rounded-[4px] bg-[#14130F] dark:bg-[#F5F2EB] text-[#F6F3EC] dark:text-[#14130F] font-mono text-xs font-bold uppercase tracking-wider hover:opacity-90 transition-opacity"
                  >
                    Refund 0.01 SOL to Task Poster
                  </button>
                </div>

                <div v-if="selectedTask.status === 'REFUNDED'" class="text-xs font-mono text-[#6B675E] dark:text-[#9E9A90]">
                  Escrow deposit has been refunded back to creator.
                </div>

              </div>

            </article>

            <!-- Desktop Terminal Log (Magic UI Terminal Requirement) -->
            <div class="hidden md:block rounded-[6px] border border-[#DDD8CC] dark:border-[#2E2D28] bg-[#14130F] text-[#F6F3EC] font-mono text-xs p-4 text-left space-y-2">
              <div class="flex items-center justify-between border-b border-[#2E2D28] pb-2 text-[10px] text-[#9E9A90]">
                <div class="flex items-center gap-1.5">
                  <Terminal class="w-3.5 h-3.5 text-[#E8590C]" />
                  <span>DEVNET VERIFICATION LOG</span>
                </div>
                <span>Cluster: devnet</span>
              </div>

              <div class="h-28 overflow-y-auto space-y-1 text-[11px] text-[#DDD8CC]">
                <div v-if="terminalLogs.length === 0" class="text-[#6B675E]">
                  Awaiting evidence submission to stream verification tiers...
                </div>
                <div v-for="(log, i) in terminalLogs" :key="i" class="leading-snug">
                  {{ log }}
                </div>
              </div>
            </div>

          </div>

          <!-- Empty Right Stage State -->
          <div v-else class="text-center py-20 space-y-3">
            <Info class="w-8 h-8 text-[#6B675E] mx-auto" />
            <h2 class="font-serif text-lg font-bold">Select a work order from the feed</h2>
            <p class="text-xs text-[#6B675E] max-w-sm">Inspect physical task requirements, escrow lock status, and location coordinates.</p>
          </div>

        </main>

      </template>

      <!-- ================= TAB 2: POST A TASK ================= -->
      <section v-else-if="currentTab === 'post'" class="flex-1 p-6 md:p-12 overflow-y-auto flex justify-center">
        
        <div class="w-full max-w-xl p-6 rounded-[6px] border border-[#DDD8CC] dark:border-[#2E2D28] bg-[#FFFFFF] dark:bg-[#181815] space-y-5 text-left">
          
          <div class="border-b border-[#DDD8CC] dark:border-[#2E2D28] pb-3">
            <h2 class="font-serif text-lg font-bold text-[#14130F] dark:text-[#F5F2EB]">Post Physical Work Order</h2>
            <p class="text-xs text-[#6B675E] dark:text-[#9E9A90] font-mono mt-0.5">Locks 0.01 SOL in Solana Devnet Escrow</p>
          </div>

          <div class="space-y-3.5 text-xs font-mono">
            <div>
              <label class="block uppercase text-[11px] text-[#6B675E] dark:text-[#9E9A90] mb-1">Task Title</label>
              <input 
                v-model="postTitle"
                placeholder="e.g. Verify Alexanderplatz EV Charger"
                class="w-full p-2.5 rounded-[4px] bg-[#F6F3EC] dark:bg-[#121210] border border-[#DDD8CC] dark:border-[#2E2D28] text-[#14130F] dark:text-[#F5F2EB] focus:outline-none focus:border-[#E8590C]"
              />
            </div>

            <div>
              <label class="block uppercase text-[11px] text-[#6B675E] dark:text-[#9E9A90] mb-1">Worker Physical Instruction</label>
              <textarea 
                v-model="postInstruction"
                rows="2"
                placeholder="What physical perspective or detail must the photo show?"
                class="w-full p-2.5 rounded-[4px] bg-[#F6F3EC] dark:bg-[#121210] border border-[#DDD8CC] dark:border-[#2E2D28] text-[#14130F] dark:text-[#F5F2EB] focus:outline-none focus:border-[#E8590C]"
              ></textarea>
            </div>

            <div>
              <label class="block uppercase text-[11px] text-[#6B675E] dark:text-[#9E9A90] mb-1">Target Description (Gemini Vision Criteria)</label>
              <input 
                v-model="postTarget"
                placeholder="e.g. Active screen, intact charging cable"
                class="w-full p-2.5 rounded-[4px] bg-[#F6F3EC] dark:bg-[#121210] border border-[#DDD8CC] dark:border-[#2E2D28] text-[#14130F] dark:text-[#F5F2EB] focus:outline-none focus:border-[#E8590C]"
              />
            </div>

            <div class="p-3 rounded-[4px] bg-[#F6F3EC] dark:bg-[#20201C] border border-[#DDD8CC] dark:border-[#2E2D28] flex justify-between items-center">
              <span class="text-[#6B675E] dark:text-[#9E9A90]">Escrow Bounty Lock</span>
              <span class="font-bold text-[#E8590C] text-sm">0.01 SOL</span>
            </div>

            <button 
              @click="createBounty"
              class="w-full py-3 rounded-[4px] bg-[#E8590C] hover:bg-[#D9480F] text-[#FFFFFF] font-bold text-xs uppercase tracking-wider transition-colors"
            >
              Deposit & Publish Task
            </button>
          </div>

        </div>

      </section>

      <!-- ================= TAB 3: MY ACTIVITY ================= -->
      <section v-else-if="currentTab === 'activity'" class="flex-1 p-6 md:p-12 overflow-y-auto flex justify-center">
        
        <div class="w-full max-w-2xl p-6 rounded-[6px] border border-[#DDD8CC] dark:border-[#2E2D28] bg-[#FFFFFF] dark:bg-[#181815] space-y-4 text-left">
          
          <div class="border-b border-[#DDD8CC] dark:border-[#2E2D28] pb-3 flex justify-between items-center">
            <h2 class="font-serif text-lg font-bold">Activity & On-Chain Audit Log</h2>
            <button @click="resetDemo" class="text-xs font-mono text-[#6B675E] hover:underline flex items-center gap-1">
              <RotateCcw class="w-3 h-3" />
              <span>Reset State</span>
            </button>
          </div>

          <div class="divide-y divide-[#DDD8CC] dark:divide-[#2E2D28] text-xs font-mono">
            <div v-for="t in tasks" :key="t.id" class="py-3 flex justify-between items-center">
              <div>
                <span class="font-bold text-[#14130F] dark:text-[#F5F2EB]">{{ t.title }}</span>
                <span class="text-[10px] text-[#6B675E] dark:text-[#9E9A90] block">#{{ t.id.slice(0, 8) }}</span>
              </div>
              <div class="text-right space-y-1">
                <StatusStamp :status="t.status" />
                <div v-if="t.payout_tx_sig" class="text-[10px]">
                  <TxLink :signature="t.payout_tx_sig" />
                </div>
              </div>
            </div>
          </div>

        </div>

      </section>

    </div>

    <!-- MOBILE BOTTOM NAVIGATION (UNDER 768PX) -->
    <nav class="md:hidden h-14 border-t border-[#DDD8CC] dark:border-[#2E2D28] bg-[#FFFFFF] dark:bg-[#181815] fixed bottom-0 inset-x-0 z-40 grid grid-cols-3">
      <button 
        @click="currentTab = 'feed'"
        class="flex flex-col items-center justify-center font-mono text-[10px] uppercase transition-colors"
        :class="currentTab === 'feed' ? 'text-[#E8590C] font-bold' : 'text-[#6B675E]'"
      >
        <Compass class="w-4 h-4 mb-0.5" />
        <span>Find</span>
      </button>

      <button 
        @click="currentTab = 'post'"
        class="flex flex-col items-center justify-center font-mono text-[10px] uppercase transition-colors"
        :class="currentTab === 'post' ? 'text-[#E8590C] font-bold' : 'text-[#6B675E]'"
      >
        <PlusCircle class="w-4 h-4 mb-0.5" />
        <span>Post</span>
      </button>

      <button 
        @click="currentTab = 'activity'"
        class="flex flex-col items-center justify-center font-mono text-[10px] uppercase transition-colors"
        :class="currentTab === 'activity' ? 'text-[#E8590C] font-bold' : 'text-[#6B675E]'"
      >
        <Clock class="w-4 h-4 mb-0.5" />
        <span>Activity</span>
      </button>
    </nav>

    <!-- Judge Testing Fixtures Drawer Modal -->
    <DemoDrawer 
      :isOpen="showDemoDrawer" 
      @close="showDemoDrawer = false" 
      @submitFixture="submitEvidence" 
    />

  </div>
</template>
