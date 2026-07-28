from __future__ import annotations

from app.core.security import hash_password, verify_password


def test_password_hashing_roundtrip() -> None:
    password = "VeryStrongPassword!123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
