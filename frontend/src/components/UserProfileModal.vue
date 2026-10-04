<script setup lang="ts">
import { ref, computed, watch, onUnmounted } from 'vue'
import { User, ShieldCheck, Clock, CheckCircle2, AlertCircle, X } from 'lucide-vue-next'

const props = defineProps<{
  isOpen: boolean
  address: string
  userProfile: any
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'profileUpdated'): void
}>()

const nameInput = ref('')
const emailInput = ref('')
const otpCode = ref('')
const isSendingCode = ref(false)
const isVerifyingCode = ref(false)
const statusMessage = ref('')
const errorMessage = ref('')
const isSavingProfile = ref(false)

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

watch(() => props.userProfile, (p) => {
  if (p) {
    nameInput.value = p.name || ''
    emailInput.value = p.email || ''
  }
}, { immediate: true })

onUnmounted(() => {
  if (timer) clearInterval(timer)
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
        name: nameInput.value,
        email: emailInput.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      statusMessage.value = 'Profile updated successfully'
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
      startTimer(data.expires_in_seconds || 900)
      statusMessage.value = `Code sent! (Dev code: ${data.dev_code})`
      emit('profileUpdated')
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
      statusMessage.value = 'Email verified! You can now claim and accept field tasks.'
      if (timer) clearInterval(timer)
      secondsLeft.value = 0
      emit('profileUpdated')
    } else {
      errorMessage.value = data.detail || 'Verification code failed'
    }
  } catch (e: any) {
    errorMessage.value = e.message || 'Error verifying code'
  } finally {
    isVerifyingCode.value = false
  }
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/35 backdrop-blur-xs">
    <div class="w-full max-w-lg bg-white border border-[#E3DFD6] rounded-[16px] shadow-2xl p-6 text-left space-y-5">
      
      <div class="flex items-center justify-between border-b border-[#E3DFD6] pb-3">
        <div class="flex items-center gap-2">
          <User class="w-5 h-5 text-[#1A1A17]" />
          <h3 class="font-semibold text-[17px] text-[#1A1A17]">Worker Profile & Verification</h3>
        </div>
        <button @click="$emit('close')" class="p-1 hover:bg-[#F7F5F0] rounded-[6px] text-[#5E5B53]">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Wallet identifier chip -->
      <div class="p-3 bg-[#F7F5F0] rounded-[10px] border border-[#E3DFD6] flex justify-between items-center text-[13px]">
        <span class="text-[#5E5B53]">Connected Wallet</span>
        <span class="font-mono text-[#1A1A17] font-medium">{{ address.slice(0, 8) }}...{{ address.slice(-6) }}</span>
      </div>

      <!-- Feedback messages -->
      <div v-if="errorMessage" class="p-3 bg-[#FEF3F2] border border-[#FECDCA] text-[#B42318] text-[13px] rounded-[8px] flex items-center gap-2">
        <AlertCircle class="w-4 h-4 shrink-0" />
        <span>{{ errorMessage }}</span>
      </div>
      <div v-if="statusMessage" class="p-3 bg-[#EDFDF5] border border-[#A6F4C5] text-[#1E7B4F] text-[13px] rounded-[8px] flex items-center gap-2">
        <CheckCircle2 class="w-4 h-4 shrink-0" />
        <span>{{ statusMessage }}</span>
      </div>

      <!-- Name & Email Inputs -->
      <div class="space-y-4">
        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Display Name / Alias</label>
          <input 
            v-model="nameInput"
            placeholder="e.g. Alex Hunter"
            class="w-full px-3 py-2 text-[14px] bg-[#F7F5F0] border border-[#E3DFD6] rounded-[8px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
          />
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <label class="text-[13px] font-medium text-[#5E5B53]">Notification Email *</label>
            <span v-if="userProfile?.is_email_verified" class="text-[12px] font-semibold text-[#1E7B4F] flex items-center gap-1">
              <CheckCircle2 class="w-3.5 h-3.5" /> Verified
            </span>
            <span v-else class="text-[12px] font-medium text-[#B42318]">Unverified (Required for tasks)</span>
          </div>
          <div class="flex gap-2">
            <input 
              v-model="emailInput"
              type="email"
              placeholder="alex@example.com"
              class="flex-1 px-3 py-2 text-[14px] bg-[#F7F5F0] border border-[#E3DFD6] rounded-[8px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
            />
            <button 
              @click="handleSaveProfile"
              :disabled="isSavingProfile"
              class="px-3.5 py-2 text-[13px] font-medium rounded-[8px] bg-[#F7F5F0] border border-[#E3DFD6] hover:bg-[#EAE6DC] transition-colors"
            >
              {{ isSavingProfile ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 15-Minute Email Verification Gate Box -->
      <div class="p-4 bg-[#FFFBEA] border border-[#FFD60A] rounded-[12px] space-y-3 text-[13px]">
        <div class="flex items-start justify-between">
          <div class="space-y-0.5">
            <span class="font-semibold text-[#1A1A17] flex items-center gap-1.5">
              <ShieldCheck class="w-4 h-4 text-[#1A1A17]" />
              <span>15-Minute Email Verification Loop</span>
            </span>
            <p class="text-[#5E5B53] text-[12px]">
              Workers must hold a verified email address to claim bounties and escrow payouts.
            </p>
          </div>

          <div v-if="secondsLeft > 0" class="flex items-center gap-1 px-2.5 py-1 bg-[#1A1A17] text-white rounded-[6px] font-mono text-[12px]">
            <Clock class="w-3.5 h-3.5 text-[#FFD60A]" />
            <span>{{ formattedTimer }}</span>
          </div>
        </div>

        <div v-if="!userProfile?.is_email_verified" class="space-y-2 pt-1">
          <div class="flex gap-2">
            <input 
              v-model="otpCode"
              maxlength="6"
              placeholder="Enter 6-digit code"
              class="w-40 px-3 py-2 text-[14px] font-mono font-semibold bg-white border border-[#E3DFD6] rounded-[8px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
            />
            <button 
              @click="handleVerifyOtp"
              :disabled="isVerifyingCode || !otpCode"
              class="px-4 py-2 bg-[#1A1A17] hover:bg-[#33332D] text-white font-medium rounded-[8px] text-[13px] disabled:opacity-40 transition-colors"
            >
              {{ isVerifyingCode ? 'Verifying...' : 'Verify Code' }}
            </button>
            <button 
              @click="handleSendOtp"
              :disabled="isSendingCode || secondsLeft > 0"
              class="px-3 py-2 bg-white border border-[#E3DFD6] hover:bg-[#F7F5F0] text-[#1A1A17] font-medium rounded-[8px] text-[12px] transition-colors"
            >
              {{ isSendingCode ? 'Sending...' : secondsLeft > 0 ? 'Code Sent' : 'Send Code' }}
            </button>
          </div>
        </div>

        <div v-else class="text-[13px] text-[#1E7B4F] font-medium flex items-center gap-1.5">
          <CheckCircle2 class="w-4 h-4" />
          <span>Your account is fully verified to claim tasks and earn SOL.</span>
        </div>
      </div>

    </div>
  </div>
</template>
