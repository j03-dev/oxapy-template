from sqlalchemy.orm import Session
from oxapy import exceptions

from app.serializers.user_serializer import UpdateUserSerializer
from app.repositories import user_repo
from app.models import User

import typing


def update_user(
    db: Session,
    user_id: str,
    new_user: UpdateUserSerializer,
) -> typing.Optional[User]:
    if user := user_repo.get_user_by_id(db, user_id):
        return new_user.update(db, user, new_user.validated_data)
    raise exceptions.NotFoundError(f"User with ID: {id} is not found")
