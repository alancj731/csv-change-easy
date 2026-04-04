<script setup lang="ts">
defineProps<{
  result: string
}>()

const emit = defineEmits<{
  dismiss: []
}>()
</script>

<template>
  <div class="border rounded-lg bg-blue-50 border-blue-200 p-4">
    <div class="flex items-start justify-between">
      <div>
        <h3 class="text-sm font-medium text-blue-800 mb-2">Analysis Result</h3>
        <pre class="text-sm text-blue-900 whitespace-pre-wrap font-mono">{{ result }}</pre>
      </div>
      <button
        class="text-blue-400 hover:text-blue-600 ml-4 text-lg leading-none"
        @click="emit('dismiss')"
      >
        &times;
      </button>
    </div>
  </div>
</template>
