import { ref } from 'vue'
import type { PreviewData } from '../types'
import { generateCode, executeCode } from '../api/client'

export interface QueryEntry {
  query: string
  code: string
  timestamp: number
  success: boolean
  resultType: 'transform' | 'analysis'
  analysisResult?: string
  error?: string
}

export interface ExecuteResult {
  resultType: 'transform' | 'analysis'
  preview: PreviewData | null
  analysisResult: string | null
}

export function useQueryHistory() {
  const queries = ref<QueryEntry[]>([])
  const isGenerating = ref(false)
  const isExecuting = ref(false)
  const generatedCode = ref<string | null>(null)
  const pendingQuery = ref<string | null>(null)
  const queryError = ref<string | null>(null)
  const analysisResult = ref<string | null>(null)

  function _extractError(err: unknown): string {
    if (err && typeof err === 'object' && 'response' in err) {
      const axiosErr = err as { response?: { data?: { detail?: string } } }
      return axiosErr.response?.data?.detail ?? 'Request failed'
    }
    return 'Request failed'
  }

  async function generate(sessionId: string, query: string) {
    isGenerating.value = true
    queryError.value = null
    generatedCode.value = null
    pendingQuery.value = query

    try {
      const response = await generateCode(sessionId, query)
      generatedCode.value = response.code
    } catch (err: unknown) {
      queryError.value = _extractError(err)
      pendingQuery.value = null
    } finally {
      isGenerating.value = false
    }
  }

  async function execute(
    sessionId: string,
    code: string,
  ): Promise<ExecuteResult | null> {
    isExecuting.value = true
    queryError.value = null
    const query = pendingQuery.value ?? ''

    try {
      const response = await executeCode(sessionId, code, query)
      queries.value = [
        ...queries.value,
        {
          query,
          code,
          timestamp: Date.now(),
          success: true,
          resultType: response.result_type,
          analysisResult: response.analysis_result ?? undefined,
        },
      ]
      generatedCode.value = null
      pendingQuery.value = null

      if (response.result_type === 'analysis') {
        analysisResult.value = response.analysis_result
      } else {
        analysisResult.value = null
      }

      return {
        resultType: response.result_type,
        preview: response.preview,
        analysisResult: response.analysis_result,
      }
    } catch (err: unknown) {
      const message = _extractError(err)
      queryError.value = message
      queries.value = [
        ...queries.value,
        { query, code, timestamp: Date.now(), success: false, resultType: 'transform', error: message },
      ]
      return null
    } finally {
      isExecuting.value = false
    }
  }

  function cancelGenerated() {
    generatedCode.value = null
    pendingQuery.value = null
    queryError.value = null
  }

  function dismissAnalysis() {
    analysisResult.value = null
  }

  return {
    queries,
    isGenerating,
    isExecuting,
    generatedCode,
    pendingQuery,
    queryError,
    analysisResult,
    generate,
    execute,
    cancelGenerated,
    dismissAnalysis,
  }
}
