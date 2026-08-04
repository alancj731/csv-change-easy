from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-v4-flash"
    deepseek_base_url: str = "https://api.deepseek.com"
    firebase_project_id: str = ""
    upload_dir: Path = Path("/tmp/process-csv-sessions")
    max_file_size_mb: int = 50
    max_file_size_mb_anonymous: int = 1
    anonymous_daily_limit: int = 3
    authenticated_daily_limit: int = 6
    contact_email: str = "winnipegdatafan@gmail.com"
    session_ttl_hours: int = 24
    preview_page_size: int = 50
    max_versions_per_session: int = 50

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
