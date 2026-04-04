import { ref, onMounted } from 'vue'
import {
  onAuthStateChanged,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  GoogleAuthProvider,
  type User,
} from 'firebase/auth'
import { auth } from '../firebase'

const user = ref<User | null>(null)
const isAuthLoading = ref(true)
const authError = ref<string | null>(null)

let listenerAttached = false

function attachListener() {
  if (listenerAttached) return
  listenerAttached = true
  onAuthStateChanged(auth, (firebaseUser) => {
    user.value = firebaseUser
    isAuthLoading.value = false
  })
}

export function useAuth() {
  onMounted(() => {
    attachListener()
  })

  async function loginWithGoogle() {
    authError.value = null
    try {
      const provider = new GoogleAuthProvider()
      await signInWithPopup(auth, provider)
    } catch (err: unknown) {
      authError.value = err instanceof Error ? err.message : 'Google sign-in failed'
    }
  }

  async function loginWithEmail(email: string, password: string) {
    authError.value = null
    try {
      await signInWithEmailAndPassword(auth, email, password)
    } catch (err: unknown) {
      authError.value = err instanceof Error ? err.message : 'Sign-in failed'
    }
  }

  async function registerWithEmail(email: string, password: string) {
    authError.value = null
    try {
      await createUserWithEmailAndPassword(auth, email, password)
    } catch (err: unknown) {
      authError.value = err instanceof Error ? err.message : 'Registration failed'
    }
  }

  async function logout() {
    authError.value = null
    try {
      await signOut(auth)
    } catch (err: unknown) {
      authError.value = err instanceof Error ? err.message : 'Sign-out failed'
    }
  }

  async function getIdToken(): Promise<string | null> {
    if (!user.value) return null
    try {
      return await user.value.getIdToken()
    } catch {
      return null
    }
  }

  return {
    user,
    isAuthLoading,
    authError,
    loginWithGoogle,
    loginWithEmail,
    registerWithEmail,
    logout,
    getIdToken,
  }
}
