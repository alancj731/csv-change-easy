import re
from io import StringIO

import httpx
import pandas as pd

from app.config import settings
from app.exceptions import AIQueryError

DANGEROUS_PATTERNS = [
    r"\bimport\s+os\b",
    r"\bimport\s+subprocess\b",
    r"\bimport\s+shutil\b",
    r"\bopen\s*\(",
    r"\bexec\s*\(",
    r"\beval\s*\(",
    r"\b__import__\b",
    r"\bos\.\w+",
    r"\bsubprocess\.\w+",
]

SYSTEM_PROMPT = """You are a pandas code generator. Given a DataFrame description and a natural language instruction, generate ONLY Python code.

There are two types of queries:
1. TRANSFORM: modifies the DataFrame (filter, sort, add/remove columns, rename, etc.)
   - Assign the transformed DataFrame to `result`
2. ANALYSIS: asks a question about the data (count, statistics, find duplicates, etc.)
   - Assign a string answer to `result` (use str() if needed)

Rules:
- The input DataFrame is available as `df`
- Always assign output to a variable called `result`
- For TRANSFORM queries: `result` must be a pandas DataFrame
- For ANALYSIS queries: `result` must be a string with the answer
- On the FIRST line, write a comment: either `# type: transform` or `# type: analysis`
- Only use pandas and numpy (imported as pd and np)
- Do NOT import any other modules
- Do NOT use file I/O, network calls, or system commands
- Do NOT use exec, eval, or __import__
- Return ONLY the Python code, no explanations, no markdown fences
"""


def _validate_query(query: str) -> None:
    if not query or not query.strip():
        raise AIQueryError("Query cannot be empty")

    if len(query) > 2000:
        raise AIQueryError("Query too long (max 2000 characters)")


def _validate_generated_code(code: str) -> None:
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            raise AIQueryError("Generated code contains unsafe operations. Try rephrasing your query.")


def _build_prompt(df: pd.DataFrame, query: str) -> str:
    buf = StringIO()
    df.head(5).to_string(buf)
    sample = buf.getvalue()

    return f"""DataFrame info:
- Shape: {df.shape[0]} rows x {df.shape[1]} columns
- Columns: {list(df.columns)}
- Dtypes: {dict(df.dtypes.astype(str))}
- Sample (first 5 rows):
{sample}

User instruction: {query}

Generate pandas code to transform `df` and assign the result to `result`."""


def _run_generated_code(code: str, df: pd.DataFrame) -> dict:
    """Run validated pandas code in a restricted namespace.

    Security: __builtins__ is set to empty dict, only pd/np/df available.
    All code is pre-validated against dangerous patterns before reaching here.
    This is intentional — the app's core purpose is running AI-generated pandas code.
    """
    import numpy as np  # noqa: F811

    local_vars: dict = {"df": df.copy(), "pd": pd, "np": np}
    compiled = compile(code, "<generated>", "exec")
    # Intentional sandboxed eval - core app functionality
    eval(compiled, {"__builtins__": {}}, local_vars)  # noqa: S307 DL-SAFE
    return local_vars


def generate_code(df: pd.DataFrame, query: str) -> str:
    """Generate pandas code from natural language query using DeepSeek."""
    _validate_query(query)

    if not settings.deepseek_api_key:
        raise AIQueryError("DeepSeek API key not configured. Set DEEPSEEK_API_KEY in .env")

    try:
        response = httpx.post(
            f"{settings.deepseek_base_url.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.deepseek_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.deepseek_model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": _build_prompt(df, query)},
                ],
                "temperature": 0,
                "stream": False,
                "thinking": {"type": "disabled"},
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        code = data["choices"][0]["message"]["content"].strip()

        if code.startswith("```"):
            code = re.sub(r"^```(?:python)?\n?", "", code)
            code = re.sub(r"\n?```$", "", code)
            code = code.strip()

    except httpx.HTTPStatusError as e:
        detail = e.response.text
        raise AIQueryError(f"DeepSeek API call failed: {e.response.status_code} {detail}") from e
    except Exception as e:
        raise AIQueryError(f"DeepSeek API call failed: {e}") from e

    _validate_generated_code(code)
    return code


def detect_result_type(code: str) -> str:
    """Detect whether code is a transform or analysis from the first-line comment."""
    first_line = code.strip().split("\n")[0].lower()
    if "# type: analysis" in first_line:
        return "analysis"
    return "transform"


def execute_code(df: pd.DataFrame, code: str) -> tuple[str, pd.DataFrame | None, str | None]:
    """Execute pandas code against a DataFrame.

    Returns (result_type, dataframe_or_none, analysis_text_or_none).
    """
    _validate_generated_code(code)

    result_type = detect_result_type(code)

    try:
        local_vars = _run_generated_code(code, df)
        result = local_vars.get("result")
    except Exception as e:
        raise AIQueryError(f"Code execution failed: {e}") from e

    if result is None:
        raise AIQueryError("Code did not assign a value to `result`.")

    if isinstance(result, pd.DataFrame):
        return ("transform", result, None)

    if isinstance(result, pd.Series):
        return ("transform", result.to_frame(), None)

    # Anything else is treated as analysis output
    return ("analysis", None, str(result))
