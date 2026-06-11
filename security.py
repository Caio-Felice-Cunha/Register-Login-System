"""Password hashing helpers.

Uses PBKDF2-HMAC-SHA256 from the standard library (no extra dependencies) with a
random per-user salt. The stored value is self-describing so the algorithm and
iteration count can change later without breaking existing hashes:

    pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>
"""

import hashlib
import hmac
import os

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 240_000
SALT_BYTES = 16


def hash_password(password: str, *, iterations: int = ITERATIONS) -> str:
    """Return a salted PBKDF2 hash string for the given plaintext password."""
    salt = os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"{ALGORITHM}${iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Verify a plaintext password against a stored hash string.

    Returns False (rather than raising) on any malformed stored value.
    """
    try:
        algorithm, iterations_str, salt_hex, hash_hex = stored.split("$")
    except (ValueError, AttributeError):
        return False
    if algorithm != ALGORITHM:
        return False
    try:
        iterations = int(iterations_str)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
    except ValueError:
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(digest, expected)
