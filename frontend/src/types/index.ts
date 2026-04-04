export interface PreviewData {
  columns: string[]
  rows: Record<string, unknown>[]
  total_rows: number
  page: number
  page_size: number
}

export interface UploadResponse {
  session_id: string
  preview: PreviewData
  version_id: number
}

export interface GenerateRequest {
  query: string
}

export interface GenerateResponse {
  code: string
  query: string
}

export interface ExecuteRequest {
  code: string
  query: string
}

export interface ExecuteResponse {
  result_type: 'transform' | 'analysis'
  preview: PreviewData | null
  version_id: number | null
  query_applied: string
  code_executed: string
  analysis_result: string | null
}

export interface VersionInfo {
  id: number
  timestamp: number
  query: string
  row_count: number
  col_count: number
}

export interface VersionListResponse {
  versions: VersionInfo[]
}

export interface RevertResponse {
  preview: PreviewData
  version_id: number
}

export interface ErrorResponse {
  detail: string
}
