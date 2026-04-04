import sqlite3
import time
from pathlib import Path

from app.config import settings

_db_path: Path | None = None

def _data_dir() -> Path:
    return settings.upload_dir


def _get_db_path() -> Path:
    global _db_path
    if _db_path is None:
        data_dir = _data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)
        _db_path = data_dir / "rate_limits.db"
    return _db_path


def _get_conn() -> sqlite3.Connection:
    return sqlite3.connect(str(_get_db_path()))


def init_db() -> None:
    """Create the usage table and clean up old entries. Call at app startup."""
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    conn = _get_conn()
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS usage ("
            "  identity TEXT NOT NULL,"
            "  identity_type TEXT NOT NULL,"
            "  timestamp REAL NOT NULL"
            ")"
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_identity_ts ON usage(identity, timestamp)")
        conn.commit()
    finally:
        conn.close()

    cleanup_old_entries()


def cleanup_old_entries() -> int:
    """Delete entries older than 24 hours. Returns count of deleted rows."""
    cutoff = time.time() - 86400
    conn = _get_conn()
    try:
        cursor = conn.execute("DELETE FROM usage WHERE timestamp < ?", (cutoff,))
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def get_usage_count(identity: str) -> int:
    """Get number of conversions for an identity in the last 24 hours."""
    cutoff = time.time() - 86400
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT COUNT(*) FROM usage WHERE identity = ? AND timestamp >= ?",
            (identity, cutoff),
        ).fetchone()
        return row[0] if row else 0
    finally:
        conn.close()


def check_rate_limit_anonymous(ip: str) -> None:
    """Raise RateLimitError if anonymous IP has exceeded daily limit."""
    from app.exceptions import RateLimitError

    count = get_usage_count(f"ip:{ip}")
    if count >= settings.anonymous_daily_limit:
        raise RateLimitError(
            f"Daily limit of {settings.anonymous_daily_limit} conversions reached. "
            "Sign in for more."
        )


def check_rate_limit_authenticated(user_id: str) -> None:
    """Raise RateLimitError if authenticated user has exceeded daily limit."""
    from app.exceptions import RateLimitError

    count = get_usage_count(f"user:{user_id}")
    if count >= settings.authenticated_daily_limit:
        raise RateLimitError(
            f"Daily limit of {settings.authenticated_daily_limit} conversions reached. "
            f"Contact {settings.contact_email} to request more."
        )


def record_usage(identity: str, identity_type: str) -> None:
    """Record a conversion for an identity."""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO usage (identity, identity_type, timestamp) VALUES (?, ?, ?)",
            (identity, identity_type, time.time()),
        )
        conn.commit()
    finally:
        conn.close()
