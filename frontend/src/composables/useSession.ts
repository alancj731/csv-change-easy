import { ref } from 'vue'
import type { PreviewData } from '../types'
import { uploadCsv } from '../api/client'

const sessionId = ref<string | null>(null)
const initialPreview = ref<PreviewData | null>(null)
const isUploading = ref(false)
const uploadError = ref<string | null>(null)

export function useSession() {
  async function createSession(file: File) {
    isUploading.value = true
    uploadError.value = null

    try {
      const response = await uploadCsv(file)
      sessionId.value = response.session_id
      initialPreview.value = response.preview
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } }
        uploadError.value = axiosErr.response?.data?.detail ?? 'Upload failed'
      } else {
        uploadError.value = 'Upload failed'
      }
    } finally {
      isUploading.value = false
    }
  }

  function resetSession() {
    sessionId.value = null
    initialPreview.value = null
  }

  return {
    sessionId,
    initialPreview,
    isUploading,
    uploadError,
    createSession,
    resetSession,
  }
}
