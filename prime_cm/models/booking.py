from decimal import Decimal
import enum
from typing import List
from pydantic import BaseModel
from datetime import datetime, date
from .user import User
from tortoise import fields, models


class PaperType(str, enum.Enum):
    LUSTRE = 'luster'
    GLOSSY = 'glossy'
    CANVAS = 'canvas'


class PaperSize(str, enum.Enum):
    FOUR_BY_SIX = '4X6'
    FIVE_BY_SEVEN = '5X7'
    FIVE_BY_FOURTEEN = '5X14'
    SIX_BY_EIGHT = '6X8'
    EIGHT_BY_TEN = '8X10'


class Booking(BaseModel):
    """
    Models a customer (`User` instance)
    booking.
    """
    paper_type: PaperType = PaperType.LUSTRE
    paper_size: PaperSize = PaperSize.FIVE_BY_SEVEN
    rate: float = 50
    copies: int = 1
    at: datetime


class Transaction(BaseModel):
    customer: User
    bookings: List[Booking]
    at: date

    class Config:
        orm_mode = True


class TransactionORM(models.Model):
    id = fields.IntField(pk=True, generated=True)
    customer = fields.ForeignKeyField(
        'models.UserORM', on_delete='CASCADE', related_name='transactions')
    at = fields.DateField(auto_now_add=True, unique=True)

    class Meta:
        table = 'transactions'


class BookingORM(models.Model):
    id = fields.IntField(pk=True, generated=True)
    transaction = fields.ForeignKeyField(
        'models.TransactionORM', on_delete='CASCADE', related_name='bookings')
    paper_type = fields.CharEnumField(
        enum_type=PaperType, default=PaperType.LUSTRE)
    paper_size = fields.CharEnumField(
        enum_type=PaperSize, default=PaperSize.FIVE_BY_SEVEN)
    rate = fields.DecimalField(
        max_digits=9, decimal_places=2, default=Decimal(50.0))
    copies = fields.IntField()  # can be a positive integer field
    at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'bookings'
