<script setup lang="ts">
import { FolderSearch } from 'lucide-vue-next'

defineProps<{
  title: string
  description: string
  actionLabel?: string
}>()

defineEmits<{
  (e: 'action'): void
}>()
</script>

<template>
  <div class="w-full p-8 md:p-12 flex flex-col items-center justify-center text-center space-y-3 bg-white">
    <div class="w-12 h-12 rounded-full bg-[#F7F5F0] border border-[#E3DFD6] flex items-center justify-center text-[#5E5B53]">
      <FolderSearch class="w-6 h-6" />
    </div>
    
    <div class="space-y-1 max-w-sm">
      <h3 class="text-[16px] font-semibold text-[#1A1A17]">{{ title }}</h3>
      <p class="text-[13px] text-[#5E5B53] leading-relaxed">{{ description }}</p>
    </div>

    <div v-if="actionLabel" class="pt-2">
      <button 
        @click="$emit('action')"
        class="h-9 px-4 rounded-[10px] bg-[#1A1A17] text-white hover:bg-[#33332D] text-[13px] font-medium transition-colors"
      >
        {{ actionLabel }}
      </button>
    </div>
  </div>
</template>
