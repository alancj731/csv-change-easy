from fastapi import Request

from app.services.auth_service import verify_token


async def optional_user(request: Request) -> dict | None:
    """Extract and verify Firebase auth token from request.

    Returns decoded user claims if authenticated, None otherwise.
    Does not reject unauthenticated requests.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        return None

    return verify_token(token)
