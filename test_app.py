"""End-to-end tests for the register/login system.

Covers the core behavior and the specific bugs fixed in the audit pass:
- duplicate-username registration is rejected (even with a different password),
- login succeeds with the right password and returns a token,
- login fails with the wrong password,
- passwords are stored hashed, not in plaintext.
"""

import uuid

from fastapi.testclient import TestClient

from main import app
from models import Person, Session
from security import hash_password, verify_password

client = TestClient(app)


def _unique_user():
    return "user_" + uuid.uuid4().hex[:8]


def test_register_succeeds():
    user = _unique_user()
    resp = client.post(
        "/register", json={"name": "Alice", "user": user, "passwd": "pw1"}
    )
    assert resp.status_code == 200
    assert resp.json() == {"status": "success"}


def test_duplicate_username_rejected_even_with_different_password():
    user = _unique_user()
    first = client.post(
        "/register", json={"name": "Alice", "user": user, "passwd": "pw1"}
    )
    assert first.json() == {"status": "success"}

    second = client.post(
        "/register", json={"name": "Eve", "user": user, "passwd": "DIFFERENT"}
    )
    assert second.json() == {"status": "User already registered"}

    # Only one row should exist for that username.
    session = Session()
    try:
        rows = session.query(Person).filter_by(user=user).all()
        assert len(rows) == 1
    finally:
        session.close()


def test_login_success_returns_token():
    user = _unique_user()
    client.post("/register", json={"name": "Bob", "user": user, "passwd": "secret"})

    resp = client.post("/login", json={"user": user, "passwd": "secret"})
    assert resp.status_code == 200
    body = resp.json()
    assert "token" in body
    assert isinstance(body["token"], str)
    assert len(body["token"]) > 0


def test_login_wrong_password_rejected():
    user = _unique_user()
    client.post("/register", json={"name": "Carol", "user": user, "passwd": "right"})

    resp = client.post("/login", json={"user": user, "passwd": "wrong"})
    assert resp.json() == {"status": "user not registered"}


def test_login_unknown_user_rejected():
    resp = client.post(
        "/login", json={"user": _unique_user(), "passwd": "whatever"}
    )
    assert resp.json() == {"status": "user not registered"}


def test_password_stored_hashed_not_plaintext():
    user = _unique_user()
    client.post("/register", json={"name": "Dan", "user": user, "passwd": "plaintext"})

    session = Session()
    try:
        person = session.query(Person).filter_by(user=user).first()
        assert person is not None
        assert person.passwd != "plaintext"
        assert person.passwd.startswith("pbkdf2_sha256$")
    finally:
        session.close()


def test_token_rotates_on_second_login():
    user = _unique_user()
    client.post("/register", json={"name": "Erin", "user": user, "passwd": "pw"})

    first = client.post("/login", json={"user": user, "passwd": "pw"}).json()["token"]
    second = client.post("/login", json={"user": user, "passwd": "pw"}).json()["token"]
    assert first != second


def test_security_helper_roundtrip():
    stored = hash_password("hunter2")
    assert verify_password("hunter2", stored)
    assert not verify_password("wrong", stored)
    assert not verify_password("hunter2", "garbage")
