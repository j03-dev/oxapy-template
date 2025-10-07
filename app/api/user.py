from oxapy import Router, Request, Status
from app.core.middlewares import jwt_middleware, db_session_middleware

router = Router()
router.middleware(jwt_middleware)
router.middleware(db_session_middleware)