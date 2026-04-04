import time

import httpx
import jwt
from cryptography.x509 import load_pem_x509_certificate

from app.config import settings

GOOGLE_CERTS_URL = "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"

_cached_certs: dict[str, str] = {}
_certs_expiry: float = 0


def _fetch_google_certs() -> dict[str, str]:
    """Fetch Google's public certificates for Firebase token verification."""
    global _cached_certs, _certs_expiry

    if _cached_certs and time.time() < _certs_expiry:
        return _cached_certs

    response = httpx.get(GOOGLE_CERTS_URL, timeout=10)
    response.raise_for_status()
    _cached_certs = response.json()

    cache_control = response.headers.get("Cache-Control", "")
    max_age = 3600
    for part in cache_control.split(","):
        part = part.strip()
        if part.startswith("max-age="):
            max_age = int(part.split("=")[1])
            break
    _certs_expiry = time.time() + max_age

    return _cached_certs


def verify_token(token: str) -> dict | None:
    """Verify a Firebase ID token using Google's public keys.

    No service account file needed — only requires FIREBASE_PROJECT_ID.
    """
    if not settings.firebase_project_id:
        return None

    try:
        certs = _fetch_google_certs()

        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if not kid or kid not in certs:
            return None

        cert_pem = certs[kid].encode()
        cert = load_pem_x509_certificate(cert_pem)
        public_key = cert.public_key()

        decoded = jwt.decode(
            token,
            key=public_key,
            algorithms=["RS256"],
            audience=settings.firebase_project_id,
            issuer=f"https://securetoken.google.com/{settings.firebase_project_id}",
        )

        return decoded

    except (jwt.PyJWTError, httpx.HTTPError, Exception) as e:
        print(f"[auth] Token verification failed: {type(e).__name__}: {e}")
        return None
