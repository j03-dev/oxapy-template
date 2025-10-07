from oxapy import Router, Request, Status

from app.core.middlewares import db_session_middleware
from app.serializers.user_serializer import Crendential, UserSerializer
from app.services import auth_srvs

router = Router()
router.middleware(db_session_middleware)


@router.post("/api/auth/login")
def login(request: Request):
    crendential = Crendential(data=request.data)
    crendential.is_valid()
    token = auth_srvs.login(request.db, crendential)  # type: ignore
    return {"token": token}, Status.ACCEPTED


@router.post("/api/auth/register")
def register(request: Request):
    new_user = UserSerializer(data=request.data)
    new_user.is_valid()
    user = auth_srvs.register(request.db, new_user)  # type: ignore
    user_serializer = UserSerializer(instance=user)
    return {"users": user_serializer.data}, Status.CREATED
