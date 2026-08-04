from fastapi import APIRouter, Depends, Request

from app.config import settings
from app.dependencies import optional_user
from app.models.schemas import ExecuteRequest, ExecuteResponse, GenerateRequest, GenerateResponse
from app.services import csv_service, session_manager, version_service
from app.services.ai_service import execute_code, generate_code
from app.services.rate_limiter import check_rate_limit_anonymous, check_rate_limit_authenticated, record_usage

router = APIRouter()


def _get_usage_identity(http_request: Request, user: dict | None) -> tuple[str, str] | None:
    client_ip = http_request.client.host if http_request.client else "unknown"
    is_local = client_ip in ("127.0.0.1", "::1", "localhost")

    if is_local:
        return None

    if user is None:
        check_rate_limit_anonymous(client_ip)
        return (f"ip:{client_ip}", "anonymous")

    user_id = user.get("uid", "")
    check_rate_limit_authenticated(user_id)
    return (f"user:{user_id}", "authenticated")


@router.post("/sessions/{session_id}/generate", response_model=GenerateResponse)
async def generate_query_code(
    session_id: str,
    request: GenerateRequest,
    http_request: Request,
    user: dict | None = Depends(optional_user),
) -> GenerateResponse:
    session_dir = session_manager.get_session_dir(session_id)
    current_df = version_service.get_current_df(session_dir)
    usage_identity = _get_usage_identity(http_request, user)

    code = generate_code(current_df, request.query)

    if usage_identity is not None:
        record_usage(*usage_identity)

    return GenerateResponse(code=code, query=request.query)


@router.post("/sessions/{session_id}/execute", response_model=ExecuteResponse)
async def execute_query_code(
    session_id: str,
    request: ExecuteRequest,
) -> ExecuteResponse:
    session_dir = session_manager.get_session_dir(session_id)
    current_df = version_service.get_current_df(session_dir)

    result_type, result_df, analysis_text = execute_code(current_df, request.code)

    if result_type == "transform" and result_df is not None:
        version_id = version_service.create_version(session_dir, result_df, request.query)

        preview = csv_service.get_preview_from_df(
            result_df,
            page=1,
            page_size=settings.preview_page_size,
        )
        return ExecuteResponse(
            result_type="transform",
            preview=preview,
            version_id=version_id,
            query_applied=request.query,
            code_executed=request.code,
        )

    return ExecuteResponse(
        result_type="analysis",
        query_applied=request.query,
        code_executed=request.code,
        analysis_result=analysis_text,
    )
