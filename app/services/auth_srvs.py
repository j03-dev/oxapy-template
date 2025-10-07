from oxapy import exceptions  # type: ignore
from sqlalchemy.orm import Session

from app.models import User
from app.core.config import JWT
from app.repositories.user_repo import get_user_by_email
from app.serializers.user_serializer import UserSerializer, Crendential

import typing


def login(db: Session, crendential: Crendential) -> str:
    data = crendential.validated_data
    assert data, "Invalid crendential data"
    if user := get_user_by_email(db, data["email"]):
        if user.password == data["password"]:
            claims = {"sub": user.id}
            token = JWT.generate_token(claims)
            return token
    raise exceptions.UnauthorizedError("Invalid credentials")


def register(db: Session, new_user: UserSerializer) -> typing.Optional[User]:
    data = new_user.validated_data
    assert data, "Invalid user data"
    if get_user_by_email(db, data["email"]):
        raise exceptions.ConflictError("Email already registered")
    return new_user.save(db)
