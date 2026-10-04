<script setup lang="ts">
import { ExternalLink } from 'lucide-vue-next'

const props = defineProps<{
  signature: string
  label?: string
}>()

const explorerUrl = `https://explorer.solana.com/tx/${props.signature}?cluster=devnet`
</script>

<template>
  <a 
    :href="explorerUrl" 
    target="_blank" 
    rel="noopener noreferrer"
    class="inline-flex items-center gap-1 font-mono text-[11px] text-[#6B675E] dark:text-[#9E9A90] hover:text-[#E8590C] hover:underline"
  >
    <span v-if="label" class="uppercase text-[9px] text-[#6B675E] dark:text-[#9E9A90]">{{ label }}:</span>
    <span>{{ signature.slice(0, 8) }}...{{ signature.slice(-6) }}</span>
    <ExternalLink class="w-3 h-3 shrink-0" />
  </a>
</template>
