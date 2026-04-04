<script setup lang="ts">
import FileUpload from '../components/FileUpload.vue'

defineProps<{
  isUploading: boolean
  error: string | null
}>()

const emit = defineEmits<{
  upload: [file: File]
}>()
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-lg">
      <h1 class="text-2xl font-bold text-center mb-8 text-gray-800">CSV Processor</h1>
      <FileUpload @upload="(file) => emit('upload', file)" />
      <div v-if="isUploading" class="mt-4 text-center text-gray-500">Uploading...</div>
      <p v-if="error" class="mt-4 text-center text-sm text-red-600">{{ error }}</p>
    </div>
  </div>
</template>
