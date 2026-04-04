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
    <div v-if="isAuthLoading" class="h-9 w-24 bg-slate-100 rounded-lg animate-pulse" />

    <!-- Logged in -->
    <div v-else-if="user" class="flex items-center gap-3">
      <div class="flex items-center gap-2 bg-white border border-slate-200 rounded-full pl-3 pr-1 py-1">
        <div class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
          <span class="text-xs font-medium text-blue-600">{{ (user.email || '?')[0].toUpperCase() }}</span>
        </div>
        <span class="text-sm text-slate-600 max-w-[160px] truncate">{{ user.email }}</span>
        <button
          class="text-xs text-slate-400 hover:text-slate-600 px-2 py-1 rounded-full hover:bg-slate-100 transition-colors"
          @click="logout"
        >
          Sign out
        </button>
      </div>
    </div>

    <!-- Not logged in -->
    <div v-else class="flex items-center gap-2">
      <button
        class="text-sm text-slate-600 hover:text-slate-800 px-3 py-2 rounded-lg hover:bg-white/60 transition-colors"
        @click="toggleDropdown"
      >
        Sign in
      </button>
      <button
        class="text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors shadow-sm"
        @click="loginWithGoogle"
      >
        Sign in with Google
      </button>
    </div>

    <!-- Email dropdown -->
    <div
      v-if="!user && showDropdown"
      class="absolute right-0 top-12 z-50 bg-white border border-slate-200 rounded-xl shadow-xl p-5 w-80"
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
