import axios from 'axios'
import type {
  ExecuteResponse,
  GenerateResponse,
  PreviewData,
  RevertResponse,
  UploadResponse,
  VersionListResponse,
} from '../types'

const api = axios.create({
  baseURL: '/api',
})

export async function uploadCsv(file: File): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post<UploadResponse>('/upload', formData)
  return data
}

export async function getPreview(
  sessionId: string,
  page = 1,
  pageSize = 50,
): Promise<PreviewData> {
  const { data } = await api.get<PreviewData>(
    `/sessions/${sessionId}/preview`,
    { params: { page, page_size: pageSize } },
  )
  return data
}

export async function generateCode(
  sessionId: string,
  query: string,
): Promise<GenerateResponse> {
  const { data } = await api.post<GenerateResponse>(
    `/sessions/${sessionId}/generate`,
    { query },
  )
  return data
}

export async function executeCode(
  sessionId: string,
  code: string,
  query: string,
): Promise<ExecuteResponse> {
  const { data } = await api.post<ExecuteResponse>(
    `/sessions/${sessionId}/execute`,
    { code, query },
  )
  return data
}

export async function getVersions(
  sessionId: string,
): Promise<VersionListResponse> {
  const { data } = await api.get<VersionListResponse>(
    `/sessions/${sessionId}/versions`,
  )
  return data
}

export async function revertToVersion(
  sessionId: string,
  versionId: number,
): Promise<RevertResponse> {
  const { data } = await api.post<RevertResponse>(
    `/sessions/${sessionId}/versions/${versionId}/revert`,
  )
  return data
}

export function getDownloadUrl(sessionId: string): string {
  return `/api/sessions/${sessionId}/download`
}
