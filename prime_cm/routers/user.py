from tortoise.exceptions import DoesNotExist
from datetime import datetime
from typing import List, Optional, cast
from prime_cm.utils import get_password_hash
from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from prime_cm.models.user import (
    AccessTokenORM,
    AdminUser,
    AdminUserCreate,
    AdminUserORM,
    Gender,
    Religion,
    UserORM,
    User,
)
from prime_cm.utils import authenticate, create_access_token

router = APIRouter(tags=['Users'])


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl='/token'))
) -> AdminUser:
    try:
        access_token: AccessTokenORM = await AccessTokenORM.get(access_token=token).prefetch_related("admin")
        return cast(AdminUser, access_token.admin)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/token", tags=['Admin User'])
async def create_token(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    phone_number = form_data.username
    password = form_data.password
    admin = await authenticate(phone_number, password)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = await create_access_token(admin)
    return {"access_token": token.access_token, "token_type": "bearer"}


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=AdminUser, tags=['Admin User'])
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


@router.post('/login', tags=['Admin User'])
async def login():
    """
    Note: Only `AdminUser` can
    login. to get the Auth Token
    for subsequent API calls.
    """
    pass


@router.post('/create', tags=['Customer User'], status_code=status.HTTP_201_CREATED)
async def create_customer(new_customer: User, admin: AdminUser = Depends(get_current_user)):
    """
    Only `AdminUser` is authorized
    to create `User` regardless of
    level.
    Only `AdminUser` with `Level.ZERO`
    can create another `AdminUser`
    """
    new_user = await UserORM.create(**new_customer.dict())
    return User.from_orm(new_user)


@router.put('/update', tags=['Customer User'], status_code=status.HTTP_200_OK)
async def update_customer(customer: User, admin: AdminUser = Depends(get_current_user)):
    """
    Endpoint allows modification of
    `User` information.
    """
    # Fetch the existing user by phone_number since
    # it is a required field in creating a customer
    # instance.
    user = await UserORM.get(phone_number=customer.phone_number)
    user = await user.update_from_dict(customer.dict())
    return User.from_orm(user)


@router.get('/search', tags=['Customer User'])
async def search_customers(firstname: Optional[str] = None,
                           lastname: Optional[str] = None,
                           email: Optional[str] = None,
                           phone_number: Optional[str] = None,
                           gender: Optional[Gender] = None,
                           religion: Optional[Religion] = None,
                           business_name: Optional[str] = None
                           ):
    """
    Returns a list of matching `User` instance based
    on the provided query.
    """
    users = await UserORM.filter(firstname=firstname,
                                 lastname=lastname,
                                 email=email,
                                 phone_number=phone_number,
                                 gender=gender,
                                 religion=religion,
                                 business_name=business_name
                                 )
    users = [User.from_orm(user) for user in users]
    return users


@router.get('/all', tags=['Customer User'])
async def list_customers(admin: AdminUser = Depends(get_current_user)):
    """
    Returns a list of
    `User`
    """
    # TODO: Paginate the number customers returned
    customers = await UserORM.all()
    customers = [User.from_orm(customer) for customer in customers]
    return customers


@router.get('/admins-all', tags=['Admin User'], response_model=List[AdminUser])
async def list_admins(admin: AdminUser = Depends(get_current_user)):
    """
    Returns a list of `AdminUser`
    Only authorized users can hit
    this endpoint.
    """
    # TODO: Paginate response
    admins = await AdminUserORM.all()
    admins = [AdminUser.from_orm(admin) for admin in admins]
    return admins
