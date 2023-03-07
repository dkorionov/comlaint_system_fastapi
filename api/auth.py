from fastapi import APIRouter, Request, Response

from managers.user import UserManager
from schemas.user import UserRegister, UserLoginIn

router = APIRouter(tags=["auth"])


@router.post("/register/", status_code=201)
async def register(user_data: UserRegister):
    token = await UserManager.register(user_data.dict())
    return {"token": token}


@router.post("/login/", status_code=200)
async def login(user_data: UserLoginIn):
    user_dict = user_data.dict()
    token = await UserManager.login(user_dict["email"], user_dict["password"])
    return {"token": token}
