<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'

const { user, isAuthLoading, authError, loginWithGoogle, loginWithEmail, registerWithEmail, logout } = useAuth()

const showDropdown = ref(false)
const isRegisterMode = ref(false)
const email = ref('')
const password = ref('')

async function handleEmailSubmit() {
  if (!email.value || !password.value) return
  if (isRegisterMode.value) {
    await registerWithEmail(email.value, password.value)
  } else {
    await loginWithEmail(email.value, password.value)
  }
  if (!authError.value) {
    showDropdown.value = false
    email.value = ''
    password.value = ''
  }
}

function toggleMode() {
  isRegisterMode.value = !isRegisterMode.value
  authError.value = null
}

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
  authError.value = null
}
</script>

<template>
  <div class="relative">
    <!-- Loading -->
    <div v-if="isAuthLoading" class="h-9 w-20 bg-slate-100 rounded-lg animate-pulse" />

    <!-- Logged in -->
    <div v-else-if="user" class="flex items-center gap-2">
      <div class="flex items-center gap-2 bg-white border border-slate-200 rounded-full pl-2 sm:pl-3 pr-1 py-1">
        <div class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center shrink-0">
          <span class="text-xs font-medium text-blue-600">{{ (user.email || '?')[0].toUpperCase() }}</span>
        </div>
        <span class="text-sm text-slate-600 max-w-[120px] sm:max-w-[200px] truncate">{{ user.email }}</span>
        <button
          class="text-xs text-slate-400 hover:text-slate-600 px-2 py-1 rounded-full hover:bg-slate-100 transition-colors whitespace-nowrap"
          @click="logout"
        >
          Sign out
        </button>
      </div>
    </div>

    <!-- Not logged in -->
    <div v-else class="flex items-center gap-1 sm:gap-2">
      <button
        class="flex items-center gap-2 text-sm text-slate-600 hover:text-slate-800 px-2 sm:px-3 py-2 rounded-lg hover:bg-white/60 transition-colors whitespace-nowrap"
        @click="toggleDropdown"
      >
        <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
        </svg>
        <span class="hidden sm:inline">Sign Up</span>
      </button>
      <button
        class="flex items-center gap-2 text-sm font-medium text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 px-3 sm:px-4 py-2 rounded-lg transition-colors shadow-sm whitespace-nowrap"
        @click="loginWithGoogle"
      >
        <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
          <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
          <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
          <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
          <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
        </svg>
        <span class="hidden sm:inline">Sign in</span>
      </button>
    </div>

    <!-- Auth error (shown when not logged in) -->
    <p v-if="!user && authError && !showDropdown" class="absolute right-0 top-12 z-50 text-xs text-red-500 bg-red-50 border border-red-200 rounded-lg px-3 py-2 w-72 shadow">
      {{ authError }}
    </p>

    <!-- Email dropdown -->
    <div
      v-if="!user && showDropdown"
      class="absolute right-0 top-12 z-50 bg-white border border-slate-200 rounded-xl shadow-xl p-5 w-72 sm:w-80"
    >
      <form class="space-y-3" @submit.prevent="handleEmailSubmit">
        <h3 class="text-sm font-semibold text-slate-800">
          {{ isRegisterMode ? 'Create account' : 'Sign in with email' }}
        </h3>
        <input
          v-model="email"
          type="email"
          placeholder="Email address"
          class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="submit"
          class="w-full py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          {{ isRegisterMode ? 'Create account' : 'Sign in' }}
        </button>
        <p class="text-center">
          <button
            type="button"
            class="text-xs text-slate-400 hover:text-blue-600 transition-colors"
            @click="toggleMode"
          >
            {{ isRegisterMode ? 'Already have an account? Sign in' : "Don't have an account? Register" }}
          </button>
        </p>
        <p v-if="authError" class="text-xs text-red-500 bg-red-50 rounded-lg px-3 py-2">{{ authError }}</p>
      </form>
    </div>
  </div>
</template>
