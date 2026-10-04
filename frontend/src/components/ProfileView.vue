<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { CheckCircle2, AlertCircle, Check, Scroll, Shield } from 'lucide-vue-next'
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
const isSavingProfile = ref(false)
const statusMessage = ref('')
const errorMessage = ref('')

// Pending Approvals & Activity stats
const pendingApprovals = ref<any[]>([])
const loadingApprovals = ref(false)
const approvingId = ref<string | null>(null)

onMounted(() => {
  if (props.userProfile) {
    nameInput.value = props.userProfile.name || ''
  }
  fetchPendingApprovals()
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

const rankBadgeColor = computed(() => {
  const r = props.userProfile?.rank || 'F'
  switch (r) {
    case 'S': return 'bg-[#FFD60A] text-[#1A1A17] border-[#1A1A17]'
    case 'A': return 'bg-[#7F56D9] text-white border-[#6941C6]'
    case 'B': return 'bg-[#1570EF] text-white border-[#175CD3]'
    case 'C': return 'bg-[#0E9384] text-white border-[#0B7B6E]'
    case 'D': return 'bg-[#E3DFD6] text-[#1A1A17] border-[#5E5B53]'
    case 'E': return 'bg-[#F7F5F0] text-[#5E5B53] border-[#E3DFD6]'
    default: return 'bg-[#F2F4F7] text-[#475467] border-[#D0D5DD]'
  }
})

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
        name: nameInput.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      statusMessage.value = 'Adventurer handle updated successfully'
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

      <!-- License Card with F -> S Rank -->
      <div class="p-5 bg-[#F7F5F0] rounded-[14px] border border-[#E3DFD6] space-y-4">
        <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-full bg-[#1A1A17] text-[#FFD60A] font-bold flex items-center justify-center text-[18px] border-2 border-[#FFD60A]">
              {{ userProfile?.rank || 'F' }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="font-bold text-[17px] text-[#1A1A17]">{{ nameInput || 'Anonymous Adventurer' }}</span>
                <span class="px-2 py-0.5 rounded-full text-[11px] font-extrabold uppercase border" :class="rankBadgeColor">
                  {{ userProfile?.rank || 'F' }}-Rank
                </span>
              </div>
              <div class="text-[13px] text-[#5E5B53] font-medium">{{ userProfile?.rank_title || 'F-Rank Novice Adventurer' }}</div>
            </div>
          </div>
          <span class="text-[12px] font-mono font-medium px-2.5 py-1 rounded-[6px] bg-white border border-[#E3DFD6] text-[#1E7B4F]">
            Solana Devnet
          </span>
        </div>

        <!-- Rank Progression Bar -->
        <div class="space-y-1.5 p-3 bg-white rounded-[10px] border border-[#E3DFD6]">
          <div class="flex justify-between text-[12px] text-[#5E5B53]">
            <span>Rank Progression</span>
            <span class="font-semibold text-[#1A1A17]">{{ userProfile?.exp || 0 }} EXP {{ userProfile?.next_tier ? `(${userProfile.next_exp_needed} EXP to ${userProfile.next_tier}-Rank)` : '(Max Rank S Reached!)' }}</span>
          </div>
          <div class="h-2 bg-[#F7F5F0] rounded-full overflow-hidden border border-[#E3DFD6]">
            <div 
              class="h-full bg-[#FFD60A] transition-all duration-500" 
              :style="{ width: `${Math.min(100, Math.max(8, ((userProfile?.exp || 0) / 1500) * 100))}%` }"
            ></div>
          </div>
          <div class="flex justify-between text-[10px] text-[#5E5B53] font-mono pt-0.5">
            <span :class="userProfile?.rank === 'F' ? 'font-bold text-[#1A1A17]' : ''">F</span>
            <span :class="userProfile?.rank === 'E' ? 'font-bold text-[#1A1A17]' : ''">E</span>
            <span :class="userProfile?.rank === 'D' ? 'font-bold text-[#1A1A17]' : ''">D</span>
            <span :class="userProfile?.rank === 'C' ? 'font-bold text-[#1A1A17]' : ''">C</span>
            <span :class="userProfile?.rank === 'B' ? 'font-bold text-[#1A1A17]' : ''">B</span>
            <span :class="userProfile?.rank === 'A' ? 'font-bold text-[#1A1A17]' : ''">A</span>
            <span :class="userProfile?.rank === 'S' ? 'font-bold text-[#1A1A17]' : ''">S</span>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-3 text-[13px] pt-1">
          <div>
            <span class="text-[#5E5B53] text-[11px] block">Public Key</span>
            <span class="font-mono text-[#1A1A17] font-medium text-[12px]">{{ address.slice(0, 6) }}...{{ address.slice(-4) }}</span>
          </div>
          <div>
            <span class="text-[#5E5B53] text-[11px] block">Quests Completed</span>
            <span class="font-bold text-[#1A1A17]">{{ userProfile?.tasks_completed || 0 }} completed</span>
          </div>
          <div>
            <span class="text-[#5E5B53] text-[11px] block">Escrow Balance</span>
            <span class="font-bold text-[#1A1A17]">{{ balance.toFixed(3) }} SOL</span>
          </div>
        </div>
      </div>

      <!-- Guild Rank Hierarchy Explanation -->
      <div class="bg-white rounded-[12px] border border-[#E3DFD6] p-5 space-y-3">
        <div class="flex items-center gap-1.5">
          <Scroll class="w-4 h-4 text-[#FFD60A]" />
          <h3 class="text-[14px] font-bold text-[#1A1A17]">Guild Rank Hierarchy & Promotion Logic</h3>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[12px]">
          <div class="p-2.5 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
            <span class="font-bold text-[#1A1A17]">F-Rank &rarr; Novice (0 EXP)</span>
            <p class="text-[#5E5B53]">Initial adventurer grade assigned to freshly initialized guild wallets.</p>
          </div>
          <div class="p-2.5 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
            <span class="font-bold text-[#1A1A17]">E-Rank &rarr; Apprentice (50 EXP)</span>
            <p class="text-[#5E5B53]">Issued first quest bounty or completed beginner municipal requests.</p>
          </div>
          <div class="p-2.5 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
            <span class="font-bold text-[#1A1A17]">D-Rank &rarr; Proven (100 EXP)</span>
            <p class="text-[#5E5B53]">Verified on-site photo verifier pass and settled first on-chain escrow.</p>
          </div>
          <div class="p-2.5 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
            <span class="font-bold text-[#1A1A17]">C-Rank &rarr; Skilled (250 EXP)</span>
            <p class="text-[#5E5B53]">3+ completed quests across multiple cities with zero fraudulent reports.</p>
          </div>
          <div class="p-2.5 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
            <span class="font-bold text-[#1A1A17]">B-Rank &rarr; Veteran (450 EXP)</span>
            <p class="text-[#5E5B53]">5+ completed quests or 450 EXP. Eligible for Sensitive Task contracts.</p>
          </div>
          <div class="p-2.5 bg-[#F7F5F0] rounded-[8px] space-y-0.5">
            <span class="font-bold text-[#1A1A17]">A & S-Rank &rarr; Elite & Grandmaster</span>
            <p class="text-[#5E5B53]">8+ and 15+ verified completions. Unrestricted guild master privileges.</p>
          </div>
        </div>
      </div>

      <!-- Adventurer Alias Form (Clean without Email) -->
      <div class="bg-white rounded-[12px] border border-[#E3DFD6] p-5 space-y-4">
        <h3 class="text-[15px] font-semibold text-[#1A1A17]">Guild Adventurer Identity</h3>
        
        <div class="space-y-2">
          <label class="block text-[13px] font-medium text-[#5E5B53]">Adventurer Alias / Handle</label>
          <div class="flex gap-2">
            <input 
              v-model="nameInput"
              placeholder="e.g. Frieren, Dennis, Hunter"
              class="flex-1 px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
            />
            <button 
              @click="handleSaveProfile"
              :disabled="isSavingProfile"
              class="px-5 py-2.5 rounded-[8px] bg-[#1A1A17] text-white text-[13px] font-medium hover:bg-[#33332D] transition-colors cursor-pointer"
            >
              {{ isSavingProfile ? 'Saving...' : 'Update Alias' }}
            </button>
          </div>
          <p class="text-[12px] text-[#5E5B53]">
            Your alias is publicly bound to your Solana address on quest board dispatches and leaderboard rankings.
          </p>
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
