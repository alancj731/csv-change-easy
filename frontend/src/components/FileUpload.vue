<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  upload: [file: File]
}>()

const isDragging = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

function handleDrop(e: DragEvent) {
  isDragging.value = false
  const file = e.dataTransfer?.files[0]
  if (file && file.name.toLowerCase().endsWith('.csv')) {
    emit('upload', file)
  }
}

function handleFileSelect(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    emit('upload', file)
  }
}

function openFilePicker() {
  fileInput.value?.click()
}
</script>

<template>
  <div
    class="relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200"
    :class="isDragging
      ? 'border-blue-400 bg-blue-50 shadow-lg shadow-blue-100'
      : 'border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50 hover:shadow-md'"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    @drop.prevent="handleDrop"
    @click="openFilePicker"
  >
    <input
      ref="fileInput"
      type="file"
      accept=".csv"
      class="hidden"
      @change="handleFileSelect"
    />
    <div class="flex flex-col items-center gap-3">
      <div
        class="w-14 h-14 rounded-full flex items-center justify-center transition-colors"
        :class="isDragging ? 'bg-blue-100' : 'bg-slate-100'"
      >
        <svg
          class="w-7 h-7 transition-colors"
          :class="isDragging ? 'text-blue-500' : 'text-slate-400'"
          fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
        </svg>
      </div>
      <div>
        <p class="text-base font-medium text-slate-700">
          Drop your CSV file here
        </p>
        <p class="text-sm text-slate-400 mt-1">
          or <span class="text-blue-500 font-medium">browse</span> to choose a file
        </p>
      </div>
      <span class="inline-block text-xs text-slate-400 bg-slate-50 px-3 py-1 rounded-full">
        .csv files only
      </span>
    </div>
  </div>
</template>
