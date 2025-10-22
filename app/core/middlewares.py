from oxapy import Request, Status, jwt

from app.core.config import JWT, DB
from app.repositories import user_repo

import typing

type Next = typing.Callable[[Request], typing.Any]


def jwt_middleware(request: Request, next: Next, **kwargs):
    if token := request.headers.get("authorization", "").replace("Bearer ", ""):
        db = DB()
        try:
            claims = JWT.verify_token(token)
            user = user_repo.get_user_by_id(db, claims["sub"])
            assert user, "User not found"
            setattr(request, "user", user)
            return next(request, **kwargs)
        except jwt.JwtError as e:
            return {"detail": str(e)}, Status.BAD_REQUEST
        finally:
            db.close()
    return {"detail": "Authorization header missing"}, Status.UNAUTHORIZED


def db_session_middleware(request: Request, next: Next, **kwargs):
    db = DB()
    try:
        setattr(request, "db", db)
        return next(request, **kwargs)
    finally:
        db.close()
