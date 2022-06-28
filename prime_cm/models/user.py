from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import null
from tortoise.models import Model
from tortoise import fields
import enum
from typing import Optional, List
import uuid


class UserType(str, enum.Enum):
    CUSTOMER = 'customer'
    ADMIN = 'admin'


class Level(int, enum.Enum):
    """
    `AdminUser` with `Level.ZERO`
    has Sudo Rights while `AdminUser`
    with `Level.ONE` has limited access.
    """
    ZERO = 0
    ONE = 1


class Gender(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class Religion(str, enum.Enum):
    CHRISTIAN = 'christian'
    MUSLIM = 'muslim'


class OtherNumber(BaseModel):
    """
    Model helps to serializer/deserialize
    other phone numbers the `User`
    has.
    """
    number: str

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    """
    Note: Because of my inablility to 
    predict how likely the Customers `User`
    are going to provide the informations,
    I've marked a lot of field as optional.
    """
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]  # TODO: Use email validator
    # TODO: Make this the unique field for identification of `User`, This field is required.
    phone_number: str
    address: Optional[str]
    gender: Optional[Gender]
    religion: Optional[Religion]


class AdminUser(BaseUser):
    """
    The `AdminUser` has access to the
    Prime CM console via
    authentication.
    """
    id: Optional[int]
    level: Level

    class Config:
        orm_mode = True


class AdminUserCreate(BaseUser):
    level: Level
    password: str


def get_expiration_date() -> datetime:
    # TODO: Provide expiration_date in the future
    return datetime.now()


def generate_token() -> str:
    # TODO: Implement a better token generator
    return str(uuid.uuid4())


class AccessToken(BaseModel):
    admin_id: Optional[int]
    access_token: str = Field(default_factory=generate_token)
    expiration_date: datetime = Field(default_factory=get_expiration_date)

    class Config:
        orm_mode = True


class AdminUserDB(AdminUser):
    hashed_password: str


class User(BaseUser):
    """
    Model should have probably been named
    `CustomerUser` but to avoid verbosity,
    I'm sticking to just `User`. This model
    is the model for Prime customers. ie.
    the Photographer.
    """
    business_name: Optional[str]

    class Config:
        orm_mode = True


class AdminUserORM(Model):
    id = fields.IntField(pk=True, generated=True)
    firstname = fields.CharField(max_length=50, null=True)
    lastname = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=150, null=True)
    phone_number = fields.CharField(max_length=15, null=False)
    addresss = fields.TextField(null=True)
    gender = fields.CharEnumField(enum_type=Gender, null=True)
    religion = fields.CharEnumField(enum_type=Religion, null=True)
    level = fields.IntEnumField(enum_type=Level)
    hashed_password = fields.CharField(max_length=255, null=False)

    class Meta:
        table = "admins"


class AdminOtherNumberORM(Model):
    id = fields.IntField(pk=True, generated=True)
    admin = fields.ForeignKeyField(
        model_name="models.AdminUserORM", related_name='other_numbers', on_delete=fields.CASCADE)
    number = fields.CharField(max_length=15)

    class Meta:
        table = "admin_other_numbers"


class UserORM(Model):
    id = fields.IntField(pk=True, generated=True)
    firstname = fields.CharField(max_length=50, null=True)
    lastname = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=150, null=True)
    phone_number = fields.CharField(max_length=15, null=False)
    address = fields.TextField(null=True)
    gender = fields.CharEnumField(enum_type=Gender, null=True)
    religion = fields.CharEnumField(enum_type=Religion, null=True)
    business_name = fields.CharField(max_length=200, null=True)

    class Meta:
        table = "customers"


class UserOtherNumberORM(Model):
    id = fields.IntField(pk=True, generated=True)
    user = fields.ForeignKeyField(
        model_name="models.UserORM", related_name='other_numbers', on_delete=fields.CASCADE)
    number = fields.CharField(max_length=15)

    class Meta:
        table = "customers_other_numbers"


class AccessTokenORM(Model):
    access_token = fields.CharField(pk=True, max_length=255)
    admin = fields.ForeignKeyField("models.AdminUserORM", null=False)
    expiration_date = fields.DatetimeField(null=False)

    class Meta:
        table = "access_tokens"
