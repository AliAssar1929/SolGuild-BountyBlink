<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Clock, CheckCircle2, AlertCircle, Check, Scroll, Shield } from 'lucide-vue-next'
import { useSolPrice } from '../composables/useSolPrice'

const props = defineProps<{
  address: string
  userProfile: any
  balance: number
}>()

const emit = defineEmits<{
  (e: 'profileUpdated'): void
  (e: 'questApproved'): void
  (e: 'openQuest', taskId: string): void
}>()

const { getUsdValue } = useSolPrice()

const nameInput = ref('')
const emailInput = ref('')
const otpCode = ref('')
const isSendingCode = ref(false)
const isVerifyingCode = ref(false)
const isSavingProfile = ref(false)
const statusMessage = ref('')
const errorMessage = ref('')

// Pending Approvals & Activity stats
const pendingApprovals = ref<any[]>([])
const loadingApprovals = ref(false)
const approvingId = ref<string | null>(null)

// 15-minute countdown (900 seconds)
const secondsLeft = ref(0)
let timer: any = null

const formattedTimer = computed(() => {
  const m = Math.floor(secondsLeft.value / 60)
  const s = secondsLeft.value % 60
  return `${m}:${s < 10 ? '0' : ''}${s}`
})

const startTimer = (seconds: number) => {
  if (timer) clearInterval(timer)
  secondsLeft.value = seconds
  timer = setInterval(() => {
    if (secondsLeft.value > 0) {
      secondsLeft.value--
    } else {
      clearInterval(timer)
    }
  }, 1000)
}

onMounted(() => {
  if (props.userProfile) {
    nameInput.value = props.userProfile.name || ''
    emailInput.value = props.userProfile.email || ''
  }
  fetchPendingApprovals()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const fetchPendingApprovals = async () => {
  if (!props.address) return
  loadingApprovals.value = true
  try {
    const res = await fetch(`/api/user/${props.address}/activity`)
    if (res.ok) {
      const data = await res.json()
      pendingApprovals.value = data.pending_approvals || []
    }
  } catch (e) {
    console.error('Error fetching pending approvals:', e)
  } finally {
    loadingApprovals.value = false
  }
}

const handleApprove = async (taskId: string) => {
  approvingId.value = taskId
  errorMessage.value = ''
  try {
    const res = await fetch(`/api/tasks/${taskId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ poster_address: props.address })
    })
    const data = await res.json()
    if (res.ok) {
      statusMessage.value = 'Bounty escrow payout released to adventurer!'
      await fetchPendingApprovals()
      emit('questApproved')
      setTimeout(() => statusMessage.value = '', 4000)
    } else {
      errorMessage.value = data.detail || 'Could not approve bounty'
    }
  } catch (e: any) {
    errorMessage.value = e.message || 'Error approving bounty'
  } finally {
    approvingId.value = null
  }
}

const handleSaveProfile = async () => {
  if (!props.address) return
  isSavingProfile.value = true
  errorMessage.value = ''
  try {
    const res = await fetch('/api/user/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        address: props.address,
        name: nameInput.value,
        email: emailInput.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      statusMessage.value = 'Adventurer profile saved successfully'
      emit('profileUpdated')
      setTimeout(() => statusMessage.value = '', 3000)
    } else {
      errorMessage.value = data.detail || 'Could not update profile'
    }
  } catch (e: any) {
    errorMessage.value = e.message || 'Error updating profile'
  } finally {
    isSavingProfile.value = false
  }
}

const handleSendOtp = async () => {
  if (!emailInput.value || !emailInput.value.includes('@')) {
    errorMessage.value = 'Please provide a valid email address first.'
    return
  }
  isSendingCode.value = true
  errorMessage.value = ''
  statusMessage.value = ''
  try {
    const res = await fetch('/api/user/email/send-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        address: props.address,
        email: emailInput.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      statusMessage.value = data.message || 'Verification code sent.'
      startTimer(data.expires_in_seconds || 900)
    } else {
      errorMessage.value = data.detail || 'Could not send verification code'
    }
  } catch (e: any) {
    errorMessage.value = e.message || 'Network error sending code'
  } finally {
    isSendingCode.value = false
  }
}

const handleVerifyOtp = async () => {
  if (!otpCode.value || otpCode.value.length < 6) {
    errorMessage.value = 'Please enter the 6-digit code.'
    return
  }
  isVerifyingCode.value = true
  errorMessage.value = ''
  try {
    const res = await fetch('/api/user/email/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        address: props.address,
        code: otpCode.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      statusMessage.value = 'Email verified! Adventurer license active.'
      emit('profileUpdated')
      if (timer) clearInterval(timer)
      secondsLeft.value = 0
    } else {
      errorMessage.value = data.detail || 'Invalid or expired code'
    }
  } catch (e: any) {
    errorMessage.value = e.message || 'Error verifying code'
  } finally {
    isVerifyingCode.value = false
  }
}
</script>

<template>
  <div class="flex-1 flex flex-col md:flex-row overflow-hidden bg-white text-left">
    
    <!-- Left 55%: Adventurer License & Credentials -->
    <div class="flex-1 overflow-y-auto p-6 md:p-8 border-r border-[#E3DFD6] space-y-6">
      
      <div>
        <div class="flex items-center gap-2">
          <Shield class="w-5 h-5 text-[#1A1A17]" />
          <h1 class="text-[22px] font-bold text-[#1A1A17] tracking-tight">Adventurer Guild License</h1>
        </div>
        <p class="text-[14px] text-[#5E5B53] mt-0.5">
          Your verifiable identity, on-chain Solana credentials, and guild reputation.
        </p>
      </div>

      <!-- Feedback notifications -->
      <div v-if="errorMessage" class="p-3.5 bg-[#FEF3F2] border border-[#FECDCA] text-[#B42318] text-[13px] rounded-[10px] flex items-center gap-2">
        <AlertCircle class="w-4 h-4 shrink-0" />
        <span>{{ errorMessage }}</span>
      </div>
      <div v-if="statusMessage" class="p-3.5 bg-[#EDFDF5] border border-[#A6F4C5] text-[#1E7B4F] text-[13px] rounded-[10px] flex items-center gap-2">
        <CheckCircle2 class="w-4 h-4 shrink-0" />
        <span>{{ statusMessage }}</span>
      </div>

      <!-- License Card -->
      <div class="p-5 bg-[#F7F5F0] rounded-[14px] border border-[#E3DFD6] space-y-4">
        <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
          <div class="flex items-center gap-2">
            <div class="w-10 h-10 rounded-full bg-[#1A1A17] text-[#FFD60A] font-bold flex items-center justify-center text-[16px]">
              {{ nameInput ? nameInput.charAt(0).toUpperCase() : '⚔' }}
            </div>
            <div>
              <div class="font-bold text-[16px] text-[#1A1A17]">{{ nameInput || 'Anonymous Adventurer' }}</div>
              <div class="text-[12px] text-[#5E5B53]">Guild Rank: Silver Adventurer</div>
            </div>
          </div>
          <span class="text-[12px] font-mono font-medium px-2.5 py-1 rounded-[6px] bg-white border border-[#E3DFD6] text-[#1E7B4F]">
            Solana Devnet
          </span>
        </div>

        <div class="grid grid-cols-2 gap-3 text-[13px]">
          <div>
            <span class="text-[#5E5B53] text-[11px] block">Public Address</span>
            <span class="font-mono text-[#1A1A17] font-medium text-[12px]">{{ address.slice(0, 8) }}...{{ address.slice(-6) }}</span>
          </div>
          <div>
            <span class="text-[#5E5B53] text-[11px] block">Escrow Balance</span>
            <span class="font-bold text-[#1A1A17]">{{ balance.toFixed(3) }} SOL <span class="text-[#5E5B53] font-normal text-[11px]">({{ getUsdValue(balance) }})</span></span>
          </div>
        </div>
      </div>

      <!-- Profile Form -->
      <div class="bg-white rounded-[12px] border border-[#E3DFD6] p-5 space-y-4">
        <h3 class="text-[15px] font-semibold text-[#1A1A17]">Guild Profile Details</h3>
        
        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Adventurer Alias / Handle</label>
          <input 
            v-model="nameInput"
            placeholder="e.g. Frieren, Dennis, Hunter"
            class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
          />
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <label class="text-[13px] font-medium text-[#5E5B53]">Guild Dispatch Email *</label>
            <span v-if="userProfile?.is_email_verified" class="text-[12px] font-semibold text-[#1E7B4F] flex items-center gap-1">
              <CheckCircle2 class="w-3.5 h-3.5" /> Verified
            </span>
            <span v-else class="text-[12px] font-medium text-[#B42318]">Unverified</span>
          </div>
          <div class="flex gap-2">
            <input 
              v-model="emailInput"
              type="email"
              placeholder="adventurer@guild.sol"
              class="flex-1 px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
            />
            <button 
              @click="handleSaveProfile"
              :disabled="isSavingProfile"
              class="px-4 py-2.5 rounded-[8px] bg-[#1A1A17] text-white text-[13px] font-medium hover:bg-[#33332D] transition-colors"
            >
              {{ isSavingProfile ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </div>

        <!-- 15-Minute Verification Loop Box -->
        <div class="p-4 bg-[#FFFBEA] border border-[#FFD60A] rounded-[10px] space-y-3 text-[13px]">
          <div class="flex items-start justify-between">
            <div>
              <span class="font-semibold text-[#1A1A17] block">15-Minute Email Verification Loop</span>
              <p class="text-[#5E5B53] text-[12px] mt-0.5">Required to accept community quests and release escrow.</p>
            </div>
            <div v-if="secondsLeft > 0" class="flex items-center gap-1 px-2 py-0.5 bg-[#1A1A17] text-white rounded-[6px] font-mono text-[11px]">
              <Clock class="w-3 h-3 text-[#FFD60A]" />
              <span>{{ formattedTimer }}</span>
            </div>
          </div>

          <div v-if="!userProfile?.is_email_verified" class="space-y-2 pt-1">
            <div class="flex gap-2">
              <input 
                v-model="otpCode"
                maxlength="6"
                placeholder="6-digit code"
                class="w-36 px-3 py-2 font-mono font-semibold bg-white border border-[#E3DFD6] rounded-[8px] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
              />
              <button 
                @click="handleVerifyOtp"
                :disabled="isVerifyingCode || !otpCode"
                class="px-3.5 py-2 bg-[#1A1A17] text-white text-[13px] font-medium rounded-[8px] hover:bg-[#33332D] disabled:opacity-40 transition-colors"
              >
                {{ isVerifyingCode ? 'Verifying...' : 'Verify' }}
              </button>
              <button 
                @click="handleSendOtp"
                :disabled="isSendingCode || secondsLeft > 0"
                class="px-3.5 py-2 bg-white border border-[#E3DFD6] text-[#1A1A17] text-[12px] font-medium rounded-[8px] hover:bg-[#F7F5F0] transition-colors"
              >
                {{ isSendingCode ? 'Sending...' : secondsLeft > 0 ? 'Sent' : 'Send Code' }}
              </button>
            </div>
          </div>

          <div v-else class="text-[13px] text-[#1E7B4F] font-medium flex items-center gap-1.5">
            <CheckCircle2 class="w-4 h-4" />
            <span>Verified: Full permissions to claim bounties and issue quests.</span>
          </div>
        </div>

      </div>

    </div>

    <!-- Right 45%: Pending Approvals Queue -->
    <div class="w-full md:w-[480px] bg-[#F7F5F0] p-6 md:p-8 flex flex-col overflow-y-auto space-y-5 shrink-0">
      
      <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
        <div>
          <h2 class="text-[17px] font-bold text-[#1A1A17]">Pending Quest Approvals</h2>
          <p class="text-[13px] text-[#5E5B53] mt-0.5">
            Verified proof waiting for your approval or automated 12h payout.
          </p>
        </div>
        <span class="px-2 py-0.5 rounded-full bg-white border border-[#E3DFD6] text-[12px] font-bold text-[#1A1A17]">
          {{ pendingApprovals.length }}
        </span>
      </div>

      <!-- Pending Approval Cards -->
      <div v-if="pendingApprovals.length > 0" class="space-y-3.5">
        <div 
          v-for="appr in pendingApprovals" 
          :key="appr.submission_id"
          class="bg-white p-4 rounded-[12px] border border-[#E3DFD6] shadow-xs space-y-3 text-left"
        >
          <div class="flex items-start justify-between gap-2">
            <div>
              <h3 class="font-semibold text-[15px] text-[#1A1A17] leading-snug">{{ appr.title }}</h3>
              <div class="text-[12px] text-[#5E5B53] mt-0.5">
                <span>{{ appr.city }}</span>
                <span> &middot; </span>
                <span class="font-mono">{{ appr.worker_address.slice(0, 6) }}...{{ appr.worker_address.slice(-4) }}</span>
              </div>
            </div>
            <div class="text-right shrink-0">
              <span class="font-bold text-[14px] text-[#1A1A17]">{{ appr.reward_sol.toFixed(2) }} SOL</span>
              <div class="text-[11px] text-[#5E5B53]">{{ getUsdValue(appr.reward_sol) }}</div>
            </div>
          </div>

          <!-- AI Verification Badge -->
          <div class="p-2.5 bg-[#EDFDF5] border border-[#A6F4C5] rounded-[8px] text-[12px] space-y-1">
            <div class="flex items-center justify-between text-[#1E7B4F] font-semibold">
              <span class="flex items-center gap-1">
                <CheckCircle2 class="w-3.5 h-3.5" />
                <span>AI Vision & Geofence Verified</span>
              </span>
              <span>{{ appr.vision_confidence }}%</span>
            </div>
            <p class="text-[#1A1A17]/80 text-[11px] leading-snug">
              {{ appr.vision_reason || 'Subject confirmed on-site within target geofence tolerance.' }}
            </p>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2 pt-1">
            <button 
              @click="handleApprove(appr.task_id)"
              :disabled="approvingId === appr.task_id"
              class="flex-1 h-9 px-3 rounded-[8px] bg-[#1E7B4F] hover:bg-[#186541] text-white text-[13px] font-semibold flex items-center justify-center gap-1.5 transition-colors shadow-xs cursor-pointer"
            >
              <Check class="w-4 h-4" />
              <span>{{ approvingId === appr.task_id ? 'Releasing...' : 'Approve & Release Escrow' }}</span>
            </button>
            <button 
              @click="$emit('openQuest', appr.task_id)"
              class="h-9 px-3 rounded-[8px] bg-[#F7F5F0] hover:bg-[#EAE6DC] text-[#1A1A17] text-[13px] font-medium transition-colors"
            >
              Inspect
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="flex-1 flex flex-col items-center justify-center p-8 text-center bg-white rounded-[14px] border border-[#E3DFD6] space-y-2">
        <Scroll class="w-8 h-8 text-[#5E5B53]/60 mb-1" />
        <h4 class="font-semibold text-[15px] text-[#1A1A17]">No pending approvals</h4>
        <p class="text-[13px] text-[#5E5B53] max-w-xs">
          When an adventurer submits verified photo evidence for your issued quests, you can approve immediate payout here.
        </p>
      </div>

    </div>

  </div>
</template>
