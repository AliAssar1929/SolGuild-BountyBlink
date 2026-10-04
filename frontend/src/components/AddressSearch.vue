<script setup lang="ts">
import { ref } from 'vue'
import { Search, Loader2, MapPin } from 'lucide-vue-next'

const emit = defineEmits<{
  (e: 'selectAddress', item: {
    display_name: string
    lat: number
    lon: number
    place_name: string
    full_address: string
    city: string
    country: string
  }): void
}>()

const query = ref('')
const results = ref<any[]>([])
const loading = ref(false)
const showDropdown = ref(false)

let debounceTimer: any = null

const handleInput = () => {
  clearTimeout(debounceTimer)
  if (!query.value || query.value.length < 3) {
    results.value = []
    showDropdown.value = false
    return
  }

  debounceTimer = setTimeout(async () => {
    loading.value = true
    try {
      const res = await fetch(`/api/geo/search?q=${encodeURIComponent(query.value)}`)
      results.value = await res.json()
      showDropdown.value = true
    } catch (e) {
      console.error(e)
    } finally {
      loading.value = false
    }
  }, 350)
}

const selectItem = (item: any) => {
  const parts = item.display_name.split(',')
  const placeName = parts[0]?.trim() || item.display_name
  const city = item.address?.city || item.address?.town || item.address?.state || 'Berlin'
  const country = item.address?.country || 'Germany'

  emit('selectAddress', {
    display_name: item.display_name,
    lat: parseFloat(item.lat),
    lon: parseFloat(item.lon),
    place_name: placeName,
    full_address: item.display_name,
    city: city,
    country: country
  })

  query.value = item.display_name
  showDropdown.value = false
}
</script>

<template>
  <div class="relative text-left">
    <div class="relative">
      <Search class="w-4 h-4 text-[#5E5B53] absolute left-3 top-3" />
      <input 
        v-model="query"
        @input="handleInput"
        placeholder="Search street, number, place or city..."
        class="w-full pl-9 pr-8 py-2.5 rounded-[8px] border border-[#E3DFD6] bg-[#F7F5F0] text-[15px] text-[#1A1A17] placeholder-[#5E5B53] focus:outline-none focus:border-[#1A1A17]"
      />
      <Loader2 v-if="loading" class="w-4 h-4 text-[#5E5B53] animate-spin absolute right-3 top-3" />
    </div>

    <!-- Dropdown results -->
    <div 
      v-if="showDropdown && results.length > 0"
      class="absolute left-0 right-0 top-full mt-1 bg-white border border-[#E3DFD6] rounded-[8px] shadow-lg z-30 divide-y divide-[#E3DFD6] overflow-hidden"
    >
      <div 
        v-for="(r, idx) in results" 
        :key="idx"
        @click="selectItem(r)"
        class="p-3 text-[14px] text-[#1A1A17] hover:bg-[#F7F5F0] cursor-pointer flex items-start gap-2.5 transition-colors"
      >
        <MapPin class="w-4 h-4 text-[#E8590C] shrink-0 mt-0.5" />
        <span class="line-clamp-2 leading-snug">{{ r.display_name }}</span>
      </div>
    </div>
  </div>
</template>
