from fastapi import APIRouter, Depends, UploadFile

from app.config import settings
from app.dependencies import optional_user
from app.exceptions import InvalidFileError
from app.models.schemas import UploadResponse
from app.services import csv_service, session_manager, version_service

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile,
    user: dict | None = Depends(optional_user),
) -> UploadResponse:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise InvalidFileError("Only .csv files are accepted")

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)

    if user is None:
        max_size = settings.max_file_size_mb_anonymous
        if size_mb > max_size:
            raise InvalidFileError(
                f"File too large: {size_mb:.1f}MB. "
                f"Anonymous users are limited to {max_size}MB. "
                f"Sign in to upload files up to  {settings.max_file_size_mb} MB."
                f"Email to winnipegdatafan@gmail.com for uploading even larger file."
            )
    else:
        max_size = settings.max_file_size_mb
        if size_mb > max_size:
            raise InvalidFileError(f"File too large: {size_mb:.1f}MB (max {max_size}MB)")

    session_id, session_dir = session_manager.create_session()

    upload_path = session_dir / "upload.csv"
    csv_service.save_uploaded_csv(content, upload_path)

    try:
        version_id = version_service.create_initial_version(session_dir, upload_path)
    except Exception as e:
        session_manager.delete_session(session_id)
        raise InvalidFileError(f"Failed to parse CSV: {e}") from e

    upload_path.unlink(missing_ok=True)

    preview = csv_service.get_preview(
        version_service.get_current_csv_path(session_dir),
        page=1,
        page_size=settings.preview_page_size,
    )

    return UploadResponse(session_id=session_id, preview=preview, version_id=version_id)
