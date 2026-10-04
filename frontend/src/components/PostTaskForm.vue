<script setup lang="ts">
import { ref, watch } from 'vue'
import AddressSearch from './AddressSearch.vue'
import ReferencePhotoPicker from './ReferencePhotoPicker.vue'
import { Scroll, Sparkles, ShieldCheck, ShieldAlert, ArrowRight, ArrowLeft } from 'lucide-vue-next'

const props = defineProps<{
  userAddress: string
  submitting: boolean
}>()

const emit = defineEmits<{
  (e: 'createTask', payload: any): void
  (e: 'updateFormData', data: any): void
}>()

// 3 Consolidated, Balanced Steps:
// Step 1: Quest Nature & Location
// Step 2: Proof Criteria & Photo Spec
// Step 3: Bounty Deposit & Escrow Seal
const currentStep = ref<number>(1)

// Form fields
const title = ref('')
const category = ref('Civil Help')
const instruction = ref('')
const targetDescription = ref('')
const forbiddenDescription = ref('')
const placeName = ref('')
const fullAddress = ref('')
const city = ref('Berlin')
const country = ref('Germany')
const latitude = ref(52.5113)
const longitude = ref(13.4593)
const radiusMeters = ref(150)
const photosRequired = ref(1)
const finishWindowMinutes = ref(15)
const rewardSol = ref(0.035)
const referencePhotos = ref<string[]>([])

const categories = ['Civil Help', 'Sensitive', 'Commercial']
const radii = [50, 100, 150, 250]
const windows = [10, 15, 30]

const emitCurrentState = () => {
  emit('updateFormData', {
    title: title.value,
    category: category.value,
    instruction: instruction.value,
    targetDescription: targetDescription.value,
    forbiddenDescription: forbiddenDescription.value,
    placeName: placeName.value,
    fullAddress: fullAddress.value,
    city: city.value,
    country: country.value,
    latitude: latitude.value,
    longitude: longitude.value,
    radiusMeters: radiusMeters.value,
    photosRequired: photosRequired.value,
    finishWindowMinutes: finishWindowMinutes.value,
    rewardSol: rewardSol.value,
    referencePhotos: referencePhotos.value
  })
}

watch(
  [title, category, instruction, targetDescription, forbiddenDescription, placeName, fullAddress, city, country, latitude, longitude, radiusMeters, photosRequired, finishWindowMinutes, rewardSol, referencePhotos],
  emitCurrentState,
  { immediate: true, deep: true }
)

const handleAddressSelect = (loc: any) => {
  fullAddress.value = loc.full_address
  placeName.value = loc.place_name
  city.value = loc.city
  country.value = loc.country
  latitude.value = loc.lat
  longitude.value = loc.lon
  emitCurrentState()
}

const applyPreset = (presetTitle: string, presetInst: string, presetTarget: string, presetCat: string, presetCity: string, presetLat: number, presetLon: number, presetPlace: string, presetReward: number) => {
  title.value = presetTitle
  instruction.value = presetInst
  targetDescription.value = presetTarget
  category.value = presetCat
  city.value = presetCity
  latitude.value = presetLat
  longitude.value = presetLon
  placeName.value = presetPlace
  rewardSol.value = presetReward
  emitCurrentState()
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
  <div class="h-full flex flex-col justify-between overflow-y-auto p-6 md:p-8 space-y-6 text-left">
    
    <div class="space-y-6">
      <!-- Step Header -->
      <div class="border-b border-[#E3DFD6] pb-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <Scroll class="w-5 h-5 text-[#1A1A17]" />
            <h2 class="text-[20px] font-bold text-[#1A1A17]">Issue a Guild Quest</h2>
          </div>
          <span class="text-[13px] text-[#5E5B53] font-medium">Stage {{ currentStep }} of 3</span>
        </div>
        <p class="text-[14px] text-[#5E5B53] mt-1">
          Lock SOL reward in Solana Devnet escrow. Bounty is released when a nearby adventurer verifies proof.
        </p>
      </div>

      <!-- Step Progress Bar (3 Equal Balanced Stages) -->
      <div class="grid grid-cols-3 gap-2">
        <div 
          v-for="s in 3" 
          :key="s" 
          class="h-1.5 rounded-full transition-colors"
          :class="s <= currentStep ? 'bg-[#FFD60A]' : 'bg-[#E3DFD6]'"
        ></div>
      </div>

      <!-- STEP 1: NATURE & LOCATION -->
      <div v-if="currentStep === 1" class="space-y-4">
        <!-- Adventurer Guild Quick Presets -->
        <div class="space-y-1.5">
          <label class="text-[13px] font-medium text-[#5E5B53] flex items-center gap-1.5">
            <Sparkles class="w-3.5 h-3.5 text-[#1A1A17]" />
            <span>Adventurer Guild Templates</span>
          </label>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
            <button 
              type="button"
              @click="applyPreset('Find my calico cat Mika near Boxhagener Platz', 'Search around park benches near Boxhagener Platz. Look for a calm calico cat with yellow bell collar.', 'Calico cat with yellow bell collar tag near bench', 'Civil Help', 'Berlin', 52.5113, 13.4593, 'Boxhagener Platz Square', 0.035)"
              class="p-2.5 text-left rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] hover:border-[#1A1A17] text-[12px] leading-snug cursor-pointer transition-colors"
            >
              🐾 Find Cat (Civil Help)
            </button>
            <button 
              type="button"
              @click="applyPreset('Designated driver: Drive patron car home from Malasaña tapas tour', 'Meet patron at Plaza del Dos de Mayo. Drive patron car safely to their parking garage in Chamberí.', 'Parked vehicle in private residential bay with garage sign', 'Civil Help', 'Madrid', 40.4276, -3.7037, 'Plaza del Dos de Mayo', 0.045)"
              class="p-2.5 text-left rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] hover:border-[#1A1A17] text-[12px] leading-snug cursor-pointer transition-colors"
            >
              🚗 Driver Escort (Civil Help)
            </button>
            <button 
              type="button"
              @click="applyPreset('Surveillance & license plate log of black courier van in Mayfair', 'Discreetly photograph logistics van plate and submit a formal investigation letter detailing origin and timetable.', 'Black logistics van rear registration plate with Mayfair alley paving visible', 'Sensitive', 'London', 51.5097, -0.1492, 'Mount Street Commercial Alley', 0.06)"
              class="p-2.5 text-left rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] hover:border-[#1A1A17] text-[12px] leading-snug cursor-pointer transition-colors"
            >
              🔍 Van Intel (Sensitive)
            </button>
            <button 
              type="button"
              @click="applyPreset('Artisan pistachio tart showcase photo & tasting reel at Belleville bakery', 'Purchase seasonal pistachio tart from bakery display, place by window terrace with shop signage, and capture commercial photo.', 'Pistachio pastry confection in packaging with Boulangerie Belleville storefront lettering', 'Commercial', 'Paris', 48.8722, 2.3811, 'Boulangerie Artisanale Belleville', 0.03)"
              class="p-2.5 text-left rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] hover:border-[#1A1A17] text-[12px] leading-snug cursor-pointer transition-colors"
            >
              📸 Pastry Reel (Commercial)
            </button>
          </div>
        </div>

        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Quest Title *</label>
          <input 
            v-model="title"
            placeholder="e.g. Find lost tortoiseshell cat near Boxhagener Platz"
            class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Guild Category</label>
            <select 
              v-model="category"
              class="w-full px-3 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
            >
              <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>

          <div>
            <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Target European City</label>
            <select 
              v-model="city"
              class="w-full px-3 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
            >
              <option value="London">London (UK)</option>
              <option value="Paris">Paris (France)</option>
              <option value="Berlin">Berlin (Germany)</option>
              <option value="Madrid">Madrid (Spain)</option>
              <option value="Rome">Rome (Italy)</option>
              <option value="Amsterdam">Amsterdam (Netherlands)</option>
              <option value="Barcelona">Barcelona (Spain)</option>
              <option value="Vienna">Vienna (Austria)</option>
            </select>
          </div>
        </div>

        <!-- Sensitive Protocol Notice Banner -->
        <div v-if="category === 'Sensitive'" class="p-3.5 rounded-[10px] bg-[#FFF8E6] border border-[#F5C242] text-left space-y-1">
          <div class="flex items-center gap-1.5 font-semibold text-[13px] text-[#8C5800]">
            <ShieldAlert class="w-4 h-4 text-[#B87A00]" />
            <span>Sensitive Intelligence Protocol Mandate</span>
          </div>
          <p class="text-[12px] text-[#8C5800] leading-relaxed">
            To claim bounties in this category, adventurers must submit both an <strong>on-site physical photo</strong> AND a formal <strong>written investigation letter</strong> with declared intelligence source attribution (e.g. municipal record, direct witness interview, visual surveillance). Gemini 3.1 Flash-Lite evaluates both streams.
          </p>
        </div>

        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Search Landmark or Street Location *</label>
          <AddressSearch @selectAddress="handleAddressSelect" />
        </div>

        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Geofence Boundary Radius</label>
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
        </div>
      </div>

      <!-- STEP 2: PROOF SPECIFICATION & PHOTO CRITERIA -->
      <div v-else-if="currentStep === 2" class="space-y-4">
        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Adventurer Instructions *</label>
          <textarea 
            v-model="instruction"
            rows="3"
            placeholder="Explain where the adventurer should look or what they must do on site."
            class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
          ></textarea>
        </div>

        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">What the photo proof MUST show *</label>
          <input 
            v-model="targetDescription"
            placeholder="e.g. Tortoiseshell calico cat, distinct yellow collar with bell"
            class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
          />
        </div>

        <div>
          <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">What the photo must NOT show (disqualifiers)</label>
          <input 
            v-model="forbiddenDescription"
            placeholder="e.g. Stray dog, blurry screenshot, indoor photo"
            class="w-full px-3.5 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[14px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
          />
        </div>

        <ReferencePhotoPicker @updatePhotos="referencePhotos = $event" />
      </div>

      <!-- STEP 3: BOUNTY DEPOSIT & ESCROW SEAL -->
      <div v-else-if="currentStep === 3" class="space-y-4">
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Completion Window</label>
            <div class="flex items-center gap-1.5">
              <button 
                v-for="w in windows" 
                :key="w"
                type="button"
                @click="finishWindowMinutes = w"
                class="flex-1 py-1.5 rounded-[8px] border text-[13px] font-medium transition-colors text-center"
                :class="finishWindowMinutes === w ? 'bg-[#1A1A17] text-white border-[#1A1A17]' : 'bg-[#F7F5F0] text-[#5E5B53] border-[#E3DFD6]'"
              >
                {{ w }} min
              </button>
            </div>
          </div>

          <div>
            <label class="block text-[13px] font-medium text-[#5E5B53] mb-1">Bounty Reward (SOL) *</label>
            <input 
              v-model.number="rewardSol"
              type="number"
              step="0.005"
              min="0.005"
              max="2.0"
              class="w-full px-3.5 py-1.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] font-bold text-[#1A1A17]"
            />
          </div>
        </div>

        <!-- Quest Summary Review Card -->
        <div class="p-4 bg-[#F7F5F0] rounded-[12px] border border-[#E3DFD6] space-y-2.5 text-[13px]">
          <div class="flex justify-between items-center border-b border-[#E3DFD6] pb-2">
            <span class="font-bold text-[15px] text-[#1A1A17]">{{ title || 'Untitled Quest' }}</span>
            <span class="px-2 py-0.5 rounded-[6px] bg-white border border-[#E3DFD6] text-[11px] font-semibold text-[#1E7B4F]">Ready to Seal</span>
          </div>

          <div class="space-y-1 text-[#5E5B53]">
            <div><strong>Location:</strong> {{ placeName || city }} ({{ radiusMeters }}m geofence)</div>
            <div><strong>Target Spec:</strong> {{ targetDescription || '-' }}</div>
            <div><strong>Execution Window:</strong> {{ finishWindowMinutes }} minutes after acceptance</div>
          </div>

          <div class="pt-2 border-t border-[#E3DFD6] flex justify-between items-center text-[15px]">
            <span class="font-medium text-[#5E5B53]">Escrow Lock Amount</span>
            <span class="font-bold text-[#1A1A17]">{{ rewardSol.toFixed(3) }} SOL</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Buttons -->
    <div class="pt-4 border-t border-[#E3DFD6] flex items-center justify-between">
      <button 
        v-if="currentStep > 1"
        type="button"
        @click="currentStep--"
        class="h-10 px-4 rounded-[10px] text-[14px] font-medium text-[#5E5B53] hover:text-[#1A1A17] flex items-center gap-1.5"
      >
        <ArrowLeft class="w-4 h-4" />
        <span>Back</span>
      </button>
      <div v-else></div>

      <button 
        v-if="currentStep < 3"
        type="button"
        @click="currentStep++"
        class="h-11 px-6 rounded-[12px] bg-[#1A1A17] text-white text-[14px] font-semibold hover:bg-[#33332D] transition-colors flex items-center gap-2"
      >
        <span>Next stage</span>
        <ArrowRight class="w-4 h-4" />
      </button>

      <button 
        v-else
        type="button"
        @click="handleSubmit"
        :disabled="submitting"
        class="h-11 px-7 rounded-[12px] bg-[#FFD60A] text-[#1A1A17] text-[15px] font-bold hover:brightness-95 transition-all shadow-xs disabled:opacity-50 flex items-center gap-2 cursor-pointer"
      >
        <ShieldCheck class="w-4 h-4" />
        <span>{{ submitting ? 'Locking in Escrow...' : 'Seal & Issue Quest' }}</span>
      </button>
    </div>

  </div>
</template>
