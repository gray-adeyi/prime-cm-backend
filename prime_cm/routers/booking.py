from fastapi import APIRouter

router = APIRouter()


@router.post('/book')
def create_booking():
