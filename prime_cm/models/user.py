from pydantic import BaseModel
from sqlalchemy import null
from tortoise.models import Model
from tortoise import fields
import enum
from typing import Optional, List


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
    other_number: Optional[List[OtherNumber]]
    address: Optional[str]
    gender: Optional[Gender]
    religion: Optional[Religion]


class AdminUser(BaseUser):
    """
    The `AdminUser` has access to the
    Prime CM console via
    authentication.
    """
    level: Level


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


class AdminUserORM(Model):
    id = fields.IntField(pk=True, generated=True)
    firstname = fields.CharField(max_length=50, null=True)
    lastname = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=150, null=True)
    phone_number = fields.CharField(max_length=15, null=False)
    addresss = fields.TextField(null=True)
    gender = fields.CharEnumField(enum_type=Gender)
    religion = fields.CharEnumField(enum_type=Religion)
    level = fields.IntEnumField(enum_type=Level)
    hashed_password = fields.CharField(max_length=255, null=False)

    class Meta:
        table = "admins"


class AdminOtherNumberORM(Model):
    admin = fields.ForeignKeyField(
        model_name="models.AdminUserORM", related_name='other_numbers')
    number = fields.CharField(max_length=15)

    class Meta:
        table = "admin_other_numbers"


class UserORM(Model):
    id = fields.IntField(pk=True, generated=True)
    firstname = fields.CharField(max_length=50, null=True)
    lastname = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=150, null=True)
    phone_number = fields.CharField(max_length=15, null=False)
    addresss = fields.TextField(null=True)
    gender = fields.CharEnumField(enum_type=Gender)
    religion = fields.CharEnumField(enum_type=Religion)

    class Meta:
        table = "customers"


class UserOtherNumberORM(Model):
    user = fields.ForeignKeyField(
        model_name="models.UserORM", related_name='other_numbers')
    number = fields.CharField(max_length=15)

    class Meta:
        table = "customers_other_numbers"
