from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import (
    AIQueryError,
    InvalidFileError,
    SessionNotFoundError,
    VersionNotFoundError,
    ai_query_handler,
    invalid_file_handler,
    session_not_found_handler,
    version_not_found_handler,
)
from app.routers import download, query, upload, versions
from app.services.session_manager import cleanup_expired_sessions


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    cleanup_expired_sessions()
    yield


app = FastAPI(title="Process CSV", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(SessionNotFoundError, session_not_found_handler)
app.add_exception_handler(VersionNotFoundError, version_not_found_handler)
app.add_exception_handler(InvalidFileError, invalid_file_handler)
app.add_exception_handler(AIQueryError, ai_query_handler)

app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(versions.router, prefix="/api")
app.include_router(download.router, prefix="/api")
