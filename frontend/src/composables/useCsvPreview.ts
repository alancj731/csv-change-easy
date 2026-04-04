import { ref } from 'vue'
import type { PreviewData } from '../types'
import { getPreview } from '../api/client'

export function useCsvPreview() {
  const columns = ref<string[]>([])
  const rows = ref<Record<string, unknown>[]>([])
  const totalRows = ref(0)
  const page = ref(1)
  const pageSize = ref(50)
  const isLoading = ref(false)

  function applyPreview(preview: PreviewData) {
    columns.value = preview.columns
    rows.value = preview.rows
    totalRows.value = preview.total_rows
    page.value = preview.page
    pageSize.value = preview.page_size
  }

  async function fetchPreview(sessionId: string, newPage?: number) {
    isLoading.value = true
    try {
      const targetPage = newPage ?? page.value
      const preview = await getPreview(sessionId, targetPage, pageSize.value)
      applyPreview(preview)
    } finally {
      isLoading.value = false
    }
  }

  const totalPages = () => Math.ceil(totalRows.value / pageSize.value)

  return {
    columns,
    rows,
    totalRows,
    page,
    pageSize,
    isLoading,
    applyPreview,
    fetchPreview,
    totalPages,
  }
}
