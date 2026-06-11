"""FastAPI register/login endpoints.

Credentials are sent in the JSON request body (not query params, so they do not
leak into URLs or access logs). Passwords are stored as salted PBKDF2 hashes.
"""

from datetime import datetime, timezone
from secrets import token_hex

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session as OrmSession

from models import Person, Session, Tokens
from security import hash_password, verify_password

app = FastAPI(title="Register-Login-System")


def get_session():
    """Yield a database session and always close it afterwards."""
    session = Session()
    try:
        yield session
    finally:
        session.close()


class RegisterRequest(BaseModel):
    name: str
    user: str
    passwd: str


class LoginRequest(BaseModel):
    user: str
    passwd: str


@app.post("/register")
def register(body: RegisterRequest, session: OrmSession = Depends(get_session)):
    # Existence check is by username only: the same user cannot be registered
    # twice regardless of the password supplied.
    existing_user = session.query(Person).filter_by(user=body.user).first()
    if existing_user is not None:
        return {"status": "User already registered"}

    person = Person(
        name=body.name,
        user=body.user,
        passwd=hash_password(body.passwd),
    )
    session.add(person)
    session.commit()
    return {"status": "success"}


@app.post("/login")
def login(body: LoginRequest, session: OrmSession = Depends(get_session)):
    person = session.query(Person).filter_by(user=body.user).first()
    if person is None or not verify_password(body.passwd, person.passwd):
        return {"status": "user not registered"}

    # Generate a token that does not already exist.
    while True:
        token = token_hex(50)
        if session.query(Tokens).filter_by(token=token).first() is None:
            break

    existing_token = session.query(Tokens).filter_by(id_person=person.id).first()
    if existing_token is None:
        session.add(Tokens(id_person=person.id, token=token))
    else:
        # Rotate the token and refresh its issue date.
        existing_token.token = token
        existing_token.date = datetime.now(timezone.utc)

    session.commit()
    return {"token": token}
