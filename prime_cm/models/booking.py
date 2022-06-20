import enum
from typing import List
from pydantic import BaseModel
from datetime import datetime


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
    paper_type: PaperType
    paper_size: PaperSize
    rate: float
    copies: int
    at: datetime


class Transaction(BaseModel):
    bookings: List[Booking]
    at: datetime
