<script setup lang="ts">
import { ref } from 'vue'
import { Image, X } from 'lucide-vue-next'

const emit = defineEmits<{
  (e: 'updatePhotos', urls: string[]): void
}>()

const photoUrls = ref<string[]>([])

const handleFile = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return

  const file = target.files[0]
  const reader = new FileReader()
  reader.onload = (event) => {
    if (event.target?.result && photoUrls.value.length < 3) {
      photoUrls.value.push(event.target.result as string)
      emit('updatePhotos', photoUrls.value)
    }
  }
  reader.readAsDataURL(file)
}

const removePhoto = (idx: number) => {
  photoUrls.value.splice(idx, 1)
  emit('updatePhotos', photoUrls.value)
}
</script>

<template>
  <div class="space-y-2 text-left">
    <label class="text-[13px] font-medium text-[#5E5B53] block">
      Reference photos (optional, up to 3)
    </label>

    <div class="flex items-center gap-3">
      <!-- Uploaded thumbnails -->
      <div 
        v-for="(url, idx) in photoUrls" 
        :key="idx" 
        class="w-16 h-16 rounded-[8px] border border-[#E3DFD6] relative overflow-hidden group shrink-0"
      >
        <img :src="url" class="w-full h-full object-cover" />
        <button 
          @click="removePhoto(idx)"
          class="absolute top-1 right-1 p-0.5 bg-black/60 rounded-full text-white hover:bg-black"
        >
          <X class="w-3 h-3" />
        </button>
      </div>

      <!-- Add photo button -->
      <label 
        v-if="photoUrls.length < 3"
        class="w-16 h-16 rounded-[8px] border border-dashed border-[#E3DFD6] hover:border-[#1A1A17] bg-[#F7F5F0] flex flex-col items-center justify-center cursor-pointer transition-colors shrink-0"
      >
        <Image class="w-4 h-4 text-[#5E5B53]" />
        <span class="text-[10px] text-[#5E5B53] mt-1">+ Photo</span>
        <input type="file" accept="image/*" @change="handleFile" class="hidden" />
      </label>
    </div>
  </div>
</template>
