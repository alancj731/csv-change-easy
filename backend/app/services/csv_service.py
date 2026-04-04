from pathlib import Path

import pandas as pd

from app.models.schemas import PreviewData


def save_uploaded_csv(content: bytes, dest: Path) -> None:
    dest.write_bytes(content)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def get_preview(path: Path, page: int = 1, page_size: int = 50) -> PreviewData:
    df = pd.read_csv(path)
    total_rows = len(df)

    start = (page - 1) * page_size
    end = start + page_size
    page_df = df.iloc[start:end]

    return PreviewData(
        columns=list(df.columns),
        rows=page_df.to_dict(orient="records"),
        total_rows=total_rows,
        page=page,
        page_size=page_size,
    )


def get_preview_from_df(df: pd.DataFrame, page: int = 1, page_size: int = 50) -> PreviewData:
    total_rows = len(df)

    start = (page - 1) * page_size
    end = start + page_size
    page_df = df.iloc[start:end]

    return PreviewData(
        columns=list(df.columns),
        rows=page_df.to_dict(orient="records"),
        total_rows=total_rows,
        page=page,
        page_size=page_size,
    )
