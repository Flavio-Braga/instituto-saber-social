"""Password hashing helpers (bcrypt). Kept separate from auth.py so the seed
script can hash passwords without importing the Flask-Login machinery."""

import bcrypt


def hash_password(plain: str) -> str:
    """Return a bcrypt hash (utf-8 string) for the given plaintext password."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        # Stored value is not a valid bcrypt hash (e.g. legacy plaintext data).
        return False
