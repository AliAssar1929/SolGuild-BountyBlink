<script setup lang="ts">
import { ref } from 'vue'
import AddressSearch from './AddressSearch.vue'
import ReferencePhotoPicker from './ReferencePhotoPicker.vue'
const props = defineProps<{
  userAddress: string
  submitting: boolean
}>()

const emit = defineEmits<{
  (e: 'createTask', payload: any): void
}>()

// Step state: 1. Basics, 2. Place, 3. Requirements, 4. Timing & Reward, 5. Review
const currentStep = ref<number>(1)

// Form fields
const title = ref('')
const category = ref('Infrastructure')
const instruction = ref('')
const targetDescription = ref('')
const forbiddenDescription = ref('')
const placeName = ref('')
const fullAddress = ref('')
const city = ref('Berlin')
const country = ref('Germany')
const latitude = ref(52.5200)
const longitude = ref(13.4050)
const radiusMeters = ref(150)
const photosRequired = ref(1)
const finishWindowMinutes = ref(10)
const rewardSol = ref(0.01)
const referencePhotos = ref<string[]>([])

const categories = ['Infrastructure', 'Storefront', 'Logistics', 'Mobility', 'Accessibility']
const radii = [50, 100, 150, 250]
const windows = [10, 15, 30]

const handleAddressSelect = (loc: any) => {
  fullAddress.value = loc.full_address
  placeName.value = loc.place_name
  city.value = loc.city
  country.value = loc.country
  latitude.value = loc.lat
  longitude.value = loc.lon
}

const applyPreset = (presetTitle: string, presetInst: string, presetTarget: string, presetCat: string) => {
  title.value = presetTitle
  instruction.value = presetInst
  targetDescription.value = presetTarget
  category.value = presetCat
}

const handleSubmit = () => {
  emit('createTask', {
    title: title.value,
    category: category.value,
    instruction: instruction.value,
    target_description: targetDescription.value,
    forbidden_description: forbiddenDescription.value,
    place_name: placeName.value,
    full_address: fullAddress.value,
    city: city.value,
    country: country.value,
    latitude: latitude.value,
    longitude: longitude.value,
    radius_meters: radiusMeters.value,
    photos_required: photosRequired.value,
    finish_window_minutes: finishWindowMinutes.value,
    reward_sol: rewardSol.value,
    poster_address: props.userAddress,
    reference_photo_url: referencePhotos.value[0] || null
  })
}
</script>

<template>
  <div class="w-full bg-white p-6 md:p-8 rounded-[16px] border border-[#E3DFD6] shadow-xs space-y-6 text-left">
    
    <!-- Step Header -->
    <div class="border-b border-[#E3DFD6] pb-4">
      <div class="flex items-center justify-between">
        <h2 class="text-[20px] font-bold text-[#1A1A17]">Post a task</h2>
        <span class="text-[13px] text-[#5E5B53] font-medium">Step {{ currentStep }} of 5</span>
      </div>
      <p class="text-[14px] text-[#5E5B53] mt-0.5">
        Deposit SOL into escrow. Payout is released when a nearby person's photo passes verification.
      </p>
    </div>

    <!-- Step Progress Dots -->
    <div class="grid grid-cols-5 gap-2">
      <div 
        v-for="s in 5" 
        :key="s" 
        class="h-1.5 rounded-full transition-colors"
        :class="s <= currentStep ? 'bg-[#FFD60A]' : 'bg-[#E3DFD6]'"
      ></div>
    </div>

    <!-- STEP 1: BASICS -->
    <div v-if="currentStep === 1" class="space-y-4">
      <!-- Quick presets -->
      <div class="space-y-1.5">
        <label class="text-[13px] font-medium text-[#5E5B53]">Quick task templates</label>
        <div class="grid grid-cols-2 gap-2">
          <button 
            type="button"
            @click="applyPreset('EV charger operational status', 'Check if charger #3 is functional.', 'Active operational screen, intact cable connector', 'Infrastructure')"
            class="p-2.5 text-left rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] hover:border-[#1A1A17] text-[13px] leading-snug"
          >
            EV charger check
          </button>
          <button 
            type="button"
            @click="applyPreset('Opening hours blackboard check', 'Photograph the chalkboard near front door.', 'Chalkboard sign with clear hours visible', 'Storefront')"
            class="p-2.5 text-left rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] hover:border-[#1A1A17] text-[13px] leading-snug"
          >
            Storefront hours
          </button>
        </div>
      </div>

      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Task title *</label>
        <input 
          v-model="title"
          placeholder="e.g. Is the EV charger at Alexanderplatz working?"
          class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
        />
      </div>

      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Category</label>
        <select 
          v-model="category"
          class="w-full px-3 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
        >
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Worker instructions *</label>
        <textarea 
          v-model="instruction"
          rows="2"
          placeholder="What physical perspective or detail must the photo show?"
          class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
        ></textarea>
      </div>
    </div>

    <!-- STEP 2: PLACE -->
    <div v-else-if="currentStep === 2" class="space-y-4">
      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Search address or place name *</label>
        <AddressSearch @selectAddress="handleAddressSelect" />
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">City</label>
          <input 
            v-model="city"
            class="w-full px-3 py-2 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px]"
          />
        </div>
        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Country</label>
          <input 
            v-model="country"
            class="w-full px-3 py-2 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px]"
          />
        </div>
      </div>

      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Verification radius tolerance</label>
        <div class="flex items-center gap-2">
          <button 
            v-for="r in radii" 
            :key="r"
            type="button"
            @click="radiusMeters = r"
            class="px-3 py-1.5 rounded-[8px] border text-[13px] font-medium transition-colors"
            :class="radiusMeters === r ? 'bg-[#1A1A17] text-white border-[#1A1A17]' : 'bg-[#F7F5F0] text-[#5E5B53] border-[#E3DFD6]'"
          >
            {{ r }} m
          </button>
        </div>
        <p class="text-[12px] text-[#5E5B53] mt-1">Photo must be taken within this distance of the pin.</p>
      </div>
    </div>

    <!-- STEP 3: PHOTO REQUIREMENTS -->
    <div v-else-if="currentStep === 3" class="space-y-4">
      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">What the photo must show *</label>
        <input 
          v-model="targetDescription"
          placeholder="e.g. Green operational display, undamaged cable"
          class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
        />
      </div>

      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">What the photo must NOT show (optional)</label>
        <input 
          v-model="forbiddenDescription"
          placeholder="e.g. Out of order red warning light, blurred screen"
          class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
        />
      </div>

      <ReferencePhotoPicker @updatePhotos="referencePhotos = $event" />
    </div>

    <!-- STEP 4: TIMING & REWARD -->
    <div v-else-if="currentStep === 4" class="space-y-4">
      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Time to finish after claiming</label>
        <div class="flex items-center gap-2">
          <button 
            v-for="w in windows" 
            :key="w"
            type="button"
            @click="finishWindowMinutes = w"
            class="px-3 py-1.5 rounded-[8px] border text-[13px] font-medium transition-colors"
            :class="finishWindowMinutes === w ? 'bg-[#1A1A17] text-white border-[#1A1A17]' : 'bg-[#F7F5F0] text-[#5E5B53] border-[#E3DFD6]'"
          >
            {{ w }} minutes
          </button>
        </div>
      </div>

      <div>
        <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Reward in SOL *</label>
        <div class="flex items-center gap-2">
          <input 
            v-model.number="rewardSol"
            type="number"
            step="0.005"
            min="0.005"
            max="1.0"
            class="w-32 px-3 py-2 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] font-semibold text-[#1A1A17]"
          />
          <span class="text-[14px] text-[#5E5B53]">SOL (held in Solana Devnet escrow)</span>
        </div>
      </div>
    </div>

    <!-- STEP 5: REVIEW & FUND -->
    <div v-else-if="currentStep === 5" class="space-y-4 text-left">
      <div class="p-4 bg-[#F7F5F0] rounded-[12px] border border-[#E3DFD6] space-y-3">
        <div>
          <span class="text-[12px] text-[#5E5B53] uppercase font-semibold">Summary</span>
          <h3 class="text-[17px] font-bold text-[#1A1A17] mt-0.5">{{ title }}</h3>
          <p class="text-[13px] text-[#5E5B53]">{{ category }} &middot; {{ city }}, {{ country }}</p>
        </div>

        <div class="text-[13px] text-[#5E5B53] space-y-1">
          <div><strong>Instructions:</strong> {{ instruction }}</div>
          <div><strong>Must show:</strong> {{ targetDescription }}</div>
          <div><strong>Radius:</strong> {{ radiusMeters }} m &middot; <strong>Finish window:</strong> {{ finishWindowMinutes }} min</div>
        </div>

        <div class="pt-2 border-t border-[#E3DFD6] flex justify-between items-center text-[15px]">
          <span class="text-[#5E5B53]">Escrow deposit</span>
          <span class="font-bold text-[#1A1A17]">{{ rewardSol.toFixed(2) }} SOL</span>
        </div>
      </div>
    </div>

    <!-- Form Navigation Buttons -->
    <div class="pt-4 border-t border-[#E3DFD6] flex items-center justify-between">
      <button 
        v-if="currentStep > 1"
        type="button"
        @click="currentStep--"
        class="px-4 py-2 text-[14px] font-medium text-[#5E5B53] hover:text-[#1A1A17]"
      >
        Back
      </button>
      <div v-else></div>

      <button 
        v-if="currentStep < 5"
        type="button"
        @click="currentStep++"
        class="h-10 px-5 rounded-[10px] bg-[#1A1A17] text-white text-[14px] font-medium hover:bg-[#33332D] transition-colors"
      >
        Next step
      </button>

      <button 
        v-else
        type="button"
        @click="handleSubmit"
        :disabled="submitting"
        class="h-11 px-6 rounded-[12px] bg-[#FFD60A] text-[#1A1A17] text-[15px] font-semibold hover:brightness-95 transition-all shadow-xs disabled:opacity-50"
      >
        {{ submitting ? 'Confirming deposit...' : 'Fund and publish task' }}
      </button>
    </div>

  </div>
</template>
