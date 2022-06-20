from os import access
from datetime import datetime
from typing import cast
from prime_cm.utils import get_password_hash
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from prime_cm.models.user import (
    AccessTokenORM,
    AdminUser,
    AdminUserCreate,
    AdminUserORM
)
from prime_cm.utils import authenticate, create_access_token

router = APIRouter()


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl='/token'))
) -> AdminUser:
    try:
        access_token: AccessTokenORM = await AccessTokenORM.get(access_token=token, expiration_date__gte=datetime.now()).prefetch_related("admin")
        return cast(AdminUser, access_token.user)
    except AdminUserORM.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/token")
async def create_token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    phone_number = form_data.username
    password = form_data.password
    admin = await authenticate(phone_number, password)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = await create_access_token(admin)
    return {"access_token": token.access_token, "token_type": "bearer"}


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=AdminUser)
async def register(new_admin: AdminUserCreate):
    """
    Note: Not to be exposed.
    Used for creating `AdminUser`
    """
    try:
        password_hash = get_password_hash(new_admin.password)
        new_admin = await AdminUserORM.create(**new_admin.dict(), hashed_password=password_hash)
        return AdminUser.from_orm(new_admin)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post('/login')
async def login():
    """
    Note: Only `AdminUser` can
    login. to get the Auth Token
    for subsequent API calls.
    """
    pass


@router.post('/create')
async def create_user(admin: AdminUser = Depends(get_current_user)):
    """
    Only `AdminUser` is authorized
    to create `User` regardless of
    level.
    Only `AdminUser` with `Level.ZERO`
    can create another `AdminUser`
    """
    pass


@router.put('/update')
async def update_user():
    """
    Endpoint allows modification of
    `User` information.
    """
    pass


@router.get('/search')
async def search_user():
    """
    Returns a list of matching `User` instance based
    on the provided query.
    """


@router.get('/all')
async def list_customers():
    """
    Returns a list of
    `User`
    """
    pass


@router.get('/admins-all')
async def list_admins():
    """
    Returns a list of `AdminUser`
    Only authorized users can hit
    this endpoint.
    """
    pass
