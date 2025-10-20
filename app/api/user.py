from oxapy import Router, Request

from app.core.middlewares import jwt_middleware, db_session_middleware
from app.serializers.user_serializer import UpdateUserSerializer, UserSerializer
from app.services import user_srvs

router = Router()
router.middleware(jwt_middleware)
router.middleware(db_session_middleware)


@router.get("/api/users/me")
def retrieve(request: Request):
    user_serializer = UserSerializer(instance=request.user)
    return {"users": user_serializer.data}


@router.put("/api/users")
def update(request: Request):
    new_user = UpdateUserSerializer(request.data)
    user = user_srvs.update_user(request.db, request.user.id, new_user)
    user_serializer = UserSerializer(instance=user)
    return {"users": user_serializer.data}
