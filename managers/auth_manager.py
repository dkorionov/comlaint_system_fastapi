import datetime
from typing import Optional
from starlette.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from decouple import config
from db import database
from models.user import user_model, RoleType
from fastapi import HTTPException


class AuthManager:
    @staticmethod
    def encode_token(user_object):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
                'iat': datetime.datetime.utcnow(),
                'sub': user_object.id
            }
            return jwt.encode(
                payload,
                config('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as ex:
            # log the exception
            raise ex


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        result = await super().__call__(request)
        try:
            payload = jwt.decode(result.credentials, config('SECRET_KEY'), algorithms=['HS256'])
            user_object = await database.fetch_one(user_model.select().where(user_model.c.id == payload['sub']))
            request.state.user = user_object
            return user_object
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, 'Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(401, 'Invalid token')


oauth2_scheme = CustomHTTPBearer()


def is_complainer(request: Request):
    if not request.state.user['role'] == RoleType.COMPLAINER:
        raise HTTPException(403, 'Forbidden')


def is_approver(request: Request):
    if not request.state.user['role'] == RoleType.APPROVER:
        raise HTTPException(403, 'Forbidden')


def is_admin(request: Request):
    if not request.state.user['role'] == RoleType.ADMIN:
        raise HTTPException(403, 'Forbidden')
