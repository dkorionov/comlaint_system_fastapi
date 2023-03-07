from asyncpg import UniqueViolationError
from passlib.context import CryptContext
from db import database
from managers.auth_manager import AuthManager
from models import user_model, RoleType
from fastapi import HTTPException

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserManager:
    @staticmethod
    async def register(user_data: dict):
        user_data['password'] = pwd_context.hash(user_data['password'])
        try:
            id_ = await database.execute(user_model.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, 'User with this email already exists')
        user_do = await database.fetch_one(user_model.select().where(user_model.c.id == id_))
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(email: str, password: str):
        user = await database.fetch_one(user_model.select().where(user_model.c.email == email))
        if user is None:
            raise HTTPException(400, 'User with this email does not exist')
        if not pwd_context.verify(password, user['password']):
            raise HTTPException(400, 'Invalid password')
        return AuthManager.encode_token(user)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user_model.select())

    @staticmethod
    async def get_user_by_email(email: str):
        return await database.fetch_one(user_model.select().where(user_model.c.email == email))

    @staticmethod
    async def change_role(role: RoleType, user_id: int):
        await database.execute(user_model.update().where(user_model.c.id == user_id).values(role=role))
        return await database.fetch_one(user_model.select().where(user_model.c.id == user_id))
