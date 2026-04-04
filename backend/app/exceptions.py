from fastapi import Request
from fastapi.responses import JSONResponse


class SessionNotFoundError(Exception):
    def __init__(self, session_id: str):
        self.session_id = session_id
        super().__init__(f"Session not found: {session_id}")


class VersionNotFoundError(Exception):
    def __init__(self, session_id: str, version_id: int):
        self.session_id = session_id
        self.version_id = version_id
        super().__init__(f"Version {version_id} not found in session {session_id}")


class InvalidFileError(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class AIQueryError(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class RateLimitError(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


async def session_not_found_handler(_request: Request, exc: SessionNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def version_not_found_handler(_request: Request, exc: VersionNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


async def invalid_file_handler(_request: Request, exc: InvalidFileError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": exc.reason})


async def ai_query_handler(_request: Request, exc: AIQueryError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.reason})


async def rate_limit_handler(_request: Request, exc: RateLimitError) -> JSONResponse:
    return JSONResponse(status_code=429, content={"detail": exc.reason})
