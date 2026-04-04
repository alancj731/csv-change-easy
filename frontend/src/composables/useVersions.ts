import { ref } from 'vue'
import type { VersionInfo, PreviewData } from '../types'
import { getVersions, revertToVersion } from '../api/client'

export function useVersions() {
  const versions = ref<VersionInfo[]>([])
  const isReverting = ref(false)
  const revertError = ref<string | null>(null)

  async function fetchVersions(sessionId: string) {
    const response = await getVersions(sessionId)
    versions.value = response.versions
  }

  async function revert(
    sessionId: string,
    versionId: number,
  ): Promise<PreviewData | null> {
    isReverting.value = true
    revertError.value = null

    try {
      const response = await revertToVersion(sessionId, versionId)
      await fetchVersions(sessionId)
      return response.preview
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } }
        revertError.value = axiosErr.response?.data?.detail ?? 'Revert failed'
      } else {
        revertError.value = 'Revert failed'
      }
      return null
    } finally {
      isReverting.value = false
    }
  }

  return {
    versions,
    isReverting,
    revertError,
    fetchVersions,
    revert,
  }
}
