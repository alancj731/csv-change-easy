from pydantic import BaseModel


class PreviewData(BaseModel):
    columns: list[str]
    rows: list[dict]
    total_rows: int
    page: int
    page_size: int


class UploadResponse(BaseModel):
    session_id: str
    preview: PreviewData
    version_id: int


class GenerateRequest(BaseModel):
    query: str


class GenerateResponse(BaseModel):
    code: str
    query: str


class ExecuteRequest(BaseModel):
    code: str
    query: str


class ExecuteResponse(BaseModel):
    result_type: str  # "transform" or "analysis"
    preview: PreviewData | None = None
    version_id: int | None = None
    query_applied: str
    code_executed: str
    analysis_result: str | None = None


class VersionInfo(BaseModel):
    id: int
    timestamp: float
    query: str
    row_count: int
    col_count: int


class VersionListResponse(BaseModel):
    versions: list[VersionInfo]


class RevertResponse(BaseModel):
    preview: PreviewData
    version_id: int


class ErrorResponse(BaseModel):
    detail: str
