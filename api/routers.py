from fastapi import APIRouter
from api.auth import router as auth_router
from api.complaints import router as complaints_router
from api.users import router as users_router
api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(complaints_router, prefix="/complaints")
api_router.include_router(users_router, prefix="/users")