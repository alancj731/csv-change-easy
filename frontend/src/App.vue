<script setup lang="ts">
import { useSession } from './composables/useSession'
import UploadView from './views/UploadView.vue'
import WorkspaceView from './views/WorkspaceView.vue'

const { sessionId, initialPreview, isUploading, uploadError, createSession, resetSession } = useSession()
</script>

<template>
  <WorkspaceView
    v-if="sessionId && initialPreview"
    :session-id="sessionId"
    :initial-preview="initialPreview"
    @reset="resetSession"
  />
  <UploadView
    v-else
    :is-uploading="isUploading"
    :error="uploadError"
    @upload="createSession"
  />
</template>
