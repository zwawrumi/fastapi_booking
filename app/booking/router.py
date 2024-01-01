from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from pydantic import TypeAdapter

from app.booking.schemas import SBooking
from app.booking.service import BookingService
from app.exceptions import NotFoundException, RoomFullException
from app.models.models import UserModel
from app.tasks.tasks import send_confirmation_email
from app.user.dependencies import get_current_user

router = APIRouter(
    prefix='/bookings',
    tags=['Booking']
)


@router.get('')
async def get_bookings(user: UserModel = Depends(get_current_user)):
    return await BookingService.find_all(user_id=user.id)


@router.post('')
async def add_booking(
        room_id: int,
        date_from: date = Query(
            ..., description=f'For example, {datetime.now().date()}'
        ),
        date_to: date = Query(
            ..., description=f'For example, {(datetime.now() + timedelta(days=7)).date()}'
        ),
        user: UserModel = Depends(get_current_user)
):
    """Add Booking."""
    booking = await BookingService.add(
        user_id=user.id, room_id=room_id,
        date_from=date_from, date_to=date_to
    )
    adapter = TypeAdapter(SBooking)
    booking_dict = adapter.validate_python(booking).model_dump()
    send_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: UserModel = Depends(get_current_user)):
    booking = await BookingService.delete(user, booking_id)
    if not booking:
        raise NotFoundException
    return booking
