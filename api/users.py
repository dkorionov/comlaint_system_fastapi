from typing import List, Optional

from fastapi import APIRouter, Depends

from managers.auth_manager import oauth2_scheme, is_admin
from managers.user import UserManager
from models import RoleType
from schemas.user import UserOut

router = APIRouter(tags=["users"])


@router.get("/", status_code=200, dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
            response_model=List[UserOut])
async def get_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.put("/{user_id}/make-admin/", status_code=200, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def change_role(user_id: int):
    return await UserManager.change_role(RoleType.ADMIN, user_id)


@router.put("/{user_id}/make-approver/", status_code=200, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def change_role(user_id: int):
    return await UserManager.change_role(RoleType.APPROVER, user_id)
