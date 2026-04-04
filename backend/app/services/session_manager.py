import json
import shutil
import time
import uuid
from pathlib import Path

from app.config import settings
from app.exceptions import SessionNotFoundError


def _sessions_root() -> Path:
    return settings.upload_dir


def create_session() -> tuple[str, Path]:
    session_id = uuid.uuid4().hex
    session_dir = _sessions_root() / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    versions_file = session_dir / "versions.json"
    versions_file.write_text(json.dumps([]))

    return session_id, session_dir


def get_session_dir(session_id: str) -> Path:
    session_dir = _sessions_root() / session_id
    if not session_dir.exists():
        raise SessionNotFoundError(session_id)
    return session_dir


def cleanup_expired_sessions() -> int:
    root = _sessions_root()
    if not root.exists():
        return 0

    cutoff = time.time() - (settings.session_ttl_hours * 3600)
    removed = 0

    for session_dir in root.iterdir():
        if not session_dir.is_dir():
            continue
        versions_file = session_dir / "versions.json"
        if versions_file.exists() and versions_file.stat().st_mtime < cutoff:
            shutil.rmtree(session_dir)
            removed += 1

    return removed


def delete_session(session_id: str) -> None:
    session_dir = get_session_dir(session_id)
    shutil.rmtree(session_dir)
