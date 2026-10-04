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
import UserProfileModal from './components/UserProfileModal.vue'
import EmptyState from './components/EmptyState.vue'
import { useSolPrice } from './composables/useSolPrice'

import ProfileView from './components/ProfileView.vue'
import { useGuildSocket, type GuildEvent } from './composables/useGuildSocket'

import {
  ArrowLeft,
  Camera,
  Search,
  CheckCircle2,
  AlertCircle,
  FlaskConical,
  RotateCcw,
  Wallet,
  User,
  ShieldCheck,
  Shield,
  Scroll
} from 'lucide-vue-next'

const { 
  publicKey, 
  balance, 
  isConnecting, 
  userProfile, 
  isNewUser, 
  initWallet, 
  connectPhantom, 
  fetchFaucet, 
  refreshProfile, 
  sendEscrowDepositTransaction,
  disconnect 
} = useWallet()

const { getUsdValue } = useSolPrice()

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
const currentTab = ref<'feed' | 'post' | 'activity' | 'profile'>('feed')
const showDemoDrawer = ref(false)
const showWalletModal = ref(false)
const showProfileModal = ref(false)
const showLocationPrompt = ref(true)

// Post a task live sticky data
const livePostData = ref<any>({
  title: '',
  category: 'Pet Rescue',
  placeName: '',
  fullAddress: '',
  city: 'Berlin',
  country: 'Germany',
  latitude: 52.5200,
  longitude: 13.4050,
  radiusMeters: 150,
  photosRequired: 1,
  finishWindowMinutes: 15,
  rewardSol: 0.02,
  instruction: '',
  targetDescription: '',
  forbiddenDescription: '',
  referencePhotos: []
})

// Activity Tab Filter & Isolated Data
const activityTab = ref<'ALL' | 'POSTED' | 'WORKING' | 'COMPLETED'>('ALL')
const activitySelectedTask = ref<Task | null>(null)
const userActivityData = ref<any>({ posted_tasks: [], claimed_tasks: [], submissions: [], pending_approvals: [] })

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

// Realtime WebSocket Listener: Auto-update on new data arrival without polling
useGuildSocket((event: GuildEvent) => {
  console.log('⚡ SolGuild Event Received:', event)
  fetchTasks()
  if (publicKey.value) {
    fetchUserActivity()
  }
})

// Clean HTML5 History Routing (No # Hash)
const syncRouteFromPath = () => {
  // Support both clean pathname and legacy hash fallback
  let path = window.location.pathname
  if (window.location.hash) {
    path = window.location.hash.replace(/^#\/?/, '/')
  }
  const parts = path.replace(/^\//, '').split('/')
  const section = parts[0]

  if (section === 'post' || section === 'issue') {
    currentTab.value = 'post'
    selectedTask.value = null
  } else if (section === 'activity') {
    currentTab.value = 'activity'
    selectedTask.value = null
    fetchUserActivity()
  } else if (section === 'profile') {
    currentTab.value = 'profile'
    selectedTask.value = null
  } else if ((section === 'tasks' || section === 'quests') && parts[1]) {
    currentTab.value = 'feed'
    const found = tasks.value.find(t => t.id === parts[1])
    if (found) selectedTask.value = found
  } else {
    currentTab.value = 'feed'
  }
}

const navigateTo = (tab: 'feed' | 'post' | 'activity' | 'profile', taskId?: string) => {
  currentTab.value = tab
  let targetUrl = '/quests'
  if (tab === 'post') {
    targetUrl = '/issue'
    selectedTask.value = null
  } else if (tab === 'activity') {
    targetUrl = '/activity'
    selectedTask.value = null
  } else if (tab === 'profile') {
    targetUrl = '/profile'
    selectedTask.value = null
  } else if (tab === 'feed') {
    if (taskId) {
      targetUrl = `/quests/${taskId}`
    } else {
      selectedTask.value = null
      targetUrl = '/quests'
    }
  }

  window.history.pushState({}, '', targetUrl)
}

const fetchUserActivity = async () => {
  if (!publicKey.value) return
  try {
    const res = await fetch(`/api/user/${publicKey.value}/activity`)
    if (res.ok) {
      userActivityData.value = await res.json()
    }
  } catch (e) {
    console.error('Error fetching user activity:', e)
  }
}

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
    // Do NOT auto-select tasks[0] by default to ensure feed overview is shown first
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
  navigateTo('feed', task.id)
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
  
  if (!publicKey.value) {
    showWalletModal.value = true
    return
  }

  if (!userProfile.value?.is_email_verified) {
    showProfileModal.value = true
    return
  }

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
      if (res.status === 403) {
        showProfileModal.value = true
      }
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
  if (!publicKey.value) {
    showWalletModal.value = true
    return
  }

  if (!userProfile.value?.is_email_verified) {
    showProfileModal.value = true
    return
  }

  submittingPost.value = true
  try {
    // 1. Get escrow vault public key from backend
    const healthRes = await fetch('/api/health')
    const healthData = await healthRes.json()
    const escrowPubkey = healthData.escrow_pubkey || 'EscrowVault11111111111111111111111111111111'

    // 2. Prompt Phantom wallet to sign and broadcast on-chain SOL escrow transfer
    let fundTxSig = ''
    try {
      fundTxSig = await sendEscrowDepositTransaction(payload.reward_sol, escrowPubkey)
    } catch (txErr) {
      console.warn('Escrow deposit simulation fallback:', txErr)
      fundTxSig = `DEVNET_TX_${Date.now()}_${publicKey.value.slice(0, 6)}`
    }

    payload.fund_tx_sig = fundTxSig

    // 3. Post task to backend with on-chain lock transaction signature
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      await fetchTasks()
      await fetchUserActivity()
      navigateTo('activity')
    }
  } catch (e) {
    console.error(e)
  } finally {
    submittingPost.value = false
  }
}

const handleConnectPhantom = async () => {
  const connected = await connectPhantom()
  if (connected) {
    showWalletModal.value = false
  }
}

const userActivityTasksList = computed<Task[]>(() => {
  if (!publicKey.value || !userActivityData.value) return []
  const posted: Task[] = userActivityData.value.posted_tasks || []
  const claimed: Task[] = userActivityData.value.claimed_tasks || []
  // Merge and deduplicate by task id
  const map = new Map<string, Task>()
  posted.forEach(t => map.set(t.id, t))
  claimed.forEach(t => map.set(t.id, t))
  return Array.from(map.values())
})

const activityCounts = computed(() => {
  if (!publicKey.value) return { all: 0, posted: 0, working: 0, completed: 0 }
  const allList = userActivityTasksList.value
  const posted = allList.filter(t => t.poster_address === publicKey.value).length
  const working = allList.filter(t => t.status === 'CLAIMED').length
  const completed = allList.filter(t => t.status === 'PAID' || t.status === 'REFUNDED').length
  return {
    all: allList.length,
    posted,
    working,
    completed
  }
})

const filteredActivityTasks = computed(() => {
  // If user is not logged in with Phantom, show NO tasks (strictly gated)
  if (!publicKey.value) return []

  const myAddress = publicKey.value.trim()
  const list = userActivityTasksList.value
  
  if (activityTab.value === 'ALL') {
    return list
  }
  if (activityTab.value === 'POSTED') {
    return list.filter(t => t.poster_address === myAddress)
  }
  if (activityTab.value === 'WORKING') {
    return list.filter(t => t.status === 'CLAIMED')
  }
  if (activityTab.value === 'COMPLETED') {
    return list.filter(t => t.status === 'PAID' || t.status === 'REFUNDED')
  }
  return []
})

onMounted(async () => {
  await initWallet()
  await fetchTasks()
  if (publicKey.value) {
    await fetchUserActivity()
  }
  syncRouteFromPath()
  window.addEventListener('popstate', syncRouteFromPath)
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
          <Shield class="w-5 h-5 text-[#1A1A17]" />
          <span class="font-bold text-[17px] tracking-tight">SolGuild</span>
          <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-[#FFD60A] text-[#1A1A17]">Devnet</span>
        </div>

        <nav class="hidden md:flex items-center gap-5 text-[15px]">
          <button 
            @click="navigateTo('feed')"
            class="font-medium transition-colors"
            :class="currentTab === 'feed' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
          >
            Guild Quests
          </button>
          <button 
            @click="navigateTo('post')"
            class="font-medium transition-colors"
            :class="currentTab === 'post' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
          >
            Issue a Quest
          </button>
          <button 
            @click="navigateTo('activity')"
            class="font-medium transition-colors"
            :class="currentTab === 'activity' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
          >
            Activity
          </button>
          <button 
            @click="navigateTo('profile')"
            class="font-medium transition-colors flex items-center gap-1.5"
            :class="currentTab === 'profile' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
          >
            <span>Guild License</span>
            <span v-if="userActivityData?.pending_approvals?.length" class="px-1.5 py-0.2 text-[10px] font-bold rounded-full bg-[#FFD60A] text-[#1A1A17]">
              {{ userActivityData.pending_approvals.length }}
            </span>
          </button>
        </nav>
      </div>

      <!-- Controls: Demo tools, Profile trigger & Wallet Chip -->
      <div class="flex items-center gap-2.5">
        <button 
          @click="showDemoDrawer = true"
          class="h-8 px-3 rounded-[12px] bg-[#F7F5F0] hover:bg-[#EAE6DC] text-[#1A1A17] text-[13px] font-medium flex items-center gap-1.5 transition-colors"
        >
          <FlaskConical class="w-3.5 h-3.5" />
          <span>Demo tools</span>
        </button>

        <button 
          v-if="publicKey"
          @click="showProfileModal = true"
          class="h-8 px-2.5 rounded-[10px] bg-[#F7F5F0] hover:bg-[#EAE6DC] text-[#1A1A17] text-[13px] font-medium flex items-center gap-1.5 transition-colors border border-[#E3DFD6]"
          title="Manage name & email verification"
        >
          <User class="w-3.5 h-3.5 text-[#5E5B53]" />
          <span>Profile</span>
          <ShieldCheck v-if="userProfile?.is_email_verified" class="w-3.5 h-3.5 text-[#1E7B4F]" />
          <span v-else class="w-2 h-2 rounded-full bg-[#B42318]"></span>
        </button>

        <!-- Connect / Join / Wallet Chip -->
        <button 
          v-if="!publicKey"
          @click="showWalletModal = true"
          class="h-8 px-3.5 rounded-[10px] bg-[#FFD60A] hover:bg-[#F2CA00] text-[#1A1A17] text-[13px] font-semibold flex items-center gap-1.5 transition-transform active:scale-95 cursor-pointer shadow-xs"
        >
          <Wallet class="w-3.5 h-3.5 text-[#1A1A17]" />
          <span>Join / Connect</span>
        </button>

        <button 
          v-else
          @click="showWalletModal = true"
          class="flex items-center gap-2 text-[13px] bg-[#F7F5F0] hover:bg-[#EAE6DC] px-2.5 py-1 rounded-[10px] border border-[#E3DFD6] transition-colors"
        >
          <span class="w-2 h-2 rounded-full bg-[#1E7B4F]"></span>
          <span class="font-mono text-[#5E5B53] hidden sm:inline">{{ publicKey.slice(0, 4) }}...{{ publicKey.slice(-4) }}</span>
          <span class="font-semibold text-[#1A1A17]">{{ balance.toFixed(3) }} SOL</span>
          <span class="text-[#5E5B53] text-[11px] hidden md:inline">({{ getUsdValue(balance) }})</span>
        </button>
      </div>

    </header>

    <!-- MAIN BODY CONTENT AREA (EDGE-TO-EDGE FULL WIDTH) -->
    <div class="flex-1 flex flex-col md:flex-row overflow-hidden relative">
      
      <!-- ================= TAB 1: FIND TASKS (MAP-FIRST APP) ================= -->
      <template v-if="currentTab === 'feed'">
        
        <!-- Left Panel (+20% width for location & filter breathing room) -->
        <section class="w-full md:w-[550px] lg:w-[580px] xl:w-[600px] h-1/2 md:h-full bg-white md:border-r border-[#E3DFD6] flex flex-col shrink-0 z-10 shadow-xs order-2 md:order-1">
          
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

              <EmptyState 
                v-if="tasks.length === 0 && !loading"
                title="No tasks match your criteria"
                description="We couldn't find any bounties matching your search or location filters. Try switching cities or clearing filters."
                actionLabel="Reset filters"
                @action="filterStatus = 'ALL'; filterCategory = 'ALL'; filterCity = 'ALL'; searchQuery = ''; fetchTasks()"
              />
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

      <!-- ================= TAB 2: ISSUE A QUEST (EDGE-TO-EDGE EQUAL-HEIGHT SPLIT SCREEN) ================= -->
      <section v-else-if="currentTab === 'post'" class="flex-1 flex flex-col md:flex-row overflow-hidden bg-white text-left">
        
        <!-- Left: Balanced 3-Stage Wizard (Full height, scrollable) -->
        <div class="flex-1 overflow-y-auto border-r border-[#E3DFD6] p-6 md:p-8 flex justify-center bg-[#F7F5F0]">
          <div class="w-full max-w-2xl bg-white p-6 md:p-8 rounded-[16px] border border-[#E3DFD6] shadow-xs">
            <PostTaskForm 
              :userAddress="publicKey"
              :submitting="submittingPost"
              @createTask="handleCreateTask"
              @updateFormData="(data) => livePostData = data"
            />
          </div>
        </div>

        <!-- Right: Live 12-Item Specification Review Board (Full height, scrollable, equal balance) -->
        <aside class="w-full md:w-[480px] lg:w-[520px] bg-[#F7F5F0] overflow-y-auto p-6 space-y-4 shrink-0 border-t md:border-t-0 md:border-l border-[#E3DFD6]">
          <div class="bg-white p-5 rounded-[16px] border border-[#E3DFD6] shadow-xs space-y-4">
            <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-2.5">
              <div class="flex items-center gap-1.5">
                <Scroll class="w-4 h-4 text-[#FFD60A]" />
                <span class="text-[12px] font-bold text-[#1A1A17] uppercase tracking-wider">Quest Parchment Spec</span>
              </div>
              <span class="text-[11px] font-mono font-semibold px-2 py-0.5 rounded-full bg-[#EBF5EF] text-[#1E7B4F]">Solana Devnet</span>
            </div>
            
            <!-- Mini map of target coordinate -->
            <div class="h-44 bg-[#F7F5F0] rounded-[10px] border border-[#E3DFD6] overflow-hidden relative">
              <MapCanvas 
                :tasks="tasks" 
                :selectedTask="selectedTask" 
              />
              <div class="absolute bottom-2 left-2 px-2 py-0.5 bg-white/90 backdrop-blur rounded text-[11px] font-medium text-[#1A1A17] shadow-xs">
                📍 Target Area
              </div>
            </div>

            <!-- Complete 12-Item Field Specification Grid -->
            <div class="grid grid-cols-2 gap-2.5 text-[12px]">
              <!-- 1. Title -->
              <div class="col-span-2 p-2.5 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">1. Quest Title</span>
                <div class="font-semibold text-[#1A1A17] text-[13px] leading-tight">
                  {{ livePostData.title || '-' }}
                </div>
              </div>

              <!-- 2. Category -->
              <div class="p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">2. Category</span>
                <div class="font-medium text-[#1A1A17]">{{ livePostData.category || '-' }}</div>
              </div>

              <!-- 3. Escrow Deposit -->
              <div class="p-2 bg-[#FFFBEA] border border-[#FFD60A]/60 rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">3. Escrow Bounty</span>
                <div class="font-bold text-[#1A1A17]">
                  {{ livePostData.rewardSol ? `${livePostData.rewardSol.toFixed(2)} SOL (${getUsdValue(livePostData.rewardSol)})` : '-' }}
                </div>
              </div>

              <!-- 4. Place / Landmark -->
              <div class="p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">4. Place / Landmark</span>
                <div class="font-medium text-[#1A1A17] truncate">{{ livePostData.placeName || '-' }}</div>
              </div>

              <!-- 5. City & Country -->
              <div class="p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">5. Realm & City</span>
                <div class="font-medium text-[#1A1A17]">{{ livePostData.city && livePostData.country ? `${livePostData.city}, ${livePostData.country}` : '-' }}</div>
              </div>

              <!-- 6. Full Address -->
              <div class="col-span-2 p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">6. Waypoint Address</span>
                <div class="font-medium text-[#1A1A17] line-clamp-1">{{ livePostData.fullAddress || '-' }}</div>
              </div>

              <!-- 7. Coordinates -->
              <div class="p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">7. GPS Coordinates</span>
                <div class="font-mono text-[#1A1A17] text-[11px]">
                  {{ livePostData.latitude && livePostData.longitude ? `${livePostData.latitude.toFixed(4)}, ${livePostData.longitude.toFixed(4)}` : '-' }}
                </div>
              </div>

              <!-- 8. Boundary Radius -->
              <div class="p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">8. Discovery Radius</span>
                <div class="font-medium text-[#1A1A17]">{{ livePostData.radiusMeters ? `${livePostData.radiusMeters} meters` : '-' }}</div>
              </div>

              <!-- 9. Must Show -->
              <div class="col-span-2 p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">9. Verification Target</span>
                <div class="text-[#1A1A17]">{{ livePostData.targetDescription || '-' }}</div>
              </div>

              <!-- 10. Disqualifiers -->
              <div class="col-span-2 p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">10. Guild Disqualifiers</span>
                <div class="text-[#1A1A17]">{{ livePostData.forbiddenDescription || '-' }}</div>
              </div>

              <!-- 11. Completion Window -->
              <div class="p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">11. Quest Window</span>
                <div class="font-medium text-[#1A1A17]">{{ livePostData.finishWindowMinutes ? `${livePostData.finishWindowMinutes} min` : '-' }}</div>
              </div>

              <!-- 12. Reference Photos -->
              <div class="p-2 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
                <span class="text-[#5E5B53] text-[11px] font-medium block">12. Reference Scroll</span>
                <div class="font-medium text-[#1A1A17]">
                  {{ livePostData.referencePhotos && livePostData.referencePhotos.length > 0 ? `${livePostData.referencePhotos.length} attached` : '-' }}
                </div>
              </div>
            </div>

          </div>
        </aside>

      </section>

      <!-- ================= TAB 3: MY ACTIVITY (FULL-WIDTH EDGE-TO-EDGE + RIGHT DETAIL DRAWER) ================= -->
      <section v-else-if="currentTab === 'activity'" class="flex-1 flex flex-col md:flex-row overflow-hidden bg-white text-left">
        
        <!-- Left: Activity List Table / Rows -->
        <div class="flex-1 flex flex-col min-w-0 overflow-y-auto border-r border-[#E3DFD6]">
          
          <!-- Sticky Header inside activity pane -->
          <div class="p-4 md:p-6 border-b border-[#E3DFD6] bg-white sticky top-0 z-10 space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h1 class="text-[20px] font-bold text-[#1A1A17] tracking-tight">My activity</h1>
                <p class="text-[13px] text-[#5E5B53] mt-0.5">Audit on-chain escrow releases, verifications, and refunds</p>
              </div>
              <button 
                @click="resetDemo" 
                class="h-8 px-3 rounded-[10px] bg-[#F7F5F0] hover:bg-[#EAE6DC] text-[#1A1A17] text-[13px] font-medium flex items-center gap-1.5 transition-colors"
                title="Reset demo tasks to initial state"
              >
                <RotateCcw class="w-3.5 h-3.5" />
                <span>Reset demo</span>
              </button>
            </div>

            <!-- Segmented Sub-filters -->
            <div class="flex items-center gap-1 bg-[#F7F5F0] p-1 rounded-[10px] w-fit text-[13px]">
              <button 
                @click="activityTab = 'ALL'"
                class="px-3 py-1 rounded-[8px] font-medium transition-colors"
                :class="activityTab === 'ALL' ? 'bg-white text-[#1A1A17] shadow-xs' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
              >
                All ({{ activityCounts.all }})
              </button>
              <button 
                @click="activityTab = 'POSTED'"
                class="px-3 py-1 rounded-[8px] font-medium transition-colors"
                :class="activityTab === 'POSTED' ? 'bg-white text-[#1A1A17] shadow-xs' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
              >
                Posted by me ({{ activityCounts.posted }})
              </button>
              <button 
                @click="activityTab = 'WORKING'"
                class="px-3 py-1 rounded-[8px] font-medium transition-colors"
                :class="activityTab === 'WORKING' ? 'bg-white text-[#1A1A17] shadow-xs' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
              >
                In progress ({{ activityCounts.working }})
              </button>
              <button 
                @click="activityTab = 'COMPLETED'"
                class="px-3 py-1 rounded-[8px] font-medium transition-colors"
                :class="activityTab === 'COMPLETED' ? 'bg-white text-[#1A1A17] shadow-xs' : 'text-[#5E5B53] hover:text-[#1A1A17]'"
              >
                Completed ({{ activityCounts.completed }})
              </button>
            </div>
          </div>

          <!-- Activity Rows List -->
          <div class="divide-y divide-[#E3DFD6] flex-1">
            <div 
              v-for="t in filteredActivityTasks" 
              :key="t.id" 
              @click="activitySelectedTask = t"
              class="px-4 md:px-6 py-4 flex items-center justify-between cursor-pointer transition-colors text-left"
              :class="activitySelectedTask?.id === t.id ? 'bg-[#FFFBEA]' : 'hover:bg-[#FBF9F5]'"
            >
              <div class="min-w-0 pr-4 space-y-1">
                <div class="flex items-center gap-2">
                  <h3 class="font-medium text-[15px] text-[#1A1A17] truncate">{{ t.title }}</h3>
                  <StatusWord :status="t.status" />
                </div>
                <div class="flex items-center gap-2 text-[13px] text-[#5E5B53]">
                  <span>{{ t.category || 'General' }}</span>
                  <span>&middot;</span>
                  <span>{{ t.city || 'Berlin' }}</span>
                  <span>&middot;</span>
                  <span class="font-semibold text-[#1A1A17]">{{ t.reward_sol.toFixed(2) }} SOL</span>
                  <span class="text-[12px] text-[#5E5B53]">({{ getUsdValue(t.reward_sol) }})</span>
                </div>
              </div>

              <div class="shrink-0 flex items-center gap-3">
                <div v-if="t.payout_tx_sig" class="hidden sm:block">
                  <TxLink :signature="t.payout_tx_sig" label="Payout" />
                </div>
                <div v-else-if="t.refund_tx_sig" class="hidden sm:block">
                  <TxLink :signature="t.refund_tx_sig" label="Refund" />
                </div>
                <div class="text-[13px] text-[#5E5B53] font-medium flex items-center gap-1">
                  <span>Inspect</span>
                  <span>&rarr;</span>
                </div>
              </div>
            </div>

            <!-- Empty State when filtered activity is empty -->
            <EmptyState 
              v-if="filteredActivityTasks.length === 0"
              title="No activity recorded"
              :description="publicKey ? 'You do not have any tasks under this filter yet. Post a bounty or claim an open task in your city to get started.' : 'Connect your Phantom wallet to view your personal on-chain task history, payouts, and claims.'"
              :actionLabel="publicKey ? 'Explore open bounties' : 'Connect Phantom'"
              @action="publicKey ? navigateTo('feed') : showWalletModal = true"
            />
          </div>

        </div>

        <!-- Right: Detail Inspection Drawer (420px fixed on desktop) -->
        <aside 
          v-if="activitySelectedTask"
          class="w-full md:w-[420px] bg-[#F7F5F0] flex flex-col shrink-0 overflow-y-auto border-t md:border-t-0 md:border-l border-[#E3DFD6] p-6 space-y-5 text-left"
        >
          <div class="flex items-center justify-between">
            <span class="text-[12px] font-semibold text-[#5E5B53] uppercase tracking-wider">Escrow Audit Detail</span>
            <button 
              @click="activitySelectedTask = null"
              class="text-[13px] text-[#5E5B53] hover:text-[#1A1A17] font-medium"
            >
              Close
            </button>
          </div>

          <div class="bg-white p-5 rounded-[12px] border border-[#E3DFD6] space-y-3">
            <div class="space-y-1">
              <h2 class="text-[18px] font-semibold text-[#1A1A17] leading-snug">{{ activitySelectedTask.title }}</h2>
              <RewardLine :status="activitySelectedTask.status" :amount="activitySelectedTask.reward_sol" />
            </div>

            <div class="pt-2 border-t border-[#E3DFD6] space-y-2 text-[13px]">
              <div class="flex justify-between">
                <span class="text-[#5E5B53]">Location</span>
                <span class="font-medium text-[#1A1A17]">{{ activitySelectedTask.place_name || activitySelectedTask.city || 'Berlin' }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-[#5E5B53]">Poster</span>
                <span class="font-mono text-[#1A1A17] text-[12px]">{{ activitySelectedTask.poster_address.slice(0, 6) }}...{{ activitySelectedTask.poster_address.slice(-4) }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-[#5E5B53]">Current Status</span>
                <StatusWord :status="activitySelectedTask.status" />
              </div>
            </div>
          </div>

          <!-- On-Chain Signatures & Settlement Audit -->
          <div class="bg-white p-5 rounded-[12px] border border-[#E3DFD6] space-y-3">
            <h3 class="text-[14px] font-semibold text-[#1A1A17]">On-Chain Settlement</h3>
            
            <div class="space-y-2 text-[13px]">
              <div>
                <span class="text-[#5E5B53] block text-[11px] uppercase">Lock In Escrow Tx:</span>
                <TxLink v-if="activitySelectedTask.fund_tx_sig" :signature="activitySelectedTask.fund_tx_sig" />
                <span v-else class="text-[#5E5B53] italic">Simulated devnet genesis lock</span>
              </div>

              <div v-if="activitySelectedTask.payout_tx_sig" class="pt-2 border-t border-[#E3DFD6]">
                <span class="text-[#5E5B53] block text-[11px] uppercase">Payout Release Tx:</span>
                <TxLink :signature="activitySelectedTask.payout_tx_sig" />
              </div>

              <div v-if="activitySelectedTask.refund_tx_sig" class="pt-2 border-t border-[#E3DFD6]">
                <span class="text-[#5E5B53] block text-[11px] uppercase">Escrow Refund Tx:</span>
                <TxLink :signature="activitySelectedTask.refund_tx_sig" />
              </div>
            </div>
          </div>

          <!-- Instructions & Verification Rules -->
          <div class="bg-white p-5 rounded-[12px] border border-[#E3DFD6] space-y-2 text-[13px]">
            <h3 class="text-[14px] font-semibold text-[#1A1A17]">Task Requirements</h3>
            <p class="text-[#5E5B53]">{{ activitySelectedTask.instruction }}</p>
            <div v-if="activitySelectedTask.target_description" class="pt-2 text-[12px] text-[#5E5B53]">
              <strong class="text-[#1A1A17]">What verifier checks:</strong> {{ activitySelectedTask.target_description }}
            </div>
          </div>
        </aside>

        <!-- Empty state prompt for desktop when no task is selected -->
        <div 
          v-else 
          class="hidden md:flex w-[420px] bg-[#F7F5F0] border-l border-[#E3DFD6] shrink-0 items-center justify-center p-8 text-center text-[#5E5B53] text-[14px]"
        >
          Select an activity row to audit its on-chain settlement, verifications, and escrow status.
        </div>

      </section>

      <!-- ================= TAB 4: GUILD LICENSE & PENDING APPROVALS ================= -->
      <section v-else-if="currentTab === 'profile'" class="flex-1 flex overflow-hidden bg-white text-left">
        <ProfileView 
          :address="publicKey"
          :userProfile="userProfile"
          :balance="balance"
          @profileUpdated="refreshProfile"
          @questApproved="fetchUserActivity"
          @openQuest="(id) => navigateTo('feed', id)"
        />
      </section>

    </div>

    <!-- Mobile Bottom Tab Bar -->
    <nav class="md:hidden h-14 bg-white border-t border-[#E3DFD6] grid grid-cols-4 shrink-0 z-20">
      <button 
        @click="navigateTo('feed')"
        class="flex flex-col items-center justify-center text-[12px]"
        :class="currentTab === 'feed' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53]'"
      >
        <span>Quests</span>
      </button>

      <button 
        @click="navigateTo('post')"
        class="flex flex-col items-center justify-center text-[12px]"
        :class="currentTab === 'post' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53]'"
      >
        <span>Issue</span>
      </button>

      <button 
        @click="navigateTo('activity')"
        class="flex flex-col items-center justify-center text-[12px]"
        :class="currentTab === 'activity' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53]'"
      >
        <span>Activity</span>
      </button>

      <button 
        @click="navigateTo('profile')"
        class="flex flex-col items-center justify-center text-[12px] relative"
        :class="currentTab === 'profile' ? 'text-[#1A1A17] font-semibold' : 'text-[#5E5B53]'"
      >
        <span>License</span>
        <span v-if="userActivityData?.pending_approvals?.length" class="absolute top-2 right-4 w-2 h-2 rounded-full bg-[#FFD60A]"></span>
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
      :isConnecting="isConnecting"
      :isNewUser="isNewUser"
      :userProfile="userProfile"
      @close="showWalletModal = false"
      @connectPhantom="handleConnectPhantom"
      @faucet="fetchFaucet"
      @disconnect="disconnect"
    />

    <UserProfileModal 
      :isOpen="showProfileModal"
      :address="publicKey"
      :userProfile="userProfile"
      @close="showProfileModal = false"
      @profileUpdated="refreshProfile"
    />

  </div>
</template>
