from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    firebase_project_id: str = ""
    upload_dir: Path = Path("/tmp/process-csv-sessions")
    max_file_size_mb: int = 50
    max_file_size_mb_anonymous: int = 1
    anonymous_daily_limit: int = 3
    authenticated_daily_limit: int = 10
    contact_email: str = "winnipegdatafan@gmail.com"
    session_ttl_hours: int = 24
    pandasai_timeout_seconds: int = 30
    preview_page_size: int = 50
    max_versions_per_session: int = 50

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
