<script setup lang="ts">
import { useAuth } from '../composables/useAuth'
import FileUpload from '../components/FileUpload.vue'
import AuthButton from '../components/AuthButton.vue'

const { user } = useAuth()

defineProps<{
  isUploading: boolean
  error: string | null
}>()

const emit = defineEmits<{
  upload: [file: File]
}>()
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 relative">
    <!-- Header -->
    <header class="flex items-center justify-between px-4 sm:px-8 py-4">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shrink-0">
          <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <span class="text-lg font-semibold text-slate-800 hidden sm:inline">CSV Processor</span>
      </div>
      <AuthButton />
    </header>

    <!-- Hero -->
    <div class="flex items-center justify-center px-4 sm:px-6" style="min-height: calc(100vh - 72px)">
      <div class="w-full max-w-2xl">
        <div class="text-center mb-8 sm:mb-10">
          <h1 class="text-2xl sm:text-4xl font-bold text-slate-900 mb-3 tracking-tight">
            Transform your CSV with AI
          </h1>
          <p class="text-base sm:text-lg text-slate-500 max-w-md mx-auto">
            Upload a CSV file, describe changes in plain English, and download the result.
          </p>
        </div>

        <!-- Upload area -->
        <FileUpload @upload="(file) => emit('upload', file)" />

        <div v-if="isUploading" class="mt-6 text-center">
          <div class="inline-flex items-center gap-2 text-blue-600">
            <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <span class="text-sm font-medium">Uploading and parsing...</span>
          </div>
        </div>

        <p v-if="error" class="mt-4 text-center text-sm text-red-600 bg-red-50 rounded-lg py-2 px-4">
          {{ error }}
        </p>

        <!-- Features -->
        <div class="mt-10 sm:mt-12 grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 text-center">
          <div class="flex sm:flex-col items-center sm:items-center gap-3 sm:gap-0 sm:space-y-2 bg-white/60 sm:bg-transparent rounded-xl p-3 sm:p-0">
            <div class="w-10 h-10 shrink-0 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div class="text-left sm:text-center">
              <h3 class="text-sm font-semibold text-slate-700">Natural Language</h3>
              <p class="text-xs text-slate-400">Describe changes in plain English</p>
            </div>
          </div>
          <div class="flex sm:flex-col items-center sm:items-center gap-3 sm:gap-0 sm:space-y-2 bg-white/60 sm:bg-transparent rounded-xl p-3 sm:p-0">
            <div class="w-10 h-10 shrink-0 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="text-left sm:text-center">
              <h3 class="text-sm font-semibold text-slate-700">Version History</h3>
              <p class="text-xs text-slate-400">Revert to any previous state</p>
            </div>
          </div>
          <div class="flex sm:flex-col items-center sm:items-center gap-3 sm:gap-0 sm:space-y-2 bg-white/60 sm:bg-transparent rounded-xl p-3 sm:p-0">
            <div class="w-10 h-10 shrink-0 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </div>
            <div class="text-left sm:text-center">
              <h3 class="text-sm font-semibold text-slate-700">Review Code</h3>
              <p class="text-xs text-slate-400">Inspect and edit generated pandas code</p>
            </div>
          </div>
        </div>

        <!-- Limit info -->
        <p class="mt-8 sm:mt-10 text-center text-xs text-slate-400 pb-6">
          <template v-if="user">
            Signed in &middot; 4MB per file &middot; 10 conversions/day &middot;
            Need more? Contact <a href="mailto:winnipegdatafan@gmail.com" class="text-blue-500 hover:underline">winnipegdatafan@gmail.com</a>
          </template>
          <template v-else>
            Free to use &middot; 1MB file limit &middot; 3 conversions/day &middot;
            <span class="text-blue-500">Sign in for 10/day</span>
          </template>
        </p>

      </div>
    </div>

    <!-- GitHub link - fixed to bottom -->
    <div class="absolute bottom-12 left-0 right-0 text-center">
      <a href="https://github.com/alancj731/csv-change-easy" target="_blank" rel="noopener noreferrer"
         class="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-600 transition-colors">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</template>
