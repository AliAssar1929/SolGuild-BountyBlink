<script setup lang="ts">
import { ref, watch } from 'vue'
import { FileText, Camera, Upload, X, ShieldAlert, Paperclip } from 'lucide-vue-next'

const props = defineProps<{
  isOpen: boolean
  task: any
  submitting: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'submitDossier', payload: {
    photo: File
    investigationLetter: string
    sourceInfo: string
    letterFile?: File
  }): void
}>()

const photoFile = ref<File | null>(null)
const photoPreview = ref<string | null>(null)
const investigationLetter = ref('')
const sourceInfo = ref('')
const docFile = ref<File | null>(null)
const formError = ref<string | null>(null)

watch(() => props.isOpen, (open) => {
  if (open) {
    photoFile.value = null
    photoPreview.value = null
    investigationLetter.value = ''
    sourceInfo.value = ''
    docFile.value = null
    formError.value = null
  }
})

const handlePhotoSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    photoFile.value = target.files[0]
    photoPreview.value = URL.createObjectURL(target.files[0])
    formError.value = null
  }
}

const handleDocSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    docFile.value = target.files[0]
  }
}

const applySampleSource = (src: string) => {
  sourceInfo.value = src
}

const handleSubmit = () => {
  formError.value = null
  if (!photoFile.value) {
    formError.value = 'Photographic evidence is required. Please capture or upload a clear photo.'
    return
  }
  if (!investigationLetter.value.trim() || investigationLetter.value.trim().length < 35) {
    formError.value = 'Investigation letter must be at least 35 characters with detailed field findings.'
    return
  }
  if (!sourceInfo.value.trim() || sourceInfo.value.trim().length < 4) {
    formError.value = 'Please declare your intelligence source (e.g. Physical Surveillance, Eyewitness, Public Registry).'
    return
  }

  emit('submitDossier', {
    photo: photoFile.value,
    investigationLetter: investigationLetter.value.trim(),
    sourceInfo: sourceInfo.value.trim(),
    letterFile: docFile.value || undefined
  })
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
    <div class="w-full max-w-xl bg-white border border-[#E3DFD6] rounded-[16px] shadow-2xl overflow-hidden flex flex-col max-h-[90dvh] text-left">
      
      <!-- Header -->
      <div class="px-6 py-4 border-b border-[#E3DFD6] bg-[#F7F5F0] flex items-center justify-between shrink-0">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-full bg-[#FFD60A]/30 border border-[#FFD60A] flex items-center justify-center">
            <FileText class="w-4 h-4 text-[#1A1A17]" />
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-[16px] text-[#1A1A17]">Sensitive Intelligence Dossier</h3>
              <span class="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-[#1A1A17] text-[#FFD60A]">Mandatory Protocol</span>
            </div>
            <p class="text-[12px] text-[#5E5B53]">{{ task?.title }}</p>
          </div>
        </div>
        <button @click="$emit('close')" class="p-1.5 hover:bg-[#EAE6DC] rounded-[8px] text-[#5E5B53]">
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Scrollable Form Body -->
      <div class="p-6 overflow-y-auto space-y-5">
        
        <!-- Instruction Banner -->
        <div class="p-3.5 rounded-[12px] bg-[#FFF8E6] border border-[#F5C242] text-[13px] text-[#8C5800] space-y-1">
          <div class="flex items-center gap-1.5 font-semibold">
            <ShieldAlert class="w-4 h-4 text-[#B87A00]" />
            <span>Dual-Evidence Requirement</span>
          </div>
          <p class="text-[12px] leading-relaxed">
            Sensitive tasks require both <strong>photographic verification</strong> AND a formal <strong>written field report</strong> detailing the origin, observations, and declared intelligence source. Gemini 3.1 Flash-Lite inspects both evidence streams.
          </p>
        </div>

        <!-- Section 1: Photo Evidence -->
        <div class="space-y-2">
          <label class="block text-[13px] font-semibold text-[#1A1A17]">
            1. Photographic Evidence (On-Site Capture) *
          </label>
          
          <div v-if="photoPreview" class="relative rounded-[12px] overflow-hidden border border-[#E3DFD6] bg-black/5 aspect-video flex items-center justify-center">
            <img :src="photoPreview" alt="Proof Preview" class="w-full h-full object-cover" />
            <button 
              @click="photoFile = null; photoPreview = null"
              class="absolute top-2 right-2 px-2.5 py-1 rounded-[6px] bg-black/70 hover:bg-black text-white text-[11px] font-medium transition-colors"
            >
              Replace Photo
            </button>
          </div>

          <label 
            v-else
            class="flex flex-col items-center justify-center p-6 border-2 border-dashed border-[#E3DFD6] hover:border-[#1A1A17] rounded-[12px] bg-[#F7F5F0] hover:bg-[#FFFDF5] cursor-pointer transition-all space-y-1.5"
          >
            <Camera class="w-6 h-6 text-[#5E5B53]" />
            <span class="text-[13px] font-medium text-[#1A1A17]">Click to snap or upload target photo</span>
            <span class="text-[11px] text-[#5E5B53]">JPG, PNG or mobile camera capture</span>
            <input type="file" accept="image/*" capture="environment" @change="handlePhotoSelect" class="hidden" />
          </label>
        </div>

        <!-- Section 2: Investigation Letter / Report -->
        <div class="space-y-1.5">
          <div class="flex justify-between items-center">
            <label class="block text-[13px] font-semibold text-[#1A1A17]">
              2. Field Investigation Letter / Intelligence Report *
            </label>
            <span class="text-[11px] font-medium" :class="investigationLetter.length >= 35 ? 'text-[#1E7B4F]' : 'text-[#5E5B53]'">
              {{ investigationLetter.length }} / 35 min chars
            </span>
          </div>
          <textarea 
            v-model="investigationLetter"
            rows="4"
            placeholder="Document your on-site observations in full detail: time of arrival, subject/vehicle identification numbers, origin findings, situational context, and conclusions..."
            class="w-full px-3.5 py-2.5 rounded-[10px] border border-[#E3DFD6] bg-[#F7F5F0] text-[13px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17] leading-relaxed"
          ></textarea>
        </div>

        <!-- Section 3: Intelligence Source Attribution -->
        <div class="space-y-2">
          <label class="block text-[13px] font-semibold text-[#1A1A17]">
            3. Declared Intelligence Source *
          </label>
          <input 
            v-model="sourceInfo"
            placeholder="e.g. Direct Physical Surveillance, Eyewitness Interview, Municipal Vehicle Registry, Maritime Port Records"
            class="w-full px-3.5 py-2 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[13px] text-[#1A1A17] focus:outline-none focus:border-[#1A1A17]"
          />
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="text-[11px] text-[#5E5B53]">Quick presets:</span>
            <button 
              type="button"
              v-for="src in ['Physical Surveillance', 'Eyewitness Account', 'Municipal Records', 'On-Site Inspection']"
              :key="src"
              @click="applySampleSource(src)"
              class="px-2 py-0.5 rounded-[4px] bg-[#F7F5F0] hover:bg-[#EAE6DC] border border-[#E3DFD6] text-[11px] text-[#5E5B53] transition-colors"
            >
              {{ src }}
            </button>
          </div>
        </div>

        <!-- Section 4: Supporting Document Attachment (Optional) -->
        <div class="space-y-1.5 pt-1 border-t border-[#E3DFD6]">
          <div class="flex items-center justify-between">
            <label class="text-[12px] font-medium text-[#5E5B53] flex items-center gap-1">
              <Paperclip class="w-3.5 h-3.5" />
              <span>Attach Supporting Document (.pdf, .txt, .md)</span>
            </label>
            <span class="text-[11px] text-[#5E5B53] italic">Optional</span>
          </div>

          <div v-if="docFile" class="flex items-center justify-between p-2 rounded-[8px] bg-[#F7F5F0] border border-[#E3DFD6] text-[12px]">
            <span class="font-medium text-[#1A1A17] truncate max-w-xs">{{ docFile.name }}</span>
            <button @click="docFile = null" class="text-[#B42318] hover:underline text-[11px]">Remove</button>
          </div>

          <label v-else class="inline-flex items-center gap-2 px-3 py-1.5 rounded-[8px] bg-[#F7F5F0] hover:bg-[#EAE6DC] border border-[#E3DFD6] text-[12px] text-[#1A1A17] cursor-pointer transition-colors">
            <Upload class="w-3.5 h-3.5 text-[#5E5B53]" />
            <span>Select file</span>
            <input type="file" accept=".pdf,.txt,.md,.doc,.docx" @change="handleDocSelect" class="hidden" />
          </label>
        </div>

        <!-- Validation Error Message -->
        <div v-if="formError" class="p-2.5 rounded-[8px] bg-[#FAECEB] border border-[#FDA29B] text-[#B42318] text-[12px] font-medium">
          {{ formError }}
        </div>

      </div>

      <!-- Sticky Footer Actions -->
      <div class="px-6 py-4 border-t border-[#E3DFD6] bg-[#F7F5F0] flex items-center justify-between shrink-0">
        <button 
          @click="$emit('close')"
          type="button"
          class="px-4 py-2 rounded-[10px] text-[13px] font-medium text-[#5E5B53] hover:text-[#1A1A17]"
        >
          Cancel
        </button>

        <button 
          @click="handleSubmit"
          :disabled="submitting"
          type="button"
          class="px-6 py-2.5 rounded-[10px] bg-[#FFD60A] hover:brightness-95 text-[#1A1A17] font-semibold text-[14px] transition-all flex items-center gap-2 shadow-xs cursor-pointer disabled:opacity-50"
        >
          <span v-if="submitting">Transmitting Dossier to Gemini...</span>
          <span v-else>Submit Dossier for Escrow Verification</span>
        </button>
      </div>

    </div>
  </div>
</template>
