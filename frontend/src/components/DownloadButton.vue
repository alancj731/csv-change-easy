<script setup lang="ts">
import { getDownloadUrl } from '../api/client'

const props = defineProps<{
  sessionId: string
}>()

function handleDownload() {
  window.open(getDownloadUrl(props.sessionId), '_blank')
}
</script>

<template>
  <button
    class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
    @click="handleDownload"
  >
    Download CSV
  </button>
</template>
