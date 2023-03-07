from datetime import datetime

from pydantic import BaseModel
from models.user import RoleType

class UserBase(BaseModel):
    email: str


class UserRegister(UserBase):
    password: str
    phone: str
    first_name: str
    last_name: str
    iban: str


class UserLoginIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    role: RoleType
    first_name: str
    last_name: str
    email: str
    phone: str
    joined_at: datetime
    updated_at: datetime
    iban: str
