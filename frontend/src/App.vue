<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useWallet } from './composables/useWallet'
import TaskRow from './components/TaskRow.vue'
import StatusWord from './components/StatusWord.vue'
import RewardLine from './components/RewardLine.vue'
import VerificationSteps from './components/VerificationSteps.vue'
import DemoToolsDrawer from './components/DemoToolsDrawer.vue'
import MapCanvas from './components/MapCanvas.vue'
import LandingPage from './components/LandingPage.vue'
import TxLink from './components/TxLink.vue'
import PostTaskForm from './components/PostTaskForm.vue'
import TaskFilters from './components/TaskFilters.vue'
import LocationPermissionCard from './components/LocationPermissionCard.vue'
import WalletModal from './components/WalletModal.vue'

import {
  ArrowLeft,
  Camera,
  Search,
  CheckCircle2,
  AlertCircle,
  FlaskConical,
  RotateCcw,
  Wallet
} from 'lucide-vue-next'

const { publicKey, balance, initWallet, fetchFaucet } = useWallet()

interface Task {
  id: string
  title: string
  category?: string
  instruction: string
  target_description: string
  forbidden_description?: string
  place_name?: string
  full_address?: string
  city?: string
  country?: string
  latitude: number
  longitude: number
  radius_meters?: number
  photos_required?: number
  finish_window_minutes?: number
  reward_sol: number
  poster_address: string
  status: string
  reference_photo_url?: string
  fund_tx_sig?: string
  payout_tx_sig?: string
  refund_tx_sig?: string
}

// Navigation & Modals
const showLanding = ref(false)
const currentTab = ref<'feed' | 'post' | 'activity'>('feed')
const showDemoDrawer = ref(false)
const showWalletModal = ref(false)
const showLocationPrompt = ref(true)
const activeWalletProvider = ref('demo')

// Activity Tab Filter
const activityTab = ref<'ALL' | 'POSTED' | 'WORKING' | 'COMPLETED'>('ALL')
const activitySelectedTask = ref<Task | null>(null)

// Tasks & Filters
const tasks = ref<Task[]>([])
const selectedTask = ref<Task | null>(null)
const loading = ref(false)
const submittingPost = ref(false)
const searchQuery = ref('')
const filterStatus = ref('ALL')
const filterCategory = ref('ALL')
const filterCity = ref('ALL')

// Claim & Verification Flow
const isSubmitting = ref(false)
const verificationResult = ref<any>(null)
const currentStep = ref<number>(0)

const fetchTasks = async () => {
  loading.value = true
  try {
    let url = '/api/tasks?'
    if (filterStatus.value !== 'ALL') url += `status=${filterStatus.value}&`
    if (filterCategory.value !== 'ALL') url += `category=${filterCategory.value}&`
    if (filterCity.value !== 'ALL') url += `city=${filterCity.value}&`
    if (searchQuery.value) url += `search=${encodeURIComponent(searchQuery.value)}&`

    const res = await fetch(url)
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

const handleUseLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      () => {
        showLocationPrompt.value = false
        filterCity.value = 'Berlin'
        fetchTasks()
      },
      () => {
        showLocationPrompt.value = false
      }
    )
  }
}

const handleSelectCity = (city: string) => {
  filterCity.value = city
  fetchTasks()
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
  showDemoDrawer.value = false
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
    showDemoDrawer.value = false
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleCreateTask = async (payload: any) => {
  submittingPost.value = true
  try {
    await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    fetchTasks()
    currentTab.value = 'feed'
  } catch (e) {
    console.error(e)
  } finally {
    submittingPost.value = false
  }
}

const handleSelectWallet = (providerId: string) => {
  activeWalletProvider.value = providerId
  if (providerId === 'phantom' && (window as any).solana?.isPhantom) {
    (window as any).solana.connect().then((resp: any) => {
      publicKey.value = resp.publicKey.toString()
    }).catch(console.error)
  }
  showWalletModal.value = false
}

const filteredActivityTasks = computed(() => {
  if (activityTab.value === 'ALL') return tasks.value
  if (activityTab.value === 'POSTED') return tasks.value.filter(t => t.poster_address === publicKey.value)
  if (activityTab.value === 'WORKING') return tasks.value.filter(t => t.status === 'CLAIMED')
  if (activityTab.value === 'COMPLETED') return tasks.value.filter(t => t.status === 'PAID' || t.status === 'REFUNDED')
  return tasks.value
})

onMounted(() => {
  initWallet()
  fetchTasks()
})
</script>

<template>
  <LandingPage v-if="showLanding" @startApp="showLanding = false" />

  <div v-else class="h-screen w-screen flex flex-col bg-[#F7F5F0] text-[#1A1A17] overflow-hidden">
    
    <!-- TOP BAR (SHARED FULL-WIDTH SHELL) -->
    <header class="h-14 bg-white border-b border-[#E3DFD6] px-4 md:px-6 flex items-center justify-between shrink-0 z-20">
      
      <!-- Brand & Tabs -->
      <div class="flex items-center gap-6">
        <div class="flex items-center gap-2 cursor-pointer" @click="showLanding = true">
          <span class="font-bold text-[17px] tracking-tight">BountyBlink</span>
          <span class="text-[12px] text-[#5E5B53]">Devnet</span>
        </div>

        <nav class="hidden md:flex items-center gap-5 text-[15px]">
          <button 
            @click="currentTab = 'feed'"
            class="font-medium transition-colors"
            :class="currentTab === 'feed' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
          >
            Find tasks
          </button>
          <button 
            @click="currentTab = 'post'"
            class="font-medium transition-colors"
            :class="currentTab === 'post' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
          >
            Post a task
          </button>
          <button 
            @click="currentTab = 'activity'"
            class="font-medium transition-colors"
            :class="currentTab === 'activity' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
          >
            My activity
          </button>
        </nav>
      </div>

      <!-- Controls: Demo tools & Wallet Chip -->
      <div class="flex items-center gap-3">
        <button 
          @click="showDemoDrawer = true"
          class="h-8 px-3 rounded-[12px] bg-[#F7F5F0] hover:bg-[#EAE6DC] text-[#1A1A17] text-[13px] font-medium flex items-center gap-1.5 transition-colors"
        >
          <FlaskConical class="w-3.5 h-3.5" />
          <span>Demo tools</span>
        </button>

        <button 
          @click="showWalletModal = true"
          class="flex items-center gap-2 text-[13px] hover:bg-[#F7F5F0] px-2 py-1 rounded-[8px] transition-colors"
        >
          <Wallet class="w-3.5 h-3.5 text-[#5E5B53]" />
          <span class="font-mono text-[#5E5B53] hidden sm:inline">{{ publicKey.slice(0, 4) }}...{{ publicKey.slice(-4) }}</span>
          <span class="font-semibold text-[#1A1A17]">{{ balance.toFixed(2) }} SOL</span>
        </button>
      </div>

    </header>

    <!-- MAIN BODY CONTENT AREA (EDGE-TO-EDGE FULL WIDTH) -->
    <div class="flex-1 flex flex-col md:flex-row overflow-hidden relative">
      
      <!-- ================= TAB 1: FIND TASKS (MAP-FIRST APP) ================= -->
      <template v-if="currentTab === 'feed'">
        
        <!-- 400px Left Panel (Single Replacement Pattern) -->
        <section class="w-full md:w-[400px] h-1/2 md:h-full bg-white md:border-r border-[#E3DFD6] flex flex-col shrink-0 z-10 shadow-xs order-2 md:order-1">
          
          <!-- DETAIL STATE IN LEFT PANEL -->
          <div v-if="selectedTask" class="h-full flex flex-col justify-between overflow-y-auto text-left">
            
            <div class="p-5 space-y-4">
              <button 
                @click="selectedTask = null"
                class="flex items-center gap-1 text-[13px] text-[#5E5B53] hover:text-[#1A1A17] font-medium"
              >
                <ArrowLeft class="w-4 h-4" />
                <span>All tasks</span>
              </button>

              <div class="space-y-1">
                <span class="text-[12px] font-semibold text-[#5E5B53] uppercase">{{ selectedTask.category || 'General' }}</span>
                <h1 class="text-[20px] font-semibold text-[#1A1A17] leading-tight">
                  {{ selectedTask.title }}
                </h1>
                <RewardLine :status="selectedTask.status" :amount="selectedTask.reward_sol" />
              </div>

              <!-- What to do & What photo should show -->
              <div class="space-y-3 pt-1 text-[15px] leading-relaxed">
                <div>
                  <h4 class="font-medium text-[#1A1A17] text-[13px]">What to do</h4>
                  <p class="text-[#5E5B53] text-[14px] mt-0.5">{{ selectedTask.instruction }}</p>
                </div>

                <div>
                  <h4 class="font-medium text-[#1A1A17] text-[13px]">What the photo should show</h4>
                  <p class="text-[#5E5B53] text-[14px] mt-0.5">{{ selectedTask.target_description }}</p>
                </div>

                <div v-if="selectedTask.forbidden_description">
                  <h4 class="font-medium text-[#B42318] text-[13px]">What the photo must not show</h4>
                  <p class="text-[#5E5B53] text-[14px] mt-0.5">{{ selectedTask.forbidden_description }}</p>
                </div>

                <div class="pt-2 border-t border-[#E3DFD6] text-[13px] text-[#5E5B53] space-y-1">
                  <div>Take the photo within {{ selectedTask.radius_meters || 150 }} m of the pin.</div>
                  <div>You have {{ selectedTask.finish_window_minutes || 10 }} minutes to submit after claiming.</div>
                </div>
              </div>

              <!-- Live Verification checking steps -->
              <div v-if="isSubmitting || verificationResult" class="pt-3 border-t border-[#E3DFD6]">
                <h4 class="font-medium text-[#1A1A17] text-[13px] mb-2">Verification</h4>
                <VerificationSteps 
                  :currentStep="currentStep" 
                  :status="verificationResult?.status"
                  :txSig="verificationResult?.payout_tx_sig"
                  :reason="verificationResult?.verification?.reason"
                />
              </div>

              <!-- Result verdict box -->
              <div v-if="verificationResult" class="pt-2">
                <div 
                  class="p-3.5 rounded-[12px] text-[14px] space-y-1.5"
                  :class="verificationResult.status === 'PAID' ? 'bg-[#EBF5EF] text-[#1E7B4F]' : 'bg-[#FAECEB] text-[#B42318]'"
                >
                  <div class="flex items-center gap-1.5 font-semibold">
                    <CheckCircle2 v-if="verificationResult.status === 'PAID'" class="w-4 h-4" />
                    <AlertCircle v-else class="w-4 h-4" />
                    <span>{{ verificationResult.status === 'PAID' ? 'Paid' : 'Not approved' }}</span>
                  </div>
                  <p class="text-[13px] leading-snug">{{ verificationResult.verification.reason }}</p>
                </div>

                <div v-if="verificationResult.status === 'REJECTED' && selectedTask.status !== 'REFUNDED'" class="pt-2">
                  <button 
                    @click="triggerRefund"
                    class="w-full py-2.5 rounded-[12px] bg-[#1A1A17] text-white text-[13px] font-medium"
                  >
                    Refund reward to poster
                  </button>
                </div>
              </div>

            </div>

            <!-- Sticky Bottom Action Button -->
            <div class="p-4 border-t border-[#E3DFD6] bg-white sticky bottom-0">
              <button 
                v-if="selectedTask.status === 'OPEN'"
                @click="claimTask"
                class="w-full h-12 rounded-[12px] bg-[#FFD60A] hover:brightness-95 text-[#1A1A17] font-semibold text-[15px] transition-all flex items-center justify-center shadow-xs"
              >
                Claim this task
              </button>

              <label 
                v-else-if="selectedTask.status === 'CLAIMED' && !isSubmitting && !verificationResult"
                class="w-full h-12 rounded-[12px] bg-[#FFD60A] hover:brightness-95 text-[#1A1A17] font-semibold text-[15px] transition-all flex items-center justify-center gap-2 cursor-pointer shadow-xs"
              >
                <Camera class="w-4 h-4" />
                <span>Take or upload photo</span>
                <input type="file" accept="image/*" capture="environment" @change="handleFileUpload" class="hidden" />
              </label>

              <button 
                v-else-if="verificationResult"
                @click="selectedTask = null"
                class="w-full h-12 rounded-[12px] bg-[#F7F5F0] text-[#1A1A17] font-medium text-[15px] transition-all flex items-center justify-center"
              >
                Find another task
              </button>
            </div>

          </div>

          <!-- LIST STATE IN LEFT PANEL -->
          <div v-else class="h-full flex flex-col overflow-hidden text-left">
            
            <div class="p-4 border-b border-[#E3DFD6] space-y-3 shrink-0">
              <h2 class="text-[17px] font-semibold text-[#1A1A17]">Tasks near you</h2>
              
              <!-- Location Permission Card -->
              <LocationPermissionCard 
                :show="showLocationPrompt"
                :activeCity="filterCity"
                @useLocation="handleUseLocation"
                @selectCity="handleSelectCity"
                @dismiss="showLocationPrompt = false"
              />

              <!-- Search -->
              <div class="relative">
                <Search class="w-4 h-4 text-[#5E5B53] absolute left-3 top-2.5" />
                <input 
                  v-model="searchQuery"
                  @input="fetchTasks"
                  placeholder="Search title, place, address..." 
                  class="w-full pl-9 pr-3 py-1.5 text-[14px] bg-[#F7F5F0] border border-[#E3DFD6] rounded-[8px] text-[#1A1A17] placeholder-[#5E5B53] focus:outline-none focus:border-[#1A1A17]"
                />
              </div>

              <!-- Filter Bar (Categories, Cities, Status) -->
              <TaskFilters 
                v-model:status="filterStatus"
                v-model:category="filterCategory"
                v-model:city="filterCity"
                @update:status="fetchTasks"
                @update:category="fetchTasks"
                @update:city="fetchTasks"
              />
            </div>

            <!-- List rows -->
            <div class="flex-1 overflow-y-auto divide-y divide-[#E3DFD6]">
              <TaskRow 
                v-for="task in (tasks as any[])" 
                :key="task.id"
                :task="task"
                :isSelected="Boolean(selectedTask && (selectedTask as any).id === task.id)"
                @select="selectTask(task)"
              />

              <div v-if="tasks.length === 0" class="p-8 text-center text-[#5E5B53] text-[14px]">
                No tasks match your filters. Try picking another city or resetting filters.
              </div>
            </div>

          </div>

        </section>

        <!-- Full-bleed Map Canvas -->
        <main class="flex-1 h-1/2 md:h-full relative order-1 md:order-2">
          <MapCanvas 
            :tasks="tasks" 
            :selectedTask="selectedTask" 
            @selectTask="selectTask"
          />
        </main>

      </template>

      <!-- ================= TAB 2: POST A TASK (FULL-WIDTH 60/40 LIVE PREVIEW) ================= -->
      <section v-else-if="currentTab === 'post'" class="flex-1 p-6 md:p-8 overflow-y-auto flex justify-center bg-[#F7F5F0]">
        
        <div class="w-full max-w-6xl grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          
          <!-- Left 60%: Sectioned Form -->
          <div class="md:col-span-7">
            <PostTaskForm 
              :userAddress="publicKey"
              :submitting="submittingPost"
              @createTask="handleCreateTask"
            />
          </div>

          <!-- Right 40%: Sticky Live Preview -->
          <div class="md:col-span-5 sticky top-6 space-y-4 text-left">
            <div class="bg-white p-5 rounded-[16px] border border-[#E3DFD6] shadow-xs space-y-3">
              <span class="text-[12px] font-semibold text-[#5E5B53] uppercase">Live task preview</span>
              
              <div class="h-44 bg-[#F7F5F0] rounded-[10px] border border-[#E3DFD6] overflow-hidden">
                <MapCanvas 
                  :tasks="tasks" 
                  :selectedTask="selectedTask" 
                />
              </div>

              <div class="p-3 bg-[#F7F5F0] rounded-[8px] space-y-1 text-[13px]">
                <div class="font-semibold text-[#1A1A17]">Verification rules</div>
                <div class="text-[#5E5B53]">Radius boundary: 150 meters &middot; Multimodal vision inspection enabled.</div>
              </div>
            </div>
          </div>

        </div>

      </section>

      <!-- ================= TAB 3: MY ACTIVITY (FULL-WIDTH LIST + DETAIL DRAWER) ================= -->
      <section v-else-if="currentTab === 'activity'" class="flex-1 p-6 md:p-8 overflow-y-auto flex justify-center bg-[#F7F5F0]">
        
        <div class="w-full max-w-5xl bg-white p-6 md:p-8 rounded-[16px] border border-[#E3DFD6] shadow-xs space-y-5 text-left">
          
          <div class="flex justify-between items-center border-b border-[#E3DFD6] pb-4">
            <div>
              <h2 class="text-[20px] font-bold text-[#1A1A17]">My activity</h2>
              <p class="text-[13px] text-[#5E5B53]">Audit on-chain escrow releases and refunds</p>
            </div>
            <button @click="resetDemo" class="text-[13px] text-[#5E5B53] hover:text-[#1A1A17] flex items-center gap-1 font-medium">
              <RotateCcw class="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          </div>

          <!-- Sub-tabs: Posted, Working, Completed -->
          <div class="flex items-center gap-2 border-b border-[#E3DFD6] pb-3 text-[13px]">
            <button 
              @click="activityTab = 'ALL'"
              class="px-3 py-1.5 rounded-[8px] font-medium transition-colors"
              :class="activityTab === 'ALL' ? 'bg-[#1A1A17] text-white' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
            >
              All ({{ tasks.length }})
            </button>
            <button 
              @click="activityTab = 'POSTED'"
              class="px-3 py-1.5 rounded-[8px] font-medium transition-colors"
              :class="activityTab === 'POSTED' ? 'bg-[#1A1A17] text-white' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
            >
              Posted by me
            </button>
            <button 
              @click="activityTab = 'WORKING'"
              class="px-3 py-1.5 rounded-[8px] font-medium transition-colors"
              :class="activityTab === 'WORKING' ? 'bg-[#1A1A17] text-white' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
            >
              In progress
            </button>
            <button 
              @click="activityTab = 'COMPLETED'"
              class="px-3 py-1.5 rounded-[8px] font-medium transition-colors"
              :class="activityTab === 'COMPLETED' ? 'bg-[#1A1A17] text-white' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
            >
              Completed
            </button>
          </div>

          <!-- Activity Rows -->
          <div class="divide-y divide-[#E3DFD6] text-[15px]">
            <div 
              v-for="t in filteredActivityTasks" 
              :key="t.id" 
              @click="activitySelectedTask = t"
              class="py-3.5 flex justify-between items-center cursor-pointer hover:bg-[#F7F5F0] px-3 rounded-[8px] transition-colors"
            >
              <div>
                <h4 class="font-medium text-[#1A1A17]">{{ t.title }}</h4>
                <div class="flex items-center gap-2 text-[13px] text-[#5E5B53]">
                  <span>{{ t.category || 'General' }}</span>
                  <span>&middot;</span>
                  <span>{{ t.city || 'Berlin' }}</span>
                  <span>&middot;</span>
                  <span class="font-semibold text-[#1A1A17]">{{ t.reward_sol.toFixed(2) }} SOL</span>
                </div>
              </div>
              <div class="text-right space-y-1">
                <StatusWord :status="t.status" />
                <div v-if="t.payout_tx_sig" class="text-[12px]">
                  <TxLink :signature="t.payout_tx_sig" />
                </div>
              </div>
            </div>
          </div>

        </div>

      </section>

    </div>

    <!-- Mobile Bottom Tab Bar -->
    <nav class="md:hidden h-14 bg-white border-t border-[#E3DFD6] grid grid-cols-3 shrink-0 z-20">
      <button 
        @click="currentTab = 'feed'"
        class="flex flex-col items-center justify-center text-[12px]"
        :class="currentTab === 'feed' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53]'"
      >
        <span>Find</span>
      </button>

      <button 
        @click="currentTab = 'post'"
        class="flex flex-col items-center justify-center text-[12px]"
        :class="currentTab === 'post' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53]'"
      >
        <span>Post</span>
      </button>

      <button 
        @click="currentTab = 'activity'"
        class="flex flex-col items-center justify-center text-[12px]"
        :class="currentTab === 'activity' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53]'"
      >
        <span>Activity</span>
      </button>
    </nav>

    <!-- Modals & Drawers -->
    <DemoToolsDrawer 
      :isOpen="showDemoDrawer" 
      @close="showDemoDrawer = false" 
      @submitFixture="submitEvidence" 
      @reset="resetDemo"
      @faucet="fetchFaucet"
    />

    <WalletModal 
      :isOpen="showWalletModal"
      :currentAddress="publicKey"
      :balance="balance"
      :connectedProvider="activeWalletProvider"
      @close="showWalletModal = false"
      @selectWallet="handleSelectWallet"
      @disconnect="publicKey = ''"
    />

  </div>
</template>
