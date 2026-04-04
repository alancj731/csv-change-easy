<script setup lang="ts">
import { ref, onMounted } from 'vue'
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
import AuthButton from '../components/AuthButton.vue'

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

const showSidebar = ref(false)

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
  showSidebar.value = false
}

function handlePageChange(newPage: number) {
  fetchPreview(props.sessionId, newPage)
}
</script>

<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <header class="flex items-center justify-between px-3 sm:px-6 py-3 bg-white border-b gap-2">
      <div class="flex items-center gap-2 sm:gap-4 min-w-0">
        <h1 class="text-base sm:text-lg font-bold text-gray-800 whitespace-nowrap">CSV Processor</h1>
        <button
          class="text-xs sm:text-sm text-gray-500 hover:text-gray-700 whitespace-nowrap"
          @click="emit('reset')"
        >
          New file
        </button>
      </div>
      <div class="flex items-center gap-2 sm:gap-4">
        <!-- Versions toggle (mobile only) -->
        <button
          class="lg:hidden text-sm text-gray-500 hover:text-gray-700 px-2 py-1 border rounded"
          @click="showSidebar = !showSidebar"
        >
          Versions
        </button>
        <div class="hidden sm:block">
          <AuthButton />
        </div>
        <DownloadButton :session-id="sessionId" />
      </div>
    </header>

    <!-- Mobile auth row -->
    <div class="sm:hidden flex justify-end px-3 py-2 bg-white border-b">
      <AuthButton />
    </div>

    <div class="flex flex-1 overflow-hidden relative">
      <!-- Main content -->
      <main class="flex-1 flex flex-col p-3 sm:p-4 gap-3 sm:gap-4 overflow-y-auto">
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

      <!-- Sidebar overlay (mobile) -->
      <div
        v-if="showSidebar"
        class="lg:hidden fixed inset-0 bg-black/30 z-40"
        @click="showSidebar = false"
      />

      <!-- Sidebar -->
      <aside
        class="bg-white border-l overflow-y-auto z-50 transition-transform duration-200
          fixed right-0 top-0 h-full w-72 p-4 lg:relative lg:translate-x-0 lg:block"
        :class="showSidebar ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'"
      >
        <div class="lg:hidden flex justify-between items-center mb-4">
          <h3 class="text-sm font-semibold text-gray-700">Versions</h3>
          <button class="text-gray-400 hover:text-gray-600 text-lg" @click="showSidebar = false">&times;</button>
        </div>
        <VersionSidebar
          :versions="versions"
          :is-reverting="isReverting"
          @revert="handleRevert"
        />
      </aside>
    </div>
  </div>
</template>
