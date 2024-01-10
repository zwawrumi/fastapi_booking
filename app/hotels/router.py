from datetime import date

from fastapi import APIRouter



from app.exceptions import NotFoundException
from app.hotels.schemas import SFreeHotels, SHotels
from app.hotels.service import HotelService


router = APIRouter(prefix='/hotel', tags=['Hotels'])


@router.get("")
async def get_hotels():
    return await HotelService.find_all()


@router.get("/{location}")
async def get_hotels_by_location(
        location: str, date_from: date, date_to: date
) -> list[SFreeHotels]:
    return await HotelService.find_free_by_location(location=location, date_from=date_from, date_to=date_to)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int) -> SHotels:
    hotel = await HotelService.find_one_or_none(id=hotel_id)
    if not hotel:
        raise NotFoundException
    return hotel



