<script setup lang="ts">
import { ref } from 'vue'
import type { QueryEntry } from '../composables/useQueryHistory'

defineProps<{
  queries: QueryEntry[]
}>()

const expandedIdx = ref<number | null>(null)

function toggleExpand(idx: number) {
  expandedIdx.value = expandedIdx.value === idx ? null : idx
}

function formatTime(ts: number) {
  return new Date(ts).toLocaleTimeString()
}
</script>

<template>
  <div v-if="queries.length > 0" class="space-y-2">
    <h3 class="text-sm font-medium text-gray-500">Query History</h3>
    <div
      v-for="(entry, idx) in [...queries].reverse()"
      :key="idx"
      class="text-sm rounded-lg overflow-hidden"
      :class="entry.success ? 'bg-green-50' : 'bg-red-50'"
    >
      <div
        class="px-3 py-2 cursor-pointer flex justify-between items-start"
        :class="entry.success ? 'text-green-800' : 'text-red-800'"
        @click="toggleExpand(queries.length - 1 - idx)"
      >
        <div class="flex-1">
          <span class="font-medium">{{ entry.query }}</span>
          <p v-if="entry.error" class="text-xs mt-1 opacity-75">{{ entry.error }}</p>
        </div>
        <span class="text-xs opacity-60 ml-2 whitespace-nowrap">{{ formatTime(entry.timestamp) }}</span>
      </div>
      <div
        v-if="expandedIdx === queries.length - 1 - idx"
        class="px-3 pb-2"
      >
        <pre class="text-xs bg-gray-900 text-green-300 p-2 rounded font-mono overflow-x-auto">{{ entry.code }}</pre>
      </div>
    </div>
  </div>
</template>
