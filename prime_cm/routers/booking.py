from fastapi import APIRouter, status
from prime_cm.models import booking
from datetime import date

from prime_cm.models.user import UserORM

router = APIRouter()


@router.post('/book', status_code=status.HTTP_201_CREATED, response_model=booking.Transaction)
async def create_booking(transaction: booking.Transaction):
    customer = await UserORM.get(**transaction.customer.dict())
    txn, _ = await booking.TransactionORM.get_or_create(customer=customer, at=date.today())
    booked = [await booking.BookingORM.get_or_create(
        transaction=txn,
        paper_size=book.paper_size,
        paper_type=book.paper_type,
        rate=book.rate,
        copies=book.copies
    ) for book in transaction.bookings]
    return booking.Transaction(
        customer=transaction.customer,
        bookings=[book[0] for book in booked],
        at=txn.at
    )
