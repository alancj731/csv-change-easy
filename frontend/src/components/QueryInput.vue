<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  isProcessing: boolean
  error: string | null
}>()

const emit = defineEmits<{
  submit: [query: string]
}>()

const query = ref('')

function handleSubmit() {
  const trimmed = query.value.trim()
  if (!trimmed) return
  emit('submit', trimmed)
  query.value = ''
}
</script>

<template>
  <div>
    <form class="flex gap-2" @submit.prevent="handleSubmit">
      <input
        v-model="query"
        type="text"
        placeholder="Describe what you want to do with the data..."
        class="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        :disabled="isProcessing"
      />
      <button
        type="submit"
        :disabled="isProcessing || !query.trim()"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-40 transition-colors"
      >
        {{ isProcessing ? 'Generating...' : 'Generate' }}
      </button>
    </form>
    <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>
  </div>
</template>
