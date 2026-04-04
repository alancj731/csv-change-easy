import json
import shutil
import time
from pathlib import Path

import pandas as pd

from app.config import settings
from app.exceptions import VersionNotFoundError
from app.models.schemas import VersionInfo
from app.services.csv_service import read_csv, write_csv


def _versions_file(session_dir: Path) -> Path:
    return session_dir / "versions.json"


def _load_versions(session_dir: Path) -> list[dict]:
    vf = _versions_file(session_dir)
    return json.loads(vf.read_text())


def _save_versions(session_dir: Path, versions: list[dict]) -> None:
    vf = _versions_file(session_dir)
    vf.write_text(json.dumps(versions, indent=2))


def _current_csv(session_dir: Path) -> Path:
    return session_dir / "current.csv"


def create_version(
    session_dir: Path,
    df: pd.DataFrame,
    query: str,
) -> int:
    versions = _load_versions(session_dir)
    version_id = len(versions)
    ts = time.time()
    filename = f"v{version_id}_{int(ts)}.csv"

    write_csv(df, session_dir / filename)
    write_csv(df, _current_csv(session_dir))

    versions.append({
        "id": version_id,
        "timestamp": ts,
        "query": query,
        "filename": filename,
        "row_count": len(df),
        "col_count": len(df.columns),
    })

    if len(versions) > settings.max_versions_per_session:
        oldest = versions.pop(1)
        old_file = session_dir / oldest["filename"]
        if old_file.exists():
            old_file.unlink()

    _save_versions(session_dir, versions)
    return version_id


def create_initial_version(session_dir: Path, csv_path: Path) -> int:
    df = read_csv(csv_path)
    shutil.copy2(csv_path, _current_csv(session_dir))

    ts = time.time()
    filename = "v0_original.csv"
    shutil.copy2(csv_path, session_dir / filename)

    versions = [{
        "id": 0,
        "timestamp": ts,
        "query": "Original upload",
        "filename": filename,
        "row_count": len(df),
        "col_count": len(df.columns),
    }]
    _save_versions(session_dir, versions)
    return 0


def list_versions(session_dir: Path) -> list[VersionInfo]:
    versions = _load_versions(session_dir)
    return [VersionInfo(**v) for v in versions]


def revert_to_version(session_dir: Path, version_id: int) -> pd.DataFrame:
    versions = _load_versions(session_dir)

    target = None
    for v in versions:
        if v["id"] == version_id:
            target = v
            break

    if target is None:
        raise VersionNotFoundError(session_dir.name, version_id)

    version_file = session_dir / target["filename"]
    df = read_csv(version_file)

    create_version(session_dir, df, f"Reverted to version {version_id}")
    return df


def get_current_csv_path(session_dir: Path) -> Path:
    return _current_csv(session_dir)


def get_current_df(session_dir: Path) -> pd.DataFrame:
    return read_csv(_current_csv(session_dir))
