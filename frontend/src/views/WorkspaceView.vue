<script setup lang="ts">
import { onMounted } from 'vue'
import type { PreviewData } from '../types'
import { useCsvPreview } from '../composables/useCsvPreview'
import { useQueryHistory } from '../composables/useQueryHistory'
import { useVersions } from '../composables/useVersions'
import CsvTable from '../components/CsvTable.vue'
import QueryInput from '../components/QueryInput.vue'
import CodeEditor from '../components/CodeEditor.vue'
import AnalysisResult from '../components/AnalysisResult.vue'
import QueryHistory from '../components/QueryHistory.vue'
import VersionSidebar from '../components/VersionSidebar.vue'
import DownloadButton from '../components/DownloadButton.vue'

const props = defineProps<{
  sessionId: string
  initialPreview: PreviewData
}>()

const emit = defineEmits<{
  reset: []
}>()

const { columns, rows, totalRows, page, pageSize, isLoading, applyPreview, fetchPreview } = useCsvPreview()
const {
  queries, isGenerating, isExecuting, generatedCode, pendingQuery, queryError,
  analysisResult, generate, execute, cancelGenerated, dismissAnalysis,
} = useQueryHistory()
const { versions, isReverting, fetchVersions, revert } = useVersions()

onMounted(() => {
  applyPreview(props.initialPreview)
  fetchVersions(props.sessionId)
})

async function handleGenerate(query: string) {
  await generate(props.sessionId, query)
}

async function handleExecute(code: string) {
  const result = await execute(props.sessionId, code)
  if (result && result.resultType === 'transform' && result.preview) {
    applyPreview(result.preview)
    await fetchVersions(props.sessionId)
  }
}

async function handleRevert(versionId: number) {
  const preview = await revert(props.sessionId, versionId)
  if (preview) {
    applyPreview(preview)
  }
}

function handlePageChange(newPage: number) {
  fetchPreview(props.sessionId, newPage)
}
</script>

<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="flex items-center justify-between px-6 py-3 bg-white border-b">
      <div class="flex items-center gap-4">
        <h1 class="text-lg font-bold text-gray-800">CSV Processor</h1>
        <button
          class="text-sm text-gray-500 hover:text-gray-700"
          @click="emit('reset')"
        >
          Upload new file
        </button>
      </div>
      <DownloadButton :session-id="sessionId" />
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Main content -->
      <main class="flex-1 flex flex-col p-4 gap-4 overflow-y-auto">
        <CsvTable
          :columns="columns"
          :rows="rows"
          :total-rows="totalRows"
          :page="page"
          :page-size="pageSize"
          :is-loading="isLoading"
          @page-change="handlePageChange"
        />

        <!-- Analysis result display -->
        <AnalysisResult
          v-if="analysisResult"
          :result="analysisResult"
          @dismiss="dismissAnalysis"
        />

        <!-- Query input (hidden while code is pending) -->
        <QueryInput
          v-if="!generatedCode"
          :is-processing="isGenerating"
          :error="queryError"
          @submit="handleGenerate"
        />

        <!-- Code editor (shown after generation) -->
        <CodeEditor
          v-if="generatedCode && pendingQuery"
          :code="generatedCode"
          :query="pendingQuery"
          :is-executing="isExecuting"
          @execute="handleExecute"
          @cancel="cancelGenerated"
        />

        <p v-if="queryError && generatedCode" class="text-sm text-red-600">{{ queryError }}</p>

        <QueryHistory :queries="queries" />
      </main>

      <!-- Sidebar -->
      <aside class="w-72 border-l bg-white p-4 overflow-y-auto">
        <VersionSidebar
          :versions="versions"
          :is-reverting="isReverting"
          @revert="handleRevert"
        />
      </aside>
    </div>
  </div>
</template>
