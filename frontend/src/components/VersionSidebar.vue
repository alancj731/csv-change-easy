<script setup lang="ts">
import type { VersionInfo } from '../types'

defineProps<{
  versions: VersionInfo[]
  isReverting: boolean
}>()

const emit = defineEmits<{
  revert: [versionId: number]
}>()

function formatTime(ts: number) {
  return new Date(ts * 1000).toLocaleTimeString()
}
</script>

<template>
  <div class="space-y-2">
    <h3 class="text-sm font-medium text-gray-500">Versions</h3>
    <div
      v-for="version in [...versions].reverse()"
      :key="version.id"
      class="text-sm px-3 py-2 bg-gray-50 rounded-lg"
    >
      <div class="flex justify-between items-start">
        <div>
          <span class="font-medium">v{{ version.id }}</span>
          <span class="text-xs text-gray-400 ml-2">{{ formatTime(version.timestamp) }}</span>
        </div>
        <button
          v-if="version.id < versions.length - 1"
          :disabled="isReverting"
          class="text-xs text-blue-600 hover:text-blue-800 disabled:opacity-40"
          @click="emit('revert', version.id)"
        >
          Revert
        </button>
      </div>
      <p class="text-xs text-gray-500 mt-1 truncate">{{ version.query }}</p>
      <p class="text-xs text-gray-400">{{ version.row_count }} rows, {{ version.col_count }} cols</p>
    </div>
  </div>
</template>
