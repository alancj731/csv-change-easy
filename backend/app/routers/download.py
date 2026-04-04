from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services import session_manager, version_service

router = APIRouter()


@router.get("/sessions/{session_id}/download")
async def download_csv(session_id: str) -> FileResponse:
    session_dir = session_manager.get_session_dir(session_id)
    current_path = version_service.get_current_csv_path(session_dir)

    return FileResponse(
        path=current_path,
        media_type="text/csv",
        filename="result.csv",
    )
