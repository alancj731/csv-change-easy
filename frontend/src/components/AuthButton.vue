<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'

const { user, isAuthLoading, authError, loginWithGoogle, loginWithEmail, registerWithEmail, logout } = useAuth()

const showEmailForm = ref(false)
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
    showEmailForm.value = false
    email.value = ''
    password.value = ''
  }
}

function toggleMode() {
  isRegisterMode.value = !isRegisterMode.value
  authError.value = null
}
</script>

<template>
  <div class="flex items-center gap-3">
    <template v-if="isAuthLoading">
      <span class="text-sm text-gray-400">Loading...</span>
    </template>

    <template v-else-if="user">
      <span class="text-sm text-gray-600">{{ user.email }}</span>
      <span class="text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded">50MB limit</span>
      <button
        class="text-sm text-gray-500 hover:text-gray-700"
        @click="logout"
      >
        Logout
      </button>
    </template>

    <template v-else>
      <span class="text-xs text-amber-600 bg-amber-50 px-2 py-0.5 rounded">1MB limit</span>

      <button
        class="text-sm px-3 py-1 bg-white border rounded hover:bg-gray-50 transition-colors"
        @click="loginWithGoogle"
      >
        Sign in with Google
      </button>

      <button
        class="text-sm text-blue-600 hover:text-blue-800"
        @click="showEmailForm = !showEmailForm"
      >
        {{ showEmailForm ? 'Cancel' : 'Email' }}
      </button>
    </template>
  </div>

  <!-- Email/password dropdown form -->
  <div
    v-if="!user && showEmailForm"
    class="absolute right-4 top-14 z-50 bg-white border rounded-lg shadow-lg p-4 w-72"
  >
    <form class="space-y-3" @submit.prevent="handleEmailSubmit">
      <h3 class="text-sm font-medium text-gray-700">
        {{ isRegisterMode ? 'Create Account' : 'Sign In' }}
      </h3>
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full px-3 py-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="w-full px-3 py-2 border rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        class="w-full py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
      >
        {{ isRegisterMode ? 'Register' : 'Sign In' }}
      </button>
      <button
        type="button"
        class="w-full text-xs text-gray-500 hover:text-gray-700"
        @click="toggleMode"
      >
        {{ isRegisterMode ? 'Already have an account? Sign in' : "Don't have an account? Register" }}
      </button>
      <p v-if="authError" class="text-xs text-red-600">{{ authError }}</p>
    </form>
  </div>
</template>
