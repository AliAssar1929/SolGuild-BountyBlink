<script setup lang="ts">
import { MapPin, Navigation, X } from 'lucide-vue-next'

defineProps<{
  show: boolean
  activeCity: string
}>()

defineEmits<{
  (e: 'useLocation'): void
  (e: 'selectCity', city: string): void
  (e: 'dismiss'): void
}>()

const cities = ['Berlin', 'Paris', 'London', 'Tokyo']
</script>

<template>
  <div v-if="show" class="p-3 bg-white border border-[#E3DFD6] rounded-[12px] shadow-xs text-left space-y-2.5 relative">
    <button @click="$emit('dismiss')" class="absolute top-2 right-2 p-1 text-[#5E5B53] hover:text-[#1A1A17]">
      <X class="w-3.5 h-3.5" />
    </button>

    <div class="flex items-center gap-2">
      <MapPin class="w-4 h-4 text-[#1A1A17]" />
      <span class="font-semibold text-[13px] text-[#1A1A17]">Filter tasks by location</span>
    </div>

    <div class="flex flex-wrap items-center gap-2 pt-1">
      <button 
        @click="$emit('useLocation')"
        class="h-8 px-3 rounded-[8px] bg-[#1A1A17] text-white text-[12px] font-medium flex items-center gap-1.5 hover:bg-[#33332D] transition-colors shrink-0"
      >
        <Navigation class="w-3.5 h-3.5 text-[#FFD60A]" />
        <span>Use my location</span>
      </button>

      <span class="text-[12px] text-[#5E5B53] shrink-0">or pick:</span>

      <div class="flex items-center gap-1.5 flex-wrap">
        <button 
          v-for="c in cities" 
          :key="c"
          @click="$emit('selectCity', c)"
          class="px-2.5 py-1 rounded-[6px] text-[12px] font-medium transition-colors"
          :class="activeCity === c ? 'bg-[#FFD60A] text-[#1A1A17] font-semibold' : 'bg-[#F7F5F0] text-[#5E5B53] hover:text-[#1A1A17] hover:bg-[#EAE6DC]'"
        >
          {{ c }}
        </button>
      </div>
    </div>
  </div>
</template>
