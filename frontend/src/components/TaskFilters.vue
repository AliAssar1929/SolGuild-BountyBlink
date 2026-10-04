<script setup lang="ts">
import { ChevronDown } from 'lucide-vue-next'

const props = defineProps<{
  status: string
  category: string
  city: string
}>()

const emit = defineEmits<{
  (e: 'update:status', val: string): void
  (e: 'update:category', val: string): void
  (e: 'update:city', val: string): void
}>()

const categories = ['ALL', 'Civil Help', 'Sensitive', 'Commercial']
const cities = ['ALL', 'London', 'Paris', 'Berlin', 'Madrid', 'Rome', 'Amsterdam', 'Barcelona', 'Vienna']
</script>

<template>
  <div class="flex items-center gap-2 overflow-x-auto pb-1 text-[13px] text-left">
    <!-- Category Filter -->
    <div class="relative shrink-0">
      <select 
        :value="category"
        @change="$emit('update:category', ($event.target as HTMLSelectElement).value)"
        class="appearance-none pl-3 pr-7 py-1.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[#1A1A17] font-medium focus:outline-none focus:border-[#1A1A17]"
      >
        <option v-for="c in categories" :key="c" :value="c">
          {{ c === 'ALL' ? 'All categories' : c }}
        </option>
      </select>
      <ChevronDown class="w-3.5 h-3.5 text-[#5E5B53] absolute right-2 top-2.5 pointer-events-none" />
    </div>

    <!-- City Filter -->
    <div class="relative shrink-0">
      <select 
        :value="city"
        @change="$emit('update:city', ($event.target as HTMLSelectElement).value)"
        class="appearance-none pl-3 pr-7 py-1.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[#1A1A17] font-medium focus:outline-none focus:border-[#1A1A17]"
      >
        <option v-for="ct in cities" :key="ct" :value="ct">
          {{ ct === 'ALL' ? 'All cities' : ct }}
        </option>
      </select>
      <ChevronDown class="w-3.5 h-3.5 text-[#5E5B53] absolute right-2 top-2.5 pointer-events-none" />
    </div>

    <!-- Status pill -->
    <button 
      @click="$emit('update:status', status === 'OPEN' ? 'ALL' : 'OPEN')"
      class="px-2.5 py-1.5 rounded-[8px] font-medium shrink-0 transition-colors"
      :class="status === 'OPEN' ? 'bg-[#1A1A17] text-white' : 'border border-[#E3DFD6] bg-[#F7F5F0] text-[#5E5B53] hover:text-[#1A1A17]'"
    >
      {{ status === 'OPEN' ? 'Open only' : 'All status' }}
    </button>
  </div>
</template>
