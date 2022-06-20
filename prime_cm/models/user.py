from pydantic import BaseModel
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
    business_name = Optional[str]
