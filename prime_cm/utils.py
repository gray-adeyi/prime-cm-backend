from typing import Optional
from passlib.context import CryptContext
from datetime import datetime
from prime_cm.models.user import (
    AccessTokenORM,
    AdminUser,
    AdminUserORM,
    AccessToken
)
from tortoise.exceptions import DoesNotExist

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate(phone_number: str, password: str) -> Optional[AdminUser]:
    try:
        admin = await AdminUserORM.get(phone_number=phone_number)
    except DoesNotExist:
        return None

    if not verify_password(password, admin.hashed_password):
        return None

    return AdminUser.from_orm(admin)


async def create_access_token(admin: AdminUser) -> AccessToken:
    # TODO: Stop generating new tokens if they already exist
    # in the Database
    access_token = AccessToken(admin_id=admin.id)
    access_token_obj, _ = await AccessTokenORM.get_or_create(**access_token.dict())
    return AccessToken.from_orm(access_token_obj)
