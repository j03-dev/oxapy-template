from sqlalchemy.orm import Session
from app.models import User
import typing


def get_user_by_id(db: Session, user_id: str) -> typing.Optional[User]:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> typing.Optional[User]:
    return db.query(User).filter(User.email == email).first()
