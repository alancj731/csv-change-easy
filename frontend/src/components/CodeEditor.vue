<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  code: string
  query: string
  isExecuting: boolean
}>()

const emit = defineEmits<{
  execute: [code: string]
  cancel: []
}>()

const editableCode = ref(props.code)

watch(() => props.code, (newCode) => {
  editableCode.value = newCode
})

function handleExecute() {
  emit('execute', editableCode.value)
}
</script>

<template>
  <div class="border rounded-lg bg-gray-900 text-white overflow-hidden">
    <div class="flex items-center justify-between px-4 py-2 bg-gray-800 text-sm">
      <span class="text-gray-400">Generated code for: <span class="text-gray-200">{{ query }}</span></span>
      <div class="flex gap-2">
        <button
          class="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded transition-colors"
          @click="emit('cancel')"
        >
          Cancel
        </button>
        <button
          :disabled="isExecuting"
          class="px-3 py-1 text-sm bg-green-600 hover:bg-green-700 rounded disabled:opacity-40 transition-colors"
          @click="handleExecute"
        >
          {{ isExecuting ? 'Running...' : 'Run Code' }}
        </button>
      </div>
    </div>
    <textarea
      v-model="editableCode"
      class="w-full bg-gray-900 text-green-300 font-mono text-sm p-4 outline-none resize-y min-h-[120px]"
      spellcheck="false"
    />
  </div>
</template>
