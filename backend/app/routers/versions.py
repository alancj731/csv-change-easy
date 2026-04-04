from fastapi import APIRouter, Query

from app.config import settings
from app.models.schemas import PreviewData, RevertResponse, VersionListResponse
from app.services import csv_service, session_manager, version_service

router = APIRouter()


@router.get("/sessions/{session_id}/preview", response_model=PreviewData)
async def get_preview(
    session_id: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
) -> PreviewData:
    session_dir = session_manager.get_session_dir(session_id)
    current_path = version_service.get_current_csv_path(session_dir)
    return csv_service.get_preview(current_path, page=page, page_size=page_size)


@router.get("/sessions/{session_id}/versions", response_model=VersionListResponse)
async def list_versions(session_id: str) -> VersionListResponse:
    session_dir = session_manager.get_session_dir(session_id)
    versions = version_service.list_versions(session_dir)
    return VersionListResponse(versions=versions)


@router.post("/sessions/{session_id}/versions/{version_id}/revert", response_model=RevertResponse)
async def revert_version(session_id: str, version_id: int) -> RevertResponse:
    session_dir = session_manager.get_session_dir(session_id)
    version_service.revert_to_version(session_dir, version_id)

    preview = csv_service.get_preview(
        version_service.get_current_csv_path(session_dir),
        page=1,
        page_size=settings.preview_page_size,
    )

    versions = version_service.list_versions(session_dir)
    latest_version_id = versions[-1].id if versions else 0

    return RevertResponse(preview=preview, version_id=latest_version_id)
